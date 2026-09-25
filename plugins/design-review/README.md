# design-review

<!-- description:start -->

Reviews a software design for complexity with the red flags and principles of Ousterhout's A Philosophy of Software Design, each finding cited by chapter.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install design-review@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add design-review@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install design-review@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md).

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/design-review --no-enable
hermes plugins list
hermes plugins enable design-review
```

Keep the `plugins/design-review` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it.

<!-- install:end -->

## Usage

Describe the design, or paste it:

```text
Review the design of our storage module. Callers must call open, configure
and start in that order before every read, and three services wrap it.
```

The `red-flags` skill first asks who reads the module, who changes it, and
how often. It judges the module's depth and walks the book's fourteen red
flags. It ranks the findings by how often each part is touched and what
touching it costs. Each
finding names the change, its cost and the chapter it rests on.

## What's inside

| Path | What it is |
| :-- | :-- |
| [`skills/red-flags/SKILL.md`](skills/red-flags/SKILL.md) | the procedure: frame, symptom and cause, depth, red flags, together or apart, errors, rank, report |
| [`skills/red-flags/references/complexity.md`](skills/red-flags/references/complexity.md) | the book's definition of complexity, its symptoms and causes, and how it differs from Brooks' |
| [`skills/red-flags/references/red-flags.md`](skills/red-flags/references/red-flags.md) | the fourteen red flags, the book's wording, and what to look for |
| [`skills/red-flags/references/principles.md`](skills/red-flags/references/principles.md) | the sixteen design principles of the second edition, with a chapter for each |
| [`skills/red-flags/references/decisions.md`](skills/red-flags/references/decisions.md) | the criteria for together or apart, errors, design it twice, comments and names |
| [`skills/red-flags/references/positions.md`](skills/red-flags/references/positions.md) | where the book takes a side, the other side where it was read, and the evidence read |
| [`skills/red-flags/references/sources.md`](skills/red-flags/references/sources.md) | where each reference was read, at which commit, and what was not read |
| [`plugin.json`](plugin.json) | the Agent Plugins 1.0.0 manifest |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | a byte-identical copy of `plugin.json` at the one manifest path Claude Code documents ([documentation](https://code.claude.com/docs/en/plugins-reference), "Plugin manifest schema") |
| [`LICENSE`](LICENSE) | the MIT license |

The package has no script, hook, rule file or network access.

The book is under copyright, and `sources.md` records no bought copy of
either edition. It records the sixteen principles verbatim from three
public copies that agree, and the fourteen red flags from one. Chapter
quotations are a few sentences at most, from two public translation
repositories that carry the English. `sources.md` names each copy by
commit. The second edition lists sixteen principles and the first lists
fifteen, and the references say which is which.

## Boundaries

- The review weighs one quality: complexity in the book's sense.
- For method length, comments and test-driven development, a finding
  carries Robert Martin's reply from his written discussion with
  Ousterhout. The book's other positions carry no reply, because
  `positions.md` quotes no text of the other side for them.
- The skill reads the design you give it. It does not read a code base on
  its own and measures nothing.
- A trade-off between two measured qualities belongs to the
  `contradiction` skill of [`triz`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/triz). Many symptoms with
  one unclear cause belong to `root-cause` in
  [`toc-thinking`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/toc-thinking). What a reader cannot hold
  in their head belongs to `extraneous` in
  [`cognitive-load`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/cognitive-load). The skill hands over
  only to a skill that is installed.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/ai-plugins/blob/main/SUPPORT.md).
