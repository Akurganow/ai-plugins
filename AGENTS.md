# AGENTS.md

What an agent working in this repository reads first. **It carries no rule of
its own:** every rule below is owned by a file named beside it, and where this
file and that file disagree, that file is right and this one is stale.

## What this repository is

A public marketplace of Agent Plugins 1.0.0 packages. `README.md` owns what it
publishes and which clients it claims, `plugins/` holds the packages, and
`.claude-plugin/marketplace.json` is the catalogue index.

## Read these before changing anything

Four rule files under `.agents/rules/`. None carries `paths` front matter and
each loads unconditionally, because this repository is small enough that every
rule bears on every change.

| File | Owns |
| :-- | :-- |
| `claims.md` | what a sentence about a client may rest on, and that it cites where it was read |
| `conformance.md` | the check, what the check is allowed to be, package shape, versions |
| `slop.md` | what generator residue looks like here, and what is protected from that judgement |
| `unattended.md` | how a run works when nobody is present to answer |

## The check

`tools/check-conformance.py`, and it must exit 0.
`.agents/rules/conformance.md` owns what it proves and what it needs
importable; `.github/workflows/conformance.yml` runs the same check in CI. "It
looks right" is not a result the check produced.

## This repository's own machinery

Nine roles, as skills under `.agents/skills/`, each with one thin Claude
binding under `.claude/agents/` that names its skills and carries no role text.
Four pipeline roles share `pipeline-law`; four analysis roles share
`github-needs`; the ninth patrols the other eight. `.agents/manifest.yaml`
declares the set and records why each arrangement is what it is.

**The routines that fire them are not in this repository and never will be.** A
routine carries the measured facts of its own environment and the clone
sequence that environment needs, because another person cloning this repository
works in an environment of their own. `unattended.md` owns that rule.

## Content states the action, not the instrument

A sentence here says what has to be done. Which tool does it is a fact about
an environment and belongs to whoever runs there — which is why no rule file
names an installer, an interpreter, or a route to GitHub.

## What no change does

Three prohibitions bite hardest and are the easiest to breach without meaning
to. **All three are `.agents/rules/conformance.md`'s and none of them is
stated here** — this list says only that they exist and under which heading,
so read them there before going near any of the three:

- **Versions**, on the three files a release job in another repository writes
  and nobody edits by hand. That section carries the owner's decision in his
  own words, quoted rather than paraphrased.
- **The vendored schema is a copy, not a source**, on `tools/schemas/` and on
  what may replace it.
- **Text only**, on what may be committed to this repository at all.

## `CLAUDE.md`

A symlink to this file. Claude Code reads `CLAUDE.md` and every other harness
reads `AGENTS.md`; a symlink is how there comes to be one text rather than two
that drift apart. It is the same arrangement `.claude/rules` and
`.claude/skills/` already use for the canonical directories under `.agents/`.
