# Plugin hooks: Claude Code and Codex CLI

Researched 2026-09-24, clean room, no repository access. Every fact names its source and its kind: documentation, source, or third-party observation. What was not found is said so.

Method note. The rendered docs pages were read as Markdown (`code.claude.com/docs/en/<page>.md`, `learn.chatgpt.com/docs/<page>.md`, `developers.openai.com/plugins/build/plugins.md`), downloaded with `curl` and grepped. Line numbers below are line numbers in those downloads on 2026-09-24. Two earlier WebFetch summaries of the Claude hooks page returned sentences that are not in the Markdown (a "Note on /compact and /clear" paragraph and a "Neither stdout nor additionalContext reach the subagent" sentence). They are discarded; only the downloaded text is cited.

Versions dated against: Claude Code CHANGELOG top heading `## 2.1.282` at commit `ddcb43a`; Codex latest release `rust-v0.156.1`, published 2026-09-23 (GitHub releases API).

## 1. Unknown key on a command hook handler in `hooks/hooks.json`

Short answer: the documentation does not state what happens to an unknown key inside a hook handler object. It states what happens to unknown top-level `plugin.json` fields, and to a top-level `$schema` in `hooks.json`. Two third-party issues report a startup notice naming unknown keys in `hooks.json`; the CHANGELOG confirms such a notice exists. SchemaStore's settings schema closes the handler object with `additionalProperties: false`, but that schema is community-maintained, not Anthropic's.

### Documentation

- Unknown top-level `plugin.json` fields are ignored at load and warned about by `validate`. `plugins-reference.md` lines 513-524:
  > Claude Code ignores top-level fields it does not recognize. You can keep metadata from another ecosystem in `plugin.json` and the plugin still loads.
  > `claude plugin validate` reports unrecognized fields as warnings, not errors. If a field is one or two characters off from a recognized one, the warning suggests the likely intended name. A plugin with only unrecognized-field warnings still passes validation and loads at runtime.
  Source: https://code.claude.com/docs/en/plugins-reference.md (documentation). The heading is "Unrecognized fields" and the paragraph is about `plugin.json`. It says nothing about `hooks.json` handler objects.
- `hooks.json` `$schema` is tolerated. `plugins-reference.md` line 105:
  > `hooks/hooks.json` can carry a top-level `$schema` key that names a JSON Schema URL for editor autocomplete and validation. Claude Code ignores the key at load time.
  Source: same page (documentation).
- `validate` reads `hooks.json`. `plugin-marketplaces.md` line 1412, table "Claude Code checks": `plugin.json`, `hooks/hooks.json`, and the `skills`, `agents`, and `commands` directories at the plugin root. Line 1449: "`Invalid JSON syntax: ...` on `hooks/hooks.json`: fix the JSON syntax. Until you do, a session loads the plugin without the hooks in that file." Source: https://code.claude.com/docs/en/plugin-marketplaces.md (documentation). Line 1441 of `plugins-reference.md` says the same run checks these files "for syntax and schema errors". Neither page says what an unknown handler key produces.
- The only sentence about an unknown key on a hook object is about `matcher`. `hooks.md` line 353: "If you add a `matcher` field to an event without matcher support, it is silently ignored." Source: https://code.claude.com/docs/en/hooks.md (documentation). This is a known key on the wrong event, not an unknown key.
- `--strict` turns warnings into errors. `plugins-reference.md` line 1334: "Treat warnings as errors and exit 1 on them. Use in CI to catch issues the runtime tolerates, such as unrecognized fields." (documentation).

### CHANGELOG (Anthropic's repository; release notes, not documentation)

Pinned copy: https://github.com/anthropics/claude-code/blob/ddcb43a29b2d4da61fd22a55f6030c6d376b0545/CHANGELOG.md

- Line 629, under `## 2.1.274`: "Fixed plugins with a top-level `$schema` in `hooks/hooks.json` showing an "unknown key" notice". This confirms Claude Code emits an "unknown key" notice for keys in `hooks.json` it does not recognise, and that `$schema` was carved out.
- Line 5239, under `## 2.1.77`: "Improved `claude plugin validate` to check skill, agent, and command frontmatter plus `hooks/hooks.json`, catching YAML parse errors and schema violations".
- Line 207, under `## 2.1.281`: "added a `claude plugin validate` warning when a shell-form hook leaves `${CLAUDE_PLUGIN_ROOT}` unquoted". So `validate` reads handler objects, not just the file's syntax.

### Third-party observation (not documentation, not Anthropic source)

- https://github.com/affaan-m/ECC/issues/3063 (open, filed 2026-09-10). Reported notice, quoted by the reporter: `hooks.json: unknown keys "$schema", "description" in hooks.PreToolUse[0], "id" in hooks.PreToolUse[0], ... and 42 more ignored`. The reporter says the hooks still ran. The keys were at matcher-entry level (`hooks.PreToolUse[0]`), not inside a handler object.
- https://github.com/WorldFlowAI/everything-claude-code/issues/13 (open, filed 2026-09-14). Same notice shape, reporter says all commands still registered and executed. The reporter places `description` inside handler items; the quoted notice path (`hooks.PreToolUse[0]`) is a matcher entry, so the level is not settled by the quote.
- Both reports say the notice is a warning and the file still loads. Neither cites Anthropic source. Claude Code's loader source is not public; the anthropics/claude-code repository root holds no `src/` (contents API listing on 2026-09-24: `.claude-plugin, .claude, .devcontainer, .github, .vscode, CHANGELOG.md, LICENSE.md, README.md, SECURITY.md, Script, demo.gif, examples, feed.xml, mods, plugins, scripts`).

### JSON schema

- No Anthropic-published schema for `hooks.json` was found. The docs point to SchemaStore for `plugin.json` (`plugins-reference.md` line 543: example `$schema` value `https://json.schemastore.org/claude-code-plugin-manifest.json`) and for settings (`settings.md` line 554: "The `$schema` line points to the published JSON schema ... The schema can lag behind the newest CLI releases, so a validation warning on a recently documented key doesn't mean your configuration is invalid."). (documentation)
- SchemaStore `claude-code-settings.json` (fetched from https://www.schemastore.org/claude-code-settings.json on 2026-09-24; `$id` `https://json.schemastore.org/claude-code-settings.json`, title "Claude Code Settings"). Its `hookCommand` definition is a `oneOf`; the command branch has properties `type, command, timeout, async, asyncRewake, shell, if, statusMessage, args` and `additionalProperties: false`. `hookMatcher` has properties `matcher, hooks` and `additionalProperties: false`. So an `additionalContextLimit` key fails this schema. (source: schema file)
- That schema is community-maintained. The first five commits touching `src/schemas/json/claude-code-settings.json` in SchemaStore/schemastore are by Matthew Wagerfield (2025-06-17, "Add Claude Code settings.json schema (#4798)"), adam jones, thomscode, Brennan Goewert, Jim Mazur; the latest is `d2cbdcde9855c1bf9ea99c336163cc6c93753e39` (2026-08-03, Alex Chen). No Anthropic authorship is shown. (GitHub commits API, 2026-09-24)
- The unofficial hesreallyhim/claude-code-json-schema repository is archived (README says archived 2026-04-27 because schemas moved to SchemaStore) and never held a hooks schema. (third-party)

### Verdict for question 1

- Documented: unknown top-level `plugin.json` fields are ignored and warned; `hooks.json` `$schema` is ignored; `validate` reads `hooks.json` for "schema errors". Not documented: the fate of an unknown key inside a `type: "command"` handler.
- Observed by third parties and consistent with CHANGELOG 2.1.274: Claude Code prints an "unknown keys ... ignored" notice for unrecognised `hooks.json` keys and loads the hooks anyway. Whether `claude plugin validate` reports such a key as a warning is not stated anywhere read; the "unrecognized fields" warning paragraph is written about `plugin.json`.
- Not found: any Anthropic statement that an unknown handler key is rejected. Not reachable: Claude Code's loader source (not published).

## 2. SessionStart and SubagentStart

All from https://code.claude.com/docs/en/hooks.md, downloaded 2026-09-24 (documentation).

- Plain stdout is context for SessionStart. Line 810: "For most events, Claude Code writes stdout to the debug log and doesn't show it in the transcript. The exceptions are `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart`, and `PostModelSwitch`, where Claude Code adds plain-text stdout as context that Claude can see and act on." Line 1209: "Since plain stdout already reaches Claude for this event, a hook that only loads context can print to stdout directly without building JSON."
- Matcher values. Line 310, matcher table row for `SessionStart`: `startup`, `resume`, `clear`, `compact`, `fork`. Lines 1134-1138: `startup` "New session"; `resume` "`--resume`, `--continue`, or `/resume`"; `clear` "`/clear`"; `compact` "Auto or manual compaction"; `fork` "A new session forked from an existing one: `--fork-session` with `--resume` or `--continue`, the `/fork` background copy, or `/branch`". Line 1140: "Before v2.1.214, forked sessions reported source `"resume"`."
- SessionStart hook types. Line 1128: "Only `type: "command"` and `type: "mcp_tool"` hooks are supported."
- Re-injection after `/compact` and `/clear`. No sentence says earlier SessionStart output is re-injected. What is said: SessionStart fires again. Line 583: "after `/clear` or a compaction, `SessionStart` fires again with the servers already available, and its `mcp_tool` hooks run." Line 1156: `source` is `"clear"` after `/clear`, `"compact"` after compaction. Line 1195: `sessionTitle` is "ignored on `"clear"` and `"compact"`". Line 1144: "If you run `/clear` or switch to another conversation while background hooks are still running, nothing they return applies to the session." So context survives only by the hook running again under the `clear` or `compact` matcher. An explicit "not re-injected" sentence: not found.
- SubagentStart exists. Line 2359 heading `### SubagentStart`; line 2361: "Runs when Claude spawns a subagent with the Agent tool, when Claude resumes a subagent, and each time an in-process agent team teammate handles a new message." CHANGELOG line 6597 under `## 2.0.43`: "Added the `SubagentStart` hook event" (release notes).
- SubagentStart `additionalContext` reaches the subagent. Line 2382: "SubagentStart hooks can't block subagent creation, but they can inject context into the subagent." Line 2384: "`additionalContext` | String added to the subagent's context at the start of its conversation, before its first prompt." Line 2395: "When the hook runs again for the same subagent, Claude Code injects the returned context only when the subagent's context doesn't already hold the copy from an earlier run. ... After auto-compaction discards that copy, Claude Code injects the next run's context again."
- SubagentStart plain stdout. `SubagentStart` is not in the line-810 list of events whose plain stdout becomes context. The SubagentStart section lists only the JSON `additionalContext` field. Conclusion: plain stdout is not documented as reaching the subagent; use JSON `hookSpecificOutput.additionalContext`.
- SubagentStart hook types. CHANGELOG line 3808 under `## 2.1.142`: "configuring a prompt- or agent-type hook for `SessionStart`/`Setup`/`SubagentStart` now shows a clear "use a command-type hook instead" error" (release notes).

## 3. Exec form (`command` plus `args`) and `${CLAUDE_PLUGIN_ROOT}`

All from https://code.claude.com/docs/en/hooks.md unless noted (documentation).

- Field table, line 458: "`command` | yes | Shell command to execute. With `args`, the executable to spawn directly."
- Line 459: "`args` | no | Argument list. When present, `command` is resolved as an executable and spawned directly with `args` as the argument vector, with no shell involved."
- Line 462, `shell`: "... Ignored when `args` is set".
- Line 466 heading "Exec form and shell form". Line 468: "A command hook runs as exec form when `args` is set, and shell form when `args` is omitted. Set `args` whenever the hook references a path placeholder, since each element is passed as one argument with no quoting."
- Line 470: "**Exec form** runs when `args` is present. Claude Code resolves `command` as an executable on `PATH` and spawns it directly with `args` as the argument vector. There is no shell, so each `args` element is one argument exactly as written, and path placeholders like `${CLAUDE_PLUGIN_ROOT}` are substituted into `command` and into each `args` element as plain strings."
- Line 472: "**Shell form** runs when `args` is absent. The `command` string is passed to a shell: `sh -c` on macOS and Linux, Git Bash on Windows, or PowerShell when Git Bash isn't installed."
- Line 484, example: `"args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"]`.
- Line 497: "Both forms support the same path placeholders, and both export them as the environment variables `CLAUDE_PROJECT_DIR`, `CLAUDE_PLUGIN_ROOT`, and `CLAUDE_PLUGIN_DATA` on the spawned process".
- Line 622: "`${CLAUDE_PLUGIN_ROOT}`: the plugin's installation directory, for scripts bundled with a plugin."
- Line 499: "Plugin hooks additionally substitute `${user_config.*}` values, in exec form only".
- `plugins-reference.md` line 775: "In hook commands, use exec form with `args` so each path is passed as one argument with no quoting."
- Introduced: CHANGELOG line 3898 under `## 2.1.139`: "Added hook `args: string[]` field (exec form) that spawns the command directly without a shell, so path placeholders never need quoting" (release notes).

## 4. Codex CLI: where plugin hooks are declared, and `additionalContextLimit`

### Documentation

Packaging page: https://developers.openai.com/plugins/build/plugins.md, downloaded 2026-09-24.

- Line 22-24: "Put OpenAI-specific presentation, registered MCP server mappings, and hook settings under `extensions.com.openai` in root `plugin.json`. Existing `.codex-plugin/plugin.json` files remain supported as a compatibility fallback."
- Lines 607-609 and example lines 620-622: `"extensions": { "com.openai": { "apps": "./.app.json", "hooks": "./hooks/hooks.json", ...` .
- Line 647-649: "When `extensions.com.openai` is an object, it replaces the entire `.codex-plugin/plugin.json` overlay as the source of OpenAI-specific settings; the two aren't merged."
- Line 666: "`hooks` points to lifecycle hook configuration."
- Lines 744-745: "Codex discovers `hooks/hooks.json` by default when the selected OpenAI extension or compatibility manifest doesn't define `hooks`". The example `hooks/hooks.json` there (lines 748-760) uses `"type": "command"`, `"command": "python3 ${PLUGIN_ROOT}/hooks/session_start.py"`, `"statusMessage"`.
- Lines 766-769: "To override that default, define `hooks` inside `extensions.com.openai` in root `plugin.json`. The field can be a single path, an array of paths, an inline hooks object, or an array of inline hooks objects. An explicit value replaces default-file discovery; it doesn't add to `hooks/hooks.json`."
- Lines 740-742: "Installing or enabling a plugin doesn't automatically trust its hooks. Plugin-bundled hooks are non-managed hooks, so Codex skips them until the user reviews and trusts the current hook definition."

Hooks page: https://learn.chatgpt.com/docs/hooks.md (the `developers.openai.com/codex/hooks` URL 308-redirects here), downloaded 2026-09-24.

- Lines 373-375: "By default, Codex looks for `hooks/hooks.json` inside the plugin root. A plugin manifest can override that default with a `hooks` entry in `.codex-plugin/plugin.json`." This page names only the compatibility manifest; the packaging page names `extensions.com.openai.hooks`.
- Lines 392-397: `PLUGIN_ROOT`, `PLUGIN_DATA`; "Codex also sets `CLAUDE_PLUGIN_ROOT` and `CLAUDE_PLUGIN_DATA` for compatibility with existing plugin hooks."
- Command handler fields, lines 184-192: `timeout`, `statusMessage`, `additionalContextLimit`, `commandWindows`, `async`. No `args` field is documented for Codex.
- Line 186: "`additionalContextLimit` sets how much `additionalContext` a command hook can send to the model before Codex saves the full text to disk and sends a shorter preview instead."
- Lines 536-553: "For any command hook that returns `additionalContext`, set `additionalContextLimit` on the handler to customize the approximate token threshold ... Omit `additionalContextLimit` to use the default `2500`-token threshold. Use a positive integer to select a different threshold, or `0` to pass the handler's complete additional context directly to the model. ... For events that can't produce additional context, Codex ignores `additionalContextLimit` and reports a configuration warning."
- Events whose sections document `additionalContext` output: SessionStart (line 660), SubagentStart (732), PreToolUse (793), PostToolUse (915), UserPromptSubmit (1006).
- Unknown fields: not addressed on either page.

### Source (commit permalinks)

- `additionalContextLimit` is defined on the command handler. https://github.com/openai/codex/blob/c2abf869d539a6326a6e5a125dfdb8a5dc488ab4/codex-rs/config/src/hook_config.rs lines 162-185: `#[serde(tag = "type")] pub enum HookHandlerConfig { #[serde(rename = "command")] Command { command, command_windows ("commandWindows"), timeout_sec ("timeout"), r#async, status_message ("statusMessage"), additional_context_limit (#[serde(default, rename = "additionalContextLimit", skip_serializing_if = "Option::is_none")]) : Option<usize> }`. Doc comment lines 175-178: "Approximate token threshold for spilling this hook's `additionalContext` to disk. Unset uses 2,500 tokens; `0` disables spilling for this hook."
- Unknown keys in Codex `hooks.json`. Same file line 11-12: `#[serde(deny_unknown_fields)] pub struct HooksFile { description: Option<String>, hooks: HookEventsToml }`. `MatcherGroup` (line 154) and `HookHandlerConfig` (line 163) carry no `deny_unknown_fields`. Serde therefore rejects an unknown top-level key in the file and ignores an unknown key inside a matcher group or a handler object. Files are parsed as `HooksFile` at https://github.com/openai/codex/blob/108e6a6dbeed5485b3b732ed4a29c002780c8632/codex-rs/core-plugins/src/loader.rs line 1265 (plugin hooks; parse failure pushes the warning "failed to parse plugin hooks config ..." and skips the file) and at https://github.com/openai/codex/blob/c7c824dce4da186e5142af5d9a1587ae553efe46/codex-rs/hooks/src/engine/discovery.rs line 359.
- Which events keep `additionalContextLimit`: discovery.rs (same permalink) lines 539-555: kept for `PreToolUse | PostToolUse | SessionStart | UserPromptSubmit | SubagentStart`; otherwise the warning "ignoring additionalContextLimit for {event_name:?} hook in {}: this event cannot emit additionalContext" is pushed and the value dropped. This matches the documented event set.
- Where `extensions.com.openai.hooks` is read: https://github.com/openai/codex/blob/05de93520542d5d1a3f3af76ad446607a12d98fd/codex-rs/core-plugins/src/agent_plugin_manifest.rs line 17 `CODEX_AGENT_PLUGIN_EXTENSION_NAMESPACE: &str = "com.openai"`, lines 89-92 read `extensions["com.openai"]`, line 211 `resolved.paths.hooks = extension.paths.hooks;` in `apply_codex_agent_plugin_extension`.
- Whether those hooks then load: https://github.com/openai/codex/blob/108e6a6dbeed5485b3b732ed4a29c002780c8632/codex-rs/core-plugins/src/loader.rs lines 950-960:
  ```
  let (hook_sources, hook_load_warnings) =
      if loaded_manifest.format == PluginManifestFormat::AgentPlugin {
          (Vec::new(), Vec::new())
      } else {
          load_plugin_hooks(...)
      };
  ```
  For an Agent Plugins format manifest the hook list is empty and `load_plugin_hooks` is never called. `load_plugin_hooks` (line 1189, comment lines 1186-1188) is the function that reads manifest `hooks` entries or the default `hooks/hooks.json`. A second `AgentPlugin` early return for apps is at line 1134.
- Open issue on exactly this: https://github.com/openai/codex/issues/47925 "Hooks from Agent Plugins 1.0 plugins are never loaded (extensions.com.openai.hooks ignored)", open, filed 2026-09-24, against 0.156.1, cites the same `loader.rs` lines. No maintainer reply at read time. An older open issue, https://github.com/openai/codex/issues/16430 (2026-04-01), reports plugin-local hooks not executing. (third-party reports; the source above is the primary evidence)

### Verdict for question 4

- Documented: hooks are declared as `extensions["com.openai"].hooks` in root `plugin.json` (path, array of paths, inline object, or array of inline objects), with `.codex-plugin/plugin.json` `hooks` as fallback and `hooks/hooks.json` as default discovery. Documented and in source: `additionalContextLimit` is a field of the `type: "command"` handler, default 2500, `0` disables spilling, accepted on SessionStart, SubagentStart, PreToolUse, PostToolUse, UserPromptSubmit, warned and dropped elsewhere.
- Source at the pinned commits: a manifest in Agent Plugins format yields no hooks at all, so the documented declaration does not currently take effect in the Rust loader. Reported as open issue #47925.
- Not found: any Codex documentation of an `args` array for command hooks, or of unknown-field handling. The source shows unknown handler keys are ignored (no `deny_unknown_fields` on the handler enum) and unknown top-level keys in `hooks.json` fail the parse.

## Not reached or not found, in one place

- Claude Code loader source: not published; behaviour for unknown handler keys rests on CHANGELOG 2.1.274 plus two third-party issues.
- An Anthropic-published JSON schema for `hooks.json`: not found. SchemaStore's settings schema is community-authored.
- A Claude docs sentence on SessionStart context re-injection after `/compact` or `/clear`: not found; the docs say the hook fires again with `source` `compact` or `clear`.
- Codex docs on unknown fields or on an `args` array: not found.
- All docs pages were reachable; no fetch was blocked.
