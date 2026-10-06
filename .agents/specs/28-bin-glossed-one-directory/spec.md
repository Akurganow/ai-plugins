# Spec: procedures.md glosses $BIN one directory above where install.md sets it

## Work item

Pull request #70, branch `pipeline/28-bin-glossed-one-directory`, built from
issue #28. The item corrects one sentence in
`plugins/howp/skills/forecast/references/procedures.md` that defines `$BIN`
as a directory one level above the one the file it cites assigns to `$BIN`.
The brief is the pull-request body.

## Problem

Re-read at `5e92a5f` (this branch's head; its parent is `c0cf300`, the tip
of `main`), `plugins/howp/skills/forecast/references/procedures.md:39-41`
reads:

> `$W` is the workspace, as the `forecast` skill's `SKILL.md` sets it, and
> `$BIN` the directory the archive unpacked into, as `install.md` Step 2 sets
> it.

The file that sentence cites says otherwise.
`plugins/howp/skills/forecast/references/install.md:57-58` gives the phrase
to a different directory:

> | `target.root` | the directory the archive unpacks into |
> | `target.bin_dir` | the directory inside it holding the binaries |

and `install.md` Step 2 (heading at `install.md:132`) assigns `$BIN` one
level below it, at `install.md:137`:

    BIN="$DEST/<root>/<bin_dir>"          # target.root / target.bin_dir

`plugins/howp/skills/forecast/SKILL.md:82-83` agrees with `install.md`:

> The copy caches at `${HOWP_CACHE:-$HOME/.cache/howp}/<version>`. `$BIN`
> below is `$DEST/<root>/<bin_dir>`, and `install.md` sets both.

So in this package's own vocabulary "the directory the archive unpacked
into" is `$DEST/<root>`, and `$BIN` is `$DEST/<root>/<bin_dir>`. The two are
different directories: `plugins/howp/binaries.json:13` and `:26` both carry
`"bin_dir": "bin"`. The gloss governs every landing command in
`procedures.md`: `"$BIN/hp"` appears on 19 of its lines, the first at
`procedures.md:117`. Read under line 40, each of them points one directory
above the binary. `procedures.md:40` is the only line in the package that
uses the phrase for `$BIN`. `grep -rn 'archive unpack' plugins/ README.md`
returns `procedures.md:40` and `install.md:57`, and nothing else.

**The source's quoted evidence has moved, and its substance still holds.**
Issue #28 quoted the sentence at `51da31f`, under a path that no longer
exists:

> `plugins/howp/skills/howp/references/procedures.md:14-15`:
> `$W` is the workspace and `$BIN` the directory the archive unpacked into, as
> `SKILL.md` sets them.

At the head it is the three lines quoted at the top of this section, at
`plugins/howp/skills/forecast/references/procedures.md:39-41`. Issue #28's
comment of 2026-10-01 recorded the move. The skill directory was renamed to
`forecast/`, and the citation changed from "as `SKILL.md` sets them" to
"as `install.md` Step 2 sets it". The phrase "the directory the archive
unpacked into" is byte-identical in both, and it still contradicts the file
cited beside it. The issue's line numbers for `install.md` (43, 118) and
`SKILL.md` (57-58) are stale too. The numbers given above are the ones at
the head. Nothing in the proposed change depends on the old numbers.

## The rule it serves

`.agents/rules/slop.md`, under **The kinds**:

> 2. **`lying`** — text that contradicts this repository: a README sentence
>    the check does not do, a step name the step does not perform, a
>    `description` the skill does not keep, a count the tree does not have, a
>    comment for a check that was deleted.

The sentence contradicts `install.md` Step 2, the file it names as its own
authority, and `SKILL.md:82-83`. The court sustained #28 under that kind.

## Proposed change

One file changes: `plugins/howp/skills/forecast/references/procedures.md`.
Lines 39-41 become, exactly:

```text
`$W` is the workspace, as the `forecast` skill's `SKILL.md` sets it, and
`$BIN` the directory inside the unpacked archive that holds the binaries, as
`install.md` Step 2 sets it.
```

As a diff:

```diff
 `$W` is the workspace, as the `forecast` skill's `SKILL.md` sets it, and
-`$BIN` the directory the archive unpacked into, as `install.md` Step 2 sets
-it.
+`$BIN` the directory inside the unpacked archive that holds the binaries, as
+`install.md` Step 2 sets it.
```

The new wording is `install.md:58`'s gloss of `target.bin_dir`, "the
directory inside it holding the binaries", with its antecedent "it" spelled
out as the unpacked archive. It makes no new claim. Every name in it is
already used by `install.md`, and the citation to `install.md` Step 2 stays.
No other line of `procedures.md` changes. The 19 `"$BIN/hp"` lines are
right once the gloss is, so they stay as they are.

Rejected alternatives:

- **Spell `$BIN` out as `$DEST/<root>/<bin_dir>`**, the fuller repair #28
  offered. `procedures.md` never defines `$DEST`, so this would put an
  undefined variable into a third file. `install.md` defines it and
  `SKILL.md` defers to `install.md` for it. The court's comment on #28 names
  the shorter wording as the repair that "avoids naming `$DEST` in a third
  file and leaves the deferral chain as it is".
- **Drop the gloss and keep only the citation** ("`$BIN` as `install.md`
  Step 2 sets it"). This also removes the false statement, but the reader of
  `procedures.md` then has to open `install.md` to learn what `$BIN` names.
  The finding is about a wrong gloss, not about having one.
- **Change `install.md` or `SKILL.md` to match `procedures.md`.** These two
  files and the runnable assignment at `install.md:137` are correct, and the
  binaries sit under `bin_dir`, per `binaries.json`. The one wrong sentence
  is what bends.

## Acceptance criteria

1. `plugins/howp/skills/forecast/references/procedures.md` no longer
   contains the string `the directory the archive unpacked into`.
2. The same file contains, as consecutive lines, the three lines in the
   fenced block under `## Proposed change`.
3. `git diff --numstat origin/main...HEAD -- plugins/` lists exactly one
   file, `plugins/howp/skills/forecast/references/procedures.md`, with
   `2	2`.
4. `grep -c '"$BIN/hp"'` on that file prints `19`, the same count as at
   `c0cf300`.
5. `plugins/howp/skills/forecast/references/install.md`,
   `plugins/howp/skills/forecast/SKILL.md` and `plugins/howp/binaries.json`
   are byte-identical to `origin/main`.
6. `tools/check-conformance.py` exits 0.
7. `tools/regenerate.sh` leaves nothing to commit.

## Out of scope

- `plugins/howp/binaries.json`. It is a forbidden path, written by the
  release job, and it is read here only as evidence of `bin_dir`.
- `plugins/howp/skills/forecast/references/commands.md` and the `version`
  field of `plugins/howp/plugin.json` and its `.claude-plugin/plugin.json`
  copy. These are forbidden paths, written by the release job, and not
  touched or judged.
- The `$DEST` deferral chain (`procedures.md` defers to `install.md`, and
  `SKILL.md` defers to `install.md`). #28 lists it as not addressed. It is a
  choice about where a definition lives, not a false statement.
- `install.md`'s use of "the manifest" for `binaries.json`, listed by #28
  under "Not addressed" and dropped there.
- Every other sentence of `procedures.md`, including the `$W` half of the
  same sentence, which is correct and stays word for word.
- `tools/check-conformance.py`. It never opens a `references/*.md` body, and
  this item adds no check.

## Risks

- **The replacement is wrong in a new way.** The tell is a disagreement
  between the new line 40 and `install.md:58` or `install.md:137`.
  Criterion 2 fixes the wording, and the Reviewer can read it against both
  lines.
- **The edit reaches further than the sentence.** The tell is any other line
  of `plugins/` in the diff, or a changed `"$BIN/hp"` count. Criteria 3 and
  4 catch both.
- **A claim that reads as verified when it was not.** The new sentence makes
  no claim about a client, an install command or a released artifact. It
  restates a definition from `install.md`, which is cited beside it.

