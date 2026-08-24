# ai-plugins

A public marketplace of agent plugins.

Every plugin under `plugins/` is a package in the
[Agent Plugins 1.0.0](https://agent-plugins.org/specification) format: a
directory with `plugin.json` at its root, and its skills under
`skills/<name>/SKILL.md` per the
[Agent Skills specification](https://agentskills.io/specification).

The repository holds text. The one program in it is
`tools/check-conformance.py`, the conformance check described at the bottom;
no compiled artefact is stored here. The `howp` plugin is a placeholder: the
binaries it describes are not released yet, and neither is the checksum table
that will accompany them.

## Compatibility

Agent Plugins 1.0.0 governs a plugin *given its root*: "A plugin is a
directory rooted at a single filesystem location" (§4.1(1)), and a conformant
client at minimum "can load a plugin from a directory path" (§11.1(1)). That
is what conformance buys here — point a client that implements the standard
at `plugins/howp` and everything it needs is there: the manifest at the
plugin root with the canonical `$schema` (§5.1, §5.2), and skills in the
fixed `skills/` location (§6.1).

What conformance does not buy is the step before that. The specification
defines no repository-level index, and nothing about how a client gets from a
repository to a plugin root. That step is client-specific, and a command that
works for one client says nothing about another. So every install path below
is stated per client with its source, or not stated at all.

The surfaces this marketplace is meant for:

- **Claude** — Claude Code, local and cloud, and the Claude desktop app.
- **Hermes** — Desktop and server. Required.
- **Codex**
- **OpenCode**
- **Any client that implements Agent Plugins Specification 1.0.0.**

Nothing below has been installed from this repository as published, because
what is published does not yet contain the package layout described here.
Every instruction is read off that client's own documentation first, and its
own source only where the documentation does not answer; each says which, and
where a statement comes from running a client's own code, it says that too.
Only Claude's documentation site is reachable from the network this was
written on, and it was read directly. Hermes' and OpenCode's are blocked, and
both publish the same pages as Markdown in their own repositories, which is
what was read instead. Codex's is blocked as well and its repository carries
no replacement — `docs/skills.md` there is a three-line stub pointing back at
the blocked page — so its claims come from its own source, install commands
included, which is where Codex keeps its command help.

## Installing

### Claude

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install howp@ai-plugins
```

Source: Claude Code's own documentation
(<https://code.claude.com/docs/en/discover-plugins>), which documents
`/plugin marketplace add owner/repo` for "a GitHub repository that contains a
`.claude-plugin/marketplace.json` file" and `/plugin install
plugin-name@marketplace-name`. Nothing in this repository differs between
local and cloud Claude; the plugin is the same package either way.

The desktop app installs from the marketplaces already configured, without a
terminal: the **+** button beside the prompt box, then **Plugins** → **Add
plugin**, which opens a browser over "available plugins from your configured
marketplaces" (<https://code.claude.com/docs/en/desktop>). The desktop app
applies name rules the CLI does not, and this repository satisfies them:
Claude Desktop's managed marketplace sync rejects a marketplace named `org`,
`org-provisioned` or `unknown` in any casing, and accepts names of up to 128
characters made of letters, digits, `.`, `_` and `-`, starting with a letter
or digit — it rejects a whole marketplace whose name fails that and silently
drops a plugin entry whose name does
(<https://code.claude.com/docs/en/plugin-marketplaces>). `ai-plugins` and
`howp` both pass.

### Hermes — Desktop and server

Hermes has no per-repository catalogue and does not read
`.claude-plugin/marketplace.json` or anything resembling it. Its catalogue is
a single central community index, `NousResearch/hermes-plugin-index`, that a
plugin joins by pull request. This repository is therefore not a marketplace
to Hermes, and a package is installed from it directly, by identifier.

What Hermes does support is the package format, in a documented section
called "Portable Agent Plugins v1 packages": root `plugin.json`, `skills/`,
`mcp.json`, symlink containment validated locally, no schema fetched while
loading, and packages disabled until explicitly enabled. Its own scope note
is worth repeating rather than upgrading — "This is an explicit supported
subset, not a claim of full Agent Plugins conformance."

```
hermes plugins install Akurganow/ai-plugins/plugins/howp --no-enable
hermes plugins list
hermes plugins enable howp
```

The trailing `plugins/howp` is load-bearing. `hermes plugins install
Akurganow/ai-plugins` copies the whole repository into
`~/.hermes/plugins/ai-plugins/`, which leaves the package at discovery depth
3 while Hermes' scan stops at depth 2, so nothing is ever discovered — and
the install still exits 0 and tells you to enable a plugin that is not there.

Sources, in the order they were consulted. Hermes' documentation site is
unreachable from the network this was written on, but the site is a build of
Markdown published in the project's own repository under `website/docs/`
(<https://github.com/NousResearch/hermes-agent/tree/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs>),
and that is where these claims come from:
`developer-guide/plugins/index.md` for the portable-package section, the
scope note and the install-list-enable sequence,
`user-guide/features/plugins.md` for the community index and the discovery
layout, `reference/cli-commands.md` for `plugins install <identifier>`.

Documentation did not answer one question, and it is the one this section
turns on: the CLI reference documents `owner/repo`, a Git URL and a bare
index name, and does not document the subdirectory form at all. That came
from the implementation — `_resolve_git_url` in
[`hermes_cli/plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py),
same repository — and was then executed:
`Akurganow/ai-plugins/plugins/howp` resolves to that repository with subdir
`plugins/howp`, while `Akurganow/ai-plugins` resolves with no subdir.

Also executed, against this working tree rather than against what is
published: Hermes' own Agent Plugins loader reads this package with zero
diagnostics — manifest valid, one skill, the vendor symlink preserved and
still contained — and a full install, list and enable through Hermes' own
installer, from a `file://` clone, produced `howp | enabled | 0.0.3` — the
manifest version as it stood at that run. Its
plugin scanner finds `howp` when it scans a directory that *holds* the
package — `plugins/`, or the repository root as `plugins/howp` — and finds
nothing when it is pointed at `plugins/howp` itself, because it iterates the
children of the directory it is given.

Desktop and server are one backend: the desktop app's install goes through
the same installer, so manifest rules, the depth cap and the enablement
default are identical, and the differences are surface-level — a pre-flight
probe over the repository, and a `hermes://plugin/install?repo=…` deep link
that takes the same identifier, subdirectory included.

The documentation does not settle that last point:
`user-guide/features/plugins.md` gives three deep-link forms, all bare
`repo=owner/repo`, describes the handler as shallow-cloning "the repo", and
carries no path segment anywhere. The source settles it. The desktop passes
the `repo` parameter through as it stands
([`apps/desktop/src/lib/deeplink-routes.ts`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/apps/desktop/src/lib/deeplink-routes.ts)),
and each half of the install then splits it the way the CLI does. The desktop
half splits it in `resolvePluginGitUrl`, which rejects an unusable identifier
with "Use a Git URL or 'owner/repo' (optionally with a subdirectory)" and
whose own test pins `owner/repo/plugins/foo` to subdirectory `plugins/foo`
([`apps/desktop/electron/desktop-plugin-install.ts`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/apps/desktop/electron/desktop-plugin-install.ts)).
The agent half — the half that installs this package — goes through the
gateway's `plugins.manage` install action
([`tui_gateway/methods_tools.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/tui_gateway/methods_tools.py)),
which calls `dashboard_install_plugin` in `hermes_cli/plugins_cmd.py`: the same
module, and the same `_resolve_git_url`, as the command above.

### Codex

Codex reads Agent Plugins manifests: its loader looks for `plugin.json` at
the plugin root and recognises
`https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` as a supported
schema identifier, falling back to `.claude-plugin/plugin.json` when there is
no root manifest. Source: Codex's own source,
`codex-rs/utils/plugins/src/plugin_namespace.rs` in
<https://github.com/openai/codex>.

It reads this repository's marketplace index too: `.claude-plugin/marketplace.json`
is one of the marketplace manifest paths Codex looks for, it needs only a
top-level `name` and `plugins`, each entry needs only `name` and `source`, and
a `source` string beginning with `./` is resolved against the marketplace root
— the directory that holds `.claude-plugin/` — which is the form used here
(`codex-rs/core-plugins/src/marketplace.rs`).

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add howp@ai-plugins
```

Source: Codex's own CLI, where its command help lives — the `after_help`
examples in `codex-rs/cli/src/marketplace_cmd.rs` give `codex plugin
marketplace add owner/repo --ref main`, and those in
`codex-rs/cli/src/plugin_cmd.rs` give `codex plugin add PLUGIN@MARKETPLACE`. The marketplace name is not chosen on the command line:
Codex takes it from the `name` field of the index it has just fetched, which
here is `ai-plugins` (`validate_marketplace_root` in
`codex-rs/core-plugins/src/marketplace.rs`, not either CLI file).

### OpenCode

OpenCode loads Agent Skills; what it calls plugins is a different,
JavaScript extension mechanism. So the skill directory is what you install,
and it goes to the vendor-neutral location rather than OpenCode's own:

```
cp -r plugins/howp/skills/howp ~/.agents/skills/howp
```

Source, for both halves of that first sentence: OpenCode's own
documentation. Its site is unreachable from the network this was written on;
the same pages are published in the project's repository, on its default
branch `dev` — there is no `main` there, so a commit permalink is what
resolves as well as what dates the claim.

The skills half is
[`packages/web/src/content/docs/skills.mdx`](https://github.com/sst/opencode/blob/03521003fafdc6d340de6a36a189e3c121b07d40/packages/web/src/content/docs/skills.mdx),
which lists six search locations, among them "Global agent-compatible:
`~/.agents/skills/<name>/SKILL.md`" and "Project agent-compatible:
`.agents/skills/<name>/SKILL.md`", beside the vendor paths
`~/.config/opencode/skills/<name>/SKILL.md` and
`.opencode/skills/<name>/SKILL.md`. The vendor-neutral pair is what this
repository points at, because a standard location is preferred to a
vendor one wherever a client offers both. Use `.agents/skills/howp` inside a
project instead of the home directory to scope the skill to that project.

The plugins half is
[`packages/web/src/content/docs/plugins.mdx`](https://github.com/sst/opencode/blob/03521003fafdc6d340de6a36a189e3c121b07d40/packages/web/src/content/docs/plugins.mdx),
same repository and revision: an OpenCode plugin is "a JavaScript/TypeScript
module that exports one or more plugin functions", loaded from
`.opencode/plugins/`, `~/.config/opencode/plugins/` or an npm package. That
page describes no manifest and mentions neither `plugin.json` nor Agent
Plugins — which is why what you install above is the skill directory and not
this package's plugin root.

### Any client implementing Agent Plugins 1.0.0

Point it at `plugins/howp`, the plugin root. Everything the standard requires
is there: the manifest at the plugin root with the canonical `$schema`, and
skills in `skills/`. Pointing a client at the repository instead is a
different operation that the standard does not describe — see
[Compatibility](#compatibility).

## Plugins

| Plugin | What it does | Status |
|---|---|---|
| `howp` | Personal probability dashboard: interests → measurable questions → prediction-market probabilities → a markdown dashboard | placeholder; the first binary release is not published yet |

## Layout

```
.claude-plugin/marketplace.json    the marketplace index: Claude's path and format,
                                   read by Codex as well; pointers only, no plugin
                                   metadata of its own
plugins/<name>/
  plugin.json                      the manifest — Agent Plugins 1.0.0, at the plugin root
  .claude-plugin/plugin.json       symlink → ../plugin.json, Claude's documented manifest
                                   path; it holds no content of its own
  skills/<name>/SKILL.md           the skill, per the Agent Skills specification
tools/check-conformance.py         the conformance check
tools/schemas/                     the official manifest schema, vendored
.github/workflows/conformance.yml  runs the check on pushes to main and on pull requests
```

Plugin versions are bumped on every change. The standard does not require a
client to care — §10.2 says only that clients "MAY use `version` to determine
whether updates are available and whether caches are stale" — but Claude Code
does: "If set (here or in `plugin.json`), the plugin is pinned to this string
and users only receive updates when it changes"
(<https://code.claude.com/docs/en/plugin-marketplaces>). So a corrected
package shipped without a bump is a correction that installed copies do not
get.

## Cloning on Windows

`plugins/howp/.claude-plugin/plugin.json` is a symlink to the manifest one
directory up, recorded in git as mode 120000. Git only materialises it as a
link where the checkout permits symlinks. With `core.symlinks=false` — git's
default on Windows — git writes a 14-byte text file containing
`../plugin.json` instead, at exactly the path Claude Code reads a manifest
from. Claude Code's documented failure for that file is `Plugin <name> has a
corrupt manifest file at .claude-plugin/plugin.json. JSON parse error: ...`,
which is worse than having no manifest at all: the same reference calls the
manifest optional and auto-discovers components when it is absent. Source:
Claude Code's plugin reference
(<https://code.claude.com/docs/en/plugins-reference>).

So clone with symlinks enabled:

```
git clone -c core.symlinks=true https://github.com/Akurganow/ai-plugins
```

or set it once with `git config --global core.symlinks true`. On Windows the
setting only takes effect where the account may create symlinks at all, which
is what Developer Mode grants. `tools/check-conformance.py` fails on such a
checkout, and names that cause in the finding rather than reporting only a
second copy of the manifest.

The plugin manifest is not the only symlink here: `.claude/rules` is a link to
`.agents/rules` and materialises as a 16-byte text file under the same
setting. The conformance check speaks only for the plugin packages, so that
one is not covered by it — the clone flag above is what covers both.

The vendor symlink is kept rather than dropped, and it is not free. It is the
only manifest location Claude Code documents, so dropping it would cost every
Claude user the plugin's version, description, author and license in order to
protect one platform's default checkout setting, and Claude Code documents
this exact arrangement as supported: a symlink whose target resolves "within
the plugin's own directory … is preserved as a relative symlink in the cache,
so it keeps resolving to the copied target at runtime". The cost is in
Hermes, which validates a package by resolving `plugin.json` inside the
directory it was handed: when its scanner descends into `plugins/howp` and
reaches `.claude-plugin/` as if that were a package root, it logs `Failed to
parse …/.claude-plugin/plugin.json: plugin.json must be a regular file within
the plugin root`. Executed, and confirmed non-fatal — that scan finds nothing
at that depth either way, and the supported install path never reaches it —
but it is a warning in a mandatory client that the arrangement causes.

## Checking conformance

```
pip install jsonschema pyyaml
python3 tools/check-conformance.py
```

It verifies the parts of Agent Plugins 1.0.0 this repository is responsible
for. The same check runs in CI on pushes to `main` and on every pull request.
