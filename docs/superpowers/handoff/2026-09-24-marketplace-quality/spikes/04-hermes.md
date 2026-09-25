# Spike 4: Hermes

Run on 2026-09-25 with `Hermes Agent v0.21.5 (2026.9.24) · upstream d350422b`, fixture built from plan 03 blocks A–F at commit `c3b88b9`.

The fixture and every run file sat outside the repository, under a per-run scratch directory called `$RUN` below. `$CFG` is `/Users/akurganow/.hermes/config.yaml`.

Every fact below comes from running the client. Both model runs used `-m deepseek/deepseek-v4-pro` on the configured provider `openrouter`. OpenRouter's `/api/v1/models` listed it at $0.70 input and $1.41 output per million tokens that day. The two configured Gemini Flash models listed at $0.75 and $3.75. The configured `qwen/qwen3.8-max` had no exact entry, and every `qwen3.8-max` variant listed higher.

## Assertions

| Id | Assertion | Result | Evidence |
| :-- | :-- | :-- | :-- |
| 4-install | the portable package installs flat from a Git URL, enabled, with `skills/house-style` | pass | `hermes plugins install "file://$RUN/pkg" --force --enable` exited `0`. The list showed `prose-discipline │ enabled │ 1.3.0`, and `ls` printed `house-style`. |
| 4a | `skill_view` loads the skill by its qualified name `agent-plugin-prose-discipline-cf518319:house-style` | pass | The tool result starts `{"success": true, "name": "agent-plugin-prose-discipline-cf518319:house-style"`. The marker count printed `1` and the `Bundle context` count printed `1`. |
| 4b | `skills.auto_load` puts the skill, with Hermes's wrapper, into the system prompt | pass | The wrapper count printed `1`, the marker count `1`, the `# House style` count `1`. The log check printed `no auto_load log line`. |
| 4c | Hermes on Windows | not run | This machine runs macOS. The Windows × Hermes job of plan 07's integration matrix covers it. |

## Commands and output

### Step 1: versions and backup

```sh
hermes --version
hermes plugins list | grep -A1 'prose-discipline'
CFG=$(hermes config path); echo "$CFG"; cp "$CFG" "$RUN/config.yaml.bak"
hermes config get skills.auto_load
printf %s prose-discipline | shasum -a 256 | cut -c1-8
```

```
Hermes Agent v0.21.5 (2026.9.24) · upstream d350422b
│ prose-discipline     │ enabled     │ 1.3.0   │ Engineering prose   │ user    │
/Users/akurganow/.hermes/config.yaml
[]
cf518319
```

The installed 1.3.0 package came from `https://github.com/Akurganow/ai-plugins.git#plugins/prose-discipline` at revision `232aabaa`. Its directory and `.install-metadata.json` were copied to `$RUN` before Step 3.

### Step 2: fixture and validator

Blocks A, B, C, D and F were extracted from the plan file, then the recipe ran.

```
fixture-syntax-ok
# Prose discipline: core rules
1
```

`diff -r` against the spike 1 fixture printed nothing. The fixture became a Git repository with one commit, `69f4070 fixture`.

```sh
hermes plugins validate "$RUN/pkg"; echo "exit=$?"
```

```
✓ portable manifest — plugin.json parses (Agent Plugins v1)
✓ manifest fields — name present
✓ security scan — safe

Validation passed.
exit=0
```

### Step 3: 4-install

```sh
hermes plugins install "file://$RUN/pkg" --force --enable; echo "exit=$?"
hermes plugins list | grep -A1 'prose-discipline'
ls ~/.hermes/plugins/prose-discipline/skills
```

```
Warning: custom (unreviewed) source — not from the Hermes catalog.
Warning: Using insecure/local URL scheme. Consider using https:// or git@ for
production installs.
Location: /Users/akurganow/.hermes/plugins/prose-discipline
✓ Plugin prose-discipline enabled.
Live in open chats now: 0 MCP tools, 1 skills.
exit=0
│ prose-discipline     │ enabled     │ 1.3.0   │ An engineering      │ git     │
house-style
```

Hermes accepted the `file://` URL, so the copy route did not run.

### Step 4: 4a

```sh
hermes chat -q 'Call skill_view with the name "agent-plugin-prose-discipline-cf518319:house-style" and reply with the first heading of its content.' --oneshot -Q -m deepseek/deepseek-v4-pro
```

```
session_id: 20260925_192134_f944bc
# House style
```

The session's assistant message called `skill_view` with `{"name": "agent-plugin-prose-discipline-cf518319:house-style"}`. The start of the tool result, from `$RUN/4a-tool.txt`:

```
{"success": true, "name": "agent-plugin-prose-discipline-cf518319:house-style", "content": "[Bundle context: This skill is part of the 'agent-plugin-prose-discipline-cf518319' plugin.]\n\n---\nname: house-style\n
```

The brief's two `grep -c` lines printed:

```
1
1
```

`skills_list` did not run, because `skill_view` found the skill.

### Step 5: 4b

```sh
hermes config set skills.auto_load '["agent-plugin-prose-discipline-cf518319:house-style"]'
hermes config get skills.auto_load
```

```
✓ Set skills.auto_load = ['agent-plugin-prose-discipline-cf518319:house-style'] in /Users/akurganow/.hermes/config.yaml
- agent-plugin-prose-discipline-cf518319:house-style
```

It printed a list, so the hand edit did not run.

```sh
hermes chat -q 'Reply with the single word ok.' --oneshot -Q -m deepseek/deepseek-v4-pro
```

```
session_id: 20260925_192205_f17d56
ok
```

The brief's three counts and log check printed:

```
1
1
1
no auto_load log line
```

The deciding lines of `$RUN/4b-system.txt`, numbered:

```
90:[IMPORTANT: The "agent-plugin-prose-discipline-cf518319:house-style" skill is auto-loaded via config (skills.auto_load). Treat its instructions as active guidance for the duration of this session unless the user overrides them.]
92:[Bundle context: This skill is part of the 'agent-plugin-prose-discipline-cf518319' plugin.]
106:# House style
117:<!-- rules:start -->
118:# Prose discipline: core rules
120:The user installed the prose-discipline plugin, so this standard governs
182:<!-- rules:end -->
```

The agent log grew by 62 lines during the run. Each of the two sessions also logged `Auxiliary title_generation: using openrouter (deepseek/deepseek-v4-pro)`.

### Step 6: 4c

Not run: this machine runs macOS.

### Step 7: restore

```sh
cp "$RUN/config.yaml.bak" "$CFG"
hermes config set skills.auto_load '["agent-plugin-prose-discipline-cf518319:house-style"]'
hermes config get skills.auto_load
diff "$RUN/config.yaml.bak" "$CFG"
hermes plugins install Akurganow/ai-plugins/plugins/prose-discipline --force --enable
hermes plugins list | grep -A1 'prose-discipline'
git status --porcelain
```

```
✓ Set skills.auto_load = ['agent-plugin-prose-discipline-cf518319:house-style'] in /Users/akurganow/.hermes/config.yaml
- agent-plugin-prose-discipline-cf518319:house-style
426a427,428
>   auto_load:
>     - agent-plugin-prose-discipline-cf518319:house-style
Cloning https://github.com/Akurganow/ai-plugins.git (subdir:
plugins/prose-discipline)...
✓ Plugin prose-discipline enabled.
│ prose-discipline     │ enabled     │ 1.3.0   │ Engineering prose   │ user    │
```

`git status --porcelain` printed nothing. `diff -r` of the plugin directory against its Step 1 copy printed nothing. `diff` of `.install-metadata.json` against its copy printed nothing.

## State left on the owner's machine

The owner keeps one change: the `skills.auto_load` entry. `hermes config get skills.auto_load` prints:

```
- agent-plugin-prose-discipline-cf518319:house-style
```

`diff "$RUN/config.yaml.bak" "$CFG"` prints only the two added lines:

```
426a427,428
>   auto_load:
>     - agent-plugin-prose-discipline-cf518319:house-style
```

The published 1.3.0 ships its skill as `prose-discipline`, so the entry names no installed skill. Hermes skips a missing name and logs `skills.auto_load: skill(s) not found or disabled, skipped: …`. That warning is from `agent/system_prompt.py` line 334 and `cli.py` line 1028 at `d350422b`. It was not observed here, because that needs one more model call. It lasts until a release ships `house-style`.

`prose-discipline` 1.3.0 is installed and enabled from `Akurganow/ai-plugins`, as found. The two spike sessions stay in `~/.hermes/state.db`, and the agent log keeps their lines.

## Consequence for plan 03

None. All three assertions that ran passed, so Task 5's Hermes lines and Task 8's Hermes section can rest on them.
