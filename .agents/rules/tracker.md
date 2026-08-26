# Filing issues from an automated run

The protocol any unattended analysis follows when its output is a GitHub
issue. The analysis itself — what to look for, what disqualifies a
candidate, what an issue's body must contain — belongs to whoever runs the
analysis; this file owns the tracker discipline around it, so that every
automated filer behaves the same way and the tracker stays worth reading.

## Silence is the default

Filing an issue is not the goal of a run and is not expected of it. A run
that finds nothing is a successful run and, in a healthy repository, the
common outcome. One issue a maintainer acts on is worth more than five that
are merely plausible; the five teach the reader to ignore the label, and
the one real finding gets ignored with them. When in doubt, stay silent —
the run's report (below) is where doubt goes.

## Before analysing: the do-not-report list

First load what the tracker already holds, with the REST calls from
`.agents/rules/unattended.md`: every issue carrying the run's own label or
fingerprint, open **and** closed, and the whole open list. Read full
bodies, not titles — each automated issue ends with a fingerprint comment,
and the fingerprint is the identity. Build a do-not-report list and write
it to a file (`$RUN/do-not-report.md`, in the per-run state directory
`.agents/rules/unattended.md` prescribes) before any analysis:

- Fingerprint present in **any** state → never report it again. A closed
  issue means a person looked and declined; re-filing is worse than silence.
- An open issue covers the same file and the same rule under different
  wording → no second issue. Materially new evidence becomes a comment on
  the existing issue; anything less is left alone.
- An earlier issue of the run's own is now stale (the file it points at was
  fixed or deleted) → one comment saying so, a note in the report, and the
  issue stays open — closing is a person's call.
- Issues without the run's label are skimmed too: a person may already have
  filed the same thing.

Re-read the file immediately before filing anything — the list must survive
to the moment it is needed, not just the moment it was built.

## Backpressure

An untouched backlog means the maintainer is not consuming what the runs
produce, and adding to it is pure noise. Count the open issues carrying the
run's own label before analysing anything, and cap the run:

| Open issues with the run's label | Maximum filed this run |
| :-- | :-- |
| 0–2 | the run's own cap (its instructions name it) |
| 3–4 | 1 |
| 5 or more | 0 — file nothing, and say so |

When the cap is 0, a light pass still happens so the report is honest, but
nothing is filed. A run's instructions may name one narrow exception that
overrides the cap (a fabricated claim published to readers, a security
problem); absent that, nothing does.

## Verify before you file

For every candidate finding, re-open the file and confirm the quote is
verbatim and the line number is right. Then ask: *if the maintainer
disagreed, what would I show them?* If the answer is only "it feels off",
drop it — taste is not a finding. Every finding rests on a named rule (a
spec clause, a rule file of this repository, a cited external source) or a
demonstrated factual inconsistency between two places in the repository.
Prefer one well-evidenced finding to five weak ones.

A run whose instructions add independent triage on top of this — clean
subagents that re-derive candidates and a ranker whose empty shortlist is a
normal answer — follows them; this section is the floor, not the ceiling.

## Filing

Labels first, created the way `.agents/rules/unattended.md` prescribes —
that file owns the mechanics, including what a duplicate answers. One issue
per finding, never bundled, never more than the cap. Each issue ends with
an HTML-comment fingerprint that names the finding stably enough for the
next run to recognise it — same problem, same file, same fingerprint,
across runs. Immediately before each create, the do-not-report file is
consulted once more.

## The report

Every run ends with a report in a fixed shape, because reports that share a
shape can be compared across weeks:

1. **Coverage** — what was swept (and the commit SHA audited), and what was
   not reached or not checkable, so the next run can start there.
2. **Candidates** — found / cut by the run's own verification.
3. **Filed** — the issues with URLs, or the single line `Filed nothing.`
4. **Strongest rejected** — the two or three best candidates that were not
   filed, with the reason. This is the most useful section of a quiet week.
5. **Blockers** — missing tools, blocked sources, GitHub errors, and the
   `git status --porcelain` result.

Filing nothing is stated in one line, without apology or hedging. The
report is the deliverable of a quiet week; it is not a failed run.

## Hard constraints

- Never modify, commit, or push anything. Never open a pull request. Never
  edit or close issues the run did not create.
- Never exceed the backpressure cap (outside the run's one named exception,
  if it has one), and never re-file an existing fingerprint.
- Never file a finding backed by nothing but taste, and never file an issue
  to demonstrate that the run happened.
- If the conformance check itself cannot run — missing interpreter, missing
  dependency — the report says so and the conformance findings are reported
  as not checked, not as clean.
