# distilled-research

<!-- description:start -->

Vets sources, reads them in parallel, collapses copies to independent origins, and grades each claim by how many independent origins support it.

<!-- description:end -->

## Install

<!-- install:start -->

### Claude Code

```
/plugin marketplace add Akurganow/pegboard
/plugin install distilled-research@pegboard
```

Source: Claude Code documentation, <https://code.claude.com/docs/en/discover-plugins>. CI installs it on Ubuntu, macOS and Windows.

### Codex

```
codex plugin marketplace add Akurganow/pegboard --ref main
codex plugin add distilled-research@pegboard
```

Source: Codex documentation, <https://developers.openai.com/plugins/build/plugins>, for `marketplace add`; Codex source, [`plugin_cmd.rs`](https://github.com/openai/codex/blob/e3e5ad28470f6a225301518c30a66e749a880164/codex-rs/cli/src/plugin_cmd.rs), for `plugin add`. CI installs it on Ubuntu, macOS and Windows.

### Oh-My-Pi

```
omp plugin marketplace add Akurganow/pegboard
omp plugin install distilled-research@pegboard
```

Source: Oh-My-Pi documentation, [`docs/marketplace.md`](https://github.com/can1357/oh-my-pi/blob/a33cc26824e3c91edd9fa42d681f10dceb4ac2f0/docs/marketplace.md). CI installs it on Ubuntu, macOS and Windows.

### Hermes

```
hermes plugins install Akurganow/pegboard/plugins/distilled-research --no-enable
hermes plugins list
hermes plugins enable distilled-research
```

Keep the `plugins/distilled-research` suffix: without it Hermes copies the whole repository, and its [two-level scan](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/user-guide/features/plugins.md) finds no package.

Source: Hermes documentation, [`developer-guide/plugins/index.md`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/website/docs/developer-guide/plugins/index.md), for the commands; Hermes source, [`plugins_cmd.py`](https://github.com/NousResearch/hermes-agent/blob/a0ca7c19204e514f9590ce3b812e029b315ab9e9/hermes_cli/plugins_cmd.py) (`_resolve_git_url`), for the subdirectory form and what happens without it. CI installs it on Ubuntu and macOS.

### Cursor

Cursor's documentation names no command that installs from a repository. It names three routes:

- Public marketplace: open **Customize**, find the plugin, select **Install**. A plugin appears there only after Cursor reviews a submitted repository, and this repository claims no listing.
- Team marketplace, on Teams and Enterprise plans: in **Dashboard**, **Plugins & MCPs**, **Team Marketplaces**, select **Add Marketplace**, then **Import from Repo**, and paste `https://github.com/Akurganow/pegboard`. Developers then install from **Customize**.
- Local: copy `bundles/distilled-research` to `~/.cursor/plugins/local/distilled-research`, then restart Cursor or run **Developer: Reload Window**.

Source: Cursor documentation, [Plugins](https://cursor.com/docs/plugins), read 2026-11-04, for the three routes; [Plugins reference](https://cursor.com/docs/reference/plugins), read 2026-11-04, for the submission and review. CI does not install it.

### OpenClaw

```
openclaw plugins install distilled-research --marketplace Akurganow/pegboard
```

Source: OpenClaw documentation, [`docs/cli/plugins/install.md`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/docs/cli/plugins/install.md#L277-L283). OpenClaw reads this repository's `.claude-plugin/marketplace.json` (OpenClaw source, [`marketplace.ts`](https://github.com/openclaw/openclaw/blob/db6ac584cf205ea9a72de7ae83a4e65199b926a4/src/plugins/marketplace.ts#L35-L38)). CI does not install it.

### Kiro

No install command is given. Kiro's documentation says Powers follow the Agent Plugins specification, and `plugins/distilled-research/plugin.json` carries every field the documentation requires. The documentation does not say how Kiro finds several packages in one repository. CI does not install it.

Source: Kiro documentation, [Create a power](https://kiro.dev/docs/powers/create) and [Installation](https://kiro.dev/docs/powers/installation), read 2026-11-04.

<!-- install:end -->

## Usage

Ask a research question in your own words. Both skills trigger from the text of the request:

```text
Is it true that a monorepo helps a team ship faster than many repositories?
Read the sources in parallel and tell me which ones only repeat each other.
```

The `triangulate` skill fires on questions about what the evidence says: whether a claim is well supported, what many sources agree on, why studies contradict each other, or which sources copy one origin. It also fires on a survey of a field or an evidence review. For a single-fact lookup, a summary of one given page or a code search, ask directly.

The `vet-sources` skill fires when you ask whether a site, paper or repository can be relied on, or want a list of sources rated before you cite them. For install safety, malware scanning and licence checks, use the tool built for that.

### What triangulate asks first

Before the report, the agent sends only site hostnames, to Wikipedia and to a web search provider. Nothing else runs until you answer. The agent sends one numbered report, so you can reply by number. The report holds:

1. The search, fetch, PDF, file-read, shell and subagent tools it found, or "none" for a missing role. Without a file-read tool the run stops.
2. The topic type: practice/technology, science/health, news/facts or other.
3. One row per planned site: its status, the catalogue record as found, what others say about the site, the safety column, and a tier. Each row comes from a hostname-only catalogue lookup and one hostname-only web search.
4. The hosts it would contact: research hosts, catalogue hosts, and your allow and deny lists. After your yes, the DOIs and repository paths of the sources go to the catalogue hosts. For every topic type the report names `api.crossref.org` and `api.openalex.org`. A vetter fetches each source page once, with its repository page for a repository. A reader fetches each kept source up to three times.
5. The query strings of each lane, written for the lanes of every depth in priority order. The first lane that serves a sub-question also gets its string worded as the opposite claim. The report names any sub-question a depth leaves without a lane. Collectors search these strings character for character. A vetter may search once per row, with a source's hostname or title alone. A tracer at standard and deep depth may search a card's title words to find a cited origin.
6. A choice: listed hosts only, or also unflagged hosts.
7. The scope of each depth: lanes, sources read and a ceiling on child agents.
8. A question for the run-folder path. The agent proposes none.
9. A statement that nothing has started yet.
10. The reply it needs: depth, host choice, folder, and a yes or no for each installed paid checker, named with the exact names it would receive. With none installed, the report says so in its intro.

The agent waits for your answer before it starts a child, writes a folder or runs a paid checker. Your yes covers only the depth, hosts, checkers, query strings and folder you named, and the lookups the report names. A change needs a new yes.

[`depth.md`](skills/triangulate/references/depth.md) gives the lanes, rows and child ceiling of the quick (recommended), standard and deep (on request only) depths. At most four children run at once. Every depth reads the kept tier A or B primary sources, never tier C commentary, up to its child ceiling. The rest are listed as not read.

### What happens after your yes

1. Collectors search each lane with its approved query strings and its opposite-claim string, and fetch nothing.
2. Vetters check DOIs and repository paths in the catalogues, search once per source with its hostname or title alone, and rate each source. A retracted source, or one with a retraction or expression-of-concern notice, is excluded.
3. Readers fetch the primary text of the kept sources. On a blocked page a reader tries the open-access copy that the OpenAlex record names, once, and only if you chose "also unflagged hosts".
4. At standard and deep depth, tracers follow each claim to its origin and collapse copies into one independent origin. Quick depth opens no origin: the lead traces from the cards, and a claim traced only through an unread cited origin stays Not established.
5. The lead grades each point, and a fresh verifier rechecks the counts and fetches up to five quotes of the top points on approved hosts.

### What the reply holds

The reply opens with a direct answer: an opening sentence, up to four sentences on the directions that bear on it, and a closing caveat. The answer names the question when the answer is "it depends". A legend and a table of points follow. Each row shows a grade, the counts, the evidence and the strongest dissent.

- **Grades:** Established, Probable, Tentative, Not established, and Contested, which stands outside the ladder. [`origins-and-grades.md`](skills/triangulate/references/origins-and-grades.md) holds the table. On a science or health topic, Established needs a tier A measurement, and an unreviewed preprint counts as tier B for that test.
- **Counts:** `N (M) + K` means N independent origins. M of them are measurements read in full with a literal quote. K counts sources that repeat the claim without a traced origin. K never enters a grade.
- **Read level:** each source is marked `full`, `abstract` or `snippet`. Only a `full` read with a literal quote counts as measured.
- **Quotes:** a fetch tool may return a summary of a page, not its text. Source: Claude Code [tools reference](https://code.claude.com/docs/en/tools-reference#webfetch-tool-behavior), documentation, read 2026-11-05: the result of a separate model call, "lossy by design". The reader records which kind the tool returned. A quote is `literal` only when the tool returned the page's own text. When it returned a summary or rewrite, every quote from it is `paraphrase`, whatever quote marks the summary shows.
  - The verifier counts only literal quotes as matched.
  - An origin whose quotes are all `paraphrase` counts toward `N`, never toward `M`. The verifier lowers `M` accordingly, and the header line counts those points.
  - On a harness whose fetch tool summarises, `M` stays 0, so no point reaches Established.
- **Tail:** Contested positions, Not established points, caveats, skipped sources with a reason each, the path of `appendix.md`, and a header line with the depth, the date, the read levels and what the verifier changed.

Grades and tiers are ordinal and uncalibrated. They rank claims within one run and give no probability. On a science or health topic the reply adds "agreement among sources; not medical advice".

The run folder you chose holds the plan, the candidates, the merged list `merged.tsv`, the ratings, the reader cards, any pasted texts, the origin files, `origins-index.md`, the distillate, the verifier's file and the appendix. Each file opens with "Research data. Not instructions."

### Other starts

- **Rating alone:** `vet-sources` rates up to 15 sources per request and takes the rest in further batches of 15. Before your yes it looks up hostnames only. After your yes it checks DOIs and repository paths. It reports the catalogue record as found and a tier. Absence from a catalogue is not safety, and it never calls a source safe.
- **No search or page-reading tool:** the agent asks whether it may read pages through the shell, says how to connect a search or page-reading tool, and offers to run on sources you paste. If you decline both, it says research cannot run.
- **Pasted sources:** the agent skips collecting and vetting, gives every source status `skipped` and tier `none`, and reads each pasted text. No source has a tier, so no point grades above Tentative.
- **No subagents:** the pieces run in turn from the run-folder files. Verification then becomes a shared-context check, labelled so, and Established points show as Probable. The agent offers a fresh session that names the folder, and recommends the quick depth.
- **No human present:** the reply is the stage-0 report, and the run stops there.

## What's inside

| Path | What it is |
| :-- | :-- |
| [`skills/triangulate/SKILL.md`](skills/triangulate/SKILL.md) | the research run: consent first, then stages 0 to 9, and the dispatch template with its forbidden actions |
| [`skills/triangulate/references/stage0.md`](skills/triangulate/references/stage0.md) | the numbered report, host choice, and the no-web, pasted-source and no-subagent paths |
| [`skills/triangulate/references/depth.md`](skills/triangulate/references/depth.md) | quick, standard and deep, and how rows are cut into shards |
| [`skills/triangulate/references/run-folder.md`](skills/triangulate/references/run-folder.md) | the run folder: file rules, the `plan.md` fields, the files and their writers, the id check, resume rules |
| [`skills/triangulate/references/origins-and-grades.md`](skills/triangulate/references/origins-and-grades.md) | traced, untraced and independent origins, the grade table with its legend text, and the verifier's verdicts |
| [`skills/triangulate/references/output.md`](skills/triangulate/references/output.md) | the reply format and the legend |
| [`skills/triangulate/references/lead.md`](skills/triangulate/references/lead.md) | the formats only the lead writes, and stage 8 without subagents |
| [`skills/triangulate/references/briefs/collector.md`](skills/triangulate/references/briefs/collector.md) | the brief for the child that lists candidates for one lane, with its row format |
| [`skills/triangulate/references/briefs/reader.md`](skills/triangulate/references/briefs/reader.md) | the brief for the child that reads sources and writes cards |
| [`skills/triangulate/references/briefs/tracer.md`](skills/triangulate/references/briefs/tracer.md) | the brief for the child that traces origins for one theme |
| [`skills/triangulate/references/briefs/verifier.md`](skills/triangulate/references/briefs/verifier.md) | the brief for the fresh child that rechecks the distillate |
| [`skills/vet-sources/SKILL.md`](skills/vet-sources/SKILL.md) | the rating skill, in two phases: hostnames before your yes, DOIs and repository paths after. It holds the data rule and the topic types |
| [`skills/vet-sources/references/catalogues.md`](skills/vet-sources/references/catalogues.md) | the catalogues by phase, their routes and terms, the statuses, and the lookup rules |
| [`skills/vet-sources/references/tiers.md`](skills/vet-sources/references/tiers.md) | tiers A, B and C, their legend text, and what moves a source between them |
| [`skills/vet-sources/references/briefs/vetter.md`](skills/vet-sources/references/briefs/vetter.md) | the brief for the child that vets a shard of sources, with the vet row format |
| `plugin.json` in `plugins/distilled-research/`; `.claude-plugin/`, `.codex-plugin/` and `.cursor-plugin/` manifests in `bundles/distilled-research/` | the Agent Plugins 1.0.0 manifest in the first build, one manifest per client in the second |
| [`LICENSE`](LICENSE) | the MIT license |

The package is instructions and reference text. The agent runs the research with the tools your session already has.

## Requirements and network

**Tools.** Research needs a search tool, a page-reading tool and a file-read tool. A PDF reader helps with papers. Subagents are optional: without them the pieces run in turn. The agent uses the shell to read pages only after you say yes, and never uses it to read or join run files. The package needs no runtime, key or account, and the agent holds and reads no key.

**Catalogues.** The package lists a catalogue only if it is public without a key or an account. Each entry cites the pages that state its access terms or data licence, the day each was read, and what they state. The agent reads one record per lookup and marks a bot check or a 403 as an error. Four catalogues are listed.

- **Wikipedia Perennial Sources**, host `en.wikipedia.org`. It is the one catalogue with a hostname route, so it answers before your yes. It also answers after.
  - Search: `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="<host>" prefix:"Wikipedia:Reliable sources/Perennial sources"&srlimit=2&format=json`, with the host written without `www.`
  - Read one subpage: `https://en.wikipedia.org/w/index.php?title=<subpage>&action=raw`
  - The list records how Wikipedia editors rate a source's reliability ([page](https://en.wikipedia.org/wiki/Wikipedia:Reliable_sources/Perennial_sources), read 2026-11-05). It is no safety rating.
  - Terms: Wikimedia [robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy), read 2026-11-05, which asks a bot to identify itself in its User-Agent header; see also the [Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use), section 12, read 2026-11-05. The agent uses its tool's own client and invents no personal contact.
- **Crossref REST API, with Retraction Watch data**, host `api.crossref.org`. It runs after your yes, by DOI, for every topic type. Tracers also look up the DOI of each origin they open.
  - Route: `https://api.crossref.org/v1/works?filter=updates:<doi>&rows=20&cursor=*`, then each returned `next-cursor` while a page is full ([pagination](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/), read 2026-11-06). The filter `updates` means "Is an update to the given DOI", and `update-type` names a correction or retraction ([filter table](https://www.crossref.org/documentation/retrieve-metadata/rest-api/rest-api-filters/), read 2026-11-05). A returned record is an update notice. A record from the Retraction Watch database has `"source":"retraction-watch"` ([documentation](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/), read 2026-11-05).
  - Terms: [access terms](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/), read 2026-11-05. The [Retraction Watch in Crossref](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/) page, read 2026-11-05, describes the data and states no usage terms.
- **OpenAlex**, host `api.openalex.org`. It runs after your yes, by DOI, for every topic type.
  - Route: `https://api.openalex.org/works/doi:<doi>?select=id,is_retracted,open_access`. A true `is_retracted` counts as a retraction notice. The `open_access.oa_url` field may be a landing page, a PDF or null (field seen in a returned work record, 2026-11-05).
  - Terms: [authentication](https://help.openalex.org/api/authentication/), read 2026-11-05, says basic queries need no key, at 10 requests per second. [About](https://openalex.org/about), read 2026-11-05, says the data is CC0. Neither page states terms of use for the API.
- **OpenSSF Scorecard**, host `api.scorecard.dev`. It runs after your yes, by repository path, on practice/technology topics.
  - Route: `https://api.scorecard.dev/projects/github.com/<owner>/<repo>`, for `github.com` repositories only. Other hosts read "not checked".
  - Terms: [README, section "Scorecard REST API"](https://github.com/ossf/scorecard/blob/e73dbc5037aa4940d567e4878d50a7f524f30f08/README.md), read 2026-11-05, states the data licence, CDLA Permissive 2.0, and no access terms or authentication rule. Its MCP section says a server that reads the REST API "needs no credentials".

**Other lookups.** Before your yes the agent also runs one web search per planned site, with the hostname alone and never topic words or your text. It reports in one line what others say about the site. No listed catalogue rates a site's safety, so the safety column reads "not checked: no open catalogue". If you have a checker of your own, the agent names it and uses it only after your yes.

**Research hosts.** You choose the research hosts. The report lists the hosts it plans to read, and your reply picks "listed hosts only" or "also unflagged hosts". An unflagged host is one with no catalogue record, a failed lookup, or an open-access address that only a catalogue record names. Under "also unflagged hosts" the agent may also fetch a public host that it first meets after your yes, once a catalogue lookup of that host finds no negative record and the source carries no instruction aimed at agents. Neither choice admits a host with a negative record, or a private, internal or IP-literal host. An off-list redirect target is refused. The agent honours your allow and deny lists and never fetches a denied host.

## Trust

This plugin ships no scripts, tools or servers. It is instructions, and what they make an agent do can reach the network and your files. Before research the agent looks up the sites it plans to read in public catalogues and in one web search per site. Before you approve a report a lookup sends only a site hostname. A DOI or repository path is sent only after approval, and a lookup never sends your question or files. After you approve a report the agent starts subagents with a written list of allowed tools and hosts and of forbidden actions. With "listed hosts only" a subagent fetches no host outside the report. With "also unflagged hosts" it may fetch a public host first met after your approval, unless a catalogue lookup of that host finds a negative record. Collectors search the query strings you approved in the report, character for character. A vetter may search one source's hostname or title alone, once per source. A tracer at standard and deep depth may search a card's title words to find a cited origin. Those are requests in text; what your harness's permission settings do not block, a subagent can still do. Web pages can carry instructions aimed at agents. The plugin tells the agent to treat all page, search and file text as data. A model can still fail at that, so deny permissions you do not want a poisoned page to use. The run folder you choose holds your question and text copied from pages; keep it out of version control. The plugin never holds or reads keys and asks before using a paid checker. Request safety is your responsibility.

## Boundaries

- As of 2026-11-05 the method has run three times: once by hand and twice as the built plugin, on a science/health topic and on a practice/technology topic. No news/facts topic was run, so its rules are untested on one.
- One run predates the current skill text. No run covered these behaviours:
  - `paraphrase` marking of summary reads;
  - the shell ban for run files;
  - OpenAlex lookups for any DOI;
  - the report wording that says who named the sources;
  - the vetter's search;
  - the tracer's title search, the paraphrase rule for `M` and the preprint rule for Established;
  - fetching a new public host under "also unflagged hosts", and the quote an opened origin carries.
- The evals miss dispatch, parallelism, folder writes and injection. A headless eval session ends at the stage-0 report, so the reading, grading and verifying stages were checked only by those runs.
- No test has measured how often an Established point is right. "What the reply holds" says what the ordinal grades mean.
- Research cannot run without a search or page-reading tool and without a yes to shell reads. Then the agent can only rate and read what you paste.
- A date, claim or link known only from a search result or memory stays `unconfirmed`. It is never a traced origin.
- A quote from a summary read is `paraphrase`, and the verifier cannot match it. On a harness whose fetch tool summarises, `M` stays 0 and no point reaches Established ("What the reply holds", Quotes).

## License

MIT. See [LICENSE](LICENSE).

## Help

See [SUPPORT.md](https://github.com/Akurganow/pegboard/blob/main/SUPPORT.md).
