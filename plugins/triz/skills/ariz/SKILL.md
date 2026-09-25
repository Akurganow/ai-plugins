---
name: ariz
description: >
  Walk a hard software problem through ARIZ-85C, Altshuller's nine-part
  algorithm of inventive problem solving, one part at a time with the
  user. Use when the contradiction matrix gave nothing the user can use,
  or when a problem keeps coming back after ordinary fixes. Use when
  several contradictions feed each other, or when a fix in one place
  breaks another. Use when every compromise between two requirements has
  failed and the conflict needs a sharper statement.
license: MIT
---

# ARIZ

You walk the user through ARIZ-85C on a software problem. The output is
the mini-problem, the physical contradiction and the solution directions
the algorithm produces. Each is written in the wording the algorithm
gives and filled from the user's system. Reply in the user's language.
Think between steps. The formulations carry the method. Filling them from
the system is the work.

Do not guess the system. When a step needs a fact you do not have, ask
the user before you continue. Examples: "Which element acts, and which is
acted upon?", "When exactly does the conflict happen?", "What does the
system already contain that nobody uses?"

Three files serve this skill. Read each at the point its row names, and
not before. The last two belong to the `contradiction` skill of this
package, and this skill reads them where they are.

| File | What it holds | Read when |
| --- | --- | --- |
| [`references/ariz-85c.md`](references/ariz-85c.md) | ARIZ-85C part by part, with the formulas quoted and a software gloss under each step | before Part 1, and again at each part as you reach it |
| [`../contradiction/references/principles.md`](../contradiction/references/principles.md) | the 40 inventive principles, with a reading of each for software | Step 2, when the user wants them tried at ARIZ step 5.3; ARIZ step 9.2, to compare the solution with them |
| [`../contradiction/references/sources.md`](../contradiction/references/sources.md) | where each reference of both skills was read, and what could not be opened | when the user asks where a formula or a step comes from |

## Step 1: take the problem in

Start from what the user brings. When the `contradiction` skill hands
the problem over, it passes the technical contradiction, the ideal final
result and the reason for the hand-over. Keep them in view. ARIZ restates
the problem in its own form in Part 1 all the same.

A problem with no contradiction in it is not an ARIZ problem. Say so
before Part 1, because ARIZ has nothing to add.

Tell the user what the reference records. Altshuller's text asks for at
least 80 academic hours of study before ARIZ is applied to a new
practical problem. The walk here is a guided substitute for that study.

## Step 2: walk the nine parts

Walk the parts in order with the user. Do not skip a part and do not
compress two into one. Write each formulation out in the wording the
reference gives, and fill it from the user's system.

- Parts 1 to 3 produce the mini-problem, the conflicting pair, the
  intensified conflict, the operative zone and time, and the resource
  list. They end with the two ideal final results and the physical
  contradiction.
- Parts 4 and 5 produce the solution directions from the resources and
  from the information fund. Step 5.3 applies the algorithm's own table of
  eleven transformations. The 40 principles may be read at 5.3 too, with
  a note that the algorithm names them only in step 9.2.
- Part 6 restates the problem when nothing came out.
- Parts 7 to 9 check the solution, generalise it and record what the walk
  taught.

Stop after any part when the user has a direction they can act on, and
say which parts were not walked.

## Step 3: hand back

- When Part 6 restates the problem as a new technical contradiction
  between two parameters, offer the `contradiction` skill of this package
  for it. The matrix may crack the restated problem in one lookup.
- When the physical contradiction from Part 3 fits a separation of later
  teaching, offer the `contradiction` skill's Step 4.

## Boundaries

- ARIZ gives directions with a published origin. They are not a
  guarantee. When a direction contradicts what the user knows about their
  system, the user's knowledge wins and the direction is dropped.
- A root cause hidden behind many symptoms belongs to the `root-cause`
  skill of this marketplace's `toc-thinking` package, which builds the
  cause-and-effect tree. Hand over when the user's problem is a tangle of
  symptoms rather than a trade-off, and only if that skill is installed.
