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

### Run the evals selftest and folder check

The selftest of [`tools/evals.py`](tools/evals.py) needs only Python 3.12:

```
python3 tools/evals.py selftest
```

It calls no model. The evals themselves run in CI after a release, as
[About this repository's design](docs/design.md) describes.

The `validate` subcommand checks every `evals/<package>/<skill>/` folder. Each
folder needs its skill's `SKILL.md`, and its files must load. It needs the
Python package `pyyaml`, in the version that
[`conformance.yml`](.github/workflows/conformance.yml) pins:

```
python3 tools/evals.py validate
```

It must exit 0. CI runs it in the `check` job.

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
10. For each skill, write `evals/<name>/<skill>/cases.yaml` and `rubric.yaml` by [these rules](#write-a-skills-evals-cases).
11. Run `bash tools/regenerate.sh`, then the checks above.
12. After the merge, a maintainer pushes the seed tag `<name>--v<version>` at the merge commit.

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

### Write a skill's evals cases

A skill's folder holds two files:

- `cases.yaml` has a `positive` list and a `near_miss` list. Each list has ten
  entries, and each entry has an `id` and a `prompt`.
- `cases.yaml` may also have `always_on`, a list of the clients that get the
  skill's rules in every session without loading the skill. A comment beside
  it names each client's route and its source. For those clients the summary
  shows `trigger_hit` and `compliance` as `n/a`.
- `rubric.yaml` has a `questions` map from a question id to one statement,
  or to an `instructions` statement with optional `criteria` and `cases`.
  `criteria` holds a quoted `"true"` and `"false"`, each saying what that
  answer means. `cases` lists the ids of the positive prompts the question
  applies to. A question without `cases` applies to every positive prompt.

The Agent Skills guide sets the shape of a trigger test. Source:
[Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions),
Agent Skills documentation, read 2026-10-09. These rules follow the guide, add
this repository's own, and apply to every skill:

- **Positive prompts** cover every "Use when" clause of the skill's
  `description` at least once.
- **Positive prompts** vary along four axes. Phrasing runs from formal to
  casual, with an occasional typo. Explicitness runs from naming the domain to
  describing only the need. Detail runs from terse to context-heavy.
  Complexity runs from a single step to a task buried in a larger one.
- **The most useful positive prompts** are those where the skill would help
  but the query does not make the connection obvious.
- **Near-miss prompts** share keywords or concepts with the skill but need
  something different. A prompt with no overlap tests nothing and does not
  belong.
- **Realism.** The guide asks for file paths, personal context, specific
  details and casual language.
- **Self-contained.** Each session starts in an empty directory. A prompt
  carries the code, text or situation it asks about in its own body.
- **The result in the reply.** A prompt asks for its result in the reply, never
  in a file, because Jev grades only the final message.
- **Neutral.** A prompt never names the skill, its package or the text the
  skill rests on. A user who names them needs no trigger.
- **Ids** are short kebab-case names of what the prompt asks. They stay unique
  across both lists.

Jev grades each positive answer on the questions that apply to its prompt. Two
of the rules below rest on the failure modes that TypeSafe documents for
`jev-1.13`. Source:
[Jev 1.13 jaggedness](https://docs.typesafe.ai/model-jaggedness/jev-1.13.md),
TypeSafe documentation, read 2026-10-09. The measurements behind the other
rules are in
[About this repository's design](docs/design.md#behavioural-evals-run-after-each-release).

- **One question per rule** of the skill that a reader can check in the answer
  text. Take the rules from `SKILL.md` and the references it names as required
  output.
- **`cases` for a rule of one form.** A question about one artifact form, such
  as a review comment or a PR description, names in `cases` the prompts that
  write it.
- **No question at the ceiling.** Drop a question that every answer passes in
  both arms, because it measures nothing.
- **A statement that holds** for an answer which follows the skill, such as
  "Each finding names the chapter of the book it rests on."
- **One step.** Each question is answerable from the answer text in one step.
  Jev answers less reliably when a question needs extra levels of indirection
  (section "Indirection").
- **No counting.** `jev-1.13` does not count reliably (section "Counting"). A
  sentence-length or item-count rule stays out.
- **No condition, position or bundle.** A question is not conditional ("each
  finding that rests on X ..."), positional ("before any finding ...", "ends
  with ...") or a bundle of several facts. Each of those makes Jev find
  something first and then judge it, which is two steps.
- **Criteria where the boundary is unclear.** TypeSafe documents `criteria`
  for a subtle yes-or-no boundary. Source:
  [Noul](https://docs.typesafe.ai/primitives/noul.md), TypeSafe documentation,
  read 2026-10-09. Keep criteria only where they lower Jev's mean error against
  labelled answers, on a second set of answers as well as the first. The
  skill's `calibration.json` holds each labelled answer, its label with the
  evidence, its half of the split, and Jev's score with and without the
  criteria.
- **No checks of sentence structure.** A question about semicolons, dashes or
  one thought per sentence stays out, because Jev's answers to such questions
  do not follow the labels.
- **Judged from the answer alone.** A question never compares the answer with
  the request, and never needs knowledge the answer does not contain. When an
  answer may quote the text it checks or cleans, a style question says
  "outside text it quotes".
- **Three to eight questions** apply to each positive prompt. Each id is a
  short snake_case name.
