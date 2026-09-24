# 06 — Oh-My-Pi: how a marketplace plugin can make written rules always active

Clean-room research. Nothing under /home/user/ai-plugins or /home/user/how-possible was read.
Every quote below comes from can1357/oh-my-pi fetched with curl (proxy CA bundle, TLS verified).

## Sources and reachability

| Route | Result |
| :-- | :-- |
| `raw.githubusercontent.com/can1357/oh-my-pi/main/...` | **200**, the route used for everything quoted below |
| `api.github.com/repos/can1357/oh-my-pi/commits/main` | **403**: `{"message":"GitHub access to this repository is not enabled for this session. Use add_repo to request access. ..."}` |
| `github.com/can1357/oh-my-pi/commits/main.atom` | **403**, same message |
| `cdn.jsdelivr.net/gh/...` (for a directory listing) | `curl: (56) CONNECT tunnel failed, response 403` |
| `registry.npmjs.org/@oh-my-pi/pi-coding-agent/latest` | **200**: version `18.3.0`, `gitHead` absent. I used the tarball's `src/` **only as a file index** to learn file names. |

**The commit could not be recorded.** raw.githubusercontent does not return the commit sha, and both routes that would have returned it were blocked (see above). The files were fetched from `main` on 2026-09-24 at about 20:40 UTC. `packages/coding-agent/package.json` on main says `"version": "18.3.0"`. Six discovery files on main differ from the npm 18.3.0 tarball (`builtin.ts`, `claude.ts`, `codex.ts`, `mcp-json.ts`, `omp-plugins.ts`, `opencode.ts`), so main has moved past the published build. All line numbers below are for **main as fetched**. To allow a re-check, here are the sha256 prefixes of the fetched files:

```
ea2a963d6aaed2dc packages/coding-agent/src/discovery/agent-plugin-format.ts
592b582c58902414 packages/coding-agent/src/discovery/agent-plugins.ts
b2862c9f637d3d25 packages/coding-agent/src/discovery/claude-plugins.ts
0c8cd705f3f86c17 packages/coding-agent/src/discovery/omp-plugins.ts
9f673afe2f292582 packages/coding-agent/src/discovery/omp-extension-roots.ts
946f9775676b7be0 packages/coding-agent/src/discovery/helpers.ts
9ee10d4c7285b807 packages/coding-agent/src/discovery/index.ts
fc73774c9f5c6185 packages/coding-agent/src/capability/rule-buckets.ts
8fafa4b61bf3e803 packages/coding-agent/src/capability/rule.ts
2e805339f31a2a03 packages/coding-agent/src/capability/hook.ts
ad1f2eaddf5f822e packages/coding-agent/src/sdk.ts
060e14b914024983 packages/coding-agent/src/system-prompt.ts
6bd744aca5d6cf94 packages/coding-agent/src/prompts/system/system-prompt.md
da67cf2726c6884f packages/coding-agent/src/extensibility/extensions/types.ts
6ce3fcecb30caca8 packages/coding-agent/src/extensibility/extensions/loader.ts
4ed2ee9fb9263cbf packages/coding-agent/src/extensibility/plugins/loader.ts
4db976a1fc505fed packages/coding-agent/src/extensibility/plugins/marketplace/manager.ts
1008db43007781cb docs/rulebook-matching-pipeline.md
efa25f0190bf06d5 docs/context-files.md
2d2633c90117896e docs/config-usage.md
81950a3df94e161a docs/marketplace.md
71c6fe1b883e1b41 docs/hooks.md
d63808102d1da382 docs/extensions.md
b46297cf5b82ff83 docs/extension-loading.md
1044b74dee2fa4ca docs/skills.md
d87ef0a74fbb3762 docs/ttsr-injection-lifecycle.md
```

These requested docs returned **404** on main: `docs/rules.md`, `docs/plugins.md`, `docs/agent-plugins.md`, `docs/plugin-format.md`, `docs/claude-plugins.md`, `docs/system-prompt.md`, `docs/api.md`, `docs/README.md`. There is no `docs/skills/` directory and no `docs/hooks-*.md` file. I found the documentation files by following links from `README.md` and between docs, because no directory listing was reachable. A doc that no page links to may exist and not have been read.

I followed the sourcing order of documentation first, then source where the documentation does not answer. Each finding below says which kind of source it rests on.

---

## Q1. Discovery providers, the surfaces each reads, and priorities

**Documented.** `docs/config-usage.md` L211-226:
> - Native OMP (`builtin.ts`): `100` / - OMP plugins (`omp-plugins`): `90` / - Claude: `80` / - Agent Plugins standard (`agent-plugins`): `75` / - Codex / agents / Claude plugins marketplace: `70` / - Gemini: `60` / - OpenCode: `55` / - Cursor / Windsurf: `50` / - Cline: `40` / - GitHub Copilot: `30` / - VS Code: `20` / - agents-md: `10` / - mcp-json / ssh-json: `5` / - Built-in default rules (`builtin-defaults`): `1`

`docs/context-files.md` L74 is the only documentation of the surfaces each plugin provider reads:
> `claude-plugins` (Claude marketplace plugins: skills, commands, rules, hooks, tools, MCP servers), `omp-plugins` (OMP plugins: skills, commands, rules, prompts, hooks, tools, MCP servers), `agent-plugins` (Agent Plugins standard packages: skills and MCP servers)

**From source.** I extracted the `registerProvider(...)` calls from every file in `packages/coding-agent/src/discovery/`:

| file | provider id | priority | capabilities registered |
| :-- | :-- | :-- | :-- |
| builtin.ts | `native` | 100 (and `omp-managed` 5) | context-file, extension, extension-module, hook, instruction, mcp, prompt, **rule**, settings, skill, slash-command, system-prompt, tool |
| skillshare.ts | `skillshare` | 95 | skill |
| omp-plugins.ts | `omp-plugins` | 90 | hook, mcp, prompt, **rule**, skill, slash-command, tool |
| claude.ts | `claude` | 80 | context-file, extension-module, hook, mcp, settings, skill, slash-command, system-prompt, tool (**no rule**, so `.claude/rules` is not read) |
| agent-plugins.ts | `agent-plugins` | 75 | **mcp, skill only** |
| claude-plugins.ts | `claude-plugins` | 70 | hook, mcp, **rule**, skill, slash-command, tool |
| agents.ts | `agents` | 70 | context-file, prompt, **rule**, skill, slash-command, system-prompt |
| codex.ts | `codex` | 70 | context-file, extension-module, hook, mcp, prompt, settings, skill, slash-command, system-prompt, tool |
| gemini.ts | `gemini` | 60 | context-file, extension, extension-module, mcp, settings, system-prompt |
| opencode.ts | `opencode` | 55 | context-file, extension-module, mcp, settings, skill, slash-command |
| cursor.ts | `cursor` | 50 | mcp, **rule**, settings |
| windsurf.ts | `windsurf` | 50 | mcp, **rule** |
| cline.ts | `cline` | 40 | **rule** |
| github.ts | `github` | 30 | context-file, instruction, prompt, **rule**, skill |
| vscode.ts | `vscode` | 20 | mcp |
| agents-md.ts / claude-md.ts | | 10 | context-file |
| mcp-json.ts / ssh.ts | | 5 | mcp / ssh |
| builtin-defaults.ts | | 1 | **rule** |

Where priorities tie, registration order decides. `discovery/index.ts` imports `./claude-plugins` at L29, before `./agents` at L31 and `./codex` at L32.

**Which roots each plugin provider walks (source):**
- `claude-plugins` walks `listClaudePluginRoots()` (`helpers.ts` L1133-1330). That list is built from Claude Code's `installed_plugins.json`, **OMP's own marketplace registry**, and `--plugin-dir` roots. L1134-1135: "List all installed Claude Code plugin roots from its active plugin cache and ~/.omp/plugins/installed_plugins.json, plus the nearest project registry when present." OMP marketplace installs are pushed with `origin: "omp"` (L1262), and the project `.omp/plugins/installed_plugins.json` is read at L1271-1309.
- `omp-plugins` walks `listOmpExtensionRoots()`, which covers configured `extensions:`, `-e`, and npm/link plugins. `omp-extension-roots.ts` L272-273: "3. Installed npm/link plugins under `<plugins>/node_modules/` ... Marketplace installs load via the `claude-plugins` provider." L378-379 filters marketplace realpaths out.
- `agent-plugins` walks both lists (`agent-plugins.ts` L60-64).

**So a package installed from an OMP marketplace is read by `claude-plugins` (priority 70) for every non-portable surface, and by `agent-plugins` (priority 75) for skills and MCP.**

## Q2. `legacyProviderAllowed`: what is stood down for a root that declares the `$schema`

**From source.** `packages/coding-agent/src/discovery/agent-plugin-format.ts` L539-551:
```ts
/**
 * Whether a legacy plugin provider (claude-plugins, omp-plugins) may process a
 * root for the given surface. Roots governed by the Agent Plugins standard keep
 * their portable components (`skills`, `mcp`) exclusive to the standard loader,
 * while client-specific surfaces (commands, hooks, tools, …) still load from
 * hybrid packages. Fatally invalid Agent Plugins packages are rejected entirely.
 */
export async function legacyProviderAllowed(rootPath: string, surface: "skills" | "mcp" | "other"): Promise<boolean> {
	const status = await classifyAgentPluginRoot(rootPath);
	if (status.kind === "none") return true;
	if (status.kind === "invalid") return false;
	return surface === "other";
}
```
A root is classified `standard` only when its root `plugin.json` has `$schema` equal to `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` and passes the closed-manifest checks (L167-236, L504-523).

**Only skills and MCP are stood down.** The surface each call site passes, in `claude-plugins.ts`:
- `loadSkills` → `allowedRoots(ctx, "skills")` (L222), which is **stood down**
- `loadRules` → `allowedRoots(ctx, "other")` (L267), which **still loads**
- `loadSlashCommands` → `"other"` (L295), which **still loads**
- `loadHooks` → `"other"` (L369), which **still loads**
- `loadTools` → `"other"` (L417), which **still loads**
- `loadMCPServers` → `allowedRoots(ctx, "mcp")` (L580), which is **stood down**

`omp-plugins.ts` follows the same pattern: skills L66 `"skills"`, commands L88 `"other"`, **rules L114 `"other"`**, prompts L135 `"other"`, **hooks L162 `"other"`**, tools L200 `"other"`, MCP L294 `"mcp"`.

For an `invalid` root (a standard `$schema` with a fatal manifest violation), every surface is stood down, and `agent-plugins` reports the rejection (`agent-plugins.ts` L204-208).

**Documentation does not describe this hybrid behaviour.** The docs list the surfaces of `agent-plugins` (context-files.md L74), but only the source says that a standard root still has its `rules/`, `hooks/`, `commands/` and `tools/` loaded by the legacy providers.

## Q3. Rules

### OMP rule files and their front matter (documented)
`docs/rulebook-matching-pipeline.md` L31-51 gives the canonical `Rule` shape: `globs?`, `alwaysApply?`, `description?`, `condition?`, `astCondition?`, `question?`, `scope?`, `agents?`, `interruptMode?`. OMP uses **`globs`, not `paths`**. `RuleFrontmatter` in `src/capability/rule.ts` L23-42 has no `paths` key. It does have `enabled?` (L25, "Whether discovery should omit this rule").

Locations. The native provider reads `<cwd>/.omp/rules/*.{md,mdc}`, `~/.omp/agent/rules/*.{md,mdc}` and `RULES.md` (L70-79). The agents provider reads `.agent/rules` and `.agents/rules`, walking up to the repo root (L93-100). Cursor reads `.cursor/rules/*.{mdc,md}` (L102-115), and Windsurf, Cline and GitHub have their own locations (L117-157). **`.claude/rules` is not read**: the `claude` provider registers no rule capability (source table above).

### What `alwaysApply: true` does (documented, confirmed from source)
`docs/rulebook-matching-pipeline.md` L227:
> **Always-apply bucket**: `alwaysApply === true`, not TTSR. Full content injected into system prompt. Resolvable via `rule://`.

L248-254:
> ### `alwaysApply` ... - **Full rule content is auto-injected into the system prompt** (before the rulebook rules section).

`docs/context-files.md` L185, about `RULES.md` sticky rules:
> It is loaded as an **always-apply rule** ... so its full body is carried on every request — never demoted to an on-demand rulebook entry — and keeps its hold across long sessions.

The source path matches:
- `src/sdk.ts` L1872-1880: `loadCapability<Rule>(ruleCapability.id, { cwd })` → `bucketRules(...)` at session creation.
- `src/capability/rule-buckets.ts` L68-82 checks TTSR first, then `if (rule.alwaysApply === true) { alwaysApplyRules.push(rule); continue; }`, then rulebook.
- `src/sdk.ts` L3655-3656 passes `rules: rulebookRules, alwaysApplyRules` to `buildSystemPromptInternal`.
- `src/prompts/system/system-prompt.md` L37-43:
  ```
  {{#if alwaysApplyRules.length}}
  <generic-rules>
  {{#each alwaysApplyRules}}
  {{content}}
  {{/each}}
  </generic-rules>
  {{/if}}
  ```
- `src/system-prompt.ts` L181-190 `dedupeAlwaysApplyRules`: a rule whose content already appears in the system, custom or append prompt or in a context file is left out. The text is already present in that case, so nothing is lost.

The parse, from source (`src/discovery/helpers.ts` L235-249): `alwaysApply: frontmatter.alwaysApply === true`. Only the literal boolean `true` counts. Front matter goes through the lenient `parseFrontmatter` (L272). `enabled: false` drops the rule (L273).

### Can a plugin ship rules? Which provider, which directory? (source; partly documented)
**Yes: the `rules/` directory at the plugin root, read by `claude-plugins` for marketplace installs.** `src/discovery/claude-plugins.ts` L266-285:
```ts
async function loadRules(ctx: LoadContext): Promise<LoadResult<Rule>> {
	const { roots, warnings: rootWarnings } = await allowedRoots(ctx, "other");
	...
			loadFilesFromDir<Rule>(ctx, path.join(root.path, "rules"), PROVIDER_ID, root.scope, {
				extensions: ["md", "mdc"],
				origin: root.origin,
				transform: (name, content, filePath, source) =>
					discoverRuleFromMarkdown(name, content, filePath, source, { stripNamePattern: /\.(md|mdc)$/ }),
```
It is registered at L705-711 with `description: "Load rules from marketplace plugin rules directories", priority: PRIORITY` (70).

`omp-plugins.ts` L113-128 has the same `rules/*.{md,mdc}` loader for extension or npm roots, at priority 90.

`loadFilesFromDir` (`helpers.ts` L568-646) is **non-recursive** by default (`recursive = false`, L587). It is gitignore-aware, skips hidden files (L603-604), and matches `*.{md,mdc}` directly under `rules/`. `rules/sub/x.md` is not loaded. **Unlike the `agent-plugins` loader, it makes no containment or symlink check.**

The `allowedRoots` user-source gate does not affect OMP marketplace installs. `claude-plugins.ts` L47-48: `const userEnabled = isUserSourceEnabled("claude-plugins", ctx) || isUserSourceEnabled("claude", ctx); const scopedRoots = userEnabled ? roots : roots.filter(root => root.scope === "project" || root.origin !== "claude");`. Roots with `origin: "omp"` always pass.

**Documentation status.**
- `docs/context-files.md` L74 documents that `claude-plugins` contributes "rules".
- `docs/marketplace.md` L18 says a plugin may contain "skills, commands, agents, rules, hooks, tools, MCP servers, or LSP servers".
- **But `docs/rulebook-matching-pipeline.md` is stale on this point.** It lists the rule providers as `native`, `omp-plugins`, `agents`, `cursor`, `windsurf`, `cline`, `github`, `builtin-defaults` (L59-68, L187-196, and L345: "The rule providers currently loaded for `rules` are ..."). It omits `claude-plugins`, which source registers for rules at priority 70 (claude-plugins.ts L705-711).

Documentation is therefore split. The existence of plugin rules is documented; that they reach the always-apply bucket through `claude-plugins` is **from source**.

**Dedup risk (documented plus source).** Rules deduplicate **by name only**, first wins (rulebook doc L53-55, L177-185; `rule.ts` L396 `key: rule => rule.name`). A plugin rule `rules/foo.md` is named `foo`. It is shadowed by any `foo` from `native` (100) or `omp-plugins` (90). It wins over `agents`, which ties at 70 but registers after it, and over everything below 70. A distinctive name is therefore needed.

**User off-switches (documented).**
- `ttsr.disabledRules` drops a rule by name (rulebook doc L217; ttsr doc L262).
- The `agents:` front matter restricts which agents get a rule (L256-262). If it is omitted, the rule applies to every agent, including subagents, which "re-evaluate `agents` under their own name" (L262).
- `disabledProviders` can turn off `claude-plugins` entirely (context-files.md L74).
- `disabledExtensions` can target `rule:<name>` (`rule.ts` L397, source).

**Refresh (documented plus source).** Rules are discovered at session creation (`sdk.ts` L1866-1885). `sdk.ts` L1887-1889 says they are re-discovered "on /clear and /new". `docs/marketplace.md` L78 says installs "do not refresh the active session", so a new install takes effect from the next session.

## Q4. Hooks

**OMP does not run Claude-style `hooks/hooks.json` with `SessionStart` and `additionalContext`.**
- Documentation: `docs/hooks.md` and `docs/extensions.md` describe only OMP's own event names (`session_start`, `before_agent_start`, `tool_call`, …). Neither mentions `hooks.json` or `SessionStart`.
- Source: `hooks.json`, `"SessionStart"` and `UserPromptSubmit` do not appear anywhere in `packages/coding-agent/src` of the **npm 18.3.0 tarball**. `SessionStartEvent` appears only as OMP's TS type for `session_start`. On main, `extensions/types.ts` has no `hooks.json` or `Claude Code` hook reference either. I could not search main's whole tree, because no directory listing was reachable.
- Source: `claude-plugins.ts` L365-407 reads only `hooks/pre/*` and `hooks/post/*` files. `capability/hook.ts` L3-4 describes them as "Pre/post tool execution hooks defined as shell scripts", with `type: "pre"|"post"` and `tool`.

**What OMP does with plugin `hooks/pre|post/` files.**
- Documented, `docs/hooks.md` L9-10: "JS/TS hook factories discovered through `hookCapability` (for example `.omp/hooks/pre/*.ts`) are loaded as extension modules so their `pi.on(...)` handlers bind to the runtime event bus". L69: "Only `.ts`/`.js` factories are appended to the extension pipeline".
- Documented, `docs/extension-loading.md` L46-48: `discoverAndLoadExtensions()` "appends JS/TS hook factories from the `hook` capability — any hook whose entry path is a `.ts`/`.js` file".
- Source, `src/extensibility/extensions/loader.ts` L621-629:
  ```ts
  if (options.includeAmbientHooks !== false) {
      const hooks = await loadCapability<Hook>(hookCapability.id, loadOptions);
      for (const hookPath of hooks.items.map(hook => hook.path).filter(hookPath => isExtensionFile(path.basename(hookPath)))) {
          addPath(hookPath);
  ```
  `loadCapability(hook)` includes `claude-plugins` (L721-727), which walks marketplace roots, including Agent Plugins standard roots through `"other"`. **So a `.ts` or `.js` file at `<plugin>/hooks/pre/<name>.ts` in a marketplace plugin is imported as a full extension module.** The docs illustrate this only with `.omp/hooks/pre/*.ts`; that it applies to marketplace plugin roots is **from source**.

**Events that can inject context (documented).**
- `docs/hooks.md` L91-118 and `docs/extensions.md` L325-351 list `session_start`, `before_agent_start`, `context`, `tool_call`, `session_stop`, and others.
- `hooks.md` L108: "`before_agent_start` → can return `{ message?: { customType; content; display; details; attribution } }`".
- `hooks.md` L122 and `extensions.md` L437-447: `tool_call` can return `additionalContext`, which is "trusted handler-authored instructions ... with developer/system priority where the transport supports it". That fires only on tool calls.
- `extensions.md` L357: "Handlers chain from the current base system prompt. Their final override governs the next provider request and its continuations".
- Source, `src/extensibility/extensions/types.ts` L758-765: `BeforeAgentStartEvent { ...; systemPrompt: string[] }`. L1169-1173:
  ```ts
  export interface BeforeAgentStartEventResult {
  	message?: CustomMessagePayload;
  	/** Replace policy for the next request and its continuations, until the next preparation. Extensions chain in order. */
  	systemPrompt?: string[];
  }
  ```
So a TS hook factory can append rule text to the system prompt on every user prompt, starting with the first one. That is from source plus documented event semantics. **I did not run it.**

Shell-script hooks (`.sh`) in `hooks/pre|post` are listed by the capability, but the current runtime does not import them into the extension pipeline, which takes only `.ts`/`.js` (hooks.md L69). Whether anything still executes them was not verified.

## Q5. `.omp-plugin/plugin.json`

**Documentation: none.** `docs/marketplace.md` mentions only `.omp-plugin/marketplace.json` (L16, L92, L96). No doc describes a `.omp-plugin/plugin.json`.

**Source: it is read in exactly two places, and for two fields at most:**
1. `claude-plugins.ts` L464-539, `resolvePluginMCPConfig`: "`.omp-plugin/plugin.json` takes precedence over `.claude-plugin/plugin.json`". The only field read is **`mcpServers`**, as an inline map or a path (L488-528). The caller runs under `allowedRoots(ctx, "mcp")` (L580), so **for a standard root this read never happens.**
2. `agent-plugin-format.ts` L566-571, `pluginUsesClaudeModelDialect`: only its *existence* is checked, `if ((await readFile(path.join(rootPath, ".omp-plugin", "plugin.json"))) !== null) return false;`. It decides whether task-agent `model:` front matter is treated as OMP selectors.

`readPluginManifest` (claude-plugins.ts L85-97), which reads the `skills` / `commands` / `slash-commands` path fields, reads **only `.claude-plugin/plugin.json`**. The marketplace installer resolves the version from `.claude-plugin/plugin.json`, then root `plugin.json`, then `package.json` (`marketplace/manager.ts` L545-557), and does not read `.omp-plugin/plugin.json`. I found no source that reads rule or hook fields from `.omp-plugin/plugin.json`, **and rules and hooks are not manifest-driven at all**: they come from the fixed `rules/` and `hooks/pre|post/` directories.

**Can it sit next to a root Agent Plugins `plugin.json`?** Nothing in source rejects it. The root is classified from root `plugin.json` alone (`classifyUncached`, L504-523). A `.omp-plugin/plugin.json` would contribute nothing for a standard root beyond the model-dialect flag. OMP does not merge "vendor fields from `.omp-plugin`" with "core fields from root". **It is not needed for rules or hooks.**

## Q6. TypeScript extensions shipped by a marketplace plugin

**Documented, `docs/marketplace.md` L18:**
> Marketplace installs also load extension modules declared by `package.json` `omp.extensions`: installation symlinks the cached plugin into the scope's `node_modules` tree and records it in `omp-plugins.lock.json`, the same runtime surfaces used by npm-installed and `omp plugin link`ed plugins.

`docs/extension-loading.md` L52-58: "`discoverAndLoadExtensions()` appends extension entry points from enabled installed plugins via `getAllPluginExtensionPaths(cwd)`. Plugin extension entries come from package `omp.extensions` / `pi.extensions` manifests".

**Source.** `src/extensibility/plugins/loader.ts` L459-468 `getAllPluginExtensionPaths`, and `extensions/loader.ts` L636-639. No `legacyProviderAllowed` gate applies on this path, so the Agent Plugins `$schema` does not affect it. An extension can use `pi.on("before_agent_start", …)` → `{ systemPrompt: [...] }` (types.ts L1169-1173) or `session_start` (extensions.md L77, L279).

**Two routes, both marketplace-reachable.**
- (a) `package.json` with `"omp": { "extensions": [...] }`. This is documented for marketplace plugins.
- (b) `hooks/pre/<name>.ts`. This is from source, via `claude-plugins` hooks → extension loader.

Both put **executable TypeScript** in the package, which runs in-process with full host API access. Whether a text-only repository may carry that is the caller's judgement; this report does not settle it.

Refresh: marketplace.md L78 says "restart the session for newly installed tools, hooks, or extension modules".

## Q7. Skills

**The strict six-field set is confirmed from source.** `agent-plugin-format.ts` L89-97:
```ts
/** The closed frontmatter field set from the skills-ref reference validator. */
const SKILL_FIELDS: Record<string, true> = { name: true, description: true, license: true, "allowed-tools": true, metadata: true, compatibility: true };
```
L124-127: `for (const key in frontmatter) { if (!SKILL_FIELDS[key]) return \`unexpected frontmatter field "${key}"\`; }`

`agent-plugins.ts` L153-176 uses a strict YAML parse (`repair: false`, `rawKeys: true`). Its comment reads: "client conventions like `enabled` reject the skill as an unexpected field". The name must equal the directory (L110-112). A skill that fails is skipped with a warning. This strictness is **not in the docs**: `docs/skills.md` does not mention the `agent-plugins` provider at all (its provider list at L85-96 omits it).

**Skills have no always-on mechanism.**
- Documented: skills are listed by name and description ("Matching skill → MUST read `skill://<name>` first", system-prompt.md L28-35) and injected in full only when invoked (skills.md "System prompt exposure", and `/skill:<name>`).
- `docs/skills.md` L57 lists `alwaysApply?: boolean` on the skill type. I found no use of it in `system-prompt.ts`; `grep alwaysApply` there hits only rules. It is also impossible for a standard-root skill, because the closed six-field validator rejects any `alwaysApply` key.
- `autoloadSkills` (skills.md L54) is agent-definition front matter for subagents, not a plugin mechanism.

---

## Recommended mechanism(s) for a standard Agent Plugins package that must enforce a writing standard in every Oh-My-Pi session

**1. Primary: ship `rules/<distinctive-name>.md` at the package root with `alwaysApply: true`.**
```md
---
description: <one line>
alwaysApply: true
---
<the writing standard>
```
- **Documented:**
  - Always-apply rules are injected in full into the system prompt on every request (rulebook-matching-pipeline.md L227, L248-254; context-files.md L185).
  - `claude-plugins` contributes rules from marketplace plugins (context-files.md L74; marketplace.md L18).
- **From source:**
  - The loader reads `<root>/rules/*.{md,mdc}` (claude-plugins.ts L266-285).
  - It runs for Agent Plugins standard roots, because rules are an `"other"` surface (agent-plugin-format.ts L546-551; claude-plugins.ts L267).
  - OMP marketplace installs are among its roots (helpers.ts L1220-1264).
  - The `<generic-rules>` template block renders it (system-prompt.md L37-43).
  - Subagents get it too unless `agents:` narrows it (rulebook doc L262).
- **Caveats:**
  - Do **not** add `condition`, `astCondition` or `question` to this same file. That would make it TTSR-only and remove it from the always-apply bucket (rule-buckets.ts L69-74).
  - Pick a name no user or native rule is likely to use (name dedup, first wins).
  - It takes effect in a new session after install.
  - The rulebook doc's provider list omits `claude-plugins`. That is a documentation gap, and it cuts against calling this path "documented" end to end.
  - It needs no `.omp-plugin/plugin.json`, no `package.json`, and no code.
- **Unverified:** nobody installed a package and observed the text in a live system prompt. The doc/source chain has not been run.

**2. Optional enforcement layer, still text-only: a second rule file that uses TTSR** (`condition:` regex for mechanically detectable violations, or `question:` for judged ones).
- **Documented:**
  - A `condition` match aborts the stream and retries with the rule injected, with `interruptMode` default `"always"` and `ttsr.enabled` default `true` (ttsr-injection-lifecycle.md L65-80, L106-124).
  - `question` rules are judged after output. Their default `ttsr.judge: auto` judges "only when the judge role resolves to a native System One model", so they are **off in most setups** (ttsr doc L279).
  - The same `rules/` loader applies, so TTSR rules ship the same way.
- **Unverified.**

**3. Not recommended for this repository:**
- **(a)** `hooks/pre/<x>.ts` returning `systemPrompt` from `before_agent_start`. This path is from source only; docs show only `.omp/hooks/pre`.
- **(b)** `package.json` `omp.extensions`. This is documented for marketplace installs.

Both work by shipping executable TypeScript that runs in-process. Both replace the system prompt wholesale, since overrides are "complete replacements" (extensions.md L357), and so risk clobbering other extensions. Neither is needed when mechanism 1 exists.

**Not available:**
- Claude-style `hooks/hooks.json` `SessionStart` `additionalContext`. No support was found in docs or source.
- `.omp-plugin/plugin.json` fields for rules or hooks. None exist; the file is read only for `mcpServers`, and that read is stood down for standard roots.
- Any always-on skill mechanism.
