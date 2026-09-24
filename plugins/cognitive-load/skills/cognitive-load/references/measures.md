# What can be counted, and what the studies on code found

Two published ways to put a number on a unit of code, and the studies of
programmers that were read. `sources.md` names each copy and says which
were read whole, which as abstracts, and which not at all. Nothing here
was measured by this skill.

## Cognitive Complexity

A metric proposed by G. Ann Campbell of SonarSource in the white paper
"Cognitive Complexity: A new way of measuring understandability". The
paper's own site was not reachable, and its text was read from a public
copy. Its three rules:

> A Cognitive Complexity score is assessed according to three basic rules:
> 1. Ignore structures that allow multiple statements to be readably
> shorthanded into one
> 2. Increment (add one) for each break in the linear flow of the code
> 3. Increment when flow-breaking structures are nested

The paper's Appendix B lists the increments: `if`, `else if`, `else`, the
ternary operator, `switch`, loops, `catch`, labelled jumps, "sequences of
binary logical operators", and each method in a recursion cycle; and a
nesting increment for each level a flow-breaking structure sits inside
another. "Thus, Cognitive Complexity does not increment for methods."

PMD's rule description restates it independently: "Code that contains a
break in the control flow is more complex, whereas the use of language
shorthands doesn't increase the level of complexity. Nested control flows
can make a method more difficult to understand, with each additional
nesting of the control flow leading to an increase in cognitive
complexity." Sonar's own Java implementation matches the rules, and its
rule text for the metric claims nothing about validation: "Cognitive
Complexity is a measure of how hard the control flow of a method is to
understand."

Two implementations read here default to a threshold of 15 per function:
PMD's rule, and SonarSource's ESLint plugin. The number is a default,
not a finding.

Validation: Muñoz Barón, Wyrich and Wagner, "An Empirical Validation of
Cognitive Complexity as a Measure of Source Code Understandability", ESEM
2020. Its abstract, read from a mirror: "we obtained about 24,000
understandability evaluations of 427 code snippets ... Cognitive
Complexity positively correlates with comprehension time and subjective
ratings of understandability. The metric showed mixed results for the
correlation with the correctness of comprehension tasks and with
physiological measures." The paper was not opened.

Use: a per-function count the user can run with a linter, for the
"complex conditionals" and "nested ifs" entries of `patterns.md`. It
counts control flow only. It does not see names, vocabulary or the
distance between a fact and its use.

## Intrinsic Complexity Points

Tavares de Souza and Costa Pinto, "Toward a Definition of
Cognitive-Driven Development", ICSME 2020, three pages, read from the
first author's own copy. Its abstract: "This paper presents an approach
called Cognitive-Driven Development (CDD) that is based on cognitive
complexity measurements and Cognitive Load Theory. This strategy can
reduce the cognitive overload of the developers through the limitation of
intrinsic complexity points from source code." Its grounding, in its
words: "Experimental studies performed by Miller have suggested that
humans are generally able to hold only seven plus or minus two units of
information in short-term memory."

Its table of points per element: `if`-`else` 2, `case` 1,
`try`-`catch`-`finally` 3, contextual coupling 1, a function passed as an
argument 1, crosscutting infrastructure 0. "Elements depicted here are not
limited, developers are free to include additional elements that they
consider interesting." Its limit: "five plus or minus two points, where
seven would be the limit" for web applications and mixed teams, and "ten
and twelve points for each implementation unit" for frameworks and
libraries. The paper says "Experimental studies are currently being
conducted to evaluate the CDD." The later papers were not opened.

Use: a budget per class the user sets and counts by hand. The budget is
the team's choice, and the paper says so.

## Studies of programmers

Read as abstracts from public mirrors, unless said otherwise.

- **Peitek, Apel, Parnin, Brechmann and Siegmund, "Program Comprehension
  and Code Complexity Metrics: An fMRI Study", ICSE 2021.** "We have
  conducted a functional magnetic resonance imaging (fMRI) study with 19
  participants ... While our data corroborate that complexity metrics
  can—to a limited degree—explain programmers' cognition in program
  comprehension, fMRI allowed us to gain insights into why some code
  properties are difficult to process. In particular, a code's textual
  size drives programmers' attention, and vocabulary size burdens
  programmers' working memory." The authors' replication package was also
  read; the scan data are not public.
- **Hansen, Goldstone and Lumsdaine, "What Makes Code Hard to
  Understand?", 2013.** "We present an experiment in which participants
  with programming experience predict the exact output of ten small Python
  programs ... seemingly insignificant notational changes can have
  profound effects on correctness and response times. Our results show
  that experience increases performance in most cases, but may hurt
  performance significantly when underlying assumptions about related
  code statements are violated." The first author's own post gives the
  count: 162 programmers.
- **Gonçales, Farias, da Silva and Fessler, "Measuring the Cognitive Load
  of Software Developers: A Systematic Mapping Study", ICPC 2019.** "In
  total, 33 articles (out of 2,612) were selected ... 55% of the studies
  adopted electroencephalogram (EEG) technology for monitoring the
  cognitive load ... the precision of machine learning techniques is low
  for realistic scenarios". A map of how load is measured, not a finding
  about code.
- **Wyrich, Bogner and Wagner, "40 Years of Designing Code Comprehension
  Experiments: A Systematic Mapping Study", 2023.** "We therefore
  conducted a systematic mapping study of 95 source code comprehension
  experiments published between 1979 and 2019." A map of study designs.
- **Fakhoury, Ma, Arnaoudova and Adesope, "The Effect of Poor Source Code
  Lexicon and Readability on Developers' Cognitive Load", ICPC 2018.**
  Only the replication package's README and a truncated abstract were
  read. The often-quoted result, that poor naming raised measured load
  where structural changes did not, was not verified and is not stated
  here.

None of these measures intrinsic, extraneous or germane load as such.
They measure time, correctness, ratings and physiological signals. What
they support, as read: vocabulary and textual size cost working memory;
notation changes that look small are not; a metric of control flow
explains part of comprehension and not the rest.

## A size that reviewers use

Google's guide for authors of changes, read in its repository: "There are
no hard and fast rules about how large is 'too large.' 100 lines is
usually a reasonable size for a CL, and 1000 lines is usually too large,
but it's up to the judgment of your reviewer. The number of files that a
change is spread across also affects its 'size.' A 200-line change in one
file might be okay, but spread across 50 files it would usually be too
large." The guide's reason is stated as reading, not as load: a small
change is "Reviewed more thoroughly" and "Less likely to introduce bugs".
The word "cognitive" does not appear in it.
