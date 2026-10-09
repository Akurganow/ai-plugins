# About this repository's design

This page explains why the repository and its packages are built the way they are.
The client facts behind each reason are in [How the four clients load a package](clients.md), with their sources.
The evals section cites its running facts in place, because `clients.md` admits a running fact only from a run with no client signed in.
Every other fact here names its kind: source at a commit, or documentation read on 2026-09-25 unless its citation gives a date or a commit.
A fact about this repository names a dated read of its settings or releases, or a run of this repository's CI.

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

## CI checks structure and installation

CI runs these checks without a model:

- the conformance check against the vendored schema, and the regeneration diff;
- the 8,000-byte bound on the rules file, and the messages of pull request commits that touch `plugins/`;
- the validators that Claude Code, the Agent Skills project and Hermes publish;
- the evals runner's selftest, and `tools/evals.py validate` over every folder under `evals/`;
- an install matrix, where each client installs every package from the checkout.

In the matrix, Claude Code, Codex and Oh-My-Pi must list every skill after the install.
Hermes cells check that each package is installed and enabled, and no more.
Hermes 0.21.5 has no model-free command that prints a portable package's skills ([Hermes](clients.md#hermes)).
The matrix leaves out Hermes on Windows.
There the installer clones a branch before it checks out the pinned commit, and it failed in run 36183358181 ([Hermes](clients.md#hermes)).
Every client installs on the hosted runners with no account signed in ([How the four clients load a package](clients.md)).

## Behavioural evals run after each release

The conformance check, the validators and the install matrix prove structure and installation.
None of them shows that a skill triggers on a matching request, or that it improves the answer.
After each release, `.github/workflows/evals.yml` measures both for every released skill that has cases in `evals/`.
It is the only workflow here that calls a model.

`release.yml` calls it as a job of the release run.
A workflow triggered by the tags or the releases would never start, because the release makes both with `GITHUB_TOKEN`.
(documentation: [GitHub Docs, GITHUB_TOKEN](https://github.com/github/docs/blob/75ea7dd097a5564f27364a5b70eaa1979106eabd/data/reusables/actions/actions-do-not-trigger-workflows.md))
It can also run by hand on existing tags.
A re-run of the release job skips the evals, because its bump step then finds no releasable commit.
So a run by hand is the recovery when a release run created its tags but stopped before the evals job.
howp is not measured here, because another repository builds, checks and releases it.

Each skill has ten positive and ten near-miss prompts in `evals/<package>/<skill>/cases.yaml`.
The folder sits outside the packages, so no installed package carries the prompts.
A positive prompt runs with the package and again without it, and a near-miss prompt runs with it.
Each prompt runs three times in each of three clients: Claude Code with `sonnet`, Codex with `gpt-6-luna`, and Oh-My-Pi with `openrouter/z-ai/glm-5.3-flash`.
The counts follow the Agent Skills guide on trigger tests.
(documentation: [Optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions), read 2026-10-08)
Oh-My-Pi runs `z-ai/glm-5.3-flash`, because in Oh-My-Pi 18.8.6 it loaded `red-flags` in 3 of 3 sessions.
`deepseek-v4-flash` loaded it in 1 of 3, and `gemini-3.1-flash-lite` in 0 of 3.
(running: [run 37847660604](https://github.com/Akurganow/ai-plugins/actions/runs/37847660604), 2026-10-08)
TypeSafe's Jev grades each positive answer against the yes-or-no questions in `rubric.yaml`.
It is pinned to `jev-1.13.0`, because `jev-latest` moves to each new stable release and its answers can change with it.
(documentation: [Models](https://docs.typesafe.ai/models.md), read 2026-10-08)

The without arm removes a different set in each client.
Claude Code disables this package alone, with `claude plugin disable` and the package name.
(documentation: [Plugins CLI reference, plugin disable](https://code.claude.com/docs/en/plugins/cli-reference#plugin-disable), read 2026-10-09)
Codex turns off its `plugins` feature with `--disable plugins`.
(documentation: [Command line options, `--disable`](https://learn.chatgpt.com/docs/cli/reference.md) and [Configuration reference, `features.plugins`](https://learn.chatgpt.com/docs/config-file/config-reference.md), read 2026-10-09;
source: [`Feature::Plugins`](https://github.com/openai/codex/blob/979011409de0a60b52f179721948e65531d26144/codex-rs/features/src/lib.rs#L257-L258))
With it, Codex 0.161.0 listed only its four built-in skills and none from this package.
(running: [run 37789029106](https://github.com/Akurganow/ai-plugins/actions/runs/37789029106), 2026-10-08)
Oh-My-Pi disables every skill with `--no-skills`.
(documentation: [CLI reference, `--no-skills`](https://github.com/can1357/oh-my-pi/blob/40e9368ef0458fd9073329cdff4174895f91bc6b/docs/cli-reference.md#L159))
So a comparison of `improvement` across clients compares different removals.

Each skill and client gets four numbers per repeat:

- `trigger_hit`, the share of completed positive sessions with the package in which the skill loaded;
- `false_fire`, the share of completed near-miss sessions in which it loaded;
- `compliance`, Jev's mean on answers where the skill loaded;
- `improvement`, Jev's mean with the package minus its mean without.

`compliance` uses only those answers, so it does not mix following the skill with triggering it.
`improvement` keeps every graded answer with the package, because a user who installs the package gets both.
A session that errored leaves every denominator, and an answer Jev did not grade leaves the two Jev means.
The job summary lists both under `Excluded` with the reason.
It shows each figure with the sessions or answers behind it, so a share of 7 sessions is never read as a share of 10.
In `prose-discipline--v2.0.0`, a hook also prints the package's rules into every Claude Code session (see [the rules route](#one-rules-file-one-documented-route-per-client)).
It does the same in a Codex session once the user trusts the hook ([Codex](clients.md#codex)).
A with-package answer in such a session can follow the rules without the model loading `house-style`, and `trigger_hit` counts only that load.

The run attaches its results to the release as `evals.json`.
Workflow artifacts would not serve as the record, because a public repository keeps them 90 days at most.
(documentation: GitHub Docs, [artifact and log retention L1](https://github.com/github/docs/blob/7b807926df3ccb7f3d1bcd4ad1c652fb42b0931d/data/reusables/actions/about-artifact-log-retention.md#L1) and [L15](https://github.com/github/docs/blob/7b807926df3ccb7f3d1bcd4ad1c652fb42b0931d/data/reusables/actions/about-artifact-log-retention.md#L15))
A package can go longer than that between releases.
A metric regressed when the three repeats of this release and of the package's previous release do not overlap, and the new ones are worse.
The spread between repeats is the tolerance, so the rule has no threshold.
Where a package's previous release has no `evals.json`, nothing is compared.
`release.yml` runs one release at a time, its evals included, so a release's `evals.json` exists before the next release compares against it.
A regression opens an issue in the machine population, where the Issue Court and the delivery pipeline take it up.
Two releases are compared only when their `cases.yaml` and their `rubric.yaml` are byte-identical.
Each run installs the client's latest release, so the issue shows both client versions.

Four repository secrets reach the run, each only in the steps that need it: `ANTHROPIC_API_KEY`, `OPENAI_API_KEY`, `OPENROUTER_API_KEY` and `TYPESAFE_API_KEY`.
Each client process sees its own key alone, and the runner removes every key value from the published results.
Every session makes model calls billed to its key, and so does every Jev request.
No session has a time or cost limit, because no measurement shows that a limit would prevent a failure.
GitHub terminates a hosted job at six hours of execution, and that is the only bound.
(documentation: [GitHub Docs, Actions limits L45](https://github.com/github/docs/blob/7b807926df3ccb7f3d1bcd4ad1c652fb42b0931d/content/actions/reference/limits.md#L45))
A session or a grade that errors does not fail the job.
The job fails when the client does not install, every session errors, or every grade does.
`conformance.yml` runs `python tools/evals.py selftest`, which checks the event parsers and the arithmetic without a model.
How each client shows a loaded skill is written beside its parser in `tools/evals.py`, with the source it was read from.

Hermes is not measured.
The runner reads skill loads from a client's JSON event stream.
Hermes's stream, `--format stream-json`, implies one-shot mode.
(documentation: [`reference/cli-commands.md`](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/website/docs/reference/cli-commands.md#L123-L130))
Hermes leaves plugin skills out of the system prompt's skill index, and its `skills_list` tool shows them ([Hermes](clients.md#hermes)).
In one-shot mode the system prompt's skills section is loading guidance followed by that index, which lists each skill as its name and description.
(source: [`agent/prompt_builder.py`](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/agent/prompt_builder.py#L1372-L1382))
So the one-shot prompt shows the description of no plugin skill.
The guidance tells the model to load a skill only for knowledge it lacks, such as an API, a tool's commands or a project's conventions.
It names testing, debugging and review methodology as general process skills not to load for work the model knows how to do.
(source: [`agent/oneshot_footprint.py`](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/agent/oneshot_footprint.py#L42-L47))
`red-flags` reviews a design, and `root-cause` finds the core problem behind many symptoms.
`extraneous` diagnoses what a reader must hold in mind to do a task.
`ariz` and `contradiction` resolve a hard problem or a trade-off with TRIZ.
`house-style` applies a prose standard to anything an agent writes.
(source: the `description` front matter of the six skills at the tags `cognitive-load--v0.2.0`, `design-review--v0.2.0`, `prose-discipline--v2.0.0`, `toc-thinking--v0.2.0` and `triz--v0.2.0`, read 2026-10-09)
The five descriptions other than `house-style`'s each name a method, and none describes knowledge of a particular API, a tool's commands or a project's conventions.
So for those five skills a Hermes trigger rate would measure Hermes's prompt, not the description.
For `house-style` that conclusion rests on the index fact alone, because the one-shot prompt shows no plugin skill's description.

Five alternatives lost.
In Claude Code 2.1.293, `claude plugin eval` wrote the final reply only as the evidence of an LLM grader.
That grader runs a judge model of its own.
(running: [run 37784785554](https://github.com/Akurganow/ai-plugins/actions/runs/37784785554), 2026-10-08)
`claude plugin eval` has no custom-code graders, so Jev could not take the judge's place.
(documentation: [Test plugins with evals](https://code.claude.com/docs/en/plugin-evals), read 2026-10-08)
Concurrent sessions of one client sharing one configuration were not tested, so each job runs on a runner of its own.
A separate workflow on `workflow_run` would have to recover the release's tags, and would also start on every push that releases nothing.
A pinned client version would measure an older client than the one a user installs that day.
Prompts inside a package would reach every user who installs it, because Claude Code copies the plugin directory into its cache.
(documentation: [Plugin loading](https://code.claude.com/docs/en/plugins/loading), read 2026-10-08)

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
It runs `cosign verify-blob` against that identity and issuer, then compares the digest the table lists for the archive with the one in `binaries.json`.
(documentation: [Verifying blobs L34–L35](https://github.com/sigstore/docs/blob/842c30981f1bf5061fe0d370512db4de8cdf3b33/content/en/cosign/verifying/verify.md#L34-L35))
A release without a bundle, or with a table another identity signed, fails that job.
So the digests the skill trusts are the ones CI has checked against a signed table.
The skill itself keeps its SHA-256 check and never calls cosign.

Two alternatives lost.
GitHub artifact attestations would come from the build, which runs in a private repository because the sources are not public.
In a private repository, attestations need a GitHub Enterprise Cloud plan.
(documentation: [GitHub Docs, attestations availability](https://github.com/github/docs/blob/dec1018594fb5061bb1554dcafea7968fb10ff96/data/reusables/gated-features/attestations.md))
cosign inside the skill would need cosign on every user's machine.

## Pipeline items carry no closing keyword

A pipeline item names its sources in its fingerprint, as `sources=#a,#b`.
The pull-request bodies the pipeline Clerk and the Implementer write carry no closing keyword such as `Closes #n`.
GitHub closes a linked issue when a pull request whose description carries such a keyword merges into the default branch.
(documentation: [Linking a pull request to an issue](https://github.com/github/docs/blob/2bd66de8cea336061c9ea060c9b37385136e6ab3/content/issues/tracking-your-work-with-issues/using-issues/linking-a-pull-request-to-an-issue.md#L28-L35))
That close would skip the tracker Clerk's checks.
The tracker Clerk closes an issue as completed only when every claim re-derives as gone at the commit it runs on.
A remainder no pull request can carry gets a note and stays open.
The tracker Clerk closes the open sources of a pipeline item closed unmerged, as not planned.

The other direction belongs to the pipeline.
The pipeline Clerk closes an item whose sources are all closed, and narrows one when only some are.
The law proves a pipeline item by three facts.
One is that its head repository is this repository, so a fork cannot forge an item.
`.agents/skills/pipeline-law/SKILL.md` holds the stale and narrowing rules under "When a source closes", and the three facts under "What a fired stage trusts".
