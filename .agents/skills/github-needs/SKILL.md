---
name: github-needs
description: "What an unattended analysis run of this repository needs from GitHub, stated as needs and never as routes. It defines the machine population, and lists the probe, the listings, the reads of one issue, the full-set label write and the close. It also holds the audit every fire owes and where a run finds its environment's facts. Read it before acting as the Issue Court or the Tracker Clerk."
---

# What a run needs from GitHub

Two roles read this file: the Issue Court and the Tracker Clerk. The four
pipeline roles read its first section, which `pipeline-law` cites.

It names **what** a run needs and never **how** it is reached.
`.agents/rules/unattended.md` owns that rule: a run reaches GitHub through
whatever route its environment gives it, and the route is not recorded here.
Each environment has its own, so the route stays with whatever fired
you.

## The machine population

This is the one definition. Every other skill names the machine population
and points here; none restates it.

An issue is in the machine population when both hold:

- it carries the label `police-report`;
- its body carries a fingerprint line. That is an HTML comment on a line of
  its own that begins `<!-- `, outside any code block. Its text begins with
  a word ending `-fingerprint:` or with `repo-audit-routine:`.

A marker quoted in a sentence or in a code block counts for nothing.

Every filer writes `<!-- police-fingerprint: <role> <value> -->`. `<role>` is
the skill name of the role that filed it. `<value>` is the finding's identity,
in the form the filer's skill gives. One filer is not a role: the evals
runner, `tools/evals.py`, writes `evals` as `<role>` and
`<package>/<skill>@<client>` as `<value>`. It files nothing whose fingerprint
line is already on an open issue. The older prefixes stand on issues
already filed, and no filer writes them.

**No issue belongs to a role.** `<role>` records who filed, and grants
nothing. Every role that reads the tracker lists the population, never a
subset by filer. The Issue Court and both Clerks do.

**Dedupe.** A filer files nothing whose finding an open issue in the
population already carries. That holds whatever role filed it and whatever
its line's prefix. A finding is the same when its fingerprint value names the
same file and concept. It is also the same when the issue states the same
defect in other words. A part the pipeline Clerk cuts from its parent is
not a second filing of the parent's finding.

An issue outside the population exists for no role. No role lists it,
reads it, comments on it, labels it or closes it.

Every filer applies `police-report` when it files. A filer that cannot
confirm the label on the repository's label list files nothing, and says so
in its report.

## The audit every fire owes

A record that says work was done is evidence that a fire reached the subject.
It is never evidence that the work landed. **So no fire ends because a marker
or a label says its work is already done.** It checks what the record names,
completes what is missing, and says what it checked.

That rule replaces every "already done, so skip" shortcut in a role that
reads this file. Where it meets an older decision, it wins. The owner settled
that a decision's age ranks it, the recent one wins, and every role repairs.

**An audit is owed** whenever a fire finds a marker of its own on a subject
it came to work, before doing the work. The marker may be the comment it
would have posted, the close it would have made, or the issue it would have
filed.

**An audit may:**

- apply a label that should already stand;
- post a comment only where no comment of its own exists for that subject;
- finish a write its own previous fire left half done.

**An audit may never:**

- post a second comment on the same subject;
- create a label;
- file a new issue or re-file a fingerprint;
- reopen anything;
- spend a cap or a count a marker already records as spent;
- take an irreversible act on the audit's authority alone.

**Where a read does not settle whether the work landed, the audit reports and
writes nothing.** A repair that corrupts is worse than a stall somebody can
see. This binds a close in particular. A state you cannot explain from the
record is a report line.

**It is bounded.** It reads what the fire already holds: the listing, the
bodies, the comments, the labels. It re-derives evidence only where a cheap
read came back wrong, never as a standing pass. It never re-runs a trial, a
triage or an analysis that a marker already records.

**Then the fire either works or exits.**

- Audit clean and the work genuinely done: exit, saying what was audited.
- Audit clean and the work not done: do the work.
- Audit found a gap: close the gap, then exit saying what was closed.

An exit that reports nothing audited is a fire that wasted itself.

## Your environment

**The measured facts of an environment** are not in this repository and never
will be. They are what the network refuses and allows, and what an
interpreter or a package index did there. They belong to whatever fired you,
which carries them, and you read them there. A caller that carries none is a
report line. Treat every environment-dependent check as not run rather than
guessing at one.

## The needs

- **GitHub.** Reach it through whatever route this environment gives
  you; the route is not recorded here. What a run needs, and what it
  does where a route serves a need differently:
  - the probe: the cheapest read that touches `Akurganow/ai-plugins`,
    before any analysis, per `unattended.md`;
  - metadata: description, homepage, license — and topics, which a
    route may not return: where it does not, report topics as not
    checked;
  - releases, and tags, and a release's assets by name, which is how
    `evals.json` is read;
  - issues by label and state, with full bodies, paginated to the end.
    The label is mandatory: every issue listing names `police-report`,
    alone or beside another label, and none is ever made without it. A
    route may return pull requests in an issue listing: filter them out;
  - pull requests, open or all, with number, title, head, head
    repository, labels, body, whether it merged, when it closed, and the
    paths each one touches;
  - the comments on one issue, and the labels on one issue;
  - an issue's place in a hierarchy: whether it has a parent and whether
    it has parts, which a listing may not carry; its parts, in the
    parent's order; and its parent;
  - whether a label exists: confirm every name you intend to apply.
    Nothing here creates one, so a name that cannot be confirmed is
    dropped. The exception is `police-report`: a filer that cannot
    confirm it files nothing (see **The machine population**);
  - file an issue with a title, a body and labels; comment on one;
  - add a label to an existing issue: read the whole set first and send
    it back complete with the new name — a route may replace the set
    rather than add to it, so a set you did not read back in full is a
    set you silently deleted;
  - close an issue with a reason — completed, not planned, or duplicate
    naming the survivor. Send no label set with a close: the labels must
    come through untouched.
