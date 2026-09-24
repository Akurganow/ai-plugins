# Brainstorm decisions (superpowers/brainstorming, architectural path)

Date: 2026-09-24. Branch for implementation: claude/marketplace-plugin-quality-review-b5tbjh.

## Intent
Success = all four: outside reader installs without questions; packages pass external
catalogues (Anthropic community, Hermes catalog, awesome lists); same package works fully in
Claude Code, Codex, Hermes, Oh-My-Pi; repo reads as the owner's showcase.

## Constraints (owner)
- hp sources stay private.
- Nine-role agent system stays (compose unchanged; rules may change).
- Any copy of a file must be generated on CI from one source; automatic version bump and tags.
- Prefer proven ready-made tools over home-grown ("no bicycles, even other people's").
- Symlink manifest and "no vendor manifests" are OPEN, subject to the CI-generation rule.
- Delivery: spec + plan here, implementation in this session, PR on the designated branch.

## Decisions
- H7 diary: remove entirely. No statements about testing in README/SKILL.md. Drop
  "Say what was not verified" from claims.md; drop its protection in slop.md, slop-police,
  spec-writer, implementer, project.md. Keep: every client claim cites docs/source by permalink.
- H7 rule-checking: agent-police gets an external measure (list of external sources read
  first, rules judged against them). No scheduled external run, no change to slop-police scope.
- NEW: integration tests in CI, matrix macOS/Linux/Windows x Claude Code/Codex/Oh-My-Pi/Hermes.
  Spike to verify: Hermes on Windows; auth needs for headless plugin install per client.
  Windows job also decides the symlink-manifest question empirically.
- H1 SECURITY.md: no package enumeration. Two rules: package with releases -> latest release;
  package without releases -> state of main.
- H2 README: one template for all six by standard-readme (what, install, usage with a prompt,
  what's inside, boundaries, license, help). howp adds network, prerequisites, failure behaviour.
  Five existing READMEs rewritten to it.

## Order the items were taken in
H3+H4 descriptions/catalogue -> H5 root README -> H6 binary provenance -> M1 changelog/tags ->
M2 LICENSE -> M3 community files -> M4 validators/evals -> M5-M7 skills -> M8 prose-discipline
components -> M9 extensions -> L1-L6.
- H3+H4: plugin.json is the source (short description <=250 chars, homepage, category under
  extensions in the repo's own namespace); marketplace.json generated on CI with name, source,
  description, homepage, category; CI fails if committed catalogue differs. Long text only in
  README. prose-discipline's interface/shortDescription/displayName in extensions removed.
- H5 root README: one file, restructured: TOC, install right after the first paragraph,
  explanations moved to the end under their own headings, sentences <=26 words, plugin table
  generated on CI (name, one line, link to package README). Text checked with prose-discipline.
- H6 (chosen by me at owner's request after reading how-possible@c4fb194): cosign keyless
  signing in how-possible's `publish` job (needs `id-token: write` there), over SHA256SUMS
  (goreleaser convention): SHA256SUMS.sig + SHA256SUMS.pem uploaded beside the archives in the
  public release. Verification: ai-plugins integration CI runs cosign verify-blob against the
  workflow identity; howp README documents the one-line check. Skill keeps sha256 only.
  Rejected: actions/attest-build-provenance (private-repo attestations verifiable only with
  repo access); cosign in the skill (users lack cosign).
  how-possible facts: cargo-release + git-cliff auto-bump on merge; release.yml permissions
  contents:read; publish via gh + HP_RELEASES_TOKEN; commits three files into ai-plugins main.
- M1: release-please, monorepo manifest config; per-package path, release-type simple, version
  written into plugin.json via extra-files JSON path, CHANGELOG.md per package, per-package tag
  (separator to decide; Claude Code documents `{plugin}--v{version}` for dependency resolution);
  howp excluded (its release job in how-possible owns version). Release via release-PR.
- M2: LICENSE copied into each package; CI step checks each equals the root LICENSE.
- how-possible change (H6 cosign): to be filed as an issue in Akurganow/how-possible at
  implementation time with the exact spec; no work in that repo in this session (owner).
- NEW H8 (found during M3): issue-court tries issues filed by people (SKILL.md:53-54, queue =
  all open issues :151-158); tracker-clerk lists every open issue (:173) and applies
  pipeline/intake. Owner: pipelines are private; outsiders must never learn of them; machine
  issues are labelled and separate; agents never touch human issues.
  Decision: invert the filter. Roles read ONLY issues carrying the machine label `police-report`
  AND a fingerprint marker; everything else does not exist for them. Human issue templates apply
  their own labels (bug, install, package). Edit issue-court, tracker-clerk, pipeline-clerk,
  github-needs, pipeline-law where the queue is defined. Public docs never mention the pipeline.
- M3: CONTRIBUTING.md, SUPPORT.md, issue templates (YAML forms with package/client/OS fields,
  applying human labels), Contributing and Help sections in README, trust warning above install.
  No CODE_OF_CONDUCT. Not one mention of the pipeline or the agents anywhere in these.
- M4a validators in CI: conformance check; `claude plugin validate <plugin>` per package, no
  --strict (extensions warning stays in the log); `skills-ref validate` per SKILL.md;
  `hermes plugins validate` + `hermes plugins doctor --ci`. Integration matrix on top.
- M4b evals: NONE. Owner will not run paid model tests. No evals/, no trigger tests.
- M5 (no choice): every reference named from SKILL.md by relative path with a "read when" condition;
  prose-discipline rules routing table gets real paths; toc-thinking names sources.md.
- M6 (no choice): TOC at top of every reference >100 lines except howp commands.md (release-written);
  generated by a ready-made tool (markdown-toc/doctoc) with a CI check.
- M7: imperative voice for all six skill descriptions ("Review a software design... Use when...");
  key use case first; `license: MIT` in all six SKILL.md front matters (prose-discipline gets it).
- M8 REFRAMED (owner): support of ALL declared harnesses is mandatory; prose-discipline MUST reach
  each harness by whatever documented mechanism that harness offers for always-on instructions;
  after install every agent MUST follow the standard; the plugin's job is to force compliance and
  give the agent suitable tools. No dropping of functionality. Options that remove a route are
  rejected. Needs per-harness research (06-*.md) before a design can be proposed.
- L1: drop `agent-skills` keyword from all six manifests.
- L2: rewrite the "Hermes ... Required." line within H5.
- L3: covered by the H2 README template.
- L4: rename skills by action (proposals for the spec: triz -> resolve-contradiction,
  design-review -> review-design, howp -> dashboard, toc-thinking -> thinking-processes,
  cognitive-load -> diagnose-load, prose-discipline -> write-prose). Names to be approved in spec.
- L5: absolutes in prose-discipline rules get their reason beside them; requirements not softened.
- L6: howp host list kept in one place, others reference it; which place decided with M9.
- Pending research 06-*: M8 (per-harness always-on mechanisms), then M9 (extensions content).
- NEW H9 (owner): howp is no longer a dashboard. Identity now: a forecasting tool — interests ->
  measurable questions -> prediction-market probabilities plus the agent's judgement -> a written
  forecast. Outcome scoring (Brier, the F1 pages in how-possible) is the owner's own end-to-end
  test of the predictor, not a product function; verification stays with the user and is not
  claimed by the package. Rewrite howp plugin.json description, root README row, README (new),
  SKILL.md description and body from this identity. Skill renamed `forecast` (L4).
  how-possible's own README still opens with "the page" — that is that repo's business.

## Filled after the 06-* research (proposed in the spec, awaiting owner review)
- M8: per-harness routes as specified in spec §5.5: Claude Code hooks (SessionStart +
  SubagentStart, plain stdout via sed, no node); Codex `extensions["com.openai"].hooks`
  (currently dropped upstream, skill catalogue is the live route); Oh-My-Pi `rules/*.md`
  with alwaysApply (existing route, confirmed from source); Hermes native plugin under
  `com.nousresearch.hermes/` with register_system_prompt_section, rules.md generated on CI.
  Owner decides: enforcement hook kind, TTSR files, Python under "text only", skill names.
- M9: prose paragraphs leave `extensions`; howp keeps a machine-readable hosts array as the
  single source (L6); Codex namespace is the only vendor extension.
- Reading order for the next session is in README.md of this folder.
- Skills may be split: a plugin may hold several skills; at plan time each skill is assessed and
  oversized/over-broad ones are split into several skills of the same plugin, names proposed to owner.
- Codex: design for the documented behaviour (hooks via extensions["com.openai"]), never for the
  upstream defect; the defect is recorded here only; CI's Codex hook assertion allowed-to-fail
  with the issue link until upstream closes it.
- Behavioural evals: deferred, not dropped. A human-filed issue (no police-report label) holds the
  requirements and sources; the owner will look at cost next week; if cheap enough, considered.

## Closed at the end of the session (no open questions remain)
- Claude Code enforcement: NONE. No blocking Stop/SubagentStop hook ("a harmful gate"), no
  UserPromptSubmit reminder (repetition is noise). SessionStart + SubagentStart injection only,
  re-injected where the client dropped it (compact/clear/resume).
- Oh-My-Pi: no TTSR rule files (same gate). rules/ with alwaysApply stays.
- Hermes: NO Python, no native plugin. README Hermes section and the first lines of the prose
  skill recommend `skills.auto_load`; Hermes surfaces it itself when the skill loads. Spike
  verifies the qualified-name form.
- Categories: howp Data & Analytics; prose-discipline Productivity; design-review,
  cognitive-load, toc-thinking, triz Developer Tools.
- Skill names, one word: forecast, contradiction, review, root-cause, load, prose.
- MANDATORY CLEANUP: docs/superpowers/ (spec, handoff, plans) is deleted after the work is done
  AND verified (acceptance met, CI green, owner confirmed), before merge.
