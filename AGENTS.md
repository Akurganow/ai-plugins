# AGENTS.md

What an agent working in this repository reads first. **It carries no rule of
its own:** every rule below is owned by a file named beside it, and where this
file and that file disagree, that file is right and this one is stale.

## What this repository is

A public marketplace of agent plugins. `README.md` owns what it publishes and
which clients it claims. `src/<name>/` holds each package's hand-written source,
and no client reads it. `tools/build.sh` writes two committed builds from it:
`bundles/<name>/`, one tree with a manifest folder per client, and
`plugins/<name>/`, an Agent Plugins 1.0.0 package. It also writes four
catalogues, which index the bundles. Everything under `bundles/` and
`plugins/` and every catalogue is a generated copy of `src/`.
`.agents/rules/conformance.md` owns the layout.

## Read these before changing anything

Rule files under `.agents/rules/`. None carries `paths` front matter and
each loads unconditionally, because this repository is small enough that every
rule bears on every change.

| File | Owns |
| :-- | :-- |
| `agent-plugins-review.md` | the sources of record for the marketplace's claims and the agent configuration |
| `claims.md` | what a sentence about a client may rest on, and that it cites where it was read |
| `conformance.md` | the check, what the check is allowed to be, source and builds, package shape, versions |
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

A file of imports only: `@AGENTS.md`, then one `@.agents/rules/<file>.md`
line per rule file. Claude Code reads `CLAUDE.md` and expands each `@path`
into the text of that file, so this file and every rule stay one text each
([memory](https://code.claude.com/docs/en/memory.md), "Import additional
files", documentation). Claude Code reads nothing under `.agents/` on its own
(same page, "When Claude Code reads AGENTS.md"), so a new rule file loads in
Claude Code only once it has its line here. Imports replaced symlinks because
the Anthropic directory's Validate does not check a symlinked file and warns
on each one.
