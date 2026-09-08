---
alwaysApply: true
description: Engineering prose standard for all agent-written text
---

# Prose discipline: core rules

This standard is mandatory in every session, without exceptions.

These rules govern everything you write: user replies, prose, code
comments, review comments, commit messages, change descriptions, error
messages, and agent instructions. Artifacts stay English. Replies use
the user's language.

## Structure

- Sentences: 25 words max in English, or equivalent single-thought brevity. Split conjunction chains.
- Match reply length to the question: a one-fact question gets a one-sentence answer, and the reply stops after the answer. Definitions, background, and elaboration only on request.
- One action per sentence or numbered step.
- Prefer active voice: the subject performs the action.
- Noun chains: 3 consecutive nouns or dependent layers max. Rephrase longer chains using verbs or prepositions.
- Replace semicolons and excess connective dashes with separate sentences. Keep dashes where grammatically mandatory.

## Vocabulary

- Plain verbs: use direct action verbs. Avoid weak-verb combinations like "perform validation" or "make use of".
- Connectives: use simple conjunctions. Avoid heavy compound bureaucratic phrases.
- Delete filler: "it is important to note", "rest assured", "please be advised", and non-English equivalents.
- State facts directly. No "not just X — it's Y" frames and no teaser setups.
- Keep domain terms: accessible, accept, validate, rotate, robust (term of art). Established technical terms never count as violations.

## Code comments

- No narration of the obvious ("This function handles...") and no step markers ("// Step 1:").
- Default to no comments. Add one only when the why is non-obvious: a hidden constraint, a subtle invariant, a bug workaround, or surprising behavior. A short orienting comment before a complex block is fine.
- No committed uncertainty ("should work"). Fix the code or delete the comment.
- No ASCII section dividers.
- Comments explain why. Names and code explain what.

## Artifact formats

- Review comments start with a label: `issue:`, `issue (blocking):`, `suggestion (non-blocking):`, `question:`, `nitpick:`.
- Change descriptions: what changed, why, verification performed. No journey narrative, no session-process narrative. Verification states commands and results, never the process that produced them.
- Error message: what failed, the cause, the fix.
- Numbered steps: one imperative instruction per step, 20 words max.
- When the host or repository defines a template, the template outranks these formats. The standard governs the wording inside it.

## Exemptions

- Code blocks, identifiers, commands, and URLs are never flagged. Quoted text, changelogs, migration examples, and licenses are exempt.
- The changelog and migration exemptions cover quoted historical text, not text you author now.
- In review diffs, only added lines count.

The depth behind every rule lives in the prose-discipline skill. Read
the matching reference before writing or reviewing an artifact:

- Prose, docs, runbooks: `structural-rules.md`
- Wording, filler, slop patterns: `vocabulary.md`, `slop-pruning.md`
- Code comments: `comment-hygiene.md`
- Commits, change descriptions, errors, review comments, agent instructions: `artifact-formats.md`
- Calibration examples: `examples.md`
