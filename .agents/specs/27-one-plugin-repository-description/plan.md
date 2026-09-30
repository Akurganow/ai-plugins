# Plan: `.gitattributes` says every program sits under `tools/`, and a package carries one outside it

## Steps

1. **`.gitattributes`, one slice.** Replace the head's lines 3-9 so that
   lines 1-12 of the file read exactly as the second fenced block of
   `spec.md`'s **Proposed change**. Change no other line. The file has 22
   lines afterwards, two more than the 20 it has at the head. Its lines 12
   onward are the head's lines 10 onward, unchanged.

   This is the whole implementation. The final slice also deletes
   `.agents/specs/27-one-plugin-repository-description/`, as the law
   prescribes.

## Verification

Run the repository's two programs, each with whatever the environment has.
`.agents/rules/conformance.md` owns what they need.

- `tools/regenerate.sh` must leave nothing to commit.
  `.gitattributes` is not a generated file, so a difference here means the edit
  touched something it should not have.
- `tools/check-conformance.py` must exit 0. It reads no `.gitattributes`, so
  this confirms only that nothing else moved.

Then, per acceptance criterion in `spec.md`:

1. `grep -c 'Its own programs sit under' .gitattributes` prints `1`.
2. `grep -cx '# below does not reach it.' .gitattributes` prints `1`.
3. `grep -c 'Its programs sit under' .gitattributes` prints `0`.
4. `grep -c 'linguist counts those files' .gitattributes` prints `0`.
5. `sed -n '1,12p' .gitattributes` is compared byte for byte with the second
   fenced block of `spec.md`'s **Proposed change**. Any difference fails.
6. `git diff origin/main -- .gitattributes` shows hunks only within lines 3-9
   of the old file. `sed -n '12,$p' .gitattributes` equals
   `git show origin/main:.gitattributes | sed -n '10,$p'`.
7. `git diff --name-only origin/main...HEAD`, on the final slice, lists
   `.gitattributes` and nothing else.
8. and 9. are the two program runs above.

Additionally, `git check-attr -a plugins/prose-discipline/hooks/print-rules.sh`
still prints no `linguist-vendored` line. The comment says the rule does not
reach that script, and the rule is unchanged, so this stays true.

A live run proves nothing more here. This item changes no install path and no
client-visible file.

## Rollback

Revert the one commit that edits `.gitattributes`. No other file changes.
