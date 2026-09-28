# Every `hp` command, verbatim

Written by the release job from the binary's own `--help`, top level and every
subcommand recursively, at `hp 0.3.10` (`howp-v0.3.10`) on 2026-09-28.
Nothing here is paraphrased and nothing is added. Where this file and the binary
in front of you disagree, **the binary is right**. This file is never edited by
hand: the next release rewrites it from the binary it publishes.

## `hp --help`

```
One command over a how-possible workspace: ingest what somebody else fetched, name what to fetch next, and compute, render and score what the store holds

Usage: hp <COMMAND>

Commands:
  ingest     Write a source's raw response into the record
  sources    Name the requests a fetch needs
  matches    Read the verdict cache
  stats      Everything the dashboard computes about a question, as JSON
  render     The dashboard, as one Markdown page
  digest     The weekly digest, read rather than written
  moves      Sharp probability moves over the live snapshot history
  bench      The benchmark's deterministic half: arithmetic, a substring check, two reports, and the requests a case's own sources imply
  forecast   Probability distributions from finishing orders, rates and markets: files in, JSON out
  estimator  Evidence rows as the states an estimator that answers yes or no with a probability is asked in: anonymised, rotated, and beside a control state that holds no evidence; and its answers read back
  help       Print this message or the help of the given subcommand(s)

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

## `hp forecast --help`

```
Probability distributions from finishing orders, rates and markets: files in, JSON out

Usage: hp forecast <COMMAND>

Commands:
  strengths  Participant and group strengths fitted from finishing orders
  places     The probability of every finishing position, counted over seeded draws, and each group's ranks by points
  rates      A place's rate of an event per session, shrunk toward every place's: how many times in the next session, or whether at all
  pool       A question's every variant: its baseline pooled with the gated market and the evidence effect, or rows drawn from another question's entry; appended to the record, and printed
  score      Each record's questions scored against what happened, every variant with its skill against the market and the base, and the estimator's variant against the market's, record by record
  fit        The constants, fitted once: each family's weights over past records, leaving one record out at a time; the decays and Harville exponents over past finishing orders; and the space an estimator's shifts are averaged in, over its answers; written to `--out`, with what each was fitted over printed
  help       Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp forecast strengths --help`

```
Participant and group strengths fitted from finishing orders

Usage: hp forecast strengths --orderings <FILE> --entrants <FILE> --kind <KIND> --as-of <ISO> --constants <FILE> --json

Options:
      --orderings <FILE>
          The finishing orders of past events (`hp-orderings-1`)

      --entrants <FILE>
          Who takes part in the event being forecast (`hp-entrants-1`); the output lists them in this order

      --kind <KIND>
          The kind of event to fit over; events of every other kind are left out

      --as-of <ISO>
          The moment of the fit: only events strictly before it count, each weighted by its age in days before it.
          
          **Required, and never defaulted**, for the reason `--ts` is: this binary reads no clock, and a moment it invented would decide which events count and how much.

      --constants <FILE>
          The constants (`hp-constants-1`); the two decays are read from it

      --json
          Print JSON. Required for the reason `hp sources urls` gives

  -h, --help
          Print help (see a summary with '-h')
```

### `hp forecast places --help`

```
The probability of every finishing position, counted over seeded draws, and each group's ranks by points

Usage: hp forecast places [OPTIONS] --input <FILE> --constants <FILE> --seed <N> --draws <N> --json

Options:
      --input <FILE>      What the places are drawn from: strengths (`hp-strengths-1`), or a win distribution (`hp-distribution-1` of form `options`)
      --constants <FILE>  The constants (`hp-constants-1`); the two Harville exponents are read from it
      --seed <N>          The generator's seed. Required, and never defaulted: with the number of draws it is what the same probabilities are drawn again from
      --draws <N>         How many draws the probabilities are counted over, 1 or more
      --points <FILE>     Points by position (`hp-points-1`); with it, each group's ranks by points and the probability that it scores the most are counted too
      --entrants <FILE>   The group each option of a win distribution takes part for (`hp-entrants-1`); strengths name their own
      --json              Print JSON. Required for the reason `hp sources urls` gives
  -h, --help              Print help
```

### `hp forecast rates --help`

```
A place's rate of an event per session, shrunk toward every place's: how many times in the next session, or whether at all

Usage: hp forecast rates [OPTIONS] --counts <FILE> --place <PLACE> --session <KIND> --as-of <ISO> --form <FORM> --question <ID> --json

Options:
      --counts <FILE>
          How many times the event happened, per place and session (`hp-counts-1`)

      --place <PLACE>
          The place the forecast is for. A place the counts do not name has no sessions and takes the pooled rate, a misspelt one too

      --session <KIND>
          The kind of session to read; sessions of every other kind are left out

      --as-of <ISO>
          The moment of the forecast: only sessions strictly before it count.
          
          **Required, and never defaulted**, for the reason `--ts` is: this binary reads no clock, and a moment it invented would decide which sessions count.

      --form <FORM>
          What the distribution answers

          Possible values:
          - count:  How many times in the next session: the cells `0`, `1` and `2+`
          - yes-no: Whether it happens at all: the cell `yes`

      --sessions <N>
          With `yes-no`, the probability that it happens in at least one of N sessions rather than in the next one; 1 or more, and refused with `count`

      --question <ID>
          The question the distribution answers, as it names it

      --json
          Print JSON. Required for the reason `hp sources urls` gives

  -h, --help
          Print help (see a summary with '-h')
```

### `hp forecast pool --help`

```
A question's every variant: its baseline pooled with the gated market and the evidence effect, or rows drawn from another question's entry; appended to the record, and printed

Usage: hp forecast pool [OPTIONS] --question <ID> --family <NAME> --record <PATH> --constants <FILE> --estimator <ESTIMATOR> --json <--live|--reconstruction>

Options:
      --question <ID>
          The question the entry answers

      --family <NAME>
          The question's family, which names its weights in the constants

      --record <PATH>
          The record (`hp-forecast-record-1`) the entry is appended to. Made when there is no file there yet, with the four header flags

      --constants <FILE>
          The constants (`hp-constants-1`): the family's weights, the Harville exponents derived rows are drawn under, and the model id a new record carries

      --estimator <ESTIMATOR>
          Which variant is printed. The protocol sets it, and it is never defaulted

          Possible values:
          - shadow: Recorded beside the printed `market` variant and never printed
          - on:     Printed

      --live
          The entry is forecast before the cutoff, from what was available then

      --reconstruction
          The entry is rebuilt afterwards, from inputs available before the cutoff

      --baseline <FILE>
          The baseline: a distribution (`hp-distribution-1`) of form options, yes-no or count — or, with `--slice`, places (`hp-places-1`) to cut one from

      --slice <SLICE>
          What is cut from places: `win` or `group-most-points` for a baseline; `membership:K`, or `positions:K` or `group-positions:K` of up to three ordered rows, for derived rows

      --derive-from <QUESTION>
          Rows derived from this question's last entry in the record: each of its variants drawn through places and cut by `--slice`. Its pick heads ordered rows unless `--head` names another question

      --head <QUESTION>
          The question whose pick heads ordered rows, when it is not the one they are derived from: rows over groups are headed by a question over the groups. Membership takes no head

      --seed <N>
          The seed every variant of derived rows is drawn with

      --draws <N>
          How many draws derived rows are counted over, 1 or more

      --points <FILE>
          Points by position (`hp-points-1`), for derived rows over groups

      --entrants <FILE>
          The group each option takes part for (`hp-entrants-1`), for derived rows over groups

      --market <FILE>
          The question's market after the gate (`hp-market-1`)

      --effect <FILE>
          The evidence effect of the selected rows (`hp-effect-1`)

      --effect-unselected <FILE>
          The evidence effect of every admitted row (`hp-effect-1`): the `estimator_unselected` variant

      --floor-question <ID>
          Another yes-no question in the record, whose variants this yes-no's are floored at

      --stage <STAGE>
          Which pass of the forecast the entry is. A question has one `initial` entry, and a rerun is appended beside it

          Possible values:
          - initial:     The first pass
          - tie-rerun:   The pass after more evidence was gathered on options tied at the top
          - after-trial: The pass after a trial session
          
          [default: initial]

      --issued <ISO>
          When the forecast was issued: ISO-8601 with an offset. Part of a new record's header, and checked against an existing one's

      --cutoff <ISO>
          The moment no input may postdate: ISO-8601 with an offset. A market price taken after it is not used. Part of a new record's header, and checked against an existing one's

      --protocol <TEXT>
          The protocol's version, as the caller names it. Part of a new record's header, and checked against an existing one's

      --inputs <FILE>
          The files the forecast is made from (`hp-inputs-1`), each hashed here and named by the entry. Part of a new record's header; a later call adds those the header does not list, and is refused for one it lists with another hash

      --json
          Print JSON. Required for the reason `hp sources urls` gives

  -h, --help
          Print help (see a summary with '-h')
```

### `hp forecast score --help`

```
Each record's questions scored against what happened, every variant with its skill against the market and the base, and the estimator's variant against the market's, record by record

Usage: hp forecast score [OPTIONS] --record <FILE>... --json

Options:
      --record <FILE>...      The records (`hp-forecast-record-1`) to score; each question's last entry is its forecast
      --resolution <FILE>...  What happened (`hp-resolution-1`), each naming the record it resolves by file name. A record given with none is listed as unresolved
      --json                  Print JSON. Required for the reason `hp sources urls` gives
  -h, --help                  Print help
```

### `hp forecast fit --help`

```
The constants, fitted once: each family's weights over past records, leaving one record out at a time; the decays and Harville exponents over past finishing orders; and the space an estimator's shifts are averaged in, over its answers; written to `--out`, with what each was fitted over printed

Usage: hp forecast fit [OPTIONS] --orderings <FILE> --priors <FILE> --model-id <TEXT> --out <FILE> --json

Options:
      --orderings <FILE>      The finishing orders of past events (`hp-orderings-1`): the decays and the Harville exponents are fitted from them alone
      --priors <FILE>         Each family's prior weight on the market and where it comes from (`hp-priors-1`): the constants carry every family it names, and a question of another family is refused
      --record <FILE>...      The records (`hp-forecast-record-1`) the weights are fitted over, one event each; without any, every family keeps its prior and no effect
      --resolution <FILE>...  What happened (`hp-resolution-1`), each naming the record it resolves by file name. A record given with none is listed and not fitted over
      --answers <FILE>...     The estimator's answers of earlier rounds (`hp-answers-1`): the space its shifts are averaged in is chosen from them, and without any it is log-odds
      --model-id <TEXT>       The estimator the constants are fitted for, as the opaque id the caller supplies. Every record and every answers file given must have been made for it
      --out <FILE>            Where the constants (`hp-constants-1`) are written, whole
      --json                  Print JSON. Required for the reason `hp sources urls` gives
  -h, --help                  Print help
```

## `hp estimator --help`

```
Evidence rows as the states an estimator that answers yes or no with a probability is asked in: anonymised, rotated, and beside a control state that holds no evidence; and its answers read back

Usage: hp estimator <COMMAND>

Commands:
  prepare  A family's evidence as a plan: every rotation of its options' labels, each over the admitted rows and over none, with the stage's questions and the re-identification check
  read     An estimator's answers read back against their plan: the select stage's as a selection, and the estimate stage's as each option's evidence effect, with the re-identification check scored
  help     Print this message or the help of the given subcommand(s)

Options:
  -h, --help  Print help
```

### `hp estimator prepare --help`

```
A family's evidence as a plan: every rotation of its options' labels, each over the admitted rows and over none, with the stage's questions and the re-identification check

Usage: hp estimator prepare [OPTIONS] --evidence <FILE> --stage <STAGE> --as-of <ISO> --json

Options:
      --evidence <FILE>
          The family's options and every name each is known by, the rows, and the questions (`hp-evidence-1`)

      --stage <STAGE>
          `select` asks of every row which option it concerns, whether it bears on the question and whether it states a fact; `estimate` asks the family's questions over the admitted rows and over none

          Possible values:
          - select:   Of every row: which options it concerns, whether it bears on the question, and whether it states a fact
          - estimate: The family's questions, over the admitted rows and over none

      --selection <FILE>
          The select stage's answers read back (`hp-selection-1`): the estimate stage admits the rows it admits

      --all-rows
          The estimate stage admits every row of kind evidence published before the moment, with no selection

      --as-of <ISO>
          The moment the states are prepared for: only rows published strictly before it are admitted, each with its age in whole days before it.
          
          **Required, and never defaulted**, for the reason `--ts` is: this binary reads no clock, and a moment it invented would decide which rows count. It may not be later than the evidence's own cutoff.

      --json
          Print JSON. Required for the reason `hp sources urls` gives

  -h, --help
          Print help (see a summary with '-h')
```

### `hp estimator read --help`

```
An estimator's answers read back against their plan: the select stage's as a selection, and the estimate stage's as each option's evidence effect, with the re-identification check scored

Usage: hp estimator read --plan <FILE> --answers <FILE> --constants <FILE> --json

Options:
      --plan <FILE>       The plan the answers answer (`hp-estimator-plan-1`), of either stage
      --answers <FILE>    What the estimator answered (`hp-answers-1`)
      --constants <FILE>  The constants (`hp-constants-1`): the space the estimate stage's shifts are averaged in, and the model id its answers must be of for an effect other than 0
      --json              Print JSON. Required for the reason `hp sources urls` gives
  -h, --help              Print help
```
