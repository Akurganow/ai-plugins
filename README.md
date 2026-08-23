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

- **Claude** — cloud and local.
- **Hermes** — Desktop and server. Required.
- **Codex**
- **OpenCode**
- **Any client that implements Agent Plugins Specification 1.0.0.**

No client has been installed end to end against this repository. Every
instruction below is read off that client's own documentation or its own
source, and says which; where a statement comes from running a client's own
code against this tree, it says that too.

## Installing

### Claude

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install howp@ai-plugins
```

Source: the `/plugin` command's built-in help in Claude Code
(`/plugin marketplace add <path/url>`, `/plugin install <plugin>@<market>`).
Nothing in this repository differs between local and cloud Claude; the
plugin is the same package either way.

### Hermes — Desktop and server

Hermes reads Agent Plugins 1.0.0 packages directly. In
<https://github.com/NousResearch/hermes-agent>, `hermes_cli/agent_plugins.py`
validates a portable manifest at `plugin.json` in the plugin root, requires
the canonical 1.0.0 `$schema`, and hands the package's skills to Hermes' own
skill runtime; `hermes_cli/plugins.py` scans installed plugin directories for
that manifest. Those two were executed against this tree:
`read_agent_plugin_manifest` returns the `howp` manifest with no diagnostics,
and `_scan_directory_level` reports one plugin, `howp` — when what it scans
is the package directory itself.

The install command is not stated here yet. Hermes' installer accepts an
`owner/repo` identifier with an optional trailing subdirectory, and the
identifier has to name the package, not the repository: given
`Akurganow/ai-plugins`, Hermes' own `_resolve_git_url` returns no
subdirectory (executed, same repository as above), so the clone root is
treated as the plugin, no manifest is found there, the plugin is installed
under the repository's name and Hermes logs that it "may not be a valid
plugin". Nothing named `howp` is created, and
`hermes plugins enable howp` would have nothing to enable. The identifier and
flags to write instead are being verified against Hermes' own source in a
separate pass; until that lands, no command is stated rather than guessed.

What is already sourced: portable packages install disabled and are enabled
explicitly. Hermes' own `plugins` parser says so in its description
("Portable packages install disabled"), and its `--no-enable` help points at
`hermes plugins enable <name>` (`hermes_cli/subcommands/plugins.py`).

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

Source: Codex's own CLI — `codex-rs/cli/src/marketplace_cmd.rs` documents
`codex plugin marketplace add owner/repo --ref main`, and
`codex-rs/cli/src/plugin_cmd.rs` documents `codex plugin add
PLUGIN@MARKETPLACE`. The marketplace name is not chosen on the command line:
Codex takes it from the `name` field of the index it has just fetched, which
here is `ai-plugins` (`validate_marketplace_root`, same file as above).

### OpenCode

OpenCode loads Agent Skills; what it calls plugins is a different,
JavaScript extension mechanism. So the skill directory is what you install:

```
cp -r plugins/howp/skills/howp ~/.config/opencode/skills/howp
```

Source: OpenCode's own documentation (<https://opencode.ai/docs/skills/>),
which lists `~/.config/opencode/skills/<name>/SKILL.md` as the global
location and `.opencode/skills/<name>/SKILL.md` as the project-local one.

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

Plugin versions are bumped on every change — without a `version` bump in
`plugin.json`, installed copies do not receive the update.

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

## Checking conformance

```
pip install jsonschema pyyaml
python3 tools/check-conformance.py
```

It verifies the parts of Agent Plugins 1.0.0 this repository is responsible
for. The same check runs in CI on pushes to `main` and on every pull request.
