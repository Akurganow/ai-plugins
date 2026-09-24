# The design principles

The second edition's "Summary of Design Principles", verbatim, sixteen
items, with the chapter that argues each. The page numbers are the book's
own. The first edition lists fifteen: items 1 to 15 below, with item 11
worded "Define errors (and special cases) out of existence". Item 16
belongs to chapter 21, which the second edition added. `sources.md` names
the copies read and how they were compared.

The book calls these "the most important software design principles
discussed in this book" and nothing more. A principle is a direction the
review can cite. It is not a rule the code fails.

| # | Principle | Chapter |
| --- | --- | --- |
| 1 | Complexity is incremental: you have to sweat the small stuff (see p. 11). | 2, §2.4 |
| 2 | Working code isn't enough (see p. 14). | 3 |
| 3 | Make continual small investments to improve system design (see p. 15). | 3, §3.3; 16 |
| 4 | Modules should be deep (see p. 23) | 4 |
| 5 | Interfaces should be designed to make the most common usage as simple as possible (see p. 27). | 4 |
| 6 | It's more important for a module to have a simple interface than a simple implementation (see pp. 61, 74). | 8 |
| 7 | General-purpose modules are deeper (see p. 39). | 6 |
| 8 | Separate general-purpose and special-purpose code (see pp. 45, 68). | 6, §6.6; 9, §9.4 |
| 9 | Different layers should have different abstractions (see p. 51). | 7 |
| 10 | Pull complexity downward (see p. 61). | 8 |
| 11 | Define errors out of existence (see p. 81). | 10 |
| 12 | Design it twice (see p. 91). | 11 |
| 13 | Comments should describe things that are not obvious from the code (see p. 101). | 13 |
| 14 | Software should be designed for ease of reading, not ease of writing (see p. 151). | 18 |
| 15 | The increments of software development should be abstractions, not features (see p. 156). | 19, §19.2 |
| 16 | Separate what matters from what doesn't matter and emphasize the things that matter (see p. 171). | 21 |

## Deep and shallow

The book's picture for principle 4: "imagine that each module is
represented by a rectangle ... The top edge of a rectangle represents the
module's interface; the length of that edge indicates the complexity of the
interface. The best modules are deep: they have a lot of functionality
hidden behind a simple interface" (§4.4, 1e). "A shallow module is one
whose interface is relatively complex in comparison to the functionality
that it provides" (§4.5, 1e).

Ousterhout on why the pair is the measure: "One of the reasons I use the
deep/shallow characterization is that it captures both sides of the
tradeoff; it will tell you when a decomposition is good and also when
decomposition makes things worse" (`aposd-vs-clean-code`, Method Length).

The extreme the book names: "The extreme of the 'classes should be small'
approach is a syndrome I call classitis, which stems from the mistaken view
that 'classes are good, so more classes are better'" (§4.6, 1e). "Small
classes don't contribute much functionality, so there have to be a lot of
them, each with its own interface. These interfaces accumulate to create
tremendous complexity at the system level."

## General purpose, and its limit

Principle 7 comes with the book's own qualifier, "somewhat general-purpose"
(§6.1 title). Chapter 6 is the chapter the second edition reworked most.
Its conclusion in the first edition: "General-purpose interfaces have many
advantages over special-purpose ones. They tend to be simpler, with fewer
methods that are deeper" (§6, 1e).

The counterweight is Google's reviewer guide, which asks reviewers to be
"especially vigilant about over-engineering" and adds: "Encourage
developers to solve the problem they know needs to be solved now, not the
problem that the developer speculates might need to be solved in the
future." This skill reads principle 7 as
bounded by that line: general in interface, not speculative in features.

## Pull complexity downward

Chapter 8's opening: "Most modules have more users than developers, so it
is better for the developers to suffer than the users" and "it is more
important for a module to have a simple interface than a simple
implementation" (§8, 2e). Principles 6 and 10 are the same idea seen from
the interface and from the implementation.

## Abstractions, not features

Principle 15 is argued against agile development: "Agile development tends
to focus developers on features, not abstractions" and "the increments of
development should be abstractions, not features" (§19.2, 1e).
`positions.md` carries the dispute around it.

## What matters

Principle 16 is the second edition's addition. Chapter 21 opens: "One of
the most important elements of good software design is separating what
matters from what doesn't matter" (§21, 2e). In a review it is the step
that decides which findings to report at all.
