# Sources

What the references in this skill were checked against, how each was read,
and what was not read. Dates are the day of reading. The book's own site
and every publisher and journal site named below were not reachable from
the network this was written on, and each entry says what was read
instead.

## The book

John Ousterhout, *A Philosophy of Software Design*. First edition, Yaknyam
Press, 2018, ISBN 978-1732102200. Second edition, Yaknyam Press, 2021,
ISBN 978-1732102217. Section numbers in this skill are the second
edition's, and the page numbers inside the two summaries are the book's
own.

No copy of either edition was bought. The first edition's English text
was read section by section in a public translation repository that
interleaves it with Chinese. Whether that copy is authorised was not
established. The skill quotes passages of a few sentences at most from it
and reproduces no longer extract. Full-text files of either edition that
a search engine surfaces on document-sharing sites were not opened. What
was read, on 2026-09-24:

- The second edition's preface, each chapter's opening and conclusion,
  its back matter, and the passages the second edition added or reworked,
  in English, from a public translation repository that keeps those
  parts in the original language, at
  <https://github.com/yingang/aposd2e-zh/tree/4362314d5bb8eedbe2a088f950850a187b3f8641/docs/en>.
  Its `summary.md` is the source of the "Summary of Design Principles"
  and the "Summary of Red Flags" quoted in `principles.md` and
  `red-flags.md`. The repository's `docs/README.md` translates the
  author's note on what the second edition changed: chapter 6 reworked
  and absorbing the first edition's §9.7 and §10.9, passages on *Clean
  Code* added to chapters 9 and 12, chapter 21 added. Quotations marked
  **2e** are from this copy.
- The first edition's English text, at
  <https://github.com/Cactus-proj/A-Philosophy-of-Software-Design-zh/tree/20d96914b82f02c225cc1530022555d84c27b096/docs>.
  Quotations marked **1e** are from this copy, at the section the second
  edition gives the same text. Where the second edition reworded a
  passage and the reworded text is in the second-edition copy, the
  reworded text is quoted and marked 2e. Where it is not, the first
  edition's wording is quoted and marked 1e.
- Two further copies of the principles list, compared item by item with
  the first:
  <https://github.com/dmahr1/quick-reference/blob/6330aea52335dcc9c788b3c0475f1684194aae50/index.md>
  and
  <https://github.com/farzinnasiri/learning-hub/blob/6e62cdcda06d5396f9f622a945d13ae93b8a6891/software-engineering/philosophy-of-software-design.md>.
  All three agree on the sixteen items and their order. The first
  edition's fifteen were read in the Cactus-proj copy and in a 2019 note
  at
  <https://github.com/haiiiiiyun/haiiiiiyun.github.io/blob/78ed1d4140ace5e703f3eb08c0eb0b9118126cc1/_posts.bak/2019-02-27-tips-from-a-philosophy-of-software-design.md>.
- Reading notes on the second edition, used to confirm the chapter list,
  at
  <https://github.com/sglavoie/sglavoie.github.io/blob/25be05a3a7e78c36afe0a6ada8a8055501d91006/content/posts/book-summary-philosophy-software-design-2nd-edition.md>.
  Nothing is quoted from them.
- The edition facts: the first edition's publisher, year and ISBN from
  the Wikipedia article on John Ousterhout, listed under Wikipedia below.
  The second edition's date and ISBN come from bookseller listings as a
  search engine summarised them. The listings were not opened.

The preface says the book "is based on the design principles that emerged
from" the author's Stanford course CS 190, and calls itself "an opinion
piece". Nothing in this skill is described as research. The course pages
were not reachable.

## Ousterhout and Martin

John Ousterhout and Robert C. Martin, "A Philosophy of Software Design vs
Clean Code", a written discussion held between September 2024 and February
2025, published at
<https://github.com/johnousterhout/aposd-vs-clean-code/blob/2ce0742228fbf850e15101f83308de2cd72144b2/README.md>,
read whole on 2026-09-24. Quotations in `positions.md`, `complexity.md`,
`principles.md` and `red-flags.md` are marked with its section headings:
Introductions, Method Length, Method Length Summary, Comments, Comments
Summary, Test-Driven Development, TDD Summary, Closing Remarks. The
speaker is named in each case. Martin's words are from the discussion.
The one sentence of *Clean Code* quoted in `positions.md` is the one
Ousterhout quotes there.

## Parnas

D. L. Parnas, "On the Criteria To Be Used in Decomposing Systems into
Modules", *Communications of the ACM* 15(12), 1972, pp. 1053–1058. The
journal printing was not reachable. Read instead: a transcription of the
August 1971 Carnegie-Mellon technical-report text, at
<https://github.com/taowen/awesome-lowcode/blob/5de5c9201c46dd350607d53394b34303731baca0/on-the-criteria-to-be-used-in-decomposing-systems-into-modules/README.md>,
on 2026-09-24. The conclusion quoted in `decisions.md` and `red-flags.md`
is from it. The journal, volume and page facts are from the Wikipedia
article on information hiding, listed below.

## Brooks

Frederick P. Brooks, Jr., "No Silver Bullet: Essence and Accident in
Software Engineering", 1986. Read from a public copy of the 1986 text at
<https://github.com/efrainefeso/No-Silver-Bullet/blob/d64ca5b6c20cb22a76cf5dbc67ab354c187ce13a/Brooks-NoSilverBullet.pdf>,
on 2026-09-24, with the text extracted by a PDF library. The quotations in
`complexity.md` are from it. The later printings, in *IEEE Computer* in
1987 and as a chapter of the anniversary edition of *The Mythical
Man-Month*, are known from the Wikipedia article on the essay, listed
below. The 1975 *Mythical Man-Month* was not read.

## Google's reviewer guide

Google, "What to look for in a code review" and "The Standard of Code
Review", in the `eng-practices` repository, read at
<https://github.com/google/eng-practices/blob/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/looking-for.md>
and
<https://github.com/google/eng-practices/blob/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/standard.md>
on 2026-09-24. Quotations in `complexity.md`, `principles.md` and
`decisions.md` are from the first.

## Nygard's decision-record template

Michael Nygard, "Documenting Architecture Decisions", 2011. The post was
not reachable. The template was read as reproduced in
<https://github.com/joelparkerhenderson/architecture-decision-record/blob/b1de91256a57110b655ff3572ce1fc41fbc2dac6/locales/en/templates/decision-record-template-by-michael-nygard/index.md>
on 2026-09-24, which names the post as its source.

## Wikipedia

Read on 2026-09-24 as raw wikitext, each for the fact named:

- *John Ousterhout*,
  <https://en.wikipedia.org/w/index.php?title=John_Ousterhout&action=raw>:
  the first edition's publisher, year and ISBN.
- *Information hiding*,
  <https://en.wikipedia.org/w/index.php?title=Information_hiding&action=raw>:
  the journal, volume, issue and pages of Parnas 1972.
- *No Silver Bullet*,
  <https://en.wikipedia.org/w/index.php?title=No_Silver_Bullet&action=raw>:
  the essay's year and later printings.
- *Architecture tradeoff analysis method*,
  <https://en.wikipedia.org/w/index.php?title=Architecture_tradeoff_analysis_method&action=raw>:
  that the method weighs quality attributes against each other with
  stakeholders, which is all `SKILL.md` says of it.
- *Test-driven development*,
  <https://en.wikipedia.org/w/index.php?title=Test-driven_development&action=raw>,
  and *Cyclomatic complexity*,
  <https://en.wikipedia.org/w/index.php?title=Cyclomatic_complexity&action=raw>:
  the two evidence summaries in `positions.md`. The papers those pages
  cite were not opened.

## Not read

Named in the references or in the literature around them, and not opened
from the network this was written on. Titles are given as commonly cited
and were not verified against the works. Nothing in this skill is quoted
from them.

- Robert C. Martin, *Clean Code*, Prentice Hall, 2008.
- The Software Engineering Institute's Architecture Tradeoff Analysis
  Method, Kazman, Klein and Clements, technical report CMU/SEI-2000-TR-004,
  2000. Only the Wikipedia article on the method was read.
- Y. Rafique and V. B. Mišić, "The Effects of Test-Driven Development on
  External Quality and Productivity: A Meta-Analysis", *IEEE Transactions
  on Software Engineering* 39(6), 2013. D. Fucci and others, "A Dissection
  of the Test-Driven Development Process: Does It Really Matter to
  Test-First or to Test-Last?", *IEEE Transactions on Software
  Engineering* 43(7), 2017. Known through Wikipedia's sentences only.
- D. I. K. Sjøberg and others on code smells and maintenance effort,
  *IEEE Transactions on Software Engineering*, 2013. D. Landman, A.
  Serebrenik and J. Vinju on cyclomatic complexity and lines of code,
  2014 and 2016. C. Zhang and D. Budgen on the effectiveness of design
  patterns, *IEEE Transactions on Software Engineering*, 2012. None
  opened, so no finding of theirs is reported.
- The author's site, including the book page and the second-edition
  extract, and the Stanford CS 190 course pages.

## What the skill adds on its own

These parts of `SKILL.md` and the references are this skill's adaptation
for a review and not the book's text:

- The order of the steps in `SKILL.md`, the rule that the first step
  fixes who reads and who changes the design, and the routing of a
  one-question user to a step.
- The depth test in Step 3, a one-line interface against a one-line
  function, and the calibration that a small utility or a thin adapter is
  shallow by nature.
- The rule in Step 4 that a reason the user gives is recorded beside the
  finding, and drops it only when the user says it outweighs the flag.
- The ranking of findings by the part's weight in the formula, and the
  choice to give no other overall ranking.
- Every "Look for" paragraph in `red-flags.md`.
- The reading of principle 7 as bounded by Google's over-engineering
  line, and the reading of principles 6 and 10 as one idea from two
  sides, in `principles.md`.
- The reading of Brooks against Ousterhout in `complexity.md`.
- The "For a review" paragraphs in `positions.md`.
- The hand-overs to the `cognitive-load`, `triz` and `toc-thinking`
  skills of this marketplace.
