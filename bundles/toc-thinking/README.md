# toc-thinking

<!-- description:start -->

Applies Goldratt's Thinking Processes to software: finds the core problem behind many symptoms, resolves the conflict that sustains it, and plans the change.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/ai-plugins
/plugin install toc-thinking@ai-plugins
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>.

### Codex

```
codex plugin marketplace add Akurganow/ai-plugins --ref main
codex plugin add toc-thinking@ai-plugins
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/ai-plugins
omp plugin install toc-thinking@ai-plugins
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md).

### Hermes

```
hermes plugins install Akurganow/ai-plugins/plugins/toc-thinking --no-enable
hermes plugins list
hermes plugins enable toc-thinking
```

Keep the `plugins/toc-thinking` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it.

<!-- install:end -->

## Usage

List what you observe:

```text
Deploys fail about once a week, the nightly build is flaky, and on-call
pages keep coming back after every fix. Find the core problem.
```

The `root-cause` skill states each symptom as an undesirable effect. It
builds a Current Reality Tree down to the root causes, and checks every
link with the Categories of Legitimate Reservation. It asks you to confirm
the core problem before going on. It then builds the Evaporating Cloud for
the conflict that keeps the problem in place. A Future Reality Tree checks
the injection for new undesirable effects. The skill plans the change with
a Prerequisite Tree and a Transition Tree.

## What's inside

| Path | What it is |
| :-- | :-- |
| [`skills/root-cause/SKILL.md`](skills/root-cause/SKILL.md) | the procedure: classify, Current Reality Tree, Evaporating Cloud, Future Reality Tree, Prerequisite Tree, Transition Tree |
| [`skills/root-cause/references/tools.md`](skills/root-cause/references/tools.md) | the structure of each tree and of the cloud, with its logic |
| [`skills/root-cause/references/clr.md`](skills/root-cause/references/clr.md) | the eight Categories of Legitimate Reservation, each with a software example |
| [`skills/root-cause/references/sources.md`](skills/root-cause/references/sources.md) | the books and dictionary entries the references rest on, and what stays unread |
| [`plugin.json`](plugin.json) | the Agent Plugins 1.0.0 manifest |
| [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json) | a byte-identical copy of `plugin.json` at the one manifest path Claude Code documents ([documentation](https://code.claude.com/docs/en/plugins-reference), "Plugin manifest schema") |
| [`LICENSE`](LICENSE) | the MIT license |

The package has no script, hook, rule file or network access.

The references rest on the TOCICO Dictionary and on Dettmer's *The
Logical Thinking Process*. `sources.md` names the public copy of each by
commit. The Categories of Legitimate Reservation are Dettmer's eight, and
`clr.md` notes TOCICO's count of seven.

## Boundaries

- The procedure works on facts you can observe. It asks you for a fact
  it lacks rather than guessing the system's structure. It does not
  replace a profiler, a debugger or a test.
- The skill attributes nothing to Goldratt or Dettmer without a chapter or
  a dictionary entry that `sources.md` names.
- A cloud that reduces to a trade-off between two measurable parameters
  belongs to the `contradiction` skill of [`triz`](https://github.com/Akurganow/ai-plugins/tree/main/plugins/triz).
  `root-cause` hands over only when `contradiction` is installed.

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/ai-plugins/blob/main/SUPPORT.md).
