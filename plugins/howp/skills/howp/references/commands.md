# Every howp command

The complete command surface of the six released binaries. Nothing outside
this file exists — if a command you want is not here, it is not there.

Paths below are relative to the workspace directory given by `--repo`.
`--repo` defaults to the `HP_ROOT` environment variable, and to the current
directory when that is unset; `HP_DATA_DIR` moves the `data/` tree elsewhere
while leaving the configs under the workspace root. Pass `--repo` explicitly
anyway.

Every binary also answers `--help` and `--version`. `--help` is Russian.

---

## `hp-collect` — record what the markets say

```
hp-collect collect  [--repo PATH]
hp-collect backfill [--repo PATH]
```

**`collect`** quotes one market per active question — its best match — and
appends the result to `data/snapshots/<YYYY-MM-DD>.<source>.jsonl`, one line
per outcome, so a binary question contributes one row and a multi-outcome
market contributes one per outcome. "Best match" is the same choice the
dashboard shows: per question the record with the strongest verdict, `match`
before `partial`, and a `mismatch` never. Only questions with
`status: active` are quoted.

**`backfill`** pulls whole price histories into
`data/snapshots/backfill.<source>.jsonl`, one file per source. A pass where
every market answered rewrites that file whole; a pass where some failed
merges into it instead, so a bad day cannot erase history already gathered.
Safe to re-run either way, and worth running once on a new workspace so the
dashboard has a history on day one. The move detector ignores these
files on purpose: backfill and live quotes come from different endpoints,
and the seam between them is not a market movement.

Exit 0 means the run finished. A market that refused to quote is reported
and skipped, one line per market, and does not fail the run — "no snapshots"
is an answer, not an error. Non-zero means the workspace could not be read
or a file could not be written.

## `hp-moves` — find sharp movements

```
hp-moves detect [--repo PATH] [--now ISO]
hp-moves report [--repo PATH] [--now ISO]
```

**`detect`** finds the moves and appends them to `data/moves/`.
**`report`** prints what the detector sees and writes nothing — the one to
run when a user asks "why did it flag that?".

`--now ISO` sets the cutoff moment (ISO-8601 with an offset). Without it the
cutoff is the latest snapshot, never the wall clock, so two runs over the
same workspace answer the same.

It reads **live snapshots only**, on a six-hour grid with a tolerance either
side; it needs at least two collect runs about six hours apart before it can
say anything. Finding nothing is the normal state of a market feed. Exit 0
either way; non-zero only if the workspace could not be read or the log
could not be written.

## `hp-render` — the dashboard

```
hp-render render [--repo PATH] [--note TEXT] [--out PATH]
hp-render wiki   [--repo PATH] [--out PATH]
```

**`render`** writes the interactive HTML dashboard, by default to
`data/dashboard/index.html`, and prints the path it wrote. `--note` puts a
banner line in the page header.

The page is grouped by interest, and per question shows the probability that
answers the question **as asked** — an inverse market appears as 1−P — with
its 24-hour and 7-day change, a history chart and the source. Several venues
on one binary question are folded into one number with each venue's
contribution visible beside it. A partial match's divergence is shown above
the fold, not hidden under it. There is no money on the page: liquidity,
volume and spread are kept as a reliability signal and come out in words
rather than sums. Frozen, closed and expired outcomes are marked and stay
out of the headline. Questions with no market do not disappear — they land
in a coverage block at the end. The one piece of written text is the weekly
digest, which `hp-explain` produces; `render` only displays the file that is
already there.

**`wiki`** writes `Home.md` plus `charts/*.svg` into a directory (default
`wiki-out`), for a user who keeps their dashboard in a wiki clone.

Neither costs anything and neither needs a model. A rendered page is
all-or-nothing: exit 0 means the page was written, non-zero means nothing
was, because half a dashboard is worse than yesterday's whole one.

## `hp-verify` — does this market actually answer this question?

```
hp-verify plan   [--repo PATH] --work-dir PATH [--refresh] [--chunks N]
hp-verify apply  [--repo PATH] --work-dir PATH
hp-verify status --work-dir PATH
```

The `plan`/`apply` split with you in between — see `model-steps.md`.

**`plan`** searches the sources for candidate markets, applies the checks it
can make without judgement, writes those verdicts straight into
`matches/*.yaml`, and leaves prompt files plus `manifest.json` in the work
directory. It calls no model and spawns no process.

**`apply`** reads the answer files, validates them against the manifest, and
writes the accepted verdicts into `matches/<interest>.yaml`. An item the
answers failed is recorded in `outcome.json`, **not** in the exit code, so
what did validate can be saved first.

**`status`** exits non-zero when the run left items unverified.

`--refresh` re-verifies records whose resolution criteria changed and keeps
looking for better markets for questions that only matched partially — the
periodic mode. `--chunks N` writes prompts for at most N chunks; it is a
smoke limiter, and what it leaves out is picked up by the next run.

## `hp-scout` — which news explains a move

```
hp-scout index      [--repo PATH] [--now ISO]
hp-scout eligible   [--repo PATH] [--now ISO]
hp-scout candidates [--repo PATH] [--now ISO] --move-id MOVE_ID [--json]
hp-scout plan       [--repo PATH] [--now ISO] --work-dir PATH [--moves N]
hp-scout apply      [--repo PATH] [--now ISO] --work-dir PATH
hp-scout status     --work-dir PATH
```

**`index`** polls the curated feeds and updates `data/news/`. Free and
read-only towards the world; worth running alongside `collect`.

**`eligible`** prints, one id per line on stdout, the moves a run would take:
confirmed by a later snapshot, not mechanical, not already decided, and
inside the age window. The reasons for what it dropped go to stderr, so the
stdout list stays machine-readable.

**`candidates --move-id ID`** runs both search legs for one move and prints
to stdout the exact prompt text `plan` would have written for it — so a
person can work one move by hand without planning a cycle. `--json` prints
the candidate list with its URLs instead. The run report goes to stderr.

**`plan` / `apply` / `status`** are the cycle; see `model-steps.md`.
`--moves N` takes at most N moves, leaving the rest for the next run.

`apply` writes the journal under `data/news_scout/`. Note that the dashboard
does not display it in this release: it is a data product, so report it to
the user yourself.

## `hp-explain` — the weekly digest

```
hp-explain plan   [--repo PATH] --work-dir PATH [--force]
hp-explain apply  [--repo PATH] --work-dir PATH
hp-explain status --work-dir PATH
```

**`plan`** builds the digest's facts from the current page and writes a
prompt **only when a digest is actually due** — when the numbers have moved
away from the stored digest's snapshot, or the stored one is about a week
old. Otherwise it writes no prompt, and that is a successful run.
`--force` asks for a rewrite anyway.

**`apply`** reads the answer and either writes `data/summaries.yaml` or
writes one rewrite prompt. **`status`** exits non-zero when there is no
digest at the end; a digest that is deliberately empty is a real answer and
stays green.

`hp-render render` picks up `data/summaries.yaml` on its next run, so
re-render after a digest lands.
