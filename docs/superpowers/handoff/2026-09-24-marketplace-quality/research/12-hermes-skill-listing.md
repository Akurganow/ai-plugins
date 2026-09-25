# Hermes 0.21.5: does any CLI route print a portable package's skills?

Target: NousResearch/hermes-agent at `f97608f178d1ffeca59860195ab7da295f7c8e5f`. `git ls-remote` shows
`refs/tags/v2026.9.24^{}` resolves to that commit. Permalink base, written `P/` below:
`https://github.com/NousResearch/hermes-agent/blob/f97608f178d1ffeca59860195ab7da295f7c8e5f/`

## Answer

**No.** Hermes 0.21.5 has no command, documented or not, that prints the names of a portable
Agent Plugins package's skills without a model call. The only thing that enumerates them by name
is the model-facing tool `skills_list`, and no CLI subcommand calls it. `hermes plugins list
--json`, `plugins show`, `plugins validate --json`, `plugins doctor`, `skills list` and
`/skills list` never read the plugin-skill registry. `plugins enable` prints at most a count.

## 1. Documentation (read first)

Sources: raw.githubusercontent.com at the commit, saved under `docs/`.

| Fact | Source (documentation) |
| :-- | :-- |
| Portable skills are "read-only, namespaced, and loaded through `skills_list` plus `skill_view`". "Use `skills_list` to discover the full qualified skill name." The namespace form is `agent-plugin-<slug>-<hash>`. The page names no CLI route. | `P/website/docs/developer-guide/plugins/index.md#L70-L78` |
| Plugin skills are "**not** listed in the system prompt's `<available_skills>` index", so they are opt-in explicit loads. | `P/website/docs/developer-guide/plugins/index.md#L844-L847` |
| `hermes plugins doctor` validates "a native plugin". It reports tools and hooks, not skills. | `P/website/docs/developer-guide/plugins/index.md#L203-L217`; `P/website/docs/reference/cli-commands.md#L1639` |
| `plugins list`: "List installed plugins with enabled/disabled status". No skills field is documented. | `P/website/docs/reference/cli-commands.md#L1638` |
| The `hermes plugins` table in the CLI reference omits `show`, `validate`, `compat`, `capabilities` and `browse`. `validate` is mentioned only in passing. | `P/website/docs/reference/cli-commands.md#L1618-L1646`; `P/website/docs/user-guide/features/plugin-catalog.md#L75` |
| `hermes skills list`: "List installed skills". The only documented filter is `--source hub`. No plugin source is mentioned. | `P/website/docs/reference/cli-commands.md#L1396`; `P/website/docs/user-guide/features/skills.md#L684` |
| `skills.md` never mentions plugin-provided skills (its only "plugin" hits are an unrelated config example near L292). | `P/website/docs/user-guide/features/skills.md` (whole page grepped) |
| The user guide says bundled skills are "namespaced as `plugin:skill`, loaded via `skill_view(\"plugin:skill\")`". No listing command is given. | `P/website/docs/user-guide/features/plugins.md#L108` |
| `HERMES_PLUGINS_DEBUG=1 hermes plugins list` is documented to log "what `register(ctx)` registered (tools, hooks, slash commands, CLI commands)". Skills are not in that list. | `P/website/docs/developer-guide/plugins/index.md#L721-L736` |

The documentation has no route that prints plugin skills, so step 2 applies.

## 2. Source: every place that enumerates plugin skills

The registry is `PluginManager._plugin_skills`, keyed `"<namespace>:<skill>"`
(`P/hermes_cli/plugins.py#L993-L1022`). Four places read it:

| Reader | Reached from | Prints names on a CLI? |
| :-- | :-- | :-- |
| `list_plugin_skill_metadata()`, `P/hermes_cli/plugins.py#L1529-L1536` | Only `tools/skills_tool.py::skills_list`, `P/tools/skills_tool.py#L234-L259`. That is the model tool registered at `P/tools/skills_tool.py#L690`. | No. No CLI subcommand calls `skills_list`. A repo-wide grep finds no caller outside the tool registry and tests. |
| `list_plugin_skills(ns)`, `P/hermes_cli/plugins.py#L1524-L1527` | Called from `skill_view` (`P/tools/skills_tool.py#L300`) and `P/tools/skills_tool_plugin.py#L149`, both model tools. | No |
| `plugins_activation_live.plugin_skills(key)`, `P/hermes_cli/plugins_activation_live.py#L75-L83` | `_go_live`, `P/hermes_cli/plugins_activation.py#L140-L170`. That runs only when `activate_plugin_now(..., in_process=True)`. The names go to open chats as a turn note (`live_notice`, same file, L86-L110), not to stdout. | No, see below |
| `activation_hint`, `P/hermes_cli/plugins_activation.py#L205-L213` | `hermes plugins enable` (`P/hermes_cli/plugins_cmd.py#L1359-L1362`) and `install --enable` (`P/hermes_cli/plugins_cmd.py#L1000-L1003`). Both pass `in_process=False`, so skills appear only if a running `hermes serve`/Desktop backend answers (`P/hermes_cli/plugins_activation.py#L93-L108`). | **A count only**: `Live in open chats now: {N} MCP tools, {M} skills.` No names are printed. |

Commands that do **not** reach the registry:

- `hermes plugins list [--json]`, `P/hermes_cli/plugins_cmd.py#L1672-L1703`. It scans directories
  (`_discover_all_plugins`, L1613-L1629) and loads nothing. The JSON keys are exactly
  `("name", "status", "version", "description", "source", "removed")` (L1701).
- `hermes plugins show <name>`, `P/hermes_cli/plugins_cmd.py#L1814-L1836`. It prints name, `v<version>`,
  description, `Status:`, `Source:`, `Key:`, `Emits:` and `Listens:`, and nothing else. `plugins info`
  is dispatched to the catalog `cmd_info` instead (`P/hermes_cli/plugins_cmd.py#L2493-L2494`), which
  falls back to `cmd_show` for a non-catalog name (`P/hermes_cli/plugins_cmd_catalog.py#L468-L474`).
- `hermes plugins validate [--json] <dir>`, `P/hermes_cli/plugins_cmd_catalog.py#L503-L526`. It runs
  `ValidationReport.to_dict()`, whose keys are exactly `ok`, `checks[] {name, ok, detail}` and
  `warnings` (`P/hermes_cli/plugin_validate.py#L62-L70`). For a portable package,
  `_validate_portable_plugin` (`P/hermes_cli/plugin_validate.py#L587-L628`) loads the package, so
  `package.skills` is computed. It never reports `package.skills`, though: the checks are only
  `portable manifest`, `manifest fields`, `server availability: <server>`, the security scan and the
  desktop surface. A skill name appears only in `warnings`, as a diagnostic string
  `skill:<dir>: <error>`, and only when that skill was **rejected**
  (`P/hermes_cli/agent_plugins.py#L250-L251`, copied in at `plugin_validate.py#L606-L609`).
- `hermes plugins doctor [target]`, `P/hermes_cli/plugin_dev.py#L191-L204` and L335-L395. The
  output is `manifest: <name> <version> (<kind>)`, findings, and
  `registrations: N tool(s), N hook(s)`. It has no skills line.
- `hermes skills list [--source {all,hub,builtin,local}] [--enabled-only]`.
  `do_list` (`P/hermes_cli/skills_hub.py#L782-L828`) reads only `_find_all_skills()`
  (`P/tools/skills_tool.py#L184-L226`), which scans skill directories. The plugin merge happens
  only inside `skills_list` (L239-L248). The in-chat `/skills list` calls the same `do_list`
  (`P/hermes_cli/skills_hub.py#L1448`).
- The argument parsers define no `--plugins`, `--all` or `--skills` flag on any of these:
  `P/hermes_cli/subcommands/plugins.py#L54-L81` and `L152-L154`;
  `P/hermes_cli/subcommands/skills.py#L69-L73`.

An undocumented side channel exists; I read it in source and did not run it. With
`HERMES_PLUGINS_DEBUG=1`, a plugin load logs `Plugin %s registered skill: %s` at DEBUG level
(`P/hermes_cli/plugins.py#L340-L348` and L1021-L1022), and the stderr handler format is
`[plugins] %(levelname)s %(message)s` (L96-L100). The line would read
`[plugins] DEBUG Plugin <manifest-name> registered skill: agent-plugin-<slug>-<hash>:<skill>`.
`hermes plugins list` does not load plugins, though. Built-in subcommands skip discovery
(`P/hermes_cli/main.py#L2662-L2666`, `#L2940-L2941`), so the documented
`HERMES_PLUGINS_DEBUG=1 hermes plugins list` would not print it. Which model-free command would
load a portable package is not established here.

## 3. How a plugin skill name is printed on each route

| Route | Printed form |
| :-- | :-- |
| `skills_list` model tool (JSON) | `{"name": "agent-plugin-<slug>-<sha8>:<skill-dir>", "description": "...", "category": "plugin"}` (`P/hermes_cli/plugins.py#L1529-L1536`). Example: `agent-plugin-triz-3db6c5da:ariz`. `3db6c5da` is `sha256("triz")[:8]`, recomputed here. |
| `hermes plugins enable` / `install --enable` | `Live in open chats now: <N> MCP tools, <M> skills.`, a count with no names, printed only if a serve/Desktop backend answers. |
| Open-chat turn note (not stdout) | `- agent-plugin-<slug>-<sha8>:<skill>: <description>` under `Skills now available; load one with skill_view:` (`P/hermes_cli/plugins_activation_live.py#L99-L102`) |
| `plugins validate --json` | A name appears only for a rejected skill: `"skill:<dir>: <error>"` in `warnings` |
| Debug log (source only, not run) | `[plugins] DEBUG Plugin <name> registered skill: agent-plugin-<slug>-<sha8>:<skill>` |

The names can be derived offline, with no Hermes command:
- Namespace = `agent-plugin-` + slug(key) + `-` + `sha256(key)[:8]`. The slug is the key lowercased,
  with every character outside `[a-z0-9_-]` turned into `-` and `-`/`_` trimmed from the ends
  (`P/hermes_cli/plugins_manifest.py#L60-L69`).
- Key = the manifest `name` for a top-level install, or `<prefix>/<dir>` when nested
  (`P/hermes_cli/plugins_manifest.py#L461-L465`).
- Skill = the immediate `skills/<dir>` name (`P/hermes_cli/agent_plugins.py#L237-L256`).

## 4. Local `--help` output

Every command below ran with `HERMES_HOME=<scratch>/home`. The owner's Hermes home was not touched.

`hermes --version` prints `Hermes Agent v0.21.5 (2026.9.24) · upstream d350422b`, so the installed
tree is at `d350422b15863fc4c0b7962b122b625a0271516c`, **not** the tag commit. I compared every
relevant file byte for byte against the tag checkout. All are identical except
`hermes_cli/plugins.py`, and none of that file's diff lines contain "skill". Line numbers in the
installed `plugins.py` therefore differ from the permalinks above.

The full outputs are under `help/`. The relevant excerpts:

```
usage: hermes plugins show [-h] name
  name        Plugin name or key to show

usage: hermes plugins list [-h] [--enabled] [--user] [--no-bundled] [--plain] [--json]

usage: hermes plugins validate [-h] [--install-deps] [--json] path

usage: hermes plugins doctor [-h] [--ci] [target]

usage: hermes skills list [-h] [--source {all,hub,builtin,local}] [--enabled-only]
```

`hermes plugins` subcommands: `install, search, browse, validate, update, remove, rm, uninstall,
list, ls, enable, disable, capabilities, doctor, compat, pack, show, info`. None of them lists skills.

## Not done

- No command that installs, enables or loads a package was run, not even in the scratch home.
  The DEBUG-log route and the `enable` count line are therefore from source only.
