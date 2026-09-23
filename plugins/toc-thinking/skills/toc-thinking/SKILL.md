---
name: toc-thinking
description: >
  Theory of Constraints Thinking Processes for software systems: find the
  core problem behind many symptoms, resolve a conflict between two
  requirements, and plan a change with its obstacles named. Use when
  symptoms are many and the cause is unclear, when the same failure keeps
  returning, when two requirements block each other, when a migration or
  refactoring needs a plan, or when a proposed change needs checking before
  it is built. Five logic trees, and the published reservations for
  scrutinising them.
license: MIT
---

# TOC Thinking Processes

You guide the user through Goldratt's Thinking Processes on a software
system. The procedure turns "the system is broken" into a core problem, a
resolved conflict and a sequenced plan. Reply in the user's language. Think
between steps. Do not relay a template. Reason about the system.

Do not guess the system's structure. When a step needs a fact you do not
have, ask the user before you continue. Examples: "What do you observe, and
where?", "What changed before it started?", "Which component fails first?"

## The three questions and the tools

The Thinking Processes answer three questions in order. The TOCICO
Dictionary calls them the change question sequence.

| Question | Tool | Logic |
| --- | --- | --- |
| What to change? | Current Reality Tree (CRT) | sufficiency: *if* cause *then* effect |
| To what to change? | Evaporating Cloud (EC), then Future Reality Tree (FRT) | necessity for the cloud, sufficiency for the FRT |
| How to cause the change? | Prerequisite Tree (PRT), then Transition Tree (TT) | necessity for the PRT, sufficiency for the TT |

`references/tools.md` carries the structure of each tool and how its arrows
are read. Read it before building one.

Two kinds of check apply, and they differ by logic:

- A sufficiency tree (CRT, FRT, TT) is scrutinised with the Categories of
  Legitimate Reservation. `references/clr.md` carries them with software
  examples. Read it before Step 2.
- A necessity diagram (EC, PRT) is scrutinised by writing out and
  questioning the assumption under each arrow.

## Step 1: classify the problem

Read the user's description and pick the entry point.

- Many symptoms, unclear cause: start with the CRT.
- Two requirements that block each other: start with the EC.
- A known change that needs a plan: start with the PRT.
- A proposed change that needs checking: start with the FRT.

When unsure, start with the CRT. State the choice and the reason to the
user in one sentence.

## Step 2: Current Reality Tree

1. Collect undesirable effects (UDEs). Each is a complete sentence in the
   present tense stating a condition that exists, not a suspected cause.
   "p99 latency exceeds 5 seconds during concurrent writes" qualifies. "The
   system is slow" does not. One UDE is enough to start.
2. Connect the UDEs downward with sufficiency logic. For each UDE ask what
   condition in the system produces it. Write the link as *if* cause *then*
   effect. When several causes are needed together, join them with *and*.
   When any one of several causes suffices on its own, draw them as separate
   arrows.
3. Scrutinise every link with `references/clr.md`, level by level: clarity
   first, then existence of entity and causality, then the rest. Show each
   reservation and fix the wording with the user.
4. Look for a loop: an effect that feeds a cause below it, so the situation
   reinforces itself. Draw it, and mark it. Dettmer counts removing the root
   cause behind such a loop among the most powerful changes there are.
5. Keep building down until a cause has no cause the user can change. That
   is a root cause. Several may exist. The one whose branches reach most of
   the UDEs, including the most serious, is the core problem. TOCICO's
   guideline is that one to three core problems account for over 70% of
   the UDEs. Dettmer reports the 70% figure as Goldratt's and rejects it,
   because UDEs are not equally serious. Weigh the UDEs, do not count them.
6. State the core problem to the user and ask whether it matches what they
   see in the code. Do not continue until they confirm or correct it.

## Step 3: Evaporating Cloud

A core problem usually persists because a conflict keeps it in place. The
cloud makes the conflict precise.

1. Fill the five boxes with the user:

   ```
   A  objective      what both sides want
   B  requirement    a need that must be met to reach A
   C  requirement    a second need that must be met to reach A
   D  prerequisite   what is wanted to meet B
   D' prerequisite   what is wanted to meet C, and cannot coexist with D
   ```

   Read each arrow from its head: "to have A, we must have B", "to have B,
   we must have D". The conflict is between D and D'.
2. Write the assumption under each of the five arrows, A-B, A-C, B-D, C-D'
   and D-D'. Each reads "because ...". An arrow with no assumption the user
   can state is a clarity problem in the cloud.
3. Question each assumption. Any of the five arrows may be attacked. The
   conflict exists only while every assumption holds.
4. State the injection: a condition or action that invalidates one
   assumption, so that the conflict disappears instead of being split. A
   compromise between D and D' is not an injection.

## Step 4: Future Reality Tree

1. Put the injection at the bottom. Build sufficiency chains upward: *if*
   injection *then* effect, until the majority of the UDEs from Step 2 are
   replaced by desired effects.
2. Look for negative branches: a chain from the injection to a new
   undesirable effect. Write each one out as a Negative Branch Reservation.
3. Trim each negative branch with a second injection at the point where the
   branch turns negative. When the new effect is serious and no trimming
   injection can be found, reconsider the main injection.
4. Scrutinise every link with `references/clr.md`. Dettmer sets one
   reservation aside in this tree: additional cause does not matter here,
   because the question is whether the injection produces the effect, not
   whether something else also could.

## Step 5: Prerequisite Tree

1. State the objective: the injection, in place.
2. List every obstacle that blocks it today. Name each as a condition in the
   system: "fifteen call sites import the module directly", "no transaction
   boundary exists around the write".
3. For each obstacle, state the intermediate objective that overcomes it.
4. Order the intermediate objectives: which must be reached before which.
   Read the result as necessity: "to reach X, we must first reach Y".
5. Question the assumption under each arrow, as in Step 3.

## Step 6: Transition Tree

For each intermediate objective, in the order from Step 5, write the five
elements of the tree in the form Dettmer reports from Goldratt. The
original tree had four, without the rationale.

1. The existing reality: the condition now.
2. The need: why the next state is wanted.
3. The specific action.
4. The expected effect of the action, which is the next state.
5. The rationale: why the action produces that effect in this system.

Read it as sufficiency: *if* the existing reality *and* the action *then*
the expected effect. Scrutinise the links with `references/clr.md`.

The tree is the implementation plan. For a software change this skill adds
one line per step that TOC does not prescribe: how the expected effect is
observed, as a command, a test or a metric. Say so when you add it.

## Boundaries

- The procedure works on facts. Every UDE is observable in logs, metrics or
  tests. An interpretation is reworded into the condition behind it.
- The cloud is where the conflict becomes precise. Iterate on it with the
  user rather than moving on with a vague one.
- A tree whose links have not been scrutinised is not finished.
- A trade-off between two measurable parameters belongs to the `triz` skill
  from the same marketplace, which resolves it with the contradiction matrix
  and ARIZ. Hand over when a cloud reduces to such a trade-off, and only if
  that skill is installed.
