# Lead formats

Only the lead reads this file.

## origins-index.md

One line per cluster: id, theme, claim, `N`, `M`, `K`, best tier, traced origin ids and untraced source ids. Mark each measured origin with its tier and review status. Copy the `all opinion` mark of a cluster. The lead reads the index for counts. It opens a theme file only to copy evidence, dissent, the Caveats line and the gaps.

## distillate.md

One row per point: the point, grade, `N`, `M`, `K`, best tier, cluster ids, evidence and dissent. An evidence cell holds at most 25 words per origin. The file ends with one `## Caveats` line per theme, copied from the theme files. The lead edits a row in place when a verdict changes it.

## Stage 8 without subagents

The lead cannot drop its transcript, so the check is a shared-context check.

1. Run the steps of `briefs/verifier.md` with the file-read tool.
2. Write the result as `verify-shared.md`, labelled "shared-context check".
3. Offer a fresh session that names the run folder. In it, run stage 8 with the verifier mode independent.
4. Without an independent verifier, Established points show as Probable.

## appendix.md

Copy these lists from the files. Give each entry its reason.

- Excluded: vet rows with `keep` = `no`, and overflow leads.
- Read: each source with its `read` level.
- Not read: each source with its error code, and each source on the over-limit list in `plan.md`.
- Lane gaps: each collector's `## Gaps`.
