# prose-discipline Implementation Plan (cluster 03)

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `plugins/prose-discipline` deliver one rules file to every session of Claude Code, Codex, Oh-My-Pi and Hermes by each client's documented always-on route, and bring the package to the shared manifest, skill and README norms.

**Architecture:** `rules/prose-discipline.md` stays the single source. Claude Code and Codex run `hooks/print-rules.sh` from one shell-form `hooks/hooks.json`. Oh-My-Pi reads the rules file itself. Hermes gets the rules through the renamed `house-style` skill, whose body carries them in a region that `tools/regenerate.sh` (plan 02) fills. Three runtime spikes on the owner's installed clients run first, against a throwaway fixture, before any file in the tree changes.

**Tech Stack:** POSIX `sh` and `awk` (the hook), JSON (`plugin.json`, `hooks.json`), Markdown, `jq`, `tools/regenerate.sh` and `tools/check-conformance.py` (plan 02), `claude plugin validate`, `hermes plugins validate`, `sqlite3` (spike 4 only).

## Global Constraints

Copied from spec `../specs/2026-09-24-marketplace-quality-design.md` (§4.1, §5.1, §5.4, §5.5, §8, §9, §10) and from `2026-09-25-00-conventions.md`. Every task's requirements include this section.

- Files this plan may touch: `plugins/prose-discipline/**`, and the three spike records under `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/`. It never edits `tools/`, `tools/schemas/`, root files or another package.
- "Single source of the core rules: `plugins/prose-discipline/rules/prose-discipline.md`." Every other carrier reads it at run time or is generated from it.
- "The rules file stays under 8,000 characters, and CI checks the bound." The CI step is plan 07's; the bound is stated in Task 9.
- `hooks/hooks.json`: "shell form only, no `args`, no `additionalContextLimit`, top-level keys `description` and `hooks` only. `SessionStart` matcher `startup|resume|clear|compact|fork`, command `sh "${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh"`. `SubagentStart` (no matcher), command `sh "${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh" --json`."
- `hooks/print-rules.sh`: "POSIX sh, `sed` and `awk` only. Without a flag it prints the rules body (front matter stripped) as plain text starting with the H1. With `--json` it prints one JSON object `{"hookSpecificOutput":{"hookEventName":"SubagentStart","additionalContext":"<escaped body>"}}`. Any failure exits 0 with nothing on stdout and one line on stderr. `hooks/session-rules.sh` is deleted." No `node`.
- Closed by the owner (§8): no blocking hook, no per-turn reminder, no TTSR rule files, no Python and no native Hermes plugin.
- Manifest: `description` one sentence, at most 250 characters; `keywords` without `agent-skills`; `extensions["io.github.akurganow.ai-plugins"].category` = `Productivity`; `extensions["com.openai"].hooks = "./hooks/hooks.json"`; `components`, `components_note` and `interface` deleted; nothing else under `extensions`. `version` is not edited by hand.
- Plan 06 consumes the description as "one sentence of at most 25 words".
- Skill: directory and front-matter `name` `house-style`, renamed with `git mv`; `description` in imperative voice, key use case first, "Use when …", at most 1024 characters; `license: MIT`. "Every reference is named from SKILL.md by relative path with a 'read when' condition."
- Regions: `rules` in `skills/house-style/SKILL.md`; `description`, `install` and `hermes-auto-load` in the package `README.md`. Markers are two whole lines, `<!-- NAME:start -->` and `<!-- NAME:end -->`, written next to each other; the generator fills them (plan 02 contract).
- Hermes qualified name: `agent-plugin-prose-discipline-cf518319:house-style` (`printf %s prose-discipline | shasum -a 256 | cut -c1-8` prints `cf518319`).
- README: the eight sections of §5.1 in order: H1 with description, Install, Usage, What's inside, Requirements and network, Boundaries, License, Help.
- Prose: every sentence written into the repository follows `plugins/prose-discipline/rules/prose-discipline.md`; at most 25 words; no maintainer diary. Every sentence about a client cites its documentation or source by link, with the kind named; a source link is a commit permalink.
- §10 acceptance: no file under `plugins/` contains "not verified", "has been installed", "was installed", "verified on", or a date-stamped verification claim.
- Commits: conventional, one per task; body sentences of at most 25 words; last line `Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`. Stage paths explicitly, never `git add -A`.
- Nothing in CI calls a model. The spikes call a model on the owner's installed clients, with the cheapest model available; the owner accepted that cost (spec §9).

---

## Interfaces with other plans

**Consumed from plan 02** (`2026-09-25-02-tooling.md`, "Contract for plans 03–07"):

- `tools/regenerate.sh`, no arguments, exit 0 on success. A file without region markers is skipped, so running it between tasks is safe.
- It fills `rules` in `plugins/prose-discipline/skills/house-style/SKILL.md` with the rules file minus its leading `---` … `---` block, trimmed of blank lines at both ends, with one blank line inside each marker.
- It fills `description`, `install` and `hermes-auto-load` in `plugins/prose-discipline/README.md`. The Hermes region is a fenced `yaml` block ending in the line `    - agent-plugin-prose-discipline-cf518319:house-style`.
- It copies `LICENSE` and `plugin.json` to `plugins/prose-discipline/LICENSE` and `plugins/prose-discipline/.claude-plugin/plugin.json`, replacing a symlink.
- It runs `npx --yes doctoc@2.2.1 --github --notitle` over references longer than 100 lines. Here that is `references/examples.md` (126 lines).
- `tools/check-conformance.py` checks that the vendor manifest is a byte-identical regular file.

**Requested from plan 02** (one line, not yet in its script): also fill `hermes-auto-load` in the skill, so the skill's first lines can show the exact `config.yaml` lines (spec §5.5, Hermes row). The line to add after the README call in step 6:

```bash
replace_region plugins/prose-discipline/skills/house-style/SKILL.md hermes-auto-load "$WORK/auto-load.md"
```

Task 5 detects whether the line landed and picks Block C1 (with the region) or Block C2 (pointing at the README). A hand-written qualified name in the skill is not an option: it would be a hand-kept copy of a computed value (spec §2).

**Produced for plan 06:** the manifest `description` (23 words, Block F); the skill path `plugins/prose-discipline/skills/house-style/SKILL.md`; the hooks in `plugins/prose-discipline/hooks/`.

**Produced for plan 07:** the skill name `house-style` for the integration matrix; the size bound in Task 9 for the CI step; the three spike records.

**Produced for plan 08:** the spike records, whose client facts move into `docs/` before `docs/superpowers/` is deleted.

---

## File map

| Path | Change | Responsibility |
| :-- | :-- | :-- |
| `plugins/prose-discipline/plugin.json` | rewrite (Block F) | the manifest |
| `plugins/prose-discipline/.claude-plugin/plugin.json` | generated | copy of the manifest |
| `plugins/prose-discipline/rules/prose-discipline.md` | rewrite (Block D) | the single source of the core rules |
| `plugins/prose-discipline/hooks/hooks.json` | rewrite (Block A) | the two hook registrations |
| `plugins/prose-discipline/hooks/print-rules.sh` | create (Block B) | prints the rules body, plain or as hook JSON |
| `plugins/prose-discipline/hooks/session-rules.sh` | delete | replaced by `print-rules.sh`, and its `node` dependency goes with it |
| `plugins/prose-discipline/skills/prose-discipline/` | `git mv` to `skills/house-style/` | the skill directory |
| `plugins/prose-discipline/skills/house-style/SKILL.md` | rewrite (Block C1 or C2) | Hermes note, generated rules, procedure, reference routing |
| `plugins/prose-discipline/skills/house-style/references/examples.md` | generated TOC | doctoc |
| `plugins/prose-discipline/README.md` | rewrite (Block E) | the package README |
| `plugins/prose-discipline/LICENSE` | generated | copy of the root LICENSE |
| `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-1-claude-code.md` | create | spike 1 record |
| `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-3-oh-my-pi.md` | create | spike 3 record |
| `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-4-hermes.md` | create | spike 4 record |

The six other reference files keep their text. They name each other by bare filename inside one directory, which is a correct relative path.

---

## Code blocks

Each block is the exact content of one file. The spike fixture (below) and the implementation tasks both write these blocks, so the spikes test the text that ships. A block is written verbatim, for example with the Write tool; no block contains a line `EOF`, so a quoted heredoc works too.

Two marker sentences tell the rules texts apart in transcripts:

- **New marker** (Block D): `The user installed the prose-discipline plugin`
- **Old marker** (published 1.3.0): `This standard is mandatory in every session`

### Block A: `hooks/hooks.json`

```json
{
  "description": "Print the prose-discipline core rules into every session and every subagent.",
  "hooks": {
    "SessionStart": [
      {
        "matcher": "startup|resume|clear|compact|fork",
        "hooks": [
          {
            "type": "command",
            "command": "sh \"${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh\""
          }
        ]
      }
    ],
    "SubagentStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "sh \"${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh\" --json"
          }
        ]
      }
    ]
  }
}
```

The file has no `timeout`: the conventions list the keys exactly, and the script reads one local file.

### Block B: `hooks/print-rules.sh`

The script uses `awk` and shell built-ins only. It escapes one character at a time because `gsub` replacement strings treat backslashes differently in mawk (Ubuntu), gawk (Git Bash) and BWK awk (macOS). The plan writer ran this exact text under macOS `sh`, `dash` and `bash --posix`, in the C and UTF-8 locales. Plain and JSON modes produced identical text. Backslash, quote, tab, CR and U+0001 came out as valid JSON, and every failure path gave empty stdout, one stderr line and exit 0.

```sh
#!/bin/sh
# Prints the body of rules/prose-discipline.md for a hook to inject.
#
# Without an argument the output is plain text starting with the H1:
# Claude Code adds plain SessionStart stdout to the context, and output that
# starts with "{" would be parsed as JSON instead.
# With --json the output is one SubagentStart hook object, because a
# subagent receives only hookSpecificOutput.additionalContext.
#
# Every failure prints one line to stderr and exits 0 with empty stdout.
# A non-zero exit would surface as a hook error, and the rules are context,
# never a gate on the session.

fail() {
  printf 'prose-discipline print-rules.sh: %s\n' "$1" >&2
  exit 0
}

case $# in
  0) mode=plain ;;
  1) [ "$1" = --json ] || fail "unknown argument: $1"; mode=json ;;
  *) fail "expected no argument or --json, got $# arguments" ;;
esac

# The script's own path locates the plugin root, so it reads the rules file
# of the package it belongs to whichever client ran it.
case $0 in
  */*) hooks_dir=${0%/*} ;;
  *) hooks_dir=. ;;
esac
rules=$hooks_dir/../rules/prose-discipline.md

[ -f "$rules" ] && [ -r "$rules" ] || fail "cannot read $rules"

# The command substitution holds the whole output until awk has succeeded,
# so a failure midway leaves stdout empty.
out=$(awk -v mode="$mode" '
  BEGIN {
    # Escapes are applied one character at a time. gsub replacement strings
    # treat backslashes differently in mawk, gawk and BWK awk.
    for (i = 1; i < 32; i++) esc[sprintf("%c", i)] = sprintf("\\u%04x", i)
    esc["\t"] = "\\t"
    esc["\r"] = "\\r"
    esc["\\"] = "\\\\"
    esc["\""] = "\\\""
    code = 0
  }
  NR == 1 && $0 == "---" { in_front = 1; next }
  in_front { if ($0 == "---") in_front = 0; next }
  !started && $0 == "" { next }
  !started {
    if (substr($0, 1, 2) != "# ") { code = 4; exit code }
    started = 1
  }
  { line[++n] = $0 }
  END {
    if (code) exit code
    if (in_front) exit 3
    if (!started) exit 4
    if (mode == "plain") {
      for (i = 1; i <= n; i++) print line[i]
      exit 0
    }
    text = ""
    for (i = 1; i <= n; i++) {
      if (i > 1) text = text "\\n"
      s = line[i]
      len = length(s)
      for (j = 1; j <= len; j++) {
        c = substr(s, j, 1)
        text = text ((c in esc) ? esc[c] : c)
      }
    }
    printf "{\"hookSpecificOutput\":{\"hookEventName\":\"SubagentStart\",\"additionalContext\":\"%s\"}}\n", text
  }
' "$rules" 2>/dev/null)
status=$?

case $status in
  0) printf '%s\n' "$out" ;;
  3) fail "$rules has front matter with no closing --- line" ;;
  4) fail "$rules has no level-1 heading where its body starts" ;;
  *) fail "awk exited with status $status while reading $rules" ;;
esac
```

Newlines inside the body become `\n` between lines; the escape table covers the rest of U+0001–U+001F. A NUL byte cannot reach awk, and the rules file holds none.

### Block C1: `skills/house-style/SKILL.md` (plan 02 fills the skill's `hermes-auto-load` region)

```markdown
---
name: house-style
description: >-
  Apply this plugin's engineering prose standard to anything an agent
  writes, from replies and code comments to commit messages and error
  messages. Use when writing or reviewing replies, docs, code comments,
  review comments, commit messages, change descriptions, error messages or
  agent instructions. Also use when asked to check, clean up, shorten or
  de-slop text.
license: MIT
---

# House style

In Hermes, add this skill to `skills.auto_load` so the standard is active in
every session. Hermes lists no plugin skill in its system prompt, so without
that setting the rules below reach a session only when this skill is loaded.
Add these lines to the Hermes `config.yaml`, merging them into an existing
`skills:` block:

<!-- hermes-auto-load:start -->
<!-- hermes-auto-load:end -->

<!-- rules:start -->
<!-- rules:end -->

## Replying to the user

- Reply in the user's language, directly and factually.
- Lead with the answer, then the evidence.
- Keep the language-neutral rules in every reply: one action per sentence,
  plain verbs, no hedging, no filler, no rhetorical negations.
- Match reply length to the question. A one-fact question gets a
  one-sentence answer.

## Writing artifacts

Read the matching reference before producing an artifact. Paths are
relative to this file:

- `references/structural-rules.md`: read when writing prose, docs or
  runbooks, or when a sentence, a procedure or a noun stack needs splitting.
- `references/vocabulary.md`: read when choosing words, for the
  substitution table, significance inflation and the domain-term contract.
- `references/slop-pruning.md`: read when text has rhetorical negations,
  teaser hooks, filler openers, false engagement or session-process
  narrative.
- `references/comment-hygiene.md`: read when writing or reviewing code
  comments.
- `references/artifact-formats.md`: read when writing a review comment,
  commit message, change description, error message or agent instruction.
- `references/examples.md`: read when calibrating an audit, to name each
  finding after its closest before/after pair.

When the host or repository defines a template for the artifact, the
template outranks this standard's formats. The standard governs only
the text that remains and never adds blocks on top.

Produce the artifact in the governing format directly. No preamble and
no closing commentary unless asked.

## Checking and cleaning text, when asked

1. Identify the artifact types and read the matching references above.
2. Report findings first, ordered by severity. Do not rewrite yet.
3. Apply the Exemptions section of the core rules as written there. Do not
   restate it here.
4. Each finding states the location, the violated rule, and the smallest
   fix.
5. Interactive sessions: apply the minimal fixes after the user approves.
   Autonomous and headless runs: apply only mechanical fixes, meaning the
   substitution table and Conventional Comments labels. Report judgment
   calls as findings.

On step 3, two things about that contract are easy to lose. It names
licenses as well. It limits the changelog and migration exemptions to
quoted historical text, never to text you author now.

Severity: `major` covers hedging comments, unlabeled review feedback,
merge-decision risks, change descriptions with no verification result,
and session-process narrative replacing a real result. `minor` covers
narrator, step, and divider comments, vocabulary, structure, and
format deviations. `nit` covers punctuation and single-word issues.

## Dogfooding

This plugin's own files must pass this standard. Check whole sentences, not
lines. Check punctuation as well as vocabulary: semicolons, em-dash quota,
and sentence budgets. Quoted specimens of banned patterns are exempt.
```

The rules region's routing table uses paths relative to the plugin root (Block D). The "Writing artifacts" list repeats the six files relative to this file, because no single relative path is right in both the rules file and its copy here. The old lines 13–22 ("reach a session by one of three routes" … "no route has been observed working") are gone: the routes live in the README, and the last sentence was the diary §3.1 removes.

### Block C2: `skills/house-style/SKILL.md` (plan 02 does not fill the skill's `hermes-auto-load` region)

Block C1 with one change. The paragraph from "In Hermes, add this skill" through the `<!-- hermes-auto-load:end -->` line is replaced by this paragraph:

```markdown
In Hermes, add this skill to `skills.auto_load` so the standard is active in
every session. Hermes lists no plugin skill in its system prompt, so without
that setting the rules below reach a session only when this skill is loaded.
The package README's Hermes section shows the exact `config.yaml` lines.
```

Everything else, front matter included, is Block C1 verbatim.

### Block D: `rules/prose-discipline.md`

L5 of the quality review: every absolute carries its reason beside it, and no requirement is softened. The opening line changes from "mandatory in every session, without exceptions" to a factual statement with its reason. That line contradicted the Exemptions section, and Claude Code's hooks documentation warns that text framed as system commands can trip its prompt-injection defences (research `06-claude-code-alwayson.md` line 52). The routing table names real paths (spec §5.4). Size: 4,942 bytes by `wc -c`.

```markdown
---
alwaysApply: true
description: Engineering prose standard for all agent-written text
---

# Prose discipline: core rules

The user installed the prose-discipline plugin, so this standard governs
everything you write in this session. The Exemptions section names the only
exceptions.

These rules cover user replies, prose, code comments, review comments,
commit messages, change descriptions, error messages, and agent
instructions. Replies use the user's language, because the user reads them.
Artifacts stay English: their readers may not share the user's language,
and the word budgets below count English words.

## Structure

- Sentences: 25 words max in English, or equivalent single-thought brevity in other languages. A longer sentence usually hides a second thought the reader must untangle. Split conjunction chains.
- Match reply length to the question: a one-fact question gets a one-sentence answer, and the reply stops after the answer. Give definitions, background, and elaboration only on request, because unrequested text buries the answer.
- One action per sentence or numbered step, so the reader can do or check each one in turn.
- Prefer active voice: the subject performs the action. Passive voice hides who acts.
- Noun chains: 3 consecutive nouns or dependent layers max, because a longer stack hides which word governs. Rephrase longer chains using verbs or prepositions.
- Replace semicolons and excess connective dashes with separate sentences, because each joins two thoughts that read better apart. Keep dashes where grammatically mandatory.

## Vocabulary

- Plain verbs: use direct action verbs. Weak-verb combinations like "perform validation" or "make use of" add words and no meaning.
- Connectives: use simple conjunctions. Heavy compound bureaucratic phrases slow the reader and add nothing.
- Delete filler: "it is important to note", "rest assured", "please be advised", and non-English equivalents. Filler carries no fact.
- State facts directly. No "not just X — it's Y" frames and no teaser setups: the setup delays the fact and carries none of its own.
- Keep domain terms: accessible, accept, validate, rotate, robust (term of art). Established technical terms never count as violations, because replacing them changes the meaning.

## Code comments

- No narration of the obvious ("This function handles...") and no step markers ("// Step 1:"). The code already says it, and narration goes stale when the code changes.
- Default to no comments. Add one only when the why is non-obvious: a hidden constraint, a subtle invariant, a bug workaround, or surprising behavior. A short orienting comment before a complex block is fine.
- No committed uncertainty ("should work"). Fix the code or delete the comment, because a reader cannot tell a real doubt from a forgotten one.
- No ASCII section dividers. A region that needs a banner needs its own file, class, or module.
- Comments explain why. Names and code explain what.

## Artifact formats

- Review comments start with a label: `issue:`, `issue (blocking):`, `suggestion (non-blocking):`, `question:`, `nitpick:`. The label tells the author whether the comment blocks the merge.
- Change descriptions: what changed, why, verification performed. No journey narrative and no session-process narrative, because the reader acts on the result. Verification states commands and results, never the process that produced them.
- Error message: what failed, the cause, the fix. The reader needs all three to act.
- Numbered steps: one imperative instruction per step, 20 words max, so each step is one thing to do.
- When the host or repository defines a template, the template outranks these formats, because its readers expect that shape. The standard governs the wording inside it.

## Exemptions

- Code blocks, identifiers, commands, and URLs are never flagged, because rewording them breaks them. Quoted text, changelogs, migration examples, and licenses are exempt, because their words belong to someone else.
- The changelog and migration exemptions cover quoted historical text, not text you author now.
- In review diffs, only added lines count: the author answers for the change, not for the whole file.

## Where the depth lives

The house-style skill of this plugin holds the depth behind every rule. Read
the matching reference before writing or reviewing an artifact. Paths are
relative to the plugin root.

| Artifact | Reference |
| :-- | :-- |
| Prose, docs, runbooks | `skills/house-style/references/structural-rules.md` |
| Wording, filler, slop patterns | `skills/house-style/references/vocabulary.md`, `skills/house-style/references/slop-pruning.md` |
| Code comments | `skills/house-style/references/comment-hygiene.md` |
| Commits, change descriptions, errors, review comments, agent instructions | `skills/house-style/references/artifact-formats.md` |
| Calibration examples | `skills/house-style/references/examples.md` |
```

### Block E: `README.md`

Citations reuse research `09-claude-codex-hooks.md`, `06-claude-code-alwayson.md`, `06-omp-alwayson.md`, `07-skill-names.md` and `08-hermes-auto-load.md`. The plan writer checked each Oh-My-Pi line number against the files at `ba56afb` and each Hermes line number at `749220ef`. Research 07 puts `_portable_skill_namespace` at lines 79–88 of `plugins_manifest.py`; the file at `749220ef` has it at lines 60–69, as research 08 says, and the block cites 60–69. The Claude Code and Codex documentation sites have no permalinks, so those links name the page and section; research 09 dates the reading 2026-09-24. The Codex loader defect stays out of the package, as spec §5.5 says.

The per-client routes sit under Usage as `###` sections. §5.1 has no slot of their own, and Usage is where a reader asks "what happens after install".

````markdown
# prose-discipline

<!-- description:start -->
<!-- description:end -->

## Install

<!-- install:start -->
<!-- install:end -->

## Usage

The standard needs no prompt. Claude Code and Oh-My-Pi load it into every
session on their own, and Codex does once you trust its hooks. Hermes loads
it once you pin the skill, as its section below shows.

To check existing text against the standard, ask for it:

```
Check this commit message against the house style: "Updated some stuff in auth so it works better now."
```

The agent reports each finding with the rule it breaks and the smallest fix.
In an interactive session it applies the fixes after you approve them.

Each client gets the same rules file by its own documented route:

| Client | Route | What you do |
| :-- | :-- | :-- |
| Claude Code | `SessionStart` and `SubagentStart` hooks | nothing |
| Codex | the same hooks, declared in `plugin.json` | trust the hooks |
| Oh-My-Pi | the rules file, applied to every request | nothing |
| Hermes | the skill, pinned with `skills.auto_load` | add the lines below to `config.yaml` |

### Claude Code

The `SessionStart` hook prints the core rules as plain text, and Claude Code
adds that text to the context. The hook runs again after `/clear`, a resume
and every compaction, so the rules come back where the context lost them.
The `SubagentStart` hook hands each subagent the same text as
`additionalContext`. Claude Code does not load a plugin's `CLAUDE.md`, and
its documentation sends plugin instructions through skills and hooks instead.

Sources, all Claude Code documentation:

- [Hooks](https://code.claude.com/docs/en/hooks), the `SessionStart` and
  `SubagentStart` sections: plain stdout and `additionalContext` as context.
- [Hooks guide](https://code.claude.com/docs/en/hooks-guide), "Re-inject
  context after compaction".
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference),
  "Standard plugin layout": a plugin's `CLAUDE.md` is not loaded, and
  plugins contribute context through skills, agents and hooks.

### Codex

`plugin.json` declares the hook file under `extensions["com.openai"].hooks`,
and Codex runs the same `SessionStart` and `SubagentStart` hooks. Codex skips
a plugin's hooks until you review and trust the current hook definition. It
sets `CLAUDE_PLUGIN_ROOT` for compatibility, so the same command finds the
script. Codex also lists every installed skill and tells the model to use one
whose description matches the task.

Sources:

- Codex documentation,
  [plugin packaging](https://developers.openai.com/plugins/build/plugins):
  the `hooks` field under `extensions.com.openai`, and hook trust.
- Codex documentation, [hooks](https://learn.chatgpt.com/docs/hooks):
  `CLAUDE_PLUGIN_ROOT` for compatibility.
- Codex source,
  [`catalog_prompt.rs`](https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/catalog_prompt.rs#L3-L8):
  the skill trigger rule.

### Oh-My-Pi

Oh-My-Pi reads `rules/prose-discipline.md` from a marketplace install. The
file's `alwaysApply: true` puts its full text into the system prompt of every
request. The file names no agents, so subagents get it too.

Sources:

- Oh-My-Pi documentation,
  [`docs/context-files.md`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/context-files.md#L74):
  marketplace plugins contribute rules.
- Oh-My-Pi documentation,
  [`docs/rulebook-matching-pipeline.md`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/rulebook-matching-pipeline.md#L248-L262):
  `alwaysApply` puts the full rule into the system prompt, and a rule with
  no `agents` applies to every agent.
- Oh-My-Pi source,
  [`claude-plugins.ts`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/claude-plugins.ts#L266-L285):
  the loader for a plugin's `rules/` directory.
- Oh-My-Pi source,
  [`agent-plugin-format.ts`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugin-format.ts#L539-L551):
  an Agent Plugins package keeps its rules.

### Hermes

Hermes loads `plugin.json` and `skills/` from this package, and lists no
plugin skill in its system prompt. To keep the standard active, pin the
skill with `skills.auto_load` in `config.yaml`. Merge the lines into an
existing `skills:` block:

<!-- hermes-auto-load:start -->
<!-- hermes-auto-load:end -->

Hermes then puts the whole skill, core rules included, into the system
prompt of every new session and marks it as active guidance. The name has
the form `agent-plugin-<name>-<hash>:house-style`. The hash is the first
eight hex digits of the SHA-256 of `plugin.json`'s `name`. That holds for a
package installed directly under the plugins directory, which
`hermes plugins install` does.

Sources:

- Hermes documentation,
  [`user-guide/cli.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/user-guide/cli.md#L297-L310):
  `skills.auto_load`.
- Hermes documentation,
  [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L71-L77):
  what a portable package provides, and the form of its namespace.
- Hermes documentation,
  [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L845):
  plugin skills are not in the system prompt's skills index.
- Hermes source,
  [`agent/skill_commands.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L165-L192) and
  [`tools/skills_tool.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/tools/skills_tool.py#L573-L590):
  `skills.auto_load` resolves a plugin skill by its qualified name.
- Hermes source,
  [`agent/skill_commands.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L653-L681):
  the auto-load wrapper.
- Hermes source,
  [`hermes_cli/plugins_manifest.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L455-L467)
  and [lines 60–69](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L60-L69):
  how the namespace is computed from the manifest `name`.

## What's inside

| Path | What it is |
| :-- | :-- |
| `rules/prose-discipline.md` | the core rules, the one source every client receives |
| `skills/house-style/SKILL.md` | the skill: a generated copy of the core rules, the checking procedure, and which reference to read when |
| `skills/house-style/references/` | structural rules, vocabulary, slop pruning, comment hygiene, artifact formats, and a calibration corpus |
| `hooks/hooks.json` | the `SessionStart` and `SubagentStart` hooks |
| `hooks/print-rules.sh` | prints the core rules, as plain text or, with `--json`, as a hook object |
| `plugin.json` | the Agent Plugins 1.0.0 manifest |
| `.claude-plugin/plugin.json` | a generated copy of `plugin.json`, where Claude Code reads it |
| `LICENSE` | the MIT license |

## Requirements and network

The hooks run `sh` and `awk` from `PATH`. On Windows, Claude Code runs
shell-form hooks in Git Bash when it is installed, and in PowerShell
otherwise ([hooks](https://code.claude.com/docs/en/hooks), "Exec form and
shell form", Claude Code documentation). If the script fails, it writes one
line to stderr and the session starts without the hook's copy of the rules.

The rules file stays under 8,000 characters. That keeps the hook text under
Claude Code's 10,000-character cap and Codex's default 2,500-token threshold
for hook context ([Claude Code hooks](https://code.claude.com/docs/en/hooks),
[Codex hooks](https://learn.chatgpt.com/docs/hooks), both documentation).

The package makes no network requests, needs no credentials and writes no
files.

## Boundaries

- It governs text mechanics, not whether a document serves its reader.
- It governs durable artifacts, not the register of a live conversation.
- It is not a code linter. Behaviour-level checks belong to a linter. For
  the design of the code itself, use `design-review` or `cognitive-load`.
- It states the standard once per context and never blocks a reply. There is
  no checker script: enforcement is model judgement over rule texts a person
  can read and argue with.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](../../SUPPORT.md).
````

### Block F: `plugin.json`

`version` stays `1.3.0`: release-please (plan 07) moves it from the commits. The description is one sentence of 23 words and 159 characters.

```json
{
  "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
  "name": "prose-discipline",
  "version": "1.3.0",
  "description": "An engineering prose standard kept active in every agent session: short active sentences, plain words, comments that explain why, and labelled review comments.",
  "author": {
    "name": "Alexander Kurganov",
    "url": "https://github.com/Akurganow"
  },
  "homepage": "https://github.com/Akurganow/ai-plugins/tree/main/plugins/prose-discipline",
  "repository": "https://github.com/Akurganow/ai-plugins",
  "license": "MIT",
  "keywords": [
    "prose",
    "writing",
    "style-guide",
    "anti-slop",
    "code-review",
    "conventional-comments",
    "commit-messages"
  ],
  "extensions": {
    "com.openai": {
      "hooks": "./hooks/hooks.json"
    },
    "io.github.akurganow.ai-plugins": {
      "category": "Productivity"
    }
  }
}
```

---

## Spike fixture recipe

Each spike builds this fixture under its own `$RUN` directory, outside the working tree, so the spikes change no tracked file. The recipe works before and after Task 5, because the glob matches the one skill directory either way.

```sh
REPO=$(git rev-parse --show-toplevel)
F="$RUN/fixture/prose-discipline"
mkdir -p "$F/.claude-plugin" "$F/hooks" "$F/rules" "$F/skills/house-style"
cp -R "$REPO"/plugins/prose-discipline/skills/*/references "$F/skills/house-style/references"
```

Then write, verbatim:

- Block F to `$F/plugin.json`, then `cp "$F/plugin.json" "$F/.claude-plugin/plugin.json"`.
- Block D to `$F/rules/prose-discipline.md`.
- Block A to `$F/hooks/hooks.json`.
- Block B to `$F/hooks/print-rules.sh`.
- Block C1 to `$RUN/SKILL.template.md`.

Then fill the rules region and check the fixture:

```sh
{
  awk '{print} /^<!-- rules:start -->$/{exit}' "$RUN/SKILL.template.md"
  sh "$F/hooks/print-rules.sh"
  awk '/^<!-- rules:end -->$/{f=1} f' "$RUN/SKILL.template.md"
} > "$F/skills/house-style/SKILL.md"
sh -n "$F/hooks/print-rules.sh" && jq empty "$F/hooks/hooks.json" "$F/plugin.json" && echo fixture-syntax-ok
sh "$F/hooks/print-rules.sh" | head -1
grep -c 'The user installed the prose-discipline plugin' "$F/skills/house-style/SKILL.md"
```

Expected: `fixture-syntax-ok`, `# Prose discipline: core rules`, `1`. The fixture leaves the skill's Hermes region empty; no spike reads it.

## Spike record template

Each spike writes one record under `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/`, in this shape:

```markdown
# Spike <n>: <client>

Run on <date> with <client> <version, as its --version printed it>, fixture built from plan 03 blocks A–F at commit <git rev-parse --short HEAD>.

## Assertions

| Id | Assertion | Result | Evidence |
| :-- | :-- | :-- | :-- |
| <id> | <what must hold> | pass, fail or not run | <the command, and the output lines that decide it> |

## Commands and output

<every command in order, each followed by the output lines that decide an assertion, verbatim>

## Consequence for plan 03

<"None", or the change from the task's failure list, and the owner's answer>
```

Record what the client printed, never a paraphrase. An assertion that could not run is "not run" with the reason.

---

### Task 1: Spike 1, Claude Code hook delivery

**Files:**
- Create: `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-1-claude-code.md`

**Interfaces:**
- Consumes: Blocks A, B, C1, D, F; the fixture recipe; Claude Code 2.1.278 on the owner's machine.
- Produces: assertions 1v, 1a, 1b, 1c with results. Tasks 6 and 7 read them before they start.

Spec §9 item 1: "install the package with `--plugin-dir`, confirm SessionStart stdout appears in context and survives `/compact`; confirm SubagentStart delivery." Each run below calls a model, with `--model haiku` and a turn cap to keep the cost small.

Evidence comes from the session transcript, not from the model's reply. A Claude Code transcript (`~/.claude/projects/<dir>/<session>.jsonl`) records each hook as an `attachment` line. `hook_success` carries `hookName` (for example `SessionStart:startup`), `command`, `exitCode` and `stderr`; `hook_additional_context` carries the injected `content`. The plan writer read that shape from a local 2.1.278 transcript.

- [ ] **Step 1: Prepare the run directory and record versions**

```sh
cd "$(git rev-parse --show-toplevel)"
RUN=$(mktemp -d "${TMPDIR:-/tmp}/pd-spike1.XXXXXX"); echo "$RUN"
claude --version
claude plugin list | grep -n 'prose-discipline' || echo 'prose-discipline: not installed in the CLI'
```

Expected: `2.1.278 (Claude Code)` and `prose-discipline: not installed in the CLI`. If the published package is installed, its old hook runs too. Every check below keys on `print-rules.sh` and on the new marker, so the two stay apart.

- [ ] **Step 2: Build the fixture**

Run the fixture recipe with this `$RUN`. Expected: `fixture-syntax-ok`, `# Prose discipline: core rules`, `1`.

- [ ] **Step 3: Assertion 1v, the validator accepts the fixture**

```sh
claude plugin validate "$RUN/fixture/prose-discipline"; echo "exit=$?"
```

Expected: `exit=0`. Record every warning line. A warning about `extensions` is expected, because Claude Code warns about top-level `plugin.json` fields it does not recognise. Any line naming `hooks.json` is recorded verbatim.

- [ ] **Step 4: Assertion 1a, SessionStart plain stdout reaches the context**

```sh
mkdir -p "$RUN/cwd" && cd "$RUN/cwd"
claude --plugin-dir "$RUN/fixture/prose-discipline" --model haiku --max-turns 2 \
  -p 'Reply with the single word ok.' --output-format json > "$RUN/startup.json"
SID=$(jq -r .session_id "$RUN/startup.json"); echo "$SID"
T=$(find ~/.claude/projects -name "$SID.jsonl" -print -quit); echo "$T"
jq -c 'select(.type=="attachment" and .attachment.hookEvent=="SessionStart")
  | .attachment | {type, hookName, command, exitCode, stderr}' "$T"
grep -c 'The user installed the prose-discipline plugin' "$T"
jq -r .result "$RUN/startup.json"
```

1a passes when all four hold:

- a `hook_success` object has `hookName` `SessionStart:startup`, a `command` ending in `print-rules.sh"`, `exitCode` `0` and an empty `stderr`;
- a `hook_additional_context` object is listed;
- the marker count is at least `1`;
- the result is `ok`.

A result that quotes the rules, warns about injected instructions or asks about them is **1a-injection**. It means Claude Code's prompt-injection defence treated the text as a command.

- [ ] **Step 5: Assertion 1b, the rules return after `/compact`**

```sh
touch "$RUN/before-compact"
cd "$RUN/cwd" && claude --plugin-dir "$RUN/fixture/prose-discipline" --model haiku --resume "$SID"
```

In the session, type `/compact` and wait for it to finish. Then type `Quote the first heading of the prose rules in your context, verbatim, or reply NONE.` and wait for the reply. Then type `/exit`.

```sh
T2=$(grep -l 'SessionStart:compact' $(find ~/.claude/projects -name '*.jsonl' -newer "$RUN/before-compact") | head -1); echo "$T2"
jq -c 'select(.attachment.hookName=="SessionStart:compact") | .attachment | {command, exitCode, stderr}' "$T2"
grep -n '"compact_boundary"' "$T2" | cut -c1-80
grep -n 'The user installed the prose-discipline plugin' "$T2" | cut -d: -f1 | tail -3
```

1b passes when a `SessionStart:compact` object names `print-rules.sh` with `exitCode` `0`, and a marker line number is greater than the `compact_boundary` line number. The quoted heading `# Prose discipline: core rules` supports it but does not decide it.

- [ ] **Step 6: Assertion 1c, SubagentStart delivers `additionalContext`**

```sh
cd "$RUN/cwd"
claude --plugin-dir "$RUN/fixture/prose-discipline" --model haiku --max-turns 4 --allowedTools Agent \
  -p "Use the Agent tool once to start a general-purpose subagent with this task: 'Quote the first heading of the prose rules in your context, verbatim, or reply NONE.' Then repeat the subagent's reply verbatim." \
  --output-format json > "$RUN/subagent.json"
SID3=$(jq -r .session_id "$RUN/subagent.json")
T3=$(find ~/.claude/projects -name "$SID3.jsonl" -print -quit); echo "$T3"
jq -c 'select(.type=="attachment" and .attachment.hookEvent=="SubagentStart")
  | .attachment | {type, hookName, command, exitCode, stderr}' "$T3" "${T3%.jsonl}"/subagents/*.jsonl
grep -l 'The user installed the prose-discipline plugin' "${T3%.jsonl}"/subagents/*.jsonl
jq -r .result "$RUN/subagent.json"
```

1c passes when a `SubagentStart` hook object has a `command` ending in `print-rules.sh" --json` with `exitCode` `0`, and `grep -l` lists a subagent transcript. A hook object with no subagent transcript holding the marker is **1c-undelivered**.

- [ ] **Step 7: Confirm the tree is untouched**

```sh
cd "$(git rev-parse --show-toplevel)" && git status --porcelain
```

Expected: no line for any tracked file. Untracked files of other plans in progress may be listed; this spike added none.

- [ ] **Step 8: Write the record**

Write `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-1-claude-code.md` from the record template, with rows 1v, 1a, 1b and 1c. Quote each deciding `jq` line and each count.

- [ ] **Step 9: Commit**

```sh
git add docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-1-claude-code.md
git commit -m "docs: record spike 1, Claude Code hook delivery" -m "Spike 1 of spec §9 checks SessionStart at startup and after /compact, and SubagentStart, against the plan 03 fixture." -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

**If it fails.** Stop before Task 6 and show the record to the owner when any row fails.

- **1v fails on `hooks.json`:** apply the change the error names to Block A and rerun Steps 3–6. If the error names `description`, the fix drops that key. Codex accepts its absence (`HooksFile.description` is an `Option`, research 09 §4). The conventions list the key, so the owner confirms first.
- **1a fails with exit 0 and no context:** Claude Code did not take plain stdout. SessionStart then needs JSON too, and `print-rules.sh` needs the event name (`--json SessionStart` or `--json SubagentStart`). That changes the conventions' interface, so the owner decides. Blocks A and B, and Task 7, change with it.
- **1a-injection:** the mechanism works and the wording does not. The owner decides whether Block D restates the rules as facts. Requirements are not softened (L5). Task 6 waits for that answer.
- **1b fails:** if no `SessionStart:compact` line exists, rerun Step 5 with the `matcher` line removed from the fixture's `hooks.json`. The spec's route column says "no matcher", so if that run passes, propose that change to the owner. If the hook ran and the marker is absent, record it; the plan keeps the hook.
- **1c fails:** a missing `SubagentStart` object means the event did not fire for the Agent tool in 2.1.278. **1c-undelivered** means it fired and the text did not arrive. In both cases the plan keeps the `SubagentStart` entry, which is harmless, unless the owner removes it.

---

### Task 2: Spike 3, Oh-My-Pi rules file and skill

**Files:**
- Create: `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-3-oh-my-pi.md`

**Interfaces:**
- Consumes: Blocks A, B, C1, D, F; the fixture recipe; Oh-My-Pi 18.2.8 and its `ai-plugins` marketplace (`Akurganow/ai-plugins`) on the owner's machine.
- Produces: assertions 3a-rules, 3a-skill, 3b-rules, 3b-skill. Task 8's Oh-My-Pi section rests on them.

Spec §9 item 3: "install from the marketplace, confirm `rules/prose-discipline.md` appears in the system prompt on every request; confirm the `agent-plugins` provider still loads the skill." The new package is not on `main` yet, so the spike runs twice:

- **3a:** the fixture through `--plugin-dir` (`docs/cli-reference.md` line 137), for the new text and the `house-style` skill.
- **3b:** the published 1.3.0 package through the marketplace, for the marketplace-origin route. That package already ships `rules/prose-discipline.md` with `alwaysApply: true` and a standard root.

Evidence comes from `/dump`. Its sidecar `omp-llm-request-<id>.json`, written under the OS temporary directory, holds the system prompt of the current request (`docs/session-operations-export-share-fork-resume.md`, "`/dump`"). Always-apply rules render inside `<generic-rules>` (`system-prompt.md` lines 37–42 at `ba56afb`). Each prompt below calls a model.

- [ ] **Step 1: Prepare and record versions and state**

```sh
cd "$(git rev-parse --show-toplevel)"
RUN=$(mktemp -d "${TMPDIR:-/tmp}/pd-spike3.XXXXXX"); echo "$RUN"
omp --version
jq -r '.plugins | keys[]' ~/.omp/plugins/installed_plugins.json | tee "$RUN/installed-before.txt"
omp plugin marketplace list
```

Expected: `omp/18.2.8`; a list without `prose-discipline@ai-plugins` (the state on 2026-09-25); `ai-plugins  Akurganow/ai-plugins`.

- [ ] **Step 2: Build the fixture**

Run the fixture recipe with this `$RUN`. Expected: `fixture-syntax-ok`, `# Prose discipline: core rules`, `1`.

- [ ] **Step 3: Run 3a with `--plugin-dir`**

```sh
mkdir -p "$RUN/cwd" && touch "$RUN/before-3a" && cd "$RUN/cwd"
omp --plugin-dir "$RUN/fixture/prose-discipline" --model haiku
```

If `--model haiku` matches no model, start without `--model` and pick the cheapest model `/model` lists. Record any startup warning, especially one containing `name collision` or `unexpected frontmatter field`. In the session:

1. Type `Reply with the single word ok.` and wait.
2. Type `/dump` and note the sidecar path it prints.
3. Type `Reply with the single word again.` and wait.
4. Type `/dump` again.
5. Type `/exit`.

```sh
for f in $(find "${TMPDIR:-/tmp}" -maxdepth 1 -name 'omp-llm-request-*.json' -newer "$RUN/before-3a"); do
  echo "== $f"
  printf 'generic-rules=%s new-marker=%s house-style=%s\n' \
    "$(grep -c '<generic-rules>' "$f")" \
    "$(grep -c 'The user installed the prose-discipline plugin' "$f")" \
    "$(grep -c 'house-style' "$f")"
done
```

If `/dump` printed a path outside `${TMPDIR:-/tmp}`, run the loop over that directory instead. 3a-rules passes when both sidecars show `generic-rules` and `new-marker` of at least 1. 3a-skill passes when both show `house-style` of at least 1 and no startup warning named the skill.

- [ ] **Step 4: Run 3b through the marketplace**

```sh
omp plugin install prose-discipline@ai-plugins
touch "$RUN/before-3b" && cd "$RUN/cwd" && omp --model haiku
```

In the session, type `Reply with the single word ok.`, then `/dump`, then `/exit`.

```sh
for f in $(find "${TMPDIR:-/tmp}" -maxdepth 1 -name 'omp-llm-request-*.json' -newer "$RUN/before-3b"); do
  echo "== $f"
  printf 'generic-rules=%s old-marker=%s skill=%s\n' \
    "$(grep -c '<generic-rules>' "$f")" \
    "$(grep -c 'This standard is mandatory in every session' "$f")" \
    "$(grep -c 'prose-discipline' "$f")"
done
```

3b-rules passes when `generic-rules` and `old-marker` are at least 1. 3b-skill passes when the skill `prose-discipline` appears in the prompt's skill list; quote that line.

- [ ] **Step 5: Restore the owner's install state**

```sh
omp plugin uninstall prose-discipline@ai-plugins
jq -r '.plugins | keys[]' ~/.omp/plugins/installed_plugins.json | diff "$RUN/installed-before.txt" - && echo restored
rm -f $(find "${TMPDIR:-/tmp}" -maxdepth 1 -name 'omp-llm-request-*.json' -newer "$RUN/before-3a")
cd "$(git rev-parse --show-toplevel)" && git status --porcelain
```

Expected: `restored`, and no line for a tracked file. The sidecars hold raw context, which is why the spike deletes them (`docs/session-operations-export-share-fork-resume.md` warns about that).

- [ ] **Step 6: Write the record**

Write `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-3-oh-my-pi.md` from the record template, with rows 3a-rules, 3a-skill, 3b-rules and 3b-skill.

- [ ] **Step 7: Commit**

```sh
git add docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-3-oh-my-pi.md
git commit -m "docs: record spike 3, Oh-My-Pi rules file and skill" -m "Spike 3 of spec §9 checks the always-apply rules file and the skill, from --plugin-dir and from the marketplace." -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

**If it fails.** Stop before Task 8 and show the record to the owner when 3b-rules or 3a-skill fails.

- **3a-rules fails and 3b-rules passes:** `--plugin-dir` roots behave differently from marketplace roots. Users install from the marketplace, so no plan change; record it.
- **3b-rules fails:** the rules route does not work for a standard root in 18.2.8. Block E's Oh-My-Pi section then claims what the client does not do. The spec closed the two alternatives (TTSR files, TypeScript hooks), so the owner decides.
- **3a-skill fails:** a front-matter warning means Block C1's front matter breaks the six-field validator; fix it and rerun. A `name collision` means another installed source ships `house-style`. The name is then chosen again by the §5.4 rule, with the owner.

---

### Task 3: Spike 4, Hermes skill and `skills.auto_load`

**Files:**
- Create: `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-4-hermes.md`

**Interfaces:**
- Consumes: Blocks A, B, C1, D, F; the fixture recipe; Hermes 0.21.5 on the owner's machine, with the published `prose-discipline` 1.3.0 installed and enabled at user scope.
- Produces: assertions 4-install, 4a, 4b, 4c. Task 5's Hermes lines and Task 8's Hermes section rest on them.

Spec §9 item 4: "install the portable package, confirm the skill loads; set `skills.auto_load` with the computed qualified name and confirm the rules appear in the system prompt with Hermes's auto-load wrapper; test Hermes on Windows at all."

The installed Hermes reports `upstream d350422b`. Research 08 read `749220ef`. The wrapper text at line 673 of `agent/skill_commands.py` is the same in both. Hermes stores each session's system prompt in `~/.hermes/state.db`: `sessions.system_prompt_hash` points into table `system_prompts`. The plan writer read that schema from the local database. Each `hermes chat` call below calls a model; pass `-m` with the cheapest model the configured provider offers.

The spike changes the owner's Hermes install and config, and Step 7 restores both.

- [ ] **Step 1: Prepare, record versions and back up the config**

```sh
cd "$(git rev-parse --show-toplevel)"
RUN=$(mktemp -d "${TMPDIR:-/tmp}/pd-spike4.XXXXXX"); echo "$RUN"
hermes --version
hermes plugins list | grep -A1 'prose-discipline'
CFG=$(hermes config path); echo "$CFG"; cp "$CFG" "$RUN/config.yaml.bak"
hermes config get skills.auto_load
printf %s prose-discipline | shasum -a 256 | cut -c1-8
```

Expected: `Hermes Agent v0.21.5 …`; `prose-discipline │ enabled │ 1.3.0 …`; a config path; an empty or unset `skills.auto_load`; `cf518319`.

- [ ] **Step 2: Build the fixture as a Git repository**

Run the fixture recipe with this `$RUN`, then:

```sh
cp -R "$RUN/fixture/prose-discipline" "$RUN/pkg"
git -C "$RUN/pkg" init -q
git -C "$RUN/pkg" add -A
git -C "$RUN/pkg" -c user.name=spike -c user.email=spike@invalid commit -qm fixture
hermes plugins validate "$RUN/pkg"; echo "exit=$?"
```

Record the validator output in full; plan 07 adds the same validator to CI.

- [ ] **Step 3: Assertion 4-install, the portable package installs flat**

```sh
hermes plugins install "file://$RUN/pkg" --force --enable; echo "exit=$?"
hermes plugins list | grep -A1 'prose-discipline'
ls ~/.hermes/plugins/prose-discipline/skills
```

4-install passes when the list shows `prose-discipline` enabled and `ls` prints `house-style`. `--force` removes the existing install first (`hermes plugins install --help`). If Hermes refuses the `file://` URL, use the loader-equivalent route and record which one ran:

```sh
rm -rf ~/.hermes/plugins/prose-discipline
cp -R "$RUN/fixture/prose-discipline" ~/.hermes/plugins/prose-discipline
hermes plugins enable prose-discipline
```

- [ ] **Step 4: Assertion 4a, the skill loads by its qualified name**

```sh
hermes chat -q 'Call skill_view with the name "agent-plugin-prose-discipline-cf518319:house-style" and reply with the first heading of its content.' --oneshot -Q
S4A=$(sqlite3 -readonly ~/.hermes/state.db "SELECT id FROM sessions ORDER BY started_at DESC LIMIT 1")
sqlite3 -readonly ~/.hermes/state.db "SELECT content FROM messages WHERE session_id='$S4A' AND role='tool'" > "$RUN/4a-tool.txt"
grep -c 'The user installed the prose-discipline plugin' "$RUN/4a-tool.txt"
grep -c 'Bundle context' "$RUN/4a-tool.txt"
```

4a passes when both counts are at least 1. If `skill_view` reports the skill missing, get the real name and record it as **4a-name**:

```sh
hermes chat -q 'Call skills_list with category "plugin" and print every name it returns, verbatim.' --oneshot -Q
```

- [ ] **Step 5: Assertion 4b, `skills.auto_load` pins the skill into the system prompt**

```sh
hermes config set skills.auto_load '["agent-plugin-prose-discipline-cf518319:house-style"]'
hermes config get skills.auto_load
```

Expected: a list with the one entry. If it prints a string instead, copy `$RUN/config.yaml.bak` back to `$CFG`. Then add these two lines inside the existing `skills:` block, indented one level, and run `hermes config get skills.auto_load` again:

```yaml
  auto_load:
    - agent-plugin-prose-discipline-cf518319:house-style
```

Then:

```sh
: > "$RUN/log-mark"; wc -l < ~/.hermes/logs/agent.log > "$RUN/log-lines-before"
hermes chat -q 'Reply with the single word ok.' --oneshot -Q
sqlite3 -readonly ~/.hermes/state.db "SELECT COALESCE(p.prompt, s.system_prompt) FROM sessions s LEFT JOIN system_prompts p ON p.hash = s.system_prompt_hash ORDER BY s.started_at DESC LIMIT 1" > "$RUN/4b-system.txt"
grep -F -c '[IMPORTANT: The "agent-plugin-prose-discipline-cf518319:house-style" skill is auto-loaded via config (skills.auto_load).' "$RUN/4b-system.txt"
grep -c 'The user installed the prose-discipline plugin' "$RUN/4b-system.txt"
grep -c '^# House style' "$RUN/4b-system.txt"
tail -n +"$(( $(cat "$RUN/log-lines-before") + 1 ))" ~/.hermes/logs/agent.log | grep -n 'skills.auto_load' || echo 'no auto_load log line'
```

4b passes when the wrapper count is `1`, the marker and `# House style` counts are at least 1, and the log shows `no auto_load log line`. A log line `skills.auto_load: skill(s) not found or disabled, skipped: …` is **4b-skipped**.

- [ ] **Step 6: Assertion 4c, Hermes on Windows**

Record 4c as "not run: this machine runs macOS". The Windows × Hermes job of plan 07's integration matrix covers it.

- [ ] **Step 7: Restore the owner's Hermes state**

```sh
cp "$RUN/config.yaml.bak" "$CFG"
hermes plugins install Akurganow/ai-plugins/plugins/prose-discipline --force --enable
hermes plugins list | grep -A1 'prose-discipline'
hermes config get skills.auto_load
cd "$(git rev-parse --show-toplevel)" && git status --porcelain
```

Expected: `prose-discipline` enabled at `1.3.0`; `skills.auto_load` as Step 1 printed it; no line for a tracked file.

- [ ] **Step 8: Write the record**

Write `docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-4-hermes.md` from the record template, with rows 4-install, 4a, 4b and 4c. Quote the wrapper line exactly as `4b-system.txt` holds it.

- [ ] **Step 9: Commit**

```sh
git add docs/superpowers/handoff/2026-09-24-marketplace-quality/spikes/spike-4-hermes.md
git commit -m "docs: record spike 4, Hermes skill and skills.auto_load" -m "Spike 4 of spec §9 checks the portable install, the qualified skill name and the auto-load wrapper against the plan 03 fixture." -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

**If it fails.** Stop before Task 5 and show the record to the owner when 4a or 4b fails.

- **4-install needs the copy route:** no plan change; the record says which route ran.
- **4a-name:** the namespace formula differs in 0.21.5. The fix goes to plan 02's `hermes_namespace` and to Block E's Hermes paragraph; the owner hears of it first.
- **4b-skipped with 4a passing:** `skills.auto_load` does not resolve plugin skills in this version, and the documented route fails. The spec closed Python and native plugins, so the owner decides what the README recommends.
- **4b with the wrapper but no marker:** the skill loaded without its rules region. Check the fixture's `SKILL.md` and rerun Step 5.

---

### Task 4: Manifest

**Files:**
- Modify: `plugins/prose-discipline/plugin.json` (whole file; Block F)
- Generated: `plugins/prose-discipline/.claude-plugin/plugin.json`

**Interfaces:**
- Consumes: plan 02 landed (`tools/regenerate.sh`, the byte-equality check, the six vendor manifests as regular files).
- Produces: the description plan 06 shows; `extensions["com.openai"].hooks`, which Task 7's `hooks/hooks.json` satisfies.

Today's `plugin.json` holds a 1,154-character description, the `agent-skills` keyword and `extensions["io.github.akurganow.ai-plugins"]` with `components`, `components_note` and `interface` (lines 5, 21, 24–35 at `344c8fc`).

- [ ] **Step 1: Check the preconditions**

```sh
cd "$(git rev-parse --show-toplevel)"
test -x tools/regenerate.sh && echo regenerate-present
test -f plugins/prose-discipline/.claude-plugin/plugin.json && ! test -L plugins/prose-discipline/.claude-plugin/plugin.json && echo vendor-is-a-file
/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python tools/check-conformance.py; echo "exit=$?"
```

Expected: `regenerate-present`, `vendor-is-a-file`, `exit=0`. Otherwise plan 02 has not landed; stop.

- [ ] **Step 2: Write the failing test**

```sh
jq -e '(.description | length) <= 250
  and (.keywords | index("agent-skills")) == null
  and .extensions["io.github.akurganow.ai-plugins"].category == "Productivity"
  and .extensions["com.openai"].hooks == "./hooks/hooks.json"
  and (.extensions | keys) == ["com.openai", "io.github.akurganow.ai-plugins"]
  and (.extensions["io.github.akurganow.ai-plugins"] | keys) == ["category"]' \
  plugins/prose-discipline/plugin.json; echo "exit=$?"
```

Expected now: `false`, `exit=1`.

- [ ] **Step 3: Write Block F to `plugins/prose-discipline/plugin.json`**

- [ ] **Step 4: Regenerate the copies**

```sh
tools/regenerate.sh; echo "exit=$?"
```

Expected: `exit=0`.

- [ ] **Step 5: Run the tests**

```sh
jq -e '(.description | length) <= 250
  and (.keywords | index("agent-skills")) == null
  and .extensions["io.github.akurganow.ai-plugins"].category == "Productivity"
  and .extensions["com.openai"].hooks == "./hooks/hooks.json"
  and (.extensions | keys) == ["com.openai", "io.github.akurganow.ai-plugins"]
  and (.extensions["io.github.akurganow.ai-plugins"] | keys) == ["category"]' \
  plugins/prose-discipline/plugin.json
jq -r .description plugins/prose-discipline/plugin.json | wc -w
jq -r .description plugins/prose-discipline/plugin.json | grep -o '[.!?]' | wc -l
jq -r .version plugins/prose-discipline/plugin.json
jq empty plugins/prose-discipline/plugin.json plugins/prose-discipline/.claude-plugin/plugin.json
cmp plugins/prose-discipline/plugin.json plugins/prose-discipline/.claude-plugin/plugin.json && echo copy-equal
/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python tools/check-conformance.py; echo "exit=$?"
claude plugin validate plugins/prose-discipline; echo "exit=$?"
```

Expected: `true`; `23`; `1`; `1.3.0`; no `jq` output; `copy-equal`; `exit=0`; `exit=0`. The validator may warn about `extensions` as an unrecognised top-level field; record the line and move on (no `--strict`, spec §7.3).

- [ ] **Step 6: Commit**

`tools/regenerate.sh` may also rewrite `.claude-plugin/marketplace.json` and the root `README.md` table. Those are plan 06's files: leave them unstaged.

```sh
git add plugins/prose-discipline/plugin.json plugins/prose-discipline/.claude-plugin/plugin.json
git status --porcelain plugins/prose-discipline
git commit -m "feat(prose-discipline): one-line description, category and Codex hook path" \
  -m "The description becomes one 23-word sentence, because catalogues show a one-line summary. The category is Productivity, for the generated catalogue. Codex reads hooks from extensions[\"com.openai\"].hooks. The components, components_note and interface keys go, because no client reads them." \
  -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Expected from `git status` before the commit: only the two staged files under `plugins/prose-discipline`.

---

### Task 5: Rename the skill to `house-style`

**Files:**
- Rename: `plugins/prose-discipline/skills/prose-discipline/` → `plugins/prose-discipline/skills/house-style/` (`git mv`)
- Modify: `plugins/prose-discipline/skills/house-style/SKILL.md` (whole file; Block C1 or C2)
- Generated: the `rules` region, the `hermes-auto-load` region (C1 only), the doctoc TOC in `references/examples.md`

**Interfaces:**
- Consumes: plan 02's `rules` region contract; the optional `hermes-auto-load` line in the skill (see "Requested from plan 02").
- Produces: the path `plugins/prose-discipline/skills/house-style/references/*.md`, which Block D's routing table names in Task 6.

- [ ] **Step 1: Choose the block**

```sh
grep -F 'replace_region plugins/prose-discipline/skills/house-style/SKILL.md hermes-auto-load' tools/regenerate.sh && echo use-C1 || echo use-C2
```

- [ ] **Step 2: Write the failing test**

```sh
test -f plugins/prose-discipline/skills/house-style/SKILL.md; echo "exit=$?"
```

Expected now: `exit=1`.

- [ ] **Step 3: Rename the directory**

```sh
git mv plugins/prose-discipline/skills/prose-discipline plugins/prose-discipline/skills/house-style
```

- [ ] **Step 4: Write Block C1 or C2 (Step 1's answer) to `plugins/prose-discipline/skills/house-style/SKILL.md`**

- [ ] **Step 5: Regenerate**

```sh
tools/regenerate.sh; echo "exit=$?"
```

Expected: `exit=0`. The `rules` region now holds today's rules text; Task 6 replaces it.

- [ ] **Step 6: Run the tests**

```sh
S=plugins/prose-discipline/skills/house-style/SKILL.md
/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python - "$S" <<'PY'
import sys, yaml
text = open(sys.argv[1], encoding="utf-8").read()
front = yaml.safe_load(text.split("\n---\n", 1)[0].removeprefix("---\n"))
d = front["description"]
print(front["name"], front["license"], len(d) <= 1024, d.startswith("Apply "), "Use when" in d)
PY
awk '/^<!-- rules:start -->$/{f=1;next} /^<!-- rules:end -->$/{f=0} f' "$S" | grep -v '^$' | head -1
for r in plugins/prose-discipline/skills/house-style/references/*.md; do
  grep -q "^- \`references/${r##*/}\`: read when" "$S" || echo "not routed: $r"
done
grep -c '^<!-- START doctoc' plugins/prose-discipline/skills/house-style/references/examples.md
grep -rln 'skills/prose-discipline' plugins/prose-discipline | grep -v '/README.md$' || echo no-old-path
/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python tools/check-conformance.py; echo "exit=$?"
claude plugin validate plugins/prose-discipline; echo "exit=$?"
```

Expected: `house-style MIT True True True`; `# Prose discipline: core rules`; no `not routed` line; `1`; `no-old-path`; `exit=0`; `exit=0`. The README still names the old path until Task 8, which is why the grep skips it.

With Block C1, also:

```sh
grep -x -- '    - agent-plugin-prose-discipline-cf518319:house-style' "$S"
```

Expected: that line, once.

- [ ] **Step 7: Commit**

```sh
git add plugins/prose-discipline/skills
git status --porcelain plugins/prose-discipline
git commit -m "feat(prose-discipline)!: rename the skill to house-style" \
  -m "Oh-My-Pi shows bare skill names and drops a later duplicate, so a skill name must be distinctive without its plugin. The skill now carries the core rules in a generated region, because Hermes loads nothing else from the package. It names each reference by path with a read-when condition, and its front matter gains license: MIT." \
  -m "BREAKING CHANGE: the skill is house-style. Claude Code invokes it as /prose-discipline:house-style." \
  -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Expected from `git status` before the commit: only staged paths under `plugins/prose-discipline/skills/`.

---

### Task 6: Rules file with reasons and real paths

**Files:**
- Modify: `plugins/prose-discipline/rules/prose-discipline.md` (whole file; Block D)
- Generated: the `rules` region of `plugins/prose-discipline/skills/house-style/SKILL.md`

**Interfaces:**
- Consumes: Task 5's `skills/house-style/references/`; spike 1's answer on 1a-injection.
- Produces: the rules body that `print-rules.sh` (Task 7) prints and the generator copies.

Start only when spike 1 recorded no **1a-injection**, or the owner has answered it.

- [ ] **Step 1: Write the failing tests**

```sh
R=plugins/prose-discipline/rules/prose-discipline.md
grep -c 'without exceptions' "$R"
grep -o 'skills/house-style/references/[a-z-]*\.md' "$R" | wc -l
```

Expected now: `1`, then `0`.

- [ ] **Step 2: Write Block D to `plugins/prose-discipline/rules/prose-discipline.md`**

- [ ] **Step 3: Run the rules-file tests**

```sh
R=plugins/prose-discipline/rules/prose-discipline.md
grep -c 'without exceptions' "$R"
grep -o 'skills/house-style/references/[a-z-]*\.md' "$R" | wc -l
for p in $(grep -o 'skills/house-style/references/[a-z-]*\.md' "$R"); do
  test -f "plugins/prose-discipline/$p" || echo "missing $p"
done
wc -c < "$R"
sed -n '1,4p' "$R"
awk '/^```/{c=!c;next} !c && !/^\|/ && !/^#/ && !/^---$/ && !/^[a-zA-Z]+:/' "$R" \
  | sed 's/^- //' | awk 'BEGIN{RS=""} {gsub(/\n/," "); print}' \
  | sed 's/\([.?!]\) /\1\n/g' | awk 'NF>25{print NF": "$0}'
```

Expected: `0`; `6`; no `missing` line; `4942`; the front matter with `alwaysApply: true`; no sentence line over 25 words.

- [ ] **Step 4: Review L5 by reading**

```sh
grep -nE '^- .*(never|No |max|only|must)' plugins/prose-discipline/rules/prose-discipline.md
```

Read each printed bullet. It must state its reason in the same bullet, after "because", "so", or a colon. Compare it with the same bullet at `344c8fc` (`git show 344c8fc:plugins/prose-discipline/rules/prose-discipline.md`); no limit, word list or format may be weaker. Block D passes this review as written; the step guards against an edit made while copying it.

- [ ] **Step 5: Regenerate and compare the skill's copy**

```sh
tools/regenerate.sh; echo "exit=$?"
S=plugins/prose-discipline/skills/house-style/SKILL.md
awk '/^<!-- rules:start -->$/{f=1;next} /^<!-- rules:end -->$/{f=0} f' "$S" | grep -v '^$' > "${TMPDIR:-/tmp}/pd-region.txt"
awk 'NR==1 && /^---$/{f=1;next} f && /^---$/{f=0;next} !f' "$R" | grep -v '^$' | diff - "${TMPDIR:-/tmp}/pd-region.txt" && echo region-equal
/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python tools/check-conformance.py; echo "exit=$?"
```

Expected: `exit=0`, `region-equal`, `exit=0`.

- [ ] **Step 6: Commit**

```sh
git add plugins/prose-discipline/rules/prose-discipline.md plugins/prose-discipline/skills/house-style/SKILL.md
git status --porcelain plugins/prose-discipline
git commit -m "feat(prose-discipline): give each core rule its reason and route by path" \
  -m "Every absolute in the rules now states its reason beside it, and no limit is weaker. The opening line states a fact instead of an unexplained absolute. The routing table names each reference by its path from the plugin root." \
  -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 7: Hooks without `node`

**Files:**
- Create: `plugins/prose-discipline/hooks/print-rules.sh` (Block B), mode 100644
- Modify: `plugins/prose-discipline/hooks/hooks.json` (whole file; Block A)
- Delete: `plugins/prose-discipline/hooks/session-rules.sh`

**Interfaces:**
- Consumes: Task 6's rules file; spike 1's answers on 1v, 1a and 1c.
- Produces: `sh hooks/print-rules.sh` prints the body starting with `# Prose discipline: core rules`; `sh hooks/print-rules.sh --json` prints one `SubagentStart` object. Task 8's README describes both.

Today's `hooks.json` registers `SessionStart` only, with `sh "${CLAUDE_PLUGIN_ROOT:-${PLUGIN_ROOT:-.}}/hooks/session-rules.sh"` and `"timeout": 10` (lines 6–11 at `344c8fc`). `session-rules.sh` needs `node` (line 19). Start only when spike 1 recorded 1v, 1a and 1c as passing, or the owner has answered each failure.

- [ ] **Step 1: Write the failing tests**

```sh
H=plugins/prose-discipline/hooks
test -f "$H/print-rules.sh"; echo "exit=$?"
jq -e '.hooks | has("SubagentStart")' "$H/hooks.json"; echo "exit=$?"
grep -c 'node' "$H/session-rules.sh"
```

Expected now: `exit=1`; `false` and `exit=1`; a count of at least 1.

- [ ] **Step 2: Write Block B to `plugins/prose-discipline/hooks/print-rules.sh`**

Keep it without an execute bit. `hooks.json` runs it through `sh`, and the package dropped the bit on purpose in `b775fa5`.

- [ ] **Step 3: Write Block A to `plugins/prose-discipline/hooks/hooks.json`**

- [ ] **Step 4: Delete the old script**

```sh
git rm -q plugins/prose-discipline/hooks/session-rules.sh
```

- [ ] **Step 5: Run the structure and output tests**

```sh
H=plugins/prose-discipline/hooks
ROOT=$PWD/plugins/prose-discipline
sh -n "$H/print-rules.sh" && echo syntax-ok
command -v dash >/dev/null && dash -n "$H/print-rules.sh" && echo dash-syntax-ok
jq empty "$H/hooks.json"
jq -e '(keys == ["description", "hooks"])
  and (.hooks | keys) == ["SessionStart", "SubagentStart"]
  and .hooks.SessionStart[0].matcher == "startup|resume|clear|compact|fork"
  and (.hooks.SubagentStart[0] | has("matcher") | not)
  and ([.. | objects | select(has("args") or has("additionalContextLimit"))] | length) == 0' "$H/hooks.json"
sh "$H/print-rules.sh" | head -1
sh "$H/print-rules.sh" --json | jq empty && echo json-valid
sh "$H/print-rules.sh" --json | jq -r '.hookSpecificOutput.hookEventName'
sh "$H/print-rules.sh" > "${TMPDIR:-/tmp}/pd-plain.txt"
sh "$H/print-rules.sh" --json | jq -r .hookSpecificOutput.additionalContext | cmp - "${TMPDIR:-/tmp}/pd-plain.txt" && echo modes-agree
CLAUDE_PLUGIN_ROOT=$ROOT sh -c "$(jq -r '.hooks.SessionStart[0].hooks[0].command' "$H/hooks.json")" | head -1
CLAUDE_PLUGIN_ROOT=$ROOT sh -c "$(jq -r '.hooks.SubagentStart[0].hooks[0].command' "$H/hooks.json")" | jq -r .hookSpecificOutput.hookEventName
git ls-files -s "$H/print-rules.sh" | cut -c1-6
```

Expected: `syntax-ok`; `dash-syntax-ok` where `dash` exists; no `jq empty` output; `true`; `# Prose discipline: core rules`; `json-valid`; `SubagentStart`; `modes-agree`; `# Prose discipline: core rules`; `SubagentStart`. The `git ls-files` line prints nothing until Step 8 stages the file, then `100644`.

- [ ] **Step 6: Run the escaping and failure tests in a scratch copy**

```sh
T=$(mktemp -d "${TMPDIR:-/tmp}/pd-hook.XXXXXX")
mkdir -p "$T/hooks" "$T/rules"
cp plugins/prose-discipline/hooks/print-rules.sh "$T/hooks/"
printf -- '---\na: b\n---\n\n# T\nback\\slash "quote"\ttab\rcr\001ctl\n' > "$T/rules/prose-discipline.md"
sh "$T/hooks/print-rules.sh" --json | jq -r .hookSpecificOutput.additionalContext | od -c | head -3
check() { out=$(sh "$T/hooks/print-rules.sh" "$@" 2>"$T/err"); printf 'exit=%s stdout=[%s] stderr_lines=%s\n' "$?" "$out" "$(wc -l < "$T/err" | tr -d ' ')"; }
check --bogus
check --json extra
printf -- '---\na: b\n# T\n' > "$T/rules/prose-discipline.md"; check
printf -- '{"a": 1}\n' > "$T/rules/prose-discipline.md"; check
rm "$T/rules/prose-discipline.md"; check --json
```

Expected: the `od` dump shows `#   T  \n   b   a   c   k   \   s   l   a   s   h       "   q   u   o   t   e   "  \t   t   a   b  \r   c   r 001   c   t   l`. Each of the five `check` lines prints `exit=0 stdout=[] stderr_lines=1`.

- [ ] **Step 7: Run the package checks**

```sh
grep -rln 'session-rules\|node' plugins/prose-discipline | grep -v '/README.md$' || echo no-node
/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python tools/check-conformance.py; echo "exit=$?"
claude plugin validate plugins/prose-discipline; echo "exit=$?"
```

Expected: `no-node`; `exit=0`; `exit=0`. Record any validator line that names `hooks.json`. The README still describes the old hook until Task 8, which is why the grep skips it.

- [ ] **Step 8: Commit**

```sh
git add plugins/prose-discipline/hooks/print-rules.sh plugins/prose-discipline/hooks/hooks.json
git ls-files -s plugins/prose-discipline/hooks/print-rules.sh | cut -c1-6
git status --porcelain plugins/prose-discipline
git commit -m "feat(prose-discipline): print the rules at session and subagent start without node" \
  -m "print-rules.sh uses sh and awk only, so the hook runs wherever the shell does. SessionStart gets plain text, which Claude Code adds to the context. SubagentStart gets JSON additionalContext, the documented route into a subagent. Every failure exits 0 with one stderr line." \
  -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

Expected before the commit: `100644`, and the staged add, modify and delete under `plugins/prose-discipline/hooks/`.

---

### Task 8: README

**Files:**
- Modify: `plugins/prose-discipline/README.md` (whole file; Block E)
- Generated: its `description`, `install` and `hermes-auto-load` regions

**Interfaces:**
- Consumes: Tasks 4–7; spike 3 (3b-rules) and spike 4 (4a, 4b) results; plan 02's `install` template; `LICENSE` from plan 02; `SUPPORT.md` from plan 06.
- Produces: the package README that plan 06's root table links to.

Today's README holds the diary paragraph "Nothing below has been verified from this repository as published" (lines 56–62 at `344c8fc`), the symlink passage (64–70) and a superseded Codex passage (72–90). Start only when 3b-rules, 4a and 4b passed, or the owner has answered each failure.

- [ ] **Step 1: Write the failing tests**

```sh
P=plugins/prose-discipline/README.md
grep -c '^<!-- hermes-auto-load:start -->$' "$P"
grep -c 'Nothing below has been verified' "$P"
```

Expected now: `0`, then `1`.

- [ ] **Step 2: Write Block E to `plugins/prose-discipline/README.md`**

- [ ] **Step 3: Regenerate**

```sh
tools/regenerate.sh; echo "exit=$?"
```

Expected: `exit=0`.

- [ ] **Step 4: Run the tests**

```sh
P=plugins/prose-discipline/README.md
grep '^## ' "$P"
awk '/^<!-- description:start -->$/{f=1;next} /^<!-- description:end -->$/{f=0} f' "$P" | grep -v '^$' \
  | diff - <(jq -r .description plugins/prose-discipline/plugin.json) && echo description-equal
grep -c 'prose-discipline@ai-plugins' "$P"
grep -c 'hermes plugins install Akurganow/ai-plugins/plugins/prose-discipline' "$P"
grep -x -- '    - agent-plugin-prose-discipline-cf518319:house-style' "$P"
grep -niE 'not verified|has been installed|was installed|verified on' "$P" || echo no-diary
grep -nE 'skills/prose-discipline|session-rules|node' "$P" || echo no-old-names
grep -o 'github\.com/[^)]*/blob/[^/)]*/' "$P" | grep -v '/blob/[0-9a-f]\{40\}/' || echo all-permalinks
test -f plugins/prose-discipline/LICENSE && echo license-present
test -f SUPPORT.md && echo support-present || echo 'SUPPORT.md absent: plan 06 creates it'
awk '/^```/{c=!c;next} !c && !/^\|/ && !/^<!--/ && !/^#/' "$P" \
  | sed -E 's/\[([^]]*)\]\([^)]*\)/\1/g; s/^- //' \
  | awk 'BEGIN{RS=""} {gsub(/\n/," "); print}' \
  | sed 's/\([.?!]\) /\1\n/g' | awk 'NF>25{print NF": "$0}'
```

Expected, in order:

- the seven headings `## Install`, `## Usage`, `## What's inside`, `## Requirements and network`, `## Boundaries`, `## License`, `## Help`;
- `description-equal`;
- a count of at least 3 (the Claude Code, Codex and Oh-My-Pi install lines);
- `1`;
- the qualified-name line once;
- `no-diary`, `no-old-names`, `all-permalinks`, `license-present`;
- `support-present` or the plan 06 note;
- no sentence over 25 words.

Install-template lines that plan 02 owns may differ in count; the test asks only that each client's line is there.

- [ ] **Step 5: Commit**

```sh
git add plugins/prose-discipline/README.md
git status --porcelain plugins/prose-discipline
git commit -m "docs: rewrite the prose-discipline README to the package template" \
  -m "The README follows the eight-section template, with generated description, install and Hermes regions. Usage shows how each client keeps the standard active, with sources. The unverified-state paragraph and the symlink and Codex passages are gone." \
  -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

---

### Task 9: Regenerate, verify every copy, and check acceptance

**Files:**
- Verify: everything under `plugins/prose-discipline/`
- Modify: only what a failing check below requires

**Interfaces:**
- Consumes: Tasks 4–8.
- Produces: the package state that plan 06 regenerates the root files from, and the size bound for plan 07's CI step.

**The size bound for plan 07.** `wc -c < plugins/prose-discipline/rules/prose-discipline.md` must print a number below `8000`. The reason is Codex's default 2,500-token spill threshold for hook `additionalContext` (`learn.chatgpt.com/docs/hooks.md` lines 536–553, research 09). It also keeps the text under Claude Code's 10,000-character hook cap. Proposed CI failure message: `plugins/prose-discipline/rules/prose-discipline.md is N bytes; keep it under 8000 so the hook text stays under Codex's default 2,500-token additionalContext threshold.` Plan 07 writes the step.

- [ ] **Step 1: Regenerate and confirm the package is at the generator's fixed point**

```sh
tools/regenerate.sh; echo "exit=$?"
git status --porcelain plugins/prose-discipline
tools/regenerate.sh && git diff --exit-code -- plugins/prose-discipline && echo package-fixed-point
```

Expected: `exit=0`; no line; `package-fixed-point`. A line in the second command means an earlier task skipped a regeneration: stage those paths and commit them in Step 5.

- [ ] **Step 2: Check every generated copy**

```sh
D=plugins/prose-discipline
cmp LICENSE "$D/LICENSE" && echo license-equal
cmp "$D/plugin.json" "$D/.claude-plugin/plugin.json" && ! test -L "$D/.claude-plugin/plugin.json" && echo vendor-equal
awk '/^<!-- rules:start -->$/{f=1;next} /^<!-- rules:end -->$/{f=0} f' "$D/skills/house-style/SKILL.md" | grep -v '^$' > "${TMPDIR:-/tmp}/pd-region.txt"
sh "$D/hooks/print-rules.sh" | grep -v '^$' | diff - "${TMPDIR:-/tmp}/pd-region.txt" && echo rules-region-equals-hook
grep -c -x -- '    - agent-plugin-prose-discipline-cf518319:house-style' "$D/README.md" "$D/skills/house-style/SKILL.md"
grep -l '^<!-- START doctoc' "$D"/skills/house-style/references/*.md
```

Expected: `license-equal`; `vendor-equal`; `rules-region-equals-hook`; `README.md:1`, and `SKILL.md:1` with Block C1 or `SKILL.md:0` with Block C2; only `…/references/examples.md`.

- [ ] **Step 3: Run the validators and syntax checks**

```sh
D=plugins/prose-discipline
/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python tools/check-conformance.py; echo "exit=$?"
claude plugin validate "$D"; echo "exit=$?"
hermes plugins validate "$D"; echo "exit=$?"
jq empty "$D/plugin.json" "$D/.claude-plugin/plugin.json" "$D/hooks/hooks.json" && echo json-ok
sh -n "$D/hooks/print-rules.sh" && echo sh-ok
```

Expected: `exit=0` three times, `json-ok`, `sh-ok`. `hermes plugins validate` becomes a CI step in plan 07. If it fails on something inside this package, fix it here. If it fails on something outside, record the output for plan 07.

- [ ] **Step 4: Check the §10 acceptance items for this package**

```sh
D=plugins/prose-discipline
grep -rniE 'not verified|has been installed|was installed|verified on' "$D" || echo no-diary
test "$(wc -c < "$D/rules/prose-discipline.md")" -lt 8000 && echo size-ok
test ! -e "$D/hooks/session-rules.sh" && test ! -e "$D/skills/prose-discipline" && echo old-paths-gone
grep -rn 'node' "$D/hooks" || echo no-node
jq -e '(.description | length) <= 250 and .extensions["io.github.akurganow.ai-plugins"].category == "Productivity"' "$D/plugin.json"
grep -x 'license: MIT' "$D/skills/house-style/SKILL.md"
test -f "$D/README.md" && test -f "$D/LICENSE" && echo readme-and-license
git status --porcelain
```

Expected: `no-diary`; `size-ok`; `old-paths-gone`; `no-node`; `true`; `license: MIT`; `readme-and-license`. The last command may list `.claude-plugin/marketplace.json` and `README.md` as modified by the generator. Those are plan 06's; report them and leave them unstaged. `CHANGELOG.md` comes from release-please's first run (plan 07), so this plan does not check for it.

- [ ] **Step 5: Commit what the checks changed**

If Steps 1–4 changed a file under `plugins/prose-discipline/`, stage those paths by name and commit:

```sh
git add <each changed path under plugins/prose-discipline/>
git commit -m "chore: regenerate the prose-discipline copies" \
  -m "The generated regions, the LICENSE copy and the vendor manifest now match their sources, as the CI regeneration check requires." \
  -m "Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>"
```

If nothing changed, there is nothing to commit. Record `package-fixed-point` in the plan's execution notes instead.

---

## Spec coverage

| Spec item | Task |
| :-- | :-- |
| §5.5 single source, size bound | 6, 9 (bound handed to plan 07) |
| §5.5 Claude Code row: hooks, shell form, plain SessionStart, JSON SubagentStart, no `node` | 7; spike 1 (Task 1) |
| §5.5 Codex row: `extensions["com.openai"].hooks`, no Codex key, README describes the route | 4, 7, 8 |
| §5.5 Oh-My-Pi row: rules file stays, no TTSR | 6, 8; spike 3 (Task 2) |
| §5.5 Hermes row: rules region in the skill, `skills.auto_load` in README and skill's first lines, computed name | 5, 8; spike 4 (Task 3) |
| §5.5 manifest paragraph: `components` deleted, `session-rules.sh` and `node` removed | 4, 7 |
| §4.1 per-manifest: description, keywords, category, prose leaves `extensions` | 4 |
| §5.1 README template | 8 |
| §5.2 LICENSE (generated) | 9 checks it |
| §5.4 references by path with "read when", real routing paths, TOC, imperative description, `license: MIT`, rename | 5, 6, 9 |
| §9 spikes 1, 3, 4 | 1, 2, 3 |
| §10 acceptance for this package | 9 |
| Quality review L5 | 6 |
| §3.1 texts removed (diary lines in README and SKILL.md) | 5, 8 |

## Open questions the spec leaves for this cluster

1. **Hermes lines in the skill.** Spec §5.5 wants the skill's first lines to show the exact `config.yaml` lines. The conventions assign `hermes-auto-load` to the README only, and plan 02's script fills only the README. This plan asks plan 02 for one more `replace_region` line and falls back to Block C2 without it.
2. **`timeout` in `hooks.json`.** Today's file sets `"timeout": 10`. Block A drops it, because the conventions list the keys exactly. The owner may want it back.
3. **Matcher.** The spec's §5.5 route column says SessionStart has "no matcher", and its ships column and the conventions give `startup|resume|clear|compact|fork`. Both match every source Claude Code documents today; the plan follows the conventions. Spike 1's 1b decides if they differ.
4. **Imperative rules and Claude Code's injection warning.** Claude Code's hooks documentation advises factual statements over imperative instructions. Block D makes the opening factual and keeps the rules imperative, because L5 forbids softening them. Spike 1 (1a-injection) shows whether that holds; if not, the owner chooses the wording.
5. **Oh-My-Pi from the marketplace before merge.** The new package cannot be installed from the marketplace until it is on `main`. Spike 3 tests the new tree through `--plugin-dir` and the marketplace route with the published 1.3.0.
6. **Hermes on Windows** (spec §9 item 4) cannot run on this macOS machine. The record says "not run", and plan 07's integration matrix covers it.
7. **Owner state during spikes.** Spikes 3 and 4 install and uninstall on the owner's Oh-My-Pi and Hermes, and spike 4 edits the Hermes config. Both restore the state they found, and the owner should know before they run.
8. **Where the per-client routes live.** §5.1 has no section for them; Block E puts them under Usage.
9. **Citation line numbers.** Research 07 cites `plugins_manifest.py` lines 79–88 for the namespace function; the file at `749220ef` has it at 60–69, as research 08 says. Block E cites 60–69.
10. **Documentation without permalinks.** Claude Code's and Codex's documentation sites offer no commit permalinks. Block E links the pages and names the section, as the root README does today; research 09 dates the reading.
