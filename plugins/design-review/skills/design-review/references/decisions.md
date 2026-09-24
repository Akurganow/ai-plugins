# The decisions a review asks about

Four decisions the book argues, with its criteria, for the steps of the
procedure that make them. Quotations marked with a section number are
from *A Philosophy of Software Design*. A section number is the second
edition's. "1e" or "2e" after it names the edition whose wording is
quoted, and `sources.md` names the copy each was read in.

## Together or apart

Chapter 9 opens with signs that two pieces of code are related (§9, 1e):

- "They share information; for example, both pieces of code might depend
  on the syntax of a particular type of document."
- "They are used together: anyone using one of the pieces of code is likely
  to use the other as well. This form of relationship is only compelling
  if it is bidirectional." The book's counter-example: a disk block cache
  always involves a hash table, and hash tables serve many other uses, so
  the two stay separate.
- "They overlap conceptually, in that there is a simple higher-level
  category that includes both of the pieces of code."
- "It is hard to understand one of the pieces of code without looking at
  the other."

The chapter's four sections are the criteria: "Bring together if
information is shared" (§9.1), "Bring together if it will simplify the
interface" (§9.2), "Bring together to eliminate duplication" (§9.3),
"Separate general-purpose and special-purpose code" (§9.4). Its
conclusion: "The decision to split or join modules should be based on
complexity. Pick the structure that results in the best information
hiding, the fewest dependencies, and the deepest interfaces" (§9.9, 2e).

Parnas gave the criterion the book builds on: "one begins with a list of
difficult design decisions or design decisions which are likely to change.
Each module is then designed to hide such a decision from the others"
(Parnas 1972, conclusion).

### Splitting a method

"Length by itself is rarely a good reason for splitting up a method. In
general, developers tend to break up methods too much. Splitting up a
method introduces additional interfaces, which add to complexity" (§9.7,
1e). "Long methods aren't always bad. For example, suppose a method
contains five 20-line blocks of code that are executed in order. If the
blocks are relatively independent, then the method can be read and
understood one block at a time" (§9.7, 1e). The second edition adds:
"Depth is more important than length: first make functions deep, then try
to make them short enough to be easily read. Don't sacrifice depth for
length" (§9.8, 2e).

The test for a split that went too far is the Conjoined Methods flag
(`red-flags.md`).

## Errors

Chapter 10 gives three techniques for reducing the places where an
exception must be handled, and one answer for the rest.

1. **Define errors out of existence.** "The best way to eliminate
   exception handling complexity is to define your APIs so that there are
   no exceptions to handle: define errors out of existence" (§10.3, 1e).
   The book's example is Tcl's `unset`: rather than deleting a variable
   and failing when it is absent, "unset should ensure that a variable no
   longer exists". The same move applies to other special cases, which
   the second edition treats in chapter 6: "Special cases can result in
   code that is riddled with if statements, which make the code hard to
   understand and are prone to bugs. Thus, special cases should be
   eliminated wherever possible. The best way to do this is by designing
   the normal case in a way that automatically handles the edge conditions
   without any extra code" (§6.8, 2e).
2. **Mask exceptions.** "An exceptional condition is detected and handled
   at a low level in the system, so that higher levels of software need
   not be aware of the condition" (§10.6, 1e). The book's example is TCP
   retransmission.
3. **Aggregate exceptions.** "Handle many exceptions with a single piece
   of code; rather than writing distinct handlers for many individual
   exceptions, handle them all in one place with a single handler" (§10.7,
   1e). "Exception aggregation works best if an exception propagates
   several levels up the stack before it is handled ... This is the
   opposite of exception masking: masking usually works best if an
   exception is handled in a low-level method" (§10.7, 1e).
4. **Just crash?** (§10.8.) For errors not worth handling, the book's
   answer is to print diagnostic information and abort.

The book ranks the first above the other two and no further: "The best way
to do this is by redefining semantics to eliminate error conditions. For
exceptions that can't be defined away, you should look for opportunities
to mask them at a low level, so their impact is limited, or aggregate
several special-case handlers into a single more generic handler" (§10.10,
2e). Masking and aggregation are alternatives that fit different shapes of
the problem, as the §10.7 quotation says. The chapter also names the
opposite failure: an "over-defensive style where anything that looks even a
bit suspicious is rejected with an exception" (§10.2, 1e).

## Design it twice

"You'll end up with a much better result if you consider multiple options
for each major design decision: design it twice" (§11, 2e). "Try to pick
approaches that are radically different from each other; you'll learn more
that way. Even if you are certain that there is only one reasonable
approach, consider a second design anyway, no matter how bad you think it
will be" (§11, 2e). Then list the pros and cons of each. "The most
important consideration for an interface is ease of use for higher level
software" (§11, 2e).

A review can ask for the second design to be written down. Nygard's
decision-record template has a title and four sections: Status, Context
("What is the issue that we're seeing that is motivating this decision or
change?"), Decision, Consequences ("What becomes easier or more difficult
to do because of this change?"). `sources.md` says where the template was
read. The review does not require the format. It asks that the alternative
and the reason it lost survive somewhere a later reader can find.

## Comments and names

The book's four excuses for not writing comments open chapter 12: "Good
code is self-documenting", "I don't have time to write comments",
"Comments get out of date and become misleading", "The comments I have
seen are all worthless; why bother?" (§12, 2e). Its answer to the first:
"The overall idea behind comments is to capture information that was in
the mind of the designer but couldn't be represented in the code" (§12,
1e). Chapter 13's rule: "comments should describe things that aren't
obvious from the code" (§13, 2e).

Google's reviewer guide agrees on the direction: "Usually comments are
useful when they explain why some code exists, and should not be
explaining what some code is doing", and "mostly comments are for
information that the code itself can't possibly contain, like the
reasoning behind a decision." So a review that asks for a comment is not
taking a side against common practice. The dispute is with one book, and
`positions.md` states it.

Names: "Names should be precise" (§14.3 title). The flags Vague Name and
Hard to Pick Name in `red-flags.md` are the review's tests. Chapter 14's
second edition adds a section on the opposite view, "A different opinion:
Go style guide" (§14.6 title), which this skill has not read beyond the
heading.

## What the review reports

Chapter 16 gives the standing rule for any change: "if you invest a little
extra time to refactor and improve the system design, you'll end up with
a cleaner system" (§16.1, 1e). A finding names the change that would do
that, the flag or principle it rests on, and the part's weight in the
formula. Chapter 21's rule decides how many findings to report: separate
what matters from what does not (`principles.md`, item 16).
