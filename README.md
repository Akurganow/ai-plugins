# ai-plugins

Agent plugins for Claude Code, Codex, Cursor, Oh-My-Pi, Hermes, OpenClaw and
Kiro. Each plugin has one hand-written source and two builds. The bundle in
`bundles/<name>` carries a manifest folder per client. The
[Agent Plugins 1.0.0](https://agent-plugins.org/specification) package in
`plugins/<name>` serves the clients that document that format. A plugin's
skills follow the [Agent Skills specification](https://agentskills.io/specification).

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
from [Plugins](#plugins). Each client reads its own catalogue in this
repository, and each section names its source. A section says whether CI
installs the plugins into that client.

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install <name>@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>. CI installs it on Ubuntu, macOS and Windows.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add <name>@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`. CI installs it on Ubuntu, macOS and Windows.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install <name>@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md). CI installs it on Ubuntu, macOS and Windows.

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/<name> --no-enable
hermes plugins list
hermes plugins enable <name>
```

Keep the `plugins/<name>` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it. CI installs it on Ubuntu and macOS.

### Cursor

Cursor's documentation names no command that installs from a repository. It names three routes:

- Public marketplace: open **Customize**, find the plugin, select **Install**. A plugin appears there only after Cursor reviews a submitted repository, and this repository claims no listing.
- Team marketplace, on Teams and Enterprise plans: in **Dashboard**, **Plugins & MCPs**, **Team Marketplaces**, select **Add Marketplace**, then **Import from Repo**, and paste `https://github.com/Akurganow/ai-plugins`. Developers then install from **Customize**.
- Local: copy `bundles/<name>` to `~/.cursor/plugins/local/<name>`, then restart Cursor or run **Developer: Reload Window**.

Source: Cursor documentation, [Plugins](https://cursor.com/docs/plugins), read 2026-11-04, for the three routes; [Plugins reference](https://cursor.com/docs/reference/plugins), read 2026-11-04, for the submission and review. CI does not install it.

### OpenClaw

```
openclaw plugins install <name> --marketplace Akurganow/ai-plugins
```

Source: OpenClaw documentation, [`docs/cli/plugins/install.md`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L277-L283). OpenClaw reads this repository's `.claude-plugin/marketplace.json` (OpenClaw source, [`marketplace.ts`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38)). CI does not install it.

### Kiro

No install command is given. Kiro's documentation says Powers follow the Agent Plugins specification, and `plugins/<name>/plugin.json` carries every field the documentation requires. The documentation does not say how Kiro finds several packages in one repository. CI does not install it.

Source: Kiro documentation, [Create a power](https://kiro.dev/docs/powers/create) and [Installation](https://kiro.dev/docs/powers/installation), read 2026-11-04.

<!-- install:end -->

What differs between clients:

- **Claude Code**: the desktop app installs from configured marketplaces,
  through the **+** button, then **Plugins**, then **Add plugin**. Source:
  [Desktop](https://code.claude.com/docs/en/desktop), documentation, read
  2026-09-25.
- **Codex**: start a new session after you install a plugin, before you use
  its skills. Source: [Plugins](https://learn.chatgpt.com/docs/plugins),
  documentation, read 2026-09-25.
- **Codex and `prose-discipline`**: Codex asks you to approve the plugin's
  hook again after each release. It records approval against a hash of the
  whole installed plugin, and every release changes `version` in the manifests.
  Source: [`plugin_trust.rs`](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/plugin_trust.rs#L29-L69)
  and [`plugin_fingerprint.rs`](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/hooks/src/engine/plugin_fingerprint.rs#L13-L91),
  source code at `rust-v0.166.0`. The documentation says the same of a changed
  bundled script: [Hooks](https://learn.chatgpt.com/docs/hooks#plugin-bundled-hooks),
  read 2026-11-04.
- **Oh-My-Pi**: `omp --plugin-dir bundles/<name>` loads a plugin from a local
  clone. Source: [`docs/cli-reference.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/cli-reference.md),
  documentation.
- **Hermes**: installed with `--no-enable`, a package stays disabled until
  `hermes plugins enable <name>` runs. Source:
  [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md)
  and [`user-guide/features/plugins.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md),
  documentation.
- **OpenClaw**: it reads `.claude-plugin/marketplace.json`, which points at the
  bundle. With several manifests in one bundle, it picks the Codex manifest
  first. Source: [`marketplace.ts` L35–L38](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38)
  and [`bundle-manifest.ts` L388–L397](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L388-L397),
  source code at `db6ac58`.
- **OpenClaw and `prose-discipline`**: the plugin gets its skills only.
  OpenClaw detects `hooks/hooks.json` and does not run it
  ([`docs/plugins/bundles.md` L197–L201](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/plugins/bundles.md#L197-L201),
  documentation). It reads a Codex manifest's `hooks` value as a list of hook
  directories, so the file `hooks/codex.json` loads nothing
  ([`discovery.ts` L178–L180](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/hooks/discovery.ts#L178-L180),
  source code). No bundle format reads a plugin-root `rules/`
  ([`bundle-manifest.ts` L170–L175](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L170-L175),
  source code, which looks only at `.cursor/rules`).

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
| [prose-discipline](plugins/prose-discipline/README.md) | An engineering prose standard for agent-written text: short active sentences, plain words, comments that explain why, and labelled review comments. |
| [toc-thinking](plugins/toc-thinking/README.md) | Applies Goldratt's Thinking Processes to software: finds the core problem behind many symptoms, resolves the conflict that sustains it, and plans the change. |
| [triz](plugins/triz/README.md) | Resolves software trade-offs with TRIZ: the contradiction matrix and 40 inventive principles, the separation principles, and ARIZ-85C walked part by part with the user. |

<!-- plugins:end -->

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

## Layout

```
src/<name>/                       the hand-written source; no client reads it
  source.json                     name, version, description and the other metadata
  README.md                       what the plugin does and how to use it
  CHANGELOG.md                    written by the release
  skills/<skill>/SKILL.md         a skill, Agent Skills format
  skills/<skill>/references/      files the skill reads when a step needs them
src/prose-discipline/rules/       the full rules, with the marked short form the hooks print
bundles/<name>/                   generated; one tree with a manifest folder per client
  .claude-plugin/plugin.json      Claude Code, and OpenClaw when no Codex manifest exists
  .codex-plugin/plugin.json       Codex, and OpenClaw
  .cursor-plugin/plugin.json      Cursor
  hooks/, rules/                  prose-discipline only: two hooks files and the .mdc rule
plugins/<name>/                   generated; the Agent Plugins 1.0.0 package
  plugin.json                     manifest with the canonical $schema
  README.md, LICENSE, skills/     copies of the source and the root LICENSE
.claude-plugin/marketplace.json   generated catalogue, read by Claude Code and OpenClaw
.agents/plugins/marketplace.json  generated catalogue, read by Codex
.omp-plugin/marketplace.json      generated catalogue, read by Oh-My-Pi
.cursor-plugin/marketplace.json   generated catalogue, read by Cursor
tools/build.sh                    writes bundles/, plugins/ and the catalogues from src/
tools/regenerate.sh               fills the README regions, then runs the builder
tools/regions.sh                  region helpers both scripts source
tools/check-conformance.py        the conformance check
tools/evals.py                    the post-release evals runner, with selftest and validate
tools/evals-fixtures/             event streams recorded from the clients, for the selftest
tools/templates/                  sources of generated text
tools/source.schema.json          schema of source.json
tools/schemas/                    vendored Agent Plugins manifest schema
tools/package.json                pins doctoc for tools/regenerate.sh
tools/package-lock.json           pins doctoc's dependency tree
docs/clients.md                   how each client loads a package, with sources
docs/design.md                    why the repository is built this way
evals/<name>/<skill>/             prompts and Jev questions for one skill's evals
cog.toml                          release configuration, one entry per package
.github/                          CI workflows and issue forms
```

Edit `src/` only. [CONTRIBUTING.md](CONTRIBUTING.md#run-the-checks) says how
the builds follow.

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

[MIT](LICENSE), © Alexander Kurganov. Each build of a plugin carries a copy
of the license.

## What conformance buys

Agent Plugins 1.0.0 describes a plugin as a directory with a single root
(§4.1). A conforming client can at least load a plugin from a directory path
(§11.1). Every `plugins/<name>/` keeps its manifest at the root with the
canonical `$schema` (§5.1, §5.2). Its skills sit in the fixed `skills/`
location (§6.1). Source: [Agent Plugins 1.0.0](https://agent-plugins.org/specification),
the specification.

`bundles/<name>/` is not an Agent Plugins package. It has no root
`plugin.json`, because Codex loads no hooks from a package that has one
([docs/design.md](docs/design.md#two-builds-from-one-source)).

The specification defines no repository-level catalogue. How a client gets
from this repository to a plugin root is specific to that client. So each
install command above cites that client's own source.

## Client notes

What each client reads from a package, with sources, is in
[docs/clients.md](docs/clients.md). The reasons behind the repository's design
are in [docs/design.md](docs/design.md).

Each note names its source and says whether it is documentation or source
code. A link into a repository points at the commit at which the note holds.

### Claude Code

- The desktop app accepts marketplace and plugin names of at most 128
  characters from letters, digits, `.`, `_` and `-`. A name starts with a
  letter or digit. Every name here meets that rule. Source:
  [Troubleshoot plugins](https://code.claude.com/docs/en/plugins/troubleshooting),
  documentation, read 2026-09-25.
- A change here reaches Claude Code users only after the plugin's next
  release. It arrives through background auto-update once a user or an admin
  turns that on. Otherwise it arrives when the user updates the plugin.
  Source: [Host and maintain a marketplace](https://code.claude.com/docs/en/plugins/host-marketplace),
  documentation, read 2026-09-25.
- The catalogue is `.claude-plugin/marketplace.json`, and each entry's
  `source` is `./bundles/<name>`. A relative `source` must start with `./`.
  Source: [Marketplace reference](https://code.claude.com/docs/en/plugins/marketplace-reference),
  documentation, read 2026-11-04.

### Codex

- The Codex CLI looks for a catalogue at `.agents/plugins/marketplace.json`
  first, and then at `.claude-plugin/marketplace.json` and
  `.cursor-plugin/marketplace.json`. Source:
  [`marketplace.rs` L21–L24](https://github.com/openai/codex/blob/6ff1e1ca3b30fc8b914720681fcf5fe62e95f856/codex-rs/core-plugins/src/marketplace.rs#L21-L24),
  source code at `rust-v0.166.0`. This repository ships the first, so nothing
  rests on the fallbacks.
- Codex documents that each catalogue entry carries `policy.installation`,
  `policy.authentication` and `category`, and every entry here does. Source:
  [Build plugins](https://developers.openai.com/plugins/build/plugins),
  documentation, read 2026-11-04.
- The ChatGPT desktop app can read `.claude-plugin/marketplace.json` as a
  legacy-compatible marketplace. Source:
  [Build plugins](https://developers.openai.com/plugins/build/plugins),
  documentation, read 2026-09-25.
- Codex identifies the marketplace by the catalogue's top-level `name`, `ai-plugins`.
  Source: [Build plugins](https://developers.openai.com/plugins/build/plugins),
  documentation, read 2026-09-25.
- `codex plugin marketplace add` takes no name argument. Source:
  `AddMarketplaceArgs` in
  [`marketplace_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/marketplace_cmd.rs#L63-L83),
  source code. Codex reads the name from the catalogue. Source:
  `validate_marketplace_root` in
  [`marketplace.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/core-plugins/src/marketplace.rs#L312-L321),
  source code.

### Oh-My-Pi

- Oh-My-Pi prefers `.omp-plugin/marketplace.json`, which this repository
  ships, and falls back to `.claude-plugin/marketplace.json`. Source:
  [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md),
  documentation.
- A plugin identifier is `name@marketplace-name`, and the marketplace half is
  the catalogue's `name` field. Source:
  [`docs/skills/authoring-marketplaces.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/skills/authoring-marketplaces.md),
  documentation.

### Cursor

- Cursor reads `.cursor-plugin/marketplace.json` at the root of a repository
  that holds several plugins. It merges the `.cursor-plugin/plugin.json` of
  each plugin folder into the catalogue entry. Source:
  [Plugins reference](https://cursor.com/docs/reference/plugins),
  documentation, read 2026-11-04.
- The documentation shows an entry `source` as a bare folder name. Cursor's own
  template repository writes `./plugins/<name>`, as this catalogue writes
  `./bundles/<name>`. The documentation does not say whether Cursor's parser
  accepts the `./` prefix. Source: [`cursor/plugin-template`](https://github.com/cursor/plugin-template/tree/46216072ac5750f782f95bb325b4d12b7c3ae9c9),
  source code, and the reference above, documentation.
- A rule with `alwaysApply: true` applies to all files, and Cursor's default
  discovery reads `rules/*.mdc`. That is how `prose-discipline` reaches Cursor.
  Source: [Plugins reference](https://cursor.com/docs/reference/plugins),
  documentation, read 2026-11-04.
- Default discovery also reads `hooks/hooks.json`, and the bundle holds Claude
  Code's hooks file there. The documentation does not say whether Cursor
  accepts that file's format, and nothing here ran it.

### OpenClaw

- With several manifests in one root, OpenClaw picks `.codex-plugin/plugin.json`,
  then `.cursor-plugin/plugin.json`, then `.claude-plugin/plugin.json`. Source:
  [`bundle-manifest.ts` L388–L397](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/bundle-manifest.ts#L388-L397),
  source code at `db6ac58`.
- It accepts a catalogue entry whose `source` is a relative path inside the
  cloned repository. Source: [`docs/cli/plugins/install.md` L301](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L301),
  documentation at `db6ac58`.

### Kiro

- Kiro documents the manifest fields `$schema`, `name`, `version`,
  `description`, `author` and `keywords`, and the components `skills/` and
  `mcp.json`. It mentions no hooks or rules. Source:
  [Create a power](https://kiro.dev/docs/powers/create), documentation, read
  2026-11-04.
- A repository can hold several powers, each in its own directory. The pages
  do not say how Kiro finds them or whether it reads a catalogue file. Source:
  [Create a power](https://kiro.dev/docs/powers/create) and
  [Installation](https://kiro.dev/docs/powers/installation), documentation,
  read 2026-11-04.

### Hermes

- Hermes reads no per-repository catalogue. It installs a package by
  identifier, and its community index is `NousResearch/hermes-plugin-index`.
  Source: [`user-guide/features/plugins.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md),
  documentation.
- In the desktop app, a `hermes://plugin/install?repo=owner/repo` link
  installs a plugin after a confirmation dialog. An agent-plugin install from
  that link goes through the same install-time security scanning as
  `hermes plugins install`. Source: the "One-click install links (Desktop)"
  section of
  [`user-guide/features/plugins.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md),
  documentation.
- Hermes scans a package when it installs it. A `caution` verdict shows the
  findings and asks `Install anyway? [y/N]`. A `dangerous` verdict blocks the
  install, and `--force` does not override it. Source:
  [`user-guide/features/plugins.md` L625–L643](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md#L625-L643),
  documentation.

## The conformance check

`tools/check-conformance.py` checks the parts of Agent Plugins 1.0.0 that this
repository controls. It validates each `plugins/<name>/plugin.json` against the
vendored schema in `tools/schemas/`, and each `src/<name>/source.json` against
`tools/source.schema.json`. It also checks what a schema cannot express:

- where files sit
- where paths resolve
- what skill front matter says
- that no symlink sits under `bundles/` or `plugins/`

CI runs it on every pull request and on pushes to `main`, as
[`conformance.yml`](.github/workflows/conformance.yml) defines.
[CONTRIBUTING.md](CONTRIBUTING.md#run-the-checks) shows how to run it locally.
