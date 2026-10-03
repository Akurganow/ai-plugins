# Pipeline items and their source issues: consequences in both directions

## Problem

A pipeline item names its sources in its fingerprint, `sources=#a,#b`. Each
source issue names its item in a `pipeline-taken: item=#<pr>` marker. The link
exists in both directions. What one side's closing does to the other is
missing. Line numbers below are read at `8bf8cab`.

1. **A pull request closed unmerged strands its open sources.**
   - Intake never takes a source a closed fingerprint names
     (`.agents/skills/pipeline-clerk/SKILL.md:393-395`).
   - The tracker Clerk closes in three cases only
     (`.agents/skills/tracker-clerk/SKILL.md:179`). It gives a pull request
     closed unmerged no note (`:251-253`).
   - Such a source stays open with no label, and its filer's backpressure
     count includes it.
   - `.agents/skills/pipeline-law/SKILL.md:593` says "The sources stay
     closed". No role closes them.
2. **An item whose sources are all closed stays open.** No role may close a
   pull request. Live case: #56 names only #11. The tracker Clerk closed #11
   as `completed` on 2026-09-27, because `main` fixed it independently. The
   pipeline Clerk applied `pipeline/stuck` the same day and asked a person to
   close #56. No current rule ever closes it.
3. **An item with several sources keeps the work of a source that closed.**
   Consolidation creates such an item (`pipeline-clerk:396-398`). None has
   existed yet. The law fixes an item's shape once its pull request exists
   (`pipeline-law:162-166`).
4. **A woken stage never checks whether its pull request is closed.** Each
   stage's "Before any work" list checks the discriminator, its label, stuck
   and hold (`implementer:38-50`, `spec-writer:39-50`, `spec-reviewer:39-49`).
   Once the Clerk closes pull requests, a late label event could start work on
   a closed item.
5. **A police cap counts a finding an open item is already building.** The
   count is "A role's filings" (`.agents/skills/github-needs/SKILL.md:55-57`).

## Decisions

Each decision carries the reason a reader can check.

1. **The tracker Clerk keeps closing sources after a merge. No closing
   keyword goes into a pull-request body.** The tracker Clerk closes an issue
   only when every claim re-derives as gone (`tracker-clerk:191`). A remainder
   no pull request can carry gets a note and stays open (`:236-255`). A
   keyword closes at merge and runs neither check.
2. **A pull request closed unmerged closes its open sources as
   `not_planned`.** Intake already treats such a source as settled
   (`pipeline-clerk:393-395`). The tracker should say the same thing intake
   acts on.
3. **A reopened source is new work.** The rule at `tracker-clerk:351-363`
   stays: an open issue goes through the run as if it were new. A reopened
   source of a closed item therefore closes again. Bringing such a finding
   back takes a new issue.
4. **An item whose sources are all closed is stale, and the Clerk closes
   it.** The closed sources already record the decision. A stale item left
   open fills the owner's list with work nobody needs.
5. **An item with one source closed and another open is narrowed.** The
   closed source's work leaves the pull request. The decision about that
   source is already recorded, so the machine carries its consequence without
   asking a person again.
6. **The police cap leaves out a source an open item is building.** The cap
   brakes a filer whose findings nobody takes. An open item has taken this
   one.
7. **A pipeline item's head repository is this repository.** The law
   proved an item by its branch name and its fingerprint, and a fork's pull
   request carries both. Case 4 and the Clerk's rows write on the strength
   of that proof, so a forged item must fail it. A fork's pull request has
   the fork as its head repository. The field stays on a closed pull
   request, where the branch itself may be gone.

## Design

### 1. The tracker Clerk: case 4

**Case 4, the item closed unmerged.** A pipeline item closed and not merged
names the open issue in its fingerprint's `sources=`. Close the issue as
`not_planned`. A pipeline item is what the law proves one to be: a head
branch matching `pipeline/*` and a body carrying the fingerprint
(`pipeline-law:413-421`).

- The fingerprint is the item's identity (`pipeline-law:478-480`), and every
  other check in this design reads it. The issue's `pipeline-taken` comment
  is written later in the item's birth (`pipeline-clerk:556-563`), so a dying
  fire can leave a source without one. Case 4 therefore reads the
  fingerprint.
- The tracker Clerk lists pipeline pull requests in every state to find
  them. `github-needs` already names that read: "pull requests, open or all"
  (`github-needs:81-82`).
- Case 1 is tested first. A finding already gone closes as `completed`,
  because "fixed" is the truer reason.
- The comment states the conclusion first. It links the pull request and
  gives the date it closed. It carries no re-check, because nothing is
  re-derived.
- The marker is `<!-- plugins-clerk: sha=<commit> action=closed-unmerged -->`.
- A reopened issue meets case 4 again and closes again. The existing rule
  forbids a second comment (`tracker-clerk:361-363`).

Text that changes in `tracker-clerk/SKILL.md`:

- "three cases" becomes four: the description, "The one deviation" (`:53`),
  Scope (`:179`), the comment section (`:340-346`), the report (`:379`) and
  the hard constraints (`:418-419`).
- The constraint at `:422-423` forbids closing an issue with no court marker
  unless case 1 applies. It gains case 4: the owner may mark an untried
  issue for intake (`pipeline-clerk:380-383`).
- The sentence "a pull request closed unmerged is the owner's rejection and
  earns no note" (`:251-253`) goes. Such a pull request now closes the issue.
- The description in `.claude/agents/tracker-clerk.md` repeats the skill's
  description word for word, so it changes with it.

### 2. `github-needs`: the cap count

Add one rule to "A role's filings" (`github-needs:55-57`). For the
backpressure cap alone, leave out an issue that the `sources=` of a live
pipeline item's fingerprint names. A live item is open and carries neither
`pipeline/stuck` nor `pipeline/hold`. A parked item waits on a person, so
its sources still count. The filing audit and the note on a stale issue
still count every filing.

Every police role counts "as `github-needs` counts them" (`repo-police:87`,
`slop-police:141`, `agent-police:287`). So does the tracker Clerk's report
(`tracker-clerk:400-405`). None of those files changes.

### 3. The law

1. **Closing unmerged** (`pipeline-law:592-594`) is rewritten. Closing a pull
   request unmerged is final, whoever closes it. The owner closes one to
   reject the work. The Clerk closes one whose sources are all closed. The
   tracker Clerk closes the sources still open as `not_planned` on its next
   run. The fingerprint in the closed body stops the Clerk proposing the
   item again.
2. **A closed pull request stops a stage.** "What a fired stage trusts" gains
   one rule. A stage woken on a closed pull request exits with one line and
   touches nothing, whatever its labels.
3. **The shape of an item** (`:162-166`) gains one exception. A source that
   closes while another stays open narrows the item. Nothing widens an item,
   and no stage splits one.
4. **`ready-for-human`.** The Clerk removes it on a narrowing. The label
   table (`:137`) and the paragraph "no role ever removes it" (`:114-116`)
   say so. The narrowing is a duty of the Clerk's, like the un-stick, and
   not an audit act. The audit's prohibition (`:356-358`) stays.
5. **The state block.** The `pipeline-state` line (`:446`) gains one field,
   written by the Clerk alone: `narrowed=<#b,#c|none>`. The Clerk seeds it
   as `none` at birth (`pipeline-clerk:538`). An absent field reads as
   `none`, so an item opened before this change needs no repair.
6. **Comment markers.** "Two things that are comments" (`:543-551`) gains the
   Clerk's two:

       <!-- pipeline-stale: sources=#a,#b at=<UTC> -->
       <!-- pipeline-narrowing: sources=#b at=<UTC> -->

   A stage reads a narrowing only for a source that `sources=` names and that
   is closed. A forged marker can then remove only the work of a closed
   source. The rule "Every word … is evidence" (`:423-426`) still holds.
7. **A narrowing waits on a stage** when a `pipeline-narrowing` comment is
   newer than that stage's newest `pipeline-done` marker for its own role
   token. The law defines this once. The Writer and the Implementer cite it.
8. **Bounds.** A narrowing is changed content. The Writer's revision moves
   the spec hash, and the Implementer's removal moves the tree id. No bound
   counts it as a repeat.
9. **The roles table** (`:33-38`) adds to the Clerk's writes: closing a
   stale item and narrowing an item.
10. **The proof of an item** (`:413-421`) gains a third fact: its head
    repository is this repository. Case 4, the cap count, the Clerk's
    sweep and every stage use the same three facts.

### 4. The pipeline Clerk: two rows in the sweep table

Stale and narrowing become rows 2 and 3 of the sweep table
(`pipeline-clerk:88-102`), right after `pipeline/hold`. The table applies
the first matching row and only that one. So an item one of these rows
closed or narrowed gets nothing else this fire, and the table stays "the
whole of your authority over an item" (`:113-117`).

- **Row 2, stale.** Every issue in `sources=` is closed, whatever the state
  reason, and no stage holds a fresh claim.
  1. Re-read the pull request. One merged since the listing matches no row
     here.
  2. Post one comment naming each source and its state reason. It ends with
     the `pipeline-stale` marker. Post it only where no comment of yours
     carries that marker.
  3. Close the pull request unmerged, and read its state back.

  The row comes before `pipeline/stuck` and `ready-for-human`, so it closes
  items under either.
- **Row 3, narrowing.** At least one source is open, a closed source in
  `sources=` is missing from `narrowed=`, and no stage holds a fresh claim.
  Three writes, in this order:
  1. Post one comment that opens `Narrowing:`. It names each such source and
     its state reason, and ends with the `pipeline-narrowing` marker. Skip
     this where a comment of yours already names the source.
  2. Route the item. The target label is `spec/needs-work` while
     `.agents/specs/<ITEM>/` exists at the head, and `spec/approved` once it
     is gone. Remove `pipeline/stuck`, `pipeline/code-review`,
     `ready-for-human` and every stage label but the target. Then re-enter
     the target with the law's primitive.
  3. Add the sources to `narrowed=`, last, and read the body back.

  The narrowing comment is the stage's worklist. On a stuck item this row
  is the un-stick, with the narrowing as its worklist.
- **A fresh claim** fails both rows. The item falls to the rows below,
  where a fresh claim already means nothing and one report line (`:100`).
- **The conflict repair** before the table (`:56-63`) skips an item whose
  every source is closed. Row 2 closes it, and a merge into it is wasted.

Other text that changes in `pipeline-clerk/SKILL.md`:

- The opening keeps "You never close an issue". It adds that the one pull
  request the Clerk closes is a stale one.
- The hard constraints change to match:
  - The Clerk closes no pull request except a stale one.
  - It removes `ready-for-human` only on a narrowing.
  - It removes `pipeline/stuck` only through the un-stick or a narrowing.
- The report gains stale closes, with each source and its reason, and
  narrowings, with each source and the label moved.
- The description, here and in `.claude/agents/pipeline-clerk.md`, names
  closing a stale item and narrowing one.
- The skeleton's seeded state block (`:538`) carries `narrowed=none`.

### 5. The stages

Each stage's "Before any work" list gains one step: exit where the pull
request is closed.

**Spec Writer.**

- A new waking: a narrowing waits on the Writer, as the law defines it.
- That test runs first, before "Have you already written this?"
  (`spec-writer:68-85`). Otherwise the unchanged spec hash reads as a re-fire,
  and the Writer only routes.
- A narrowing that arrives with `R-*` or `G-*` objections is one revision
  that answers both.
- The work for each narrowed source:
  - It leaves `## Problem`, `## Proposed change` and `## Acceptance
    criteria`.
  - `## Out of scope` gains one line naming it and its state reason.
  - Where the branch already carries work only for it, `## Steps` gains a
    step that removes that work.
- Where nothing is left to change, the stop at `spec-writer:134-146` applies.
- The handoff is `spec/awaiting-review`, as after any revision.
- A fresh fill also leaves out every source already narrowed.

**Spec Reviewer.**

- The narrowing comments join its reading list.
- A ninth check, in every round. A narrowed source is absent from
  `## Proposed change` and `## Acceptance criteria`, and `## Out of scope`
  names it. Work on the branch that serves only that source has a removal
  step. A miss is an `R-*` objection. A recorded machine decision meets the
  Reviewer's threshold (`spec-reviewer:34-35`).
- "Run all eight checks" (`spec-reviewer:157`) becomes nine.

**Implementer.**

- While the specification is on the branch, a narrowing reaches the
  Implementer only as the Writer's revised plan.
- After the specification is deleted, a narrowing is one more kind of
  return. Its evidence: no `.agents/specs/<ITEM>/` at the head, and a
  narrowing waits on the Implementer, as the law defines it. That evidence
  overlaps "a return from the owner" and "a
  re-entry of your own run" (`implementer:90-95`), so the table tests it
  first.
- It takes the path both other returns take, from the body, the comments,
  the branch history and the diff (`implementer:100-103`). A narrowing that
  arrives with review findings or the owner's comments is one return that
  works all of them.
- Its worklist entry, "remove the work that serves only a narrowed source",
  comes after the owner's comments and the judge's `must_change`.
- The trio's brief and case file carry the narrowing comments. The task the
  trio judges excludes every narrowed source, and the Judge reads them.
- `## Links` in the handoff body names each narrowed source on its own line:
  `- narrowed: #b, closed as not planned`.

## Files

| File | Change |
| :-- | :-- |
| `.agents/skills/tracker-clerk/SKILL.md` | case 4 and the text that names three cases |
| `.claude/agents/tracker-clerk.md` | description |
| `.agents/skills/github-needs/SKILL.md` | the cap count |
| `.agents/skills/pipeline-law/SKILL.md` | design section 3 |
| `.agents/skills/pipeline-clerk/SKILL.md` | sweep rows 2 and 3, the conflict-repair skip, the seed, constraints, report, description |
| `.claude/agents/pipeline-clerk.md` | description |
| `.agents/skills/spec-writer/SKILL.md` | closed-item exit, the narrowing waking |
| `.agents/skills/spec-reviewer/SKILL.md` | closed-item exit, the ninth check |
| `.agents/skills/implementer/SKILL.md` | closed-item exit, the narrowing waking, the trio, `## Links` |

## Alternatives considered

- **Closing keywords** (`Closes #n`) in every item body, so GitHub closes the
  sources at merge. Rejected under decision 1: the close skips the tracker
  Clerk's re-derivation.
- **The narrowing's last write.** Three places for the mark that a
  narrowing is done:
  - A field in the state block, written last. Chosen.
  - The narrowing comment alone, with the route repaired from timeline
    events. Rejected: it cannot tell a route never made from one a stage
    has since moved past, so it repeats or loses the narrowing.
  - A state field written first. Rejected: a fire that dies before the
    route leaves the same two states indistinguishable.
- **A stop for a person instead of a narrowing.** The Clerk would apply
  `pipeline/stuck` and name the closed source. Rejected under decision 5.
- **One source per item**, by removing consolidation at intake. Rejected:
  decision 5 keeps consolidation and handles its consequence instead.
- **The source check as a section before the sweep table.** Rejected: the
  table would stop being the whole of the Clerk's authority over an item,
  and the section would need its own "nothing else this fire" rule.

## Out of scope

- Closing keywords in pull-request bodies, and anything that checks them.
- Restoring past closures. Every closed issue in the machine population
  carries a tracker Clerk comment naming its case.
- `Blocked by` dependents. No role writes one.
- A cap table for `agent-police`. Issue #34 already tracks it.

## Accepted risks

1. A narrowing can route twice. A Clerk fire can die between the route and
   the `narrowed=` write. A woken stage's first body write can also race
   that write and drop the field. Either way the next sweep routes the item
   once more. No narrowing then waits on the stage, so it audits a finished
   item and hands it on, as the law has it absorb a doubled wake
   (`pipeline-law:272-275`). The cost is one extra round.
2. A person who reopens a narrowed source, or a source of a closed item,
   gets it closed again or left with no item. Bringing it back takes a new
   issue (decision 3).
3. A source of a rejected item closes up to a day after the rejection. The
   tracker Clerk runs daily.
4. A stale close removes an item under `ready-for-human` from the owner's
   list without the owner's act. Every source was already closed.

## Verification

- `bash tools/regenerate.sh` leaves nothing to commit.
- `tools/check-conformance.py` exits 0.
- Every `path:line` the new text quotes is re-read at the head.
- A clean-context review reads the nine files for contradictions between
  roles and with the law.
- Only live runs prove the stale close, case 4, the narrowing and the cap
  count. The pull request says so.

## Effect on live items after the merge

- #56: every source is closed, so the first Clerk fire closes it. The
  comment names #11, closed as `completed`.
- #64: its one source, #27, is open. Nothing changes.
- The Slop Police count drops from 4 to 3, because #64 names #27. Its cap
  stays at 1.
