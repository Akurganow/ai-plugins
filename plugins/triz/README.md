# triz

TRIZ for engineering trade-offs in software. One skill with two routes.
The contradiction matrix serves a trade-off that can be named in two
parameters. ARIZ-85C serves a problem the matrix did not crack.

Part of the [`ai-plugins` marketplace](../../README.md).

## What it does

The short route:

- restates the user's problem as a contradiction
- writes the ideal final result
- maps the two sides to Altshuller's 39 engineering parameters
- reads the classic contradiction matrix for the principles it recommends
- states each principle as a change to the user's system

A physical contradiction, where one element must have two opposite
properties, goes to the four separation principles instead.

The long route is ARIZ-85C, Altshuller's algorithm of 1985. The skill walks
it part by part with the user, from the mini-problem to the analysis of
the walk itself, in the wording the algorithm gives.

## What ships here

| Path | What it is |
| --- | --- |
| `plugin.json` | the manifest, Agent Plugins 1.0.0, at the plugin root |
| `skills/triz/SKILL.md` | the skill, per the Agent Skills specification: the procedure |
| `skills/triz/references/parameters.md` | the 39 parameters, each with a reading for software |
| `skills/triz/references/principles.md` | the 40 principles, each with Altshuller's sub-items and a reading for software |
| `skills/triz/references/matrix.md` | the classic matrix, one line per cell, with its provenance and the cells the transcriptions dispute |
| `skills/triz/references/ariz-85c.md` | the nine parts and forty steps of ARIZ-85C, with the formulas quoted |
| `skills/triz/references/sources.md` | where each reference was read from, at which commit, and what was not read |
| `README.md` | this file |
| `.claude-plugin/plugin.json` | a symlink to the root manifest, at the manifest path Claude Code documents. The root README cites the documentation |

No script, no hook, no rule file, no network, no credentials. The matrix
is a text file the agent searches for one line, so nothing has to be
installed for the lookup. The skill is discovered from the fixed `skills/`
location every Agent Plugins 1.0.0 client reads. That is the only route
the package has.

## What the matrix here is

The classic 39-by-39 matrix, with 1,248 non-empty cells. It was not copied
from one file. Two public transcriptions were compared cell by cell. The
40 cells where they differ were settled by majority against a third and a
fourth. Every disputed cell is listed in `matrix.md` with every reading.
The often-quoted count of 1,263 cells was not confirmed. No transcription
that could be reached is a scan of a printed edition. `sources.md` names
each copy and the commit it was read at.

**Nothing here has been installed from this repository as published.** The
references have been checked against the sources they cite. No client has
been pointed at this package from this repository, so the behaviour of any
particular client with it is not stated.

## Configuration

None. Removing the plugin removes the skill.

## Boundaries

- The matrix and the principles are directions with a published origin,
  not a guarantee. The user's knowledge of their system decides which
  direction survives.
- A problem with no trade-off in it is not a TRIZ problem.
- The software readings of the parameters and the principles are this
  skill's own, and `sources.md` says so. No published mapping of the 39
  parameters to software was found. No study that measures the classic
  matrix on software problems was found either. Of Altshuller's text, the
  package quotes the Russian formulas in `ariz-85c.md` and the English
  Table 2 and three steps. `principles.md` paraphrases his sub-items from a
  third-party transcription.
- A tangle of symptoms with no trade-off in sight belongs to the
  `toc-thinking` package from this marketplace, and the skill says so when
  it is installed.
