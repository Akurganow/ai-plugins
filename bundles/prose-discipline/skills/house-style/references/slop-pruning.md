# Slop Pruning: Depth

Extends the Vocabulary and Structure sections of the core rule with the
syntactic tells that mark generated text. Each pattern is deleted and
replaced by the direct statement.

## Rhetorical negation

Pattern: "This isn't just about X — it's about Y", "It's not X, it's Y".

The setup sentence carries no information. Only the positive claim matters.
State it directly: "This improves review latency." Fix: delete the frame,
keep the fact.

## Teaser hooks

Patterns: "The catch?", "Here's the thing", "The kicker:", "Plot twist:",
"Let that sink in", "Buckle up".

Fix: delete the hook and state the constraint as a fact. "The migration is
irreversible after step 3."

## Filler openers

Patterns: "It is important to note that", "It's worth noting that", "It
should be noted that".

Fix: delete the opener. The following sentence is the content.

## False engagement

Patterns: "Let's dive in", "Let's take a deep dive", "Grab a coffee",
"you're in for a treat".

Fix: delete. Engineering text has no cold open.

## Significance inflation and hollow reassurance

Handled in `vocabulary.md`: delete or quantify.

## Session-process narrative

The writing session's roles and rituals, not human review records:
"an independent verification agent reviewed the change", "verdict:
PASS", "the adversarial review found no issues".

Fix: delete the machinery, keep the result. "Verification: `npm test`
green." Session-process narrative belongs to the session log, never
to a durable artifact, meaning text that outlives the session.

## Audit severity

- Teasers, filler openers, false engagement: `minor`.
- A rhetorical negation that replaces a missing concrete claim ("it's not
  about speed, it's about velocity"): `major`. The text asserts importance
  while stating nothing actionable.
- Session-process narrative in a durable artifact: `minor`.
- The same narrative replacing a missing concrete verification
  result: `major`. It claims verification without stating it.
