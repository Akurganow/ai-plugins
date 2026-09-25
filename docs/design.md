# About this repository's design

This page explains why the repository and its packages are built the way they are.
The client facts behind each reason are in [How the four clients load a package](clients.md), with their sources.
Every other fact here names its kind: documentation, read on 2026-09-25, source at a commit, or a dated read of this repository's settings or releases.

## One source for every copy

Clients read the same facts from different files.
Claude Code documents one manifest path, `.claude-plugin/plugin.json` ([Claude Code](clients.md#claude-code)).
Codex shows the category `Other` unless the marketplace entry supplies one ([Codex](clients.md#codex)).
So the catalogue repeats each manifest's description and category.
Every package README repeats the install commands, and every package carries its own `LICENSE`.
A package installs alone, and Agent Plugins 1.0.0 §4.1 keeps every path it supplies inside its root.
(documentation: [Agent Plugins specification §4.1](https://github.com/agentplugins/agent-plugins-spec/blob/ff8ab5e392cc87bd88d87c060815a87490e51003/spec/1.0.0.md#L58-L64))
So each package carries its own copy, not a path to a root file.

A copy kept by hand drifts from its source, and nothing notices until a reader does.
So `plugins/<name>/plugin.json` is the only source of a package's metadata.
Its category sits under `extensions["io.github.akurganow.ai-plugins"]`, and reaches clients through the catalogue.
`tools/regenerate.sh` writes every copy from its source, with ready-made tools such as `jq` and `doctoc`.
CI runs the script and fails when the tree then differs from the commit.
The failure message names the command that repairs it.

Two alternatives lost.
One command per kind of copy leaves a contributor to remember which command follows which edit.
A CI job that commits the copies back would put changes on `main` that no pull request showed.

## The vendor manifest is a byte copy, not a symlink

Claude Code reads only `.claude-plugin/plugin.json`, and fails on a manifest that is not JSON ([Claude Code](clients.md#claude-code)).
Claude Code, Codex and Oh-My-Pi fetch a marketplace with git on the user's machine ([Claude Code](clients.md#claude-code), [Codex](clients.md#codex), [Oh-My-Pi](clients.md#oh-my-pi)).

With `core.symlinks` false, git checks a symlink out as a plain file holding the link text.
(documentation: [git manual, `core.symlinks`](https://github.com/git/git/blob/c44beea485f0f2feaf460e2ac87fdd5608d63cf0/Documentation/config/core.adoc#L237-L246))
Git for Windows disables symlink support by default.
(documentation: [Git for Windows vs symbolic links](https://gitforwindows.org/symbolic-links))
Its installer enables symlinks only under Developer Mode, or when a test link succeeds for the installing user.
(source: [`install.iss` L1342–L1369](https://github.com/git-for-windows/build-extra/blob/c8241c75c7c06d6db94ed6a8dd9b8ca76d1ed842/installer/install.iss#L1342-L1369),
[L2459–L2467](https://github.com/git-for-windows/build-extra/blob/c8241c75c7c06d6db94ed6a8dd9b8ca76d1ed842/installer/install.iss#L2459-L2467))
So a default Windows checkout turns a symlinked vendor manifest into text, and Claude Code fails to load it.
The link cannot point the other way either: Codex rejects a plugin whose root `plugin.json` is a symlink ([Codex](clients.md#codex)).

A CI job cannot settle the question.
GitHub's Windows runner image installs Git with symlinks enabled.
(source: [`Install-Git.ps1` L27–L37](https://github.com/actions/runner-images/blob/ebade26c60adcb867918b31c8f8caa37343a3d39/images/windows/scripts/build/Install-Git.ps1#L27-L37))
A job there loads a symlink that a default user checkout breaks.

So `plugins/<name>/.claude-plugin/plugin.json` is a regular file, byte-identical to the root `plugin.json`.
`tools/regenerate.sh` writes it, and the conformance check compares the two files byte for byte.
Agent Plugins 1.0.0 §5.1 says no other file can "replace, supplement, or override the core fields in root `plugin.json`".
(documentation: [Agent Plugins specification §5.1](https://github.com/agentplugins/agent-plugins-spec/blob/ff8ab5e392cc87bd88d87c060815a87490e51003/spec/1.0.0.md#L133-L137))
A byte-identical copy overrides nothing.
The cost is a second manifest in every package, which the generator and the check keep equal.

## Skill names carry no plugin prefix

Claude Code, Codex and Hermes prefix a plugin skill with a namespace ([Claude Code](clients.md#claude-code), [Codex](clients.md#codex), [Hermes](clients.md#hermes)).
So a skill named after its plugin reads `/triz:triz` in Claude Code.
Claude Code also answers a bare `/<skill>` while no other command uses that name ([Claude Code](clients.md#claude-code)).
Oh-My-Pi shows the bare name, keeps the first skill of each name, and drops the rest ([Oh-My-Pi](clients.md#oh-my-pi)).
A generic name such as `review` collides in Oh-My-Pi with any other source that ships one.

A skill name is therefore distinctive without the plugin prefix, and never repeats the plugin name.
It is one word, or one compound such as `root-cause`, so it stays short in Oh-My-Pi's bare list and still names its method.
The directories under `plugins/*/skills/` hold the names in use:

| Package | Skills |
| :-- | :-- |
| cognitive-load | `extraneous` |
| design-review | `red-flags` |
| howp | `forecast`, `interests` |
| prose-discipline | `house-style` |
| toc-thinking | `root-cause` |
| triz | `contradiction`, `ariz` |

A package holds a second skill when one skill carried two jobs with different triggers.
In `howp`, `interests` interviews the person and writes the two files they own, once per interest.
`forecast` keeps the binary, the cycle and the procedures that run on every cycle.
`interview` lost as that skill's name, because it is the likeliest bare name for an unrelated skill.
In `triz`, `ariz` walks ARIZ-85C, a nine-part algorithm that the matrix route never opens.
`contradiction` keeps the matrix route, and hands a problem it did not crack to `ariz`.
`toc-thinking` stays one skill.
Its five trees form one sequence, and each tree's output is the next one's input.

A rename changes every invocation, so it ships as a breaking release.
A Hermes `skills.auto_load` entry names the skill, so a rename breaks that entry too.

## One rules file, one documented route per client

`prose-discipline` ships a writing standard that should be active in every session, without the user invoking it.
Each client documents a different route for standing instructions:

- Claude Code: a `SessionStart` hook's plain stdout, and `SubagentStart`'s `additionalContext` for subagents ([Claude Code](clients.md#claude-code)).
- Codex: plugin hooks declared under `extensions.com.openai`, run after the user trusts them ([Codex](clients.md#codex)).
- Oh-My-Pi: a plugin `rules/` file with `alwaysApply: true` ([Oh-My-Pi](clients.md#oh-my-pi)).
- Hermes: the user's `skills.auto_load` list, which loads a named skill in full ([Hermes](clients.md#hermes)).

`plugins/prose-discipline/rules/prose-discipline.md` is the one source of the rules.
Every other carrier reads it at run time, or `tools/regenerate.sh` generates it.

One `hooks/hooks.json` serves Claude Code and Codex.
Its commands use shell form, with no `args` field.
Claude Code's exec form needs `args`, and Codex documents no such field ([Claude Code](clients.md#claude-code), [Codex](clients.md#codex)).
Codex's parser ignores an unknown handler key, so under Codex an `args` hook would run `sh` with no script ([Codex](clients.md#codex)).
The hook runs `hooks/print-rules.sh`, which needs `sh` and `awk` and no language runtime.
For `SessionStart`, the script prints a heading first.
The rules then open with a statement of fact, as Claude Code advises for hook text ([Claude Code](clients.md#claude-code)).
Claude Code parses stdout that starts with `{` and ends with `}` as JSON ([Claude Code](clients.md#claude-code)).

The rules file stays under 8,000 bytes, and CI fails at that size.
Claude Code caps hook text at 10,000 characters ([Claude Code](clients.md#claude-code)).
Codex writes `additionalContext` over 2,500 tokens to disk by default ([Codex](clients.md#codex)).
The bound keeps the rules under Claude Code's cap, and keeps English prose under Codex's threshold.
So `hooks/hooks.json` carries no `additionalContextLimit`, the Codex key that moves that threshold.
(documentation: [Codex, Hooks](https://learn.chatgpt.com/docs/hooks), read 2026-09-26)
Claude Code's [Hooks page](https://code.claude.com/docs/en/hooks) says nothing about a handler key it does not know (documentation, read 2026-09-26).

Hermes loads no hooks and no `rules/` from a package ([Hermes](clients.md#hermes)).
So `skills/house-style/SKILL.md` carries the rules in a generated region.
The package README shows the `skills.auto_load` entry, with the qualified name `tools/regenerate.sh` computes from the manifest `name`.

Python lost.
A Hermes native plugin can add a system-prompt section, but it needs `plugin.yaml` and an `__init__.py` ([Hermes](clients.md#hermes)).
When a directory holds both manifests, Hermes loads the native one and skips the portable `plugin.json`.
(source: [`plugins_discovery.py` L147–L155](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_discovery.py#L147-L155),
[`plugin_validate.py` L482–L485](https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugin_validate.py#L482-L485))
A native half would stop Hermes from loading the package as Agent Plugins.

In Claude Code and Oh-My-Pi, invoking `house-style` puts the rules in context a second time.
The skill body stays anyway, because it is the only carrier Hermes loads.
In Hermes, the user adds one config entry, and nothing else loads the rules.
In Codex, the user trusts the hook once, and again after each change to it ([Codex](clients.md#codex)).

## No hook blocks the agent

Clients offer ways to force a standard, not only to state it.
A Claude Code `Stop` hook can return `"decision": "block"` and keep Claude working.
(documentation: [Hooks, Stop decision control](https://code.claude.com/docs/en/hooks#stop-decision-control))
A `PreToolUse` hook can deny a tool call.
(documentation: [Hooks, PreToolUse decision control](https://code.claude.com/docs/en/hooks#pretooluse-decision-control))
A `UserPromptSubmit` hook can add context to every prompt.
(documentation: [Hooks, UserPromptSubmit](https://code.claude.com/docs/en/hooks#userpromptsubmit))
In Oh-My-Pi, a TTSR rule aborts a response on a match and retries it ([Oh-My-Pi](clients.md#oh-my-pi)).

`prose-discipline` states the standard and enforces nothing.
It ships no blocking hook, no per-prompt reminder and no TTSR rule file.
A gate on prose halts real work over a style match.
Repeating text already in context adds tokens and no fact.
The rules enter each context once, and again where the client dropped them, as after compaction ([Claude Code](clients.md#claude-code)).

Compliance therefore rests with the model, and nothing in the package checks the output.

## Codex gets its documented hook route

Codex documents plugin hooks under `extensions.com.openai` in a root `plugin.json` ([Codex](clients.md#codex)).
Its loader returns no hooks for a package in Agent Plugins format, and two open issues report it ([Codex](clients.md#codex)).
In Codex 0.155.1, the config parser skips a `plugin_hooks` toggle, so no setting changes that ([Codex](clients.md#codex)).
The same branch loads hooks for every other manifest format, such as a package without a root `plugin.json`.
(source: [`loader.rs` L954–L964 at `rust-v0.155.1`](https://github.com/openai/codex/blob/be2951ea34f0d295ed0becf97079f92fa5f6950e/codex-rs/core-plugins/src/loader.rs#L954-L964))
That package would not conform to Agent Plugins 1.0.0.

So `prose-discipline` declares its hooks the documented way and ships no workaround.
In Codex 0.155.1, the rules reach a session only when the model loads `house-style`.
When upstream fixes the loader, the hook runs with no change here.

The integration workflow reports the Codex hook check as not run.
The step's comment links [openai/codex#39895](https://github.com/openai/codex/issues/39895) and [openai/codex#47925](https://github.com/openai/codex/issues/47925).
While the loader drops the hooks, an assertion that the hook runs can only fail.
An assertion allowed to fail lost: it would turn green in silence when upstream changes, and the allowance would stay.
When upstream fixes the loader, someone replaces the notice with a real check by hand.

## Releases come from cocogitto, straight to main

Claude Code keeps users on their cached copy until `version` changes ([Claude Code](clients.md#claude-code)).
It documents release tags of the form `<plugin-name>--v<version>` ([Claude Code](clients.md#claude-code)).
A version moved by hand gets forgotten, and users then keep an old copy.
A release should follow the commit that earned it, with no release pull request to merge.

[cocogitto](https://github.com/cocogitto/cocogitto) releases every package but `howp`.
`cog bump --auto` derives each package's next version from the conventional commits that touched its path.
It writes one version commit and one tag per bumped package.
(documentation: [cocogitto, Monorepo](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/guide/monorepo.md))
`cog.toml` sets the separator `--` and the prefix `v`, so tags read `<name>--v<version>`.
(documentation: [cocogitto configuration reference L138–L140](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/reference/config.md#L138-L140),
[L209–L212](https://github.com/cocogitto/cocogitto/blob/8cfddce66f6eece4e5f310565737cac030be8e63/website/reference/config.md#L209-L212))
A workflow on each push to `main` runs the bump and publishes one GitHub release per new tag.
It pushes with `GITHUB_TOKEN`, and a push made with that token starts no workflow run.
(documentation: [GitHub Docs, GITHUB_TOKEN](https://github.com/github/docs/blob/75ea7dd097a5564f27364a5b70eaa1979106eabd/data/reusables/actions/actions-do-not-trigger-workflows.md))
So the version commit cannot start the release again.

Three other tools lost.
release-please works through release pull requests.
(documentation: [release-please README L18–L21](https://github.com/googleapis/release-please/blob/edce3d805ef3ac964d1ba2b29b0f42905f2fa412/README.md#L18-L21))
A pull request opened with `GITHUB_TOKEN` starts its workflow runs in an approval-required state.
(documentation: [GitHub Docs, GITHUB_TOKEN](https://github.com/github/docs/blob/75ea7dd097a5564f27364a5b70eaa1979106eabd/data/reusables/actions/actions-do-not-trigger-workflows.md))
So every release would wait for a person to approve its checks and merge a second pull request.
semantic-release does not officially support monorepos.
(documentation: [Supported branching L89–L93](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/foundation/supported-branching.md#L89-L93))
Its FAQ also advises against committing the release back to the branch.
(documentation: [FAQ L22–L31](https://github.com/semantic-release/docs/blob/d4d3420ade2348e15739bc46cd15aaab8d2bf373/src/content/docs/support/FAQ.md#L22-L31))
git-cliff computes the next version and the changelog.
(documentation: [git-cliff, Bump version](https://github.com/orhun/git-cliff/blob/60e0be97e945f71148172675be82399d382c9677/website/docs/usage/bump-version.md))
The commit, the tags and the push would then be a shell loop kept here.

### Seed tags

Without a tag, cocogitto reads a package's history from the repository's first commit.
It also starts that package from version 0.0.0.
(source: [`bump.rs` L190–L194](https://github.com/cocogitto/cocogitto/blob/055a9fa8db8ac8ce50074d50162b48b92e9d0c47/crates/cocogitto/src/conventional/bump.rs#L190-L194),
[`monorepo.rs` L413–L416](https://github.com/cocogitto/cocogitto/blob/055a9fa8db8ac8ce50074d50162b48b92e9d0c47/crates/cocogitto/src/command/bump/monorepo.rs#L413-L416),
[`tag.rs` L187–L191](https://github.com/cocogitto/cocogitto/blob/055a9fa8db8ac8ce50074d50162b48b92e9d0c47/crates/cocogitto/src/git/tag.rs#L187-L191))
For `prose-discipline`, at 1.3.0, that would release a lower version than the one users hold.
So each package has one seed tag at `232aaba`, carrying the version its manifest held there:
`cognitive-load--v0.1.0`, `design-review--v0.1.0`, `prose-discipline--v1.3.0`, `toc-thinking--v0.1.0` and `triz--v0.1.0`.
The release workflow refuses to run while any package in `cog.toml` has no reachable tag.

### Breaking changes

[CONTRIBUTING.md](../CONTRIBUTING.md#write-commits) gives the commit types and the versions they release.
`prose-discipline` is past 1.0.0, so its rename to `house-style`, a `feat!` commit, releases it as 2.0.0.

### Changelogs

Each package keeps a `CHANGELOG.md`, written by the bump from `tools/templates/changelog.tera`.
cocogitto's default package template adds an inline-HTML `BREAKING` badge, and credits the author and co-authors on every line.
(source: [`template.rs` L18](https://github.com/cocogitto/cocogitto/blob/055a9fa8db8ac8ce50074d50162b48b92e9d0c47/crates/cocogitto/src/conventional/changelog/template.rs#L18),
[`macros.tera` L1–L13](https://github.com/cocogitto/cocogitto/blob/055a9fa8db8ac8ce50074d50162b48b92e9d0c47/crates/cocogitto/src/conventional/changelog/template/macro/macros.tera#L1-L13))
The template keeps `BREAKING:` as text, and drops the HTML and the author credit, which says who, not what.

### Merges and commit messages

[CONTRIBUTING.md](../CONTRIBUTING.md#write-commits) gives the rules; these are their reasons.
A squash merge folds a branch's commits into one commit, and the bump then loses each commit's type and paths.
So the repository settings allow merge commits only (GitHub API, read 2026-09-25).
The bump drops a commit whose message does not parse, and says nothing.
(source: [`bump.rs` L204–L208](https://github.com/cocogitto/cocogitto/blob/055a9fa8db8ac8ce50074d50162b48b92e9d0c47/crates/cocogitto/src/conventional/bump.rs#L204-L208))
That is why CI checks the messages of pull request commits that touch `plugins/`.

### Trade-offs

The release runs beside the conformance run on the same push, not after it.
The same checks run on each pull request before its merge.
A release can still publish a commit whose check on `main` then fails.

The release step runs `gh release create` without `--latest`, so GitHub picks the repository's Latest release by date and version.
(source: [`create.go` L218](https://github.com/cli/cli/blob/9b031151a825bda919203c5202876a725d637368/pkg/cmd/release/create/create.go#L218))
A package release can take the Latest label from a `howp` release.
Nothing downloads by that label: `plugins/howp/binaries.json` names each archive by its tag.

### howp

The private repository that builds `hp` releases `howp`, and cocogitto leaves it out.
Only that release job knows the version, the digests and the binary's help text.
It writes the files [CONTRIBUTING.md](../CONTRIBUTING.md#write-commits) lists, such as `plugins/howp/skills/forecast/references/commands.md`.
A second writer would move `version` with no binary behind it.

## Nothing in CI calls a model

Claude Code can run a plugin's eval suite with `claude plugin eval`.
Every eval run and every judge grader is a model call billed to the account.
(documentation: [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals))
Nothing in CI or in a package calls a model.
CI therefore needs no model credentials, and a run costs no model calls.

CI checks structure instead:

- the conformance check against the vendored schema, and the regeneration diff;
- the 8,000-byte bound on the rules file, and the messages of pull request commits that touch `plugins/`;
- the validators that Claude Code, the Agent Skills project and Hermes publish;
- an install matrix, where each client installs every package from the checkout.

In the matrix, Claude Code, Codex and Oh-My-Pi must list every skill after the install.
Hermes cells check that each package is installed and enabled, and no more.
Hermes 0.21.5 has no model-free command that prints a portable package's skills ([Hermes](clients.md#hermes)).
The matrix leaves out Hermes on Windows.
There the installer clones a branch before it checks out the pinned commit, and it failed in run 36183358181 ([Hermes](clients.md#hermes)).
Every client installs on the hosted runners with no account signed in ([How the four clients load a package](clients.md)).

CI does not measure whether a skill changes an agent's behaviour.
Behavioural evals are tracked in [issue #62](https://github.com/Akurganow/ai-plugins/issues/62).

## The repository records no maintainer verification

A sentence about what the maintainer ran describes one machine on one date.
[How the four clients load a package](clients.md) shows what takes its place: every fact cites its kind and source.

## howp's host list and signature

`howp` downloads and runs `hp`, a binary built from sources that are not public.

The manifest's `extensions["io.github.akurganow.ai-plugins"].network.hosts` is the one list of hosts the package reaches.
The README's host list is generated from it.
It names every host the skill's steps name, so an allowlist built from it alone lets every step through.
That includes `release-assets.githubusercontent.com`, which GitHub lists as needed to download release assets.
(documentation: [Self-hosted runners reference, accessible domains by function](https://docs.github.com/en/actions/reference/runners/self-hosted-runners#accessible-domains-by-function))
It also includes `raw.githubusercontent.com`, where the skill can read the package's manifest files.

The skill checks each archive's SHA-256 against `plugins/howp/binaries.json`.
A digest proves the archive is the recorded one, not who built it.
The release [`howp-v0.3.7`](https://github.com/Akurganow/ai-plugins/releases/tag/howp-v0.3.7) carries `SHA256SUMS` and `SHA256SUMS.sigstore.json`, a Sigstore bundle over the table (release assets, read 2026-09-26).
The certificate in that bundle names `https://github.com/Akurganow/how-possible/.github/workflows/release.yml@refs/heads/main` as the signer and `https://token.actions.githubusercontent.com` as the issuer (the bundle's certificate, read 2026-09-26).
Those are the two values a GitHub Actions workflow gets under keyless signing.
The identity is the workflow file at a branch, and no long-lived key exists.
(documentation: [OIDC in Fulcio L40–L43](https://github.com/sigstore/docs/blob/842c30981f1bf5061fe0d370512db4de8cdf3b33/content/en/certificate_authority/oidc-in-fulcio.md#L40-L43); [Signing blobs L10–L12](https://github.com/sigstore/docs/blob/842c30981f1bf5061fe0d370512db4de8cdf3b33/content/en/cosign/signing/signing_with_blobs.md#L10-L12))
The `howp-archive` job of `.github/workflows/integration.yml` downloads the table and the bundle of the release `binaries.json` names.
It runs `cosign verify-blob` against that identity and issuer, then compares the table's digest with the one in `binaries.json`.
(documentation: [Verifying blobs L34–L35](https://github.com/sigstore/docs/blob/842c30981f1bf5061fe0d370512db4de8cdf3b33/content/en/cosign/verifying/verify.md#L34-L35))
A release without a bundle, or with a table another identity signed, fails that job.
So the digests the skill trusts are the ones CI has checked against a signed table.
The skill itself keeps its SHA-256 check and never calls cosign.

Two alternatives lost.
GitHub artifact attestations would come from the build, which runs in a private repository because the sources are not public.
In a private repository, attestations need a GitHub Enterprise Cloud plan.
(documentation: [GitHub Docs, attestations availability](https://github.com/github/docs/blob/dec1018594fb5061bb1554dcafea7968fb10ff96/data/reusables/gated-features/attestations.md))
cosign inside the skill would need cosign on every user's machine.
