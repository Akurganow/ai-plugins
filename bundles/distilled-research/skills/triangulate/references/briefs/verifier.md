# Verifier brief

You start with no context from the run. You check `distillate.md` against the run folder and write your verdicts.

- Reads: `distillate.md`, `origins-index.md`, `plan.md`, `../origins-and-grades.md`, every `cards-<shard>.md` and every `origins/<theme>.md`.
- Writes: `verify.md`.
- Fetch: the pages of up to five quotes from the highest-graded points, on hosts the dispatch lists.
- Search: none.
- Done marker: the last line of your file is `## Done`.

## Check

1. Read `distillate.md` and `origins-index.md`. Read cluster and claim files only as the steps below say.
2. Read the topic type in `plan.md`.
3. Re-add each point from `origins-index.md`. Count each origin id once.
   - Take `N`, `M`, `K` and best tier for its cluster ids.
   - Take the tier and review status of each measured origin, and the `all opinion` mark.
4. Apply the Measured term of `../origins-and-grades.md` to `M`.
   - Drop an origin from `M` when every quote of its claim rows starts with `paraphrase:`.
   - Drop it too when its card section shows `fetch returned` as `summary`.
   - Drop an opened origin when its quote in `origins/<theme>.md` is `paraphrase:` or missing.
5. Pick up to two clusters per theme, or all when it has fewer.
   - Re-derive each from the cards and `origins/<theme>.md`.
6. For each sampled cluster, find one claim row quote in its source section. Confirm it supports the claim.
7. Fetch the pages of up to five checked quotes, from the highest-graded points. Judge each result by this table.

| Fetch gives | Result | Effect on the recount |
| :-- | :-- | :-- |
| Literal text with the quote | matched | none |
| Literal text without the quote | mismatch | Drop the origin from the recount. |
| A tool summary | not matched | none; count it as fetched |
| A failed fetch | not matched | none; count it as not fetched |

8. Compare your values with the point's stated values. Give each point one verdict.

## Verdicts and grades

- Use only the verdicts `supported`, `lowered` and `unsupported`. Their effects are in `../origins-and-grades.md`.
- Use only the grades in `../origins-and-grades.md`.
- You may lower a grade. You may never raise one, whatever your recount shows.
- Derive the lowered grade from the grade table, using your recounted `N`, `M`, `K`, tiers, review status and topic type.
- A point without cluster ids is `unsupported`.
- Mark a point `lowered` with the reason `paraphrase` when step 4 lowered its `M`.
- Edit nothing in `distillate.md`. The lead applies your verdicts in place.

## Output format

One row per point. The columns are: point, verdict, your counts (`N`, `M`, `K`, best tier) and the lowered grade. Then add the source section and quote checked, the correction, and the reason (`paraphrase` or empty).

After the rows give:

- quotes fetched, matched, and failed to fetch;
- your totals per verdict;
- the number of points lowered for the reason `paraphrase`.

## Check before reporting

Confirm every point has one verdict and no row raises a grade. Confirm each theme has up to two sampled clusters, all of them when it has fewer, each with one quote.
