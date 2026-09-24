# Sources

What the references in this skill were checked against, how each was read,
and what was not read. Dates are the day of reading. Every publisher,
preprint server and aggregator tried was unreachable from the network this
was written on, so most papers were read as abstracts mirrored in public
repositories, and each entry says so. Nothing is quoted from a paper whose
text was not opened in some form.

## The practitioner essay

Artem Zakirullin, "Cognitive load is what matters", copyright (c) 2023
Artem Zakirullin, Creative Commons Attribution 4.0 International, "a
living document, last update: June 2026" by its own status line. Read
whole, with its agent-facing summary and its licence file, on 2026-09-24
at
<https://github.com/zakirullin/cognitive-load/tree/d2d60d2311c3854f16d87bf34f38c829667be2a4>.
Every quotation in `patterns.md` is from its `README.md` at that commit.
Its "roughly four such chunks" links to the repository's own issue 16,
which was opened: the only visible post in it questions the figure and
has no reply. The essay cites neither Cowan nor Miller.

## The theory

Read on 2026-09-24. "Mirror" means a public repository file that carries
the paper's abstract verbatim, cited by path and commit.

- Sweller, "Cognitive Load During Problem Solving: Effects on Learning",
  *Cognitive Science* 12(2), 1988, pp. 257–285. Abstract, mirror:
  <https://github.com/yiren-liu/coquest/blob/0ea8c605686d3342bca8ac888ef1fc29cb28c5f8/backend/paper_graph/data/venue_txt/1823_.txt>.
- Sweller, van Merriënboer and Paas, "Cognitive Architecture and
  Instructional Design", *Educational Psychology Review* 10, 1998, pp.
  251–296. Abstract, mirror:
  <https://github.com/OpenKnowledgeMaps/Headstart/blob/3b227c8866baa2e9865f45ced3a7fa6975cb336e/server/static/data/edu4.csv>.
- Sweller, "Element Interactivity and Intrinsic, Extraneous, and Germane
  Cognitive Load", *Educational Psychology Review* 22, 2010, pp. 123–138.
  Abstract, mirror:
  <https://github.com/aslakhol/thesis/blob/1f81ed09a7e997a4db7e03b172db3242cd79966b/library.bib>.
- Sweller, van Merriënboer and Paas, *Educational Psychology Review* 31,
  2019, DOI 10.1007/s10648-019-09465-5. Abstract,
  mirror:
  <https://github.com/lexnederbragt/ten_quick_tips_live_coding/blob/8a5f69b2a08f81070c294764f8b6c1f0ea63725b/references.bib>.
  The one body sentence quoted in `theory.md` was read as a third party
  quotes it, at
  <https://github.com/AadiTakle/aai-gt-screening/blob/7b83147bab91b40fadff9c37d91898f34f66c877/brainlifting/reasoning-growth-brainlift/brainlift-reasoning-growth.md>,
  and `theory.md` says so.
- Cowan, "The magical number 4 in short-term memory: A reconsideration of
  mental storage capacity", *Behavioral and Brain Sciences* 24, 2001, pp.
  87–114. Abstract, mirror:
  <https://github.com/yiren-liu/coquest/blob/0ea8c605686d3342bca8ac888ef1fc29cb28c5f8/backend/paper_graph/data/venue_txt/2002_.txt>.
- Miller, "The Magical Number Seven, Plus or Minus Two: Some Limits on Our
  Capacity for Processing Information", *Psychological Review* 63, 1956.
  Full text, mirror:
  <https://github.com/chsasank/chsasank.github.io/blob/58e2ab7e19709ed088ba2089aad39fee5ea261ab/_posts/classic_papers/2020-09-19-magic-number-seven.md>.
- Wikipedia, read as raw wikitext on 2026-09-24: *Cognitive load*
  (revision 1372321243), *Worked-example effect* (1374577294), *Split
  attention effect* (1358740769), *Expertise reversal effect*
  (1373503326). The attribution of the terms intrinsic and extraneous to
  Chandler and Sweller 1991, the article's definitions of the two, the
  list of effects demonstrated in the 1990s, the sentence on dividing a
  schema into subschemas, and the three effect definitions in `theory.md`
  are from these pages.

## The measures

- G. Ann Campbell, "Cognitive Complexity: A new way of measuring
  understandability", SonarSource. The publisher's copy was not reachable.
  The text was read from a public copy interleaved with a translation, at
  <https://github.com/baibaichen/blogs/blob/1d1bee7ab8086692b4422aab99da71ae04b8b949/paper/COGNITIVE%20COMPLEXITY.md>,
  on 2026-09-24. The copy carries no author line. The attribution to the
  paper and to G. Ann Campbell is from the README of a third-party
  implementation,
  <https://github.com/matkoch/resharper-cognitivecomplexity/tree/598c5370998c6bded546f87eab4b3c1488f59570>.
  PMD's rule links the paper without naming its author. Corroborated
  against SonarSource's own Java implementation,
  <https://github.com/SonarSource/sonar-java/blob/19c175083700fce46f80c3c133c4609c12857234/java-frontend/src/main/java/org/sonar/java/ast/visitors/CognitiveComplexityVisitor.java>,
  its rule text at tag `5.14.0.18788`, its ESLint plugin's rule document
  at
  <https://github.com/SonarSource/eslint-plugin-sonarjs/blob/fa48884330437fab852b9a52256183b7d140259b/docs/rules/cognitive-complexity.md>,
  and PMD's rule at
  <https://github.com/pmd/pmd/blob/0a145687301d8e330271e27ff3d9ab279fb565a8/pmd-java/src/main/resources/category/java/design.xml>.
- Muñoz Barón, Wyrich and Wagner, "An Empirical Validation of Cognitive
  Complexity as a Measure of Source Code Understandability", ESEM 2020.
  Abstract, mirror:
  <https://github.com/heuerleon/bachelor-thesis-public/blob/75298b791ed590fdf6f1151ff9c0af6102510596/src/res/literature.bib>.
  Replication package README at
  <https://github.com/mmunozba/esem20-cognitive-complexity-validation/tree/a4b08a7f3e4ffd9207e02d244f55ce97fbd3db98>.
- Tavares de Souza and Costa Pinto, "Toward a Definition of
  Cognitive-Driven Development", ICSME 2020. Read whole from the first
  author's copy at
  <https://github.com/asouza/pilares-design-codigo/blob/a693d8001b787e9e3762fdebb6f0dfc3a0784175/ICSME-2020-cognitive-driven-development.pdf>,
  with the text extracted by a script, so spacing inside quotations was
  reconstructed.
- Google, "Small CLs" and "What to look for in a code review", in the
  `eng-practices` repository, read at
  <https://github.com/google/eng-practices/blob/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/developer/small-cls.md>
  and
  <https://github.com/google/eng-practices/blob/3bb3ec25b3b0199f4940b1aa75f0ac5c5753301c/review/reviewer/looking-for.md>.

## The studies of programmers

Abstracts, from mirrors, read on 2026-09-24:

- Peitek, Apel, Parnin, Brechmann and Siegmund, ICSE 2021:
  <https://github.com/serqco/qabstracts/blob/9f3d93a0070a785c1c9829886eb1c89ffd4c3b4c/prestudy/abstracts.raw/PeiApePar21.txt>.
  Replication package
  <https://github.com/brains-on-code/fMRI-complexity-metrics-icse2021/tree/ed6c0028742012a1a63e22508e9851ae70aab1b4>.
- Hansen, Goldstone and Lumsdaine, 2013, arXiv 1304.5257:
  <https://github.com/mpickering/blog/blob/54cfa8e13791f7a8507967b42f5e4c681a729c56/library.bib>.
  The first author's post at
  <https://github.com/synesthesiam/blog/blob/309efa1d6589e59d0fabbdae3ce6830997ef6cbd/posts/what-makes-code-hard-to-understand.markdown>.
- Gonçales, Farias, da Silva and Fessler, ICPC 2019:
  <https://github.com/kleinnerfarias/kleinnerfarias.github.io/blob/8b74a3a412b5de8765a551c97a30800927989b73/publication/icpc-2019/index.html>.
- Wyrich, Bogner and Wagner, 2023, arXiv 2206.11102:
  <https://github.com/dabi-team/someData/blob/74b8f4f141f9dcc58f17d6f1f6c3408ad7c3a170/data/Software/2206.11102.txt>.
- Fakhoury, Ma, Arnaoudova and Adesope, ICPC 2018: the replication
  package's README at
  <https://github.com/smfakhoury/fNIRS-and-Cognitive-Load/blob/53f03081736adb6359068aa9767261b891c68585/README.md>,
  which gives the title and the design, and a truncated abstract at
  <https://github.com/AndresPonciano/finalprojectforsure/blob/f2a87eb157180b64cb0ecd94fc019ef817d7cfa4/data/elasticsearchScripts/data_finalfiles_ndjson/VeneraArnaoudova.json>,
  cut off before its result. The result was not read.

## Not read

Named in the literature and not opened from the network this was written
on. Titles are given as commonly cited and were not verified against the
works. Nothing in this skill is quoted from them.

- Chandler and Sweller, "Cognitive Load Theory and the Format of
  Instruction", *Cognition and Instruction* 8(4), 1991. The origin of the
  intrinsic and extraneous distinction, known here through Wikipedia.
- Sweller, "Cognitive load theory, learning difficulty, and instructional
  design", *Learning and Instruction* 4, 1994.
- Kalyuga, *Educational Psychology Review* 23(1), 2011, pp. 1–19, as two
  readers' notes cite it. Known here through a search engine's summary and
  those notes.
- Sweller, Ayres and Kalyuga, *Cognitive Load Theory*, 2011. The
  catalogue of effects. Known here through a search engine's table of
  contents.
- Duran, Zavgorodniaia and Sorva, "Cognitive Load Theory in Computing
  Education Research: A Review", *ACM Transactions on Computing
  Education* 22(4), 2022.
- Matthew Skelton and Manuel Pais, *Team Topologies*, IT Revolution,
  2019. What was read is its public reference list, which cites Sweller
  1988 and 1994, and its glossary translations, which carry the three
  kinds of load as entries without definitions, at
  <https://github.com/TeamTopologies/Team-Topologies-Book-References/tree/5207ac26845b13e807e1fff987877897b041dbc0>
  and
  <https://github.com/TeamTopologies/Team-Topologies-Glossary-Translations/tree/64d952b437a34a9b9f3e14d6d8aa7f2178741b25>.
  The authors' "Team Cognitive Load Assessment" template repository, at
  <https://github.com/TeamTopologies/Team-Cognitive-Load-Assessment/tree/39b542e1da873abbe39a4c05d84c172bbf983b27>,
  is empty apart from a link. Nothing about how the book defines team
  cognitive load is stated in this skill.
- Ousterhout, *A Philosophy of Software Design*. Its three symptoms of
  complexity, change amplification, cognitive load and unknown unknowns,
  belong to that book and to the `design-review` package of this
  marketplace, which cites them by section. This skill does not present
  them as cognitive load theory.
- The later Cognitive-Driven Development papers, a 2022 evaluation of
  Cognitive Complexity in the *Journal of Systems and Software* seen in a
  search listing only, and the authors' sites for Team Topologies,
  SonarSource and the ICSE study.

## What the skill adds on its own

These parts of `SKILL.md` and the references are this skill's adaptation
for work on code and not any source's text:

- The order of the steps, the rule that the frame names the reader before
  any judgement, and the newcomer as the default reader.
- The reading of the user's own phrasings in Step 2 against the essay's
  three questions, and the rule for a place nobody measured.
- The count in Step 3 of elements that must be related to one another,
  and the structural test that applies the 2010 abstract's
  essential-to-the-task line to code by asking whether the element
  survives every structure that does the same task. The tie-break there,
  that the extraneous test decides when both seem to answer yes.
- The sentence under Capacity in `theory.md` that reading code blocks no
  recoding, so the four is not a budget, and the two cautions on
  Intrinsic Complexity Points in `measures.md`.
- The triage order in Step 4, and the stop rule for a place whose count
  is small and all intrinsic.
- The ranking in Step 6 by extraneous count times how often readers do
  the task there.
- Every "Look for" paragraph in `patterns.md`, the bridge sentence under
  "Too many small methods" that puts deep and shallow modules in this
  skill's terms, and the "For code" sentences under the effects in
  `theory.md`.
- The decision to work with two loads and to give germane load no action
  of its own, drawn from the 2010 and 2019 abstracts and the questioning
  of additivity, and the reading of "instructional procedures" as the
  structure of the code.
- The "What this means for code" paragraph under Capacity in
  `theory.md`, and the sentence there that a developer reading code is
  often not learning it.
- The reading of the studies in `measures.md` as the paragraph that
  begins "What they support".
- The hand-overs to the `design-review`, `triz` and `toc-thinking` skills
  of this marketplace.
