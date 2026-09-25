# Spike 5: headless marketplace add and install

Two parts. The local part ran on the owner's machine on 2026-09-25, at tree `07a8938`.
It used Hermes 0.21.5, Claude Code 2.1.282 and Codex 0.155.1, with Codex in its own `CODEX_HOME`.
`CODEX_HOME` did not isolate the user skill root: `codex debug prompt-input` listed `~/.agents/skills` as skill root `r0`.
The local part asks how commands behave, not whether they need a login.
Every quoted line below is output from the clients' own code, from `find`, or from the probe's own `echo` lines. The two verdicts read that output.
The clean part is the first run of `integration.yml` on the pull request.

Every client command in the brief's two steps, the probe and the evidence re-runs ran with stdin from `/dev/null`.
No command asked for input or a login.

## Local: Hermes validators on a portable package

| Package | `validate` exit | `doctor --ci` exit | Failing checks, verbatim |
| :-- | :-- | :-- | :-- |
| cognitive-load | 0 | 0 | none |
| design-review | 0 | 0 | none |
| howp | 0 | 0 | none; `validate` warns `⚠ security scan caution: path_traversal_deep (install.md:23)` |
| prose-discipline | 0 | 0 | none |
| toc-thinking | 0 | 0 | none |
| triz | 0 | 0 | none |

`validate` printed `Validation passed.` for every package.
For five packages, these three checks preceded it:

```
✓ portable manifest — plugin.json parses (Agent Plugins v1)
✓ manifest fields — name present
✓ security scan — safe
```

For howp, the third check read `✓ security scan — caution`, followed by `⚠ security scan caution: path_traversal_deep (install.md:23)`.

`doctor --ci` printed this line for every package:

```
  OK: runtime discovery, manifest parsing, import, and registration passed
```

Verdict: both pass. Neither command fails on a portable package by design.

`claude plugin validate` exited 0 on every package, with one warning each:

```
  ❯ extensions: Unknown field 'extensions'. Claude Code ignores it at load time.

✔ Validation passed with warnings
```

## Local: Codex hook control

`codex plugin marketplace add` and `codex plugin add` both exited 0.
In the first control's `CODEX_HOME`, `codex plugin list --json` printed these adjacent lines:

```
      "pluginId": "hook-control@hook-control",
      "name": "hook-control",
      "marketplaceName": "hook-control",
      "version": "0.0.1",
      "installed": true,
      "enabled": true,
```

`find plugins/cache -type f`, run inside the first control's `CODEX_HOME`, printed this line among two:

```
plugins/cache/hook-control/hook-control/0.0.1/hooks/hooks.json
```

`codex --dangerously-bypass-hook-trust debug prompt-input` exit 0; `HOOK-CONTROL-MARKER` count 0.
Without the flag, the command also exited 0; after stripping ids, `diff` showed only `create_time` lines.

A second control, beyond the brief, added `touch "$RUN/hook-ran"` to the hook command, in a fresh `CODEX_HOME`.
Both installs exited 0.
It then printed `marker count: 0` and `side effect: hook-ran absent`, so the hook never ran.

`codex features list`, run in the first control's `CODEX_HOME`, printed this line among its flags:

```
plugin_hooks                             removed            false
```

Verdict: runs none of the control's plugin hooks. `codex debug prompt-input` runs no plugin SessionStart hook (the control's).
The control cannot tell `debug prompt-input` skipping hooks apart from Codex 0.155.1 loading no plugin hooks at all.
