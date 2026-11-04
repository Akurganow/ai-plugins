---
contract_version: 3
---

# Constitution of Akurganow/pegboard

## Read first

- AGENTS.md
- .agents/rules/conformance.md
- .agents/rules/claims.md
- .agents/rules/slop.md "What is protected"
- docs/design.md

## Departments

- abstractions: judged by .agents/rules/design-vocabulary.md
- proportion: judged by .agents/rules/design-vocabulary.md
- text-residue: judged by .agents/rules/slop.md
- claims: judged by .agents/rules/claims.md
- tests: judged by .agents/rules/tests.md

## Fence

- The conformance check (`python tools/check-conformance.py`), the evals runner selftest and folder check (`python tools/evals.py selftest`, `python tools/evals.py validate`), the regeneration diff (`bash tools/regenerate.sh`, which runs `tools/build.sh` and so its limits on the prose-discipline short form) run on every pull request and on pushes to main, in the `check` job: .github/workflows/conformance.yml
- A pull request commit that touches src/, bundles/ or plugins/ must be a conventional commit, in the `commits` job: .github/workflows/conformance.yml
- A pull request commit that changes src/, LICENSE, tools/build.sh or tools/regions.sh must carry the builds it produces: .github/workflows/conformance.yml
- The client validators run on every pull request and on pushes to main: `claude plugin validate` on each bundles/<name> and on .claude-plugin/marketplace.json, and `skills-ref validate`, `hermes plugins validate` and `hermes plugins doctor --ci` on each plugins/<name>: .github/workflows/conformance.yml
- Every package installs into Claude Code, Codex and Oh-My-Pi on Linux, macOS and Windows, and into Hermes on Linux and macOS, on every pull request and on pushes to main: .github/workflows/integration.yml
- The fence does not run a skill against a model on a pull request. .github/workflows/evals.yml runs after a release or by hand.
- The fence does not lint, type check or scan for unused code. A dead function in tools/ passes it.
- The fence does not exercise .github/workflows/release.yml on a pull request. A break in the release job passes it.
- The fence does not read .agents/ and does not judge what a sentence says.

## Regression proof

- python3 tools/check-conformance.py
- python3 tools/evals.py selftest
- python3 tools/evals.py validate
- bash tools/regenerate.sh
- git add --intent-to-add --all
- git diff --exit-code

## Not judged

- .claude-plugin/marketplace.json
- .agents/plugins/marketplace.json
- .omp-plugin/marketplace.json
- .cursor-plugin/marketplace.json
- bundles
- plugins
- src/cognitive-load/CHANGELOG.md
- src/design-review/CHANGELOG.md
- src/prose-discipline/CHANGELOG.md
- src/toc-thinking/CHANGELOG.md
- src/triz-thinking/CHANGELOG.md
- plugins/howp/binaries.json
- plugins/howp/skills/forecast/references/commands.md
- tools/schemas
- tools/evals-fixtures
- tools/package-lock.json
- evals

## Execution

- Run code only in a copy under the run directory. Never run it in the clone.
- The tree expects the Python version and the `jsonschema` and `pyyaml` versions that .github/workflows/conformance.yml pins.
- The tree expects the Node.js major that .github/workflows/conformance.yml pins, with npm and jq, for tools/regenerate.sh.
- tools/regenerate.sh installs doctoc from tools/package-lock.json when tools/node_modules does not match it. That install needs the npm registry.
- tools/check-conformance.py reads the tree in place. Everything else a run writes goes under the run directory.

## Executor loads

- .agents/rules/conformance.md
- .agents/rules/claims.md
- .agents/rules/slop.md
- CONTRIBUTING.md

## Labels

- `needs-human` (owner attention): Lawman cannot decide this issue alone. A person decides on it.
- `install`: A package does not install or load in a client
- `package`: A proposal for a new package
- `bug`: Something isn't working
- `documentation`: Improvements or additions to documentation
- `duplicate`: This issue or pull request already exists
- `enhancement`: New feature or request
- `good first issue`: Good for newcomers
- `help wanted`: Extra attention is needed
- `invalid`: This doesn't seem right
- `question`: Further information is requested
- `wontfix`: This will not be worked on
- `accessibility`: Barrier affecting people with disabilities

## Precedents

none

## Licenses

reaches copies
use non-commercial
sources deps-dev,npm-registry,clearly-defined
