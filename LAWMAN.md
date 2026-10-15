---
contract_version: 1
---

# Constitution of Akurganow/ai-plugins

## Read first

- AGENTS.md
- .agents/rules/conformance.md
- .agents/rules/claims.md
- .agents/rules/slop.md "What is protected"
- docs/design.md

## Departments

- abstractions: judged by .agents/skills/police-law/references/design-vocabulary.md

## Fence

- The conformance check (`python tools/check-conformance.py`), the evals runner selftest and folder check (`python tools/evals.py selftest`, `python tools/evals.py validate`), the regeneration diff (`bash tools/regenerate.sh`) and the size bound on plugins/prose-discipline/rules/prose-discipline.md run on every pull request and on pushes to main, in the `check` job: .github/workflows/conformance.yml
- A pull request commit that touches plugins/ must be a conventional commit, in the `commits` job: .github/workflows/conformance.yml
- The client validators `claude plugin validate`, `skills-ref validate`, `hermes plugins validate` and `hermes plugins doctor --ci` run on every pull request and on pushes to main: .github/workflows/conformance.yml
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
- plugins/cognitive-load/.claude-plugin/plugin.json
- plugins/design-review/.claude-plugin/plugin.json
- plugins/howp/.claude-plugin/plugin.json
- plugins/prose-discipline/.claude-plugin/plugin.json
- plugins/toc-thinking/.claude-plugin/plugin.json
- plugins/triz/.claude-plugin/plugin.json
- plugins/cognitive-load/LICENSE
- plugins/design-review/LICENSE
- plugins/howp/LICENSE
- plugins/prose-discipline/LICENSE
- plugins/toc-thinking/LICENSE
- plugins/triz/LICENSE
- plugins/cognitive-load/CHANGELOG.md
- plugins/design-review/CHANGELOG.md
- plugins/prose-discipline/CHANGELOG.md
- plugins/toc-thinking/CHANGELOG.md
- plugins/triz/CHANGELOG.md
- plugins/howp/binaries.json
- plugins/howp/skills/forecast/references/commands.md
- tools/schemas
- tools/evals-fixtures
- tools/package-lock.json
- evals
- .agents

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

## Precedents

none
