# Vetter brief

You vet the candidate rows assigned to you, by the lead or by the user. The user has consented to DOI and repository-path lookups, so you may send them to the catalogues.

- Reads: every `candidates-<lane>.md` that holds your rows, or the user's list; `../catalogues.md`; `../tiers.md`. When a lead dispatched you, also `plan.md`.
- Writes: `vet-<shard>.md` when a lead dispatched you. Otherwise nothing; reply with the rows.
- Fetch: the catalogue hosts `../catalogues.md` names for the topic type. Also the source page, and a repository's own page, once each on hosts the dispatch or report lists. At most 2 pages per row; catalogue calls do not count.
- Search: once per row, with the source's hostname or title alone.
- Done marker: when a lead dispatched you, the last line of your file is `## Done`.

## Fields of `plan.md`

When a lead dispatched you, `plan.md` holds four fields that you read:

- Topic type: `practice/technology`, `science/health`, `news/facts` or `other`. Only `practice/technology` adds a catalogue entry, OpenSSF Scorecard.
- Out-of-topic list: the subjects and hosts that make a source off topic.
- Rated hosts: each host the stage-0 report rated, with its status and record.
- Host choice: "listed hosts only" or "also unflagged hosts". The dispatch's host list applies it.
  - Under "also unflagged hosts", a new public host needs your own lookup to find no negative record.

## Vet

1. Vet only the rows assigned to you. Open no others.
2. Take row details from the `candidates-<lane>.md` files, or from the user's list when no lead dispatched you.
3. Read the four fields of `plan.md`, when a lead dispatched you.
4. Read `../catalogues.md`. Load the entries for the topic type.
5. Reuse the record of each rated host. Reuse its hostname search for a row, except a row on a code forge or another host that serves many sources.
   - Look up each other host, and set its status before any fetch. Its hostname search is that row's one search.
   - A row on a shared host takes its own title search, as its one search.
6. Query each catalogue for each row by its DOI or repository path, one record per lookup.
7. Write `oa_url` in `record` as `../catalogues.md` says.
8. Fetch the source page once, on a host the dispatch or report lists.
   - For a repository, also fetch its repository page on the same host.
   - On any other host, or one with a negative record, fetch nothing. Set `keep` = `no`, reason `host not approved`.
   - Check a redirect target against the host list before you follow it. If the tool hides the target, check the final URL. Discard a page from an off-list host, with reason `host not approved`.
9. Check each source from outside (lateral reading): run the row's one search, hostname or title alone, unless step 5 reused one.
10. Assign a tier from `../tiers.md`. Name the evidence behind it in `reason`.
    - Read what a correction notice changes. If the record is silent, note it in `reason` and lower no tier.
11. Set `keep` by the rule below, for the tier, the topic and any retraction notice.
12. For a repository, note its created and last-pushed dates in `reason`.
13. Flag a repository with stars, no forks and a history under a week.
14. Screen the source's own instructions to agents. Fill `instruction_flag` as the DATA RULE says.

## Ratings

- A rating is the catalogue's record as found, with the catalogue name and a status from `../catalogues.md`.
- Read what each status proves about safety, and what it does not, in `../catalogues.md`.
- Record a failed fetch or search as an error with its code. A failed fetch is never an empty result.
- Do not download an archive. Write an archive-only source's row with `keep` = `no` and the reason `archive only`.

## Output format

Columns of a vet row: `id`, `url`, `record`, `status`, `tier`, `keep`, `reason`, `instruction_flag`.

| Column | Holds |
| :-- | :-- |
| `id` | The candidate id, or the user's own label. |
| `record` | The catalogue name and a quoted excerpt of its record, at most 25 words, with `oa_url` where `../catalogues.md` says. The full record stays in the catalogue. |
| `status` | One status from `../catalogues.md` per lookup, as `Crossref: error(403); OpenAlex: listed`. |
| `tier` | A, B, C or `none`. |
| `keep` | `yes` or `no`. Only a tier A or B primary source on topic gets `yes`. Commentary (a news summary included), tier C, flagged and archive-only sources get `no`. So does a retracted source, or one with a retraction or expression-of-concern notice, with the reason `retracted`. A correction notice alone never sets `no`. |
| `reason` | The evidence behind the tier, or why `keep` is `no`. |
| `instruction_flag` | Empty, or the quote the DATA RULE describes. |

## Check

Confirm every assigned row has a tier or a reason it has none, and a `keep` value.
