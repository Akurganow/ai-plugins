# Marketplace quality rework — design spec

Date 2026-09-24. Branch `claude/marketplace-plugin-quality-review-b5tbjh`. Status: **written,
all decisions closed, awaiting the owner's review** (superpowers brainstorming,
architectural path). After approval: `superpowers:writing-plans`, then execution on this
branch.

Evidence and reasons live in `../handoff/2026-09-24-marketplace-quality/` (decisions,
review, research). This file says what will be built. No decision is left open; §8 lists
the ones the owner closed last.

**Mandatory cleanup.** `docs/superpowers/` in its entirety (this spec, the handoff folder,
any plan written later) is temporary. It is deleted once the work is done **and verified**
(acceptance in §10 met, CI green, the owner has confirmed), before the pull request merges.
The history stays in git and in the pull request.

## 1. Purpose and success

Bring the marketplace and its six packages to the norm that mature plugin ecosystems,
the Agent Plugins and Agent Skills specifications, Claude Code's documentation and the
other three target clients share. Success is all four at once:

1. An outside reader opens the repository, understands it within a minute and installs a
   package into their client without a question.
2. Packages pass external catalogues' validators and admission rules (Anthropic community
   marketplace, Hermes catalog, awesome lists).
3. The same package works in Claude Code, Codex, Hermes and Oh-My-Pi with nothing lost.
4. The repository reads as the owner's own work.

## 2. Constraints

- `hp` sources stay private. The nine-role agent system stays in composition.
- Every copy of a file is generated on CI from one source; nothing is kept by hand twice.
  Version bumps and tags are automatic. Ready-made tools over home-grown scripts.
- No paid tests: nothing in CI or in the packages calls a model.
- Pipelines are private: public docs never mention the roles; agents never touch issues
  filed by people.
- All four harnesses are supported; `prose-discipline` uses every documented always-on
  route each harness has.
- The repository does not record the maintainer's own verification.
- Changes to how-possible are filed as an issue there, not made from this branch.

## 3. Rules and roles (`.agents/`)

### 3.1 Remove the verification diary rule (H7, M10)

- `.agents/rules/claims.md`: delete the bullet "Say what was not verified" (lines 22–27).
  Keep every other bullet: documentation first, cite the source in the text with its kind,
  never invent a command, "the standard says" vs "this client does", supported-surface
  list as obligations, claims about released artifacts point at machine-written records.
- `.agents/rules/slop.md`: in kind 1 (`noise`) delete the sentence pair "Not noise: a
  sentence that says what was not verified … has not read `claims.md`" (34–37); in "What is
  protected" delete "The claims discipline's sentences …" (83–85) except its parts that
  protect a per-fact source and a date beside a measurement, which stay as their own bullet.
  Keep line 89 as is (the owner chose `agent-police` for rules review, not `slop-police`).
- `.agents/skills/slop-police/SKILL.md` 340–341: delete "The install section's opening
  sentence and every "not verified" line are `claims.md`'s and protected."
- `.agents/skills/spec-writer/SKILL.md` 205, `.agents/skills/implementer/SKILL.md` 482–485,
  `.agents/prompts/project.md` 32: delete the "says what was not verified" clauses.
- Texts that the rule produced are removed in §5 and §6.

### 3.2 `agent-police` gets an external measure (H7)

Add to `.agents/skills/agent-police/SKILL.md` a second question beside "one machine?":
"the right machine?". Before reading `.agents/`, the role reads an external source list
(kept in the skill under a heading, each with URL and what to check there): the Agent
Plugins and Agent Skills specifications, Claude Code plugin docs, Codex/Hermes/Oh-My-Pi
plugin docs in their repositories, and the marketplace norms this review used (standard-
readme, Keep a Changelog, SemVer, the ecosystems' listing rules). A rule that contradicts
those sources is a finding of a new kind, `external-disagreement`, filed like the others.
`.agents/manifest.yaml`'s description of the role is updated in the same change.

### 3.3 Agents never touch human issues (H8)

- Define one machine population: an issue carries the label `police-report` **and** a
  fingerprint marker (`repo-audit-routine:`, `slop-police-fingerprint:`,
  `agent-police-fingerprint:`). Everything else does not exist for any role.
- `issue-court`: the queue is built from `police-report`-labelled open issues only; delete
  "A case a person filed is judged …" (53–54); the listing in `github-needs` is "issues by
  label" (already there) and the label is mandatory, never omitted.
- `tracker-clerk`: "List every open issue" (173) becomes "List every open issue labelled
  `police-report`"; `pipeline/intake` is applied only within that population.
- `pipeline-clerk`, `pipeline-law`, `github-needs`: same population wherever an issue
  listing is defined. Every filer must apply `police-report` at filing (already the case
  for the three police roles; confirm in each skill).
- Human issue templates (§6.3) apply their own labels (`bug`, `install`, `package`) and
  never `police-report`. Label creation of `bug`/`install`/`package` is a repository
  setting the owner makes; the templates reference them.

## 4. Catalogue and manifests

### 4.1 Source of truth and generated catalogue (H3, H4, M9, L1)

- `plugins/<name>/plugin.json` is the only source of package metadata. Changes per file:
  `description` becomes one sentence ≤ 250 characters that says what the package does;
  `keywords` loses `agent-skills`; `homepage` unchanged; add
  `extensions["io.github.akurganow.ai-plugins"].category` from Codex's category list
  (`research/04-other-clients.md` §1.4): `howp` Data & Analytics; `prose-discipline`
  Productivity; `design-review`, `cognitive-load`, `toc-thinking`, `triz` Developer Tools. The prose paragraphs now under `extensions`
  (howp `network.not_listed`, `network.status`; prose-discipline `components_note`,
  `interface`) are deleted; howp keeps a machine-readable
  `extensions["io.github.akurganow.ai-plugins"].network.hosts` array as the single source
  of its host list (L6) and the README explains it in prose.
- `.claude-plugin/marketplace.json` is generated: a `jq` invocation in
  `.github/workflows/conformance.yml` builds `{name, owner, description, plugins:[{name,
  source:"./plugins/<name>", description, homepage, category}]}` from the six manifests
  and `cmp`s it with the committed file; a mismatch fails CI with the diff. The same
  invocation is documented in `CONTRIBUTING.md` for local regeneration. Top-level
  `description` becomes a user-facing sentence ("Six agent plugins: forecasting from
  prediction markets, an engineering prose standard, and four reasoning methods …").
- The root README's plugin table (§6.1) is generated by the same mechanism (jq → Markdown
  rows between `<!-- plugins:start -->`/`<!-- plugins:end -->` markers, checked with `cmp`).

### 4.2 Vendor manifest symlink

Kept for now. The Windows job of the integration matrix (§7.3) decides empirically whether
it must change; nothing in this spec depends on it.

## 5. Packages

### 5.1 README template, one for all six (H2, L3)

standard-readme order, English, sentences ≤ 25 words, no maintainer diary:

1. `# <name>` and the one-line description (identical to `plugin.json` — generated into
   the README between markers by the §4.1 mechanism, so it is one source).
2. **Install**: one code block per client (Claude Code, Codex, Oh-My-Pi, Hermes), commands
   taken from the root README, each with a `Source:` line.
3. **Usage**: one first prompt in a code block and what happens.
4. **What's inside**: the skill(s), the references, any rule/hook, in a table.
5. **Requirements and network** (only where they exist): interpreters, hosts, what is
   read and written, failure behaviour. howp: the host list from the manifest, the cache
   path, the sha256 refusal, "no source build".
6. **Boundaries**: what the package does not do; hand-offs to sibling packages.
7. **License**: `MIT`, link to the package's LICENSE.
8. **Help**: link to `SUPPORT.md`.

The five existing READMEs are rewritten to this; `plugins/howp/README.md` is created.

### 5.2 LICENSE in every package (M2)

`plugins/<name>/LICENSE` is a copy of the root LICENSE; a CI step `cmp`s each with the
root and fails on difference.

### 5.3 howp identity (H9, L4)

- Identity: a forecasting tool: interests → measurable questions → prediction-market
  probabilities plus the agent's judgement → a written forecast. Outcome scoring is not a
  product function and is not claimed. The description, README, SKILL.md description and
  body are rewritten from this. The word "dashboard" survives only where it names the
  `hp render` output file.
- Skill directory `skills/howp/` → `skills/forecast/` (front matter `name: forecast`).
- The "What has been verified, and what has not" section is deleted; operational
  instructions in it (run the preflight every time, never a source build, two-match rule)
  move into the procedure text without dates or machines.
- `references/commands.md` is untouched (release-written).

### 5.4 Skill hygiene across packages (M5, M6, M7, L4)

- Every reference is named from SKILL.md by relative path with a "read when" condition.
  prose-discipline's rules routing table gets real paths.
- Every reference over 100 lines starts with a TOC generated by `doctoc` between its
  markers, checked on CI; `howp/references/commands.md` is excluded.
- All six descriptions in imperative voice, key use case first, "Use when …" with the
  trigger words users say; ≤ 1024 characters. `license: MIT` in all six front matters.
- A plugin may carry several skills (Agent Plugins §6.1: every immediate child of `skills/` with a `SKILL.md`). At plan time every skill is assessed for size and breadth; a skill that is too long, too wordy or takes on too much is split into several skills of the same plugin (candidates: howp install vs forecast vs interview; triz matrix route vs ARIZ; toc-thinking per tree). Splits are proposed to the owner with the names below.
- Skill directories renamed, one word each, never repeating the plugin name:
  `howp/skills/forecast`, `triz/skills/contradiction`, `design-review/skills/review`,
  `toc-thinking/skills/root-cause`, `cognitive-load/skills/audit`,
  `prose-discipline/skills/standard`. A skill split off at plan time gets a one-word name
  by the same rule. Every link in READMEs and the root README follows.

### 5.5 prose-discipline: every documented always-on route per harness (M8)

Single source of the core rules: `plugins/prose-discipline/rules/prose-discipline.md`
(3,385 characters today). All other carriers either
read it at run time or are generated from it on CI.

| Harness | Documented route (research `06-*`) | What ships |
| :-- | :-- | :-- |
| **Claude Code** | `hooks/hooks.json` `SessionStart` (no matcher; plain stdout is added as context; re-injected after `compact`, `clear`, resume); `SubagentStart` with `additionalContext`; `Stop`/`SubagentStop` may return `{"decision":"block","reason":…}`; `PreToolUse` on writes may deny. Plugin `rules/`, `CLAUDE.md` are not loaded. | `hooks/hooks.json` with `SessionStart` and `SubagentStart` entries in exec form (`command` + `args`, `${CLAUDE_PLUGIN_ROOT}`), running `hooks/print-rules.sh`, which is `sed` over the rules file (front matter stripped) — **no `node`**. Text starts with a heading, never `{`. **No enforcement hook and no per-turn reminder** (owner: a blocking gate is harmful, and repeating what was already said is noise). The package recommends insistently, once per context: at session start and at subagent start, re-injected only where Claude Code has dropped it (compaction, clear, resume). |
| **Codex** | Hooks are declared in the root manifest under `extensions["com.openai"].hooks` (Claude-compatible `hooks.json`; SessionStart stdout becomes developer-role context; `additionalContextLimit: 0` avoids truncation); hooks run after the user's one-time trust. Skills are listed in every session with "must use that skill" wording when a task matches. | `extensions["com.openai"].hooks: "./hooks/hooks.json"` in `plugin.json`, the same `hooks.json` as for Claude Code, with `additionalContextLimit: 0` on the SessionStart entry. The package README describes this documented route. **Design targets the documented behaviour, not today's defect** (owner): Codex currently drops every hook of a package with an Agent Plugins root manifest (`loader.rs` 950–952; upstream issues #39895, #47925); that fact stays in the handoff, not in the package. The Codex job of the integration matrix asserts the hook and is marked allowed-to-fail with the issue link until upstream closes it. |
| **Oh-My-Pi** | The `claude-plugins` provider loads `<root>/rules/*.md` from marketplace installs even for standard roots; `alwaysApply: true` puts the full body into the system prompt on every request, subagents included. A second rule file with `condition:` (TTSR) interrupts the model on a regex match. Claude-style hooks are not read. | `rules/prose-discipline.md` stays (distinctive name kept: `prose-discipline`). No TTSR rule files: a TTSR `condition` interrupts the model and forces a retry, which is the same gate the owner rejected for Claude Code. |
| **Hermes** | Portable subset loads `plugin.json`, `skills/`, `mcp.json` only; `hooks/`, `rules/` ignored; portable skills are not listed in the system prompt. The documented user-side route is `skills.auto_load` in the Hermes config (`cli.md` 297–310): the named skill is pinned in full into the stable tier of the system prompt with Hermes's own "treat its instructions as active guidance" wrapper. Native Python plugins can register a system-prompt section, but that is code in the tree. | **No Python, no native plugin** (owner). The package README's Hermes section and the first lines of `skills/standard/SKILL.md` say: in Hermes, add this skill to `skills.auto_load` so the standard is active in every session, with the exact config key. Because the skill body is what Hermes loads, Hermes itself surfaces the recommendation the first time the skill is used. Whether `skills.auto_load` accepts a plugin skill's qualified name (`agent-plugin-<slug>-<hash>:<skill>`) is from source only; spike 4 in §9 verifies it and the README states the working form. |

Manifest: `plugin.json` `extensions["io.github.akurganow.ai-plugins"].components` is
deleted (no client reads it); the Codex namespace above is the only vendor extension.
The `hooks/session-rules.sh` script and its `node` dependency are removed.

## 6. Root documents

### 6.1 README (H5, L2, M10)

One file, restructured: title and one paragraph (what this is, four clients); TOC; **Install**
right after it (four client blocks, each: commands, one `Source:` line, one line of
what differs); **Plugins** (generated table: name, one line, link to package README);
**Trust** (Anthropic's wording: make sure you trust a plugin before installing);
**Layout**; **Contributing** and **Help** (links); **License**; then, at the end under their
own headings, the explanations that are now inline: what conformance buys, per-client
notes (Hermes depth-2 and `plugins/howp` suffix, Codex marketplace name, Oh-My-Pi
providers), Windows and the symlink, the conformance check. The "Nothing below has been
installed…" paragraph and every "not verified" sentence are removed. Sentences ≤ 25 words;
the result is checked with the `prose-discipline` skill before commit.

### 6.2 SECURITY.md (H1)

"Supported versions" becomes two rules with no package names: a package with releases is
supported at its latest release; a package without releases at the state of `main`. The
reporting section is kept.

### 6.3 CONTRIBUTING, SUPPORT, issue templates (M3)

- `CONTRIBUTING.md`: how to file an issue (templates), conventional commits (release-please
  reads them; `feat:`/`fix:`/`feat!:`), how to run the checks locally, how a new package is
  proposed (a PR with `plugins/<name>/` in the template shape). No mention of any agent.
- `SUPPORT.md`: issues for defects, Discussions for questions if the owner enables them.
- `.github/ISSUE_TEMPLATE/`: `install.yml` (client, OS, package, version, command, output;
  label `install`), `bug.yml` (package, what, expected; label `bug`), `package.yml`
  (proposal; label `package`), `config.yml` pointing security reports to SECURITY.md.

## 7. Releases and CI

### 7.1 release-please (M1)

`release-please-config.json` + `.release-please-manifest.json`, `release-type: simple`
per package path (`plugins/<name>`), `extra-files` `[{"type":"json","path":"plugin.json",
"jsonpath":"$.version"}]`, `changelog-path: CHANGELOG.md`, `tag-separator: "--"` so tags
read `<name>--v<version>` (the form Claude Code documents). `howp` is not in the config.
Workflow `.github/workflows/release-please.yml` (`googleapis/release-please-action`,
pinned by sha). Initial versions: current values.

### 7.2 cosign in how-possible (H6) — issue text

Filed in Akurganow/how-possible at implementation time. Body: in `release.yml` job
`publish` add `permissions: id-token: write`, install `sigstore/cosign-installer` (pinned),
after `SHA256SUMS` is assembled run `cosign sign-blob --yes --bundle SHA256SUMS.sigstore.json
SHA256SUMS` (or `.sig`+`.pem` pair) and upload the bundle with the release assets; document
in `release-publish.sh` header. Verification identity:
`https://github.com/Akurganow/how-possible/.github/workflows/release.yml@refs/heads/main`,
issuer `https://token.actions.githubusercontent.com`. ai-plugins then adds the check (§7.3)
and the README line.

### 7.3 CI (M4a, M2, §4.1, H7)

`.github/workflows/conformance.yml` gains steps, all with pinned actions and versions:
conformance check (as now); generated-copy checks (`marketplace.json`, README table,
package LICENSEs, TOCs via `doctoc --check` or `cmp`); `claude plugin
validate plugins/<name>` for each package, no `--strict`; `skills-ref validate` per skill;
`hermes plugins validate` and `hermes plugins doctor --ci` on each package. A second
workflow `integration.yml`: matrix `os ∈ {ubuntu, macos, windows}` × `client ∈ {claude,
codex, omp, hermes}`, each job installs the client, adds the marketplace (or installs the
package by path for Hermes), installs every package, and asserts the skill is listed; the
howp job downloads the release archive and verifies sha256 and, once §7.2 lands, the
cosign signature. Spikes before writing it (§9). No evals, no model calls anywhere.

## 8. Decisions the owner closed last (no open questions remain)

1. Skill names: one word each — `forecast`, `contradiction`, `review`, `root-cause`,
   `audit`, `standard` (§5.4).
2. Claude Code: no blocking hook, no per-turn reminder; SessionStart and SubagentStart
   injection only (§5.5). A gate is harmful; the package recommends, insistently, once.
3. Oh-My-Pi: no TTSR rule files (§5.5).
4. Hermes: no Python module; `skills.auto_load` recommended in the README and in the
   skill's first lines (§5.5).
5. Categories as in §4.1.
6. `docs/superpowers/` (spec, handoff, plans) is deleted after the work is done and
   verified, before merge.

## 9. Spikes (run first, in the local session)

1. Claude Code: install the package with `--plugin-dir`, confirm SessionStart stdout appears
   in context and survives `/compact`; confirm SubagentStart delivery.
2. Codex: confirm the loader drops hooks for a standard root (issues #39895, #47925 state);
   confirm `extensions["com.openai"].hooks` parses without error.
3. Oh-My-Pi: install from the marketplace, confirm `rules/prose-discipline.md` appears in the
   system prompt on every request; confirm the `agent-plugins` provider still loads the skill.
4. Hermes: install the portable package, confirm the skill loads; set `skills.auto_load` with
   the plugin skill's qualified name and confirm the rules appear in the system prompt; record
   the exact working form for the README; test Hermes on Windows at all.
5. Headless install in CI: whether each CLI needs authentication for `plugin marketplace
   add`/`plugin install` (Claude Code CLI validated without auth here).
6. Windows checkout: what each client does with the symlinked vendor manifest.

## 10. Acceptance

- `tools/check-conformance.py` exits 0; every CI step in §7.3 green on the PR.
- No file under `plugins/`, root README, SECURITY.md contains "not verified", "has been
  installed", "was installed", "verified on", or a date-stamped verification claim.
- `.agents/` has no clause demanding the diary; `agent-police` carries the external list;
  every issue-listing clause names the `police-report` population.
- Generated files equal their sources (CI proves it).
- Every package has README.md, LICENSE, CHANGELOG.md (after first release-please run),
  a ≤ 250-char description, a category, imperative skill description, referenced paths,
  TOCs.
- `docs/superpowers/` (spec, handoff, plans) deleted after the work is done and verified,
  before merge.

## 11. Out of scope

Opening `hp` sources; changing the nine-role composition; any model-calling test (behavioural evals are deferred to a human-filed issue, to be considered after this work if they can be run cheaply);
altering `tools/schemas/`; changing how-possible from this branch.
