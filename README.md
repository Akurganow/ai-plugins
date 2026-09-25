# ai-plugins

Agent plugins for Claude Code, Codex, Oh-My-Pi and Hermes. Each plugin is an
[Agent Plugins 1.0.0](https://agent-plugins.org/specification) package, and
its skills follow the [Agent Skills specification](https://agentskills.io/specification).

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Install](#install)
- [Plugins](#plugins)
- [Trust](#trust)
- [Layout](#layout)
- [Contributing](#contributing)
- [Help](#help)
- [License](#license)
- [What conformance buys](#what-conformance-buys)
- [Client notes](#client-notes)
- [The conformance check](#the-conformance-check)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Install

Read [Trust](#trust) before you install a plugin. Replace `<name>` with a name
from [Plugins](#plugins).

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install <name>@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add <name>@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install <name>@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md).

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/<name> --no-enable
hermes plugins list
hermes plugins enable <name>
```

Keep the `plugins/<name>` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it.

<!-- install:end -->

What differs between clients:

- **Claude Code**: the desktop app installs from configured marketplaces,
  through the **+** button, then **Plugins**, then **Add plugin**. Source:
  [Desktop](https://code.claude.com/docs/en/desktop), documentation.
- **Codex**: start a new session after you install a plugin, before you use
  its skills. Source: [Plugins](https://learn.chatgpt.com/docs/plugins),
  documentation.
- **Oh-My-Pi**: `omp --plugin-dir plugins/<name>` loads a plugin from a local
  clone. Source: [`docs/cli-reference.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/cli-reference.md),
  documentation.
- **Hermes**: a package stays disabled until `hermes plugins enable <name>`
  runs. Source: [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md),
  documentation.

A client that implements Agent Plugins 1.0.0 can load `plugins/<name>`
directly. [Client notes](#client-notes) and
[What conformance buys](#what-conformance-buys) go into more depth.

## Plugins

Each name links to the plugin's README.

<!-- plugins:start -->

| Plugin | What it does |
| :-- | :-- |
| [cognitive-load](plugins/cognitive-load/README.md) | Separates the cognitive load a task needs from the load a code base's structure adds, and names the change that removes the second. |
| [design-review](plugins/design-review/README.md) | Reviews a software design for complexity with the red flags and principles of Ousterhout's A Philosophy of Software Design, each finding cited by chapter. |
| [howp](plugins/howp/README.md) | Turn what you follow into measurable questions, bind them to Polymarket and Manifold markets, and write a forecast from their probabilities and the agent's judgement. |
| [prose-discipline](plugins/prose-discipline/README.md) | An engineering prose standard for agent-written text: short active sentences, plain words, comments that explain why, and labelled review comments. |
| [toc-thinking](plugins/toc-thinking/README.md) | Applies Goldratt's Thinking Processes to software: finds the core problem behind many symptoms, resolves the conflict that sustains it, and plans the change. |
| [triz](plugins/triz/README.md) | Resolves software trade-offs with TRIZ: the contradiction matrix and 40 inventive principles, the separation principles, and ARIZ-85C walked part by part with the user. |

<!-- plugins:end -->

## Trust

Claude Code's documentation says: "Make sure you trust a plugin before
installing it." It also says a plugin can run arbitrary code with your user
privileges. Source: [Discover plugins](https://code.claude.com/docs/en/discover-plugins),
Claude Code documentation.

Read a plugin's README and files before you install it. `howp` downloads a
released binary, checks its sha256 and runs it. `prose-discipline` runs a
shell script from its hooks when a session or a subagent starts, in clients
that run plugin hooks. The other plugins carry instructions and reference text
only.

## Layout

```
.claude-plugin/marketplace.json   catalogue index, generated from every plugin.json
plugins/<name>/
  plugin.json                     manifest, Agent Plugins 1.0.0
  .claude-plugin/plugin.json      generated copy of plugin.json, for Claude Code
  README.md                       what the plugin does and how to use it
  LICENSE                         generated copy of the root LICENSE
  skills/<skill>/SKILL.md         a skill, Agent Skills format
  skills/<skill>/references/      files the skill reads when a step needs them
  binaries.json                   howp only: released binaries and their sha256,
                                  written by the howp release
tools/check-conformance.py        the conformance check
tools/regenerate.sh               rewrites every generated file from its source
tools/templates/                  sources of generated text
tools/schemas/                    vendored Agent Plugins manifest schema
.github/                          CI workflows and issue forms
```

A plugin may add directories of its own, such as `hooks/` and `rules/` in
`prose-discipline`. Its README describes them.

## Contributing

Pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) covers:

- the issue forms
- the commit format
- the local checks
- how to propose a package

## Help

[SUPPORT.md](SUPPORT.md) says where to ask a question or report a defect.
Report a vulnerability privately, as [SECURITY.md](SECURITY.md) describes.

## License

[MIT](LICENSE), © Alexander Kurganov. Each plugin carries a copy of the
license.

## What conformance buys

Agent Plugins 1.0.0 describes a plugin as a directory with a single root
(§4.1). A conforming client can at least load a plugin from a directory path
(§11.1). Every plugin here keeps its manifest at the root with the canonical
`$schema` (§5.1, §5.2). Its skills sit in the fixed `skills/` location (§6.1).
Source: [Agent Plugins 1.0.0](https://agent-plugins.org/specification), the
specification.

The specification defines no repository-level catalogue. How a client gets
from this repository to a plugin root is specific to that client. So each
install command above cites that client's own source.

## Client notes

Each note names its source and says whether it is documentation or source
code. A link into a repository points at the commit the note describes.

### Claude Code

- The desktop app accepts marketplace and plugin names of letters, digits,
  `.`, `_` and `-`, up to 128 characters. Every name here meets that rule.
  Source: [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces),
  documentation.
- Claude Code pins a plugin to its `version` and delivers an update only when
  the version changes. A change reaches Claude Code users at the plugin's next
  release. Source: the same page.

### Codex

- Codex reads a root `plugin.json` that declares the Agent Plugins schema.
  Source: [Build plugins](https://developers.openai.com/plugins/build/plugins),
  documentation.
- Codex reads `.claude-plugin/marketplace.json` as a legacy-compatible
  marketplace. Source: the same page.
- Codex takes the marketplace name from the catalogue's `name` field,
  `ai-plugins`, not from the command line. Source: `validate_marketplace_root` in
  [`marketplace.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/core-plugins/src/marketplace.rs),
  source code.

### Oh-My-Pi

- Oh-My-Pi prefers `.omp-plugin/marketplace.json` and falls back to
  `.claude-plugin/marketplace.json`, the only catalogue here. Source:
  [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md),
  documentation.
- A plugin identifier is `name@marketplace-name`, and the marketplace half is
  the catalogue's `name` field. Source:
  [`docs/skills/authoring-marketplaces.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/skills/authoring-marketplaces.md),
  documentation.
- The `agent-plugins` provider reads standard packages at priority 75. The
  `claude-plugins` and `codex` providers sit at 70. Source:
  [`docs/context-files.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/context-files.md)
  and [`docs/config-usage.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/config-usage.md),
  documentation.
- For a package that declares the standard, the `claude-plugins` provider
  stands down for skills and MCP servers. Each skill therefore loads once.
  Source: `legacyProviderAllowed` in
  [`agent-plugin-format.ts`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/packages/coding-agent/src/discovery/agent-plugin-format.ts),
  source code.

### Hermes

- Hermes reads no per-repository catalogue. It installs a package by
  identifier, and its community index is `NousResearch/hermes-plugin-index`.
  Source: [`user-guide/features/plugins.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md),
  documentation.
- Hermes loads a subset of the format: root `plugin.json`, `skills/` and
  `mcp.json`. Its documentation calls this "an explicit supported subset, not a
  claim of full Agent Plugins conformance". Source:
  [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md),
  documentation.
- The desktop app and the server install through the same code. A
  `hermes://plugin/install?repo=…` deep link takes the same identifier,
  subdirectory included. Source:
  [`deeplink-routes.ts`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/apps/desktop/src/lib/deeplink-routes.ts),
  [`desktop-plugin-install.ts`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/apps/desktop/electron/desktop-plugin-install.ts)
  and [`methods_tools.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/tui_gateway/methods_tools.py),
  source code.

## The conformance check

`tools/check-conformance.py` checks the parts of Agent Plugins 1.0.0 that this
repository controls. It validates each manifest against the vendored schema in
`tools/schemas/`. It also checks what a schema cannot express:

- where files sit
- where paths resolve
- what skill front matter says

CI runs it on every pull request and on pushes to `main`, as
[`conformance.yml`](.github/workflows/conformance.yml) defines.
[CONTRIBUTING.md](CONTRIBUTING.md#run-the-checks) shows how to run it locally.
