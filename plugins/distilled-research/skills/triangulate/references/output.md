# Output

The reply is the distillate, in the order below, unless the user asked for a form ("A requested form" below). Grades, `N`, `M`, `K` and tiers come from `origins-and-grades.md`. The lists behind the reply stay in `appendix.md`. Report final totals only.

1. **Answer:** write one opening sentence, up to four direction sentences and one closing caveat sentence.
   - The opening sentence answers in plain words. For "it depends", name the question, not the topic, and say on what.
   - Write one direction sentence per direction that bears on the answer.
   - Give it a grade word from the legend, the strongest study (first author, year) and its effect with interval.
   - Leave other points in the table.
   - Use no other word of strength, such as "weakly" or "consistent".
   - The closing sentence names the largest caveat when it bears on the answer.
2. **Legend:** copy these lines unchanged, in this order:
   - the Legend text column of the grade table in `origins-and-grades.md`;
   - the counts legend line in `origins-and-grades.md`;
   - the Legend text column of the tier table in `../../vet-sources/references/tiers.md`;
   - this line: "Grades and tiers are ordinal and uncalibrated. They rank claims in this run and give no probability."
3. **Table:** write one row per point, with the columns below.
   - Order the rows Established, Probable, Contested, Tentative, Not established. A Not established point also appears in its own section.
4. **Contested:** list each Contested point's positions, then its "Why the sides differ" line.
   - List each position with its origins, tier, first-public date, and measured or asserted.
   - Copy the `differ` line of the cluster as the "Why the sides differ" line.
   - Pick no side, unless the positions differ in tier. Say so in one sentence.
5. **Not established:** list each point graded Not established, and what would settle it per `## Gaps`.
6. **Caveats:** write one line per theme, copied from `distillate.md`, naming the theme.
7. **Skipped:** list sources found and not read, by reason.
   - Give the count per reason, then up to five URLs each. For `host not approved`, give hosts and no URLs.
   - Name every retracted source with its URL. List any skipped stage.
   - List each source searched for and not found, its cause, and who named it (the plan's queries or the user).
8. **Appendix:** name the path of `appendix.md`, which holds the full lists.
9. **Header line:** end with one line, with these slots.
   - Depth and date.
   - Sources read in full, abstract and snippet.
   - Verifier mode, quotes matched of those fetched, quotes not fetched, points lowered.
   - Points whose `M` the verifier lowered because every quote of a measured origin was `paraphrase`.
   - Card quotes that were literal and card quotes that were `paraphrase`, summed from the `quotes:` line of each cards file.
   - When item 1 of the stage-0 report answered no or unknown on redirects, add: "the fetch tool may have followed a redirect to an unlisted host before the check".
   - When no card quote and no tracer quote was literal, add: "no quote was literal; no point can reach Established".
   - Write "shared-context check" as the mode when no independent verifier ran.
   - On a science or health topic, add: "agreement among sources; not medical advice".

| Column | Content |
| :-- | :-- |
| Claim | One sentence, with its `kind`. A Contested row says "Studies disagree on ...". |
| Grade | A grade from the legend. Show Established as Probable when no independent verifier ran. Add "(lowered by the verifier)" on every lowered point. |
| `N (M) + K` | Copy the final row of `distillate.md`. |
| Evidence | Per study: year (the card's `first-public date`), first author, name, design, `n`, population and effect with its interval, copied from the cards. Add `preprint` when the card's review status says so. Add `read: full`, `abstract` or `snippet`. End with up to two plain URLs, best tier first. |
| Dissent | The strongest opposing origin, or "none found". An untraced or `unconfirmed` opposing source shows as a `K` line. |

- Evidence URLs are plain, on hosts the run could read. Embed no images. Copy no link text from a page.
- Mark every date or collapse the run did not open as `unconfirmed`.
- Never say that a failed check changed no grade unless you name the rows.

## A requested form

When the user asks for a length or a form, such as a short answer, one section or about 500 words, the reply takes that form instead of items 1 to 9. Every form keeps these:

- The grade word of each point the reply states, by the Grade column above.
- The line "Grades and tiers are ordinal and uncalibrated. They rank claims in this run and give no probability."
- Each line that item 9 adds and that applies: the redirect line, the no-literal-quote line and the science or health line.
- The paths of `distillate.md` and `appendix.md`, which hold the table and the full lists.
