# Spec: `.gitattributes` says every program sits under `tools/`, and a package carries one outside it

## Work item

Pull request #64, built from issue #27. The item corrects prose that describes the
repository's contents as they stood before `plugins/` held more than one package.
At the branch head only one of the filed passages is still live, the program
sentence in `.gitattributes`. This item corrects that sentence and nothing else.

## Problem

**Five of the six filed passages are gone at the head.** The head is `999db5c`,
whose parent is `b8e4271`. The re-check on #27 found passages 3 and 4
rewritten by `10644ee`. Passages 1, 5 and 6 were removed by `24695a5`
(2026-09-25, *"docs: restructure the README around install, plugins and
trust"*); `git log -S` on each quoted string returns it. Each quote, searched
at the head:

| Passage | Quote at filing (`51da31f`) or re-check (`11c6b67`) | At the head |
| :-- | :-- | :-- |
| 1 | `README.md:11-13` "The one program in it is `tools/check-conformance.py`" | `git grep -n 'one program' HEAD -- README.md` prints nothing |
| 3 | `README.md:300-310`, `binaries.json` listed under `plugins/<name>/` | `README.md:135-136` reads, whitespace collapsed, "`binaries.json` howp only: released binaries and their sha256, written by the howp release" |
| 4 | `README.md:317-320` "A plugin's `version`, its `binaries.json` …" | `git grep -n "A plugin's .version." HEAD -- README.md` prints nothing |
| 5 | `README.md:363-366` "covers **both**", `README.md:368` "The vendor symlink is kept" | `git grep -nE 'covers \*\*both|vendor symlink' HEAD -- README.md` prints nothing |
| 6 | `README.md:242-244` "which is the form both entries in this repository's index use" | `git grep -n 'both entries' HEAD -- README.md` prints nothing |

The symlink census has no successor to correct. The vendor manifests stopped
being symlinks and became byte copies. `docs/design.md:29` is headed "The vendor
manifest is a byte copy, not a symlink". `README.md:130` lists
`.claude-plugin/plugin.json` as "generated copy of plugin.json, for Claude Code".
`git ls-tree -r HEAD` now records thirteen mode-120000 entries: `.claude/rules`,
eleven `.claude/skills/*` and `CLAUDE.md`. None is under `plugins/`. No prose at
the head counts them. `git grep -nE 'symlink' HEAD -- README.md` prints nothing.

**Passage 2 stands, reworded but with the same defect.** At filing, `.gitattributes:4-5`:

> \# catalogue index. The one program in it is `tools/check-conformance.py`,
> \# which validates those packages; it ships with no package.

At the head, `.gitattributes:3-6`:

> \# The repository holds text: plugin packages, their skills, and the
> \# catalogue index. Its programs sit under `tools/`: `check-conformance.py`
> \# validates those packages, and `regenerate.sh` writes every generated
> \# copy. Neither ships with a package.

"Its programs" means the repository's programs, and the sentence places all of
them under `tools/`. The tree holds a third program outside `tools/`, and it
ships with a package:

```
$ git grep -lE '^#!' HEAD -- .
HEAD:plugins/prose-discipline/hooks/print-rules.sh
HEAD:tools/check-conformance.py
HEAD:tools/regenerate.sh
```

`plugins/prose-discipline/hooks/hooks.json` runs it on every `SessionStart` and
`SubagentStart`: `"command": "sh \"${CLAUDE_PLUGIN_ROOT}/hooks/print-rules.sh\""`.
`README.md:119-121`, in the same repository, says so: "`prose-discipline` runs a
shell script from its hooks when a session or a subagent starts, in clients that
run plugin hooks."

The rule beneath the sentence reaches only `tools/`:

```
$ git check-attr -a plugins/prose-discipline/hooks/print-rules.sh
plugins/prose-discipline/hooks/print-rules.sh: text: set
plugins/prose-discipline/hooks/print-rules.sh: eol: lf
$ git check-attr -a tools/regenerate.sh
tools/regenerate.sh: text: set
tools/regenerate.sh: linguist-vendored: set
tools/regenerate.sh: eol: lf
```

This wording was false when it was written. `88d35f0` (2026-09-25 09:34,
*"chore: add tools/regenerate.sh, the one entry point for generated copies"*)
wrote "Its programs sit under `tools/`". At that commit
`plugins/prose-discipline/hooks/` already held `session-rules.sh`
(`git show 88d35f0:plugins/prose-discipline/hooks/` lists `hooks.json` and
`session-rules.sh`). `552370c` (2026-09-25 19:46) replaced it with
`print-rules.sh`. The script's name changed. That a package carries a program
outside `tools/` did not.

Line 7 depends on the sentence being corrected. "Left alone, linguist counts
those files" takes "those files" from the program sentence above it. Once that
sentence also mentions a script inside a package, the reference becomes
ambiguous.

## The rule it serves

`.agents/rules/slop.md`, under **The kinds**:

> 2. **`lying`** — text that contradicts this repository: a README sentence
>    the check does not do, a step name the step does not perform, a
>    `description` the skill does not keep, a count the tree does not have, a
>    comment for a check that was deleted.

The same file names `.gitattributes`'s kind of text in **The one test**:
"Ask it of every comment and name in the check and in `tools/regenerate.sh`."
It is judged here as prose that describes the tree, and the tree contradicts it.

The contradiction is also internal. `.gitattributes:3-6` says every program
sits under `tools/`. `README.md:119-121` says a package runs a shell script of
its own.

## Proposed change

One file changes: `.gitattributes`, the head's lines 3-9. The rules on lines 15,
18 and 20 and every other comment line stay byte-identical.

```diff
 # The repository holds text: plugin packages, their skills, and the
-# catalogue index. Its programs sit under `tools/`: `check-conformance.py`
+# catalogue index. Its own programs sit under `tools/`: `check-conformance.py`
 # validates those packages, and `regenerate.sh` writes every generated
-# copy. Neither ships with a package.
-# Left alone, linguist counts those files and labels the whole marketplace
-# "Python" — the first thing a visitor sees about a repository that
-# contains no Python for them to use.
+# copy. Neither ships with a package. A script inside a package, such as
+# a hook, ships with that package; it is not under `tools/`, and the rule
+# below does not reach it.
+# Left alone, linguist counts the files under `tools/` and labels the whole
+# marketplace "Python" — the first thing a visitor sees about a repository
+# that contains no Python for them to use.
```

Lines 1-12 afterwards read exactly:

```
# What this repository is, as GitHub's language bar reports it.
#
# The repository holds text: plugin packages, their skills, and the
# catalogue index. Its own programs sit under `tools/`: `check-conformance.py`
# validates those packages, and `regenerate.sh` writes every generated
# copy. Neither ships with a package. A script inside a package, such as
# a hook, ships with that package; it is not under `tools/`, and the rule
# below does not reach it.
# Left alone, linguist counts the files under `tools/` and labels the whole
# marketplace "Python" — the first thing a visitor sees about a repository
# that contains no Python for them to use.
#
```

Each new clause holds a fact the tree confirms. "Its own" matches
`.agents/rules/conformance.md`: "This repository runs two programs of its own."
"A script inside a package … ships with that package" is what
`plugins/prose-discipline/hooks/print-rules.sh` is. "The rule below does not
reach it" is what `git check-attr` prints above. "The files under `tools/`"
names what line 15 marks.

The new text makes no claim about GitHub's linguist. It does not say whether
linguist counts the package script, or as which language. Nothing in this item
measured that.

Alternatives rejected:

- **Name `print-rules.sh` in the comment**, as the filing's replacement named
  `session-rules.sh`. Rejected: `552370c` already renamed that script once, and
  the filed text would have been stale within the day. The general clause stays
  true through a rename and through a second package that adds a hook.
- **Mark package scripts `linguist-vendored` too.** Rejected as out of scope.
  #27's own **Not addressed** calls it "the owner's call, not a correction",
  and the court repeated that: "Widening `tools/** linguist-vendored` is a
  maintainer's call, not a correction."
- **Delete the program sentence.** Rejected: it is the reason line 15 exists.
  Without it the rule stands unexplained, which `slop.md` also counts against.
- **Apply #27's replacement text for `README.md`.** Rejected: every passage it
  replaces is gone at the head (see **Problem**). The court warned against
  applying it as written, and it names `Akurganow/how-possible`, which `fdbb065`
  removed from this public file.

## Acceptance criteria

1. `.gitattributes` contains the string `Its own programs sit under`.
2. `.gitattributes` contains the line `# below does not reach it.`
3. `.gitattributes` no longer contains the string `Its programs sit under`.
4. `.gitattributes` no longer contains the string `linguist counts those files`.
5. `.gitattributes` lines 1-12 are byte-identical to the second fenced block of
   **Proposed change**.
6. `git diff origin/main -- .gitattributes` changes none of the head's lines
   10 to 20, which become lines 12 to 22. In particular the three rule lines,
   `tools/** linguist-vendored`, `*.sh text eol=lf` and `*.md text eol=lf`, are
   unchanged.
7. `git diff --name-only origin/main...HEAD` lists `.gitattributes` and no
   other path outside `.agents/specs/27-one-plugin-repository-description/`.
   The final slice deletes that directory, so the final diff is `.gitattributes`
   alone.
8. `tools/check-conformance.py` exits 0.
9. `tools/regenerate.sh` leaves nothing to commit.

## Out of scope

- **`README.md`.** None of #27's passages survives in it (see **Problem**).
  Nothing in it is edited under this item.
- **The rule `tools/** linguist-vendored`**, and whether a package script should
  be marked. That is the owner's decision, per #27 and the court.
- **`.gitattributes:17`**, "bash fails on a script checked out with CRLF line
  endings". `hooks.json` runs `print-rules.sh` with `sh`, not bash, so the
  comment may be narrower than the rule under it. It is a different sentence
  about a different rule, and no source reports it.
- **`docs/design.md`**, the successor of the removed symlink discussion. No
  source reports a defect in it.
- **`plugins/*/plugin.json` `version`, `plugins/*/CHANGELOG.md`,
  `plugins/howp/binaries.json` and `plugins/*/skills/*/references/commands.md`.**
  #27's passage 4 was about who writes these. They are forbidden paths and stay
  untouched. The passage itself is gone.
- **`.agents/**`**, including `.agents/rules/conformance.md`'s "This repository
  runs two programs of its own". That sentence is consistent with the new
  wording, and `.agents/**` is a forbidden path.

## Risks

- **The new clause over-reaches.** "A script inside a package … ships with
  that package" is a general statement. The tell is a package file that sits
  inside a package and is excluded from what that package ships. No such
  mechanism exists at the head: `git grep -n 'export-ignore' HEAD` prints
  nothing, and no package manifest names an exclusion. If one is ever added,
  this sentence is the one to revisit.
- **A claim about linguist creeps in during implementation.** The replacement
  deliberately says nothing about how linguist classifies the package script.
  The tell is a sentence that says what linguist does with a file outside
  `tools/`. Nothing here measured it, so no such sentence may be written.
- **Unrelated lines get rewrapped.** Acceptance criteria 5 and 6 catch this.
