# What this repository is

Composable project context: what the marketplace is and which of its
properties must survive a change. The rules of engagement are in
`.agents/prompts/base.md` and `.agents/rules/`; this file is the subject
matter.

## The shape

`plugins/<name>/` is an Agent Plugins 1.0.0 package: the manifest at the
plugin root, skills under `skills/<name>/SKILL.md`. A vendor discovery path
inside a package is a symlink to the real manifest, never a second copy of
it. `.claude-plugin/marketplace.json` at the repository root is a client's
index — outside the standard, pointers only, labelled for what it is.

`tools/check-conformance.py` decides by the published schema everything the
published schema can decide, and implements by hand the rules a JSON Schema
cannot express — where files sit, what symlinks resolve to, what a skill's
front matter says — plus a short list of deliberate duplicates of the schema,
kept because they turn a schema rejection into a line somebody can act on.
`tools/schemas/` holds a verbatim copy of the published manifest schema, with
its provenance and checksum recorded.

## Properties that must survive any change

- **The specification is the authority.** A client's behaviour is evidence
  about that client, not about what the package should be. Where they
  disagree, the package follows the specification and the client's behaviour
  is recorded as a note with a source.
- **Every compatibility claim is sourced.** Install instructions, supported
  surfaces, loader behaviour — each names the documentation or the source
  file it was read from. What was not verified says so.
- **The repository holds text only.** No executables, no built artefacts.
  Released binaries live elsewhere and are referenced.
- **One manifest per package.** A second `plugin.json` anywhere below a
  plugin root is acceptable only as a symlink to the root one; a real copy
  would drift, and the specification is explicit that nothing else may
  supplement or override the root manifest.
- **Nothing here is client-specific except what a standard does not
  define**, and that is labelled as such.
