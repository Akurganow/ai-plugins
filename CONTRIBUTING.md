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
- `feat!:` or `fix!:` marks a breaking change and releases a major version.

Source: [Conventional Commits 1.0.0](https://www.conventionalcommits.org/en/v1.0.0/), documentation.

cocogitto versions each package from the commits that touched its path, and
writes that package's `CHANGELOG.md`. Source:
[Automatic versioning for monorepo](https://github.com/cocogitto/website/blob/8fa24cde1ec4598ccee7cdd47de40fa594282de2/src/guide/README.md#automatic-versioning-for-monorepo),
cocogitto documentation.

Put the package name in the scope, as in `fix(triz): correct one matrix cell`.
Renaming a skill breaks its users, so it takes `!`, as in
`feat(triz)!: rename the skill`. Use `docs:`, `ci:` or `chore:` for changes
outside `plugins/`.

Never edit `version` in a `plugin.json`. The release step writes it when it
releases a package.

`howp` is released from the repository that builds its `hp` binary. That
release writes three files here, and nobody edits them by hand:

- `version` in `plugins/howp/plugin.json`
- `plugins/howp/binaries.json`
- `plugins/howp/skills/forecast/references/commands.md`

## Run the checks

CI runs these checks on every pull request. Run them before you push.

### Regenerate the copies

Some files and regions are copies of another source.
[`tools/regenerate.sh`](tools/regenerate.sh) rewrites all of them. Edit the
source, run the script, and commit what it changes:

```
bash tools/regenerate.sh
```

It needs `jq`, `npx` from Node.js, and `shasum` or `sha256sum`. CI runs it
and fails if the tree changes afterwards.

These files are whole copies:

- `.claude-plugin/marketplace.json`, built from every `plugin.json` and
  `tools/templates/marketplace.json`
- `plugins/<name>/.claude-plugin/plugin.json`, a copy of `plugins/<name>/plugin.json`
- `plugins/<name>/LICENSE`, a copy of the root `LICENSE`

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
Claude Code documentation. CI also runs the other clients' validators, as
`.github/workflows/` defines.

## Propose a new package

1. Open a **New package** issue before you write the package.
2. Once the proposal is accepted, open a pull request that adds `plugins/<name>/`.
3. Follow the shape of an existing package, such as `plugins/triz/`.
4. Write `plugin.json` as an Agent Plugins 1.0.0 manifest.
5. Make its `description` one sentence of at most 250 characters.
6. Set `extensions["io.github.akurganow.ai-plugins"].category` to the category of the closest package.
7. Write `README.md` with the sections of the other package READMEs, in their order.
8. Put each skill in `skills/<skill>/SKILL.md` with `license: MIT` in its front matter.
9. Add the package to the `[monorepo.packages]` table in `cog.toml`.
10. Run `bash tools/regenerate.sh`, then the checks above.

Name each skill so that it stays distinct without the plugin name. Never
repeat the plugin name in it. Oh-My-Pi shows the bare skill name and drops a
later skill with the same name. Source:
[`docs/skills.md`](https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/skills.md),
Oh-My-Pi documentation.
