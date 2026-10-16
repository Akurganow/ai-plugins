# Sources of record for the agent system

The published sources this repository's agent configuration rests on. Each
site is the source of record. Where a repository publishes the same text,
that copy stands in when the site is blocked. A copy is cited by file and
commit.

- **Agent Plugins specification.** https://agent-plugins.org/specification;
  repository https://github.com/agentplugins/agent-plugins-spec, files
  `spec/1.0.0.md` and `schemas/1.0.0/`. Covers package shape, fixed
  locations, manifest fields and what a client must do.
- **Agent Skills specification.** https://agentskills.io/specification;
  repository https://github.com/agentskills/agentskills, file
  `docs/specification.mdx`. Covers a skill's directory, `name`,
  `description` and front matter.
- **Claude Code plugin documentation.**
  https://code.claude.com/docs/en/plugins, and `plugins-reference`,
  `plugin-marketplaces`, `skills`, `hooks` and `sub-agents` under the same
  path; `.md` appended returns the Markdown. Covers the vendor manifest, the
  catalogue, hooks and agent bindings.
- **Codex plugin documentation.** https://learn.chatgpt.com/docs/plugins,
  https://learn.chatgpt.com/docs/build-skills,
  https://learn.chatgpt.com/docs/hooks.md and
  https://developers.openai.com/plugins/build/plugins.md. The repository
  https://github.com/openai/codex held no copy: its `docs/` held fifteen
  files at `dda2278`, and none mentioned plugins (from source:
  https://github.com/openai/codex/tree/dda227891d27b6e0f3f244eda149a98d098969ad/docs).
  Covers how Codex reads a package.
- **Hermes plugin documentation.**
  https://hermes-agent.nousresearch.com/docs/developer-guide/plugins;
  repository https://github.com/NousResearch/hermes-agent, files
  `website/docs/developer-guide/plugins/index.md`,
  `website/docs/user-guide/features/plugins.md`,
  `website/docs/user-guide/features/skills.md` and
  `website/docs/user-guide/cli.md`. Covers the portable subset and skill
  names.
- **Oh-My-Pi plugin documentation.** https://omp.sh/docs/marketplace;
  repository https://github.com/can1357/oh-my-pi, files
  `docs/marketplace.md` and `docs/skills.md`. Covers the catalogue path and
  skill-name collisions.
- **standard-readme.** Repository
  https://github.com/RichardLitt/standard-readme, file `spec.md`. Covers a
  README's sections and their order.
- **Keep a Changelog.** https://keepachangelog.com/en/1.1.0/; repository
  https://github.com/olivierlacan/keep-a-changelog, file
  `source/en/1.1.0/index.html.haml`. Covers a changelog.
- **Semantic Versioning.** https://semver.org/; repository
  https://github.com/semver/semver, file `semver.md`. Covers versions and
  tags.
- **The ecosystems' listing rules.** The Claude Code community marketplace:
  https://code.claude.com/docs/en/plugins.md, section "Submit your plugin to
  the community marketplace". The Hermes catalogue: `plugin-catalog/README.md`
  in https://github.com/NousResearch/hermes-agent. The awesome lists: the
  `CONTRIBUTING.md` of https://github.com/hesreallyhim/awesome-claude-code,
  https://github.com/travisvn/awesome-claude-skills and
  https://github.com/ComposioHQ/awesome-claude-skills. Cover what a listed
  package must carry.
