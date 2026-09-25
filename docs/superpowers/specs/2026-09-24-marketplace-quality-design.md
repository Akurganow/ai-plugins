# Marketplace quality rework — design spec

Date 2026-09-24. Branch `claude/marketplace-plugin-quality-review-b5tbjh`. Status: **approved by the owner on 2026-09-24**, section by section (superpowers
brainstorming, architectural path). Next: `superpowers:writing-plans`, then execution on
this branch.

Evidence and reasons live in `../handoff/2026-09-24-marketplace-quality/` (decisions,
review, research). This file says what will be built. No decision is left open; §8 lists
the ones the owner closed last.

**Mandatory cleanup.** `docs/superpowers/` in its entirety (this spec, the handoff folder,
any plan written later) is temporary. It is deleted once the work is done **and verified**
(acceptance in §10 met, CI green, the owner has confirmed), before the pull request merges.
Before the deletion, what outlives this task moves into `docs/` as finished documents:
how each client loads a package and what was measured there (the facts behind §5.5 and
§9), and the decisions with their reasons. Task state (process, handoff, plan) does not
move. The history stays in git and in the pull request.

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
  fingerprint line `police-fingerprint: <role> <value>`, where `<role>` is the filing role
  and `<value>` is what that role writes today. Everything else does not exist for any
  role. The definition is written once, in `github-needs`; `pipeline-law` cites it for
  the pipeline roles; every other skill names the population and never restates it. An
  open issue carrying one of the three old markers (`repo-audit-routine:`,
  `slop-police-fingerprint:`, `agent-police-fingerprint:`) counts as a machine issue
  until it is closed; the three filers write only the new line from the first run after
  the change.
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
- `.claude-plugin/marketplace.json` is generated: a `jq` invocation builds `{name, owner,
  description, plugins:[{name, source:"./plugins/<name>", description, homepage,
  category}]}` from the six manifests. Top-level `description` becomes a user-facing
  sentence ("Six agent plugins: forecasting from prediction markets, an engineering prose
  standard, and four reasoning methods …").
- The root README's plugin table (§6.1) is generated by the same mechanism (jq → Markdown
  rows between `<!-- plugins:start -->`/`<!-- plugins:end -->` markers).
- **One entry point regenerates every copy.** `tools/regenerate.sh` runs, in order, every
  generator this spec names: the catalogue and the README table (jq), the description and
  Install regions of the package READMEs (§5.1), the package LICENSEs (§5.2, `cp` from the
  root), the TOCs (§5.4, `doctoc`), the rules region of the prose-discipline skill and the
  Hermes `skills.auto_load` snippet in its README (§5.5). It calls ready-made tools (`jq`,
  `doctoc`, `shasum`, `cp`) and owns only what no tool provides: the marker contract
  (replace the lines between `<!-- x:start -->` and `<!-- x:end -->`), the front-matter
  strip, the Hermes namespace derivation from the package name, and the choice of files
  that get a table of contents. Reviewed on 2026-09-25 against the written script; the
  owner chose to state this rather than move the same logic into a Node script.
  `CONTRIBUTING.md` documents that one command. CI runs the same command and then
  `git diff --exit-code`; the step's failure message names the command to run. No other
  step compares a generated file. `.agents/rules/conformance.md` "Text only" names the
  entry point beside the check as the second thing this repository runs.

### 4.2 Vendor manifest: a generated copy, not a symlink

`plugins/<name>/.claude-plugin/plugin.json` becomes a regular file, byte-identical to the
root `plugin.json`, written by `tools/regenerate.sh` (§4.1) and proven equal by CI like
every other copy. Reason (research `research/10-windows-symlink.md`): Git for Windows
installs with `core.symlinks=false` unless Developer Mode is on, and then checks out a
mode 120000 entry as a plain file holding the link text; every client fetches with `git
clone` on the user's machine; Claude Code reads only `.claude-plugin/plugin.json` and
fails a non-JSON file with its documented "corrupt manifest" error. Codex, Hermes and
Oh-My-Pi's `agent-plugins` provider read the root manifest and are unaffected. The CI
Windows image installs Git with symlinks enabled, so the integration job could not have
decided this. Consequences in the same change:

- `.agents/rules/conformance.md`, "Package shape", first bullet: "may be a symlink to it
  and may not be a second copy" becomes "is a byte-identical copy of it, written by the
  regeneration entry point". §5.1's "No other file can replace, supplement, or override
  the core fields" is kept beside it: an identical copy overrides nothing. The Codex
  sentence about a symlinked **root** manifest stays; it is about the root.
- `tools/check-conformance.py`: the hand check that resolves the vendor path as a symlink
  becomes a byte-equality check between the two files, with the same §5.1 clause quoted
  beside it and the Windows reason stated briefly, within the 25-word sentence limit.
- Root README's Windows note (§6.1) no longer mentions the symlink.

## 5. Packages

### 5.1 README template, one for all six (H2, L3)

standard-readme order, English, sentences ≤ 25 words, no maintainer diary:

1. `# <name>` and the one-line description (identical to `plugin.json` — generated into
   the README between markers by the §4.1 mechanism, so it is one source).
2. **Install**: one code block per client (Claude Code, Codex, Oh-My-Pi, Hermes), each with
   a `Source:` line, generated between markers from one template
   (`tools/templates/install.md`) with the package name substituted. The root README's
   four blocks come from the same template, so an install command exists in one file.
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

`plugins/<name>/LICENSE` is a copy of the root LICENSE, written by the regeneration
entry point (§4.1) and proven equal by CI the same way as every other copy.

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
- Skill directories renamed. The rule: a name is distinctive without the plugin prefix,
  because Oh-My-Pi shows the bare skill name, dedupes on it across every source and drops
  the later duplicate with a `name collision` warning (`docs/skills.md` line 98 and
  `claude-plugins.ts` 249–253 at `ba56afb`, research `research/07-skill-names.md`), and
  it never repeats the plugin name. One word, or one compound like `root-cause`:
  `howp/skills/forecast`, `triz/skills/contradiction`, `design-review/skills/red-flags`,
  `toc-thinking/skills/root-cause`, `cognitive-load/skills/extraneous`,
  `prose-discipline/skills/house-style`. A skill split off at plan time is named by the
  same rule. Every link in READMEs and the root README follows.

### 5.5 prose-discipline: every documented always-on route per harness (M8)

Single source of the core rules: `plugins/prose-discipline/rules/prose-discipline.md`
(3,385 characters today). Every other carrier either reads it at run time (the hook, the
Oh-My-Pi rule loader) or is generated from it by `tools/regenerate.sh` (§4.1): the body of
`skills/house-style/SKILL.md` carries the rules between markers, front matter stripped,
because Hermes loads nothing else from the package (its portable loader reads only
`plugin.json`, `skills/` and `mcp.json`; `agent_plugins.py` at `749220ef`, research
`research/08-hermes-auto-load.md`). In Claude Code and Oh-My-Pi the rules then sit in
context twice when the skill is invoked; that cost was weighed and accepted. The rules
file stays under 8,000 characters, and CI checks the bound: it keeps the injected text
under Codex's default 2,500-token spill threshold (`learn.chatgpt.com/docs/hooks.md`
536–553), so no client-specific size key is needed anywhere.

| Harness | Documented route (research `06-*`) | What ships |
| :-- | :-- | :-- |
| **Claude Code** | `hooks/hooks.json` `SessionStart` (no matcher; plain stdout is added as context; re-injected after `compact`, `clear`, resume); `SubagentStart` with `additionalContext`; `Stop`/`SubagentStop` may return `{"decision":"block","reason":…}`; `PreToolUse` on writes may deny. Plugin `rules/`, `CLAUDE.md` are not loaded. | `hooks/hooks.json` with `SessionStart` (matcher `startup|resume|clear|compact|fork`) and `SubagentStart` entries in **shell form**, `"sh \"${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh\""` with the placeholder quoted (exec form with `args` is Claude Code only, `hooks.md` 458–472; Codex ignores an unknown handler key, so `args` there would leave `sh` with no script). `print-rules.sh` is `sed` and `awk` over the rules file, front matter stripped — **no `node`**. For SessionStart it prints plain text starting with a heading, never `{` (plain stdout is context for that event, `hooks.md` 810). For SubagentStart, invoked with `--json`, it prints `{"hookSpecificOutput":{"hookEventName":"SubagentStart","additionalContext":…}}` with the text JSON-escaped in `awk`, because plain stdout is not documented to reach a subagent and `additionalContext` is (`hooks.md` 2382–2395); Claude Code injects it once per subagent context and again only after compaction dropped it. **No enforcement hook and no per-turn reminder** (owner: a blocking gate is harmful, and repeating what was already said is noise). The package recommends insistently, once per context: at session start and at subagent start, re-injected only where Claude Code has dropped it (compaction, clear, resume). |
| **Codex** | Hooks are declared in the root manifest under `extensions["com.openai"].hooks` (Claude-compatible `hooks.json`; SessionStart stdout becomes developer-role context; `additionalContextLimit: 0` avoids truncation); hooks run after the user's one-time trust. Skills are listed in every session with "must use that skill" wording when a task matches. | `extensions["com.openai"].hooks: "./hooks/hooks.json"` in `plugin.json` (documented at `developers.openai.com/plugins/build/plugins.md` 766–769), the same `hooks.json` as for Claude Code, with **no Codex-specific key**: the rules stay under the 2,500-token spill threshold (see the size bound above), so `additionalContextLimit` is not written and Claude Code sees no unknown key. Codex sets `CLAUDE_PLUGIN_ROOT` for compatibility (`hooks.md` 392–397). The package README describes this documented route. **Design targets the documented behaviour, not today's defect** (owner): Codex currently drops every hook of a package with an Agent Plugins root manifest (`loader.rs` 950–952; upstream issues #39895, #47925); that fact stays in the handoff, not in the package. The Codex job of the integration matrix asserts the hook and is marked allowed-to-fail with the issue link until upstream closes it. |
| **Oh-My-Pi** | The `claude-plugins` provider loads `<root>/rules/*.md` from marketplace installs even for standard roots; `alwaysApply: true` puts the full body into the system prompt on every request, subagents included. A second rule file with `condition:` (TTSR) interrupts the model on a regex match. Claude-style hooks are not read. | `rules/prose-discipline.md` stays (distinctive name kept: `prose-discipline`). No TTSR rule files: a TTSR `condition` interrupts the model and forces a retry, which is the same gate the owner rejected for Claude Code. |
| **Hermes** | Portable subset loads `plugin.json`, `skills/`, `mcp.json` only; `hooks/`, `rules/` ignored; portable skills are not listed in the system prompt. The documented user-side route is `skills.auto_load` in the Hermes config (`cli.md` 297–310): the named skill is pinned in full into the stable tier of the system prompt with Hermes's own "treat its instructions as active guidance" wrapper. Native Python plugins can register a system-prompt section, but that is code in the tree. | **No Python, no native plugin** (owner). The package README's Hermes section and the first lines of `skills/house-style/SKILL.md` say: in Hermes, add this skill to `skills.auto_load` so the standard is active in every session, and show the exact `config.yaml` lines. `skills.auto_load` resolves a plugin skill by its qualified name through the same `skill_view` lookup as a manual load (`agent/skill_commands.py` 165–192 and `tools/skills_tool.py` 573–590 at `749220ef`; from source, the documentation says only "each entry is a skill name"). The namespace is `agent-plugin-<slug>-<sha256(key)[:8]>` where, for `hermes plugins install`, `key` is exactly `plugin.json`'s `name` (`plugins_manifest.py` 455–467), so the qualified name is a function of the manifest: `tools/regenerate.sh` computes it with `shasum -a 256` and writes the snippet into the README between markers; nothing is copied from a Hermes session. No CLI command prints that name and plugin skills are absent from the `<available_skills>` index (documented, `developer-guide/plugins/index.md` 845); spike 4 in §9 confirms the auto-load at run time. |

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
providers), the conformance check. The "Nothing below has been
installed…" paragraph and every "not verified" sentence are removed. Sentences ≤ 25 words;
the result is checked with the `prose-discipline` skill before commit.

### 6.2 SECURITY.md (H1)

"Supported versions" becomes two rules with no package names: a package with releases is
supported at its latest release; a package without releases at the state of `main`. The
reporting section is kept.

### 6.3 CONTRIBUTING, SUPPORT, issue templates (M3)

- `CONTRIBUTING.md`: how to file an issue (templates), conventional commits (cocogitto
  reads them; `feat:`/`fix:`/`feat!:`), how to run the checks locally, how a new package is
  proposed (a PR with `plugins/<name>/` in the template shape). No mention of any agent.
- `SUPPORT.md`: issues for defects, Discussions for questions if the owner enables them.
- `.github/ISSUE_TEMPLATE/`: `install.yml` (client, OS, package, version, command, output;
  label `install`), `bug.yml` (package, what, expected; label `bug`), `package.yml`
  (proposal; label `package`), `config.yml` pointing security reports to SECURITY.md.

## 7. Releases and CI

### 7.1 cocogitto: releases committed straight to `main` (M1)

The owner rejected release pull requests (2026-09-25): a version bump is committed to
`main` by the workflow right after the commit that earned it. Tool: cocogitto
(`cog`, pinned), chosen from the research in
`../handoff/2026-09-24-marketplace-quality/research/11-release-no-pr.md`: `cog bump
--auto` works out each package's next version from the conventional commits that
touched its path, writes one version commit and one tag per package, and takes hooks
for the files it does not know. `cog.toml` at the repository root declares the five
packages (`plugins/<name>`, howp excluded), `monorepo_version_separator = "--"` and
`tag_prefix = "v"` so tags read `<name>--v<version>` (the form Claude Code documents),
the global tag turned off, a `CHANGELOG.md` per package, and a bump hook that writes the
new version into `plugin.json` and its `.claude-plugin/plugin.json` copy with `jq`. The
workflow `.github/workflows/release.yml` runs on push to `main`, installs `cog` pinned,
runs the bump, pushes the commit and the tags, and creates one GitHub release per new
tag with `gh release create`. A push made with `GITHUB_TOKEN` starts no other workflow
(GitHub's documented rule), so the release commit cannot loop; the conformance check
does not run on it, which is accepted because the commit changes only what the hooks
write. cocogitto never bumps a `0.y.z` version to `1.0.0` on its own, so the `feat!`
renames in this rework stay in `0.x`. Initial versions: current values, seeded as one
`<name>--v<current>` tag per package before the workflow is enabled. Conventional
commits are the input (`CONTRIBUTING.md` says so, §6.3).

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
conformance check (as now); the regeneration entry point followed by `git diff
--exit-code` (§4.1), which proves every generated copy equal to its source; `claude plugin
validate plugins/<name>` for each package, no `--strict`; `skills-ref validate` per skill;
`hermes plugins validate` and `hermes plugins doctor --ci` on each package. A second
workflow `integration.yml`: matrix `os ∈ {ubuntu, macos, windows}` × `client ∈ {claude,
codex, omp, hermes}`, each job installs the client, adds the marketplace (or installs the
package by path for Hermes), installs every package, and asserts the skill is listed; the
howp job downloads the release archive and verifies sha256 and, once §7.2 lands, the
cosign signature. The Windows jobs prove loading on the CI image only; a user's default
Git for Windows checkout differs (§4.2), which is why the vendor manifest is a copy.
Spikes before writing it (§9). No evals, no model calls anywhere.

## 8. Decisions the owner closed last (no open questions remain)

1. Skill names, distinctive without the plugin prefix: `forecast`, `contradiction`,
   `red-flags`, `root-cause`, `extraneous`, `house-style` (§5.4).
2. Claude Code: no blocking hook, no per-turn reminder; SessionStart and SubagentStart
   injection only (§5.5). A gate is harmful; the package recommends, insistently, once.
3. Oh-My-Pi: no TTSR rule files (§5.5).
4. Hermes: no Python module; `skills.auto_load` recommended in the README and in the
   skill's first lines (§5.5).
5. Categories as in §4.1.
6. `docs/superpowers/` (spec, handoff, plans) is deleted after the work is done and
   verified, before merge.

## 9. Spikes (run first, in the local session)

Where a spike needs a clean run, run it in a fresh environment that matches what CI can reach: no authentication, no paid calls. The owner's own installs of the four clients, with the packages already installed and authorised, serve every spike that does not need a clean run. CI asserts the clean behaviour: without authentication wherever a client allows it, and without cost.

1. Claude Code: install the package with `--plugin-dir`, confirm SessionStart stdout appears
   in context and survives `/compact`; confirm SubagentStart delivery.
2. Codex: confirm the loader drops hooks for a standard root (issues #39895, #47925 state);
   confirm `extensions["com.openai"].hooks` parses without error.
3. Oh-My-Pi: install from the marketplace, confirm `rules/prose-discipline.md` appears in the
   system prompt on every request; confirm the `agent-plugins` provider still loads the skill.
4. Hermes: install the portable package, confirm the skill loads; set `skills.auto_load` with
   the computed qualified name (§5.5) and confirm the rules appear in the system prompt with
   Hermes's auto-load wrapper; test Hermes on Windows at all.
5. Headless install in CI: whether each CLI needs authentication for `plugin marketplace
   add`/`plugin install` (Claude Code CLI validated without auth here).
6. Windows checkout: the Windows job of the integration matrix asserts that Claude Code
   loads the package from a `windows-latest` checkout; the symlink question is closed by
   §4.2 from research, not by this job.

## 10. Acceptance

- `tools/check-conformance.py` exits 0; every CI step in §7.3 green on the PR.
- No file under `plugins/`, root README, SECURITY.md contains "not verified", "has been
  installed", "was installed", "verified on", or a date-stamped verification claim.
- `.agents/` has no clause demanding the diary; `agent-police` carries the external list;
  every issue-listing clause names the `police-report` population.
- Generated files equal their sources (CI proves it).
- Every package has README.md, LICENSE, CHANGELOG.md (after the first release run),
  a ≤ 250-char description, a category, imperative skill description, referenced paths,
  TOCs.
- What outlives the task (client loading facts, the reasons behind decisions) exists as
  finished documents under `docs/`; then `docs/superpowers/` (spec, handoff, plans) is
  deleted, before merge.

## 11. Out of scope

Opening `hp` sources; changing the nine-role composition; any model-calling test (behavioural evals are deferred to a human-filed issue, to be considered after this work if they can be run cheaply);
altering `tools/schemas/`; changing how-possible from this branch.
