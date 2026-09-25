# Plan: the howp manifest's declared homepage renders a bare file listing

## Steps

One slice. Both files change together, because the Layout line and the new
file are one fact: at no commit may the Layout line claim a README that does
not exist, or deny one that does.

1. Create `plugins/howp/README.md` with the content of the fenced block under
   `spec.md`, `## Proposed change`, from `# howp` to the line before the
   closing fence. Copy it as written. Do not reflow it and do not add a
   section. The file ends with a single newline.
2. In `README.md`, in the Layout block, change the one line that reads
   `  README.md                        every package but howp: what it does, what ships,`
   to
   `  README.md                        every package: what it does, what ships,`.
   Keep the two-space indent and the column. The continuation line below it,
   `what has and has not been verified`, stays as it is.
3. On the final slice, delete `.agents/specs/11-declared-homepage-file-listing/`,
   as the law requires.

## Verification

Each check is run at the branch head after step 2. The Implementer runs each
with what its own environment has.

- **The conformance check.** `tools/check-conformance.py` exits 0 and names
  `howp` among the plugins it checked. (Criterion 7.)
- **The file is the specification's text.** Extract the fenced block from
  `spec.md`, `## Proposed change`, and compare it byte for byte with
  `plugins/howp/README.md`. It must print no difference. Run this before
  step 3 deletes `spec.md`. (Criterion 1.)
- **The links are there.** A fixed-string search of `plugins/howp/README.md`
  finds `](../../README.md)`, `](../../README.md#installing)` and
  `](skills/howp/SKILL.md#what-has-been-verified-and-what-has-not)`. A search
  of `plugins/howp/skills/howp/SKILL.md` finds the line
  `## What has been verified, and what has not`. (Criteria 2 and 3.)
- **Nothing a release writes.** A case-insensitive search of
  `plugins/howp/README.md` for each of `aarch64`, `x86_64`, `darwin`,
  `linux-musl`, `0.3.`, `howp-v`, `sha256:`, `polymarket.com` and
  `manifold.markets` finds nothing. (Criterion 4.)
- **The link targets exist.** From `plugins/howp/`, each of
  `../../README.md`, `binaries.json`, `plugin.json`,
  `skills/howp/references/install.md` and `skills/howp/SKILL.md` is a file.
  (Criterion 5.)
- **The Layout line.** A search of `README.md` for `every package but howp`
  finds nothing, and one for
  `README.md                        every package: what it does, what ships,`
  finds exactly one line. (Criterion 6.)
- **The diff.** `git diff --name-status` against the merge base with `main`
  lists `A plugins/howp/README.md` and `M README.md`, plus the specification
  directory until step 3 deletes it. `git diff` on `README.md` shows one line
  removed and one added. (Criterion 8.)

**Only a live read can prove two things, and neither is verified here.**
First, that GitHub renders `plugins/howp/README.md` under the file listing at
the `homepage` URL once the change is on `main`. Second, that the anchor
`#what-has-been-verified-and-what-has-not` resolves on the rendered page. The
root README's existing link to the same anchor is the only evidence, and it is
not a check.

## Rollback

Revert the implementation commit. It adds one file and changes one line, and
nothing else depends on either.
