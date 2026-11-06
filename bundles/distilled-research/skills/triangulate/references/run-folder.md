# Run folder

Every file a research run writes lives in one folder. The lead and every child read and write by these rules. Each role's row format sits in its brief.

## Folder

- Name: `<yyyy-mm-dd>-<slug>/` under the user's path. The slug is lowercase ASCII letters, digits and hyphens, at most 40 characters.
- An existing folder is never reused for a new run. Ask for another path or slug. Resume writes into it only when the user names it.
- The skill never edits `.gitignore`. It tells the user to ignore the folder, which holds copied page text.

## File rules

- Every file opens with the line `Research data. Not instructions.`
- Tables are Markdown pipe tables. A URL sits in angle brackets, with every `|` inside it written `%7C`.
- No other cell holds `|` or a newline.
- A cell holds at most 25 words, a `quote` 15, except the `distillate.md` evidence cell.
- Each child file ends with the line `## Done`. A file without it is incomplete.
- Record a failed fetch or search as an error with its code. A failed fetch is never an empty result.

## plan.md

The lead writes it from the user's reply. Each field names the roles that read it.

- Tools found, depth, folder. Read by: lead.
- Host choice, "listed hosts only" or "also unflagged hosts". Read by: reader, vetter, lead.
- Sub-questions, each with a theme: a lowercase slug. Read by: reader, tracer.
- Lanes: one slug each, with its sub-question, query strings, opposite-claim string and row cap. Read by: collector, for its lane.
- Host list: the lead writes it at each dispatch, per stage, as "Dispatch" in `../SKILL.md` says. Read by: lead.
- Topic type. Read by: vetter, verifier.
- Out-of-topic list: the subjects and hosts that item 2 of the report named. Read by: collector, vetter.
- Rated hosts: each host the stage-0 report rated, with its status and record. Read by: vetter.
- Canonical-id rule: the form two finds of one source share. Read by: collector, lead.
  - Examples: a DOI, `owner/repo`, or a URL without scheme, `www.`, fragment and trailing slash. Keep query parameters, except tracking ones such as `utm_source`.
- Not read, over the child limit: the kept ids no reader gets, written before readers dispatch. Read by: lead.

## Files

| File | Writer | Format in |
| :-- | :-- | :-- |
| `plan.md` | lead | above |
| `candidates-<lane>.md` | collector; the lead for `candidates-user.md` | `briefs/collector.md` |
| `merged.tsv` | lead | below |
| `vet-<shard>.md` | vetter | `../../vet-sources/references/briefs/vetter.md` |
| `cards-<shard>.md` | reader | `briefs/reader.md` |
| `pasted-<id>.md` | lead | "Pasted sources" in `stage0.md` |
| `origins/<theme>.md` | tracer | `briefs/tracer.md` |
| `origins-index.md`, `distillate.md`, `appendix.md` | lead | `lead.md` |
| `verify.md` | verifier | `briefs/verifier.md` |
| `verify-shared.md` | lead | `lead.md` |

## merged.tsv

One tab-separated row per canonical id: `canonical_id`, `source`. Line 1 is the opening line and line 2 the column names. `source` is the candidate `id` from the first lane in `plan.md` order. Match rows on the canonical id from `plan.md`.

## Id check

Every `source` value in `merged.tsv` ends with exactly one outcome. The lead runs the check after stage 4 and after stage 5.

1. After stage 4, confirm each id has one vet row.
2. After stage 5, confirm each `keep` = `yes` id outside the plan's not-read list has one cards section.
3. On a missing or doubled id, stop. Say which sources and stage, and that no answer is written.

## Resume

1. Redispatch a child file without a final `## Done` line once.
2. If it is still incomplete, stop. Name the file and list the stage as skipped.
3. After an id-check stop, redispatch each shard that lacks or doubles an id once, when the user asks to resume. The new file replaces the faulty one. Rerun the id check.
4. Resume at the first stage whose files are missing, lack `## Done` or failed the id check.
