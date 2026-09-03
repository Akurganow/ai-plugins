# Slop: what generator residue looks like

What a text generator leaves behind and a person would not have written on
purpose. This repository is prose almost entirely — a README, a skill with
its references, one check, one workflow — and its whole value is that its
sentences hold (`.agents/rules/claims.md`). A sentence that holds nothing is
the cheapest thing to add here and the hardest to see in review, because it
reads exactly like the kind that holds. Read by any reviewer, a person or an
unattended run. What the conformance check decides is owned by
`.agents/rules/conformance.md`; this file is about the words the check
cannot read.

## The one test

> Does this text carry a fact a reader cannot get from the text or the code
> beside it, in the same file?

A comment or a name in the check, a step name in the workflow, a paragraph
of the README or the skill, a `description` in a manifest: no fact left over
is noise; a false fact is a lie. Judge the sentence, not the block: a
paragraph that states a reason and adds one empty sentence is a reason, not
a finding, and so is a reason with a hedge or a reassurance word inside it.
One excerpt can hold several findings; each has one kind, and when two kinds
fit, the later in the list below wins — its measurement is the stronger
evidence.

## The kinds

1. **`noise`** — text with no fact: a paragraph restating the one above it,
   a comment narrating the line below it, a `description` that repeats the
   name, hedges and reassurance words ("robust", "seamlessly", "simply")
   standing in for a fact, a sentence that exists to make a section look
   complete. Measurement: the content words against the text and code
   beside them, nothing left over. Not noise: a sentence that says what was
   not verified. `claims.md` makes that sentence load-bearing — the one
   `README.md` opens its install section with carries a fact a reader acts
   on, and reads like a hedge only to an eye that has not read `claims.md`.
2. **`lying`** — text that contradicts this repository: a README sentence
   the check does not do, a step name the step does not perform, a
   `description` the skill does not keep, a count the tree does not have, a
   comment for a check that was deleted. Measurement: the two quotes side by
   side, with the commit that wrote the text and the commit that changed
   what it describes. Distinct from a false claim about a client or a
   released artifact — that is a claims defect, judged under `claims.md` on
   its own terms, and the graver of the two.
3. **`naming`** — in the check: generic names, filler suffixes, a helper
   named for its shape rather than its job; across the prose: one thing
   under three names between the README, the skill and the manifest.
   Measurement: the census, every name for the thing with its file. Not a
   finding: a name the specification fixes (`plugin.json`, `SKILL.md`, the
   front-matter keys) or one a client's own documentation uses — those are
   quoted, not chosen.
4. **`ceremony`** — a check that cannot fail on this tree and says nothing
   beside itself about why it exists. `conformance.md` already sets the
   rule: a hand-written check either enforces what a schema cannot express
   or turns a schema rejection into a message somebody can act on, and says
   which; "a duplicate with neither reason is the one to delete". A workflow
   step that proves nothing is the same shape. Measurement: the change to a
   package the check ought to reject and does not, or the reason it can
   never fire, written out in full.
5. **`residue`** — what the process left behind: changelog in comments or
   prose ("now", "updated", "since the rewrite" with nothing the reader can
   use after it), attribution of a tool, a paragraph describing the change
   that introduced it instead of the thing, a section kept for a plugin or
   a surface that is gone, a reference file nothing links. Measurement:
   `git log -S` for the commit that brought it and the commit that made it
   moot — or, for what was moot on arrival, the introducing commit alone
   and the statement that nothing ever used it.

## What is protected

Never a finding:

- **Recorded reasons.** The check's docstring argues its own existence,
  `conformance.md` argues the two checks that duplicate the schema, the
  workflow's comments say why a commit sha and not a tag. Other reviews
  read these as evidence.
- **The owner's decision, quoted.** `conformance.md` quotes the version
  rule in the owner's own words and language. A quotation is evidence, and
  its language is part of the evidence.
- **What a release writes.** `version` in `plugins/howp/plugin.json`,
  `plugins/howp/binaries.json` and
  `plugins/howp/skills/howp/references/commands.md` are machine-written,
  and `conformance.md` says by whom. A wrong sentence in one is a defect of
  the release job, in the repository that runs it — never judged here.
- **The claims discipline's sentences.** The statement of what was not
  verified, the per-fact source and its kind, a date and a tag beside a
  measurement. To an outside eye these read as hedging; each is a fact.
- **House style.** Long paragraphs that argue a point through, em-dashes,
  bold on the load-bearing clause, a section number beside every claim
  about the specification.
- **The vendored schema.** `tools/schemas/` is a verbatim copy; its text
  belongs to its publisher.
- **The instructions.** `.agents/**`. Read, never judged.

## The fence

`tools/check-conformance.py` is the only program here and the only fence:
where files sit, what a symlink resolves to, what a manifest and a skill's
front matter say, decided against the published schema and against the
clause quoted beside each hand check. Nothing keys on vocabulary, and
nothing should — words have legitimate readings, and the sentence
`claims.md` protects would be the first casualty of a hedge filter.
Anything the check names cannot exist on a green `main`; a report of it is
a misread. Slop is judged strictly above it: text that passes the check and
still says nothing. A tell that recurs and could be named by a pattern is a
proposal, recorded in a review's report — not a check added on the spot.

## Neighbours

A false or unsourced claim about a client, an install command or a
released artifact is a claims defect under `claims.md`, the graver kind: it
is what a reader acts on, and it is judged first. Missing community files,
discoverability, a specification clause the check does not reach — those
are repository-audit matters with a checklist of their own. A conformance
failure is the check's. Slop names the text that says nothing, or that
contradicts the tree beside it; where one sentence is both a lie about the
tree and a false claim to a reader, it is a claims defect, never both.
