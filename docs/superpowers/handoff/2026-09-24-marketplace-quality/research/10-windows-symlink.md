# Symlinked vendor manifest on Windows: what the sources say

Researched 2026-09-25 from public documentation and source only. No repository
access was used. Each fact is tagged **[doc]**, **[source]** or **[not found]**.
Source citations are commit permalinks. Nothing below was verified by running
a client; every claim is what a text says.

Working copies of everything read are under
`/private/tmp/claude-501/-Users-akurganow-Projects-ai-plugins/aa53b02e-f388-4b09-bc13-baf4eb5c52bb/scratchpad/`.

## 1. Git on Windows and mode 120000 entries

**What `core.symlinks` does. [doc]** The git manual, `core.symlinks`:
"If false, symbolic links are checked out as small plain files that contain
the link text. git-update-index and git-add will not change the recorded type
to regular file. Useful on filesystems like FAT that do not support symbolic
links. The default is true, except git-clone or git-init will probe and set
core.symlinks false if appropriate when the repository is created."
Read at https://git-scm.com/docs/git-config#Documentation/git-config.txt-coresymlinks,
and verbatim from the manual source at tag v2.51.0:
https://github.com/git/git/blob/c44beea485f0f2feaf460e2ac87fdd5608d63cf0/Documentation/config/core.adoc
lines 237-246.

**Git for Windows default. [doc]** https://gitforwindows.org/symbolic-links:
"Short version: there is no exact equivalent for POSIX symlinks on Windows,
and the closest thing is unavailable for non-admins by default unless
Developer Mode is enabled and a relatively recent Windows 10 version is used.
Therefore, symlink emulation support is only turned on by default when that
scenario is detected. Support can be enabled by the user, via the
core.symlinks=true config setting." Later: "For those reasons, Git for
Windows disables support for symbolic links by default (it will still read
them when it encounters them). You can enable support via the core.symlinks
config variable, e.g. when cloning: git clone -c core.symlinks=true <URL>".

**Privilege. [doc]** Same page: "You need the SeCreateSymbolicLinkPrivilege
privilege, which is by default assigned only to Administrators and guarded by
UAC, but can be assigned to other users or user groups". And: "Since Windows
10 version 1703 (Creators Update), enabling Developer Mode will disable this
restriction and allow creating symlinks without UAC elevation".

**The installer option. [source]** The page does not describe the installer
checkbox; the installer script does.
https://github.com/git-for-windows/build-extra/blob/c8241c75c7c06d6db94ed6a8dd9b8ca76d1ed842/installer/install.iss:
- Line 2454 creates the checkbox "Enable symbolic links" with the caption
  "(requires the SeCreateSymbolicLink permission). Please note that existing
  repositories are unaffected by this setting."
- Lines 2459-2467: the choice defaults to `Auto`; `Auto` resolves through
  `EnableSymlinksByDefault()`.
- Lines 1342-1369, `EnableSymlinksByDefault()`: returns true when the
  registry value `HKLM\SOFTWARE\Microsoft\Windows\CurrentVersion\AppModelUnlock\AllowDevelopmentWithoutDevLicense`
  is 1 and the Windows build is >= 14972 (comment: "Developer mode enabled").
  When the installer runs as admin it returns false ("detection only works
  when we're not running as admin"). Otherwise it runs `mklink /d` in `%TEMP%`
  as the original user and returns true only if the link was created.
- Lines 3296-3300: the checkbox writes `core.symlinks` `true` or `false` into
  the **system** git config (`GitSystemConfigSet('core.symlinks',Cmd)`).
- Unattended installs pass `/o:EnableSymlinks=Enabled` (this is what GitHub's
  runner images do; see §3).

**Net effect on a default checkout.** On a stock Windows machine without
Developer Mode, the installer's `Auto` resolves to `Disabled`, the system
config carries `core.symlinks=false`, and per the manual every mode 120000
entry is checked out as a plain file whose content is the link text. For the
marketplace in question that file is `plugins/<name>/.claude-plugin/plugin.json`
containing `../plugin.json`. With Developer Mode on, or the privilege
assigned and the box ticked, the entry becomes a real symlink. Even with
`core.symlinks=true` in config, `git clone`/`git init` may probe and set it
false per repository if creation fails (manual, lines 244-246). **[not
found]**: no source states what the probe does when config says true but
the privilege is absent; the manual says only "if appropriate".

## 2. Claude Code marketplaces and the manifest path

**Fetch mechanism: git clone. [doc]** https://code.claude.com/docs/en/plugin-marketplaces
(Markdown copy `cc-plugin-marketplaces.md`, line 760): "When users add a
marketplace hosted in a git repository, or install a git-based plugin it
lists, Claude Code clones that marketplace or plugin repository onto their
machine. The clone never downloads Git LFS content, so LFS-tracked files
arrive as pointer files." Line 786: "GitHub `owner/repo` shorthand sources
clone over SSH by default; set `CLAUDE_CODE_PLUGIN_PREFER_HTTPS=1` to clone
them over HTTPS instead." Line 371: `git-subdir` "uses a sparse, partial
clone". Line 266: only the `archive` source "Works without git or npm on the
user's machine". Line 1506: timeouts surface as "Git clone timed out after
120s". https://code.claude.com/docs/en/discover-plugins, "Add from other Git
hosts": Claude Code "clones" GitHub, GitLab and Azure DevOps URLs; a bare
`marketplace.json` URL is downloaded instead, and then relative paths do not
resolve (plugin-marketplaces, "Plugins with relative paths fail in URL-based
marketplaces").

**Manifest location: `.claude-plugin/plugin.json` only. [doc]**
https://code.claude.com/docs/en/plugins-reference, "Plugin manifest schema":
"Location: `.claude-plugin/plugin.json` in plugin root". The file-locations
table lists the manifest at that path and nowhere else. The warning under
"Standard plugin layout": "The `.claude-plugin/` directory contains the
`plugin.json` file. All other directories ... must be at the plugin root, not
inside `.claude-plugin/`." **[not found]**: neither plugins-reference,
plugins, plugin-marketplaces nor discover-plugins mentions a root
`plugin.json`, "Agent Plugins", "agent-plugins.org", "portable" or "vendor"
(grep over the Markdown copies). The Claude Code changelog at commit
684ffc4da0eaaddcafa61842dc719c6a8febc5c2 also has no entry mentioning Agent
Plugins or a root manifest. So the question "which wins" has no documented
answer: only one path is read.

**What a corrupt manifest does. [doc]** plugins-reference line 1454:
"`Plugin <name> has a corrupt manifest file at .claude-plugin/plugin.json.
JSON parse error: ...`: JSON syntax error." Line 1441: "Plugin not loading |
Invalid `plugin.json`". A text file reading `../plugin.json` is not JSON.

**Symlinks. [doc]** plugins-reference, "Share files within a marketplace with
symlinks" (lines 915-925): "Within the plugin's own directory: the symlink is
preserved as a relative symlink in the cache, so it keeps resolving to the
copied target at runtime." "Elsewhere within the same marketplace: the
symlink is dereferenced." "Outside the marketplace: the symlink is skipped
for security." Then: "On Windows, use `mklink /D` from an elevated Command
Prompt or enable Developer Mode". Line 907: a "symlink that leads outside the
plugin" is rejected. plugin-marketplaces line 644: "Claude Code doesn't
support link mode on Windows and refuses to install a link-mode plugin
there." **[not found]**: nothing says what Claude Code does when a symlink
arrives from `git clone` as a text file, and nothing mentions
`core.symlinks`. The Windows sentence above is about creating links as an
author, not about checking them out as a user.

## 3. `actions/checkout` on `windows-latest`

**The action runs git. [doc]** README at
https://github.com/actions/checkout/blob/f548e57e544e1ff5a4c46bf1e1b8685f8e4a348a/README.md
line 35: "When Git 2.18 or higher is not in your PATH, falls back to the REST
API to download the files." **[source]** `grep -rni symlink src/` at that
commit returns nothing: the action sets no `core.symlinks` and handles
symlinks nowhere itself. Checkout behaviour is therefore the runner's Git.

**The runner's Git has symlinks enabled. [source]**
https://github.com/actions/runner-images/blob/ebade26c60adcb867918b31c8f8caa37343a3d39/images/windows/scripts/build/Install-Git.ps1
lines 27-37 install Git for Windows with `"/o:EnableSymlinks=Enabled"`. That
argument was added by https://github.com/actions/runner-images/pull/1186,
"Install Git for Windows with symbolic links enabled", merged 2020-07-07, PR
body: "Bug fix: enable symlink support of Git for Windows". Per §1 the option
writes `core.symlinks=true` to the system config. README line 37 at the same
commit maps `windows-latest` to Windows Server 2025; `Windows2025-Readme.md`
line 67 lists "Git 2.55.0.windows.5".

**Caveat. [not found]** No actions/checkout documentation or issue found
states whether the checkout produces real links or text files. GitHub issue
searches (`repo:actions/checkout symlink windows`, `repo:actions/runner-images
core.symlinks`, `symlink "text file" windows-latest checkout org:actions`)
returned no report either way. The only inference available is: config says
true, the runner user's privilege decides, and git's clone-time probe (§1)
decides per repository. Not verified by running a workflow.

## 4. Codex CLI, Hermes Agent, Oh-My-Pi

### OpenAI Codex CLI

**Fetch: git clone. [doc]** https://developers.openai.com/plugins/build/plugins,
"Add a marketplace from the CLI": `codex plugin marketplace add owner/repo`,
`--ref`, `--sparse`; "Marketplace sources can be GitHub shorthand (owner/repo
or owner/repo@ref), HTTP or HTTPS Git URLs, SSH Git URLs, or local
marketplace root directories." Installs land in
"`~/.codex/plugins/cache/$MARKETPLACE_NAME/$PLUGIN_NAME/$VERSION/`". The page
does not say the word "clone". **[source]** At commit
dda227891d27b6e0f3f244eda149a98d098969ad:
https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/core-plugins/src/marketplace_add/install.rs
lines 7-45 run `git clone url destination` (or `clone --filter=blob:none
--no-checkout` plus `sparse-checkout set` when sparse paths are given), and
https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/core-plugins/src/loader.rs
lines 1831-1862 do the same for plugin sources, with `git checkout <sha>` and
a `rev-parse HEAD` check when a sha is pinned. Both spawn the `git` binary.

**Manifest paths and precedence. [doc]** Same docs page: "For a portable
Agent Plugins package, add plugin.json at the plugin root and declare the
Agent Plugins schema." "Existing .codex-plugin/plugin.json files remain
supported as a compatibility fallback." Marketplaces: "$REPO_ROOT/.agents/plugins/marketplace.json",
"a legacy-compatible marketplace at $REPO_ROOT/.claude-plugin/marketplace.json",
"~/.agents/plugins/marketplace.json". **[source]**
https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/utils/plugins/src/plugin_namespace.rs
lines 43-80, `find_plugin_manifest_path`: root `plugin.json` is checked first
via `symlink_metadata`; a symlink or non-file root manifest returns `None`
(the plugin is rejected); a regular file whose `$schema` starts with
`https://agent-plugins.org/schemas/` is used; otherwise the fallbacks in
`DISCOVERABLE_PLUGIN_MANIFEST_PATHS` are tried in order
`.codex-plugin/plugin.json`, `.claude-plugin/plugin.json`,
`.cursor-plugin/plugin.json`
(https://github.com/openai/codex/blob/dda227891d27b6e0f3f244eda149a98d098969ad/codex-rs/exec-server-protocol/src/protocol.rs
lines 49-53), each also required to be a regular file, not a symlink. Test
`rejects_symlinked_root_plugin_manifest` (line 253) pins the root rule. So a
package with a real root `plugin.json` carrying the Agent Plugins `$schema`
never reaches the `.claude-plugin` fallback.

**Windows and symlinks in docs. [not found]** The build-plugins page and
https://learn.chatgpt.com/docs/plugins mention neither. The repository's
`docs/` at dda2278 holds 15 files; none contains the word "plugin". The
marketplace docs page `https://learn.chatgpt.com/docs/plugins/marketplace`
(target of the `/codex/plugins/marketplace` redirect) returned 404 on
2026-09-25. `core.symlinks` appears nowhere in the plugin crates.

### Hermes Agent (NousResearch/hermes-agent)

**Fetch: shallow git clone. [doc]** User guide (repo file
`website/docs/user-guide/features/plugins.md` at
749220ef0007f8d87bd1531f1c24b0fe93816385, lines 164-168 and 219-221; the
live URL for this file was not probed): a `clone_timeout_seconds` setting
"for each Git clone, fetch or checkout"; "`hermes plugins install` clones
non-interactively". Catalog page
https://hermes-agent.nousresearch.com/docs/user-guide/features/plugin-catalog
(repo file lines 48-49, 123): catalog entries carry `repo` and `sha`, "The
exact 40-hex commit that was reviewed — installs check out this pin, not a
branch tip". **[source]**
https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_cmd.py
lines 694-730: `git clone --depth 1 [--filter=blob:none] [--no-checkout] <url>`,
then sparse checkout for a subdirectory and `checkout --detach <sha>` for a
pin; "git is not installed or not in PATH." is the failure when no git.

**Manifest path: root `plugin.json` only. [doc]**
https://hermes-agent.nousresearch.com/docs/developer-guide/plugins/ (HTTP
200; repo file `website/docs/developer-guide/plugins/index.md` lines 45-110):
"Hermes can also install and load directory packages that target the Agent
Plugins v1.0.0 format." Layout shows `plugin.json` at the root. "Hermes
validates `plugin.json`, Agent Skills frontmatter, fixed component locations,
`mcp.json`, resolved paths, and symlink containment locally." Line 748:
"Portable packages use root `plugin.json` in the same locations." Line 110:
"This is an explicit supported subset, not a claim of full Agent Plugins
conformance." **[source]**
https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/agent_plugins.py
lines 152-155: `manifest_path = root / "plugin.json"`; "plugin.json must be a
regular file within the plugin root".
https://github.com/NousResearch/hermes-agent/blob/749220ef0007f8d87bd1531f1c24b0fe93816385/hermes_cli/plugins_discovery.py
lines 30-36: `.claude-plugin`, `.codex-plugin`, `.cursor-plugin`,
`.devin-plugin`, `.kimi-plugin` are listed as `_FOREIGN_HARNESS_MANIFEST_DIRS`
with the comment "Their plugin.json is not an Agent Plugins v1 manifest and
can never validate, so parsing it on every discovery pass only spams
warnings". Hermes never reads `.claude-plugin/plugin.json`.

**Windows. [not found]** `website/docs/user-guide/windows-native.md` exists
and mentions plugins only in passing (a symlinked bash path, a PID API note);
it says nothing about installing plugins or about symlinks in packages.

### Oh-My-Pi (`@oh-my-pi/pi-coding-agent`)

Repository https://github.com/can1357/oh-my-pi, default branch `main`, head
4a7b586821a4df0afcea657717247f6ec9db8f88 on 2026-09-24; package name
confirmed in `packages/coding-agent/package.json`. The live page
https://omp.sh/docs/marketplace returned 200 but its extracted text contained
none of the marketplace content (client-rendered), so the in-repo docs are
cited instead.

**Fetch: git clone via the git CLI. [doc]**
https://github.com/can1357/oh-my-pi/blob/4a7b586821a4df0afcea657717247f6ec9db8f88/docs/marketplace.md
line 16: "A marketplace is a Git repository (or local directory) containing a
catalog file at `.omp-plugin/marketplace.json` (preferred) or
`.claude-plugin/marketplace.json` (Claude Code-compatible fallback)." Lines
86-92: `owner/repo` is GitHub shorthand; `https://...` is a "Git repository
unless the URL path ends in `.json`"; "Direct catalog URLs cache only the
JSON catalog". Line 231: "Cached marketplace clone/catalog". **[source]**
https://github.com/can1357/oh-my-pi/blob/4a7b586821a4df0afcea657717247f6ec9db8f88/packages/coding-agent/src/extensibility/plugins/marketplace/fetcher.ts
line 249: "GitHub/git sources are cloned with `git`; URL sources are fetched
over HTTP."; line 300 calls `vcs.clone(url, tmpDir, ...)`.
https://github.com/can1357/oh-my-pi/blob/4a7b586821a4df0afcea657717247f6ec9db8f88/packages/natives/native/vcs.js
lines 88-91: "Clone a repository (git CLI under the hood for credential
parity)." The native body behind `vcsGitClone` was not located in the clone.

**Manifest paths. [source]** Two providers exist.
- `claude-plugins` provider,
  https://github.com/can1357/oh-my-pi/blob/4a7b586821a4df0afcea657717247f6ec9db8f88/packages/coding-agent/src/discovery/claude-plugins.ts
  line 86: `path.join(root.path, ".claude-plugin", "plugin.json")`; lines
  476-477 read `.omp-plugin/plugin.json` then `.claude-plugin/plugin.json`.
  This provider reads no root `plugin.json`; the report that it reads only
  that path is confirmed. Lines 91-95: a manifest that fails `JSON.parse`
  yields `null` (treated as absent, no error).
- `agent-plugins` provider,
  https://github.com/can1357/oh-my-pi/blob/4a7b586821a4df0afcea657717247f6ec9db8f88/packages/coding-agent/src/discovery/agent-plugin-format.ts
  lines 508-515: resolves root `plugin.json` and proves containment "BEFORE
  reading it" ("Spec §4.1 failure boundary 1"); a manifest resolving outside
  the root is `invalid`. Lines 540-552, `legacyProviderAllowed`: when the root
  is a standard Agent Plugins package, skills and MCP are exclusive to the
  standard loader and the `claude-plugins` provider gets only "other"
  surfaces; an invalid package is rejected entirely. Line 562-564 comment:
  "a `.omp-plugin/plugin.json` (OMP-native) or an Agent Plugins standard root
  `plugin.json` wins over a sibling `.claude-plugin/plugin.json`."
- `--plugin-dir` roots,
  https://github.com/can1357/oh-my-pi/blob/4a7b586821a4df0afcea657717247f6ec9db8f88/packages/coding-agent/src/discovery/helpers.ts
  lines 1396-1405: name is read from `.claude-plugin/plugin.json` first, then
  root `plugin.json`, each "proven inside the plugin directory BEFORE the
  read (Agent Plugins §4.1)".

**Windows. [not found]** `docs/marketplace.md` and
`docs/plugin-manager-installer-plumbing.md` contain no "Windows" mention;
`core.symlinks` appears nowhere in the repository's `.ts` or `.md` files.

## 5. Agent Plugins specification, sections 4 and 5

Read at https://agent-plugins.org/specification (WebFetch summary) and
verbatim from
https://github.com/agentplugins/agent-plugins-spec/blob/ff8ab5e392cc87bd88d87c060815a87490e51003/spec/1.0.0.md
(head of `main` on 2026-08-19). Section 1: "This specification defines
version `1.0.0` of the Agent Plugins format." The same commit also carries
`spec/1.1.0.md`, "Status: Working Draft".

**§4.1 (line 62). [doc]** "When a client discovers, reads, or executes a file
or directory supplied by the plugin package, the filesystem-resolved path
MUST remain within the filesystem-resolved plugin root. Symlinks, junctions,
reparse points, and equivalent filesystem mechanisms MAY resolve to targets
within the plugin root, but clients MUST reject package paths that resolve
outside it." Lines 98-104, failure boundaries: "1. If `plugin.json` does not
resolve within the plugin root, the client MUST reject the plugin." "3. If a
discovered `SKILL.md` does not resolve within the plugin root, the client
MUST skip that skill under §7.1."

**§5.1 (lines 133-137). [doc]** "Clients MUST check for a manifest at
`plugin.json` in the plugin root." "The Agent Plugins core specification
defines exactly one portable manifest per plugin. No other file can replace,
supplement, or override the core fields in root `plugin.json`." "A client
loads and validates root `plugin.json` before discovering components or
applying client-specific behavior."

**Vendor discovery paths. [not found in the spec]** The spec never names
`.<vendor>-plugin/plugin.json` or `.claude-plugin/`. The only client-specific
mechanism is §8 (lines 401-447): "Client-specific files MUST be represented
under a top-level directory named for that namespace", with a reverse-domain
name such as `com.example.client/`; "Agent Plugins assigns no portable
discovery, validation, loading, or failure semantics to client extension data
or files." A `.claude-plugin/` directory is therefore outside the spec's
vocabulary: neither forbidden nor given any meaning. The spec's one symlink
sentence (§4.1) constrains where a link may resolve, not whether a link may
exist; a link to `../plugin.json` from inside the package resolves inside the
root and is permitted by that clause. §6.2 (line 265) adds that a fixed
location "present but does not resolve to the expected filesystem kind" makes
that component type invalid, which is the spec's only statement about a path
that exists as the wrong kind of file. Nothing in the spec mentions Windows
beyond §7.2.1's `.bat`/`.cmd` launcher note.

## Conclusion

On a default Windows checkout the vendor manifest is a text file, not a link.
Git for Windows installs with `core.symlinks=false` unless Developer Mode is
on or a non-admin `mklink` test succeeds at install time (install.iss lines
1342-1369, 2459-2467, 3296-3300), and with that setting git writes every mode
120000 entry "as small plain files that contain the link text" (git manual).
Every client here fetches with `git clone` on the user's machine (Claude Code
docs line 760; Codex `install.rs`/`loader.rs`; Hermes `plugins_cmd.py`;
Oh-My-Pi `fetcher.ts`), so all of them inherit that checkout. Who is
affected: **Claude Code**, because it reads only `.claude-plugin/plugin.json`
and a file containing `../plugin.json` produces its documented "corrupt
manifest file ... JSON parse error" load failure. **Oh-My-Pi's
`claude-plugins` provider** reads the same path but swallows the parse
failure as "no manifest", while its `agent-plugins` provider reads the real
root `plugin.json` and takes precedence for skills and MCP. **Codex** and
**Hermes** are unaffected: both read the root `plugin.json` first, Codex
never consults the `.claude-plugin` fallback when the root manifest carries
the Agent Plugins `$schema`, and Hermes explicitly ignores `.claude-plugin/`.
On **GitHub Actions `windows-latest`** the image installs Git with
`EnableSymlinks=Enabled` (PR #1186), so the config says true and a real link
is the expected outcome, but no source confirms it and git's clone-time probe
can still turn it off; that case is not verified. The Agent Plugins spec
neither requires nor forbids the vendor path; it only requires that whatever
resolves, resolves inside the root, which `../plugin.json` does.
