# How each client loads a package

This page says what each client reads from a package in this repository.
Every fact names its kind: documentation, source read at a commit, or running the client.
A documentation page with no revision is dated by the day it was read.
A running fact names the client version and the command, or cites a GitHub Actions run of this repository on hosted runners, with no client signed in.
Install commands and install-time notes are in the [README](../README.md).
The reasons built on these facts are in [About this repository's design](design.md).

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
- The Hooks page advises writing hook context as factual statements, not imperative system instructions.
  Text framed as out-of-band system commands can trigger Claude's prompt-injection defences, and Claude then shows it to the user instead.
  (documentation: [Hooks, Add context for Claude](https://code.claude.com/docs/en/hooks#add-context-for-claude), read 2026-09-26)
- `SubagentStart` adds its `additionalContext` to a subagent's context before the first prompt.
  The page documents no plain-stdout route for this event.
  (documentation: [Hooks, SubagentStart](https://code.claude.com/docs/en/hooks#subagentstart))
- When the hook runs again for the same subagent, Claude Code injects its context only if the earlier copy is gone.
  Auto-compaction discards that copy, so the next run's context arrives again.
  (documentation: [Hooks, SubagentStart input](https://code.claude.com/docs/en/hooks#subagentstart-input), read 2026-09-26)
- A command hook without `args` runs in shell form: `sh -c` on macOS and Linux, Git Bash on Windows.
  Windows falls back to PowerShell when Git Bash is not installed.
  With `args`, it runs in exec form, without a shell.
  (documentation: [Hooks, Exec form and shell form](https://code.claude.com/docs/en/hooks#exec-form-and-shell-form))

### Catalogue and manifests

Documentation pages in this subsection were read on 2026-11-04.

- The catalogue is `.claude-plugin/marketplace.json`.
  It requires `name`, `owner` and `plugins`, and each entry requires `name` and `source`.
  A relative `source` must start with `./`.
  (documentation: [Marketplace reference, Top-level fields](https://code.claude.com/docs/en/plugins/marketplace-reference#top-level-fields),
  [Plugin sources](https://code.claude.com/docs/en/plugins/marketplace-reference#plugin-sources))
- An entry accepts `description`, `category` and `homepage`.
  When an entry and `plugin.json` both set `version`, `plugin.json` wins, and `claude plugin validate` warns if they differ.
  (documentation: [Marketplace reference, Plugin entries](https://code.claude.com/docs/en/plugins/marketplace-reference#plugin-entries))
- The Fields table of the manifest reference lists `name`, `version`, `description`, `author`, `homepage`, `repository`, `license` and `keywords`, and no `category`.
  (documentation: [Plugin manifest reference, Fields](https://code.claude.com/docs/en/plugins/manifest-reference))
- With `--strict`, a manifest that carries `category` fails with `Field 'category' belongs in the marketplace entry (marketplace.json), not plugin.json`.
  A catalogue entry that carries Codex's `policy` or `interface` warns as an unknown field.
  (running: `claude plugin validate --strict` on Claude Code 2.1.278 and 2.1.308, 2026-11-04)
- `.codex-plugin/` and `.cursor-plugin/` folders beside `.claude-plugin/` raised no warning.
  (running: `claude plugin validate --strict` on Claude Code 2.1.308, 2026-11-04)
- `icon` is the path to an image file inside the plugin, such as `./logo.png`: "Icon for the plugin's listing in Anthropic's directory. Claude Code doesn't read it".
  In a catalogue entry `claude plugin validate` reports it as an unknown field, so it is set in `plugin.json` only.
  (documentation: [Plugins reference](https://code.claude.com/docs/en/plugins-reference), read 2026-11-04)
- The default hooks file is `hooks/hooks.json` at the plugin root.
  A `hooks` manifest field names further files, and Claude Code merges them with the default.
  (documentation: [Plugin components, Hooks](https://code.claude.com/docs/en/plugins/components#hooks),
  [Plugin manifest reference, `hooks`](https://code.claude.com/docs/en/plugins/manifest-reference#hooks))

### Validator

- `claude plugin validate` documents `--strict` and `--json`.
  The CLI reference does not document `--profile`.
  (documentation: [Plugins CLI reference, plugin validate](https://code.claude.com/docs/en/plugins/cli-reference#plugin-validate), read 2026-11-04)
- `--profile directory` exits 1 when the plugin directory would refuse a submission on a check the command runs.
  Claude Code 2.1.305 is the first published version whose help lists it, and 2.1.304 lacks it.
  (running: `claude plugin validate --help` on each npm release, 2026-11-04)
- The directory profile reports findings with `code`, `severity`, `blocking` and `hold`.
  (running: `claude plugin validate --profile directory --json` on Claude Code 2.1.308, 2026-11-04)

### Windows and PowerShell

- A hook's `shell` field accepts `"bash"` or `"powershell"`.
  It defaults to `"bash"`, or to `"powershell"` on Windows when Git Bash is not installed.
  (documentation: [Hooks, Command hook fields](https://code.claude.com/docs/en/hooks#command-hook-fields), read 2026-11-04)
- Without Git Bash, a shell-form hook with no `shell` set runs in PowerShell, where it can fail.
  (documentation: [Hooks, Failed hooks on Windows without Git Bash](https://code.claude.com/docs/en/hooks#failed-hooks-on-windows-without-git-bash), read 2026-11-04)
- `prose-discipline`'s `SubagentStart` command runs `printf`.
  No source read here says whether PowerShell has a `printf`, and no check runs the command in PowerShell.
  So the command may print nothing there, and the hook then gives a subagent no rules.
  Hosted Windows runners install Git for Windows, which brings Git Bash, so CI cannot show the gap.
  (source: [`Install-Git.ps1` L27–L37](https://github.com/actions/runner-images/blob/ebade26c60adcb867918b31c8f8caa37343a3d39/images/windows/scripts/build/Install-Git.ps1#L27-L37))
  The `SessionStart` command runs `echo`, and its behaviour in PowerShell is untested too.

### Cowork

- The platform-support page lists hooks as `hooks/hooks.json`, ignored in Chat and loaded in Cowork and Claude Code.
  It names no other hooks path.
  (documentation: [Compare component support by app](https://claude.com/docs/plugins/platform-support#compare-component-support-by-app), read 2026-11-04)
- A marketplace sync in Cowork rejected a plugin whose `hooks/hooks.json` held `commandWindows`: `Unknown hook field(s) ['commandWindows']`, because hooks "must only use fields the approval UI can display".
  (issue: [DietrichGebert/ponytail#593](https://github.com/DietrichGebert/ponytail/issues/593), closed 2026-08-07)
- The documentation does not say whether Cowork loads a hooks file that a manifest declares, or reads a file such as `hooks/codex.json` that nothing declares.

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
- The documentation says Codex can load an enabled plugin's hooks alongside user, project and managed hooks.
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
  Codex 0.155.1, tagged `rust-v0.155.1`, has the same check.
  (source: [`loader.rs` L950–L960](https://github.com/openai/codex/blob/108e6a6dbeed5485b3b732ed4a29c002780c8632/codex-rs/core-plugins/src/loader.rs#L950-L960),
  [`loader.rs` L954–L964 at `rust-v0.155.1`](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/core-plugins/src/loader.rs#L954-L964))
- [openai/codex#39895](https://github.com/openai/codex/issues/39895) and [openai/codex#47925](https://github.com/openai/codex/issues/47925) report the same.
  (issues, open on 2026-09-25)
- In Codex 0.155.1, `plugin_hooks` is a removed compatibility flag for plugin-bundled hooks.
  The config parser skips a `plugin_hooks` toggle.
  (source: [`lib.rs` L238–L239](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L238-L239),
  [L567–L568](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L567-L568),
  [L607–L609](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L607-L609),
  [L1394–L1399](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/features/src/lib.rs#L1394-L1399))

### Catalogue and bundle manifest

Links in this subsection are at `rust-v0.166.0` (`6ff1e1c`), and at `rust-v0.155.1` (`be2951e`) where they say so.
Documentation pages were read on 2026-11-04.

- Codex looks for a catalogue at `.agents/plugins/marketplace.json`, then `.agents/plugins/api_marketplace.json`, `.claude-plugin/marketplace.json` and `.cursor-plugin/marketplace.json`.
  The first file found wins.
  (source: [`marketplace.rs` L21–L24](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/marketplace.rs#L21-L24), and the same list at `rust-v0.155.1`)
- Codex documents that each entry carries `policy.installation`, `policy.authentication` and `category`.
  The loader defaults them to `AVAILABLE` and `ON_INSTALL`, and accepts `NOT_AVAILABLE`, `INSTALLED_BY_DEFAULT` and `ON_USE`.
  (documentation: [Build plugins, Marketplace metadata](https://developers.openai.com/plugins/build/plugins);
  source: [`marketplace.rs` L167–L185](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/marketplace.rs#L167-L185))
- An entry's `source` is a string path or an object tagged by `source`, such as `{"source": "local", "path": "./..."}`.
  (source: [`marketplace.rs` L1044–L1049](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/marketplace.rs#L1044-L1049), and [L1020 at `rust-v0.155.1`](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/core-plugins/src/marketplace.rs#L1020))
- An unknown key in a catalogue or an entry is not rejected.
  The top level reads `name`, `plugins` and `interface.displayName`, so `owner` and `description` are ignored.
  (source: [`marketplace.rs` L997–L1024](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/marketplace.rs#L997-L1024))
- Codex tries `.codex-plugin/plugin.json`, then `.claude-plugin/plugin.json`, then `.cursor-plugin/plugin.json`.
  The first that exists decides, and a root Agent Plugins `plugin.json` outranks all three.
  (source: [`protocol.rs` L54–L58](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/exec-server-protocol/src/protocol.rs#L54-L58),
  [`plugin_namespace.rs` L43–L83](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/utils/plugins/src/plugin_namespace.rs#L43-L83))
- Codex 0.155.1 reads `.codex-plugin/plugin.json`.
  (source: [`manifest.rs` L170 at `rust-v0.155.1`](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/core-plugins/src/manifest.rs#L170))
- The manifest parser reads `name`, `version`, `description`, `keywords`, `skills`, `mcpServers`, `apps`, `hooks`, `interface` and `extensions`.
  It drops every other key without a message, `author`, `homepage`, `repository`, `license` and `category` among them.
  (source: [`manifest.rs` L50](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/manifest.rs#L50), which has no `deny_unknown_fields`)
- The submission documentation says to omit `$schema` from a standalone Codex compatibility manifest.
  (documentation: [Plugin submission](https://developers.openai.com/plugins/deploy/submission))
- `interface.composerIcon` and `interface.logo` take `./`-prefixed paths to square images of at least 48 by 48 px, PNG among the accepted formats.
  The same page lists `displayName`, `shortDescription`, `longDescription`, `developerName`, `category` and `capabilities` as required for the Codex format, with limits it calls the limits for public submission.
  (documentation: [Plugin submission, Listing metadata and Icons and screenshots](https://developers.openai.com/plugins/deploy/submission), read 2026-11-04)
- The loader reads every `interface` field as optional or defaulted, so an `interface` with only the two icon paths loads.
  (source: [`manifest.rs` L80–L117](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/manifest.rs#L80-L117), and [L76–L112 at `rust-v0.155.1`](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/core-plugins/src/manifest.rs#L76-L112))
  The bundles carry only the two paths, because this repository submits nothing to the Codex directory.

### Hook files, Windows and trust

- A manifest that is not in Agent Plugins format loads hooks from its declared `hooks` entries, and otherwise from the default `hooks/hooks.json`.
  A declared entry replaces the default.
  A package in Agent Plugins format loads none.
  (source: [`loader.rs` L984–L996](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/loader.rs#L984-L996),
  [L1220–L1275](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/loader.rs#L1220-L1275), and the same match at [L1189–L1211 at `rust-v0.155.1`](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/core-plugins/src/loader.rs#L1189-L1211))
- The documentation says legacy packages can declare `hooks` directly in `.codex-plugin/plugin.json`, and that existing `.codex-plugin/plugin.json` files remain supported as a compatibility fallback.
  (documentation: [Build plugins](https://developers.openai.com/plugins/build/plugins))
- On Windows, Codex runs the program in `COMSPEC`, or `cmd.exe`, with `/C`.
  (source: [`command_runner.rs` L450–L458](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/command_runner.rs#L450-L458),
  [L498–L503](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/command_runner.rs#L498-L503))
- `commandWindows` is the optional Windows-only override of `command`.
  (documentation: [Hooks, command handler fields](https://learn.chatgpt.com/docs/hooks))
- For `SubagentStart`, plain text on stdout is added as extra developer context for the subagent.
  (documentation: [Hooks, SubagentStart](https://learn.chatgpt.com/docs/hooks#subagentstart))
- Before a non-managed hook runs, Codex requires the user to review and trust its exact definition.
  Codex records trust against the hook's current hash, so changed hooks are skipped until trusted.
  (documentation: [Hooks, Review and trust hooks](https://learn.chatgpt.com/docs/hooks#review-and-trust-hooks))
- For a plugin, Codex also compares a SHA-256 of every file under the installed plugin root with the one recorded at approval.
  A difference fails with `plugin contents changed; hook approval required`.
  The hash skips `__pycache__`, `.venv`, `*.pyc` and `*.egg-info`, and fails on an entry that is neither a regular file nor a directory.
  (source: [`plugin_trust.rs` L29–L69](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/plugin_trust.rs#L29-L69),
  [`plugin_fingerprint.rs` L13–L91](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/plugin_fingerprint.rs#L13-L91))
- The documentation says that when a plugin update changes a bundled script, Codex requires a new review even if the hook definition stays the same.
  (documentation: [Hooks, Plugin-bundled hooks](https://learn.chatgpt.com/docs/hooks#plugin-bundled-hooks), read 2026-11-04)
- A release changes `version` in the manifests of the installed plugin, so its hash changes, and the user approves the hook again.
  (source: the two links above; the release writes `version`, see [About this repository's design](design.md#releases-come-from-cocogitto-straight-to-main))

### Measured on hosted runners

- Codex 0.155.1 added this marketplace and every package on Ubuntu, macOS and Windows.
  It printed ``Added plugin `<name>` from marketplace `ai-plugins`.`` for each package.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613), at `7dd891d`)
- `codex debug prompt-input` listed each skill as `- <plugin>:<skill>: ` followed by its description.
  (running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613))
- The run checks no plugin hook, because the loader drops such hooks, as above.
  It reports that check as not run.
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
- Providers are sorted by priority, higher first: `agent-plugins` has 75, and `claude-plugins` and `codex` have 70.
  (documentation: [`context-files.md` L80–L86](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/context-files.md#L80-L86),
  [`config-usage.md` L211–L217](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/config-usage.md#L211-L217))
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

### Catalogue

Links in this subsection are permalinks at commit `33ea58a`.

- Oh-My-Pi looks for `.omp-plugin/marketplace.json` first, then `.claude-plugin/marketplace.json`.
  (documentation: [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/33ea58aa7dfd696c1ac419ba51fb915660740ab2/docs/marketplace.md);
  source: [`fetcher.ts` L105–L220](https://github.com/can1357/oh-my-pi/blob/33ea58aa7dfd696c1ac419ba51fb915660740ab2/packages/coding-agent/src/extensibility/plugins/marketplace/fetcher.ts#L105-L220))
- A catalogue requires `name`, `owner.name` and `plugins`.
  An invalid entry is logged and skipped.
  (documentation: [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/33ea58aa7dfd696c1ac419ba51fb915660740ab2/docs/marketplace.md);
  source: [`fetcher.ts` L105–L220](https://github.com/can1357/oh-my-pi/blob/33ea58aa7dfd696c1ac419ba51fb915660740ab2/packages/coding-agent/src/extensibility/plugins/marketplace/fetcher.ts#L105-L220))
- An entry requires `name` and `source`, and a string `source` must start with `./`.
  `description`, `version`, `author`, `homepage`, `repository`, `license`, `keywords`, `category` and `tags` are optional.
  Extra fields are preserved, and nothing warns on an unknown entry key.
  (documentation: [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/33ea58aa7dfd696c1ac419ba51fb915660740ab2/docs/marketplace.md);
  source: [`fetcher.ts` L105–L220](https://github.com/can1357/oh-my-pi/blob/33ea58aa7dfd696c1ac419ba51fb915660740ab2/packages/coding-agent/src/extensibility/plugins/marketplace/fetcher.ts#L105-L220))
- `--plugin-dir <dir>` adds a local plugin directory to discovery.
  (documentation: [`docs/cli-reference.md` L137](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/cli-reference.md#L137), at `a33cc26`)

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
  (source: [`plugins_discovery.py` L33–L34](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_discovery.py#L33-L34),
  [L131–L133](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_discovery.py#L131-L133))
- `hermes plugins install` resolves the identifier to a git URL and clones that repository with depth one.
  (source: [`plugins_cmd.py` L225](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L225),
  [L707](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L707))
- An identifier of the form `owner/repo/subdir` resolves to that GitHub repository and a subdirectory.
  (source: [`plugins_cmd.py` L252–L257](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L252-L257))
- The desktop app turns a `hermes://plugin/install?repo=owner/repo` link into a `plugins.manage` install request with that identifier.
  (source: [`deeplink-routes.ts` L53–L58](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/apps/desktop/src/lib/deeplink-routes.ts#L53-L58),
  [`plugin-install-modal.tsx` L225–L232](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/apps/desktop/src/app/settings/plugin-install-modal.tsx#L225-L232),
  [`agent-plugins.ts` L293–L299](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/apps/desktop/src/store/agent-plugins.ts#L293-L299))
- The server hands that request to `dashboard_install_plugin`.
  It and `hermes plugins install` both call `_install_plugin_core`, so the link takes the same identifiers.
  (source: [`methods_tools.py` L1626–L1636](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/tui_gateway/methods_tools.py#L1626-L1636),
  [L1708–L1712](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/tui_gateway/methods_tools.py#L1708-L1712),
  [`plugins_cmd.py` L973](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L973),
  [L2095](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L2095))
- The desktop's own repository probe also reads `owner/repo` with an optional subdirectory.
  (source: [`desktop-plugin-install.ts` L94–L100](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/apps/desktop/electron/desktop-plugin-install.ts#L94-L100))
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
- A package skill gets no slash command, because Hermes builds slash commands from skill directories only.
  The agent loads a package skill with the `skill_view` tool and its qualified name.
  (documentation: [`developer-guide/plugins/index.md` L70–L78](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L70-L78);
  source: [`skill_commands.py` L391–L425](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L391-L425))
- In Hermes 0.21.5, neither `hermes plugins show`, `hermes plugins list --json` nor `hermes skills list` prints a portable package's skill names.
  `hermes plugins show` prints name, version, description, `Status`, `Source`, `Key`, `Emits` and `Listens`.
  (source: [`plugins_cmd.py` L1814–L1836](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L1814-L1836))
- `hermes plugins list --json` carries `name`, `status`, `version`, `description`, `source` and `removed`.
  `hermes skills list` reads skill directories only.
  The `skills_list` tool adds plugin skills after that scan.
  (source: [`plugins_cmd.py` L1672–L1703](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L1672-L1703),
  [`skills_hub.py` L782–L828](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/skills_hub.py#L782-L828),
  [`skills_tool.py` L184–L226](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/tools/skills_tool.py#L184-L226),
  [L234–L246](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/tools/skills_tool.py#L234-L246))

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
- `hermes plugins validate` printed `✓ security scan — safe` for every package, `howp` included.
  (running: [run 36197524862](https://github.com/Akurganow/ai-plugins/actions/runs/36197524862), job `validate-hermes`, at `a8a3c94`)
- On the windows-latest runner, the pinned checkout failed: `Your local changes to the following files would be overwritten by checkout`.
  (running: [run 36183358181](https://github.com/Akurganow/ai-plugins/actions/runs/36183358181), at `0f89614`)
- The integration matrix excludes Hermes on the windows-latest runner, so run 36189587613 has no such job.
  (source: [`integration.yml` L56–L64](https://github.com/Akurganow/ai-plugins/blob/7dd891d8fbd3eb576d96567f5266ab7b7d81db08/.github/workflows/integration.yml#L56-L64);
  running: [run 36189587613](https://github.com/Akurganow/ai-plugins/actions/runs/36189587613))

## Cursor

Documentation pages below were read on 2026-11-04.
No Cursor client ran for these facts, and CI installs nothing into Cursor.
The pages show no commit, so each link is dated by that read.

### Manifest and catalogue

- Every Cursor plugin requires `.cursor-plugin/plugin.json`.
  `name` is required, in lowercase kebab-case.
  Optional fields include `description`, `version`, `author` with `name` and `email`, `homepage`, `repository`, `license`, `keywords`, `logo`, `rules`, `skills`, `hooks` and `mcpServers`.
  (documentation: [Plugins reference, Cursor Plugin manifest](https://cursor.com/docs/reference/plugins))
- `logo` is a relative path to a logo file in the repository, shown as `assets/logo.svg`, or an absolute URL.
  (documentation: [Plugins reference, Logos](https://cursor.com/docs/reference/plugins))
- The reference documents no `category` and no `$schema` for this manifest, and no `url` in `author`.
  It does not say what Cursor does with an unknown manifest key.
  (documentation: [Plugins reference](https://cursor.com/docs/reference/plugins), by absence)
- Cursor's template validator checks the manifest `name`, that an entry name equals its manifest `name`, and that path fields are safe relative paths that exist.
  It has no check for unknown fields.
  (source: [`validate-template.mjs`](https://github.com/cursor/plugin-template/blob/46216072ac5750f782f95bb325b4d12b7c3ae9c9/scripts/validate-template.mjs) at `4621607`)
- A repository with several plugins places `.cursor-plugin/marketplace.json` at its root.
  It requires `name`, `owner` and `plugins`, and an entry requires `name` and `source`.
  (documentation: [Plugins reference, Cursor multi-plugin repositories](https://cursor.com/docs/reference/plugins))
- Cursor merges the plugin folder's `.cursor-plugin/plugin.json` into the entry, and the manifest's values take precedence.
  (documentation: [Plugins reference, Cursor multi-plugin repositories](https://cursor.com/docs/reference/plugins))
- The documentation shows `source` as a bare folder name.
  Cursor's template repository writes `./plugins/<name>`, and its guide calls `source` the path from the repository root to the plugin folder.
  The documentation does not say whether the parser accepts the `./` prefix.
  (documentation: [Plugins reference](https://cursor.com/docs/reference/plugins);
  source: [`docs/add-a-plugin.md`](https://github.com/cursor/plugin-template/blob/46216072ac5750f782f95bb325b4d12b7c3ae9c9/docs/add-a-plugin.md) at `4621607`)

### Components

- Default discovery reads `skills/`, `rules/` (`.md`, `.mdc` and `.markdown` files), `agents/`, `commands/`, `hooks/hooks.json` and `mcp.json`.
  A manifest field for a component replaces discovery of that component.
  (documentation: [Plugins reference, component discovery](https://cursor.com/docs/reference/plugins))
- A rule with `alwaysApply: true` applies to all files, and `false` makes it available on request.
  (documentation: [Plugins reference](https://cursor.com/docs/reference/plugins))
- Discovery parses `hooks/hooks.json` for hook event names.
  Claude Code's file sits at that path in the bundle.
  The documentation does not say whether Cursor accepts that file, and nothing here ran it.
  (documentation: [Plugins reference, component discovery](https://cursor.com/docs/reference/plugins))
- Cursor loads a root Agent Plugins `plugin.json` for skills and MCP servers only.
  Rules and hooks need `.cursor-plugin/plugin.json`.
  (documentation: [Plugins](https://cursor.com/docs/plugins))

### Install routes

- Public marketplace: open **Customize**, find the plugin, and select **Install** with a project or user scope.
  A plugin appears there after submission and review by the Cursor team.
  (documentation: [Plugins, Installing plugins](https://cursor.com/docs/plugins),
  [Plugins reference](https://cursor.com/docs/reference/plugins))
- Team marketplace, on Teams and Enterprise plans: **Dashboard**, **Plugins & MCPs**, **Team Marketplaces**, **Add Marketplace**, **Import from Repo**, then the repository URL.
  Import accepts GitHub, GitLab, Bitbucket and Azure DevOps URLs.
  Developers install from **Customize**.
  (documentation: [Plugins](https://cursor.com/docs/plugins))
- The page does not say which catalogue file **Import from Repo** reads.
  The reference names `.cursor-plugin/marketplace.json` for a multi-plugin repository, and no page mentions `.claude-plugin/marketplace.json`.
  (documentation: [Plugins](https://cursor.com/docs/plugins), [Plugins reference](https://cursor.com/docs/reference/plugins))
- Local: put either plugin format in `~/.cursor/plugins/local`, then restart Cursor or run **Developer: Reload Window**.
  On Enterprise, **Allow Local Plugin Imports** is off by default.
  (documentation: [Plugins, Test plugins locally](https://cursor.com/docs/plugins))
- The pages document no `cursor` command that installs a plugin.
  The CLI's API-key route for automation reads `CURSOR_API_KEY`.
  (documentation: [Plugins](https://cursor.com/docs/plugins),
  [CLI authentication, API key authentication](https://cursor.com/docs/cli/reference/authentication))

## OpenClaw

Links are permalinks at commit `db6ac58`, which is `db6ac584cf205ea9a72de7ae83a4e65199b926a4`.
No OpenClaw client ran for these facts, and CI installs nothing into OpenClaw.

- OpenClaw reads `.claude-plugin/marketplace.json`, then `marketplace.json` at the marketplace root.
  (source: [`marketplace.ts` L35–L38](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38))
- For a marketplace on GitHub or git, a plugin entry must stay inside the cloned repository, and OpenClaw accepts relative path sources.
  (documentation: [`docs/cli/plugins/install.md` L301](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L301))
- The documented install command from a GitHub repository is `openclaw plugins install <plugin-name> --marketplace <owner/repo>`.
  `openclaw plugins marketplace list <source>` lists the entries.
  (documentation: [`docs/cli/plugins/install.md` L277–L283](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L277-L283),
  [`docs/cli/plugins/marketplace.md` L36](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/marketplace.md#L36))
- Of `.codex-plugin/plugin.json`, `.cursor-plugin/plugin.json` and `.claude-plugin/plugin.json`, the first that exists sets the bundle format.
  A root `plugin.json` counts only when none of them exists.
  The documentation lists the markers in that order and says a client marker beats a root `plugin.json`, and the source fixes the order among the three.
  (source: [`bundle-manifest.ts` L388–L397](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L388-L397);
  documentation: [`docs/plugins/bundles.md` L380–L386](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L380-L386))
- `hooks/hooks.json` of a Claude bundle is "detected but not executed".
  (documentation: [`docs/plugins/bundles.md` L197–L201](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L197-L201))
- A Codex manifest's `hooks` value is read as a list of hook-root directories, each holding child directories with `HOOK.md` and a handler.
  A path that is a file, such as `./hooks/codex.json`, loads no entries, and the hooks capability is reported unavailable.
  (documentation: [`docs/plugins/bundles.md` L110–L115](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L110-L115);
  source: [`bundle-manifest.ts` L131–L142](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L131-L142),
  [`installed-plugin-components.ts` L74–L90](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/installed-plugin-components.ts#L74-L90),
  [`discovery.ts` L178–L180](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/hooks/discovery.ts#L178-L180))
- No bundle format reads a plugin-root `rules/` directory.
  A Cursor bundle's `.cursor/rules/` is detect-only.
  The documentation never mentions a root `rules/`, and the only `rules` lookup in the manifest reader is for `.cursor/rules`.
  (documentation: [`docs/plugins/bundles.md` L364–L370](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L364-L370);
  source: [`bundle-manifest.ts` L170–L175](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L170-L175))
- A bundle's skill roots load as normal OpenClaw skills, in every bundle format.
  A Codex bundle lists `skills/` as content.
  (documentation: [`docs/plugins/bundles.md` L79](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L79),
  [L331–L337](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L331-L337))
- The hooks answer comes from reading source, not from running OpenClaw.

## Kiro

Pages below are Kiro documentation, read as Markdown on 2026-11-04.
Each page shows "Page updated" and no commit.
Kiro is closed source, so no source was read, and CI installs nothing into Kiro.

- Powers follow the Agent Plugins specification.
  Kiro supports the Agent Plugins format (`plugin.json`) and the legacy `POWER.md` format.
  (documentation: [Create a power](https://kiro.dev/docs/powers/create), updated October 8, 2026;
  [Installation](https://kiro.dev/docs/powers/installation), updated October 23, 2026)
- A power requires `$schema`, `name`, `version`, `description`, `author` with at least `name`, and `keywords`.
  `plugins/<name>/plugin.json` carries all six.
  (documentation: [Create a power](https://kiro.dev/docs/powers/create))
- Kiro documents the components `skills/` and `mcp.json`, and mentions no hooks and no rules.
  (documentation: [Create a power](https://kiro.dev/docs/powers/create))
- A power can live at the root of a repository or in a folder, and one repository can hold several powers, each in its own folder.
  The pages do not say how Kiro finds the folders, how deep it looks, or whether it reads a catalogue file.
  (documentation: [Create a power](https://kiro.dev/docs/powers/create),
  [Installation](https://kiro.dev/docs/powers/installation))
- GitHub import is a flow in the Powers panel: **Add Custom Power**, **Import power from GitHub**, a repository URL, **Install**.
  The pages document no command for it.
  (documentation: [Installation](https://kiro.dev/docs/powers/installation))
- `/powers install <name|path>` and `kiro-cli powers install <name|path>` install a power from an existing directory, or else by an exact name in the powers catalog.
  (documentation: [Installation](https://kiro.dev/docs/powers/installation), CLI V3)
- This repository states no Kiro import command, because the pages leave the several-packages case open.

## Anthropic plugin directory

The pre-submission checklist was read as Markdown on 2026-11-04.
It shows no "Page updated" date.

- The portal's Validate runs every directory check.
  A finding labelled "Blocks" stops a submission until it is fixed, and one "Held for a reviewer" still lets the plugin be submitted.
  (documentation: [Pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist))
- The portal's Validate wants a square PNG or JPEG, 512 to 2048 px a side and under 2 MB, at `.claude-plugin/icon.png` or named by `icon`, and accepts no SVG or WebP.
  The file "may become the listing icon only once: the first time the plugin is saved or submitted in the developer portal".
  (running: the portal's Validate on `bundles/prose-discipline` at `4b2a8b8`, its "No icon" warning, 2026-11-04)
- With `icon` set in `.claude-plugin/plugin.json`, Validate warns "Field from another tool's manifest": "The plugin directory reads 'icon' for the listing; Claude Code itself ignores it at load time."
  So the bundles keep the file at `.claude-plugin/icon.png` and set no `icon`.
  (running: the portal's Validate on `bundles/prose-discipline` at `fd262d6`, 2026-11-04)
- The plugin folder "can be the repository root or a subfolder".
  (documentation: [Pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist))
- The rule for hook commands, unchanged: "In the command of a hook or an MCP server, write each path in full from `${CLAUDE_PLUGIN_ROOT}`, with no other variable, command substitution, wildcard, or inline program such as `python3 -c`". The result if you do not: "Blocks when the plugin folder is a subfolder of the repository".
  (documentation: [Pre-submission checklist, Review what the plugin runs and connects to](https://claude.com/docs/plugins/pre-submission-checklist))
- A companion row asks to keep launchers and package installs out of each script that a hook runs, and a hook that runs a non-shell file from the plugin is held for a reviewer.
  (documentation: [Pre-submission checklist](https://claude.com/docs/plugins/pre-submission-checklist))
- The text does not say whether a literal `echo '<text>'` or `printf '%s' '<json>'` counts as an inline program.
  It names no such command as allowed or disallowed, and the hooks here use no variable and no path.
  The validator is not published.
