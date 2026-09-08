# Artifact Formats: Depth

Extends the Artifact formats section of the core rule with full templates.

## Review comments (Conventional Comments)

Every review comment starts with a label. An unlabeled comment is a `major`
finding: the author cannot tell whether it blocks the merge.

| Label | Meaning |
| --- | --- |
| `praise:` | Highlight something positive (rarely needed) |
| `nitpick:` | Trivial preference, non-blocking by nature |
| `suggestion:` | Improve the approach, non-blocking unless decorated |
| `issue:` | A concrete problem, blocking by default |
| `todo:` | Small, trivial, but necessary changes (docs, typos, config) |
| `question:` | Request for information or clarification |
| `thought:` | Idea worth considering, no action required |
| `chore:` | Simple task for the author (docs, tests, cleanup) |

Decorations change blocking defaults: `(blocking)`, `(non-blocking)`,
`(security)`, `(if-minor)`.

Anatomy: `label: finding`, then the impact, then the concrete fix. Provide
the fix as a diff or a precise instruction, not as a wish.

Before: "I was just wondering if maybe we could somehow avoid the query
inside the loop since it might be slow?"
After: "`issue (blocking):` This query runs inside the loop and produces an
N+1 pattern on a 10k-row page. Fetch all IDs upfront and query once with
`WHERE id IN (...)`."

## Commit message

- Subject: imperative mood, 50 chars max, states what and hints why.
- "Replace custom OAuth handler with provider adapter", not "changes" and
  not "Update code".
- Body only when the why is non-obvious from the diff. Wrap at 72 chars.

## Change description

Any human-readable description of work, at minimum three blocks:

- **What changed**: the contract-level delta, one bullet per change.
- **Why**: the defect, requirement, or decision driving it.
- **Verification**: tests run, commands executed, evidence produced.
  One to three lines by default, scaled to the change, not to the
  session's process.

No effort narration ("we spent significant effort"), no apologies, no
thanks paragraphs, no session-process narrative (patterns:
`slop-pruning.md`). Verification states commands and results, never
the process that produced them. Where another format in this file is
stricter, such as the commit message, that format governs.

## Error message

Three parts, no apology, no filler:

1. What failed, with the subject named.
2. The root cause or error code.
3. The actionable resolution.

Before: "Oops! Something went wrong while attempting to establish a
connection. Please verify your settings or contact support if the issue
persists."
After: "Connection to Postgres failed: authentication rejected for user
`app`. Verify `DB_PASSWORD` in `.env` and retry."

## Agent and subagent instructions

- One intent per step, 20 words max, inputs named explicitly.
- No motivation or context paragraphs inside instruction steps. Context goes
  above the steps.

## Audit severity

- Review feedback without a label, a change description that states no
  verification result anywhere: `major`. A short verification that
  states commands and results is never a finding. Template precedence
  applies: the verification result goes wherever the governing
  template has room for it.
- Format deviations in any artifact format above: `minor`.
