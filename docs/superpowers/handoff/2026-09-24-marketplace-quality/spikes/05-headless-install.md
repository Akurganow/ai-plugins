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

## Clean: first pull-request run

Run: https://github.com/Akurganow/ai-plugins/actions/runs/36178689054, at `a94e003bf3aeb42937f4f72fa245efe8f9dce35a`.
Pinned clients in this run: Claude Code 2.1.278, Codex 0.155.1, Oh-My-Pi 18.2.8, and Hermes v0.21.5 at `f97608f`.
Hosted runners; neither workflow referenced a secret (Task 7 Step 1).
Every quoted line is from a run log (kind: running), cited by run id and job name. The step name follows where it matters.

| OS | Client | Command | Exit | Decisive line | Verdict |
| :-- | :-- | :-- | :-- | :-- | :-- |
| ubuntu | claude | `claude plugin marketplace add ./`, `claude plugin install triz@ai-plugins` | 0 | `Adding marketplace…✔ Successfully added marketplace: ai-plugins (declared in user settings)`; `Installing plugin "triz@ai-plugins"...✔ Successfully installed plugin: triz@ai-plugins (scope: user)` | no authentication |
| macos | claude | same | 0 | same two lines | no authentication |
| windows | claude | same | 0 | same two lines | no authentication |
| ubuntu | codex | `codex plugin marketplace add ./`, `codex plugin add triz@ai-plugins` | 0 | ``Added plugin `triz` from marketplace `ai-plugins`.`` | no authentication |
| macos | codex | same | 0 | same line | no authentication |
| windows | codex | same | 0 | same line | no authentication |
| ubuntu | omp | `omp plugin marketplace add ./`, `omp plugin install triz@ai-plugins` | 0 | `✔ Added marketplace: ./`; `✔ Installed triz from ai-plugins (0.1.0)` | no authentication |
| macos | omp | same | 0 | same two lines | no authentication |
| windows | omp | same | 0 | same two lines | no authentication |
| ubuntu | hermes | `install.sh --commit f97608f…`, `hermes --version` | 0 | `│              ✓ Installation Complete!                   │`; `Hermes Agent v0.21.5 (2026.9.24) · upstream 1b57acf9 · local f97608f1 (+41514 carried commits)` | no authentication |
| ubuntu | hermes | `hermes plugins show triz` | 0 | `Status: enabled`, `Key: triz`, `Emits: (none)`, `Listens: (none)`; no skill; `##[error]hermes does not list skill ariz of triz` | client gap (see below) |
| macos | hermes | `install.sh --commit f97608f…`, `hermes --version` | 0 | `│              ✓ Installation Complete!                   │`; `Hermes Agent v0.21.5 (2026.9.24) · upstream 1b57acf9 · local f97608f1 (+41514 carried commits)` | no authentication |
| macos | hermes | `hermes plugins show triz` | 0 | the same four lines; no skill; `##[error]hermes does not list skill ariz of triz` | client gap (see below) |
| windows | hermes | `install.ps1 -Commit … -SkipSetup -HermesHome …` | 0 | `\|              [OK] Installation Complete!                \|` | no authentication |
| windows | hermes | `hermes --version \| tee /dev/stderr \| grep -qF 'v0.21.5'` | 1 | `tee: /dev/stderr: No such file or directory` | workflow defect |

In this run, `install (ubuntu-latest, hermes)` and `install (macos-latest, hermes)` also printed `hermes lists howp:howp` and `hermes lists triz:contradiction`.
Both passes were vacuous: `grep -F` matched the package name and the description's "the contradiction matrix".
The claude, codex and omp cells printed only `claude lists triz:contradiction` and similar lines, because the passing branch discarded the output.
Run 36180544459 (at `07a4e73`) matched each client's own line for the skill and printed the output. Every claude, codex and omp cell on all three OSes listed all seven skills:

- Claude Code, `install (ubuntu-latest, claude)` and the macos and windows jobs: `  Skills (2)  ariz, contradiction` under `Component inventory`.
- Codex, `install (ubuntu-latest, codex)` and the macos and windows jobs: `\n- triz:contradiction: Resolve an …` in the `codex debug prompt-input` JSON.
- Oh-My-Pi, `install (ubuntu-latest, omp)` and the macos and windows jobs: `name: contradiction` from `omp read "skill://contradiction:raw"`.

The howp archive, run 36178689054:
- `howp-archive (ubuntu-latest)`: `howp-0.3.6-x86_64-unknown-linux-musl.tar.gz: OK`, then `hp 0.3.6`.
- `howp-archive (macos-latest)`: `howp-0.3.6-aarch64-apple-darwin.tar.gz: OK`, then `hp 0.3.6`.
- `howp-archive (windows-latest)`: `binaries.json names no target for MINGW64_NT-10.0-26100/x86_64, so the skill refuses this platform.`

The Codex hook step, every codex job of run 36178689054: `##[notice]Hook check not run - codex debug prompt-input ran no plugin SessionStart hook in the spike, and no model-free route exists.`
From `e9875ac` on, the notice reads `##[notice]Hook check not run - Codex 0.155.1 lists plugin_hooks as removed, and no model-free route to the hook exists.`
Its ground is the local part above: `plugin_hooks                             removed            false`.

Every job warned, 16 times in run 36178689054: `##[warning]Node.js 20 is deprecated. The following actions target Node.js 20 but are being forced to run on Node.js 24: actions/checkout@11d5960a326750d5838078e36cf38b85af677262.`
The pin stays; plan 02 owns it.

Run 36180420083 (at `6b784d6`) showed one transient failure, in `install (windows-latest, hermes)`, step `Install the client (Hermes on Windows)`.
`irm` of `install.ps1` from raw.githubusercontent.com printed `429: This request was rate-limited due to too many requests from your network.`
The next run installed with no change. It may recur, because the installer is fetched without authentication.

### Windows Hermes: installs, then fails, dropped under O4

Kind: running, for every line below.
In `install (windows-latest, hermes)`, the installer succeeded in run 36180544459 (at `07a4e73`) and in run 36182597972 (at `3f00b7a`).
Both runs printed `|              [OK] Installation Complete!                |`.
In run 36183358181 (at `0f89614`), step `Install the client (Hermes on Windows)` failed twice.
Attempt 1 printed `429: This request was rate-limited due to too many requests from your network.`
Attempt 2 downloaded `install.ps1`, cloned upstream (`Cloning into 'D:\a\_temp/hermes-home\hermes-agent'...`), then printed:

```
-> Pinning to commit f97608f178d1ffeca59860195ab7da295f7c8e5f...
From https://github.com/NousResearch/hermes-agent
 * branch                  f97608f178d1ffeca59860195ab7da295f7c8e5f -> FETCH_HEAD
error: Your local changes to the following files would be overwritten by checkout:
	website/i18n/zh-Hans/docusaurus-plugin-content-docs/current/index.mdx
Please commit your changes or stash them before you switch branches.
Aborting

[X] Installation failed: git checkout f97608f178d1ffeca59860195ab7da295f7c8e5f failed (exit 1)
```

`install.ps1` clones upstream main before checking out the pinned commit, so the result depends on upstream at run time.
Kind: source, [`scripts/install.ps1` L20–L24](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/scripts/install.ps1#L20-L24).
Verdict: Hermes cannot install on Windows. The cell is dropped under O4 by a matrix `exclude` that quotes these lines.

### Hermes lists no portable package's skills

"Client gap" is not one of the brief's five verdicts. It records the owner's decision of 2026-09-25 to drop the Hermes skill assertion.

`hermes plugins show <name>` prints name, version, description, `Status:`, `Source:`, `Key:`, `Emits:` and `Listens:`, and nothing else.
Kind: running, in the run above. Source agrees: [`plugins_cmd.py` L1814–L1836](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L1814-L1836).
`hermes plugins list --json` carries only `name`, `status`, `version`, `description`, `source` and `removed`. Kind: source, [`plugins_cmd.py` L1672–L1703](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_cmd.py#L1672-L1703).
`hermes skills list` is documented only as "List installed skills." Kind: documentation, [`cli-commands.md` L1396](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/website/docs/reference/cli-commands.md#L1396).
It printed `0 hub-installed, 0 builtin, 0 local — 0 enabled, 0 disabled` with triz and howp enabled. Kind: running, local Hermes 0.21.5 at `d350422b`, in its own `HERMES_HOME`.
Its `do_list` reads skill directories only. Kind: source, [`skills_hub.py` L782–L828](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/skills_hub.py#L782-L828).
The documentation names the model-facing tool as the route: "Use `skills_list` to discover the full qualified skill name". Kind: documentation, [`developer-guide/plugins/index.md` L70–L78](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/website/docs/developer-guide/plugins/index.md#L70-L78).
That tool returns `agent-plugin-<slug>-<sha256[:8]>:<skill>`. Kind: source, [`plugins_manifest.py` L60–L64](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/hermes_cli/plugins_manifest.py#L60-L64) for the namespace and [`skills_tool.py` L234–L259](https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/tools/skills_tool.py#L234-L259).
Called in-process with no model, it printed `agent-plugin-triz-3db6c5da:ariz`. Kind: running, local, as above. No CLI subcommand calls it.

## Fixes

| Commit | Verdict | What changed |
| :-- | :-- | :-- |
| `6b784d6` | workflow defect: `tee: /dev/stderr: No such file or directory` on windows-latest | The Hermes version check keeps the output in a variable, prints it, and greps it through a here-string. |
| `07a4e73` | workflow defect: vacuous `hermes lists triz:contradiction`, and passing output discarded | Each client matches its own skill line. A passing pair prints its output in a group. `packages` sets `nullglob`, and `grep -q` reads a here-string instead of a pipe. |
| `3f00b7a` | client gap: no Hermes command prints a portable package's skills without a model call | By the owner's decision, the Hermes cells assert `Key: <name>` and `Status: enabled` from `hermes plugins show <name>`, not the skills. |
| `c787e37` | Hermes cannot install on Windows: `[X] Installation failed: git checkout f97608f178d1ffeca59860195ab7da295f7c8e5f failed (exit 1)` | The `install` matrix excludes `windows-latest` × `hermes` (O4). |

Run 36182597972 (at `3f00b7a`): every job `success`.
All three Hermes jobs, for example `install (windows-latest, hermes)`, printed `##[group]hermes has triz installed and enabled`, then `Key: triz` and `Status: enabled`.
Run 36182597974 (conformance, same commit): `check`, `validate-claude`, `validate-skills` and `validate-hermes` all `success`.
After the exclude, at `344db4d`: integration run 36184574245 finished 15 of 15 jobs `success`, and conformance run 36184574204 finished 4 of 4.

## Decisions for the workflows

- Claude Code: auth none; list command `claude plugin details <n>@ai-plugins`.
- Codex: auth none; list command `codex debug prompt-input`; hook step reported as not run, because Codex 0.155.1 lists `plugin_hooks` as removed.
- Oh-My-Pi: auth none; list command `omp read skill://<s>:raw`.
- Hermes: auth none; Windows: cell dropped under O4. The first failure was the workflow's `tee`, not the installer. Later the installer's pinned checkout failed in run 36183358181. List command: none exists. Decision: install and enable are checked with `hermes plugins show <n>`, skills are not asserted, and `hermes plugins validate` runs in `conformance.yml`.
