# Structural Rules: Depth

Extends the Structure section of the core rule. The core states each rule
once. This file adds measurement and edge cases.

## Sentence budget

- English text: 25 words is the ceiling, not the target.
- Non-English text: keep equivalent single-thought brevity. Do not build multi-clause compound sentences.
- Split at the natural seam: a conjunction, a relative clause, or a second verb that starts a new action.
- Lists outrank sentences. 3 or more parallel items in one sentence become a bullet list.
- Do not count code, identifiers, quoted text, or URLs toward the budget.
## Action density

- A sentence states one action. Chains joined by "and then", "after which",
  or "while also" become numbered steps.
- Numbered steps: one imperative instruction per step, 20 words max. The
  step is a command, not a paragraph.
- Descriptive prose (explanations, ADRs) keeps full sentences and articles.
  Procedures do not need articles. Do not compress explanations into
  telegram style.

## Voice

- Passive constructions to rewrite: "is handled by", "was implemented to",
  "are considered". Name the actor: "The handler maintains state."
- Passive is acceptable when the actor is genuinely irrelevant or when an
  error message must not assign blame. Example: "The request was rejected"
  in an error message stays passive.
- Detection cue: a be-verb followed by a past participle plus "by".

## Noun chains

- Four or more consecutive nouns or dependent layers are a finding.
- In English, this targets noun stacks without prepositions ("service cluster event bus message priority handler").
- In other languages, this targets nested genitive or prepositional chains.
- Established technical terms and component names are exempt.
- Fix by rephrasing with verbs or prepositions: "the handler that sets event priority on the service bus".
- Hyphenated compounds count as one noun.
## Punctuation

- Semicolons: split the sentence instead. A semicolon signals two complete thoughts that deserve two sentences.
- Connective dashes: do not use dashes as glue to connect independent thoughts. Use separate sentences instead.
- Grammatically mandatory dashes (such as subject-predicate dashes with zero copula) are permitted.
- In English text, limit stylistic em-dashes to at most 1 per 1,000 words.
- Parenthetical asides carrying real content become their own sentence. Empty ones are deleted.

## Audit severity

- Over-budget sentences and verb chains: `minor`.
- Noun stacks that obscure the actor or object: `minor`.
- Procedures compressed into a single sentence that a reader must parse to
  execute: `major` when it can cause a wrong action.
