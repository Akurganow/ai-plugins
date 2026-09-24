# How four clients show and invoke a plugin skill

Clean-room research, 2026-09-24. No repository access. Documentation was read
first; source only where documentation did not answer. Each fact says which
kind it is: **doc**, **source**, or **not found**. Source citations are commit
permalinks. Sentences are kept short.

Commit shas used for every source permalink (each is the `main` head returned
by the GitHub commits API on 2026-09-24):

| Repository | Sha | Commit date |
| :-- | :-- | :-- |
| `can1357/oh-my-pi` | `ba56afb26280a6a3195c329fa66a3f8fb52f82eb` | 2026-09-24T19:36:44Z |
| `openai/codex` | `549455f3ec5a7f2a0489894543a0e49f307142a6` | 2026-09-24T21:25:53Z |
| `NousResearch/hermes-agent` | `749220ef0007f8d87bd1531f1c24b0fe93816385` | 2026-09-24 |

## Summary table

| Client | Model-facing name | User invocation | Namespaced by plugin? | Two plugins both shipping `review` |
| :-- | :-- | :-- | :-- | :-- |
| Oh-My-Pi | bare `review` | `/skill:review` | **No** | first wins by provider priority then sort order; the other is skipped with a `name collision` warning |
| Codex CLI | `<plugin-name>:review` | `/skills`, or `$<plugin-name>:review` | **Yes** (from the plugin manifest `name`) | both load; a bare `$review` mention selects neither when the plain name is ambiguous |
| Claude Code | `/<plugin-name>:review` | `/<plugin-name>:review`; bare `/review` also works unless another command already has that name | **Yes** | both load under their prefixes; which one gets the bare name is not stated |
| Hermes Agent | `agent-plugin-<slug>-<hash>:review` | model tool call `skill_view("agent-plugin-<slug>-<hash>:review")`; no slash command | **Yes** (hash-suffixed namespace) | both load; namespaces differ |

Short names are unambiguous in Codex, Claude Code and Hermes. They are **not**
unambiguous in Oh-My-Pi, which dedupes on the bare skill name across every
provider.

---

## 1. Oh-My-Pi (`@oh-my-pi/pi-coding-agent`, github.com/can1357/oh-my-pi)

### Where the documentation lives

- `docs/plugins.md` does not exist on `main`: raw fetch returned HTTP 404.
  **Not found.** The marketplace document is `docs/marketplace.md`.
- The skills document is `docs/skills.md`. It names the source files it
  describes: `packages/coding-agent/src/extensibility/skills.ts`,
  `src/modes/skill-command.ts`, `input-controller.ts`. **Doc:**
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/skills.md

### How a skill is listed in the system prompt

- **Doc** (`docs/skills.md` line 134): "include discovered skills list in
  prompt, excluding skills with `hide: true`". The list is of discovered
  skills; no plugin prefix is described anywhere in the file.
- **Doc** (`docs/skills.md` line 98): "Dedup key is skill name. First item
  with a given name wins."
- The exact rendered format of each entry was not read. **Not found** in the
  files fetched.

### How the user invokes a skill

- **Doc** (`docs/skills.md` lines 142-148): heading "Interactive
  `/skill:<name>` commands". "If `skills.enableSkillCommands` is true,
  interactive mode registers one slash command per discovered skill."
  "`/skill:<name> [args]` behavior: recognizes the traditional leading form
  and a whitespace-delimited `/skill:<name>` token embedded in ordinary
  prose".
- **Source** confirming the command name is `skill:` plus the bare skill
  name, with no plugin segment:
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/extensibility/skills.ts#L422-L424
  ```ts
  export function getSkillSlashCommandName(skill: Pick<Skill, "name">): string {
  	return `skill:${skill.name}`;
  }
  ```
- **Source** for the registration loop, one command per loaded skill:
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/modes/interactive-mode.ts#L2121-L2131
  ```ts
  this.skillCommands.clear();
  if (this.session.skillsSettings?.enableSkillCommands !== false) {
  	const icon = getSlashCommandTypeIcon("skill");
  	for (const skill of this.session.skills) {
  		const commandName = `skill:${skill.name}`;
  		this.skillCommands.set(commandName, skill);
  ```
- **Source** for parsing `/skill:<name>`; the parsed `name` is documented as
  "Bare skill name without the leading `skill:` prefix":
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/extensibility/skills.ts#L433-L458

So the invocation is `/skill:<name>`, not `/skill:<plugin>:<name>`.

### Which provider loads a marketplace-installed plugin's skills

- **Doc** (`docs/skills.md` lines 85-98), the registered providers: `native`
  (100); `omp-plugins` (90) — "`skills/` bundled next to extension packages
  loaded through `extensions:`, `--extension`/`-e`, or installed plugins under
  `~/.omp/plugins/node_modules`"; `claude` (80); a priority-70 group of
  `claude-plugins`, `agents`, `codex`; `opencode` (55); `github` (30);
  `omp-managed` (5). The document does not list an `agent-plugins` provider.
- **Source**: an `agent-plugins` provider exists, priority 75, and its header
  says which roots it reads:
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugins.ts#L1-L41
  "Roots come from the shared plugin registries (marketplace installs,
  `--plugin-dir`) and from configured extension packages." and
  `const PRIORITY = 75;` with the comment "Above claude-plugins (70) so the
  standard's semantics win for packages that declare it; below claude.ts (80)
  so user-level .claude/ overrides still apply."
- **Source**: the provider stores each skill under its directory name, with
  no prefix:
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugins.ts#L177-L183
  ```ts
  // Validation guarantees the frontmatter name matches the directory
  // (NFKC-normalized), so the on-disk directory name is the identity.
  ...
  items.push({
  	name: entry.name,
  ```
- **Source**: the Claude-format provider states the no-prefix decision in a
  comment:
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/claude-plugins.ts#L249-L253
  ```ts
  // Intentionally do NOT prefix skill names with `root.plugin`.
  // The `plugin:name` format breaks skill:// URL parsing (colons are
  // ambiguous with port separators) and is unintuitive for callers.
  // Dedup-by-key in the capability layer already handles name collisions
  // across providers using priority ordering.
  ```
- **Doc** (`docs/marketplace.md` line 78): "Run `/reload-plugins` to refresh
  skills, slash commands, and MCP servers".
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/docs/marketplace.md

### Are skill names namespaced by plugin?

No. **Doc** (`docs/skills.md`): no passage mentions a plugin prefix.
**Source**: the three quotes above. Skills from every provider share one
namespace keyed by the bare name.

### Two installed plugins both carrying `review`

- **Doc** (`docs/skills.md` line 98): "Dedup key is skill name. First item
  with a given name wins."
- **Source**, the dedup and the warning the loser gets:
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/extensibility/skills.ts#L216-L254
  ```ts
  const seenAuthoredSkillNames = new Set<string>();
  const filteredSkills = result.all.filter(capSkill => {
  	...
  	if (seenAuthoredSkillNames.has(capSkill.name)) return false;
  	seenAuthoredSkillNames.add(capSkill.name);
  ...
  const existing = skillMap.get(capSkill.name);
  if (existing) {
  	collisionWarnings.push({
  		skillPath: capSkill.path,
  		message: `name collision: "${capSkill.name}" already loaded from ${existing.filePath}, skipping this one`,
  ```
- **Source**: within the `agent-plugins` provider, items are sorted by name
  then path before dedup, so between two portable packages the first in that
  order wins:
  https://github.com/can1357/oh-my-pi/blob/ba56afb26280a6a3195c329fa66a3f8fb52f82eb/packages/coding-agent/src/discovery/agent-plugins.ts#L194
  `items.sort((a, b) => compareSkillOrder(a.name, a.path, b.name, b.path));`

Conclusion for Oh-My-Pi: a short name like `review` is ambiguous the moment
any other installed source, at any priority, ships a `review`. The second one
is silently dropped from the prompt and from `/skill:review`, with only a
warning in the load result.

---

## 2. OpenAI Codex CLI

### Where the documentation lives

- `github.com/openai/codex/docs/skills.md` is a one-line pointer: "For
  information about skills, refer to
  [this documentation](https://developers.openai.com/codex/skills)." **Doc:**
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/docs/skills.md
- `developers.openai.com/codex/skills` returns 308 to
  `https://learn.chatgpt.com/docs/build-skills`.
  `developers.openai.com/codex/plugins` returns 308 to
  `https://learn.chatgpt.com/docs/plugins`. Both redirect targets were read.
- `docs/slash_commands.md` in the repository contains no line about `/skills`,
  `/plugins` or `$`. **Not found** there.

### How skills are listed to the model

- **Doc** (https://learn.chatgpt.com/docs/build-skills): "ChatGPT and Codex
  start with each skill's name and description, then load the full `SKILL.md`
  instructions when they decide to use that skill." For Codex, "the initial
  list also includes each skill's file path."
- **Source**, the prompt intro text:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/catalog_prompt.rs#L3-L8
  "Below is the list of skills that can be used. Each entry includes a name,
  description, and source locator." and "Trigger rules: If the user names a
  skill (with `$SkillName` or plain text) OR the task clearly matches a
  skill's description shown above, you must use that skill for that turn."

### Are plugin skill names namespaced?

Yes. The documentation does not say so; the source does.

- **Source**, the rule, stated in the resolver's doc comment:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/loader_namespace.rs#L11-L15
  ```rust
  /// Resolves the namespace prefix applied to skill names during one skills scan.
  ///
  /// A plugin namespace is the plugin name from the nearest valid plugin manifest
  /// above a skill path. For example, a skill named `search` beneath a plugin named
  /// `sample` is exposed as `sample:search`.
  ```
- **Source**, the composition:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/loader_namespace.rs#L176-L181
  ```rust
  pub(crate) fn qualify(&self, base_name: &str) -> String {
      match self {
          Self::Plain => base_name.to_string(),
          Self::Plugin(namespace) => format!("{namespace}:{base_name}"),
  ```
- **Source**, where the namespace comes from — the manifest `name`, falling
  back to the plugin root's directory name when `name` is empty:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/utils/plugins/src/plugin_namespace.rs#L89-L119
  ```rust
  /// Returns the plugin manifest `name` defined directly below `plugin_root`.
  pub async fn plugin_namespace_for_root_uri(
  ...
      Some(
          plugin_root
              .basename()
              .filter(|_| raw_name.trim().is_empty())
              .unwrap_or(raw_name),
      )
  ```
- **Source**, an installed plugin's skill root carries its namespace
  explicitly (`PluginSkillRoot { ..., plugin_namespace: String, ... }`):
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/utils/plugins/src/lib.rs#L34-L41
  and the host loader uses it when present:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/ext/skills/src/loader_host.rs#L272-L275
- **Source**, the model is told about the prefix when a plugin is selected:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/core/src/plugins/render.rs#L38-L45
  ```rust
  if plugin.has_skills {
      let skill_namespace = plugin
          .plugin_namespace
          .as_deref()
          .unwrap_or(plugin.display_name.as_str());
      lines.push(format!(
          "- Skills from this plugin are prefixed with `{skill_namespace}:`."
  ```

### How the user sees and invokes one

- **Doc** (https://learn.chatgpt.com/docs/build-skills): "In Codex CLI or the
  IDE extension, run `/skills` or type `$` to mention a skill."
- **Doc** (https://learn.chatgpt.com/docs/plugins): "In Codex CLI, enter
  `/plugins` to open the plugin browser. Install a plugin from a configured
  marketplace, then start a new session before using its bundled skills or
  tools." The same page says "Type `@` to invoke the plugin or one of its
  bundled skills explicitly." in the ChatGPT section; the build-skills page
  says "ChatGPT supports `@` mentions, while Codex supports `$` mentions for
  skills."
- **Source**, the `$` mention parser accepts `:` inside a name, so
  `$plugin:skill` is one mention:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/skills/src/mentions.rs#L226-L228
  ```rust
  fn is_mention_name_char(byte: u8) -> bool {
      matches!(byte, b'a'..=b'z' | b'A'..=b'Z' | b'0'..=b'9' | b'_' | b'-' | b':')
  ```
- **Source**, the TUI `/skills` list shows a plugin skill as
  `skill-name (plugin-name)` while keeping the qualified name underneath:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/tui/src/skills_helpers.rs#L4-L21
  ```rust
  if let Some((plugin_name, skill_name)) = skill.name.split_once(':')
      && !plugin_name.is_empty()
      && !skill_name.is_empty()
  {
      return format!("{skill_name} ({plugin_name})");
  ```
  used at
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/tui/src/chatwidget/skills.rs#L76-L83

### Collisions

- **Doc** (https://learn.chatgpt.com/docs/build-skills): "If two skills share
  the same `name`, Codex doesn't merge them; both can appear in skill
  selectors."
- **Source**, a plain `$name` text mention is honoured only when exactly one
  enabled skill has that name; otherwise it is skipped:
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/skills/src/selection.rs#L31-L37
  "plain names are only used when the match is unambiguous", and
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/skills/src/selection.rs#L178-L190
  ```rust
  let skill_count = selection_context
      .skill_name_counts
      .get(skill.name.as_str())
  ...
  if skill_count != 1 || connector_count != 0 {
      continue;
  }
  ```
  The counts come from
  https://github.com/openai/codex/blob/549455f3ec5a7f2a0489894543a0e49f307142a6/codex-rs/skills/src/name_counts.rs#L8-L25
  ("Counts how often each skill name appears (exact and ASCII-lowercase)").
- A structured selection from the `/skills` popup resolves by path, not by
  name (same file, lines 61-70), so the picker is never ambiguous.

Conclusion for Codex: two installed plugins each shipping `review` load as
`<plugin-a>:review` and `<plugin-b>:review`. They never collide with each
other, nor with a repository or user `review`, whose name stays bare.

---

## 3. Claude Code

All facts below are **doc**. Source was not needed.

- Prefix on invocation and in listings.
  https://code.claude.com/docs/en/plugins, "Create the plugin manifest":
  `name` — "Unique identifier and skill namespace. Skills are prefixed with
  this (e.g., `/my-first-plugin:hello`)." Same page, "Add a skill": "The
  folder name becomes the skill name, prefixed with the plugin's namespace
  (`hello/` in a plugin named `my-first-plugin` creates
  `/my-first-plugin:hello`)." Same page, "Test your plugin": "Run `/help` and
  open the **Custom commands** tab to see your skill listed under the plugin
  namespace." Note box: "Plugin skills are always namespaced (like
  `/my-first-plugin:hello`) to prevent conflicts when multiple plugins have
  skills with the same name."
- Front-matter `name` replaces the directory segment, and the bare name is
  also reachable. https://code.claude.com/docs/en/skills, "How a skill gets
  its command name": "In a plugin skill, the frontmatter `name` replaces the
  directory name in the last segment of the command, so
  `my-plugin/skills/review/SKILL.md` with `name: fancy` becomes
  `/my-plugin:fancy`. The bare `/fancy` also invokes the skill unless another
  command already uses that name."
- Collision with a personal, project or bundled skill.
  https://code.claude.com/docs/en/skills, table "Resolve skills that share a
  name": "A plugin skill and a skill at any of the locations above — Both
  load, because plugin skills are namespaced as `/plugin-name:skill-name`."
  The plugins page repeats it: "Plugin skills are namespaced as
  `/plugin-name:skill-name`, so the original `/skill-name` and the plugin
  copy both remain available rather than one overriding the other."
- What the model sees. https://code.claude.com/docs/en/skills, "Skill content
  lifecycle": "In a regular session, skill descriptions are loaded into
  context so Claude knows what's available, but full skill content only loads
  when invoked."
- Two plugins both shipping `review`: both are reachable as
  `/<plugin-a>:review` and `/<plugin-b>:review` (the note box above). Which
  of the two, if either, answers the bare `/review` is **not found** in the
  documentation; the skills page says only that the bare form works "unless
  another command already uses that name".

---

## 4. Hermes Agent (github.com/NousResearch/hermes-agent)

### Where the documentation lives

- `https://hermes-agent.nousresearch.com/docs/guides/agent-plugins` returns
  HTTP 404. **Not found.**
- The portable-package section is in the developer guide,
  https://hermes-agent.nousresearch.com/docs/developer-guide/plugins, heading
  "Portable Agent Plugins v1 packages". The user guide for skills is
  https://hermes-agent.nousresearch.com/docs/guides/work-with-skills, heading
  "Plugin-Provided Skills".
- The two pages disagree on one point (below). The source settles it.

### The qualified name and how the namespace is derived

- **Doc** (developer guide, "Portable Agent Plugins v1 packages"): "An
  enabled package may provide immediate skills/*/SKILL.md directories and
  stdio MCP servers from root mcp.json. Skills are read-only, namespaced, and
  loaded through skills_list plus skill_view." "Use skills_list to discover
  the full qualified skill name. Portable skill namespaces have the
  deterministic form agent-plugin-<slug>-<hash>, derived from the discovered
  plugin key so sanitized names cannot collide."
- **Source**, the namespace function:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L79-L88
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
- **Source**, the key the namespace is derived from — the `plugin.json`
  `name` for a package directly under a plugins root, or
  `<category-dir>/<package-dir>` for one nested a level down:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_manifest.py#L455-L467
  ```python
  def portable_plugin_manifest(child: Path, source: str, prefix: str) -> PluginManifest:
      """Build the manifest for a portable Agent Plugin directory (``plugin.json``); diagnostics warn."""
      ...
      key = f"{prefix}/{child.name}" if prefix else data["name"]
      return PluginManifest(
          name=data["name"], ..., key=key,
          portable=True, skill_namespace=_portable_skill_namespace(key),
  ```
  The `prefix` is set by the directory scanner, empty at the top level and
  the intermediate directory name one level down:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_discovery.py#L109-L160
  (`sub_prefix = f"{prefix}/{child.name}" if prefix else child.name`).
- **Source**, the qualified name is `<skill_namespace>:<skill-directory>`:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins.py#L1011-L1040
  ```python
  def register_skill(self, name, path, description="", frontmatter=None):
      """Register a read-only skill resolvable as ``'<plugin_name>:<name>'`` via ``skill_view()``
      and listed by ``skills_list``. Not copied into ``~/.hermes/skills/`` and not in the system
      prompt's ``<available_skills>``. ..."""
      ...
      namespace = self.manifest.skill_namespace or self.manifest.name
      qualified = f"{namespace}:{name}"
      if self.manifest.portable and qualified in self._manager._plugin_skills:
          raise ValueError(f"Plugin skill '{qualified}' is already registered")
  ```
  and the portable loader calls it once per discovered skill:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_loader.py#L551-L566
  ```python
  for skill in package.skills:
      try:
          ctx.register_skill(skill.name, skill.skill_md, skill.description, skill.frontmatter)
  ```
- **Source**, the skill name is its directory name and must match the
  front matter: `hermes_cli/agent_plugins.py` validates the front matter
  against `child.name`:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/agent_plugins.py#L168-L200

Worked example: a package whose `plugin.json` says `"name": "howp"` with a
skill directory `skills/review/` is `agent-plugin-howp-<8 hex>:review`, where
the 8 hex are the first eight characters of `sha256("howp")`.

### How the user lists plugin skills

- **Doc** (developer guide): "hermes plugins install owner/repository
  --no-enable", "hermes plugins list", "hermes plugins enable
  <plugin-name>"; "Portable packages are disabled after installation unless
  you explicitly enable them." "Use skills_list to discover the full
  qualified skill name."
- **Doc** (work-with-skills, "Plugin-Provided Skills"): "Plugin skills are
  not listed in the system prompt and don't appear in skills_list. They're
  opt-in — load them explicitly when you know a plugin provides one."
  **This contradicts the developer guide.**
- **Source** settles it: `skills_list` does include plugin skills, under
  their qualified names, category `plugin`:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/tools/skills_tool.py#L234-L246
  ```python
  def skills_list(category: str = None, task_id: str = None) -> str:
      ...
          for plugin_skill in get_plugin_manager().list_plugin_skill_metadata():
              ...
              all_skills.append(plugin_skill)
  ```
  with the metadata built at
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins.py#L1569-L1576
  (`"name": qualified, ... "category": "plugin"`). They stay out of the
  system prompt's `<available_skills>` (the `register_skill` docstring
  above).
- **Source**, the CLI commands do not print skills. `hermes plugins list`
  prints name, status, version, description and source:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_cmd.py#L1672-L1700
  `hermes plugins show` (alias `info`) prints name, version, description,
  status, source, key, emits, listens — no skills:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_cmd.py#L1814-L1837
  `hermes skills list --source` accepts only `all`, `hub`, `builtin`,
  `local`:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/subcommands/skills.py#L69-L70
  A user-facing command that prints a portable package's qualified skill
  names was **not found** in the files read; the route is the model's
  `skills_list` tool.

### How the user invokes one

- **Doc** (developer guide): `skill_view("agent-plugin-<slug>-<hash>:skill-name")`;
  built-in `skill_view("built-in-skill")` "unchanged".
- **Doc** (work-with-skills): "Every installed skill is automatically a
  slash command. Just type its name", with examples `/ascii-art`, `/plan`.
  For plugin skills: "You can also trigger skills through natural
  conversation — ask Hermes to use a specific skill, and it will load it via
  the `skill_view` tool."
- **Source**, `skill_view` dispatches any name containing `:` to the plugin
  registry:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/tools/skills_tool.py#L576-L586
  ```python
  or path ("axolotl", "03-fine-tuning/axolotl"); "plugin:skill" resolves plugin-provided
  ...
  if ":" in name:  # plugin registry; bare names use the flat-tree scan below
      served, local_category_name = _resolve_plugin_skill(name, file_path, task_id, preprocess)
  ```
- **Source**, slash commands are built only from skill directories (project,
  local `~/.hermes/skills/`, external), never from the plugin registry:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/agent/skill_commands.py#L391-L425
  The file contains no reference to plugin skills. So there is no
  `/<name>` slash command for a portable package's skill in the files read;
  invocation is by the model calling `skill_view` with the qualified name,
  or by the user asking for it in prose. A slash route was **not found**.
- **Source**, when a plugin skill is loaded, a banner names its siblings:
  https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/tools/skills_tool_plugin.py#L147-L152
  "[Bundle context: This skill is part of the '{namespace}' plugin." ...
  "Use qualified form to invoke siblings".

### Collisions

- **Doc** (work-with-skills): "Plugins can bundle their own skills using
  namespaced names (`plugin:skill`). This prevents name collisions with
  built-in skills."
- **Source**: two different packages each shipping `review` get different
  namespaces (the sha256 of different keys), so both register. Only the same
  qualified name twice is refused (`register_skill`, quoted above), and the
  loader then logs "Agent Plugin '%s' skill '%s' skipped" and continues
  (`plugins_loader.py` lines 564-566).

---

## What could not be reached or was not found

- Oh-My-Pi `docs/plugins.md`: HTTP 404 on `main`; `docs/marketplace.md`
  stands in for it.
- Oh-My-Pi: the rendered format of a skill entry in the system prompt was
  not read.
- Codex: `developers.openai.com/codex/{skills,plugins}` both redirect (308)
  to `learn.chatgpt.com`; the redirect targets were read. No documentation
  page states that plugin skills carry a `<plugin>:` prefix; that fact is
  from source only. `docs/slash_commands.md` in the repository says nothing
  about `/skills`.
- Claude Code: which plugin answers the bare `/review` when two plugins ship
  it is not stated in the documentation.
- Hermes: `docs/guides/agent-plugins` is HTTP 404. The two documentation
  pages contradict each other on whether `skills_list` shows plugin skills;
  the source says it does. No user-facing command that prints a package's
  qualified skill names was found, and no slash-command route to a plugin
  skill was found.
- No client was run. Every fact above is from reading documentation or
  source at the pinned commits.
