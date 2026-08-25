# Proposal: `assize` — a package of adversarial review roles

**Status: proposal.** Nothing described here is implemented. No package named
`assize` exists in `plugins/`, no skill has been written, and no client has
loaded any of it. Every claim about a client is quoted from that client's own
documentation, or from its source where it publishes none, at a commit
permalink; [Sources](#sources) says which kind each one is, and §10 says what
was not checked at all.

The subject is a family of unattended review roles — the police, the
prosecutor, the defender, the judge — that today exist as six cloud routines
against two repositories, each a single prompt of roughly twenty thousand
characters stored in an account and nowhere else.

An assize is a court that sits in each county in turn, on a circuit, rather
than one that waits to be visited: a review that arrives at a repository on a
schedule, sits, decides, and leaves.

## 1. What is actually being packaged

The routines conflate three things with different lifetimes, different owners
and — decisively — different portability:

1. **The role.** What an abstraction finding *is*; what separates a logic
   error from a style preference; the rules of evidence in a trial; the
   doctrine that filing nothing is a successful run. Durable,
   repository-agnostic, and the part worth versioning.
2. **The repository's facts.** Which commands verify a change here; which
   paths are never edited by hand; which labels exist; what the search
   excludes. Changes per repository, and belongs to that repository.
3. **The schedule.** Weekly at 03:00 UTC, against `owner/repo`. Belongs to
   whoever runs it, and no plugin format carries it (§6).

Today all three live inside one opaque prompt, at four costs:

- **The prompts are not reviewable.** Twenty thousand characters of procedure
  deciding what gets filed against a repository, outside version control:
  not diffable, not reviewable in a pull request, not blameable, not
  revertible.
- **The roles cannot be run on demand.** There is no way to say "run the
  abstraction police over this crate now". The role exists only as something
  a cron fires.
- **Every new repository is a copy-paste.** The two Issue Court prompts
  already differ in ways that look like drift rather than intent, and the four
  police prompts repeat the same GitHub-over-REST recipes, the same
  `/tmp/run` state discipline, the same backpressure table and the same
  fingerprint protocol, four times over.
- **The environment rules are load-bearing and invisible.** "Never run `gh
  auth status`", "the clone is shallow", "keep your state in files, not in
  your context" were expensive to learn and are currently retyped into each
  new prompt.

The proposal moves (1) into a versioned package, (2) into the repository being
policed, and shrinks (3) to a stub naming a role and a repository. A routine's
prompt becomes two lines; everything else arrives through a pull request.

## 2. Equal support on every surface is the governing requirement

The stated requirement is that Claude, Codex, OpenCode, Gemini CLI and any
Agent Plugins 1.0.0 client are supported **at the same level, with no
degradation**. No surface is the priority; the weakest one sets the product.

That is a stronger constraint than conformance, and it happens to point the
same way. Two ceilings meet:

**The standard's ceiling.** Agent Plugins 1.0.0 §7: "Agent Plugins v1 defines
exactly two component types: **skills** and **MCP servers**. Other component
types are outside the v1 format and do not affect conformance." Its design
notes name this exact case: "Other proposed component types — such as
commands, hooks, **agents**, rules, and LSP servers — remain too
client-specific for a stable portable contract and are outside the v1 format
until their formats converge." §6.1's fixed-location table has two rows,
`skills/` and `mcp.json`. The 1.1.0 working draft changes neither.

**Equality's floor.** A capability only some hosts have cannot be part of the
product, because using it degrades the rest. Codex resolves no agent component
from a plugin at all, and OpenCode reads agents only from user or project
configuration — so shipping `agents/*.md` would make Claude and Gemini the
good case and the other two the compromised case. That is precisely what "no
degradation" forbids.

So the package is **skills, and only skills**. Not skills as the portable
subset with agent files bolted on for the lucky hosts — skills as the entire
product, with nothing shipped that only some hosts can read.

This is a change from the first draft of this proposal, which treated agent
files as a per-client projection and accepted a lesser court on Codex and
OpenCode. Under equal support that is not acceptable, and §3 is why it is also
not necessary.

## 3. Why a skills-only court is not a lesser court

The obvious objection: the trial's whole value is **context isolation**. The
prosecutor must not see the defender's reasoning; the judge must have seen
neither until the record is complete. If agent files are what create isolated
contexts, and agent files cannot be shipped, the trial degrades to three
personas talking to themselves in one context — which is not a trial.

The objection fails, and the reason is the pivot of this design: **a skill is
prose read by the host's model, and prose can address a capability
generically.** The skill does not need a portable API for spawning workers. It
needs each host's model to *have* some clean-context delegation primitive, and
to be told what the brief requires of it. All four have one:

| Host | Primitive | Kind of source |
| :-- | :-- | :-- |
| Claude Code | the Agent tool; subagents documented as running in a separate context window | documentation |
| Codex | `spawn_agent`, in a tool namespace whose description is "Tools for spawning and managing sub-agents" | source |
| Gemini CLI | subagents exposed to the main agent as tools — "Interactions with a subagent happen in a separate context loop" | documentation |
| OpenCode | the Task tool, with a built-in `general` subagent for exactly this | documentation |

So `issue-court` ships as one skill — the clerk's procedure — carrying the
prosecutor, defender, judge and expert briefs as reference files. The clerk
delegates each brief to a fresh worker using whatever primitive its host
offers. The procedure is identical everywhere; only the tool call differs, and
the model already knows its own tools.

**One trap has to be carried in the package, because it silently destroys the
isolation.** Codex's `spawn_agent` documents its `agent_type` parameter as
"Agent type override for the new agent. Omit to inherit the parent agent type
with a full-history fork; otherwise, `default` is used." A full-history fork
is not a clean context: the defender would inherit the prosecutor's reasoning
and the trial would be theatre. The charter (§5) therefore states the
requirement in capability terms — *the worker must start with none of your
history* — and names the hosts where the default does not satisfy it.

That is what equal support actually costs here: not a weaker feature, but a
paragraph of host-specific care held once, in one place, rather than four
copies of a Claude-shaped assumption.

## 4. Three layers

### Layer 1 — the package (portable, versioned, installed)

One plugin, `plugins/assize/`, whose skills are the roles. Repository-agnostic
and host-agnostic: a role skill names no crate, no verification command, no
label, and no vendor's tool.

### Layer 2 — the charter in the policed repository (per-repo, committed)

A single file the role skills read, proposed as `.agents/assize.yaml` in the
target repository — the same `.agents/` tree this repository already uses for
`rules/`, `policies/` and `modes/`. It declares what a role cannot know:

- the verification commands, exactly, and the traps in them (this
  repository's own `.agents/rules/verification.md` is the model);
- paths never edited by hand, and therefore never a finding;
- search exclusions;
- labels the roles may use, and the backpressure caps;
- how GitHub is reachable — session tools, `gh api` REST, or not at all;
- which rule files a role must read before analysing anything.

A role skill that finds no charter runs reduced and **says so in its report**.
It never invents a verification command: `.agents/rules/claims.md` applied to a
machine — declining to check is a correct outcome, a plausible invented
command is not.

### Layer 3 — the schedule (per-repository, not shippable)

Reduced to a stub. A scheduled run's prompt becomes:

    Run the assize dependency-police skill against this repository,
    following it exactly. Report in the shape it specifies.

Everything a reviewer would want to argue with now lives in a file with a
history. §6 covers what "equal support" does to the scheduling mechanism
itself, which is the part of this proposal equality changes most.

## 5. The roster

Every entry is one skill directory. There are no other component types.

**The police** — periodic, read-only, adversarial towards their own findings,
biased hard towards silence. Each sweeps, verifies, hands surviving candidates
to clean-context workers for independent triage, and files at most what a
backpressure cap allows.

| Skill | Looks for |
| :-- | :-- |
| `dependency-police` | updates that let the repository *delete* code, not updates for their own sake |
| `abstraction-police` | dead, superfluous, wrong or duplicated abstractions, each with a regression-free removal plan |
| `logic-police` | logic errors, reproduced before they are believed |
| `repo-police` | documentation, manifest and marketplace hygiene; unbacked compatibility claims; generated filler |

A fifth is worth considering for this repository specifically: a
`claims-police` enforcing `.agents/rules/claims.md` — every statement about a
client carries a citation, of a stated kind, at a pinned revision. That rule
is currently enforced by the owner reading carefully.

**`issue-court`** — one skill, one issue per run, tried adversarially, one
comment posted, nothing modified. The clerk builds the case file, runs the
proceedings, vets expert briefs for leading questions, and posts the comment.
Its `references/` hold the briefs it delegates:

| Brief | Role |
| :-- | :-- |
| `prosecutor.md` | argues the issue is wrong or not actionable; bears the burden |
| `defender.md` | argues it is real and worth acting on; steelmans a badly written report |
| `judge.md` | fresh context, strikes unexhibited assertions, re-runs the decisive exhibit itself, returns a structured verdict |
| `experts.md` | spec expert, host expert, verification engineer, archaeologist, docs-standards expert — commissioned blind, capped, every report entering the record in full whatever it says |

**`assize-muster`** — the setup role. Given a repository, it writes the Layer 2
charter by reading what the repository actually has, then installs Layer 3 as
§6 describes. This is the "configure the routines across repositories" half of
the request, and it is a skill rather than a document precisely so that it
works the same on every host.

**`assize-charter`** — not a role. The doctrine every other skill would
otherwise repeat, held once: the GitHub-over-REST recipes and why `gh issue
list` is not used, the shallow-clone fetch, the "keep state in files, not in
your context" discipline, the backpressure table, the fingerprint-and-dedup
protocol, the untrusted-input rule for issue bodies and fire payloads, the
delegation requirement and its per-host traps (§3), the fixed report shape,
and the doctrine that a run which files nothing is a successful run. Every
role skill's first instruction is to read it.

### Why the charter is a sibling skill and not a copy

Three ways to share text across skills were considered:

1. **Duplicate it in each skill.** What the routines do today. Four copies
   drift; three already have.
2. **Generate the skills from fragments.** Rejected: `.agents/rules/
   conformance.md` forbids built artefacts in the tree, and a generated
   `SKILL.md` is one.
3. **A sibling skill directory, referenced by relative path.** Each role skill
   opens with "read `../assize-charter/SKILL.md` before anything else".

(3) resolves in every install path that lays down the whole `skills/` tree,
which is all of them, provided OpenCode's documented copy takes every skill
directory rather than one. No symlink, no generation, no duplication. It
assumes the host tells the model where the skill it is running lives, which
§10 records as unverified.

### Skill naming

Claude namespaces plugin skills as `/assize:dependency-police`, so an
`assize-` prefix on every directory would read as `/assize:assize-…`. But
OpenCode's vendor-neutral location, `~/.agents/skills/<name>/`, is a flat
namespace shared with every other package, where `charter` and `muster` are
collisions waiting to happen. Proposed split: role skills unprefixed
(`dependency-police`, `issue-court`), the two generic ones prefixed
(`assize-charter`, `assize-muster`).

## 6. Scheduling, and what equality costs there

No target format has a component type for "run this weekly". Not Agent
Plugins, whose §6.1 table has two rows; not Claude Code, whose plugin
components are skills, commands, agents, hooks, MCP, LSP, monitors, `bin/` and
`settings.json`; not Codex, whose plugin manifest resolves `skills`,
`mcp_servers`, `apps` and `hooks`; not Gemini CLI, whose extensions carry
commands, hooks, skills, sub-agents, themes and policies; not OpenCode, whose
agents are user or project configuration. So Layer 3 is always set up and
never shipped, and `assize-muster` exists because that step cannot be
packaged.

Equal support decides *which* mechanism `assize-muster` sets up, and this is
where the requirement bites hardest.

Claude Code has **routines**: cloud scheduling with no CI job, no runner and
no API key, created with `/schedule`, and that is how all six roles run today.
No other target has an equivalent. Making routines the baseline would make
Claude the good case and every other host the compromised one — the exact
degradation the requirement rules out.

So the baseline is the mechanism all four share: **a scheduled GitHub Actions
workflow that invokes the host's own non-interactive mode**, committed to the
policed repository beside its charter. Each of the four documents one:

| Host | Non-interactive invocation | Kind of source |
| :-- | :-- | :-- |
| Claude Code | `claude -p "…"` | documentation |
| Codex | `codex exec` — "Run Codex non-interactively" | source |
| Gemini CLI | `gemini -p "…"`, with `--output-format json` for scripting | documentation |
| OpenCode | `opencode run "…"` | documentation |

Claude routines remain available and are strictly more convenient — no
workflow file, no runner minutes, no key in repository secrets. Under this
requirement they are an *alternative* a user may choose, not the path the
package assumes. `assize-muster` should offer both and default to the
workflow.

The honest cost, stated rather than buried: equality here is paid in
credentials. The workflow needs an API key or subscription token in the
policed repository's secrets on every host, where the routine needed none on
one of them. That is a real regression for the surface that is best served
today, and it is the price of the other three not being second-class. Whether
that trade is worth making is a decision, not a fact, and §9 leaves it open.

## 7. Proposed layout

```text
plugins/assize/
  plugin.json                       Agent Plugins 1.0.0, at the plugin root
  .claude-plugin/plugin.json        symlink → ../plugin.json (as howp does)
  gemini-extension.json             so Gemini loads the package at all (§8.4)
  skills/
    assize-charter/SKILL.md         the shared doctrine, incl. delegation rules
    assize-muster/SKILL.md          writes the charter, installs the schedule
    dependency-police/SKILL.md
    abstraction-police/SKILL.md
    logic-police/SKILL.md
    repo-police/SKILL.md
    issue-court/
      SKILL.md                      the clerk's procedure
      references/
        prosecutor.md
        defender.md
        judge.md
        experts.md
  README.md
```

No `agents/`, no `commands/`, no `hooks/`, no `.mcp.json` — §2. Everything
except `gemini-extension.json` and the vendor symlink is the standard's own
layout.

## 8. What equal support means on each surface

Nothing below has been executed against a published copy of a package that
does not yet exist.

### 8.1 Any Agent Plugins 1.0.0 client

Point it at `plugins/assize/`. It gets the manifest at the plugin root with
the canonical `$schema` and the skills in `skills/` — which is the entire
product. This row is the floor the other four are held to, not a lesser case.

### 8.2 Claude Code, terminal and web

Terminal: the marketplace path this repository already documents. Web: the
`/plugin` command does not exist there — Claude Code's own documentation gives
the substitute, "declare the plugin under `enabledPlugins` in
`.claude/settings.json` for cloud sessions", paired with
`extraKnownMarketplaces` in the same file:

```json
{
  "extraKnownMarketplaces": {
    "ai-plugins": { "source": { "source": "github", "repo": "Akurganow/ai-plugins" } }
  },
  "enabledPlugins": { "assize@ai-plugins": true }
}
```

That file is committed to the *policed* repository, which is the repository a
cloud session clones. **This is the one unverified claim whose failure changes
the design rather than the wording**, and equal support raises rather than
lowers its importance: the same documentation says adding a marketplace does
not install a plugin from an external source, so whether a cloud session
performs the install is unestablished. If it does not, Claude's web surface
needs the skills committed to the policed repository's own `.claude/` tree,
and Layer 1 gains a second shape.

### 8.3 Codex

Skills install: Codex reads Agent Plugins manifests, its loader's default
skill directory is `skills`, and for an Agent Plugins manifest it discovers
skills as `SkillDiscoveryMode::DirectChildren` — the standard's
immediate-children rule. Its marketplace reading of this repository's index is
covered in `README.md`.

Codex resolves no agent component from a plugin — its manifest paths are
`skills`, `mcp_servers`, `apps` and `hooks`. Under §2 that costs nothing,
because the package ships none. Its delegation primitive is present and
usable (§3), with the full-history-fork trap the charter carries.

### 8.4 Gemini CLI

Its skills location is the standard's: "Place skill definitions in a
`skills/` directory. For example, `skills/security-audit/SKILL.md`". Its
extension format requires one thing the standard does not — "Each extension
must have a `gemini-extension.json` file in its root directory" — so that file
is shipped. It is an install-enabler, not a capability: it adds nothing the
other hosts lack, which is why it does not breach §2.

It does breach the letter of Agent Plugins §8, and the proposal should say so
rather than be caught saying so later: "Client-specific files MUST be
represented under a top-level directory named for that namespace", and
`gemini-extension.json` sits at the root under no namespace. The same is
already true of `.claude-plugin/`, which this repository keeps as a symlink
for reasons `README.md` records. `tools/check-conformance.py` passes either
way — it checks the closed manifest, `skills/`, containment and the absence of
a second manifest — so this is a claims question, not a check failure: the
README must not call such a package fully conformant without naming the files
that sit outside §8.

Gemini's sub-agents are documented as "a preview feature currently under
active development". The package does not ship any, so the preview status
affects only the delegation primitive §3 relies on, which is a documented
capability of the CLI rather than of the extension format.

### 8.5 OpenCode

Skills install to the vendor-neutral location `README.md` already cites, and
because of the sibling-charter decision in §5 the copy must take **every**
skill directory:

```
cp -r plugins/assize/skills/. ~/.agents/skills/
```

That command has not been executed. It is a direct application of the
documented location and is stated as such rather than as a tested
instruction.

OpenCode reads agent files only from `~/.config/opencode/agents/` or
`.opencode/agents/` — user and project configuration, with no package-level
path. Under §2 that costs nothing. Its Task tool and built-in `general`
subagent supply the delegation §3 needs.

### 8.6 The one inequality that remains

Installation ergonomics differ, and cannot be made equal from inside a
package: `/plugin install` on Claude, `codex plugin add` on Codex, `gemini
extensions install` on Gemini, a `cp -r` on OpenCode. That is not a
degradation of what the roles do — every host runs the identical skills once
they are in place — and it is not this repository's to fix: Agent Plugins
defines no repository-level index and says nothing about how a client gets
from a repository to a plugin root, which `README.md` already states as the
limit of what conformance buys.

## 9. Decisions

**Settled — the name is `assize`.** A court that sits in each county in turn.
It satisfies §5.5's name pattern. It is also an obscure word in English, which
was weighed and accepted over `precinct`, `docket`, `nightwatch` and
`tribunal`; the cost is that the package README must define the word in its
first paragraph, because a reader deciding whether to install will not know
it.

**Settled — equal support on every surface, no priority surface.** The
weakest host sets the product. Its consequences are §2 (skills only, no agent
files), §3 (delegation addressed generically, with per-host traps held in the
charter) and §6 (a workflow, not routines, as the scheduling baseline).

**Open — whether the credential cost in §6 is acceptable.** Making the
workflow the baseline regresses the one surface that today needs no key.
Choosing routines as the baseline instead would be a deliberate, stated
exception to equal support, confined to Layer 3, and would leave Layers 1 and
2 fully equal. Both are defensible; this proposal does not decide it.

**Open — whether the four existing routines migrate or are re-authored.**
Their prompts carry repository facts about `how-possible` — the excluded
`chartgen/` workspace, the frozen `src/hp/**` Python original, the
`#[ignore]`d parity oracles — that must move to that repository's Layer 2
charter rather than into the package. That separation is the real work of the
first version.

**Open — whether `claims-police` is in scope**, and whether it polices this
repository only or any repository carrying an `.agents/rules/claims.md`.

## 10. What has not been verified

- No package exists, so nothing here has been installed, loaded or executed on
  any client.
- The `enabledPlugins` path for cloud sessions (§8.2). The one whose failure
  changes the design.
- That a host tells the model the on-disk location of the skill it is running,
  which is what makes `../assize-charter/SKILL.md` resolve (§5). Not checked on
  any host. If it fails, the charter has to be duplicated into each skill and
  kept in step by the `repo-police`.
- That each host's delegation primitive is reachable *from inside a running
  skill* rather than only from a top-level turn. §3 establishes that the
  primitive exists on all four; it does not establish that a skill may invoke
  it, and no host was run.
- The non-interactive invocations in §6 are quoted, not executed; none was run
  inside a GitHub Actions job, and no host's authentication in CI was checked.
- Codex's lack of a plugin agent component is a bounded negative claim: no
  agent or subagent path appears in the manifest resolver's component fields or
  the loader's default component-path constants, in the two files cited. It is
  not a claim about Codex as a whole — Codex has sub-agents, reachable through
  `spawn_agent` and a `codex agents` subcommand; they are simply not something
  a plugin ships.
- Gemini CLI's sub-agents are documented as a preview feature under active
  development; nothing was run against them.
- `agent-plugins.org`, `opencode.ai`, `geminicli.com` and
  `developers.openai.com` are unreachable from the network this was written
  on. The specification and OpenCode's and Gemini CLI's pages were read as
  Markdown in their own repositories, which is documentation. Codex publishes
  no plugins or CLI documentation to read — `docs/skills.md` and
  `docs/getting-started.md` are two-line pointers to blocked pages — so its
  claims come from its source. Claude's documentation site was reachable and
  was read directly.

## Sources

Each link is a commit permalink, so it dates the claim.

**The standard** — documentation.
[Agent Plugins Specification 1.0.0](https://github.com/agentplugins/agent-plugins-spec/blob/ff8ab5e392cc87bd88d87c060815a87490e51003/spec/1.0.0.md),
§6.1, §6.2, §7, §8, and the design note "Why only Agent Skills and MCP in
v1?"; the [1.1.0 working
draft](https://github.com/agentplugins/agent-plugins-spec/blob/ff8ab5e392cc87bd88d87c060815a87490e51003/spec/1.1.0.md)
carries the same two-row table.

**Claude Code** — documentation, read from the site directly. Plugin
components: <https://code.claude.com/docs/en/plugins> and
<https://code.claude.com/docs/en/plugins-reference>. Subagents and their
separate context: <https://code.claude.com/docs/en/sub-agents>. The cloud
substitute for `/plugin`, `extraKnownMarketplaces`, and marketplace-addition
not implying install: <https://code.claude.com/docs/en/discover-plugins>.
`/plugin` unavailable in cloud sessions:
<https://code.claude.com/docs/en/claude-code-on-the-web>. Routines, and
sessions using skills committed to the cloned repository:
<https://code.claude.com/docs/en/routines>. Non-interactive `claude -p`:
<https://code.claude.com/docs/en/cli-reference>.

**Codex** — source, because Codex publishes no plugins or CLI documentation.
Plugin manifest component fields:
[`codex-rs/core-plugins/src/manifest.rs`](https://github.com/openai/codex/blob/d52478c52ef09f001142a4b82339467c3880877f/codex-rs/core-plugins/src/manifest.rs).
Default component paths and Agent Plugins skill discovery:
[`codex-rs/core-plugins/src/loader.rs`](https://github.com/openai/codex/blob/d52478c52ef09f001142a4b82339467c3880877f/codex-rs/core-plugins/src/loader.rs).
The `spawn_agent` tool, its namespace description and the `agent_type`
full-history-fork default:
[`codex-rs/core/src/tools/handlers/multi_agents_spec.rs`](https://github.com/openai/codex/blob/d52478c52ef09f001142a4b82339467c3880877f/codex-rs/core/src/tools/handlers/multi_agents_spec.rs).
`codex exec` as the non-interactive subcommand:
[`codex-rs/cli/src/main.rs`](https://github.com/openai/codex/blob/d52478c52ef09f001142a4b82339467c3880877f/codex-rs/cli/src/main.rs).
The manifest and marketplace claims `README.md` already carries are cited
there at their own revision.

**Gemini CLI** — documentation, published as Markdown in its own repository
because `geminicli.com` is blocked.
[`docs/extensions/reference.md`](https://github.com/google-gemini/gemini-cli/blob/812f7a2bcf20b6e80e2e50c3c8fa8e26567bc1e8/docs/extensions/reference.md),
"Extension format", "Agent skills" and "Sub-agents";
[`docs/core/subagents.md`](https://github.com/google-gemini/gemini-cli/blob/812f7a2bcf20b6e80e2e50c3c8fa8e26567bc1e8/docs/core/subagents.md)
for the separate context loop and the built-in subagents;
[`README.md`](https://github.com/google-gemini/gemini-cli/blob/812f7a2bcf20b6e80e2e50c3c8fa8e26567bc1e8/README.md),
"Non-interactive mode for scripts", for `gemini -p`.

**OpenCode** — documentation, published as Markdown in its own repository
because `opencode.ai` is blocked.
[`packages/web/src/content/docs/agents.mdx`](https://github.com/sst/opencode/blob/a57230b80be1c3bffab71ac021d11b02fb2fbe6c/packages/web/src/content/docs/agents.mdx)
for the built-in `general` subagent, the Task tool, and the
`~/.config/opencode/agents/` and `.opencode/agents/` locations;
[`packages/web/src/content/docs/cli.mdx`](https://github.com/sst/opencode/blob/a57230b80be1c3bffab71ac021d11b02fb2fbe6c/packages/web/src/content/docs/cli.mdx),
"run", for `opencode run`. The skills locations are cited in `README.md` at
their own revision.
