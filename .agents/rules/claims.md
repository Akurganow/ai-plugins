# Claims

This repository is read by people deciding whether their client can install
something. Every sentence about a client is therefore a claim someone will
act on, and the standing rule is that a claim names where it was read.

## The rule

- **Documentation first, source only where it does not answer.**
  An order rather than a choice, and the owner set it: a pass that works
  source-first is invalid and its conclusions are not used, however right
  they turn out to be. "The documentation is unreachable" is a claim to be
  tested, not accepted — and a vendor whose site is blocked usually publishes
  the same pages as Markdown in its own repository, which is documentation
  and is read first.
- **Cite the source, in the text, and say which kind it is.** A statement
  about a client's behaviour cites that client's documentation or its source,
  by link, at the place the statement is made — not in a commit message, not
  in a review thread — and says, per fact, which of the two it came from, or
  that it came from running the client's own code. `README.md` does this
  today for every surface it lists.
- **Say what was not verified.** `README.md` opens the install section by
  saying nothing below has been installed from this repository as published.
  That sentence is load-bearing; it is not softened, moved to a footnote, or
  quietly upgraded because a package "should" work — and testing a fix in a
  working tree does not retire it, because what is published is what a reader
  will install.
- **Never invent a command.** Where a client's install command could not be
  verified, none is stated and the reason is given. Declining to answer is a
  correct answer here; a plausible command that does not exist is worse than
  a gap, because a gap is visible.
- **Separate "the standard says" from "this client does".** The first is
  quotable from a specification and stays true. The second is only as good as
  the client's own source and can change without notice, so it is attributed
  and dated by its link rather than stated as a property of the world. A link
  into a moving branch does not date anything: cite a commit permalink.
- **A supported-surface list is a list of obligations.** A row is added when
  there is a source for it, and it is removed rather than left standing when
  the source stops supporting it.

## Why it is written down rather than assumed

Fluent, confident, unsourced compatibility text is the easiest thing in this
repository to produce and the hardest thing to catch in review — it reads
exactly like the sourced kind. The rule is not "be careful"; it is that a
claim without a citation next to it is treated as not yet written, whoever
wrote it.

Where this file describes what `README.md` currently says, `README.md` is the
truth and this file is stale — the standard above is the durable part, the
examples are only current. The sourcing order is owned here rather than
borrowed: this file is where it is written down, and it defers outward to
nothing — a rule that lives somewhere the reader cannot open is a rule this
repository does not really have.
