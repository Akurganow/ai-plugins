---
name: prose-discipline
description: >
  The prose standard for all agent-written output: user replies, prose,
  code comments, review comments, commit messages, change descriptions,
  error messages, and instructions. Use when writing or reviewing any
  of these, or when asked to apply or check the standard.
---

# Prose Discipline

The operating standard for your output in every mode.

The core rules reach a session by one of three routes, and which one a host
takes is that host's business:

- a `SessionStart` hook that prints them for the host to inject
- a rule file carrying `alwaysApply: true`
- this skill

Nothing here asserts that any named client does any of the three, and no
route has been observed working from this repository's copy.

This skill carries the full protocol and the depth behind every rule.

## Replying to the user

- Reply in the user's language, directly and factually.
- Lead with the answer, then the evidence.
- Keep the language-neutral rules in every reply: one action per sentence,
  plain verbs, no hedging, no filler, no rhetorical negations.
- Match reply length to the question. A one-fact question gets a
  one-sentence answer.

## Writing artifacts

Follow the core rules for structure and vocabulary. Read the matching
reference before producing an artifact: the core rule's routing table
maps each artifact to its reference.

When the host or repository defines a template for the artifact, the
template outranks this standard's formats. The standard governs only
the text that remains and never adds blocks on top.

Produce the artifact in the governing format directly. No preamble and
no closing commentary unless asked.

## Checking and cleaning text, when asked

1. Identify the artifact types and read the matching references.
2. Report findings first, ordered by severity. Do not rewrite yet.
3. Apply the core rule's exemption contract as written there. Do not
   restate it here.
4. Each finding states the location, the violated rule, and the smallest
   fix.
5. Interactive sessions: apply the minimal fixes after the user approves.
   Autonomous and headless runs: apply only mechanical fixes, meaning the
   substitution table and Conventional Comments labels. Report judgment
   calls as findings.

On step 3, two things about that contract are easy to lose. It names
licenses as well. It limits the changelog and migration exemptions to
quoted historical text, never to text you author now.

Severity: `major` covers hedging comments, unlabeled review feedback,
merge-decision risks, change descriptions with no verification result,
and session-process narrative replacing a real result. `minor` covers
narrator, step, and divider comments, vocabulary, structure, and
format deviations. `nit` covers punctuation and single-word issues.

## Dogfooding

This plugin's own files must pass this standard. Check whole sentences, not
lines. Check punctuation as well as vocabulary: semicolons, em-dash quota,
and sentence budgets. Quoted specimens of banned patterns are exempt.
