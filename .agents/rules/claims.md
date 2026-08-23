# Claims

This repository is read by people deciding whether their client can install
something. Every sentence about a client is therefore a claim someone will
act on, and the standing rule is that a claim names where it was read.

## The rule

- **Cite the source, in the text.** A statement about a client's behaviour
  cites that client's own documentation or its own source, by link, at the
  place the statement is made — not in a commit message, not in a review
  thread. `README.md` does this today for every surface it lists.
- **Say what was not verified.** `README.md` says that none of the listed
  clients has been tested against this repository, because none has. That
  sentence is load-bearing; it is not softened, moved to a footnote, or
  quietly upgraded because a package "should" work.
- **Never invent a command.** Where a client's install command could not be
  verified, none is stated and the reason is given. Declining to answer is a
  correct answer here; a plausible command that does not exist is worse than
  a gap, because a gap is visible.
- **Separate "the standard says" from "this client does".** The first is
  quotable from a specification and stays true. The second is only as good as
  the client's own source and can change without notice, so it is attributed
  and dated by its link rather than stated as a property of the world.
- **A supported-surface list is a list of obligations.** A row is added when
  there is a source for it, and it is removed rather than left standing when
  the source stops supporting it.

## Why it is written down rather than assumed

Fluent, confident, unsourced compatibility text is the easiest thing in this
repository to produce and the hardest thing to catch in review — it reads
exactly like the sourced kind. The rule is not "be careful"; it is that a
claim without a citation next to it is treated as not yet written, whoever
wrote it.
