# 06: How a Codex plugin can keep rules active in every session

Question: every documented or source-evidenced way an OpenAI Codex **plugin** can make a set of written rules active from a session's first turn, without the user invoking anything, and make the agent follow them.

Clean-room: I did not read `/home/user/ai-plugins` or `/home/user/how-possible`. Research date: 2026-09-24.

## Sources and reachability

| Source | Result |
|---|---|
| `developers.openai.com` (curl and WebFetch) | **BLOCKED.** curl: `CONNECT tunnel failed, response 403`. WebFetch: `EGRESS_BLOCKED ... Access to developers.openai.com is blocked by the network egress proxy.` |
| `doc.jarvisuni.com` (an unofficial third-party mirror of the Codex hooks page) | **BLOCKED** (`EGRESS_BLOCKED`). It is not a vendor copy, so it would not count as documentation in any case. |
| `api.github.com/repos/openai/codex/...`, `codeload.github.com`, `github.com/.../tree/...` HTML | 403 (the session is not attached to that repository). |
| `https://github.com/openai/codex.git/info/refs` (smart-HTTP ref advertisement, read with curl) | OK. `refs/heads/main` = **`694d8d45bd3d440fa4f4cbf22667ac6c17a13758`**. The newest release tag is `rust-v0.156.1`. |
| `raw.githubusercontent.com/openai/codex/<sha>/...` | OK. **Every source path and line number below is at commit `694d8d45bd3d440fa4f4cbf22667ac6c17a13758`** unless it names another ref. Local copies are under `research/codex06/src/`. |
| `raw.githubusercontent.com/openai/plugins/main/README.md` | OK. main = `1dc195897af4161d039b80d8471ec0a10c9bbc89`. |
| GitHub issue pages via WebFetch | OK, but only as **model-summarised** text. The quotes from issues below are that summary's words, not verbatim page text. |
| WebSearch | OK. It returned search-engine *summaries* of developers.openai.com pages. These are **not quotable documentation**. I use them only to show what the docs appear to claim, and I label them. |

### What the vendor documentation in the repo says
`openai/codex` `docs/` is almost entirely pointer stubs to developers.openai.com: `docs/config.md`, `docs/agents_md.md`, `docs/skills.md`, `docs/sandbox.md`, `docs/exec.md`, `docs/slash_commands.md`, `docs/execpolicy.md`, `docs/getting-started.md`. None of them says anything about plugins or plugin hooks. The only hook text in the repository docs is `docs/config.md` "## Lifecycle hooks":
> "Admins can set top-level `allow_managed_hooks_only = true` in `requirements.toml` to ignore user, project, and session hook configs while still allowing managed hooks from requirements and managed config layers."

The documentation that matters is on the blocked site: `/codex/hooks`, `/codex/plugins/build`, `/plugins/build/plugins`, `/codex/guides/agents-md`, `/codex/skills`. **The documentation-first order therefore could not be completed.** Everything marked "from source" below was read from source only because the documentation was unreachable, and it should be re-checked against the docs when they can be reached. Two docs claims arrived second-hand, through WebSearch summaries and through issue #47925 quoting the build page:
- "hooks can be defined inside `extensions.com.openai`" in root `plugin.json" (quoted in issue #47925, which cites the build documentation).
- "Codex discovers hooks/hooks.json by default when the selected OpenAI extension or compatibility manifest doesn't define hooks" and "installing or enabling a plugin doesn't automatically trust its hooks; Codex skips plugin-bundled hooks until you review and trust the current hook definition" (WebSearch summaries of developers.openai.com/codex/hooks; not verbatim).

---

## 1. Codex hooks: whether they exist, their events, file format, and where a plugin declares them

**They exist and are on by default (from source).** `codex-rs/features/src/lib.rs`:
- L106-107: `/// Enable Claude-style lifecycle hooks loaded from hooks.json files.` / `CodexHooks,`
- L1205-1210: `id: Feature::CodexHooks, key: "hooks", stage: Stage::Stable, default_enabled: true`
- L251-252 and L1455-1460: `/// Removed compatibility flag for plugin-bundled lifecycle hooks.` `PluginHooks`, `key: "plugin_hooks", stage: Stage::Removed`. Plugin hooks no longer need their own flag.

**Events (from source).** `codex-rs/hooks/src/lib.rs` L22-36:
```rust
pub const HOOK_EVENT_NAMES: [&str; 12] = [
    "PreToolUse", "PermissionRequest", "PostToolUse", "PreCompact", "PostCompact",
    "SessionStart", "SessionEnd", "UserPromptSubmit", "SubagentStart", "SubagentStop",
    "Stop", "Interrupt",
];
```
SessionStart sources are `startup | resume | clear | compact | fork` (`hooks/src/events/session_start.rs` L23-42), and the matcher is compared against these values.

**File format: Claude-compatible `hooks.json` (from source).** The engine type is named `ClaudeHooksEngine` (`hooks/src/engine/mod.rs` L220). `codex-rs/config/src/hook_config.rs`:
- L10-17: `#[serde(deny_unknown_fields)] pub struct HooksFile { description: Option<String>, #[serde(default)] pub hooks: HookEventsToml }`
- L35-61: `HookEventsToml` has one field per event, each renamed to its Claude name (`#[serde(rename = "SessionStart", default)] pub session_start: Vec<MatcherGroup>`, and so on).
- L153-159: `MatcherGroup { matcher: Option<String>, hooks: Vec<HookHandlerConfig> }`
- L161-200: `#[serde(tag = "type")] enum HookHandlerConfig { "command" { command, commandWindows, timeout, async, statusMessage, additionalContextLimit }, "mcp_tool" {...}, "prompt" {}, "agent" {} }`

So `{"hooks":{"SessionStart":[{"matcher":"startup","hooks":[{"type":"command","command":"..."}]}]}}` is the exact shape. The loader test fixture writes exactly that (`core-plugins/src/loader_tests.rs` L674-690, L804-827). Plugin hook commands receive `PLUGIN_ROOT`, `CLAUDE_PLUGIN_ROOT`, `PLUGIN_DATA` and `CLAUDE_PLUGIN_DATA` (`hooks/src/engine/discovery.rs` L262-270, with the comment "For OOTB compat with existing plugins that use this env var.").

**Where a plugin declares hooks: two parsers, one loader.**

*Legacy vendor manifest* (`.codex-plugin/plugin.json`, `.claude-plugin/plugin.json` or `.cursor-plugin/plugin.json`, searched in that order: `exec-server-protocol/src/protocol.rs` L49-53). `core-plugins/src/manifest.rs`:
- L45-70: `RawPluginManifest` has fields `name, version, description, keywords, skills, mcp_servers, apps, hooks, interface, extensions`.
- L147-155: `enum RawPluginManifestHooks { Path(String), Paths(Vec<String>), Inline(Box<HooksFile>), InlineList(Vec<HooksFile>), Invalid(JsonValue) }`. The field takes a `./` path, a list of paths, an inline hooks object, or a list of inline objects.
- L567-581: `resolve_openai_onboarding_skill` reads `extensions["com.openai"].onboardingSkill`, even in a legacy manifest.

*Agent Plugins root manifest* (`plugin.json` at the plugin root). `core-plugins/src/agent_plugin_manifest.rs`:
- L17-29: `CODEX_AGENT_PLUGIN_EXTENSION_NAMESPACE = "com.openai"`. `AGENT_PLUGIN_FIELDS` = `$schema, name, version, description, author, homepage, repository, license, keywords, extensions`. Any other top-level field is dropped with the warning "ignoring unknown Agent Plugins manifest field" (L76-81).
- L161-182: the portable manifest's components are **fixed**: `skills: Some(RawPluginManifestPaths::Path("./skills"))` and `mcp_servers: Some(RawPluginManifestMcpServers::Path("./mcp.json"))`. The interface is synthesised from `name` and `description` and gets `category: "Other"`.
- L184-195: if `extensions["com.openai"]` is present and is an object, it is applied. Otherwise `.codex-plugin/plugin.json` is read as an **overlay** and applied (the overlay load is at `manifest.rs` L171-178).
- L203-217, which answers which `com.openai` fields are accepted:
```rust
fn apply_codex_agent_plugin_extension(...) -> Result<(), serde_json::Error> {
    let extension = parse_legacy_plugin_manifest_uri(plugin_root, source_path, contents)?;
    resolved.paths.apps = extension.paths.apps;
    resolved.paths.hooks = extension.paths.hooks;
    resolved.paths.onboarding_skill = extension.paths.onboarding_skill;
    if extension.interface.is_some() {
        resolved.interface = extension.interface;
    }
    Ok(())
}
```
  The extension object is parsed as a legacy manifest, and then **only `apps`, `hooks`, `onboardingSkill` and `interface` are taken from it.** `skills` and `mcpServers` inside `com.openai` are parsed and thrown away, so the portable fixed `./skills` and `./mcp.json` stay. The tests `legacy_codex_overlay_keeps_portable_components_fixed` (`agent_plugin_manifest_tests.rs` L193-245) and `inline_openai_extension_precedes_legacy_overlay` (L247-275) confirm this.

**BUT the loader discards hooks from every Agent Plugins manifest (from source).** `core-plugins/src/loader.rs` L950-960:
```rust
    let (hook_sources, hook_load_warnings) =
        if loaded_manifest.format == PluginManifestFormat::AgentPlugin {
            (Vec::new(), Vec::new())
        } else {
            load_plugin_hooks(&plugin_root, &loaded_plugin_id, &plugin_data_root, manifest_paths)
        };
```
The plugin-detail path does the same thing: `core-plugins/src/manager.rs` L2713-2718 (`if manifest_format == PluginManifestFormat::Legacy { load_plugin_hooks(...) } else { (Vec::new(), Vec::new()) }`). The branch is identical at release tag `rust-v0.156.1` (`loader.rs` L950-953).

A root `plugin.json` wins over the vendor manifests. Its `$schema` only has to start with the agent-plugins.org prefix (`utils/plugins/src/plugin_namespace.rs` L43-61). The same function returns `None` for a **symlinked** root `plugin.json` (L45-48), which means the plugin does not load at all. So a standard package gets the AgentPlugin format and, at main, **Codex runs no plugin hooks for it, whether they are declared in `extensions["com.openai"].hooks`, in a `.codex-plugin/plugin.json` overlay, or in `hooks/hooks.json`.** Two open issues independently report this (model-summarised):
- openai/codex#39895 (open, codex 0.149.0): "A root `plugin.json` silently disables all of a plugin's hooks". The TUI still looks normal and there is no warning.
- openai/codex#47925 (open, filed 2026-09-24, codex 0.156.1): "Hooks from Agent Plugins 1.0 plugins are never loaded (extensions.com.openai.hooks ignored)". It cites `loader.rs` L950-953. `/hooks` shows "Installed 0".

The executor path (`core-plugins/src/executor_hooks.rs`) does parse Agent Plugins manifests. However, it accepts only inline hooks (L56-59: "Only inline hooks are supported for now"), and L27-28 plus L81 say: "Executor manifests are not signed yet, so temporarily we only admit the known cleanup hooks from the bundled cleanup allowlist and the remote Browser plugin." / `// FIXME: Remove this temporary filter once executor plugin hooks can be trusted.` A third-party package cannot use it.

## 2. Can hook output add context or instructions to the session?

**Yes, from source, for SessionStart, SubagentStart, UserPromptSubmit, PreToolUse and PostToolUse.**

- `hooks/src/events/session_start.rs` L218-223, doc comment: "hook JSON can emit warnings/context, invalid JSON-looking stdout fails, and **plain stdout becomes model context**. Only `SessionStart` honors `continue:false`; `SubagentStart` stays context-injection-only."
- L244-312: on exit code 0, JSON stdout is parsed. `hookSpecificOutput.additionalContext` becomes model context, and `systemMessage` becomes a warning shown to the user. Stdout that starts with `{` or `[` but does not parse fails the hook ("hook returned invalid session start JSON output"). Any other non-empty stdout is appended as context in full (L304-311).
- Wire schema `hooks/src/schema.rs` L395-403: `SessionStartHookSpecificOutputWire { hook_event_name, #[serde(default)] additional_context: Option<String> }`, with `deny_unknown_fields`. The universal fields are `continue, stopReason, suppressOutput, systemMessage` (L87-99). UserPromptSubmit has the same `additionalContext` (L441-449) and also supports `decision: "block"` with `reason`.
- Tests: `plain_stdout_becomes_model_context` (session_start.rs L373-402) and `continue_false_preserves_context_for_later_turns` (L404-440, JSON with `hookSpecificOutput.additionalContext`).
- The context reaches the model as a **developer-role message**. `core/src/hook_runtime.rs` L849-873 (`record_additional_contexts` → `sess.record_conversation_items`) and `core/src/context/hook_additional_context.rs` L15-22 (`fn role(&self) -> &'static str { "developer" }`).
- The context is recorded into conversation history once, when the hook fires. `run_pending_session_start_hooks` (`hook_runtime.rs` L128-181) runs when the first turn starts, and again for `resume/clear/compact/fork`. So the text is re-injected after compaction only if the matcher includes `compact`.
- **Size cap:** `hook_config.rs` L175-184: "Approximate token threshold for spilling this hook's `additionalContext` to disk. Unset uses 2,500 tokens; `0` disables spilling for this hook." `hooks/src/output_spill.rs` L12 `DEFAULT_HOOK_OUTPUT_TOKEN_LIMIT: usize = 2_500`. Above the cap, the model sees a truncated preview and the line "Full hook output saved to: <path>" (L127-130). A long writing standard needs `"additionalContextLimit": 0`.
- **Conflict, unresolved:** openai/codex#45999 (closed "not planned", codex 0.154.0 `codex exec`, model-summarised) reports that any SessionStart output containing `additionalContext` fails with "SessionStart Failed" and injects nothing. The source at `rust-v0.154.0` does have the field (`schema.rs` L398-403), and main's test parses it. I could not run the client, so this is **unverified either way**. Plain stdout avoids the question.

## 3. Does Codex read AGENTS.md or instruction files from a plugin directory? Do onboardingSkill or defaultPrompt run automatically?

- **AGENTS.md: not from a plugin (from source).** `core/src/agents_md.rs` L1-18: AGENTS.md is collected "from the project root down to the current working directory", combined with host "user instructions" (L56-63), and skipped entirely when `config.active_project.is_untrusted()` (L64-66). Neither `agents_md.rs` nor `agents_md_manager.rs` mentions "plugin" (grep found no matches). A plugin cannot contribute AGENTS.md text.
- **Plugin instructions are injected only on explicit mention.** `core/src/plugins/injection.rs` L14-22 returns nothing unless `mentioned_plugins` is non-empty ("Turn each explicit plugin mention into a developer hint"). `core/src/plugins/render.rs` L17-25/L74 renders only a capabilities list ("Capabilities from the `X` plugin: ... Use these plugin-associated capabilities to help solve the task."). No plugin-authored text is included.
- **`onboardingSkill` is metadata only.** `manager.rs` L456-457: `/// Packaged onboarding path; callers apply visibility and enablement.` The path is kept only if it resolves to one of the plugin's loaded skills (L2700-2711). The app-server protocol exposes it as `/// The declared onboarding skill, when the plugin and visible skill are enabled.` `pub onboarding_skill: Option<SkillSummary>` (`app-server-protocol/src/protocol/v2/plugin.rs` L766-768). Nothing in the open-source core runs it on install or at session start. Whether a closed-source client (the desktop app or ChatGPT) auto-launches it is **unverified**.
- **`defaultPrompt`:** `plugin-creator/references/plugin-json-spec.md` L102: "Starter prompts shown in composer/UX context". The parser caps it at 3 prompts of 128 characters each (`manifest.rs` L13-14, L489-561). These are suggestions and do not run.
- **Marketplace `policy.installation: "INSTALLED_BY_DEFAULT"`** (`plugin-json-spec.md` L175-178) controls whether the plugin is installed. It says nothing about injecting context.

## 4. Can a Codex skill be always-on?

**No, from source.**
- Front matter honoured (`codex-rs/skills/src/parser.rs` L6-20): `name`, `description`, and `metadata.short-description`. Nothing else is read from SKILL.md.
- Per-skill policy comes from `agents/openai.yaml` (`skills/src/interface.rs` L13), not front matter. `SkillPolicy { allow_implicit_invocation: Option<bool>, products: Vec<Product> }` (`model.rs` L62-68), and `allows_implicit_invocation()` defaults to `true` (L23-28). The only switch turns implicit use **off**. There is no always-on or preload flag.
- What is always present is the **catalog**: name, description and path for every enabled skill, inside a `## Skills` block (`ext/skills/src/catalog_prompt.rs` L87). Its rules (L25): "If the user names a skill ... OR the task clearly matches a skill's description shown above, you must use that skill for that turn. ... **Do not carry skills across turns unless re-mentioned.**" So a skill body is loaded per turn, when the model judges that the task matches the description. Descriptions can be truncated or dropped under the skills context budget (`ext/skills/src/render.rs` L22-25: "Exceeded skills context budget. All skill descriptions were removed and ...").

## 5. Default discovery of `hooks/hooks.json`

**For legacy-format plugins only, and a manifest `hooks` field replaces it (from source).**
- `loader.rs` L67-70: `DEFAULT_SKILLS_DIR_NAME = "skills"`, `DEFAULT_HOOKS_CONFIG_FILE = "hooks/hooks.json"`, `DEFAULT_MCP_CONFIG_FILE = ".mcp.json"`, `DEFAULT_APP_CONFIG_FILE = ".app.json"`.
- `loader.rs` L1186-1243, comment: "Discover plugin-bundled hooks from manifest `hooks` entries when present (path, paths, inline object, or inline objects), **otherwise** from the default `hooks/hooks.json` file." The `None =>` arm alone reads `hooks/hooks.json`.
- Test `load_plugin_hooks_manifest_paths_replace_default_hooks_file` (`loader_tests.rs` L778-801) writes `hooks/hooks.json` with `echo ignored` and asserts that only the manifest paths load.
- Skills behave the same way: `plugin_skill_roots` (`loader.rs` L1079-1098) uses the default `skills/` directory only `if manifest_paths.skills.is_empty()`.
- **This contradicts the vendor's own reference text.** `plugin-creator/references/plugin-json-spec.md` L117: "`skills`, `hooks`, and string-valued `mcpServers` are supplemented on top of default component discovery; they do not replace defaults." For hooks and skills, the code and its test replace the defaults. The same skill also says (`SKILL.md` L195, `plugin-json-spec.md` L215) "Validation rejects unsupported manifest fields such as `hooks`, so the scaffold keeps them out of generated manifests", which conflicts with the loader accepting `hooks`. The WebSearch summary of the hooks docs page agrees with the code: default discovery applies "when the selected OpenAI extension or compatibility manifest doesn't define hooks".
- For an Agent Plugins package, none of this applies, because L950-952 short-circuits before `load_plugin_hooks` runs.

## 6. Is `extensions["com.openai"].hooks` in a root manifest the documented route?

- **Documented: apparently yes, second-hand only.** Issue #47925 quotes the build documentation as saying hooks "can be defined inside `extensions.com.openai`" in the root manifest. The WebSearch summaries of `/plugins/build/plugins` say the same ("OpenAI-specific presentation, registered MCP server mappings, and hook settings are placed under `extensions.com.openai` in the root `plugin.json`"). I could not read the page.
- **From source: the manifest parser accepts it, and the loader then ignores it.** `agent_plugin_manifest.rs` L211 copies the hooks into `resolved.paths.hooks`, and then `loader.rs` L950-952 and `manager.rs` L2713-2718 drop them for the AgentPlugin format. At main `694d8d4` and at `rust-v0.156.1`, **the documented route does not work.** Two open upstream issues (#39895, #47925) report the same. Codex 0.156.1 as released has not been run here, so no runtime claim is made.

## 7. Security: prompts, trust, sandbox

- **Plugin hooks are untrusted until the user trusts them (from source).** `hooks/src/engine/discovery.rs` L244-295: plugin sources are `source: HookSource::Plugin, is_managed: false`. L713-719: a handler runs only if `enabled && (bypass_hook_trust || trust_status is Managed | Trusted)`. L794-811: a non-managed, non-builtin hook is `Trusted` only when the stored `trusted_hash` equals its current hash, `Modified` if the hash differs, and `Untrusted` if none is stored. Any edit to a hook needs re-trust. `hooks/src/config_rules.rs` L8-14: only user and session layers may write hook state, and "Project, managed, and plugin layers can discover hooks, but they do not get to write user hook state." **A plugin cannot pre-trust its own hooks.**
- **The prompt the user sees:** `tui/src/startup_hooks_review.rs` L228-271: "Hooks need review", "N hooks are new or changed.", "**Hooks can run outside the sandbox after you trust them.**", with the options "Review hooks", "Trust all and continue" (which requires explicit confirmation), and "Continue without trusting (hooks won't run)".
- **Bypass flag:** `core/src/config/mod.rs` L958-961 ("runtime-only knob populated from invocation overrides, not from config files") and L3331-3335 (warning "`--dangerously-bypass-hook-trust` is enabled. Enabled hooks may run without review for this invocation."). `codex exec` passes it through (`exec/src/lib.rs` L597). Without the flag or a stored trust, a non-interactive `codex exec` runs no plugin hook.
- **Admins** can set `allow_managed_hooks_only` in `requirements.toml` (docs/config.md, quoted above; `discovery.rs` L83-116). With it set, plugin hooks never run.
- **Sandbox:** the TUI text above says that trusted hooks can run outside the sandbox. I did not trace the command runner's sandboxing further.

---

## Recommended mechanism(s) for a standard Agent Plugins package that must enforce a writing standard in every Codex session

**Short answer: at Codex main `694d8d4` (and release `rust-v0.156.1`), no mechanism lets a standard Agent Plugins package make rules active from the first turn without user action.** The ranking below says, for each option, how far it gets and what it rests on.

1. **SessionStart hook injecting the standard: the right mechanism, but it does not reach a standard package today.**
   - What it would take: a `SessionStart` command hook with matcher `startup|resume|clear|compact` that prints the rules as plain stdout (plain stdout avoids the #45999 question), with `"additionalContextLimit": 0` so text over 2,500 tokens is not spilled. The text enters as a developer message (§2).
   - Declared in the root manifest as `"extensions": {"com.openai": {"hooks": "./<path>.json"}}` (path form) or as an inline hooks object. This matches what the docs reportedly say, and the manifest parser accepts it (§1, §6).
   - **Status:** documented (second-hand only; the docs page is blocked). **From source, it does not run for AgentPlugin-format packages** (`loader.rs` L950-952). Upstream issues #39895 and #47925 are open. Even once it is fixed, it runs only after the user trusts the hook ("Hooks need review"), or under `--dangerously-bypass-hook-trust` (§7). "Without the user invoking anything" is therefore never fully achievable through hooks: at least one trust decision is always needed, and editing the hook needs it again.
   - Declaring it costs little and is harmless now. Codex ignores it, and other clients ignore an unknown `extensions` namespace. It would start working if upstream lands a fix. It is **unverified at runtime.**
   - For enforcement rather than advice, a `Stop` hook can return `decision: "block"` with a reason to force another pass, and `UserPromptSubmit` can re-inject a short reminder on every prompt (`output_parser.rs` L266-288). The same loader limit and trust limit apply.

2. **Skill with a precise, trigger-worthy `description`: works today, but is not "always".** The description is in the catalog every session, and the catalog tells the model it "must use that skill for that turn" when the task matches (§4). This is **from source.** Nothing can mark it always-on, the body is not carried across turns, and whether it fires is the model's judgement. It is the only mechanism a standard package has that works in Codex at main without user action beyond installing and enabling the plugin.

3. **Not available to a plugin:** AGENTS.md or instruction files (a plugin directory is never read, §3), `onboardingSkill` (metadata for clients, not auto-run in open-source core; closed-client behaviour unverified), and `defaultPrompt` (UI suggestions).

4. **Workaround outside the standard format:** a package with **no root `plugin.json`** and a `.codex-plugin/plugin.json` (or `.claude-plugin/plugin.json`) gets the legacy format, and `hooks/hooks.json` is default-discovered and loaded (`loader.rs` L1228-1240; test L735-758). That package is not an Agent Plugins 1.0.0 package, and trust review still applies. I record it here as the only source-evidenced way hooks load for a third-party plugin at main, **not** as a recommendation for a repository whose rule is a real root `plugin.json`.

**What each conclusion rests on:**
- **Documented** (second-hand, blocked page): the `extensions.com.openai` hooks route; plugin hooks require trust.
- **From source at `694d8d4`:** everything with a path and line number above, including the AgentPlugin hook short-circuit, the fixed `./skills` and `./mcp.json`, the extension fields honoured (`apps`, `hooks`, `onboardingSkill`, `interface`), the plain-stdout and `additionalContext` → developer message path, the 2,500-token spill, the trust model, and the skill catalog trigger rule.
- **Unverified:** any runtime behaviour of a released binary; #45999's `additionalContext` failure; whether any closed client auto-runs `onboardingSkill`; the exact wording on developers.openai.com.
