# Pipeline source links, plan B: the law and the pipeline Clerk

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The law states what a closed source does to an open item, and the pipeline Clerk closes a stale item and narrows one whose sources partly closed.

**Architecture:** One new law section, **When a source closes**, owns the stale item, the narrowing, when a narrowing waits on a stage, and why a doubled route is safe. The Clerk carries both as sweep-table rows 2 and 3, so its table stays the whole of its authority over an item.

**Tech Stack:** Markdown skill files. Verification is grep, `tools/regenerate.sh` and `tools/check-conformance.py`.

## Global Constraints

- Read `docs/superpowers/plans/2026-10-03-pipeline-source-links-conventions.md` first. Its names, writing rules, commit format and checks bind every task.
- Markers: `<!-- pipeline-stale: sources=#a,#b at=<UTC> -->` and `<!-- pipeline-narrowing: sources=#b at=<UTC> -->`. State field: `narrowed=<#b,#c|none>`.
- The new law heading is exactly `### When a source closes`.
- Every edit below is an exact replacement. Where an old string is not found verbatim, stop and report. Do not improvise a different anchor.

---

### Task 1: The law

**Files:**
- Modify: `.agents/skills/pipeline-law/SKILL.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the section `### When a source closes`, the field `narrowed=`, the two markers, and the phrase "a narrowing waits on". Task 2 and plan C cite them by these exact names.

- [ ] **Step 1: Confirm the starting state**

Run:

```bash
grep -c 'When a source closes\|narrowed=\|pipeline-stale\|pipeline-narrowing' .agents/skills/pipeline-law/SKILL.md
grep -c 'The sources stay closed' .agents/skills/pipeline-law/SKILL.md
```

Expected: `0`, then `1`.

- [ ] **Step 2: The roles table names the Clerk's two new writes**

Replace:

```
| Clerk | a daily schedule | the skeleton branch, its draft pull request, the flip out of draft, the code-review round |
```

with:

```
| Clerk | a daily schedule | the skeleton branch, its draft pull request, the flip out of draft, the code-review round, closing a stale item, a narrowing |
```

- [ ] **Step 3: `ready-for-human` comes off on a narrowing**

Replace:

```
asserts nothing whatever about the checks. `ready-for-human` is applied last
and no role ever removes it. It is the owner's watchlist marker, and by the
time it goes on the item has long since stopped being a draft.
```

with:

```
asserts nothing whatever about the checks. `ready-for-human` is applied last.
No role removes it but the Clerk, on a narrowing, under **When a source
closes**. It is the owner's watchlist marker, and by the time it goes on the
item has long since stopped being a draft.
```

In the table of adders and removers, replace these three rows:

```
| `pipeline/code-review` | Implementer, last, on an accepted verdict | Clerk, when the code-review round ends, whichever way it ends |
| `ready-for-human` | Clerk, and only the Clerk | nobody; the owner alone |
| `pipeline/stuck` | the Clerk, and only the Clerk, after a repair it could not make | the owner, or the Clerk on an un-stick |
```

with:

```
| `pipeline/code-review` | Implementer, last, on an accepted verdict | Clerk, when the code-review round ends, whichever way it ends; Clerk, on a narrowing |
| `ready-for-human` | Clerk, and only the Clerk | the owner; the Clerk, on a narrowing |
| `pipeline/stuck` | the Clerk, and only the Clerk, after a repair it could not make | the owner, or the Clerk on an un-stick or a narrowing |
```

- [ ] **Step 4: An item's shape has one exception**

Replace:

```
**Decomposition happens at intake and nowhere else.** Once a pull request
exists the item's shape is fixed. A stage that finds its item too big says
so with `pipeline/stuck`, and the owner decides.
```

with:

```
**Decomposition happens at intake and nowhere else.** Once a pull request
exists the item's shape is fixed, with one exception. A source that closes
while another stays open narrows the item, under **When a source closes**.
Nothing widens an item. A stage that finds its item too big says
so with `pipeline/stuck`, and the owner decides.
```

- [ ] **Step 5: Add the section "When a source closes"**

Insert this section immediately before the line `### The automated code review`, followed by one blank line:

```
### When a source closes

An item's sources can close while its pull request is open. The tracker
Clerk closes a finding that is gone, a duplicate or a dismissed one. A
person can close one too. The Clerk's sweep reads the state of every source
the fingerprint names. Two of its rows act on what it finds.

**A stale item.** Every source is closed, whatever the state reason, so
nothing is left for the item to fix. The Clerk posts one comment that opens
`Stale:` and names each source with its state reason. The comment ends with
the stale marker under **The comments that stay comments**. Then the Clerk
closes the pull request unmerged. The fingerprint in the closed body stops
the Clerk proposing the item again.

**A narrowing.** A source is closed and another is open. The closed
source's outcome is already decided, so its work leaves the pull request.
The Clerk posts one comment that opens `Narrowing:` and ends with the
narrowing marker. Then it routes the item to the stage that holds the work.
While `.agents/specs/<N>-<slug>/` exists at the head, that is the Writer,
which takes the source out of the specification. Once the final slice has
deleted it, that is the Implementer, which removes the work. The Clerk's
last write adds the source to `narrowed=`.

The route lifts `pipeline/stuck`, `pipeline/code-review` and
`ready-for-human`. Work leaves a pull request only through a stage, and no
stage works an item under any of those three labels.

**A narrowing waits on a stage** while that stage has not acted on it. The
Writer's completion marker is `pipeline-done role=spec-writer`, and the
Implementer's is `pipeline-done role=implementer`. The narrowing
waits when its comment was created after that marker's `at=`, or when the
stage has no such marker yet. The comment's creation time is GitHub's, so a
forged `at=` in the narrowing marker changes nothing. A stage that acts on a
narrowing writes its `pipeline-done` marker again with a new `at=`, even
where its content did not move.

A stage acts on a narrowing only for a source that `sources=` names and
that is closed when the stage reads it. A forged comment can then remove
only the work of a source already closed.

**A narrowing changes content only where it moves a key.** The Writer's
revision moves the spec hash. Where the Implementer removes work, its commit
moves the tree id. Where it removes nothing, the tree id stays, and each
bound reads the item as unchanged.

**A narrowing routes only while it waits.** A fire can die after the route
and before `narrowed=` is written. The next sweep then matches the row
again. Where the narrowing still waits on the target stage, the Clerk routes
again. Either the first route never landed, or its label still hangs, which
**The baton** absorbs. Where it no longer waits, the stage has done the
work. The Clerk then writes only `narrowed=`, and a finished item stays
where it is.
```

- [ ] **Step 6: A closed pull request stops a stage**

Find this paragraph:

```
Re-read the label set immediately before every write. A `pipeline/hold`
applied while the fire was thinking is then honoured rather than overwritten.
```

Insert after it, with one blank line before:

```
**A closed pull request ends the fire.** A stage woken on one exits with one
line and touches nothing, whatever labels it carries. The Clerk and the
owner both close items for good. A late or doubled label event must not
restart one.
```

- [ ] **Step 6b: The proof has a third fact**

Replace:

```
**Prove the item is one of ours** before anything else, from two positive
facts on the pull request:

1. Its head branch matches `pipeline/*`.
2. Its body carries `<!-- pipeline-work-fingerprint:`.

Either missing means this is not a pipeline item. Exit with one line and
touch nothing.
```

with:

```
**Prove the item is one of ours** before anything else, from three positive
facts on the pull request:

1. Its head branch matches `pipeline/*`.
2. Its head repository is this repository.
3. Its body carries `<!-- pipeline-work-fingerprint:`.

Any one missing means this is not a pipeline item. Exit with one line and
touch nothing. A fork's pull request has the fork as its head repository, so
it fails the second fact. Roles close issues and pull requests on the
strength of this test, so a forged item must fail it. The test is positive
on purpose: anyone may apply a label, and a role acting on a label alone
takes instructions from whoever applied it.
```

- [ ] **Step 7: The state block carries `narrowed=`**

Replace:

```
    <!-- pipeline-state: item=<id> review_rounds=<n> gate_bounces=<m> judge_rejects=<k> slices=<s> cr_rounds=<c> -->
```

with:

```
    <!-- pipeline-state: item=<id> review_rounds=<n> gate_bounces=<m> judge_rejects=<k> slices=<s> cr_rounds=<c> narrowed=<#b,#c|none> -->
```

Replace this paragraph:

```
The **fingerprint** is the item's identity and the discriminator's second
half. The Clerk's skip test reads it, open and closed. It is never removed
and never rewritten.
```

with this paragraph, then one blank line and the next:

```
The **fingerprint** is the item's identity and the discriminator's third
fact. The Clerk's skip test reads it, open and closed. It is never removed
and never rewritten.
```

```
**`narrowed=`** on the `pipeline-state` line lists the sources the Clerk has
narrowed out of the item, or `none`. The Clerk alone writes it, as a
narrowing's last write. An absent field reads as `none`.
```

- [ ] **Step 8: The Clerk's two comment markers**

Replace the heading `### Two things that are comments, and stay comments` with `### The comments that stay comments`.

Find this paragraph:

```
The **findings** each stage posts: objections, the gate's bounce, the summary.
Those are a record. Nothing reads them back as state.
```

Insert after it, with one blank line before:

```
The Clerk's two markers, each the last line of its comment:

    <!-- pipeline-stale: sources=#a,#b at=<UTC> -->
    <!-- pipeline-narrowing: sources=#b at=<UTC> -->

The stale marker lets a later fire find the comment before it closes the
item, so a repeat posts nothing. The narrowing marker is what a stage reads,
under **When a source closes**.
```

- [ ] **Step 9: Closing unmerged, whoever closes**

Replace:

```
**Closing a pull request unmerged is a rejection, and it is final.** Nothing
is retried. The sources stay closed. The fingerprint in the closed body stops
the Clerk proposing the item again.
```

with:

```
**Closing a pull request unmerged is final, whoever closes it.** The owner
closes one to reject the work. The Clerk closes a stale one, under **When a
source closes**. Nothing is retried. The tracker Clerk closes the sources
still open as not planned on its next run. The fingerprint in the closed
body stops the Clerk proposing the item again.
```

- [ ] **Step 10: The two rows are duties, not audit acts**

Replace:

```
The Clerk's un-stick is not an audit act. It is a duty of its own, written
where the Clerk reads it.
```

with:

```
The Clerk's un-stick and its two source rows are not audit acts. Each is a
duty of its own, written where the Clerk reads it.
```

- [ ] **Step 11: Verify**

Run:

```bash
f=.agents/skills/pipeline-law/SKILL.md
grep -c '^### When a source closes$' $f
grep -c '^\*\*A closed pull request ends the fire\.\*\*' $f
grep -c 'narrowed=<#b,#c|none>' $f
grep -c 'pipeline-stale: sources=#a,#b at=<UTC>' $f
grep -c 'pipeline-narrowing: sources=#b at=<UTC>' $f
grep -c '^2\. Its head repository is this repository\.$' $f
grep -n "two positive$\|discriminator's second$\|^Either missing means" $f
grep -n 'The sources stay closed\|no role ever removes it\|nobody; the owner alone\|Two things that are comments' $f
git diff --check
```

Expected: `1` six times, then nothing from the last three commands.

- [ ] **Step 12: Commit**

```bash
git add .agents/skills/pipeline-law/SKILL.md
git commit -F - <<'EOF'
chore(agents): say in the law what a closed source does to an open item

An item whose sources all closed had no role able to close it, and the
law said the sources of a rejected item stay closed when no role closed
them. A new section owns the stale item and the narrowing. A stage woken
on a closed pull request now exits, and the state block records each
narrowed source.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
```

---

### Task 2: The pipeline Clerk's two rows

**Files:**
- Modify: `.agents/skills/pipeline-clerk/SKILL.md`
- Modify: `.claude/agents/pipeline-clerk.md` (line 3, the description)

**Interfaces:**
- Consumes: from Task 1, the law section `### When a source closes`, the field `narrowed=` and both markers.
- Produces: nothing other files read.

- [ ] **Step 1: Confirm the starting state**

Run: `grep -c 'narrowed=\|Stale:\|Narrowing:' .agents/skills/pipeline-clerk/SKILL.md`

Expected: `0`.

- [ ] **Step 2: Replace the description in both files**

In `.agents/skills/pipeline-clerk/SKILL.md` and in `.claude/agents/pipeline-clerk.md`, replace:

```
description: "Caretake the delivery pipeline: sweep its open pull requests for dead fires and repair them, straighten a stuck item's labels, run the automated code-review round, and take one new finding into a skeleton branch and draft pull request. Use for the pipeline's scheduled run."
```

with:

```
description: "Caretake the delivery pipeline. Sweep its open pull requests, repair dead fires and straighten a stuck item's labels. Close an item whose sources all closed, and narrow one when only some did. Run the automated code-review round, and take one new finding into a skeleton branch and draft pull request. Use for the pipeline's scheduled run."
```

- [ ] **Step 3: The one pull request the Clerk closes**

Replace:

```
reads the police and the court, it comments, and it closes issues. **You never
close an issue.** It never touches a pull request. The two of you share a name
and nothing else.
```

with:

```
reads the police and the court, it comments, and it closes issues. **You never
close an issue.** It never touches a pull request. The two of you share a name
and nothing else. The one pull request you close is a stale item, under the
sweep's stale-item row.
```

- [ ] **Step 3b: The sweep lists by the law's three facts**

Replace:

```
List every open pull request whose head branch matches `pipeline/*` and whose
body carries `<!-- pipeline-work-fingerprint:`. Both facts, per the law. That
```

with:

```
List every open pull request whose head branch matches `pipeline/*`, whose
head repository is this one, and whose body carries
`<!-- pipeline-work-fingerprint:`. All three facts, per the law. That
```

- [ ] **Step 4: The sweep reads every source's state**

Replace `Read each one's labels, body and comments, **and its mergeability**.` with:

```
Read each one's labels, body and comments, **and its mergeability**. Read
the state of every issue its fingerprint's `sources=` names, with its state
reason.
```

- [ ] **Step 5: The conflict repair skips a stale item**

Replace:

```
fresh by the law's claim-freshness bound. Say so in the report. Skip it too
on an item carrying `pipeline/hold`, which is the owner's freeze. A stuck item
```

with:

```
fresh by the law's claim-freshness bound. Say so in the report. Skip it too
on an item carrying `pipeline/hold`, which is the owner's freeze. Skip it on
an item whose every source is closed: the stale-item row closes it, and a
merge into it is wasted. A stuck item
```

- [ ] **Step 6: Only a narrowing removes `ready-for-human`**

Replace:

```
already passed.** The label stays. No role removes it, and your merge
does not send the owner's item back into the machine.
```

with:

```
already passed.** The label stays. No role removes it but you, on a
narrowing, and your merge does not send the owner's item back into the
machine.
```

Replace:

```
draft.** No role removes the label, no other role ever flips a draft,
```

with:

```
draft.** No role removes the label outside your narrowing, no other role ever flips a draft,
```

- [ ] **Step 7: Rows 2 and 3 of the sweep table**

Find this row:

```
| `pipeline/hold` | nothing at all, one report line. It is the owner's freeze |
```

Insert these two rows directly below it:

```
| every source in the fingerprint's `sources=` closed | the stale item, below: one comment, then close the pull request unmerged |
| a source in `sources=` closed and missing from `narrowed=`, another source open, and no stage label beside a `state=held` claim the law's claim-freshness bound calls fresh | the narrowing, below: one comment, the route, then `narrowed=` |
```

- [ ] **Step 8: Describe the two rows**

Insert this text immediately before the paragraph that opens `**Straightening a stuck item.**`, followed by one blank line:

```
**The stale item.** Every source is closed, so the item has nothing left to
fix. The law's **When a source closes** says why it closes. A fire that
holds the item does not defer the close. Its work is moot once every source
is closed. The close claims nothing, so it takes the item from no fire. The
stage that fire hands to then exits, under the law's **A closed pull request
ends the fire**.

1. Re-read the pull request and its labels. Where it merged or closed since
   your listing, or now carries `pipeline/hold`, stop.
2. Post one comment that opens `Stale:` and names each source with its state
   reason. End it with
   `<!-- pipeline-stale: sources=#a,#b at=<UTC> -->`. Post it only where no
   comment of yours carries that marker.
3. Close the pull request unmerged, and read its state back.

The row sits above `pipeline/stuck` and `ready-for-human`, so it closes an
item under either.

**The narrowing.** A source closed while another stays open, and the closed
source's work leaves the item. Three writes, in this order:

1. Post one comment that opens `Narrowing:`. Name each closed source that
   is missing from `narrowed=` and that no `pipeline-narrowing` marker of
   yours lists in `sources=`, with its state reason. End it with
   `<!-- pipeline-narrowing: sources=#b at=<UTC> -->`. Where no such source
   is left, skip this write.
2. Route the item, but only while the narrowing waits on the target stage,
   as the law's **When a source closes** defines it. Where it no longer
   waits, the stage has done the work: go to step 3. The target is `spec/needs-work` while
   `.agents/specs/<N>-<slug>/` exists at the head, and `spec/approved` once
   the final slice has deleted it. Remove `pipeline/stuck`,
   `pipeline/code-review`, `ready-for-human` and every stage label but the
   target. Then re-enter the target by the law's primitive, and read the
   label set back.
3. Add to `narrowed=` each source a `pipeline-narrowing` marker of yours
   lists, and read the body back. This write is last on purpose.

Until step 3 lands, the row still matches. The next sweep posts no comment
for a source a marker already lists, and step 2's test decides whether the
route runs again. A finished
item therefore stays where it is. On a stuck item this row is the un-stick,
with the narrowing comment as its worklist. It never reaches an item
carrying `pipeline/hold`, because the `pipeline/hold` row sits above it.

The narrowing row waits while a stage holds a fresh claim, because a write
under a running fire races it. A route would re-enter a label the fire may still
hand on. A `narrowed=` write would compete with the fire's own body writes.

Neither source row counts against the repair limit below. That limit stops
a machine at fault, and a closed source is not one.
```

- [ ] **Step 10: The skeleton seeds `narrowed=none`**

Replace:

```
    <!-- pipeline-state: item=<pr number> review_rounds=0 gate_bounces=0 judge_rejects=0 slices=0 cr_rounds=0 -->
```

with:

```
    <!-- pipeline-state: item=<pr number> review_rounds=0 gate_bounces=0 judge_rejects=0 slices=0 cr_rounds=0 narrowed=none -->
```

- [ ] **Step 11: The report names both rows**

Find the line `   say that no worklist named work a stage can do.` in the report's item 2. Insert after it:

```
   **Stale and narrowed**: each item closed as stale, with every source and
   its state reason. Each narrowing, with every source it took out, the label
   set before and after, and `narrowed=` read back. Neither counts against
   the limit of three.
```

- [ ] **Step 12: The hard constraints**

Replace:

```
  carrying it. Remove `pipeline/stuck` only through the un-stick, only below
  its bound, and never on an item also carrying `pipeline/hold`.
```

with:

```
  carrying it. Remove `pipeline/stuck` only through the un-stick, only below
  its bound, or through a narrowing, and never on an item also carrying
  `pipeline/hold`.
```

Replace:

```
- Never remove `ready-for-human`, and never apply it to an issue.
```

with:

```
- Never remove `ready-for-human` outside a narrowing, and never apply it to
  an issue.
```

Find this bullet:

```
- Never merge a pull request — merging the base into an item branch to
  resolve a conflict is not that merge. Never put a pull request back into
  draft, whatever state it
  reaches and however a surface spells it.
```

Insert after it:

```
- Never close a pull request except a stale item, under the sweep's
  stale-item row.
```

- [ ] **Step 13: Verify**

Run:

```bash
f=.agents/skills/pipeline-clerk/SKILL.md
grep -c '^| every source in the fingerprint' $f
grep -c '^| a source in `sources=` closed and missing from `narrowed=`' $f
grep -c '^\*\*The stale item\.\*\*' $f
grep -c '^\*\*The narrowing\.\*\*' $f
grep -c 'cr_rounds=0 narrowed=none' $f
grep -c 'All three facts, per the law' $f
grep -n 'Both facts, per the law\|No role removes it\|No role removes the label,' $f
diff <(sed -n 3p $f) <(sed -n 3p .claude/agents/pipeline-clerk.md)
git diff --check
```

Expected: `1` six times, then nothing from the last three commands.

- [ ] **Step 14: Commit**

```bash
git add .agents/skills/pipeline-clerk/SKILL.md .claude/agents/pipeline-clerk.md
git commit -F - <<'EOF'
chore(agents): close a stale item and narrow a partly closed one

No role could close an item whose sources all closed, so it waited for a
person. An item with one source closed kept that source's work. Two sweep
rows, right after the owner's hold, carry the law's new section, so the
table stays the whole of the Clerk's authority over an item.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
```

---

### End of plan B

Run the checks the conventions file names for the end of a plan.
