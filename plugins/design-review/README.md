# design-review

A design review for complexity, for an engineer who reviews a module, an
API, an architecture or a refactoring plan, with the principles and red
flags of John Ousterhout's *A Philosophy of Software Design*. One skill
that turns the design into a ranked list of findings. Each finding
carries the chapter it rests on, and the other side where the book is
disputed in a text that was read.

Part of the [`ai-plugins` marketplace](../../README.md). Installing: the
per-client sections of the [root README](../../README.md#installing).

## What it does

The skill fixes the frame first: what is reviewed, who reads it, who
changes it, and how often. A user with one question starts at the step
that answers it. Then it works through the book's questions in order.

| Step | Question | Criteria |
| --- | --- | --- |
| Locate | Which symptom, which cause? | change amplification, cognitive load or unknown unknowns, from a dependency or from obscurity |
| Depth | Is the interface simpler than what it hides? | deep and shallow modules, classitis |
| Flags | Which of the fourteen red flags fire? | the book's names and definitions |
| Together or apart | Should these two pieces be one? | shared information, use in both directions, one concept, one piece unreadable without the other, a simpler interface, duplication, general kept from special |
| Errors | Must a caller handle this? | define out of existence, mask, aggregate, or crash |
| Rank | Which findings matter? | the part's weight: how often it is touched, times its cost |

Every finding cites a chapter. For method length, comments and
test-driven development, the finding carries Robert Martin's reply from
his written discussion with Ousterhout. For the book's other positions,
inheritance, design patterns, accessors and small classes among them, the
finding says the position is the book's alone, because no text of the
other side was read. The agent asks for facts it does not have instead of
guessing the design.

## What ships here

| Path | What it is |
| --- | --- |
| `plugin.json` | the manifest, Agent Plugins 1.0.0, at the plugin root |
| `skills/design-review/SKILL.md` | the skill, per the Agent Skills specification: the procedure |
| `skills/design-review/references/complexity.md` | the book's definition of complexity, its symptoms and causes, and how it differs from Brooks' |
| `skills/design-review/references/red-flags.md` | the fourteen red flags, the book's wording, and what to look for |
| `skills/design-review/references/principles.md` | the sixteen design principles of the second edition, with a chapter for each |
| `skills/design-review/references/decisions.md` | the criteria for together or apart, errors, design it twice, comments and names |
| `skills/design-review/references/positions.md` | where the book takes a side, with the other side quoted where it was read, and what evidence was read |
| `skills/design-review/references/sources.md` | where each reference was read, at which commit, and what was not read |
| `README.md` | this file |
| `.claude-plugin/plugin.json` | a symlink to the root manifest, at the manifest path Claude Code documents. The root README cites the documentation |

No script, no hook, no rule file, no network, no credentials. The skill is
discovered from the fixed `skills/` location every Agent Plugins 1.0.0
client reads. That is the only route the package has.

## What the references are

The book is copyrighted and no copy was bought. The two lists it ends
with, sixteen principles and fourteen red flags, were read verbatim from
three public copies that agree. The chapter passages quoted are a few
sentences at most, from two public translation repositories that carry
the English. `sources.md` names each copy by commit. The second edition
lists sixteen principles and the first lists fifteen, and the references
say which is which.

**Nothing here has been installed from this repository as published.** The
references have been checked against the sources they cite. No client has
been pointed at this package from this repository, so the behaviour of any
particular client with it is not stated.

## Configuration

None. Removing the plugin removes the skill.

## Boundaries

- The review weighs one quality, complexity in the book's sense. A
  trade-off between two measured qualities belongs to the `triz` package
  from this marketplace. Many symptoms with one unclear cause belong to
  `toc-thinking`. What a reader can hold in their head belongs to
  `cognitive-load`. The skill hands over only when the package is
  installed.
- The book's positions on method length, comments and test-driven
  development are reported with Martin's reply beside them. Its
  positions on inheritance, design patterns, accessors and small classes
  carry no reply, because no text of the other side was read.
  `positions.md` says what evidence was read, which is little, and
  `sources.md` lists the studies that were not.
- The skill reads what the user gives it. It does not read a code base on
  its own and does not measure anything.
