# Spike 1: Claude Code

Run on 2026-09-25 with Claude Code `2.1.278 (Claude Code)`, fixture built from plan 03 blocks A–F at commit `8bd2d49`.

The fixture and every run directory sat outside the repository, under a per-run scratch directory called `$RUN` below. All model runs used `--model haiku`, which answered as `claude-haiku-4-5-20251001`.

## Assertions

| Id | Assertion | Result | Evidence |
| :-- | :-- | :-- | :-- |
| 1v | `claude plugin validate` accepts the fixture | pass | `exit=0`. One warning, about `extensions`. No line names `hooks.json`. |
| 1a | SessionStart plain stdout reaches the context | pass | Decided by the reply: the model quoted `# Prose discipline: core rules` with no tool call. Transcript lines support it. |
| 1b | the rules return after `/compact` | not run | The interactive session stopped at the folder trust dialog. Accepting it writes the owner's `~/.claude.json`, so the run stopped. |
| 1c | SubagentStart delivers `additionalContext` to a subagent | pass | Decided by the subagent's own reply, `# Prose discipline: core rules`. Its transcript holds the rules in `hook_additional_context`. |

No run showed 1a-injection: neither reply quoted the rules beyond the heading, warned about them, or asked about them.

## Commands and output

### Step 1: versions

```sh
claude --version
claude plugin list | grep -n 'prose-discipline' || echo 'prose-discipline: not installed in the CLI'
```

```
2.1.278 (Claude Code)
prose-discipline: not installed in the CLI
```

### Step 2: fixture

Blocks A, B, C, D and F were copied by line range from the plan file, then the recipe ran.

```
fixture-syntax-ok
# Prose discipline: core rules
1
```

`wc -c` of `rules/prose-discipline.md` printed `4942`.

### Step 3: 1v

```sh
claude plugin validate "$RUN/fixture/prose-discipline"; echo "exit=$?"
```

```
Validating plugin manifest: $RUN/fixture/prose-discipline/.claude-plugin/plugin.json

⚠ Found 1 warning:

  ❯ extensions: Unknown field 'extensions'. Claude Code ignores it at load time.

✔ Validation passed with warnings
exit=0
```

The validator named only the manifest. It printed no line about `hooks.json`.

### Step 4: 1a

The brief's prompt `Reply with the single word ok.` was replaced by the quote question. The coordinator ruled that the reply decides 1a, because transcript markers exist whenever the hook ran.

```sh
cd "$RUN/cwd"
claude --plugin-dir "$RUN/fixture/prose-discipline" --model haiku --max-turns 2 \
  -p 'Quote the first heading of the prose rules in your context, verbatim, or reply NONE.' --output-format json > "$RUN/startup.json"
```

Session `43598692-7664-4030-9c78-2044555e4f70`. The brief's `jq` over its transcript printed:

```
{"type":"hook_success","hookName":"SessionStart:startup","command":"sh \"${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh\"","exitCode":0,"stderr":""}
{"type":"hook_success","hookName":"SessionStart:startup","command":"\"${CLAUDE_PLUGIN_ROOT}/hooks/run-hook.cmd\" session-start","exitCode":0,"stderr":""}
{"type":"hook_additional_context","hookName":"SessionStart","command":null,"exitCode":null,"stderr":null}
```

Marker count: `1`. Result:

```
# Prose discipline: core rules
```

`startup.json` also reported `"is_error":false`, `"num_turns":1` and `"terminal_reason":"completed"`. The assistant turn held only `thinking` and `text` blocks, so no tool read the rules.

Supporting transcript facts, read with `jq` and `grep -n`:

- The marker sits on line 3 only, the `print-rules.sh` `hook_success` object. Its `stdout` and `content` fields hold the rules text.
- The one `hook_additional_context` object has a 1-element `content` array. That element is the superpowers plugin's text (`run-hook.cmd`), not the rules.
- So Claude Code 2.1.278 stores plain SessionStart stdout as `hook_success.content`, and the model received it.

The second `hook_success` line comes from the owner's installed superpowers plugin. The brief's condition "a `hook_additional_context` object is listed" held only because of it.

### Step 5: 1b

```sh
touch "$RUN/before-compact"
cd "$RUN/cwd" && expect "$RUN/step5.exp"
```

`step5.exp` spawned `claude --plugin-dir "$RUN/fixture/prose-discipline" --model haiku --resume 43598692-7664-4030-9c78-2044555e4f70`. It was to type `/compact`, the quote question and `/exit`. The session log, with terminal escapes stripped, showed:

```
Accessingworkspace:
…/scratchpad/spike1/cwd
Quicksafetycheck:Isthisaprojectyoucreatedoroneyoutrust?(Likeyour
owncode,awell-knownopensourceproject,orworkfromyourteam).Ifnot,
takeamomenttoreviewwhat'sinthisfolderfirst.
ClaudeCode'llbeabletoread,edit,andexecutefileshere.
Securityguide
❯No,exit
Yes,Itrustthisfolder
Entertoconfirm·Esctocancel
```

```
STEP5: no input prompt within 60s
expect exit=3
```

The script typed nothing into the dialog, and the process ended at the timeout. `/compact` never ran. No new transcript for this session appeared under `find ~/.claude/projects -newer "$RUN/before-compact"`.

### Step 6: 1c

```sh
cd "$RUN/cwd"
claude --plugin-dir "$RUN/fixture/prose-discipline" --model haiku --max-turns 4 --allowedTools Agent \
  -p "Use the Agent tool once to start a general-purpose subagent with this task: 'Quote the first heading of the prose rules in your context, verbatim, or reply NONE.' Then repeat the subagent's reply verbatim." \
  --output-format json > "$RUN/subagent.json"
```

Session `c500be30-d30e-48ac-a2e1-5e2424e78925`. The brief's `jq` printed:

```
{"type":"hook_success","hookName":"SubagentStart:general-purpose","command":"sh \"${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh\" --json","exitCode":0,"stderr":""}
{"type":"hook_additional_context","hookName":"SubagentStart","command":null,"exitCode":null,"stderr":null}
```

`grep -l` listed `c500be30-d30e-48ac-a2e1-5e2424e78925/subagents/agent-aee077d21917bc961.jsonl`. Result: `# Prose discipline: core rules`.

The main session also had the rules from SessionStart, so its result alone cannot decide 1c. The subagent's transcript decides it:

- Its first lines are the task, then `hook_success` `SubagentStart:general-purpose`, then `hook_additional_context` `SubagentStart`.
- That `hook_additional_context` `content` array has 1 element, starting `# Prose discipline: core rules\n\nThe user installed the prose-discipline plugin,`.
- Its assistant text, at `2026-09-25T17:05:58.773Z`, is `# Prose discipline: core rules`.

The Agent tool ran the subagent in the background. The main session repeated the reply at `17:06:00.176Z`, after the task notification at `17:05:58.849Z`.

### Step 7: tree

```sh
git status --porcelain
```

It printed nothing before this record was written.

## State left on the owner's machine

- Claude Code wrote transcripts for sessions `43598692`, `c500be30`, `adbf630b` and `c52c913c` under `~/.claude/projects/-private-tmp-claude-501--…-scratchpad-spike1-cwd/`, and a `memory` directory there.
- `adbf630b` and `c52c913c` are two earlier Step 4 attempts that ended with `Not logged in · Please run /login` at zero cost.
- `grep -c spike1 ~/.claude.json` printed `0`: the trust dialog wrote no entry.
- No setting, installed plugin or credential was changed.

## Consequence for plan 03

1a and 1c need no change. Plain stdout serves SessionStart, and `--json` serves SubagentStart, as Blocks A and B have them.

1b is open. It needs the trust of `$RUN/cwd` accepted, which changes `~/.claude.json`, or Step 5 typed by the owner. The owner decides which, and Task 6 waits for 1b.

The brief's 1a and 1b transcript conditions hold whenever the hook runs. The coordinator ruled that the model's quoted heading decides both rows.
