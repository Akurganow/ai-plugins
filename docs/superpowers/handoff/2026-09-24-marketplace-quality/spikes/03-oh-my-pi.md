# Spike 3: Oh-My-Pi

Run on 2026-09-25 with Oh-My-Pi `omp/18.2.8`, fixture built from plan 03 blocks A–F at commit `b836b12`.

The fixture and every run directory sat outside the repository, under a per-run scratch directory called `$RUN` below. `$TMPDIR` was `/var/folders/3s/wqmf9fc17fq54yt52m1wvqvh0000gn/T/`.

Every fact below comes from running the client. Both model runs used `--model haiku`, which each sidecar names as `claude-haiku-4-5`, provider `anthropic`, thinking level `low`.

## Assertions

| Id | Assertion | Result | Evidence |
| :-- | :-- | :-- | :-- |
| 3a-rules | the fixture's `rules/prose-discipline.md`, loaded by `--plugin-dir`, is in the system prompt on each request | pass | Both sidecars printed `generic-rules=1 new-marker=1`. Each system prompt holds the rules body between `<generic-rules>` and `</generic-rules>`. |
| 3a-skill | the fixture's `house-style` skill loads with no startup warning | pass | Both sidecars printed `house-style=1`. The skill list holds `- house-style: Apply this plugin's engineering prose standard …`. No warning names the skill. |
| 3b-rules | the published 1.3.0 package's rules file, installed from the marketplace, is in the system prompt | pass | The sidecar printed `generic-rules=1 old-marker=1`. `<generic-rules>` opens with the 1.3.0 heading and the old marker. |
| 3b-skill | the published package's `prose-discipline` skill is in the prompt's skill list | pass | The sidecar printed `skill=1`. The skill list holds `- prose-discipline: The prose standard for all agent-written output: …`. |

## Commands and output

The interactive steps ran under `expect`, which typed the brief's lines into the Oh-My-Pi TUI. The script is `$RUN/session.exp`.

### Step 1: versions and state

```sh
omp --version
jq -r '.plugins | keys[]' ~/.omp/plugins/installed_plugins.json | tee "$RUN/installed-before.txt"
omp plugin marketplace list
```

```
omp/18.2.8
cognitive-load@ai-plugins
design-review@ai-plugins
toc-thinking@ai-plugins
triz@ai-plugins
typesafe@typesafe-ai
Configured Marketplaces:

  ai-plugins  Akurganow/ai-plugins
  typesafe-ai  typesafe-ai/skills
```

The list held no `prose-discipline@ai-plugins`.

### Step 2: fixture

Blocks A, B, C, D and F were copied by line range from the plan file, then the recipe ran.

```
fixture-syntax-ok
# Prose discipline: core rules
1
```

`diff -r` against the spike 1 fixture printed nothing.

### Probe before 3a

A start with no prompt checked for a startup dialog before `expect` typed anything. It ran `omp --plugin-dir "$RUN/fixture/prose-discipline" --model haiku` in `$RUN/cwd`.

The TUI showed the welcome panel, `Claude Haiku 4.5`, `anthropic` and `New version 18.3.1 is available. Run: omp update`. It showed no dialog. Ctrl-C did not end it, so it was killed.

### Step 3: 3a

```sh
touch "$RUN/before-3a"
cd "$RUN/cwd" && omp --plugin-dir "$RUN/fixture/prose-discipline" --model haiku
```

`expect` typed `Reply with the single word ok.`, `/dump`, `Reply with the single word again.`, `/dump` and `/exit`. The model replied `ok`, then `again`. The TUI printed `omp-llm-request-158db106890a3aac.json` after the first `/dump`.

The brief's loop printed:

```
== /var/folders/3s/wqmf9fc17fq54yt52m1wvqvh0000gn/T/omp-llm-request-158db106890a3aac.json
generic-rules=1 new-marker=1 house-style=1
== /var/folders/3s/wqmf9fc17fq54yt52m1wvqvh0000gn/T/omp-llm-request-158db129b1ca3aad.json
generic-rules=1 new-marker=1 house-style=1
```

`grep -c` counts matching lines, not occurrences, so `1` means the text is present.

The `systemPrompt` text was read with `jq`. The two sidecars have identical system prompts. The deciding lines, numbered in that text:

```
40:<skills>
50:- house-style: Apply this plugin's engineering prose standard to anything an agent writes, from replies and code comments to commit messages and error messages. Use when writing or reviewing replies, docs, code comments, review comments, commit messages, change descriptions, error messages or agent instructions. Also use when asked to check, clean up, shorten or de-slop text.
83:</skills>
84:<generic-rules>
85:# Prose discipline: core rules
87:The user installed the prose-discipline plugin, so this standard governs
149:</generic-rules>
```

The second sidecar's `messages` roles are `user`, `assistant`, `user`, `assistant`. So the second request also carried the rules.

Startup warnings, from the TUI log and `~/.omp/logs/omp.2026-09-25.49345.log`:

- `grep -i -c -E 'collision|unexpected frontmatter'` over the log printed `0`.
- `grep -i -c -E 'collision|frontmatter|warn'` over the TUI log, escapes stripped, printed `0`.
- The log's only `warn` entries are `model discovery failed for provider` (ollama, llama.cpp, lm-studio) and `ui.loop-blocked`.

### Step 4: 3b

```sh
omp plugin install prose-discipline@ai-plugins
```

```
✔ Installed prose-discipline from ai-plugins (1.3.0)
```

The marketplace cache held `Akurganow/ai-plugins` at `232aaba`, with `rules/prose-discipline.md` starting `alwaysApply: true`.

```sh
touch "$RUN/before-3b" && cd "$RUN/cwd" && omp --model haiku
```

`expect` typed `Reply with the single word ok.`, `/dump` and `/exit`. The model replied `ok`. The brief's loop printed:

```
== /var/folders/3s/wqmf9fc17fq54yt52m1wvqvh0000gn/T/omp-llm-request-158db195440d3ee8.json
generic-rules=1 old-marker=1 skill=1
```

The deciding lines of its `systemPrompt`:

```
40:<skills>
50:- prose-discipline: The prose standard for all agent-written output: user replies, prose, code comments, review comments, commit messages, change descriptions, error messages, and instructions. Use when writing or reviewing any of these, or when asked to apply or check the standard.
83:</skills>
85:<generic-rules>
86:# Prose discipline: core rules
88:This standard is mandatory in every session, without exceptions.
142:</generic-rules>
```

`~/.omp/logs/omp.2026-09-25.49704.log` has `0` lines matching `collision|frontmatter`. Its `warn` entries are the same two kinds as in 3a.

### Step 5: restore

```sh
omp plugin uninstall prose-discipline@ai-plugins
jq -r '.plugins | keys[]' ~/.omp/plugins/installed_plugins.json | diff "$RUN/installed-before.txt" - && echo restored
rm -f $(find "${TMPDIR:-/tmp}" -maxdepth 1 -name 'omp-llm-request-*.json' -newer "$RUN/before-3a")
git status --porcelain
```

```
✔ Uninstalled prose-discipline@ai-plugins
restored
```

`rm` removed the three sidecars named above; a second `find` counted `0`. `git status --porcelain` printed nothing.

`diff` of `jq -S` over `installed_plugins.json`, before and after, printed nothing.

## State left on the owner's machine

Installed plugins match the state found. Other changes, from `shasum` over `~/.omp` before and after, `logs` excluded:

- The probe start logged `[marketplace] cloning` for both marketplaces; the two later starts logged none. `marketplaces.json` now has `updatedAt` `2026-09-25T17:10:04.385Z` and `2026-09-25T17:10:05.284Z`.
- Oh-My-Pi wrote two session transcripts under `~/.omp/agent/sessions/--private-tmp-claude-501--…-scratchpad-spike3-cwd--/`.
- It updated `agent.db`, `history.db` and `models.db`, and wrote `agent/cache/composer/32eaa851b860aee4/` and `agent/terminal-sessions/ttys001`, `ttys003`, `ttys004`.
- It wrote three logs: `~/.omp/logs/omp.2026-09-25.49098.log`, `49345.log` and `49704.log`.
- The killed probe left `~/.omp/run/daemons/1ebf7b0855b44bb0/clients/49098-….json`. It was removed after pid 49098 ended; the empty directory remains.
- The TUI `/dump` copied the 3b transcript text to the clipboard. `pbpaste` starts with `## System Prompt`.

No setting was changed.

## Consequence for plan 03

None. All four assertions passed, so Task 8's Oh-My-Pi section can rest on them.
