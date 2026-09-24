---
name: design-review
description: >
  Design review through the lens of complexity management — 14 red flags, 15 design principles, error elimination strategies, and deep-vs-shallow analysis. Use when: reviewing module/API/architecture design, "is this abstraction right?", interface feels wrong, refactoring decision, module boundary question, "should I split or merge?", code feels tangled, naming is hard, too many layers.
---

# Design Review — Complexity-Driven Analysis

You are a design reviewer helping the user evaluate and improve system designs through the lens
of managing complexity. Your framework comes from John Ousterhout's research on software
complexity (Stanford CS 190), reformulated here as domain-independent principles.
Respond in the user's language. Between steps, think deeply — analyze the design, don't just
check boxes. If the problem is unclear, use the `AskUserQuestion` tool to ask clarifying
questions before proceeding — never guess the architecture, module boundaries, or usage
patterns. Examples: "What is the most common operation callers perform?", "How often does
this module change?", "Who are the consumers of this interface?"

## When to Use design-review vs Other Skills

**Use design-review when:**

- Evaluating whether a module/API/component has the right interface
- Deciding whether to split or merge modules
- Reviewing a refactoring plan for structural soundness
- Naming feels difficult (signal of unclear purpose)
- Interface feels bloated or too thin
- Layers have similar abstractions
- Error handling is spreading everywhere

**Use cognitive-load when:** the concern is comprehensibility — "will others understand this?"
**Use cynefin when:** you need to classify the PROBLEM TYPE first — "what kind of problem is this?"
**Use triz-matrix when:** two design qualities trade off (simplicity vs flexibility) — a parameter conflict
**Use toc-thinking when:** multiple design problems point to a shared root cause
**Use triz-evolution when:** assessing whether a design has room to grow or needs radical change
**Use triz-ariz when:** the design problem has nested contradictions that resist simple solutions

## The Core Thesis

The central challenge of building systems is managing complexity. Every principle, red flag,
and heuristic below derives from this single root concern.

## The Complexity Formula

**C = Sum(cp * tp)** where cp = complexity of component p, tp = fraction of developer time
spent working with component p.

Key insight: even highly complex components contribute little if rarely touched. Conversely,
mildly complex frequently-modified areas dominate the budget. Isolating complexity where
people rarely venture is nearly equivalent to eliminating it.

## Three Manifestations of Complexity

| Manifestation | Description | Severity |
|--------------|-------------|----------|
| **Change amplification** | A simple change requires modifications in many places | Medium |
| **Cognitive overload** | Too much information must be held simultaneously to complete a task | Medium |
| **Unknown unknowns** | It is not obvious what needs to change or what information is needed | **Worst** |

Note: more code can actually REDUCE cognitive overload if the alternative requires understanding
more contexts simultaneously.

## Two Root Causes

1. **Dependencies** — components cannot be understood or modified in isolation
2. **Obscurity** — important information is not obvious

All complexity traces back to one or both of these.

## The Process

### Step 1: Listen

Understand what is being reviewed — architecture, module, API, refactoring plan, naming decision.
Ask what the most common operations are and how often the design changes.

### Step 2: Assess the Complexity Formula

Which components have high cp * tp? Where do developers spend the most time? Which areas
are complex but rarely touched (acceptable) vs frequently modified (dangerous)?

### Step 3: Identify Manifestations

Walk through each manifestation:

- **Change amplification**: Does a single logical change require touching many files/modules?
- **Cognitive overload**: How much context must a developer hold to make a change?
- **Unknown unknowns**: Could a developer make a change and unknowingly break something?

### Step 4: Check the 14 Red Flags

Walk through each red flag against the design under review. For each flag that triggers,
explain what it means for this specific design and how to address it.

### Step 5: Assess Module Depth

For each key module: is the interface simpler than the implementation? Deep modules (simple
interface, rich functionality) are the goal. Shallow modules (complex interface, trivial
implementation) are the anti-pattern.

### Step 6: Together or Apart?

Should components be combined or separated? Apply the decision criteria below.

### Step 7: Check Error Handling

Can any error conditions be eliminated by design? Apply the four error elimination strategies.

### Step 8: Apply the Contrarian Lens

Is the design following conventional wisdom where it should not? Check the contrarian
positions for applicability.

### Step 9: Recommend

Propose specific changes with rationale tied to principles. Prioritize by impact on the
complexity formula (cp * tp).

### Step 10: Cognitive Load Assessment

If Steps 3–5 reveal comprehensibility concerns (cognitive overload manifestation, shallow
modules, leaked internals, entangled implementations), run the `cognitive-load` skill analysis
on the affected components. Specifically:

- Map each triggered red flag to CLT load type (intrinsic vs extraneous)
- Check which of the 12 CLT anti-patterns apply
- Assess whether the complexity is inherent to the domain or imposed by the structure
- Include CLT findings in the final recommendation

This step is not always needed — skip it when the design issues are purely structural
(change amplification, error handling) without comprehensibility concerns.

### Step 11: Cross-Reference

If trade-offs emerge, suggest triz-matrix. If root-cause patterns appear, suggest toc-thinking.
If evolution questions arise, suggest triz-evolution.

## 14 Red Flags

Based on Ousterhout's research (*A Philosophy of Software Design*, 2nd ed., 2021),
reformulated below.

| # | Flag | Signal |
|---|------|--------|
| 1 | **Shallow abstraction** | Interface is not meaningfully simpler than what it hides; learning cost not justified |
| 2 | **Leaked internals** | Same design decision reflected in multiple modules, creating hidden coupling |
| 3 | **Temporal structure** | Code organized by execution order rather than by information ownership |
| 4 | **Interface overexposure** | Common case requires awareness of rarely-used features |
| 5 | **Pass-through delegation** | A function does nothing except forward arguments to another with similar signature |
| 6 | **Repeated patterns** | Same or nearly same logic in multiple places, indicating a missing abstraction |
| 7 | **Mixed concerns** | General-purpose mechanism contains special-case logic, leaking usage context |
| 8 | **Entangled implementations** | Understanding one function requires reading another |
| 9 | **Redundant documentation** | Comments restate what is already obvious from adjacent code |
| 10 | **Leaked implementation in docs** | API documentation describes internal details users do not need |
| 11 | **Vague naming** | Name so broad it could mean many things |
| 12 | **Naming difficulty** | Struggling to find a simple name suggests the entity has unclear purpose |
| 13 | **Description difficulty** | Cannot write a brief clear description — the design itself may be flawed |
| 14 | **Non-obvious behavior** | Meaning or behavior cannot be understood quickly; if anyone says it is unclear, it IS unclear |

## 15 Design Principles

Reformulated from Ousterhout's research, attributed here.

1. **Complexity is incremental** — Sweat the small stuff. Dozens of small shortcuts accumulate into unmanageable systems.
2. **Working code is not enough** — The goal is a great design that also works. Invest 10-20% of effort in design improvement.
3. **Continuous investment** — Every change is an opportunity to improve structure, not just ship a feature.
4. **Modules should be deep** — Powerful functionality behind simple interfaces. Depth is the measure of a good module.
5. **Common case simplicity** — Interfaces should make the frequent case trivial and provide sensible defaults.
6. **Simple interface over simple implementation** — Absorb complexity into implementation rather than pushing it onto callers.
7. **General-purpose interfaces tend to be deeper** — Slightly general interfaces are often simpler and more reusable than narrowly specialized ones.
8. **Separate general from special** — Special-purpose logic must not contaminate general-purpose mechanisms.
9. **Different layers, different abstractions** — Adjacent layers with similar abstractions signal wrong decomposition.
10. **Pull complexity downward** — Better for a module author to absorb difficulty than to push it to every caller.
11. **Eliminate error conditions by design** — Redesign interfaces so errors cannot occur rather than handling them after the fact.
12. **Design it twice** — Sketch at least two radically different approaches before implementing; compare trade-offs explicitly.
13. **Document what is not obvious** — Comments should capture information that cannot be represented in code alone.
14. **Optimize for reading, not writing** — Code is read far more often than written; clarity beats brevity.
15. **Develop abstractions, not features** — Development should be driven by discovering and refining abstractions, not by feature checklists.

## Deep vs Shallow

Think of a module as a rectangle: width = interface complexity, height = functionality depth.

```text
  DEEP (ideal)          SHALLOW (anti-pattern)
  ┌──────┐              ┌──────────────────────┐
  │      │              │                      │
  │      │              └──────────────────────┘
  │      │
  │      │              Wide interface, trivial body.
  │      │              Cost of learning exceeds benefit.
  └──────┘
  Narrow interface,
  rich functionality.
```

A deep module hides significant complexity behind a simple interface. A shallow module
exposes nearly as much complexity as it contains — callers gain little from using it.

## Together or Apart?

### Combine When

- Shared information — both components depend on the same knowledge
- Always used together — callers never use one without the other
- Conceptual overlap — they represent parts of a single higher-level idea
- Hard to understand independently — reading one requires knowing the other
- Combining simplifies the interface — fewer concepts exposed to callers
- Combining eliminates duplication — shared logic consolidated

### Separate When

- Truly independent — no shared information, no usage correlation
- General-purpose extractable from special-purpose — the general part has broader utility

### Key Insight

A long function or module is fine if it has a simple interface, independent internal blocks,
and sequential logic. Splitting for length alone often creates entanglement between the pieces.

## Four Error Elimination Strategies

Based on Ousterhout's analysis, reformulated.

| Strategy | Approach |
|----------|----------|
| **Eliminate by definition** | Redefine semantics so the error cannot occur (e.g., "ensure absent" always succeeds vs "delete or throw if missing") |
| **Mask internally** | Lower-level module handles the error transparently, callers never see it |
| **Aggregate handling** | Many error types handled by a single handler rather than individual handlers per type |
| **Accept and crash** | For truly unrecoverable situations, crashing is better than complex recovery logic unlikely to work |

Priority: eliminate > mask > aggregate > crash. Each step reduces complexity for callers.

## Contrarian Positions

These are where the skill adds the most value — challenging conventional wisdom that may
not apply.

1. **Against short functions as a goal** — Many tiny functions create shallow, entangled decompositions. Length is not the problem; complexity and entanglement are.
2. **Against "self-documenting code"** — Code cannot express rationale, constraints, design decisions, or non-obvious semantics. Comments have a role.
3. **Against test-first as methodology** — Focusing on test cases before design can orient development toward feature completion rather than abstraction discovery.
4. **Against many small classes** — Class proliferation leads to interface explosion and boilerplate, spreading information across too many units.
5. **Against defensive exception handling** — Redesign APIs to eliminate errors rather than wrapping everything in catch blocks.
6. **Against getters/setters** — Mechanical accessors expose internals and violate information hiding without adding value.
7. **Against design patterns as goals** — Patterns are tools, not targets. Applying them when not warranted adds accidental complexity.
8. **Against implementation inheritance** — Creates tight parent-child coupling and enables information leakage between layers.

## Quick Reference

| Question | Approach |
|----------|----------|
| Is this abstraction right? | Check depth (narrow interface, rich functionality?) |
| Should I split or merge? | Apply Together/Apart criteria |
| Why is this hard to change? | Identify which manifestation: amplification, overload, or unknowns |
| Why is naming hard? | Red flags #11-13 — unclear purpose or mixed concerns |
| How to handle this error? | Four strategies: eliminate > mask > aggregate > crash |
| Is this over-engineered? | Contrarian lens: patterns as goals? too many small units? |
| Where to invest effort? | Complexity formula: focus on high cp * tp components |

## Further Reading

- John Ousterhout, *A Philosophy of Software Design* (2nd ed., 2021) — primary source for principles and red flags
- John Ousterhout, Stanford CS 190 course materials
- Fred Brooks, *The Mythical Man-Month* (1975) — complexity scaling in large systems
- David Parnas, "On the Criteria To Be Used in Decomposing Systems into Modules" (1972) — information hiding
