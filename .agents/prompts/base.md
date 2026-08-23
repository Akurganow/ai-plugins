# Working agreement

Agent-agnostic on purpose: what any agent working in this repository must
know, whichever vendor it came from. The subject matter is in `project.md`
next to this file; the topic rules are in `.agents/rules/`.

## What this repository is responsible for

Not the text in it — the promise that a client implementing a published
specification can install what is here without knowing anything about this
repository. Every rule here exists to keep that promise checkable rather
than asserted.

## The two things that make a change unmergeable

- `python3 tools/check-conformance.py` does not exit 0.
- A claim about a client is stated without naming where it was read.

The first is mechanical and CI enforces it. The second is not mechanical,
which is exactly why it is written down.

## Language

Everything new is written in English: files, comments, commit messages.
