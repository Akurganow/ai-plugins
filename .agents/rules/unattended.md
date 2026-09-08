# Working unattended

How an **analysis run** works in this repository when nobody is present to
answer: any unattended run whose whole job is reading, judging and
reporting. An autonomous session that *implements* a change is a different
animal: it commits and pushes by design, and this file does not govern it.

The other rule files say what is true of this repository; this one says
what is true of running in it alone. It names what a run needs and how a
run behaves when a need is not met. Which tool reaches GitHub from a given
environment, which hosts its network passes, what is installed — those are
facts about the environment, and they belong with whoever runs the
analysis there, not in a public repository that other people clone into
environments of their own.

## GitHub: what a run needs, and probe it

A run reads and writes the tracker through whatever route its environment
gives it. This file does not name the route; it names the needs, so that a
run can tell before analysing anything whether its environment serves
them:

- the repository's metadata — description, topics, homepage, license;
- its releases and tags;
- its issues carrying a given label, open and closed, **with full
  bodies** — the fingerprint at the foot of a body is an issue's identity,
  and a listing that returns titles alone cannot build the do-not-report
  list `.agents/rules/tracker.md` requires;
- the comments on an issue;
- filing an issue with a title, a body and labels; commenting on one;
  adding a label to one;
- whether a label exists on the repository.

Take the repository from the clone, never from an API call:

    # two substitutions on purpose: ERE has no lazy quantifier, so a single
    # pattern with an optional `(\.git)?` tail lets the greedy class swallow
    # the suffix and returns "owner/repo.git" for SSH-style remotes.
    R=$(git remote get-url origin | sed -E 's#\.git$##; s#.*[:/]([^/]+/[^/]+)$#\1#')

Then **probe the thing actually needed** — the cheapest read that touches
this repository — before any analysis. Never gate a run on an
authentication status command: such a command answers about a credential,
not about access, and an unattended run that stops on it has spent itself
on nothing. If the probe fails, stop and say so in the final report; a
need the environment cannot serve at all is reported as not served, and
whatever depended on it as not checked.

Two things a route may do differently, and what the run does about each:

- A listing of issues may return pull requests among them. Filter them
  out; a pull request is never a case, a finding or a fingerprint.
- Labels are checked before their first use — every name a run intends to
  apply, before the analysis rather than after it. Where the route can
  create a label, create it first, and treat "already exists" as success.
  Where it cannot, a missing name is a line in the report and the issue is
  filed without it; an issue's identity is its fingerprint, never a label.
  A name applied without checking may create the label silently, which
  is a change to the repository nobody decided on.

## The network is allowlisted

The session's egress may pass through a proxy with an allowlist. A
reference source this repository's checks lean on — a specification site,
a style guide, a vendor's documentation — may simply be unreachable. A
blocked source is reported as blocked, with the reply the environment
gave, and the checks that depend on it are reported as not run — never
guessed at. `.agents/rules/claims.md` owns what a claim may rest on;
nothing about a blocked fetch loosens it.

A source blocked as a site may be published a second way — the same text
in a public repository, the same page as a raw file — and that way may be
open when the site is not. `claims.md` already calls such a copy
documentation and reads it first; here it is also the route. Read it from
the copy, keep the copy under `$RUN`, and cite the file and the commit the
copy was at, never the blocked page. A source with no such copy stays
blocked, and the checks that lean on it stay not run.

The conformance check's own dependencies come over the same network. A
transient failure installing them — a timeout, a reset — is retried once;
only a second failure makes the check not run, and then the report says
so, with the output.

## The clone may be shallow

A session's clone may be truncated (`.git/shallow` exists when it
is). Before anything that reads history — `git log`, `git blame`, tag
archaeology — run:

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
