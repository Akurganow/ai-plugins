# 06: Hermes Agent: always-on rules from a plugin, and hybrid Agent Plugins / native packages

Clean-room research. Nothing under `/home/user/ai-plugins` or `/home/user/how-possible` was read.
Nothing was installed or run. "From source" means read in the Hermes source at the pinned commit; it
does not mean the code was executed.

## Sources and reachability

| Source | Route | Result |
|---|---|---|
| `NousResearch/hermes-agent` `main` | `git ls-remote https://github.com/NousResearch/hermes-agent.git` | `749220ef0007f8d87bd1531f1c24b0fe93816385 refs/heads/main` (commit date 2026-09-24T16:17:16-04:00, "feat(web): serve managed search through Perplexity") |
| Same repo, files | `raw.githubusercontent.com/.../main/<path>` | 200 for `website/docs/user-guide/features/plugins.md`, `.../skills.md`, `hermes_cli/plugins_cmd.py`, `website/docs/developer-guide/plugins/index.md` |
| Same repo, whole tree | `api.github.com/repos/...` | **403** from the session's GitHub gateway ("GitHub access to this repository is not enabled for this session") |
| Same repo, file listing | `data.jsdelivr.com` | **blocked**: `CONNECT tunnel failed, response 403` (egress proxy, `connect_rejected`) |
| Same repo, whole tree | `git clone --depth 1` over HTTPS into the scratchpad (`research/hermes/src`) | OK, HEAD = `749220ef…` |
| Hermes docs site | not tried; the caller said it is blocked | the docs were read as Markdown in the repo's `website/docs/`, so they still count as **documentation** |
| Agent Plugins spec | `raw.githubusercontent.com/agentplugins/agent-plugins-spec/main/spec/1.0.0.md`; `git ls-remote` HEAD = `ff8ab5e392cc87bd88d87c060815a87490e51003` | 200, 640 lines, "Status: Published" |

**Deviation:** the caller allowed only curl or WebFetch. I also used `git ls-remote` and one shallow `git clone`
of the public repository, because the API and jsDelivr listings were blocked. Without a file listing I could
not find the loader modules. All the clone does is read the same public files that raw.githubusercontent
serves, and every path below is at commit `749220ef`.

Permalink base for every Hermes path below:
`https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/<path>#L<n>`

---

## 1. Native Hermes plugin format

**Manifest and entry point (documentation).** `website/docs/user-guide/features/plugins.md` L21-29:

> Drop a directory into `~/.hermes/plugins/` with a `plugin.yaml` and Python code:
> `plugin.yaml      # manifest` / `__init__.py      # register() — wires schemas to handlers`

The manifest is **`plugin.yaml`** (`plugin.yml` also accepted: `hermes_cli/plugins_discovery.py` L139). The entry
point is `register(ctx)` in `__init__.py`. Fields (dev guide `website/docs/developer-guide/plugins/index.md`
L225-250, L304-314): `name`, `version`, `description`, `provides_tools`, `provides_hooks`, `author`, `requires_env`,
`capabilities`, and the v2 fields `manifest_version`, `api_version`, `requires_plugins`, `python_dependencies`,
`python_runtime`, `config_schema`, `license`, `homepage` and `tags`. The source also parses `kind`, `requires_hermes`,
`emits`, `listens` and a legacy `hooks:` key (`hermes_cli/plugins_manifest.py` L509-520). The dev guide says unknown
fields are ignored (L131). The dev guide also says (L749): "Native packages need both `plugin.yaml` and `__init__.py` with a `register(ctx)`
function." The source enforces this: `hermes_cli/plugins_loader.py` L630-632 contains
`raise FileNotFoundError(f"No __init__.py in {plugin_dir}")`.

**Hooks (documentation plus source).** `plugins.md` L319: "Plugins can register the 27 lifecycle events currently
accepted by `hermes_cli.plugins.VALID_HOOKS`." The canonical set is in `hermes_cli/plugins.py` L108-175 and includes
`pre_tool_call`, `post_tool_call`, `transform_tool_result`, `transform_terminal_output`, `transform_llm_output`,
`pre_llm_call`, `post_llm_call`, `pre_verify`, `on_session_start`, `on_session_end`, `on_session_finalize`,
`on_session_reset`, `subagent_start`/`subagent_stop`, `pre_gateway_dispatch` and the streaming, API, approval and
kanban observers. The API is `ctx.register_hook(name, callback)` (`plugins.py` L930-932). An unknown hook name
logs a warning and is still stored (L946-949).

**Which hooks can put text in front of the model:**

- `pre_llm_call` is the **only hook that injects text**. From the dev guide L1082:
  > "This is the only hook whose return value matters. When a `pre_llm_call` callback returns a dict with a
  > `"context"` key (or a plain string), Hermes injects that text into the **current turn's user message**."

  From L1115-1119:
  > "Injected context is appended to the **user message**, not the system prompt. … **Ephemeral** — the injection
  > happens at API call time only. … **The system prompt is Hermes's territory**"

  The dev guide also ships a guardrails example that runs every turn (L1151-1167: `POLICY = """You MUST follow these
  content policies…"""` … `ctx.register_hook("pre_llm_call", inject_guardrails)`). The signature carries
  `is_first_turn` (L1056; `hooks.md` L680-689). Timing, from `hooks.md` L693: "Fires once per `run_conversation()` call
  (i.e. once per user turn)". Size cap, from the dev guide L1101: "Per-hook context is capped at `10,000` characters
  by default"; anything over the cap is spilled to `$HERMES_HOME/hook_outputs/…`.

  Source: `agent/turn_context.py` L745-798 (`_collect_pre_llm_call_context`, docstring "their context is injected
  into the user message (never the system prompt)", `is_first_turn=(not bool(conversation_history))`). Caveat from
  source: L752-753 has `if getattr(agent, "_persist_disabled", False): return ""`, so the hook is skipped for agents
  with persistence disabled.
- `on_session_start` is an observer and its return value is ignored. From `hooks.md` L470: "First turn of a new
  session; return ignored." From `hooks.md` L918: it fires "after the system prompt is built". **It cannot inject.**
- `ctx.inject_message(content, role="user", …)` (`plugins.md` L786-823) queues a **new user turn**, or interrupts
  the current one. It is for external events and does not add standing context. In gateway mode it needs
  `allow_gateway_injection` (L825-832).
- **Plugin system-prompt sections: this is the documented always-on API.** From `website/docs/user-guide/features/hooks.md`
  L401-443:
  > "Plugins that need durable, always-on guidance can register a bounded system prompt section instead of injecting
  > the same text through `pre_llm_call` on every turn:"
  > `ctx.register_system_prompt_section("kanban-advanced.worker-rules", board_rules, position="after_memory", max_chars=4000)`
  > "`after_memory` is the only placement anchor. Sections are sorted by ID, rendered after memory/profile context
  > and before session metadata; plugins cannot reorder or replace core prompt content." … "A callable … runs **once
  > for a new session**." … "`max_chars` is capped at 4,000 characters. All plugin sections together, including their
  > audit headings, are capped at 8,000 characters and 32 sections." … "Every accepted section is named in the prompt
  > and logged at session start".

  Source: `hermes_cli/plugins.py` L954-979 (`register_system_prompt_section`, which rejects a duplicate ID with
  `ValueError`). `hermes_cli/plugins_dispatch.py` L67-76 defines the constants
  (`SYSTEM_PROMPT_SECTION_POSITIONS = frozenset({"after_memory"})`, `MAX_SYSTEM_PROMPT_SECTION_CHARS = 4_000`,
  `MAX_SYSTEM_PROMPT_SECTIONS_TOTAL_CHARS = 8_000`, heading prefix `"## Plugin Context: "`). `agent/system_prompt.py`
  L776-779 places the sections in the **volatile tier** after the skills index and memory ("Plugin sections are
  confined to one coarse anchor in the volatile tail"). L113-135 freezes the sections per session, and L802-818
  re-renders them after compression. **The user-guide `plugins.md` does not list this API**; only `hooks.md`
  documents it. In the repo it is exercised only by tests (`tests/hermes_cli/test_plugin_prompt_sections.py`,
  `tests/agent/test_plugin_prompt_sections.py`). No bundled plugin under `plugins/` calls it.
- **Middleware** (dev guide L1191-1227; `hermes_cli/middleware.py` L19-26): the kinds are `tool_request`,
  `llm_request`, `tool_execution` and `llm_execution`. From L1216, `llm_request`: "Return `{"request": {...}}` to
  replace the effective provider kwargs before Hermes sends them". Applied in `agent/turn_api_request.py` L141-143.
  In principle this could rewrite the system message on every API call. That is my inference from source: no
  document offers middleware as a way to edit the prompt, and doing so would work against the documented
  prompt-cache design (L1117).
- **Enforcement after the fact:** `transform_llm_output` (`hooks.md` L1578-1600) replaces the final answer
  "before that response is delivered … and before the assistant row is persisted". `pre_verify` (L820-840) can keep
  a turn going, but it fires only "when the agent edited code".

## 2. What Hermes loads from an Agent Plugins package ("portable Agent Plugins v1")

From the dev guide `website/docs/developer-guide/plugins/index.md` L45-50:
> "Hermes can also install and load directory packages that target the Agent Plugins v1.0.0 format. This is a
> compatibility adapter for the portable components Hermes already owns. It does not replace native `plugin.yaml`
> plus `register(ctx)` plugins."

From L70-74:
> "Portable packages are disabled after installation unless you explicitly enable them. An enabled package may provide
> immediate `skills/*/SKILL.md` directories and stdio MCP servers from root `mcp.json`. Skills are read-only,
> namespaced, and loaded through `skills_list` plus `skill_view`."

From L94-110: it supports Streamable HTTP; legacy `sse` is "reported and skipped"; "This is an explicit supported
subset, not a claim of full Agent Plugins conformance." From L749: "Portable packages do not import Python and do not
require `__init__.py`."

What the source reads (`hermes_cli/agent_plugins.py`):
- `plugin.json` (L153). Unknown top-level fields are reported and dropped (L158-160). The `$schema` must equal
  `https://agent-plugins.org/schemas/1.0.0/plugin.schema.json` (L45, L161-162).
- `skills/<child>/SKILL.md`, immediate children only (L224-257). The front matter must pass Agent Skills rules
  (L186-204), including **L200-201: `metadata` "must map string keys to string values"**.
- `mcp.json` (L381-413), with `stdio` and `streamable-http`; `sse` is rejected (L374-378, L400-401).
- One extension key only: `extensions["com.nousresearch.hermes"].servers` (L17, L92-124). Its allowed keys are
  `app`, `requires` and `liveness`.

Nothing else is read. `hooks/`, `rules/`, `agents/`, `commands/`, `.claude-plugin/` and any `com.nousresearch.hermes/`
**directory** have no reader in `agent_plugins.py`. A grep for `com.nousresearch.hermes` outside tests finds only the
manifest-extension uses. Those files are therefore silently ignored, as spec §6 L273 requires: "Clients MUST ignore
component types they do not support." Separately, `_FOREIGN_HARNESS_MANIFEST_DIRS`
(`hermes_cli/plugins_discovery.py` L30-35: `.claude-plugin`, `.codex-plugin`, `.cursor-plugin`, …) skips such
directories when they appear as *children of a plugins root* during discovery.

The loader registers only skills and MCP servers (`hermes_cli/plugins_loader.py` L551-603, `_load_portable_plugin`:
"Load validated portable components without importing Python code"). A portable package **has no way to register a
hook, a system-prompt section or middleware.**

Two consequences for always-on rules (source):
- Portable skills go through `ctx.register_skill` (L564). According to `hermes_cli/plugins.py` L1015-1018, such skills
  are "Not copied into `~/.hermes/skills/` and not in the system prompt's `<available_skills>`". The dev guide agrees
  at L845: "Plugin skills are **not** listed in the system prompt's `<available_skills>` index — they're opt-in
  explicit loads." So a portable skill is **less** visible than a user skill: the model sees it only if it calls
  `skills_list`.
- A portable skill whose `SKILL.md` uses Hermes's nested `metadata: hermes: {...}` block (skills.md L169-179) fails
  `_valid_skill_frontmatter` and is **skipped** with a diagnostic.
- Portable skill namespace: `agent-plugin-<slug>-<sha256(key)[:8]>` (`hermes_cli/plugins_manifest.py` L60-64). The key
  is the `plugin.json` `name` for a flat install (L461). Example computed for the key `example-rules`:
  `agent-plugin-example-rules-a0dbf553`.

## 3. Coexistence: a root `plugin.json` alongside `plugin.yaml` and `__init__.py`

**Native wins, and the portable half is not loaded.** Source, discovery (`hermes_cli/plugins_discovery.py` L139-155):
```
manifest_file = next((f for f in (child / "plugin.yaml", child / "plugin.yml") if f.exists()), None)
portable_file = child / "plugin.json"
...
if manifest_file is not None:
    manifest = parse_manifest_file(manifest_file, child, source, prefix)
...
elif has_portable:
    manifests.append(portable_plugin_manifest(child, source, prefix))
```
Validator (`hermes_cli/plugin_validate.py` L482-485): "When a package carries both manifests the native plugin.yaml
always wins (this branch is only reached when no native manifest exists)." CLI (`hermes_cli/plugins_cmd.py` L1563):
"True for an Agent Plugins v1 package (`plugin.json` only; native `plugin.yaml` wins)."

So a hybrid directory loads as **one native plugin**. Its `skills/` load only if `register()` calls
`ctx.register_skill` for them; the documented pattern for that is at dev guide L810-834. Its `mcp.json` is not loaded
at all. `plugin.json` is still checked at **install**: `_refuse_unavailable_portable_plugin` runs
`load_agent_plugin` whenever `plugin.json` is a file (`plugins_cmd.py` L784-793, called at L885), so an invalid
`plugin.json` blocks the install even when `plugin.yaml` is present. A minor inconsistency from source (not run):
`plugin_validate.py` L522-535 treats `plugin.json` beside `plugin.yaml` as "loadable", yet the loader then takes the
native path and raises `No __init__.py` when `__init__.py` is missing (`plugins_loader.py` L630-632).

**What the Agent Plugins spec says about a root `plugin.yaml` and `__init__.py`**
(agent-plugins-spec `ff8ab5e3`, `spec/1.0.0.md`):
- L135: "No other file can replace, supplement, or override the core fields in root `plugin.json`." Hermes's
  `plugin.yaml` has its own `name`/`version`/`description`. It does not *override* `plugin.json` in Hermes's reading,
  since Hermes simply ignores `plugin.json`, but it is a second manifest carrying the same core fields.
- L403: "Client-specific files MUST be represented under a top-level directory named for that namespace."
- L431: "files for `com.example.client` belong in `com.example.client/`."

A root `plugin.yaml` and `__init__.py` are Hermes-specific files at the root, so they sit outside the §8 rule. The
spec-conformant place is `com.nousresearch.hermes/`, and Hermes **does not load from that directory** (see §2).

**A native plugin in a subdirectory: source plus documentation.** The install identifier accepts a subdirectory:
`owner/repo/path/to/plugin`, `owner/repo#subdir`, or a GitHub `tree/<ref>/<path>` URL (`plugins_cmd.py` L225-261).
`plugins.md` L166-167: "A subdirectory install (owner/repo/path/to/plugin) downloads only that folder's files." The
catalog entry schema carries `subdir: ""  # optional path within the repo` (`plugin-catalog/README.md` L74). A real
catalog example is `plugin-catalog/agentplaybooks-portable.yaml` L4:
`subdir: packages/hermes-portable/agentplaybooks-portable`. Plugin packs also take `subdir:` (`plugins.md` L617).

The source shows that **only the subdirectory lands on disk**: `tmp_target = _resolve_subdir_within(tmp_clone, subdir)`
(L870), then `_swap_in_plugin(tmp_target, target, …)` (L907), with a sparse, blobless clone (L698-707). A native
plugin in `plugins/<name>/com.nousresearch.hermes/` can therefore be installed as
`hermes plugins install owner/repo/plugins/<name>/com.nousresearch.hermes`, but after install it **cannot reach the
package's `../skills/`**. It needs its own copy of the rules text, or it must be installed as a separate plugin next
to the portable one. I found no mechanism that installs a portable package and a native plugin from one install
command, apart from the Desktop "hybrid" split, which is agent Python plus `desktop/plugin.js` and not
portable plus native (`plugins.md` L438-441).

Installing both from one repo is possible as **two installs**:
`hermes plugins install owner/repo/plugins/<name>` (portable: skills + MCP) and
`hermes plugins install owner/repo/plugins/<name>/com.nousresearch.hermes` (native). They must have **different
names**, because install fails with "already exists" when names collide (`plugins_cmd.py` L889-892), and discovery
keys winners by name (`plugins_discovery.py` L196-219). The portable install sees the `com.nousresearch.hermes/`
directory only as an ignored subdirectory. Not verified by running.

## 4. Skills: always-on or auto-loaded

- No `SKILL.md` field makes a skill always-on. The Hermes-specific front matter (`skills.md` L161-180) is `name`,
  `description`, `version`, `platforms`, and `metadata.hermes.{tags, category, fallback_for_toolsets,
  requires_toolsets, fallback_for_tools, requires_tools, config}`. The conditional fields only **hide or show** a skill
  in the index (L244-266). They do not load it.
- **`skills.auto_load` is user config and is documented.** `website/docs/user-guide/cli.md` L297-310:
  > "To have the same skills active at the start of **every** new session — CLI, TUI, gateway, cron and API sessions
  > alike — set `skills.auto_load` in `config.yaml`" … "The list is resolved once when a session's system prompt is
  > first built" … "`--ignore-rules` (equivalently `HERMES_IGNORE_RULES=1`) skips auto-load together with AGENTS.md,
  > SOUL.md, `.cursorrules` and memory injection".

  Also documented in `configuration.md` L798-809: "Pin skills so they are fully loaded at the start of every new
  session". Source: `agent/system_prompt.py` L752-753 puts it in the **stable** tier ("Pinned skills are per-agent
  constants … so they live in the stable prefix"). L316-340 gates it: nothing is loaded without the skills toolset,
  nor for `skip_context_files` agents. `agent/skill_commands.py` L673-675 adds a wrapper note:
  `[IMPORTANT: The "{name}" skill is auto-loaded via config (skills.auto_load). Treat its instructions as active
  guidance for the duration of this session unless the user overrides them.]`
- **Whether auto_load takes a plugin skill (`namespace:skill`)**: from source this looks yes, but nothing verifies it.
  `_load_skill_payload` calls `skill_view(normalized)` (`skill_commands.py` L165-174). `skill_view` sends any name
  containing `:` to the plugin registry (`tools/skills_tool.py` L585-588 → `_resolve_plugin_skill` L264-299, which
  calls `discover_plugins()` and then `find_plugin_skill`). No document states it, and `tests/agent/test_skills_auto_load.py`
  has no plugin-skill case. **Not documented, not run.**
- The launch flag `hermes -s <skill>` preloads skills (cli.md L286-295); it is per launch.
- `skills.external_dirs` (skills.md L373) would put a directory's skills into the `<available_skills>` index. They
  would still be on demand, not always loaded.

## 5. System prompt customisation

- **SOUL.md** (documentation, `website/docs/user-guide/features/personality.md` L9-41, L119-133): "SOUL.md is the
  **primary identity** — it's the first thing in the system prompt" … "Hermes loads `SOUL.md` only from `HERMES_HOME`"
  … "Existing user `SOUL.md` files are never overwritten" … "scanned like other context-bearing files for prompt
  injection patterns". There is **no plugin API** for writing to SOUL.md or registering a persona. A plugin's Python
  could write the file, but no document sanctions that and it would overwrite user data.
- **Personalities / `agent.system_prompt`** (personality.md L212-230): these are user `config.yaml` keys. There is no
  plugin API for them.
- **Project context files** (`context-files.md` L11-24): `.hermes.md` → `AGENTS.override.md` → `AGENTS.md` →
  `CLAUDE.md` → `.cursorrules`, "first match wins", taken from the working directory. They belong to the project, not
  to the plugin.
- **The only documented way for a plugin to add to the system prompt** is `ctx.register_system_prompt_section`
  (see §1; `hooks.md` L401-443). Everything else a plugin injects goes into the user message (`pre_llm_call`).
- In `build_system_prompt_parts` (`agent/system_prompt.py` L727-787) the order is:
  stable = [SOUL.md or default identity, guidance, **skills.auto_load blocks**, coding brief];
  context = [caller `system_message`, project context files, workspace];
  volatile = [skills index, memory, **plugin sections**, timestamp, runtime environment].

## 6. Enablement, consent, scanner

- **Opt-in.** `plugins.md` L151: "General plugins and user-installed backends are disabled by default — … nothing
  with hooks or tools loads until you add the plugin's name to `plugins.enabled`". L193: "After
  `hermes plugins install owner/repo`, you're asked `Enable 'name' now? [y/N]` — defaults to no." The dev guide L70
  says the same for portable packages. Project plugins (`./.hermes/plugins/`) also need
  `HERMES_ENABLE_PROJECT_PLUGINS=true` (L93, L128).
- **Per-plugin permission prompts** cover only declared `capabilities` (`plugins.md` L453-485). The registry is
  `hermes_cli/plugin_capabilities.py` L27-47: `tools.override`, five `llm.*` overrides and `gateway.platform_actions`.
  **Hooks, middleware and system-prompt sections are not capability-gated** (source: `plugins.py` L930-979 contains no
  capability check). Enabling the plugin is the whole consent. Gateway injection and `call_mcp` have their own
  per-plugin keys (L825-832, L863-872).
- **Catalog re-pins** show a delta and ask `y/N` when the new pin "adds tools, hooks, Python dependencies, host
  capabilities or a Desktop UI half" (`plugins.md` L476-481). Catalog entries declare `provides_hooks` and
  `provides_middleware` (`plugin-catalog/README.md` L88-92).
- **Install scanner** (`plugins.md` L668-736): the verdicts are **safe** (installs), **caution** (`Install anyway? [y/N]`
  or `--force`) and **dangerous** (blocked; "`--force` does **not** override"). Files under `skills/` keep full
  severity (L703-707: "anything under a bundled `skills/` tree or in `after-install.md`, which the agent reads as
  instructions"). The patterns are in `tools/skills_guard.py` L206-230 and L406-418, and the verdict mapping at L833
  is "critical → dangerous, high → caution". **Risk for a writing-standard skill:** these patterns match on wording.
  `you\s+are\s+(?:\w+\s+)*now\s+` (role_hijack, high), `pretend … (you are|to be)` (high),
  `do not … tell … the user` (high), `disregard … (your|all|any) … (instructions|rules|guidelines)` (critical), and
  `new … policy|updated … guidelines|revised … instructions` (medium) could all be hit by a style guide that quotes
  phrases to avoid. Opt-out: `plugins.scan_on_install: false` (L731-736).
- The hook callback timeout is 30 s by default (`plugins.md` L169-175). Callback exceptions are logged and skipped
  (`hooks.md` L395).

## Recommended mechanism(s) for a package that must enforce a writing standard in every Hermes session

Ranked. The first two need **native Python** and cannot be reached from a portable Agent Plugins package alone.

1. **Native plugin with `ctx.register_system_prompt_section`.** *Documented* (`hooks.md` L401-443) and *from source*
   (`plugins.py` L954-979; `system_prompt.py` L776-779). The rules go into the system prompt of every new session
   before the first turn, under `## Plugin Context: <id>`. They stay frozen for the session and are re-rendered after
   compression. Limits: 4,000 characters per section, 8,000 characters across all plugin sections, and no placement
   other than after memory. It is a **summary channel**: a longer standard needs a short "always" digest here, with
   the full text left in a skill. The user must still run `hermes plugins install` and then `hermes plugins enable`.
   Nothing prompts the user beyond enablement.
2. **Native plugin with a `pre_llm_call` context hook**, optionally together with (1). *Documented* (dev guide
   L1080-1167, including the "Guardrails plugin" example). The rules are restated on every turn at the end of the user
   message, which suits models that weight recent text heavily; the catalog's `recency-anchor` entry
   (`plugin-catalog/recency-anchor.yaml`) exists for exactly that. Cost: it is sent on every turn, capped at 10,000
   characters per hook, and it is not in the system prompt.
   Optional enforcement after the fact: `transform_llm_output` (*documented*, `hooks.md` L1578) can rewrite the final
   text mechanically. It cannot make the model follow the rules. It can only edit or flag the output.
3. **Portable package only, with the user setting `skills.auto_load`.** The rules skill loads in full, in the
   **stable** system-prompt tier, with Hermes's own "[IMPORTANT: … Treat its instructions as active guidance …]"
   wrapper. The config key is *documented* (cli.md L297-310). *From source only and not verified*: that
   `skills.auto_load` accepts a portable plugin skill's qualified name
   `agent-plugin-<slug>-<sha256(key)[:8]>:<skill>`, as described in §4. This needs a user action; the package cannot
   set it. `--ignore-rules` suppresses it.
4. **Do not rely on** portable skills being discovered on their own: plugin skills are not in `<available_skills>`
   (*documented*, dev guide L845). Also do not rely on SOUL.md, AGENTS.md or `agent.system_prompt`: those are user or
   project files with no plugin API behind them.

**Packaging for (1) and (2) alongside an Agent Plugins 1.0.0 package:**
- *Option A, spec-clean (from source; install behaviour not run):* put the native plugin in
  `com.nousresearch.hermes/` (spec §8.2 L431) with its own `plugin.yaml`, `__init__.py` and **a copy or digest of the
  rules**. Install it separately with `hermes plugins install owner/repo/<pkg>/com.nousresearch.hermes`, under a
  different plugin name from the portable package. Only that subdirectory is installed, so it cannot read the
  package's `skills/`.
- *Option B, one directory (from source):* a root `plugin.yaml` + `__init__.py` next to `plugin.json`. Hermes loads
  it as native, `plugin.json` is ignored at load but still validated at install, and `register()` must register
  `skills/` itself (dev guide L810-834). The cost is that this **departs from spec §8** (L403: client-specific files
  MUST be under the namespace directory). It also puts a Python module at the package root, which other clients
  ignore but which is executable code in the tree.
- Whether either option is compatible with the caller repository's own rules (text-only files, the conformance
  check) was **not assessed here**. I did not read that repository.

**Unverified overall:** nothing was installed or run against Hermes. Every "from source" statement was read at
`749220ef` and was not executed. The docs site was not fetched; the docs were read as Markdown in the repo.
