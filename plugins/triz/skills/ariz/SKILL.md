---
name: ariz
description: >
  Walk a hard software problem through ARIZ-85C, Altshuller's nine-part
  algorithm of inventive problem solving, part by part. Use when the obvious
  fixes were tried and the problem is still there: a setting flipped back
  and forth between two teams who each hold a rule, or a fix that breaks
  something else while the next fix brings the first problem back. Use when
  the same issue keeps returning, every compromise failed, or the user
  suspects the problem is stated wrong. Use when two or three tensions are
  tied and what one choice improves makes another worse. Use when a
  contradiction-matrix lookup gave nothing usable. Use even when the
  question is short and never says TRIZ: a few failed attempts and "what is
  the way out?" count.
license: MIT
---

# ARIZ

You walk the user through ARIZ-85C on a software problem. The output is
the mini-problem, the physical contradiction and the solution directions
the algorithm produces. Write each in the wording the algorithm gives,
and fill it from the user's system. Reply in the user's language.
Think between steps. The formulations carry the method. Filling them from
the system is the work.

Do not present a guess about the system as a fact. When a step needs a
fact you do not have, draft the step from what the user said and mark the
assumed fact. Then ask for it after the draft. Examples: "Is the cache the
tool and the stale read the product?", "When exactly does the conflict
happen?", "What does the system already contain that nobody uses?"

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

Open the first reply with one sentence that gives the number. Altshuller's
text asks for at least 80 academic hours of study before ARIZ is applied
to a new practical problem, and this guided walk does not replace that
study. Write 80, not "substantial study".

## Step 2: walk the nine parts

Walk the parts in order. Do not skip a part and do not compress two into
one. Write each formulation out in the wording the reference gives, and
fill it from the user's system.

Write Part 1 whole in your first reply, steps 1.1 to 1.6. Draft it from
what the user said and mark each assumed fact. Ask for the missing facts in
one list after the draft. Never end a reply at 1.1 or 1.2: a formulation
the user can correct is worth more than a question. Write the formulations
in the same reply that carries your questions. Write each later part the
same way, whole, before you ask.

Write these in Part 1:

- Open 1.1 with "A technical system for <purpose> includes <main parts>."
  Then write TC-1 and TC-2 each as one sentence in the form IF <state of
  the tool>, THEN <good effect>, BUT <bad effect>. Use all three words.
- End 1.1 with "It is necessary, with minimum changes to the system, to
  <the required result>." Keep the words "with minimum changes".
- In 1.2 write "Tool: ..." and "Product: ..." from the user's text. Ask the
  user to correct them. Do not ask the user to supply them.
- In 1.5 write each contradiction at its limit, as "Not <the user's value>,
  but <never, always, zero or unbounded>". Use the user's own parameter,
  not the reference's cache example.
- In 1.6 write "The X-element must keep <useful action> and must remove,
  improve or provide <what the conflict demands>". Use the name X-element.

Then cover the parts in this order.

- Parts 1 to 3 produce the mini-problem, the conflicting pair, the
  intensified conflict, the operative zone and time, and the resource
  list. They end with the two ideal final results and the physical
  contradiction.
- Parts 4 and 5 produce the solution directions from the resources and
  from the information fund. Step 5.3 applies the algorithm's own table of
  eleven transformations. Read the 40 principles at 5.3 only when the
  user asks, and note that the algorithm names them only in step 9.2.
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
