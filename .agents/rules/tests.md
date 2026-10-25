# Tests: what a test must earn

What a test here must earn beyond being able to fail. Its readers are whoever
writes or changes a test, every reviewer of one, and the `tests` department. A
test that cannot fail is text-residue's `ceremony` (`.agents/rules/slop.md`, "The kinds").
This file owns the tests that can fail and still cost more than they protect.

## What counts as a test here

Three groups, and nothing else:

- **The runner's selftest.** `python tools/evals.py selftest` runs the
  `_selftest_*` functions in `tools/evals.py` over the recorded event streams
  in `tools/evals-fixtures/`. `.github/workflows/conformance.yml` runs it on
  every pull request, and it calls no model.
- **The eval suites.** `evals/<package>/<skill>/` holds `cases.yaml`,
  `held-out.yaml`, `rubric.yaml` and, for a calibrated rubric,
  `calibration.json`. `.github/workflows/evals.yml` runs them against real
  clients after a release. `python tools/evals.py validate` loads them on every
  pull request and checks that each folder has its skill, nothing more. No
  program under `tools/` reads `calibration.json`. It is the evidence behind a
  rubric's criteria.
- **The assertion steps** of `.github/workflows/conformance.yml` and
  `.github/workflows/integration.yml`: the steps whose job is to refuse
  something, such as a skill a client does not list.

`tools/check-conformance.py` is the check, not a test. `.agents/rules/conformance.md`
governs it.

## The kinds

Other kinds: the shared tests page.

| Kind | Definition | Measurement |
| :-- | :-- | :-- |
| `misaligned` | A case or question measures something other than the skill's behaviour. Its expectation contradicts the skill's text, a near-miss prompt matches a "Use when" clause of the description, or it breaks a rule `CONTRIBUTING.md` writes for cases | The two texts side by side, each with its permalink at the analysed commit: the case or question, and the clause of the skill or of the rule. A recorded session where the effect shows is a lead |
| `ceiling` | A rubric question every graded answer passes in both arms. `CONTRIBUTING.md` says to drop it, "because it measures nothing" | Every recorded answer to the question in the comparable releases, labelled yes or no with its evidence quoted, by arm. Beside it the question's mean per arm and repeat from the evals records in `ghcr.io/akurganow/ai-plugins-evals`. Ceiling when one label stands in both arms |

## Reading the records

The OCI artifacts in `ghcr.io/akurganow/ai-plugins-evals` are the record of
how a case behaved against real clients. `tools/evals.py` writes them
(`cmd_run`, `run_session`, `grade_runs`, `cmd_report`, `push_record`).

- **Fields.** Each artifact holds one run record per skill, client and repeat.
  A run records `tag`, `package`, `skill`, `client`, `repeat`, `run`,
  `run_id`, `client_version`, `model`, `jev_model`, `cases_sha256`,
  `rubric_sha256`, `always_on`, `questions` and `sessions`. A session records
  `case`, `kind`, `arm`, `fired`, `answer`, `cost_usd`, `error` and `nouls`,
  Jev's score per question id.
- **Comparable.** Two runs are comparable when both hashes are equal.
  `compare` applies the same rule. A record measures the folder at the
  analysed commit when its hashes equal the `sha256` of `cases.yaml` and
  `rubric.yaml` there.
- **The unit is the metric range over the three repeats** of one complete run
  of one skill on one client. `docs/design.md`, "Behavioural evals run after
  each release", says the spread between repeats is the tolerance. A swing
  inside the spread is no exhibit.
- **A per-prompt load count is a lead.** A prompt has three sessions per
  client, so its count can move from 0 of 3 to 3 of 3 with nothing changed.
- **A claim that a test is unstable** needs three things. They are two
  comparable releases, an empty `git diff` of `plugins/<package>/skills`
  between their tags, and equal `client_version`, `model` and `jev_model`.
  Otherwise the input that moved is the client or the model, and the runner
  installs the latest client by design (`docs/design.md`, same section). One
  record, or one CI run, makes a finding `plausible` at most.
- **`always_on` clients** have no `trigger_hit` or `compliance`. Nothing is
  claimed about those two metrics for them.

## No protection lost silently

Editing `cases.yaml` or `rubric.yaml` has a price that is not a lost mutation.
The next release's `compare` returns "not comparable", so that release has no
regression check. The release after it compares again. Every release also
repeats the model sessions. So an alternative that touches a folder lists all
its edits to `cases.yaml` and `rubric.yaml` at once, and states the price.
`held-out.yaml` is outside the comparison and pays
nothing. `calibration.json` records the `sha256` of the rubric it scored, so a
rubric edit leaves it describing the old text. The alternative says so.

## Protected: never a finding

1. A probe that exists to prove a check can fail. Examples are a wrong skill
   name that must not count as a load, and an input a function must refuse.
   The assertion that it does is the probe.
2. A test or step turned off with a stated reason beside it. Examples are the
   matrix exclusion that cites its failed run, and the notice step that
   reports a check as not run. It is `environment-coupled` only when skipping
   it leaves its contract with no CI signal.
3. The platform, tested on purpose. The install matrix and the archive
   verification job test what a client does with a package and what a release
   publishes. Their breadth across systems is the contract, and the header of
   `integration.yml` says what each job proves.
4. Exactness that is the requirement: a recorded client event stream, the
   fingerprint line `tools/evals.py` writes and reads back, the byte-identical
   comparison of `cases.yaml` and `rubric.yaml`, a digest check.
5. Duplication kept for clarity: one fixture and one set of assertions per
   client, setup repeated so each test reads alone.
6. A distinct input. A case or fixture that feeds what no other feeds is not
   redundant because another runs the same lines.
7. A shape with a recorded reason, while the reason is true. The runner's
   docstring and `docs/design.md`, "Behavioural evals run after each release",
   record these:
   - the runner is this repository's own;
   - the Jev model is pinned;
   - the latest client is installed;
   - held-out prompts are never graded;
   - ten prompts per kind and three repeats follow the Agent Skills guide;
   - the without arm removes a different set in each client.

   A claim of fact inside a reason is still judged against the tree.
8. Spread between repeats that stays inside the spread.
9. `calibration.json` as recorded evidence. An edit that makes it stale is a
   cost of that edit, stated in the finding that proposes the edit.
10. A held-out prompt's existence, its count and its being left out of
    grading.
