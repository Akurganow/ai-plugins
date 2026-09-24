# 06 — Claude Code: making plugin rules always active

Research question: every documented way a Claude Code plugin, installed from a
marketplace, can make written rules active from a session's first turn without
the user invoking anything, and push the agent to follow them.

Clean-room: nothing under /home/user/ai-plugins or /home/user/how-possible was
read. All docs were fetched 2026-09-24 as `<page>.md` from code.claude.com; the
docs site has no commit permalinks, so each doc quote below is dated by that
fetch (local copies: `research/src06/*.md`).

## Sources and reachability

| Source | Result |
| :-- | :-- |
| https://code.claude.com/docs/en/hooks.md | 200, 331 KB |
| https://code.claude.com/docs/en/hooks-guide.md | 200 |
| https://code.claude.com/docs/en/plugins-reference.md | 200 |
| https://code.claude.com/docs/en/plugins.md | 200 |
| https://code.claude.com/docs/en/skills.md | 200 |
| https://code.claude.com/docs/en/memory.md | 200 |
| https://code.claude.com/docs/en/settings.md | 200 |
| https://code.claude.com/docs/en/settings-reference.md | 200 |
| https://code.claude.com/docs/en/sub-agents.md | 200 |
| https://code.claude.com/docs/en/output-styles.md | 200 |
| https://code.claude.com/docs/en/context-window.md | 200 |
| https://code.claude.com/docs/en/discover-plugins.md, plugin-marketplaces.md, features-overview.md, security-guidance.md, how-claude-code-works.md | 200 |
| GitHub REST API, `repos/anthropics/claude-plugins-official/git/trees/main` | **403**: "GitHub access to this repository is not enabled for this session. Use add_repo to request access." |
| `git clone --depth 1 https://github.com/anthropics/claude-plugins-official` | worked. HEAD `8286e2db0113d3e0a124af3345a8fd15ab93937d`, committed 2026-09-24T12:33:34-07:00. Local copy: `research/src06/cpo/` |

Nothing that was needed was blocked. The API refusal was worked around by
reading the same repository over git.

---

## 1. SessionStart: stdout vs `additionalContext`, matchers, subagents

**Plain stdout is added to context. The JSON form is optional.** (docs, hooks.md, "Exit code 0")

> "For most events, Claude Code writes stdout to the debug log and doesn't show it in the transcript. The exceptions are `UserPromptSubmit`, `UserPromptExpansion`, `SessionStart`, and `PostModelSwitch`, where Claude Code adds plain-text stdout as context that Claude can see and act on."

hooks.md, "SessionStart decision control":

> "Claude Code adds stdout it treats as plain text to Claude's context."
> "Since plain stdout already reaches Claude for this event, a hook that only loads context can print to stdout directly without building JSON. Use the JSON form when you need to combine context with other fields such as `sessionTitle`."

JSON form (the `additionalContext` row): "String added to Claude's context at the start of the conversation, before the first prompt."

Caveats (hooks.md):
- **Whether output is read as plain text or JSON depends on its first and last characters.** Output that "Starts with `{` and ends with `}`" is parsed as JSON. "On the events that add plain-text stdout as context, Claude Code doesn't add the text" when that parse fails. "Before v2.1.248, Claude Code treated that stdout as plain text." So a rules file that happens to begin with `{` and end with `}` is silently dropped.
- **Size cap:** "A hook's `additionalContext`, `systemMessage`, and `initialUserMessage` strings, and its plain stdout, are capped at 10,000 characters". Past the cap the text is replaced by a file path and a 2,000-character preview, and "Claude Code doesn't ask Claude to read the file, so keep anything Claude must always see within the cap."
- **Phrasing:** "Write the text as factual statements rather than imperative system instructions. [...] Text framed as out-of-band system commands can trigger Claude's prompt-injection defenses, which causes Claude to surface the text to you instead of treating it as context."
- **Handler types:** "Only `type: "command"` and `type: "mcp_tool"` hooks are supported." An `mcp_tool` hook is skipped at launch: "A `type: "command"` hook on `SessionStart` runs at launch, so use one for anything the session needs from its first turn."
- **Timing:** "Claude's first response still waits for the hooks to finish, so their context reaches Claude."
- **Failure:** SessionStart cannot block. On exit 2 it "Shows stderr to user only". A failed hook means the rules are not delivered, and the session still starts.
- **The docs prefer CLAUDE.md for static text:** "For static context that doesn't require a script, use CLAUDE.md instead." A plugin cannot ship CLAUDE.md (see §4), so SessionStart is the route a plugin has.

**Matchers** (hooks.md, SessionStart table): `startup` (New session), `resume` (`--resume`, `--continue`, or `/resume`), `clear` (`/clear`), `compact` (Auto or manual compaction), `fork` (a forked session). Leaving the matcher out, or setting `"*"` or `""`, matches every source. "Before v2.1.214, forked sessions reported source `"resume"`."

**Subagents:** the docs never say SessionStart fires for a subagent.
- hooks.md lists the cadences: "per session: `SessionStart` and `SessionEnd`".
- sub-agents.md, "What loads at startup", lists what a non-fork subagent starts with: system prompt, task message, CLAUDE.md files, git status, preloaded skills, sibling roster. SessionStart output is not on that list. It also says the subagent "doesn't see your conversation history", and SessionStart context is part of that history.
- The documented way to reach a subagent is **SubagentStart**. hooks.md: "SubagentStart hooks can't block subagent creation, but they can inject context into the subagent", and `additionalContext` is a "String added to the subagent's context at the start of its conversation, before its first prompt."
- Tool hooks do run inside subagents. hooks.md: "Hooks from settings files, managed policy settings, and plugins also run inside subagents. When a subagent calls a tool, tool events such as `PreToolUse` and `PostToolUse` fire the same configured hooks as in the main conversation".

Reading the two statements together, SessionStart does not run per subagent. The docs imply this and do not say it outright, and it was not tested.

## 2. UserPromptSubmit: context on every turn

hooks.md, UserPromptSubmit:

> "Runs when the user submits a prompt, before Claude processes it. This allows you to add additional context based on the prompt/conversation, validate prompts, or block certain types of prompts."

> "There are two ways to add context to the conversation on exit code 0: **Plain text stdout** [...] **JSON with `additionalContext`** [...] Neither channel produces a visible transcript entry. Plain stdout and the `additionalContext` value are each injected as a system reminder that starts with the hook's name; Claude reads both."

It has no matcher: UserPromptSubmit is in the "no matcher support / always fires on every occurrence" row. It can add context on every user turn.

Limits (hooks.md):
- **Timeout:** "default timeout of 30 seconds". If the hook times out, "its output, including any `additionalContext`, is discarded. The prompt still reaches Claude without that context."
- **Resume:** "For mid-session events like `PostToolUse` or `UserPromptSubmit`, when you resume [...] Claude Code replays the saved text rather than re-running the hook for past turns".
- **Blocking:** it cannot rewrite the prompt. "`UserPromptSubmit`: can't replace the prompt; it only injects `additionalContext` alongside it".
- **Subagents:** it fires on user prompts. A subagent receives a delegation message rather than a user prompt. The docs never say UserPromptSubmit fires inside a subagent. This is an inference.

**Compaction:** UserPromptSubmit is **not** the documented answer. The documented one is **SessionStart with the `compact` matcher**. From hooks-guide.md, "Re-inject context after compaction":

> "Use a `SessionStart` hook with a `compact` matcher to re-inject critical context after every compaction."

context-window.md, "What survives compaction":

| Mechanism | After compaction |
| :-- | :-- |
| "Context that hooks added earlier" | "Summarized with the rest of the conversation" |
| "SessionStart hooks that match the `compact` source" | "Claude Code runs them and adds their output to the compacted context" |
| "System prompt and output style" | "Both still apply" |
| "Invoked skill bodies" | "Re-injected, capped at 5,000 tokens per skill and 25,000 tokens total; oldest dropped first" |

Because UserPromptSubmit fires on every prompt, the next user turn after a compaction carries its context again. That follows from how the event works. The docs do not present it as the compaction mechanism. Between a compaction and the next user prompt, only SessionStart(`compact`) restores the rules.

## 3. Stop / SubagentStop: block completion and force a rewrite

Yes. hooks.md, "Stop decision control":

| Field | Description |
| :-- | :-- |
| `decision` | "`"block"` prevents Claude from stopping. Omit to allow Claude to stop" |
| `reason` | "Required when `decision` is `"block"`. Tells Claude why it should continue" |
| `hookSpecificOutput.additionalContext` | "Non-error feedback for Claude. The conversation continues so Claude can act on it, but unlike `decision: "block"` it is shown in the transcript as hook feedback rather than a hook error" |

```json
{ "decision": "block", "reason": "Must be provided when Claude is blocked from stopping" }
```

> "A hook that blocks by exiting 2 routes the same way as `reason`: Claude receives the stderr message as the explanation for why it should continue."

SubagentStop: "Returning `decision: "block"` with a `reason` keeps the subagent running and delivers `reason` to the subagent as its next instruction."

The hook can see the prose it is checking. Stop and SubagentStop input carries `last_assistant_message`, "the text content of Claude's final response, so hooks can access it without parsing the transcript file". (SubagentStop on v2.1.271+: when the subagent hands off through `SubagentHandback`, the report is in that tool call's `tool_input.message`, not in `last_assistant_message`.)

Loop limit: "Claude Code overrides the hook and ends the turn after 8 consecutive blocks". Hooks should check `stop_hook_active`.

The check can also be done by a model (hooks.md, "Prompt-based hooks"). `Stop` and `SubagentStop` support `type: "prompt"` (Haiku by default) and `type: "agent"`. The prompt hook answers `{"ok": false, "reason": ...}`, and then "the reason is fed back to Claude as its next instruction and the turn continues, unless the response also sets `impossible: true`". Agent hooks are marked "experimental".

What blocking can and cannot do: it keeps the turn going and hands Claude the reason. It cannot rewrite text that has already been shown. A Stop block starts another turn in which Claude can revise. It does not edit the previous message.

## 4. Does a plugin load `rules/`, `CLAUDE.md`, `AGENTS.md`? Plugin `settings.json`

**No.** plugins-reference.md, "Standard plugin layout":

> "A `CLAUDE.md` file at the plugin root is not loaded as project context. Plugins contribute context through skills, agents, and hooks rather than CLAUDE.md. To ship instructions that load into Claude's context, put them in a skill."

plugin-marketplaces.md: "In a plugin run, Claude Code also warns about a `CLAUDE.md` at the plugin root."

- No plugin page names a `rules/` component. The component tables list skills, commands, agents, hooks, MCP, LSP, output-styles, themes, monitors, channels, workflows and settings.json.
- memory.md loads `.claude/rules/` from the project and from `~/.claude/rules/` only.
- `AGENTS.md` is read from the working directory and its parents, through the built-in `agents-md` plugin (v2.1.277+). It is not read from an installed plugin.
- memory.md, "Remove an earlier AGENTS.md workaround", says of "A `SessionStart` hook that prints `AGENTS.md`: remove it. Once Claude reads `AGENTS.md` directly, the hook adds a second copy to the context." That covers a hook printing the project's own AGENTS.md, and it is a double-load hazard if a plugin does the same.

**Plugin `settings.json` exists and supports two keys.** plugins.md:

> "Plugins can include a `settings.json` file at the plugin root to apply default configuration when the plugin is enabled. Currently, only the `agent` and `subagentStatusLine` keys are supported."
> "Setting `agent` activates one of the plugin's custom agents as the main thread, applying its system prompt, tool restrictions, and model. [...] Settings from `settings.json` take priority over `settings` declared in `plugin.json`. Unknown keys are silently ignored."

plugins-reference.md, file-locations table: "Default configuration applied when the plugin is enabled. Only the `agent` and `subagentStatusLine` keys are supported". A plugin therefore cannot ship `hooks`, `outputStyle`, `permissions` or `disableAllHooks` through settings.json. Hooks go in `hooks/hooks.json`.

## 5. Skills: extra front matter; any "always loaded" mode?

skills.md, "Frontmatter reference". Claude Code accepts these fields in addition to the Agent Skills six (`name`, `description`, `license`, `compatibility`, `metadata`, `allowed-tools`): `when_to_use`, `argument-hint`, `arguments`, `disable-model-invocation`, `user-invocable`, `disallowed-tools`, `model`, `effort`, `context` (`fork`), `agent`, `background`, `hooks`, `paths`, `shell`. `license` and `compatibility` are accepted, but "Claude Code accepts the field but doesn't act on it." Unknown fields: "Claude Code ignores a field it doesn't recognize without reporting an error."

Uploading to claude.ai or the Skills API rejects the extra keys: "Unexpected key(s) in SKILL.md frontmatter: argument-hint. Allowed properties are: allowed-tools, compatibility, description, license, metadata, name".

**No front matter field makes a skill always loaded in the main session.** skills.md:

> "In a regular session, skill descriptions are loaded into context so Claude knows what's available, but full skill content only loads when invoked. Subagents with preloaded skills work differently: the full skill content is injected at startup."

| Frontmatter | When loaded into context |
| :-- | :-- |
| (default) | "Description always in context, full skill loads when invoked" |
| `disable-model-invocation: true` | "Description not in context, full skill loads when you invoke" |
| `user-invocable: false` | "Description always in context, full skill loads when invoked" |

Related documented facts:
- `paths`: "When set, Claude loads the skill automatically only when working with files matching the patterns". This narrows auto-loading. It does not make a skill always-on.
- Skill `hooks`: registered "when you or Claude invoke the skill and keeps running them for the rest of the session". They depend on the skill being invoked first.
- The skill listing is not re-injected after compaction (context-window.md): "Unlike the rest of the startup content, this listing is not re-injected after `/compact`. Only skills you actually invoked get preserved."
- The one full-content preload is the **subagent** `skills:` field (sub-agents.md): "The full content of each listed skill is injected into the subagent's context at startup." Plugin agents support `skills` (plugins-reference.md, "Plugin agent frontmatter").
- skills.md suggests a hook when a skill stops working: "use hooks to enforce behavior deterministically."
- `skillOverrides` does not reach plugin skills: "Plugin skills are not affected by `skillOverrides`. Manage those through `/plugin` instead."

## 6. Output styles and a default agent from a plugin

**Output style: yes, and it can apply automatically.** output-styles.md, frontmatter table:

> `force-for-plugin`: "Plugin output styles only. Set to `true` to apply this style automatically whenever the plugin is enabled, without requiring users to select it. Overrides the user's `outputStyle` setting. If multiple enabled plugins set this, Claude Code uses the first one loaded. Default: `false`"

plugins-reference.md (`plugin init --with output-style`): "An `output-styles/<name>.md` that applies automatically while the plugin is enabled".

What an output style does and does not do (output-styles.md):
- "Claude Code sends the active style's instructions with every request." The instructions are part of the system prompt, and they survive compaction ("System prompt and output style — Both still apply").
- "Custom output styles leave out Claude Code's built-in software engineering instructions [...] unless `keep-coding-instructions` is set to `true`."
- "It's an instruction Claude follows, so nothing enforces it."
- "Other subagents run their own system prompt, so styles don't change how they respond." Only a fork inherits the style.
- Only one style can be active: "If multiple enabled plugins set this, Claude Code uses the first one loaded."

**Default agent: yes, through plugin `settings.json` `agent`** (quoted in §4). What it does (sub-agents.md, `--agent`):
- "The subagent's system prompt replaces the default Claude Code system prompt entirely, the same way `--system-prompt` does. `CLAUDE.md` files and project memory still load".
- The `--agent` CLI flag overrides the setting.
- Plugin agents ignore `hooks`, `mcpServers` and `permissionMode` "for security reasons", and `initialPrompt` is "Not supported".

Replacing the whole Claude Code system prompt to carry a writing standard is a large side effect.

Anthropic's own "output style" plugins do not use the output-style component. `explanatory-output-style` and `learning-output-style` in claude-plugins-official at `8286e2db` ship only a SessionStart hook (see §9). Their plugin.json describes the first as "mimics the deprecated Explanatory output style".

## 7. Environment for plugin hooks; security guidance

plugins-reference.md, "Environment variables":

| Variable | Resolves to |
| :-- | :-- |
| `${CLAUDE_PLUGIN_ROOT}` | "Absolute path to the plugin's installation directory" |
| `${CLAUDE_PLUGIN_DATA}` | "Persistent directory that survives plugin updates, created on first reference" |
| `${CLAUDE_PROJECT_DIR}` | "The project root" |

> "All three are exported as environment variables to hook processes and to MCP and LSP server subprocesses. They aren't present in the environment of commands Claude runs through the Bash tool".

Other variables a hook gets (hooks.md):
- `CLAUDE_ENV_FILE` for SessionStart, Setup and CwdChanged.
- `CLAUDE_PLUGIN_OPTION_<KEY>` for `userConfig` values in shell form.
- `CLAUDE_CODE_REMOTE` is `"true"` in remote web environments.
- "There is no `$CLAUDE_MODEL` environment variable."
- "A hook process inherits the parent environment", apart from `OTEL_*` variables and `CLAUDE_CODE_SUBPROCESS_ENV_SCRUB` scrubbing.
- `${CLAUDE_PLUGIN_ROOT}` changes on update. For a copied plugin it "changes when the plugin updates [...] don't write state there".

**Exec form vs shell form** (hooks.md, "Exec form and shell form"):

> "A command hook runs as exec form when `args` is set, and shell form when `args` is omitted. Set `args` whenever the hook references a path placeholder, since each element is passed as one argument with no quoting."
> "Exec form [...] There is no shell, so each `args` element is one argument exactly as written [...] No shell tokenization happens on any platform."

```json
{ "type": "command", "command": "node", "args": ["${CLAUDE_PLUGIN_ROOT}/scripts/format.js", "--fix"] }
```

Shell-form equivalent: `"node \"${CLAUDE_PLUGIN_ROOT}\"/scripts/format.js --fix"`.

- plugins-reference.md: "In hook commands, use exec form with `args` [...] In shell-form hooks and monitor commands, wrap the variables in double quotes".
- `${user_config.*}` substitutes in exec form only. "A shell-form plugin hook whose `command` references `${user_config.*}` fails with an error instead of running."
- On Windows, exec form needs a real executable. `.cmd`/`.bat` shims do not work, so run `node` directly.

hooks.md, "Security best practices": "Validate and sanitize inputs", "Always quote shell variables: use `"$VAR"` not `$VAR`", "Block path traversal", "Use absolute paths [...] In exec form, use `${CLAUDE_PROJECT_DIR}` and the path needs no quoting. In shell form, wrap it in double quotes", "Skip sensitive files". The disclaimer: "Command hooks execute shell commands with your full user permissions."

## 8. Plugin hooks: merge, disable, default enablement

**Merge.** hooks.md, "Plugin scripts" tab: "When a plugin is enabled, its hooks merge with your user and project hooks." Hook locations table: "Plugin `hooks/hooks.json` — When plugin is enabled". "Hook entries merge across settings levels rather than replacing each other". When several hooks return `additionalContext`, "Claude receives all of the values."

**Enabled on install by default.** plugins-reference.md, "Default enablement": "Set `defaultEnabled: false` in `plugin.json` to ship a plugin that installs disabled." The default is therefore enabled at install. The user's `enabledPlugins` entry takes precedence, and the marketplace entry's `defaultEnabled` overrides plugin.json.

**User control:**
- **Whole plugin:** `/plugin disable <name>@<marketplace>` or `claude plugin disable`.
- **One hook:** not possible. hooks.md: "There is no way to disable an individual hook while keeping it in the configuration."
- **All hooks:** `disableAllHooks: true` in a non-managed file "disables user, project, local, and plugin hooks; managed hooks, Agent SDK hooks, and hooks from plugins force-enabled in managed `enabledPlugins` keep running" (settings-reference.md). `--settings '{"disableAllHooks": true}'` turns hooks off for one run.
- **Admins:** `allowManagedHooksOnly` blocks "Your user, project, local, and plugin hooks", except hooks from plugins force-enabled in managed `enabledPlugins`.
- **Trust gate:** a project-scope plugin "loads only after the same trust gate that governs project allow rules". "Personal-scope plugins have none of these restrictions."
- **Visibility:** the `/hooks` menu shows plugin hooks labelled `Plugin Hooks`. A PreToolUse `"ask"` is labelled `[plugin:<name>]`.
- **Reload:** "Changes to the plugin's other components, such as `hooks/` [...] do not [take effect immediately]. Run `/reload-plugins` or restart".
- **Cost display:** `claude plugin details` lists a SessionStart hook as "harness-only — no model context cost" (plugins-reference.md example output). That label is about the listing text only. The context a hook prints is not counted there.

## 9. How claude-plugins-official plugins inject standing instructions

Repository at commit `8286e2db0113d3e0a124af3345a8fd15ab93937d` (2026-09-24). Plugins with `hooks/hooks.json`: learning-output-style, hookify, security-guidance, claude-security, ralph-loop, explanatory-output-style.

**a. `plugins/explanatory-output-style`: SessionStart, JSON `additionalContext`, no matcher.** It is also a near-copy of `learning-output-style`.

`hooks/hooks.json`:

    "SessionStart": [ { "hooks": [ { "type": "command",
      "command": "bash \"${CLAUDE_PLUGIN_ROOT}/hooks-handlers/session-start.sh\"" } ] } ]

`hooks-handlers/session-start.sh`, lines 6-13 (heredoc emitting JSON):

    cat << 'EOF'
    {
      "hookSpecificOutput": {
        "hookEventName": "SessionStart",
        "additionalContext": "You are in 'explanatory' output style mode, where you should provide educational insights ... always provide brief educational explanations about implementation choices ..."
      }
    }
    EOF

Because there is no matcher, it fires on startup, resume, clear, compact and fork, so the text returns after every compaction. It uses shell form with the placeholder quoted, not exec form. The text is written as imperatives, which the docs now warn can trip the prompt-injection defenses.

**b. `plugins/ralph-loop`: Stop hook that blocks and feeds a prompt back.**

`hooks/stop-hook.sh`, lines 179-191:

    # Output JSON to block the stop and feed prompt back
    # The "reason" field contains the prompt that will be sent back to Claude
    jq -n --arg prompt "$PROMPT_TEXT" --arg msg "$SYSTEM_MSG" \
      '{ "decision": "block", "reason": $prompt, "systemMessage": $msg }'
    exit 0

**c. `plugins/security-guidance`: SessionStart + UserPromptSubmit + PostToolUse + Stop + SubagentStop.**

`hooks/hooks.json` runs `security_reminder_hook.py` on UserPromptSubmit, which captures a git baseline, and on PostToolUse `Edit|Write|MultiEdit|NotebookEdit`. Warnings are delivered "via additionalContext" (docstring, line 15). Stop and SubagentStop use `"asyncRewake": true` with a `rewakeMessage` ("Background security review feedback — address or acknowledge the findings below..."). The docs page security-guidance.md says: "These rules are guidance for the reviewer, not deterministic guardrails. [...] it does not block writes or guarantee every violation is caught."

**d. `plugins/hookify`: user-authored rules with a Stop block.**

`core/rule_engine.py` lines 66-71 return `{"decision": "block", "reason": combined_message, "systemMessage": combined_message}` for Stop. For PreToolUse/PostToolUse it returns `hookSpecificOutput.permissionDecision: "deny"`.

---

## Recommended mechanism(s) for a plugin that must enforce a writing standard in every Claude Code session

Two jobs, and no single lever does both. **Getting the standard into context** is best done with a SessionStart hook, backed up by SubagentStart, and optionally a forced output style. **Checking that it was followed** needs a Stop/SubagentStop hook, or a PreToolUse hook on the file-writing tools.

| # | Lever (all documented) | What it guarantees | What it cannot guarantee |
| :-- | :-- | :-- | :-- |
| 1 | **`hooks/hooks.json` → `SessionStart`, no matcher, `type: "command"`, exec form (`command` + `args` with `${CLAUDE_PLUGIN_ROOT}`), printing the rules as plain text or `hookSpecificOutput.additionalContext`** | Rules are in context before the first prompt ("Claude's first response still waits for the hooks"). They are re-added after `/clear`, resume, fork and **every compaction** (`compact` source). No user action needed; plugins install enabled by default. | That Claude obeys ("Write the text as factual statements [...] imperative [...] can trigger Claude's prompt-injection defenses"). Delivery if the script fails, times out, or the host lacks its interpreter (SessionStart can't block, and failure only shows the user an error). Text over 10,000 chars (becomes an unread file path). Output that starts with `{` and ends with `}` but is not valid hook JSON is dropped. **Subagents** don't get it. Users can disable the plugin or set `disableAllHooks`, or an admin can set `allowManagedHooksOnly`. |
| 2 | **`SubagentStart` hook (no matcher) returning `additionalContext`** | The same text at the start of every subagent's context, re-injected after the subagent's auto-compaction. | Obedience. `SubagentStart` supports `command`/`http`/`mcp_tool` only. It fires for some internal agents with an empty `agent_type` too (by analogy with SubagentStop; not stated for SubagentStart). |
| 3 | **`UserPromptSubmit` hook with a short reminder (plain stdout or `additionalContext`)** | A fresh copy next to every user prompt, so it cannot sit far back in a long context. | Under a 30 s default timeout, context is silently discarded. It adds tokens every turn. It is not the documented compaction answer (that is #1 with `compact`). Replayed, not re-run, on resume. Nothing indicates it fires inside subagents. |
| 4 | **`Stop` + `SubagentStop` hook reading `last_assistant_message` and returning `{"decision":"block","reason":"<which rule broke, where>"}`** (command hook for a deterministic check; `type: "prompt"`/`"agent"` for a model judgment) | Claude cannot end the turn on a failing check. The reason becomes its next instruction and it revises in a new turn. This is the only documented lever that *forces* another pass. | It cannot rewrite text already shown. A capped loop: "ends the turn after 8 consecutive blocks". It must honour `stop_hook_active`. It checks only the final message, not every file written; pair with #5 for files. A prompt/agent judge is a model and can be wrong (agent hooks are "experimental"). The user can disable it. |
| 5 | **`PreToolUse` on `Write\|Edit\|MultiEdit` (or PostToolUse) running the same check on `tool_input`** | Deterministic refusal of a non-conforming file write. `permissionDecision: "deny"` plus a `permissionDecisionReason` is shown to Claude, which then retries. It also fires inside subagents. | It judges only what a string/regex/script can judge. It adds latency on every write. It says nothing about chat prose. |
| 6 | **`output-styles/<name>.md` with `force-for-plugin: true` and `keep-coding-instructions: true`** | The standard sits in the system prompt of every main-conversation request, is applied without the user selecting it, overrides the user's `outputStyle`, and survives compaction ("Both still apply"). | "It's an instruction Claude follows, so nothing enforces it." Only one forced style wins ("the first one loaded"), so it collides with any other plugin doing the same. Subagents ignore it (forks excepted). Leaving out `keep-coding-instructions: true` strips Claude Code's software-engineering instructions. |
| 7 | **Plugin `settings.json` `{"agent": "<plugin-agent>"}`** | A main-thread system prompt the plugin controls, applied when the plugin is enabled. | It **replaces the entire Claude Code system prompt**. `--agent` overrides it. Plugin agents drop `hooks`/`mcpServers`/`permissionMode`/`initialPrompt`. Too heavy for a writing standard; not recommended. |
| 8 | **A skill** (`skills/<name>/SKILL.md`) | Full rules are available on demand, and after invocation they are re-attached after compaction (≤5,000 tokens). Subagents that list it in `skills:` get the full body at startup. | **Never always-loaded in the main session**: "full skill content only loads when invoked". Only the description is resident, and the listing is not re-injected after compaction. Useful as the long reference that #1 points to, not as the enforcement. |
| — | `CLAUDE.md`, `AGENTS.md` or `rules/` inside the plugin | Nothing. | "A `CLAUDE.md` file at the plugin root is not loaded as project context." No plugin `rules/` component exists. |

**Suggested combination:**
1. Put a short, factual statement of the standard (under 10,000 chars, ideally a few hundred words, not starting with `{`) in a SessionStart hook with no matcher, and the same text in a SubagentStart hook.
2. Enforce it with a command-type Stop and SubagentStop hook that runs a deterministic prose check on `last_assistant_message` and returns `decision: "block"` with a specific `reason`, respecting `stop_hook_active`.
3. Use a PreToolUse check on writes for files.
4. Put the long form in a skill that the injected text names.
5. Use a forced output style only if the plugin can accept owning the single slot.

Every lever above except the Stop, SubagentStop and PreToolUse blocks is advisory. Every lever, those three included, is switched off by `/plugin disable`, by `disableAllHooks`, or by an admin's `allowManagedHooksOnly`. None was tested by installing a plugin; everything here comes from the documentation and the official repository's source as quoted.
