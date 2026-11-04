# toc-thinking

<!-- description:start -->

Applies Goldratt's Thinking Processes to software: finds the core problem behind many symptoms, resolves the conflict that sustains it, and plans the change.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/pegboard
/plugin install toc-thinking@pegboard
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>. CI installs it on Ubuntu, macOS and Windows.

### Codex

```
codex plugin marketplace add Akurganow/pegboard --ref main
codex plugin add toc-thinking@pegboard
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`. CI installs it on Ubuntu, macOS and Windows.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/pegboard
omp plugin install toc-thinking@pegboard
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md). CI installs it on Ubuntu, macOS and Windows.

### Hermes

```
hermes plugins install Akurganow/pegboard/plugins/toc-thinking --no-enable
hermes plugins list
hermes plugins enable toc-thinking
```

Keep the `plugins/toc-thinking` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it. CI installs it on Ubuntu and macOS.

### Cursor

Cursor's documentation names no command that installs from a repository. It names three routes:

- Public marketplace: open **Customize**, find the plugin, select **Install**. A plugin appears there only after Cursor reviews a submitted repository, and this repository claims no listing.
- Team marketplace, on Teams and Enterprise plans: in **Dashboard**, **Plugins & MCPs**, **Team Marketplaces**, select **Add Marketplace**, then **Import from Repo**, and paste `https://github.com/Akurganow/pegboard`. Developers then install from **Customize**.
- Local: copy `bundles/toc-thinking` to `~/.cursor/plugins/local/toc-thinking`, then restart Cursor or run **Developer: Reload Window**.

Source: Cursor documentation, [Plugins](https://cursor.com/docs/plugins), read 2026-11-04, for the three routes; [Plugins reference](https://cursor.com/docs/reference/plugins), read 2026-11-04, for the submission and review. CI does not install it.

### OpenClaw

```
openclaw plugins install toc-thinking --marketplace Akurganow/pegboard
```

Source: OpenClaw documentation, [`docs/cli/plugins/install.md`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L277-L283). OpenClaw reads this repository's `.claude-plugin/marketplace.json` (OpenClaw source, [`marketplace.ts`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38)). CI does not install it.

### Kiro

No install command is given. Kiro's documentation says Powers follow the Agent Plugins specification, and `plugins/toc-thinking/plugin.json` carries every field the documentation requires. The documentation does not say how Kiro finds several packages in one repository. CI does not install it.

Source: Kiro documentation, [Create a power](https://kiro.dev/docs/powers/create) and [Installation](https://kiro.dev/docs/powers/installation), read 2026-11-04.

### If you added the marketplace as `ai-plugins`

This marketplace was named `ai-plugins` before it was named `pegboard`. An install from that time keeps the old name. Remove every plugin you installed from it and the old marketplace, then install each plugin again with the commands above.

- Claude Code: `claude plugin list` shows the plugins you installed from `ai-plugins`; note them first. `claude plugin marketplace remove ai-plugins` removes the marketplace and uninstalls all of them. Source: Claude Code documentation, [Plugin marketplaces](https://code.claude.com/docs/en/plugin-marketplaces), "Remove the marketplace to start over", for `marketplace remove`; `claude plugin --help` in Claude Code 2.1.318 for `list`.
- Codex: for each plugin you installed from it, run `codex plugin remove <plugin>@ai-plugins`, then run `codex plugin marketplace remove ai-plugins`. Source: Codex documentation, [Build plugins](https://developers.openai.com/plugins/build/plugins), for `marketplace remove`; Codex source, [`plugin_cmd.rs` L61–L112](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs#L61-L112), for `plugin remove`.
- Oh-My-Pi: `omp plugin list` shows each installed plugin and its scope. For each plugin from `ai-plugins` and each scope it is installed in, run `omp plugin uninstall --scope <user|project> <plugin>@ai-plugins`, then run `omp plugin marketplace remove ai-plugins`. Removing a marketplace alone leaves its plugins installed. Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L64-L73), for the commands, [L222](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L222) for `--scope` when a plugin is in both scopes, and [L226](https://github.com/can1357/oh-my-pi/blob/7ceb80109236dbe6bbc90e303a14fd7748cc472d/docs/marketplace.md#L226) for what removal leaves; `omp plugin --help` in Oh-My-Pi 18.16.0 for `list`.

<!-- install:end -->

## Usage

List what you observe:

```text
Deploys fail about once a week, the nightly build is flaky, and on-call
pages keep coming back after every fix. Find the core problem.
```

The `root-cause` skill states each symptom as an undesirable effect. It
builds a Current Reality Tree down to the root causes, and checks every
link with the Categories of Legitimate Reservation. It asks you to confirm
the core problem before going on. It then builds the Evaporating Cloud for
the conflict that keeps the problem in place. A Future Reality Tree checks
the injection for new undesirable effects. The skill plans the change with
a Prerequisite Tree and a Transition Tree.

## What's inside

| Path | What it is |
| :-- | :-- |
| [`skills/root-cause/SKILL.md`](skills/root-cause/SKILL.md) | the procedure: classify, Current Reality Tree, Evaporating Cloud, Future Reality Tree, Prerequisite Tree, Transition Tree |
| [`skills/root-cause/references/tools.md`](skills/root-cause/references/tools.md) | the structure of each tree and of the cloud, with its logic |
| [`skills/root-cause/references/clr.md`](skills/root-cause/references/clr.md) | the eight Categories of Legitimate Reservation, each with a software example |
| [`skills/root-cause/references/sources.md`](skills/root-cause/references/sources.md) | the books and dictionary entries the references rest on, and what stays unread |
| [`plugin.json`](plugin.json) | the Agent Plugins 1.0.0 manifest |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | a byte-identical copy of `plugin.json` at the one manifest path Claude Code documents ([documentation](https://code.claude.com/docs/en/plugins-reference), "Plugin manifest schema") |
| [`LICENSE`](LICENSE) | the MIT license |

The package has no script, hook, rule file or network access.

The references rest on the TOCICO Dictionary and on Dettmer's *The
Logical Thinking Process*. `sources.md` names the public copy of each by
commit. The Categories of Legitimate Reservation are Dettmer's eight, and
`clr.md` notes TOCICO's count of seven.

## Boundaries

- The procedure works on facts you can observe. It asks you for a fact
  it lacks rather than guessing the system's structure. It does not
  replace a profiler, a debugger or a test.
- The skill attributes nothing to Goldratt or Dettmer without a chapter or
  a dictionary entry that `sources.md` names.
- A cloud that reduces to a trade-off between two measurable parameters
  belongs to the `contradiction` skill of [`triz-thinking`](https://github.com/Akurganow/pegboard/tree/main/plugins/triz-thinking).
  `root-cause` hands over only when `contradiction` is installed.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/pegboard/blob/main/SUPPORT.md).
