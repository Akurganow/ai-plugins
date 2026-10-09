#!/usr/bin/env python3
"""Measure whether each skill triggers, and whether it improves the answer.

CI runs this after a package release (`.github/workflows/evals.yml`). One
`run` covers one skill, one client and one repeat: positive prompts with the
package, near-miss prompts with it, then positive prompts without it. Jev
grades every positive answer against the skill's rubric. `report` merges the
runs of a release and attaches them to its GitHub Release as `evals.json`. It
files an issue for a metric that regressed against the previous release.

The runner is this repository's own. In Claude Code 2.1.293, `claude plugin
eval` wrote the final reply only as the evidence of an LLM grader (running,
2026-10-08: https://github.com/Akurganow/ai-plugins/actions/runs/37784785554).
That grader runs a judge model of its own. `claude plugin eval` has no
custom-code grader, so Jev could not take the judge's place (documentation:
https://code.claude.com/docs/en/plugin-evals).
`validate` checks that every folder under evals/ has its skill and loads.
`selftest` checks the parsers against the event streams in
tools/evals-fixtures/, and the arithmetic, without calling a model. The comment
above `_selftest_parsers` gives the fixtures' origin.
"""

import argparse
import hashlib
import http.client
import json
import os
import statistics
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
PLUGINS_DIR = REPO_ROOT / "plugins"
EVALS_DIR = REPO_ROOT / "evals"
FIXTURES_DIR = REPO_ROOT / "tools" / "evals-fixtures"
MARKETPLACE = json.loads((REPO_ROOT / ".claude-plugin" / "marketplace.json").read_text())["name"]

CLIENTS = ("claude", "codex", "omp")
REPEATS = 3
MODELS = {
    "claude": "sonnet",
    "codex": "gpt-6-luna",
    "omp": "openrouter/z-ai/glm-5.3-flash",
}
CASES_PER_KIND = 10
METRICS = ("trigger_hit", "false_fire", "compliance", "improvement")

JEV_URL = "https://api.typesafe.ai/v1/systemone"
# Pinned because the `jev-latest` alias moves with each Jev release
# (documentation: https://docs.typesafe.ai/models.md).
JEV_MODEL = "jev-1.13.0"
JEV_RETRY_STATUSES = (429, 529)
JEV_ATTEMPTS = 6

# Each client process sees only its own key. The answers are published in
# evals.json, and an agent with a shell can print its environment.
SECRET_VARS = ("ANTHROPIC_API_KEY", "CODEX_API_KEY", "OPENAI_API_KEY", "OPENROUTER_API_KEY", "TYPESAFE_API_KEY")
CLIENT_KEY = {"claude": "ANTHROPIC_API_KEY", "codex": "CODEX_API_KEY", "omp": "OPENROUTER_API_KEY"}

# `gh ... list` stops at --limit without saying so, so a listing that fills its
# limit is an error.
RELEASE_LIMIT, ISSUE_LIMIT = 200, 500

FINGERPRINT_PREFIX = "<!-- police-fingerprint: "


@dataclass
class Parsed:
    fired: bool
    answer: str | None
    cost_usd: float | None
    tokens: dict | None
    model: str | None
    error: str | None


class Claude:
    name = "claude"

    def __init__(self, package: str, skill: str):
        self.package, self.skill = package, skill

    # Read lets the skill open its reference files. With only Skill allowed,
    # Claude Code 2.1.293 denied the skill's Read call (running, 2026-10-08:
    # https://github.com/Akurganow/ai-plugins/actions/runs/37784785554).
    def command(self, prompt: str, arm: str) -> list[str]:
        return ["claude", "-p", prompt, "--model", MODELS["claude"], "--output-format", "stream-json",
                "--verbose", "--allowedTools", "Skill", "Read"]

    # `claude plugin disable` changes the plugin's state for later sessions, so it
    # runs once between the arms (documentation:
    # https://code.claude.com/docs/en/plugins/cli-reference#plugin-disable).
    def switch_to_without(self) -> None:
        subprocess.run(["claude", "plugin", "disable", f"{self.package}@{MARKETPLACE}"], check=True,
                       env=client_env(self.name))

    # Claude Code 2.1.293 shows a loaded skill as a Skill tool call whose `skill`
    # input holds "<package>:<skill>" (running, 2026-10-08:
    # https://github.com/Akurganow/ai-plugins/actions/runs/37789029106).
    def parse(self, events: list[dict]) -> Parsed:
        fired, answer, cost, model, error = False, None, None, None, None
        for e in events:
            kind = e.get("type")
            if kind == "system" and e.get("subtype") == "init":
                model = e.get("model")
            elif kind == "assistant":
                for block in (e.get("message") or {}).get("content") or []:
                    if (block.get("type") == "tool_use" and block.get("name") == "Skill"
                            and block.get("input", {}).get("skill") == f"{self.package}:{self.skill}"):
                        fired = True
            elif kind == "result":
                answer, cost = e.get("result"), e.get("total_cost_usd")
                if e.get("is_error") or e.get("subtype") != "success":
                    error = f"result {e.get('subtype')}"
        if answer is None and error is None:
            error = "no result event"
        return Parsed(fired, answer, cost, None, model, error)


class Codex:
    name = "codex"

    def __init__(self, package: str, skill: str):
        self.package, self.skill = package, skill

    # On GitHub's ubuntu-latest the read-only sandbox failed every command with
    # "bwrap: loopback: Failed RTM_NEWADDR", so Codex never read SKILL.md
    # (running: Codex 0.161.0, 2026-10-08,
    # https://github.com/Akurganow/ai-plugins/actions/runs/37786134780).
    def command(self, prompt: str, arm: str) -> list[str]:
        cmd = ["codex", "exec", "--json", "--skip-git-repo-check", "--sandbox", "danger-full-access",
               "-m", MODELS["codex"]]
        if arm == "without":
            cmd += ["--disable", "plugins"]
        return cmd + [prompt]

    def switch_to_without(self) -> None:
        pass

    # Codex has no skill item kind (source: ThreadItemDetails in
    # https://github.com/openai/codex/blob/979011409de0a60b52f179721948e65531d26144/codex-rs/exec/src/exec_events.rs#L107-L133).
    # A skill load is a shell read of its SKILL.md in the plugin cache (running:
    # https://github.com/Akurganow/ai-plugins/actions/runs/37786134780).
    # A top-level "error" event also announces each retry, so only "turn.failed"
    # marks a failed turn (source:
    # https://github.com/openai/codex/blob/979011409de0a60b52f179721948e65531d26144/codex-rs/exec/src/event_processor_with_jsonl_output.rs#L447-L457,
    # https://github.com/openai/codex/blob/979011409de0a60b52f179721948e65531d26144/codex-rs/app-server/src/bespoke_event_handling.rs#L1054-L1066).
    # A stream that stops before turn.completed is an interrupted turn, and its last
    # agent_message can be a preamble such as the fixture's first one.
    def parse(self, events: list[dict]) -> Parsed:
        fired, answer, tokens, error, retried = False, None, None, None, None
        completed = False
        skill_path = f"/skills/{self.skill}/SKILL.md"
        cache_path = f"/plugins/cache/{MARKETPLACE}/{self.package}/"
        for e in events:
            kind, item = e.get("type"), e.get("item") or {}
            if kind == "item.completed" and item.get("type") == "command_execution":
                command = item.get("command", "")
                if cache_path in command and skill_path in command:
                    fired = True
            elif kind == "item.completed" and item.get("type") == "agent_message":
                answer = item.get("text")
            elif kind == "turn.completed":
                completed, tokens = True, e.get("usage")
            elif kind == "turn.failed":
                error = json.dumps(e)[:500]
            elif kind == "error":
                retried = e.get("message")
        if answer is None and error is None:
            error = f"no agent_message, last error: {retried}" if retried else "no agent_message"
        elif not completed and error is None:
            error = "no turn.completed"
        return Parsed(fired, answer, None, tokens, MODELS["codex"], error)


class Omp:
    name = "omp"

    def __init__(self, package: str, skill: str):
        self.package, self.skill = package, skill

    # Oh-My-Pi thinks at `high` unless told otherwise (documentation:
    # https://github.com/can1357/oh-my-pi/blob/cde91bb38674d365e8c3916d05d2292273bb8554/docs/settings.md#L495).
    # On three red-flags cases `low` took 116 s against 472 s at `high`, and loaded
    # the skill every time (running, Oh-My-Pi 18.8.6, 2026-10-08:
    # https://github.com/Akurganow/ai-plugins/actions/runs/37860528358).
    def command(self, prompt: str, arm: str) -> list[str]:
        cmd = ["omp", "-p", "--mode", "json", "--no-session", "--no-title", "--auto-approve",
               "--model", MODELS["omp"], "--thinking", "low"]
        if arm == "without":
            cmd.append("--no-skills")
        return cmd + [prompt]

    def switch_to_without(self) -> None:
        pass

    # Oh-My-Pi loads a skill by reading skill://<name>, a file under it, or either
    # with a selector such as ":raw" (documentation:
    # https://github.com/can1357/oh-my-pi/blob/40e9368ef0458fd9073329cdff4174895f91bc6b/docs/skills.md#L182-L183,
    # https://github.com/can1357/oh-my-pi/blob/40e9368ef0458fd9073329cdff4174895f91bc6b/docs/tools/read.md#L33).
    # A failed assistant message can come before a retry that succeeds, so only
    # the last one decides (source:
    # https://github.com/can1357/oh-my-pi/blob/40e9368ef0458fd9073329cdff4174895f91bc6b/packages/coding-agent/src/session/agent-session.ts#L4323-L4324).
    def parse(self, events: list[dict]) -> Parsed:
        fired, answer, cost, model, last = False, None, 0.0, None, None
        base = f"skill://{self.skill}"
        for e in events:
            kind = e.get("type")
            if kind == "tool_execution_start" and e.get("toolName") == "read":
                path = (e.get("args") or {}).get("path", "")
                if path == base or path.startswith((base + "/", base + ":")):
                    fired = True
            elif kind == "message_end" and (e.get("message") or {}).get("role") == "assistant":
                last = e["message"]
                model = last.get("model") or model
                cost += ((last.get("usage") or {}).get("cost") or {}).get("total") or 0.0
                answer = "".join(b.get("text", "") for b in last.get("content") or [] if b.get("type") == "text")
        error = None
        if last and last.get("stopReason") in ("aborted", "error"):
            error = last.get("errorMessage") or last.get("stopReason")
        if not answer and error is None:
            error = "no assistant text"
        return Parsed(fired, answer or None, cost, None, model, error)


ADAPTERS = {"claude": Claude, "codex": Codex, "omp": Omp}


def load_events(text: str) -> list[dict]:
    events = []
    for line in text.splitlines():
        try:
            event = json.loads(line)
        except json.JSONDecodeError:
            continue
        if isinstance(event, dict):
            events.append(event)
    return events


class JevError(Exception):
    pass


# A malformed file fails here, before the first paid session.
def load_cases(skill_dir: Path) -> tuple[dict, dict]:
    import yaml  # Imported here, so `selftest` needs only the standard library.

    cases = yaml.safe_load((skill_dir / "cases.yaml").read_text())
    rubric = yaml.safe_load((skill_dir / "rubric.yaml").read_text())
    if not isinstance(cases, dict):
        raise SystemExit(f"{skill_dir}/cases.yaml: expected a map with positive and near_miss.")
    for kind in ("positive", "near_miss"):
        entries = cases.get(kind)
        if not isinstance(entries, list) or len(entries) != CASES_PER_KIND:
            raise SystemExit(f"{skill_dir}/cases.yaml: {kind} must list exactly {CASES_PER_KIND} entries.")
        if not all(isinstance(c, dict) and isinstance(c.get("id"), str) and isinstance(c.get("prompt"), str)
                   for c in entries):
            raise SystemExit(f"{skill_dir}/cases.yaml: every {kind} entry needs a string id and prompt.")
    ids = [c["id"] for kind in ("positive", "near_miss") for c in cases[kind]]
    if len(ids) != len(set(ids)):
        raise SystemExit(f"{skill_dir}/cases.yaml: case ids repeat.")
    questions = rubric.get("questions") if isinstance(rubric, dict) else None
    if not isinstance(questions, dict) or not questions or not all(isinstance(q, str) for q in questions.values()):
        raise SystemExit(f"{skill_dir}/rubric.yaml: questions must map each id to one statement.")
    return cases, questions


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def client_env(client: str) -> dict:
    env = {k: v for k, v in os.environ.items() if k not in SECRET_VARS}
    key = CLIENT_KEY[client]
    if os.environ.get(key):
        env[key] = os.environ[key]
    return env


# Each session runs in a new empty directory outside the checkout, so the
# repository's own skills under `.agents/skills` stay out of the session. Codex
# loads skills from `.agents/skills` between the working directory and the
# repository root (documentation, read 2026-10-08:
# https://learn.chatgpt.com/docs/build-skills, "Where Codex loads local skills").
# Oh-My-Pi has an `agents` provider for `.agent[s]/skills` with toggles of its own.
# Disabling the Claude, Codex and Pi providers does not turn it off (documentation:
# https://github.com/can1357/oh-my-pi/blob/40e9368ef0458fd9073329cdff4174895f91bc6b/docs/skills.md#L122).
def run_session(adapter, case: dict, kind: str, arm: str) -> dict:
    with tempfile.TemporaryDirectory() as cwd:
        started = time.monotonic()
        proc = subprocess.run(adapter.command(case["prompt"], arm), cwd=cwd, env=client_env(adapter.name),
                              stdin=subprocess.DEVNULL, capture_output=True, text=True)
        duration = round(time.monotonic() - started, 1)
    parsed = adapter.parse(load_events(proc.stdout))
    error = parsed.error
    if proc.returncode != 0:
        error = f"exit {proc.returncode}: {proc.stderr[-500:]}"
    return {"case": case["id"], "kind": kind, "arm": arm, "fired": parsed.fired, "answer": parsed.answer,
            "cost_usd": parsed.cost_usd, "tokens": parsed.tokens, "model": parsed.model,
            "duration_s": duration, "error": error, "nouls": None, "grade_error": None}


def jev_request(body: dict) -> dict:
    data = json.dumps(body).encode()
    headers = {"Authorization": f"Bearer {os.environ['TYPESAFE_API_KEY']}", "Content-Type": "application/json"}
    for attempt in range(JEV_ATTEMPTS):
        request = urllib.request.Request(JEV_URL, data=data, headers=headers, method="POST")
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return json.loads(response.read())
        except urllib.error.HTTPError as e:
            if e.code in JEV_RETRY_STATUSES and attempt < JEV_ATTEMPTS - 1:
                time.sleep(2 ** attempt)
                continue
            try:
                detail = e.read()[:300].decode(errors="replace")
            except (OSError, http.client.HTTPException) as cut:
                detail = f"error body unreadable: {cut!r}"
            raise JevError(f"jev {e.code}: {detail}") from e
        # A refused, reset or cut-off connection is retried like a 429, so one
        # network blip does not cost a graded answer.
        except (OSError, http.client.HTTPException) as e:
            if attempt < JEV_ATTEMPTS - 1:
                time.sleep(2 ** attempt)
                continue
            raise JevError(f"jev unreachable: {e!r}") from e
        except ValueError as e:
            raise JevError(f"jev reply is not JSON: {e}") from e


# The answer is never split, and Jev limits the state plus the longest question
# to 32k tokens (documentation: https://docs.typesafe.ai/models.md, read
# 2026-10-08). A request Jev rejects raises `JevError`, and `run_job` records
# the session as not graded.
def grade(request_text: str, answer: str, questions: dict, send=jev_request) -> dict:
    body = {
        "model": JEV_MODEL,
        "state": {"request": request_text, "answer": answer},
        "questions": {qid: {"type": "noul", "instructions": text} for qid, text in questions.items()},
    }
    reply = send(body)
    try:
        return {qid: float(reply["answers"][qid]["noul"]) for qid in questions}
    except (KeyError, TypeError, ValueError) as e:
        raise JevError(f"jev reply without a noul: {json.dumps(reply)[:300]}") from e


def run_job(adapter, cases: dict, questions: dict, session=run_session, grader=grade) -> list[dict]:
    sessions = [session(adapter, c, kind, "with") for kind in ("positive", "near_miss") for c in cases[kind]]
    adapter.switch_to_without()
    sessions += [session(adapter, c, "positive", "without") for c in cases["positive"]]
    prompts = {c["id"]: c["prompt"] for c in cases["positive"]}
    for s in sessions:
        if s["kind"] != "positive" or s["error"]:
            continue
        try:
            s["nouls"] = grader(prompts[s["case"]], redact(s["answer"]), questions)
        except JevError as e:
            s["grade_error"] = str(e)
    return sessions


def redact(text: str) -> str:
    for var in SECRET_VARS:
        value = os.environ.get(var, "")
        if value:
            text = text.replace(value, "***")
    return text


# A refused client key fails every session, and a refused Jev key fails every
# grade. Either means the run itself broke.
def run_broke(sessions: list[dict]) -> bool:
    gradable = [s for s in sessions if s["kind"] == "positive" and not s["error"]]
    return all(s["error"] for s in sessions) or (bool(gradable) and all(s["grade_error"] for s in gradable))


def metrics(sessions: list[dict]) -> dict:
    done = [s for s in sessions if not s["error"]]
    pos_with = [s for s in done if s["kind"] == "positive" and s["arm"] == "with"]
    pos_without = [s for s in done if s["kind"] == "positive" and s["arm"] == "without"]
    near = [s for s in done if s["kind"] == "near_miss"]

    def share(group):
        return (sum(s["fired"] for s in group) / len(group)) if group else None

    def pooled(group):
        values = [v for s in group if s["nouls"] for v in s["nouls"].values()]
        return statistics.fmean(values) if values else None

    with_mean, without_mean = pooled(pos_with), pooled(pos_without)
    fired_with = [s for s in pos_with if s["fired"]]
    return {
        "trigger_hit": share(pos_with),
        "false_fire": share(near),
        "compliance": pooled(fired_with),
        "improvement": None if with_mean is None or without_mean is None else with_mean - without_mean,
        "counts": {
            "positive_with": len(pos_with),
            "near_miss": len(near),
            "graded_fired": sum(1 for s in fired_with if s["nouls"]),
            "graded_with": sum(1 for s in pos_with if s["nouls"]),
            "graded_without": sum(1 for s in pos_without if s["nouls"]),
        },
    }


# Values compare at the two decimals the summary shows. Means over pools of
# different sizes differ in the last bits, and that is not a regression.
def regressed(metric: str, old: list[float], new: list[float]) -> bool:
    old, new = [round(v, 2) for v in old], [round(v, 2) for v in new]
    if not old or not new:
        return False
    if metric == "false_fire":
        return min(new) > max(old)
    return max(new) < min(old)


def compare(old_runs: list[dict], new_runs: list[dict]) -> dict:
    for field, label in (("cases_sha256", "cases"), ("rubric_sha256", "rubric")):
        if {r[field] for r in old_runs} != {r[field] for r in new_runs}:
            return {"comparable": False, "reason": f"not comparable: {label} changed"}
    found = {}
    for metric in METRICS:
        old = [v for r in old_runs if (v := metrics(r["sessions"])[metric]) is not None]
        new = [v for r in new_runs if (v := metrics(r["sessions"])[metric]) is not None]
        # A range needs all three repeats on both sides.
        if len(old) == REPEATS and len(new) == REPEATS and regressed(metric, old, new):
            found[metric] = (old, new)
    return {"comparable": True, "regressed": found}


# A package without skills/ is valid (Agent Plugins 1.0.0 §6.2) and has nothing to measure.
def skills_of(package: str) -> list[str]:
    skills = PLUGINS_DIR / package / "skills"
    return sorted(p.name for p in skills.iterdir() if p.is_dir()) if skills.is_dir() else []


def has_cases(package: str, skill: str) -> bool:
    return (EVALS_DIR / package / skill).is_dir()


def package_of(tag: str) -> str:
    package, sep, version = tag.rpartition("--v")
    if not sep or not package or not version:
        raise SystemExit(f"{tag}: not a <package>--v<version> tag.")
    if not (PLUGINS_DIR / package).is_dir():
        raise SystemExit(f"{tag}: no package {package} under plugins/.")
    return package


def matrix(tags: list[str]) -> dict:
    include = []
    for tag in dict.fromkeys(tags):
        package = package_of(tag)
        for skill in skills_of(package):
            if not has_cases(package, skill):
                continue
            for client in CLIENTS:
                for repeat in range(1, REPEATS + 1):
                    include.append({"tag": tag, "package": package, "skill": skill, "client": client, "repeat": repeat})
    return {"include": include}


# `load` is a parameter so that the selftest runs without PyYAML.
def check_folder(folder: Path, load=load_cases) -> str | None:
    package, skill = folder.parent.name, folder.name
    if not (PLUGINS_DIR / package / "skills" / skill / "SKILL.md").is_file():
        return f"evals/{package}/{skill}: no plugins/{package}/skills/{skill}/SKILL.md."
    try:
        load(folder)
    except SystemExit as e:
        return str(e.code)
    except Exception as e:  # PyYAML raises its own error type, and one folder must not hide the rest.
        return " ".join(f"evals/{package}/{skill}: {type(e).__name__}: {e}".split())
    return None


def cmd_validate(args) -> int:
    folders = sorted(p for p in EVALS_DIR.glob("*/*") if p.is_dir())
    failures = [message for folder in folders if (message := check_folder(folder))]
    for message in failures:
        print(message)
    if not failures:
        print(f"{len(folders)} evals folders have their skill and load.")
    return 1 if failures else 0


def client_version(client: str) -> str:
    return subprocess.run([client, "--version"], capture_output=True, text=True, env=client_env(client)).stdout.strip()


def cmd_run(args) -> int:
    package = package_of(args.tag)
    skill_dir = EVALS_DIR / package / args.skill
    cases, questions = load_cases(skill_dir)
    adapter = ADAPTERS[args.client](package, args.skill)
    version = client_version(args.client)
    sessions = run_job(adapter, cases, questions)
    record = {
        "tag": args.tag, "package": package, "skill": args.skill, "client": args.client, "repeat": args.repeat,
        "client_version": version, "model": next((s["model"] for s in sessions if s["model"]), None),
        "jev_model": JEV_MODEL, "cases_sha256": sha256(skill_dir / "cases.yaml"),
        "rubric_sha256": sha256(skill_dir / "rubric.yaml"), "sessions": sessions,
    }
    Path(args.out).write_text(redact(json.dumps(record, indent=1)))
    failed = sum(1 for s in sessions if s["error"])
    ungraded = sum(1 for s in sessions if s["grade_error"])
    print(f"{package}/{args.skill} on {args.client}, repeat {args.repeat}: {len(sessions)} sessions, "
          f"{failed} failed, {ungraded} not graded.")
    return 1 if run_broke(sessions) else 0


# stderr goes straight to the job log, so a refused upload or a missing release
# shows its reason.
def gh(*args: str) -> str:
    return subprocess.run(["gh", *args], check=True, stdout=subprocess.PIPE, text=True).stdout


def within_limit(items: list, limit: int, listing: str) -> list:
    if len(items) >= limit:
        raise SystemExit(f"gh {listing} returned {limit} entries, its --limit, so older ones may be missing. "
                         "Raise the limit in tools/evals.py.")
    return items


def version_key(tag: str) -> tuple:
    parts = tag.rpartition("--v")[2].split(".")
    return tuple(int(p) for p in parts) if all(p.isdigit() for p in parts) else ()


def previous_results(package: str, tag: str, workdir: Path) -> dict | None:
    tags = within_limit(json.loads(gh("release", "list", "--limit", str(RELEASE_LIMIT), "--json", "tagName")),
                        RELEASE_LIMIT, "release list")
    older = sorted((t["tagName"] for t in tags if t["tagName"].startswith(f"{package}--v")
                    and version_key(t["tagName"]) and version_key(t["tagName"]) < version_key(tag)),
                   key=version_key, reverse=True)
    if not older:
        return None
    previous = older[0]
    assets = json.loads(gh("release", "view", previous, "--json", "assets"))["assets"]
    if not any(a["name"] == "evals.json" for a in assets):
        return None
    target = workdir / "previous" / previous
    gh("release", "download", previous, "--pattern", "evals.json", "--dir", str(target))
    return json.loads((target / "evals.json").read_text())


def open_fingerprints() -> set[str]:
    issues = within_limit(json.loads(gh("issue", "list", "--label", "police-report", "--state", "open",
                                        "--limit", str(ISSUE_LIMIT), "--json", "body")),
                          ISSUE_LIMIT, "issue list")
    return {line for issue in issues for line in fingerprint_lines(issue["body"] or "")}


def label_exists(name: str) -> bool:
    labels = json.loads(gh("label", "list", "--search", name, "--limit", "100", "--json", "name"))
    return any(label["name"] == name for label in labels)


# A code fence opens with three or more backticks or tildes. Only a fence of the
# same character, at least as long and with no info string, closes it
# (specification: https://spec.commonmark.org/0.31.2/#fenced-code-blocks).
def fence_of(line: str) -> tuple[str, int, str] | None:
    text = line.strip()
    if text[:3] not in ("```", "~~~"):
        return None
    char = text[0]
    length = len(text) - len(text.lstrip(char))
    info = text[length:].strip()
    return None if char == "`" and "`" in info else (char, length, info)


def fingerprint_lines(body: str) -> list[str]:
    lines, open_fence = [], None
    for line in body.splitlines():
        fence = fence_of(line)
        if open_fence:
            if fence and fence[0] == open_fence[0] and fence[1] >= open_fence[1] and not fence[2]:
                open_fence = None
        elif fence:
            open_fence = fence
        elif line.startswith(FINGERPRINT_PREFIX):
            lines.append(line.strip())
    return lines


def fingerprint(package: str, skill: str, client: str) -> str:
    return f"{FINGERPRINT_PREFIX}evals {package}/{skill}@{client} -->"


def span(values: list[float]) -> str:
    return f"{min(values):.2f}–{max(values):.2f}" if values else "–"


def covers(values: list[float]) -> str:
    return f"{len(values)} of {REPEATS} repeats"


METRIC_COUNTS = {
    "trigger_hit": ("positive_with",),
    "false_fire": ("near_miss",),
    "compliance": ("graded_fired",),
    "improvement": ("graded_with", "graded_without"),
}


def counted(runs: list[dict], metric: str) -> str:
    parts = []
    for field in METRIC_COUNTS[metric]:
        counts = [metrics(r["sessions"])["counts"][field] for r in runs]
        parts.append(f"{min(counts)}" if min(counts) == max(counts) else f"{min(counts)}–{max(counts)}")
    return "/".join(parts)


def issue_body(package, skill, client, old_tag, new_tag, found, old_runs, new_runs, run_url, repo) -> str:
    rows = "\n".join(f"| `{m}` | {span(old)} ({covers(old)}) | {span(new)} ({covers(new)}) |"
                     for m, (old, new) in found.items())
    asset = "https://github.com/{}/releases/download/{}/evals.json"
    return (
        f"{fingerprint(package, skill, client)}\n\n"
        f"`{package}/{skill}` on {client} regressed between `{old_tag}` and `{new_tag}`. "
        "Each range spans the repeats of one release, and the two ranges do not overlap.\n\n"
        f"| Metric | `{old_tag}` | `{new_tag}` |\n| :-- | :-- | :-- |\n{rows}\n\n"
        f"Client version: {old_runs[0]['client_version']} → {new_runs[0]['client_version']}. "
        f"Model: {old_runs[0]['model']} → {new_runs[0]['model']}.\n\n"
        f"Run: {run_url}. Results: {asset.format(repo, old_tag)} and {asset.format(repo, new_tag)}.\n"
    )


def file_issue(title: str, body: str) -> None:
    gh("issue", "create", "--title", title, "--body", body, "--label", "police-report")


def cmd_report(args) -> int:
    records = [json.loads(p.read_text()) for p in Path(args.runs).rglob("*.json")]
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    run_url = f"{os.environ.get('GITHUB_SERVER_URL', 'https://github.com')}/{repo}/actions/runs/{os.environ.get('GITHUB_RUN_ID', '')}"
    summary = ["# Behavioural evals", "",
               "Each cell is the range over the repeats that gave a figure, so a repeat without one drops out. "
               "n is the sessions or graded answers behind it, "
               "and for improvement the graded answers with and without the package.", ""]
    seen = open_fingerprints()
    can_file = label_exists("police-report")
    with tempfile.TemporaryDirectory() as tmp:
        workdir = Path(tmp)
        for tag in dict.fromkeys(args.tags.split()):
            package = package_of(tag)
            runs = [r for r in records if r["tag"] == tag]
            no_cases = [s for s in skills_of(package) if not has_cases(package, s)]
            if not runs:
                # A failed manual run must not replace a release's complete evals.json.
                summary += [f"## `{tag}`", "", "No run reported, so nothing was uploaded.", ""]
                if no_cases:
                    summary += ["No cases: " + ", ".join(no_cases), ""]
                continue
            # gh names the asset after the file. A "#" suffix sets only a display
            # label (documentation: https://cli.github.com/manual/gh_release_upload).
            results = workdir / tag / "evals.json"
            results.parent.mkdir()
            results.write_text(json.dumps({"tag": tag, "package": package, "no_cases": no_cases, "runs": runs}, indent=1))
            gh("release", "upload", tag, str(results), "--clobber")
            previous = previous_results(package, tag, workdir)
            summary += report_tag(tag, package, runs, no_cases, previous, seen, run_url, repo, can_file)
    Path(os.environ.get("GITHUB_STEP_SUMMARY", "/dev/stdout")).write_text("\n".join(summary) + "\n")
    return 0


def report_tag(tag, package, runs, no_cases, previous, seen, run_url, repo, can_file, file=file_issue) -> list[str]:
    lines = [f"## `{tag}`", "", "| Skill | Client | " + " | ".join(f"`{m}`" for m in METRICS) + " | Cost | Compared |",
             "| :-- | :-- | " + "".join(":-- | " for _ in METRICS) + ":-- | :-- |"]
    excluded = []
    for skill in sorted({r["skill"] for r in runs}):
        for client in CLIENTS:
            group = [r for r in runs if r["skill"] == skill and r["client"] == client]
            if not group:
                continue
            values = {m: [v for r in group if (v := metrics(r["sessions"])[m]) is not None] for m in METRICS}
            sessions = [s for r in group for s in r["sessions"]]
            cost = sum(s["cost_usd"] or 0 for s in sessions)
            tokens = sum((s["tokens"] or {}).get("input_tokens", 0) + (s["tokens"] or {}).get("output_tokens", 0)
                         for s in sessions)
            excluded += [f"- {skill} on {client}, repeat {r['repeat']}, case `{s['case']}` ({s['arm']}): "
                         + " ".join((s["error"] or s["grade_error"]).split())[:300]
                         for r in group for s in r["sessions"] if s["error"] or s["grade_error"]]
            old = [r for r in (previous or {}).get("runs", []) if r["skill"] == skill and r["client"] == client]
            if not old:
                status = "no previous results"
            else:
                outcome = compare(old, group)
                if not outcome["comparable"]:
                    status = outcome["reason"]
                elif outcome["regressed"]:
                    status = "regressed: " + ", ".join(outcome["regressed"])
                    mark = fingerprint(package, skill, client)
                    if not can_file:
                        status += " (no issue: the label police-report is not on the label list)"
                    elif mark not in seen:
                        file(f"evals: {package}/{skill} regressed on {client} in {tag}",
                             issue_body(package, skill, client, previous["tag"], tag, outcome["regressed"],
                                        old, group, run_url, repo))
                        seen.add(mark)
                else:
                    status = "no regression"
            spent = f"${cost:.2f}" if client != "codex" else f"{tokens} tokens"
            cells = " | ".join(f"{span(values[m])} (n={counted(group, m)}, {covers(values[m])})" for m in METRICS)
            lines.append(f"| {skill} | {client} | {cells} | {spent} | {status} |")
    lines.append("")
    if no_cases:
        lines += ["No cases: " + ", ".join(no_cases), ""]
    if excluded:
        lines += ["Excluded:", "", *excluded, ""]
    return lines


# The fixtures are event streams trimmed from runs on GitHub's ubuntu-latest on
# 2026-10-08: Claude Code 2.1.293 and Oh-My-Pi 18.8.4 in
# https://github.com/Akurganow/ai-plugins/actions/runs/37789029106, and Codex
# 0.161.0 in https://github.com/Akurganow/ai-plugins/actions/runs/37786134780.
def _selftest_parsers() -> None:
    def events(name):
        return load_events((FIXTURES_DIR / f"{name}.jsonl").read_text())

    claude = Claude("design-review", "red-flags").parse(events("claude"))
    assert claude.fired and claude.error is None, claude
    assert claude.model == "claude-sonnet-5-5" and claude.cost_usd == 0.1016514, claude
    assert claude.answer.startswith("**Short answer:** the abstraction is wrong."), claude.answer
    assert not Claude("design-review", "ariz").parse(events("claude")).fired

    codex = Codex("design-review", "red-flags").parse(events("codex"))
    assert codex.fired and codex.error is None, codex
    assert codex.answer.startswith("## Review"), codex.answer
    assert codex.tokens["input_tokens"] == 141929, codex.tokens
    assert not Codex("triz", "red-flags").parse(events("codex")).fired
    retry = {"type": "error", "message": "Reconnecting... 1/5"}
    assert Codex("design-review", "red-flags").parse([retry] + events("codex")).error is None
    failed = {"type": "turn.failed", "error": {"message": "quota exceeded"}}
    assert "quota exceeded" in Codex("design-review", "red-flags").parse(events("codex") + [failed]).error
    only_retry = Codex("design-review", "red-flags").parse([{"type": "turn.started"}, retry])
    assert only_retry.error == "no agent_message, last error: Reconnecting... 1/5", only_retry
    interrupted = Codex("design-review", "red-flags").parse(events("codex")[:-1])
    assert interrupted.error == "no turn.completed" and interrupted.answer, interrupted

    omp = Omp("design-review", "red-flags").parse(events("omp"))
    assert omp.fired and omp.error is None, omp
    assert omp.model == "z-ai/glm-5.3-flash" and omp.answer.startswith("Review per the red-flags skill"), omp
    assert abs(omp.cost_usd - 0.00813) < 0.00001, omp.cost_usd
    assert not Omp("design-review", "red").parse(events("omp")).fired
    broken = {"type": "message_end", "message": {"role": "assistant", "content": None, "stopReason": "error",
                                                 "errorMessage": "429 rate limited"}}
    assert Omp("design-review", "red-flags").parse([broken] + events("omp")).error is None
    assert Omp("design-review", "red-flags").parse(events("omp") + [broken]).error == "429 rate limited"

    assert Codex("p", "s").command("q", "without")[-3:] == ["--disable", "plugins", "q"]
    assert Omp("p", "s").command("q", "without")[-2:] == ["--no-skills", "q"]


def _session(case, kind, arm, fired, nouls=None, error=None) -> dict:
    return {"case": case, "kind": kind, "arm": arm, "fired": fired, "nouls": nouls, "error": error,
            "grade_error": None}


def _expect_error(call, *needles: str) -> None:
    try:
        call()
    except (SystemExit, JevError) as e:
        assert all(n in str(e) for n in needles), e
    else:
        raise AssertionError(f"expected an error naming {needles}")


def _selftest_core() -> None:
    assert regressed("trigger_hit", [0.8, 0.9, 0.9], [0.5, 0.6, 0.7])
    assert not regressed("trigger_hit", [0.8, 0.9, 0.9], [0.7, 0.8, 0.9])
    assert regressed("false_fire", [0.0, 0.1, 0.1], [0.3, 0.4, 0.4])
    assert not regressed("compliance", [], [0.1])
    assert not regressed("compliance", [0.99] * 3, [statistics.fmean([0.99] * 6)] * 3)

    sample = [
        _session("p1", "positive", "with", True, {"a": 1.0, "b": 0.5}),
        _session("p2", "positive", "with", False, {"a": 0.5, "b": 0.5}),
        _session("p3", "positive", "with", False, error="exit 1"),
        _session("n1", "near_miss", "with", True),
        _session("n2", "near_miss", "with", False),
        _session("p1", "positive", "without", False, {"a": 0.0, "b": 0.5}),
    ]
    got = metrics(sample)
    assert got["trigger_hit"] == 0.5 and got["counts"]["positive_with"] == 2, got
    assert got["false_fire"] == 0.5 and got["compliance"] == 0.75, got
    assert got["improvement"] == 0.625 - 0.25, got

    old = [{"cases_sha256": "a", "rubric_sha256": "r", "sessions": sample}]
    assert compare(old, [{"cases_sha256": "b", "rubric_sha256": "r", "sessions": sample}]) == {
        "comparable": False, "reason": "not comparable: cases changed"}
    assert compare(old, [{"cases_sha256": "a", "rubric_sha256": "s", "sessions": sample}]) == {
        "comparable": False, "reason": "not comparable: rubric changed"}
    assert compare(old, old) == {"comparable": True, "regressed": {}}

    def runs(sessions, count=REPEATS):
        return [{"cases_sha256": "a", "rubric_sha256": "r", "sessions": sessions}] * count

    hit, miss = [_session("p", "positive", "with", True)], [_session("p", "positive", "with", False)]
    assert list(compare(runs(hit), runs(miss))["regressed"]) == ["trigger_hit"]
    assert compare(runs(hit), runs(miss, 2))["regressed"] == {}

    os.environ.update({"TYPESAFE_API_KEY": "selftest-secret-value", "ANTHROPIC_API_KEY": "a-key",
                       "OPENROUTER_API_KEY": "o-key"})
    env = client_env("omp")
    assert env.get("OPENROUTER_API_KEY") == "o-key", env.get("OPENROUTER_API_KEY")
    assert "ANTHROPIC_API_KEY" not in env and "TYPESAFE_API_KEY" not in env
    assert redact('{"answer": "key selftest-secret-value"}') == '{"answer": "key ***"}'

    spawned, real_run = [], subprocess.run
    subprocess.run = lambda cmd, **kw: spawned.append(kw["env"]) or subprocess.CompletedProcess(cmd, 0, stdout="1.0\n")
    try:
        Claude("p", "s").switch_to_without()
        assert client_version("claude") == "1.0"
    finally:
        subprocess.run = real_run
    assert len(spawned) == 2 and all("TYPESAFE_API_KEY" not in e and "ANTHROPIC_API_KEY" in e for e in spawned), spawned

    class Reply:
        def __enter__(self):
            return self

        def __exit__(self, *exc):
            return False

        def read(self):
            return b'{"answers": {"q": {"noul": 0.5}}}'

    opened = []

    def flaky_open(request, timeout):
        opened.append(request.full_url)
        if len(opened) == 1:
            raise ConnectionResetError("reset by peer")
        return Reply()

    def closed_open(request, timeout):
        raise http.client.RemoteDisconnected("closed without a reply")

    class CutBody:
        def read(self, *size):
            raise ConnectionResetError("reset while reading the error body")

        def close(self):
            pass

    def cut_open(request, timeout):
        raise urllib.error.HTTPError(request.full_url, 400, "Bad Request", {}, CutBody())

    real_open, real_sleep = urllib.request.urlopen, time.sleep
    urllib.request.urlopen, time.sleep = flaky_open, lambda seconds: None
    try:
        assert jev_request({"q": 1}) == {"answers": {"q": {"noul": 0.5}}} and len(opened) == 2, opened
        urllib.request.urlopen = closed_open
        try:
            jev_request({"q": 1})
        except JevError as e:
            assert "unreachable" in str(e), e
        else:
            raise AssertionError("a connection closed on every attempt must raise JevError")
        urllib.request.urlopen = cut_open
        _expect_error(lambda: jev_request({"q": 1}), "jev 400", "unreadable")
    finally:
        urllib.request.urlopen, time.sleep = real_open, real_sleep

    class Fake:
        name = "fake"

        def __init__(self):
            self.order = []

        def switch_to_without(self):
            self.order.append("switch")

    fake = Fake()
    cases = {"positive": [{"id": "p", "prompt": "P"}], "near_miss": [{"id": "n", "prompt": "N"}]}

    def fake_session(adapter, case, kind, arm):
        adapter.order.append(f"{case['id']}:{arm}")
        return _session(case["id"], kind, arm, arm == "with") | {"answer": "leaked selftest-secret-value"}

    seen = []
    graded = run_job(fake, cases, {"q": "Q"}, session=fake_session,
                     grader=lambda r, a, q: seen.append(a) or {"q": 1.0})
    assert fake.order == ["p:with", "n:with", "switch", "p:without"], fake.order
    assert [s["nouls"] for s in graded] == [{"q": 1.0}, None, {"q": 1.0}], graded
    assert seen == ["leaked ***", "leaked ***"], seen
    assert not run_broke(graded)

    def broken_session(adapter, case, kind, arm):
        return _session(case["id"], kind, arm, True, error="exit 1" if arm == "without" else None) | {"answer": "A"}

    def refusing(request_text, answer, questions):
        raise JevError("jev 401: invalid key")

    refused = run_job(Fake(), cases, {"q": "Q"}, session=broken_session, grader=refusing)
    assert [s["grade_error"] for s in refused] == ["jev 401: invalid key", None, None], refused
    assert run_broke(refused)
    assert run_broke([_session("p", "positive", "with", False, error="exit 1")])

    sent = {}
    grade("R", "A", {"q": "Q?"}, send=lambda body: sent.update(body) or {"answers": {"q": {"noul": 0.9}}})
    assert sent["model"] == JEV_MODEL and sent["state"] == {"request": "R", "answer": "A"}, sent
    assert sent["questions"] == {"q": {"type": "noul", "instructions": "Q?"}}, sent
    try:
        grade("R", "A", {"q": "Q?"}, send=lambda body: {"answers": {"q": {"error": "state too long"}}})
    except JevError as e:
        assert "without a noul" in str(e), e
    else:
        raise AssertionError("a reply without a noul must raise JevError")


def _selftest_publish() -> None:
    body = "text\n```\n" + fingerprint("p", "s", "c") + "\n```\n~~~\n" + fingerprint("p", "s", "e") + "\n~~~\n"
    body += fingerprint("p", "s", "d") + "\n"
    assert fingerprint_lines(body) == [fingerprint("p", "s", "d")], fingerprint_lines(body)
    mark = {name: fingerprint("p", "s", name) for name in "fghi"}
    nested = (f"```\n~~~\n{mark['f']}\n```\n````\n```\n{mark['g']}\n````\n"
              f"```\n```python\n{mark['i']}\n```\n{mark['h']}\n")
    assert fingerprint_lines(nested) == [mark["h"]], fingerprint_lines(nested)
    assert package_of("triz--v0.2.0") == "triz"
    for bad in ("howp-v0.3.12", "nosuch--v1.0.0"):
        try:
            package_of(bad)
        except SystemExit:
            pass
        else:
            raise AssertionError(f"{bad} must be rejected")
    assert version_key("triz--v0.10.0") > version_key("triz--v0.9.1")
    assert span([0.5, 0.25]) == "0.25–0.50" and span([]) == "–"

    def run(repeat, fired, version, extra=()):
        sessions = [_session("p", "positive", "with", fired) | {"cost_usd": 0.1, "tokens": None}, *extra]
        return {"tag": "t", "skill": "s", "client": "claude", "repeat": repeat, "client_version": version,
                "model": "m", "cases_sha256": "a", "rubric_sha256": "r", "sessions": sessions}

    failed = _session("q", "positive", "with", False, error="exit 1: line one\n# not a heading") | {
        "cost_usd": None, "tokens": None}
    previous = {"tag": "p--v1.0.0", "runs": [run(r, True, "1.0") for r in (1, 2, 3)]}
    current = [run(1, False, "2.0", [failed]), run(2, False, "2.0"), run(3, False, "2.0")]
    filed, seen = [], set()

    def report(runs, can_file, marks):
        return report_tag("p--v1.1.0", "p", runs, ["other"], previous, marks, "RUN", "o/r", can_file,
                          file=lambda title, text: filed.append((title, text)))

    lines = report(current, True, seen)
    assert len(filed) == 1 and fingerprint("p", "s", "claude") in filed[0][1], filed
    assert "Client version: 1.0 → 2.0" in filed[0][1], filed[0][1]
    row = next(line for line in lines if line.startswith("| s | claude |"))
    assert "regressed: trigger_hit" in row and "0.00–0.00 (n=1, 3 of 3 repeats)" in row, row
    assert "| `trigger_hit` | 1.00–1.00 (3 of 3 repeats) | 0.00–0.00 (3 of 3 repeats) |" in filed[0][1], filed[0][1]
    dropped = [current[0], current[1], run(3, False, "2.0") | {"sessions": [failed]}]
    row = next(line for line in report(dropped, True, set()) if line.startswith("| s | claude |"))
    assert "0.00–0.00 (n=0–1, 2 of 3 repeats)" in row and len(filed) == 1, row
    assert "No cases: other" in lines
    assert "- s on claude, repeat 1, case `q` (with): exit 1: line one # not a heading" in lines, lines
    report(current, True, seen)
    assert len(filed) == 1, "a fingerprint already open must not be filed twice"
    lines = report([dict(r, cases_sha256="b") for r in current], True, set())
    assert len(filed) == 1 and any("not comparable: cases changed" in line for line in lines), lines
    lines = report(current, False, set())
    assert len(filed) == 1 and any("not on the label list" in line for line in lines), lines


def _selftest_gh() -> None:
    global gh, PLUGINS_DIR
    calls, replies = [], {}

    def fake(*args):
        calls.append(args)
        return replies.get(" ".join(args[:2]), "[]")

    real_gh, gh = gh, fake
    try:
        with tempfile.TemporaryDirectory() as tmp:
            workdir = Path(tmp)
            runs_dir = workdir / "runs"
            runs_dir.mkdir()
            record = {"tag": "triz--v0.3.0", "skill": "ariz", "client": "claude", "repeat": 1, "client_version": "1",
                      "model": "m", "cases_sha256": "a", "rubric_sha256": "r",
                      "sessions": [_session("p", "positive", "with", True) | {"cost_usd": 0.1, "tokens": None}]}
            (runs_dir / "run.json").write_text(json.dumps(record))
            os.environ["GITHUB_STEP_SUMMARY"] = str(workdir / "summary.md")
            assert cmd_report(argparse.Namespace(tags="triz--v0.2.0 triz--v0.3.0", runs=str(runs_dir))) == 0
            uploads = [c[2] for c in calls if c[:2] == ("release", "upload")]
            assert uploads == ["triz--v0.3.0"], "a tag with no runs must not replace its evals.json"
            summary = (workdir / "summary.md").read_text()
            assert "## `triz--v0.2.0`\n\nNo run reported, so nothing was uploaded." in summary, summary

            real_dir, PLUGINS_DIR = PLUGINS_DIR, workdir / "plugins"
            (PLUGINS_DIR / "nocases" / "skills" / "s").mkdir(parents=True)
            try:
                cmd_report(argparse.Namespace(tags="nocases--v1.0.0", runs=str(runs_dir)))
            finally:
                PLUGINS_DIR = real_dir
            summary = (workdir / "summary.md").read_text()
            assert "No run reported, so nothing was uploaded.\n\nNo cases: s" in summary, summary

            replies["release view"] = '{"assets": []}'
            replies["release list"] = json.dumps([{"tagName": f"p--v0.0.{i}"} for i in range(RELEASE_LIMIT - 1)])
            assert previous_results("p", "p--v1.0.0", workdir) is None
            replies["release list"] = json.dumps([{"tagName": f"p--v0.0.{i}"} for i in range(RELEASE_LIMIT)])
            _expect_error(lambda: previous_results("p", "p--v1.0.0", workdir), "release list", str(RELEASE_LIMIT))
            replies["issue list"] = json.dumps([{"body": ""}] * (ISSUE_LIMIT - 1))
            assert open_fingerprints() == set()
            replies["issue list"] = json.dumps([{"body": ""}] * ISSUE_LIMIT)
            _expect_error(open_fingerprints, "issue list", str(ISSUE_LIMIT))
    finally:
        gh = real_gh


def _selftest_folders() -> None:
    global PLUGINS_DIR
    real_dir = PLUGINS_DIR
    with tempfile.TemporaryDirectory() as tmp:
        PLUGINS_DIR = Path(tmp)
        try:
            (PLUGINS_DIR / "bare").mkdir()
            (PLUGINS_DIR / "p" / "skills" / "s").mkdir(parents=True)
            (PLUGINS_DIR / "p" / "skills" / "s" / "SKILL.md").write_text("")
            assert package_of("bare--v1.0.0") == "bare" and skills_of("bare") == []
            assert matrix(["bare--v1.0.0"]) == {"include": []}
            _expect_error(lambda: package_of("nosuch--v1.0.0"), "nosuch")
            loaded = []
            assert check_folder(Path("evals/p/s"), load=loaded.append) is None and loaded == [Path("evals/p/s")]
            loaded.clear()
            assert check_folder(Path("evals/p/gone"), load=loaded.append) == (
                "evals/p/gone: no plugins/p/skills/gone/SKILL.md.") and not loaded

            def refuse(folder):
                raise SystemExit("evals/p/s/cases.yaml: case ids repeat.")

            def corrupt(folder):
                raise ValueError("expected the node content,\n  found '<stream end>'")

            assert check_folder(Path("evals/p/s"), load=refuse) == "evals/p/s/cases.yaml: case ids repeat."
            assert check_folder(Path("evals/p/s"), load=corrupt) == (
                "evals/p/s: ValueError: expected the node content, found '<stream end>'")
        finally:
            PLUGINS_DIR = real_dir


def selftest() -> int:
    _selftest_parsers()
    _selftest_core()
    _selftest_publish()
    _selftest_gh()
    _selftest_folders()
    print("selftest passed")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = parser.add_subparsers(dest="command", required=True)
    m = sub.add_parser("matrix", help="print the job matrix for some release tags")
    m.add_argument("--tags", required=True)
    r = sub.add_parser("run", help="run one skill on one client, one repeat")
    for name in ("--tag", "--skill", "--out"):
        r.add_argument(name, required=True)
    r.add_argument("--client", required=True, choices=CLIENTS)
    r.add_argument("--repeat", required=True, type=int)
    p = sub.add_parser("report", help="publish the runs of some release tags")
    p.add_argument("--tags", required=True)
    p.add_argument("--runs", required=True)
    sub.add_parser("validate", help="check that every evals folder has its skill and loads")
    sub.add_parser("selftest", help="check the parsers and the arithmetic without a model")
    args = parser.parse_args()
    if args.command == "matrix":
        result = matrix(args.tags.split())
        print(json.dumps(result))
        return 0
    if args.command == "run":
        return cmd_run(args)
    if args.command == "report":
        return cmd_report(args)
    if args.command == "validate":
        return cmd_validate(args)
    return selftest()


if __name__ == "__main__":
    sys.exit(main())
