# Per-package release without a release PR: tooling research (2026-09-25)

Method. I read the documentation first and went to source only where the documentation had no answer. Each fact below names its source. **doc** means the vendor's documentation, read as its Markdown source at a pinned commit where one exists. **src** means source code at a commit permalink. **reg** means a registry or GitHub API reading taken on 2026-09-25. I ran none of the tools. Every behaviour below is as documented or as the code reads, not as observed.

Release dates come from the GitHub releases API and the npm and PyPI registries, read on 2026-09-25.

---

## 1. release-please and release-please-action

**No direct-commit mode is documented.** The design is PR-only.

- doc, [release-please README L20-21](https://github.com/googleapis/release-please/blob/edce3d805ef3ac964d1ba2b29b0f42905f2fa412/README.md#L20-L21): "Rather than continuously releasing what's landed to your default branch, release-please maintains Release PRs".
- doc, [docs/design.md L17-20](https://github.com/googleapis/release-please/blob/edce3d805ef3ac964d1ba2b29b0f42905f2fa412/docs/design.md#L17-L20): "`release-please` is designed to propose releases via a pull request." and "Releases are not created until after this "release pull request" is merged".
- doc, [design.md L55-61](https://github.com/googleapis/release-please/blob/edce3d805ef3ac964d1ba2b29b0f42905f2fa412/docs/design.md#L55-L61) gives the lifecycle. A commit lands, then "`release-please` opens a release pull request", then "A maintainer reviews/merges the release pull request", and only then is the GitHub release created.
- The action has two skip flags. Neither one commits a version bump. doc, [release-please-action README L85-86](https://github.com/googleapis/release-please-action/blob/0b6b3fc0186a2f7118bfd88fab9ea481e1839504/README.md#L85-L86):
  - `skip-github-release`: "If `true`, do not attempt to create releases. This is useful if splitting release tagging from PR creation."
  - `skip-github-pull-request`: "If `true`, do not attempt to create release pull requests. This is useful if splitting release tagging from PR creation."
  
  With `skip-github-pull-request: true` the action only tags and releases PRs that were already merged. Nothing writes the bumped `version` or the changelog.
- I searched the README and every file under `docs/` for "direct", "without a pull", "commit directly" and "skip-github-pull-request". None of them describes a PR-less bump.

**GITHUB_TOKEN and the workaround.** doc, [README L104-117](https://github.com/googleapis/release-please-action/blob/0b6b3fc0186a2f7118bfd88fab9ea481e1839504/README.md#L104-L117), section "Other Actions on Release Please PRs":

> "all resources created by `release-please` (release tag or release pull request) will not trigger future GitHub actions workflows, and workflows normally triggered by `release.created` events will also not run."

The recommended workaround is a PAT: "You will want to configure a GitHub Actions secret with a Personal Access Token if you want GitHub Actions CI checks to run on Release Please PRs." The README's workflow example uses `token: ${{ secrets.MY_RELEASE_PLEASE_TOKEN }}` ([L30-33](https://github.com/googleapis/release-please-action/blob/0b6b3fc0186a2f7118bfd88fab9ea481e1839504/README.md#L30-L33)).

**Permissions.** doc, [L119-131](https://github.com/googleapis/release-please-action/blob/0b6b3fc0186a2f7118bfd88fab9ea481e1839504/README.md#L119-L131): `contents: write`, `issues: write`, `pull-requests: write`, plus possibly "Allow GitHub Actions to create and approve pull requests".

**Versions (reg).** The action is at v5.0.0 (2026-04-22). The library is at v17.11.2 (2026-08-24).

**Also seen.** Open issue [#2898](https://github.com/googleapis/release-please/issues/2898), "Merged release PRs create no release under REST API version 2026-03-10". I did not investigate it.

**Verdict.** release-please does not fit a no-PR requirement.

---

## 2. semantic-release and its monorepo wrappers

### Core: direct commit, tags, GitHub releases

- **Tags.** semantic-release creates the Git tag itself. `tagFormat` defaults to `v${version}`, and "The `tagFormat` must contain the `version` variable exactly once". Source: doc, [configuration.md L134-143](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/usage/configuration.md#L134-L143), published at https://semantic-release.org/usage/configuration/#tagformat. A literal `howp--v${version}` is therefore valid.
- **Direct commit.** The `@semantic-release/git` `prepare` step will "Create a release commit, including configurable file assets". Source: doc, [semantic-release/git README L13-15](https://github.com/semantic-release/git/blob/bd77b8f91fd7124c2314f22cfbac7f281e08d9b6/README.md#L13-L15).
  - The default message is `chore(release): ${nextRelease.version} [skip ci]\n\n${nextRelease.notes}` ([L77-78](https://github.com/semantic-release/git/blob/bd77b8f91fd7124c2314f22cfbac7f281e08d9b6/README.md#L77-L78)).
  - The README warns: "You likely _do not_ need this plugin". The FAQ says: "we strongly recommend against this practice". Source: doc, [FAQ.md L22-31](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/support/FAQ.md#L22-L31).
  - Both are still documented and maintained. `@semantic-release/git` 11.0.1 was released 2026-07-24 (reg).
- **GitHub releases.** The `@semantic-release/github` `publish` step will "Publish a GitHub release". It needs at least `contents: write`, plus `issues`/`pull-requests: write` for its comments. It also notes: "releases done with this token will NOT trigger release events to start other workflows". Source: doc, [README L66-73](https://github.com/semantic-release/github/blob/a63f45804a21a4ddeba97f219ea8930e8d1dc7fb/README.md#L66-L73). Version 12.0.10 was released 2026-09-21 (reg).
- **Monorepos are not officially supported.** doc, [supported-branching.md L89-93](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/foundation/supported-branching.md#L89-L93): monorepos "are also not an officially supported **semantic-release** setup at this time … community plugins can enable monorepo support".
- **Versions (reg).** semantic-release 25.0.9 (2026-08-05), with a 26.0.0-beta.1 out (2026-08-07).

### Bumping `version` in a plain JSON file that is not package.json

- **`@semantic-release/exec` works.** It has a `prepareCmd` ("Execute a shell command to prepare the release"), and commands are templated with `${nextRelease.version}`. Source: doc, [exec README L8-17 and L29-47](https://github.com/semantic-release/exec/blob/3988e52646c4f4300a108b1bedcf512505c9373e/README.md#L8-L47).
  - Example: `"prepareCmd": "jq --arg v ${nextRelease.version} '.version=$v' plugin.json > t && mv t plugin.json"`.
  - `@semantic-release/git` then commits the file when it is listed in `assets`.
  - exec 7.1.0 was released 2025-05-09 (reg). That is the oldest release in the stack, but the repo was pushed 2026-09-24.
- **The plugins list has regex/glob "replace" plugins.** Examples are `semantic-release-replace-plugin`, "Replace version strings in files using regex and glob", and `semantic-release-mirror-version`. Source: doc, [plugins-list.mdx L359-362, L507-511](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/extending/plugins-list.mdx#L359-L362). I did not check whether either is maintained.

### multi-semantic-release family

All three variants find packages through **package.json workspaces** (npm/yarn `workspaces`, `pnpm-workspace.yaml` or bolt). Each package therefore needs a `package.json`, which these packages do not have.

- **dhoulb/multi-semantic-release**
  - Tags are fixed. "Releases always use a `tagFormat` of `my-pkg-1@1.0.1` for Git tags, and always overrides any `gitTag` set in semantic-release configuration." Source: doc, [README L321-323](https://github.com/dhoulb/multi-semantic-release/blob/257a7caaf1880d245c75a915189b8d2872b50cf7/README.md#L321-L323). **`<name>--v<version>` is not possible.**
  - It calls itself a "Proof of concept" that "may not be fundamentally stable enough for important production use" ([L12-17](https://github.com/dhoulb/multi-semantic-release/blob/257a7caaf1880d245c75a915189b8d2872b50cf7/README.md#L12-L17)).
  - Last release v3.1.0 on 2025-11-15. Before that, v3.0.2 on 2023-03-14 (reg).
- **@anolilab/multi-semantic-release**
  - `tagFormat` / `--tag-format` is configurable: "Should include "name" and "version" vars. Default: `"${name}@${version}"`". Source: doc, [README L293](https://github.com/anolilab/semantic-release/blob/76cd5db9ad7c5a6cd4d8b88a77f7cdc78ac611c4/packages/multi-semantic-release/README.md#L293). So `"${name}--v${version}"` fits, where `name` is the package.json `name`.
  - `ignorePrivate` is "**True by default.**" ([L291](https://github.com/anolilab/semantic-release/blob/76cd5db9ad7c5a6cd4d8b88a77f7cdc78ac611c4/packages/multi-semantic-release/README.md#L291)), so stub package.json files must not be private, or the option must be turned off.
  - Actively maintained: 4.4.19 on 2026-09-22 (reg).
- **@qiwi/multi-semantic-release**
  - The same `tagFormat` option ([README L56](https://github.com/qiwi/multi-semantic-release/blob/9adc120091a85b23a735de84ce702aa9d6c92c06/README.md#L56)).
  - Last release 7.1.2 on 2024-07-28, and the repo was last pushed that same day (reg). Treat it as unmaintained.

### semantic-release-monorepo

- **What it does.** It filters commits by path: "If a commit touched a file in or below a package's root, it will be considered for that package's next release". Tags are `<package-name>-<version>`. Source: doc, [README L15-19](https://github.com/pmowrer/semantic-release-monorepo/blob/a734b063bc4f325f6f70a8fbf0634d9bb02b9df5/README.md#L15-L19).
- **Tag format can be overridden.** The default is `<PACKAGE_NAME>-v<VERSION>`, overridable with `--tag-format` ([L90-100](https://github.com/pmowrer/semantic-release-monorepo/blob/a734b063bc4f325f6f70a8fbf0634d9bb02b9df5/README.md#L90-L100)). semantic-release's own rule is that "Options defined via CLI arguments or in the configuration file will take precedence over the ones defined in any shareable configuration" ([configuration.md L96-97](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/usage/configuration.md#L96-L97)). So `<name>--v${version}` is settable per package.
- **Needs a package.json per package.** The docs say it "allows using `semantic-release` with a single GitHub repository containing many `npm` packages". The source reads the name from the nearest package.json: src, [src/index.js L56](https://github.com/pmowrer/semantic-release-monorepo/blob/a734b063bc4f325f6f70a8fbf0634d9bb02b9df5/src/index.js#L56) `readPkg.sync().name`, and [only-package-commits.js L17](https://github.com/pmowrer/semantic-release-monorepo/blob/a734b063bc4f325f6f70a8fbf0634d9bb02b9df5/src/only-package-commits.js#L17) `pkgUp()`.
- **Runs one package at a time.** semantic-release has to be run once per package directory ([L29-45](https://github.com/pmowrer/semantic-release-monorepo/blob/a734b063bc4f325f6f70a8fbf0634d9bb02b9df5/README.md#L29-L45)).
- **Not maintained.** Last release 8.0.2 on 2024-02-05. The repo was last pushed 2024-08-05 (reg).

**Cost for this repository.** Any semantic-release route needs Node, a lockfile or pinned npx calls, and a package.json per plugin (for the wrappers) or one config per package. It also needs exec plus jq for plugin.json. Every commit it makes goes through `@semantic-release/git`, which the project itself recommends against.

---

## 3. git-cliff

Current version: **2.14.2**, released 2026-09-18 on GitHub and PyPI (reg; [Cargo.toml L3](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/git-cliff/Cargo.toml#L3)).

All four capabilities are documented.

- **Next version from conventional commits.** doc, [bump-version.md](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/usage/bump-version.md), also at https://git-cliff.org/docs/usage/bump-version: "To calculate and set the next semantic version (i.e. _bump the version_) for the unreleased changes: `git cliff --bump`". The rules are "fix:" to PATCH, "feat:" to MINOR, and breaking to MAJOR. `git cliff --bumped-version` will "calculate and print the next semantic version to `stdout`".
- **Tag prefixes.** "Tag prefixes are also supported, for example `testing/v1.0.0-beta.1` can be updated to `testing/v1.0.0-beta.2`". Also: "The next version is checked against the regex value set by tag_pattern".
- **Path restriction.** doc, [monorepos.md](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/usage/monorepos.md): "To include/exclude specific paths, use the `--include-path` and `--exclude-path` arguments … These paths must be relative to the repository's root and should be a valid glob pattern."
- **Per-package tags.** doc, [args.md L41](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/usage/args.md#L41): `--tag-pattern <PATTERN>  Sets the regex for matching git tags`. See also [configuration/git.md L280-284](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/configuration/git.md#L280-L284).
- **Writing the changelog.** doc, [args.md L49-51](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/usage/args.md#L49-L51) lists `-p, --prepend [<PATH>]`, `-o, --output`, and `-t, --tag <TAG>  Sets the tag for the latest version`. [examples.md L82-93](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/usage/examples.md#L82-L93) shows `git cliff --unreleased --tag 1.0.0 --prepend CHANGELOG.md`.
- **Config through environment variables.** Config values can be overridden with `GIT_CLIFF__<SECTION>__<FIELD>` ([configuration/index.md L45-67](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/configuration/index.md#L45-L67)).

Source-only facts that matter for the glue (the docs do not say these):

- **No bump still exits 0.** When nothing is releasable, `--bumped-version` prints the **current** version and exits 0. It logs "There is nothing to bump" and returns `last_version`. Source: src, [lib.rs L936-976](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/git-cliff/src/lib.rs#L936-L976). The glue has to compare the output against the current version.
- **The prefix is kept.** The output keeps the tag prefix, so `howp--v1.2.3` becomes `howp--v1.2.4`. The prefix is everything before the first numeric run that parses as semver. Source: src, [release.rs L155-229](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/git-cliff-core/src/release.rs#L155-L229).
- **No matching tag means `initial_tag`.** With no matching tag, the next version is `bump.initial_tag` (default `0.1.0`, unprefixed). An unprefixed value then fails the `tag_pattern` check with an error. Sources: src, [release.rs L236-239](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/git-cliff-core/src/release.rs#L236-L239) and [lib.rs L961-967](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/git-cliff/src/lib.rs#L961-L967); doc, [configuration/bump.md L31-35](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/configuration/bump.md#L31-L35). Seed one `<name>--v<current>` tag per package before enabling the workflow.

**Installation, pinned.**

- `pip install git-cliff==2.14.2` is available ([pypi.md](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/installation/pypi.md)).
- `taiki-e/install-action` is documented ([taiki-e-install-action.md](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/github-actions/taiki-e-install-action.md)).
- `orhun/git-cliff-action` also exists. Its latest tag is v4.9.1 (reg, `git ls-remote`).
- The ubuntu-24.04 runner ships jq 1.7 and GitHub CLI 2.100.0. Source: doc, [Ubuntu2404-Readme.md L84, L112](https://github.com/actions/runner-images/blob/ebade26c60adcb867918b31c8f8caa37343a3d39/images/ubuntu/Ubuntu2404-Readme.md#L84), image 20260907.

**`gh release create`.** doc, https://cli.github.com/manual/gh_release_create:

- `-F, --notes-file`, `-t, --title`, and `--target`.
- `--verify-tag`: "Abort in case the git tag doesn't already exist in the remote repository".
- Without it: "If a matching git tag does not yet exist, one will automatically get created from the latest state of the default branch." Use `--verify-tag` so the release attaches to the pushed tag.

**Remaining glue.** This is one workflow, one `cliff.toml`, and one shell step, about 30 lines. It is a sketch. I did not run it.

```yaml
on: { push: { branches: [main] } }
permissions: { contents: write }
concurrency: { group: release, cancel-in-progress: false }
jobs:
  release:
    runs-on: ubuntu-24.04
    steps:
      - uses: actions/checkout@<commit-sha>   # v7; fetch-depth 0 for tags and history
        with: { fetch-depth: 0 }
      - run: pip install git-cliff==2.14.2
      - env: { GH_TOKEN: "${{ github.token }}" }
        run: |
          set -euo pipefail
          git config user.name  "github-actions[bot]"
          git config user.email "41898282+github-actions[bot]@users.noreply.github.com"
          notes="$RUNNER_TEMP/notes"; mkdir -p "$notes"; bumped=()
          for dir in plugins/*/; do
            name=$(basename "$dir"); [ "$name" = howp ] && continue   # versioned by another repo
            p="${name}--v"; a=(--include-path "plugins/$name/**" --tag-pattern "^${p}[0-9]")
            cur=$(jq -r .version "plugins/$name/plugin.json")
            nxt=$(git cliff "${a[@]}" --bumped-version); nxt=${nxt#"$p"}
            [ "$nxt" = "$cur" ] && continue
            git cliff "${a[@]}" --unreleased --tag "$p$nxt" --strip all > "$notes/$name.md"
            git cliff "${a[@]}" --unreleased --tag "$p$nxt" --prepend "plugins/$name/CHANGELOG.md"
            jq --arg v "$nxt" '.version=$v' "plugins/$name/plugin.json" > "$RUNNER_TEMP/pj" \
              && mv "$RUNNER_TEMP/pj" "plugins/$name/plugin.json"
            bumped+=("$name@$nxt")
          done
          [ ${#bumped[@]} -eq 0 ] && exit 0
          git commit -am "chore(release): ${bumped[*]}"
          for b in "${bumped[@]}"; do git tag "${b%@*}--v${b#*@}"; done
          git push --atomic origin HEAD:main $(for b in "${bumped[@]}"; do echo "refs/tags/${b%@*}--v${b#*@}"; done)
          for b in "${bumped[@]}"; do n=${b%@*}; v=${b#*@}
            gh release create "$n--v$v" --verify-tag --title "$n v$v" -F "$notes/$n.md"; done
```

Points in this sketch that are my reasoning, not documentation:

- **The release commit must touch the package.** One release commit carries all bumped packages. All the new tags point at that commit, and it touches each bumped package's path. That keeps it inside `--include-path` for that package on the next run.
- **Push races.** `--atomic` plus the `concurrency` group guard against pushes racing in. A push rejected because `main` moved fails the run. It does not produce half a release.
- **jq reformatting.** `jq` re-serialises the file. If `plugin.json` is not already in jq's 2-space format, the first bump also reformats it.
- **CHANGELOG.md in the package.** A `CHANGELOG.md` inside `plugins/<name>/` becomes part of the published package.

---

## 4. Other ready-made tools

- **changesets**
  - **Not driven by conventional commits.** doc, [decisions.md L46-54](https://github.com/changesets/changesets/blob/c73949ba7b3160a4aa5729223335c190de1528f8/docs/decisions.md#L46-L54): "We commit our change information to the file system, instead of storing it in git", and it uses major/minor/patch rather than commit types. Contributors write changeset files.
  - **Needs package.json.** "The only requirement is that the project has a package.json file", and "Changesets only versions NPM package.json files" ([versioning-apps.md L8, L13](https://github.com/changesets/changesets/blob/c73949ba7b3160a4aa5729223335c190de1528f8/docs/versioning-apps.md#L8-L13)).
  - **Tags are fixed at `pkg-name@version-number`** ([command-line-options.md L166](https://github.com/changesets/changesets/blob/c73949ba7b3160a4aa5729223335c190de1528f8/docs/command-line-options.md#L166)).
  - `@changesets/cli` 3.0.3 was released 2026-09-14 (reg).
- **standard-version** is deprecated: "`standard-version` is deprecated" ([README L3](https://github.com/conventional-changelog/standard-version/blob/d70752c463991d34fa192e0332d7e4efacad78ba/README.md#L3)). Last release 9.5.0 on 2022-05-15 (reg).
- **commit-and-tag-version** (the maintained fork of standard-version)
  - **Single package per run.** It bumps files, commits and tags locally, and does "**without** automatic pushing (to GitHub)" ([README L551](https://github.com/absolute-version/commit-and-tag-version/blob/d56e5615b24510cafb0d662aca9cb87c5f7eea12/README.md#L551)).
  - **Several packages by running it once per package.** The `--path` option ("Only populate commits made under this path") is a CLI option in source (src, [command.js L117-120](https://github.com/absolute-version/commit-and-tag-version/blob/d56e5615b24510cafb0d662aca9cb87c5f7eea12/command.js#L117-L120)). I did not find it in the README.
  - **Tag prefix.** `-t/--tag-prefix` gives e.g. `howp--v` ([README L471-483](https://github.com/absolute-version/commit-and-tag-version/blob/d56e5615b24510cafb0d662aca9cb87c5f7eea12/README.md#L471-L483)).
  - **plugin.json needs explicit config.** It needs `{"filename": ".../plugin.json", "type": "json"}` ([README L567-586](https://github.com/absolute-version/commit-and-tag-version/blob/d56e5615b24510cafb0d662aca9cb87c5f7eea12/README.md#L567-L586)). Filename detection only knows the package.json-family names (src, [lib/updaters/index.js L36-39](https://github.com/absolute-version/commit-and-tag-version/blob/d56e5615b24510cafb0d662aca9cb87c5f7eea12/lib/updaters/index.js#L36-L39)).
  - **One commit per package.** Each run makes its own commit.
  - **No GitHub release.** The glue adds a push and `gh release create`.
  - 13.2.1 was released 2026-09-14 (reg).
- **knope**
  - **Several packages from conventional commits.** Yes, but it attributes commits to packages **by scope, not by path**: "An array of conventional commit scopes that Knope should consider for the package … Commits with no scope are always considered." Source: doc, [packages.mdx L407-419](https://github.com/knope-dev/knope/blob/c95207772898f344e160e3434c93f7c9f5fb0362/docs/src/content/docs/reference/Config%20File/packages.mdx#L407-L419). An unscoped `fix:` would bump every package.
  - **Any file through a regex.** `versioned_files` accepts a `regex` entry for any file ([L30-50](https://github.com/knope-dev/knope/blob/c95207772898f344e160e3434c93f7c9f5fb0362/docs/src/content/docs/reference/Config%20File/packages.mdx#L30-L50)).
  - **Tags are fixed** at `{name}/v{version}` (doc, [Steps/release.md L14-21](https://github.com/knope-dev/knope/blob/c95207772898f344e160e3434c93f7c9f5fb0362/docs/src/content/docs/reference/Config%20File/Steps/release.md#L14-L21)). The format is hardcoded (src, [action.rs L44-49](https://github.com/knope-dev/knope/blob/c95207772898f344e160e3434c93f7c9f5fb0362/crates/knope-versioning/src/action.rs#L44-L49)). **`<name>--v` is not possible.**
  - **Direct commit** is possible through workflow `Command` steps (`git commit`, `git push`), and the `Release` step creates GitHub releases (same release.md). 
  - knope 0.23.0 was released 2026-05-24 (reg).
- **cocogitto**
  - **Full per-package flow.** `cog bump --auto` in monorepo mode will "Calculate next version for each package based on commits that changes the package content", "Create a version commit", and "Create a tag for each new package version". Source: doc, [website/guide/monorepo.md](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/guide/monorepo.md), published at https://docs.cocogitto.io/guide/monorepo. The attribution is path-based.
  - **The global tag can be turned off.** `generate_mono_repository_global_tag` defaults to `true` (doc, [reference/config.md L94-100](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/reference/config.md#L94-L100)).
  - **Tag format.** `monorepo_version_separator` ([L138-140](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/reference/config.md#L138-L140)) and `tag_prefix` ([L209-213](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/reference/config.md#L209-L213)) are both settable. The tag is built as `{package}{separator}{prefix}{version}` (src, [git/tag.rs L286-294](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/crates/cocogitto/src/git/tag.rs#L286-L294)). Separator `--` with prefix `v` gives **`howp--v1.2.3`**.
  - **plugin.json through hooks.** It is bumped through `pre_package_bump_hooks` (e.g. jq).
  - **Push and release are glue.** Pushing is done through `post_bump_hooks` (`"git push"`, doc, [guide/bump.md L225-232](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/guide/bump.md#L225-L232)). GitHub releases are not built in; the docs pair it with `softprops/action-gh-release` ([ci_cd/action.md L86-114](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/ci_cd/action.md#L86-L114)).
  - **Caveats.**
    - `skip_ci` defaults to `"[skip ci]"` ([config.md L192-198](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/reference/config.md#L192-L198)).
    - It "will never do an auto bump to the `1.0.0` version" from `0.y.z` ([bump.md L124-125](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/guide/bump.md#L124-L125)).
    - The action "runs on x86 Linux runner only".
  - **Releases.** Last release 7.0.0 on 2026-03-04. The repo was last pushed 2026-04-22 (reg). That is slower than git-cliff.
- **release-plz** is Rust-only. It helps "release your Rust packages", does "Version bumps in `Cargo.toml`", and works "with a release Pull Request". Tags are `<package_name>-v<version>`. Source: doc, [README](https://github.com/release-plz/release-plz/blob/0409a66cc75c1590d8a998db3e6da8f522d380ae/README.md). It does not apply here. 0.3.169 was released 2026-09-19 (reg).

---

## 5. Committing to `main` from GitHub Actions

**Permissions.**

- The `contents` permission means "Work with the contents of the repository. For example, `contents: read` permits an action to list the commits, and `contents: write` allows the action to create a release". Source: doc, [github-token-scope-descriptions.md](https://github.com/github/docs/blob/75ea7dd097a5564f27364a5b70eaa1979106eabd/data/reusables/actions/github-token-scope-descriptions.md), shown at https://docs.github.com/en/actions/reference/workflows-and-actions/workflow-syntax#permissions.
- "If you specify the access for any of these permissions, all of those that are not specified are set to `none`."
- Pushing commits and tags and creating releases therefore needs `contents: write`. No other scope is needed.

**actions/checkout.**

- "The auth token is persisted in the local git config. This enables your scripts to run authenticated git commands." Also: "Set `fetch-depth: 0` to fetch all history for all branches and tags." Source: doc, [README L31-33](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/README.md#L31-L33).
- A built-in-token push example with the `github-actions[bot]` identity is at [L332-349](https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/README.md#L332-L349).
- The current major version is v7.

**GITHUB_TOKEN does not trigger workflows.** doc, [actions-do-not-trigger-workflows.md](https://github.com/github/docs/blob/75ea7dd097a5564f27364a5b70eaa1979106eabd/data/reusables/actions/actions-do-not-trigger-workflows.md), shown at https://docs.github.com/en/actions/concepts/security/github_token:

> "When you use the repository's `GITHUB_TOKEN` to perform tasks, events triggered by the `GITHUB_TOKEN` will not create a new workflow run, with the following exceptions: `workflow_dispatch` and `repository_dispatch` events always create workflow runs." It also lists `pull_request` opened/synchronize/reopened, which run in an approval-required state.
>
> "For all other events, this behavior prevents you from accidentally creating recursive workflow runs. For example, if a workflow run pushes code using the repository's `GITHUB_TOKEN`, a new workflow will not run even when the repository contains a workflow configured to run when `push` events occur."

The alternative, doc, [trigger-a-workflow.md L24-30](https://github.com/github/docs/blob/75ea7dd097a5564f27364a5b70eaa1979106eabd/content/actions/how-tos/write-workflows/choose-when-workflows-run/trigger-a-workflow.md#L24-L30): "use a GitHub App installation access token or a personal access token instead of `GITHUB_TOKEN`".

**What that means here.**

- **No loop.** The bump push made with GITHUB_TOKEN will not re-run the release workflow. The tags will not trigger it either.
- **CI does not see the release commit.** The release commit is not checked by `conformance.yml`, because no push workflow runs for it.
- **Releases trigger nothing.** Releases created with GITHUB_TOKEN will not fire `release` workflows. The same point is made by the semantic-release/github README (L66) and the release-please-action README (L106-108).

**Branch protection.**

- The semantic-release docs say: "The automatically populated `GITHUB_TOKEN` cannot be used if branch protection is enabled for the target branch. In that case, prefer GitHub App authentication". Source: doc, [github-actions.mdx L151-159](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/recipes/ci-configurations/github-actions.mdx#L151-L159).
- An App token *does* trigger workflows. The loop guard would then be `[skip ci]` in the message. GitHub documents `[skip ci]`, `[ci skip]`, `[no ci]`, `[skip actions]` and `[actions skip]` for `push`/`pull_request` (doc, [skip-workflow-runs.md](https://github.com/github/docs/blob/75ea7dd097a5564f27364a5b70eaa1979106eabd/content/actions/how-tos/manage-workflow-runs/skip-workflow-runs.md)). An `if:` on the commit author also works.
- Not verified: I did not read GitHub's own ruleset/branch-protection pages on whether GITHUB_TOKEN can be listed as a bypass actor.

---

## Comparison

| Tool | Direct commit | Multi-package (independent, from conventional commits) | Tag `<name>--v<version>` configurable | Maintained (last release) | Glue needed |
| :-- | :-- | :-- | :-- | :-- | :-- |
| release-please (+ action) | **No**, PR only | Yes (manifest) | Partly: component + `tag-separator`; the exact `--v` form was not checked | Yes (lib 17.11.2, 2026-08-24; action v5.0.0, 2026-04-22) | Not applicable; fails the no-PR requirement |
| semantic-release + git + exec + github | Yes (`@semantic-release/git`, which the docs discourage) | No (single package; "not officially supported") | Yes (`tagFormat`) | Yes (25.0.9, 2026-08-05) | Node toolchain, exec+jq for plugin.json, one run per package |
| dhoulb/multi-semantic-release | Yes (via git plugin) | Yes, but needs package.json workspaces | **No** (forced `name@version`) | Weak (3.1.0, 2025-11-15; previous 2023) | package.json stubs, exec+jq |
| @anolilab/multi-semantic-release | Yes (via git plugin) | Yes, needs package.json workspaces | Yes (`${name}--v${version}`) | Yes (4.4.19, 2026-09-22) | package.json stub per plugin (non-private), exec+jq, Node |
| @qiwi/multi-semantic-release | Yes (via git plugin) | Yes, needs workspaces | Yes | No (7.1.2, 2024-07-28) | As above |
| semantic-release-monorepo | Yes (via git plugin) | Yes, path-based; needs package.json per package | Yes (`--tag-format`) | No (8.0.2, 2024-02-05) | package.json stubs, per-package loop, exec+jq |
| **git-cliff** | No: computes and writes the changelog only | Yes (`--include-path` + `--tag-pattern`, path-based) | Yes (tag is caller-chosen; prefix preserved on bump) | Yes (2.14.2, 2026-09-18) | ~30-line shell step: loop, jq, commit, tag, push, `gh release create`; seed tags once |
| changesets | Via `changeset version` + manual commit | Yes, but from changeset files, **not** conventional commits; package.json only | No (`pkg@version`) | Yes (cli 3.0.3, 2026-09-14) | Not applicable |
| standard-version | Local commit | No | Prefix yes | **Deprecated** (9.5.0, 2022-05-15) | Not applicable |
| commit-and-tag-version | Local commit + tag, no push | One package per run (`--path`, source only) | Yes (`--tag-prefix`) | Yes (13.2.1, 2026-09-14) | Per-package loop and config, push, `gh release create`; one commit per package |
| knope | Yes (Command steps) | Yes, but **by commit scope, not path** | **No** (fixed `name/v`) | Yes (0.23.0, 2026-05-24) | Scope discipline in commits; tag format unacceptable |
| cocogitto | Yes (one version commit; push via hook) | Yes, path-based, per-package tags | Yes (`monorepo_version_separator = "--"`, `tag_prefix = "v"`) | Moderate (7.0.0, 2026-03-04) | `cog.toml`, jq pre-bump hook, disable global tag, push step, release step per tag |
| release-plz | No (release PR) | Rust/Cargo only | No (`name-v`) | Yes (0.3.169, 2026-09-19) | Not applicable |

**Short reading.** Two candidates meet every constraint.

- **git-cliff plus a short shell step.** It has the smallest dependency and is the most active. The glue is explicit.
- **cocogitto.** It does bump, commit and tag natively, path-based, with the exact tag form. It needs the same jq hook and a release step, and its release cadence is slower.

Every semantic-release route needs package.json files the packages do not have, a Node toolchain, and a commit plugin its own maintainers advise against. knope and changesets cannot produce the tag form or do not read conventional commits.

**Not verified / not found.**

- I did not run any tool. The git-cliff edge cases come from reading the source.
- I did not check whether release-please's `tag-separator` plus component can produce `name--v`. It is moot for this requirement.
- I did not read GitHub's ruleset docs on letting GITHUB_TOKEN bypass protection.
- I did not assess the maintenance of `semantic-release-replace-plugin` or `semantic-release-mirror-version`.
- I did not read the release-please-action v5 release notes; the API was rate-limited.
