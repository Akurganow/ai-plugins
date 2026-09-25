# Spec: the howp manifest's declared homepage renders a bare file listing

## Work item

Pull request #56, built from issue #11. The item gives `plugins/howp/` the
`README.md` that every other package in `plugins/` already has, so the page
`howp`'s declared `homepage` opens says what the package is and links back to
the marketplace root.

## Problem

`howp`'s manifest points `homepage` at the package's own directory and
`repository` at the root, at the branch head `daf211a`,
`plugins/howp/plugin.json:10-11`:

    "homepage": "https://github.com/Akurganow/ai-plugins/tree/main/plugins/howp",
    "repository": "https://github.com/Akurganow/ai-plugins",

That directory holds no `README.md`. `git ls-tree daf211a plugins/howp/` lists
exactly four entries: `.claude-plugin`, `binaries.json`, `plugin.json`,
`skills`. Nothing under `plugins/howp/` links to the root `README.md`, which
is where the install sections and the verification pointer live.

Every other package in the tree has one. At the head,
`find plugins -iname 'readme*'` prints `plugins/prose-discipline/README.md`,
`plugins/toc-thinking/README.md` and `plugins/triz/README.md`; on `main` at
`232aaba` it also prints `plugins/design-review/README.md` and
`plugins/cognitive-load/README.md`. Each of those packages sets `homepage` to
its own directory the same way `howp` does. The root `README.md` records the
gap as the design, in its Layout block, `README.md:305` at the head
(`README.md:307` on `main`):

    README.md                        every package but howp: what it does, what ships,

The court's comment on #11 establishes why the gap is reader-facing. Agent
Plugins 1.0.0 §5.4 gives `homepage` as "Documentation or homepage URL"
(`spec/1.0.0.md` line 205 at `ff8ab5e`). Claude Code's documentation, read by
the court on 2026-09-10, shows the field "In plugin listings and details,
before and after install", and says "users see the `plugin.json` value" where
the marketplace entry sets none
([plugin-marketplaces.md](https://code.claude.com/docs/en/plugin-marketplaces.md)).
`howp`'s entry in `.claude-plugin/marketplace.json` is `name` and `source`
only.

**Where #11's evidence has aged.** Three parts, none of which moves the
finding:

- #11 says "There is no README anywhere under `plugins/`" and shows
  `find plugins -iname 'readme*'` printing nothing. At the head it prints the
  three paths above.
- #11 cites `README.md:260-264` for the catalogue table. At the head the
  table is `README.md:287-292`, and the `howp` row is `README.md:289`.
- #11's `## Suggested fix` block names the target `aarch64-apple-darwin` in
  its Limitations section and attributes it to the root README. The court
  found the root README carries no such string, and it still carries none at
  the head. That block cannot be applied as written, and this specification
  does not use it.

## The rule it serves

Nothing recorded requires a per-plugin README. Neither Agent Plugins 1.0.0 nor
the Agent Skills specification mentions one, and `tools/check-conformance.py`
exits 0 at the head. The item rests on a demonstrated inconsistency instead:
every other package carries a README at the directory its `homepage` names,
three at the head and five on `main`, and `howp` alone does not.

The new file is prose about a package and its released artifact, so every
sentence in it is held to `.agents/rules/claims.md`:

> **A claim about a released artifact is written so a release cannot silently
> falsify it**: it points at the machine-written record or at the artifact's
> own output, or it names the tag and date it was measured against.

> **Say what was not verified.** `README.md` opens the install section by
> saying nothing below has been installed from this repository as published.

## Proposed change

**One new file, `plugins/howp/README.md`**, with exactly this content:

````markdown
# howp

A personal probability dashboard. It turns what a person follows into
measurable questions, binds each question to a prediction market on
Polymarket or Manifold, records the probabilities over time, detects sharp
moves, and renders a local Markdown dashboard of what became more or less
likely.

Part of the [`ai-plugins` marketplace](../../README.md). Installing: the
per-client sections of the [root README](../../README.md#installing).

## What it does

One skill drives one binary, `hp`. `hp` does the deterministic work:
extracting a probability out of a venue's raw response, the append-only
history, move detection and the rendered page. It opens no socket and reads
no clock, so the agent fetches each market body with its own tools and
passes the moment in. Every judgement is the agent's, and no part of this
package invokes a model. No API keys and no accounts.

## What ships here

| Path | What it is |
| --- | --- |
| `plugin.json` | the manifest, Agent Plugins 1.0.0, at the plugin root |
| `binaries.json` | the released binary set: tag, targets, archives, download URLs and their sha256 digests. Written by the release job |
| `skills/howp/SKILL.md` | the skill, per the Agent Skills specification: the routine cycle and the rules around it |
| `skills/howp/references/install.md` | getting the binary: the platform gate, the preflight, the download, the digest check, the unpack |
| `skills/howp/references/interview.md` | the interests interview, and the two files the user owns |
| `skills/howp/references/procedures.md` | the three procedures that need judgement: binding a question to a market, explaining a sharp move, the weekly digest |
| `skills/howp/references/commands.md` | `hp --help` and every subcommand's, as the release records it |
| `README.md` | this file |
| `.claude-plugin/plugin.json` | a symlink to the root manifest, at the manifest path Claude Code documents. The root README cites the documentation |

The binary is not stored here. It is published on this repository's
[releases page](https://github.com/Akurganow/ai-plugins/releases), and
[`binaries.json`](binaries.json) is the record of which release and which
targets exist. No sentence in this file names either. The skill stops on any
platform that file does not name.

## Before you run it

- A platform [`binaries.json`](binaries.json) names.
- The hosts declared under `extensions` in [`plugin.json`](plugin.json),
  reachable over HTTPS. The declaration says there what it grants and what it
  does not.
- What the machine needs to download, verify and unpack the archive, and
  the preflight that checks the hosts, are in
  [`skills/howp/references/install.md`](skills/howp/references/install.md).

## What has been verified

**No client has installed this package from this repository as published.**
What has been downloaded, verified and run, with its date, the release it
was measured against, and what it did not exercise, is recorded once, in
the skill's own [What has been verified, and what has
not](skills/howp/SKILL.md#what-has-been-verified-and-what-has-not). This
file keeps no second copy of it.
````

Where each sentence comes from, all inside this repository at the head:

- The opening paragraph and `## What it does`: the `description` in
  `plugins/howp/plugin.json` and the `description` in
  `plugins/howp/skills/howp/SKILL.md`, reworded, adding nothing.
- The `## What ships here` rows: `find plugins/howp` at the head, and each
  reference's own first heading and the line in `SKILL.md` that points at it.
  The `.claude-plugin/plugin.json` row is the row `toc-thinking`'s and
  `prose-discipline`'s READMEs already carry, verbatim.
- "Written by the release job": `.agents/rules/conformance.md`, **Versions**.
- "The skill stops on any platform that file does not name":
  `SKILL.md`, **Before anything**, rule 1.
- The bold sentence under `## What has been verified`: `README.md:60`,
  "Nothing below has been installed from this repository as published", and
  `README.md:289`, "the package itself through no client". The paragraph after
  it is `README.md:30-34`, repointed from the root.

**No sentence names a release, a tag, a version, a target, a digest or a
host.** Each of those is a fact `binaries.json`, `plugin.json` or `SKILL.md`
holds and a release can move. The file points at the holder instead, so the
next release cannot falsify it.

**One line in the root `README.md` changes**, in the Layout block,
`README.md:305` at the head (`README.md:307` on `main`), so that it stops
naming `howp` as the exception. The two lines

    README.md                        every package but howp: what it does, what ships,
                                     what has and has not been verified

become

    README.md                        every package: what it does, what ships,
                                     what has and has not been verified

For `howp`, "what has and has not been verified" is the section that points
at `SKILL.md`. That is still where a reader learns it, one link away, and the
root README's own paragraph at `README.md:30-34` does the same.

**Alternatives rejected.**

- **Retarget `homepage` in `plugins/howp/plugin.json` at the root README.**
  Two reasons. Every other package's `homepage` names its own directory, so
  `howp` would become the one exception, and the Layout line would stay
  true. And `howp`'s `version` moves only at a release (`conformance.md`,
  **Versions**), while Claude Code pins a plugin to that string and "users
  only receive updates when it changes" (`README.md:329-333`, citing
  plugin-marketplaces). A manifest edit therefore reaches those readers at
  the next release and not before. A new README is read at the existing URL at
  once, with no manifest change.
- **Set `homepage` on the `howp` entry in `.claude-plugin/marketplace.json`.**
  That file's own `description` says it "holds pointers to those packages and
  nothing else", and `README.md:297-300` says the index carries "no plugin
  metadata of its own". A `homepage` there is plugin metadata. And the
  court's case for it rests on Claude Code's documentation alone.
- **Apply #11's `## Suggested fix` block.** It names `aarch64-apple-darwin`
  and attributes it to the root README, which does not carry the string.
  `claims.md` forbids that sentence.
- **Add a worked example with expected output.** #11 says such an example
  "should be taken from an actual run". `SKILL.md` records that no run has
  driven the cycle end to end. Nothing observed exists to take it from.

## Acceptance criteria

1. `plugins/howp/README.md` exists and is byte-identical to the fenced block
   under `## Proposed change`, from `# howp` to the last line before the
   closing fence.
2. `plugins/howp/README.md` contains `](../../README.md)` and
   `](../../README.md#installing)`.
3. `plugins/howp/README.md` contains
   `](skills/howp/SKILL.md#what-has-been-verified-and-what-has-not)`, and
   `plugins/howp/skills/howp/SKILL.md` has the heading
   `## What has been verified, and what has not`.
4. `plugins/howp/README.md` contains none of: `aarch64`, `x86_64`, `darwin`,
   `linux-musl`, `0.3.`, `howp-v`, `sha256:`, `polymarket.com`,
   `manifold.markets`. Checked case-insensitively.
5. Every relative link target in `plugins/howp/README.md` exists on disk,
   resolved from `plugins/howp/`: `../../README.md`, `binaries.json`,
   `plugin.json`, `skills/howp/references/install.md`,
   `skills/howp/SKILL.md`.
6. `README.md` no longer contains `every package but howp`, and does contain
   `README.md                        every package: what it does, what ships,`.
7. `tools/check-conformance.py` exits 0.
8. The diff against the base touches exactly `plugins/howp/README.md` (added)
   and `README.md` (one line changed), besides the specification's own
   directory, which the Implementer's final slice deletes.

## Out of scope

- `plugins/howp/plugin.json`, the whole file. Its `version` is a forbidden
  path, and `homepage` stays as it is (see the rejected alternative).
- `plugins/howp/binaries.json` and
  `plugins/howp/skills/howp/references/commands.md`, both forbidden paths.
  The README points at them and quotes neither.
- `.claude-plugin/marketplace.json`: no `homepage` is added to any entry.
- `plugins/howp/skills/howp/SKILL.md` and its other references. The README
  links into them and changes none of them.
- The `howp` row of the catalogue table, `README.md:289`. #11 names a link to
  `plugins/howp/` there as optional, the court did not assess it, and no
  other row links its package's README either.
- The dated `howp-v0.3.1` measurement in that same row. Whether a release has
  outrun it is a claims question about the root README, not about this file.
- The other five packages' READMEs.
- `tools/check-conformance.py`. Nothing in this change is a conformance rule,
  and no check is added to enforce that a package has a README.

## Risks

- **A sentence in the new README that reads as verified when it was not.**
  The bold sentence under `## What has been verified` carries that weight.
  Its tell is any sentence stating how a client or the binary behaves with no
  pointer beside it. Criterion 4 catches the kinds a release can move.
- **The file goes stale at the next release.** It cannot, because it names
  nothing the release writes. Criterion 4 is the tell if a later edit breaks
  that.
- **A broken relative link or anchor.** GitHub derives the anchor from the
  heading text. The root README already uses the same anchor at
  `README.md:33`. Criteria 3 and 5 check the files. Whether GitHub renders
  the anchor is checked only by opening the published page (see
  `plan.md`, `## Verification`).
- **`main` has moved since the branch was cut.** `232aaba` adds two packages
  and two rows to the root README's catalogue table, above the Layout line
  and not on it. The
  Layout line's text is identical on both sides, and `plugins/howp/README.md`
  does not exist on either. No conflict is expected. If one appears, the law's
  merge rule applies.
