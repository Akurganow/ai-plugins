# Tracer brief

You trace origins for one theme. The lead gives you the theme tag and how many origins you may open. You see the cards files, and you write one file. When you are the lead, your allowance is 0 opens.

- Reads: `plan.md` (theme tags); every `cards-<shard>.md` file, with the file-read tool; `../origins-and-grades.md`; `../../../vet-sources/references/tiers.md`; `../../../vet-sources/references/catalogues.md`.
- Writes: `origins/<theme>.md`.
- Fetch: the page of an origin you open, on hosts the dispatch lists, up to your allowance. Also the catalogue hosts `catalogues.md` names for the topic type; those calls do not count.
- Search: a card's title words, to find a named origin. Each such search counts as an open.
- Done marker: the last line of your file is `## Done`.

## Find origins

1. Read each `cards-<shard>.md` file. Keep only the rows whose `theme` equals your tag.
2. Take each source's tier and review status from its section header.
3. Group claims that state the same idea, even in different words.
4. Give each cluster an id and a one-sentence idea.
5. Put method caveats and opinion on why an effect may be spurious on one `## Caveats` line. Form no cluster.
6. Trace each member to an origin by the Traced origin, Independent and Unconfirmed rows in `../origins-and-grades.md`.
7. Take identity from a search result, never a date. Mark a date it gave `unconfirmed`.

## Open named origins

Open an origin only when a card names it and no reader read it. A title search counts as an open.

1. Stop at your allowance of opens.
   - Record a failed fetch as a gap with its error code.
   - Record an origin on a host the dispatch does not list as a gap, cause `host not approved`.
2. Set `read` for an origin you open: `full` (whole page fetched), `abstract` (abstract alone) or `snippet` (search excerpt only).
3. Rate an origin you opened by `../../../vet-sources/references/tiers.md`, from the opened page alone.
   - Give tier C where tier B needs a mention from outside the page.
   - Write the evidence in the origin's evidence cell.
4. Look up an opened origin's DOI by "After the yes" in `catalogues.md`. Check its page for a notice.
   - Exclude a retracted origin or one with an expression of concern from `N`. List it under `## Gaps` as `retracted`.
5. Set its `review status` to `peer-reviewed`, `preprint` or `not a paper`, as the opened page shows.
6. Set its `fetch returned`: `page text` when the tool returned the page's own words, else `summary`.
7. Write one quote of at most 15 words. Start it with `paraphrase:` unless `fetch returned` is `page text`.

## Count and report

1. Count `N`, `M` and `K` as `../origins-and-grades.md` defines them. Never count an untraced source toward `N`.
   - Leave out the literal-quote test for `M` of an origin from the cards. The verifier applies it.
   - Count an origin you opened in `M` only when its quote is literal.
2. Name the collapse reason when sources merge into one origin.
3. Record dissent with the origin behind each opposing position.
4. For a Contested pair, add a `differ` line. Give each side's population, measure and dose, or the topic equivalent.
   - Write "not stated in the cards" for any fact the cards lack.
5. Under `## Gaps`, name the study or data that could settle each `N` = 0 cluster and Contested pair.
6. Under `## Gaps`, also list ideas only one source holds, and origins you could not resolve.
7. List each claim row you leave out of every cluster under `## Set aside`, with a reason.

## Output format

Each cluster has these fields:

- `id`: `<theme>-<n>`, and a one-sentence idea;
- traced origins, each with id, date, tier, review status, kind, `read` and evidence;
- for an origin you opened, also `fetch returned` and its quote;
- an origin's id: the candidate id of its source, or `o-<theme>-<n>` for an origin you opened;
- `kind`: `technique` (a method described), `measured` (own measurement or dataset) or `opinion` (a judgement, no measurement);
- `N`, the traced origins; `M`, the measured ones among them; `K`, the untraced sources;
- the collapse reason, when sources merged into one origin;
- dissent, with the origin behind each position, and its `differ` line;
- the mark `all opinion`, when every claim row of the cluster has the `kind` `opinion`.

The file also holds one `## Caveats` line, a `## Gaps` list and a `## Set aside` list.

## Check

Confirm `N` is at least `M` for every cluster. Confirm every claim row of your theme appears in exactly one cluster or under `## Set aside` or `## Caveats`.
