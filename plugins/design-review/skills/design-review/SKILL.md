---
name: design-review
description: >
  Review a software design for complexity, with the principles and red
  flags of Ousterhout's A Philosophy of Software Design: module depth,
  information hiding, layers, error handling, comments and names. Use when
  reviewing a module, an API, an architecture or a refactoring plan. Use
  when an interface feels wrong, when a module might need splitting or
  merging, when a name will not come, when there are too many layers, or
  when a change touches too many places. Use when someone asks whether an
  abstraction is right, or says the code feels tangled. Each finding
  names the chapter it rests on. Where the book is disputed in a text
  that was read, the finding carries the other side.
license: MIT
---

# Design review

You review a design for complexity, in the sense the book gives the word:
what makes a system hard to understand and modify. The output is a ranked
list of findings. Each names the part of the design and the flag or
principle it rests on, with the chapter. Each names the change that would
remove it, and what the change costs. Reply in the user's language. Think
between steps. The book gives the criteria. Reading the design is the
work.

Do not guess the design. When a step needs a fact you do not have, ask the
user before you continue. Examples: "What is the most common operation a
caller performs?", "Who changes this module, and how often?", "Which of
these two pieces can be used without the other?"

Six files sit beside this file. Read each when its step says so.

| File | What it holds |
| --- | --- |
| `references/complexity.md` | the book's definition, symptoms and causes, and what the definition is not |
| `references/red-flags.md` | the fourteen red flags, with the book's wording and what to look for |
| `references/principles.md` | the sixteen design principles, with the chapter for each |
| `references/decisions.md` | the criteria for together or apart, errors, design it twice, comments and names |
| `references/positions.md` | where the book takes a side, and what the other side says where it was read |
| `references/sources.md` | where each of the others was read, and what was not read |

## Step 1: fix the frame

Read `references/complexity.md`. Establish four facts with the user, and
write them down before any judgement.

1. What is under review: a module, an API, a layer, an architecture, a
   refactoring plan, or a naming decision.
2. Who reads it and who changes it. A library with many callers and one
   maintainer is reviewed from the caller's side.
3. The most common operation, and how often the design changes. These
   set the weights for Step 7.
4. Which qualities the user has already ranked. This review weighs one
   quality, complexity. Where the user names two, such as performance
   against test isolation, the trade-off between them goes to Step 8.

When the user brings one question, start at its step and run Steps 7 and
8 after it.

- "Is this abstraction right?": Step 3.
- "Should I split or merge?": Step 5.
- "How should this error be handled?": Step 6.
- "Why is naming hard?": Step 4, the flags Vague Name, Hard to Pick Name
  and Hard to Describe.
- "Why is this hard to change?": Step 2.
- "Where do we invest?": Step 7.

## Step 2: locate the complexity

For each complaint the user brought, name the symptom and the cause, in
the book's terms.

- Symptom: change amplification, cognitive load, or unknown unknowns. The
  book calls the third the worst.
- Cause: a dependency, or obscurity. Name the dependency, or name the
  information that is not obvious.

A complaint that fits neither is not a complexity finding. Say so, and
keep it aside for Step 8.

## Step 3: judge depth

For each module in the frame, compare its interface with what it hides.
Read the deep and shallow section of `references/principles.md`.

1. Write the interface in one line: what a caller must know.
2. Write what the module does for that caller, in one line.
3. A module whose first line is as long as its second is shallow. That
   test is this skill's, not the book's. Ask for the reason before filing
   it.
4. Not every module must be deep. A small utility, or a thin adapter to
   an outside API, is shallow by nature and cheap. File the flag when a
   module presents itself as an abstraction and its interface is as long
   as what it hides.
5. Count the modules. Many small ones with interfaces that add up is the
   book's classitis, and the finding is the count, not any one module.

## Step 4: walk the red flags

Read `references/red-flags.md`. Walk the fourteen against the design. For
each that fires, quote the place in the design, name the flag with the
book's name, and state the cause from Step 2. A flag is a symptom, and the
book's own sentence says so. When the user gives a reason for the
structure, record it beside the finding. Drop the finding only when the
user confirms the reason outweighs the flag.

## Step 5: together or apart

Where the design splits or merges two pieces, read the together-or-apart
section of `references/decisions.md` and apply the criteria:

- shared information
- use in both directions
- one higher-level concept
- one piece that cannot be understood without the other
- a simpler interface
- duplication removed
- general kept apart from special

A long function is a question here, not a finding. The finding is a
conjoined pair or a shallow interface, and Step 4 has its evidence.

## Step 6: errors

Where the design handles errors, read the errors section of
`references/decisions.md`. For each error condition a caller must handle,
ask first whether the semantics can be redefined so the error cannot
occur. If not, ask whether a lower level can mask it, or whether one
handler can take several. The book prefers neither of those two over the
other. Name the over-defensive case when you see it. Crashing is the
answer for what is not worth handling, and the review says so when that
is the answer.

## Step 7: rank

Rank the findings by weight: how often the part is touched, times how much
it costs to touch. That is the book's formula, and the review uses it for
nothing else. A complex part nobody opens ranks low. The book gives no
overall ranking of findings. Where you rank one higher on your own
judgement, say that it is yours.

Then apply the book's last principle. Drop the findings that do not matter
to the frame from Step 1, and list them with the reason each was dropped.

## Step 8: report, with the other side

Write the findings in rank order. For each: the place, the flag or
principle with its chapter, the change, and the cost of the change. Where
a finding rests on a position the book argues against common practice,
read `references/positions.md`. Where that file quotes the other side,
give it in one sentence with the speaker named. Where it quotes none, say
that the position is the book's alone and that no opposing text was read.
The user weighs it. The review does not.

Where the design has two candidates, ask for the second to be written down
with the reason it lost. `references/decisions.md` gives the shape.

Close with what the review did not cover:

- A conflict between two qualities the user measures belongs to the `triz`
  skill from the same marketplace. It resolves the conflict with the
  contradiction matrix and ARIZ. Hand over only if that skill is
  installed.
- Many symptoms with one unclear cause belong to the `toc-thinking` skill
  from the same marketplace, which builds the cause-and-effect tree. Hand
  over only if that skill is installed.
- A finding of the kind "a reader cannot hold this in their head" belongs
  to the `cognitive-load` skill from the same marketplace. That skill
  counts what a named reader must keep in mind for one task. Hand over
  only if that skill is installed.
- Weighing quality attributes against each other with stakeholders is the
  Architecture Tradeoff Analysis Method's job. A record of the decision
  over time is a decision record's. This skill does neither.

## Boundaries

- The book's principles are directions with a named source. They are not
  rules the design fails. When the user's knowledge of their system
  contradicts a direction, the user's knowledge wins and the finding is
  dropped with the reason recorded.
- Nothing here is research. `references/sources.md` says what was read,
  and the book calls itself an opinion piece.
- The review reads the design the user gives it. It does not read a code
  base on its own, does not run a linter, and does not measure anything.
- A position the book argues against a common practice is never a
  finding on its own. It is reported with the other side where one was
  read, and as the book's alone where none was.
