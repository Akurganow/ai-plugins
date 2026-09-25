# Spike 5: headless marketplace add and install

Two parts. The local part ran on the owner's machine on 2026-09-25, at tree `07a8938`.
It used Hermes 0.21.5, Claude Code 2.1.282 and Codex 0.155.1, with Codex in its own `CODEX_HOME`.
It asks how commands behave, not whether they need a login.
The clean part is the first run of `integration.yml` on the pull request.

Every command ran with stdin from `/dev/null`, so no command could wait on a prompt.
No command asked for input, a login or a model.

## Local: Hermes validators on a portable package

| Package | `validate` exit | `doctor --ci` exit | Failing checks, verbatim |
| :-- | :-- | :-- | :-- |
| cognitive-load | 0 | 0 | none |
| design-review | 0 | 0 | none |
| howp | 0 | 0 | none; `validate` warns `⚠ security scan caution: path_traversal_deep (install.md:23)` |
| prose-discipline | 0 | 0 | none |
| toc-thinking | 0 | 0 | none |
| triz | 0 | 0 | none |

`validate` printed `Validation passed.` for every package, after these checks:

```
✓ portable manifest — plugin.json parses (Agent Plugins v1)
✓ manifest fields — name present
✓ security scan — safe
```

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
`codex plugin list --json` then showed `hook-control@hook-control` installed and enabled.
The installed copy held `hooks/hooks.json`.

`codex --dangerously-bypass-hook-trust debug prompt-input` exit 0; `HOOK-CONTROL-MARKER` count 0.
Without the flag, the command also exited 0; its output differed only in timestamps and ids.

A second control added `touch "$RUN/hook-ran"` to the hook command, in a fresh `CODEX_HOME`.
It printed `marker count: 0` and `side effect: hook-ran absent`, so the hook never ran.

Verdict: runs none. `codex debug prompt-input` runs no SessionStart hook.
