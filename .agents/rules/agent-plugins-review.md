# Reviewing a package against Agent Plugins 1.0.0

What `tools/check-conformance.py` does not decide, and the sources of record
for the claims this marketplace makes. `conformance.md` owns what the check
decides and what it needs importable.

## What stays by hand

Never re-implement by hand what the check already decides. Four things
remain:

1. Each `SKILL.md` `name` and `description` is written to actually
   trigger. It says what the skill does and when to use it, not only
   what it is.
2. `keywords` are accurate and not generic. They are search surface too.
3. `description`, `author`, `homepage` and `repository` are accurate,
   not merely present.
4. The vendored schema still equals its published source. The check proves
   the copy matches the digest it records, and cannot know whether the
   published file has changed since. Compare
   `schemas/1.0.0/plugin.schema.json` from the Agent Plugins spec repository
   byte for byte with `tools/schemas/agent-plugins/1.0.0/plugin.schema.json`.
   `conformance.md`, "The vendored schema is a copy, not a source", says the
   copy is replaced only from its source.

Where this summary contradicts the live specification
(https://agent-plugins.org/specification), the live specification wins.

A plugin README states one sentence on what the plugin does and for whom,
matches its own `plugin.json` on `name` and `description` and on nothing
else, lists the shipped components, gets a reader to a sourced install path
for every surface the root README's Install section lists, shows an example
where the plugin has runnable behaviour, states prerequisites and
limitations, and links the marketplace root. It never states a `version`:
only a release writes it (`conformance.md`, "Versions").

## Sources of record

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

A source the network refuses, site and repository both, is reported as
blocked, and the checks that depend on it are reported as not run.
