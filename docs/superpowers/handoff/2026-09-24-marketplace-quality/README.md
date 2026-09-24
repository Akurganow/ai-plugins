# Handoff: marketplace quality rework

**Temporary folder.** It exists so a later session can continue this work without
repeating the research or the decisions. **Mandatory cleanup:** delete the whole
`docs/superpowers/` tree (this folder, the spec, any plan) once the work is done **and
verified** (spec §10 acceptance met, CI green, the owner has confirmed), before the pull
request merges. Nothing in the repository references it.

## What this is

A quality review of this marketplace against external norms, a brainstorm with the
owner that turned every finding into a decision, and a design spec. The next step is
the implementation plan and then the implementation, on this branch, by the same
assistant in a **local** session on the owner's machine.

## Read in this order

1. `decisions.md` — every decision the owner made, with the constraints. Short. Binding.
2. `../../specs/2026-09-24-marketplace-quality-design.md` — the design spec built from
   those decisions. The superpowers brainstorming path is **architectural**; the spec is
   written and awaits the owner's review, then `writing-plans`, then execution.
3. `review/quality-review.md` — the findings (H1–H9, M1–M10, L1–L6) with evidence.
   Read when a spec item needs its "why".
4. `research/` — the clean-room research the review and the spec rest on. Read a file
   only when a spec item cites it. Each file names its sources and what was unreachable.

## Process state (superpowers)

- Path: architectural. Stage reached: **spec written with every decision closed (spec §8),
  not yet reviewed by the owner.** No question is open; do not re-ask any of them.
- Next: owner reviews the spec → `superpowers:writing-plans` → execute on this branch.
- The owner answers questions through a proper choice prompt (AskUserQuestion), one
  question per message, each with the context it needs to be understood by someone who
  does not see the assistant's context. Options equally weighted; no strawmen; no
  recommendation put first unless asked. A question without context was rejected twice.
- The owner reads artifacts (published pages), not downloaded files.

## Owner's constraints (do not re-ask)

- `hp` sources (Akurganow/how-possible, private) stay private.
- The nine-role agent system under `.agents/` stays in composition; its rules may change.
- Any copy of a file is generated on CI from one source, never kept by hand. Version
  bumps and tags are automatic. Ready-made tools over home-grown scripts ("no bicycles").
- No paid tests: no `claude plugin eval`, no trigger tests, nothing that calls a model
  (deferred to issue #62, human-filed).
- No blocking gates on the agent and no repetition of what is already in context: the
  standard is recommended insistently, once per context, never enforced by a hook.
- No Python or any other code module in a package; text and shell hooks only.
- Pipelines are private. Public docs never mention the agent roles. Agents never touch
  issues filed by people. Machine issues carry `police-report` and a fingerprint marker.
- Support of all four declared harnesses (Claude Code, Codex, Hermes, Oh-My-Pi) is
  mandatory. `prose-discipline` must reach each by every documented mechanism it has.
  Dropping a route is not an option.
- Plugins are installed on the owner's machine through Hermes, Codex and Oh-My-Pi, from
  the published repository. That is private experience; the repository says nothing
  about it either way (H7/M10).
- The repository must not claim the maintainer's own verification. The "not verified"
  diary and the rule that demands it are removed (H7).
- The how-possible change (H6, cosign signing) is filed as an issue in that repository,
  never worked in the ai-plugins session.

## Tools the local session needs

- `superpowers` plugin: `claude plugin marketplace add obra/superpowers-marketplace`,
  `claude plugin install superpowers@superpowers-marketplace` (v6.4.1 was used here).
- Python with `jsonschema` and `pyyaml` for `tools/check-conformance.py`.
- Claude Code CLI 2.1.281 or later for `claude plugin validate`.
- For the integration matrix and validators (spec §CI): Codex CLI, Oh-My-Pi CLI, Hermes
  CLI, `skills-ref`, `cosign`, `release-please`, `doctoc` or `markdown-toc`, `jq`.

## What was verified here and what was not

- Verified in this container: `tools/check-conformance.py` exits 0 at `232aaba`;
  `claude plugin validate .` warns on the six symlinked vendor manifests and, per
  plugin, on `extensions` for `howp` and `prose-discipline`; measurements in the review.
- Not verified: any install through Codex, Hermes or Oh-My-Pi (not installed here);
  hook behaviour in any client; everything in `research/06-*` is from docs and source,
  not from running a client.
- Research reachability: most vendor sites were blocked by the proxy; pages were read from
  their GitHub repositories at `main` on 2026-09-24 and, where the API allowed, pinned to
  a commit. Each research file records this per source.
