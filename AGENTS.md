# AGENTS.md

What an agent working in this repository reads first. **It carries no rule of
its own:** every rule below is owned by a file named beside it, and where this
file and that file disagree, that file is right and this one is stale.

## What this repository is

A public marketplace of Agent Plugins 1.0.0 packages. `README.md` owns what it
publishes and which clients it claims, `plugins/` holds the packages, and
`.claude-plugin/marketplace.json` is the catalogue index.

## Read these before changing anything

Rule files under `.agents/rules/`. None carries `paths` front matter and
each loads unconditionally, because this repository is small enough that every
rule bears on every change.

| File | Owns |
| :-- | :-- |
| `agent-plugins-review.md` | the sources of record for the marketplace's claims and the agent configuration |
| `claims.md` | what a sentence about a client may rest on, and that it cites where it was read |
| `conformance.md` | the check, what the check is allowed to be, package shape, versions |
| `design-vocabulary.md` | the words for a design objection, and the shapes in this tree that already answer one |
| `slop.md` | what generator residue looks like here, and what is protected from that judgement |
| `tests.md` | what counts as a test here, how to read the evals records, and which protections are not findings |

## The check

`tools/check-conformance.py`, and it must exit 0.
`.agents/rules/conformance.md` owns what it proves and what it needs
importable; `.github/workflows/conformance.yml` runs the same check in CI. "It
looks right" is not a result the check produced.

## This repository's own machinery

`LAWMAN.md` is the constitution the Lawman roles read here.

## Content states the action, not the instrument

A sentence here says what has to be done. Which tool does it is a fact about
an environment and belongs to whoever runs there — which is why no rule file
names an installer, an interpreter, or a route to GitHub.

## What no change does

Three prohibitions bite hardest and are the easiest to breach without meaning
to. **All three are `.agents/rules/conformance.md`'s and none of them is
stated here** — this list says only that they exist and under which heading,
so read them there before going near any of the three:

- **Versions**, on the files a release writes, which nobody edits by hand.
  `.github/workflows/release.yml` writes them.
- **The vendored schema is a copy, not a source**, on `tools/schemas/` and on
  what may replace it.
- **Text only**, on what may be committed to this repository at all.

## `CLAUDE.md`

A symlink to this file. Claude Code reads `CLAUDE.md` and every other harness
reads `AGENTS.md`; a symlink is how there comes to be one text rather than two
that drift apart. It is the same arrangement `.claude/rules` already uses for
the canonical directory `.agents/rules/`.
