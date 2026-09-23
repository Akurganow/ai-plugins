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

Report privately, through GitHub's advisory form for this repository. **The
authoritative way in is the repository itself**, because it is the only one
GitHub publishes: "Under the repository name, click the **Security and
quality** tab. […] Click **Report a vulnerability** to open the advisory form"
— [Privately reporting a security
vulnerability](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately),
GitHub's documentation, read 2026-09-14.

The form's own address is below, for a reader who would rather paste a link
than navigate:

<https://github.com/Akurganow/ai-plugins/security/advisories/new>

**That URL was not opened from the environment that wrote this file**, and
GitHub documents no address for the form anywhere: at commit `078b583` of
[`github/docs`](https://github.com/github/docs/tree/078b5832caa5cde591c2babb389ef447a0ef66eb/content),
GitHub's documentation in source form, no file under `content/` carries the
string `advisories/new`. If the link does not open a report form, that settles
nothing about this repository's settings — use the **Report a vulnerability**
control described above and disregard the link.

**Do not open a public issue describing a vulnerability.** If neither route
reaches a private form, open a public issue asking for a security contact and
put nothing about the vulnerability in it. That is what GitHub tells a reporter
to do where private reporting is unavailable: "you need to initiate the
reporting process by following the instructions in the security policy for the
repository, or by creating an issue asking the maintainers for a preferred
security contact" — the same page, read the same day.

Private vulnerability reporting was on for this repository on 2026-09-22, read
as `{"enabled": true}` from
`https://api.github.com/repos/Akurganow/ai-plugins/private-vulnerability-reporting`,
GitHub's API, authenticated as the repository owner — which establishes the
setting and not what a signed-out reader is shown. Nothing rewrites this file
if it is switched off, so trust what the repository shows you over this
paragraph.

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

The `hp` binary is built from `Akurganow/how-possible`, which
[`plugins/howp/binaries.json`](plugins/howp/binaries.json) names in its
`source_repository` field. **Its release assets are published from this
repository, not from that one**: every `url` under that file's `targets` names
a release of `Akurganow/ai-plugins`. Both are the release job's own record
rather than a sentence kept in step by hand, so a report about an asset you
downloaded belongs here whichever repository built it.

**That repository is private**, as this repository's own `howp` skill states
where it forbids a build from source:
[`plugins/howp/skills/howp/SKILL.md`](plugins/howp/skills/howp/SKILL.md) —
"never a build from source: that repository is private". Unless its owner has
given you access it does not open for you, so nothing here asks you to file
anything there. Report both of these through this repository instead, by the
routes above:

- **A defect in the `hp` program itself.** Use the advisory form if it is a
  vulnerability; open a public issue if it is not.
- **A wrong version, digest or target in `binaries.json`.** Open a public
  issue — unless the digest recorded there looks tampered with rather than
  stale, which is a vulnerability report and belongs in the advisory form.
  Nobody can correct the file here: `.agents/rules/conformance.md` holds that
  it is written by the release job "and by nothing else", so what a report
  here achieves is reaching the person who runs that job.
