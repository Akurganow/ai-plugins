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

So "do not complicate the code" here — the checks below being the only code
this repository has — is not "never duplicate the schema". It is: a hand-written
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

`version` in `plugins/howp/plugin.json` and the whole of
`plugins/howp/binaries.json` are written by the release that publishes the
binaries — `.github/scripts/release-plugin-commit.sh` in
`Akurganow/how-possible`, in one commit — and by nothing else. **Nobody edits
either by hand, ever.** A pull request that moves `version` is refused
whatever else it does, and the machine half of that refusal is
`tools/check-release-record.py`.

Two files is what that job writes, and it is dated: on how-possible's `main`,
read 2026-09-03, it stages `binaries.json` and the manifest, and refuses to
commit at all if the index holds anything besides those two — "the index
holds files this release may not change". Extending it to
`plugins/howp/skills/howp/references/commands.md` is intended and **has not
landed**: nothing on that `main` writes that file, and no open pull request
there proposed it when this was checked on 2026-09-03. Until such a change
lands, `commands.md` is hand-written like any other text here; when it lands,
this paragraph is what gets updated, with that pull request named.

The owner decided it on 2026-09-03: «вручную бампать версии строжайше
запрещено … никто и никогда не имеет права руками менять версии» — *bumping
versions by hand is strictly forbidden … nobody, ever, has the right to
change versions by hand*. Quoted rather than only translated, because a
decision is evidence and a translation is a paraphrase.

Two failures are why. On 2026-09-02 how-possible's `release-version.yml` read
this repository's `plugin.json` and computed from it — `The plugin package is
at 0.2.0, so the floor is 0.2.1.`, printed at 17:54:52.76Z in that run's job
log — and six seconds later, at 17:54:59Z, PR #7 merged a hand bump of the
same file to 0.2.1 (the pull request's own merge time). The release itself
succeeded: `howp-v0.2.1` exists, published at 18:03:49Z with both archives
and `SHA256SUMS`. What failed was the last step, which refuses a package
already at the version being released — "release-plugin-commit: the package
is already at 0.2.1", the script on how-possible's `main`, read 2026-09-03 —
so the package was never pointed at that release. `binaries.json` stayed at
`howp-v0.2.0`, and this repository's history holds no 0.2.1 release commit
between `howp 0.2.0` and `howp 0.3.1`: the binaries exist and nothing here
names them.

The second failure is the floor itself. While a version sits here by hand,
how-possible has to release one patch above whatever it reads, so a
documentation-only bump in this repository, 0.3.1 → 0.3.2, would have pushed
the next `hp` release to 0.3.3; it was reverted with this rule.

**The catalogue index carries no version at all.** `.claude-plugin/marketplace.json`
has no top-level `version`, none under `metadata`, and no `version` in a plugin
entry. Claude Code's marketplace reference
(<https://code.claude.com/docs/en/plugin-marketplaces>, read as documentation
on 2026-09-03) puts the field in the marketplace schema's *Optional fields*
table, whose whole description of it is "Marketplace manifest version", and
adds under that table: "`description` and `version` are also accepted under
`metadata` for backward compatibility." Optional is what lets the rule above
decide the rest: a version no machine writes is a version somebody moves by
hand, and this one already had — `0.3.0` in the index against a package the
release had moved to `0.3.1`. A plugin entry is left without one because the
same page describes that field as a second pin beside the manifest's: "Plugin
version. If set (here or in `plugin.json`), the plugin is pinned to this
string and users only receive updates when it changes. A plugin with a
`command` source isn't pinned by either field. If set in neither place, the
version comes from the next source in version management." Of those two
places, `plugin.json` is the one a machine keeps current.

§10.2 is untouched by any of it: clients *MAY* use `version` to decide
whether an update exists or a cache is stale, and Claude Code does. The
consequence is accepted rather than worked around — a change to a package
between two releases reaches such a client at the next release, which follows
the next merge to how-possible's `main`, and not before.

## Text only

No executables and no built artefacts are stored in the tree. Released
binaries are published elsewhere and referenced from here; the only things
this repository runs are its own two checks, and
`.github/workflows/conformance.yml` runs both.

The second is `tools/check-release-record.py`, and it lives outside
`check-conformance.py` on purpose. That script's remit is installability
against the published specification, and the section above allows a
hand-written check inside it only where the check expresses a rule JSON
Schema cannot express, with its clause beside it, or turns a schema rejection
into a message somebody can act on. A hand-moved version is neither: it
breaks nothing about the package's shape, and a package whose `version` and
`binaries.json` disagree still validates. What the script reads is text a
machine wrote, or the absence of text no machine writes, three times over. It
holds `plugin.json`'s `version` to the `version` and the `tag` the release
writes into `plugins/howp/binaries.json` — three strings from one release
commit, so a disagreement is a hand edit and not an opinion. It refuses a
release URL naming a tag anywhere in the text under `plugins/` or in
`README.md`, `binaries.json` excepted because that is the one file a release
rewrites: nothing in the release path can rewrite a sentence, so a tag in
prose is a claim the next release falsifies in silence
(`.agents/rules/claims.md`). And it refuses a `version` key anywhere in
`.claude-plugin/marketplace.json`, which nothing writes, so a version there
is one somebody has to remember to move. No hit of any of the three needs a
reader's judgement. That is the test for a check
belonging in this tree at all: not whether it is committed, but whether a hit
of it can be wrong.

If this file and the things it describes ever disagree — the specification,
the script, the workflow — they are right and this file is stale.
