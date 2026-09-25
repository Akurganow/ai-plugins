# How the four clients load a package

This page says what each client reads from a package in this repository.
Every fact names its kind: documentation, source read at a commit, or running the client.
A documentation page with no revision is dated by the day it was read.
A running fact cites a GitHub Actions run of this repository, on hosted runners, with no client signed in.
Install commands and install-time notes are in the [README](../README.md).
The decisions built on these facts are in [decisions](decisions/).

## Claude Code

Documentation pages below were read on 2026-09-25.

### Manifest and fetch

- The documented manifest location is `.claude-plugin/plugin.json` under the plugin root.
  (documentation: [Plugin manifest reference, Manifest file](https://code.claude.com/docs/en/plugins/manifest-reference#manifest-file))
- A manifest that is not valid JSON fails with `Plugin <name> has a corrupt manifest file`.
  (documentation: [Troubleshoot plugins](https://code.claude.com/docs/en/plugins/troubleshooting#plugin-has-a-corrupt-manifest-file-or-has-an-invalid-manifest-file))
- Claude Code strips an unrecognized top-level manifest field, and the plugin loads.
  `claude plugin validate` reports the field as a warning.
  (documentation: [Plugin manifest reference, Unrecognized fields](https://code.claude.com/docs/en/plugins/manifest-reference#unrecognized-fields))
- Claude Code clones a marketplace hosted in git onto the user's machine.
  (documentation: [Host and maintain a marketplace, Keep plugin files out of Git LFS](https://code.claude.com/docs/en/plugins/host-marketplace#keep-plugin-files-out-of-git-lfs))
- A plugin starts enabled unless `defaultEnabled` is `false`.
  (documentation: [Plugin manifest reference, defaultEnabled](https://code.claude.com/docs/en/plugins/manifest-reference#defaultenabled))
- Users stay on their cached copy until the `version` string changes.
  (documentation: [Host and maintain a marketplace, Release a new version](https://code.claude.com/docs/en/plugins/host-marketplace#release-a-new-version))
- Release tags take the form `<plugin-name>--v<version>`.
  (documentation: [Plugin dependencies, Create a release tag](https://code.claude.com/docs/en/plugins/dependencies#create-a-release-tag))

### Skills

- Claude Code namespaces a plugin skill by its plugin: `skills/review/` in `my-plugin` is `/my-plugin:review`.
  The bare `/review` also works unless another command already uses that name.
  (documentation: [Skills, How a skill gets its command name](https://code.claude.com/docs/en/skills#how-a-skill-gets-its-command-name))
- Skill descriptions sit in context, and a skill's full content loads only when it is invoked.
  (documentation: [Skills, Control who invokes a skill](https://code.claude.com/docs/en/skills#control-who-invokes-a-skill))

### Always-on instructions

- A `CLAUDE.md` at the plugin root is not loaded as context.
  The page directs instructions into a skill.
  (documentation: [Plugin manifest reference, Standard layout](https://code.claude.com/docs/en/plugins/manifest-reference#standard-layout))
- The component list names no `rules/` directory.
  (documentation: [Add components to a plugin](https://code.claude.com/docs/en/plugins/components#add-each-kind-of-component))
- For `SessionStart`, Claude Code adds plain-text stdout to the context.
  Stdout that starts with `{` and ends with `}` is parsed as JSON instead.
  (documentation: [Hooks, Exit code 0](https://code.claude.com/docs/en/hooks#exit-code-0))
- `SessionStart` matchers are `startup`, `resume`, `clear`, `compact` and `fork`.
  (documentation: [Hooks, SessionStart](https://code.claude.com/docs/en/hooks#sessionstart))
- After compaction, `SessionStart` hooks matching `compact` run, and their output joins the compacted context.
  (documentation: [Context window, What survives compaction](https://code.claude.com/docs/en/context-window#what-survives-compaction))
- Plain stdout and `additionalContext` are capped at 10,000 characters.
  Longer text reaches Claude as a file path and a preview.
  (documentation: [Hooks, JSON output](https://code.claude.com/docs/en/hooks#json-output))
- `SubagentStart` adds its `additionalContext` to a subagent's context before the first prompt.
  The page documents no plain-stdout route for this event.
  (documentation: [Hooks, SubagentStart](https://code.claude.com/docs/en/hooks#subagentstart))
- A command hook without `args` runs in shell form: `sh -c` on macOS and Linux, Git Bash on Windows.
  Windows falls back to PowerShell when Git Bash is not installed.
  With `args`, it runs in exec form, without a shell.
  (documentation: [Hooks, Exec form and shell form](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form))

### Measured on hosted runners

- Claude Code 2.1.278 added this marketplace and installed every package on Ubuntu, macOS and Windows.
  It printed `Successfully added marketplace: ai-plugins` and `Successfully installed plugin: <name>@ai-plugins (scope: user)`.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613), at `7dd891d`)
- `claude plugin details <name>@ai-plugins` printed a `Skills (N)` line with the bare skill names.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613))

## Codex

Documentation pages below were read on 2026-09-25.
Source links are commit permalinks into `openai/codex`.

### Manifest and fetch

- A portable package puts `plugin.json` at the plugin root and declares the Agent Plugins schema.
  `.codex-plugin/plugin.json` remains a compatibility fallback.
  (documentation: [Package your plugin](https://developers.openai.com/plugins/build/plugins))
- The loader checks the root `plugin.json` first.
  A symlink there, or anything but a regular file, rejects the plugin.
  (source: [`plugin_namespace.rs` L43–L80](https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/utils/plugins/src/plugin_namespace.rs#L43-L80))
- A root manifest with an `https://agent-plugins.org/schemas/` `$schema` wins.
  The vendor paths `.codex-plugin/`, `.claude-plugin/` and `.cursor-plugin/` are then never read.
  (source: [`plugin_namespace.rs` L43–L80](https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/utils/plugins/src/plugin_namespace.rs#L43-L80),
  [`protocol.rs` L49–L53](https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/exec-server-protocol/src/protocol.rs#L49-L53))
- Such a package takes skills from `./skills` and MCP servers from `./mcp.json`, with no override.
  (source: [`agent_plugin_manifest.rs` L161–L182](https://github.com/openai/codex/blob/694d8d45bd3d440fa4f4cbf22667ac6c17a13758/codex-rs/core-plugins/src/agent_plugin_manifest.rs#L161-L182))
- The loader drops an unknown top-level manifest field with a warning.
  (source: [`agent_plugin_manifest.rs` L76–L81](https://github.com/openai/codex/blob/694d8d45bd3d440fa4f4cbf22667ac6c17a13758/codex-rs/core-plugins/src/agent_plugin_manifest.rs#L76-L81))
- The listing shows the category `Other` unless the marketplace entry supplies one.
  (source: [`agent_plugin_manifest.rs` L176](https://github.com/openai/codex/blob/694d8d45bd3d440fa4f4cbf22667ac6c17a13758/codex-rs/core-plugins/src/agent_plugin_manifest.rs#L176),
  [`marketplace.rs` L945](https://github.com/openai/codex/blob/edd0df9084eb8446e586305b68a4d62202278afd/codex-rs/core-plugins/src/marketplace.rs#L945))
- Adding a marketplace runs `git clone`.
  (source: [`install.rs` L7–L45](https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/core-plugins/src/marketplace_add/install.rs#L7-L45))

### Skills

- Codex starts with each skill's name and description, and loads the full `SKILL.md` when it uses the skill.
  Users run `/skills` or type `$` to mention one.
  (documentation: [Build skills](https://learn.chatgpt.com/docs/build-skills))
- The listing tells the model it "must use that skill" when a task clearly matches the description.
  (source: [`catalog_prompt.rs` L8](https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/catalog_prompt.rs#L8))
- Codex exposes a plugin skill as `<plugin>:<skill>`, with the prefix taken from the manifest `name`.
  (source: [`namespace.rs` L11–L15](https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/loader/namespace.rs#L11-L15),
  [L176–L181](https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/loader/namespace.rs#L176-L181))

### Always-on instructions

- Hook settings go under `extensions.com.openai` in the root `plugin.json`.
  An explicit `hooks` value replaces default discovery of `hooks/hooks.json`.
  (documentation: [Package your plugin](https://developers.openai.com/plugins/build/plugins))
- The documentation says Codex loads an enabled plugin's hooks alongside user, project and managed hooks.
  (documentation: [Hooks, Plugin-bundled hooks](https://learn.chatgpt.com/docs/hooks#plugin-bundled-hooks))
- Codex skips plugin hooks until the user reviews and trusts the current hook definition.
  (documentation: [Package your plugin](https://developers.openai.com/plugins/build/plugins),
  [Hooks, Plugin-bundled hooks](https://learn.chatgpt.com/docs/hooks#plugin-bundled-hooks))
- Codex sets `CLAUDE_PLUGIN_ROOT` for compatibility with existing plugin hooks.
  (documentation: [Hooks](https://learn.chatgpt.com/docs/hooks))
- The documented command-handler fields are `timeout`, `statusMessage`, `additionalContextLimit`, `commandWindows` and `async`.
  (documentation: [Hooks](https://learn.chatgpt.com/docs/hooks))
- By default, Codex saves `additionalContext` over 2,500 tokens to disk and gives the model a preview.
  (documentation: [Hooks, Large hook output](https://learn.chatgpt.com/docs/hooks#large-hook-output))
- Plain `SessionStart` stdout becomes model context, recorded as a developer-role message.
  (source: [`session_start.rs` L218–L223](https://github.com/openai/codex/blob/694d8d45bd3d440fa4f4cbf22667ac6c17a13758/codex-rs/hooks/src/events/session_start.rs#L218-L223),
  [`hook_additional_context.rs` L15–L22](https://github.com/openai/codex/blob/694d8d45bd3d440fa4f4cbf22667ac6c17a13758/codex-rs/core/src/context/hook_additional_context.rs#L15-L22))
- An unknown top-level key in `hooks.json` fails the parse.
  The parser ignores an unknown key inside a handler.
  (source: [`hook_config.rs` L11–L12](https://github.com/openai/codex/blob/c2abf869d539a6326a6e5a125dfdb8a5dc488ab4/codex-rs/config/src/hook_config.rs#L11-L12),
  [L162–L185](https://github.com/openai/codex/blob/c2abf869d539a6326a6e5a125dfdb8a5dc488ab4/codex-rs/config/src/hook_config.rs#L162-L185))
- The loader returns no hooks for a package in Agent Plugins format, against the documentation above.
  Codex 0.155.1, tagged `rust-v0.155.1`, has the same branch.
  (source: [`loader.rs` L950–L960](https://github.com/openai/codex/blob/108e6a6dbeed5485b3b732ed4a29c002780c8632/codex-rs/core-plugins/src/loader.rs#L950-L960),
  [`loader.rs` L954–L964 at `rust-v0.155.1`](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/core-plugins/src/loader.rs#L954-L964))
- [openai/codex#39895](https://github.com/openai/codex/issues/39895) and [openai/codex#47925](https://github.com/openai/codex/issues/47925) report the same.
  Both were open on 2026-09-25.
- In Codex 0.155.1, `plugin_hooks` is a removed compatibility flag for plugin-bundled hooks.
  The config parser skips a `plugin_hooks` toggle.
  (source: [`lib.rs` L238–L239](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L238-L239),
  [L567–L568](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L567-L568),
  [L607–L609](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L607-L609),
  [L1394–L1399](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L1394-L1399))

### Measured on hosted runners

- Codex 0.155.1 added this marketplace and every package on Ubuntu, macOS and Windows.
  It printed ``Added plugin `<name>` from marketplace `ai-plugins`.`` for each package.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613), at `7dd891d`)
- `codex debug prompt-input` listed each skill as `- <plugin>:<skill>: ` followed by its description.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613))
- The runs check no plugin hook, and report that check as not run.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613))

## Oh-My-Pi

Documentation is the Markdown under `docs/` in `can1357/oh-my-pi`.
Documentation and source links are permalinks at commit `ba56afb`.

### Manifest and fetch

- The `agent-plugins` provider loads skills and MCP servers from packages that declare the standard.
  (documentation: [`context-files.md` L74](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/context-files.md#L74))
- Skill front matter is closed to the six Agent Skills fields.
  Any other key skips the skill.
  (source: [`agent-plugin-format.ts` L90–L126](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugin-format.ts#L90-L126))
- For such a package, the `claude-plugins` provider stands down from skills and MCP.
  It still loads the other surfaces, rules included.
  (source: [`agent-plugin-format.ts` L546–L551](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugin-format.ts#L546-L551))
- The `claude-plugins` provider reads `.claude-plugin/plugin.json`, and treats a file that fails `JSON.parse` as absent.
  (source: [`claude-plugins.ts` L86–L96](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/claude-plugins.ts#L86-L96))
- The marketplace fetcher clones git sources with `git`.
  (source: [`fetcher.ts` L249](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/extensibility/plugins/marketplace/fetcher.ts#L249))

### Skills

- A skill keeps its bare name, with no plugin prefix.
  (source: [`claude-plugins.ts` L249–L253](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/claude-plugins.ts#L249-L253),
  [`agent-plugins.ts` L182–L183](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugins.ts#L182-L183))
- The dedup key is the skill name, and the first item with that name wins.
  (documentation: [`skills.md` L98](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/skills.md#L98))
- The dropped duplicate gets a `name collision` warning.
  (source: [`skills.ts` L253](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/extensibility/skills.ts#L253))
- Users invoke a skill with `/skill:<name>`.
  (documentation: [`skills.md` L142–L148](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/skills.md#L142-L148))

### Always-on instructions

- The `claude-plugins` provider contributes rules from marketplace plugins.
  (documentation: [`context-files.md` L74](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/context-files.md#L74))
- It reads `rules/*.md` and `rules/*.mdc` directly under the plugin root.
  (source: [`claude-plugins.ts` L266–L285](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/claude-plugins.ts#L266-L285))
- A rule with `alwaysApply: true` has its full content injected into the system prompt.
  (documentation: [`rulebook-matching-pipeline.md` L227](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/rulebook-matching-pipeline.md#L227),
  [L248–L253](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/rulebook-matching-pipeline.md#L248-L253))
- A rule with `condition`, `astCondition` or `question` is a TTSR rule, and leaves the always-apply bucket.
  (source: [`rule-buckets.ts` L68–L78](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/capability/rule-buckets.ts#L68-L78))
- A TTSR match aborts the response and retries it with the rule injected.
  (documentation: [`ttsr-injection-lifecycle.md` L106–L129](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/ttsr-injection-lifecycle.md#L106-L129))
- Rules deduplicate by name, and the first wins.
  (documentation: [`rulebook-matching-pipeline.md` L179–L185](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/rulebook-matching-pipeline.md#L179-L185))
- A rule without `agents:` applies to every agent, subagents included.
  (documentation: [`rulebook-matching-pipeline.md` L259–L262](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/rulebook-matching-pipeline.md#L259-L262))
- Plugin hooks are files under `hooks/pre/` and `hooks/post/`.
  A Claude-style `hooks/hooks.json` has no reader.
  (source: [`claude-plugins.ts` L365–L374](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/claude-plugins.ts#L365-L374))

### Measured on hosted runners

- Oh-My-Pi 18.2.8 added this marketplace and installed every package on Ubuntu, macOS and Windows.
  It printed `✔ Installed <name> from ai-plugins (<version>)` for each package.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613), at `7dd891d`)
- `omp read skill://<skill>:raw` resolved each skill by its bare name and printed `name: <skill>`.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613))

## Hermes

Documentation is the Markdown under `website/docs/` in `NousResearch/hermes-agent`.
Documentation and source links are permalinks at commit `749220e`.
Facts about Hermes 0.21.5, the version the runs install, link to its commit `f97608f`.

### Manifest and fetch

- Hermes loads a supported subset of an Agent Plugins package: root `plugin.json`, `skills/*/SKILL.md` and root `mcp.json`.
  (documentation: [`developer-guide/plugins/index.md` L45–L77](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L45-L77))
- `plugin.json` must be a regular file inside the plugin root, with the exact 1.0.0 `$schema`.
  (source: [`agent_plugins.py` L155–L162](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/agent_plugins.py#L155-L162))
- The loader reads skills and MCP servers, and nothing else: no `hooks/`, no `rules/`.
  (source: [`agent_plugins.py` L423–L435](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/agent_plugins.py#L423-L435))
- Discovery skips `.claude-plugin` and other vendor manifest directories.
  (source: [`plugins_discovery.py` L33–L34](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_discovery.py#L33-L34))
- A portable package stays disabled after install until the user enables it.
  (documentation: [`developer-guide/plugins/index.md` L70](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L70))
- On Windows, `install.ps1` clones a branch and then checks out the pinned commit.
  (source: [`install.ps1` L20–L24](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/scripts/install.ps1#L20-L24))

### Skills

- A package skill has the qualified name `agent-plugin-<slug>-<hash>:<skill>`.
  (documentation: [`developer-guide/plugins/index.md` L75–L77](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L75-L77))
- The hash is the first eight hex digits of the SHA-256 of the key.
  For a package directly under a plugins root, the key is `plugin.json`'s `name`.
  (source: [`plugins_manifest.py` L60–L69](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L60-L69),
  [L461](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L461))
- Hermes leaves plugin skills out of the system prompt's `<available_skills>` index.
  (documentation: [`developer-guide/plugins/index.md` L845](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L845))
- The agent's `skills_list` tool shows the qualified name.
  (documentation: [`developer-guide/plugins/index.md` L75](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L75))
- In Hermes 0.21.5, neither `hermes plugins show`, `hermes plugins list --json` nor `hermes skills list` prints a portable package's skill names.
  `hermes plugins show` prints name, version, description, `Status`, `Source`, `Key`, `Emits` and `Listens`.
  (source: [`plugins_cmd.py` L1814–L1836](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L1814-L1836))
- `hermes plugins list --json` carries `name`, `status`, `version`, `description`, `source` and `removed`.
  `hermes skills list` reads skill directories only.
  (source: [`plugins_cmd.py` L1672–L1703](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L1672-L1703),
  [`skills_hub.py` L782–L828](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/skills_hub.py#L782-L828))

### Always-on instructions

- `skills.auto_load` in `config.yaml` loads the listed skills in full at the start of every new session.
  `--ignore-rules` skips it.
  (documentation: [`user-guide/cli.md` L297–L310](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/user-guide/cli.md#L297-L310))
- The documentation calls each entry a skill name.
  A qualified plugin name resolves too: the lookup sends any name containing `:` to the plugin registry.
  (source: [`skill_commands.py` L165–L192](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L165-L192),
  [`skills_tool.py` L573–L590](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/tools/skills_tool.py#L573-L590))
- An auto-loaded skill sits in the stable part of the system prompt.
  (source: [`system_prompt.py` L752–L753](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/system_prompt.py#L752-L753))
- Hermes wraps it with a note to "Treat its instructions as active guidance for the duration of this session".
  (source: [`skill_commands.py` L673–L675](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L673-L675))
- A native plugin can add a system-prompt section.
  A native plugin needs `plugin.yaml` and an `__init__.py` with a `register(ctx)` function.
  (documentation: [`user-guide/features/hooks.md` L401–L443](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/user-guide/features/hooks.md#L401-L443),
  [`developer-guide/plugins/index.md` L749](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L749))

### Measured on hosted runners

- Hermes 0.21.5 installed on Ubuntu and macOS, and every package installed and enabled.
  `hermes plugins show <name>` printed `Key: <name>` and `Status: enabled` for each package.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613), at `7dd891d`)
- On Windows, the pinned checkout failed: `Your local changes to the following files would be overwritten by checkout`.
  The runs therefore install no Hermes on Windows.
  (running: [run 36183358181](https://github.com/Akurganow/ai-plugins/actions/runs/36183358181), at `0f89614`)
