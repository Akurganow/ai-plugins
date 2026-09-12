# Security policy

## Supported versions

Two packages are published from this repository, and they are versioned
differently.

| Package | What is supported |
| :-- | :-- |
| `howp` | the release recorded in [`plugins/howp/binaries.json`](plugins/howp/binaries.json) |
| `prose-discipline` | the state of `main` |

There are no backports. `plugins/howp/binaries.json` is written by the release
job in `Akurganow/how-possible` and is the record of which release and which
targets exist; this file does not restate what it holds.

## Reporting a vulnerability

Report privately, through GitHub's advisory form for this repository:

<https://github.com/Akurganow/ai-plugins/security/advisories/new>

**Do not open a public issue describing a vulnerability.** If that form is not
available to you, private vulnerability reporting has been switched off since
this file was written; open a public issue asking for a security contact and
put nothing about the vulnerability in it. That is the route GitHub documents
for a repository without private reporting — [Privately reporting a security
vulnerability](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately),
GitHub's documentation, read 2026-09-11. Private vulnerability reporting was on
for this repository that day; no file here is rewritten if it is turned off, so
trust the form and not this sentence.

Include what you have:

- the package, and for `howp` the release tag and the platform target that
  `plugins/howp/binaries.json` names;
- for a report about a release asset, the sha256 you observed beside the one
  `binaries.json` records for that target;
- what you ran, and what happened.

A digest mismatch is worth reporting. The `howp` skill refuses and deletes an
archive whose sha256 does not match the recorded digest
([`plugins/howp/skills/howp/SKILL.md`](plugins/howp/skills/howp/SKILL.md)), so
whoever hits that refusal is holding the evidence, and this is where it goes.
`README.md` says where each release's `SHA256SUMS` asset is published and how
its digests relate to `binaries.json`; this file keeps no second copy of that.

## What belongs elsewhere

The `hp` binary is built and released from `Akurganow/how-possible`. A defect
in the program itself belongs there, and so does a wrong version, digest or
target in `binaries.json`, which that release job writes and nobody here edits
by hand. The exception is an archive whose digest looks tampered with rather
than stale: report that here, privately.
