# Contributing

Issues and pull requests are welcome.

## File an issue

Open an issue with one of the forms:

- **Install problem**: a plugin fails to install, enable or load in a client.
- **Bug**: a plugin loads but does the wrong thing.
- **New package**: you propose a plugin for this marketplace.

Report a vulnerability privately, as [SECURITY.md](SECURITY.md) describes.
[SUPPORT.md](SUPPORT.md) says where to ask a question.

## Write commits

Commits follow Conventional Commits. The type sets the next version:

- `fix:` marks a bug fix and releases a patch version.
- `feat:` marks a new feature and releases a minor version.
- `feat!:`, `fix!:` or a `BREAKING CHANGE:` footer marks a breaking change and releases a major version from 1.0.0 up.

Source: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), documentation.

cocogitto versions each package from the commits that touched its path, and
writes that package's `CHANGELOG.md`. Source:
[Automatic versioning for monorepo](https://github.com/cocogitto/website/blob/8fa24cde1ec4598ccee7cdd47de40fa594282de2/src/guide/README.md#automatic-versioning-for-monorepo),
cocogitto documentation.

cocogitto never bumps a package below 1.0.0 to 1.0.0, even for a breaking
change. Source:
[Auto bump](https://github.com/cocogitto/website/blob/8fa24cde1ec4598ccee7cdd47de40fa594282de2/src/guide/README.md#L614-L615),
cocogitto documentation. Below 1.0.0 the type alone sets the version: `feat!:`
releases a minor version and `fix!:` a patch version. Source:
[`bump.rs`](https://github.com/cocogitto/cocogitto/blob/055a9fa8db8ac8ce50074d50162b48b92e9d0c47/crates/cocogitto/src/conventional/bump.rs#L258-L273),
cocogitto source at 7.0.0, the release that `release.yml` installs.

Put the package name in the scope, as in `fix(triz): correct one matrix cell`.
Renaming a skill breaks its users, so it takes `!`, as in
`feat(triz)!: rename the skill`. Use `docs:`, `ci:` or `chore:` for changes
outside `plugins/`.

Pull requests merge with a merge commit, so each commit reaches `main` as
written. CI refuses a pull request with a non-conventional commit that touches
`plugins/`, because the release would skip that commit. The `commits` job in
[`conformance.yml`](.github/workflows/conformance.yml) runs that check.

Never edit `version` in a `plugin.json`, and never edit a package's
`CHANGELOG.md`. [`release.yml`](.github/workflows/release.yml) writes both when
it releases a package.

The repository that builds the `hp` binary releases `howp`. That release
writes four files here, and nobody edits them by hand:

- `version` in `plugins/howp/plugin.json`
- `plugins/howp/binaries.json`
- `plugins/howp/skills/forecast/references/commands.md`
- `plugins/howp/.claude-plugin/plugin.json`, a byte copy of `plugins/howp/plugin.json`

## Run the checks

CI runs these checks on every pull request. Run them before you push.

### Regenerate the generated files

[`tools/regenerate.sh`](tools/regenerate.sh) writes some files and regions
from another source. Edit the source, run the script, and commit what it
changes:

```
bash tools/regenerate.sh
```

It needs `jq`, Node.js with `npm`, and `shasum` or `sha256sum`. It installs
doctoc from `tools/package-lock.json` when `tools/node_modules` does not match it.
That install needs the npm registry. CI runs the script and fails if the tree
changes afterwards.

It writes these whole files:

- `.claude-plugin/marketplace.json`, built from every `plugin.json` and
  `tools/templates/marketplace.json`
- `plugins/<name>/.claude-plugin/plugin.json`, a byte-identical copy of `plugins/<name>/plugin.json`
- `plugins/<name>/LICENSE`, a byte-identical copy of the root `LICENSE`

A generated region sits between two comments, `<!-- <region>:start -->` and
`<!-- <region>:end -->`. A table of contents sits between doctoc's
`START doctoc` and `END doctoc` comments. Never edit inside either pair.

### Run the conformance check

The check needs the Python packages `jsonschema` and `pyyaml`. Install the
versions that [`conformance.yml`](.github/workflows/conformance.yml) pins,
then run:

```
python3 tools/check-conformance.py
```

It must exit 0.

### Validate with Claude Code

With Claude Code installed, validate each plugin you changed:

```
claude plugin validate plugins/<name>
```

Source: [Plugins reference](https://code.claude.com/docs/en/plugins-reference),
Claude Code documentation, read 2026-09-25. CI also runs the Agent Skills and
Hermes validators. It installs every package into each client that
[`integration.yml`](.github/workflows/integration.yml) lists.

## Propose a new package

1. Open a **New package** issue before you write the package.
2. Once a maintainer accepts the proposal, open a pull request that adds `plugins/<name>/`.
3. Follow the shape of an existing package, such as `plugins/triz/`.
4. Write `plugin.json` as an Agent Plugins 1.0.0 manifest.
5. Make its `description` one sentence of at most 250 characters and 25 words.
6. Set `extensions["io.github.akurganow.ai-plugins"].category` to the category of the closest package.
7. Write `README.md` with the sections of the other package READMEs, in their order.
8. Put each skill in `skills/<skill>/SKILL.md` with `license: MIT` in its front matter.
9. Add the package to the `[monorepo.packages]` table in `cog.toml`.
10. Run `bash tools/regenerate.sh`, then the checks above.
11. After the merge, a maintainer pushes the seed tag `<name>--v<version>` at the merge commit.

In a package README, link a file outside the package by its full GitHub URL,
and a file inside it by a relative path. A package installs alone, and the
Hermes catalogue renders its README at the pinned commit. Source:
[`plugin-catalog/README.md`](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/plugin-catalog/README.md#L86),
Hermes documentation.

The seed tag carries the version in the package's `plugin.json`.
[`release.yml`](.github/workflows/release.yml) refuses to release any package
while a `cog.toml` package has no such tag reachable from `main`.

Name each skill so that it stays distinct without the plugin name. Never
repeat the plugin name in it. Oh-My-Pi shows the bare skill name and drops a
later skill with the same name. Source:
[`docs/skills.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/skills.md#L98),
Oh-My-Pi documentation.
