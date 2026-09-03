# The interests interview, and the files the user owns

Everything downstream is built on `interests.yaml` and `questions/*.yaml`.
Those two come out of the interview below, and they are the reason a howp
dashboard is about *them* rather than about whatever happened to be liquid
this week. Get them wrong and the rest of the pipeline works perfectly on
the wrong subject.

Do not fill them in from a template. Do not guess someone's interests from
their repository, their timezone or the fact that they installed this. Ask.

## How to run the interview

**One question at a time, each one informed by the last answer.** Not a
form, not a numbered list of ten questions pasted at once. The user answers,
you learn something, and the next question exists because of what they just
said. Stop when you have enough to write questions somebody could later
check the answer to — usually four to eight exchanges per interest area,
fewer if the user is already precise.

Open wide, then narrow:

1. **What do you actually follow?** Not "what topics interest you" — what
   do they already read, check, argue about, refresh?
2. **Why that?** The answer decides everything below. "I work in it" wants
   different questions from "I have money on it" or "I want to know if the
   scary version is real". Ask it, and do not answer it for them.
3. **What would change your mind about it?** This is the question that
   converts an interest into something measurable, and it is the one worth
   pushing on. Follow whatever they say with "how would you know that
   happened?"
4. **By when?** An interest with no horizon produces questions no market can
   answer. If they say "eventually", offer two or three concrete horizons
   and let them pick.
5. **What would you not want on the dashboard?** Just as useful. Someone
   following a war does not necessarily want a casualty count on their
   morning page.

Techniques that make it adaptive rather than an interrogation:

- **Follow the energy.** When an answer gets longer and more specific,
  that is the vein — dig there before moving on.
- **Reflect back a sharper version and let them correct it.** "So: whether
  any lab publicly claims AGI before 2028 — or is it more that you want to
  know when the claims stop being marketing?" People correct a wrong precise
  statement far more readily than they produce a right one from nothing.
- **When an answer is unmeasurable, say so and ask for the proxy.** "Nobody
  settles 'is the field slowing down'. What would you accept as evidence?"
- **Do not stack questions.** One at a time, and wait.
- **Repeat back the list before writing anything**, and let the user cut it.
  A dashboard of twelve questions they half-care about is worse than four
  they check daily.

Then: state which interests and questions you are about to write, in plain
language, and get an explicit yes before touching a file.

## `interests.yaml`

A list at the top level. One entry per area.

```yaml
- id: ai-frontier
  name: The AI lab race
  notes: >
    Who is ahead: releases at the frontier, benchmark positions, public
    claims about AGI. I care about the claims stopping, not the leaderboard.
- id: my-city-housing
  name: Housing where I live
  notes: >
    Prices and rates in the city I want to buy in over the next two years.
```

- `id` — short, lowercase, `[a-z0-9-]`. It becomes the file name
  `questions/<id>.yaml` and `matches/<id>.yaml`, so it is awkward to change
  later; pick it deliberately.
- `name` — how the user says it. It appears on the dashboard.
- `notes` — optional free text. This is context for you, later: what
  specifically matters, what the user already knows, what they would not
  want. Write it in enough detail that a later session can pick up the
  thread without re-running the interview.

## `questions/<interest-id>.yaml`

One file per interest, a list at the top level.

```yaml
- id: ai-agi-claim-2028
  text: >
    Will a major AI lab publicly claim to have achieved AGI before
    1 January 2028?
  kind: binary
  horizon: '2027-12-31'
  status: active
  search_terms:
    - AGI declared before 2028
    - lab claims artificial general intelligence
- id: ai-frontier-leader-2026
  text: Which lab holds the top frontier model position at the end of 2026?
  kind: multi
  horizon: '2026-12-31'
  status: active
  search_terms:
    - best AI model end of 2026
    - frontier model leader
```

- `id` — **validated when the file is read**: it must start with a lowercase
  letter or digit and hold only lowercase letters, digits and `-`. Anything
  else is a parse error that stops the run. It is also a chart file name.
  Prefixing with the interest id keeps them unique and readable.
- `text` — the question as a person would ask it. A concrete event, a
  checkable outcome, a horizon. If you cannot say who would confirm it and
  how, it is not a question yet.
- `kind` — `binary` (one yes/no outcome) or `multi` (several mutually
  exclusive outcomes). Defaults to `binary`.
- `horizon` — free text, but a date is what makes verification work: you
  measure the market's own deadline against it when you bind one, and a
  divergence of up to three months makes the match `partial`, more than three
  months a `mismatch`, and a deadline already passed a `mismatch` outright
  (`references/procedures.md`). So a vague horizon does not produce a lenient
  verdict, it produces a worse one. Quote a bare date so YAML keeps it a
  string.
- `status` — `active`, `resolved`, `expired` or `archived`. Defaults to
  `active`. **Only `active` questions are quoted**, which is also how a user
  parks something without deleting it.
- `search_terms` — English phrases to search Polymarket and Manifold with
  when binding this question to a market. English regardless of the user's
  language: the markets are English. Nothing in the package searches for you,
  so these are notes to whoever does — phrase them as somebody would title a
  market rather than as a sentence, and two or three well-aimed ones beat a
  long list. An empty list leaves the question's own text as the only thing to
  search with, which for a question written in another language is close to
  useless.

The user edits both files by hand afterwards, and should be told so. Never
overwrite a question they wrote; append.

## What makes a good question here

- **Checkable by a named source.** "Will X be announced" beats "will X be
  important".
- **One event.** A question with an "and" in it usually wants to be two.
- **Dated.** "By the end of 2026", not "soon".
- **Something a market might plausibly cover.** Prediction markets are
  thickest on elections, macro numbers, sport, company events, model
  releases and public claims; they are thin on anything local or personal.
  A question no market covers is not wasted — the dashboard lists it as
  uncovered — but a page of them is a disappointment worth warning about
  before you write twelve.

## After writing the files

Verification is what turns a question into something with a probability: a
question with no market behind it is listed on the dashboard as uncovered and
never gets a number. Binding one is the first of the three procedures in
`references/procedures.md` — you find candidate markets yourself, fetch the
market's own body, judge it, and land the judgement with one `hp ingest match`
call that reads every fact about the market out of that body. `hp ingest check
questions` and `hp ingest check matches` read these files strictly afterwards
and report what is wrong with them.

Then tell the user which questions got a market and which did not. The ones
that did not are not a failure of the interview; they are the honest part of
the page, and often the ones worth rewording together.
