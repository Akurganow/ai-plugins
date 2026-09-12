---
name: github-needs
description: "What an unattended analysis run of this repository needs from GitHub, stated as needs and never as routes: the probe, the listings, the reads of one issue, the label write that must send the whole set back, and the close. Read it before acting as the Issue Court, the Tracker Clerk, the Repo Police or the Slop Police."
---

# What a run needs from GitHub

This file is one file and the four analysis agents all read it: the Issue
Court, the Tracker Clerk, the Repo Police and the Slop Police. It was four
byte-identical copies inside four routine bodies until 2026-09-12.

It names **what** a run needs and never **how** it is reached.
`.agents/rules/unattended.md` owns that rule: a run reaches GitHub through
whatever route its environment gives it, and the route is not recorded here.
Each environment has its own, so the route stays with the routine that fired
you.

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
    A route may return pull requests in an issue listing: filter them
    out;
  - pull requests, open or all, with number, title, head, labels and
    body, and the paths each one touches;
  - a fingerprint anywhere in the tracker: a search may be inexact, so
    confirm the marker in each hit's body;
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
