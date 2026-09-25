<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [Getting the binary, and proving it is the right bytes](#getting-the-binary-and-proving-it-is-the-right-bytes)
  - [Step 0 — the platform gate](#step-0--the-platform-gate)
  - [Step 1 — the preflight: what has to be reachable, and by whom](#step-1--the-preflight-what-has-to-be-reachable-and-by-whom)
  - [Step 2 — is a checked copy already here?](#step-2--is-a-checked-copy-already-here)
  - [Step 3 — download](#step-3--download)
  - [Step 4 — verify. This is the step that must not be skipped](#step-4--verify-this-is-the-step-that-must-not-be-skipped)
  - [Step 5 — unpack, into a staging directory](#step-5--unpack-into-a-staging-directory)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# Getting the binary, and proving it is the right bytes

`SKILL.md` states the five rules this file carries out. This is how, with the
commands. Everything in `<angle brackets>` is a placeholder for a value read
out of `binaries.json`; a command run with the brackets still in it does
nothing useful.

## Step 0 — the platform gate

Read `../../binaries.json` — the manifest at the plugin root, two
directories above `SKILL.md`. It is the authority on what has been published.
Never hardcode its values, and read it again on every run rather than
remembering it from the last one: each release rewrites it.

`.schema` must be `howp-binaries-1`. That string is the file's shape marker:
anything else means the shape has changed and the fields below may have
moved, so stop and tell the user this skill is older than the package it is
reading.

**If the file is not there at all**, the skill arrived without its
package. Say so, and offer the choice rather than deciding for the user.
Either they install the whole package, or you fetch
<https://raw.githubusercontent.com/Akurganow/ai-plugins/main/plugins/howp/binaries.json>
and, for the host list,
<https://raw.githubusercontent.com/Akurganow/ai-plugins/main/plugins/howp/plugin.json>.
When you offer it, say that the fetched copies are the weaker guarantee.
The package's copy is the revision the user's client fetched, while
whatever `main` serves today can change under them.

```sh
uname -s    # the OS name to match
uname -m    # the architecture to match
```

Find the entry in `targets[]` whose `os` equals `uname -s` and whose `arch`
equals `uname -m`. From it, take:

| From `binaries.json` | Used as |
| --- | --- |
| `.version` | the cache directory's name |
| `target.archive` | the file name to download |
| `target.url` | the address to download it from |
| `target.sha256` | the digest the download must have |
| `target.root` | the directory the archive unpacks into |
| `target.bin_dir` | the directory inside it holding the binaries |
| `target.binaries` | the names that must be there afterwards |

**If there is no such entry, stop.** Say this much: howp publishes binaries
only for the targets `binaries.json` lists, this machine is `<uname -s>`/`<uname
-m>`, and none of the entries matches — so there is nothing to run here. Name
the targets the file does list, read out of the file rather than from memory.
Do not download an archive for another platform, do not offer to build from
source — the source repository is private — and do not carry on. That is the
whole answer, and it is not a failure of the skill.

**If two entries match, stop as well and report it.** `uname -s`/`uname -m`
cannot tell two builds of the same OS and architecture apart — a glibc and a
musl build of Linux/`x86_64` answer identically — so at most one entry can be
meant for a given machine. Two matching means the manifest is asking you to
guess, and guessing which C library a binary wants is how a user gets an
executable that will not start.

**`target.binaries` is the authority on what an archive holds.** It is what
Step 5 checks against, and it is also what says whether this skill can drive
the release at all: these procedures are written for one binary, `hp`, and an
archive whose `binaries` array does not name it is a release older than this
skill. Say so and stop rather than running something else out of it.

## Step 1 — the preflight: what has to be reachable, and by whom

`../../plugin.json` lists the hosts, under
`extensions["io.github.akurganow.ai-plugins"].network.hosts`. Probe each one
before spending a download on it. On every run, probe again the first time
the run needs a market. Reachability changes with the machine, its proxy and
the day. Probe with the tool you will actually fetch with, not with a
different one. A `HEAD` or a small `GET` is enough. Any answer from the
host proves the connection, so a root 404 or 301 is reachable; only a
failed connection or proxy refusal is blocked. The download in Step 3
is its own probe of `github.com` and of the host it redirects to.

**If something is blocked, do not work around it — say precisely what to
allow, and where.** Which mechanism that is depends on the client, so name
the one in front of you rather than a generic one:

- **Claude Code.** Two settings, and which one you need depends on what does
  the fetching. Its own fetch tool is allowed per domain with a permission
  rule: `WebFetch(domain:example.com)` "Matches fetch requests to
  example.com", saved to `.claude/settings.local.json` for one repository or
  `~/.claude/settings.json` for every project — from Claude Code's own
  documentation, <https://code.claude.com/docs/en/permissions>. A shell
  command like `curl` runs under the Bash sandbox instead, whose network
  layer is an allowlist, shaped like that documentation's own example
  (`"sandbox": {"network": {"allowedDomains": ["github.com",
  "*.npmjs.org"]}}`), and "Claude Code pre-allows no domains by default" — its
  sandboxing documentation, <https://code.claude.com/docs/en/sandboxing>,
  which also records that a `WebFetch(domain:…)` allow rule adds its domain
  to that same list.
- **Any other client.** This skill names no mechanism for it, because a
  setting named without that client's documentation beside it would be a
  guess. Tell the user which host answered what, and let them use whatever
  their setup provides.
- **Neither, sometimes.** A corporate proxy, a container's egress policy or a
  firewall is not something a client setting reaches. If a host is blocked
  below the client, say so plainly instead of sending the user to edit a
  settings file that will not help.

The package declares its hosts in one machine-readable place, the
`extensions` object of `plugin.json`. **It is not a grant.** No client is
documented to read that field as network permission. Nothing in Agent
Plugins 1.0.0 or the Agent Skills specification gives a plugin a way to
request it. The manifest schema describes `extensions` in two sentences and
nothing more (`tools/schemas/agent-plugins/1.0.0/plugin.schema.json`, the
vendored copy of the published schema). It is "Client-specific manifest
data keyed by reverse-domain extension namespace", and "Agent Plugins
assigns no semantics to namespace object contents". The declaration is
there to be quoted at a user who asks what to allow. This step is what
actually finds out.

## Step 2 — is a checked copy already here?

```sh
HOWP_CACHE="${HOWP_CACHE:-$HOME/.cache/howp}"
DEST="$HOWP_CACHE/<version>"          # .version from binaries.json
BIN="$DEST/<root>/<bin_dir>"          # target.root / target.bin_dir
```

Skip Steps 3 to 5 when **both** of these hold: `$DEST/verified.sha256` exists
and its contents equal `target.sha256`, **and** every name in
`target.binaries` exists under `$BIN` and is executable. Check both — a stamp
beside a tree that is missing a binary is exactly the state a half-finished
install leaves behind, and a shortcut that reads only the stamp would skip the
install that never finished.

```sh
# `<binary> …` is target.binaries, expanded from binaries.json.
cached=false
if [ "$(cat "$DEST/verified.sha256" 2>/dev/null)" = "<sha256>" ]; then
  cached=true
  for name in <binary> …; do
    [ -x "$BIN/$name" ] || { cached=false; break; }
  done
fi
if $cached; then echo cached; else echo install; fi
```

Anything else — no stamp, a different digest, a missing or non-executable
binary — means download again. The stamp is what makes a new release replace
an old copy instead of being ignored: a new version lands in a new `$DEST`,
and a re-released digest fails the comparison.

A cache under `$HOME` is not promised to survive. A cloud session, a fresh
container or a machine that clears `~/.cache` starts with nothing here, and
downloading again is then the normal outcome and not a fault to investigate —
it costs one archive. Say that rather than hunting for what deleted it.

## Step 3 — download

```sh
mkdir -p "$DEST"
curl --fail --location --proto '=https' --tlsv1.2 --connect-timeout 15 \
  --output "$DEST/<archive>" "<url>"
```

`--connect-timeout` and no `--max-time`: a host that never answers should fail
in seconds rather than hang a run, while the transfer itself is tens of
megabytes and may legitimately take minutes on a slow link.

`--fail` matters: without it curl writes GitHub's error page into the file and
exits 0, and you would go on to checksum an HTML page.

`--location` matters too: `github.com` answers `<url>` with a redirect to
`release-assets.githubusercontent.com`, so an allowlist needs both hosts.
Running `curl -sI` on the `howp-v0.3.6` archive URL on 2026-09-25 returned
`HTTP/2 302` and `location: https://release-assets.githubusercontent.com/…`
(measured by running the command). GitHub's runner documentation lists that
host as needed for downloading release assets, but does not describe the
redirect
([self-hosted runners reference](https://docs.github.com/en/actions/reference/runners/self-hosted-runners#accessible-domains-by-function),
documentation).

## Step 4 — verify. This is the step that must not be skipped

You are about to run a binary from the internet on someone else's machine.
The digest in `binaries.json` is what stands between that and a stranger's
code, and unlike a release asset — which can be replaced after the fact — the
copy in the package was fixed when the user's client fetched this package.

```sh
# macOS, and any Linux that has it:
( cd "$DEST" && printf '%s  %s\n' "<sha256>" "<archive>" | shasum -a 256 -c - )

# Linux without `shasum` — a minimal container usually has only this one:
( cd "$DEST" && printf '%s  %s\n' "<sha256>" "<archive>" | sha256sum -c - )
```

Two spaces between the digest and the name; that is the format both readers
expect. Each prints `<archive>: OK` and exits 0, or `<archive>: FAILED` and
exits non-zero. Use whichever exists — check for one before running it, and
if neither is there, stop: an unverified archive is not unpacked, and there
is no third option in this file.

**On any non-zero exit**, `rm -f "$DEST/<archive>"` and stop. Do not retry
silently, do not unpack "just to look", do not proceed. Tell the user
plainly: the archive downloaded from `<url>` did not have the digest
`binaries.json` records, the file has been deleted, and nothing was run. A
mismatch is either a corrupted transfer or a tampered asset, and neither is
something to work around.

The release also publishes a `SHA256SUMS` asset beside the archive. It is a
convenience for a person checking by hand; the digest this skill checks
against is the one inside the package.

## Step 5 — unpack, into a staging directory

**Never extract over the destination.** A `tar` that dies half way — a full
disk, a killed shell — would leave a partial tree where the next run expects a
complete one, and if the stamp were already there that run would happily use
it. So the archive is opened somewhere else, checked there, and moved into
place only once it is known good; the stamp is written last of all, so a stamp
is only ever beside a tree that was extracted whole and shown to run.

```sh
STAGE=$(mktemp -d "${TMPDIR:-/tmp}/howp-unpack.XXXXXX")
trap 'rm -rf "$STAGE"' EXIT
tar -xzf "$DEST/<archive>" -C "$STAGE"

# Validate in the staging tree, before anything in $DEST is touched.
# `<binary> …` is target.binaries again.
ok=true
for name in <binary> …; do
  [ -x "$STAGE/<root>/<bin_dir>/$name" ] &&
    continue || { echo "the archive does not hold $name" >&2; ok=false; }
done
"$STAGE/<root>/<bin_dir>/hp" --version >/dev/null 2>&1 ||
  { echo "hp will not run on this machine" >&2; ok=false; }

# Replace the destination only if every check passed — stale contents and all.
if $ok; then
  rm -rf "$DEST/<root>"
  mkdir -p "$DEST"
  mv "$STAGE/<root>" "$DEST/<root>"
  rm -f "$DEST/<archive>"
  # Last of all, so the stamp can never describe a tree that is not there.
  printf '%s\n' "<sha256>" > "$DEST/verified.sha256"
else
  echo "nothing was put in place; $DEST is untouched" >&2
fi
```

The `rm -rf "$DEST/<root>"` is what makes a re-released digest recover rather
than half-overwrite: whatever an earlier attempt left is gone before the new
tree lands. The stamp is a record that these bytes passed Step 4 *and*
unpacked whole, and one written any earlier is worse than no stamp — Step 2's
shortcut believes it.

A helper script has no field in `binaries.json`, and `SKILL.md` rule 5
says what to do instead.

**On macOS only:** Gatekeeper may refuse to open `hp` because it cannot
check the developer. Offer a way past it only **after** Step 4 passed,
because the digest is what shows the file is the released one. Apple
documents **Open Anyway** under System Settings → Privacy & Security
([Safely open apps on your Mac](https://support.apple.com/en-us/102445),
Apple's documentation). The command-line route is
`xattr -d com.apple.quarantine <file>`, though the Apple documentation
cited here does not tie that attribute to Gatekeeper. Apple names
`com.apple.quarantine` as the quarantine extended file attribute
([App Store Connect notice](https://developer.apple.com/news/upcoming-requirements/?id=02182025a),
Apple's developer documentation). `xattr -d` removes the named attribute
(`man xattr`, the manual page macOS ships; documentation). Either route lifts
a protection the user's system applied, so report it and let the user
choose. Nothing in this paragraph applies to Linux, which has no such
attribute — a binary that will not start there is usually the wrong C
library, and Step 0's two-matching-entries rule is what guards against that.

**If a step here fails, that is new information**, and worth reporting to
<https://github.com/Akurganow/ai-plugins> rather than working around. Say which
platform you were on and which release `binaries.json` named — both change what
the answer means.
