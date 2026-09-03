# Getting the binary, and proving it is the right bytes

`SKILL.md` states the four rules this file carries out. This is how, with the
commands. Everything in `<angle brackets>` is a placeholder for a value read
out of `binaries.json`; a command run with the brackets still in it does
nothing useful.

## Step 0 — the platform gate

Read `../../../binaries.json` — the manifest at the plugin root, two
directories above `SKILL.md`. It is the authority on what has been published.
Never hardcode its values, and read it again on every run rather than
remembering it from the last one.

`.schema` must be `howp-binaries-1`. That string is the file's shape marker:
anything else means the shape has changed and the fields below may have
moved, so stop and tell the user this skill is older than the package it is
reading.

**If the file is not there at all**, the skill was installed on its own,
without the plugin package around it — some clients load skills but not
plugins. Say so, and offer the choice rather than deciding for the user:
install the whole package, or let you fetch
<https://raw.githubusercontent.com/Akurganow/ai-plugins/main/plugins/howp/binaries.json>.
Note when offering it that the fetched copy is the weaker guarantee: the
package's copy was fixed at the revision the user installed, while whatever
`main` serves today can change under them.

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

`SKILL.md` carries the host table. Check it before spending a download on it,
and check again the first time a run needs a market rather than assuming this
step settled the whole day. Probe with the tool you will actually fetch with,
not with a different one; a `HEAD` or a small `GET` is enough, and the
download in Step 3 is its own probe of `github.com`.

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
- **Any other client.** This skill names no mechanism, because none was
  verified for one when this was written. Tell the user which host answered
  what, and let them use whatever their setup provides.
- **Neither, sometimes.** A corporate proxy, a container's egress policy or a
  firewall is not something a client setting reaches. If a host is blocked
  below the client, say so plainly instead of sending the user to edit a
  settings file that will not help.

The package declares its hosts in two machine-readable places — the
`extensions` object of `plugin.json`, and `SKILL.md`'s own frontmatter
`metadata`. **Neither is a grant.** No client is documented to read either
field as network permission, and nothing in Agent Plugins 1.0.0 or the Agent
Skills specification gives a plugin a way to request it; the manifest schema
says of `extensions` only that it is "Client-specific manifest data keyed by
reverse-domain extension namespace" and that "Agent Plugins assigns no
semantics to namespace object contents"
(`tools/schemas/agent-plugins/1.0.0/plugin.schema.json`, the vendored copy of
the published schema). The declaration is there to be quoted at a user who
asks what to allow. This step is what actually finds out.

## Step 2 — is a verified copy already here?

```sh
HOWP_CACHE="${HOWP_CACHE:-$HOME/.cache/howp}"
DEST="$HOWP_CACHE/<version>"          # .version from binaries.json
BIN="$DEST/<root>/<bin_dir>"          # target.root / target.bin_dir
```

Skip Steps 3 to 5 when **both** of these hold: `$DEST/verified.sha256` exists
and its contents equal `target.sha256`, and every name in `target.binaries`
exists under `$BIN` and is executable.

```sh
[ "$(cat "$DEST/verified.sha256" 2>/dev/null)" = "<sha256>" ] && echo cached
```

Anything else — no stamp, a different digest, a missing binary — means
download again. The stamp is what makes a new release replace an old copy
instead of being ignored: a new version lands in a new `$DEST`, and a
re-released digest fails the comparison.

A cache under `$HOME` is not promised to survive. A cloud session, a fresh
container or a machine that clears `~/.cache` starts with nothing here, and
downloading again is then the normal outcome and not a fault to investigate —
it costs one archive. Say that rather than hunting for what deleted it.

## Step 3 — download

```sh
mkdir -p "$DEST"
curl --fail --location --proto '=https' --tlsv1.2 \
  --output "$DEST/<archive>" "<url>"
```

`--fail` matters: without it curl writes GitHub's error page into the file and
exits 0, and you would go on to checksum an HTML page.

## Step 4 — verify. This is the step that must not be skipped

You are about to run a binary from the internet on someone else's machine.
The digest in `binaries.json` is what stands between that and a stranger's
code, and unlike a release asset — which can be replaced after the fact — the
copy in the package was fixed when the user installed this plugin.

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

## Step 5 — unpack

```sh
tar -xzf "$DEST/<archive>" -C "$DEST"
rm -f "$DEST/<archive>"
printf '%s\n' "<sha256>" > "$DEST/verified.sha256"
```

Then confirm the archive held what it promised: every name in
`target.binaries` is present under `$BIN`, and `"$BIN/hp" --version` runs.
Write the stamp only after the checksum passed — it is a record that these
bytes were verified, and a stamp written on unverified bytes is worse than no
stamp.

**Every archive holds the binaries and a licence, and nothing else.** There is
no helper script in one, for the fetch cycle or anything else, and
`binaries.json` promises none: its `binaries` array is the list of names that
must be under `bin/`, and there is no field for anything more. Whatever a
script would have done, you do.

**On macOS only:** if the system refuses to open a binary ("cannot be opened
because the developer cannot be verified"), that is Gatekeeper's quarantine
attribute, applied by whatever fetched the file. It is cleared with `xattr -d
com.apple.quarantine <file>`; that command has not been run or verified by
anyone who wrote this file, and it is only reasonable **after** Step 4 passed.
Report it to the user rather than doing it silently. Nothing in this paragraph
applies to Linux, which has no such attribute — a binary that will not start
there is usually the wrong C library, and Step 0's two-matching-entries rule
is what guards against that.
