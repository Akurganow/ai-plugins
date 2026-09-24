# Complexity, as the book defines it

The definitions the review rests on. Quotations marked with a section
number are from *A Philosophy of Software Design*. `sources.md` says which
edition each was read in and where. Section numbers are the second
edition's.

## Definition

Chapter 2 opens by defining complexity as "anything related to the
structure of a software system that makes it hard to understand and modify
the system" (§2.1, 1e). Ousterhout restates it in his discussion with
Robert Martin: "I use the term 'complexity' to refer to things that make it
hard to understand and modify a system. The most important contributors to
complexity relate to information: How much information must a developer
have in their head in order to carry out a task? How accessible and obvious
is the information that the developer needs?" (`aposd-vs-clean-code`,
Introductions).

Complexity is a property of a particular design, and the reader decides it.
"If you write code that someone else thinks is complicated, then you must
accept that the code is probably complicated" (`aposd-vs-clean-code`, Method
Length). The same rule in the book: "If someone reading your code says it's
not obvious, then it's not obvious, no matter how clear it may seem to you"
(§18, 2e).

## The weighting

The book gives the overall complexity of a system as the sum, over its
parts, of each part's complexity weighted by the fraction of time
developers spend working on that part. In the book's words: "The overall
complexity of a system (C) is determined by the complexity of each part p
(cp) weighted by the fraction of time developers spend working on that part
(tp). Isolating complexity in a place where it will never be seen is almost
as good as eliminating the complexity entirely" (§2.1, 1e). The formula
itself is typeset as an image in the copy read, so it is not reproduced
here. The book calls the formula crude. The review uses it for one thing:
ranking findings by how often the part is touched.

## Three symptoms

"Complexity manifests itself in three general ways" (§2.2, 1e):

1. **Change amplification.** "A seemingly simple change requires code
   modifications in many different places."
2. **Cognitive load.** How much a developer needs to know to complete a
   task. The book adds: "Sometimes an approach that requires more lines of
   code is actually simpler, because it reduces cognitive load."
3. **Unknown unknowns.** "It is not obvious which pieces of code must be
   modified to complete a task, or what information a developer must have
   to carry out the task successfully."

"Of the three manifestations of complexity, unknown unknowns are the worst"
(§2.2, 1e). The book grades nothing else. Where this skill ranks a finding
higher, it says so as its own judgement.

## Two causes

"Complexity is caused by two things: dependencies and obscurity" (§2.3,
1e). "A dependency exists when a given piece of code cannot be understood
and modified in isolation." "Obscurity occurs when important information
is not obvious." The chapter's conclusion: "Complexity comes from an
accumulation of dependencies and obscurities" (§2, 2e).

Dependencies are not removable. The book's goal is fewer of them, and
simpler and more obvious ones. Every finding in a review names which cause
it rests on.

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
are not inherent", and holds that "The complexity of software is an
essential property, not an accidental one." Brooks writes about the
problem: the concepts any correct program must carry. Ousterhout writes
about a design: how hard one system is to understand and change. A review
under this skill lowers the second and cannot touch the first. When a
finding says "accidental complexity", the word is Brooks' and the skill
says so.

Google's reviewer guide gives the same reading of the second kind in one
line: "Too complex" usually means "can't be understood quickly by code
readers." It names a particular type: "over-engineering, where developers
have made the code more generic than it needs to be, or added functionality
that isn't presently needed by the system." The skill uses that line as the
counterweight to the book's preference for general-purpose modules.
