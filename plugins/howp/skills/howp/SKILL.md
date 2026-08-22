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
binary release. This skill downloads nothing and configures nothing — it
only explains the idea. If the user asks for a real task, say the skill is
still in development and point to the link below.

## What it will be

- Probabilities instead of a news feed: interests unfold into measurable
  questions, questions are matched to prediction markets, and the dashboard
  shows "what became more likely and by how much" — with honest caveats.
- Deterministic work (quote collection, computation, a sharp-move detector,
  rendering, storage) is done by a set of Rust binaries. The skill downloads
  them for your system from the published releases and verifies checksums
  against the table committed in this repository.
- Agent roles (the interests interview, market discovery, resolution
  criteria verification, explanations) are performed by your agent following
  the skill's instructions — no external API keys required.
- Per-environment setup: macOS (a scheduled collector via launchd — only
  after your explicit consent, explained in plain language), a GitHub fork
  (workflows: free data collection on a schedule, agent work manual-only),
  and a local mode (data lives in ~/.local/share/howp, never in git).

## Follow the project

https://github.com/Akurganow/ai-plugins
