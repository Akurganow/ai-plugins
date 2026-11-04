# prose-discipline

<!-- description:start -->

An engineering prose standard for agent-written text: short active sentences, plain words, comments that explain why, and labelled review comments.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/pegboard
/plugin install prose-discipline@pegboard
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>. CI installs it on Ubuntu, macOS and Windows.

### Codex

```
codex plugin marketplace add Akurganow/pegboard --ref main
codex plugin add prose-discipline@pegboard
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`. CI installs it on Ubuntu, macOS and Windows.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/pegboard
omp plugin install prose-discipline@pegboard
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md). CI installs it on Ubuntu, macOS and Windows.

### Hermes

```
hermes plugins install Akurganow/pegboard/plugins/prose-discipline --no-enable
hermes plugins list
hermes plugins enable prose-discipline
```

Keep the `plugins/prose-discipline` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it. CI installs it on Ubuntu and macOS.

### Cursor

Cursor's documentation names no command that installs from a repository. It names three routes:

- Public marketplace: open **Customize**, find the plugin, select **Install**. A plugin appears there only after Cursor reviews a submitted repository, and this repository claims no listing.
- Team marketplace, on Teams and Enterprise plans: in **Dashboard**, **Plugins & MCPs**, **Team Marketplaces**, select **Add Marketplace**, then **Import from Repo**, and paste `https://github.com/Akurganow/pegboard`. Developers then install from **Customize**.
- Local: copy `bundles/prose-discipline` to `~/.cursor/plugins/local/prose-discipline`, then restart Cursor or run **Developer: Reload Window**.

Source: Cursor documentation, [Plugins](https://cursor.com/docs/plugins), read 2026-11-04, for the three routes; [Plugins reference](https://cursor.com/docs/reference/plugins), read 2026-11-04, for the submission and review. CI does not install it.

### OpenClaw

```
openclaw plugins install prose-discipline --marketplace Akurganow/pegboard
```

Source: OpenClaw documentation, [`docs/cli/plugins/install.md`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L277-L283). OpenClaw reads this repository's `.claude-plugin/marketplace.json` (OpenClaw source, [`marketplace.ts`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38)). CI does not install it.

### Kiro

No install command is given. Kiro's documentation says Powers follow the Agent Plugins specification, and `plugins/prose-discipline/plugin.json` carries every field the documentation requires. The documentation does not say how Kiro finds several packages in one repository. CI does not install it.

Source: Kiro documentation, [Create a power](https://kiro.dev/docs/powers/create) and [Installation](https://kiro.dev/docs/powers/installation), read 2026-11-04.

### If you added the marketplace as `ai-plugins`

This marketplace was named `ai-plugins` before it was named `pegboard`. An install from that time keeps the old name, so remove it and install again with the commands above.

- Claude Code: `claude plugin marketplace remove ai-plugins` removes the marketplace and uninstalls its plugins. Source: Claude Code documentation, [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), "Remove the marketplace to start over".
- Codex: run `codex plugin remove prose-discipline@ai-plugins`, then `codex plugin marketplace remove ai-plugins`. Source: Codex documentation, [Build plugins](https://developers.openai.com/plugins/build/plugins), for `marketplace remove`; Codex source, [`plugin_cmd.rs` L61–L112](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs#L61-L112), for `plugin remove`.
- Oh-My-Pi: run `omp plugin uninstall prose-discipline@ai-plugins`, then `omp plugin marketplace remove ai-plugins`. Removing a marketplace alone leaves its plugins installed. Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L64-L73), for the commands, and [L226](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L226) for what removal leaves.

<!-- install:end -->

## Usage

The standard needs no prompt. Claude Code, Cursor and Oh-My-Pi load it into
every session on their own. Codex runs its hooks once you trust them
([hooks](https://learn.chatgpt.com/docs/hooks#plugin-bundled-hooks),
documentation). Hermes loads it once you pin the skill, as its section below
shows. OpenClaw loads the skill only.

To check existing text against the standard, ask for it:

```
Check this commit message against the house style: "Updated some stuff in auth so it works better now."
```

The agent reports each finding with the rule it breaks and the smallest fix.
In an interactive session it applies the fixes after you approve them.

Each client gets the same core rules by its own documented route:

| Client | Route | What you do |
| :-- | :-- | :-- |
| Claude Code | `SessionStart` and `SubagentStart` hooks | nothing |
| Codex | the same hooks, declared in the Codex manifest, `.codex-plugin/plugin.json`, as `hooks: ./hooks/codex.json` | trust the hooks, again after each release |
| Cursor | the `.mdc` rule, with `alwaysApply: true` | nothing |
| Oh-My-Pi | the `.mdc` rule, applied to every request | nothing |
| Hermes | the skill, pinned with `skills.auto_load` | add the lines below to `config.yaml` |
| OpenClaw | the skill only | nothing |

### Claude Code

The `SessionStart` hook prints the short form of the core rules as plain text,
and Claude Code adds that text to the context. The short form ends by saying
that the full rules, with their reasons and examples, are in the `house-style`
skill. The hook also runs on a resume, a fork, `/clear` and every compaction,
so the rules come back after `/clear` or a compaction removes them. The
`SubagentStart` hook hands each subagent the same text as `additionalContext`. Claude Code does not load a plugin's
`CLAUDE.md`. Its documentation says to put instructions for the context in a
skill.

Sources, all Claude Code documentation:

- [Hooks](https://code.claude.com/docs/en/hooks), the `SessionStart` and
  `SubagentStart` sections: the `SessionStart` matchers, and plain stdout and
  `additionalContext` as context.
- [Hooks guide](https://code.claude.com/docs/en/hooks-guide), "Re-inject
  context after compaction".
- [Plugins reference](https://code.claude.com/docs/en/plugins-reference#standard-layout),
  "Standard layout": a `CLAUDE.md` at the plugin root is not loaded as
  context, and instructions for the context go in a skill.

### Codex

The Codex manifest, `.codex-plugin/plugin.json`, declares
`"hooks": "./hooks/codex.json"`. A declared `hooks` entry replaces Codex's
default `hooks/hooks.json`, so Codex never runs Claude Code's hooks file. The
file holds the `SessionStart` and `SubagentStart` hooks, each with a Windows
command. Codex skips a plugin's hooks until you review and trust the current
hook definition. When hooks are new or changed, Codex opens a "Hooks need
review" prompt at startup. Its options include "Review hooks" and "Trust all
and continue". Codex ties that trust to a hash of the whole installed plugin,
and every release changes `version` in the manifests, so it asks again after
each release. Codex also lists every installed skill and tells the model to
use one whose description matches the task.

Sources:

- Codex documentation,
  [plugin packaging](https://developers.openai.com/plugins/build/plugins):
  legacy packages declare `hooks` in `.codex-plugin/plugin.json`, loading an
  enabled plugin's hooks, and hook trust.
- Codex documentation, [hooks](https://learn.chatgpt.com/docs/hooks):
  the `SessionStart` and `SubagentStart` events, `commandWindows`, and a new
  review after a plugin update.
- Codex source,
  [`loader.rs` L1220–L1275](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/loader.rs#L1220-L1275):
  a declared `hooks` entry replaces the default `hooks/hooks.json`.
- Codex source,
  [`plugin_trust.rs`](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/plugin_trust.rs#L29-L69)
  and [`plugin_fingerprint.rs`](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/plugin_fingerprint.rs#L13-L91),
  at `rust-v0.166.0`: trust is bound to a hash of every file in the installed
  plugin.
- Codex source,
  [`catalog_prompt.rs`](https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/catalog_prompt.rs#L3-L8):
  the skill trigger rule.
- Codex source,
  [`startup_hooks_review.rs`](https://github.com/openai/codex/blob/694d8d45bd3d440fa4f4cbf22667ac6c17a13758/codex-rs/tui/src/startup_hooks_review.rs#L228-L271):
  the startup prompt that asks you to trust new or changed hooks.

### Oh-My-Pi

Oh-My-Pi reads `rules/prose-discipline.mdc` from the bundle that a
marketplace install copies. The file's `alwaysApply: true` puts its full text
into the system prompt of every request. The file names no agents, so
subagents get it too.

Sources:

- Oh-My-Pi documentation,
  [`docs/context-files.md`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/context-files.md#L74):
  marketplace plugins contribute rules.
- Oh-My-Pi documentation,
  [`docs/rulebook-matching-pipeline.md`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/rulebook-matching-pipeline.md#L248-L262):
  `alwaysApply` puts the full rule into the system prompt, and a rule with
  no `agents` applies to every agent.
- Oh-My-Pi source,
  [`claude-plugins.ts`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/claude-plugins.ts#L266-L285):
  the loader for a plugin's `rules/` directory.

### Cursor

Cursor reads the same `rules/prose-discipline.mdc` from the bundle. Its
default discovery takes every `.mdc` file in `rules/`, and a rule with
`alwaysApply: true` applies to all files. Cursor's default discovery also
parses `hooks/hooks.json`, where the bundle holds Claude Code's hooks file.
The documentation does not say whether Cursor accepts that file, and nothing
here ran it. CI does not install the plugin into Cursor.

Source: Cursor documentation,
[Plugins reference](https://cursor.com/docs/reference/plugins), component
discovery and rules, read 2026-11-04.

### OpenClaw

OpenClaw loads this plugin's skill and nothing else. It picks the Codex
manifest when a bundle holds several, detects `hooks/hooks.json` without
running it, reads a Codex manifest's `hooks` value as a list of hook
directories, so `hooks/codex.json` loads nothing, and reads no plugin-root
`rules/`. CI does not install the plugin into OpenClaw.

Sources, at OpenClaw commit `db6ac58`:

- OpenClaw source,
  [`bundle-manifest.ts` L388–L397](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L388-L397):
  the Codex manifest comes first.
- OpenClaw documentation,
  [`docs/plugins/bundles.md` L197–L201](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L197-L201):
  Claude `hooks/hooks.json` is recognised and not run.
- OpenClaw source,
  [`discovery.ts` L178–L180](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/hooks/discovery.ts#L178-L180):
  a hook root that is not a directory loads nothing.
- OpenClaw source,
  [`bundle-manifest.ts` L170–L175](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L170-L175):
  the only `rules` lookup is for `.cursor/rules`.

### Hermes

Hermes loads `plugin.json` and `skills/` from this package, and lists no
plugin skill in its system prompt. To keep the standard active, pin the
skill with `skills.auto_load` in `config.yaml`. Merge the lines into an
existing `skills:` block:

<!-- hermes-auto-load:start -->

```yaml
skills:
  auto_load:
    - agent-plugin-prose-discipline-cf518319:house-style
```

<!-- hermes-auto-load:end -->

Hermes then puts the whole skill, core rules included, into the system
prompt of every new session and marks it as active guidance. The name has
the form `agent-plugin-<slug>-<hash>:house-style`. The slug is
`plugin.json`'s `name` in lower case, with each character other than an ASCII
letter, digit, `_` or `-` turned into `-`. Hermes then strips leading and
trailing `-` and `_`. The hash is the
first eight hex digits of the SHA-256 of that `name`. Hermes builds the
namespace from that `name` for a package installed directly under the
plugins directory. Source: Hermes source,
[`hermes_cli/plugins_manifest.py` lines 60–69](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L60-L69)
and [lines 455–467](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L455-L467).

`hermes plugins install` names the package directory after the manifest
`name` and puts it directly under the plugins directory. Source: Hermes
source, [`hermes_cli/plugins_cmd.py` lines 873–876](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_cmd.py#L873-L876)
and [line 210](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_cmd.py#L210).

Sources:

- Hermes documentation,
  [`user-guide/cli.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/user-guide/cli.md#L297-L310):
  `skills.auto_load`.
- Hermes documentation,
  [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L71-L77):
  what a portable package provides, and the form of its namespace.
- Hermes documentation,
  [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/website/docs/developer-guide/plugins/index.md#L845):
  plugin skills are not in the system prompt's skills index.
- Hermes source,
  [`agent/skill_commands.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L165-L192) and
  [`tools/skills_tool.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/tools/skills_tool.py#L573-L590):
  `skills.auto_load` resolves a plugin skill by its qualified name.
- Hermes source,
  [`agent/skill_commands.py`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L653-L681):
  the auto-load wrapper.

## What's inside

| Path | What it is |
| :-- | :-- |
| `src/prose-discipline/rules/prose-discipline.md` | the core rules, the one source of every client's copy, with a `hook-text` region that holds the short form the hooks print |
| `src/prose-discipline/skills/house-style/SKILL.md` | the skill: a generated copy of the core rules, the checking procedure, and which reference to read when |
| `src/prose-discipline/skills/house-style/references/` | structural rules, vocabulary, slop pruning, comment hygiene, artifact formats, and a calibration corpus |
| `bundles/prose-discipline/hooks/hooks.json` | Claude Code's `SessionStart` and `SubagentStart` hooks |
| `bundles/prose-discipline/hooks/codex.json` | Codex's two hooks, each with a Windows command |
| `bundles/prose-discipline/rules/prose-discipline.mdc` | the full rules without the short-form region, with `alwaysApply: true`, for Cursor and Oh-My-Pi |
| `plugins/prose-discipline/plugin.json` | the Agent Plugins 1.0.0 manifest, for Hermes and Kiro |
| `LICENSE` | the MIT license |

`bundles/` and `plugins/` are generated from `src/`. No file in the package is
a script.

Changes to the hand-written files above must pass this standard, so the
package stays an example of what it asks for.

## Requirements and network

The hooks print text with a literal `echo` or `printf`. They read no file,
name no variable and run no script, so they need no `awk` and no runtime. On
Windows, Claude Code runs shell-form hooks in Git Bash when it is installed,
and in PowerShell otherwise. Source: Claude Code documentation,
[hooks](https://code.claude.com/docs/en/hooks), "Exec form and shell form".
The `SubagentStart` command uses `printf`. Whether PowerShell has a `printf`
is untested, so without Git Bash that command may print nothing, and a
subagent then gets no rules. Codex runs `cmd.exe` on Windows, and its file
carries a `commandWindows` for it. The skill still ships.

The builder limits the short form, the text the hooks print. It must stay
under 8,000 bytes, because Codex's default 2,500-token threshold for hook
context and Claude Code's 10,000-character cap would otherwise cut it
([Codex hooks](https://learn.chatgpt.com/docs/hooks),
[Claude Code hooks](https://code.claude.com/docs/en/hooks), both
documentation). Its Windows command must stay under 8,191 characters, the
command-line limit of cmd.exe
([Microsoft](https://learn.microsoft.com/en-us/troubleshoot/windows-client/shell-experience/command-line-string-limitation),
documentation). The builder also refuses characters that `sh`, PowerShell or
cmd.exe would read as something other than text.
[About this repository's design](https://github.com/Akurganow/pegboard/blob/main/docs/design.md#no-hook-blocks-the-agent)
gives each limit and its reason.

The package makes no network requests, needs no credentials and writes no
files. It adds no MCP servers and no settings files.

## Boundaries

- It governs text mechanics, not whether a document serves its reader.
- It governs durable artifacts, not the register of a live conversation.
- It is not a code linter. Behaviour-level checks belong to a linter. For
  the design of the code itself, use `design-review` or `cognitive-load`.
- It states the standard once per context and never blocks a reply. There is
  no checker script: enforcement is model judgement over rule texts a person
  can read and argue with.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/pegboard/blob/main/SUPPORT.md).
