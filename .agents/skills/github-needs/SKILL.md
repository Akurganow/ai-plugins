---
name: github-needs
description: "What an unattended analysis run of this repository needs from GitHub, stated as needs and never as routes: the machine population, the probe, the listings, the reads of one issue, the label write that must send the whole set back, and the close. Read it before acting as the Issue Court, the Tracker Clerk, the Repo Police, the Slop Police or the Agent Police."
---

# What a run needs from GitHub

This file is one file and the four analysis agents all read it: the Issue
Court, the Tracker Clerk, the Repo Police and the Slop Police. The Agent
Police reads it too. The four pipeline roles read its first section, which
`pipeline-law` cites.

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
- its body carries the fingerprint line, an HTML comment of the form
  `<!-- police-fingerprint: <role> <value> -->`. `<role>` is the skill name
  of the role that filed it. `<value>` is that role's identity for the
  finding, in the form its skill gives.

An open issue carrying `police-report` and one of three older markers is in
the population too, until it is closed. Each marker belongs to one role:
`repo-audit-routine:` to `repo-police`, `slop-police-fingerprint:` to
`slop-police`, and `agent-police-fingerprint:` to `agent-police`. Every
filer writes only the fingerprint line.

A role's own issues are the issues in the population whose fingerprint line
or older marker names that role.

Every other issue does not exist for any role. No role lists it, reads it,
comments on it, labels it or closes it.

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
    dropped;
  - file an issue with a title, a body and labels; comment on one;
  - add a label to an existing issue: read the whole set first and send
    it back complete with the new name — a route may replace the set
    rather than add to it, so a set you did not read back in full is a
    set you silently deleted;
  - close an issue with a reason — completed, not planned, or duplicate
    naming the survivor. Send no label set with a close: the labels must
    come through untouched.
