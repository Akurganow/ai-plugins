# Plan: each pipeline counter's number is stated once, in the law

## Steps

1. **Bring `main` in.** This branch's head, `704957d`, is 48 commits behind
   `main` (`281b817` when this plan was written), and every line `spec.md`
   cites is `main`'s. Merge `main` into the branch, as the law's
   **The branch never stops being mergeable** says: merge, never rebase.
   No conflict is expected, because the branch changes only
   `.agents/specs/33-bound-numbers-one-place/`. Re-read the five files'
   cited lines after the merge. If one moved, find it by its quoted text,
   not by its number.
2. **The law.** In `.agents/skills/pipeline-law/SKILL.md`, rewrite the
   `slices` paragraph and add the bold line, the five-row table and the
   closing sentence, exactly as `spec.md` § 1 gives them.
3. **The Spec Writer and the Spec Reviewer.** Make the three replacements in
   `.agents/skills/spec-writer/SKILL.md` and
   `.agents/skills/spec-reviewer/SKILL.md` that § 2 and § 3 give.
4. **The Implementer.** Make the twelve replacements in
   `.agents/skills/implementer/SKILL.md` that § 4 gives.
5. **The Clerk.** Make the three replacements in
   `.agents/skills/pipeline-clerk/SKILL.md` that § 5 gives.

Each of steps 2 to 5 leaves the tree consistent on its own. A role that still
states a number before its own step lands is in the state `main` is in today.
Steps 2 and 3 may go in one slice, and steps 4 and 5 in another.

## Verification

After every slice:

- `tools/regenerate.sh` leaves nothing to commit.
- `tools/check-conformance.py` exits 0.
- The `selftest` and the `validate` subcommand of `tools/evals.py` pass.

None of these reads `.agents/skills/`, so they show that nothing else broke,
not that this change is right. The checks below are what prove the change.

After the last of steps 2 to 5, per acceptance criterion:

1. The `git grep -nE` pattern of criterion 1, run over `.agents/skills/`,
   prints nothing. Before the change it prints 20 lines at `281b817`. Quote
   both outputs.
2. Read `### How every bound behaves` in
   `.agents/skills/pipeline-law/SKILL.md`. Quote the bold line and the table.
   Check the five rows and their order against `spec.md`.
3. `grep -c 'three the Implementer stops' .agents/skills/pipeline-law/SKILL.md`
   prints 0. Compare each of the 20 lines from check 1 with its replacement
   in `spec.md` §§ 1–5. Quote the diff hunks.
4. `grep -c 'How every bound behaves'` on each of the four role files prints
   1 or more.
5. `git diff origin/main -- .agents/skills/agent-police/SKILL.md` prints
   nothing.
6. to 8. The three checks above, after the last slice.
9. `git diff --name-only origin/main...HEAD` lists only the five files, plus
   `.agents/specs/33-bound-numbers-one-place/` until the final slice
   deletes it.

Whether a live fire follows the new wording the way it followed the numbers
can only be proved by a live run of each stage. This plan does not claim that
as verified.

## Rollback

One `git revert` of the implementation commits puts every number back in the
role that stated it. Nothing outside `.agents/skills/` changes, so nothing
else needs undoing.
