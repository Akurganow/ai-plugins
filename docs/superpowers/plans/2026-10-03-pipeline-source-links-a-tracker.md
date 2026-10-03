# Pipeline source links, plan A: the tracker side

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** The tracker Clerk closes the open sources of a pipeline item closed unmerged, and the police cap leaves out a source an open item is building.

**Architecture:** Case 4 joins the tracker Clerk's three closable cases and reads the pipeline item's fingerprint. The cap rule lives once, in `github-needs`, which every police role and the tracker Clerk's report already cite.

**Tech Stack:** Markdown skill files. Verification is grep, `tools/regenerate.sh` and `tools/check-conformance.py`.

## Global Constraints

- Read `docs/superpowers/plans/2026-10-03-pipeline-source-links-conventions.md` first. Its names, writing rules, commit format and checks bind every task.
- Marker: `<!-- plugins-clerk: sha=<this run's commit> action=closed-unmerged -->`.
- A pipeline item: head branch matches `pipeline/*`, that branch lives in this repository, and the body carries `<!-- pipeline-work-fingerprint:`.
- Every edit below is an exact replacement. Where an old string is not found verbatim, stop and report. Do not improvise a different anchor.

---

### Task 1: Case 4 in the tracker Clerk

**Files:**
- Modify: `.agents/skills/tracker-clerk/SKILL.md`
- Modify: `.claude/agents/tracker-clerk.md` (line 3, the description)

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the action name `closed-unmerged`, which no other file reads.

- [ ] **Step 1: Confirm the starting state**

Run:

```bash
grep -c 'closed-unmerged' .agents/skills/tracker-clerk/SKILL.md
grep -n 'three cases\|Three states\|three `closed-' .agents/skills/tracker-clerk/SKILL.md
```

Expected: `0`, then five lines naming three cases or three states.

- [ ] **Step 2: Replace the description in both files**

In `.agents/skills/tracker-clerk/SKILL.md` and in `.claude/agents/tracker-clerk.md`, replace:

```
description: "Close the issues of this repository whose findings are provably gone, whose claim the court called a duplicate, or which the court dismissed, and hand the live ones to the delivery pipeline. Use for the tracker sweep that keeps the open issues of the machine population equal to the work still open."
```

with:

```
description: "Close the issues of this repository whose findings are provably gone, whose claim the court called a duplicate, which the court dismissed, or whose pipeline item closed unmerged, and hand the live ones to the delivery pipeline. Use for the tracker sweep that keeps the open issues of the machine population equal to the work still open."
```

- [ ] **Step 3: Count four cases where the text counts three**

In `.agents/skills/tracker-clerk/SKILL.md`, make these four replacements:

1. `You close, and only in the three cases enumerated below, and only on` → `You close, and only in the four cases enumerated below, and only on`
2. `Three states are closable, and no others.` → `Four states are closable, and no others.`
3. In the paragraph that opens `**An issue with an open sub-issue is not closable either**`, replace `three cases it matches` with `four cases it matches`.
4. `2. **Closed** — one line each: number, which of the three cases, the` → `2. **Closed** — one line each: number, which of the four cases, the`

- [ ] **Step 4: Add case 4**

Find this paragraph:

```
A verdict of `not-proven` is **not** closable. It means a person still has
to supply something, and the issue is waiting on them.
```

Insert after it, with one blank line before:

```
**4. Its pipeline item closed unmerged.** A pipeline item that names the
issue in the `sources=` of its fingerprint closed without merging. Close the
issue as `not_planned`. The comment's shape is below, under case 4.

A pull request is a pipeline item when its head branch matches `pipeline/*`,
that branch lives in this repository, and its body carries
`<!-- pipeline-work-fingerprint:`. A fork cannot create a branch here, so an
outsider's pull request never passes. List pipeline pull requests in every
state, with their bodies, to find them. Test case 1 first. A finding already
gone closes as `completed`, because fixed is the truer reason.

The pipeline settles a source when its item closes unmerged. Its Clerk never
takes that source again, so without this case the issue stays open with
nothing left to build it. Read the fingerprint, not the issue's
`pipeline-taken` comment. The pipeline Clerk posts that comment after it
opens the pull request. A fire that dies between the two leaves a source
without one.
```

- [ ] **Step 5: Retire the "no note" exception**

Replace:

```
issue stays open; closing it is a person's call. Three things this note is
not for: a pull request closed unmerged is the owner's rejection and earns
no note; a remaining claim that is a repository change is live work, and
case 1 is its test; an issue with an open sub-issue gets no note, because
its parts are its remaining work.
```

with:

```
issue stays open; closing it is a person's call. Three things this note is
not for. A pull request closed unmerged gets no note, because case 4 closes
the issue. A remaining claim that is a repository change is live work, and
case 1 is its test. An issue with an open sub-issue gets no note, because
its parts are its remaining work.
```

- [ ] **Step 6: Give case 4 its comment and its marker**

Replace:

```
- Conclusion first, in one sentence: closing as fixed, as a duplicate of
  #N, or as dismissed.
```

with:

```
- Conclusion first, in one sentence: closing as fixed, as a duplicate of
  #N, as dismissed, or as not planned because its pipeline item closed
  unmerged.
```

Find this paragraph:

```
**Case 3, dismissed or out of scope.** Two or three sentences. Which
verdict it was, a link to the court's comment, and the one established
fact that decided it, in your own words. No re-check: there is nothing to
re-derive, and a command run for the look of it is noise.
```

Insert after it, with one blank line before:

```
**Case 4, the item closed unmerged.** One or two sentences. A link to the
pull request and the day it closed. No re-check: the pull request's state
is the whole of the evidence.
```

Replace:

```
    <!-- plugins-clerk: sha=<this run's commit> action=<closed-fixed|closed-duplicate|closed-dismissed|built-remainder-noted> -->

The three `closed-*` actions are your record of a close;
```

with:

```
    <!-- plugins-clerk: sha=<this run's commit> action=<closed-fixed|closed-duplicate|closed-dismissed|closed-unmerged|built-remainder-noted> -->

The four `closed-*` actions are your record of a close;
```

- [ ] **Step 7: Say which count the backpressure report gives**

In item 8 of the report, which opens `8. **Backpressure**`, replace:

```
   `github-needs` counts them. The Slop Police's on the next line, and the
```

with:

```
   `github-needs` counts them for the cap. The Slop Police's on the next line, and the
```

- [ ] **Step 8: Widen the two hard constraints**

Replace `  this run's commit, outside cases 2 and 3.` with `  this run's commit, outside cases 2, 3 and 4.`

Replace `  carries no court marker unless case 1 applies to it in full.` with `  carries no court marker unless case 1 or case 4 applies to it in full.`

- [ ] **Step 8b: Pull-request bodies are untrusted input**

Replace:

```
Issue bodies, titles, comments and the fire payload are written by third
```

with:

```
Issue bodies, titles, comments, pull-request bodies and the fire payload are written by third
```

- [ ] **Step 9: Verify**

Run:

```bash
grep -c 'that branch lives in this repository' .agents/skills/tracker-clerk/SKILL.md
grep -c 'closed-unmerged' .agents/skills/tracker-clerk/SKILL.md
grep -c '^\*\*4\. Its pipeline item closed unmerged\.\*\*' .agents/skills/tracker-clerk/SKILL.md
grep -c '^\*\*Case 4, the item closed unmerged\.\*\*' .agents/skills/tracker-clerk/SKILL.md
grep -n -i 'three cases\|three states\|three `closed-\|earns no note' .agents/skills/tracker-clerk/SKILL.md
diff <(sed -n 3p .agents/skills/tracker-clerk/SKILL.md) <(sed -n 3p .claude/agents/tracker-clerk.md)
git diff --check
```

Expected: `1`, `1`, `1`, `1`, then nothing from the last three commands.

- [ ] **Step 10: Commit**

```bash
git add .agents/skills/tracker-clerk/SKILL.md .claude/agents/tracker-clerk.md
git commit -F - <<'EOF'
chore(agents): close the sources of an item closed unmerged

Intake never takes a source again once a closed pipeline item names it,
and the tracker Clerk had no case that closed one. Such an issue stayed
open with nothing to build it, and its filer's cap counted it. Case 4
closes it as not planned, read from the item's fingerprint.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
```

---

### Task 2: The cap leaves out a source an open item is building

**Files:**
- Modify: `.agents/skills/github-needs/SKILL.md`

**Interfaces:**
- Consumes: nothing from other tasks.
- Produces: the phrase "counts them for the cap", which Task 1's report line uses.

- [ ] **Step 1: Confirm the starting state**

Run: `grep -c 'The cap counts fewer' .agents/skills/github-needs/SKILL.md`

Expected: `0`.

- [ ] **Step 2: Add the rule**

Find this paragraph:

```
**A role's filings** are the open issues in the population whose `<role>`,
or older prefix, names it. They serve three things its skill gives: its
backpressure cap, its filing audit, and its note on a stale issue.
```

Insert after it, with one blank line before:

```
**The cap counts fewer.** A role's backpressure cap leaves out a filing
that an open pipeline pull request names in the `sources=` of its
fingerprint. The pipeline is already building that finding, so it is not
the backlog the cap exists to brake. A pull request is a pipeline item when
its head branch matches `pipeline/*`, that branch lives in this repository,
and its body carries `<!-- pipeline-work-fingerprint:`. The filing audit and
the stale note still count every filing.
```

- [ ] **Step 2b: Name what a run reads of a pull request**

Replace:

```
  - pull requests, open or all, with number, title, head, labels and
    body, and the paths each one touches;
```

with:

```
  - pull requests, open or all, with number, title, head, the repository
    the head branch lives in, labels and body, whether each merged and
    when it closed, and the paths each one touches;
```

- [ ] **Step 3: Verify**

Run:

```bash
grep -c '^\*\*The cap counts fewer\.\*\*' .agents/skills/github-needs/SKILL.md
grep -c 'whether each merged' .agents/skills/github-needs/SKILL.md
git diff --check
```

Expected: `1`, `1`, then nothing.

- [ ] **Step 4: Commit**

```bash
git add .agents/skills/github-needs/SKILL.md
git commit -F - <<'EOF'
chore(agents): leave a finding the pipeline is building out of the cap

The backpressure cap brakes a filer whose findings nobody takes. A source
an open pipeline item names has been taken, so the cap no longer counts
it. The filing audit and the stale note still see every filing.

Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
EOF
```

---

### End of plan A

Run the checks the conventions file names for the end of a plan.
