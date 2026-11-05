# Depth

Counts are planned. The lead states the table row of each depth in the stage-0 report, before anything starts, with the children as a ceiling. The row shows scope only. Every depth reads the kept tier A or B primary sources, up to its child ceiling.

| Depth | Lanes x rows | Children | Opens per tracer |
| :-- | :-- | :-- | :-- |
| quick (recommended default) | 2 x 12 | at most 12 | 0; the lead traces origins |
| standard | 4 x 25 | at most 30 | 3 |
| deep (on request only) | 6 x 30 | at most 40 | 5 |

## Rules for every depth

- At most 4 children run at once.
- The verifier always runs.
- Kept sources never exceed lanes x rows. A row cut by a lane's row cap goes to the overflow-leads list.
- The ceiling covers every child. Readers allowed = ceiling − collectors − vetters − tracers − 1 verifier.
- A quick run has no tracer. Standard and deep have one tracer per theme.
- Cap themes at 6 (standard) and 8 (deep), keeping readers allowed above 0. Merge surplus sub-questions in stage 0.
- Size the reader set last, best tier first. Record sources over the limit in `plan.md`.
- The lead opens no origin at quick depth. An origin it cannot date from the cards is a gap.

## Shards

A shard is a set of rows the lead assigns to one child.

- A vetter takes at most 25 rows. Vetter shards follow `merged.tsv` and are named `v1`, `v2` and so on.
- A reader takes at most 5 sources. Shard kept vet rows best tier first, named `r1`, `r2`, and so on.
- A pasted run uses the order of `candidates-user.md`.
