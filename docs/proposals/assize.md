# Proposal: `assize` — a package of adversarial review roles

**Status: proposal.** Nothing described here is implemented. No package named
`assize` exists in `plugins/`, no skill has been written, and no client has
loaded any of it. Every install path below is quoted from a client's own
documentation or its own source, per `.agents/rules/claims.md`, and the
[Sources](#sources) section says which kind each one is. Where a client was
not checked, this document says so instead of guessing.

The subject is a family of unattended review roles — the police, the
prosecutor, the defender, the judge — that today exist as six cloud routines
against two repositories, each one a single prompt of roughly twenty thousand
characters stored in an account, and nowhere else.

## 1. What is actually being packaged

The routines conflate three things that have different lifetimes, different
owners, and — decisively — different portability:

1. **The role.** What an abstraction finding *is*; what separates a logic
   error from a style preference; the rules of evidence in a trial; the
   doctrine that filing nothing is a successful run. This is durable,
   repository-agnostic, and it is the part worth versioning.
2. **The repository's facts.** Which commands verify a change here; which
   paths are never edited by hand; which labels exist; what the search
   excludes. This changes per repository and belongs to that repository.
3. **The schedule.** Weekly at 03:00 UTC, against `owner/repo`, in this cloud
   environment. This belongs to an account, and no plugin format in existence
   can carry it (§5 below).

Today all three live inside one opaque prompt. That has four costs, and they
are the argument for doing this at all:

- **The prompts are not reviewable.** Twenty thousand characters of procedure
  that decides what gets filed against a repository sit outside version
  control. They cannot be diffed, reviewed in a pull request, blamed, or
  reverted.
- **The roles cannot be run on demand.** There is no way to say "run the
  abstraction police over this crate now". The role exists only as something
  a cron fires.
- **Every new repository is a copy-paste.** The two Issue Court prompts
  already differ in ways that are drift rather than intent, and the four
  police prompts repeat the same GitHub-over-REST recipes, the same
  `/tmp/run` state discipline, the same backpressure table, and the same
  fingerprint protocol, four times each.
- **The environment rules are load-bearing and invisible.** "Never run `gh
  auth status`", "the clone is shallow", "keep your state in files, not in
  your context" are hard-won and are currently re-derived by hand into each
  new prompt.

The proposal is to move (1) into a versioned package, move (2) into the
repository being policed, and shrink (3) to a stub that names a role and a
repository. A routine's prompt becomes two lines; everything else becomes
text that arrives through a pull request.

## 2. The constraint that decides the shape

The obvious design — "a plugin that ships a set of agents" — is not
available, and the standard is explicit about why.

Agent Plugins 1.0.0 §7: "Agent Plugins v1 defines exactly two component
types: **skills** and **MCP servers**. Other component types are outside the
v1 format and do not affect conformance." Its design notes name this case
directly: "Other proposed component types — such as commands, hooks,
**agents**, rules, and LSP servers — remain too client-specific for a stable
portable contract and are outside the v1 format until their formats
converge." §6.1's fixed-location table has exactly two rows, `skills/` and
`mcp.json`. The 1.1.0 working draft changes neither the table nor that
paragraph.

So the portable substance of this package is **skills**. An agent file is a
per-client projection of a skill, shipped where that client looks for one, and
it is a convenience rather than the product. Concretely: a host with
subagents gets `@assize:prosecutor` as an addressable agent; a host without
gets the same brief handed to whatever the skill can spawn, or run in
sequence in one context. The skill works everywhere; the agent file works
where the client has the concept.

That inversion — skills first, agents as a projection — is the whole design
decision, and everything below follows from it.

## 3. Three layers

### Layer 1 — the package (portable, versioned, installed)

One plugin, `plugins/assize/`, whose skills are the roles. Repository-
agnostic: a role skill never names a crate, a verification command, or a
label.

### Layer 2 — the charter in the policed repository (per-repo, committed)

A single file the role skills read, proposed as `.agents/assize.yaml` in the
target repository — the same `.agents/` tree this repository already uses for
`rules/`, `policies/` and `modes/`. It declares what a role cannot know:

- the verification commands, exactly, and the traps in them (this repository's
  own `.agents/rules/verification.md` is the model);
- paths that are never edited by hand, and therefore never a finding;
- search exclusions;
- labels the roles may use, and the backpressure caps;
- whether GitHub is reachable through session tools, `gh api` REST, or not at
  all;
- which rule files the role must read before analysing anything.

A role skill that finds no charter runs in a reduced mode and **says so in its
report**. It never invents a verification command — the standing rule in
`.agents/rules/claims.md` applied to a machine: declining to check is a
correct outcome, a plausible invented command is not.

### Layer 3 — the schedule (per-account, not shippable)

Unchanged in mechanism, reduced in content. A routine's prompt becomes:

    Run the `assize:dependency-police` skill against this repository,
    following it exactly. Report in the shape it specifies.

Everything a reviewer would want to argue with now lives in a file with a
history.

## 4. The roster

Two families and one setup role. Each is one skill directory.

**The police** — periodic, read-only, adversarial towards their own findings,
and biased hard towards silence. Each sweeps, verifies, hands surviving
candidates to clean-context subagents for independent triage, and files at
most what a backpressure cap allows.

| Skill | Looks for |
| :-- | :-- |
| `dependency-police` | updates that let the repository *delete* code, not updates for their own sake |
| `abstraction-police` | dead, superfluous, wrong or duplicated abstractions, each with a regression-free removal plan |
| `logic-police` | logic errors, reproduced before they are believed |
| `repo-police` | documentation, manifest and marketplace hygiene; unbacked compatibility claims; generated filler |

A fifth is worth considering for this repository specifically: a
`claims-police` that enforces `.agents/rules/claims.md` — every statement
about a client carries a citation, of a stated kind, at a pinned revision.
That rule is currently enforced by the owner reading carefully.

**The court** — one issue per run, tried adversarially, one comment posted,
nothing modified.

| Skill / brief | Role |
| :-- | :-- |
| `issue-court` | the clerk: builds the case file, runs the proceedings, vets expert briefs for leading questions, posts the comment |
| `prosecutor` | argues the issue is wrong or not actionable; bears the burden |
| `defender` | argues it is real and worth acting on; steelmans a badly written report |
| `judge` | fresh context, strikes unexhibited assertions, re-runs the decisive exhibit itself, returns a structured verdict |
| expert witnesses | spec expert, host-agent expert, verification engineer, archaeologist, docs-standards expert — commissioned blind, capped, and every report enters the record in full whatever it says |

The clerk is a skill. The prosecutor, defender and judge are **briefs held as
reference files inside the `issue-court` skill**, and additionally shipped as
agent files for the clients that have subagents. That way the trial runs
identically whether the host can spawn three isolated contexts or has to run
them in sequence — and where it can, `@assize:prosecutor` is directly
addressable by a human who wants to argue with one side by hand.

**`assize-muster`** — the setup role. Given a repository, it writes the
Layer 2 charter by reading what the repository actually has, then sets up
Layer 3 on whichever surface is available: routines on Claude, a scheduled
GitHub Actions workflow anywhere else. This is the part of the ask that reads
"a set of agents for configuring routines in different repositories", and
making it a skill rather than a document is what makes it work on every host.

**`assize-charter`** — not a role. The doctrine every other skill repeats
today, held once: the GitHub-over-REST recipes and why `gh issue list` is not
used, the shallow-clone fetch, the "keep state in files, not in your context"
discipline, the backpressure table, the fingerprint-and-dedup protocol, the
untrusted-input rule for issue bodies and fire payloads, the fixed report
shape, and the doctrine that a run which files nothing is a successful run.
Every role skill's first instruction is to read it.

### Why the shared charter is a sibling skill and not a copy

Three ways to share text across skills were considered:

1. **Duplicate it in each skill.** What the routines do today. Four copies
   drift; three already have.
2. **Generate the skills from fragments.** Rejected: `.agents/rules/
   conformance.md` forbids built artefacts in the tree, and a generated
   `SKILL.md` is one.
3. **A sibling skill directory, referenced by relative path.** Each role skill
   opens with "read `../assize-charter/SKILL.md` before anything else".

(3) resolves in every install path that copies the whole `skills/` tree —
which is all of them, including OpenCode's, provided the documented command
copies every skill directory rather than one. It needs no symlink, no
generation, and no duplication. It is the recommendation.

### Skill naming

Claude namespaces plugin skills as `/assize:dependency-police`, so a
`assize-` prefix on every directory would read as `/assize:assize-…`.
But OpenCode's vendor-neutral location, `~/.agents/skills/<name>/`, is a flat
namespace shared with every other package, where `charter` and `muster` are
collisions waiting to happen. Proposed split: role skills unprefixed
(`dependency-police`, `issue-court`), the two generic ones prefixed
(`assize-charter`, `assize-muster`).

## 5. What no plugin format carries: the schedule

Worth stating plainly, because it is the one thing a reader will expect the
package to do and it cannot. None of the four target formats has a component
type for "run this weekly":

- Agent Plugins 1.0.0 §6.1: two fixed locations, `skills/` and `mcp.json`.
- Claude Code's plugin components are skills, commands, agents, hooks, MCP,
  LSP, monitors, `bin/` and `settings.json` — no schedule. Claude Code's
  schedules are **routines**, which belong to a claude.ai account, not to a
  repository or a package.
- Codex's plugin manifest resolves `skills`, `mcp_servers`, `apps` and
  `hooks` — no schedule and, notably, no agents either.
- Gemini CLI extensions carry commands, hooks, skills, sub-agents, themes and
  policies — no schedule.
- OpenCode's agents are user or project configuration, not package content.

So Layer 3 is set up, never shipped, and `assize-muster` exists precisely
because that step cannot be packaged. Its two honest targets are Claude
routines and a scheduled GitHub Actions workflow committed to the policed
repository — the second being the only mechanism that works for Codex,
OpenCode and Gemini alike.

## 6. Proposed layout

```text
plugins/assize/
  plugin.json                       Agent Plugins 1.0.0, at the plugin root
  .claude-plugin/plugin.json        symlink → ../plugin.json (as howp does)
  skills/
    assize-charter/SKILL.md       the shared doctrine
    assize-muster/SKILL.md        writes the charter, sets up the schedule
    dependency-police/SKILL.md
    abstraction-police/SKILL.md
    logic-police/SKILL.md
    repo-police/SKILL.md
    issue-court/
      SKILL.md                      the clerk's procedure
      references/
        prosecutor.md               the brief, verbatim
        defender.md
        judge.md
        experts.md
  agents/                           Claude Code and Gemini CLI subagents
    prosecutor.md
    defender.md
    judge.md
  gemini-extension.json             Gemini CLI extension manifest
  README.md
```

`skills/` and `plugin.json` are the conformant core. `agents/` and
`gemini-extension.json` are client surface, and §7.4 below says what that
costs.

## 7. Per-surface support

Every row is what that client's own documentation or source says, at the
revision linked in [Sources](#sources). Nothing in this table has been
executed against a published copy of a package that does not yet exist.

### 7.1 Claude Code — terminal

Skills from `skills/`, agents from `agents/*.md` at the plugin root, both
documented. Install is the marketplace path this repository already
documents in `README.md`. Routines are created from the CLI with `/schedule`.
This is the only surface where all three layers have first-class support.

### 7.2 Claude Code on the web — the cloud surface the routines already run on

The important difference: `/plugin` does not exist there. Claude Code's own
documentation gives the substitute — "If Claude replies that `/plugin` isn't
available in this environment, use the plugin browser in the Claude desktop
app, or declare the plugin under `enabledPlugins` in `.claude/settings.json`
for cloud sessions" — paired with `extraKnownMarketplaces` in the same file:

```json
{
  "extraKnownMarketplaces": {
    "ai-plugins": { "source": { "source": "github", "repo": "Akurganow/ai-plugins" } }
  },
  "enabledPlugins": { "assize@ai-plugins": true }
}
```

That file is committed to the *policed* repository, which is exactly the
repository a routine clones, so the package arrives with the clone. Two
sentences from the routines documentation make the layering work: a routine
session "can run shell commands, use skills committed to the cloned
repository, and call any connectors you include", and "Subagents defined in
your repo's `.claude/agents/` are picked up automatically". A repository can
therefore carry the roles even with no plugin installation at all — which is
the fallback if `enabledPlugins` turns out not to resolve an external
marketplace in a cloud session. **That is the one claim in this section that
should be executed before it is published**; the documentation says
marketplace-sourced plugins are not installed by adding the marketplace
alone, and whether a cloud session performs the install has not been checked.

### 7.3 Codex

Codex reads Agent Plugins manifests and this repository's marketplace index —
the ground `README.md` already covers. What it means here: **the skills
install and the agents do not**. Codex's plugin manifest resolves exactly
`skills`, `mcp_servers`, `apps` and `hooks`, and its loader's default
component paths are `skills`, `hooks/hooks.json`, `.mcp.json` and
`.app.json`. No agent or subagent component appears in either. Skill
discovery for an Agent Plugins manifest is `SkillDiscoveryMode::DirectChildren`
— the standard's immediate-children rule.

So on Codex the court runs as the clerk skill with the briefs read from
`references/`, which is why the briefs are reference files and not only agent
files. Scheduling is GitHub Actions.

### 7.4 Gemini CLI

The closest fit after Claude, and the one that changes the package. A Gemini
extension needs `gemini-extension.json` at its root, and from there its
component paths coincide with what is already proposed: "Place skill
definitions in a `skills/` directory. For example,
`skills/security-audit/SKILL.md`", and "Add agent definition files (`.md`) to
an `agents/` directory in your extension root" — the latter marked "a preview
feature currently under active development", which is worth repeating rather
than smoothing over.

One directory tree therefore serves Claude and Gemini for both skills and
agents. The cost is a conformance question this repository should answer
deliberately rather than discover later: Agent Plugins §8 says "Client-
specific files MUST be represented under a top-level directory named for that
namespace", and `gemini-extension.json` and `agents/` are client-specific
files at the root, under no namespace. The same is already true of
`.claude-plugin/`, which this repository keeps as a symlink for reasons
`README.md` records. `tools/check-conformance.py` would pass either way — it
checks the closed manifest, `skills/`, containment and the absence of a
second manifest — so this is a claims question, not a check failure: the
README must not describe such a package as fully conformant without saying
which files sit outside §8.

### 7.5 OpenCode

Skills yes, agents no. OpenCode's agent files are read from
`~/.config/opencode/agents/` or `.opencode/agents/` — user and project
configuration, with no package-level path. Its skills, per `README.md`'s
existing citation, are read from six locations including the vendor-neutral
`~/.agents/skills/<name>/SKILL.md`.

So the install is a copy of the skill tree, and — because of the sibling-
charter decision in §4 — it must copy **every** skill directory, not one:

```
cp -r plugins/assize/skills/. ~/.agents/skills/
```

That command has not been executed. It is a direct application of the
documented location, and it is stated as such rather than as a tested
instruction.

Anyone wanting the prosecutor and defender as real OpenCode subagents copies
the three agent files into `.opencode/agents/` by hand; the package cannot
place them.

### 7.6 Any Agent Plugins 1.0.0 client

Point it at `plugins/assize/`. It gets the skills, which is the whole
product. It gets no agents, because §7 of the standard has no such component.

## 8. Decisions

Two are settled and recorded here so the reasoning does not have to be had
again. Two are open.

**Settled — the name is `assize`.** An assize is a court that sits in each
county in turn, on a circuit, rather than one that waits to be visited. That
is what these roles are: a review that arrives at a repository on a schedule,
sits, decides, and leaves. It satisfies §5.5's name pattern. It is also an
obscure word in English, which was weighed and accepted: `precinct`, `docket`,
`nightwatch` and `tribunal` were the alternatives, and the metaphor was
preferred to the familiarity. The obscurity has one practical consequence —
the package README has to say what the word means in its first paragraph,
because a reader deciding whether to install will not know.

**Settled — Claude Code on the web is the priority surface.** The request
named "cloud Codex from Anthropic", which is two different products; the one
meant is Claude Code on the web (§7.2), where the six routines already run.
OpenAI's Codex (§7.3) stays supported, because this repository already
supports it and skills install there unchanged, but it is not what gets
executed and verified first. Concretely this makes §7.2's unverified
`enabledPlugins` claim the first thing to settle before any skill is written:
if a cloud session does not install a marketplace-sourced plugin from a
committed `.claude/settings.json`, the priority surface needs the roles
committed to the policed repository's own `.claude/` tree instead, and that
changes Layer 1's shape rather than a sentence about it.

**Open — whether the four existing routines migrate or are re-authored.** The
prompts contain repository facts about `how-possible` — the excluded
`chartgen/` workspace, the frozen `src/hp/**` Python original, the
`#[ignore]`d parity oracles — that must move to that repository's Layer 2
charter, not into the package. That split is the real work of the first
version.

**Open — whether `claims-police` is in scope**, and whether it polices this
repository only or any repository carrying an `.agents/rules/claims.md`.

## 9. What has not been verified

- No package exists, so nothing here has been installed, loaded or executed on
  any client.
- The `enabledPlugins` path for cloud sessions (§7.2) is read off
  documentation and has not been run. It is the one claim whose failure would
  change the design rather than the wording.
- Gemini CLI's sub-agent support is documented as a preview feature under
  active development; nothing was run against it.
- Codex's lack of an agents component is a negative claim, and it is bounded:
  it means no agent or subagent path appears in the manifest resolver's
  component fields or the loader's default component-path constants, in the
  two files cited. It is not a claim about every file in Codex.
- `agent-plugins.org`, `opencode.ai`, `geminicli.com` and
  `developers.openai.com` are all unreachable from the network this was
  written on. The specification, OpenCode's pages and Gemini CLI's pages were
  read as Markdown in their own repositories, which is documentation.
  Codex publishes no plugins documentation to read — its `docs/skills.md` is
  a two-line pointer to the blocked page — so its claims come from its source.
  Claude's documentation site was reachable and was read directly.

## Sources

Each link is a commit permalink, so it dates the claim.

**The standard** — documentation.
[Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/ff8ab5e392cc87bd88d87c060815a87490e51003/spec/1.0.0.md),
§6.1, §6.2, §7, §8, and the design note "Why only Agent Skills and MCP in
v1?"; the [1.1.0 working
draft](https://github.com/agentplugins/agent-plugins-spec/blob/ff8ab5e392cc87bd88d87c060815a87490e51003/spec/1.1.0.md)
carries the same two-row table.

**Claude Code** — documentation, read from the site directly.
Plugin components and the `agents/` directory:
<https://code.claude.com/docs/en/plugins> and
<https://code.claude.com/docs/en/plugins-reference>. The cloud substitute for
`/plugin`, and `extraKnownMarketplaces`:
<https://code.claude.com/docs/en/discover-plugins>. `/plugin` being
unavailable in cloud sessions, and repo `.claude/agents/` being picked up:
<https://code.claude.com/docs/en/claude-code-on-the-web>. Routines using
skills committed to the cloned repository:
<https://code.claude.com/docs/en/routines>.

**Codex** — source, because Codex publishes no plugins documentation.
Manifest component fields:
[`codex-rs/core-plugins/src/manifest.rs`](https://github.com/openai/codex/blob/d52478c52ef09f001142a4b82339467c3880877f/codex-rs/core-plugins/src/manifest.rs)
(`skills`, `mcp_servers`, `apps`, `hooks`). Default component paths and
Agent Plugins skill discovery:
[`codex-rs/core-plugins/src/loader.rs`](https://github.com/openai/codex/blob/d52478c52ef09f001142a4b82339467c3880877f/codex-rs/core-plugins/src/loader.rs).
The manifest and marketplace claims `README.md` already carries are cited
there at their own revision.

**Gemini CLI** — documentation, published as Markdown in its own repository
because `geminicli.com` is blocked.
[`docs/extensions/reference.md`](https://github.com/google-gemini/gemini-cli/blob/812f7a2bcf20b6e80e2e50c3c8fa8e26567bc1e8/docs/extensions/reference.md),
"Extension format", "Agent skills" and "Sub-agents";
[`docs/extensions/index.md`](https://github.com/google-gemini/gemini-cli/blob/812f7a2bcf20b6e80e2e50c3c8fa8e26567bc1e8/docs/extensions/index.md)
for what an extension packages.

**OpenCode** — documentation, published as Markdown in its own repository
because `opencode.ai` is blocked.
[`packages/web/src/content/docs/agents.mdx`](https://github.com/sst/opencode/blob/a57230b80be1c3bffab71ac021d11b02fb2fbe6c/packages/web/src/content/docs/agents.mdx),
"Markdown" — `~/.config/opencode/agents/` and `.opencode/agents/`. The skills
locations are cited in `README.md` at their own revision.
