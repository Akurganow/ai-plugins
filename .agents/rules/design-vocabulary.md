# Design vocabulary

The standard is "do not complicate the code"
(`.agents/rules/conformance.md`, "What the check is allowed to be"). The
measure is what a reader must hold in mind to change a unit safely. This file
gives the `abstractions` and `proportion` departments words to point with. It
also lists the shapes in this tree that already answer a question. Their
findings are tried by it.

The code here is Python (`tools/check-conformance.py`, `tools/evals.py`), shell
(`tools/regenerate.sh`, `plugins/prose-discipline/hooks/print-rules.sh`) and
workflows (`.github/workflows/`). The words below apply to all three. An
interface is what a reader must learn to use a unit without reading it:

- a function's signature and docstring;
- a shell function's arguments and exit status;
- a script's arguments (`tools/regenerate.sh` takes none);
- a tool's subcommands (`tools/evals.py` has `matrix`, `run`, `report`,
  `validate` and `selftest`);
- a workflow's `workflow_call` inputs, secrets and job `outputs`.

## Name the symptom

An objection names one of these symptoms, or a plain term. Plain terms include
"complexity that buys nothing", "a general mechanism where a specific one would
do" and "nothing reaches it". An objection with no symptom is withdrawn.

- **Shallow module:** the interface is not much simpler than the
  implementation.
- **Pass-through method:** it forwards its arguments to a similar signature one
  layer down and adds nothing.
- **Information leakage:** one design decision is reflected in more than one
  unit, so both change together.
- **Overexposure:** the interface makes a caller learn a rare case to reach a
  common one.
- **Repetition:** a nontrivial piece is modelled in several places. Repeating a
  trivial line is not this symptom.

The `design-review` package states the first four with chapter references, in
`plugins/design-review/skills/red-flags/references/red-flags.md`. This file
keeps its own words so the court has one document to read.

## Rules of judgement

- **Dispatch is not pass-through.** A closed set whose members each do their own
  work behind one interface is the interface itself. `Claude`, `Codex` and
  `Omp` in `tools/evals.py` each define `command`, `switch_to_without` and
  `parse`. The bodies differ because each client emits a different event
  stream.
- **Deep on purpose.** A small interface over many hidden decisions is the
  goal, and a long body is not a symptom. `replace_region` in
  `tools/regenerate.sh` takes three arguments and hides marker counting, CRLF
  detection and an `awk` rewrite. `parse_frontmatter` in
  `tools/check-conformance.py` returns a dict or `None`, and its docstring
  records why it does not split on the substring `---`. `print-rules.sh` takes
  nothing or `--json`.
- **Shallow on purpose.** A block of constants with the reason beside each is a
  recalibration seam. Do not fold it into callers. The constants at the top
  of `tools/evals.py` carry comments such as the one above `JEV_MODEL`
  and the one above `NOT_APPLICABLE_ALWAYS_ON`. `MANIFEST_FIELDS` and
  `SKILL_FIELDS` in `tools/check-conformance.py` sit beside the clause they
  copy.
- **What counts as a caller.** A caller is reached from an entry point:
  - a `main` subcommand;
  - a workflow `run:` or `uses:`;
  - a hook named in `hooks.json`, or a `cog.toml` hook;
  - a command that a failure message or `CONTRIBUTING.md` tells a person to run.

  A `_selftest_*` function reaches a unit only to test it, so it does not keep
  the unit alive. The one exception is the seam in "Recorded answers", below. The
  reason for the rule: otherwise every unit with a test is alive, with the test
  as its only reader.
- **Prefer the specific mechanism** until a second caller exists. Say what a
  general one buys before proposing it.
- **Errors defined out of existence.** A design that cannot hold the bad state
  beats a check somewhere else. `tools/regenerate.sh` skips a file that has
  neither region marker, so a region takes effect once someone adds its
  markers. A lone, duplicate or reversed marker stops the run.
- **A guard is in proportion when its state can arise where the code runs.**
  To call it disproportionate, name the layer that makes the state
  impossible, with `path:line`. Without that layer the guard stands.
- **Already present means present where the code runs.** A dependency counts
  when the code's own environment provides it. A proof of misfit names the file
  that provides it. The files are:
  - the `pip install` line of `.github/workflows/conformance.yml`;
  - `tools/package.json`;
  - the tool list at the top of `tools/regenerate.sh`;
  - an `import` in the program itself.
- **A hand-written check says which of two reasons it has.** It enforces what a
  schema cannot express. Or it turns a rejection into a message someone can act
  on (`.agents/rules/conformance.md`, "What the check is allowed to be"). A check
  that says which is closed. A check that can never fire and says neither is
  text-residue's `ceremony`, never a design finding.

## Recorded answers in this tree

Shapes that read as ceremony or duplication to an outside eye, with the record
that keeps each. A finding that lands on one engages its reason or is not
filed. Every number a finding states about them is re-measured at the analysed
commit.

- **Copies of one source.** Each of these repeats a fact that lives in one
  source:
  - `plugins/<name>/.claude-plugin/plugin.json`;
  - each package's `LICENSE`;
  - the README regions between `<!-- NAME:start -->` markers;
  - `.claude-plugin/marketplace.json`;
  - the rules region of `plugins/prose-discipline/skills/house-style/SKILL.md`.

  `tools/regenerate.sh` writes every one, and `conformance.yml` fails a copy
  that differs. The records are the `docs/design.md` sections "One source for
  every copy" and "The vendor manifest is a byte copy, not a symlink". The
  section "One rules file, one documented route per client" records the rules
  region. The `cmp` hook in `cog.toml` repeats the byte check, and its comment
  says no workflow runs on the version commit. A copy edited by hand, or two
  sources for one fact, is the defect. A generated copy is not.
- **The schema duplicates, the digest and the `$id` check.** The `$schema`
  check, the closed field set, `CANONICAL_SCHEMA_ID` and the `$id` comparison
  repeat what the vendored schema says. The records are
  `.agents/rules/conformance.md`, "What the check is allowed to be", and the
  docstring of `tools/check-conformance.py`. The docstring says the `$id` check
  fires only once the digest has been updated too.
- **An evals runner of our own.** `tools/evals.py` exists beside the client's
  eval command, `claude plugin eval`. The records are its module docstring and
  `docs/design.md`, the section "Behavioural evals run after each release" and
  its paragraph "Five alternatives lost".
- **Seams for the selftest.** `grade(..., send=)`, `run_job(..., session=,
  grader=)`, `report_tag(..., file=)` and `check_folder(..., load=)` take a
  callable that production never replaces. The selftest passes a fake to each.
  The `conformance.yml` comment records that the selftest calls no model, and a
  comment above `check_folder` records its seam. These parameters have a
  non-default caller.
- **Guards with the reason beside them.**
  - `within_limit` and the `RELEASE_LIMIT, ISSUE_LIMIT` comment in
    `tools/evals.py`;
  - `doctoc_install_is_stale` in `tools/regenerate.sh`;
  - the `jq` install step and the 8000-byte step in `conformance.yml`;
  - `print-rules.sh` exiting 0 on every failure, which `docs/design.md`, "No
    hook blocks the agent", records as the package's stance.
- **Overlapping fences.** Five checks judge the same packages, each as a
  different party would:
  - the conformance check, `tools/check-conformance.py`;
  - `claude plugin validate`;
  - `skills-ref validate`;
  - `hermes plugins validate` with `hermes plugins doctor --ci`;
  - the install matrix in `integration.yml`.

  The records are `docs/design.md`, "CI checks structure and installation", the
  docstring of `check_skill_frontmatter`, and `.agents/rules/slop.md`, "The
  fence".
- **A step that reports "not run".** The step `Report the prose-discipline hook
  check as not run (Codex)` in `integration.yml` cannot fail. `docs/design.md`,
  "Codex gets its documented hook route", records why it is a notice and not an
  assertion. The court treats it as recorded.
- **A called workflow with a second entry.** `evals.yml` has one caller,
  `release.yml`, and also runs by hand through `workflow_dispatch`. The records
  are the comment above the `evals` job in `release.yml` and `docs/design.md`,
  "Behavioural evals run after each release".
- **A hash in a shell function.** `hermes_namespace` in `tools/regenerate.sh`
  computes a namespace, and its comment cites where the form was read. The
  record is `docs/design.md`, "One rules file, one documented route per
  client".
- **Ready-made tools in the regeneration script.** `jq` and `doctoc` do work a
  shell function could write. The record is `docs/design.md`, "One source for
  every copy". `run_doctoc` pins `doctoc` through `tools/package-lock.json`.

This file describes shapes in the tree. Where the tree and this file disagree,
the tree wins and this file is stale.
