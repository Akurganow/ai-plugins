# howp

A personal probability dashboard. It turns what a person follows into
measurable questions, binds each question to a prediction market on
Polymarket or Manifold, records the probabilities over time, detects sharp
moves, and renders a local Markdown dashboard of what became more or less
likely.

Part of the [`ai-plugins` marketplace](../../README.md). Installing: the
per-client sections of the [root README](../../README.md#installing).

## What it does

One skill drives one binary, `hp`. `hp` does the deterministic work:
extracting a probability out of a venue's raw response, the append-only
history, move detection and the rendered page. It opens no socket and reads
no clock, so the agent fetches each market body with its own tools and
passes the moment in. Every judgement is the agent's, and no part of this
package invokes a model. No API keys and no accounts.

## What ships here

| Path | What it is |
| --- | --- |
| `plugin.json` | the manifest, Agent Plugins 1.0.0, at the plugin root |
| `binaries.json` | the released binary set: tag, targets, archives, download URLs and their sha256 digests. Written by the release job |
| `skills/howp/SKILL.md` | the skill, per the Agent Skills specification: the routine cycle and the rules around it |
| `skills/howp/references/install.md` | getting the binary: the platform gate, the preflight, the download, the digest check, the unpack |
| `skills/howp/references/interview.md` | the interests interview, and the two files the user owns |
| `skills/howp/references/procedures.md` | the three procedures that need judgement: binding a question to a market, explaining a sharp move, the weekly digest |
| `skills/howp/references/commands.md` | `hp --help` and every subcommand's, as the release records it |
| `README.md` | this file |
| `.claude-plugin/plugin.json` | a symlink to the root manifest, at the manifest path Claude Code documents. The root README cites the documentation |

The binary is not stored here. It is published on this repository's
[releases page](https://github.com/Akurganow/ai-plugins/releases), and
[`binaries.json`](binaries.json) is the record of which release and which
targets exist. No sentence in this file names either. The skill stops on any
platform that file does not name.

## Before you run it

- A platform [`binaries.json`](binaries.json) names.
- The hosts declared under `extensions` in [`plugin.json`](plugin.json),
  reachable over HTTPS. The declaration says there what it grants and what it
  does not.
- What the machine needs to download, verify and unpack the archive, and
  the preflight that checks the hosts, are in
  [`skills/howp/references/install.md`](skills/howp/references/install.md).

## What has been verified

**No client has installed this package from this repository as published.**
What has been downloaded, verified and run, with its date, the release it
was measured against, and what it did not exercise, is recorded once, in
the skill's own [What has been verified, and what has
not](skills/howp/SKILL.md#what-has-been-verified-and-what-has-not). This
file keeps no second copy of it.
