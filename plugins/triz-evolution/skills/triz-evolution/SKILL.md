---
name: triz-evolution
description: >
  TRIZ evolution laws — predict how any system, process, or design will naturally develop next. Use when: planning next steps, assessing maturity or readiness, deciding where to invest effort, modernization strategy, "what should we improve next?", roadmap decisions, evaluating if a solution has room to grow, tech debt prioritization.
---

# TRIZ Evolution: Laws of Technical System Evolution

Respond in the user's language. Between steps, think deeply — analyze, don't just relay.
If the system or its context is unclear, use the `AskUserQuestion` tool to ask clarifying
questions before assessing — never guess the architecture, scale, or constraints. Examples:
"Is this a monolith or distributed?", "What's the main pain point?", "Who are the users?"

## Overview

This skill helps you **predict where a technical system is headed** based on TRIZ's proven laws of evolution. Every system—whether it's a monolith, API, database, or entire platform—evolves along predictable paths.

**Key insight:** Evolution is not random. Nine universal laws govern how systems change:

1. **Completeness of Parts** — all systems need engine, transmission, working body, control
2. **Energy Conductivity** — energy/data must flow freely without blockages
3. **Harmonization of Rhythms** — all parts must work in temporal harmony
4. **Increasing Ideality** — function delivered with minimal cost, size, complexity
5. **Uneven Development** — parts evolve at different rates, creating contradictions
6. **Transition to Super-system** — systems become components in larger systems
7. **Macro to Micro** — from monolith to microservices to serverless to distributed agents
8. **Increasing Dynamism** — rigid → configurable → adaptive → self-organizing
9. **Complexity then Simplification** — growth → peak complexity → simplification

Use this skill to:

- Assess where your system sits on each evolution curve
- Predict the next evolutionary step (e.g., monolith → microservices → serverless)
- Identify bottlenecks, imbalances, and contradictions
- Plan architecture roadmaps with confidence
- Cross-reference with triz-matrix when evolution reveals contradictions

---

## How to Use This Skill

### 1. Understand Your System

Start by clarifying what system we're analyzing:

- Is it a monolith, microservice, or distributed system?
- What's the current architecture? (API, database, message queue, etc.)
- Who uses it? (Internal team, customers, both?)
- What's the biggest pain point?

### 2. Assess Against Evolution Laws

For each of the 9 laws, answer the diagnostic questions:

#### Law 1: Completeness of Parts

- Does the system have all four components: power, transmission, working body, control?
- Which is weakest?
- Can it function independently?

#### Law 2: Energy Conductivity

- Where does data get blocked or slow down?
- Are there synchronous operations that should be async?
- Does the system degrade under load, or does it fail catastrophically?

#### Law 3: Harmonization of Rhythms

- Do all components operate at compatible throughput rates?
- Are there timing mismatches (slow DB with fast API)?
- Cascading failures, or graceful degradation?

#### Law 4: Increasing Ideality

- What's the ratio of core function to operational overhead?
- How much effort is spent on running the system vs. delivering value?
- Could it be a managed service or serverless function?

#### Law 5: Uneven Development of Parts

- Which parts advance fast, which lag?
- Version conflicts? API mismatches? Inconsistent patterns?
- Is tech debt rooted in uneven evolution?

#### Law 6: Transition to Super-system

- Is this a standalone product or platform component?
- How well does it integrate with other systems?
- Should optimization happen at system or platform level?

#### Law 7: Macro to Micro

- Monolith or distributed?
- Can smaller pieces be deployed/scaled independently?
- Would serverless or edge functions improve metrics?

#### Law 8: Increasing Dynamism

- How much manual control is required?
- Can behavior change without redeployment?
- Hardcoded, config files, env vars, feature flags, or adaptive?

#### Law 9: Complexity then Simplification

- Where on the curve: early, growing, peak, simplifying, or simplified?
- Time spent on new features vs. tech debt?
- Opportunities to refactor or simplify?

### 3. Identify Relevant Patterns

Eight evolution patterns cross-cut the laws. Assess your system against:

- **Mono-Bi-Poly** — single element → dual → multiple → diverse
- **Increasing Segmentation** — solid → hollow → porous → powder → field
- **Trimming** — removing waste while preserving function
- **Increasing Use of Fields** — mechanical → electromagnetic → distributed → emergent
- **Dynamization** — rigid → single joint → multiple joints → fluid → emergent
- **Coordination-Decoordination** — synchronized → coordinated → async → eventual consistency → autonomous
- **Increasing Information Content** — no feedback → reactive → adaptive → self-learning → conscious
- **Human Involvement Reduction** — manual → semi-auto → auto → autonomous → emergent

### 4. Predict the Next Step

Based on diagnostic answers:

- **Where is the system now?** (stage in each law)
- **Where should it go next?** (next stage)
- **What's blocking evolution?** (contradictions, constraints)
- **What does the next step require?** (refactoring, tooling, team skills)

### 5. Cross-Reference with TRIZ Matrix

If evolution reveals contradictions (e.g., "we need async but also consistency"), use **triz-matrix** to find inventive principles that resolve them.

---

## Example: Analyzing a Monolith

**System:** E-commerce platform, growing from 50K to 500K users.

**Current state:**

- Monolithic Node.js/Express API
- Single PostgreSQL database
- Manual deployments
- Tight coupling between modules
- Growing tech debt

**Evolution assessment:**

| Law | Current Stage | Next Stage | Action |
|-----|---------------|-----------|--------|
| **Completeness** | Complete but unbalanced (control weak) | Balanced (add observability) | Implement logging, metrics, alerting |
| **Energy Conductivity** | Partial (bottlenecks at DB) | Full (async pipelines, caching) | Async processing, queue system, cache layer |
| **Harmonization** | Chaotic (API sends 1000 req/s, DB handles 100/s) | Synchronized (rate limits, batching) | Rate limiting, connection pooling, queue |
| **Ideality** | Crude (lots of overhead) | Optimized (modular, self-contained) | Extract services, reduce dependencies |
| **Uneven Development** | Critical imbalance (modern frontend, legacy backend) | System evolution (split monolith) | Microservices refactor, API gateway |
| **Super-system** | Standalone (poorly integrated with 3rd party) | Integrated component (platform-ready) | Event bus, standard APIs, service mesh |
| **Macro to Micro** | Macro (monolith) | Meso (microservices) | Strangler fig pattern, gradual split |
| **Dynamism** | Rigid (hardcoded config) | Adaptive (feature flags, config server) | Feature flags, config management, dashboards |
| **Complexity** | Peak (30k LOC, hard to navigate) | Simplifying (refactoring, modularization) | Extract patterns, reduce coupling, pay down debt |

**Pattern evolution:**

- **Mono-Bi-Poly:** Monolith → 2 main services (API, worker) → 5-7 microservices
- **Segmentation:** Solid monolith → Layered → Modular → Service mesh
- **Dynamization:** Hardcoded → Config files → Env vars → Feature flags → Adaptive
- **Coordination:** Synchronous → Eventual consistency → Event-driven

**Next immediate steps:**

1. Add observability (logs, metrics, tracing) → fulfill "Completeness" law
2. Identify DB bottleneck → async processing, caching
3. Extract first service (e.g., auth) → begin transition to microservices
4. Introduce feature flags → increase dynamism without redeployment

**Contradictions to resolve:**

- "Need consistency (transactions) but also scalability (async)" → TRIZ: Separation in time, Dynamization
- "Need monolith stability but also flexibility" → TRIZ: Universality, Transition to super-system

---

## When to Use Each Law

| Challenge | Primary Law | Secondary Laws |
|-----------|------------|-----------------|
| "System crashes under load" | **Energy Conductivity**, **Harmonization** | Completeness, Ideality |
| "Can't add features without breaking things" | **Uneven Development**, **Increasing Dynamism** | Complexity then Simplification |
| "Operations cost is too high" | **Increasing Ideality** | Completeness, Increasing Dynamism |
| "Need to scale but monolith is limiting" | **Macro to Micro**, **Transition to Super-system** | Uneven Development, Complexity |
| "Legacy database with modern API" | **Uneven Development** | Energy Conductivity, Dynamization |
| "Can't coordinate across teams" | **Harmonization of Rhythms**, **Coordination-Decoordination** | Uneven Development |
| "Need to modernize without rewriting" | **Trimming**, **Dynamization** | Uneven Development, Macro to Micro |

---

## Integration with Other TRIZ Skills

**triz-matrix:** When evolution reveals contradictions (e.g., need to be both consistent and scalable), use triz-matrix to find inventive principles.

**triz-ariz:** When a complex problem spans multiple systems or involves innovation, use triz-ariz to structure the problem.

---

## Further Reading

- Genrich Altshuller, *To Find an Idea* (Chapters 8-10) — original TRIZ evolution laws
- [Wikipedia — TRIZ](https://en.wikipedia.org/wiki/TRIZ) — general TRIZ methodology introduction
