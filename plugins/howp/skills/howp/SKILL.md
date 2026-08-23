---
name: howp
description: >
  Placeholder for the upcoming howp probability dashboard skill — not
  functional yet, do not use for real tasks; it only explains the project.
  The future skill: a personal probability dashboard — interests →
  measurable questions → prediction-market probabilities (Polymarket,
  Manifold) → a markdown dashboard. The working version ships with the
  first binary release; until then, invoke only when the user explicitly
  asks about the howp project or this plugin.
license: MIT
---

# howp — personal probability dashboard (placeholder)

**Status: placeholder.** This plugin is published to exercise the
installation channel; the working skill ships together with the first
binary release. This skill downloads nothing, configures nothing and runs
no procedure of its own — it only explains the idea. If the user asks for a
real task, say the skill is still in development and point to the link
below.

## What it will be

Everything below is intent. None of it is implemented in this package, and
each point says what is missing.

- Probabilities instead of a news feed: interests will unfold into
  measurable questions, questions will be matched to prediction markets, and
  the dashboard will show "what became more likely and by how much" — with
  honest caveats. Nothing here produces a dashboard.
- Deterministic work (quote collection, computation, a sharp-move detector,
  rendering, storage) will be done by a set of Rust binaries, built first
  for macOS on Apple Silicon. The skill will download them for your system
  from the published releases and verify them against a checksum table
  published with the release. Neither the binaries nor the table exist yet,
  and this package contains nothing that downloads or verifies anything.
- Agent roles — the interests interview, market discovery, resolution
  criteria verification, explanations — will be carried out by your own
  agent following the skill's instructions, with no external API keys
  required. Those instructions are not written yet: there is no interview
  here, no market discovery procedure and no resolution criteria procedure.
- Raw numbers will be put where the agent can look at them rather than
  dumped into its context: a temporary folder inside the skill's own
  directory, ignoring itself, documented in the README. This package creates
  no such folder and stores nothing.

Per-environment setup — how collection is scheduled, and what runs in a fork
rather than on your own machine — is not decided yet and is deliberately not
described here.

## Follow the project

https://github.com/Akurganow/ai-plugins
