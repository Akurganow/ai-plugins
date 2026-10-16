# Dependencies

Where this repository pins third-party versions, and what an update must not
break. Read the inventory from the tree at the commit analysed, and never copy
a version from this file.

## Where the pins live

1. **Actions.** Every `uses:` line in `.github/workflows/*.yml`, with its
   commit sha and the version in its trailing comment. A comment and a sha
   that disagree are a report line.
2. **Pinned installs in `run:` steps.** The pip pins (`jsonschema==`,
   `pyyaml==`) and `skills-ref` at a commit. Also the npm clients at an exact
   version, the Hermes commit in `HERMES_COMMIT`, and the cocogitto release
   with its sha256. Also the bun version and the node major.
3. **Lockfile.** `tools/package.json` and `tools/package-lock.json`, whose one
   direct dependency is installed by `tools/regenerate.sh`.
4. **Imports.** What `tools/check-conformance.py` and `tools/evals.py` import.
   The standard library is not a dependency. A package imported there must
   appear in item 2.

## What CI does not prove

- `.github/workflows/conformance.yml` proves a pin installs and validates. It
  does not prove the pin is the right one.
- `.github/workflows/integration.yml` installs the pinned clients on three
  operating systems. A candidate that breaks that install shows only after the
  bump, so the changelog is read before.
- `.github/workflows/evals.yml` installs `@latest` of each client. Those
  installs are floating and have no pinned version to move.

## Where an update lands

- **A workaround for the upstream.** Comments in the workflows, `tools/` and
  the rule files that name a version, a bug or a floor. The Node and bun
  floors carry such comments.
- **A step the update makes pointless.** The cocogitto step "Refuse to release
  a package with no seed tag" in `.github/workflows/release.yml` rests on a
  cited line of cocogitto's source. If the upstream changes that line, the
  step may go.
- **A promise this repository keeps.**
  - `docs/clients.md` states what each pinned client version did. A bump
    makes every such sentence a claim about a version nothing re-measured.
  - `README.md` states install commands for four clients. An entry that
    renames, removes or changes one of them breaks a promise.
  - An action input a comment depends on, such as `persist-credentials: false`
    on `actions/checkout`, and `DISABLE_AUTOUPDATER` for Claude Code.
  - The byte identity of generated files. A `doctoc` change that alters its
    output changes what `tools/regenerate.sh` writes, and CI then fails on
    every pull request.
- **The other direction.** An entry that deprecates or removes something this
  repository calls breaks it, even when the version number looks minor.

Before a bump, list every file that quotes the version being moved.
`grep -rn '<version>' .github docs README.md plugins tools` finds them.
