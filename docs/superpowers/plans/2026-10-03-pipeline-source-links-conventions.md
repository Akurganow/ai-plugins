# Pipeline source links: conventions for the three plans

Read this file before any plan. The design is
`docs/superpowers/specs/2026-10-03-pipeline-source-links-design.md`.

## Plans and their order

| Plan | Files |
| :-- | :-- |
| `2026-10-03-pipeline-source-links-a-tracker.md` | `.agents/skills/tracker-clerk/SKILL.md`, `.claude/agents/tracker-clerk.md`, `.agents/skills/github-needs/SKILL.md` |
| `2026-10-03-pipeline-source-links-b-law-clerk.md` | `.agents/skills/pipeline-law/SKILL.md`, `.agents/skills/pipeline-clerk/SKILL.md`, `.claude/agents/pipeline-clerk.md` |
| `2026-10-03-pipeline-source-links-c-stages.md` | `.agents/skills/spec-writer/SKILL.md`, `.agents/skills/spec-reviewer/SKILL.md`, `.agents/skills/implementer/SKILL.md` |

The three plans touch disjoint files. Run plan B before plan C, because the
stages cite the law section plan B adds. Plan A depends on neither. The
**Finish** section below runs last.

## Names every plan uses

- The law section plan B adds is `### When a source closes`. Every other
  file cites it as the law's **When a source closes**.
- The terms: "a stale item", "a narrowing", "a narrowing waits on" a stage,
  and "case 4" of the tracker Clerk.
- The Clerk's comments open with `Stale:` and `Narrowing:`.
- The markers, verbatim:

      <!-- pipeline-stale: sources=#a,#b at=<UTC> -->
      <!-- pipeline-narrowing: sources=#b at=<UTC> -->
      <!-- plugins-clerk: sha=<this run's commit> action=closed-unmerged -->

- The state field is `narrowed=<#b,#c|none>`, the last field of the
  `pipeline-state` line.
- A pull request is a pipeline item when its head branch matches
  `pipeline/*`, its head repository is this repository, and its body
  carries `<!-- pipeline-work-fingerprint:`. A fork's pull request has the
  fork as its head repository, so it never passes. Plan B states these three facts
  in the law's **Prove the item is one of ours**.
- A narrowing's target label is `spec/needs-work` while
  `.agents/specs/<N>-<slug>/` exists at the head. It is `spec/approved` once
  the final slice has deleted that directory.

## Writing rules

- Write in English.
- Follow the prose-discipline standard in every added line:
  - A sentence carries one thought in 25 words at most.
  - Write in the active voice.
  - Added prose carries no semicolon. A table keeps the style its file
    already uses.
  - Write no filler and no hedge.
- Match each file's voice. A role skill speaks to the role as "you". The law
  names sections by their bold heading and never by line number.
- Give every new rule a reason a reader can check. Never attribute a choice
  to the owner: no "the owner's decision", no "the owner ruled".
- Name no other repository. Name no issue or pull-request number of this
  repository in a skill, because a skill describes the machine and not
  today's items.
- Change only the text a task names. Leave neighbouring text as it stands,
  including its semicolons.
- Touch nothing under `plugins/`, and no file a release writes.

## Commits

One commit per task. The subject is `chore(agents): <what the change does>`
in lower case. A one-paragraph body says why. The last line is:

    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

## Checks

**After every task:**

- `git diff --check` prints nothing.
- Every grep the task names prints what the task says it prints.
- `git show --stat HEAD` lists only the task's files.

**At the end of every plan:**

- `bash tools/regenerate.sh` exits 0, and `git status --porcelain` then
  prints nothing.
- `tools/check-conformance.py` exits 0. Run it with `jsonschema==4.26.0`
  and `pyyaml==6.0.3` importable, the versions
  `.github/workflows/conformance.yml` pins.

## Finish

Run these after plans A, B and C, in order.

1. **Consistency review.** Give a clean-context reviewer the design and the
   nine changed files, and nothing else. Ask it to list every sentence where
   two files, or a file and the design, disagree. Each item quotes both
   sides with `path:line`. Verify each reported item against the files.
   Fix the confirmed ones, one commit per file.
2. **Cross-file greps.** Each prints nothing:

       git grep -n -i 'three cases\|three states\|three `closed-' .agents/skills/tracker-clerk
       git grep -n 'The sources stay closed\|no role ever removes it\|nobody; the owner alone' .agents
       git grep -n 'Run all eight checks\|Four wakings' .agents/skills

   Each pair of descriptions matches byte for byte:

       diff <(sed -n 3p .agents/skills/tracker-clerk/SKILL.md) <(sed -n 3p .claude/agents/tracker-clerk.md)
       diff <(sed -n 3p .agents/skills/pipeline-clerk/SKILL.md) <(sed -n 3p .claude/agents/pipeline-clerk.md)

3. **The durable record.** Add the section below to the end of
   `docs/design.md`. Commit it as
   `docs: record why pipeline items close no issue at merge`.

       ## Pipeline items close no issue at merge

       A pipeline item names its sources in its fingerprint, as
       `sources=#a,#b`. Its body carries no closing keyword such as
       `Closes #n`, so GitHub closes no issue when the item merges.

       The tracker Clerk closes each source instead, on its next run. It
       closes an issue only when every claim re-derives as gone at the
       head of `main`. A remainder no pull request can carry gets a note
       and stays open. A closing keyword would close the issue at the
       merge and skip both checks.

       The other direction belongs to the pipeline. The tracker Clerk
       closes the open sources of an item closed unmerged, as not planned.
       The pipeline Clerk closes an item whose sources all closed, and
       narrows one whose sources partly closed. The section "When a source
       closes" of `.agents/skills/pipeline-law/SKILL.md` holds those rules.

4. **Remove the temporary files.** Run `git rm -r docs/superpowers`. Commit
   it as `docs: remove the design and plans the skills now carry`.
5. **Verify.** Run the checks for the end of a plan once more.
   `git status --porcelain` prints nothing.
6. **The pull request.** Rewrite the body of the pull request in three
   sections. "What changed, and why" names each behaviour and the problem
   it removes. "Verification" gives each command with its result.
   "Only a live run can prove" lists the stale close, case 4, the
   narrowing and the cap count. End the body with the line
   `🤖 Generated with [Claude Code](https://claude.com/claude-code)`. Then
   mark the pull request ready for review. The owner merges.
