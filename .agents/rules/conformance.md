# Conformance

A package here is installable because it matches a published specification,
not because a particular client happens to accept it. Everything below keeps
that difference visible.

## The check

```
pip install jsonschema pyyaml
python3 tools/check-conformance.py
```

It must exit 0. `.github/workflows/conformance.yml` runs it in CI, so a
change that breaks it does not merge. Run it locally before saying a package
conforms; "it looks right" is not a result the check produced.

## What the check is allowed to be

Everything the published schema can decide is decided by the published
schema. Only the rules a JSON Schema cannot express — where a file sits, what
a symlink resolves to, what a skill's front matter says — are implemented by
hand, and each of those quotes the clause it enforces beside it. Keep that
shape when adding a check: a hand-written rule with no clause next to it is
an opinion that later readers cannot argue with, and it will outlive whoever
had the reason.

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

None of this rests on §13. The vendored `const` plus `required` assert the
exact `$schema` on their own, so §13's "the check should assert what silently
breaks a Hermes install" is satisfied whether or not the hand check exists —
deleting it would not have breached the requirement. Keeping it is right for
the reasons above and for no others.

So "do not complicate the code" here — a check being the only code this
repository has — is not "never duplicate the schema". It is: a hand-written
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
  inside the package may be a symlink to it and may not be a second copy:
  §5.1 is explicit that "No other file can replace, supplement, or override
  the core fields in root `plugin.json`", and Codex's loader rejects a
  symlinked root manifest outright — `symlink_metadata` in
  [`plugin_namespace.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/utils/plugins/src/plugin_namespace.rs),
  pinned by its own `rejects_symlinked_root_plugin_manifest` test. That one
  is **from source**, because Codex publishes no plugins documentation to
  read first: its `docs/` carries fifteen files and none is about plugins or
  `plugin.json`. The link is a commit permalink, not a branch — a claim about
  code that moves has to name the revision it was true at.
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

Every change to a package bumps `version` in its `plugin.json`. §10.2 leaves
update detection to the client — clients *MAY* use `version` to decide
whether an update exists or a cache is stale — so a fix shipped without a
bump is one a client is entitled to never notice.

## Text only

No executables and no built artefacts are stored in the tree. Released
binaries are published elsewhere and referenced from here; the only thing
this repository runs is its own conformance check.

If this file and the things it describes ever disagree — the specification,
the script, the workflow — they are right and this file is stale. The same
holds for the owner's requirements: `docs/REQUIREMENTS.md` §5 and §13, in the
`how-possible` repository, are restated here for the people who work in this
one and are not owned here. Where this file and they disagree, they are right.
