# Conformance

A package here is installable because it matches a published specification,
not because a particular client happens to accept it. Everything below keeps
that difference visible.

## The check

The check is `tools/check-conformance.py`, and it must exit 0.

It imports `jsonschema`, which validates the manifest against the schema
vendored in `tools/schemas/`, and `yaml`, which reads `SKILL.md` front
matter. Both have to be importable by whatever runs the script. **How they
get there is not recorded here, and neither is the invocation**: those are
facts about an environment, and `.agents/rules/unattended.md` keeps them with
whoever runs in one. An environment that writes its own down is
`.github/workflows/conformance.yml`, which is also where CI runs this same
check, so a change that breaks it does not merge.

Run it before saying a package conforms; "it looks right" is not a result the
check produced.

## What the check is allowed to be

Everything the published schema can decide is decided by the published
schema. What is implemented by hand is, for the most part, the rules a JSON
Schema cannot express — where a file sits, what a symlink resolves to, what a
skill's front matter says — and each of those quotes the clause it enforces
beside it. Keep that shape when adding a check: a hand-written rule with no
clause next to it is an opinion that later readers cannot argue with, and it
will outlive whoever had the reason.

Two checks deliberately duplicate the schema, and the exception is the rule's
real shape. `$schema` is a `const` in the schema and the closed field set is
`additionalProperties: false`, yet both are also checked by hand. Not because
the schema is vague about which field broke — break a manifest both ways and
`jsonschema` names them: *"at (root): Additional properties are not allowed
('nonsense' was unexpected)"* and *"at $schema: '…/1.0.0/plugin.schema.json'
was expected"*, the second carrying the expected value as well. Run it before
arguing about it.

What the hand checks add is the **observed** value — the schema reports what
it wanted, never what it found, so its line alone does not say what is in the
file — and the **§5.2 citation**, which those messages have nowhere to carry
and which is this repository's standing rule for a hand-written check. That is
the second of the two reasons stated below, and on its own it is enough to
keep both checks.

The `$schema` one also does something no message can, and this is the part
worth arguing: its identifier is pinned **in the script**, as
`CANONICAL_SCHEMA_ID`, not read out of whichever file is sitting in
`tools/schemas/`. The vendored `const` moves with the copy; that constant does
not, so the two are independent assertions of which version this repository
targets, and the script's `$id` check turns them disagreeing into a failure
instead of a silent retarget.

None of this was forced from outside. The vendored `const` plus `required`
assert the exact `$schema` on their own, so the standing requirement that the
check assert what silently breaks a Hermes install is satisfied whether or not
the hand check exists — deleting it would have breached nothing. Keeping it is
right for the reasons above and for no others.

The checks below are the only code this repository judges packages with. So
"do not complicate the code" here is not "never duplicate the schema". It is:
a hand-written
check either enforces something a JSON Schema cannot express, or it turns a
schema rejection into a message somebody can act on, and it says beside
itself which of the two it is. A duplicate with neither reason is the one to
delete.

## The vendored schema is a copy, not a source

`tools/schemas/` holds a verbatim copy of the published manifest schema, and
the script authenticates it before using it for anything. Replace the copy
only from the source it came from, and update the recorded provenance in the
same change. It is never edited to make a check agree with a package — that
inverts the whole arrangement: the package is what bends. How the
authentication works is the script's business and is documented there; this
rule only says that it happens and that the schema does not bend.

## Package shape

The rules that decide whether a client loads a package at all:

- The manifest is a real file at the plugin root. A vendor discovery path
  inside the package is a byte-identical copy of it, written by the
  regeneration entry point, `tools/regenerate.sh`. The check compares the
  two byte for byte. §5.1 is explicit that "No other file can replace,
  supplement, or override the core fields in root `plugin.json`", and an
  identical copy overrides nothing. The copy is not a symlink. Git for
  Windows disables symbolic links by default
  ([Git for Windows](https://gitforwindows.org/symbolic-links),
  documentation). With them off, git checks a link out as a plain file
  holding the link text
  ([`core.symlinks`](https://github.com/git/git/blob/c44beea485f0f2feaf460e2ac87fdd5608d63cf0/Documentation/config/core.adoc#L237-L246),
  documentation). Claude Code documents one manifest location,
  `.claude-plugin/plugin.json`, and fails on a file that is not JSON
  ([plugins reference](https://code.claude.com/docs/en/plugins-reference),
  documentation). The root manifest may not be a symlink either. Codex's
  loader rejects a symlinked root manifest outright — `symlink_metadata` in
  [`plugin_namespace.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/utils/plugins/src/plugin_namespace.rs),
  pinned by its own `rejects_symlinked_root_plugin_manifest` test. That one
  is **from source**. The `plugin_namespace.rs` link is a commit permalink,
  not a branch — a claim about code that moves has to name the revision it
  was true at. Codex's plugin documentation,
  [Build plugins](https://developers.openai.com/plugins/build/plugins.md)
  (documentation, read 2026-09-25), does not mention a symlinked manifest.
- Every package path resolves inside that package's root (§4.1). The
  failure boundary is graded: a root `plugin.json` outside it rejects the
  plugin, while a `SKILL.md` outside it only skips that skill (§7.1) — the
  package still installs without it. §7.1's "SHOULD report" is written about
  a skill that fails the Agent Skills specification; whether a client also
  announces a containment skip is not something the spec settles.
- Skills are discovered from the fixed `skills/` location (§6.1), immediate
  children only, each with a `SKILL.md` that resolves to a regular file; no
  deeper search. The name in the front matter must equal the directory name
  — that one is the [Agent Skills
  specification](https://agentskills.io/specification), which §7.1 defers to
  for the format.
- An absent fixed location is not an error (§6.2). A package with no skills
  is a valid package. A location present but of the wrong kind is different:
  that component type is invalid.

## Versions

`version` in `plugins/howp/plugin.json`, the whole of
`plugins/howp/binaries.json` and
`plugins/howp/skills/howp/references/commands.md` are written by the release
job that builds and publishes the binaries, and by nothing else. **Nobody
edits any of the three by hand, ever.** Each is a claim about a released
artifact: a hand edit asserts a version, a digest or a target that no
release produced, and the next release overwrites it without noticing.
Every package but howp is released by `.github/workflows/release.yml`,
which runs cocogitto. It writes `version` in each `plugins/<name>/plugin.json`
and in its `.claude-plugin/plugin.json` copy, and each
`plugins/<name>/CHANGELOG.md`. Nobody edits those by hand either, for the same
reason.
**The catalogue index carries no version at all**: `.claude-plugin/marketplace.json`
has no top-level `version`, none under `metadata`, and no `version` in a
plugin entry, because a version no machine writes is a version somebody moves
by hand.

## Text only

No executables and no built artefacts are stored in the tree. Released
binaries are published elsewhere and referenced from here. This repository
runs two programs of its own. The first is its check,
`tools/check-conformance.py`. The second is its regeneration entry point,
`tools/regenerate.sh`, which writes every generated copy from its one source.
`.github/workflows/conformance.yml` runs both, and fails when a regenerated
copy differs from the committed one.

If this file and the things it describes ever disagree — the specification,
the scripts, the workflow — they are right and this file is stale.
