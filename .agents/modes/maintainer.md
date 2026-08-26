---
id: maintainer
title: Maintainer
policy: repository
---

# Maintainer

The default mode: someone changing this marketplace — adding or updating a
plugin, editing a skill, extending the conformance check, correcting the
README.

The work is small and the standard of proof is high. Read the clause you are
relying on before you rely on it; run `python3 tools/check-conformance.py`
before you claim a package conforms; source every statement about a client —
its documentation first and its source only where the documentation does not
answer (`docs/REQUIREMENTS.md` §5, in the `how-possible` repository), saying
per fact which of the two it was.

Topic rules sit in `.agents/rules/`: what conformance means here and how it
is checked, the sourcing standard for claims, how an unattended analysis
run works alone, and the discipline for filing issues from one. They are
additions to this mode, not a summary of it.
