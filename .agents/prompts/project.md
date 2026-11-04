# What this repository is

Composable project context: what the marketplace is and which of its
properties must survive a change. The rules of engagement are in
`.agents/prompts/base.md` and `.agents/rules/`; this file is the subject
matter.

## The shape

`src/<name>/` is the hand-written source of a package, and no client reads it.
`tools/build.sh` writes two builds from it. `plugins/<name>/` is an Agent
Plugins 1.0.0 package: the manifest at the plugin root, skills under
`skills/<name>/SKILL.md`. `bundles/<name>/` is one tree with a manifest folder
per client and no root manifest. Four catalogues index the bundles:
`.claude-plugin/marketplace.json`, `.agents/plugins/marketplace.json`,
`.omp-plugin/marketplace.json` and `.cursor-plugin/marketplace.json`. Each is
a client's index, outside the standard, pointers only, labelled for what it
is.

`tools/check-conformance.py` decides by the published schema everything the
published schema can decide, and implements by hand the rules a JSON Schema
cannot express — where files sit, what symlinks resolve to, what a skill's
front matter says — plus a short list of deliberate duplicates of the schema,
kept because they turn a schema rejection into a line somebody can act on.
`tools/schemas/` holds a verbatim copy of the published manifest schema, with
its provenance and checksum recorded. `tools/source.schema.json` closes the
fields of each `src/<name>/source.json`.

## Properties that must survive any change

- **The specification is the authority.** A client's behaviour is evidence
  about that client, not about what the package should be. Where they
  disagree, the package follows the specification and the client's behaviour
  is recorded as a note with a source.
- **Every compatibility claim is sourced.** Install instructions, supported
  surfaces, loader behaviour — each names the documentation or the source
  file it was read from.
- **The repository holds text only.** No executables, no compiled
  artefacts. Released binaries live elsewhere and are referenced. The one
  exception is each bundle's listing icon, a PNG the builder renders from
  `src/<name>/icon.svg`.
- **One source per fact.** Each package has one hand-written source,
  `src/<name>/`. Everything under `bundles/` and `plugins/`, and each
  catalogue, is a copy that `tools/build.sh` writes. CI runs the scripts and
  fails on any difference, so a copy cannot drift, and a copy edited by hand
  is the defect. The specification is explicit that nothing besides the root
  manifest may supplement or override it in an Agent Plugins package, so
  `plugins/<name>/` holds no other manifest.
- **Nothing here is client-specific except what a standard does not
  define**, and that is labelled as such.
