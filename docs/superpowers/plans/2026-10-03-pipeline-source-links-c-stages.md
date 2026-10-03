# Pipeline source links, plan C: the three stages

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Every stage exits on a closed pull request. The Writer and the Implementer carry out a narrowing, and the Reviewer checks it in every round.

**Architecture:** The law's **When a source closes**, written by plan B, defines when a narrowing waits on a stage. Each stage cites that definition and adds only its own work: the Writer edits the specification, the Reviewer checks it, and the Implementer removes the work once the specification is gone.

**Tech Stack:** Markdown skill files. Verification is grep, `tools/regenerate.sh` and `tools/check-conformance.py`.

## Global Constraints

- Read `docs/superpowers/plans/2026-10-03-pipeline-source-links-conventions.md` first. Its names, writing rules, commit format and checks bind every task.
- Plan B is merged into the branch first. `grep -c '^### When a source closes$' .agents/skills/pipeline-law/SKILL.md` prints `1`.
- Marker: `<!-- pipeline-narrowing: sources=#b at=<UTC> -->`. State field: `narrowed=<#b,#c|none>`.
- Every edit below is an exact replacement. Where an old string is not found verbatim, stop and report. Do not improvise a different anchor.

---

### Task 1: The Spec Writer

**Files:**
- Modify: `.agents/skills/spec-writer/SKILL.md`

**Interfaces:**
- Consumes: from plan B, the law's **When a source closes** and the field `narrowed=`.
- Produces: the section heading `## Does a narrowing wait on you?`, which only this file reads.

- [ ] **Step 1: Confirm the starting state**

Run:

```bash
grep -c 'narrowing' .agents/skills/spec-writer/SKILL.md
grep -c '^Four wakings\.' .agents/skills/spec-writer/SKILL.md
```

Expected: `0`, then `1`.

- [ ] **Step 2: Three facts, and exit on a closed pull request**

Replace:

```
2. Prove the item is yours by the law's two positive facts.
```

with:

```
2. Prove the item is yours by the law's three positive facts.
```

Replace:

```
4. Exit if it carries `pipeline/stuck` or `pipeline/hold`.
```

with:

```
4. Exit if the pull request is closed, under the law's **A closed pull
   request ends the fire**, or if it carries `pipeline/stuck` or
   `pipeline/hold`.
```

Then replace:

```
Clerk tries to straighten a stuck item on its own run, and you report it and
stop. Everything else
```

with:

```
Clerk tries to straighten a stuck item on its own run, and you report it and
stop. A pull request that closes mid-fire ends the fire the same way, before
any further write to it. Everything else
```

- [ ] **Step 3: The narrowing test comes first**

Insert this section immediately before the line `## Have you already written this?`, followed by one blank line:

```
## Does a narrowing wait on you?

Test this first. A narrowing waits on you as the law's **When a source
closes** defines it. Where you have a marker, the spec hash has not moved
since it, so the test below would read this waking as a re-fire and only
route.

For each source a waiting narrowing's marker lists, where the fingerprint's
`sources=` names it and it is closed now:

- Take it out of `## Problem`, `## Proposed change` and `## Acceptance
  criteria`.
- Add one line to `## Out of scope` naming it and the state reason its
  issue shows.
- Take out of `## Steps` and `## Verification` every step and check that
  serves only that source.
- Where the branch already carries work that serves only that source, add a
  step to `## Steps` that removes the work.

A narrowing that arrives with `R-*` or `G-*` objections is one revision that
answers both. The revision routes to `spec/awaiting-review`, because the
Reviewer has not read the narrowed content.

Where the specification already carries every edit above, a fire died
before its marker. Write your completion marker and route as a revision
would. Where the open sources leave nothing to change, **When the item has
nothing left to change** applies. That stop writes no completion marker,
because it writes no revision.

A fresh fill leaves out every source in `narrowed=` the same way.
```

Then replace:

```
Read your own `pipeline-done role=spec-writer` line before anything else.
```

with:

```
Skip this section while a narrowing waits on you. The section above writes
that revision. Otherwise read your own `pipeline-done role=spec-writer` line
next.
```

And replace:

```
This test comes first because it is the only one that distinguishes a
re-fire of finished work from fresh work.
```

with:

```
This test comes right after the narrowing test. Outside a narrowing, it is
the only one that distinguishes a re-fire of finished work from fresh work.
```

- [ ] **Step 4: The wakings and the routing table**

Replace `Four wakings. Tell them apart from what the item holds.` with `Five wakings. Tell them apart from what the item holds.`

Find this row:

```
| A revision after a gate bounce | a `gate` marker with `outcome=rejected`, and a comment carrying numbered `G-*` objections |
```

Insert this row directly below it:

```
| A narrowing | a `pipeline-narrowing` comment created after your newest `pipeline-done` marker, or with none yet. It combines with any other waking |
```

Find this row:

```
| a revision after a gate bounce, without a narrowing | `spec/needs-work` | `spec/approved` |
```

Insert this row directly below it:

```
| a narrowing, with or without objections | `spec/needs-work` | `spec/awaiting-review` |
```

- [ ] **Step 5: The report names a narrowed source**

Replace:

```
3. **Sources**: each one, whether its quoted evidence still held at the
   head, and what changed in the specification because it did not.
```

with:

```
3. **Sources**: each one, whether its quoted evidence still held at the
   head, and what changed in the specification because it did not. Each
   source a narrowing took out, with its state reason.
```

- [ ] **Step 6: Verify**

Run:

```bash
f=.agents/skills/spec-writer/SKILL.md
grep -c '^## Does a narrowing wait on you?$' $f
grep -c '^4\. Exit if the pull request is closed' $f
grep -c "law's three positive facts" $f
grep -c '^Five wakings\.' $f
grep -c '^| a narrowing, with or without objections |' $f
grep -n 'line before anything else\.$\|^This test comes first' $f
git diff --check
```

Expected: `1` five times, then nothing from the last two commands.

- [ ] **Step 7: Commit**

```bash
git add .agents/skills/spec-writer/SKILL.md
git commit -F - <<'EOF'
chore(agents): the Writer carries out a narrowing before its re-fire test

A narrowing leaves the spec hash where it was, so the re-fire test would
read it as finished work and only route. The Writer now tests for a
waiting narrowing first, takes the closed source out of the specification
and plans the removal of its work. A closed pull request ends the fire.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
```

---

### Task 2: The Spec Reviewer

**Files:**
- Modify: `.agents/skills/spec-reviewer/SKILL.md`

**Interfaces:**
- Consumes: from plan B, the law's **When a source closes** and the narrowing marker.
- Produces: check 9, which only this file reads.

- [ ] **Step 1: Confirm the starting state**

Run: `grep -c 'Run all eight checks' .agents/skills/spec-reviewer/SKILL.md`

Expected: `1`.

- [ ] **Step 2: Three facts, and exit on a closed pull request**

Replace:

```
2. Prove the item is yours by the law's two positive facts.
```

with:

```
2. Prove the item is yours by the law's three positive facts.
```

Replace:

```
4. Exit if it carries `pipeline/stuck` or `pipeline/hold`.
```

with:

```
4. Exit if the pull request is closed, under the law's **A closed pull
   request ends the fire**, or if it carries `pipeline/stuck` or
   `pipeline/hold`.
```

Then replace:

```
Clerk tries to straighten a stuck item on its own run, and you report it and
stop. Everything else
```

with:

```
Clerk tries to straighten a stuck item on its own run, and you report it and
stop. A pull request that closes mid-fire ends the fire the same way, before
any further write to it. Everything else
```

- [ ] **Step 3: Read the narrowing comments**

Replace:

```
- the pull-request body and the sources it names
- the sibling issues, where the body carries `## Part of`
```

with:

```
- the pull-request body and the sources it names
- the Clerk's narrowing comments, each ending `<!-- pipeline-narrowing:`
- the sibling issues, where the body carries `## Part of`
```

- [ ] **Step 4: Check 9**

Replace `**Run all eight checks.**` with `**Run all nine checks.**`

Find these lines, the end of check 8:

```
   and neither document may change what one claims. Quote the brief in the
   objection.
```

Insert after them, with one blank line before:

```
9. **The narrowing is carried out.** Take each source a narrowing marker
   lists, where the fingerprint's `sources=` names it and it is closed now. It appears nowhere
   in `## Proposed change` or `## Acceptance criteria`, and `## Out of scope`
   names it. Where the branch already carries work that serves only that
   source, a step in `## Steps` removes the work. A miss is an objection,
   because the narrowing is a decision the machine has recorded.
```

- [ ] **Step 5: Verify**

Run:

```bash
f=.agents/skills/spec-reviewer/SKILL.md
grep -c '^9\. \*\*The narrowing is carried out\.\*\*' $f
grep -c 'Run all nine checks' $f
grep -c "the Clerk's narrowing comments, each ending" $f
grep -c '^4\. Exit if the pull request is closed' $f
grep -c "law's three positive facts" $f
grep -n 'Run all eight checks' $f
git diff --check
```

Expected: `1` five times, then nothing from the last two commands.

- [ ] **Step 6: Commit**

```bash
git add .agents/skills/spec-reviewer/SKILL.md
git commit -F - <<'EOF'
chore(agents): the Reviewer checks a narrowing in every round

A specification that keeps a narrowed source, or keeps its work, would
build what a closed issue no longer asks for. The Reviewer reads the
Clerk's narrowing comments and objects to a narrowing left undone. A
closed pull request ends the fire.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
```

---

### Task 3: The Implementer

**Files:**
- Modify: `.agents/skills/implementer/SKILL.md`

**Interfaces:**
- Consumes: from plan B, the law's **When a source closes**, the narrowing marker and the field `narrowed=`.
- Produces: nothing other files read.

- [ ] **Step 1: Confirm the starting state**

Run:

```bash
grep -c 'narrowing' .agents/skills/implementer/SKILL.md
grep -c '^Four wakings look alike' .agents/skills/implementer/SKILL.md
```

Expected: `0`, then `1`.

- [ ] **Step 2: Three facts, and exit on a closed pull request**

Replace:

```
2. Prove the item is yours by the law's two positive facts.
```

with:

```
2. Prove the item is yours by the law's three positive facts.
```

Replace:

```
4. Exit if it carries `pipeline/stuck` or `pipeline/hold`.
```

with:

```
4. Exit if the pull request is closed, under the law's **A closed pull
   request ends the fire**, or if it carries `pipeline/stuck` or
   `pipeline/hold`.
```

Then replace:

```
Clerk tries to straighten a stuck item on its own run, and you report it and
stop. Everything else
```

with:

```
Clerk tries to straighten a stuck item on its own run, and you report it and
stop. A pull request that closes mid-fire ends the fire the same way, before
any further write to it. Everything else
```

- [ ] **Step 3: A narrowing is one more kind of return**

Replace `Four wakings look alike and are not.` with `Five wakings look alike and are not.`

Find this row:

```
| A return from the owner | `ready-for-human` is gone and `spec/approved` is back, with his review comments |
```

Insert this row directly below it:

```
| A narrowing | no `$SPEC_DIR` at the head, and a narrowing waits on you, as the law's **When a source closes** defines it |
```

Find this paragraph:

```
The first and the last are told apart by that line alone. A verdict marker
appears only on an accepted final slice, so it cannot separate them.
```

Insert after it, with one blank line before:

```
Test the narrowing row before the two returns and the re-entry, because its
evidence overlaps theirs. A narrowing is one more kind of return. It
combines with whichever other return holds, and one fire works them all.
```

Replace:

```
On a return from the code review or from the owner, the specification is
already deleted.
```

with:

```
On a return from the code review, from the owner or from a narrowing, the
specification is already deleted.
```

- [ ] **Step 4: The worklist removes the narrowed work**

Replace:

```
1. Read the item's reviews and review comments, on every waking.
2. Work the judge's `must_change` list from a rejected verdict.
3. Work the remaining plan steps.
```

with:

```
1. Read the item's reviews and review comments, on every waking.
2. Work the judge's `must_change` list from a rejected verdict.
3. With no `$SPEC_DIR` at the head, remove the work that serves only a
   source a waiting narrowing's marker lists, where the fingerprint's
   `sources=` names it and it is closed now. While the specification exists, its plan carries that
   removal. Where nothing serves only that source, the tree does not move:
   rewrite your `role=implementer` marker with a new `at=`, keeping its
   tree and outcome, so the narrowing stops waiting on you.
4. Work the remaining plan steps.
```

- [ ] **Step 5: The trio judges the narrowed task**

Replace:

```
Each brief is neutral: the diff, the spec, the plan, the commands you ran and
their output.
```

with:

```
Each brief is neutral: the diff, the spec, the plan, every narrowing comment
on the item, and the commands you ran and their output. The work it judges
excludes every source a narrowing marker lists.
```

Replace:

```
- **Judge.** Read the diff, the spec, and both reports, and nothing else.
```

with:

```
- **Judge.** Read the diff, the spec, the narrowing comments and both
  reports, and nothing else.
```

- [ ] **Step 6: The handoff body names each narrowed source**

Replace:

```
       ## Links
       - sources: #<a>, #<b>
```

with:

```
       ## Links
       - sources: #<a>, #<b>
       - narrowed: #<b>, closed as <its state reason>
```

Find this paragraph:

```
   Keep the whole state block at the foot, the `pipeline-work-fingerprint`
   line included. It is the item's identity. Its `sources=` stops the pipeline
   Clerk taking the source issues again, at intake step 5.
```

Insert before it, followed by one blank line:

```
   Write one `narrowed:` line per source in `narrowed=`, and none where it
   reads `none`.
```

- [ ] **Step 7: The report counts five wakings**

Replace `which of the four wakings this was and its evidence` with `which of the five wakings this was and its evidence`.

- [ ] **Step 8: Verify**

Run:

```bash
f=.agents/skills/implementer/SKILL.md
grep -c '^| A narrowing | no `\$SPEC_DIR` at the head' $f
grep -c '^Five wakings look alike' $f
grep -c '^Test the narrowing row before the two returns' $f
grep -c '^4\. Exit if the pull request is closed' $f
grep -c "law's three positive facts" $f
grep -c 'narrowed: #<b>, closed as <its state reason>' $f
grep -n 'Four wakings\|four wakings' $f
git diff --check
```

Expected: `1` six times, then nothing from the last two commands.

- [ ] **Step 9: Commit**

```bash
git add .agents/skills/implementer/SKILL.md
git commit -F - <<'EOF'
chore(agents): the Implementer removes a narrowed source's work

Once the final slice has deleted the specification, a narrowing reaches
the Implementer directly. It is one more kind of return, tested first
because its evidence overlaps the others. The trio judges the narrowed
task, and the handoff body names each narrowed source. A closed pull
request ends the fire.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
```

---

### End of plan C

Run the checks the conventions file names for the end of a plan. Then go to **Finish** in the conventions file.
