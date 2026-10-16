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

## The one test

> Does this test fail only when the product is wrong, and is what it costs
> in proportion to what only it protects?

- **The product is wrong** when it breaks a contract. The contract is
  written in a docstring of `tools/evals.py`, in `docs/design.md`, in a
  skill's text, or in the install promise of `README.md`.
- **A mutation** is such a break, written out as an edit. For the selftest it
  is an edit of the runner. For an eval case or question it is an edit of the
  skill that stops it loading or following its own rule. For an assertion
  step it is a package or an install that the step must refuse.
- **What a test protects** is the set of mutations that turn it red.
- **What only it protects** is the part of that set no other test catches.
- **Cost** is its lines, its upkeep, the model calls and CI minutes it spends,
  and every red it shows with nothing broken.

## Writing a test

1. **Decide at the cheapest point.** The selftest feeds a recorded stream to a
   parser and a dict to `metrics`, and starts no client. An install assertion
   reads a client's inventory and calls no model. A heavier point runs the
   platform with the decision, and fails when the platform moves.
2. **Assert the requirement and no more.** A field, a prefix or a range where
   the requirement is one. Exactness only where exactness is the requirement,
   such as a fingerprint line or a byte-identical file.
3. **Control every input.** Replace `gh`, the network, `subprocess.run` and
   `time.sleep` with fakes, and restore each in a `finally`. Restore what the
   test writes to the process, such as `os.environ`. Otherwise a later test
   depends on the order they run in.
4. **A case measures the skill and nothing else.** Its prompt carries what it
   asks about, asks for the result in the reply and never names the skill. A
   question can be judged from the answer alone. `CONTRIBUTING.md`, "Write a
   skill's evals cases", holds these rules with their reasons. A case that
   breaks one measures the prompt's wording.
5. **Before adding a case, find the case that should have caught the
   problem.** Sharpen it if it exists. A second case beside one that nearly
   held the scenario is redundancy born with the fix.
6. **A change that moves a test's protection elsewhere retires the test in the
   same change.** A green test for something gone reads as evidence about
   nothing.

## The kinds

Each is a way a test that can fail costs more than it protects. No
measurement, no finding. The token is what the fingerprint carries.

| Kind | Definition | Measurement |
| :-- | :-- | :-- |
| `environment-coupled` | The result depends on an input the test does not control: process-global state left changed, the runner image, a fetch at run time, an unpinned client or model, job order | The uncontrolled input traced to the assertion. Two runs where the result differs. Each is a CI run with its attempt numbers, or a command in a copy under `$RUN` with one input changed and its output quoted. First show the nondeterminism is not the product's. For an eval the pair is two comparable releases, read as "Reading the records" says |
| `change-detector` | It pins implementation text where a behaviour test or a validator already guards the contract, such as a log line's wording or a table row | A behaviour-preserving edit, written out, that turns it red, and the test or validator that already guards the contract |
| `redundant` | Every mutation it catches, another test catches. In an eval, two questions of one rubric judge the same rule of the skill | The protection ledger: each mutation it catches, with the other test that goes red on it. For two questions, the rule of the skill each judges, and the recorded answers one marks down that the other also marks down |
| `over-specified` | The assertion demands more than the requirement, such as exact equality on a float, a cost or a count taken from a trimmed fixture. For a question, the statement is stricter than the skill's rule | The requirement quoted, and an output that meets it and fails the assertion. For a question, a recorded answer that follows the skill's rule and scores no |
| `disproportionate` | Its machinery outweighs its contract, and a cheaper point already makes the decision. An example is a job that installs clients on three systems to learn what a validator already decides | Four items. The contract in one sentence. The line that makes the decision. The smallest check that guards it, written out and caught by the same mutation. The ways the current test fails with no change to the product, with the CI run minutes or the `cost_usd` of its sessions |
| `bloat` | A file or cluster grew without a matching contract: more assertions, helpers, cases or sessions than the contracts they pin. A helper with one call site in the selftest belongs here, because the `abstractions` department stops at test code | Two measured columns. The cost: assertions, lines, helpers, edits in commits that changed no behaviour, and for cases the sessions and their summed `cost_usd`. The protection only these tests provide |
| `misaligned` | A case or question measures something other than the skill's behaviour. Its expectation contradicts the skill's text, a near-miss prompt matches a "Use when" clause of the description, or it breaks a rule `CONTRIBUTING.md` writes for cases | The two texts side by side, each with its permalink at the analysed commit: the case or question, and the clause of the skill or of the rule. A recorded session where the effect shows is a lead |
| `ceiling` | A rubric question every graded answer passes in both arms. `CONTRIBUTING.md` says to drop it, "because it measures nothing" | Every recorded answer to the question in the comparable releases, labelled yes or no with its evidence quoted, by arm. Beside it the question's mean per arm and repeat from `evals.json`. Ceiling when one label stands in both arms |

Cross-kind rules:

- One finding, one kind: the one whose alternative is the fix proposed.
- A test born with a fix is judged against what later commits did to the code
  it pins. "It never failed" is never grounds on its own. A test that never
  failed may still guard a contract.
- Without the interpreter, a package index or a client, "this mutation turns it
  red" and "the replacement passes" are `plausible`. Say which was missing
  (`.agents/rules/unattended.md`, "Report honestly").

## Reading the records

A release's `evals.json` is the only record of how a case behaved against
real clients. `tools/evals.py` writes it (`cmd_run`, `run_session`,
`cmd_report`).

- **Fields.** `runs` holds one run per skill, client and repeat. A run records
  `client_version`, `model`, `jev_model`, `cases_sha256`, `rubric_sha256`,
  `always_on` and `sessions`. A session records `case`, `kind`, `arm`, `fired`,
  `answer`, `cost_usd`, `error` and `nouls`, Jev's score per question id.
- **Comparable.** Two runs are comparable when both hashes are equal.
  `compare` applies the same rule. A record measures the folder at the
  analysed commit when its hashes equal the `sha256` of `cases.yaml` and
  `rubric.yaml` there.
- **The unit is the metric range over the three repeats** of one skill on one
  client. `docs/design.md`, "Behavioural evals run after each release", says
  the spread between repeats is the tolerance. A swing inside the spread is
  no exhibit.
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

A removal names, for each mutation the test catches, the test that still
catches it. What nothing else catches is kept or replaced. This file measures
redundancy by mutations caught, never by lines executed, because a line can
run with nothing checked. A replacement answers to this file like any other
test. One written only to catch a named mutation can pin the implementation
and become a `change-detector` of its own.

Editing `cases.yaml` or `rubric.yaml` has a price that is not a lost mutation.
The next release's `compare` returns "not comparable", so that release has no
regression check. The release after it compares again. Every release also
repeats the model sessions. So an alternative that touches a folder lists all
its edits to `cases.yaml` and `rubric.yaml` at once, and states the price in
"What still protects". `held-out.yaml` is outside the comparison and pays
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
   fingerprint line `github-needs` defines, the byte-identical comparison of
   `cases.yaml` and `rubric.yaml`, a digest check.
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

## Neighbours

Which department owns a finding is decided by the departments' own scopes.
These cases belong to the others:

- a test that cannot fail is `text-residue`'s `ceremony`;
- a case repeated under a second id is `text-residue`'s `residue`;
- a skill text a case contradicts is `claims`' or `text-residue`'s;
- a defect a test reveals is `logic`'s;
- a pinned version in an assertion step is `dependencies`'.

The runner's own functions, `compare` and `metrics` among them, are not
tests. Only the test code is judged here.

A missing test is not a finding. Tests that cost more than they protect are
findings, and an absent test costs nothing.

## Where tests live

- **The selftest.** The `_selftest_*` functions and their helpers in
  `tools/evals.py`, and the fixtures in `tools/evals-fixtures/`. The comment
  above `_selftest_parsers` gives the fixtures' origin. Two censuses show the
  usual tells:
  - process-global writes and patches:
    ```
    awk '/^def _selftest_parsers/,/^def main/' tools/evals.py | grep -nE 'os\.environ|^\s*global |subprocess\.run =|urlopen|time\.sleep'
    ```
  - exact equality on floats, costs and lengths:
    ```
    awk '/^def _selftest_parsers/,/^def main/' tools/evals.py | grep -nE '== [0-9]+\.[0-9]+|cost_usd ==|len\([^)]*\) == [0-9]+'
    ```
- **The assertion steps.**
  ```
  grep -nE 'grep -q|diff --exit-code|verify-blob|sha256sum -c|exit "\$(status|bad)"' .github/workflows/conformance.yml .github/workflows/integration.yml
  ```
  Some assertions appear in both workflows.
- **The eval folders.** `git ls-files evals`. Each `cases.yaml` and
  `rubric.yaml` is read against the `SKILL.md` and references of its skill,
  and against the rules in `CONTRIBUTING.md`.
- **The records.** The `evals.json` of each release of a package that has
  cases, selected as "Reading the records" says.
- **Failure records.** The issues whose title begins `evals:` and whose
  fingerprint names the role `evals`. Each was filed when the runner saw a
  metric range that did not overlap. They are leads, never exhibits.
- **What CI does not prove.** `conformance.yml` proves that `selftest`
  passes and that every evals folder loads, not that either would fail when
  it should. Nothing in CI runs a case against a model on a pull request.
  `integration.yml` calls no model: it asserts that a pinned client lists a
  skill or shows a package enabled, and says nothing about whether a skill
  triggers.
