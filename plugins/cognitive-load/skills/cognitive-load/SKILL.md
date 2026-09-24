---
name: cognitive-load
description: >
  Find what a reader must hold in working memory to do a task in a code
  base, a system or a process, sort it into the load the task needs and
  the load the structure adds, and name the change that removes the
  second. Grounded in cognitive load theory as published and a
  practitioner's catalogue of extraneous load in code. Use when something
  is too complex and nobody can say why, when a review or a change means
  reading too many files, when newcomers stay confused, or when a bug
  takes too long to locate in familiar code.
license: MIT
---

# Cognitive load

You diagnose the load a task puts on its reader. The output is a list of
places in the user's system. Each place carries the elements a reader
must hold there, which of them the task needs, which the structure adds,
and the change that removes the added ones. Reply in the user's language. Think
between steps. The theory and the catalogue give the vocabulary. Counting
what the reader holds is the work.

Do not guess the system. When a step needs a fact you do not have, ask the
user before you continue. Examples: "Who reads this, and what do they
already know?", "Where did the last newcomer get stuck, and for how
long?", "What must a reader open to follow this call?"

Four files sit beside this file. Read each when its step says so.

| File | What it holds |
| --- | --- |
| `references/theory.md` | the theory as read: two loads, capacity, element interactivity, the effects, and where the theory stops |
| `references/patterns.md` | the practitioner's catalogue of extraneous load in code, with what to look for |
| `references/measures.md` | two published counts, and what the studies of programmers found |
| `references/sources.md` | where each of the others was read, and what was not read |

## Step 1: fix the reader and the task

Read the first sections of `references/theory.md`. Establish, with the
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

For each observation, get the place and the measure: which file or
service, how many things had to be open, how long the confusion lasted.
The essay's own measure is minutes of continuous confusion in a newcomer,
with about forty as the point to act. No other threshold is stated
anywhere in this skill, and none is to be invented.

## Step 3: count and sort

For each place from Step 2, list the elements the reader must hold at the
same time to do the task there: values, conditions, call sequences, names
whose meaning is elsewhere, facts from other files. That count is the
element interactivity `references/theory.md` describes.

Sort each element:

- **Intrinsic**: the task itself requires it. Test: would a reader who
  holds the domain as one schema still have to carry this element?
  Consensus, concurrency and a wire protocol carry elements no structure
  removes.
- **Extraneous**: the structure adds it. Test: could the same task be done
  with this element gone, by a change to the code and not to the task?

Do not add a third pile. `references/theory.md` says why germane load is
not one here.

## Step 4: walk the catalogue

Read `references/patterns.md`. For each place, walk the essay's sections
against it: complex conditionals, nested ifs, inheritance, too many small
modules, one-thing responsibility, shallow microservices, feature-rich
languages, numeric codes for business meanings, DRY abuse, framework
coupling, layered architecture, domain-driven design as folder structure,
familiarity mistaken for simplicity. Name the section with the essay's
name. Quote the place. Say which extraneous elements from Step 3 it
explains.

A place that matches no section still has its count from Step 3. Report
it by the count alone.

## Step 5: count with a published measure, when asked

Where the user wants a number a tool can produce, read
`references/measures.md`. Cognitive Complexity counts breaks in linear
flow and nesting per function; Intrinsic Complexity Points give a budget
per class. Name the measure, its published default, and its limit. Both
count control flow and coupling. Neither sees names, vocabulary or the
distance between a fact and its use. Say what the studies read
support, in the three sentences that file ends with, and nothing more.

## Step 6: recommend

For each place, in the order of the count from Step 3, highest first:

1. The extraneous elements, and the change that removes each. The
   catalogue entry names the move: a named intermediate, an early
   return, composition, a deeper module, a self-describing string, a
   copied line, a framework kept at the edge, a layer removed.
2. The intrinsic elements, and how the structure can sequence them so the
   reader meets fewer at once: a worked example beside the interface, the
   facts a reader needs placed where they are used, guidance a newcomer
   reads and an expert can skip. `references/theory.md` gives the effects
   these come from and the caveat that each was shown on instructional
   material, not code.
3. What the change costs, and who pays it.

Never recommend removing an element the task needs. A redesign that
changes the task is a different conversation, and Step 7 says where it
goes.

## Step 7: verify, and hand over

The check is the reader from Step 1, not the author. Ask the user to have
a newcomer do the task after the change and to measure confusion the
same way as in Step 2. Say that this is the only test the skill has.

Close with what the diagnosis did not cover:

- A module whose interface is as wide as what it hides is a depth
  finding, and the `design-review` package of this marketplace measures
  it. This skill hands over only if that package is installed.
- A trade-off between two measured qualities, load against performance
  or against flexibility, belongs to the `triz` package, on the same
  condition.
- Many complaints with one unclear cause belong to the `toc-thinking`
  package, on the same condition.

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
- The author of the code is the wrong judge of its load. The skill says
  so once and does not repeat it.
