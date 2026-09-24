# Hermes Agent: `skills.auto_load` and portable Agent Plugins packages

Clean-room research, 2026-09-24. No repository access to the marketplace; only public sources.

Method. Documentation was read first: the published site (hermes-agent.nousresearch.com) and the same Markdown files in the `website/docs/` tree of `NousResearch/hermes-agent`. Source was read only where documentation did not answer. Every source and doc file was fetched by raw URL at one commit, `749220ef0007f8d87bd1531f1c24b0fe93816385` (the `main` head at 2026-09-24T20:17:16Z per `https://api.github.com/repos/NousResearch/hermes-agent/commits/main`), and grepped locally for line numbers. All permalinks below use that sha. `P` stands for `https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/`.

Each fact is labelled **[doc]**, **[source]** or **[not found]**.

Reachability. Everything requested was reachable. One 404: `https://hermes-agent.nousresearch.com/docs/user-guide/plugins` does not exist; the page lives at `/docs/user-guide/features/plugins`. `https://github.com/NousResearch/hermes-agent/git/trees/<sha>?recursive=1` was too large for the fetch tool to summarise; per-directory tree calls were used instead. GitHub code search was not used (needs authentication).

---

## 1. What `skills.auto_load` does, and the wrapper text

**[doc]** `website/docs/user-guide/cli.md`, section "Persistent auto-load via config", lines 297–310 (`P website/docs/user-guide/cli.md#L297-L310`; rendered at `https://hermes-agent.nousresearch.com/docs/user-guide/cli#persistent-auto-load-via-config`):

> To have the same skills active at the start of **every** new session — CLI, TUI, gateway, cron and API sessions alike — set `skills.auto_load` in `config.yaml`:
>
> ```yaml
> skills:
>   auto_load:
>     - hermes-agent-dev
>     - github-pr-workflow
> ```
>
> Each entry is a skill name. The list is resolved once when a session's system prompt is first built and the rendered bytes are reused for the life of the conversation (model switches, compression), so prompt caching stays intact; config edits take effect in the next session. Missing or disabled skills log a warning and are skipped. `-s` names that overlap the list are loaded once.
>
> `--ignore-rules` (equivalently `HERMES_IGNORE_RULES=1`) skips auto-load together with AGENTS.md, SOUL.md, `.cursorrules` and memory injection; explicit `-s` skills still load. The setting is profile-scoped: each profile's `config.yaml` controls its own list.

**[doc]** `website/docs/user-guide/configuration.md`, section "Auto-loading skills every session", lines 798–809 (`P website/docs/user-guide/configuration.md#L798-L809`; rendered at `https://hermes-agent.nousresearch.com/docs/user-guide/configuration`):

> Pin skills so they are fully loaded at the start of every new session, on every surface:
> [yaml block with `my-workflow`, `github-pr-workflow`]
> Resolved once per session when the system prompt is first built (so the prompt stays cache-stable; edits apply to the next session). Missing or disabled skills warn and are skipped; `--ignore-rules` / `HERMES_IGNORE_RULES=1` suppresses the list. Profile-scoped. See [CLI — persistent auto-load](./cli.md#persistent-auto-load-via-config).

**[not found]** Neither doc page says what text wraps an auto-loaded skill in the system prompt. A grep of every downloaded doc file for `auto_load`/`auto-load` finds only those two sections (plus an unrelated sentence in `features/skills.md` line 447 about project skills not being auto-loaded).

**[source]** The wrapper. `agent/skill_commands.py`, `build_auto_load_prompt`, lines 653–681 (`P agent/skill_commands.py#L653-L681`). The activation note passed per skill is, verbatim from lines 673–675:

```
[IMPORTANT: The "{name}" skill is auto-loaded via config (skills.auto_load). Treat its instructions as active guidance for the duration of this session unless the user overrides them.]
```

**[source]** The block layout. `_build_skill_message`, lines 243–292 (`P agent/skill_commands.py#L243-L292`): `parts = [activation_note, "", content.strip()]`; then, only when a `skill_dir` is known, `[Skill directory: {skill_dir}]` plus a fixed note (`_SKILL_DIR_NOTE`, lines 210–214); then an optional `[Skill config (from …/config.yaml): …]` block; an optional `[Skill setup note: …]`; and, when supporting files exist and a dir is known, `[This skill has supporting files (paths relative to the skill directory above):]` with a `- path` list. Blocks for several auto-loaded skills are joined with `"\n\n"` (line 678).

**[source]** Where it lands. `agent/system_prompt.py`, `_auto_load_parts`, lines 316–340 (`P agent/system_prompt.py#L316-L340`), appended to the stable prefix at line 753 (`P agent/system_prompt.py#L753`), after the skills index and before the coding-posture parts. It is skipped for agents with `skip_context_files` and when none of `skills_list`/`skill_view`/`skill_manage` is an available tool (lines 323–326). Resolved once per agent and cached on `agent._auto_load_skills_result` (lines 327–339). Missing names are logged as `skills.auto_load: skill(s) not found or disabled, skipped: …` (line 334).

**[doc]** The PR that introduced the feature is #92048, "feat(skills): skills.auto_load pins skills into every new session", `https://github.com/NousResearch/hermes-agent/pull/92048`. The PR page reports merge commit `286e723db8dbc4c2ee8c554af1e6dc49eb125f3d` (2026-09-15). Its description says nothing about plugin skills.

---

## 2. Does `skills.auto_load` accept `<namespace>:<skill>`?

**[not found]** in documentation. The two doc sections above say only "Each entry is a skill name" (cli.md line 308). No doc page mentions qualified names for `auto_load`. The PR #92048 description does not mention plugin or namespaced skills.

**[source]** The resolution chain accepts a qualified name; nothing in it rejects `:`.

1. `resolve_auto_load_skills`, `P agent/skill_commands.py#L636-L650`: reads `skills.auto_load`, keeps every non-empty string, strips whitespace, dedupes. No name validation.
2. `build_auto_load_prompt`, line 672: each entry is loaded via `_load_skill_payload(identifier, task_id=task_id)`.
3. `_load_skill_payload`, `P agent/skill_commands.py#L165-L192`: `normalized = normalize_skill_lookup_name(raw_identifier)` then `skill_view(normalized, task_id=task_id, preprocess=False)`.
4. `normalize_skill_lookup_name`, `P agent/skill_utils.py#L588-L600`: a non-absolute identifier is returned as-is (`raw_identifier.lstrip("/")`). A `<namespace>:<skill>` string is not absolute, so it passes through unchanged.
5. `skill_view`, `P tools/skills_tool.py#L573-L590`. Docstring: `"plugin:skill" resolves plugin-provided skills`. Line 585: `if ":" in name:  # plugin registry` → `_resolve_plugin_skill(name, …)`. The only pre-check, `_skill_lookup_path_error` (`P tools/skills_tool.py#L78-L91`), rejects absolute paths, Windows drive letters and `..` components; a `namespace:skill` name passes.
6. `_resolve_plugin_skill`, `P tools/skills_tool.py#L264-L305`: `parse_qualified_name`, `discover_plugins()`, `pm.find_plugin_skill(name)`; if found, `_serve_plugin_skill(...)`.
7. `find_plugin_skill`, `P hermes_cli/plugins.py#L1559-L1562`: `self._plugin_skills.get(qualified_name)`. Portable packages register into that same dict through `ctx.register_skill` (see Q5), so a portable skill is found by its qualified name.

So, **[source]**: `skills.auto_load` entries go through the same `skill_view` lookup that serves `plugin:skill` names, and plugin (including portable) skills are looked up. The docs do not state this; it is an inference from code at this commit, not a documented contract.

Two consequences visible in source, both undocumented:

- The rendered name is the qualified name. `_serve_plugin_skill` returns `"name": qualified_name` (`P tools/skills_tool_plugin.py#L156-L157`), and `_load_skill_payload` uses `loaded_skill["name"]` as the display name (line 192). So the activation note reads `The "agent-plugin-<slug>-<hash>:<skill>" skill is auto-loaded via config …`.
- No `[Skill directory: …]` line for plugin skills. `_serve_plugin_skill` returns neither `skill_dir` nor `path`, so `_load_skill_payload` sets `skill_dir = None` (lines 181–191) and `_build_skill_message` omits the directory and supporting-files sections. Only the JSON `linked_files` list is available, and it is used only when `skill_dir` is set (line 262 `if supporting and skill_dir`).

Also **[source]**: the plugin response prepends a bundle banner to the content: `[Bundle context: This skill is part of the '<namespace>' plugin.` plus sibling names when there are any (`P tools/skills_tool_plugin.py#L147-L152`). That banner would appear inside the auto-loaded block. **[doc]** The developer guide states the banner exists for plugin skills loaded by the agent (`P website/docs/developer-guide/plugins/index.md#L847`).

**[not found]** No test under `tests/agent/` or `tests/hermes_cli/` has "auto_load" in its filename (per-directory tree listings at the pinned sha); I did not locate a test that pins a plugin skill via `auto_load`.

---

## 3. Namespace of a portable package, and what "key" is

**[doc]** `website/docs/developer-guide/plugins/index.md`, lines 75–77 (`P website/docs/developer-guide/plugins/index.md#L75-L77`; rendered at `https://hermes-agent.nousresearch.com/docs/developer-guide/plugins`):

> Use `skills_list` to discover the full qualified skill name. Portable skill namespaces have the deterministic form `agent-plugin-<slug>-<hash>`, derived from the discovered plugin key so sanitized names cannot collide.

The doc does not say what the key is or which hash. Source answers:

**[source]** `hermes_cli/plugins_manifest.py`, lines 60–69 (`P hermes_cli/plugins_manifest.py#L60-L69`):

```python
def _portable_skill_namespace(key: str) -> str:
    """Return a readable, collision-resistant namespace for a portable plugin."""
    slug = _portable_slug(key)
    digest = hashlib.sha256(key.encode("utf-8")).hexdigest()[:8]
    return f"agent-plugin-{slug}-{digest}"

def _portable_slug(key: str) -> str:
    slug = "".join(ch if ch.isascii() and (ch.isalnum() or ch in "_-") else "-" for ch in key.lower())
    return slug.strip("-_") or "plugin"
```

So the form `agent-plugin-<slug>-<sha256(key)[:8]>` is confirmed.

**[source]** What `key` is. `portable_plugin_manifest`, `P hermes_cli/plugins_manifest.py#L455-L466`:

```python
key = f"{prefix}/{child.name}" if prefix else data["name"]
...
key=key, portable=True, skill_namespace=_portable_skill_namespace(key),
```

`data["name"]` is the `name` field of the package's `plugin.json`. `prefix` comes from `scan_directory` (`P hermes_cli/plugins_discovery.py#L109-L161`): it is `""` for a package directly under a plugins root and `<category>` for a package one level down (`<root>/<cat>/<name>/`, docstring lines 112–115; `sub_prefix` at line 159).

Therefore:

- **Flat install** (`~/.hermes/plugins/<dir>/plugin.json`): key = the manifest `name`. The directory name and the install URL/path play no part. The namespace is `agent-plugin-<name-slug>-<sha256(name)[:8]>`.
- **Category install** (`~/.hermes/plugins/<cat>/<dir>/plugin.json`): key = `<cat>/<dir>`. Here the directory name does enter the key.

"Derived from the install source" (the prior research) is **not** what the code does: neither the git URL nor the filesystem path is hashed. The scanned roots are, in order, bundled plugins, `~/.hermes/plugins`, and (only with `HERMES_ENABLE_PROJECT_PLUGINS=1`) `./.hermes/plugins` (`P hermes_cli/plugins_discovery.py#L164-L194`).

**Same package from two paths.** **[source]**

- Two flat installs (for example user `~/.hermes/plugins/x/` and project `.hermes/plugins/x/`) share the key (the manifest name) and so the *same* namespace. They do not coexist: `resolve_manifest_winners` keeps one manifest per key, later source wins, "project > user > bundled" (`P hermes_cli/plugins_discovery.py#L196-L219`).
- A flat install and a category install of the same package have different keys (`name` vs `cat/dir`) and therefore two different namespaces.
- `hermes plugins install owner/repo` names the target directory after the manifest `name` when present (`plugin_name = manifest.get("name") or …`, `P hermes_cli/plugins_cmd.py#L873-L876`; `target = plugins_dir / name`, `P hermes_cli/plugins_cmd.py#L210`), so a normal CLI install is always flat and keyed by the manifest name.

**[doc]** Corroboration that the digest exists to disambiguate installs, and is a known cost: issue #119307, `https://github.com/NousResearch/hermes-agent/issues/119307`, "Portable MCP tool names from catalog-pinned plugins are hash-clamped past 64 chars; drop the agent-plugin-<sha8> namespace for catalog installs". **[source]** The MCP side has since dropped the namespace: `portable_mcp_server_name` docstring, `P hermes_cli/plugins_manifest.py#L72-L80`: "The plugin's skill namespace (`agent-plugin-<slug>-<digest>`) is NOT prepended … A duplicate is refused at load". Skills keep the namespace.

---

## 4. Which command lists plugin skills with exact qualified names

**[doc]** The documented way is the agent tool `skills_list`, not a CLI command: "Use `skills_list` to discover the full qualified skill name." (`P website/docs/developer-guide/plugins/index.md#L75`). Same file, line 72–73: "Skills are read-only, namespaced, and loaded through `skills_list` plus `skill_view`."

**[source]** `skills_list` appends every registered plugin skill with `"name": qualified` and `"category": "plugin"` (`P tools/skills_tool.py#L234-L246`, feeding from `list_plugin_skill_metadata`, `P hermes_cli/plugins.py#L1569-L1576`). Disabled or platform-mismatched ones are dropped (line 244).

The CLI commands asked about:

- `hermes plugins list`. **[doc]** `website/docs/reference/cli-commands.md`, `hermes plugins` table (`P website/docs/reference/cli-commands.md#L1620-L1645`): "`list` (alias: `ls`) | List installed plugins with enabled/disabled status." **[doc]** `website/docs/user-guide/features/plugins.md` line 390: "`hermes plugins list # table: enabled / disabled / not enabled …`". **[source]** Columns are Name, Status, Version, Description, Source (`P hermes_cli/plugins_cmd.py#L1714-L1716`); `--json` keys are `name, status, version, description, source, removed` (line 1701). No skill names. The Name column is the registry key (`_read_manifest_info`, `P hermes_cli/plugins_cmd.py#L1537-L1560`, `key = f"{prefix}/{d.name}" if prefix else name`), which is the string hashed in Q3, so a reader can compute the namespace from it but the command does not print the namespace.
- `hermes plugins doctor`. **[doc]** cli-commands.md line 1635: "`doctor [path-or-id] [--ci]` | Validate a native plugin through the real manifest parser, loader, and registration path." **[doc]** developer guide lines 205–212: it "reports invalid hook names, callbacks that do not accept `**kwargs`, registration failures, and drift between declared and registered tools/hooks." **[source]** `hermes_cli/plugin_dev.py` accepts `plugin.json` as a manifest name (`P hermes_cli/plugin_dev.py#L207`), but its report prints manifest name/version/kind, findings, and tool/hook/provider counts only (`format_text`, `P hermes_cli/plugin_dev.py#L192-L205`); the file contains no occurrence of "skill".
- `hermes skills list`. **[doc]** cli-commands.md `hermes skills` table (`P website/docs/reference/cli-commands.md#L1384-L1404`): "`list` | List installed skills." and features/skills.md line 684: "`hermes skills list --source hub # List hub-installed skills`". **[source]** `do_list` reads `_find_all_skills()` (the skills directories) and classifies rows as hub/builtin/local (`P hermes_cli/skills_hub.py#L782-L829`); it never calls the plugin manager, so plugin skills are not listed.

**[not found]** No CLI command that prints `agent-plugin-…:<skill>` names. Only the in-session `skills_list` tool does.

---

## 5. Does the portable loader read `rules/` or `hooks/`?

**[doc]** The developer guide names the components a portable package may provide: "An enabled package may provide immediate `skills/*/SKILL.md` directories and stdio MCP servers from root `mcp.json`." (`P website/docs/developer-guide/plugins/index.md#L71-L72`). The illustrated layout (lines 52–59) shows only `plugin.json`, `skills/`, `mcp.json`. Line 110: "This is an explicit supported subset, not a claim of full Agent Plugins conformance." Lines 85–86: "Hermes validates `plugin.json`, Agent Skills frontmatter, fixed component locations, `mcp.json`, resolved paths, and symlink containment locally."

**[not found]** No downloaded doc file (cli.md, configuration.md, features/plugins.md, features/skills.md, developer-guide/plugins/index.md, reference/cli-commands.md) mentions `hooks.json` or a `rules/` directory for portable packages; the only `rules/` hit is Cursor's `.cursor/rules/*.mdc` in configuration.md line 2988, unrelated. Hermes's own hook mechanism is `HOOK.yaml` + `handler.py` under `~/.hermes/hooks/<name>/` (`P website/docs/developer-guide/plugins/index.md#L33`), a different thing from Agent Plugins `hooks/hooks.json`.

**[source]** `hermes_cli/agent_plugins.py` ("Compatibility helpers for Agent Plugins v1 portable directory packages", line 1). `load_agent_plugin`, `P hermes_cli/agent_plugins.py#L423-L435`, calls only `_validate_root`, `_discover_skills` (line 224, reads `root / "skills"`) and `_discover_mcp` (line 381, reads `root / "mcp.json"`), and the resulting `AgentPluginPackage` dataclass (lines 78–89) has fields for `skills`, `mcp_servers`, `server_declarations` and nothing else. The file contains zero occurrences of the strings `rules` or `hooks` (local grep count 0). The loader that consumes the package, `_load_portable_plugin`, `P hermes_cli/plugins_loader.py#L551-L596`, registers `package.skills` via `ctx.register_skill(...)` (line 564) and the MCP servers (lines 567–596), nothing else.

Answer: **no**. `rules/` and `hooks/hooks.json` are not read; they are ignored silently (no diagnostic names them).

---

## 6. Are plugin skills listed in the system prompt's available-skills index?

**[doc]** Yes, there is an explicit statement. `website/docs/developer-guide/plugins/index.md`, line 845 (`P website/docs/developer-guide/plugins/index.md#L843-L847`), under "Key properties" of plugin-registered skills:

> - Plugin skills are **read-only** — they don't enter `~/.hermes/skills/` and can't be edited via `skill_manage`.
> - Plugin skills are **not** listed in the system prompt's `<available_skills>` index — they're opt-in explicit loads.
> - Bare skill names are unaffected — the namespace prevents collisions with built-in skills.
> - When the agent loads a plugin skill, a bundle context banner is prepended listing sibling skills from the same plugin.

That paragraph is written under the native `ctx.register_skill()` section. It applies to portable packages because, **[source]**, the portable loader registers through the same `ctx.register_skill` (`P hermes_cli/plugins_loader.py#L564`) into the same `_plugin_skills` registry (`P hermes_cli/plugins.py#L1011-L1040`).

**[source]** Corroboration: the index builder `build_skills_system_prompt` / `_build_skills_system_prompt_inner` (`P agent/prompt_builder.py#L1262-L1290`, `#L1411-L1436`) walks `skills_dir`, `skills.external_dirs` and trusted project dirs only; `agent/prompt_builder.py` never imports the plugin manager (grep for "plugin" in the file hits only terminal-backend and preview-directive code). The `<available_skills>` tags are emitted at lines 1380 and 1398–1400.

**Implication for the package's goal** (skill text in every session's prompt): the index will not advertise the skill, so the agent will not discover it by itself. `skills.auto_load` with the qualified name is the only mechanism found that puts the text into every session's prompt, and that combination is unsupported by any documented sentence; it rests on the source chain in Q2 at commit `749220ef…`. The namespace half of that name is stable only while the package's `plugin.json` `name` and the install layout (flat vs category) stay the same (Q3).

---

## Sources used

Documentation (site and the same files in the repository tree at the pinned sha):

- https://hermes-agent.nousresearch.com/docs/user-guide/cli#persistent-auto-load-via-config — `P website/docs/user-guide/cli.md`
- https://hermes-agent.nousresearch.com/docs/user-guide/configuration — `P website/docs/user-guide/configuration.md`
- https://hermes-agent.nousresearch.com/docs/developer-guide/plugins — `P website/docs/developer-guide/plugins/index.md`
- https://hermes-agent.nousresearch.com/docs/user-guide/features/plugins — `P website/docs/user-guide/features/plugins.md`
- https://hermes-agent.nousresearch.com/docs/user-guide/features/skills — `P website/docs/user-guide/features/skills.md`
- https://hermes-agent.nousresearch.com/docs/user-guide/features/plugin-catalog
- `P website/docs/reference/cli-commands.md`
- https://github.com/NousResearch/hermes-agent/pull/92048
- https://github.com/NousResearch/hermes-agent/issues/119307

Source (all at `749220ef0007f8d87bd1531f1c24b0fe93816385`):

- `P agent/skill_commands.py`, `P agent/system_prompt.py`, `P agent/skill_utils.py`, `P agent/prompt_builder.py`
- `P tools/skills_tool.py`, `P tools/skills_tool_plugin.py`, `P tools/mcp_tool_config.py`
- `P hermes_cli/agent_plugins.py`, `P hermes_cli/plugins_manifest.py`, `P hermes_cli/plugins_discovery.py`, `P hermes_cli/plugins_loader.py`, `P hermes_cli/plugins.py`, `P hermes_cli/plugins_cmd.py`, `P hermes_cli/plugin_dev.py`, `P hermes_cli/skills_hub.py`
- `P tests/hermes_cli/test_agent_plugins.py` (read for namespace/ignored-directory tests; none found)
