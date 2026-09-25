# Security policy

## Supported versions

- A package with releases is supported at its latest release.
- A package without releases is supported as it stands on `main`.

## Reporting a vulnerability

Report privately, through GitHub's advisory form for this repository. Under
the repository name, open the **Security and quality** tab, then click
**Report a vulnerability**. Source: [Privately reporting a security
vulnerability](https://docs.github.com/en/code-security/how-tos/report-and-fix-vulnerabilities/report-privately),
GitHub documentation, read 2026-09-14.

The form's direct address is
<https://github.com/Akurganow/ai-plugins/security/advisories/new>. If that
link opens no form, use the **Report a vulnerability** control instead.

**Do not open a public issue describing a vulnerability.** If no route
reaches a private form, open a public issue that asks for a security contact.
Put nothing about the vulnerability in it. GitHub's documentation gives this
route where private reporting is unavailable. Source: the same page.

Include what you have:

- the package and its version, and for `howp` the release tag and the
  platform target that `plugins/howp/binaries.json` names
- for a release asset, the sha256 you observed beside the one `binaries.json`
  records for that target
- what you ran, and what happened

A digest mismatch is worth reporting. The `forecast` skill refuses an archive
whose sha256 differs from the recorded digest
([`plugins/howp/skills/forecast/SKILL.md`](plugins/howp/skills/forecast/SKILL.md)).
Whoever meets that refusal holds the evidence, and this is where it goes.

## The `hp` binary

`howp` runs the `hp` binary, which a private repository builds. Report
its problems here, by the routes above:

- **A vulnerability in `hp`**: the advisory form.
- **Any other defect in `hp`**: a public issue.
- **A wrong version, digest or target in `binaries.json`**: a public issue.
  A digest that looks tampered with, not stale, is a vulnerability: use the
  advisory form.

The `howp` release job writes `binaries.json`, and nobody edits it by hand. A
report here reaches the person who runs that job.
