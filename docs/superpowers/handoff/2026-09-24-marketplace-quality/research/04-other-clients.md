# 04 — How other agent clients and catalogues define a quality plugin, skill and marketplace

Clean-room research, 2026-09-24. Nothing under `/home/user/ai-plugins` or any other local git repository was read, and no `git` command was run.
Every quote below was read from the URL named beside it. Raw copies are under
`research/raw/04/` next to this file. Where a copy was fetched from a branch, it was compared byte for byte (`cmp`) with the same path at the commit SHA cited below, and they matched. Line numbers (`#Lnn`) refer to that commit.

---

## 0. Reachability

### How this environment reaches sources

| Route | Result |
| :-- | :-- |
| `curl` to `raw.githubusercontent.com` | **Open.** Used for every GitHub-hosted file below. |
| `curl` to `github.com` / `api.github.com` / `codeload.github.com` | `github.com` HTML: HTTP 403. `api.github.com/repos/openai/codex/...`: HTTP 403, body `"GitHub access to this repository is not enabled for this session. Use add_repo to request access..."`. `codeload`: 403. |
| WebFetch to `github.com` HTML | **Open.** Used only to list directories and to read the HEAD commit SHA of each repository. |
| GitHub MCP `get_file_contents` / `list_commits` on third-party repositories | Denied: `Access denied: repository "openai/codex" is not configured for this session. Allowed repositories: akurganow/ai-plugins.` |
| GitHub MCP `search_code` | **Open.** Used only to find file paths. |
| `registry.npmjs.org` | **Open.** Used for the `@microsoft/vally` / `@microsoft/vally-cli` package metadata and tarball. |
| `agentskills.io` | **Open** (HTTP 200). The same pages were also read from `agentskills/agentskills` at a pinned commit. |
| `docs.github.com` | Open (HTTP 200). The GitHub Docs source was read from `github/docs` at a pinned commit instead of the rendered site. |

### Blocked sites, the error returned, and the copy used instead

| Source asked for | Error returned | Copy read instead |
| :-- | :-- | :-- |
| `https://developers.openai.com/codex/plugins`, `.../plugins/build/plugins` | curl: `(56) CONNECT tunnel failed, response 403`; WebFetch: `{"error_type":"EGRESS_BLOCKED","domain":"developers.openai.com","message":"Access to developers.openai.com is blocked by the network egress proxy."}` | Codex's `docs/skills.md` holds only a pointer: *"For information about skills, refer to [this documentation](https://developers.openai.com/codex/skills)."* There is no Markdown copy of the plugin docs in `openai/codex/docs/`, which has 15 files and none about plugins. **Codex facts below therefore come from source**, specifically `openai/codex` at `edd0df9084eb8446e586305b68a4d62202278afd`, its bundled `plugin-creator`/`skill-creator` skills, and OpenAI's catalogue repos. |
| `https://help.openai.com/en/articles/20001504-...` (importing marketplaces) | WebFetch: `EGRESS_BLOCKED ... help.openai.com` | None found. **Not read.** |
| `https://hermes-agent.nousresearch.com/docs...` | curl: `CONNECT tunnel failed, response 403` | Same docs as Markdown in `NousResearch/hermes-agent/website/docs/` at `130b8f2c5dbca93a81aa396dd2ba44420d78f6f0`. |
| `https://geminicli.com/docs/extensions/`, `https://geminicli.com/extensions/browse/` | curl 403; WebFetch `EGRESS_BLOCKED ... geminicli.com` | Docs: `google-gemini/gemini-cli/docs/extensions/*.md` at `87de0b6369f0466da37d9b3c0c9b77374bb59992`. **Gallery page (what a card shows) not read.** |
| `https://skills.sh` | curl 403 | `vercel-labs/skills` README and `src/telemetry.ts` at `7407f3893ad4dceab546ac002c3ef806e4000c73`. **The leaderboard and audits pages were not read.** |
| `https://vercel.com/changelog/automated-security-audits-now-available-for-skills-sh` | WebFetch `EGRESS_BLOCKED ... vercel.com` | None. Statements about skills.sh ranking in §8.2 are marked *search-snippet only, unverified*. |
| `https://opencode.ai/docs/skills` | curl 403 | `anomalyco/opencode/packages/web/src/content/docs/*.mdx` at `0f549842ee746e400b1f72516b0b2e292e267e2c`. `sst/opencode` redirects to this repository. |
| `https://cursor.com/docs`, `https://docs.cursor.com` | curl 403 | `cursor/plugins` at `57fc467a229cf2853329f19c9e6a9fd83ddc2ea2` and `cursor/plugin-template` at `46216072ac5750f782f95bb325b4d12b7c3ae9c9`. **Cursor's own docs (`cursor.com/docs/reference/plugins`) and the marketplace UI were not read.** |
| `https://github.com/NousResearch/hermes-plugin-index` | WebFetch: `The server returned HTTP 404 Not Found.`; raw README also 404 | This repository does not exist, or is not public. Hermes's curated index is `plugin-catalog/` inside `NousResearch/hermes-agent`, read at the commit above. |

### Commits read

| Repository | Commit | Date |
| :-- | :-- | :-- |
| openai/codex | `edd0df9084eb8446e586305b68a4d62202278afd` | 2026-09-24 |
| openai/plugins | `1dc195897af4161d039b80d8471ec0a10c9bbc89` | 2026-09-11 |
| openai/community-plugins | `62844ca1cd865b76c7fed7180fc1ffef16e9167b` | 2026-09-14 |
| NousResearch/hermes-agent | `130b8f2c5dbca93a81aa396dd2ba44420d78f6f0` | 2026-09-24 |
| can1357/oh-my-pi | `62d610789e7a0a09ee109ff42b6de16c63585ba5` | 2026-09-24 |
| google-gemini/gemini-cli | `87de0b6369f0466da37d9b3c0c9b77374bb59992` | 2026-09-24 |
| github/docs | `dc1c9143143ca82376681a6da6f9ff7fd813ef72` | 2026-09-24 |
| github/awesome-copilot | `1f5644080a525d26a2e24f61a7609fb9b261c21a` | 2026-09-24 |
| github/copilot-plugins | `main` (fetched 2026-09-24; SHA not recorded) | — |
| anomalyco/opencode | `0f549842ee746e400b1f72516b0b2e292e267e2c` | 2026-09-24 |
| cursor/plugins | `57fc467a229cf2853329f19c9e6a9fd83ddc2ea2` | 2026-09-24 |
| cursor/plugin-template | `46216072ac5750f782f95bb325b4d12b7c3ae9c9` | 2026-04-24 |
| anthropics/skills | `33375500bcea98d610eb30ce10ac4e59b89c390d` | 2026-09-24 |
| agentskills/agentskills | `69ef37e9424c0a7ea9dd2293b559e43ec8176379` | 2026-08-09 |
| vercel-labs/skills | `7407f3893ad4dceab546ac002c3ef806e4000c73` | 2026-09-17 |
| travisvn/awesome-claude-skills | `1da55aa810f206d3fe2005e7e3989b15a275d942` | 2026-04-28 |
| ComposioHQ/awesome-claude-skills | `be2a406907dbc61b73e6827ded415c96139d13a2` (branch `master`) | 2026-07-24 |
| hesreallyhim/awesome-claude-code | `11797a891f69692c83631f921d129b7bc250e0a3` | 2026-09-24 |
| William-Yeh/agent-skill-linter | `3ab47f0bc7a7fea28f5d3dadfa7519d3062958a5` | 2026-09-06 |
| npm `@microsoft/vally@0.17.0`, `@microsoft/vally-cli@0.17.0` | registry tarball (published 2026-09-24T03:28Z) | — |

The HEAD SHAs were read from the GitHub commits page through WebFetch. Each one is a single observation of that page.

---

## 1. OpenAI Codex (CLI and app)

**Kind of source:** mostly **source**, because the documentation site is blocked (§0), plus Codex's own bundled authoring skills and OpenAI's catalogue repositories.

### 1.1 Codex reads Agent Plugins 1.0.0 root manifests natively

`codex-rs/utils/plugins/src/plugin_namespace.rs`:

- #L12–L16: `pub const AGENT_PLUGIN_MANIFEST_RELATIVE_PATH: &str = "plugin.json";` and `pub const AGENT_PLUGIN_SCHEMA_URI: &str = "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json";`
- #L43–L48, `find_plugin_manifest_path`: a root `plugin.json` that is a symlink, or is not a regular file, returns `None`, so the plugin is not found at all:
  `Ok(metadata) if metadata.file_type().is_symlink() || !metadata.file_type().is_file() => { return None; }`
  The test `rejects_symlinked_root_plugin_manifest` is at #L253.
- A root `plugin.json` is taken as an Agent Plugins manifest only if its `$schema` status is not `Unrelated`, meaning the `$schema` starts with `https://agent-plugins.org/schemas/` (#L27–L41). Otherwise Codex falls back to vendor paths (`.codex-plugin/`, `.claude-plugin/`, `.cursor-plugin/`; tests at #L134–L135).

`codex-rs/core-plugins/src/agent_plugin_manifest.rs`:

- #L18–L28: the accepted field set is `$schema, name, version, description, author, homepage, repository, license, keywords, extensions`. Any other field is dropped with a warning: `"ignoring unknown Agent Plugins manifest field"` (#L78).
- A `null` value for `version`, `description`, `author`, `homepage`, `repository` or `license` is a **hard error**: `"Agent Plugins \`{field}\` must use its declared type when present"`.
- Name rule (#L219 onward): non-empty, at most 64 characters, no `--`, no `..`, only `[a-z0-9.-]`, alphanumeric at both ends. Error text: `"invalid Agent Plugins name \`{}\`; use lowercase letters, numbers, dots, or hyphens"`.
- **What Codex displays for an Agent Plugins package** (#L160–L180). This is the discoverability mapping:
  ```rust
  skills: Some(RawPluginManifestPaths::Path("./skills".to_string())),
  mcp_servers: Some(RawPluginManifestMcpServers::Path("./mcp.json".to_string())),
  interface: Some(RawPluginManifestInterface {
      display_name: Some(name),
      short_description: description.clone(),
      long_description: description,
      developer_name,            // from author.name
      category: Some("Other".to_string()),
      website_url: homepage,
      ..
  ```
  So in Codex's UI, `description` becomes both the subtitle and the details text, `author.name` becomes the publisher, `homepage` becomes the website link, `keywords` pass through, and the category is **"Other"** unless something overrides it. `repository`, `license`, `author.email` and `author.url` are parsed but unused: the struct fields are named `_repository`, `_license`, `_email` and `_url`.
- Two things override the interface. First, `extensions["com.openai"]`, parsed as a legacy Codex manifest, whose `interface` replaces the default and which can also name `apps`, `hooks` and `onboardingSkill`. Second, when no `com.openai` extension is present, a sibling `.codex-plugin/plugin.json` is read as an overlay (`manifest.rs` #L168–L176).

### 1.2 Codex marketplace files, including `.claude-plugin/marketplace.json`

`codex-rs/core-plugins/src/marketplace.rs`:

- #L20–L25: marketplace files are looked for, in this order, at `".agents/plugins/marketplace.json"`, `".agents/plugins/api_marketplace.json"`, `".claude-plugin/marketplace.json"`, `".cursor-plugin/marketplace.json"`.
- Top-level fields read: `name` (required), `interface.displayName` (optional) and `plugins` (required). Per entry: `name`, `source`, `policy` (defaults `installation: AVAILABLE`, `authentication: ON_INSTALL`) and `category`. **Every other entry field** (`description`, `version`, `author`, ...) is flattened into a *manifest fallback*. That fallback is used only when a local plugin has **no** manifest, or to list git/npm sources before install.
- Source forms (#L1020 onward): a plain string path, or objects with `"source"` equal to `local`, `url`, `git-subdir` or `npm`. **Any other source object is `Unsupported`**, and the entry is skipped with `"skipping marketplace plugin with unsupported source"` (#L575). Claude Code's `{"source": "github", "repo": ...}` form is not one of the accepted tags. (This is inferred from the serde enum. It was not run.)
- Local string sources: `"local plugin source path must start with \`./\`"` (#L676). Only `.cursor-plugin/marketplace.json` is exempt from the `./` prefix. Paths may not leave the marketplace root.
- Category (#L945): `// Marketplace taxonomy wins when both sources provide a category.`

### 1.3 Codex's own authoring guidance (bundled skills)

`codex-rs/skills/src/assets/samples/plugin-creator/references/plugin-json-spec.md`. These rules are for the Codex-native `.codex-plugin/plugin.json`, not for Agent Plugins manifests:

- #L205–L206: *"Plugin manifests must include real values for `name`, `version`, `description`, `author.name`, and the required `interface` fields."* `version` *"must use strict semver"*. `websiteURL`, `privacyPolicyURL` and `termsOfServiceURL` *"must be absolute `https://` URLs when present"*. Asset paths *"must point to real files inside the plugin archive"*.
- `interface.defaultPrompt`: *"Include at most 3 strings"* (#L103), *"Each string is capped at 128 characters"*, *"Prefer short starter prompts around 50 characters so they scan well in the UI"* (#L105). Screenshots: *"must be PNG filenames and stored under `./assets/`"* (#L111). The source enforces these as `MAX_DEFAULT_PROMPT_COUNT = 3` and `MAX_DEFAULT_PROMPT_LEN = 128` (`manifest.rs` #L13–L14).
- Marketplace: *"Each generated marketplace entry must include all of: `policy.installation`, `policy.authentication`, `category`"*. *"Treat plugin order in `plugins[]` as render order in Codex."* The entry `name` should *"Match the plugin folder name and `plugin.json` `name`."*
- `scripts/validate_plugin.py` is Codex's plugin validator. It requires a non-empty `name`, strict-semver `version`, `description`, `author.name`, and an `interface` with non-empty `displayName`, `shortDescription`, `longDescription`, `developerName` and `category`, plus `defaultPrompt` and `capabilities`. It also rejects `[TODO: ...]` placeholders, requires each skill's frontmatter `name` and `description` to be non-empty, and rejects `disable-model-invocation` unless it is false.
- `skill-creator/SKILL.md` gives the authoring standard for skills. *"**Keep discovery cheap and precise.** Skill names and descriptions are available before a skill is loaded. Describe the actual capability and when it applies, adding exclusions only when they prevent likely misrouting. Avoid exhaustive capability lists and catchalls that attract unrelated requests."* (#L24). *"**Assume Codex is already capable.** Include only information that changes its decisions..."*. Under *What Not to Include*: *"Avoid adding a `README.md`, installation guide, changelog, duplicated quick reference, or other auxiliary documentation unless a specific task or packaging requirement calls for it."* (#L115). That sentence is about the skill folder, not a plugin package. `skill-creator/scripts/quick_validate.py` checks that the name is at most 64 characters, that the description is at most 1024 characters with no `<` or `>`, and that no TODO placeholders remain.

### 1.4 OpenAI's catalogues

- **`openai/plugins`** is the curated "Codex official" marketplace. `.agents/plugins/marketplace.json` has 65 entries. 62 of them carry only `name`, `source`, `policy` and `category`, and 3 add `interface.displayName`. Categories counted: Developer Tools 27, Productivity 12, Creativity 9, Communication 5, Education & Research 4, Data & Analytics 3, Finance 2, Security 1, Business & Operations 1, Scientific Research 1. **Descriptions, versions and keywords live in each plugin's manifest, not in the catalogue.** Example manifests (`plugins/figma/.codex-plugin/plugin.json`, `plugins/notion/...`) carry `version`, `description`, `author`, `homepage`, `repository`, `license`, `keywords` and a full `interface`: `displayName`, `shortDescription`, `longDescription`, `developerName`, `category`, `capabilities`, `websiteURL`, `privacyPolicyURL`, `termsOfServiceURL`, `defaultPrompt`, `brandColor`, `composerIcon`, `logo`, `logoDark`, `screenshots`.
- **`openai/community-plugins`** has `CONTRIBUTING.md` and `docs/review-and-publish.md`. This is a public submission checklist:
  - *"a plugin is ready only when a new user can understand and verify it from a cold start."*
  - *"Use lower-case kebab-case, and keep the folder name, marketplace entry name, and manifest `name` identical."*
  - *"Add `plugins/<plugin-name>/.codex-plugin/plugin.json` with accurate public metadata, capabilities, authentication behavior, version, repository URL, and license."*
  - *"Include a plugin `README.md` that explains the first safe prompt, prerequisites, permissions, authentication, data boundaries, and failure behavior."*
  - *"Never commit credentials, OAuth tokens, customer data, private URLs, personal paths, or generated caches."*
  - Review checklist: *"Confirm every manifest has accurate publisher, repository, website, version, capability, authentication, and license metadata."* *"Check that plugin docs tell a cold-started Codex task what to do first, what inputs are safe, what it must never do, and how to stop when prerequisites are missing."* *"Identify files read or written, off-machine destinations, and the data sent to each destination."* *"Review each plugin's license and third-party notices before redistribution."* *"skipped checks are not passes."*
  - *"Inclusion in OpenAI's official Plugins Directory requires a separate review."* That review's requirements are at `developers.openai.com/plugins/build/plugins`, which was **not reachable** (§0).
  - Recorded as found: the README of `openai/community-plugins` tells users to add `Source: tonyloehr/community-plugins`, not `openai/community-plugins`.

---

## 2. Hermes Agent (NousResearch)

**Kind of source:** documentation, read as the Markdown source of the blocked site, plus source where it is quoted.

### 2.1 Portable Agent Plugins v1

`website/docs/developer-guide/plugins/index.md` #L45–L110:

- *"Hermes can also install and load directory packages that target the Agent Plugins v1.0.0 format. This is a compatibility adapter for the portable components Hermes already owns."*
- Install flow: `hermes plugins install owner/repository --no-enable`, then `hermes plugins enable <plugin-name>`. *"Portable packages are disabled after installation unless you explicitly enable them."*
- *"Hermes validates `plugin.json`, Agent Skills frontmatter, fixed component locations, `mcp.json`, resolved paths, and symlink containment locally. It does not fetch JSON schemas while loading a package. A bad skill or MCP entry is skipped at its own boundary when valid sibling components can still load."* (#L85)
- *"Values declared in portable MCP `env` are visible package data, not a secret storage mechanism. Do not place credentials in `mcp.json`."* (#L91–L92)
- *"This is an explicit supported subset, not a claim of full Agent Plugins conformance."* (#L110)
- #L748: *"Portable packages use root `plugin.json` in the same locations. Anything deeper is ignored."* The locations are `~/.hermes/plugins/<name>/` or one category level below it.

Source, `hermes_cli/agent_plugins.py`:

- #L48: `_PLUGIN_FIELDS = {"$schema", "name", "version", "description", "author", "homepage", "repository", "license", "keywords", "extensions"}`. Unknown fields produce the diagnostic `"ignored unknown top-level field"`.
- #L152–L162: `"plugin.json must be a regular file within the plugin root"`. A missing or different `$schema` gives `"plugin.json declares an unsupported or missing Agent Plugins schema"`, which is fatal.
- #L186–L204, skill frontmatter: `"name must match the directory and satisfy Agent Skills constraints"` (ASCII regex `^(?!.*--)[a-z0-9]+(?:-[a-z0-9]+)*$`, 1–64 characters). `"description must be a non-empty string of at most 1024 characters"`. `compatibility` must be 1–500 characters. `metadata` must be a string→string map. `allowed-tools` must be a string.

`hermes_cli/plugins_discovery.py` #L30–L35: Hermes **ignores** vendor manifest directories.
*"Per-harness manifest directories plugin repos ship for OTHER agent harnesses (e.g. obra/superpowers keeps one plugin.json per harness). Their plugin.json is not an Agent Plugins v1 manifest and can never validate..."* The set is `{".claude-plugin", ".codex-plugin", ".cursor-plugin", ".devin-plugin", ".kimi-plugin"}`. Searching `hermes-agent` for `.claude-plugin` found only this file and one test. **No evidence was found that Hermes reads `.claude-plugin/marketplace.json`.**

### 2.2 The Hermes plugin catalog: admission rules and what it displays

`plugin-catalog/README.md` gives the admission policy (quoted in part):

1. *"**Human-merged gate.** Entries are added only via a PR to the hermes-agent repository, reviewed and merged by a maintainer."*
2. *"**Exact SHA pins are mandatory.** Every entry pins a full 40-character commit SHA. Branches, tags, and short SHAs are rejected by the loader."* (#L16)
3. *"**No self-updating code.**"* (#L19)
5. *"**Owner-or-major-contributor submissions, or a maintainer-curated sweep.**"* (#L29)
6. *"**Declared capabilities must match reality.** The `capabilities:` block (tools, hooks, middleware, env vars) must match what the plugin actually registers at the pinned commit. Validation fails the entry otherwise — undeclared capability creep is treated as a security issue."* (#L38)
7. *"**The install scanner runs at admission.** ... `dangerous` fails the entry; `caution` findings appear as warnings ..."* (#L42)
9. *"Reviewers read the dependency list at the pinned SHA: bare floors (`>=X` with no upper bound) ... get a request for the oldest API-compatible floor plus an upper bound."*

Entry schema: `name` (`[a-z0-9_-]{1,64}`), `repo` (https only), `sha`, `subdir`, `description` ("One-line description."), `maintainer`, `tier`, `category` (`desktop | memory | platform | web | tools | voice | automation | models | general`), `requires_hermes`, `docs_url`, `version` (*"optional human label for the sha ... shown as "1.4.0 @ abcd1234""*), `image` (2:1, GitHub host), `screenshots` (up to 6), `readme` (*"default true; the README at the PINNED SHA renders on /docs/plugins/<name>"*, #L86), `platforms`, and `capabilities`.

`website/docs/user-guide/features/plugin-catalog.md` describes what the gallery shows:

- *"Browse it visually at /docs/plugins — entries are shelved by category ... with search, tier filters (Official / Community), capability chips, and copyable install commands for every entry."*
- *"Every entry also has its own page at `/docs/plugins/<name>` ...: the full description and any disclosure, the pinned commit, tools, hooks and environment variables, the Desktop install button and CLI command, optional screenshots and the README from the reviewed commit, plus a **More by this author** shelf."* (#L25)
- The `title` field is *"Human name shown on cards ... (optional; defaults to `name`)"*.
- Submission bar (#L218–L224): *"1. **Owner-submitted** ... 2. **A public repository** ... 3. **Released** — the repo has real releases/tags, not just a default branch. 4. **Passing validation** — the catalog validation GitHub Action is green on the PR (schema, SHA format, reachability). 5. **Not self-updating**"*.
- *"Catalog review is a point-in-time review ... It is not a security audit"* (#L113). `plugins.md` #L593: *"Cataloged ≠ audited"*.

A catalogued Agent Plugins package, for example (`plugin-catalog/glasser.yaml`): its `description` carries a disclosure (*"Disclosure — paid data broker: each run tool call charges your Glasser balance..."*), the runtime requirement (*"Requires Node.js 18+"*), and where a token is cached.

### 2.3 Quality tooling

- `hermes plugins doctor [path] --ci` runs the real discovery, parser and registration, and *"reports ... drift between declared and registered tools/hooks"*. `hermes plugins validate` runs the admission checks, including `security scan` and `desktop surface`.
- Install-time scanner (`plugins.md` #L668 onward) gives verdicts `safe` / `caution` / `dangerous`. README prose is down-weighted, but *"Agent-facing shapes keep full severity — prompt injection, Markdown exfil, agent-config edits, `curl … | sh` one-liners ... and so does anything under a bundled `skills/` tree"*.
- An optional advisory scan (`skills.md` #L334 onward) uses NVIDIA SkillEvaluator Tier 1: *"PII detection (leaked emails, personal paths, connection strings), unicode-smuggling detection, script lint, license compliance, and a static security scan"*.
- Hermes's own authoring standard for skills it generates (`skills.md` #L100) is *"≤60-char description, the standard section order, Hermes-tool framing, no invented commands"*. The section order in its template is *When to Use, Procedure, Pitfalls, Verification*. This is a house style for Hermes-authored skills, not an admission rule for third-party packages.
- Skills Hub sources are official, `skills.sh`, well-known endpoints, GitHub taps (the defaults include `anthropics/skills`, `openai/skills`, `NVIDIA/skills`), ClawHub and LobeHub. A tap may ship `skills.sh.json` `groupings`, which *"become the category labels shown in the Skills Hub page"*.

---

## 3. Oh-My-Pi (`can1357/oh-my-pi`)

**Kind of source:** documentation (`docs/`) and source.

- `docs/marketplace.md` #L16: *"A **marketplace** is a Git repository (or local directory) containing a catalog file at `.omp-plugin/marketplace.json` (preferred) or `.claude-plugin/marketplace.json` (Claude Code-compatible fallback)."* It is *"compatible with the Claude Code plugin registry format"*.
- Required catalogue fields (#L123 onward): `name` (*"Lowercase alphanumeric, hyphens, and dots. Must start and end with alphanumeric. Max 64 chars."*), `owner.name`, and `plugins`. `metadata.description`, `metadata.version` and `metadata.pluginRoot` are optional.
- Plugin entry: only `name` and `source` are required. Optional fields are `description`, `version` (*"install version falls back to plugin manifest, source SHA, then `0.0.0`"*, #L140), `author`, `homepage`, `repository`, `license`, `keywords`, `category`, `tags`, `strict`, and more.
- #L158: *"String sources must start with `./` and are resolved inside the marketplace root"*. Accepted source objects are `url`, `github`, `git-subdir` and `npm`. `npm` is parsed but its installation is rejected.
- #L211: *"Invalid catalog JSON or invalid required top-level fields reject the catalog. An invalid plugin entry is logged and skipped"*.
- Upgrades: *"Upgrading all plugins compares only catalog entries that declare `version`. Semver versions must be newer; non-semver versions are treated as changed when unequal."*
- `docs/skills/authoring-marketplaces.md` #L209 shows the plugin layout, including `README.md ← recommended: description + usage`. Its publishing workflow (#L257) is: create the catalogue, push it, and share `owner/repo`. **There is no review, gallery, or quality checklist.**
- **Agent Plugins 1.0.0.** `packages/coding-agent/src/discovery/agent-plugins.ts` is a dedicated provider for *"plugin roots whose root `plugin.json` targets the standard"*. Its priority is 75, *"Above claude-plugins (70) so the standard's semantics win for packages that declare it"* (#L39–L41). `agent-plugin-format.ts` #L90–L126: the **skill frontmatter is closed** to `name`, `description`, `license`, `allowed-tools`, `metadata` and `compatibility`: *"any unexpected key rejects the skill"* (`unexpected frontmatter field "${key}"`). The name must equal the directory (NFKC), be lowercase, be at most 64 characters, and contain no `--`. The description must be at most 1024 characters.
- `docs/skills.md` #L21: *"The runtime only requires `name` and `path` for validity. In practice, matching quality depends on `description` being meaningful."*

---

## 4. Other clients

### 4.1 GitHub Copilot (CLI, cloud agent, app)

**Kind of source:** documentation (`github/docs` source).

- `content/copilot/reference/copilot-cli-reference/cli-plugin-reference.md` #L116: *"The exact `$schema` value `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` opts a plugin into Agent Plugins 1.0 semantics."* Field table: `version`, *"Semantic Versioning is recommended."* `license`, *"An SPDX identifier is recommended."* `keywords`, *"Search and discovery keywords."* #L137: *"Unknown top-level fields are reported and ignored. Component path fields such as `agents`, `skills`, `hooks`, `mcpServers`, and `lspServers` are not Agent Plugins 1.0 manifest fields."* Copilot-only components go in `com.github.copilot/`.
- `about-plugins.md` #L43: *"For a new plugin, use Agent Plugins 1.0 unless you require configurable component paths."*
- Marketplace: `data/reusables/copilot/copilot-cli/cli-claude-plugin-dir.md` says *"Copilot CLI also looks for the `marketplace.json` file in the `.claude-plugin/` directory."* Lookup order (#L371): *"`marketplace.json`, `.plugin/marketplace.json`, `.github/plugin/marketplace.json`, or `.claude-plugin/marketplace.json` (checked in this order)"*. `source`: *"It is not necessary to use `./` at the start of the path."* Required fields are `name`, `owner` and `plugins`. Entry `description` has a *"Max 1024 chars"*. Remote `sha`: *"must be a full 40-character commit SHA. Pin to a `sha` for reproducible installs"* (#L362). `strict` defaults to `true`, meaning *"plugins must conform to the full schema and validation rules"* (#L332).
- `about-plugins.md` explains why a marketplace carries versions: *"Because plugins in a marketplace are versioned, marketplaces make it easy to discover, install, and update plugins"*. The example `marketplace.json` puts a `version` on every entry.
- **awesome-copilot** is added to Copilot CLI by default. `CONTRIBUTING.md`:
  - Quality Guidelines (#L51 onward): *"**Be specific** ... **Test your content** ... **Keep it focused** ... **Write clearly** ..."*
  - Won't accept (#L48): *"**Duplicate Existing Model Strengths Without Meaningful Uplift**: Submissions that mainly tell Copilot to do work frontier models already handle well ..."*
  - External plugin entry requirements (#L239 onward): *"`name`, `description`, and `version` (a valid semantic version ...)"*, *"`author.name`"*, *"`repository` as an HTTPS GitHub URL"*, *"`keywords` as lowercase hyphenated tags"*, `license` *"recommended to be an SPDX identifier or expression"*. It warns on *"marketplace entries whose `source` omits an immutable `ref`/`sha` locator"*.
  - Automated gates (#L256): *"`vally lint` against the submitted plugin path/ref/sha"* and an *"install smoke test via Copilot CLI"*. It runs a *"six-month re-review window"* (#L300).
  - Skills: *"Ensure the `name` matches the folder name ... and the `description` is clear and non-empty"*. Bundled assets *"under 5MB each"*.
  - Its own `plugin.json` example is an Agent Plugins 1.0 manifest (`$schema` agent-plugins.org).
  - Recorded as found: all 162 entries in `awesome-copilot/.github/plugin/marketplace.json` carry `version`, as does `metadata.version`.
- **Vally** (`@microsoft/vally@0.17.0`, from the npm tarball, `dist/skill/graders/spec-compliance.js`) runs these lint checks: `file-length` (`MAX_FILE_LINES = 500`), `name-missing`, `name-length` (64), `name-format`, `name-hyphen-edge`, `name-consecutive-hyphens`, `name-directory-mismatch`, `description-missing`, `description-length` (1024), `compatibility-length` (500), `metadata-type`, and `allowed-tools-type`. `valid-refs` checks that *"all file references in a skill resolve to existing files within the skill directory"*. Two scanners are opt-in: `HTTP-NOT-HTTPS`, `PIPE-TO-SHELL`, `EXTERNAL-DOMAIN` and `SCRIPT-NO-SRI`; and `SCRIPT-FILE`, `INVOKES-SCRIPT` and `NON-BUILTIN-TOOL-REF`. `skill-size` (default 8,000 tokens) exists in the package but is not registered by `runLint`.

### 4.2 Gemini CLI extensions

**Kind of source:** documentation (`docs/extensions/*.md`).

- The format is different: `gemini-extension.json` at the root. **No support for Agent Plugins `plugin.json` or `.claude-plugin/` was found.** `search_code` for `"claude-plugin"` and for `"agent-plugins.org"` in `google-gemini/gemini-cli` returned 0 results.
- Gallery listing (`releasing.md` #L17–L30): *"The Gemini CLI extension gallery automatically indexes public extensions ... You don't need to submit an issue"*. It needs *"a public GitHub repository"*, *"Add the `gemini-cli-extension` topic"*, and *"Place the manifest at the root"*. *"Our system crawls tagged repositories daily. Once you tag your repository, your extension will appear in the gallery if it passes validation."*
- `reference.md` #L141: `description`: *"A short description of the extension. This will be displayed on geminicli.com/extensions."* `name`: *"we expect this name to match the extension directory name."*
- `best-practices.md` #L117: *"Follow Semantic Versioning (SemVer)"*. `releasing.md` #L189: *"always ensure the `version` in `gemini-extension.json` matches your GitHub release tag. While the CLI uses tags for update detection, it displays the manifest version in the UI."*
- Secrets: *"use the `sensitive: true` option"*. Extensions only see env vars *"explicitly declared ... via the `settings` array"*.
- **Not verified:** which fields the gallery card shows, and how it ranks, because `geminicli.com` is blocked.

### 4.3 OpenCode

**Kind of source:** documentation (`packages/web/src/content/docs/*.mdx`).

- Skills (`skills.mdx`): *"Only these fields are recognized: `name` (required), `description` (required), `license`, `compatibility`, `metadata` ... Unknown frontmatter fields are ignored."* The name must match `^[a-z0-9]+(-[a-z0-9]+)*$` and *"Match the directory name"*. *"`description` must be 1-1024 characters. Keep it specific enough for the agent to choose correctly."* The agent sees only name and description in `<available_skills>`.
- Plugins are JS/TS modules loaded from npm or local files. `search_code` for `"claude-plugin"` or `"agent-plugins.org"` in `anomalyco/opencode` returned 0 results, so **no Agent Plugins or Claude marketplace support was found**. The "Ecosystem" page is a PR-curated table of name and description.

### 4.4 Cursor

**Kind of source:** the official plugin repositories. The docs are blocked.

- `cursor/plugin-template` README (#L23–L33): in `plugin.json`, *"set `name` (lowercase kebab-case), `displayName`, `author`, `description`, `keywords`, `license`, and `version`"*. **Submission checklist:**
  *"Each plugin has a valid `.cursor-plugin/plugin.json`. Plugin names are unique, lowercase, and kebab-case. `.cursor-plugin/marketplace.json` entries map to real plugin folders. All frontmatter metadata is present in rule, skill, agent, and command files. Logos are committed and referenced with relative paths. `node scripts/validate-template.mjs` passes. Repository link is ready for submission to the Cursor team."*
- `cursor/plugins/create-plugin/skills/review-plugin-submission/SKILL.md` #L33: *"`README.md` states purpose, installation, and component coverage"*. Its checklist includes *"All declared paths exist and are relative"*, *"No broken file references"*, and *"Plugin scope is clear and focused"*.
- The `cursor/plugins` README table shows `name`, the plugin display name, Author, Category, and *"`description` (from marketplace)"*. Each plugin ships `README.md`, `CHANGELOG.md` and `LICENSE`.
- Agent Plugins 1.0.0: **not verified**. The Cursor docs are unreachable, and the Codex source only shows Codex reading `.cursor-plugin/` paths.

---

## 5. How each client treats an Agent Plugins 1.0.0 package and `.claude-plugin/marketplace.json`

| Client | Root `plugin.json` with Agent Plugins `$schema` | Reads `.claude-plugin/marketplace.json` | Local `source` string | `{"source":"github"}` entries | Source kind |
| :-- | :-- | :-- | :-- | :-- | :-- |
| Codex | Yes. A symlinked root manifest means no plugin. Category shows as "Other" unless the marketplace `category`, `extensions["com.openai"].interface`, or `.codex-plugin/plugin.json` supplies one. | Yes, third in lookup order | Must start with `./` | Unsupported; entry skipped (from the serde enum, not run) | source |
| Hermes | Yes. Regular in-root file, exact `$schema`. Discovered only at `~/.hermes/plugins/<name>/` or one level deeper. | Not found; `.claude-plugin` is ignored as a foreign harness directory | n/a | n/a | docs + source |
| Oh-My-Pi | Yes. Dedicated provider; skill frontmatter closed to six keys. | Yes, as a fallback after `.omp-plugin/` | Must start with `./` | Supported | docs + source |
| GitHub Copilot | Yes, when `$schema` is exact | Yes, fourth in lookup order | `./` optional | Supported, with optional 40-character `sha` | docs |
| Gemini CLI | Not found | Not found | n/a | n/a | docs + code search |
| OpenCode | Not found (skills only, from `.claude/skills` etc.) | Not found | n/a | n/a | docs + code search |
| Cursor | Not verified | Not verified (its own `.cursor-plugin/marketplace.json`) | Bare folder names used in `cursor/plugins` | Not verified | repositories only |
| `npx skills` (skills.sh CLI) | n/a | Yes: *"If `.claude-plugin/marketplace.json` or `.claude-plugin/plugin.json` exists, skills declared in those files are also discovered"* (README #L487), via `skills` arrays and `metadata.pluginRoot` | — | — | docs |

---

## 6. Skill catalogues: inclusion criteria and what a good `SKILL.md` looks like

### 6.1 Agent Skills specification (agentskills.io; `agentskills/agentskills` `docs/`)

- `docs/specification.mdx`: `name` must be 1–64 characters, lowercase alphanumeric and hyphen, with no hyphen at either end, no `--`, and *"Must match the parent directory name"*. `description` must be 1–1024 characters, *"Should describe both what the skill does and when to use it"*, and *"Should include specific keywords that help agents identify relevant tasks"*. Good example: *"Extracts text and tables from PDF files, fills PDF forms, and merges multiple PDFs. Use when working with PDF documents or when the user mentions PDFs, forms, or document extraction."* Poor example: *"Helps with PDFs."*
- #L221–L224: *"Instructions (< 5000 tokens recommended)"*. *"Keep your main `SKILL.md` under 500 lines. Move detailed reference material to separate files."* Validation: `skills-ref validate ./my-skill`.
- `optimizing-descriptions.mdx` #L23 onward: *"**Use imperative phrasing.** ... "Use this skill when..." rather than "This skill does..."*. Also: *"Focus on user intent, not implementation"*, *"Err on the side of being pushy"*, and *"Keep it concise."* For triggering evals: *"Aim for about 20 queries: 8-10 that should trigger and 8-10 that shouldn't"*, including *"near-misses"*.
- `best-practices.mdx`: *"Add what the agent lacks, omit what it knows"*, *"Provide defaults, not menus"*, *"Favor procedures over declarations"*, *"Gotchas sections"*, *"Validation loops"*.

### 6.2 `anthropics/skills`

- No `CONTRIBUTING.md` exists at the root. Top level: `.claude-plugin`, `skills`, `spec`, `template`, `.gitignore`, `README.md`, `THIRD_PARTY_NOTICES.md`. **No inclusion or contribution criteria are stated.**
- README: *"The frontmatter requires only two fields: `name` - A unique identifier for your skill (lowercase, hyphens for spaces); `description` - A complete description of what the skill does and when to use it"*. It carries a skills.sh badge (`https://skills.sh/b/anthropics/skills`).
- The `.claude-plugin/marketplace.json` has `owner`, and `metadata` with `description` and `version: "1.0.0"`. Entries have `description`, `source: "./"`, `strict: false`, and `skills` arrays. There is no `version`, `category`, or `keywords` per entry.

### 6.3 skills.sh (Vercel)

- Read from `vercel-labs/skills`: required frontmatter is `name` and `description`. `metadata.internal: true` hides a skill. Discovery walks `skills/` and about 60 agent directories, up to 3 levels deep. `.claude-plugin/` manifests are honoured. Install telemetry sends repo and skill identifiers *"only for repositories that GitHub positively confirms are public"*. `src/telemetry.ts` #L96–L103 shows that security audits return per-partner `risk: 'safe' | 'low' | 'medium' | 'high' | 'critical' | 'unknown'`.
- *Search-snippet only, unverified:* the leaderboard ranks by install telemetry, as "trending, all-time, and hot". Detail pages show install counts and audits from Gen Agent Trust Hub, Socket and Snyk. Skills flagged malicious are hidden from the leaderboard. The pages behind these claims (`skills.sh`, `vercel.com`) are blocked.

### 6.4 Curated "awesome" lists

- **travisvn/awesome-claude-skills** `CONTRIBUTING.md`: *"if your skill hasn't acquired a basic 10 stars, it will be closed automatically"* (#L108). *"a strong general guideline would be that more exists to the skill than a single `SKILL.md` file"* (#L99). *"No "SaaS Wrappers""* (#L56). *"Include documentation (README or SKILL.md)"*. *"License information (if applicable)"*. PRs must not be AI-submitted.
- **ComposioHQ/awesome-claude-skills** `CONTRIBUTING.md`: *"Solve a real problem"*, *"Be well-documented"*, *"Include examples"*, *"Be tested"*, *"Be safe - Confirm before destructive operations"*, *"Be portable"*. Its template sections are *When to Use This Skill, What This Skill Does, How to Use, Example, Tips*. Entries use a one-sentence description with *"no emojis"*.
- **hesreallyhim/awesome-claude-code** `CONTRIBUTING.md`: *"Be at least 14 days old ... AND show signs of active development ... OR ... Have at least 100 stars"* (#L17–L21). The bot discovers the license: *"If the bot is unable to do so ... is there a properly formatted LICENSE file in the right place?"* Style (#L57): *"Resource descriptions should be written as descriptions - not a sales pitch ... Keep it formatted to one line. Don't use any emojis."*

### 6.5 Skill quality tools

| Tool | What it checks | Source |
| :-- | :-- | :-- |
| `skills-ref validate` | Agent Skills spec compliance | agentskills/agentskills `skills-ref/README.md` (the README says *"intended for demonstration purposes only"*) |
| Vally (`@microsoft/vally-cli lint`) | §4.1 list; used by awesome-copilot on PRs and nightly | npm tarball; `awesome-copilot/.github/workflows/skill-check.yml` #L120 (`npx --yes @microsoft/vally-cli lint "$skill_dir" --verbose`) |
| agent-skill-linter (William-Yeh) | about 20 rules: spec (via skills-ref), LICENSE, `metadata.author`, README Installation/Usage sections, CI workflow, body < 500 lines, *"description starts with "Use when...""*, progressive disclosure, `.claude-plugin/plugin.json` *"exists, parses, has `name` + `version`"* (Rule 24, Error), plain prose without *"marketing superlatives"* (Rule 28) | `skill/SKILL.md` #L154–L179 |
| Codex `quick_validate.py` / `validate_plugin.py` | §1.3 | openai/codex |
| `hermes plugins validate` / `doctor` | §2.3 | hermes-agent docs |
| Cursor `validate-template.mjs` | manifest JSON, kebab-case unique names, `owner.name`, safe relative `source`, frontmatter `name`/`description` on skills, agents and commands, referenced paths exist | cursor/plugin-template |
| NVIDIA SkillEvaluator Tier 1 | PII, unicode smuggling, script lint, license compliance, static security | Hermes `skills.md` #L334 onward (not read at its own repository) |

---

## 7. Quality rubric from other clients and catalogues

Each criterion can be checked against a file. "Matters for" names the clients or catalogues whose source says so. It is not a claim that other clients ignore the criterion.

| # | Criterion (checkable) | Source(s) | Matters for |
| --: | :-- | :-- | :-- |
| 1 | Root `plugin.json` is a **regular file** (not a symlink) inside the plugin root and carries the exact `$schema` `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json`. | Codex `plugin_namespace.rs` #L43–L48; Hermes `agent_plugins.py` #L152–L162; Copilot `cli-plugin-reference.md` #L116; OMP `agent-plugin-format.ts` #L21 | Codex, Hermes, Copilot, OMP |
| 2 | `plugin.json` uses only the ten spec fields. Any other top-level field is dropped with a warning, so it carries nothing. | Codex `agent_plugin_manifest.rs` #L18–L28, #L78; Hermes #L48; Copilot #L137 | Codex, Hermes, Copilot |
| 3 | No optional manifest field is `null`. Codex rejects the whole manifest. | Codex `agent_plugin_manifest.rs` (`"must use its declared type when present"`) | Codex |
| 4 | Plugin `name` is 1–64 characters of `[a-z0-9.-]`, alphanumeric at both ends, with no `--` or `..`. It equals the marketplace entry `name` and the plugin folder name. | Codex #L219; Copilot "Name constraints"; OMP naming rules; openai/community-plugins CONTRIBUTING step 1; Codex plugin-creator spec | Codex, Copilot, OMP, Cursor, openai/community-plugins |
| 5 | `description` is present, non-empty, and at most 1024 characters. It is the subtitle and details text in Codex and the gallery text in Gemini. | Codex `agent_plugin_manifest.rs` #L166–L175; Copilot legacy/marketplace "Max 1024 chars"; Gemini `reference.md` #L141; awesome-copilot #L239 | Codex, Copilot, Gemini, awesome-copilot, Cursor |
| 6 | `author.name` is present. It is Codex's "developerName", is required by awesome-copilot, and is shown in the Cursor catalogue table. | Codex #L160–L180; awesome-copilot #L240; Cursor README table; openai/community-plugins review checklist ("accurate publisher") | Codex, awesome-copilot, Cursor, openai/community-plugins |
| 7 | `version` is present and is SemVer. Where a release tag exists, it equals the tag. | Copilot "Semantic Versioning is recommended"; awesome-copilot #L239 (required semver); Codex `validate_plugin.py` (strict semver, `.codex-plugin`); Gemini `best-practices.md` #L117, `releasing.md` #L189; OMP upgrade semantics | Copilot, awesome-copilot, Codex-native, Gemini, OMP |
| 8 | `license` is an SPDX identifier, and a LICENSE file is present where GitHub license detection can find it. | Copilot ("An SPDX identifier is recommended"); awesome-copilot (warns on non-SPDX); hesreallyhim CONTRIBUTING (bot license discovery); agent-skill-linter Rule 2; openai/community-plugins review checklist | Copilot, awesome-copilot, awesome lists, openai/community-plugins |
| 9 | `homepage` and `repository` are absolute `https://` URLs. `homepage` is Codex's website link, and awesome-copilot requires `repository` to be an HTTPS GitHub URL. | Codex #L177; Codex `validate_plugin.py` https rule; awesome-copilot #L241 | Codex, awesome-copilot |
| 10 | `keywords` is non-empty, in lowercase-hyphenated form. It is passed into Codex marketplace listings and described by Copilot as search keywords. | awesome-copilot #L242; Codex `marketplace.rs` (keywords carried into `MarketplacePlugin`); Copilot field table | Codex, Copilot, awesome-copilot |
| 11 | The marketplace has a valid `name` and `owner.name`. | OMP #L123 onward; Copilot marketplace fields; Cursor `validate-template.mjs` (`Marketplace "owner.name" is required.`) | OMP, Copilot, Cursor |
| 12 | Every local `source` string starts with `./` and resolves inside the marketplace root to an existing plugin directory. Codex and OMP reject strings without `./`; Copilot accepts both forms. | Codex `marketplace.rs` #L676; OMP #L158; Copilot `cli-path-to-plugins.md`; openai/community-plugins review checklist | Codex, OMP, Copilot, Cursor |
| 13 | Marketplace entry names are unique. | Cursor `validate-template.mjs`; Codex plugin-creator | Cursor, Codex |
| 14 | Any non-local `source` pins a full 40-character commit `sha`. A branch alone is not enough. | Hermes catalog README #L16; Copilot #L362; awesome-copilot (immutable ref/sha required for public submissions) | Hermes, Copilot, awesome-copilot |
| 15 | No source uses a form one of the targeted clients cannot read. Codex accepts only a string path or `local`/`url`/`git-subdir`/`npm` objects, and skips `github` objects. | Codex `marketplace.rs` #L575, #L1020 onward | Codex |
| 16 | A category is supplied wherever the target client displays one: marketplace `category` for Codex (otherwise "Other"), `category` for the Hermes catalogue, and category or tags for Copilot and OMP entries. | Codex `agent_plugin_manifest.rs` #L176, `marketplace.rs` #L945; Hermes catalog entry schema; Copilot and OMP entry tables | Codex, Hermes, Copilot, OMP |
| 17 | Skills sit only in immediate children of `skills/`, each with a regular-file `SKILL.md`, and frontmatter `name` equals the directory name. | Hermes `agent_plugins.py` #L186–L258; OMP `docs/skills.md`; Copilot components; OpenCode `skills.mdx`; Vally `name-directory-mismatch`; agentskills spec | Hermes, OMP, Copilot, OpenCode, Vally |
| 18 | Skill frontmatter uses only `name`, `description`, `license`, `compatibility`, `metadata` (string→string) and `allowed-tools` (string). OMP **rejects** a skill with any other key; OpenCode ignores other keys; agent-skill-linter warns on Claude Code-only keys. | OMP `agent-plugin-format.ts` #L90–L126; OpenCode `skills.mdx`; Hermes #L186–L204; agent-skill-linter Rule 1 | OMP (hard), Hermes, OpenCode, linters |
| 19 | The skill `description` is 1–1024 characters and says **what** the skill does and **when** to use it, with task keywords. The imperative form "Use when…" is preferred, and there are no catch-all lists. | agentskills spec; `optimizing-descriptions.mdx` #L23; Codex `skill-creator` #L24; agent-skill-linter Rule 11; OMP `skills.md` #L21 | all skill-loading clients |
| 20 | The `SKILL.md` body is under 500 lines (and under about 5,000 tokens). Detail goes into `references/`, each linked from `SKILL.md` with a note on when to read it. | agentskills spec #L221–L224; Vally `MAX_FILE_LINES = 500`; agent-skill-linter Rules 9, 14, 15; Codex `skill-creator` (progressive disclosure) | Vally/awesome-copilot, linters, all clients |
| 21 | Every file a `SKILL.md` or manifest references exists and resolves inside the skill or plugin directory. | Vally `valid-refs`; Cursor review skill ("No broken file references"); Codex `validate_plugin.py` asset checks; Agent Plugins containment enforced by Hermes | Vally, Cursor, Codex, Hermes |
| 22 | Agent-facing text contains no `http://` URLs, no `curl … \| sh` pipe-to-shell, and no credentials. | Vally `HTTP-NOT-HTTPS`, `PIPE-TO-SHELL`; Hermes install scanner (full severity under `skills/`); openai/community-plugins ("Never commit credentials ... personal paths"); Hermes ("Do not place credentials in `mcp.json`") | Hermes, awesome-copilot, openai/community-plugins |
| 23 | Each plugin has a `README.md` stating its purpose, prerequisites, installation, components it provides, the first safe prompt, permissions and data boundaries, and failure behaviour. The Hermes catalogue renders this README, at the pinned SHA, as the plugin's page. | openai/community-plugins CONTRIBUTING step 4 and review checklist; Cursor review skill #L33; Hermes catalog README #L86 and `plugin-catalog.md` #L25; OMP authoring (README recommended); agent-skill-linter Rules 6–7 | openai/community-plugins, Cursor, Hermes, OMP |
| 24 | The README and descriptions are descriptive prose: no sales pitch, no reader-addressing hooks, no emojis, and no marketing superlatives. | hesreallyhim #L57; ComposioHQ ("no emojis"); agent-skill-linter Rule 28; travisvn ("non-promotional") | awesome lists, linters |
| 25 | The package does something the model cannot already do well: specific, tested, focused, and more than generic advice. | awesome-copilot #L48 and #L51 onward; agentskills best-practices ("Add what the agent lacks"); Codex `skill-creator` ("Assume Codex is already capable"); travisvn ("value-add"); ComposioHQ ("Solve a real problem", "Be tested") | awesome-copilot, awesome lists, all |
| 26 | What the package runs, reads, writes and sends is disclosed and matches the code. Where a catalogue asks, this includes declared capabilities, required environment variables and costs. | Hermes admission rule 6 (#L38) and `glasser.yaml` disclosure; openai/community-plugins review checklist ("Identify files read or written, off-machine destinations"); Gemini (`settings`/`sensitive`) | Hermes, openai/community-plugins, Gemini |
| 27 | The repository is public and has real **releases or tags**, not just a default branch. | Hermes `plugin-catalog.md` #L220–L221; Gemini `releasing.md` #L29 ("crawls tagged repositories") | Hermes catalogue, Gemini gallery |
| 28 | The package passes the target catalogue's validator: `skills-ref validate`, `vally lint`, `hermes plugins validate`/`doctor --ci`, Cursor `validate-template.mjs`, awesome-copilot `npm run plugin:validate`, Codex `validate_plugin.py`. A skipped gate is reported as skipped, not as a pass. | each tool's own source (§6.5); openai/community-plugins ("skipped checks are not passes") | per catalogue |
| 29 | Social proof, for the awesome lists only: at least 10 stars (travisvn), or at least 14 days old with continued commits, or at least 100 stars (hesreallyhim). | travisvn #L108; hesreallyhim #L17–L21 | awesome lists only |

---

## 8. What could not be reached or verified

- **Codex official Plugins Directory review criteria** and the Codex plugin and skills docs (`developers.openai.com`, `help.openai.com`) were blocked. Codex claims here are **from source** at `edd0df90…`, not from documentation. The rejection of `{"source":"github"}` entries is inferred from the serde enum and was not run.
- **Gemini extension gallery**: what a card displays and how it ranks were not read (`geminicli.com` blocked).
- **skills.sh**: leaderboard ranking signals and audit display are known only from search snippets and `telemetry.ts`. The site and the Vercel changelog were blocked.
- **Cursor**: official docs (`cursor.com/docs/reference/plugins`) and marketplace UI blocked. Nothing verified about Agent Plugins 1.0.0 support in Cursor.
- **NousResearch/hermes-plugin-index**: 404. The Hermes catalogue is `hermes-agent/plugin-catalog/`.
- **Hermes CLI install of a plugin that sits in a repository subdirectory** (outside the catalogue's `subdir` field) was not verified.
- **anthropics/skills** states no contribution or inclusion criteria.
- No client was installed or run. Every behaviour above is as documented or as read in source at the cited commit.
