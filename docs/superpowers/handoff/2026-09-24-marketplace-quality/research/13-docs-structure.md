# 13: How to structure `docs/`

Clean-room research, 2026-09-25. Read-only. No model was called to judge anything.
The question: where should measured client facts and design reasons live under `docs/`?
The owner rejected a folder of numbered decision records. This file reports what others do.

## 0. How the sources were read

- Web pages came through `curl` from this machine. The HTML was stripped to text locally.
- `openai.com` answered HTTP 403 to `curl`. Its one post came through `tvly extract` instead.
- `diataxis.fr/complex-hierarchies/` answered 404. No claim below rests on it.
- Repository facts come from `gh api` at the default branch head, read 2026-09-25.
- Each repository is cited at that commit. File text came from `raw.githubusercontent.com` at the same commit.
- Scratch copies sit under `$RUN` (the session scratchpad), outside the working tree.

Kinds used below: **documentation**, **specification**, **blog post**, **repository tree at commit**.

## 1. What the frameworks prescribe

**Diátaxis.** It names four needs: tutorials, how-to guides, reference and explanation ([home](https://diataxis.fr/), documentation).
Reasons belong in explanation: "explain why things are so - design decisions, historical reasons, technical constraints" ([Explanation](https://diataxis.fr/explanation/), documentation).
Explanation serves study, away from the work; reference serves someone at work ([Reference and explanation](https://diataxis.fr/reference-explanation/), documentation).
Reference must "describe and only describe", and its structure mirrors the machinery ([Reference](https://diataxis.fr/reference/), documentation).
Explanation titles should take an implicit "About", as in "About user authentication" ([Explanation](https://diataxis.fr/explanation/), documentation).
The section may also be called Discussion, Background, Conceptual guides or Topics (same page).
Diátaxis forbids empty four-part scaffolds: "Don't do that. It's horrible." ([How to use Diátaxis](https://diataxis.fr/how-to-use-diataxis/), documentation).
Structure should grow from improved pages, not be imposed first (same page). The audience is the product's user.

**Divio documentation system.** It prescribes the same four functions ([The Documentation System](https://docs.divio.com/documentation-system/), documentation).
Explanation "can also explain why things are so - design decisions, historical reasons, technical constraints" ([Explanation](https://docs.divio.com/documentation-system/explanation/), documentation).
It notes that explanation usually ends up "scattered amongst other sections" instead of written on purpose (same page).
Divio's own explanation section is titled "Background information"; "the name is not important" (same page).
Its audience is also the user, who may not strictly need the why but gains from it.

**Write the Docs.** Its guide has no page on documenting decisions at commit [`5d30b4a`](https://github.com/writethedocs/www/tree/5d30b4ad34337de00149989ad560e95d6cc3221f/docs/guide) (repository tree at commit).
Its principles still bear on the question ([Documentation principles](https://github.com/writethedocs/www/blob/5d30b4ad34337de00149989ad560e95d6cc3221f/docs/guide/writing/docs-principles.rst), documentation).
Sources should be **Nearby**: stored "as close as possible to the code which they document".
Sources should be **Unique**: each source has a disjoint scope, which prevents parallel maintenance.
Publications should be **Addressable**, with links to content "at a granular level".
Content should be **Current**: incorrect documentation is "worse than missing documentation".
The beginner's guide says documentation "states the *why* behind the code" ([guide](https://github.com/writethedocs/www/blob/5d30b4ad34337de00149989ad560e95d6cc3221f/docs/guide/writing/beginners-guide-to-docs.rst), documentation).

**Google.** Google's engineering doc guide ranks documents from names to design docs ([best practices](https://github.com/google/styleguide/blob/f43f7a72b5a97a8aa256ef0d0d377590846575df/docguide/best_practices.md), documentation).
It says a `docs` directory explains how to start, test, debug and release.
It says design docs, once implemented, "should serve as archives of these decisions, not as half-correct docs".
It says "Duplication is Evil": link to another team's guide instead of rewriting it.
It asks for "Minimum Viable Documentation": few fresh docs beat many decayed ones.
The public style guide asks for timeless text, without "now", "new" or "currently" ([Timeless documentation](https://developers.google.com/style/timeless-documentation), documentation).
The technical-writing course says conceptual guides for newcomers work better as shorter documents ([Organizing large documents](https://developers.google.com/tech-writing/two/large-docs), documentation).

**GitHub Docs.** GitHub renders a README from `.github`, then the root, then `docs` ([About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), documentation).
So a `docs/README.md` never replaces the root README on the repository page.
GitHub also reads CONTRIBUTING, SECURITY and SUPPORT from `docs` ([community health files](https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file), documentation).
A README should hold only what a user needs to start; "Longer documentation is best suited for wikis" ([About READMEs](https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes), documentation).
The wiki page names "how you designed it, or its core principles" as wiki content ([About wikis](https://docs.github.com/en/communities/documenting-your-project-with-wikis/about-wikis), documentation).
GitHub prescribes no layout inside `docs/`.

**Architecture Decision Records.** Nygard keeps one short record per decision in `doc/arch/adr-NNN.md` ([Nygard 2011](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions), blog post).
He numbers records monotonically and marks a reversed record superseded (same post).
His reader is "a new person coming on to a project", facing past decisions (same post).
adr.github.io defines an ADR as one decision "and its rationale"; the collection is a "decision log" ([adr.github.io](https://adr.github.io/), documentation).
Thoughtworks rated lightweight ADRs "Adopt" in November 2017 ([Technology Radar](https://www.thoughtworks.com/en-us/radar/techniques/lightweight-architecture-decision-records), documentation).
Its stated readers are "future team members" and "external oversight" (same page).
Fowler suggests `doc/adr`, numbered file names, statuses, and no edits after acceptance ([Architecture Decision Record](https://martinfowler.com/bliki/ArchitectureDecisionRecord.html), blog post, dated 24 March 2026).
Fowler also names a cost: some find ADRs in git "too hard for non-developers" (same post).
Every source here addresses a team deciding over time, not users of a published product.

**Design docs, RFCs, PEPs and KEPs.** Google design docs record trade-offs before coding ([Design Docs at Google](https://www.industrialempathy.com/posts/design-docs-at-google/), blog post, Malte Ubl, 2020-07-06).
Its "Alternatives considered" section "shows very explicitly why the selected solution is the best" (same post).
It warns that implementation manuals without trade-offs should not be design docs (same post).
Rust's RFC template has "Rationale and alternatives" and "Prior art" sections ([`0000-template.md`](https://github.com/rust-lang/rfcs/blob/51783df9a76c355de7ceebeae101cba47f8ca463/0000-template.md), repository tree at commit).
Accepted RFCs "should not be substantially changed" ([README](https://github.com/rust-lang/rfcs/blob/51783df9a76c355de7ceebeae101cba47f8ca463/README.md), documentation).
PEP 1 requires a Rationale section describing "why particular design decisions were made" ([PEP 1](https://peps.python.org/pep-0001/), specification).
The KEP template carries Motivation, Goals, Non-Goals, Drawbacks and Alternatives ([template](https://github.com/kubernetes/enhancements/blob/62c7b2ee307ff554882724f3d2bf05cf97f43897/keps/NNNN-kep-template/README.md), repository tree at commit).
These are proposal processes for many contributors and sub-teams, reviewed before work starts.

**`ARCHITECTURE.md`.** matklad recommends one such file "next to README and CONTRIBUTING" for 10k–200k-line projects ([ARCHITECTURE.md](https://matklad.github.io/2021/02/06/ARCHITECTURE.md.html), blog post, 2021-02-06).
He tells writers to "only specify things that are unlikely to frequently change" (same post).
He asks writers to call out invariants, often "expressed as an absence of something" (same post).
His reader is a new contributor who lacks the core developer's mental map.
His example, rust-analyzer, marks 26 "Architecture Invariant" paragraphs in one page ([architecture.md](https://github.com/rust-lang/rust-analyzer/blob/1ad44dc58e65304b594063e70c144ecb58643671/docs/book/src/contributing/architecture.md), repository tree at commit).

**Rationale FAQs.** Some mature projects answer "why" as questions for users.
Python keeps a "Design and History FAQ" of "Why ..." entries ([Design and History FAQ](https://docs.python.org/3/faq/design.html), documentation).
Go's FAQ has a Design section, including "Why does Go not have feature X?" ([Go FAQ](https://go.dev/doc/faq), documentation).
Homebrew's FAQ holds fourteen "Why" headings, such as "Why does Homebrew say sudo is bad?" ([FAQ.md](https://github.com/Homebrew/brew/blob/86650d0b4057ed583daf0c7be5e622d80b3ee286/docs/FAQ.md), documentation).

**Agent-first repositories.** An OpenAI post treats a structured `docs/` as "the system of record" ([Harness engineering](https://openai.com/index/harness-engineering/), blog post, 2026-02-11).
Its layout has `design-docs/`, `exec-plans/`, `references/` and a root `ARCHITECTURE.md` (same post).
It keeps `AGENTS.md` short, as "the table of contents" (same post).
Its reader is the coding agent first, then the engineers steering it.

## 2. Comparable repositories

All rows were read at the commit shown, on 2026-09-25 (repository tree at commit).
"Vendor citation" means a per-fact link to another product's documentation or source.

### 2.1 Plugin catalogues and multi-client packages for AI coding agents

| Repository @ commit | What is under `docs/` | Where "why" lives | How third-party facts are cited |
| :-- | :-- | :-- | :-- |
| [anthropics/claude-plugins-official @ `ca08d5e`](https://github.com/anthropics/claude-plugins-official/tree/ca08d5e47d6402db586d37780c559a0c4c7ded9a) | No `docs/`. README only. | In the README, beside the rule: "Plugin names are immutable" gives its reason inline. | Links to Claude Code documentation pages, not per fact. |
| [openai/plugins @ `1dc1958`](https://github.com/openai/plugins/tree/1dc195897af4161d039b80d8471ec0a10c9bbc89) | No `docs/`. A README of layout only. | Nowhere. | None. |
| [NousResearch/hermes-agent @ `34343e7`](https://github.com/NousResearch/hermes-agent/tree/34343e79ab603f2a6f1c1b7597a44c00c6e2ce6f) `plugin-catalog/` | Catalogue has a README; site docs sit in `website/docs/` (user-guide, developer-guide, reference, guides). | Catalogue: nine numbered admission rules, each with its reason inline. Site: `developer-guide/architecture.md` and `*-internals.md` pages. | The vendor documents itself; the catalogue README cites no outside source. |
| [can1357/oh-my-pi @ `07f0c66`](https://github.com/can1357/oh-my-pi/tree/07f0c66b56f4ebe0e07bf7f51f552462b0207839/docs) | Flat `docs/`, 82 topic-named Markdown files (`marketplace.md`, `provider-quirks.md`). | In the topic page: `provider-quirks.md` explains each special case in place. | `provider-quirks.md` cites its own source files by path; provider URLs appear as endpoints, not sources. |
| [obra/superpowers @ `8ca22db`](https://github.com/obra/superpowers/tree/8ca22dba9a94f28898bbce59f2537ff4d87c747d/docs) | `porting-to-a-new-harness.md`, `testing.md`, `windows/polyglot-hooks.md`, per-harness READMEs, and dated `superpowers/specs/` and `plans/`. | Topic guides state invariants and reasons; dated specs hold design history. | Appendix A tabulates eight harnesses by entry point and bootstrap. The guide has no URLs; it says "the code wins". |
| [obra/superpowers-marketplace @ `ff9fa8a`](https://github.com/obra/superpowers-marketplace/tree/ff9fa8a51f422d81414fa355587620d4ad2df81c) | No `docs/`. Seven entries in all. | Nowhere. | None. |
| [wshobson/agents @ `62c4d9f`](https://github.com/wshobson/agents/tree/62c4d9fa9ce2a6a366754d74fa62c458ea99931d) | Root `ARCHITECTURE.md`; `docs/` holds `architecture.md`, `harnesses.md`, `authoring.md`, `plugins.md` and six more. | `ARCHITECTURE.md` lists five numbered "Invariants", stated as rules, some with a reason inline. | `docs/harnesses.md` is a per-harness matrix generated from `tools/adapters/capabilities.py`. No vendor citation per cell. |

### 2.2 Mature catalogues and multi-package repositories elsewhere

| Repository @ commit | What is under `docs/` | Where "why" lives | How third-party facts are cited |
| :-- | :-- | :-- | :-- |
| [Homebrew/homebrew-cask @ `06ef95c`](https://github.com/Homebrew/homebrew-cask/tree/06ef95cccb5753d55de9e61a782f738cc7bb037b/doc) | `doc/` holds one FAQ page, one bug-report example page and one image. | `doc/faq/closing_issues_without_review.md` explains one policy to users. | Links to its own README and templates. |
| [Homebrew/brew @ `86650d0`](https://github.com/Homebrew/brew/tree/86650d0b4057ed583daf0c7be5e622d80b3ee286/docs) | Flat `docs/`, 73 topic pages, published as docs.brew.sh. | In topic pages: `Tap-Trust.md` has a "Why tap trust exists" section. Also a FAQ of "Why" questions. | The pages I read carry `last_review_date` front matter. `Tap-Trust.md` links the release announcement that changed the behaviour. |
| [obsidianmd/obsidian-releases @ `8f9dd52`](https://github.com/obsidianmd/obsidian-releases/tree/8f9dd5213feaaf8c0baaa32846bb8dc667680f94) | No `docs/`. README plus a stub pointing to external docs. | README section "How community plugins are pulled" lists the client's loading steps. | The vendor documents its own client; policies link to docs.obsidian.md. |
| [ohmyzsh/ohmyzsh @ `74965c9`](https://github.com/ohmyzsh/ohmyzsh/tree/74965c96098134b192f00084f966b4b02438a739) | No `docs/`. Docs live in a wiki repository, [ohmyzsh/wiki @ `9eca591`](https://github.com/ohmyzsh/wiki/tree/9eca5916bde51092c3e80f6045cc2f9afde3667b). | Wiki `Design.md`, which calls itself "not authoritative or normative". | Links into the wiki from the README. |
| [pre-commit/pre-commit-hooks @ `44d7f9b`](https://github.com/pre-commit/pre-commit-hooks/tree/44d7f9b7e32225d2bd590282037e4650064f3950) | No `docs/`. One README section per hook. | One clause per deprecated hook, e.g. "fundamentally flawed". | Links to replacement tools. |
| [oven-sh/bun @ `f063852`](https://github.com/oven-sh/bun/tree/f063852e52e6e391e4cb9f9e10053e2f09fa135b/docs) | Site source: `runtime/`, `pm/`, `bundler/`, `test/`, `guides/`, `project/`. | `project/` holds contributor pages; `bindgen.mdx` is marked "for maintainers and contributors". | Not examined per fact. |
| [rust-lang/rfcs @ `51783df`](https://github.com/rust-lang/rfcs/tree/51783df9a76c355de7ceebeae101cba47f8ca463/text) | No `docs/`. `text/` holds 653 files, most numbered RFCs. | Each RFC's "Rationale and alternatives" section. | "Prior art" section per RFC. |
| [kubernetes/enhancements @ `62c7b2e`](https://github.com/kubernetes/enhancements/tree/62c7b2ee307ff554882724f3d2bf05cf97f43897/keps) | `keps/` per SIG, plus a template. | Each KEP's Motivation, Non-Goals, Drawbacks and Alternatives. | Per KEP, free-form. |
| [tokio-rs/tokio @ `38cdde2`](https://github.com/tokio-rs/tokio/tree/38cdde2bf70057b316c0c8554c5110ecfebd1cd4/docs) | `docs/contributing/` only, six pages. | Not under `docs/`. I did not trace where else. | Not applicable. |
| [astral-sh/uv @ `716f320`](https://github.com/astral-sh/uv/tree/716f320609fec9a36b27718be4c403d73fab7c9a/docs) | `getting-started/`, `guides/`, `concepts/`, `reference/`, `pip/`. | `concepts/` pages, and `reference/policies/` pages that state a policy with its reason. | Inline links to standards: `concepts/resolution.md` links packaging.python.org six times and PEPs twice. |
| [rust-lang/rust-analyzer @ `1ad44dc`](https://github.com/rust-lang/rust-analyzer/tree/1ad44dc58e65304b594063e70c144ecb58643671/docs/book/src) | A book: user pages plus `contributing/`. | `contributing/architecture.md`, with "Architecture Invariant" paragraphs. | Not applicable. |

Across these 20 trees I found no ADR log directory.
I searched paths for `adr`, `decision` and numbered `NNNN-name.md` files.
rust-lang/rfcs matched 580 times, all numbered RFC files.
Homebrew matched 13 times, all governance minutes, not decisions. No other tree matched.

## 3. Patterns that recur

1. **Catalogues keep the reason beside the rule.** A policy states itself, then gives its reason in one or two sentences.
   Seen in claude-plugins-official's immutable-names section and Hermes's admission rules.
   Seen also in Homebrew's "Why tap trust exists" and pre-commit-hooks' deprecation notes (all §2).
2. **ADR logs belong to teams, not catalogues.** No catalogue or package repository surveyed keeps one.
   The ADR sources address "future team members" and new joiners (§1).
   Numbered records appear only as RFC and KEP processes for large, multi-team projects (§2.2).
3. **When reasons get their own home, it is a topic page, not a log.** uv puts them in `concepts/`.
   Homebrew and Oh-My-Pi use flat, topic-named pages. Superpowers has `windows/polyglot-hooks.md`.
   This matches Diátaxis explanation, titled "About X" (§1).
4. **Invariants collect the reasons for absences.** rust-analyzer and wshobson/agents state invariants, often with the reason beside them.
   matklad names absences as the invariants hardest to see in code (§1).
5. **Multi-client facts are a matrix, one row or column per client.** Superpowers Appendix A and wshobson `docs/harnesses.md` both do this.
   Obsidian lists its client's loading steps in its README (§2).
6. **Peers rarely cite vendor documentation per fact.** Superpowers and Oh-My-Pi cite their own code.
   wshobson generates its matrix from code. uv links standards inline where it relies on them.
   This repository's per-fact rule, with source kind and commit, has no direct peer precedent.
7. **Freshness is handled explicitly.** Superpowers says the code wins over the guide. wshobson regenerates its matrix.
   Homebrew stamps `last_review_date`. matklad keeps only slow-changing facts. Google asks for timeless wording (§1–§2).
8. **Dated specs and plans are process records.** Superpowers keeps them under `docs/superpowers/`. OpenAI keeps `exec-plans/`.
   Google calls implemented design docs "archives", not documentation (§1).
9. **Flat and mode-foldered layouts both occur at similar sizes.** Oh-My-Pi keeps 82 pages flat; Homebrew keeps 73 flat.
   uv splits 81 pages into `concepts/`, `reference/` and `guides/`. Bun (335) and Hermes (447) also use folders.

## 4. Candidate structures for this repository

All three respect the same limits.
Each client sentence cites its source, its kind, and a commit or read date, as `claims.md` requires.
None mentions the agent roles. None creates an empty section, per Diátaxis.
Each keeps `README.md` as the install-first entry point, with links into `docs/`.
None ranks above another; the owner decides.

### Candidate A: one reference page, one explanation page

Follows Diátaxis's reference/explanation split, Divio's "Background information", and uv's `reference/` and `concepts/` split.

| File | Contents |
| :-- | :-- |
| `docs/clients.md` | Reference. One section per client: Claude Code, Codex, Oh-My-Pi, Hermes. Each section has the same four headings: manifest path, how a package is fetched, how a skill is named, how an always-on instruction arrives. Every fact carries its source, kind and commit or date. Austere; no reasons. README "Client notes" move here, leaving a link. |
| `docs/design.md` | Explanation, "About this repository's design". One section per decision, nine in all, listed below the table. Each section states the constraint, the choice, the alternatives, and links the facts in `clients.md` by anchor. |

The nine `design.md` sections:

1. One source for every copy.
2. The vendor manifest is a byte copy, not a symlink.
3. Skill names carry no plugin prefix.
4. One rules file, with one documented delivery route per client.
5. No hook blocks the agent.
6. Cocogitto commits versions to `main` and tags `<name>--v<version>`.
7. Nothing in CI calls a model.
8. The repository records no maintainer verification.
9. The howp checksum file is signed.

Variant: write the `design.md` headings as questions, like the Python and Go FAQs and Homebrew's FAQ.
For example: "Why is the vendor manifest a copy and not a symlink?"

Trade-offs:
- Two files, so the index is the README link and each page's headings.
- The reference/explanation boundary stays clean: facts in one page, reasons in the other.
- `design.md` holds nine topics. It grows long, and anchors become the unit of linking.
- A reason and its evidence sit in different files. A reader follows links to check a claim.
- A new client adds one section to `clients.md` and touches `design.md` only if a reason changes.

### Candidate B: topic pages, each holding its facts and its reasons

Follows Homebrew's flat topic pages ("Why tap trust exists"), Oh-My-Pi's flat `docs/`, and superpowers' `windows/polyglot-hooks.md`.
Also follows Write the Docs' **Unique** principle: each page has a disjoint scope.

| File | Contents |
| :-- | :-- |
| `docs/loading.md` | How each client finds and fetches a package: manifest path, catalogue path, install route. A per-client table, then notes, each fact cited. |
| `docs/generated-copies.md` | Why every copy comes from one source through `tools/regenerate.sh`. Why the vendor manifest is a byte copy, not a symlink, with the Git for Windows and Codex facts cited in place. |
| `docs/skill-names.md` | Why skills carry no plugin prefix. A per-client table of how each client shows a skill name, each row cited. |
| `docs/always-on-instructions.md` | Why one rules file, and the one documented delivery route per client, as a cited table. Why no hook blocks the agent. |
| `docs/releases.md` | Why cocogitto commits versions straight to `main` and tags `<name>--v<version>`. Why howp's checksum file is signed, and that another repository releases howp. |
| `docs/checks.md` | What CI checks and what it cannot. Why nothing in CI calls a model. Why the repository records no maintainer verification. |

Optional: `docs/README.md` as an index. GitHub shows the root README first, so the two never compete.

Trade-offs:
- Each page answers one question and carries its own evidence, as Homebrew's `Tap-Trust.md` does.
- Pages mix a reference table with discussion. Diátaxis warns that explanation "tends to absorb other things".
- A reader who wants "everything about Codex" reads up to four pages.
- A client change can touch several pages; a decision change touches one.
- Six small pages suit Google's shorter conceptual documents and Nygard's "small, modular documents", without numbering.

### Candidate C: an architecture map with invariants, plus a client matrix

Follows matklad's `ARCHITECTURE.md`, rust-analyzer's "Architecture Invariant" paragraphs, and wshobson/agents' `ARCHITECTURE.md` with `docs/harnesses.md`.
The matrix follows superpowers' Appendix A.

| File | Contents |
| :-- | :-- |
| `ARCHITECTURE.md` at the root, or `docs/architecture.md` | A bird's-eye view, then a code map of `plugins/`, `tools/`, `.claude-plugin/` and the workflows. Then "Invariants": each decision as one numbered invariant with a short reason. Absences read naturally here: "Nothing in CI calls a model", "No hook blocks the agent", "The repository records no maintainer verification". |
| `docs/clients.md` | A matrix: rows for manifest path, catalogue path, fetch, skill naming and always-on route; one column per client. Each cell links its source. Per-client notes below carry kind and commit or date. |

Trade-offs:
- The invariant form suits this repository's reasons, several of which are absences.
- matklad's reader is a contributor, not an installer. The installer path stays in the README.
- matklad advises keeping only slow-changing facts in it and revisiting it "a couple of times a year".
- A root file adds a seventh document beside README, CONTRIBUTING, SECURITY, SUPPORT, AGENTS and CLAUDE.
- `docs/architecture.md` avoids that, but GitHub does not surface it the way it surfaces a root file.
- A code map must decide what to say about `.agents/` without naming roles. That line needs the owner's ruling.
- A matrix gives a one-glance view but cramps long citations. Notes below the table carry them.

## 5. What this research did not settle

- No source measured which layout readers of a plugin catalogue actually use. The patterns above are observed practice only.
- I read the peers' trees and chosen pages, not every page. "No ADR log" rests on the path search in §2.
- `openai.com` was read through Tavily's extractor, not directly. The quoted layout matches the extracted text.
