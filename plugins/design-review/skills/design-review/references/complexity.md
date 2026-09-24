# Complexity, as the book defines it

The definitions the review rests on. Quotations marked with a section
number are from *A Philosophy of Software Design*. A section number is
the second edition's. "1e" or "2e" after it names the edition whose
wording is quoted, and `sources.md` names the copy each was read in.

## Definition

Section 2.1 defines complexity as "anything related to the structure of a
software system that makes it hard to understand and modify the system"
(§2.1, 1e). Ousterhout restates it in his discussion with Robert Martin:
"I use the term 'complexity' to refer to things that make it hard to
understand and modify a system. The most important contributors to
complexity relate to information: How much information must a developer
have in their head in order to carry out a task? How accessible and obvious
is the information that the developer needs?" (`aposd-vs-clean-code`,
Introductions).

Complexity is a property of a particular design, and the reader decides it.
"If you write code that someone else thinks is complicated, then you must
accept that the code is probably complicated" (`aposd-vs-clean-code`,
Comments). The same rule in the book: "If someone reading your code says
it's not obvious, then it's not obvious, no matter how clear it may seem to
you" (§18, 2e).

## The weighting

The book gives the overall complexity of a system as a weighted sum. In
its words: "The overall complexity of a system (C) is determined by the
complexity of each part p (cp) weighted by the fraction of time developers
spend working on that part (tp). Isolating complexity in a place where it
will never be seen is almost as good as eliminating the complexity
entirely" (§2.1, 1e). The formula itself is typeset as an image in the
copy read, so it is not reproduced here. The book calls the formula crude.
The review uses it for one thing: ranking findings by how often the part
is touched.

## Three symptoms

"Complexity manifests itself in three general ways" (§2.2, 1e):

1. **Change amplification.** "A seemingly simple change requires code
   modifications in many different places."
2. **Cognitive load.** "How much a developer needs to know in order to
   complete a task." The book adds: "Sometimes an approach that requires
   more lines of code is actually simpler, because it reduces cognitive
   load."
3. **Unknown unknowns.** "It is not obvious which pieces of code must be
   modified to complete a task, or what information a developer must have
   to carry out the task successfully."

"Of the three manifestations of complexity, unknown unknowns are the worst"
(§2.2, 1e). The book grades a few other things in passing: information
leakage is "one of the most important red flags in software design" (§5.2,
1e), and exception handling "one of the worst sources of complexity in
software systems" (§10, 2e). It gives no overall ranking. Where this skill
ranks a finding higher, it says so as its own judgement.

The book's "cognitive load" is an amount of information a developer must
know. It is not cognitive load theory's working-memory load, which the
`cognitive-load` package of this marketplace uses. When a finding is about
how many things a reader must keep in mind at once, it is that package's.

## Two causes

"Complexity is caused by two things: dependencies and obscurity" (§2.3,
1e). "A dependency exists when a given piece of code cannot be understood
and modified in isolation." "Obscurity occurs when important information
is not obvious." The chapter's conclusion: "Complexity comes from an
accumulation of dependencies and obscurities" (§2.5, 2e).

Dependencies "can't be completely eliminated" (§2.3, 1e). The book's goal
is fewer of them, and simpler and more obvious ones. Every finding in a
review names which cause it rests on.

## Incremental

"Complexity is incremental: you have to sweat the small stuff" (Summary of
Design Principles, item 1, 2e). The book's chapter 3 sets the investment:
"I suggest spending about 10–20% of your total development time on
investments" (§3.3, 1e). The figure is the book's suggestion and not a
measured result.

## What this definition is not

Brooks' "No Silver Bullet" divides the difficulties of software into
"essence — the difficulties inherent in the nature of the software — and
accidents — those difficulties that today attend its production but that
are not inherent". His essence is "a construct of interlocking concepts:
data sets, relationships among data items, algorithms, and invocations of
functions", and he holds "the hard part of building software to be the
specification, design, and testing of this conceptual construct, not the
labor of representing it". So Brooks puts design inside the essence, and
his accidents are the labour of representation.

Ousterhout's complexity cuts across that line. It is how hard one
particular design makes a system to understand and change, whichever of
Brooks' categories the cause falls in. A finding under this skill is not
"accidental" by virtue of being removable. When a finding says "accidental
complexity", the word is Brooks' and the skill says so. That reading of
the two texts is this skill's own.

Google's reviewer guide gives a one-line reading of the second kind: "Too
complex" usually means "can't be understood quickly by code readers." It
names a particular type: "over-engineering, where developers have made the
code more generic than it needs to be, or added functionality that isn't
presently needed by the system." The skill uses that line as the
counterweight to the book's preference for general-purpose modules.
