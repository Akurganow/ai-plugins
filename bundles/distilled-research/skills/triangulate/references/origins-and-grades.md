# Origins and grades

Two axes grade each point: how many independent origins state it, and how good the best one is. Counts of origins and tiers decide each grade. A point is a row of `distillate.md`. A claim row is a row of a cards table.

## Origins

| Term | Meaning |
| :-- | :-- |
| Traced origin | Its identity is recorded, its first-public date comes from a page the run opened, and one of three holds: (a) it reports its own measurement or dataset; (b) it cites a named origin that the reader or tracer resolved and dated; (c) it is a tier A or B document of record that states the claim. |
| States the claim | The origin's own opened text says it. A source that cites the origin does not count. |
| Unconfirmed | A date, claim or link between sources known only from memory, a search result or a snippet. It is never a traced origin, never collapses a family, and counts toward `K`. |
| Independent | The tracer found no counted origin that it copies, cites for the claim or forks. It shares no author, organisation or dataset with one. A family collapses to one origin, on evidence from a card or an opened page. |
| Untraced | Every other source whose own opened text states the claim. `K` counts them. They show spread and never support a grade. |
| Measured | A traced origin read `full` that reports its own measurement. It counts toward `M` only when a quote on file for it is literal: one of its claim rows, or the quote in the file of the tracer that opened it. A quote is literal only when the fetch tool returned the page's own text. An origin with no literal quote on file counts toward `N`, never `M`. One read at `abstract` also counts toward `N` and never `M`. |

## Output form

Each point shows `N (M) + K` and its best tier. `M` is a subset of `N`, and `M` = 0 reads as unmeasured. A point's `N`, `M` and `K` count each origin id once across its clusters. `K` never enters a grade. Best tier is the best tier among the traced origins of the point. Untraced sources never count. A measurement whose review status is `preprint` is an unreviewed preprint. Tier names come from `../../vet-sources/references/tiers.md`.

Counts legend text: `N (M) + K: N is independent origins. M is measurements among them, read in full with a literal quote. K is read sources that repeat the claim without a traced origin.`

## Grade table

Apply the rows in order. The first row that fits sets the grade. The ladder, highest first: Established, Probable, Tentative, Not established. Contested stands outside it. Write each grade in full. The reply copies the Legend text column.

| Grade | Rule | Legend text |
| :-- | :-- | :-- |
| Contested | Two positions rest on different traced origins, at least one side tier A or B or measured. A finding that only narrows the claim edits the claim text instead. | Contested: independent origins on both sides, at least one side tier A, tier B or measured. It is no rank and does not weigh the sides. |
| Established | At least one claim row is not `opinion`. `N` >= 3. `M` >= 1 from tier A, or on a topic other than science or health from tier A or B. On a science or health topic, a measurement from an unreviewed preprint counts as tier B. The reply shows the point as Probable when no independent verifier ran. | Established: three or more independent origins, one a tier A or B measurement, and the verifier agreed. On a science or health topic the measurement is tier A and no unreviewed preprint. |
| Probable | At least one claim row is not `opinion`. `N` >= 2 with a tier A or B origin. | Probable: two or more independent origins, one from a tier A or B source. |
| Tentative | `N` >= 1 and no row above fits. Every point whose claim rows are all `opinion` lands here. | Tentative: one origin, an opinion, or only lower-tier origins. |
| Not established | `N` = 0, or the point has no cluster ids. | Not established: no independent origin was traced, or the verifier found the point unsupported. |

## Verifier verdicts and their effect

| Verdict | Effect |
| :-- | :-- |
| supported | The grade stands. |
| lowered | Replace the point's grade, `N`, `M`, `K` and best tier with the verifier's values. The verifier derives the grade from the table. It is Not established only when `N` = 0. |
| unsupported | The grade is Not established. |

The lead edits the point's row in `distillate.md` in place. A Contested point keeps its grade on `supported`. On `lowered`, the lead tests the Contested row again with the verifier's origins. If both positions still rest on different traced origins, it stays Contested and the lead narrows its claim text. Otherwise the verifier's grade stands for the one position left. On `unsupported` it becomes Not established. Any grade in a run file that is not on the ladder or Contested is an error. The lead stops and fixes it.
