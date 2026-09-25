<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Where the book takes a side](#where-the-book-takes-a-side)
  - [Method length](#method-length)
  - [Comments](#comments)
  - [Test-driven development](#test-driven-development)
  - [Positions argued in the book alone](#positions-argued-in-the-book-alone)
  - [What the evidence read says](#what-the-evidence-read-says)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Where the book takes a side

The book argues against several common practices. A review that leans on
one of these positions says whose it is, and what the other side says
where a text of the other side was read. Three of the positions were
argued out between John Ousterhout and Robert Martin in a written
discussion, which `sources.md` names by commit. Quotations from it are
marked with its section heading and name the speaker. Quotations marked
with a section number are from *A Philosophy of Software Design*. A
section number is the second edition's, and "1e" or "2e" after it names
the edition whose wording is quoted.

None of these positions is a measured result. What was read of the
evidence is in the last section.

## Method length

Ousterhout: "The advice in *Clean Code* on method length is so extreme that
it encourages programmers to create teeny-tiny methods that suffer from
both shallow interfaces and entanglement" (Method Length). The book's
rule is in `decisions.md`: depth before length.

Martin: "It is certainly possible to over-decompose code" and "The
strategy that I use for deciding how far to take decomposition is the old
rule that a method should do 'One Thing'. If I can meaningfully extract one
method from another, then the original method did more than one thing"
(Method Length).

Where they ended, in Ousterhout's summary (Method Length Summary): "We
agree that it is possible to over-decompose". "We disagree on how far to decompose: you recommend
decomposing code into much smaller units than I do." "Entanglement between
methods in a class doesn't bother you as much as it bothers me." Martin's
gloss: "we disagree on the relative weighting of those two values."

For a review: a long function is a question, not a finding. The finding is
a shallow interface or a conjoined pair, and it needs the flag's evidence.

## Comments

Ousterhout: comments "play a fundamental and irreplaceable role in system
design". "I believe that it is not possible to define interfaces and
create abstractions without a lot of comments." "I would probably write
5-10x more lines of comments for a given piece of code than you would"
(Comments Summary).

*Clean Code*, as Ousterhout quotes it in the discussion: "Comments are
always failures" (Comments). Martin, in the discussion: "I prefer long
names to comments. I don't trust comments to be maintained, nor do I trust
that they will be read", and "I also agree that well-placed comments can
enhance the ability of readers to understand the abstractions ... I
disagree that comments are the only, or even the best, way to understand
those abstractions" (Comments).

Where they ended, in Ousterhout's summary (Comments Summary): "We agree
that implementation code only needs comments when the code is
nonobvious." On interfaces, the same summary records
one agreement and one dispute: "You agree for public APIs, but see little
need to comment interfaces that are internal to the team."

For a review: a missing interface comment is a finding under the book, and
the reader should know the book is one side. Google's reviewer guide is on
the same side for the reason a comment exists (`decisions.md`).

## Test-driven development

The book: "Although I am a strong advocate of unit testing, I am not a fan
of test-driven development. The problem with test-driven development is
that it focuses attention on getting specific features working, rather
than finding the best design. This is tactical programming pure and simple"
(§19.4, 1e). Its one exception: "One place where it makes sense to write
the tests first is when fixing bugs" (§19.4, 1e).

In the discussion Ousterhout withdrew his description of the practice and
kept his concern: "I plead 'guilty as charged' to inaccurately describing
TDD. I will fix this in the next revision of APOSD. That said, your
definition of TDD does not change my concerns" (Test-Driven Development).
His restatement: "The fundamental problem with TDD is that it forces
developers to work too tactically, in units of development that are too
small; it discourages design thinking." His alternative, which Martin
names "bundling": write a few methods or a class, then their tests.

Martin: "I think we simply disagree that TDD discourages design" and "I
agree with all that advice, but disagree with your assertion that TDD
might be the cause of bad code" (Test-Driven Development).

Where they ended, in Ousterhout's summary (TDD Summary): "We agree that unit tests are an essential
element in software development." "We agree that it is possible to use TDD
to produce systems with good designs." The risk of bad design under TDD
stayed in dispute.

For a review: this skill reviews a design, not a process. It raises the
position only when the design under review shows the symptom the book
names, features accreted with no abstraction between them. Then it says
the process is one candidate cause.

## Positions argued in the book alone

These were not part of the discussion. Each is the book's, at the section
given. No text of the other side was read, so none is quoted, and a
finding that rests on one of these says so.

- **Small classes.** "Classitis" (§4.6): see `principles.md`. The book's
  target is the belief that more classes are better, not any particular
  size.
- **Implementation inheritance.** "Implementation inheritance creates
  dependencies between the parent class and each of its subclasses ...
  this results in information leakage between the classes in the
  inheritance hierarchy and makes it hard to modify one class in the
  hierarchy without looking at the others" (§19.1, 1e). "Before using
  implementation inheritance, consider whether an approach based on
  composition can provide the same benefits" (§19.1, 1e).
- **Agile development.** "Agile development tends to focus developers on
  features, not abstractions" (§19.2, 1e). Principle 15 follows from it.
- **Design patterns.** "The greatest risk with design patterns is
  over-application. Not every problem can be solved cleanly with an
  existing design pattern; don't try to force a problem into a design
  pattern when a custom approach will be cleaner" (§19.5, 1e). "The
  notion that design patterns are good doesn't necessarily mean that more
  design patterns are better."
- **Getters and setters.** "Getters and setters are shallow methods
  (typically only a single line), so they add clutter to the class's
  interface without providing much functionality" (§19.6, 1e). "It's
  better not to expose instance variables in the first place."
- **Over-defensive exceptions.** "An over-defensive style where anything
  that looks even a bit suspicious is rejected with an exception, which
  results in a proliferation of unnecessary exceptions that increase the
  complexity of the system" (§10.2, 1e).

## What the evidence read says

Little was reachable, and `sources.md` lists what was not. Two secondary
summaries were read, both from Wikipedia on the date `sources.md` gives.
The papers behind them were not opened.

- On test-driven development: "A 2013 meta-analysis of 27 studies found a
  small positive effect on external quality and little or no overall
  effect on productivity, with larger quality gains but also larger
  productivity reductions in industrial studies." The page cites Rafique
  and Mišić, *IEEE Transactions on Software Engineering* 39(6), 2013. It
  also reports a later study finding that "quality and productivity
  improvements were associated more with small, uniform development steps
  than with the test-first ordering", citing Fucci and others, "A
  Dissection of the Test-Driven Development Process: Does It Really Matter
  to Test-First or to Test-Last?", *IEEE Transactions on Software
  Engineering* 43(7), 2017. Neither summary speaks to design quality,
  which is the book's concern.
- On complexity metrics and size: the page reports that "Some studies
  find a positive correlation between cyclomatic complexity and defects;
  functions and methods that have the highest complexity tend to also
  contain the most defects." It adds that the correlation between that
  metric and program size "has been demonstrated many times", that
  "Studies that controlled for program size ... are generally less
  conclusive, with many finding no significant correlation, while others
  do find correlation", and that reducing the metric "is not proven to
  reduce the number of errors or bugs in that code". Nothing read here
  isolates the length of one function, as against its branching or the
  size of the program around it, as a cause of defects.

A review should not state any of the positions above as a finding of
research. It states them as the book's, with the section, and lets the
user weigh them against their own team's practice.
