# Reviewing a package against Agent Plugins 1.0.0

The sites are the sources of record. Where a repository publishes the same
text, that copy stands in when the site is blocked. Read a single file from
`https://raw.githubusercontent.com/<owner>/<repo>/<ref>/<path>`, and clone a
repository `--depth 1` only when the whole tree is needed. Cite a copy by
file and commit.

- Agent Plugins spec: https://agent-plugins.org/specification and
  https://agent-plugins.org/schemas; repository
  https://github.com/agentplugins/agent-plugins-spec. The text is
  `spec/1.0.0.md`, the schemas are under `schemas/1.0.0/`.
- Agent Skills: repository https://github.com/agentskills/agentskills. The
  text is `docs/specification.mdx`.
- Claude Code marketplaces:
  https://code.claude.com/docs/en/plugin-marketplaces. The same path with
  `.md` appended returns the Markdown.
- SemVer: https://semver.org/; repository https://github.com/semver/semver,
  file `semver.md`.
- Keep a Changelog: https://keepachangelog.com/en/1.1.0/; repository
  https://github.com/olivierlacan/keep-a-changelog, file
  `source/en/1.1.0/index.html.haml`.
- SPDX: https://spdx.org/licenses/; repository
  https://github.com/spdx/license-list-data. The one file to fetch raw is
  `json/licenses.json`.
- GitHub community profile:
  https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories;
  repository https://github.com/github/docs. The one file to fetch raw is
  `content/communities/setting-up-your-project-for-healthy-contributions/about-community-profiles-for-public-repositories.md`.
- Open Source Guides: https://opensource.guide/; repository
  https://github.com/github/opensource.guide.
- OpenSSF criteria: https://www.bestpractices.dev/en/criteria/0; repository
  https://github.com/coreinfrastructure/best-practices-badge, file
  `docs/criteria.md`.
- Google style: https://developers.google.com/style. No repository publishes
  it.
- Diátaxis: https://diataxis.fr/; repository
  https://github.com/evildmp/diataxis-documentation-framework.
- Codex plugin documentation: https://learn.chatgpt.com/docs/plugins,
  https://learn.chatgpt.com/docs/build-skills,
  https://learn.chatgpt.com/docs/hooks.md and
  https://developers.openai.com/plugins/build/plugins.md. The repository
  https://github.com/openai/codex held no copy: its `docs/` held fifteen
  files at `dda2278`, and none mentioned plugins (from source:
  https://github.com/openai/codex/tree/dda227891d27b6e0f3f244eda149a98d098969ad/docs).
- Hermes plugin documentation:
  https://hermes-agent.nousresearch.com/docs/developer-guide/plugins;
  repository https://github.com/NousResearch/hermes-agent, files
  `website/docs/developer-guide/plugins/index.md`,
  `website/docs/user-guide/features/plugins.md`,
  `website/docs/user-guide/features/skills.md` and
  `website/docs/user-guide/cli.md`.
- Oh-My-Pi plugin documentation: https://omp.sh/docs/marketplace; repository
  https://github.com/can1357/oh-my-pi, files `docs/marketplace.md` and
  `docs/skills.md`.
- standard-readme: repository https://github.com/RichardLitt/standard-readme,
  file `spec.md`.
- The ecosystems' listing rules. The Claude Code community marketplace:
  https://code.claude.com/docs/en/plugins.md, section "Submit your plugin to
  the community marketplace". The Hermes catalogue: `plugin-catalog/README.md`
  in https://github.com/NousResearch/hermes-agent. The awesome lists: the
  `CONTRIBUTING.md` of https://github.com/hesreallyhim/awesome-claude-code,
  https://github.com/travisvn/awesome-claude-skills and
  https://github.com/ComposioHQ/awesome-claude-skills.

A source the network refuses, site and repository both, is reported as
blocked, and the checks that depend on it are reported as not run.
