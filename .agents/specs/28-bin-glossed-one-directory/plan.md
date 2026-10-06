# Plan: procedures.md glosses $BIN one directory above where install.md sets it

## Steps

1. In `plugins/howp/skills/forecast/references/procedures.md`, replace lines
   40-41 with the two new lines given in `spec.md` under
   `## Proposed change`, leaving line 39 and every other line as it is.
   This is one slice, and it completes the item.

## Verification

- `tools/check-conformance.py` exits 0.
- `tools/regenerate.sh` leaves nothing to commit: `git status --porcelain`
  is empty after it runs.
- Criterion 1: a search of `procedures.md` for
  `the directory the archive unpacked into` finds nothing.
- Criterion 2: lines 39-41 of `procedures.md`, read at the head, equal the
  fenced block in `spec.md` byte for byte.
- Criterion 3: `git diff --numstat origin/main...HEAD -- plugins/` prints
  one line, `2	2	plugins/howp/skills/forecast/references/procedures.md`.
- Criterion 4: the count of lines containing `"$BIN/hp"` in
  `procedures.md` is 19 at the head and 19 at `origin/main`.
- Criterion 5: `git diff origin/main...HEAD --` on `install.md`, `SKILL.md`
  and `binaries.json` prints nothing.

Whether an agent following `procedures.md` now resolves `"$BIN/hp"` to the
installed binary can only be proved by a live run against a released
archive, and nothing here claims that run happened.

## Rollback

Revert the one commit that changes `procedures.md`.
