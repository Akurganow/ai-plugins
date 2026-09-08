# prose-discipline

An engineering prose standard for everything an agent writes: user replies,
prose, code comments, review comments, commit messages, change descriptions,
error messages, and agent instructions.

Part of the [`ai-plugins` marketplace](../../README.md).

## What it enforces

Five layers, each a rule a reader can check rather than a preference:

- **Structure** — a 25-word sentence ceiling, one action per sentence or
  step, active voice, no noun stacks, semicolons split into sentences.
- **Vocabulary** — plain verbs, a substitution table, no significance
  inflation, and a domain-term contract that keeps `accessible`, `accept`,
  `validate`, `rotate` and `robust` where they name a technical property.
- **Comment hygiene** — no narrator comments, no step markers, no ASCII
  dividers, no committed uncertainty. Comments explain why; names explain
  what.
- **Artifact formats** — Conventional Comments labels on review feedback;
  change descriptions as what / why / verification; three-part error
  messages; single-intent instruction steps. A repository's own template
  outranks these formats.
- **Slop pruning** — no rhetorical negations, teaser hooks, filler openers,
  false engagement, hollow reassurance, or session-process narrative in a
  durable artifact.

The exemption contract is part of the standard: code blocks, identifiers,
commands and URLs are never flagged, quoted and historical text is exempt,
and in a diff only added lines count.

## What ships here

| Path | What it is |
| --- | --- |
| `plugin.json` | the manifest — Agent Plugins 1.0.0, at the plugin root |
| `rules/prose-discipline.md` | the core rules, one file, the whole mandatory part |
| `skills/prose-discipline/SKILL.md` | the skill, per the Agent Skills specification |
| `skills/prose-discipline/references/*.md` | the depth behind each rule, plus a calibration corpus |
| `hooks/hooks.json`, `hooks/session-rules.sh` | a SessionStart hook that prints the core rules for a host to inject |
| `.claude-plugin/`, `.codex-plugin/` | vendor discovery paths, each a symlink to the root manifest |

## How the standard reaches a session

Three routes, and which of them a given client takes is that client's
business:

| Route | Mechanism |
| --- | --- |
| A rule file | `rules/prose-discipline.md` carries `alwaysApply: true` in its front matter, for hosts that read plugin rule files. |
| A session hook | `hooks/hooks.json` registers a `SessionStart` command. `hooks/session-rules.sh` strips the front matter and prints the body as `hookSpecificOutput.additionalContext`. It needs `node` on `PATH`; without it the hook writes one line to stderr and exits 0, so the session always starts. |
| The skill | `skills/prose-discipline/SKILL.md` is discovered from the fixed `skills/` location every Agent Plugins 1.0.0 client reads. A client that takes neither route above still gets the standard on demand. |

**Nothing below has been verified from this repository as published.** The
upstream package this one was assembled from recorded live checks against
three hosts; those results are not reproduced here, no client has been
installed from this repository, and no route above has been observed
working from this copy. The mechanisms are stated from the files, which are
in this directory and can be read; the behaviour of any particular client is
not stated at all.

One thing is worth knowing before installing: **the vendor manifests here
are symlinks to the root manifest**, because `.agents/rules/conformance.md`
in this repository forbids a second copy, citing Agent Plugins 1.0.0 §5.1.
A client that discovers components only through vendor-specific manifest
fields will therefore find the skill, which sits at the fixed location, and
not the rule file or the hook, which the root manifest names only inside
`extensions`.

## Configuration

None. No credentials, no MCP servers, no settings files. Removing the plugin
removes the standard.

## Boundaries

- It governs text mechanics, not whether a document serves its reader.
- It governs durable artifacts, not the register of a live conversation.
- It is not a code linter. Behaviour-level checks belong to a linter.
- There is no checker script, deliberately: enforcement is model judgement
  over rule texts a person can read and argue with.
