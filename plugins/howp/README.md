# howp

<!-- description:start -->

Turn what you follow into measurable questions, bind them to Polymarket and Manifold markets, and write a forecast from their probabilities and the agent's judgement.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install howp@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add howp@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install howp@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md).

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/howp --no-enable
hermes plugins list
hermes plugins enable howp
```

Keep the `plugins/howp` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it.

<!-- install:end -->

## Usage

Give the agent a first prompt:

```
Set up a forecast workspace in ~/howp. Ask me what I follow, then bind my questions to markets and write the first forecast.
```

With the `interests` skill, the agent interviews you one question at a
time. It writes `interests.yaml` and `questions/*.yaml` only after you
approve the list. With the `forecast` skill, it reads `binaries.json`,
probes the hosts, downloads the `hp` archive for your machine and checks
its sha256. It searches Polymarket and Manifold for a market per question
and records each verdict with its reasoning. It fetches the market bodies,
and `hp` records the probabilities.
`hp render` writes the forecast page to `data/dashboard.md` in the workspace.

Later prompts refresh the forecast, explain a sharp move or write the weekly
digest.

## What's inside

| Path | What it holds |
| :-- | :-- |
| [`skills/interests/SKILL.md`](skills/interests/SKILL.md) | The `interests` skill: interviews you and writes the questions a forecast is built on. |
| [`skills/interests/references/interview.md`](skills/interests/references/interview.md) | The interview, the formats of the two files you own, and what makes a good question. |
| [`skills/forecast/SKILL.md`](skills/forecast/SKILL.md) | The `forecast` skill: the platform rules, the workspace, the routine cycle and the three judgements. |
| [`skills/forecast/references/install.md`](skills/forecast/references/install.md) | How the `forecast` skill gets `hp`: the platform gate, the preflight, the download, the sha256 check and the unpack. |
| [`skills/forecast/references/procedures.md`](skills/forecast/references/procedures.md) | Binding a question to a market, explaining a sharp move and writing the weekly digest. |
| [`skills/forecast/references/commands.md`](skills/forecast/references/commands.md) | `hp --help` for every subcommand, written by the release job. |
| [`binaries.json`](binaries.json) | The released `hp` archives: version, targets, URLs and sha256 digests, written by the release job. |
| [`plugin.json`](plugin.json) | The manifest, with the host list under `extensions`. |

## Requirements and network

`hp` runs only on the targets [`binaries.json`](binaries.json) lists. On any
other machine the `forecast` skill stops and names the listed targets. It
never builds `hp` from source, because the source repository is private.

The `forecast` skill runs `uname`, `curl`, `tar`, `mktemp`, and `shasum` or
`sha256sum`. It needs no API key and no account.

### Hosts

[`plugin.json`](plugin.json) lists every host the `forecast` skill's steps
name, under `extensions["io.github.akurganow.ai-plugins"].network.hosts`:

<!-- hosts:start -->

- `github.com`
- `release-assets.githubusercontent.com`
- `raw.githubusercontent.com`
- `gamma-api.polymarket.com`
- `clob.polymarket.com`
- `api.manifold.markets`

<!-- hosts:end -->

The release archive comes from `github.com` and its redirect host,
`release-assets.githubusercontent.com`, until the `forecast` skill caches a
checked copy, as [`install.md`](skills/forecast/references/install.md)
Step 3 records. `raw.githubusercontent.com` serves `binaries.json` and
`plugin.json` only when a client loads the `forecast` skill without its
package. The Polymarket and Manifold hosts serve the market bodies. `hp`
opens no socket: the agent fetches every URL `hp` names with its own tools,
under your client's permission flow. The `forecast` skill probes each host
on every run and reports a blocked one instead of routing around it.

The list is a floor, not a fence. The agent searches for candidate markets
and for the story behind a move on its own. The `forecast` skill names no
host for those searches, and the hosts they reach are yours to allow. The
standard gives the list no meaning: the Agent Plugins manifest schema
assigns "no semantics to namespace object contents" of `extensions`
([schema](https://agent-plugins.org/schemas/1.0.0/plugin.schema.json),
specification).

### What it reads and writes

The `forecast` skill caches the archive at `${HOWP_CACHE:-$HOME/.cache/howp}/<version>`.
The workspace holds `interests.yaml`, `questions/`, `matches/` and `data/`.
`HP_DATA_DIR` moves `data/` elsewhere.

### When something fails

- The archive's sha256 must equal the digest in `binaries.json`. On a
  mismatch the `forecast` skill deletes the archive, runs nothing and tells
  you.
- A blocked host stops the step that needs it. The `forecast` skill names
  the host and where to allow it.
- A market that does not answer costs that market, not the run.

## Boundaries

- It does not score a forecast against its outcome. Whether a forecast came
  true is yours to judge.
- The package does not search for markets. The agent searches, and `hp`
  validates what the agent hands it.
- It places no bets and needs no account on either venue.
- The package calls no model. Every judgement comes from the agent you run
  it in.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/ai-plugins/blob/main/SUPPORT.md).
