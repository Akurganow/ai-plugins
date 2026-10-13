# Spec: each pipeline counter's number is stated once, in the law

## Work item

Pull request #74, built from #33. Each bound's number, and the `slices` day's
cap, goes into the law's `### How every bound behaves`. Every role names the
counter instead of restating the number.

## Problem

All line numbers below are read at `origin/main` `281b817`. This branch's head,
`704957d`, is 48 commits behind `main`, and `## Steps` merges `main` in first.
Every quote was re-read there.

The law's bound section names the four bounds and the `slices` pace, but it
states no number for any of them.
`.agents/skills/pipeline-law/SKILL.md:745-751`:

> There are four: `review_rounds`, `gate_bounces`, `judge_rejects` and
> `cr_rounds`. All four obey the same three rules.
>
> `slices` is the fifth counter and is **not** a bound. It is a day's pace: at
> three the Implementer stops without re-entering itself, […]

Only `slices` gets a number there ("at three"). Each role states the others,
and two numbers are stated in more than one role document. This is the census
of every place a document states a counter's number, at `281b817`. It comes
from the criterion 1 pattern of `## Acceptance criteria`, run over
`.agents/skills/`, plus a read of the law's section. The law's "at three"
spans a line break, so the pattern cannot see it:

| Counter | Value | Stated at | Documents |
| :-- | :-- | :-- | :-- |
| `review_rounds` | 5 | `spec-reviewer/SKILL.md:136`, `:314`; `spec-writer/SKILL.md:365` | 2 |
| `slices` | 3 | `pipeline-law/SKILL.md:748-749`; `implementer/SKILL.md:59`, `:327`, `:328`, `:618`; `pipeline-clerk/SKILL.md:106` | 3 |
| `gate_bounces` | 2 | `implementer/SKILL.md:138`, `:181` ("A first"), `:185`, `:192` ("A second"), `:195`, `:210` | 1 |
| `judge_rejects` | 2 | `implementer/SKILL.md:468-469`, `:474` | 1 |
| `cr_rounds` | 3 | `pipeline-clerk/SKILL.md:375`, `:396` | 1 |

The quotes for the two counters stated in more than one place:

- `.agents/skills/spec-reviewer/SKILL.md:314`: "**The bound.** At `review_rounds` of 5 or above, compare the current spec"
- `.agents/skills/spec-writer/SKILL.md:365`: "**The bound.** Read `review_rounds` from the state block. At 5 or above,"
- `.agents/skills/implementer/SKILL.md:59`: "`slices` as 0. When it is today and `slices` is 3 or above, stop here:"
- `.agents/skills/pipeline-clerk/SKILL.md:106`: "| `spec/approved`, a claim released, and a `pipeline-progress` line with `slices` at 3 or above and `slices_day` before today | re-enter `spec/approved` |"

None of them attributes its number to another document. Raising
`review_rounds` therefore takes a hand edit in two files, and raising `slices`
takes one in three.

**Stale evidence in the source.** #33 has two parts. Part 1 says the bound
section leaves out `cr_rounds`, quoting `pipeline-law/SKILL.md:449` as
"There are four: `review_rounds`, `gate_bounces`, `judge_rejects`, `slices`."
That no longer holds. At `281b817`, `:745-746` reads "There are four:
`review_rounds`, `gate_bounces`, `judge_rejects` and `cr_rounds`." The court's
comment on #33 found this half stale at `6186006`. It named `2f95600` as the
commit that fixed it. Part 2's line numbers have drifted too:
`spec-reviewer/SKILL.md:283` is now `:314`, `spec-writer/SKILL.md:289` is now
`:365`, `implementer/SKILL.md:52` is now `:59` and `pipeline-clerk/SKILL.md:61`
is now `:106`. The quoted text is still there apart from wording around the
numbers, and the finding still holds. This item covers Part 2 only.

## The rule it serves

`.agents/skills/agent-police/SKILL.md`, read 6, the rule #33 was filed under:

> **A bound has one number, in one place.** Collect every number any document
> states for every counter, each with its file and line, and decide from the
> collection where that counter's number is *stated* and where it is merely
> quoted. Two documents stating it, or a quote that disagrees with the
> statement, is the finding either way.

The law already applies this pattern to its own claim-freshness bound,
`.agents/skills/pipeline-law/SKILL.md`, **Where the machine keeps its state**:

> **The claim-freshness bound is stated here and nowhere else: two hours.**
> […] Every role applies that test by naming this bound and never by restating
> the number, so raising it is one edit.

This change applies the same pattern to the counters.

## Proposed change

Five files change, all under `.agents/skills/`. No other path changes.

None of these paths is in the law's forbidden-paths table at `281b817`. The
law says, under **What no role writes**, "`.agents/**` is **not** forbidden
either." The commit that made it so is `2efd620`, "chore(agents): let the
pipeline write .agents/", dated 2026-10-12. This item's earlier stop, of
2026-10-10 at key `58fe1e6e6d22`, rested on the older table, which still
listed `.agents/**`. That reason no longer holds.

**Where the numbers go: the law.** All four pipeline roles read the law and
none of them copies it. The court's comment on #33 left the choice of document
open. The alternatives below are the reasons for choosing the law.

### 1. `.agents/skills/pipeline-law/SKILL.md`, `### How every bound behaves`

Replace

> `slices` is the fifth counter and is **not** a bound. It is a day's pace: at
> three the Implementer stops without re-entering itself, and the Clerk's sweep
> re-fires the item the next day. Nothing about it reaches a person, so it has
> no content key and records no stop.

with

> `slices` is the fifth counter and is **not** a bound. It is a day's pace: at
> the day's cap the Implementer stops without re-entering itself, and the
> Clerk's sweep re-fires the item the next day. Nothing about it reaches a
> person, so it has no content key and records no stop.
>
> **Each counter's number is stated here and nowhere else.**
>
> | Counter | Reached at | Kind |
> | :-- | :-- | :-- |
> | `review_rounds` | 5 | bound |
> | `gate_bounces` | 2 | bound |
> | `judge_rejects` | 2 | bound |
> | `cr_rounds` | 3 | bound |
> | `slices` | 3, the day's cap | pace |
>
> A role reaches a counter by naming it, as "`review_rounds` at its bound" or
> "`slices` at the day's cap", and never by restating the number. Raising one
> is then one edit.

The table goes in as a real Markdown table, not as a block quote. The quote
marks here only fence the new text off from this specification. The
paragraph "There are four: …" above it and the three numbered rules below it
stay as they are.

### 2. `.agents/skills/spec-writer/SKILL.md`, `## Routing`, **The bound.**

`:365`: replace "Read `review_rounds` from the state block. At 5 or above,"
with "Read `review_rounds` from the state block. At its bound or above (the
law's **How every bound behaves** states the number),". The rest of the
paragraph stays.

### 3. `.agents/skills/spec-reviewer/SKILL.md`

- `:136`, table row: replace "`review_rounds` at 5 or above, whatever else
  the marker says" with "`review_rounds` at its bound or above, whatever else
  the marker says".
- `:314`, **The bound.**: replace "At `review_rounds` of 5 or above, compare
  the current spec hash" with "With `review_rounds` at its bound or above (the
  law's **How every bound behaves** states the number), compare the current
  spec hash".

### 4. `.agents/skills/implementer/SKILL.md`

- `:59`: replace "When it is today and `slices` is 3 or above, stop here:"
  with "When it is today and `slices` is at the day's cap or above (the law's
  **How every bound behaves** states the number), stop here:".
- `:138`: replace "The exception is `gate_bounces` already at 2," with "The
  exception is `gate_bounces` already at its bound,".
- `:181`: replace "**A first gate failure** is one plain issue comment, then
  the handoff:" with "**A gate failure below the bound** is one plain issue
  comment, then the handoff:".
- `:185`: replace "2. Set `gate_bounces=1` in the state block." with "2.
  Increment `gate_bounces` in the state block."
- `:192`: replace "**A second gate failure** is the bound." with "**A gate
  failure that brings `gate_bounces` to its bound** is the bound."
- `:195`: replace "1. Set `gate_bounces=2` in the state block." with "1.
  Increment `gate_bounces` in the state block."
- `:210`: replace "**`gate_bounces` already at 2** is only seen after an
  un-stick," with "**`gate_bounces` already at its bound** is only seen after
  an un-stick,".
- `:327`: replace "3. Below 3, re-enter yourself:" with "3. Below the day's
  cap, re-enter yourself:".
- `:328`: replace "4. At 3 or above, stop without re-entering." with "4. At
  the day's cap or above, stop without re-entering."
- `:468-469`: replace "A second consecutive rejection, one that brings
  `judge_rejects` to 2 or above, reaches the law's bound." with "A rejection
  that brings `judge_rejects` to its bound or above reaches the law's bound.
  An accepted verdict resets the counter, so only consecutive rejections
  reach it."
- `:474`: replace "`judge_rejects` at 2 or above follows the law's bound
  rule." with "`judge_rejects` at its bound or above follows the law's bound
  rule."
- `:618`: replace "Never run more than three slices on one item in one UTC
  day," with "Never run more slices on one item in one UTC day than the day's
  cap,".

### 5. `.agents/skills/pipeline-clerk/SKILL.md`

- `:106`, table row: replace "with `slices` at 3 or above and `slices_day`
  before today" with "with `slices` at the day's cap or above and
  `slices_day` before today".
- `:375`: replace "At `cr_rounds` of 3 or above this head has had its rounds"
  with "With `cr_rounds` at its bound or above (the law's **How every bound
  behaves** states the number) this head has had its rounds".
- `:396`: replace "**The bound.** `cr_rounds` at 3 or above on an unchanged
  head is a bound reached." with "**The bound.** `cr_rounds` at its bound or
  above on an unchanged head is a bound reached."

Lines may be re-wrapped to keep each paragraph's existing width. Re-wrapping
changes no word.

### Alternatives rejected

- **Keep each number in the one role that enforces it, and have the others
  quote it.** The Spec Writer and the Spec Reviewer both test
  `review_rounds`, and neither of them owns it more than the other. The
  Implementer and the Clerk both test `slices`. Whichever role held the
  number, another role would have to point across at it. The law is the one
  document all four read and none copies.
- **Keep the ordinal wording for `gate_bounces`** ("a first / a second gate
  failure", "set `=1`" / "set `=2`"). That wording is the number 2 in
  another form. Raising the bound to 3 would leave a third failure with no
  instruction. Incrementing, and testing against the bound, works for any
  number.
- **Leave the `slices` numbers alone because `slices` is not a bound.** Read 6
  says "every number any document states for every counter", not every bound,
  and `slices` is stated in three documents today. The name "the day's cap" is
  not new: the Implementer already uses it as a heading at
  `implementer/SKILL.md:57`.

## Acceptance criteria

1. `git grep -nE '[0-9] or above|\bat three\b|\bat (2|3|5)\b|Below 3|more than three slices|gate_bounces=[12]|A (first|second) gate failure|second consecutive rejection' -- .agents/skills/`
   prints nothing.
2. `.agents/skills/pipeline-law/SKILL.md` contains the line
   `**Each counter's number is stated here and nowhere else.**` and a table
   with exactly these five data rows, in this order:
   `` `review_rounds` | 5 ``, `` `gate_bounces` | 2 ``,
   `` `judge_rejects` | 2 ``, `` `cr_rounds` | 3 ``,
   `` `slices` | 3, the day's cap ``.
3. `.agents/skills/pipeline-law/SKILL.md` no longer contains
   `three the Implementer stops`. Each of the 20 lines criterion 1's pattern
   matches at `281b817` reads, after the change, as `## Proposed change`
   writes it.
4. Each of the four role files `spec-writer`, `spec-reviewer`, `implementer`
   and `pipeline-clerk` contains `How every bound behaves` at least once.
5. `.agents/skills/agent-police/SKILL.md` is unchanged. Its line "from 3 to 5"
   is the recorded reason for read 6, not a statement of a bound.
6. `tools/check-conformance.py` exits 0.
7. `tools/regenerate.sh` leaves nothing to commit.
8. The `selftest` and `validate` of `tools/evals.py` pass.
9. `git diff --name-only origin/main...HEAD` lists only the five files of
   `## Proposed change`, plus this item's own
   `.agents/specs/33-bound-numbers-one-place/` until the final slice deletes it.

## Out of scope

- **#33 Part 1**, `cr_rounds` missing from the bound section. It is already
  fixed on `main` (see `## Problem`), so nothing here touches it.
- The secondary points the court did not look into: `cr_rounds`'s reset, and
  the Clerk's cross-reference to "the law's bound rule". Rules 2 and 3 of the
  law's section now cover both, and this item does not reopen them.
- #33's quotation that puts "on 2026-09-12" inside a quote of
  `agent-police/SKILL.md`. That is a defect of the issue text, and nothing in
  the tree needs to change for it.
- `.agents/skills/agent-police/SKILL.md:202-203`, "the owner raised one bound
  from 3 to 5". It is a recorded reason and stays word for word.
- Other numbers that are not counters: the claim-freshness bound (already in
  one place), the Clerk's "twelve hours" re-entry row
  (`pipeline-clerk/SKILL.md:107`), and the Spec Reviewer's internal "round 2"
  (`spec-reviewer/SKILL.md:165`), which is a pass inside one review and not
  `review_rounds`.
- Changing any counter's value. Every number in the new table is the value
  the roles state today.
- None of the law's forbidden paths is touched, and #33 names none.

## Risks

- **A number missed.** A role keeps a number this census did not find, and
  the old two-place problem survives in one spot. The tell is criterion 1
  printing a line. A form the pattern cannot see, like a number spelled as a
  word in a new place, is caught by criterion 3's read.
- **The gate's behaviour changes.** Replacing "set `gate_bounces=1`/`=2`" with
  "increment" is the same at today's bound only if the counter starts at 0
  and moves only through these two steps. The Clerk's skeleton writes
  `gate_bounces=0` (`pipeline-clerk/SKILL.md:611`). Rule 3 says the counter
  never resets. So "increment" gives 1 and then 2, the same values as today.
  After an un-stick, the counter is already at the bound and the
  "already at its bound" paragraph handles it, as it does today. The tell is
  a gate failure that writes a value different from the one the old text
  would have written.
- **"At its bound" read as `==`.** Every replacement keeps "or above", and
  the law's rule 1 says `>=`. The tell is a replacement sentence that drops
  "or above".

