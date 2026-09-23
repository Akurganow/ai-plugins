---
name: toc-thinking
description: >
  Theory of Constraints Thinking Processes for software systems: find the
  root cause behind many symptoms, resolve a dilemma between two
  requirements, and plan a change step by step with obstacles named. Use
  when symptoms are many and the cause is unclear, when the same failure
  keeps returning, when two requirements block each other, when a
  migration or refactoring needs a plan, or when a proposed change needs
  checking before it is built. Five tools, one logic check on every link.
license: MIT
---

# TOC Thinking Processes

You guide the user through Goldratt's Thinking Processes on a software
system. The procedure turns "the system is broken" into a named root cause,
a resolved conflict and a sequenced plan. Reply in the user's language.
Think between steps. Do not relay a template; reason about the system.

Do not guess the system's structure. When a step needs a fact you do not
have, ask the user for it before you continue. Examples: "What symptoms do
you observe?", "What changed before it started?", "Which component fails
first?"

## The three questions and the five tools

| Question | Tool | Logic |
| --- | --- | --- |
| What to change? | Current Reality Tree (CRT) | sufficiency: *if* cause *then* effect |
| What to change to? | Evaporating Cloud (EC), then Future Reality Tree (FRT) | necessity for the EC, sufficiency for the FRT |
| How to cause the change? | Prerequisite Tree (PRT), then Transition Tree (TT) | necessity for the PRT, sufficiency for the TT |

`references/tools.md` carries the structure of each tool. Read it before
building one.

Every cause-and-effect link, in every tree, passes the Categories of
Legitimate Reservation before it stays. `references/clr.md` carries the
eight categories with software examples. Read it before Step 2.

## Step 1: classify the problem

Read the user's description and pick the entry point.

- Many symptoms, unclear cause: start with the CRT.
- Two requirements that block each other: start with the EC.
- A known change that needs a plan: start with the PRT.
- A proposed change that needs checking: start with the FRT.

When unsure, start with the CRT. State the choice and the reason to the
user in one sentence.

## Step 2: Current Reality Tree

1. Collect undesirable effects (UDEs). Ask for five to ten. Each is an
   observable fact in the present tense, measured where possible.
   "p99 latency exceeds 5 seconds during concurrent writes" qualifies.
   "The system is slow" does not.
2. Connect the UDEs with sufficiency logic. For each UDE ask what design
   decision or condition allows it. Write the link as *if* cause *then*
   effect. Join independent causes with *and* when all are needed, and
   list them separately when any one suffices.
3. Check every link against the eight categories in `references/clr.md`.
   Mark each link pass or fail. Show the failures and fix the wording with
   the user.
4. Find the root cause: the entity at the bottom of the tree from which
   the chains lead to most of the UDEs. Dettmer's rule of thumb is that a
   cause accounting for about 70% of the UDEs is the core problem. It is
   usually a design decision, a missing boundary or a shared resource.
5. State the root cause to the user and ask whether it matches what they
   see in the code. Do not continue until they confirm or correct it.

## Step 3: Evaporating Cloud

A root cause usually persists because a conflict keeps it in place. The
cloud makes the conflict explicit.

1. Fill the five boxes with the user:

   ```
   A  objective          what both sides want
   B  requirement        needed for A
   C  requirement        also needed for A
   D  prerequisite       satisfies B, conflicts with D'
   D' prerequisite       satisfies C, conflicts with D
   ```

   Read each arrow as necessity: "to have A, we must have B", "to have B,
   we must do D". Read the bottom as a conflict: D and D' cannot both hold.
2. Surface the assumptions under each arrow. Each arrow rests on at least
   one "because". Write them out one by one.
3. Challenge each assumption. The conflict exists only while every
   assumption holds. The one that is false, or false under a condition the
   user can create, points to the injection.
4. State the injection: the change that makes the conflict disappear rather
   than a compromise between D and D'. Check it against
   `references/clr.md`.

## Step 4: Future Reality Tree

1. Put the injection at the bottom. Build sufficiency chains upward: *if*
   injection *then* effect, until each original UDE is replaced by its
   desired effect.
2. Look for negative branches: chains from the injection to a new
   undesirable effect. Write each one out as a Negative Branch Reservation.
3. Trim each negative branch with an added injection, or drop the main
   injection if a branch cannot be trimmed.
4. Check every link against `references/clr.md`.

## Step 5: Prerequisite Tree

1. State the objective: the injection, implemented.
2. List every obstacle that stops it today. Name each as a fact in the
   system: "fifteen call sites import the module directly", "no transaction
   boundary exists around the write".
3. For each obstacle, state an intermediate objective that removes it.
4. Order the intermediate objectives by dependency: which must exist
   before which. Read the result as necessity: "to reach X, we must first
   reach Y".

## Step 6: Transition Tree

For each intermediate objective, in order:

1. State the current condition.
2. State the specific action.
3. State the expected effect of the action.
4. State why the action produces that effect in this system.
5. State how the effect is verified: a command, a test run, a metric.

The result is the implementation plan. Each step has a verification gate,
and the next step starts only when the gate passes.

## Boundaries

- The procedure needs facts. Every UDE is observable in logs, metrics or
  tests. An interpretation is reworded into the fact behind it.
- The cloud is the place where breakthroughs happen. Iterate on it with the
  user until the conflict is precise.
- The logic check is part of the procedure. A tree with unchecked links is
  not finished.
- Trade-offs between two measurable parameters belong to the `triz` skill,
  which resolves them with the contradiction matrix and ARIZ. Hand over
  when the cloud reduces to such a trade-off, and only if that skill is
  installed.
