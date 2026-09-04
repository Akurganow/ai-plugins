# Working unattended

How an **analysis run** works in this repository when nobody is present to
answer: any unattended run whose whole job is reading, judging and
reporting. An autonomous session that *implements* a change is a different
animal: it commits and pushes by design, and this file does not govern it.

The other rule files say what is true of this repository; this one says
what is true of running in it alone. Where a detail below is specific to
one vendor's cloud environment, it says so — an agent running elsewhere
skips that detail, not the rule it serves.

## GitHub: REST, and probe what you need

In an Anthropic cloud session, GitHub traffic goes through a proxy that
serves **only a pinned set of pull-request GraphQL operations**. Everything
else on the GraphQL endpoint fails:

    403 This GraphQL query is not enabled for this session — only the pinned
    set of PR-review operations is served. Use REST via
    `gh api repos/{owner}/{repo}/...` instead.

`gh issue list`, `gh issue view`, `gh issue edit`, `gh repo view` and
`gh release list` are GraphQL-backed — do not use them there. Prefer the
session's built-in GitHub tools when it has them; otherwise `gh api` (REST).
Take the repository from the clone, not from `gh repo view`:

    # two substitutions on purpose: ERE has no lazy quantifier, so a single
    # pattern with an optional `(\.git)?` tail lets the greedy class swallow
    # the suffix and returns "owner/repo.git" for SSH-style remotes.
    R=$(git remote get-url origin | sed -E 's#\.git$##; s#.*[:/]([^/]+/[^/]+)$#\1#')

    # repository metadata (description, topics, homepage, license):
    gh api repos/$R --jq '{description, topics, homepage, license: .license.spdx_id}'

    # releases:
    gh api repos/$R/releases --paginate --jq '.[] | {tag_name, name, published_at}'

    # open issues carrying a label. REST /issues returns pull requests too —
    # the select() is required, `gh issue list` used to do it for you.
    gh api -X GET repos/$R/issues --paginate -f state=open -f labels=<label> \
      --jq '.[] | select(.pull_request | not)
            | {number, title, body, created_at, html_url, labels: [.labels[].name]}'

    gh api -X GET repos/$R/issues --paginate -f state=closed -f labels=<label> \
      --jq '.[] | select(.pull_request | not) | {number, title, body, state_reason}'

    gh api repos/$R/issues/<n>/comments --paginate --jq '.[] | {user: .user.login, body, created_at}'

    gh api -X POST repos/$R/issues            --input issue.json     # {"title":…,"body":…,"labels":[…]}
    gh api -X POST repos/$R/issues/<n>/comments --input comment.json # {"body":…}
    gh api -X POST repos/$R/issues/<n>/labels -f 'labels[]=<label>'
    gh api -X POST repos/$R/labels -f name=<label> -f color=<hex> -f description=<text>

Creating a label that already exists answers `422`; treat that as success,
and create every label before its first use — a create that names a missing
label fails after the analysis it was meant to publish.

**Never gate a run on `gh auth status`.** In a cloud session `GH_TOKEN`
reads the literal placeholder `proxy-injected` and the real credential lives
outside the container, so the status check can fail while access is fine —
and an unattended run that stops there has spent itself on nothing. Probe
the thing actually needed:

    gh api repos/$R --jq .full_name

If that fails, stop and say so in the final report. If `gh` is missing and
the session has no built-in GitHub tools either, stop and say that.

## The network is allowlisted

The session's egress goes through a proxy with an allowlist. A reference
source this repository's checks lean on — a specification site, a style
guide, a vendor's documentation — may simply be unreachable, answering
`403` with `x-deny-reason: host_not_allowed`. A blocked source is reported
as blocked, and the checks that depend on it are reported as not run —
never guessed at. `.agents/rules/claims.md` owns what a claim may rest on;
nothing about a blocked fetch loosens it.

## The clone is shallow

A cloud session's clone is truncated (`.git/shallow` exists). Before
anything that reads history — `git log`, `git blame`, tag archaeology —
run:

    git fetch --unshallow --quiet || true
    test -e .git/shallow && echo "STILL SHALLOW: unshallow failed, history is truncated"

The `|| true` keeps an already-full clone from failing the run, but it also
swallows a real fetch failure — hence the second line. If the marker file is
still there, the fetch did not happen: say so in the report, and treat every
history-based conclusion as drawn from truncated history, because it was.

## Keep run state in files, not in context

Long unattended runs get their context compacted, and a compaction can drop
exactly the thing that mattered at the last step. Anything that must still
be true at the end — a do-not-report list, collected findings, verdicts —
goes to disk the moment it is learned, outside the working tree. The state
directory is **per-run, never a fixed shared path**, so that two concurrent
runs cannot overwrite each other's state:

    RUN=$(mktemp -d /tmp/run.XXXXXX)

Re-read those files immediately before acting on them, and hand a subagent
the path to a long record rather than its text.

## Leave no trace

Running the repository's checks, fetching sources and writing throwaway
files are all allowed. A check that reads the tree in place — the
conformance check does — runs in place; everything a run *writes* goes
under its own `$RUN` directory, never into the working tree. An analysis
run must not commit, stage, push, or leave any modification behind: it
finishes with `git status --porcelain` empty and says so in its report. A run whose whole job is analysis has no business
changing what it analysed.

## Report honestly

Name the command and show what it printed; quote a file with its path and
line. A check that was not run — a blocked source, a missing tool — is
reported as not run, not as passing, and not omitted. The conformance check
is `python3 tools/check-conformance.py` and `.agents/rules/conformance.md`
owns what it does and does not prove; "it looks right" is not a result the
check produced. Unattended this matters twice over, because nobody was
watching: the report is the only record that the run did what it claims.
Never invent a path, a line number or command output.
