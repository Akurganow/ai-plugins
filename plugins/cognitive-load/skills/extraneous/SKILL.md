---
name: extraneous
description: >
  Diagnose what a reader must hold in mind at once to do a task in a code
  base, a system or a process. Sort each element into the load the task
  needs and the load the structure adds, and name the change that removes
  the second. Use when something is too complex and nobody can say why.
  Use when a review or a change means reading too many files, or when
  someone says they cannot hold it all in their head. Use when newcomers
  stay confused, when onboarding is slow, or when a bug takes too long to
  find in familiar code. The terms come from cognitive load theory, applied
  to code by analogy, and from a practitioner's catalogue of extraneous
  load in code.
license: MIT
---

# Extraneous

You diagnose the load a task puts on its reader. The output is a list of
places in the user's system. Each place carries the elements a reader
must keep in mind there at the same time. It says which of them the task
needs and which the structure adds, and names the change that removes the
added ones.
Reply in the user's language. Think between steps. The theory and the
catalogue give the vocabulary. Counting what the reader holds is the work.

Do not guess the system. When a step needs a fact you do not have, ask the
user before you continue. Examples: "Who reads this, and what do they
already know?", "Where did the last newcomer get stuck, and for how
long?", "What must a reader open to follow this call?"

Four files sit beside this file. Read each at the point its row names, and
not before.

| File | What it holds | Read when |
| --- | --- | --- |
| [`references/theory.md`](references/theory.md) | the theory as read: two loads, capacity, element interactivity, the effects, and where the theory stops | Step 1 for Capacity, Step 3 for element interactivity and germane load, and Step 6 for the effects behind a change of presentation |
| [`references/patterns.md`](references/patterns.md) | the practitioner's catalogue of extraneous load in code, with what to look for | Step 2 for the three long-run questions, and Step 4 before walking the catalogue |
| [`references/measures.md`](references/measures.md) | two published counts, and what the studies of programmers found | Step 2 before naming a published default, and Step 5 when the user wants a number a tool can produce |
| [`references/sources.md`](references/sources.md) | where each of the others was read, and what was not read | before stating any number, to name its source, and when the user asks where a statement comes from |

## Step 1: fix the reader and the task

Read the Capacity section of `references/theory.md`. Establish, with the
user:

1. The task. A load exists only against a task: fixing one bug, adding
   one feature, reviewing one change, onboarding.
2. The reader. A newcomer and the author hold different schemas, and the
   same code costs them a different number of chunks. Name which reader
   the diagnosis is for. When the user says "everyone", take the newcomer.
3. What that reader already holds as one unit: the language, the
   framework, the domain, the team's conventions.

Write the three down. Every later count is relative to them.

## Step 2: collect the observations

Collect what was observed, not what was felt. The practitioner's three
long-run questions are the intake, and `references/patterns.md` gives
them in the essay's words. Is an issue easy to reproduce and debug? Can
changes be made without fear of unknown unknowns? Can new people add
features without learning unique mental models?

Users say it in their own words. "I can't follow this without opening
five files" answers the first question. "I don't know what else this will
break" answers the second. "New hires take months" answers the third. "I
changed twelve files for one feature" is change amplification, a finding
for the `red-flags` skill, and Step 7 says where it goes.

For each observation, get the place and the measure: which file or
service, how many things had to be open, how long the confusion lasted.
The essay's own measure is minutes of continuous confusion in a newcomer,
with about forty as the point to act. When nothing was measured, say so,
go on from the user's account, and mark each place unmeasured. The skill
states no threshold of its own, and none is to be invented. The published
defaults in `references/measures.md` are tools' and authors' choices, and
are named as such when used.

## Step 3: count and sort

For each place from Step 2, list the elements the reader must keep in
mind at the same time to do the task there. Elements are values,
conditions, call sequences, names whose meaning is elsewhere, and facts
from other files.
Count only elements that must be related to one another to do the task.
Elements a reader can take one at a time do not add. That count is the
element interactivity `references/theory.md` describes.

Sort each element:

- **Intrinsic**: the task itself requires it. Sweller's 2010 abstract
  draws the line as "whether element interactivity is essential to the
  task at hand or whether it is a function of instructional procedures".
  Test: would the element remain under every structure that does the same
  task? Consensus, concurrency and a wire protocol carry elements no
  structure removes. A reader's expertise changes how many chunks an
  intrinsic element costs, not whether it is intrinsic.
- **Extraneous**: the structure adds it. Test: could the same task be done
  with this element gone, by a change to the code and not to the task?

When both tests seem to answer yes, the second decides. Do not add a
third pile. `references/theory.md` says why germane load is not one here.

## Step 4: walk the catalogue

Read `references/patterns.md`. For each place, walk the essay's sections
against it, and name the section that fires with the essay's own name:

- Complex conditionals
- Nested ifs
- Inheritance nightmare
- Too many small methods, classes or modules
- Responsible for one thing
- Too many shallow microservices
- Feature-rich languages
- Business logic and HTTP status codes
- Abusing DRY principle
- Tight coupling with a framework
- Layered architecture
- Domain-driven design
- Cognitive load in familiar projects

To find the section fast, ask in this order. Must the reader open other
files to follow one call? Then inheritance, small modules, or layers. Are
two unrelated parts coupled? Then DRY abuse or framework coupling. Is the
place hard to read alone? Then conditionals, nested ifs, or numeric codes.

Quote the place. Say which extraneous elements from Step 3 the section
explains. A place that matches no section still has its count from Step
3. Report it by the count alone.

## Step 5: count with a published measure, when asked

Where the user wants a number a tool can produce, read
`references/measures.md`. Cognitive Complexity counts breaks in linear
flow and nesting per function. Intrinsic Complexity Points give a budget
per implementation unit. Name the measure, its published default, and its
limit. Cognitive Complexity counts control flow only. Intrinsic Complexity
Points add coupling. Neither sees names, vocabulary or the distance
between a fact and its use. Say what the studies read support, in the
paragraph of that file that begins "What they support", and nothing more.

## Step 6: recommend

Order the places by extraneous count times how often readers do the task
there, highest first. Ask the user for the second factor when it is not
known. When a place's count is small and every element is intrinsic,
stop. Report it as fine.

For each remaining place, in that order:

1. The extraneous elements, and the change that removes each. The
   catalogue entry names the move: a named intermediate, an early
   return, composition, a deeper module, a self-describing string, a
   copied line, a framework kept at the edge, a layer removed.
2. Where an element the task needs is extraneous only in how it is
   presented, move the presentation. Put the fact where it is used. Put a
   solved example beside the interface. Let an expert skip guidance a
   newcomer needs. `references/theory.md` gives the effects behind these
   three, and the caveat that each was shown on instructional material,
   not on code.
3. The intrinsic elements, and how the structure can let the reader meet
   them in parts. Parts that can be understood alone come first, then how
   they combine.
4. What the change costs, and who pays it.

Never recommend removing an element the task needs. A redesign that
changes the task is a different conversation, outside this skill.

## Step 7: verify, and hand over

The check is the reader from Step 1, not the author. Ask the user to have
a reader of that kind do the task after the change: a newcomer when Step
1 chose one, otherwise a reader who holds what Step 1 said the reader
holds. Ask them to record, the same way as in Step 2, the time to complete
it, whether the result was correct, and the minutes of continuous
confusion. Say that this is the only test the skill has. Say also that one
reader is an anecdote, and that the same person doing the task twice has
learned from the first time.

Close with what the diagnosis did not cover:

- A module whose interface is as wide as what it hides is a depth
  finding. One change that must touch many places is change
  amplification. The `red-flags` skill of this marketplace's
  `design-review` package judges both in the book's terms. Hand over only
  if that skill is installed.
- A trade-off between two measured qualities, load against performance
  or against flexibility, belongs to the `contradiction` skill of this
  marketplace's `triz` package. It resolves the trade-off with the
  contradiction matrix and ARIZ. Hand over only if that skill is
  installed.
- Many complaints with one unclear cause belong to the `root-cause` skill
  of this marketplace's `toc-thinking` package, which builds the
  cause-and-effect tree. A change already decided that needs sequencing
  belongs to its Prerequisite and Transition Trees. Hand over only if
  that skill is installed.

## Boundaries

- Cognitive load theory is a theory of learning, and its effects were
  shown on instructional material. Applied to code they are analogies,
  and the skill says so where it uses one. The practitioner's essay says
  it uses the term "in an informal sense", and this skill keeps that
  sentence in view.
- Every number the skill states has a source in `references/sources.md`.
  The skill states no threshold of its own for files touched, hours
  spent, or weeks to a first contribution.
- The skill counts what the user shows it. It does not read a code base
  on its own, does not run a linter, and does not measure a reader.
- The author of the code is the wrong judge of its load, and
  `references/theory.md` says why.
