# Quality review of the ai-plugins marketplace

Date 2026-09-24. Revision `232aaba` (main). Findings against a rubric drawn from five
clean-room research files (`../research/01`–`05`). The artifact version of this report
was published at https://claude.ai/artifact/X2aMTizAQEs1hCtg8jk5TY (private to the owner).

## Method

1. Before any research, only the root `README.md` was read. There is no `docs/` folder.
2. Five independent agents with no repository access wrote the research files.
3. A 17-criterion rubric (R1–R17) was assembled from their rubrics; only then was the
   repository opened.
4. Mechanical checks: `tools/check-conformance.py` (exit 0); `claude plugin validate`
   2.1.281 on the marketplace and each plugin; counts of description length, sentence
   length, reference links, tables of contents.

Research limits: most vendor sites were blocked by the proxy; pages were read from GitHub
repositories at `main`; commits pinned where the API allowed. Not read: Anthropic's skills
PDF, nngroup, arxiv, Cursor docs, JetBrains listing pages. Hermes, Codex and Oh-My-Pi
were not installed in the container.

## Rubric (R1–R17)

| # | Criterion | Source |
| :-- | :-- | :-- |
| R1 | Root `plugin.json` regular file, exact `$schema`, ten fields, `name` = folder = catalogue entry | 01 #1–4, 8; 04 #1, 4 |
| R2 | `description` short (one line, ≤120–250 chars); long text in README | 03 §11, C2; 05 A2; 04 #5 |
| R3 | SemVer `version`, bumped on every change, changes in `CHANGELOG.md` | 02 #19–20; 03 D1–D4 |
| R4 | `license` SPDX and a LICENSE file in the package | 03 B2; 02 #22; 04 #8 |
| R5 | README per package: what, install, first safe prompt, prerequisites, reads/writes/network, failure behaviour | 02 #21; 04 #23; 03 C2–C4 |
| R6 | Catalogue entry carries `description`, `category`, `homepage` | 02 #10; 04 #16 |
| R7 | Catalogue: `owner`, user-facing description, unique names, `./` sources | 02 #3–7; 04 #11–13 |
| R8 | Skill front matter: six fields, `name` = folder, `description` ≤1024 "what + when", one voice | 01 #13–17; 04 #18–19 |
| R9 | SKILL.md body < 500 lines; every reference named by path with a "read when" | 01 #20–21; 05 #30; 04 #21 |
| R10 | Reference files > 100 lines start with a TOC | 01 #22; 05 #31 |
| R11 | Non-portable components not presented as portable; hook/script dependencies declared | 01 #11, 28; 05 #38 |
| R12 | No `http://`, `curl | sh`, secrets; network hosts and side effects disclosed | 04 #22, 26; 05 #39 |
| R13 | Binaries: no opaque builds, sha256 in reviewed metadata, signature or attestation | 03 E1–E4 |
| R14 | Behaviour checked, not only structure; strict validators in CI | 02 #5, 15, 30; 01 #30 |
| R15 | Root README: first screen says what and how to install; TOC > 100 lines; sentences ≤ 26 words; tables only for 2-D data | 05 A1–4, 9, 13, 18; 03 C1–C3 |
| R16 | Community files: CONTRIBUTING, SECURITY current, SUPPORT; "where to ask"; trust warning | 05 #22; 02 #14; 03 A5, E7 |
| R17 | Releases or tags for every package | 04 #27; 02 §3.9 |

## Findings

Severity: **high** breaks a reader's or a client's expectation or contradicts the repository;
**medium** departs from a norm two or more ecosystems share; **low** cosmetic.

### High

- **H1. `SECURITY.md` lists four packages; there are six.** "Four packages are published from
  this repository" and a four-row table. `design-review` and `cognitive-load` were added by
  `232aaba` (2026-09-24, #58); `SECURITY.md` was last touched by `10644ee` (2026-09-23).
  `slop.md` calls this `lying`. (R16)
- **H2. `howp` has no README; its `homepage` points at a directory listing.** Root README:
  "README.md — every package but howp". Claude Code tells users to check the homepage; the
  Hermes catalog renders the package README as its page; community-plugins requires a README
  with the first safe prompt, prerequisites, data boundaries and failure behaviour. (R5)
- **H3. Catalogue entries are empty; no category anywhere.** Six entries carry only `name`
  and `source`. Codex shows "Other" for all six; Claude Code has no `category` without an
  entry field; prose-discipline's `interface.category` sits in a namespace no client reads.
  The catalogue's top-level `description` describes the file format, not the contents. (R6, R7)
- **H4. Package descriptions are paragraphs, no short summary.** 701–1154 characters,
  108–189 words each. Every ecosystem caps a one-line summary at 120–250 characters. Codex
  shows `description` as the card subtitle. Descriptions repeat the READMEs. (R2)
- **H5. Root README fails readability, including the marketplace's own standard.** 394 lines,
  no TOC, first install command at line 73, 52 % of sentences over 26 words, longest 103.
  The Plugins table holds 57–134-word cells. prose-discipline's own README has 60 % of
  sentences over 26 words while its skill says "This plugin's own files must pass this
  standard". (R15)
- **H6. `howp` runs a closed-source binary with no provenance.** Only sha256 in
  `binaries.json` and `SHA256SUMS`; no signature, no attestation. Raycast, Obsidian, AMO and
  Homebrew reject opaque binaries; the trend is Sigstore/SLSA. (R13)
- **H7. The repository's rules prescribe a maintainer's diary in public files.**
  `claims.md` 22–27 ("Say what was not verified… That sentence is load-bearing"),
  `slop.md` 34–37 and 83–85 (protected), `slop.md` 89 (".agents/** Read, never judged"),
  `slop-police/SKILL.md` 340–341, `spec-writer` 205, `implementer` 484, `project.md` 32.
  The README's "Nothing below has been installed…" sentence, the same paragraph in five
  package READMEs and howp's 40-line "What has been verified" section are that diary. No
  ecosystem asks for it; the owner's private experience does not belong in a public
  repository. Root cause of M10 and part of H5. Keep: every client claim cites its source
  by permalink. `agent-police` could not find this by design: it checks internal
  consistency only, and the rules are consistently wrong.
- **H8. Agent roles act on issues filed by people.** `issue-court/SKILL.md` 53–54 ("A case
  a person filed is judged…"), queue = all open issues (151–158); `tracker-clerk` 173 lists
  every open issue and applies `pipeline/intake`. Owner: pipelines are private; agents never
  touch human issues. Found during the M3 discussion.
- **H9. `howp` is no longer what its texts say.** Manifest, root README row and SKILL.md all
  say "personal probability dashboard". The owner: it is a forecasting tool (interests →
  measurable questions → market probabilities plus the agent's judgement → a written
  forecast); outcome scoring is the owner's own end-to-end test in how-possible, not a
  product function. Claims defect across the whole package identity.

### Medium

- **M1. No CHANGELOG, tags or releases for five of six packages.** Versions move by hand;
  tags exist only for howp; Hermes catalog requires releases; Claude Code pins by version.
  prose-discipline is 1.3.0 while claiming nothing observed working. (R3, R17)
- **M2. No LICENSE file in packages.** Installed copies carry only `"license": "MIT"`. (R4)
- **M3. No community files, no "where to ask".** No CONTRIBUTING, SUPPORT, issue templates,
  trust warning, admission/removal policy. (R16)
- **M4. Only structure is checked; the strict Claude validator is not in CI and fails.**
  `claude plugin validate . --strict` warns on six symlinked vendor manifests; per plugin,
  howp and prose-discipline warn on `extensions`. No evals. (R14)
- **M5. prose-discipline references are not addressed by path.** SKILL.md names none of its
  six references; the rules-file routing table (55–61) names bare filenames in another
  directory. toc-thinking never mentions `sources.md`. (R9)
- **M6. No TOC in any of 21 references over 100 lines.** Longest hand-written:
  triz principles.md 343, ariz-85c.md 338, howp install.md 260. (R10)
- **M7. Skill description voice differs; `license` field in five of six SKILL.md.** (R8)
- **M8. prose-discipline's delivery routes and its `node` dependency.** `rules/` with
  `alwaysApply`, a SessionStart hook needing `node`, and the skill. What each harness
  actually supports is in `../research/06-*`; the owner requires every documented route
  per harness to be used. (R11)
- **M9. `extensions` used as a prose container.** howp's `not_listed`/`status` paragraphs;
  prose-discipline's unread `interface` and `components_note`. Disclosure belongs in README.
- **M10. README keeps a maintainer's diary instead of describing the package.** The
  consequence of H7 in the texts themselves; fixed only after H7.

### Low

- **L1.** `agent-skills` keyword in all six manifests (filler).
- **L2.** "Hermes — Desktop and server. Required." unexplained (README 55).
- **L3.** Three of five package READMEs say nothing about installing.
- **L4.** Skill name equals plugin name → `/triz:triz` in Claude Code.
- **L5.** Absolutes without reasons in the prose-discipline rules file.
- **L6.** howp's host list kept in three places.

## What is done well

Conformance check passes; manifests carry all ten fields; skill front matter is spec-clean;
descriptions say what and when; bodies under 500 lines; no `http://`, no pipe-to-shell, no
secrets; sha256 pinned in a reviewed file; hook fails open; CI actions pinned by sha;
SECURITY.md has a working route; every client claim cites its source by permalink.

## Not checked

Installs through any client; hook behaviour in any client; Desktop plugin browser display;
JetBrains listing rules (search summaries only); Cursor; Anthropic's skills PDF.
