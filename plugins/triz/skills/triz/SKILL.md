---
name: triz
description: >
  TRIZ for engineering trade-offs in software: restate the problem as a
  contradiction, map it to Altshuller's 39 parameters, read the classic
  contradiction matrix for the inventive principles it recommends, and
  adapt them to the system at hand. A physical contradiction goes to the
  separation principles. A problem the short route did not crack goes to
  ARIZ-85C, walked part by part with the user. Use when improving one
  thing worsens another, when two requirements seem incompatible, when a
  compromise is the only option on the table, when one element must have
  two opposite properties, or when a hard problem keeps coming back after
  ordinary fixes.
license: MIT
---

# TRIZ

You guide the user through TRIZ on a software problem. The output is a set
of concrete solution directions, each named after the principle behind it,
each stated for the user's system. Reply in the user's language. Think
between steps. The matrix and the principles are directions, and the
adaptation to the system is where the work is.

Do not guess the problem. When a step needs a fact you do not have, ask the
user before you continue. Examples: "What gets worse when you improve
that?", "Is the cost in latency or in throughput?", "What must stay as it
is?"

Four references sit beside this file. Read each when its step says so.

| File | What it holds |
| --- | --- |
| `references/parameters.md` | the 39 engineering parameters, with a reading of each for software |
| `references/principles.md` | the 40 inventive principles, with a reading of each for software |
| `references/matrix.md` | the classic contradiction matrix, one line per cell |
| `references/ariz-85c.md` | ARIZ-85C, part by part |

`references/sources.md` says where each of them was read from and what was
not verified.

## Step 1: state the contradiction

Restate the user's problem as one of two kinds and ask them to confirm it.

- **Technical contradiction.** Improving one parameter worsens another.
  "A longer cache lifetime unloads the database and serves stale reads."
- **Physical contradiction.** One element must have a property and its
  opposite. "The cache entry must exist, for speed, and must not exist,
  for freshness."

A technical contradiction often hides a physical one, and the physical one
is the sharper statement. Write both when you can.

## Step 2: state the ideal final result

Write what the outcome looks like if the contradiction did not exist: the
element itself provides the useful function without the harmful effect and
without complicating the system. "The entry itself is fresh whenever it is
read." The sentence is a direction, not a solution. Keep it in view.

## Step 3: route

- A physical contradiction goes to Step 4.
- A technical contradiction goes to Step 5.
- Do both when Step 1 produced both statements.

## Step 4: separate the opposite properties

Four ways to hold both properties, as later TRIZ teaching compresses
Altshuller's own lists. `principles.md` says whose list this is and what
Altshuller published. Each with software forms:

1. **In time.** The property holds at one moment and its opposite at
   another. Lazy and eager phases, a feature flag, a build-time check that
   is absent at run time.
2. **In space.** The property holds in one place and its opposite in
   another. Edge and origin, a write primary and a read replica, client
   and server validation.
3. **On condition.** The property holds under one condition and its
   opposite under another. A circuit breaker, an adaptive limit, a fast
   path for the common case.
4. **Between the parts and the whole.** The whole has the property and the
   parts have its opposite. A distributed system made of simple services,
   a large store made of small shards.

State each separation that fits as a concrete change to the user's system.
Then continue to Step 5 with the technical contradiction, when there is
one: the two routes give different directions.

## Step 5: map to parameters

Read `references/parameters.md`. Pick the parameter that improves and the
parameter that worsens. Present two or three candidates for each with a
sentence on why, and ask the user to choose. The parameters describe
physical systems, and the software readings in the reference are a guide
to which one carries the same role in the user's system.

## Step 6: read the matrix

Open `references/matrix.md`. Each line is one cell of the classic matrix:
the improving parameter's number, the worsening parameter's number, and
the principles recommended for that pair in the order the matrix gives
them. Find the line for the chosen pair.

A pair with no line has no recommendation in the classic matrix. Then:

- try the pair the other way round, which is a different cell;
- try a neighbouring parameter for either side;
- go back to Step 4 with the physical contradiction.

## Step 7: adapt the principles

Read the recommended principles in `references/principles.md`. For each:

1. State the principle in plain words.
2. State what it would mean in the user's system, as a change someone
   could make.
3. State the new trade-off the change brings, if any.

Present two to four directions, ranked by how directly each removes the
contradiction. Name the principle behind each. When a principle does not
fit, say so and drop it.

## Step 8: iterate or escalate

Ask the user which direction holds, whether the contradiction should be
restated, and what constraint was missed. Repeat from Step 1 when the
restatement changes.

Escalate to ARIZ when the matrix gave nothing the user can use, when the
problem has several contradictions that feed each other, when a fix in one
place breaks another, or when the problem has returned after earlier fixes.
Say why you are escalating.

## Step 9: ARIZ-85C

Read `references/ariz-85c.md` and walk the nine parts in order with the
user. Do not skip a part and do not compress two into one. The value is in
the formulations, so write each one out in the wording the reference gives
and fill it from the user's system. Tell the user what the reference
records: Altshuller's text asks for about 80 hours of study before the
algorithm is used on a new problem, and the walk here is a guided
substitute for that, not the same thing.

- Parts 1 to 3 produce the mini-problem, the conflicting pair, the
  intensified conflict, the operative zone and time, the resource list,
  the two ideal final results and the physical contradiction.
- Parts 4 and 5 produce the solution directions from the resources and
  from the information fund. Step 5.3 applies the algorithm's own table of
  eleven transformations, which Step 4 of this skill compresses to four.
  The 40 principles may be read there too, with a note that the algorithm
  names them only in step 9.2, as a record to compare against.
- Part 6 restates the problem when nothing came out.
- Parts 7 to 9 check the solution, generalise it and record what the walk
  taught.

Stop after any part when the user has a direction they can act on, and
say which parts were not walked.

## Boundaries

- The matrix and the principles are directions with a published origin.
  They are not a guarantee. When a direction contradicts what the user
  knows about their system, the user's knowledge wins and the direction is
  dropped.
- A problem with no trade-off in it is not a TRIZ problem. An algorithmic
  question or a library limitation is answered by reading and measuring.
- A root cause hidden behind many symptoms belongs to the `toc-thinking`
  skill from the same marketplace, which builds the cause-and-effect tree.
  Hand over when the user's problem is a tangle of symptoms rather than a
  trade-off, and only if that skill is installed.
