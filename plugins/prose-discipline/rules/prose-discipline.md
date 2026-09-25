---
alwaysApply: true
description: Engineering prose standard for all agent-written text
---

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

- Plain verbs: use direct action verbs. Weak-verb combinations like "perform validation" or "make use of" add words and no meaning.
- Connectives: use simple conjunctions. Heavy compound bureaucratic phrases slow the reader and add nothing.
- Delete filler: "it is important to note", "rest assured", "please be advised", and non-English equivalents. Filler carries no fact.
- State facts directly. No "not just X — it's Y" frames and no teaser setups: the setup delays the fact and carries none of its own.
- Keep domain terms: accessible, accept, validate, rotate, robust (term of art). Established technical terms never count as violations, because replacing them changes the meaning.

## Code comments

- No narration of the obvious ("This function handles...") and no step markers ("// Step 1:"). The code already says it, and narration goes stale when the code changes.
- Default to no comments. Add one only when the why is non-obvious: a hidden constraint, a subtle invariant, a bug workaround, or surprising behavior. A short orienting comment before a complex block is fine.
- No committed uncertainty ("should work"). Fix the code or delete the comment, because a reader cannot tell a real doubt from a forgotten one.
- No ASCII section dividers. A region that needs a banner needs its own file, class, or module.
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
