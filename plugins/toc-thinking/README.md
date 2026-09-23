# toc-thinking

Goldratt's Theory of Constraints Thinking Processes, applied to software
systems and their architecture. One skill that turns many symptoms into a
named root cause, a dilemma into a resolved conflict, and a change into a
sequenced plan.

Part of the [`ai-plugins` marketplace](../../README.md).

## What it does

The skill answers the three questions the Thinking Processes were built
for, in order. The user confirms the core problem before the cloud is
built.

| Question | Tool |
| --- | --- |
| What to change? | Current Reality Tree |
| What to change to? | Evaporating Cloud, then Future Reality Tree with negative-branch reservations |
| How to cause the change? | Prerequisite Tree, then Transition Tree |

Every link in a sufficiency tree is scrutinised with the Categories of
Legitimate Reservation, and every arrow of the cloud by the assumption
under it. The agent asks for facts it does not have instead of guessing the
system's structure.

## What ships here

| Path | What it is |
| --- | --- |
| `plugin.json` | the manifest, Agent Plugins 1.0.0, at the plugin root |
| `skills/toc-thinking/SKILL.md` | the skill, per the Agent Skills specification: the procedure |
| `skills/toc-thinking/references/tools.md` | the structure of each tree and of the cloud, with its logic |
| `skills/toc-thinking/references/clr.md` | the eight Categories of Legitimate Reservation, each with a software example |
| `skills/toc-thinking/references/sources.md` | the books and pages the references were checked against |
| `README.md` | this file |
| `.claude-plugin/plugin.json` | a symlink to the root manifest, at the manifest path Claude Code documents. The root README cites the documentation |

No script, no hook, no rule file, no network, no credentials. The skill is
discovered from the fixed `skills/` location every Agent Plugins 1.0.0
client reads. That is the only route the package has.

**Nothing here has been installed from this repository as published.** The
references have been checked against the sources they cite. No client has
been pointed at this package from this repository, so the behaviour of any
particular client with it is not stated.

## Configuration

None. Removing the plugin removes the skill.

## Boundaries

- The procedure works on facts the user can observe. It does not read the
  code base on its own, and it does not replace a profiler, a debugger or a
  test.
- A trade-off between two measurable parameters is a TRIZ problem. The
  skill says so when a cloud reduces to one, and hands over to the `triz`
  package from this marketplace when it is installed.
- The books it rests on are named in
  `skills/toc-thinking/references/sources.md`. Nothing in the skill is
  attributed to Goldratt or Dettmer without a chapter or a dictionary
  entry named in that file.
