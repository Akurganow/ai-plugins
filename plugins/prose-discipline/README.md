# prose-discipline

<!-- description:start -->

An engineering prose standard for agent-written text: short active sentences, plain words, comments that explain why, and labelled review comments.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install prose-discipline@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add prose-discipline@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install prose-discipline@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md).

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/prose-discipline --no-enable
hermes plugins list
hermes plugins enable prose-discipline
```

Keep the `plugins/prose-discipline` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it.

<!-- install:end -->

## Usage

The standard needs no prompt. Claude Code and Oh-My-Pi load it into every
session on their own. Codex documents that it runs the same hooks once you
trust them ([hooks](https://learn.chatgpt.com/docs/hooks#plugin-bundled-hooks),
documentation). Hermes loads it once you pin the skill, as its section below
shows.

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
| Codex | the same hooks, declared in `plugin.json` | trust the hooks |
| Oh-My-Pi | the rules file, applied to every request | nothing |
| Hermes | the skill, pinned with `skills.auto_load` | add the lines below to `config.yaml` |

### Claude Code

The `SessionStart` hook prints the core rules as plain text, and Claude Code
adds that text to the context. The hook also runs on a resume, a fork,
`/clear` and every compaction, so the rules come back after `/clear` or a
compaction removes them. The `SubagentStart` hook hands each subagent the
same text as `additionalContext`. Claude Code does not load a plugin's
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

`plugin.json` declares the hook file under `extensions["com.openai"].hooks`.
Codex documents that it loads an enabled plugin's hooks, here the same
`SessionStart` and `SubagentStart` hooks. Codex skips
a plugin's hooks until you review and trust the current hook definition.
When hooks are new or changed, Codex opens a "Hooks need review" prompt at
startup. Its options include "Review hooks" and "Trust all and continue".
It sets `CLAUDE_PLUGIN_ROOT` for compatibility, so the same command finds the
script. Codex also lists every installed skill and tells the model to use one
whose description matches the task.

Sources:

- Codex documentation,
  [plugin packaging](https://developers.openai.com/plugins/build/plugins):
  the `hooks` field under `extensions.com.openai`, loading an enabled
  plugin's hooks, and hook trust.
- Codex documentation, [hooks](https://learn.chatgpt.com/docs/hooks):
  the `SessionStart` and `SubagentStart` events, and `CLAUDE_PLUGIN_ROOT`
  for compatibility.
- Codex source,
  [`catalog_prompt.rs`](https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/catalog_prompt.rs#L3-L8):
  the skill trigger rule.
- Codex source,
  [`startup_hooks_review.rs`](https://github.com/openai/codex/blob/694d8d45bd3d440fa4f4cbf22667ac6c17a13758/codex-rs/tui/src/startup_hooks_review.rs#L228-L271):
  the startup prompt that asks you to trust new or changed hooks.

### Oh-My-Pi

Oh-My-Pi reads `rules/prose-discipline.md` from a marketplace install. The
file's `alwaysApply: true` puts its full text into the system prompt of every
request. The file names no agents, so subagents get it too.

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
- Oh-My-Pi source,
  [`agent-plugin-format.ts`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugin-format.ts#L539-L551):
  an Agent Plugins package keeps its rules.

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
| `rules/prose-discipline.md` | the core rules, the one source every client receives |
| `skills/house-style/SKILL.md` | the skill: a generated copy of the core rules, the checking procedure, and which reference to read when |
| `skills/house-style/references/` | structural rules, vocabulary, slop pruning, comment hygiene, artifact formats, and a calibration corpus |
| `hooks/hooks.json` | the `SessionStart` and `SubagentStart` hooks |
| `hooks/print-rules.sh` | prints the core rules, as plain text or, with `--json`, as a hook object |
| `plugin.json` | the Agent Plugins 1.0.0 manifest |
| `.claude-plugin/plugin.json` | a generated copy of `plugin.json`, where Claude Code reads it |
| `LICENSE` | the MIT license |

Changes to the hand-written files above must pass this standard, so the
package stays an example of what it asks for.

## Requirements and network

The hooks run `sh` and `awk` from `PATH`. On Windows, Claude Code runs
shell-form hooks in Git Bash when it is installed, and in PowerShell
otherwise. Source: Claude Code documentation,
[hooks](https://code.claude.com/docs/en/hooks), "Exec form and shell form".
If Git Bash is missing and `PATH` has no `sh`, or the script fails, the
session starts without the hook's copy of the rules. A failing script writes
one line to stderr with the cause and the fix. The skill and the rules file
still ship.

The rules file stays under 8,000 characters. That keeps the hook text under
Claude Code's 10,000-character cap and Codex's default 2,500-token threshold
for hook context ([Claude Code hooks](https://code.claude.com/docs/en/hooks),
[Codex hooks](https://learn.chatgpt.com/docs/hooks), both documentation).

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

See [SUPPORT.md](https://github.com/Akurganow/ai-plugins/blob/main/SUPPORT.md).
