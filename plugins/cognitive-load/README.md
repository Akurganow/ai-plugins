# cognitive-load

<!-- description:start -->

Separates the cognitive load a task needs from the load a code base's structure adds, and names the change that removes the second.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install cognitive-load@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add cognitive-load@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install cognitive-load@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md).

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/cognitive-load --no-enable
hermes plugins list
hermes plugins enable cognitive-load
```

Keep the `plugins/cognitive-load` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it.

<!-- install:end -->

## Usage

Name the task and the place where readers struggle:

```text
New hires take weeks to fix their first bug in our billing service.
Find what makes the code hard to follow.
```

The `extraneous` skill first fixes the reader and the task. It asks where
the last newcomer got stuck, and for how long. For each place, it counts
what the reader must hold at once and sorts each element as intrinsic or
extraneous. It names the section of Zakirullin's catalogue that explains
each extraneous element. It closes with the change that removes it, what
the change costs, and a check with a newcomer.

## What's inside

| Path | What it is |
| :-- | :-- |
| [`skills/extraneous/SKILL.md`](skills/extraneous/SKILL.md) | the procedure: reader and task, observations, count and sort, catalogue, measures, recommendation, check |
| [`skills/extraneous/references/theory.md`](skills/extraneous/references/theory.md) | cognitive load theory as read: origin, two loads, capacity, element interactivity, the effects, and where the theory stops |
| [`skills/extraneous/references/patterns.md`](skills/extraneous/references/patterns.md) | the essay's catalogue, section by section in its own words, with what to look for |
| [`skills/extraneous/references/measures.md`](skills/extraneous/references/measures.md) | Cognitive Complexity, Intrinsic Complexity Points, and what the studies of programmers found |
| [`skills/extraneous/references/sources.md`](skills/extraneous/references/sources.md) | for each reference, the public copy and commit it rests on, whether only its abstract was open, and what stays unread |
| [`plugin.json`](plugin.json) | the Agent Plugins 1.0.0 manifest |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | a byte-identical copy of `plugin.json` at the one manifest path Claude Code documents ([documentation](https://code.claude.com/docs/en/plugins-reference), "Plugin manifest schema") |
| [`LICENSE`](LICENSE) | the MIT license |

The package has no script, hook, rule file or network access.

The catalogue is Artem Zakirullin's essay "Cognitive load is what
matters", under CC BY 4.0. `sources.md` records the essay as read whole
at the commit it names, and the theory mostly as abstracts.
`sources.md` records, for each paper, whether it rests on the abstract,
the full text or nothing.

## Boundaries

- Cognitive load theory is a theory of learning, and its studies
  established its effects on instructional material. The skill applies
  them to code as analogies and says so. The essay uses "cognitive load"
  in an informal sense, and the skill keeps that distinction.
- The skill counts what you show it. It does not read a code base on its
  own, run a linter, or measure a reader.
- An interface as wide as what it hides, or one change that touches many
  places, belongs to the `red-flags` skill of
  [`design-review`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/design-review). A trade-off between two
  measured qualities belongs to `contradiction` in
  [`triz`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/triz). Many complaints with one unclear cause
  belong to `root-cause` in [`toc-thinking`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/toc-thinking).
  The skill hands over only to a skill that is installed.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/ai-plugins/blob/main/SUPPORT.md).
