---
name: root-cause
description: >
  Find the core problem behind many symptoms in a software system with
  Goldratt's Theory of Constraints Thinking Processes. Then resolve the
  conflict that keeps it in place, and plan the change with its obstacles
  named. Use when symptoms are many and the cause is unclear, or when the
  same failure keeps coming back. Use when two requirements block each
  other. Use when a migration needs a plan, or when a proposed change needs
  checking before it is built. Scrutinise every link of the five logic
  trees with the published Categories of Legitimate Reservation.
license: MIT
---

# Root cause

You guide the user through Goldratt's Thinking Processes on a software
system. The procedure turns "the system is broken" into a core problem, a
resolved conflict and a sequenced plan. Reply in the user's language. Think
between steps. Do not relay a template. Reason about the system.

Do not guess the system's structure. When a step needs a fact you do not
have, ask the user before you continue. Examples: "What do you observe, and
where?", "What changed before it started?", "Which component fails first?"

Three files sit beside this file. Read each at the point its row names, and
not before.

| File | What it holds | Read when |
| --- | --- | --- |
| [`references/tools.md`](references/tools.md) | the structure of each tree and of the cloud, and how its arrows are read | before building any tree or the cloud |
| [`references/clr.md`](references/clr.md) | the eight Categories of Legitimate Reservation, with software examples | before Step 2, and whenever a link of a CRT, FRT or TT is scrutinised |
| [`references/sources.md`](references/sources.md) | the dictionary entries and book chapters the references rest on, what was not read, and what this skill adds on its own | before attributing a statement to Goldratt, Dettmer or TOCICO, and when the user asks where a statement comes from |

## The three questions and the tools

The Thinking Processes answer three questions in order. The TOCICO
Dictionary's entry *change question sequence* names them, in its first
sense.

| Question | Tool | Logic |
| --- | --- | --- |
| What to change? | Current Reality Tree (CRT) | sufficiency: *if* cause *then* effect |
| To what to change? | Evaporating Cloud (EC), then Future Reality Tree (FRT) | necessity for the cloud, sufficiency for the FRT |
| How to cause the change? | Prerequisite Tree (PRT), then Transition Tree (TT) | necessity for the PRT, sufficiency for the TT |

`references/tools.md` carries the structure of each tool and how its arrows
are read. Read it before building one.

Two kinds of check apply, and they differ by logic.

- Scrutinise a sufficiency tree (CRT, FRT, TT) with the Categories of
  Legitimate Reservation. `references/clr.md` carries them with software
  examples. Read it before Step 2. A reservation is an offer. The tree
  builder may accept it or reject it with a reason.
- Scrutinise a necessity diagram (EC, PRT) by writing out and questioning
  the assumption under each arrow.

## Step 1: classify the problem

Read the user's description and pick the entry point.

- Many symptoms, unclear cause: start with the CRT.
- Two requirements that block each other: start with the EC.
- A known change that needs a plan: start with the PRT.
- A proposed change that needs checking: start with the FRT.

When unsure, start with the CRT. State the choice and the reason to the
user in one sentence.

## Step 2: Current Reality Tree

A UDE is a complete sentence in the present tense. It states a condition
that exists, not a suspected cause. "p99 latency exceeds 5 seconds during
concurrent writes" qualifies. "The system is slow" does not. One UDE is
enough to start.

A root cause is an entity at the bottom of the tree with no cause below
it. Several may exist. The core problem is the root cause whose branches
reach most of the UDEs, including the most serious. TOCICO's guideline is
that one to three core problems account for over 70% of the UDEs. Dettmer
reports the 70% figure as Goldratt's and rejects it, because UDEs are not
equally serious. Weigh the UDEs as well as counting them.

1. Collect the UDEs from the user.
2. For each UDE, ask what condition in the system produces it.
3. Write each link as *if* cause *then* effect.
4. Join causes that are needed together with *and*.
5. Draw causes that suffice on their own as separate arrows.
6. Scrutinise every link with `references/clr.md`, level by level.
7. Show each reservation and settle the wording with the user.
8. Mark a loop: an effect that feeds a cause below it. Dettmer ranks
   removing the root cause behind a loop among the most effective changes
   (`tools.md`, Current Reality Tree).
9. Keep building down until each branch ends in a root cause.
10. Note which root causes someone within the user's reach can change.
11. When the branches do not meet, report separate root causes. Do not
    invent a common one.
12. Name the core problem and ask the user whether it matches the code.
13. Do not continue until they confirm or correct it.

## Step 3: Evaporating Cloud

A core problem usually persists because a conflict keeps it in place. The
cloud makes the conflict precise.

```
A  objective      what both sides want
B  requirement    a need that must be met to reach A
C  requirement    a second need that must be met to reach A
D  prerequisite   what is wanted to meet B
D' prerequisite   what is wanted to meet C, and cannot coexist with D
```

Read each arrow from its head: "to have A, we must have B", "to have B, we
must have D". The conflict is between D and D'. To build the cloud from
Step 2, put the practice the core problem describes in D. Put the opposite
practice in D'. Name what each practice satisfies as B and C, and what
both serve as A.

1. Fill the five boxes with the user.
2. Write the assumption under each arrow: A-B, A-C, B-D, C-D' and D-D'.
3. Ask the user to state an assumption for any arrow that has none.
4. Question each assumption. Any of the five arrows may be attacked.
5. State the injection: a condition or action that invalidates one or more
   assumptions, so that the conflict disappears.
6. Reject a compromise between D and D'. It is not an injection.

## Step 4: Future Reality Tree

Dettmer sets one reservation aside in this tree. Additional cause does not
matter here, because the question is whether the injection produces the
effect, not whether something else also could.

1. Put the injection at the bottom.
2. Build sufficiency chains upward: *if* injection *then* effect.
3. Continue until the majority of the UDEs are replaced by desired effects.
4. Look for a negative branch: a chain to a new undesirable effect.
5. Write each one out as a Negative Branch Reservation.
6. Trim it with a second injection where the branch turns negative.
7. When a serious branch cannot be trimmed, reconsider the main injection.
8. Scrutinise every link with `references/clr.md`.

## Step 5: Prerequisite Tree

1. State the objective: the injection, in place.
2. List every obstacle that blocks it today, as a condition in the system.
3. For each obstacle, state the intermediate objective that overcomes it.
4. Order the intermediate objectives: which must be reached before which.
5. Read the result as necessity: "to reach X, we must first reach Y".
6. Question the assumption under each arrow, as in Step 3.

An obstacle reads like "fifteen call sites import the module directly" or
"no transaction boundary exists around the write".

## Step 6: Transition Tree

For each intermediate objective, in the order from Step 5, write the five
elements of the tree as Dettmer reports Goldratt's later form. The
original tree had four, without the rationale.

1. The existing reality: the condition now.
2. The need: why the next state is wanted.
3. The specific action.
4. The expected effect of the action, which is the next state.
5. The rationale: why this action is needed, and why the previous effect
   was not enough.

Read it as sufficiency: *if* the existing reality *and* the action *then*
the expected effect. Scrutinise the links with `references/clr.md`.

The tree is the implementation plan. For a software change this skill adds
one line per step that TOC does not prescribe. It names how the expected
effect is observed: a command, a test or a metric. Say so when you add it.

## Boundaries

- The procedure works on facts. State each UDE as a condition someone has
  observed, with the evidence named: what the user saw, a log, a metric, a
  test. Reword an interpretation into the condition behind it.
- Iterate on the cloud with the user rather than moving on with a vague
  one.
- A tree whose links have not been scrutinised is not finished.
- A trade-off between two measurable parameters belongs to the
  `contradiction` skill of this marketplace's `triz` package. That skill
  resolves the trade-off with the contradiction matrix and hands a hard
  case to the `ariz` skill of the same package. Hand over when a cloud
  reduces to such a trade-off, and only if the `contradiction` skill is
  installed.
