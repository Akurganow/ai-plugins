# Tools and scripts

The programs this repository runs, and what to read in each. The tree names
its own scripts: list them with `git ls-files tools .github/workflows plugins`,
filtered to `.py`, `.sh` and `.yml`.

- **`tools/check-conformance.py`.** A wrong result lets a non-conforming
  package merge or blocks a good one. Read each hand check against the clause
  quoted beside it, the front-matter parser, the containment test and the
  byte comparison of vendor manifest copies. `conformance.md` states the
  intended behaviour.
- **`tools/evals.py`.** It reads release assets, runs three clients, compares
  runs and files issues. Read the metric arithmetic and the regression test,
  the tag and version parsing, the listings with their limits and the
  fingerprint match against open issues. Also what `report` does when a
  release lacks an asset or the previous run is partial. Its module
  docstring states the intended behaviour.
- **`tools/regenerate.sh`.** It writes every generated copy. Read the marker
  parsing, the byte comparison, the second-run rule that changes nothing, and
  what a failure midway leaves on disk.
- **The `run:` scripts in `.github/workflows/*.yml`.** `release.yml` writes
  versions and changelogs, pushes the version commit and its tags, and creates
  the releases. `integration.yml` installs every package into four clients.
  `evals.yml` builds the matrix and publishes the runs. Read quoting and pipe
  status under `pipefail`, a loop over a tag list, a `grep` that selects the
  wrong line, and the order of a push against the steps after it.
- **Package scripts**, today `plugins/prose-discipline/hooks/print-rules.sh`,
  which `plugins/prose-discipline/hooks/hooks.json` runs on `SessionStart` and
  `SubagentStart`. Read the paths it builds, the JSON it prints, and how it
  behaves under other awk implementations.
- **Data, not code:** `tools/schemas/`, `tools/node_modules/` and
  `tools/evals-fixtures/`, and the files a release writes.

## Where CI stops

- `conformance.yml` proves the check exits 0 on the committed tree. It does
  not prove the check refuses a package it should refuse. Only a planted
  violation proves that.
- `tools/evals.py selftest` runs `cmd_report` and `report_tag` against fake
  `gh` calls. It does not cover real `gh` behaviour, the assets GitHub
  actually serves, or a real issue create. Those run after a release.
- `release.yml` runs on a push to `main`, and `evals.yml` runs from it or by
  hand. A green pull request says nothing about either.
