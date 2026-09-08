# Comment Hygiene: Depth

Extends the Code comments section of the core rule. Default to no
comments: add one only when the why is non-obvious. The governing test
for every surviving comment: it must add a reason, a constraint, or
business context that the code cannot show. Everything else is deleted.

## Narrator comments

Cues: "This function handles", "This class manages", "This module is
responsible for", "Here we", "The following code".

- The name and signature already say what the code does. Narration is
  duplication that rots when the code changes.
- Fix: delete. Or rewrite into the *why*: the constraint, the workaround, or
  the business reason. "// Retry 3 times because the upstream queue
  de-duplicates within 60s" survives the test. "// Retry the request" does
  not.

## Step and trivial markers

Cues: `// Step 1:`, `// Create the client`, `// Increment the counter`,
`// Return the result`, `// Loop over items`.

- Fix: delete entirely. Order and names speak.
- Before: `// Increment the counter`. After: delete. `counter += 1`
  says it.
- Exception: a numbered comment inside a genuinely non-obvious algorithm
  step is acceptable only when it explains the step's purpose, not its
  mechanics.

## Hedging comments: severity major

Cues: "should work", "might not be", "probably", "hopefully", "I think this
is correct", "TODO: replace with real implementation".

- Committed uncertainty is a correctness smell, not a style issue.
- Fix: resolve the uncertainty (verify, test, fix the code) or delete the
  comment. Never ship doubt.
- Before: `// should work for most cases`. After: delete the comment
  and add the missing case to the test.

## ASCII section dividers

Cues: `// =====`, `// --- Helper Functions ---`, `# *** SECTION ***`.

- Fix: delete. If the region genuinely needs separation, it needs a file, a
  class, or an export, not a text banner.
- Before: `// ===== Helper Functions =====`. After: delete the banner.
  Extract a module when the boundary genuinely matters.

## Severity scale

- Hedging: `major`.
- Narrator, step, divider comments: `minor`.
- A comment that is accurate but states the obvious: `nit`, delete.
