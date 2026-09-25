---
name: contradiction
description: >
  Resolve an engineering trade-off in software with TRIZ instead of a
  compromise. Restate the problem as a contradiction, map it to
  Altshuller's 39 parameters, read the classic contradiction matrix, and
  adapt the principles it recommends. Send a physical contradiction to the
  separation principles. Hand a problem the matrix route did not crack, or
  one that keeps coming back, to the ariz skill of this package. Use when
  improving one thing makes another worse, or when two requirements seem
  incompatible. Use when a compromise is the only option on the table. Use
  when one element must have two opposite properties.
license: MIT
---

# Contradiction

You guide the user through TRIZ on a software problem. The output is a set
of concrete solution directions, each named after the principle behind it,
each stated for the user's system. Reply in the user's language. Think
between steps. The matrix and the principles give directions. The
adaptation to the system is the work.

Do not guess the problem. When a step needs a fact you do not have, ask the
user before you continue. Examples: "What gets worse when you improve
that?", "Is the cost in latency or in throughput?", "What must stay as it
is?"

Four reference files sit in `references/`. Read each at the point its row
names, and not before. The `ariz` skill of this package reads
`principles.md` and `sources.md` too.

| File | What it holds | Read when |
| --- | --- | --- |
| [`references/parameters.md`](references/parameters.md) | the 39 engineering parameters, with a reading of each for software | Step 5, to map both sides of a technical contradiction |
| [`references/principles.md`](references/principles.md) | the 40 inventive principles, with a reading of each for software | Step 4, for who defined the four separations; Step 7, for each recommended principle |
| [`references/matrix.md`](references/matrix.md) | the classic contradiction matrix, one line per cell | Step 6: search it for one line, and never read it whole |
| [`references/sources.md`](references/sources.md) | where each reference of this skill and of `ariz` was read, and what could not be opened | when the user asks where a cell or a principle comes from |

## Step 1: state the contradiction

Restate the user's problem as one of two kinds and ask them to confirm it.

- **Technical contradiction.** Improving one parameter worsens another.
  "A longer cache lifetime unloads the database and serves stale reads."
- **Physical contradiction.** One element must have a property and its
  opposite. "The cache entry must exist, for speed, and must not exist,
  for freshness."

A technical contradiction often hides a physical one. The physical one is
the sharper statement. Write both when you can.

If no second parameter gets worse and no element needs two opposite
properties, there is no contradiction. Say so, because this skill has
nothing to add. Reading and measuring answer an algorithmic question or a
library limitation.

## Step 2: state the ideal final result

Write what the outcome looks like if the contradiction did not exist. The
element itself provides the useful function without the harmful effect and
without complicating the system. "The entry itself is fresh whenever it is
read." The sentence is a direction, not a solution. Keep it in view.

## Step 3: route

- A physical contradiction goes to Step 4.
- A technical contradiction goes to Step 5.
- Do both when Step 1 produced both statements.

## Step 4: separate the opposite properties

Four ways to hold both properties. Later TRIZ teaching gives this set, and
`principles.md` says whose it is and what Altshuller published instead.

- **In time.** The property holds at one moment and its opposite at
  another. Lazy and eager phases, a feature flag, a build-time check that
  is absent at run time.
- **In space.** The property holds in one place and its opposite in
  another. Edge and origin, a write primary and a read replica, client
  and server validation.
- **On condition.** The property holds under one condition and its
  opposite under another. A circuit breaker, an adaptive limit, a fast
  path for the common case.
- **Between the parts and the whole.** The whole has the property and the
  parts have its opposite. A distributed system made of simple services,
  a large store made of small shards.

State each separation that fits as a concrete change to the user's system.
Then continue to Step 5 with the technical contradiction, when there is
one. The two routes give different directions.

## Step 5: map to parameters

Read `references/parameters.md`. The improving parameter is the one the
user wants better. The worsening parameter is the one that degrades when
they get it. Present two or three candidates for each, with a sentence on
why, and ask the user to choose. The parameters describe physical systems.
The software readings in the reference show which one carries the same
role in the user's system.

## Step 6: read the matrix

Each line of `references/matrix.md` is one cell of the classic matrix. It
holds the improving parameter's number, a space, the worsening parameter's
number, a colon, and the recommended principles in the matrix's order.
Search the file for the line that begins with the two numbers and the
colon, for example `9 27:`. Do not read the file whole. A line that ends in
`(disputed)` is a cell the transcriptions disagree on, and the file's last
section lists every reading of it.

A pair with no line has no recommendation in the classic matrix. Then try
these in turn.

- Try the pair the other way round, which is a different cell.
- Try a neighbouring parameter for either side.
- Go back to Step 4 with the physical contradiction.

## Step 7: adapt the principles

Read the recommended principles in `references/principles.md`. For each:

1. State the principle in plain words.
2. State the change it would mean in the user's system.
3. State the new trade-off the change brings, if any.

Present two to four directions, ranked by how directly each removes the
contradiction. Name the principle behind each. When a principle does not
fit, say so and drop it.

## Step 8: iterate or escalate

Ask the user which direction holds, whether the contradiction should be
restated, and what constraint was missed. Repeat from Step 1 when the
restatement changes.

Hand over to the `ariz` skill of this package in four cases. The matrix
gave nothing the user can use. The problem has several contradictions
that feed each other. A fix in one place breaks another. The problem has
returned after earlier fixes. Say why you are handing over. Pass on the
technical contradiction, the ideal final result and that reason. `ariz`
walks ARIZ-85C and hands a restated technical contradiction back here.

## Boundaries

- The matrix and the principles are directions with a published origin.
  They are not a guarantee. When a direction contradicts what the user
  knows about their system, the user's knowledge wins and the direction is
  dropped.
- A problem with no trade-off in it is not a TRIZ problem, and Step 1
  says so before any lookup.
- A root cause hidden behind many symptoms belongs to the `root-cause`
  skill of this marketplace's `toc-thinking` package, which builds the
  cause-and-effect tree. Hand over when the user's problem is a tangle of
  symptoms rather than a trade-off, and only if that skill is installed.
