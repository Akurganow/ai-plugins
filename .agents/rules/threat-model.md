# Threat model

What an outside party could exploit in this repository, and the surfaces
that hold it. A security judgement argues against this model.

## The model

- The repository and its whole history are public. A secret in any commit is
  a published secret, so all of history counts, and not the tree alone.
- Anyone can open an issue or a pull request. `.github/ISSUE_TEMPLATE/config.yml`
  sets `blank_issues_enabled: true`.
- `conformance.yml` and `integration.yml` in `.github/workflows/` run on
  `pull_request`, so they run text a stranger wrote. `release.yml` runs on
  every push to `main` with `contents: write`.
- `release.yml` calls `evals.yml`, which receives API keys and runs model
  clients against released package text.
- `prose-discipline` makes a user's machine run a shell script at the start
  of a session. `README.md`, "Trust", says so.
- The agent roles act with write access to this repository and read issues,
  comments and pull requests that strangers write.

A sentence in `SECURITY.md` or `README.md` about a protection is a claim.
Measure it against the workflow files and the protection settings as read.

## Surfaces

1. **Secrets** in the tree and in all history. The API keys that
   `evals.yml` receives are the inventory. Also every step that could put a
   secret into a public log or a published artifact. `evals.yml` uploads
   each session's record and `tools/evals.py` publishes answers, so read
   `redact` in `tools/evals.py` against what a session can print.
2. **Every workflow under `.github/workflows/` and every script it
   calls.** For each: the trigger, the token permissions, the inputs an
   outsider can influence, and whether such a value reaches a shell, an
   expression, a push, a release or a model client. Titles, bodies, branch
   names, label names and comment text are such values. Give
   `pull_request_target`, `workflow_run` and `secrets: inherit` the closest
   read wherever they appear. The same goes to `release.yml` and
   `evals.yml`, which hold the write token and the keys. A stranger's pull
   request supplies a commit header: trace how it becomes a `CHANGELOG.md`
   entry and release notes, and whether any step treats it as more than text.
3. **Scripts a package runs on a user's machine.**
   `plugins/prose-discipline/hooks/hooks.json` and `print-rules.sh`, and any
   other hook, script or install command under `plugins/`. For each: what it
   reads, who writes that, and whether it reaches a shell, an `eval` or a
   path outside the plugin root. A census of `hooks`, `*.sh` and `curl` over
   `plugins/` finds the others.
4. **The agentic surface.** The roles under `.agents/skills/` and
   `.claude/agents/` act as the owner and read strangers' text. The recorded
   defence is the two-part test of `github-needs`, "The machine population",
   and `pipeline-law`, "What a fired stage trusts". Read each form under
   `.github/ISSUE_TEMPLATE/` for the labels it applies. A form that applies
   `police-report` lets a stranger's issue into the machine population.
5. **Open code-scanning alerts.** Each is a candidate, never a finding.
