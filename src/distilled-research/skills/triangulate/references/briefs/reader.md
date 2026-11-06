# Reader brief

You read the primary text of the sources the lead assigns you. You write one section per source in one cards file. You see only your sources, so you judge no agreement across sources.

- Reads: `plan.md` (host choice, themes); each assigned source's vet row in its `vet-<shard>.md`; `pasted-<id>.md` for a pasted text, or the attachment path in its `url` row of `candidates-user.md`.
- Writes: `cards-<shard>.md`.
- Fetch: your sources' primary text, on hosts the dispatch lists, at most 3 fetches each.
- Search: none.
- Done marker: the last line of your file is `## Done`.

## Read

1. Read `plan.md`. Record only claims that answer a sub-question.
2. Read only the sources assigned to you. Open no others.
3. A pasted or attached source has no vet row. Read `pasted-<id>.md` or the attached file, and take its row from `candidates-user.md`. Set `read` to `full` and `fetch returned` to `page text`.
4. Read the primary text: a paper's method and results, a repository's source files, or the page itself.
5. For a paper, prefer an HTML version on a host the dispatch lists. Otherwise use the PDF reader.
6. Take the first fetch's result and act by this table.

| First fetch gives | Action | `read` |
| :-- | :-- | :-- |
| Full text | Go on. | `full` |
| Less than full text (403, bot check, paywall, abstract only), and `plan.md` records "also unflagged hosts" | Fetch the vet row's `oa_url` once. | `full` for full text; `abstract` only if a fetch gave the abstract; else none, with `Not read` and the error code |
| Less than full text, and `plan.md` records "listed hosts only" | Add a `Not read` line for the full text, cause "open-access host not approved". | `abstract`, `snippet` or none, as read |
| A source on a host the dispatch does not list | Fetch nothing. Write `Not read`, cause `host not approved`. | none |
| An error | Write `Not read` with the error code. | none |

7. Stop at 3 fetches per source, counting failures and the open-access try. Write `Not read` for each part left.
8. Record the version read: commit, release, page date or paper version.

## Output format

Each source has a section headed `## <id>`, with the candidate id and never a URL or host. A source not read has a section that holds `Not read`, the error code and the cause.

Before its table, the section lists:

- `url`, `version read` and `instruction_flag`;
- `tier`, copied from the vet row. A pasted or attached source has tier `none`;
- `review status`: `peer-reviewed`, `preprint` or `not a paper`;
- `read`, one of three values:
  - `full`: you fetched the whole page, even if the tool returned a summary of it;
  - `abstract`: the abstract alone;
  - `snippet`: a search-result excerpt only, with `quote` left empty;
- `fetch returned`: `page text` when the tool returned the page's own words, else `summary`;
- `first-public date`, from the opened page, else `unconfirmed`;
- `related`: sources this one cites, copies or answers.

A summary is a rewrite by a separate model call, lossy by design ([tools reference](https://code.claude.com/docs/en/tools-reference), documentation, read 2026-11-05). Mark `summary` when the tool's documentation or result shows a summary or rewrite. Mark `summary` when you cannot tell.

For a paper, `full` means the method and results. For a repository it means the source files the claim rests on.

Each cards table carries its own header row. A claim row has these columns:

| Column | Holds |
| :-- | :-- |
| `id` | Source id, a dot, a number. |
| `theme` | One theme tag from `plan.md`. |
| `claim` | The claim in one sentence. |
| `evidence` | Study name, first author, design, `n`, population, and the effect with its interval, as the source states them. |
| `quote` | At most 15 words. It is literal only when `fetch returned` is `page text`. Otherwise start the cell with `paraphrase:`, whatever quote marks the summary shows. |
| `loc` | File, section or line. |
| `kind` | `technique` (a method the source describes), `measured` (the source reports its own measurement or dataset) or `opinion` (a judgement with no measurement). |
| `cited_origin` | A named origin with its date, or `untraced`. |

Fill `cited_origin` this way:

1. Read the source's references and acknowledgements.
2. Write `untraced` only when neither names an origin for the claim.
3. Otherwise name the origin with its date.

Add a `Not read` line to a section for every file, section or fetch you skipped.

Before `## Done`, write the line `quotes: literal L, paraphrase P`, with the counts over all your claim rows.

## Check

Confirm every claim has a theme tag and every assigned source has a section. Confirm the `quotes:` line matches the rows.
