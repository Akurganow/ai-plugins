# Every `hp` command, verbatim

Written by the release job from the binary's own `--help`, top level and every
subcommand recursively, at `hp 0.3.3` (`howp-v0.3.3`) on 2026-09-03.
Nothing here is paraphrased and nothing is added. Where this file and the binary
in front of you disagree, **the binary is right**. This file is never edited by
hand: the next release rewrites it from the binary it publishes.

## `hp --help`

```
One command over a how-possible workspace: ingest what somebody else fetched, name what to fetch next, and compute, render and score what the store holds

Usage: hp <COMMAND>

Commands:
  ingest   Write a source's raw response into the record
  sources  Name the requests a fetch needs
  matches  Read the verdict cache
  stats    Everything the dashboard computes about a question, as JSON
  render   The dashboard, as one Markdown page
  digest   The weekly digest, read rather than written
  moves    Sharp probability moves over the live snapshot history
  bench    The benchmark's deterministic half: arithmetic, a substring check, two reports, and the requests a case's own sources imply
  help     Print this message or the help of the given subcommand(s)

Options:
  -h, --help     Print help
  -V, --version  Print version
```

## `hp ingest --help`

```
Write a source's raw response into the record

Usage: hp ingest <COMMAND>

Commands:
  snapshot     Append one live quote per outcome to the day's snapshot file
  history      Merge one market's whole price history into the source's backfill file
  match        Record one verdict on a market, reading the market's own facts from its body
  digest       Store the weekly digest: one paragraph, and the numbers it was written against
  explanation  Record one story as the explanation of one sharp move
  check        Read the curated files strictly and report what is wrong with them
  help         Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp ingest snapshot --help`

```
Append one live quote per outcome to the day's snapshot file

Usage: hp ingest snapshot [OPTIONS] --source <SOURCE> --question <ID> --ts <ISO> --from <FILE>

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --source <SOURCE>
          The source the response came from

          Possible values:
          - polymarket: Polymarket: Gamma for markets and events, CLOB for price history
          - manifold:   Manifold Markets, through the public v0 API

      --question <ID>
          The question the response is being recorded against

      --ref <REF>
          A record of that question by its own key, e.g. event:some-slug

      --ts <ISO>
          The moment every row of this run is stamped with: ISO-8601 with an offset. Required, and one value for the whole run

      --from <FILE>
          The raw response body, or - for standard input

  -h, --help
          Print help (see a summary with '-h')
```

### `hp ingest history --help`

```
Merge one market's whole price history into the source's backfill file

Usage: hp ingest history [OPTIONS] --source <SOURCE> --question <ID> --from <DIR>

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --source <SOURCE>
          The source the response came from

          Possible values:
          - polymarket: Polymarket: Gamma for markets and events, CLOB for price history
          - manifold:   Manifold Markets, through the public v0 API

      --question <ID>
          The question the response is being recorded against

      --ref <REF>
          A record of that question by its own key, e.g. event:some-slug

      --from <DIR>
          The directory the responses were fetched into

  -h, --help
          Print help (see a summary with '-h')
```

### `hp ingest match --help`

```
Record one verdict on a market, reading the market's own facts from its body

Usage: hp ingest match [OPTIONS] --source <SOURCE> --question <ID> --ref <REF> --from <BODY> --verdict <match|partial|mismatch> --direction <direct|inverse> --confidence <high|medium|low> --notes <TEXT> --checked-at <YYYY-MM-DD>

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --source <SOURCE>
          The source the market is at

          Possible values:
          - polymarket: Polymarket: Gamma for markets and events, CLOB for price history
          - manifold:   Manifold Markets, through the public v0 API

      --question <ID>
          The question the verdict is about

      --ref <REF>
          The market's own key, e.g. event:some-slug or market:kar1

      --from <BODY>
          The raw lookup body for that market, or - for standard input. Every field the venue publishes — the wording, the link, the deadline and the resolution criteria — is read out of this, never typed

      --verdict <match|partial|mismatch>
          Does the market answer the question

      --direction <direct|inverse>
          Whether the market's YES is the question's yes

      --confidence <high|medium|low>
          How sure the verdict is

      --notes <TEXT>
          The reasoning. Refused rather than repaired if it carries a control or invisible code point, or runs past the stored cap

      --checked-at <YYYY-MM-DD>
          The day the judgement was made. Required and never defaulted, for the reason `--ts` is: this binary has no clock, and a date it invented would be a claim about when a market was read

  -h, --help
          Print help (see a summary with '-h')
```

### `hp ingest digest --help`

```
Store the weekly digest: one paragraph, and the numbers it was written against

Usage: hp ingest digest [OPTIONS] --from <FILE> --generated-at <ISO>

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --from <FILE>
          The paragraph, or - for standard input. It is refused rather than repaired if it carries a link, markup or a line break, or if it normalizes to nothing

      --generated-at <ISO>
          The moment the digest is stamped with, and the moment the card facts it is stored beside are computed at.
          
          **Required, and never defaulted**, for the reason `--ts` is: this binary reads no clock, and a moment it invented would be a claim about when the paragraph was written.

  -h, --help
          Print help (see a summary with '-h')
```

### `hp ingest explanation --help`

```
Record one story as the explanation of one sharp move

Usage: hp ingest explanation [OPTIONS] --move <MOVE_ID> --url <URL> --title <TEXT> --published <ISO> --why <TEXT>

Options:
      --repo <PATH>      Workspace root (from HP_ROOT, then the current directory, by default)
      --move <MOVE_ID>   The move being explained, by its `move_id` in `data/moves/**`
      --url <URL>        The story's link. https, and no credentials in it
      --title <TEXT>     Its headline. Refused rather than repaired if it carries a control or invisible code point, or runs past the stored cap
      --published <ISO>  When it was published: ISO-8601 with an offset. The record's label — before, inside or after the move's window — is computed from this and is never supplied
      --why <TEXT>       Why it is offered as the explanation. Screened like the headline
  -h, --help             Print help
```

### `hp ingest check --help`

```
Read the curated files strictly and report what is wrong with them

Usage: hp ingest check [OPTIONS] <SUBJECT>

Arguments:
  <SUBJECT>
          Which of the three sets of curated files to read

          Possible values:
          - interests: `interests.yaml`
          - questions: `questions/*.yaml`, and the interests naming them
          - matches:   `matches/*.yaml`, the questions they point at, and the interests naming both

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

  -h, --help
          Print help (see a summary with '-h')
```

## `hp sources --help`

```
Name the requests a fetch needs

Usage: hp sources <COMMAND>

Commands:
  urls  The first request every active best match needs
  next  The requests one already-fetched body implies
  help  Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp sources urls --help`

```
The first request every active best match needs

Usage: hp sources urls [OPTIONS] --json

Options:
      --repo <PATH>    Workspace root (from HP_ROOT, then the current directory, by default)
      --question <ID>  Only this question
      --json           Print JSON. Required rather than defaulted, so the format a caller parses is on the command line rather than implied by it
  -h, --help           Print help
```

### `hp sources next --help`

```
The requests one already-fetched body implies

Usage: hp sources next [OPTIONS] --source <SOURCE> --question <ID> --url <URL> --from <FILE> --json

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --source <SOURCE>
          The source the response came from

          Possible values:
          - polymarket: Polymarket: Gamma for markets and events, CLOB for price history
          - manifold:   Manifold Markets, through the public v0 API

      --question <ID>
          The question the response is being recorded against

      --ref <REF>
          A record of that question by its own key, e.g. event:some-slug

      --url <URL>
          The URL the body was fetched from

      --from <FILE>
          The body that URL answered with

      --status <N>
          The HTTP status it answered with, when it is known

      --history
          Walk a history rather than a live quote

      --page <N>
          Which Manifold `bets` page this body is, counting from one. The page after the eighth is never named, which is the client's own bound: a loop that did not carry it would page an active market for ever.
          
          **It has no default**, for the reason `--ts` has none: a defaulted ordinal is a silent claim about where in a walk the caller is, and a loop that forgot to count would page the first market for ever while every run looked healthy. So it is required with `--history` and refused without it, where there is no walk to be at a page of.

      --json
          Print JSON. Required for the reason `hp sources urls` gives

  -h, --help
          Print help (see a summary with '-h')
```

## `hp matches --help`

```
Read the verdict cache

Usage: hp matches <COMMAND>

Commands:
  stale  Stored verdicts whose market's resolution criteria have moved
  help   Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp matches stale --help`

```
Stored verdicts whose market's resolution criteria have moved

Usage: hp matches stale [OPTIONS] --cache <DIR> --json

Options:
      --repo <PATH>  Workspace root (from HP_ROOT, then the current directory, by default)
      --cache <DIR>  The directory the market bodies were fetched into
      --json         Print JSON. Required for the reason `hp sources urls` gives
  -h, --help         Print help
```

## `hp stats --help`

```
Everything the dashboard computes about a question, as JSON

Usage: hp stats [OPTIONS] --as-of <ISO> --json

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --as-of <ISO>
          The moment the deltas and the lifecycle badges are computed against.
          
          **Required, and never defaulted**, for the reason `--ts` is: this binary reads no clock, and a moment it invented would be a claim about when the numbers were read. A run passes the one moment it took at its start, the same one it stamps its snapshots with.

      --json
          Print JSON. Required for the reason `hp sources urls` gives

  -h, --help
          Print help (see a summary with '-h')
```

## `hp render --help`

```
The dashboard, as one Markdown page

Usage: hp render [OPTIONS] --as-of <ISO>

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --as-of <ISO>
          The moment the page is built at.
          
          **Required, and never defaulted**, for the reason `hp stats` gives — the page states when it was taken, and the charts' ninety-day window ends here.

      --out <PATH>
          Where to write the page (data/dashboard.md by default)

      --note <TEXT>
          A note in the page's header
          
          [default: ""]

  -h, --help
          Print help (see a summary with '-h')
```

## `hp digest --help`

```
The weekly digest, read rather than written

Usage: hp digest <COMMAND>

Commands:
  due   Whether the stored digest still describes the page
  help  Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp digest due --help`

```
Whether the stored digest still describes the page

Usage: hp digest due [OPTIONS] --as-of <ISO> --json

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --as-of <ISO>
          The moment the stored digest's age and drift are read against.
          
          **Required, and never defaulted**, for the reason `--as-of` is on `hp stats`: the answer is about a moment, and one this binary invented would be a claim about when the page was read.

      --json
          Print JSON. Required for the reason `hp sources urls` gives

  -h, --help
          Print help (see a summary with '-h')
```

## `hp moves --help`

```
Sharp probability moves over the live snapshot history

Usage: hp moves <COMMAND>

Commands:
  detect  Find the moves and append them to data/moves/
  report  Show what the detector sees, writing nothing
  help    Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp moves detect --help`

```
Find the moves and append them to data/moves/

Usage: hp moves detect [OPTIONS]

Options:
      --repo <PATH>  Workspace root (from HP_ROOT, then the current directory, by default)
      --now <ISO>    The cutoff moment, ISO-8601 with an offset (the last snapshot by default). It is optional here, and only here, because the detector already has a moment that is not the wall clock: the newest live snapshot
  -h, --help         Print help
```

### `hp moves report --help`

```
Show what the detector sees, writing nothing

Usage: hp moves report [OPTIONS]

Options:
      --repo <PATH>  Workspace root (from HP_ROOT, then the current directory, by default)
      --now <ISO>    The cutoff moment, ISO-8601 with an offset (the last snapshot by default). It is optional here, and only here, because the detector already has a moment that is not the wall clock: the newest live snapshot
  -h, --help         Print help
```

## `hp bench --help`

```
The benchmark's deterministic half: arithmetic, a substring check, two reports, and the requests a case's own sources imply

Usage: hp bench <COMMAND>

Commands:
  score     Turn a judge's marks into a total under a rubric
  record    Append one scored run to a case's history
  quotes    Check an article's quotations against the fixtures it cites
  verdicts  Verdict agreement with the committed match records
  brief     The brief a writing agent is given for a case
  sources   The addresses a case's evidence comes from, and what to save each as
  help      Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp bench score --help`

```
Turn a judge's marks into a total under a rubric

Usage: hp bench score --rubric <FILE> --marks <FILE> --json

Options:
      --rubric <FILE>  The rubric the marks were given under
      --marks <FILE>   The judge's marks
      --json           Print JSON. Required for the reason `hp sources urls` gives
  -h, --help           Print help
```

### `hp bench record --help`

```
Append one scored run to a case's history

Usage: hp bench record [OPTIONS] --case <ID> --page <FILE> --evidence <FILE> --marks <FILE> --at <ISO>

Options:
      --repo <PATH>
          Workspace root (from HP_ROOT, then the current directory, by default)

      --case <ID>
          The case, which is also the directory the history is written under

      --page <FILE>
          The article

      --evidence <FILE>
          The article's evidence file

      --marks <FILE>
          The judge's marks

      --at <ISO>
          The moment the run was scored at.
          
          **Required, and never defaulted**, for the reason `--ts` is: this binary reads no clock, and a moment it invented would be a claim about when a page was judged.

      --commit <SHA>
          The commit the run was made at, where the caller knows it

  -h, --help
          Print help (see a summary with '-h')
```

### `hp bench quotes --help`

```
Check an article's quotations against the fixtures it cites

Usage: hp bench quotes --page <FILE> --evidence <FILE> --fixtures <DIR> --json

Options:
      --page <FILE>      The article
      --evidence <FILE>  The article's evidence file
      --fixtures <DIR>   The directory the fixtures were collected into
      --json             Print JSON. Required for the reason `hp sources urls` gives
  -h, --help             Print help
```

### `hp bench verdicts --help`

```
Verdict agreement with the committed match records

Usage: hp bench verdicts --expected <DIR> --actual <DIR> --json

Options:
      --expected <DIR>  The labels: the committed match records, projected (`bench/verdicts/`)
      --actual <DIR>    The `matches/` of the workspace the run wrote into
      --json            Print JSON. Required for the reason `hp sources urls` gives
  -h, --help            Print help
```

### `hp bench brief --help`

```
The brief a writing agent is given for a case

Usage: hp bench brief --case <FILE>

Options:
      --case <FILE>  The case file
  -h, --help         Print help
```

### `hp bench sources --help`

```
The addresses a case's evidence comes from, and what to save each as

Usage: hp bench sources --case <FILE> --json

Options:
      --case <FILE>  The case file
      --json         Print JSON. Required for the reason `hp sources urls` gives
  -h, --help         Print help
```
