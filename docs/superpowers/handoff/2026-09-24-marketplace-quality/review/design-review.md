# Design review of the spec (design-review skill, A Philosophy of Software Design)

Date 2026-09-24. Reviewed: `../../../specs/2026-09-24-marketplace-quality-design.md` after
the owner's section-by-section approval. Findings are ranked by the book's formula: how
often a part is touched, times what a touch costs.

## Frame (Step 1)

1. Under review: an architecture and refactoring plan. Its modules: six packages, the
   catalogue, the CI generation mechanisms, the `.agents/` role system, the four delivery
   routes of prose-discipline.
2. Readers: outside users and the loaders of Claude Code, Codex, Hermes, Oh-My-Pi.
   Changers: the owner, the implementer role, two release bots.
3. Most common operation (owner): a client loads a package at session start. Design
   changes: rare (owner). So load-time parts carry the weight; change-cost findings rank
   low.
4. Qualities the owner ranked already: one source with no hand copies; no paid tests;
   all four clients; a private pipeline; ready-made tools. Complexity is weighed here;
   a conflict with those goes to the trade-off section.

## Complaints brought (Step 2)

None. Every finding below was classified when found: symptom, then cause.

## Findings, in rank order (Steps 3–7)

### F1. The Hermes route has no carrier of the rules

- Place: §5.5 Hermes row; `skills/prose-discipline/SKILL.md` today (lines 13–21 name
  "this skill" as a route, and the body carries no core rule).
- Flag: Information Leakage (§5.2) once the rules are copied into `SKILL.md` by hand;
  today the route is empty. Symptom: unknown unknowns. Cause: obscurity — the spec names
  one source and says carriers are generated, but names no generated region in `SKILL.md`.
- Change: `SKILL.md` gets a region between markers filled from
  `rules/prose-discipline.md` on CI and checked the way the other copies are. Cost: one
  more generated copy; in Claude Code and Oh-My-Pi the rules then sit in context twice
  when the skill is invoked (hook or rule file, plus the skill body).
- Weight: every session in Hermes; every invocation in the other three.

### F2. One `hooks.json` for two parsers, with one client's field

- Place: §5.5 Claude Code and Codex rows: `additionalContextLimit: 0` on the SessionStart
  entry of the file Claude Code also parses.
- Flag: Special-General Mixture (§9.4). Cause: a dependency on both parsers ignoring the
  other's keys. Research: Claude Code documents ignoring unknown SKILL.md front-matter
  keys (`06-claude-code-alwayson.md` L147); nothing read says the same for `hooks.json`.
  Codex drops unknown top-level manifest fields with a warning (`06-codex-alwayson.md` L63).
- Change: spike 1 asserts that `claude plugin validate` and a session start accept the
  key. If not, Codex points at a second hooks file generated from the first. Cost: spike
  time; possibly one more generated file.
- Weight: every session in two clients.

### F3. One-word skill names are precise only under a plugin prefix

- Place: §5.4, §8 item 1.
- Flag: Vague Name (§14.3) for `review`, `audit`, `standard` where a client shows the bare
  name; Hard to Pick Name (§14.3) — two names changed at review. Cause: a dependency on
  each client's listing format. Facts: Claude Code shows `/plugin:skill`; Hermes shows
  `namespace:skill`; Oh-My-Pi lists skills by name and invokes `/skill:<name>`
  (`06-omp-alwayson.md` L276, documented); Codex listing format not read.
- Change: spike 3 (Oh-My-Pi) and spike 2 (Codex) record the exact listing of an installed
  skill. If a client shows bare names, the names are chosen again from that fact. Cost:
  a possible second rename; the one-word rule may need a second clause.
- Weight: every listing and every invocation.

### F4. A Hermes-computed identifier written into the README

- Place: §5.5 Hermes row: "the README states the working form" of
  `agent-plugin-<slug>-<sha256(key)[:8]>:<skill>`.
- Flag: Information Leakage (§5.2): Hermes's namespace scheme, keyed on the install
  source, reproduced in the package. A literal is true for one install source.
- Change: the README shows the shape and the Hermes command that prints the installed
  name; spike 4 records that command. Cost: one more step for the user.
- Weight: install time, Hermes only.

### F5. Install blocks copied by hand into six READMEs

- Place: §5.1 item 2: "commands taken from the root README".
- Flag: Repetition (§9.3): four client blocks in seven files. Also a hand-kept copy,
  which §2 forbids. A change in one client's install syntax touches seven files.
- Change: the Install section is generated from one template with the package name
  substituted, by the same marker mechanism as the description; the root README's four
  blocks come from the same template. Cost: one template file, one more generator step.
- Weight: install time; change rare.

### F6. The machine population defined in five files, with three marker names

- Place: §3.3. Today: `repo-audit-routine:` 13 occurrences, `slop-police-fingerprint:` 7,
  `agent-police-fingerprint:` 4 across `.agents/`.
- Flag: Information Leakage (§5.2): what "an issue that exists for a role" means is known
  to issue-court, tracker-clerk, pipeline-clerk, pipeline-law and github-needs. Three
  names for one concept (the naming kind of `slop.md`).
- Change: one definition, in `github-needs` (read by the four analysis roles) and cited
  from `pipeline-law` for the pipeline roles; one marker key with the role as its value;
  open issues with old markers matched until closed. Cost: the five edits happen once
  anyway; the transition rule is one sentence.
- Weight: rare; the files are 450–800 lines, so a touch costs.

### F7. Regeneration scattered over four commands

- Place: §4.1 (jq for the catalogue, jq→Markdown for the README table), §5.2 (cmp for six
  LICENSEs), §5.4 (doctoc for 21 TOCs), plus F1 and F5 if accepted.
- Principle 10, pull complexity downward (§8.2: configuration moves complexity up). A
  contributor must know which command follows which edit; forgetting one is found only
  by CI. Symptom: unknown unknowns.
- Change: one documented entry point that runs every generator (a script calling the
  ready-made tools, not a tool of its own), and CI runs that entry point followed by
  `git diff --exit-code`, whose failure message names the entry point. Cost: one file;
  tension with "no bicycles". Alternative to record: CI writes the generated files back
  (a bot commit), the literal reading of "generated on CI".
- Weight: rare.

### F8. The Codex job's allowed-to-fail mask has no expiry

- Place: §5.5 Codex row, §7.3.
- Chapter 10: masking hides the signal wanted. When upstream fixes the loader the job
  goes green silently and the mask stays.
- Change: the job asserts the current expectation (hooks absent while the issue is open)
  and fails when hooks appear, with a message that says to remove the expectation.
  Cost: a few lines.
- Weight: rare.

## Flags with a recorded reason (not re-asked)

- Overexposure (§5): the Hermes route needs the user to edit `skills.auto_load`. Owner:
  no Python, no native plugin.
- Pass-Through (§7.1): `.claude-plugin/plugin.json` symlink, two layers of one manifest.
  Owner: decided empirically by the Windows job.
- Hard to Describe (§15.3): the §5.5 table needs a paragraph per client. Inherent to four
  clients with four mechanisms.
- Special-General Mixture (§9.4): howp's exceptions (release-please, TOC, README sections,
  integration job). The spec separates them, which is the book's remedy.

## Dropped under principle 16

- "What's inside" tables expose file layout to readers. Marketplace norms ask for it
  (`03-marketplace-norms.md`).
- Rules in context twice when the skill is invoked (see F1 cost). Bounded to invocation.

## Positions and the other side (Step 8)

No finding rests on a position the book argues against common practice. F7's tension
between one entry point and "no bicycles" is a trade-off between two qualities the owner
weighs; the `triz` package is installed and can take it if wanted.

## Design it twice

Recorded alternatives asked for: §4.1 check-versus-write-back (F7); the skill names (F3),
with the client listing facts beside them.

## Decisions (owner, 2026-09-24)

- F5 accepted: spec §5.1 item 2 and §4.1 (Install generated from `tools/templates/install.md`).
- F6 accepted: spec §3.3 (one definition in `github-needs`, one marker line
  `police-fingerprint: <role> <value>`, old markers honoured until closed).
- F7 accepted: spec §4.1 (`tools/regenerate.sh`, CI runs it then `git diff --exit-code`),
  §5.2, §7.3, and `conformance.md` "Text only".
- F8 declined: the owner weighed it and kept the allowed-to-fail job as specified.
- F1 accepted, rules file stays the source: the skill body gets a generated region
  (spec §5.5). Research: `research/08-hermes-auto-load.md`.
- F2 resolved by defining the problem away: one shell-form `hooks.json`, no Codex key, a
  CI-checked size bound on the rules file; SubagentStart output corrected to JSON
  (spec §5.5). Research: `research/09-claude-codex-hooks.md`.
- F3 accepted: the naming rule adds "distinctive without the plugin prefix"; `review`,
  `audit`, `standard` became `red-flags`, `extraneous`, `house-style` (spec §5.4, §8).
  Research: `research/07-skill-names.md`.
- F4 resolved by generation: the Hermes qualified name is a function of `plugin.json`'s
  `name`, computed by `tools/regenerate.sh` into the README (spec §5.5).
- Windows symlink (§4.2, recorded-reason flag): preliminary research pending.
