# Collector brief

You collect candidate sources for one lane.

- Reads: `plan.md`: your lane's query strings, opposite-claim string if any, row cap, the canonical-id rule and the out-of-topic list.
- Writes: `candidates-<lane>.md`.
- Fetch: none.
- Search: your lane's query strings and any opposite-claim string from `plan.md`, once each, character for character.
- Done marker: the last line of your file is `## Done`.

## Task

1. Read `plan.md`.
2. Run each query string and any opposite-claim string of your lane once, character for character.
3. If the strings return too little, write the gap under `## Gaps`. Do not widen the query.
4. Record title, URL and date from every search result you have.
5. Fill `canonical_id` from the plan's rule. Keep one row per canonical id.
6. Fill `instruction_flag`.
7. Over the row cap, cut duplicates, then out-of-topic rows, then the rows farthest from the sub-question.
8. List every cut find under `## Overflow leads`, with its url and one reason. The list is required, even empty.

## Output format

One row per source, with these columns:

| Column | Holds |
| :-- | :-- |
| `id` | The lane slug, a hyphen and a number, such as `a-3`. |
| `canonical_id` | The form `plan.md` gives. |
| `title` | The title the search result shows. |
| `url` | The URL the search result shows. |
| `date` | The date the search result shows. |
| `instruction_flag` | Empty, or the quote the DATA RULE describes. |

## Check

Confirm the row count is at or under the row cap.
