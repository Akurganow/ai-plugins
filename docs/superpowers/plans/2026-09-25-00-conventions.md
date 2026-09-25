# Marketplace quality rework: plan conventions

Read this before writing or executing any plan under this directory. It fixes the
interfaces between the plans so that eight plan writers, working in parallel, produce
work that fits together. The spec is
`../specs/2026-09-24-marketplace-quality-design.md`; where a plan and the spec disagree,
the spec wins, and where this file and the spec disagree, the spec wins too.

Temporary, like everything under `docs/superpowers/`. Deleted before merge.

## Plans and their order

One plan per cluster of files that change together. Each plan lives at
`docs/superpowers/plans/2026-09-25-<nn>-<cluster>.md` and produces a verifiable result on
its own.

| nn | Cluster | Files it may touch | Spec | Depends on |
| :-- | :-- | :-- | :-- | :-- |
| 01 | agents | `.agents/**`, `.claude/agents/*.md` | §3, §4.2 bullet 1, §4.1 "Text only" sentence | nothing |
| 02 | tooling | `tools/regenerate.sh`, `tools/templates/*`, `tools/check-conformance.py`, generation step of `.github/workflows/conformance.yml` | §4.1, §4.2, §5.2, §7.3 first two steps | nothing |
| 03 | prose-discipline | `plugins/prose-discipline/**`, spikes 1, 3, 4 | §5.5, §5.1, §5.4, §4.1 per-manifest changes, §9 | 02 (markers, entry point) |
| 04 | howp | `plugins/howp/**` except the three release-written files | §5.3, §5.1, §5.4, §4.1 per-manifest changes | 02 |
| 05 | methods | `plugins/{design-review,cognitive-load,toc-thinking,triz}/**` | §5.1, §5.4, §4.1 per-manifest changes | 02 |
| 06 | root-docs | `README.md`, `SECURITY.md`, `CONTRIBUTING.md`, `SUPPORT.md`, `.github/ISSUE_TEMPLATE/*`, `.claude-plugin/marketplace.json` (generated) | §6, §4.1 catalogue | 02, 03–05 (names, descriptions) |
| 07 | release-ci | `release-please-config.json`, `.release-please-manifest.json`, `.github/workflows/release-please.yml`, `.github/workflows/integration.yml`, validator steps of `conformance.yml`, the how-possible issue text, spike 5 | §7, §9 spike 5 | 02–06 |
| 08 | closing | new files under `docs/`, deletion of `docs/superpowers/`, acceptance §10 | §10, cleanup paragraph | 01–07 |

Plans 01 and 02 run first and in parallel. 03, 04, 05 run after 02 and in parallel with
each other. 06 after 03–05. 07 after 06. 08 last.

## Generated regions

Every generated copy inside a hand-written file sits between two HTML comments on their
own lines:

```
<!-- <region>:start -->
…generated text…
<!-- <region>:end -->
```

The generator replaces everything between the markers and leaves the markers in place.
A file may hold several regions with different names. Region names:

| Region | File | Content |
| :-- | :-- | :-- |
| `plugins` | `README.md` | the plugin table: `| Plugin | What it does |`, one row per package, name linked to `plugins/<name>/README.md`, description from `plugin.json` |
| `description` | `plugins/<name>/README.md` | the one-sentence `description` from that package's `plugin.json`, as a paragraph under the H1 |
| `install` | `plugins/<name>/README.md` and `README.md` | `tools/templates/install.md` with `{{name}}` replaced by the package name; in the root README `{{name}}` becomes the literal `<name>` |
| `rules` | `plugins/prose-discipline/skills/house-style/SKILL.md` | the body of `plugins/prose-discipline/rules/prose-discipline.md` with its front matter stripped |
| `hermes-auto-load` | `plugins/prose-discipline/README.md` | the `config.yaml` lines for `skills.auto_load` with the computed qualified name |

Files that are whole copies carry no markers: `plugins/<name>/LICENSE` (copy of
`LICENSE`), `plugins/<name>/.claude-plugin/plugin.json` (copy of
`plugins/<name>/plugin.json`), `.claude-plugin/marketplace.json` (built by jq). Tables of
contents use doctoc's own markers (`<!-- START doctoc … -->` / `<!-- END doctoc … -->`).

## `tools/regenerate.sh`

- `#!/usr/bin/env bash`, `set -euo pipefail`, mode 100644 (no execute bit, like the
  hook script and the check), always invoked as `bash tools/regenerate.sh` from the
  repository root with no arguments, idempotent: a second run changes nothing.
- Tools it calls: `jq`, doctoc 2.2.1 installed from `tools/package.json` and
  `tools/package-lock.json` with `npm ci --prefix tools` (the lockfile pins its whole
  tree; `tools/node_modules/` is ignored), `shasum -a 256` (falls back to `sha256sum`),
  `cp`, `sed`, `awk`. When a tool is missing it exits 1 and names it.
- Steps, in this order:
  1. `.claude-plugin/marketplace.json`: `tools/templates/marketplace.json` (top-level
     `name`, `owner`, `description`) plus a `plugins` array built from every
     `plugins/*/plugin.json`, sorted by `name`, each entry
     `{name, source: "./plugins/<name>", description, homepage, category}` where
     `category` is `extensions["io.github.akurganow.ai-plugins"].category`.
  2. `plugins` region of `README.md`.
  3. Per package: `description` and `install` regions of its README; `LICENSE` copy;
     `.claude-plugin/plugin.json` copy.
  4. `install` region of the root README.
  5. doctoc over every file under `plugins/*/skills/*/references/` longer than 100 lines,
     except `plugins/howp/skills/forecast/references/commands.md`.
  6. `rules` region of the house-style skill and `hermes-auto-load` region of the
     prose-discipline README. The qualified name is
     `agent-plugin-<name>-<first 8 hex of sha256(name)>:house-style`; for
     `prose-discipline` that is `agent-plugin-prose-discipline-cf518319:house-style`.
- CI runs `bash tools/regenerate.sh`, then `git add --intent-to-add --all` and
  `git diff --exit-code`; the step's failure message says: run `bash tools/regenerate.sh`
  and commit the result. No other CI step compares a generated file. `.gitattributes`
  carries `*.sh text eol=lf` so a Windows checkout keeps the script runnable.
- The plan for 02 writes the script and the templates. Plans 03–06 add the markers to
  their files and run the script; they do not edit the script. A plan that needs a change
  in the script says so in its "Interfaces" block and the change goes into plan 02.

## `tools/templates/install.md`

Four sections, one per client, in this order: Claude Code, Codex, Oh-My-Pi, Hermes. Each
has one fenced code block with the install commands for `{{name}}` and one `Source:` line
citing the client's documentation (or source, by commit permalink, where no documentation
exists), with the kind named. The commands are the ones the root README carries today
(`README.md` lines 77–80, 117–121, 199–202, 223–226 at `37d6bdc`), with `howp` replaced
by `{{name}}`. The Hermes block keeps the `plugins/{{name}}` suffix and its one-line
explanation.

## Manifests (`plugins/<name>/plugin.json`)

- `description`: one sentence, at most 250 characters, says what the package does.
- `keywords`: no `agent-skills`.
- `extensions["io.github.akurganow.ai-plugins"].category`: `Data & Analytics` (howp),
  `Productivity` (prose-discipline), `Developer Tools` (the other four).
- howp: `extensions["io.github.akurganow.ai-plugins"].network.hosts`, an array of host
  names; no other key under that namespace. `version` is not edited.
- prose-discipline: `extensions["com.openai"].hooks = "./hooks/hooks.json"`; the
  `components`, `components_note` and `interface` keys are deleted.
- Nothing else under `extensions` anywhere.

## Skills

| Package | Directory and front-matter `name` |
| :-- | :-- |
| howp | `forecast` |
| triz | `contradiction` |
| design-review | `red-flags` |
| toc-thinking | `root-cause` |
| cognitive-load | `extraneous` |
| prose-discipline | `house-style` |

Renames use `git mv`. Front matter carries `name`, `description` (imperative voice, key
use case first, "Use when …", at most 1024 characters) and `license: MIT`. Every
reference is named from SKILL.md by relative path with a "read when" condition. A split
proposed at plan time is written into the plan as a proposal with the new one-word name,
never executed before the owner approves it.

## prose-discipline delivery

- `hooks/hooks.json`: shell form only, no `args`, no `additionalContextLimit`, top-level
  keys `description` and `hooks` only. `SessionStart` matcher
  `startup|resume|clear|compact|fork`, command
  `sh "${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh"`. `SubagentStart` (no matcher), command
  `sh "${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh" --json`.
- `hooks/print-rules.sh`: POSIX sh, `sed` and `awk` only. Without a flag it prints the
  rules body (front matter stripped) as plain text starting with the H1. With `--json` it
  prints one JSON object `{"hookSpecificOutput":{"hookEventName":"SubagentStart",
  "additionalContext":"<escaped body>"}}`. Any failure exits 0 with nothing on stdout and
  one line on stderr. `hooks/session-rules.sh` is deleted.
- `rules/prose-discipline.md` stays the single source. It is under 8,000 characters; a CI
  step checks `wc -c` against that bound and names the reason (Codex's 2,500-token spill
  threshold) in its failure message.

## `.agents/`

- The machine population is defined once, in `.agents/skills/github-needs/SKILL.md`:
  label `police-report` and a body line `police-fingerprint: <role> <value>`. Open issues
  with `repo-audit-routine:`, `slop-police-fingerprint:` or `agent-police-fingerprint:`
  count until closed. `pipeline-law` cites the definition; every other skill names "the
  machine population" and does not restate it.
- `conformance.md` "Package shape" bullet 1 and "Text only" change as spec §4.2 and §4.1
  say. Line numbers in the spec are at `232aaba`; re-read the files before editing.

## Commits

Conventional commits, one per task, because release-please reads them: `feat(<plugin>):`,
`fix(<plugin>):`, `docs:`, `chore:`, `ci:`, `refactor(<plugin>):`, with `!` for a
breaking change (a skill rename is `feat(<plugin>)!:`). Body: what changed and why, in
sentences of at most 25 words. Last line:
`Co-Authored-By: Claude Fable 5.1 <noreply@anthropic.com>`.

## Prose

Every sentence written into the repository follows
`plugins/prose-discipline/rules/prose-discipline.md`: at most 25 words, active voice, no
filler, no maintainer diary. English in files. Every sentence about a client cites its
documentation or source, by link, with the kind named; a source link is a commit
permalink. The research under `../handoff/2026-09-24-marketplace-quality/research/`
holds the citations already found; reuse them.

## Verification on this machine

- Conformance check: `/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/venv/bin/python tools/check-conformance.py`
  (an isolated environment with `jsonschema` and `pyyaml`; the system Python has neither).
  Exit 0 is the only pass.
- `claude plugin validate plugins/<name>` (Claude Code 2.1.278 is installed).
- `jq empty <file>` for every JSON file touched; `bash -n tools/regenerate.sh`;
  `sh -n plugins/prose-discipline/hooks/print-rules.sh`.
- `bash tools/regenerate.sh && git diff --exit-code` once plan 02 has landed.
- Clients installed and authorised: Codex CLI 0.155.1, Hermes 0.21.5, Oh-My-Pi 18.2.8.
  Spikes that need a clean run use a fresh environment (spec §9). Nothing in a plan
  calls a model in CI.
- Not installed: `skills-ref`, `cosign`, `release-please` CLI; `doctoc` comes from
  `tools/package-lock.json` once plan 02 lands. Plan 07 states how each of the others is
  installed, pinned.

## Plan format

Every plan follows `superpowers:writing-plans`: the header block (goal, architecture,
tech stack, global constraints copied from the spec), then tasks. A task lists its
files, its interfaces (consumed and produced), and steps with checkboxes. A step is one
action. Where a test exists it is a check that fails before the change and passes after:
the conformance check, `claude plugin validate`, `jq empty`, `git diff --exit-code`, or a
`grep` that must find or must not find a string. Every task ends with a commit step.
No placeholders: no "TBD", no "similar to task N", no "add appropriate …". A plan writer
reads the current files and quotes the exact text to change.

## What a plan writer does not do

- Change any file except its own plan file.
- Run a client session, a spike, or anything that calls a model.
- Edit the three release-written howp files, `tools/schemas/`, or anything in how-possible.
- Restate a decision the spec closed; §8 lists them.
