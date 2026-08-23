# Conformance

A package here is installable because it matches a published specification,
not because a particular client happens to accept it. Everything below keeps
that difference visible.

## The check

```
pip install jsonschema pyyaml
python3 tools/check-conformance.py
```

It must exit 0. `.github/workflows/conformance.yml` runs it on every push and
pull request, so a change that breaks it does not merge. Run it locally
before saying a package conforms; "it looks right" is not a result the check
produced.

## What the check is allowed to be

Everything the published schema can decide is decided by the published
schema. Only the rules a JSON Schema cannot express — where a file sits, what
a symlink resolves to, what a skill's front matter says — are implemented by
hand, and each of those quotes the clause it enforces beside it. Keep that
shape when adding a check: a hand-written rule with no clause next to it is
an opinion that later readers cannot argue with, and it will outlive whoever
had the reason.

## The vendored schema is a copy, not a source

`tools/schemas/` holds a verbatim copy of the published manifest schema, and
the script refuses to validate with it unless its `$id` is still the
canonical one. Replace the copy only from the source it came from, and update
the recorded provenance and checksum in the same change. It is never edited
to make a check agree with a package — that inverts the whole arrangement:
the package is what bends.

## Package shape

The rules that decide whether a client loads a package at all:

- The manifest is a real file at the plugin root. A vendor discovery path
  inside the package may be a symlink to it and may not be a second copy;
  the specification is explicit that nothing else supplements or overrides
  the root manifest, and at least one client's loader refuses a symlinked
  root manifest outright.
- Every symlink in a package resolves inside that package's root. A skill
  whose `SKILL.md` resolves outside it is skipped by a conforming client —
  the package still installs, and the skill is simply not there.
- Skills are discovered from the fixed `skills/` location, one directory
  deep, each with a `SKILL.md` that resolves to a regular file. The skill's
  declared name matches its directory name.
- An absent optional component is not an error. A package with no skills is
  a valid package.

## Versions

Every change to a package bumps `version` in its `plugin.json`. Installed
copies do not receive an update without it, so a corrected package that ships
without a bump is a correction nobody gets.

## Text only

No executables and no built artefacts are stored in the tree. Released
binaries are published elsewhere and referenced from here; the only thing
this repository runs is its own conformance check.
