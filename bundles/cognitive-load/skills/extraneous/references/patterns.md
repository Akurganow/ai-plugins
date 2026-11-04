<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [The catalogue of extraneous load in code](#the-catalogue-of-extraneous-load-in-code)
  - [Complex conditionals](#complex-conditionals)
  - [Nested ifs](#nested-ifs)
  - [Inheritance nightmare](#inheritance-nightmare)
  - [Too many small methods, classes or modules](#too-many-small-methods-classes-or-modules)
  - [Responsible for one thing](#responsible-for-one-thing)
  - [Too many shallow microservices](#too-many-shallow-microservices)
  - [Feature-rich languages](#feature-rich-languages)
  - [Business logic and HTTP status codes](#business-logic-and-http-status-codes)
  - [Abusing DRY principle](#abusing-dry-principle)
  - [Tight coupling with a framework](#tight-coupling-with-a-framework)
  - [Layered architecture](#layered-architecture)
  - [Domain-driven design](#domain-driven-design)
  - [Cognitive load in familiar projects](#cognitive-load-in-familiar-projects)
  - [The long-run questions](#the-long-run-questions)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# The catalogue of extraneous load in code

The sections of Artem Zakirullin's "Cognitive load is what matters", a
practitioner's essay, in the essay's own order and wording. Copyright
(c) 2023 Artem Zakirullin, Creative Commons Attribution 4.0 International,
<https://creativecommons.org/licenses/by/4.0/>. The quotations are
unchanged. `sources.md` names the copy and its commit. Each entry gives
the essay's point, a short quotation, and what to look for in the user's
system. The last part is this skill's own.

The essay defines its subject as "how much a developer needs to think in
order to complete a task", and its model as "🧠: fresh working memory,
zero cognitive load", "🧠++: two facts in our working memory", "🤯:
cognitive overload, more than 4 facts". It calls the model simplistic. It
names two kinds of load only, intrinsic and extraneous, and says of the
second: "Can be greatly reduced. We will focus on this type of cognitive
load."

## Complex conditionals

A compound condition makes the reader carry each clause. The essay's fix:
"Introduce intermediate variables with meaningful names." The reader then
holds three names instead of five conditions.

Look for: a condition whose clauses the reader must remember to
understand the branch. The essay gives no count. A named intermediate is
the fix at any count.

## Nested ifs

Each level of nesting is a precondition the reader must carry. The fix is
early returns: "We can focus on the happy path only, thus freeing our
working memory from all sorts of preconditions."

Look for: a body that runs only when several enclosing conditions hold.
The essay's term is early returns, and it gives no depth threshold.

## Inheritance nightmare

A class four levels deep spreads one behaviour across four files and the
reader chases it. "Prefer composition over inheritance."

Look for: a change that requires reading every ancestor, and then every
descendant that overrides.

## Too many small methods, classes or modules

The essay quotes Ousterhout: "The best components are those that provide
powerful functionality yet have a simple interface." Its own sentence:
"Having too many shallow modules can make it difficult to understand the
project. Not only do we have to keep in mind each module's
responsibilities, but also all their interactions."

In this skill's terms: a deep module keeps the task's elements behind its
interface. A shallow one hands them to every caller as extraneous elements
to hold.

Look for: modules whose names and interfaces take longer to learn than
their bodies take to read. The `design-review` package of this
marketplace, when installed, judges depth for each module. This skill
counts what the reader must hold.

## Responsible for one thing

The single-responsibility principle read as "one thing" yields
`MetricsProviderFactoryFactory`. "The names and interfaces of such classes
tend to be more mentally taxing than their entire implementations, what
kind of abstraction is that?" The essay's reading of the principle: "A
module should be responsible to one, and only one, user or stakeholder."

Look for: a class extracted because a rule said to, not because a reader
needed it gone.

## Too many shallow microservices

"One of the worst and hardest to fix phenomena is so-called distributed
monolith, which is often the result of this overly granular shallow
separation." The essay's anecdote: five developers, seventeen services,
"Every new requirement led to changes in 4+ microservices."

Look for: a change that crosses a network boundary it did not need to.

## Feature-rich languages

The essay quotes Rob Pike: "You not only have to understand this
complicated program, you have to understand why a programmer decided this
was the way to approach a problem from the features that are available."
Its rule: "Reduce cognitive load by limiting the number of choices." And:
"Language features are OK, as long as they are orthogonal to each other."

Look for: a construct the reader must look up, where a plainer one would
have served.

## Business logic and HTTP status codes

A custom mapping from numbers to meanings must be rebuilt by every reader,
on the front end, in QA, in support. "Prefer self-describing strings."

Look for: any numeric or single-letter code that stands for a business
meaning, in a response, a database column or a log.

## Abusing DRY principle

"When you strive to eliminate any repetition, you might end up creating
tight coupling between unrelated components." The essay quotes Rob Pike:
"A little copying is better than a little dependency." And: "All your
dependencies are your code."

Look for: a shared helper that two callers bend in opposite directions,
or a library imported for one function.

## Tight coupling with a framework

"By relying too heavily on a framework, we force all upcoming developers
to learn that 'magic' first." The fix: "Use the framework in a
library-like fashion."

Look for: business logic that cannot be read, or tested, without knowing
what the framework does around it.

## Layered architecture

Hexagonal and onion layering, in the essay's experience: "Abstraction is
supposed to hide complexity, here it just adds indirection." Its rule:
"Do not add layers of abstractions for the sake of an architecture. Add
them whenever you need an extension point that is justified for practical
reasons."

Look for: a call that passes through ports, adapters and services and
changes nothing on the way. The `design-review` package's Pass-Through
Method flag is the same finding from the design side.

## Domain-driven design

"DDD is more about the problem space rather than the solution space."
Folder structures and repositories are a reader's own interpretation, and
"if we create a lot of extraneous cognitive load - future developers are
doomed."

Look for: a vocabulary the code base uses that its readers do not share.

## Cognitive load in familiar projects

The essay quotes Dan North: "familiarity is not the same as simplicity."
Its own sentence: "The more unique mental models there are to learn, the
longer it takes for a new developer to deliver value. If you keep the
cognitive load low, people can contribute to your codebase within the
first few hours of joining your company."

Its measurement: "Once you onboard new people on your project, try to
measure the amount of confusion they have (pair programming may help). If
they're confused for more than ~40 minutes in a row - you've got things
to improve in your code." The figure carries a tilde in the essay, and it
is a thing to try, not a rule. No study behind it was found.

## The long-run questions

The essay's test for an architecture, in place of how it feels:

- "Is it easy to reproduce and debug an issue? Or do you have to jump
  across the call stacks or distributed components, trying to make sense
  of everything in your head?"
- "Can we make changes quickly, or are there a lot of unknown unknowns,
  and people are afraid to touch things?"
- "Can new people add features quickly? Are there some unique mental
  models to learn?"

The essay attaches no threshold to any of the three. Neither does this
skill. And: "Involve junior developers in architecture reviews, they will
help you to identify the mentally demanding areas."
