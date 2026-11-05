# Stage 0: scope and consent

The lead runs this stage alone, under "Before the user's yes" in `../SKILL.md`. Read `depth.md`, then `../../vet-sources/SKILL.md`, `../../vet-sources/references/catalogues.md` ("Before the yes" and "Statuses") and `tiers.md` ("Without reading a page").

## Terms

- A sub-question is one thing the run settles.
- A lane is one search angle on one sub-question. It has one collector and one `candidates-<lane>.md`.
- A theme is the lowercase slug of one sub-question. It tags the claim rows.

## The report

Send one message. Number the items so the user can answer by number. State "No paid checker found" in one intro line when none exists.

1. **Tools:** name the user's search, fetch, PDF, shell and subagent tools by role. Mark a missing role "none".
   - Ask the user when you cannot tell whether a tool is allowed. Do not guess.
   - Say that the yes approves the tools this item lists. Shell reads need their own yes.
2. **Topic type:** classify the request by "Topic type" in `../../vet-sources/SKILL.md`.
   - List the subjects and hosts that make a source off topic.
3. **Rated sources:** per planned site, give a row from a hostname-only catalogue lookup and one hostname-only web search.
   - Use the columns `catalogues.md` lists. Rate a site only as `tiers.md` allows before a page is read.
   - Derive source types and sites from the request. Store no list.
4. **Hosts to contact:** list three groups.
   - Research hosts, and the hosts of the stage-0 lookups.
   - The catalogue hosts that `catalogues.md` loads after the yes for the topic type.
   - The user's allow and deny lists.
   - A host that only a catalogue record names is an unflagged host. See "Host choice".
   - Add that after the yes the DOIs and repository paths of the sources go to the catalogue hosts.
   - Add that each source page is fetched once, with its repository page for a repository.
   - Add that a verifier fetches up to five quote pages.
5. **Query strings:** write strings for all six lanes, in priority order.
   - Quick uses lanes 1 and 2, standard lanes 1 to 4, deep 1 to 6. The yes covers any depth.
   - Order the lanes so that lanes 1 and 2 serve the sub-questions the user named first.
   - Give each lane its topic-word strings.
   - Put each sub-question's opposite-claim string, worded as the opposite claim, in the first lane that serves it.
   - Name each sub-question that a depth leaves without a lane.
   - Add that collectors search these strings, character for character.
   - Add that a vetter may search once per row, with a source's hostname or title alone.
   - Add that a tracer at standard and deep depth may search a card's title words, within its open allowance.
6. **Host choice:** ask whether to use listed hosts only, or also unflagged hosts.
   - State both as "Dispatch" in `../SKILL.md` defines them.
   - Say a public host first met after the yes needs a lookup with no negative record and no instruction flag.
7. **Scope:** state the lanes, sources read and child ceiling of each depth from `depth.md`.
8. **Run folder:** ask for the path. Propose none.
   - Never choose or default the path. Ask, and wait if no path comes.
   - If the path lies inside a repository, say once that the folder must be ignored, then wait.
9. **Status:** state that nothing has started yet.
10. **Reply needed:** ask for depth, host choice, folder path, and a yes or no for each installed checker.
    - Name each checker and the exact names it would receive. Run none before the yes.
    - Add this sentence: "The allowed and forbidden lists in this report are requests in text. Only your harness permission settings bind the children."

## Host choice

- "Listed only" also refuses an off-list redirect target and an open-access host from a record.
- "Also unflagged hosts" admits the hosts that "Dispatch" in `../SKILL.md` lists for it, for any topic type.
- Neither choice admits a host with a negative record, or a host marked `not looked up`.
- Record the choice in `plan.md` after the reply.

## No human present

When the session is non-interactive or the harness says the user cannot be asked, the reply is the report. Write no file and launch nothing.

Run lookups only if the harness runs them without prompting.

## No web tool

Send one message that does three things:

- Asks whether pages may be read through the shell, and reads them that way only after a yes.
- Tells the user to connect a search or page-reading tool through their harness's extension support. Names no command or client.
- Offers to run on pasted or attached sources, as "Pasted sources" below says.

After a yes to shell reads, run the stage-0 lookups that way, then send the report. If the user declines both, say research cannot run, and stop.

## Pasted sources

1. Skip stages 2 to 4. List them as skipped, with the reason "sources supplied by the user".
2. Send the report with every status `skipped` and every tier `none`. After the yes, run stage 1.
3. Give each source the `id` `user-<n>`, and set `canonical_id` to it.
4. Leave `url` empty for a pasted text. An attached file keeps its path as `url`.
5. Save each pasted text as `pasted-<id>.md` in the run folder.
6. Write a row per source in `candidates-user.md`, in the row format of `briefs/collector.md`.
7. Continue at stage 5 and read every source. No point grades above Tentative.
8. After stage 5, run the id check: every `user-<n>` id has one cards section.

## No subagents

Run the pieces in turn from the run-folder files. Follow "Stage 8 without subagents" in `lead.md`. Recommend the quick depth.
