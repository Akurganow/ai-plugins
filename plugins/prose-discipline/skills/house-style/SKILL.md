---
name: house-style
description: >-
  Apply the prose-discipline engineering prose standard to anything an
  agent writes, from replies and code comments to commit messages and error
  messages. Use when writing or reviewing replies, docs, code comments,
  review comments, commit messages, change descriptions, error messages or
  agent instructions. Also use when asked to check, clean up, shorten or
  de-slop text.
license: MIT
---

# House style

In Hermes, add this skill to `skills.auto_load` so the standard is active in
every session. Hermes lists no plugin skill in its system prompt, so without
that setting the rules below reach a session only when this skill is loaded.

Source: Hermes documentation for `skills.auto_load`,
[`user-guide/cli.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/user-guide/cli.md#L297-L310).
Hermes documentation for plugin skills missing from the system prompt index,
[`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L845).
Hermes source for loading a skill by its qualified name,
[`agent/skill_commands.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L165-L192).

Add these lines to the Hermes `config.yaml`, merging them into an existing
`skills:` block:

<!-- hermes-auto-load:start -->

```yaml
skills:
  auto_load:
    - agent-plugin-prose-discipline-cf518319:house-style
```

<!-- hermes-auto-load:end -->

<!-- rules:start -->

# Prose discipline: core rules

The user installed the prose-discipline plugin, so this standard governs
everything you write in this session. The Exemptions section names the only
exceptions.

These rules cover user replies, prose, code comments, review comments,
commit messages, change descriptions, error messages, and agent
instructions. Replies use the user's language, because the user reads them.
Artifacts stay English: their readers may not share the user's language,
and the word budgets below count English words.

## Structure

- Sentences: 25 words max in English, or equivalent single-thought brevity in other languages. A longer sentence usually hides a second thought the reader must untangle. Split conjunction chains.
- Match reply length to the question: a one-fact question gets a one-sentence answer, and the reply stops after the answer. Give definitions, background, and elaboration only on request, because unrequested text buries the answer.
- One action per sentence or numbered step, so the reader can do or check each one in turn.
- Prefer active voice: the subject performs the action. Passive voice hides who acts.
- Noun chains: 3 consecutive nouns or dependent layers max, because a longer stack hides which word governs. Rephrase longer chains using verbs or prepositions.
- Replace semicolons and excess connective dashes with separate sentences, because each joins two thoughts that read better apart. Keep dashes where grammatically mandatory.

## Vocabulary

- Plain verbs: use direct action verbs. Avoid weak-verb combinations like "perform validation" or "make use of", because they add words and no meaning.
- Connectives: use simple conjunctions. Avoid heavy compound bureaucratic phrases, because they slow the reader and add nothing.
- Delete filler: "it is important to note", "rest assured", "please be advised", and non-English equivalents. Filler carries no fact.
- State facts directly. No "not just X — it's Y" frames and no teaser setups: the setup delays the fact and carries none of its own.
- Keep domain terms: accessible, accept, validate, rotate, robust (term of art). Established technical terms never count as violations, because replacing them changes the meaning.

## Code comments

- No narration of the obvious ("This function handles...") and no step markers ("// Step 1:"). The code already says it, and narration goes stale when the code changes.
- Default to no comments, because each comment is one more text to keep true when the code changes. Add one only when the why is non-obvious: a hidden constraint, a subtle invariant, a bug workaround, or surprising behavior. A short orienting comment before a complex block is fine.
- No committed uncertainty ("should work"). Fix the code or delete the comment, because a reader cannot tell a real doubt from a forgotten one.
- No ASCII section dividers. A region that needs a banner belongs in its own file, class, or module.
- Comments explain why. Names and code explain what.

## Artifact formats

- Review comments start with a label: `issue:`, `issue (blocking):`, `suggestion (non-blocking):`, `question:`, `nitpick:`. The label tells the author whether the comment blocks the merge.
- Change descriptions: what changed, why, verification performed. No journey narrative and no session-process narrative, because the reader acts on the result. Verification states commands and results, never the process that produced them.
- Error message: what failed, the cause, the fix. The reader needs all three to act.
- Numbered steps: one imperative instruction per step, 20 words max, so each step is one thing to do.
- When the host or repository defines a template, the template outranks these formats, because its readers expect that shape. The standard governs the wording inside it.

## Exemptions

- Code blocks, identifiers, commands, and URLs are never flagged, because rewording them breaks them. Quoted text, changelogs, migration examples, and licenses are exempt, because their words belong to someone else.
- The changelog and migration exemptions cover quoted historical text, not text you author now.
- In review diffs, only added lines count: the author answers for the change, not for the whole file.

## Where the depth lives

The house-style skill of this plugin holds the depth behind every rule. Read
the matching reference before writing or reviewing an artifact. Paths are
relative to the plugin root.

| Artifact | Reference |
| :-- | :-- |
| Prose, docs, runbooks | `skills/house-style/references/structural-rules.md` |
| Wording, filler, slop patterns | `skills/house-style/references/vocabulary.md`, `skills/house-style/references/slop-pruning.md` |
| Code comments | `skills/house-style/references/comment-hygiene.md` |
| Commits, change descriptions, errors, review comments, agent instructions | `skills/house-style/references/artifact-formats.md` |
| Calibration examples | `skills/house-style/references/examples.md` |

<!-- rules:end -->

## Replying to the user

- Reply in the user's language, directly and factually.
- Lead with the answer, then the evidence.
- Keep the language-neutral rules in every reply: one action per sentence,
  plain verbs, no hedging, no filler, no rhetorical negations.

## Writing artifacts

Read the matching reference before producing an artifact. Paths are
relative to this file:

- `references/structural-rules.md`: read when writing prose, docs or
  runbooks, or when a sentence, a procedure or a noun stack needs splitting.
- `references/vocabulary.md`: read when choosing words, for the
  substitution table, significance inflation and the domain-term contract.
- `references/slop-pruning.md`: read when text has rhetorical negations,
  teaser hooks, filler openers, false engagement or session-process
  narrative.
- `references/comment-hygiene.md`: read when writing or reviewing code
  comments.
- `references/artifact-formats.md`: read when writing a review comment,
  commit message, change description, error message or agent instruction.
- `references/examples.md`: read when calibrating an audit, to name each
  finding after its closest before/after pair.

Produce the artifact in the governing format directly. No preamble and
no closing commentary unless asked.

## Checking and cleaning text, when asked

1. Identify the artifact types and read the matching references above.
2. Report findings first, ordered by severity. Do not rewrite yet.
3. Apply the Exemptions section of the core rules.
4. Each finding states the location, the violated rule, and the smallest
   fix.
5. Interactive sessions: apply the minimal fixes after the user approves.
   Autonomous and headless runs: apply only mechanical fixes, meaning the
   substitution table and Conventional Comments labels. Report judgment
   calls as findings.

Severity: `major` covers hedging comments, unlabeled review feedback,
merge-decision risks, change descriptions with no verification result,
and session-process narrative replacing a real result. `minor` covers
narrator, step, and divider comments, vocabulary, structure, and
format deviations. `nit` covers punctuation and single-word issues.
