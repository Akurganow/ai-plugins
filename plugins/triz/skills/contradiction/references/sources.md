<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Sources](#sources)
  - [The contradiction matrix](#the-contradiction-matrix)
  - [The 40 principles](#the-40-principles)
  - [Separation principles](#separation-principles)
  - [ARIZ-85C](#ariz-85c)
  - [Not read](#not-read)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Sources

What the references of this skill and of the `ariz` skill beside it were
checked against, how each was read, and what was not read. Both skills
link this one file. Dates are the day of reading. The sites that hold
the primary texts were not reachable from the network this was written on,
and each entry says what was read instead.

## The contradiction matrix

No single copy was taken. Two transcriptions were compared cell by cell
and the disagreements settled by majority against a third and a fourth, as
`matrix.md` describes. All are public repositories, read on 2026-09-23 at
the commits linked.

- The English spreadsheet, as it appears in
  <https://github.com/kamil-szczepanik/TRIZ-Agents/tree/23d5deb78a892a3dbb256b8c563a1b3c6f4a3fe2>
  and, cell for cell the same table, in three other repositories. That
  copy's metadata carries an author name and a creation date in 1997. One
  of its cells repeats a principle number, which the matrix never does.
  The WUMM project, below, labels this table "Matrix 1985".
- The Altshuller Foundation's table, at
  <https://www.altshuller.ru/triz/technique2.asp>, which could not be
  opened. One transcription of it was read in two public repositories,
  which agree on every cell and share the same two corrupt cells and the
  same missing one: a Russian CSV in
  <https://github.com/Meekl-e/workshop6_TRIZ/tree/9503eb38d2b9df126c3a84cce4aa85d69fd7c568>,
  which names no source, and `Matrix/Matrix1971.json` in
  <https://github.com/wumm-project/RDFData/tree/305000d4646e29d7170e4ddc0254502d4742fba4>,
  whose README names the Foundation's page as its source and labels the
  table "Matrix 1971".
- The third transcription is known only through the twenty-nine
  disagreements with the spreadsheet that
  <https://github.com/The-Leach/triz/blob/f83ab4647d9e714d8cbbdfd03468307de2d6bd09/data/matrix-crosscheck.md>
  records against "an independently published copy".
- The fourth is a fragment, rows 1 to 8, a truncated row 9, and columns 1
  to 15, transcribed from lecture notes in
  <https://github.com/cowdedroyal/Creative_thinking/tree/1687f559a051d261a34dabd2da7ed303c4b88e46>.

None of the four is a scan of a printed edition. The parameter and
principle names are the wording those transcriptions share, with the
variants noted in the references.

Altshuller describes the table's origin in «Творчество как точная наука»
(М.: Советское радио, 1979), read in the Russian original from the copy at
<https://github.com/wumm-project/OpenDiscovery/blob/eff06517637079619c97d598135cd5c9a409f615/Sources/Altshuller_GS/Altshuller-1979-ru.pdf>
on 2026-09-23. About forty thousand descriptions of selected higher-level
inventions were analysed for the table. It was then corrected for three
years with "prognostic corrections". It holds both the most frequent
principles and rare ones that give strong solutions.

Darrell Mann and Simon Dewulf, "Updating the Contradiction Matrix" (2003),
was read from the copy at
<https://github.com/arvindvenkatadri/teachingtriz/blob/e10f20c61a4907b453fd8863a8cff7bd98247a73/content/TRIZ/Modules/400-TRIZ-References/TRIZ-Related/Updating_the_Contradiction_Matrix.pdf>.
They write of a "lack of data concerning the detailed make-up of the
classical Matrix". They also write that the classic parameters do not fit
software, which is why they built a separate software matrix. No published
mapping of the 39 parameters to software was found. No study that measures
the classic matrix on software problems was found either. That is why the
software readings in `parameters.md` and `principles.md` are this skill's
own and say so.

Copyright. The transcriptions that say anything on the point assert that
the classic matrix, the 39 parameters and the 40 principles are in the
public domain. No legal source for that assertion was read. The matrix
carried here is the majority reading across the copies and not a copy of
any one file. Matrix 2003 and Matrix 2010 are separate works. Nothing from
them is carried here.

## The 40 principles

The sub-items in `principles.md` paraphrase the transcription at
<https://github.com/Robert-Adunka/triz-skills/blob/3d78740eac639a39f19a95a9aaa17c521497a3b9/contradiction-solver/references/40_Inventive_Principles_EN.md>,
MIT licence, copyright Robert Adunka, read 2026-09-23.

## Separation principles

- The four of ARIZ-77, from the 1979 book above, step 4.1 of the algorithm
  as printed there.
- The eleven of ARIZ-85C Table 2, from the English text below.
- The four of later teaching, from Valeri Souchkov's *Glossary of TRIZ and
  TRIZ-Related Terms*, version 1.0, MATRIZ, 2014, and from *Teaching TRIZ
  at School*, the TETRIS handbook, 2009, chapter 5, both read from copies
  in
  <https://github.com/arvindvenkatadri/teachingtriz/tree/e10f20c61a4907b453fd8863a8cff7bd98247a73/content/TRIZ/Modules/400-TRIZ-References>
  on 2026-09-23. The tables of Litvin and of Zlotin and Zusman that attach
  principles to each separation were read from
  <https://github.com/Robert-Adunka/triz-skills/tree/3d78740eac639a39f19a95a9aaa17c521497a3b9/physical-contradictions/references>.

## ARIZ-85C

Two copies were read on 2026-09-23.

- The Russian step text of АРИЗ-85-В, kept in
  <https://github.com/max-talanov/1/blob/8a40e29cc2ed0ffa4d1a7815b108ead31d6c59b5/Neurotechnologies_and_TRIZ/triz.md>.
  That copy cites the Altshuller Foundation's page,
  <https://www.altshuller.ru/triz/ariz85v.asp>, as its source and elides
  steps 5.4, 7.1 and 9.2. The Russian formulas quoted in
  [`ariz-85c.md`](../../ariz/references/ariz-85c.md) are from it.
- An English text, "Algorithm of Inventive Problem Solving, © G.S.
  Altshuller, 1956-1985", 33 pages, translator not named. Its own
  references are «Правила игры без правил» (Petrozavodsk: Karelia, 1989,
  pp. 11–50), Ideation International's *Tools of Classical TRIZ* (1999)
  and Invention Machine's TechOptimizer 2.51. Read from
  <https://github.com/arvindvenkatadri/teachingtriz/blob/e10f20c61a4907b453fd8863a8cff7bd98247a73/content/TRIZ/Modules/400-TRIZ-References/TRIZ-Related/ariz85c_en.pdf>.
  Steps 5.4, 7.1 and 9.2, Table 2 and the opening warning quoted in
  [`ariz-85c.md`](../../ariz/references/ariz-85c.md) are from it.

The Foundation's pages, including Table 1 and Table 2 in Russian, were not
reachable. Neither was the English translation MATRIZ publishes at
<https://matriz.org/wp-content/uploads/2025/09/Altshuller_ARIZ-85-C_en.pdf>.

The naming of the version, 85-А, 85-Б, 85-В, and the count of forty steps
in nine parts rest on search-engine summaries of pages that could not be
opened, Vladimir Petrov's history of ARIZ and the entry "Как устроен
АРИЗ-85В" at <https://triz.org.ua/works/ws89.html>, and on counting the
steps in the copies above.

Two printed editions of the algorithm were not opened. Г. С. Альтшуллер,
«Найти идею», Новосибирск: Наука, 1986. Г. С. Альтшуллер, «АРИЗ — значит
победа», in «Правила игры без правил», Петрозаводск: Карелия, 1989, pp.
11–50.

## Not read

The following are named in TRIZ literature and were not opened from the
network this was written on. Nothing in either skill is quoted from them.

- Genrich Altshuller, *40 Principles: TRIZ Keys to Technical Innovation*,
  Technical Innovation Center, 1997.
- Genrich Altshuller, *The Innovation Algorithm*, Technical Innovation
  Center, 1999. Translation of «Алгоритм изобретения», second edition,
  1973. The 1979 book cites that edition for the printed table.
- Genrich Altshuller, *Creativity as an Exact Science*, Gordon and Breach,
  1984, the English translation of the 1979 book read in Russian above.
- Г. Альтов, «И тут появился изобретатель», М.: Детская литература,
  1984. English: *And Suddenly the Inventor Appeared*, Technical
  Innovation Center, 1996.
- Kevin C. Rea, "TRIZ and Software – 40 Principle Analogies", *TRIZ
  Journal*, 2001, and the later analogy lists for software by Fulbright
  (2004), Mishra (2010) and Beckmann (2015). The software readings in
  `principles.md` were written without them.
