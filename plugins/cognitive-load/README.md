# cognitive-load

A diagnosis of what a reader must keep in mind at the same time to do a
task in a code base, a system or a process. It is for an engineer whose
code base, system or process has become hard to read. One skill that
sorts the load into what the task needs and what the structure adds, and
names the change that removes the second. Its terms come from cognitive
load theory, read mostly as abstracts and applied to code by analogy. The
catalogue of extraneous load in code is a practitioner's essay.

Part of the [`ai-plugins` marketplace](../../README.md). Installing: the
per-client sections of the [root README](../../README.md#installing).

## What it does

The skill fixes the reader and the task first, because a load exists only
against both. Then it works in this order.

| Step | Question | Source of the vocabulary |
| --- | --- | --- |
| Observe | Where was the confusion, how long, how many things open? | the essay's three long-run questions and its measure of newcomer confusion |
| Count and sort | Which elements must be held at once, and does the task or the structure require each? | element interactivity, intrinsic and extraneous load |
| Catalogue | Which of the essay's sections explains the added elements? | the thirteen sections of "Cognitive load is what matters" |
| Measure | Which published count fits, and what does it miss? | Cognitive Complexity, Intrinsic Complexity Points |
| Recommend | Which change removes the added element, and what does it cost? | the catalogue's moves, and the theory's effects as analogies |
| Verify | Did a newcomer do the task with less confusion? | the essay's measure again, with time and correctness beside it |

The agent asks for facts it does not have instead of guessing the system,
and states no threshold of its own.

## What ships here

| Path | What it is |
| --- | --- |
| `plugin.json` | the manifest, Agent Plugins 1.0.0, at the plugin root |
| `skills/cognitive-load/SKILL.md` | the skill, per the Agent Skills specification: the procedure |
| `skills/cognitive-load/references/theory.md` | cognitive load theory as read: origin, two loads, why germane load has no action here, capacity, element interactivity, the effects, and where the theory stops |
| `skills/cognitive-load/references/patterns.md` | the essay's catalogue, section by section in its own words, with what to look for |
| `skills/cognitive-load/references/measures.md` | Cognitive Complexity and Intrinsic Complexity Points, and the studies of programmers that were read |
| `skills/cognitive-load/references/sources.md` | where each reference was read, at which commit, what was read as an abstract only, and what was not read |
| `README.md` | this file |
| `.claude-plugin/plugin.json` | a symlink to the root manifest, at the manifest path Claude Code documents. The root README cites the documentation |

No script, no hook, no rule file, no network, no credentials. The skill is
discovered from the fixed `skills/` location every Agent Plugins 1.0.0
client that supports skills reads. That is the only route the package has.

## What the references are

The essay is Artem Zakirullin's "Cognitive load is what matters", under
the Creative Commons Attribution 4.0 licence, read whole at the commit
`sources.md` names. The theory was read mostly as abstracts: the
publishers' sites were not reachable, and `sources.md` says for each paper
whether its abstract, its full text or nothing was opened. The references
say where each kind of load is attributed. Sweller's 1988 abstract names
none of the three. The theory's authors now define germane load in terms
of intrinsic load.

**Nothing here has been installed from this repository as published.** The
references have been checked against the sources they cite. No client has
been pointed at this package from this repository, so the behaviour of any
particular client with it is not stated.

## Configuration

None. Removing the plugin removes the skill.

## Boundaries

- The theory is a theory of learning, and its effects were shown on
  instructional material. The skill uses them as analogies and says so.
  The essay says it uses "cognitive load" in an informal sense, and the
  skill keeps that distinction.
- The skill counts what the user shows it. It does not read a code base
  on its own, run a linter, or measure a reader.
- A depth finding, an interface as wide as what it hides, belongs to the
  `design-review` package from this marketplace. A trade-off between two
  measured qualities belongs to `triz`. Many complaints with one unclear
  cause belong to `toc-thinking`. The skill hands over only when the
  package is installed.
