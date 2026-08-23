# ai-plugins

A public marketplace of agent plugins.

Every plugin under `plugins/` is a package in the
[Agent Plugins 1.0.0](https://agent-plugins.org/specification) format: a
directory with `plugin.json` at its root, and its skills under
`skills/<name>/SKILL.md` per the
[Agent Skills specification](https://agentskills.io/specification).

The repository holds text only. No executables are stored in the tree. The
`howp` plugin is a placeholder: the binaries it describes are not released
yet, and neither is the checksum table that will accompany them.

## Compatibility

The standard is the mechanism. A client that implements Agent Plugins 1.0.0
installs these plugins by construction: it reads `plugin.json` at the plugin
root (§5.1), discovers skills from the fixed `skills/` location (§6.1), and
needs nothing client-specific from this repository. A client that implements
only Agent Skills can take the skill directory on its own.

The surfaces this marketplace is meant for:

- **Claude** — cloud and local.
- **Hermes** — Desktop and server. Required.
- **Codex**
- **OpenCode**
- **Any client that implements Agent Plugins Specification 1.0.0.**

None of these has been tested against this repository. Every instruction
below is read off that client's own documentation or its own source, and
says which.

## Installing

### Claude

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install howp@ai-plugins
```

Source: the `/plugin` command's built-in help in Claude Code
(`/plugin marketplace add <path/url>`, `/plugin install <plugin>@<market>`).
The commands are the same wherever Claude Code runs.

### Hermes — Desktop and server

```
hermes plugins install Akurganow/ai-plugins --no-enable
hermes plugins list
hermes plugins enable howp
```

Source: Hermes Agent's own plugin developer guide, section "Portable Agent
Plugins v1 packages"
(<https://hermes-agent.nousresearch.com/docs/developer-guide/plugins>), which
documents this install-list-enable sequence for directory packages targeting
the Agent Plugins 1.0.0 format. Portable packages stay disabled until you
enable them explicitly. In the desktop app the same agent plugins are listed
and toggled under Settings → Plugins (Hermes desktop guide).

### Codex

Codex reads Agent Plugins manifests: its loader looks for `plugin.json` at
the plugin root and recognises
`https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` as a supported
schema identifier, falling back to `.claude-plugin/plugin.json` when there is
no root manifest. Source: Codex's own source,
`codex-rs/utils/plugins/src/plugin_namespace.rs` in
<https://github.com/openai/codex>.

The install command is not documented here. Codex's skills documentation is
at <https://developers.openai.com/codex/skills>; no command was verified
against that page, so none is stated rather than guessed.

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

Point it at `plugins/howp`, or at this repository if it installs from one.
Everything the standard requires is there: the manifest at the plugin root
with the canonical `$schema`, and skills in `skills/`.

## Plugins

| Plugin | What it does | Status |
|---|---|---|
| `howp` | Personal probability dashboard: interests → measurable questions → prediction-market probabilities → a markdown dashboard | placeholder; the first binary release is not published yet |

## Layout

```
.claude-plugin/marketplace.json    Claude's marketplace index: vendor configuration,
                                   pointers only, no plugin metadata of its own
plugins/<name>/
  plugin.json                      the manifest — Agent Plugins 1.0.0, at the plugin root
  .claude-plugin/plugin.json       symlink → ../plugin.json, for Claude's traditional
                                   discovery path; it holds no content of its own
  skills/<name>/SKILL.md           the skill, per the Agent Skills specification
tools/check-conformance.py         the conformance check
tools/schemas/                     the official manifest schema, vendored
.github/workflows/conformance.yml  runs the check on push and pull request
```

Plugin versions are bumped on every change — without a `version` bump in
`plugin.json`, installed copies do not receive the update.

## Checking conformance

```
pip install jsonschema pyyaml
python3 tools/check-conformance.py
```

It verifies the parts of Agent Plugins 1.0.0 this repository is responsible
for. The same check runs in CI on every push and pull request.
