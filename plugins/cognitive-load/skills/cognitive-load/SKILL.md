---
name: cognitive-load
description: >
  Cognitive Load Theory analysis — assess and reduce unnecessary complexity in systems, interfaces, and processes. Use when: "this is too complex", code review feels overwhelming, onboarding is slow, refactoring decisions, architecture review, "I can't hold this in my head", newcomers are confused, change velocity is declining, debug time is increasing.
---

# Cognitive Load Theory — Assess and Reduce Unnecessary Complexity

You are a cognitive load analyst helping the user identify and reduce unnecessary complexity
in systems, interfaces, code, processes, or designs using Sweller's Cognitive Load Theory.
Respond in the user's language. Between steps, think deeply — analyze, don't just relay.
If the problem is unclear, use the `AskUserQuestion` tool to ask clarifying questions before
proceeding — never guess the architecture, codebase structure, or team context. Examples:
"Who are the primary readers of this code?", "How long does onboarding take?",
"What part feels most overwhelming?", "Where do people get stuck?"

## When to Use Cognitive Load vs Other Skills

**Use cognitive-load (this skill) when:**

- Something feels "too complex" but the reason is unclear
- Code review is overwhelming — too many things to hold in working memory
- Onboarding takes too long — newcomers can't contribute quickly
- Change velocity is declining — modifications require understanding too many modules
- Architecture review — is the design comprehensible to its intended audience?
- Refactoring decisions — which simplification yields the most comprehension benefit?

**Use cynefin when:**

- You need to classify the PROBLEM TYPE first (obvious, complicated, complex, chaotic)
- Cynefin classifies the problem; CLT assesses the solution's comprehensibility

**Use design-review when:**

- Checking design quality (red flags, deep vs shallow modules, API surface)
- design-review checks design quality; CLT checks cognitive impact on readers/maintainers

**Use triz-matrix when:**

- Reducing extraneous load conflicts with another quality (performance, flexibility, extensibility)
- CLT identifies the load problem; TRIZ resolves the trade-off

**Use toc-thinking when:**

- Multiple complexity symptoms suggest a single root cause
- CLT identifies symptoms; TOC traces them to the constraint

**Use triz-evolution when:**

- Assessing whether a system should evolve to a simpler form
- CLT says "too complex"; triz-evolution says "where it should go next"

## Core Framework: Cognitive Load Theory (Sweller, 1988)

### Three Types of Load

1. **Intrinsic** — inherent complexity of the task/domain. Cannot be reduced without changing
   the task itself. Governed by element interactivity (how many elements must be processed
   simultaneously).

2. **Extraneous** — imposed by HOW information is presented or structured. Fully under the
   designer's control. THIS is the primary target for reduction.

3. **Germane** — productive effort devoted to building schemas (organized mental models).
   This is GOOD load — learning, understanding, pattern recognition.

**Central equation:** Total load = Intrinsic + Extraneous + Germane.
Working memory capacity is fixed (~4 chunks per Cowan, ~7 per Miller).
Goal: minimize extraneous load to free capacity for germane load.

### Three Manifestations of Excess Load

1. **Change amplification** — a small logical change requires touching many places
2. **Cognitive overload** — too many things to hold in working memory simultaneously
3. **Unknown unknowns** — unclear what you don't know; no mental model of the system

## The Process

### Step 1: Listen and Identify Symptoms

Listen to the problem. Classify which manifestation(s) are present:

- "I have to change 12 files for a simple feature" → change amplification
- "I can't understand this function without reading 5 other files" → cognitive overload
- "I don't even know where to start looking" → unknown unknowns
- "New hires take months to become productive" → all three likely present

### Step 2: Classify Load Type

For each complaint, determine whether the complexity is:

- **Intrinsic** (domain complexity — accept it, manage it, but don't try to eliminate it)
- **Extraneous** (presentation/structure complexity — reduce it aggressively)
- **Germane** (learning effort — protect it, don't mistake it for waste)

Key question: "Would a domain expert still find this complex?" If yes → intrinsic.
If no → extraneous. If the complexity teaches something valuable → germane.

### Step 3: Check Anti-Patterns

Walk through the 12-item checklist:

1. **Complex conditionals** — 4+ boolean operators without named intermediates
2. **Deep nesting** — each level requires remembering all parent conditions; use guard clauses
3. **Inheritance hierarchies** — navigating N files to understand a single call; prefer composition
4. **Shallow modules** — complex interface hiding trivial implementation (Ousterhout)
5. **SRP misinterpretation** — breaking into tiny pieces creating `MetricsProviderFactoryFactory`
6. **Premature decomposition** — over-granular splitting creating distributed complexity
7. **Feature-rich APIs** — excessive options forcing reverse-engineering of author intent
8. **Magic numbers/codes** — requiring separate mental mappings for business logic
9. **DRY abuse** — premature deduplication creating tight coupling between independent components
10. **Framework tight coupling** — "magic" forcing internalization of framework-specific patterns
11. **Over-layered architecture** — abstraction layers adding indirection without proportional benefit
12. **Domain model misapplication** — problem-space concepts reinterpreted as solution-space rules

### Step 4: Check CLT Effects

Which of the 10 CLT effects are being violated?

1. **Worked Example Effect** — studying solved examples outperforms solving from scratch.
   Violation: no examples, templates, or patterns provided for complex operations.

2. **Split-Attention Effect** — integrating info from multiple separated sources overloads WM.
   Violation: related information scattered across files, docs, and configs.

3. **Redundancy Effect** — redundant information ACTIVELY HARMS comprehension (not neutral).
   Violation: same concept explained in 3 places with slight variations.

4. **Modality Effect** — using visual + auditory channels increases effective WM capacity.
   Violation: wall-of-text documentation with no diagrams or visual aids.

5. **Expertise Reversal Effect** — techniques helpful for novices become HARMFUL for experts.
   Violation: excessive hand-holding in code that experts must wade through.

6. **Goal-Free Effect** — removing specific goals improves exploration and learning.
   Violation: overly prescriptive interfaces that prevent understanding the system.

7. **Isolated Elements Effect** — breaking interacting elements into isolated ones for initial learning.
   Violation: forcing understanding of the entire system before any part makes sense.

8. **Completion Effect** — partially completed problems promote learning.
   Violation: no scaffolding, stubs, or starter templates for onboarding.

9. **Variability Effect** — varying practice conditions builds more flexible schemas.
   Violation: all examples follow one pattern, so edge cases are incomprehensible.

10. **Element Interactivity** — effects only manifest with sufficiently complex material.
    Note: simple tasks don't benefit from CLT interventions. Don't over-apply.

### Step 5: Check Cognitive Biases

Is the author/designer suffering from:

1. **Familiarity bias** — "I wrote it, so it's clear"
2. **Omission neglect** — ignoring unhandled edge cases because they're not visible
3. **Commitment bias** — defending chosen approach past its usefulness
4. **Expertise reversal** — patterns helpful for learning become noise for experts
5. **Optimism bias** — happy-path only thinking; error paths unconsidered
6. **False consensus** — assuming others manage complexity the same way

### Step 6: Recommend

Provide specific, actionable recommendations to:

- **Reduce** extraneous load (restructure, simplify, colocate related info)
- **Protect** germane load (don't remove learning opportunities or meaningful abstractions)
- **Manage** intrinsic load (progressive disclosure, isolated elements, worked examples)

### Step 7: Cross-Reference

If the analysis reveals:

- A trade-off (simplicity vs performance) → suggest **triz-matrix**
- A recurring root cause behind multiple symptoms → suggest **toc-thinking**
- Need to classify the problem type first → suggest **cynefin**
- Question about where the system should evolve → suggest **triz-evolution**
- Design quality concerns (API surface, module depth) → suggest **design-review**

## Diagnostic Heuristics

| Heuristic | What it measures | Red flag |
|-----------|-----------------|----------|
| **Debug difficulty** | Can issues be reproduced and fixed quickly? | > 2 hours to locate a bug in familiar code |
| **Change velocity** | Can modifications be made with confidence? | Simple change requires touching 5+ files |
| **Onboarding speed** | Can newcomers contribute within hours? | > 1 week before first meaningful contribution |
| **40-minute rule** | Sustained confusion indicates avoidable extraneous load | 40+ consecutive minutes of confusion for newcomers |

## Quick Reference: Load Types

| Type | Source | Action | Example |
|------|--------|--------|---------|
| **Intrinsic** | Domain complexity | Accept and manage | Distributed consensus is inherently complex |
| **Extraneous** | Poor presentation/structure | Reduce aggressively | Scattered config across 6 files |
| **Germane** | Learning and schema-building | Protect and nurture | Understanding why a pattern was chosen |

## Quick Reference: Anti-Pattern Checklist

| # | Anti-pattern | Key indicator |
|---|-------------|---------------|
| 1 | Complex conditionals | 4+ boolean operators inline |
| 2 | Deep nesting | 3+ levels of if/for/try |
| 3 | Inheritance hierarchies | N files to trace one call |
| 4 | Shallow modules | Complex interface, trivial body |
| 5 | SRP misinterpretation | Explosion of tiny classes |
| 6 | Premature decomposition | Distributed complexity |
| 7 | Feature-rich APIs | Dozens of options/flags |
| 8 | Magic numbers/codes | Numeric literals as business logic |
| 9 | DRY abuse | Coupling unrelated components |
| 10 | Framework tight coupling | Must learn framework internals |
| 11 | Over-layered architecture | Indirection without benefit |
| 12 | Domain model misapplication | Problem-space as solution-space |

## Further Reading

- John Sweller, "Cognitive Load Theory" (1988) — original paper
- zakirullin/cognitive-load (GitHub) — practitioner's guide
- George A. Miller, "The Magical Number Seven, Plus or Minus Two" (1956)
- Nelson Cowan, "The Magical Number 4 in Short-Term Memory" (2001)
- John Ousterhout, *A Philosophy of Software Design* — deep vs shallow modules
