# ai-plugins

A public marketplace of agent plugins and skills. Skills follow the open
[Agent Skills standard](https://agentskills.io/specification) (a folder with
a `SKILL.md`) and work in Claude Code, OpenAI Codex, and other agents that
adopted the standard.

This repository contains only text instructions and pinned links to
releases. No executables are stored in the tree: a skill downloads the
binaries for your platform from the published releases and verifies their
checksums against the table committed here.

## Installation

**Claude Code:**

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install howp@ai-plugins
```

**Codex:** copy the skill folder into the Codex skills directory:

```
git clone https://github.com/Akurganow/ai-plugins /tmp/ai-plugins
mkdir -p ~/.codex/skills
cp -r /tmp/ai-plugins/plugins/howp/skills/howp ~/.codex/skills/howp
```

(check the current Codex documentation on Agent Skills for the exact skills
directory — the `SKILL.md` format is the same). **Other compatible agents:**
same idea — copy the skill folder into your agent's skills directory.

## Plugins

| Plugin | What it does | Status |
|---|---|---|
| `howp` | Personal probability dashboard: interests → measurable questions → prediction-market probabilities → a markdown dashboard | placeholder, first release in the works |

## Layout

```
.claude-plugin/marketplace.json   marketplace catalog (Claude Code)
plugins/<name>/
  .claude-plugin/plugin.json      plugin manifest (its version drives updates)
  skills/<name>/SKILL.md          the skill, per the Agent Skills standard
```

Plugin versions are bumped on every change — without a `version` bump in
`plugin.json`, installed copies do not receive the update.
