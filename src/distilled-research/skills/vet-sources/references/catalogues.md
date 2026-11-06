# Catalogues

An entry is listed only if it is public without key or account. Each entry cites the pages that state its access terms or data licence, the date each was read, and what they state. An entry with no such page is dropped. The plugin holds no key and reads none. A standalone `vet-sources` reply uses the same two phases: before the yes and after the yes.

## Before the yes

### Hostname rule

1. Send a public site hostname and nothing else.
2. Never send user text, file contents, repository paths or DOIs.
3. Give a host that the `not looked up` status covers that status, and look nothing up.
4. Look up DOIs and repository paths after the yes, and say so in the report.

### Wikipedia Perennial Sources

Host `en.wikipedia.org`. It is the only catalogue with a hostname route. Search with the host written without `www.`: `https://en.wikipedia.org/w/api.php?action=query&list=search&srsearch="<host>" prefix:"Wikipedia:Reliable sources/Perennial sources"&srlimit=2&format=json`, then read one subpage with `https://en.wikipedia.org/w/index.php?title=<subpage>&action=raw`. Read the subpage whose text lists the hostname. With no such subpage the status is `no-record`. It means the search found no subpage naming the host. It is no proof that the list holds none.

Terms: [robot policy](https://wikitech.wikimedia.org/wiki/Robot_policy), read 2026-11-05; see also [Terms of Use](https://foundation.wikimedia.org/wiki/Policy:Terms_of_Use) section 12. The robot policy asks a bot to identify itself in its User-Agent header. Use the harness's own client and never invent a personal contact.

### Lateral-reading search and report columns

Report one row per site with the columns: site, status, record as found, what others say, safety, tier. Take the tier from "Without reading a page" in `tiers.md`.

No open catalogue rates a site's safety. For each planned site, run one web search for its hostname alone, never topic words or user text. Report in one line what others say about the site. A site with no outside mention reads "no mention found". The safety column reads "not checked: no open catalogue". If the user has tools of their own, name them to the user (see paid checkers).

## Statuses

| Status | Meaning |
| :-- | :-- |
| `listed` | The catalogue returned a record. Show it as found, with the catalogue name. |
| `no-record` | The catalogue answered and holds no record. |
| `error(code)` | The call failed with this code, such as 400 or 403. |
| `skipped` | The harness refused the call, or no tool was available. |
| `not looked up` | The host is private, internal, intranet or an IP literal. |

Absence is never "safe". A `no-record` or `error(code)` says nothing about safety. A site no listed catalogue covers reads "not checked". A negative record is a `listed` entry that rates the host unreliable, deprecated or blacklisted. A `no-record` from Crossref or OpenAlex does not prove a paper is not retracted: Crossref omits a Retraction Watch record that has no notice DOI.

## After the yes

| Catalogue | Host | Route (DOI or repository path) | Terms read |
| :-- | :-- | :-- | :-- |
| Crossref REST API, with Retraction Watch data | `api.crossref.org` | `https://api.crossref.org/v1/works?filter=updates:<doi>&rows=20&cursor=*`; read each next page with the returned `next-cursor` until a page holds fewer than 20 records ([pagination](https://www.crossref.org/documentation/retrieve-metadata/rest-api/tips-for-using-the-crossref-rest-api/), read 2026-11-06); the filter `updates` means "Is an update to the given DOI", and `update-type` names a correction or retraction ([filter table](https://www.crossref.org/documentation/retrieve-metadata/rest-api/rest-api-filters/), read 2026-11-05). A returned record is an update notice. A record from the Retraction Watch database has `"source":"retraction-watch"` ([documentation](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/), read 2026-11-05). Do not download the full file | [access terms](https://www.crossref.org/documentation/retrieve-metadata/rest-api/access-and-authentication/), read 2026-11-05; [Retraction Watch in Crossref](https://www.crossref.org/documentation/retrieve-metadata/retraction-watch/), read 2026-11-05, describes the data and states no usage terms |
| OpenAlex | `api.openalex.org` | `https://api.openalex.org/works/doi:<doi>?select=id,is_retracted,open_access`; `is_retracted` true counts as a retraction notice. Write `open_access.oa_url` in `record` as `oa_url: <url>`. It may be a landing page, a PDF or null (field seen in a returned work record, 2026-11-05) | [authentication](https://help.openalex.org/api/authentication/), read 2026-11-05: basic queries need no key, at 10 requests per second; [About](https://openalex.org/about), read 2026-11-05: the data is CC0. Neither page states terms of use for the API |
| OpenSSF Scorecard | `api.scorecard.dev` | `https://api.scorecard.dev/projects/github.com/<owner>/<repo>`; for `github.com` repositories only. Any other host reads "not checked" | [README, section "Scorecard REST API"](https://github.com/ossf/scorecard/blob/e73dbc5037aa4940d567e4878d50a7f524f30f08/README.md), read 2026-11-05: the data licence is CDLA Permissive 2.0; the section states no access terms and no authentication rule. The MCP section says a server that reads the REST API "needs no credentials" |

Every route above takes a DOI or a repository path. The Wikipedia route runs again only for a host not looked up before the yes.

Entries by topic type:

- Every topic type: Wikipedia Perennial Sources, and Crossref and OpenAlex for every source with a DOI.
- practice/technology: add OpenSSF Scorecard.

## Lookup rules

- Look up one DOI or repository per call. Read the Crossref route to its last page. Never load a whole list or a bulk file.
- Never turn an error into `no-record`.
- A refusal by the harness sets `skipped`. Do not retry through another route.
- Do not work around a bot check or a 403 on a catalogue route. Mark it `error(403)` and move on.

## User lists and paid checkers

- Honour a user's allow and deny lists. Never fetch a denied host. An allowed host skips no check.
- Show both lists in the report. The plugin holds no list.
- Name each paid checker the user has installed, and the exact names it would receive, in the report or reply.
- Use a checker only after the user says yes to it. This file names no paid checker.
