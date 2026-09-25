# triz

<!-- description:start -->

Resolves software trade-offs with TRIZ: the contradiction matrix and 40 inventive principles, the separation principles, and ARIZ-85C walked part by part with the user.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install triz@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add triz@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install triz@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md).

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/triz --no-enable
hermes plugins list
hermes plugins enable triz
```

Keep the `plugins/triz` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it.

<!-- install:end -->

## Usage

Describe the trade-off in your own words:

```text
A longer cache lifetime takes load off the database but serves stale reads.
Find a way out that is not a compromise.
```

The `contradiction` skill restates the problem as a contradiction and asks
you to confirm it. It writes the ideal final result and maps both sides to
two of Altshuller's 39 parameters. It reads the matching cell of the
contradiction matrix. It returns two to four directions, each named after
its principle and stated as a change to your system. A problem the matrix
route does not crack, or one that keeps coming back, goes on to the `ariz`
skill. It walks ARIZ-85C part by part with you. When ARIZ restates the
problem as a new technical contradiction, `ariz` offers it back to
`contradiction`.

## What's inside

| Path | What it is |
| :-- | :-- |
| [`skills/contradiction/SKILL.md`](skills/contradiction/SKILL.md) | the matrix route: contradiction, ideal final result, separation, parameters, matrix, principles |
| [`skills/contradiction/references/parameters.md`](skills/contradiction/references/parameters.md) | the 39 parameters, each with a reading for software |
| [`skills/contradiction/references/principles.md`](skills/contradiction/references/principles.md) | the 40 principles, each with Altshuller's sub-items and a reading for software; `ariz` reads it too |
| [`skills/contradiction/references/matrix.md`](skills/contradiction/references/matrix.md) | the classic matrix, one line per cell, with its provenance and the disputed cells |
| [`skills/contradiction/references/sources.md`](skills/contradiction/references/sources.md) | the copy and commit each reference of both skills rests on, and the sources that stayed out of reach |
| [`skills/ariz/SKILL.md`](skills/ariz/SKILL.md) | the ARIZ-85C walk, part by part, for a problem the matrix route did not crack or that keeps coming back |
| [`skills/ariz/references/ariz-85c.md`](skills/ariz/references/ariz-85c.md) | the nine parts and forty steps of ARIZ-85C, with the formulas quoted and a software gloss |
| [`plugin.json`](plugin.json) | the Agent Plugins 1.0.0 manifest |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | a byte-identical copy of `plugin.json` at the one manifest path Claude Code documents ([documentation](https://code.claude.com/docs/en/plugins-reference), "Plugin manifest schema") |
| [`LICENSE`](LICENSE) | the MIT license |

The package has no script, hook, rule file or network access. The agent
searches the matrix for one line, so the lookup needs nothing installed.

The matrix is the classic 39 by 39 table with 1,248 non-empty cells. It
merges two public transcriptions, which differ on 40 cells. A third, and
for three cells a fourth, settle those 40 by majority. `matrix.md` lists
every reading of each disputed cell. No reachable transcription has more
than 1,248 cells, so the often-quoted count of 1,263 stays unconfirmed.
`sources.md` names each copy by commit.

## Boundaries

- The matrix, the principles and ARIZ give directions with a published
  origin, not guarantees. Your knowledge of your system decides which
  direction survives.
- A problem with no trade-off in it is not a TRIZ problem.
  `contradiction` says so before any lookup, and `ariz` before Part 1.
- The software readings of the parameters and principles are this
  package's own. `sources.md` reports finding no published mapping of the
  39 parameters to software, and no study of the matrix on software
  problems.
- A tangle of symptoms with no trade-off in sight belongs to the
  `root-cause` skill of [`toc-thinking`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/toc-thinking).
  Both skills hand over only when `root-cause` is installed.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/ai-plugins/blob/main/SUPPORT.md).
