### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install {{name}}@pegboard
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>. CI installs it on Ubuntu, macOS and Windows.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add {{name}}@pegboard
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`. CI installs it on Ubuntu, macOS and Windows.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install {{name}}@pegboard
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md). CI installs it on Ubuntu, macOS and Windows.

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/{{name}} --no-enable
hermes plugins list
hermes plugins enable {{name}}
```

Keep the `plugins/{{name}}` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it. CI installs it on Ubuntu and macOS.

### Cursor

Cursor's documentation names no command that installs from a repository. It names three routes:

- Public marketplace: open **Customize**, find the plugin, select **Install**. A plugin appears there only after Cursor reviews a submitted repository, and this repository claims no listing.
- Team marketplace, on Teams and Enterprise plans: in **Dashboard**, **Plugins & MCPs**, **Team Marketplaces**, select **Add Marketplace**, then **Import from Repo**, and paste `https://github.com/Akurganow/ai-plugins`. Developers then install from **Customize**.
- Local: copy `bundles/{{name}}` to `~/.cursor/plugins/local/{{name}}`, then restart Cursor or run **Developer: Reload Window**.

Source: Cursor documentation, [Plugins](https://cursor.com/docs/plugins), read 2026-11-04, for the three routes; [Plugins reference](https://cursor.com/docs/reference/plugins), read 2026-11-04, for the submission and review. CI does not install it.

### OpenClaw

```
openclaw plugins install {{name}} --marketplace Akurganow/ai-plugins
```

Source: OpenClaw documentation, [`docs/cli/plugins/install.md`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L277-L283). OpenClaw reads this repository's `.claude-plugin/marketplace.json` (OpenClaw source, [`marketplace.ts`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38)). CI does not install it.

### Kiro

No install command is given. Kiro's documentation says Powers follow the Agent Plugins specification, and `plugins/{{name}}/plugin.json` carries every field the documentation requires. The documentation does not say how Kiro finds several packages in one repository. CI does not install it.

Source: Kiro documentation, [Create a power](https://kiro.dev/docs/powers/create) and [Installation](https://kiro.dev/docs/powers/installation), read 2026-11-04.
