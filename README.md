# pegboard

<p align="center"><img src="docs/banner.svg" alt="Five tools hanging on a pegboard: an adjustable wrench, a drafting compass, a school ruler, a backpack and a bottle" width="100%"></p>

Agent plugins that make an agent follow published methods, such as design review and root-cause analysis.

[![conformance](https://github.com/Akurganow/pegboard/actions/workflows/conformance.yml/badge.svg)](https://github.com/Akurganow/pegboard/actions/workflows/conformance.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-blue)](LICENSE)

A plugin here is a package of skills in the [Agent Skills](https://agentskills.io/specification) format that you install into an agent.
[Install](#install) covers seven clients: Claude Code, Codex, Oh-My-Pi, Hermes, Cursor, OpenClaw and Kiro.
[docs/design.md](docs/design.md) explains the two builds that serve them.

<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Plugins](#plugins)
- [Install](#install)
- [Trust](#trust)
- [Documentation](#documentation)
- [Contributing and support](#contributing-and-support)
- [License](#license)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

## Plugins

Each name links to the plugin's README.

<!-- plugins:start -->

| Plugin | What it does |
| :-- | :-- |
| [cognitive-load](plugins/cognitive-load/README.md) | Separates the cognitive load a task needs from the load a code base's structure adds, and names the change that removes the second. |
| [design-review](plugins/design-review/README.md) | Reviews a software design for complexity with the red flags and principles of Ousterhout's A Philosophy of Software Design, each finding cited by chapter. |
| [prose-discipline](plugins/prose-discipline/README.md) | An engineering prose standard for agent-written text: short active sentences, plain words, comments that explain why, and labelled review comments. |
| [toc-thinking](plugins/toc-thinking/README.md) | Applies Goldratt's Thinking Processes to software: finds the core problem behind many symptoms, resolves the conflict that sustains it, and plans the change. |
| [triz-thinking](plugins/triz-thinking/README.md) | Resolves software trade-offs with TRIZ: the contradiction matrix and 40 inventive principles, the separation principles, and ARIZ-85C walked part by part with the user. |

<!-- plugins:end -->

## Install

Read [Trust](#trust) before you install, and replace `<name>` in a command with a name from [Plugins](#plugins).

| Client | Install | What it reads |
| :-- | :-- | :-- |
| Claude Code | [steps](#claude-code) | [notes](docs/clients.md#claude-code) |
| Codex | [steps](#codex) | [notes](docs/clients.md#codex) |
| Oh-My-Pi | [steps](#oh-my-pi) | [notes](docs/clients.md#oh-my-pi) |
| Hermes | [steps](#hermes) | [notes](docs/clients.md#hermes) |
| Cursor | [steps](#cursor) | [notes](docs/clients.md#cursor) |
| OpenClaw | [steps](#openclaw) | [notes](docs/clients.md#openclaw) |
| Kiro | [steps](#kiro) | [notes](docs/clients.md#kiro) |

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/pegboard
/plugin install <name>@pegboard
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>. CI installs it on Ubuntu, macOS and Windows.

### Codex

```
codex plugin marketplace add Akurganow/pegboard --ref main
codex plugin add <name>@pegboard
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`. CI installs it on Ubuntu, macOS and Windows.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/pegboard
omp plugin install <name>@pegboard
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md). CI installs it on Ubuntu, macOS and Windows.

### Hermes

```
hermes plugins install Akurganow/pegboard/plugins/<name> --no-enable
hermes plugins list
hermes plugins enable <name>
```

Keep the `plugins/<name>` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it. CI installs it on Ubuntu and macOS.

### Cursor

Cursor's documentation names no command that installs from a repository. It names three routes:

- Public marketplace: open **Customize**, find the plugin, select **Install**. A plugin appears there only after Cursor reviews a submitted repository, and this repository claims no listing.
- Team marketplace, on Teams and Enterprise plans: in **Dashboard**, **Plugins & MCPs**, **Team Marketplaces**, select **Add Marketplace**, then **Import from Repo**, and paste `https://github.com/Akurganow/pegboard`. Developers then install from **Customize**.
- Local: copy `bundles/<name>` to `~/.cursor/plugins/local/<name>`, then restart Cursor or run **Developer: Reload Window**.

Source: Cursor documentation, [Plugins](https://cursor.com/docs/plugins), read 2026-11-04, for the three routes; [Plugins reference](https://cursor.com/docs/reference/plugins), read 2026-11-04, for the submission and review. CI does not install it.

### OpenClaw

```
openclaw plugins install <name> --marketplace Akurganow/pegboard
```

Source: OpenClaw documentation, [`docs/cli/plugins/install.md`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L277-L283). OpenClaw reads this repository's `.claude-plugin/marketplace.json` (OpenClaw source, [`marketplace.ts`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38)). CI does not install it.

### Kiro

No install command is given. Kiro's documentation says Powers follow the Agent Plugins specification, and `plugins/<name>/plugin.json` carries every field the documentation requires. The documentation does not say how Kiro finds several packages in one repository. CI does not install it.

Source: Kiro documentation, [Create a power](https://kiro.dev/docs/powers/create) and [Installation](https://kiro.dev/docs/powers/installation), read 2026-11-04.

### If you added the marketplace as `ai-plugins`

This marketplace was named `ai-plugins` before it was named `pegboard`. An install from that time keeps the old name. Remove every plugin you installed from it and the old marketplace, then install each plugin again with the commands above.

- Claude Code: `claude plugin list` shows the plugins you installed from `ai-plugins`; note them first. `claude plugin marketplace remove ai-plugins` removes the marketplace and uninstalls all of them. Source: Claude Code documentation, [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), "Remove the marketplace to start over", for `marketplace remove`; `claude plugin --help` in Claude Code 2.1.318 for `list`.
- Codex: for each plugin you installed from it, run `codex plugin remove <plugin>@ai-plugins`, then run `codex plugin marketplace remove ai-plugins`. Source: Codex documentation, [Build plugins](https://developers.openai.com/plugins/build/plugins), for `marketplace remove`; Codex source, [`plugin_cmd.rs` L61–L112](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs#L61-L112), for `plugin remove`.
- Oh-My-Pi: `omp plugin list` shows each installed plugin and its scope. For each plugin from `ai-plugins` and each scope it is installed in, run `omp plugin uninstall --scope <user|project> <plugin>@ai-plugins`, then run `omp plugin marketplace remove ai-plugins`. Removing a marketplace alone leaves its plugins installed. Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L64-L73), for the commands, [L222](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L222) for `--scope` when a plugin is in both scopes, and [L226](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L226) for what removal leaves; `omp plugin --help` in Oh-My-Pi 18.16.0 for `list`.

<!-- install:end -->

[docs/clients.md](docs/clients.md) lists the facts that differ between clients, each with its source.

## Trust

Claude Code's documentation says: "Make sure you trust a plugin before
installing, updating, or using it." It also says a plugin "can execute
arbitrary code on your machine with your user privileges". Source:
[Plugin security and trust](https://code.claude.com/docs/en/plugins/security),
Claude Code documentation, read 2026-09-25.

Read a plugin's README and files before you install it. `prose-discipline`
runs a shell command from its hooks when a session or a subagent starts, in
clients that run plugin hooks. The command is a literal `echo` or `printf` of
the rules' short form. It reads no file and runs no script, and
`bundles/prose-discipline/hooks/` holds both hooks files. The other plugins
carry instructions and reference text only.


## Documentation

- [How each client loads a package](docs/clients.md): what each client reads, with sources.
- [About this repository's design](docs/design.md): why the builds, the catalogues and the conformance check are shaped as they are.
- [CONTRIBUTING.md](CONTRIBUTING.md#run-the-checks): how to regenerate the builds and run the conformance check.
- [Agent Plugins 1.0.0](https://agent-plugins.org/specification): the specification that `plugins/<name>` follows.

## Contributing and support

Pull requests are welcome. [CONTRIBUTING.md](CONTRIBUTING.md) covers the issue forms, the commit format, the local checks and how to propose a package.
[SUPPORT.md](SUPPORT.md) says where to ask a question or report a defect.
Report a vulnerability privately, as [SECURITY.md](SECURITY.md) describes.

## License

[MIT](LICENSE), © Alexander Kurganov. Each build of a plugin carries a copy
of the license.
