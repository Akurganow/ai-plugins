# 02 — What Claude Code's own documentation says a well-made plugin and marketplace look like

Clean-room research. No local repository was opened; no `git` was run. All reads on **2026-09-24**.
Raw copies of every source read are kept beside this file in `research/src/` (docs pages as `.md`, GitHub files under `src/gh/`).

---

## 0. Sources and reachability

### Claude Code documentation (code.claude.com)

Every page was fetched as Markdown by appending `.md` (`curl https://code.claude.com/docs/en/<page>.md`). All returned HTTP 200; nothing was blocked. The docs index `https://code.claude.com/docs/llms.txt` (200) was used to find pages. These are live pages with no revision identifier: every quote below is **as of 2026-09-24** and can change without notice.

| Page requested | URL actually read | Result |
| :-- | :-- | :-- |
| /discover-plugins | https://code.claude.com/docs/en/discover-plugins.md | 200 |
| /plugins | https://code.claude.com/docs/en/plugins.md | 200 |
| /plugins-reference | https://code.claude.com/docs/en/plugins-reference.md | 200 |
| /plugin-marketplaces | https://code.claude.com/docs/en/plugin-marketplaces.md | 200 |
| /skills | https://code.claude.com/docs/en/skills.md | 200 |
| /desktop | https://code.claude.com/docs/en/desktop.md | 200 |
| /hooks | https://code.claude.com/docs/en/hooks.md | 200 |
| /agents (subagents) | https://code.claude.com/docs/en/sub-agents.md | 200. `/agents` is a different page ("Run agents in parallel"); subagents live at `/sub-agents` according to llms.txt |
| /slash-commands | https://code.claude.com/docs/en/slash-commands.md | 200, **byte-identical to skills.md** (`cmp` reported no difference). Slash commands are documented as skills |
| "plugin eval" | https://code.claude.com/docs/en/plugin-evals.md | 200 |
| "claude plugin validate" | plugins-reference.md §plugin validate and plugin-marketplaces.md §Validation and testing / §Marketplace validation errors | 200 |
| "/skill-doctor" | skills.md §Find unused skills; commands.md | 200. No page of its own |
| "plugin best practices" / "publishing plugins" | no page with either title exists in llms.txt; the content is in plugins.md §Share your plugins / §Submit your plugin to the community marketplace, and plugins-reference.md §Distribution and versioning reference | — |
| extras | plugin-dependencies.md, plugin-hints.md, plugin-relevance.md, security.md, commands.md, features-overview.md, claude-directory.md, whats-new/2026-w37.md | all 200 |

### Anthropic marketplace repositories (GitHub)

- Read with `curl https://raw.githubusercontent.com/anthropics/<repo>/main/<path>`. All requests listed returned 200 unless stated otherwise.
- **The commit SHA could not be pinned.** `api.github.com/repos/anthropics/claude-plugins-official/commits/main` returned HTTP 403 with `"GitHub access to this repository is not enabled for this session."` The Atom feed `github.com/anthropics/claude-plugins-official/commits/main.atom` returned 403. The GitHub MCP `list_commits` returned `Access denied: repository "anthropics/claude-plugins-official" is not configured for this session.` Running `git` was not allowed. So every GitHub citation below means **branch `main` as fetched 2026-09-24**, not a commit permalink.

| File | Result |
| :-- | :-- |
| anthropics/claude-plugins-official `README.md` | 200 |
| anthropics/claude-plugins-official `.claude-plugin/marketplace.json` | 200 (187,501 bytes, 312 plugins) |
| anthropics/claude-plugins-official `CONTRIBUTING.md` | **404**: the file does not exist on `main` |
| `plugins/{example-plugin,commit-commands,plugin-dev,skill-creator}/.claude-plugin/plugin.json`, `README.md`, `LICENSE` | all 200 |
| `plugins/{example-plugin,commit-commands,plugin-dev,skill-creator}/CHANGELOG.md` | **all 404** |
| anthropics/claude-plugins-community `README.md`, `.claude-plugin/marketplace.json` | 200 (catalog is 1,565,989 bytes, 2,282 plugins) |

### Anthropic blog / engineering posts

| URL | Result |
| :-- | :-- |
| https://www.anthropic.com/news/claude-code-plugins | 308 redirect to https://claude.com/blog/claude-code-plugins (200). WebFetch dates the post October 9, 2025 |
| https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 200. WebFetch dates the post October 16, 2025 |

The quotes from these two posts were taken from the raw HTML with `curl`, not from WebFetch's summary.

---

## 1. `marketplace.json` — every documented field

Source: https://code.claude.com/docs/en/plugin-marketplaces (§Marketplace schema, §Plugin entries, §Plugin sources, §Strict mode, §Rename or remove a plugin).

Location: "Create `.claude-plugin/marketplace.json` in your repository root. This file defines your marketplace's name, owner information, and a list of plugins with their sources."

### 1.1 Top-level required fields

| Field | Docs text (quoted) |
| :-- | :-- |
| `name` (string) | "Marketplace identifier in kebab-case, with no spaces, control characters, or bidirectional-formatting characters. This is public-facing: users see it when installing plugins (for example, `/plugin install my-tool@your-marketplace`). Each user can register only one marketplace per name: when they add a second marketplace with the same name, Claude Code replaces the first." |
| `owner` (object) | "Marketplace maintainer information." Sub-fields: `name` **required** ("Name of the maintainer or team"); `email` optional ("Contact email for the maintainer"); `url` optional ("Website, GitHub profile, or organization URL") |
| `plugins` (array) | "List of available plugins" |

Name constraints:
- Reserved names: "`claude-code-marketplace`, `claude-code-plugins`, `claude-plugins-official`, `claude-plugins-community`, `claude-community`, `anthropic-marketplace`, `anthropic-plugins`, `agent-skills`, `anthropic-agent-skills`, `knowledge-work-plugins`, `life-sciences`, `claude-for-legal`, `claude-for-financial-services`, `financial-services-plugins`, `first-party-plugins`, `claude-tag-plugins`, `healthcare`. Names that impersonate official marketplaces, such as `official-claude-plugins` or `anthropic-plugins-v2`, are also blocked."
- "You also can't name a marketplace `npm`, `pip`, `uv`, `cargo`, `github`, or `gh`, in any casing. This check requires Claude Code v2.1.275 or later."
- Validator warning: "`Marketplace name "x" is reserved in Claude Desktop`: the marketplace is named `org`, `org-provisioned`, or `unknown`, in any casing."
- Validator warning: "Claude Desktop accepts names of up to 128 characters made of letters, digits, `.`, `_`, and `-`, starting with a letter or digit. Claude Code accepts other forms, but Claude Desktop's managed marketplace sync rejects a marketplace whose name fails the check and silently drops a plugin entry whose name does."

### 1.2 Top-level optional fields

| Field | Docs text (quoted) |
| :-- | :-- |
| `$schema` | "JSON Schema URL for editor autocomplete and validation. Claude Code ignores this field at load time." (The docs name no URL for the marketplace schema. The official catalog uses `https://anthropic.com/claude-code/marketplace.schema.json`, which answered HTTP 301 to `curl` without `-L`; the redirect target was not followed.) |
| `description` | "Brief marketplace description". Validator warning when it is missing: "`No marketplace description provided`: add a top-level `description` to help users understand your marketplace" |
| `version` | "Marketplace manifest version" |
| `metadata.pluginRoot` | "Directory that Claude Code resolves bare plugin source names under. See Relative paths. Requires Claude Code v2.1.239 or later." |
| `allowCrossMarketplaceDependenciesOn` | "Other marketplaces that plugins in this marketplace may depend on. Dependencies from a marketplace not listed here are blocked at install." |
| `renames` | "Map from a former plugin `name` to its current name, or to `null` if the plugin was removed. Lets existing users migrate automatically when you rename or remove an entry in `plugins`. … Requires Claude Code v2.1.193 or later." |

"`description` and `version` are also accepted under `metadata` for backward compatibility."

On `renames`: "Treat `renames` as append-only history: keep old entries in place even after you expect every user to have migrated." And: "Run `claude plugin validate .` after editing the map; it rejects any entry whose chain forms a cycle or doesn't terminate at `null` or a name listed in `plugins`."

### 1.3 Plugin entry: required

"Each plugin entry needs at minimum a `name` and a `source`."

| Field | Docs text (quoted) |
| :-- | :-- |
| `name` | "Plugin identifier in kebab-case, with no spaces, control characters, or bidirectional-formatting characters. This is public-facing: users see it when installing (for example, `/plugin install my-plugin@marketplace`)." Validator warning: "`Plugin name "x" is not kebab-case`: … Claude Code accepts other forms, but the claude.ai marketplace sync rejects them." |
| `source` | "Where to fetch the plugin from" |

Stability rule: "A plugin's `name` is its stable identifier. Users reference it in `enabledPlugins`, `pluginConfigs`, and `/plugin install` commands, so changing it breaks every existing install. To change the label shown in the UI without breaking installs, set `displayName` and keep `name` unchanged."

### 1.4 Plugin entry: optional

"You can include any field from the plugin manifest schema, such as `description`, `version`, `author`, `commands`, and `hooks`, plus these marketplace-specific fields: `source`, `category`, `tags`, `strict`, `relevance`, `headers`, and `headersHelper`."

**Standard metadata fields** (quoted from the table):

| Field | Docs text |
| :-- | :-- |
| `displayName` | "Human-readable name shown in UI surfaces. When neither the entry nor the plugin's `plugin.json` sets one, users see the plugin's `name`. May contain spaces and any casing. Not used for namespacing or lookup." |
| `description` | "Brief plugin description" |
| `version` | "Plugin version. If set (here or in `plugin.json`), the plugin is pinned to this string and users only receive updates when it changes. A plugin with a `command` source isn't pinned by either field. Neither is a plugin loaded in place from a marketplace added as a local directory." |
| `author` | "Plugin author information (`name` required; `email` and `url` optional)" |
| `homepage` | "Plugin homepage or documentation URL" |
| `repository` | "Source code repository URL" |
| `license` | "SPDX license identifier (for example, MIT, Apache-2.0)" |
| `keywords` | "Tags for plugin discovery and categorization" |
| `metadata` | "Free-form object for your own fields, such as entitlement or catalog data. Claude Code doesn't read it." |
| `category` | "Plugin category for organization" |
| `tags` | "Tags for searchability" |
| `strict` | "Controls whether `plugin.json` is the authority for component definitions (default: true)." |
| `relevance` | "Signals that tell Claude Code when to suggest this plugin to users. Takes effect only for marketplaces an administrator allowlists in managed settings." |
| `defaultEnabled` | "Whether the plugin is enabled after install (default: true). Set to `false` to install the plugin disabled until the user opts in. Takes precedence over the same field in the plugin's `plugin.json`." |

**Component configuration fields**: `skills` ("Custom paths to skill directories containing `<name>/SKILL.md`"), `commands` ("Custom paths to flat `.md` skill files or directories"), `agents` ("Custom paths to agent files"), `hooks` ("Custom hooks configuration or path to hooks file"), `mcpServers` ("MCP server configurations or path to MCP config"), `lspServers` ("LSP server configurations or path to LSP config").

**Archive authentication fields**: `headers` ("HTTP headers Claude Code sends when it downloads this entry's archive"), `headersHelper` ("Command that prints the HTTP headers for this entry's archive download … The entry must also set `"strict": false`").

**What the docs list as not documented**: the docs name **no** allowed values for `category` and no length limit for `description`. The docs name no field called `pluginRoot` at top level; it is `metadata.pluginRoot`.

### 1.5 Precedence between the entry and `plugin.json`, and what users see before install

"Both the entry and the plugin's own `plugin.json` can set the display fields `displayName`, `description`, `author`, `homepage`, `repository`, `license`, and `keywords`. In plugin listings and details, before and after install:
* For a field you set on the entry, users see the entry's value, even when `plugin.json` sets a different one.
* For a field the entry leaves unset, users see the `plugin.json` value.

Before install, Claude Code can read `plugin.json` only for entries with a relative-path source, whose plugin files live inside the marketplace itself. For an entry with any other source type, users see only the entry's own fields until they install the plugin."

For `version` the rule is the other way round (plugins-reference §Metadata fields): "If also set in the marketplace entry, `plugin.json` wins." And plugin-marketplaces §Version resolution: "Avoid setting `version` in both `plugin.json` and the marketplace entry. Claude Code always uses the `plugin.json` value without warning, so a stale manifest version can mask a version you set in `marketplace.json`." The validator "warns when the entry's `version` doesn't match the one in `plugin.json`."

### 1.6 Plugin sources

| Source | Fields | Docs notes (quoted) |
| :-- | :-- | :-- |
| Relative path | string | "Must start with `./`, unless you write a bare name under `metadata.pluginRoot`. Claude Code resolves the path relative to the marketplace root, not the `.claude-plugin/` directory" |
| `github` | `repo`, `ref?`, `sha?` | `sha`: "Full 40-character git commit SHA to pin to an exact version" |
| `url` | `url`, `ref?`, `sha?` | "Git URL source" |
| `git-subdir` | `url`, `path`, `ref?`, `sha?` | "Clones sparsely to minimize bandwidth for monorepos" |
| `npm` | `package`, `version?`, `registry?` | "fetched with your npm client and unpacked without running install scripts" |
| `archive` | `url`, `sha256?` | "Zip archive downloaded over HTTPS … Requires Claude Code v2.1.224 or later" |
| `command` | `command`, `timeout?`, `mode?` | "re-run once per session to pick up changes. Requires Claude Code v2.1.229 or later" |

- "When both `ref` and `sha` are set on any of them, the `sha` is the effective pin."
- "Don't use `../` to reference paths outside the marketplace root. On macOS and Linux, Claude Code refuses an entry path with a backslash anywhere past the leading `./`."
- URL-hosted marketplaces: "If users add your marketplace via a direct URL to the `marketplace.json` file, relative paths won't resolve, because Claude Code downloads only that file."
- Hosting: "The clone never downloads Git LFS content, so LFS-tracked files arrive as pointer files. Keep the files your plugins need out of LFS." "GitHub is the recommended way to host and distribute a marketplace."
- For claude.ai organization distribution: "Don't include a top-level `bin/` directory in any plugin you distribute through organization settings. claude.ai rejects a plugin that has one."

### 1.7 Strict mode

"`true` (default): `plugin.json` is the authority. The marketplace entry can supplement it with additional components, and both sources are merged." / "`false`: The marketplace entry is the entire definition. If the plugin also has a `plugin.json` that declares components, that's a conflict and the plugin fails to load."

### 1.8 Caching and update behaviour

- "Claude Code copies each installed plugin into the local versioned plugin cache at `~/.claude/plugins/cache`, unless the plugin loads in place."
- plugins-reference §Version management: "Claude Code uses the plugin's version as the cache key that determines whether an update is available. When you run `/plugin update` or auto-update fires, Claude Code computes the current version and skips the update if it matches what's already installed."
- Resolution order (except `command`): "1. The `version` field in the plugin's `plugin.json` 2. The `version` field in the plugin's marketplace entry in `marketplace.json` 3. The git commit SHA of the plugin's source, for `github`, `url`, `git-subdir`, and relative-path sources in a git-hosted marketplace 4. The SHA-256 digest, for `archive` sources … 5. `unknown` …"
- Warning: "If you declare `"version": "1.0.0"` in `plugin.json` and push new commits without changing that string, existing users of those sources keep the cached copy, because Claude Code sees the same version. Bump the field on every release, or omit it to fall back to the resolved version."
- Auto-update (discover-plugins §Configure auto-updates): "`claude-plugins-official`, most other official Anthropic marketplaces, and marketplaces added from claude.ai have auto-update enabled by default. Other third-party marketplaces and local development marketplaces have auto-update disabled by default."
- Old versions: "Claude Code marks the previous version directory as orphaned and removes it in a background sweep roughly 14 days later."

---

## 2. `plugin.json` (`.claude-plugin/plugin.json`)

Source: https://code.claude.com/docs/en/plugins-reference §Plugin manifest schema.

"The manifest is optional. If omitted, Claude Code auto-discovers components in default locations and derives the plugin name from the directory name. Use a manifest when you need to provide metadata or custom component paths."

### 2.1 Required

"If you include a manifest, `name` is the only required field." `name`: "Unique identifier in kebab-case, with no spaces, control characters, or bidirectional-formatting characters. When a marketplace entry lists the plugin under a different name, the marketplace entry name is what `enabledPlugins` keys and `/plugin` use." "This name is used for namespacing components. For example, in the UI, the agent `agent-creator` for the plugin with name `plugin-dev` will appear as `plugin-dev:agent-creator`."

### 2.2 Metadata fields (quoted)

| Field | Docs text |
| :-- | :-- |
| `$schema` | "JSON Schema URL for editor autocomplete and validation. Claude Code ignores this field at load time." Example `"https://json.schemastore.org/claude-code-plugin-manifest.json"` |
| `displayName` | "Human-readable name shown in the `/plugin` picker and other UI surfaces. For a marketplace-installed plugin, a `displayName` on the marketplace entry takes precedence over this value." |
| `version` | "Optional. Semantic version. Setting this pins the plugin to that version string, so users only receive updates when you bump it … If also set in the marketplace entry, `plugin.json` wins." |
| `description` | "Brief explanation of plugin purpose". plugins.md: "Shown in the plugin manager when browsing or installing plugins." |
| `author` | "Author information". plugins.md: "Optional. Helpful for attribution." |
| `homepage` | "Documentation URL" |
| `repository` | "Source code URL" |
| `license` | "License identifier" |
| `keywords` | "Discovery tags" |
| `metadata` | "Free-form object for your own data … Claude Code doesn't read it, so the values never affect plugin behavior." |
| `defaultEnabled` | "Whether the plugin starts in an enabled state when the user has not set one. Defaults to `true`." Guidance: "Use this for plugins that add cost or scope a user should opt into, such as one that connects to an external service." |

### 2.3 Component path fields

`skills` ("Adds to the default `skills/` scan"), `commands` ("replaces default `commands/`"), `agents` ("replaces default `agents/`"), `workflows`, `hooks`, `mcpServers`, `outputStyles`, `lspServers`, `experimental.themes`, `experimental.monitors`, `experimental.evals`, `userConfig`, `channels`, `dependencies`.

Path rules: "All paths must be relative to the plugin root and start with `./`, except that the `skills` field also accepts `"."`." "Claude Code rejects a component path that resolves outside the plugin root … That covers a path that points outside the plugin as written, such as `../shared-utils`, and a symlink that leads outside the plugin, other than links within one marketplace." "On macOS and Linux, Claude Code also rejects a component path that contains a backslash anywhere in it."

`userConfig`: "Use this instead of requiring users to hand-edit `settings.json`." Each option requires `type`, `title`, `description`; `sensitive: true` "masks input and stores the value in secure storage instead of `settings.json`."

### 2.4 Unrecognized and mistyped fields

"Claude Code ignores top-level fields it does not recognize." "`claude plugin validate` reports unrecognized fields as warnings, not errors. If a field is one or two characters off from a recognized one, the warning suggests the likely intended name." "Most fields: the plugin fails to load. For example, a `keywords` value that is a string instead of an array is a load error." "Pass `--strict` to treat warnings as errors. Use it in CI to catch a misspelled field name or a field left over from another tool's manifest before publishing."

### 2.5 Which surfaces display which field

What the docs actually say:
- `/plugin` **Discover** tab details pane (discover-plugins): "A **Context cost** estimate …", "The plugin's **Last updated** date", "A **Will install** section listing the plugin's commands, agents, skills, hooks, and MCP and LSP servers". "For plugins from local or custom marketplaces, you may not see the **Context cost** and **Last updated** rows, and the **Will install** section may show **Components will be discovered at installation** instead."
- `/plugin` **Installed** tab: "type to filter by plugin name or description".
- `description`: "Shown in the plugin manager when browsing or installing plugins" (plugins.md).
- `displayName`: "shown in the `/plugin` picker and other UI surfaces".
- `homepage`: discover-plugins tells users to "Check each plugin's homepage for more information" and "visit its homepage for usage guidance".
- `claude plugin details` prints name, version, description, source, component inventory, and token cost (the sample output shows `dependency-guard 1.2.0 / Dependency analysis for Claude Code sessions / Source: dependency-guard@example-marketplace`).
- `claude plugin list`: "List installed plugins with their version, source marketplace, and enable status."
- **Desktop app** (desktop.md §Install plugins): "select **Add plugin** from the submenu to open the plugin browser, which shows available plugins from your configured marketplaces including the official Anthropic marketplace." **The desktop docs do not say which manifest fields the browser displays. Not verified.**
- **claude.com/plugins** catalog: the docs link to it but say nothing about which fields it renders. Not read, so not verified.
- No page says where `license`, `repository`, `keywords`, `category`, or `tags` appear in any UI. **Not verified.**

---

## 3. Plugin layout, naming, docs, and tooling

### 3.1 Components and default locations (plugins-reference §File locations reference)

Manifest `.claude-plugin/plugin.json`; Skills `skills/` ("Skills with `<name>/SKILL.md` structure"); Commands `commands/` ("Skills as flat Markdown files. Use `skills/` for new plugins"); Agents `agents/`; Workflows `workflows/`; Output styles `output-styles/`; Themes `themes/`; Hooks `hooks/hooks.json`; MCP `.mcp.json`; LSP `.lsp.json`; Monitors `monitors/monitors.json`; Executables `bin/`; Settings `settings.json` ("Only the `agent` and `subagentStatusLine` keys are supported").

- "The `.claude-plugin/` directory contains the `plugin.json` file. All other directories … must be at the plugin root, not inside `.claude-plugin/`."
- **Rules / CLAUDE.md**: "A `CLAUDE.md` file at the plugin root is not loaded as project context. Plugins contribute context through skills, agents, and hooks rather than CLAUDE.md." `claude plugin validate` "also warns about a `CLAUDE.md` at the plugin root." No `rules/` plugin component is documented.
- The standard layout example ends with "`LICENSE                  # License file`" and "`CHANGELOG.md             # Version history`".
- Plugin agents: "**Not supported, for security reasons**: `hooks`, `mcpServers`, and `permissionMode`."
- Node dependencies: "The install runs only when the plugin's root directory contains both a `package.json` and a supported lockfile." "Ship an npm lockfile for the widest reach."

### 3.2 Namespacing

- "Plugin skills are namespaced with the plugin name." e.g. `/quality-review-plugin:quality-review`.
- plugins.md table: Standalone `/hello` vs Plugins `/plugin-name:hello`.
- Agents: "`agents/review/security.md` in a plugin named `my-plugin` loads as `my-plugin:review:security`."
- Plugin MCP tools: "`mcp__plugin_<plugin-name>_<server-name>__<tool>`" (hooks.md).
- Skill command name: "In a plugin skill, `name` sets the last segment of the command and the plugin prefix stays in place."

### 3.3 Skill authoring guidance (skills.md)

- "All fields are optional. Only `description` is recommended so Claude knows when to use the skill."
- `description`: "Put the key use case first: the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing."
- "Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files."
- "Reference supporting files from `SKILL.md` so Claude knows what each file contains and when to load it."
- Portability: outside Claude Code, only "`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`" are accepted. "If you include any field the spec doesn't allow, packaging or upload fails with a hard error."
- Troubleshooting: "Check the description includes keywords users would naturally say".

### 3.4 README, CHANGELOG, LICENSE

- README: plugins.md §Share your plugins: "1. **Add documentation**: Include a `README.md` with installation and usage instructions". This is the only mention of README in the plugin docs pages read.
- CHANGELOG: plugins-reference §Version management: "If you use explicit versions, follow semantic versioning (`MAJOR.MINOR.PATCH`): bump MAJOR for breaking changes, MINOR for new features, PATCH for bug fixes. Document changes in a `CHANGELOG.md`." It also appears in the standard layout.
- LICENSE: appears only in the standard layout ("`LICENSE # License file`") and as the `license` field. No stated requirement.

### 3.5 `claude plugin validate`

- "Check a plugin or a marketplace for syntax and schema errors before publishing." Exits "0 when validation passes, 1 when it fails, and 2 when the validation run itself fails". `--strict`: "Treat warnings as errors and exit 1 on them. Use in CI". `--json` needs v2.1.259 or later.
- Plugin directory with `plugin.json`: checks "`plugin.json`, `hooks/hooks.json`, and the `skills`, `agents`, and `commands` directories at the plugin root".
- Marketplace directory: "checks `marketplace.json` for schema errors, duplicate plugin names, and source path traversal. For each entry whose `source` is a local path, it also validates that plugin's own `plugin.json` and warns when the entry's `version` doesn't match the one in `plugin.json`."
- Limitation: "From a marketplace directory, Claude Code doesn't open the plugins' skill, agent, command, or hook files." So each plugin directory needs its own run.
- Limitation: "When you run `claude plugin validate` against a plugin directory, Claude Code doesn't check a `SKILL.md` at the plugin root."
- Limitation: "Claude Code doesn't follow symlinks inside the directory you name."
- Limitation: "For paths you set through the component path fields in `plugin.json`, Claude Code checks that each path exists but doesn't read the files there."
- Errors listed: invalid JSON; "Duplicate plugin name"; "`plugins[0].source: Path contains ".."`"; control or bidi characters in names. Warnings listed: "Marketplace has no plugins defined", "No marketplace description provided", "Plugin name "x" is not kebab-case", Desktop reserved names, Desktop name charset.
- The community submission pipeline runs the same check: "The review pipeline runs the same check on every submission, along with automated safety screening."

### 3.6 `claude plugin eval` (v2.1.269+; source https://code.claude.com/docs/en/plugin-evals)

- "runs your plugin against a suite of test cases and scores the results. Each case is a realistic prompt plus one or more graders."
- Location: "An eval suite lives in a directory called `evals/` inside your plugin". `experimental.evals` in the manifest overrides the location.
- Baseline: "each case's runs are repeated with no plugin loaded by default, and you get two scores, `WITH` and `W/OUT`. Their difference, `Δ`, is what the plugin contributed. If a case scores 1.0 both with and without the plugin, the plugin isn't what made it pass."
- Grader types: `regex`, `tool_used`, `tool_order`, `file_exists`, `llm`, `baseline`.
- CI: "run the suite with `--json` … Pass `--trust-plugin` … pin both models so scores are comparable over time, keep the report local, and set a cost ceiling".
- Requirement: "A plugin directory with a `plugin.json` or `.claude-plugin/plugin.json` manifest, or a skills-directory plugin."
- Cost: "Every eval run and every judge grader is a real model call on your account".
- plugin-marketplaces §Validation and testing: "Validation checks file structure; to test whether a plugin changes what Claude does on realistic prompts, run its eval suite with `claude plugin eval` before you publish a new version."
- The format is separate from skill-creator's: "Its case format is separate from the `evals/evals.json` file the skill-creator plugin uses."

### 3.7 `/skill-doctor`

skills.md §Find unused skills: "Run `/skill-doctor` to see what each of your skills costs and how often it gets used, so you can decide which ones to turn off." "It flags skills in the listing that have never been invoked and says where to turn them off. … The report also lists plugins you haven't used recently." Requires v2.1.252 or later. **This is a tool for the user's installed skills, not an authoring or quality checker for a published plugin.** It checks nothing about a marketplace's files.

Related: `claude plugin details <name>` shows "a plugin's component inventory and projected token cost", split into "**Always-on:** tokens added to every session by the plugin's listing text, such as skill descriptions, agent descriptions, and command names".

### 3.8 Testing recommendations

- `claude --plugin-dir ./my-plugin`; "run `/reload-plugins` to pick up the updates without restarting."
- "Try your skills with `/plugin-name:skill-name`"; "Check that agents appear in `/context` under Custom Agents"; "Trigger the event each hook matches".
- Marketplace: "Test your marketplace before sharing." Run `claude plugin validate .`, `/plugin marketplace add ./path/to/marketplace`, then `/plugin install test-plugin@marketplace-name`.
- "**Test with others**: Have team members test the plugin before wider distribution".
- `claude --debug` "shows: Which plugins are being loaded, Any errors in plugin manifests, Skill, agent, and hook registration, MCP server initialization".

### 3.9 Distribution and versioning recommendations

- Three strategies (plugins-reference): **Explicit version** "Best for: Published plugins with stable release cycles"; **Commit-SHA version** (omit `version`) "Internal or team plugins under active development"; **Digest version** for `archive` sources.
- Release tags for dependency resolution (plugin-dependencies.md): "Tag each release as `{plugin-name}--v{version}`, where `{version}` matches the `version` field in that commit's `plugin.json`." `claude plugin tag --push`.
- Release channels: "Each channel must resolve to a different version."
- Community marketplace submission (plugins.md): forms at claude.ai and platform.claude.com/plugins/submit. "Approved plugins are pinned to a specific commit SHA … and CI bumps the pin automatically as you push new commits to your repository."
- Official marketplace: "Anthropic decides which plugins to include at its discretion. There is no application process".

### 3.10 Security notes

- discover-plugins §Security: "Plugins and marketplaces are highly trusted components that can execute arbitrary code on your machine with your user privileges. Only install plugins and add marketplaces from sources you trust."
- discover-plugins §Install plugins (Warning): "Make sure you trust a plugin before installing it. Anthropic doesn't control what MCP servers, files, or other software are included in plugins and can't verify that they work as intended. Check each plugin's homepage for more information."
- Reserved names exist "to prevent a third-party marketplace from presenting itself as an Anthropic-published source."
- Caching: "For security and verification purposes, Claude Code copies marketplace plugins to the user's local plugin cache". Symlinks: "**Outside the marketplace:** the symlink is skipped for security."
- Dependency install: "`--ignore-scripts` keeps `preinstall`, `install`, and `postinstall` scripts from running".
- `userConfig`: "Fields that run in a shell reject `${user_config.*}`: substituting a configured value into a shell command would let the shell run whatever that value contains". Hooks: use exec form with `args`, or quote paths.
- `pluginConfigs` in project settings are ignored "so a cloned repository could supply values there, and those values would flow into plugin hook commands".
- Project-scope skills-directory plugins load "only after you accept the workspace trust dialog".
- Managed controls: `strictKnownMarketplaces`, `disableSideloadFlags`, `disableCommandPluginSources`.
- Agent Skills engineering post: "We recommend installing skills only from trusted sources. When installing a skill from a less-trusted source, thoroughly audit it before use. Start by reading the contents of the files bundled in the skill to understand what it does, paying particular attention to code dependencies and bundled resources like images or scripts."

---

## 4. Anthropic's own marketplaces

All read from `main` on 2026-09-24; commit SHA not obtainable (see §0).

### 4.1 `anthropics/claude-plugins-official`

**README.md (quoted):**
- "A curated directory of high-quality plugins for Claude Code."
- "**⚠️ Important:** Make sure you trust a plugin before installing, updating, or using it. Anthropic does not control what MCP servers, files, or other software are included in plugins and cannot verify that they will work as intended or that they won't change. See each plugin's homepage for more information."
- Structure: "`/plugins` - Internal plugins developed and maintained by Anthropic"; "`/external_plugins` - Third-party plugins from partners and the community".
- Installation: "To install, run `/plugin install {plugin-name}@claude-plugins-official`".
- Contributing: "Internal plugins are developed by Anthropic team members. See `/plugins/example-plugin` for a reference implementation." "External plugins must meet quality and security standards for approval. To submit a new plugin, use the plugin directory submission form." The standards themselves are not published in the repo, and there is no `CONTRIBUTING.md` (404).
- Plugin structure block: "`.claude-plugin/plugin.json # Plugin metadata (required)`", "`.mcp.json`", "`commands/`", "`agents/`", "`skills/`", "`README.md # Documentation`".
- "## Plugin names are immutable": "The `name` field in a marketplace entry is an **immutable slug**. Once a plugin has been published, its `name` must not change … To change how a plugin is labeled in the UI, set or update `displayName` instead." A `renames` map is used for unavoidable renames.
- "## License": "Please see each linked plugin for the relevant LICENSE file."

**marketplace.json (measured with a script):**
- Top level: `$schema: "https://anthropic.com/claude-code/marketplace.schema.json"`, `name: "claude-plugins-official"`, `description: "Directory of popular Claude Code extensions including development tools, productivity plugins, and MCP integrations"`, `owner: {name: "Anthropic", email: "support@anthropic.com"}`, `plugins` (312), `renames` (9 entries, e.g. `"adlc": "agentforce-adlc"`). There is no top-level `version` or `metadata`.
- Field frequency across 312 entries: `name` 312, `description` 312, `source` 312, `category` 298, `homepage` 296, `author` 230, `displayName` 14, `strict` 14, `version` 14, `lspServers` 12, `skills` 3, `tags` 3, `keywords` 1. **No entry sets `license` or `repository`.**
- `version` appears only on the 13 `*-lsp` entries plus `cwc-makers` (all `"1.0.0"`) and `security-guidance` (`"2.0.7"`). Every other entry relies on the commit-SHA fallback.
- Categories used: development 123, productivity 67, database 39, monitoring 22, security 18, deployment 9, design 8, automation 3, learning 3, location 2, testing 2, migration 1, math 1, none 14. They are single lowercase words.
- `tags` is used only as `["community-managed"]` (3 entries).
- Sources: `url` 162, `git-subdir` 98, relative path 52. **All 260 external sources carry a 40-character `sha`.** Some also carry a `ref`, e.g. `"ref": "v1.5.5"`.
- Description length: minimum 34, median 182, maximum 665 characters. The style is one or two sentences that say what the plugin does, often naming the product. Examples: `"commit-commands"`: "Commands for git commit workflows including commit, push, and PR creation"; `"skill-creator"`: "Create new skills, improve existing skills, and measure skill performance. Use when users want to …".
- `homepage` points either at the plugin's directory on GitHub (for internal plugins, e.g. `https://github.com/anthropics/claude-plugins-public/tree/main/plugins/commit-commands`) or at a vendor site. The 16 entries without one are the LSP plugins and a few channel plugins (discord, telegram, imessage, fakechat).
- `author` is `{name, email}` for Anthropic entries and `{name}` for third parties.

**Example plugins (`plugins/<name>/`):**

| Plugin | `plugin.json` fields | README | LICENSE | CHANGELOG |
| :-- | :-- | :-- | :-- | :-- |
| example-plugin | name, description, author | 69 lines | Apache 2.0 | 404 |
| commit-commands | name, description, author | 225 lines (Overview, Commands, Installation, Best Practices, Workflow Integration, Requirements, Troubleshooting, Tips, Author, Version) | Apache 2.0 | 404 |
| plugin-dev | name, description, author | 402 lines (Overview, per-skill sections with "Trigger phrases", Installation, Quick Start, Development Workflow, Best Practices, Contributing, Version, Author, License) | Apache 2.0 | 404 |
| skill-creator | name, description, author | 3 lines (title plus the description) | Apache 2.0 | 404 |

None of the four `plugin.json` files sets `version`, `homepage`, `repository`, `license`, or `keywords`. Each ships a README and an Apache-2.0 LICENSE, and none ships a CHANGELOG, even though plugins-reference says "Document changes in a `CHANGELOG.md`" (that advice is conditional on explicit versions, and these plugins set none). The example-plugin README calls `commands/*.md` "a legacy format … For new plugins, prefer the `skills/` directory format." It also shows a `version: 1.0.0` key in `SKILL.md` frontmatter, which is not in the skills.md frontmatter table. Claude Code would ignore that key: "Claude Code ignores a field it doesn't recognize without reporting an error."

### 4.2 `anthropics/claude-plugins-community`

- README: "A **read-only mirror** of the community plugin marketplace. … It is synced nightly from Anthropic's internal review pipeline." "Every plugin listed here has been submitted via claude.ai, passed automated security scanning, and been approved for distribution." "Pull requests opened directly against this repo are closed automatically".
- marketplace.json: `name: "claude-community"`, `owner: {name: "Anthropic"}`, `renames` (4), 2,282 plugins. Field frequency: `name`, `description`, `source` 2282; `homepage` 2280; `category` 157; `author` 36; `strict` 9; `displayName` 2; `mcpServers` 2; `skills` 2; `tags` 1. Sources are SHA-pinned (for example, entry `0x`: `{"source":"url","url":"https://github.com/0xProject/0x-ai.git","sha":"0167bbb4…"}`). There is no top-level `description`, although the validator warns when one is missing.

### 4.3 Blog posts

- claude.com/blog/claude-code-plugins (Oct 9, 2025): "Plugins are a lightweight way to package and share any combination of: Slash commands … Subagents … MCP servers …" and "To host a marketplace, all you need is a git repository, GitHub repository, or URL with a properly formatted .claude-plugin/marketplace.json file." It has no quality or security guidance beyond this.
- anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills (Oct 16, 2025): "This file must start with YAML frontmatter that contains some required metadata: name and description. At startup, the agent pre-loads the name and description of every installed skill into its system prompt. This metadata is the first level of progressive disclosure". "Progressive disclosure is the core design principle that makes Agent Skills flexible and scalable." Its trusted-sources quote is in §3.10.

---

## 5. What could not be verified

- Which fields the **Claude Desktop** plugin browser and the **claude.com/plugins** catalog display. The docs do not say, and the catalog site was not read.
- Where `license`, `repository`, `keywords`, `category`, and `tags` surface in any UI. The docs describe their purpose ("discovery", "organization", "searchability") but name no surface.
- An allowed list of `category` values, or any description length limit for plugins or marketplaces. Neither is documented. The 1,536-character cap applies to **skill** descriptions only.
- The "quality and security standards" that official-marketplace external plugins must meet. They are referenced in the README but not published in the repo.
- Commit SHAs for the GitHub files. API, Atom feed, and MCP access were all denied, and `git` was out of bounds.
- `claude plugin validate` and `claude plugin eval` were **not run**. Everything about them comes from the documentation.
- The marketplace `$schema` URL `https://anthropic.com/claude-code/marketplace.schema.json` answered 301. The target was not followed, so the schema's content is unverified.

---

## 6. Quality rubric for a Claude Code marketplace and its plugins

Each criterion can be checked mechanically or by reading. D = docs page (code.claude.com/docs/en/…), O = anthropics/claude-plugins-official@main.

### Marketplace (`.claude-plugin/marketplace.json`)

1. **The file sits at `.claude-plugin/marketplace.json` in the repository root.** D: plugin-marketplaces §Create the marketplace file.
2. **`name` is kebab-case, not reserved, not `npm|pip|uv|cargo|github|gh`, not `org|org-provisioned|unknown`, and fits Desktop's `[A-Za-z0-9][A-Za-z0-9._-]{0,127}`.** D: plugin-marketplaces §Required fields, §Marketplace validation errors.
3. **`owner.name` is present; `owner.email` or `owner.url` gives a contact.** D: plugin-marketplaces §Owner fields.
4. **A top-level `description` is present**, since `claude plugin validate` warns "No marketplace description provided". D: plugin-marketplaces §Marketplace validation errors.
5. **`claude plugin validate . --strict` exits 0 at the marketplace root.** D: plugins-reference §plugin validate; plugins §Submit your plugin.
6. **Plugin names are unique, kebab-case, and have no control or bidi characters.** D: plugin-marketplaces §Marketplace validation errors.
7. **Relative sources start with `./`, contain no `..` or backslash, and resolve to an existing directory.** D: plugin-marketplaces §Relative paths; plugins-reference §Common issues.
8. **External git sources pin a 40-character `sha`.** Anthropic's catalog does this for 260 of 260. D: plugin-marketplaces §GitHub repositories; O: marketplace.json.
9. **`version` is set in at most one of `plugin.json` or the marketplace entry, and never differs between them.** D: plugin-marketplaces §Version resolution (Warning); §Marketplace validation errors.
10. **Every entry has `description`, `category`, and `homepage`.** They are what users see before install for non-relative sources, and Anthropic's catalog sets them on over 94% of entries. D: plugin-marketplaces §Optional plugin fields (display precedence paragraph); discover-plugins ("Check each plugin's homepage"); O.
11. **Entries set `author`, and `license` as an SPDX identifier.** D: plugin-marketplaces §Optional plugin fields.
12. **A renamed or removed plugin appears in `renames` (append-only, and each chain terminates).** D: plugin-marketplaces §Rename or remove a plugin; O README "Plugin names are immutable".
13. **The marketplace is hosted in git, with plugin files not in LFS. For URL-hosted `marketplace.json`, no relative sources are used.** D: plugin-marketplaces §Host and distribute marketplaces, §Relative paths note.
14. **The README carries a trust warning**, like Anthropic's ("Make sure you trust a plugin before installing…"). D: discover-plugins §Security; O README.

### Plugin

15. **Each plugin directory passes `claude plugin validate <plugin-dir> --strict` on its own**, because a marketplace run does not open skill, agent, command, or hook files. D: plugin-marketplaces §Marketplace validation errors, §Validate a plugin or a directory without a manifest.
16. **`.claude-plugin/` holds only `plugin.json`; every component directory is at the plugin root.** D: plugins-reference §Standard plugin layout (Warning); plugins §Plugin structure overview.
17. **`plugin.json` has `name` (kebab-case, equal to the marketplace entry name) and `description`.** D: plugins-reference §Required fields; plugins quickstart table.
18. **There are no unrecognized or misspelled manifest fields**, because they produce warnings and fail `--strict`. D: plugins-reference §Unrecognized fields.
19. **Explicit `version` follows semver and is bumped on every release. If `version` is omitted, the commit-SHA fallback is intended.** D: plugins-reference §Version management; plugin-marketplaces walkthrough Note.
20. **With explicit versions, changes are recorded in `CHANGELOG.md`.** D: plugins-reference §Version management.
21. **A `README.md` with installation and usage instructions ships with each plugin.** Anthropic's example plugins all ship one. D: plugins §Share your plugins; O.
22. **A `LICENSE` file ships with each plugin**, as it does in the documented standard layout and in Anthropic's examples (Apache-2.0). D: plugins-reference §Standard plugin layout; O.
23. **New plugins use `skills/<name>/SKILL.md`, not `commands/`.** D: plugins-reference §File locations reference ("Use `skills/` for new plugins"); O example-plugin README.
24. **Each `SKILL.md` has frontmatter that parses on line 1, a `description` that leads with the key use case (combined text of 1,536 characters or less), and a body under 500 lines.** Long material goes into referenced supporting files. D: skills §Frontmatter reference, Tip at §Add supporting files, §Skill descriptions are cut short.
25. **The skill `name` equals its directory, and the skill uses only Agent Skills fields when it must also run outside Claude Code.** D: skills §Using skill frontmatter outside Claude Code, §How a skill gets its command name.
26. **All component paths are relative (`./`), stay inside the plugin root, and use forward slashes.** Symlinks resolve inside the plugin or the marketplace. D: plugins-reference §Path behavior rules, §Path traversal limitations, §Share files within a marketplace with symlinks.
27. **Hooks, MCP, and LSP configs reference bundled files through `${CLAUDE_PLUGIN_ROOT}`, hook commands use exec form or quoted paths, and scripts are executable with a shebang.** D: plugins-reference §Environment variables, §Hook troubleshooting.
28. **There is no `CLAUDE.md` at the plugin root, and no top-level `bin/` if the plugin may be distributed through claude.ai org settings.** D: plugins-reference §Standard plugin layout; plugin-marketplaces §Keep executables out of the top-level bin directory.
29. **Always-on token cost is known and reasonable**, checked with `claude plugin details <name>`. D: plugins-reference §plugin details.
30. **Behaviour is tested, not only structure.** An `evals/` suite runs under `claude plugin eval` with the no-plugin baseline, and the delta is above 0 for the plugin's claimed use cases. D: plugin-evals; plugin-marketplaces §Validation and testing.
