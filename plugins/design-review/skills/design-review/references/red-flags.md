# The red flags

The book's "Summary of Red Flags" lists fourteen, unnumbered, in the order
below. Each entry gives the book's name and its one-line definition
verbatim, the chapter where it is argued, and what to look for in a review.
The last part is this skill's own. The page numbers in the book's list are
the second edition's. `sources.md` names the copies read.

The book introduces the list with one sentence: "The presence of any of
these symptoms in a system suggests that there is a problem with the
system's design." A flag is a symptom, and a symptom can have a reason. Ask
for the reason before filing the finding.

## Shallow Module

"The interface for a class or method isn't much simpler than its
implementation." Chapter 4, §4.5.

Look for: a class or function whose signature, options and documented
behaviour take as long to learn as its body takes to read. A wrapper that
forwards every parameter. A method of one line that callers must
understand anyway. Getters and setters are the book's own example of
shallow methods (§19.6).

## Information Leakage

"A design decision is reflected in multiple modules." Chapter 5, §5.2.

Look for: a file format, a wire encoding, a table layout or a naming rule
that two modules both know. A change to one that would force the same
change in the other. Parnas' criterion is the test: each module should
"hide such a decision from the others" (see `sources.md`, Parnas 1972).

## Temporal Decomposition

"The code structure is based on the order in which operations are
executed, not on information hiding." Chapter 5, §5.3.

Look for: modules named after phases (read, parse, validate, write) that
share knowledge of one format. Parnas 1972 describes the same mistake as
decomposing "on the basis of a flowchart".

## Overexposure

"An API forces callers to be aware of rarely used features in order to use
commonly used features." Chapter 5.

Look for: a required parameter that almost every caller sets to the same
value. A constructor with eight arguments where two are in use. A
configuration a caller must read before the first call.

## Pass-Through Method

"A method does almost nothing except pass its arguments to another method
with a similar signature." Chapter 7, §7.1.

Look for: two layers with the same abstraction. The book's reading: "if
different layers have the same abstraction, such as pass-through methods or
decorators, then there's a good chance that they haven't provided enough
benefit" (§7, 2e).

## Repetition

"A nontrivial piece of code is repeated over and over." Chapter 9, §9.3.

Look for: the same sequence of calls in several places. The book's remedy
is to bring the pieces together (§9.3). Repeating a trivial line is not
this flag: the definition says nontrivial.

## Special-General Mixture

"Special-purpose code is not cleanly separated from general purpose code."
Chapter 9, §9.4.

Look for: a general mechanism with a branch for one caller. A library
function that knows one product's rule. The remedy the book gives is to
separate the two (§9.4), and the second edition adds a section titled
"Push specialization upwards (and downwards!)" (§6.6).

## Conjoined Methods

"Two methods have so many dependencies that its hard to understand the
implementation of one without understanding the implementation of the
other." Chapter 9, §9.7.

Look for: reading one function and having to open another to follow it.
Ousterhout's test, from the discussion with Martin: "If you've ever found
yourself flipping back and forth between the implementations of two
methods as you read code, that's a red flag that the methods might be
entangled." The book's rule: "It should be possible to understand each
method independently" (§9.7, 1e).

## Comment Repeats Code

"All of the information in a comment is immediately obvious from the code
next to the comment." Chapter 13, §13.2.

Look for: a comment that restates the line below it. The `prose-discipline`
package in this marketplace, when installed, names the same thing as a
narrator comment.

## Implementation Documentation Contaminates Interface

"An interface comment describes implementation details not needed by users
of the thing being documented." Chapter 13, §13.5.

Look for: a public doc comment that names the data structure, the
algorithm or the cache behind the call. A caller who reads it now depends
on it.

## Vague Name

"The name of a variable or method is so imprecise that it doesn't convey
much useful information." Chapter 14, §14.3.

Look for: `data`, `info`, `handle`, `process`, `manager`, a `result` that
holds one specific thing.

## Hard to Pick Name

"It is difficult to come up with a precise and intuitive name for an
entity." Chapter 14, §14.3.

Look for: a name the author changed twice. The book: "If you find it
difficult to come up with a name for a particular variable that is precise,
intuitive, and not too long, this is a red flag. It suggests that the
variable may not have a clear definition or purpose" (§14.3, 1e).

## Hard to Describe

"In order to be complete, the documentation for a variable or method must
be long." Chapter 15, §15.3.

Look for: an interface comment that needs three paragraphs. The book: "If
a method or variable requires a long comment, it is a red flag that you
don't have a good abstraction" (§15.3, 2e).

## Nonobvious Code

"The behavior or meaning of a piece of code cannot be understood easily."
Chapter 18.

Look for: a reader who says it is unclear. That is the whole test (§18,
2e). The `cognitive-load` package in this marketplace, when installed,
carries the reader-side catalogue for this flag.

## Where the names came from

A reader who knows the book by another summary will meet other names for
the same flags. This file keeps the book's, so that a finding can cite the
chapter. Numbering is not the book's, and this skill does not number them.
