---
name: github-needs
description: "What an unattended analysis run of this repository needs from GitHub, stated as needs and never as routes. It defines the machine population, and lists the probe, the listings, the reads of one issue, the full-set label write and the close. Read it before acting as the Issue Court, the Tracker Clerk, the Repo Police, the Slop Police or the Agent Police."
---

# What a run needs from GitHub

Five roles read this file. The four analysis roles are the Issue Court,
the Tracker Clerk, the Repo Police and the Slop Police. The fifth is the
Agent Police, which patrols the other eight roles. The four pipeline roles
read its first section, which `pipeline-law` cites.

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
  `police-fingerprint:`, `repo-audit-routine:`, `slop-police-fingerprint:`,
  `agent-police-fingerprint:` or `special-police-fingerprint:`.

A marker quoted in a sentence or in a code block counts for nothing.

Every filer writes `<!-- police-fingerprint: <role> <value> -->`. `<role>` is
the skill name of the role that filed it. `<value>` is the finding's
identity, in the form the filer's skill gives. The four other prefixes
stand on issues already filed, and no filer writes them.

**No issue belongs to a role.** `<role>` records who filed, and grants
nothing. Every role that reads the tracker lists the whole population. The
three police, the Issue Court and both Clerks do.

**Dedupe.** A filer files nothing whose finding an open issue in the
population already carries. That holds whatever role filed it and whatever
its line's prefix. A finding is the same when its fingerprint value names the
same file and concept. It is also the same when the issue states the same
defect in other words.

**A role's filings** are the open issues in the population whose `<role>`
names it. They set its backpressure cap and the filing audit its skill
gives, and nothing else. An older prefix counts for one role:
`repo-audit-routine:` for `repo-police`, `slop-police-fingerprint:` for
`slop-police`, and `agent-police-fingerprint:` for `agent-police`.
`special-police-fingerprint:` counts for no role.

No other issue exists for any role. No role lists it, reads it, comments
on it, labels it or closes it.

Every filer applies `police-report` when it files. A filer that cannot
confirm the label on the repository's label list files nothing, and says so
in its report.

## The needs

- **GitHub.** Reach it through whatever route this environment gives
  you; the route is not recorded here. What a run needs, and what it
  does where a route serves a need differently:
  - the probe: the cheapest read that touches `Akurganow/ai-plugins`,
    before any analysis, per `unattended.md`;
  - metadata: description, homepage, license — and topics, which a
    route may not return: where it does not, report topics as not
    checked;
  - releases, and tags;
  - issues by label and state, with full bodies, paginated to the end.
    The label is mandatory: every issue listing names `police-report`,
    alone or beside another label, and none is ever made without it. A
    route may return pull requests in an issue listing: filter them out;
  - pull requests, open or all, with number, title, head, labels and
    body, and the paths each one touches;
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
