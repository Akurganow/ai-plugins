# 05: What makes docs work for readers, and skills work for agents

Clean-room research, 2026-09-24. I read only the web. I did not open any local repository and did not run `git`.
Fetches used `curl` through the session proxy with its CA bundle; `WebFetch` and `WebSearch` were used as fallbacks.
The fetched text is kept under `research/raw/` next to this file.

**How to read the citations.** A quote is copied from the fetched text. Where a page came from a GitHub raw copy
(`raw.githubusercontent.com/.../main/...`), the branch is `main` as fetched on 2026-09-24. I could not get the commit SHA,
because the GitHub REST API answers `"GitHub access to this repository is not enabled for this session"` and `git` was not allowed.
Treat those citations as branch-dated, not commit-pinned.

---

## 0. Sources and whether I could reach them

### Reached and read

| # | Source | URL actually read | Result |
|:-:|:--|:--|:--|
| A1 | Diátaxis, *Start here* | https://diataxis.fr/start-here/ | 200 |
| A2 | Diátaxis, *Tutorials* | https://diataxis.fr/tutorials/ | 200 |
| A3 | Diátaxis, *How-to guides* | https://diataxis.fr/how-to-guides/ | 200 |
| A4 | Diátaxis, *Reference* | https://diataxis.fr/reference/ | 200 |
| A5 | Diátaxis, *Explanation*, *Compass*, *Quality*, *Application*, *How to use* | https://diataxis.fr/explanation/ · /compass/ · /quality/ · /application/ · /how-to-use-diataxis/ | 200 |
| A6 | Google dev docs style guide, *Highlights* | https://developers.google.com/style/highlights | 200 |
| A7 | Google, *Headings* / *Lists* / *Tables* / *Procedures* / *Link text* / *Sentence structure* / *Voice* | https://developers.google.com/style/{headings,lists,tables,procedures,link-text,sentence-structure,voice} | 200 each |
| A8 | Google, *Accessibility* | https://developers.google.com/style/accessibility | 200 |
| A9 | Google, *Write for a global audience* | https://developers.google.com/style/translation | 200 |
| A10 | Google, *Timeless documentation* | https://developers.google.com/style/timeless-documentation | 200 |
| A11 | Microsoft Writing Style Guide: *Scannable content*, *Headings*, *Lists*, *Tables*, *Top 10 tips* (the site is blocked, so I read the publisher's source repo) | https://raw.githubusercontent.com/MicrosoftDocs/microsoft-style-guide/main/styleguide/{scannable-content/index.md, scannable-content/headings.md, scannable-content/lists.md, scannable-content/tables.md, top-10-tips-style-voice.md} | 200 each |
| A12 | standard-readme spec | https://raw.githubusercontent.com/RichardLitt/standard-readme/main/spec.md | 200 |
| A13 | Write the Docs, *A beginner's guide to writing documentation* (includes a README template) | https://www.writethedocs.org/guide/writing/beginners-guide-to-docs/ | 200 |
| A14 | GitHub Docs, *About the repository README file* | https://docs.github.com/en/repositories/managing-your-repositorys-settings-and-features/customizing-your-repository/about-readmes | 200 |
| A15 | GitHub Docs, *Creating a default community health file* | https://docs.github.com/en/communities/setting-up-your-project-for-healthy-contributions/creating-a-default-community-health-file | 200 |
| A16 | GitHub Docs, community profiles, security policy, and contributor guidelines | .../about-community-profiles-for-public-repositories · https://docs.github.com/en/code-security/getting-started/adding-a-security-policy-to-your-repository · .../setting-guidelines-for-repository-contributors | 200 each |
| A17 | Make a README, the project's own README only | https://raw.githubusercontent.com/dguo/make-a-readme/main/README.md | 200. It only describes the site; the site's content was not reached (see below). |
| B1 | Anthropic, *Skill authoring best practices* | https://docs.claude.com/en/docs/agents-and-tools/agent-skills/best-practices.md → redirected to https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices.md | 200 |
| B2 | Anthropic, *Agent Skills overview* | https://platform.claude.com/docs/en/agents-and-tools/agent-skills/overview.md | 200 |
| B3 | Anthropic, *Prompting best practices*. The old "be clear and direct", "XML tags", "multishot", and "long context tips" URLs all redirect here. | https://platform.claude.com/docs/en/build-with-claude/prompt-engineering/claude-prompting-best-practices.md | 200 |
| B4 | Claude Code docs, *Skills* | https://code.claude.com/docs/en/skills.md | 200 |
| B5 | Claude Code docs, *Memory* (CLAUDE.md / AGENTS.md) | https://code.claude.com/docs/en/memory.md | 200 |
| B6 | Claude Code docs, *Hooks* (security section) and *Discover plugins* | https://code.claude.com/docs/en/hooks.md · https://code.claude.com/docs/en/discover-plugins.md | 200 |
| B7 | Anthropic engineering blog, *Equipping agents for the real world with Agent Skills* | https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills | 200 |
| B8 | Anthropic engineering blog, *Effective context engineering for AI agents* | https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents | 200 |
| B9 | anthropics/skills, `skill-creator/SKILL.md` | https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md | 200 |
| B10 | Agent Skills specification | https://agentskills.io/specification.md | 200 |
| B11 | agentskills.io, *Best practices for skill creators* | https://agentskills.io/skill-creation/best-practices.md | 200 |
| B12 | agentskills.io, *Optimizing skill descriptions* | https://agentskills.io/skill-creation/optimizing-descriptions.md | 200 |
| B13 | agentskills.io, *Using scripts in skills* | https://agentskills.io/skill-creation/using-scripts.md | 200 |
| B14 | openai/skills, `skill-creator/SKILL.md` (Codex's own skill-authoring skill) | https://raw.githubusercontent.com/openai/skills/main/skills/.system/skill-creator/SKILL.md | 200 |
| B15 | agents.md, the site's source: README plus the `WhySection`, `HowToUseSection`, and `FAQSection` components (the site is blocked) | https://raw.githubusercontent.com/agentsmd/agents.md/main/{README.md, components/WhySection.tsx, components/HowToUseSection.tsx, components/FAQSection.tsx} | 200 each |
| B16 | GitHub Docs, *Adding repository custom instructions for Copilot* | https://docs.github.com/en/copilot/how-tos/configure-custom-instructions/add-repository-instructions → redirected to .../copilot-on-github/customize-copilot/add-custom-instructions/add-repository-instructions | 200 |
| B17 | GitHub Docs, Copilot tutorial on custom instructions for code review | https://docs.github.com/en/copilot/tutorials/use-custom-instructions → redirected to https://docs.github.com/en/copilot/tutorials/customize-code-review | 200 |
| B18 | OWASP Top 10 for LLM Applications 2025, LLM01 *Prompt Injection* (the site is blocked, so I read the project's source repo) | https://raw.githubusercontent.com/OWASP/www-project-top-10-for-large-language-model-applications/main/2_0_vulns/LLM01_PromptInjection.md | 200 |
| B19 | Chroma, *Context Rot*, the replication repo README only (the report is blocked) | https://raw.githubusercontent.com/chroma-core/context-rot/master/README.md | 200 |

### Blocked or not found (quoted replies)

| Source wanted | URL tried | What the environment answered |
|:--|:--|:--|
| NN/g, F-shaped pattern | https://www.nngroup.com/articles/f-shaped-pattern-reading-web-content/ | curl: `CONNECT tunnel failed, response 403`; WebFetch: `{"error_type":"EGRESS_BLOCKED","domain":"www.nngroup.com","message":"Access to www.nngroup.com is blocked by the network egress proxy."}` |
| NN/g, *How users read on the web* | https://www.nngroup.com/articles/how-users-read-on-the-web/ | `CONNECT tunnel failed, response 403` |
| NN/g 1997 copy at GMU | https://chnm.gmu.edu/digitalhistory/links/pdf/chapter4/4.17c.pdf | `CONNECT tunnel failed, response 403` |
| Make a README (site) | https://www.makeareadme.com/ | curl 403; WebFetch `EGRESS_BLOCKED ... www.makeareadme.com`. The site's source is not at `index.html` or at any of the `src/pages/*` paths I tried on `raw.githubusercontent.com` (all `404`). Wayback Machine: `403`. |
| Art of README | https://raw.githubusercontent.com/hackergrrl/art-of-readme/{master,main,HEAD}/README.md, the same under `noffle/`, and the npm registry | raw: `404: Not Found` on every branch; github.com: 403; npm: `{"error":"Not found"}` |
| Microsoft Style Guide (site) | https://learn.microsoft.com/en-us/style-guide/scannable-content/ | `EGRESS_BLOCKED ... learn.microsoft.com`. **I read the source repo instead (A11).** |
| OpenAI Codex, AGENTS.md guide | https://developers.openai.com/codex/guides/agents-md | `EGRESS_BLOCKED ... developers.openai.com`. The repo stubs `openai/codex/main/docs/agents_md.md` and `docs/skills.md` only link back to that blocked site. |
| OpenAI Codex, Skills docs | https://developers.openai.com/codex/skills | `CONNECT tunnel failed, response 403` |
| agents.md (site) | https://agents.md/ | `403`. **I read the source repo instead (B15).** |
| Cursor rules docs | https://cursor.com/docs/context/rules · https://docs.cursor.com/context/rules | curl 403; WebFetch `EGRESS_BLOCKED ... docs.cursor.com`. No public source copy was found. **Cursor guidance is not covered.** |
| arXiv papers: *Evaluating AGENTS.md* (2602.11988), *Agent Skills in the Wild* (2601.10338), *Lost in the Middle* (2307.03172), *IFScale* (2507.11538), *Agent Skill Security* (2607.13987) | https://arxiv.org/abs/... · export.arxiv.org · Semantic Scholar API · alphaxiv · openreview · huggingface · aclanthology | Every one: `CONNECT tunnel failed, response 403`; WebFetch on arXiv: `EGRESS_BLOCKED ... arxiv.org` |
| Chroma *Context Rot* report | https://research.trychroma.com/context-rot | `403` |
| OWASP site | https://genai.owasp.org/llmrisk/llm01-prompt-injection/ | `403`. **I read the source repo instead (B18).** |
| Snyk *ToxicSkills* | https://snyk.io/blog/toxicskills-malicious-ai-agent-skills-clawhub/ | `403` |
| GOV.UK content design, digital.gov plain language | https://www.gov.uk/guidance/content-design/writing-for-gov-uk · https://digital.gov/guides/plain-language/ | `403` each |
| Codex `project_doc_max_bytes` in source | https://raw.githubusercontent.com/openai/codex/main/codex-rs/core/src/project_doc.rs | `404` (the path has moved; not pursued further) |

**Search snippets only. I did not read these, and nothing below rests on them as a rule.**

- WebSearch summaries say that NN/g found *"79 percent of their test users always scanned any new page ...; only 16 percent read word-by-word"*.
- They say Gloaguen et al., *Evaluating AGENTS.md* (arXiv 2602.11988), found that context files *"do not generally improve task success rates, while increasing inference cost by over 20%"*.
- They say *Agent Skills in the Wild* (arXiv 2601.10338) found *"26.1% of skills contain at least one vulnerability"* and that script-bundling skills are *"2.12x more likely"* to contain one.
- They say Codex's `project_doc_max_bytes` defaults to 32 KiB and silently truncates AGENTS.md beyond it.

These are leads, not findings. **The research-backed claims about context rot, lost-in-the-middle, and instruction-count scaling rest here only on what Anthropic's own blog (B8) and prompting guide (B3) state. The primary papers were not read.**

---

## Part A: docs for the person deciding whether to install and how

### A.1 Separate the kinds of documentation (Diátaxis)

- The four kinds: *"there are fundamentally four identifiable kinds of documentation, that respond to four different needs. The four kinds are: tutorials, how-to guides, reference and explanation. Each has a different purpose, and needs to be written in a different way."* (A1)
- The compass, quoted from A1:
  - *"tutorials and how-to guides are concerned with what the user does (action)"*
  - *"reference and explanation are about what the user knows (cognition)"*
  - *"tutorials and explanation serve the acquisition of skill (the user's study)"*
  - *"how-to guides and reference serve the application of skill (the user's work)"*
- Mixing the kinds is the main failure: *"Crossing or blurring the boundaries described in the map is at the heart of a vast number of problems in documentation."* (A1)
- How-to guides:
  - *"Maintain focus on that goal. … Anything else that's added distracts … Typically, the temptations are to explain or to provide reference for completeness. … They get in the way of the action; if they're important, link to them."* (A3)
  - Titles: *"Choose titles that say exactly what a how-to guide shows."* The bad example given is *"Integrating application performance monitoring (maybe the document is about how to decide whether you should, not about how to do it)"*. (A3)
  - Language: *"Use conditional imperatives."* (A3)
- Reference:
  - *"Describe and only describe"* and *"austere and uncompromising"*. *"It can be tempting to introduce instruction and explanation … Instead, link to how-to guides, explanation and introductory tutorials."* (A4)
  - *"Reference material is useful when it is consistent. … place the material that your user needs where they expect to find it, in a format that they are familiar with."* (A4)
  - The language of reference: *"State facts about the machinery and its behaviour. List commands, options, operations, features, flags, limitations, error messages, etc."* (A4)
- Tutorials:
  - *"Every step the learner follows should produce a comprehensible result, however small."* (A2)
  - *"Ruthlessly minimise explanation … provide a link or reference to that explanation"*. (A2)
  - *"Ignore options and alternatives"*. (A2)
- Two kinds of quality: accuracy, completeness, consistency, usefulness, and precision are *"functional quality"* and can be checked. *"having flow"* and *"anticipating the user"* are *"deep quality"* and *"cannot be checked"* the same way. (A5, *Quality*)
- **Diátaxis says nothing about READMEs as such.** None of the pages I fetched covers a README or landing page; a grep for `readme`, `landing page`, and `overview` came back empty. Anything about README orientation below comes from A11–A15, not Diátaxis.

### A.2 README content, order, and length

- **GitHub says what a README is for.** *"A README is often the first item a visitor will see … README files typically include information on:"* (A14)
  - *"What the project does"*
  - *"Why the project is useful"*
  - *"How users can get started with the project"*
  - *"Where users can get help with your project"*
  - *"Who maintains and contributes to the project"*
- GitHub caps the README's scope: *"A README should only contain information necessary for developers to get started using and contributing to your project. Longer documentation is best suited for wikis."* (A14)
- Rendering limit: *"When your README is viewed on GitHub, any content beyond 500 KiB will be truncated."* (A14)
- Relative links: *"Relative links are easier for users who clone your repository. Absolute links may not work in clones of your repository - we recommend using relative links to refer to other files within your repository."* (A14)
- **standard-readme gives the section order as a MUST.** *"Sections must appear in order given below."* (A12). The order is:
  - Title, Banner, Badges
  - Short Description, Long Description
  - Table of Contents
  - Security, Background
  - Install, Usage
  - Extra Sections, API
  - Maintainers, Thanks
  - Contributing, License
- standard-readme's Short Description rules (A12):
  - *"Must be less than 120 characters."*
  - *"Must not have its own title."*
  - *"Must match the description in the packager manager's `description` field."*
  - *"Must match GitHub's description (if on GitHub)."*
- standard-readme's Long Description (A12), quoting perlmodstyle: *"someone who's slightly familiar with your module should be able to refresh their memory without hitting "page down". As your reader continues through the document, they should receive a progressively greater amount of knowledge."*
- Table of Contents: *"Required; optional for READMEs shorter than 100 lines"*. It *"Must link to all sections in the file."* (A12)
- Install: *"Code block illustrating how to install."* The `Dependencies` subsection is *"Required if there are unusual dependencies or dependencies that must be manually installed."* (A12)
- Usage: *"Code block illustrating common usage."* The `CLI` subsection is *"Required if CLI functionality exists."* (A12)
- Contributing (A12):
  - *"State where users can ask questions."*
  - *"State whether PRs are accepted."*
  - Suggestion: *"Link to a Code of Conduct."*
- License: *"State license full name or identifier, as listed on the SPDX license list"*, and *"Must be last section."* (A12)
- Links and examples: *"Must not contain broken links."* and *"If there are code examples, they should be linted in the same way as the code is linted in the rest of the project."* (A12)
- **Write the Docs** (A13):
  - *"Give users the information they need, but not too much."*
  - *"clearly state what your project does and why."*
  - *"Show a common example use case for your project."*
  - *"Keep your install instructions to a couple of lines for the basic case. Link to a page with more information and any caveats."*
  - *"Tell people how to get support"*
  - It warns against FAQs as documentation: they *"Become quickly outdated"*, *"Accumulate disparate content on unrelated topics"*, and *"Are rarely an actual list of frequently asked questions from real users."*
- **Microsoft** (A11, *Scannable content*):
  - *"Content on the first screen (also called above the fold) is the most likely to be read. Many readers won't scroll further without a compelling reason. So as always, keep it short, and lead with what's most important to the customer."*
  - *"In left-to-right languages, people read in an F shape, giving the most attention to the upper-left corner of a page. Put your most important information there."*
  - *"When you have a great, customer-focused reason to create longer content, provide readers with at least one way to navigate within it"*

### A.3 Sentences, paragraphs, and scannability

- **Sentence length.** Google: *"Use shorter sentences. Try to use fewer than 26 words per sentence."* (A8, *Accessibility*). Google again: *"Write shorter sentences. The shorter the sentence, the easier it is to translate."* (A9)
- **Paragraph length.** Microsoft: *"Three to seven lines is about the right length for a paragraph. It's also fine to have a single-line paragraph now and then."* (A11)
- **Front-loading.**
  - Google: *"Place distinguishing and important information of a paragraph in the first sentence to aid in scannability."* (A8)
  - Microsoft: *"Place important keywords near the beginning of headings, table entries, and paragraphs so they're easy to spot."* (A11)
  - Microsoft: *"Lead with what's most important. Front-load keywords for scanning."* (A11, *Top 10 tips*)
- **Walls of text.**
  - Google: *"Break up walls of text to aid in scannability."* (A8)
  - Microsoft: *"Long spans of dense text are daunting and unapproachable to readers. Write short headings, short sentences, and short paragraphs"* and *"Use short, simple words. Get to the point. Then stop."* (A11)
- **Brevity.** Microsoft: *"Give customers just enough information to make decisions confidently. Prune every excess word."* (A11, *Top 10*)
- **Conditions before instructions.** Google: *"try to mention the circumstance, conditions, or goal before you provide the instruction. Mentioning the circumstance first lets the reader skip the instruction if it doesn't apply."* The recommended form is *"To delete the entire document, click Delete."*, not *"Click Delete if you want to delete the entire document."* (A7, *Sentence structure*)
- **Voice and person.** Google: *"Use second person: 'you' rather than 'we'"* and *"Use active voice: make clear who's performing the action"*. (A6)
- **Timelessness.**
  - Google: *"Timeless documentation is documentation that avoids words and phrases that anchor the documentation to a point in time"*. *"Words like now, new, and currently can render"* such text outdated. (A10)
  - Google: *"If you must use words like new, give a reference point such as a date or version release number"*. (A10)
  - Google, in the highlights: *"Don't pre-announce anything"*. (A6)
- **Consistent terms.**
  - Google: *"Don't use the same word to mean different things."* and *"Repeat a word if the redundancy improves comprehension."* (A9)
  - Microsoft: *"Apply the same sentence structures to similar information."* (A11)
- **Plain words.** Google: *"don't use words like utilize or leverage when you mean use."* and *"Provide context. Don't assume that the reader already knows what you're talking about."* (A9)

### A.4 Headings, lists, tables, and links

- **Headings.**
  - Google: *"Use sentence case for headings and titles. Use descriptive headings"*. (A7)
  - Google: *"For a task-based heading, start with a [bare infinitive] verb"*. (A7)
  - Google: *"avoid using -ing verb forms as the first word in any heading"*. (A7)
  - Google: *"Use a unique level-1 heading (h1) for each page … Avoid repeating the exact page title in a heading on the page."* (A7)
  - Microsoft: *"If readers don't read the headings, they probably won't read the text that follows, either."* (A11)
  - Microsoft: *"If you can't find at least two distinct topics, skip the second-level headings."* (A11)
  - Microsoft: *"Avoid having two headings in a row without text in between … But don't insert filler text just to separate the headings."* (A11)
  - Microsoft: *"Keep headings as short as possible, and put the most important idea at the beginning."* (A11)
- **Lists.**
  - Microsoft: *"Lists work best when they have two to seven items. … Make items in a list parallel."* (A11)
  - Google: *"Don't use a list to show only one item"*. (A7)
  - Google: use numbered lists *"where the sequence is significant"*. (A7)
  - Google: in a bulleted list, *"Make sure it's clear whether or not every item is required."* (A7)
- **When a table beats prose or a list.**
  - Google: a table is for items where *"Each item is three or more pieces of related data."* Pairs go in a description list. (A7, *Tables*)
  - Google: *"If you have only one column in your table, turn the table into a list."* and *"Use tables only to present two-dimensional data"*. (A7)
  - Google: *"Avoid tables in the middle of a numbered procedure."* (A7)
  - Google: *"Introduce tables with a complete sentence that describes the purpose of the table because not all screen readers preannounce tables."* (A7)
  - Microsoft: *"Don't use a table just to present a list of items that are similar. Use a list instead."* (A11)
- **Linking out versus inlining.**
  - Google: *"When possible, provide help in context rather than linking elsewhere"*. It gives two cases for inlining: *"Define a term"* and *"Briefly explain a concept."* (A7, *Link text*)
  - Diátaxis says the opposite for explanation inside how-to and tutorial pages: *"if they're important, link to them"*. (A3, A2)
  - **The two rules do not conflict.** Google's rule is to inline a definition or a one-line gloss. Diátaxis's rule is to link out an extended explanation.
- **Link text.**
  - Google: *"use short, unique, descriptive phrases"*, *"Place important words at the beginning of the link text."*, and *"Don't use the same link text in the same document for different target"* pages. (A7)
  - GitHub, on relative links: see A.2.
- **Procedures.**
  - Google: *"When there's more than one way to do something, give only the best way. Giving alternate ways can confuse readers."* (A7, *Procedures*)
  - Google: *"State the action first and the result second."* (A7)
  - Google: mark optional steps with *"Optional:"*. (A7)

### A.5 Community health files (GitHub)

- The recognised files are `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`, `SECURITY.md`, `SUPPORT.md`, `FUNDING.yml`, issue and PR templates, and discussion forms. (A15)
  - *"A SECURITY file gives instructions on how to report a security vulnerability in your project"* (A15)
  - *"A SUPPORT file lets people know about ways to get help with your project."* (A15)
- *"You cannot create a default license file. License files must be added to individual repositories"*. (A15)
- SECURITY.md content: *"add information about supported versions of your project and how to report a vulnerability."* (A16)
- The community profile checklist looks for *"README, CODE_OF_CONDUCT, LICENSE, or CONTRIBUTING, in a supported location"*. (A16)
- Issue templates count only if they are *"located in the .github/ISSUE_TEMPLATE folder and contain valid name: and about: keys"*. (A16)
- CONTRIBUTING can include *"Steps for creating good issues or pull requests."* (A16)

### A.6 What could not be established for Part A

- **"Time to first success".** No source I could read gives a metric for it. The nearest rules are WTD's *"couple of lines for the basic case"* and Diátaxis's *"Deliver visible results early and often"*.
- **NN/g's primary findings** (scanning, the F-pattern) were not read. The F-shape claim appears here only as Microsoft states it (A11).
- **Art of README and the Make a README site content** were not read.

---

## Part B: skills and instruction files for the agent that consumes them

### B.1 Context budget and size ceilings

- **The context window is shared.**
  - Anthropic: *"The context window is a public good. Your Skill shares the context window with everything else Claude needs to know"*. (B1)
  - Anthropic: *"once Claude loads it, every token competes with conversation history and other context."* (B1)
  - OpenAI's Codex skill-creator uses the same framing: *"The context window is a public good."* (B14)
- **Assume the model is capable.**
  - Anthropic: *"Default assumption: Claude is already very smart. Only add context Claude doesn't already have."* The tests it gives: *"Does this paragraph justify its token cost?"* (B1)
  - agentskills.io: *"Would the agent get this wrong without this instruction?" If the answer is no, cut it."* (B11)
- **The loading tiers** (B2 table):
  - Level 1, metadata: *"Always (at startup)"*, *"~100 tokens per Skill"*.
  - Level 2, the SKILL.md body: loaded *"When Skill is triggered"*, *"Under 5k tokens"*.
  - Level 3+, bundled resources: loaded *"As needed"*, costing *"None until accessed"*.
  - The spec (B10) says: *"Metadata (~100 tokens)"*, *"Instructions (< 5000 tokens recommended)"*.
  - OpenAI (B14) says *"SKILL.md body - When skill triggers (<5k words)"*. It measures in words where the others measure in tokens.
- **SKILL.md line ceiling.** Four sources agree on 500 lines:
  - *"Keep SKILL.md body under 500 lines for optimal performance"* (B1)
  - *"Keep your main `SKILL.md` under 500 lines."* (B10)
  - *"Keep `SKILL.md` under 500 lines. Move detailed reference material to separate files."* (B4)
  - *"under 500 lines to minimize context bloat"* (B14)
- **Always-loaded instruction files** have lower ceilings than skills:
  - Claude Code, CLAUDE.md: *"target under 200 lines per CLAUDE.md file. Longer files consume more context and reduce adherence."* (B5)
  - Claude Code's auto-memory `MEMORY.md` is truncated: *"The first 200 lines of `MEMORY.md`, or the first 25KB, whichever comes first, are loaded"*. (B5)
  - GitHub Copilot's own prompt for generating instructions: *"Instructions must be no longer than 2 pages."* and *"Instructions must not be task specific."* (B16)
  - Copilot code review: *"Limit any single instruction file to a maximum of about 1,000 lines. Beyond this, the quality of responses may deteriorate."* and *"Very long instruction files may result in some instructions being overlooked."* (B17)
- **The description has hard and soft limits.**
  - Hard limit: `description` *"Must be 1-1024 characters"*. (B10, B1)
  - Claude Code truncation: *"the combined `description` and `when_to_use` text is truncated at 1,536 characters in the skill listing"*. (B4)
  - Claude Code budget: when there are many skills, *"Claude Code shortens descriptions to fit the listing's character budget, which can strip the keywords Claude needs"*. (B4)
  - Hence Claude Code's advice: *"Put the key use case first"*. (B4)
- **Longer reference files need a table of contents.**
  - Anthropic: *"For reference files longer than 100 lines, include a table of contents at the top. This ensures Claude can see the full scope … even when previewing with partial reads."* (B1)
  - Anthropic's skill-creator sets the threshold at *">300 lines"*. (B9)
- **Context rot**, as Anthropic states it (B8):
  - *"as the number of tokens in the context window increases, the model's ability to accurately recall information from that context decreases."*
  - *"Context, therefore, must be treated as a finite resource with diminishing marginal returns."*
  - The goal: *"find the smallest set of high-signal tokens that maximize the likelihood of your desired outcome."*
  - The caveat: *"minimal does not necessarily mean short"*.
  - Chroma's repo README (B19) states the premise: *"model performance varies significantly as input length changes, even on simple tasks."* The report's measured results were not read.
- **Long-context placement** (B3):
  - *"Place your long documents and inputs near the top of your prompt, above your query, instructions, and examples."*
  - *"Queries at the end can improve response quality by up to 30 percent in tests"*.

### B.2 Progressive disclosure and where reference material goes

- *"SKILL.md serves as an overview that points Claude to detailed materials as needed, like a table of contents in an onboarding guide."* (B1)
- **Keep references one level deep.** *"Keep references one level deep from SKILL.md. All reference files should link directly from SKILL.md"*. The reason: with nested references *"Claude might use commands like `head -100` to preview content … resulting in incomplete information."* (B1; the same rule is in B10)
- **Say when to load each file.**
  - agentskills.io: *"The key is telling the agent *when* to load each file. "Read `references/api-errors.md` if the API returns a non-200 status code" is more useful than a generic "see references/ for details.""* (B11)
  - OpenAI: *"it is very important to reference them from SKILL.md and describe clearly when to read them"*. (B14)
- **Split by domain.**
  - *"For Skills with multiple domains, organize content by domain to avoid loading irrelevant context."* (B1)
  - *"If certain contexts are mutually exclusive or rarely used together, keeping the paths separate will reduce the token usage."* (B7)
- **No duplication.** OpenAI: *"Information should live in either SKILL.md or references files, not both."* (B14)
- **No extra files in a skill.** OpenAI: *"Do NOT create extraneous documentation or auxiliary files, including: README.md, INSTALLATION_GUIDE.md, QUICK_REFERENCE.md, CHANGELOG.md"*. It adds: *"It should not contain auxiliary context about the process that went into creating it, setup and testing procedures, user-facing documentation, etc."* (B14)
- **Gotchas stay in SKILL.md.** agentskills.io: *"Keep gotchas in `SKILL.md` where the agent reads them before encountering the situation."* (B11)
- **Name files descriptively.** *"Use names that indicate content: `form_validation_rules.md`, not `doc2.md`"*. (B1)
- **Use forward slashes.** *"Always use forward slashes in file paths"*. (B1)
- **One file for humans, one for agents.**
  - agents.md: *"README.md files are for humans … AGENTS.md complements this by containing the extra, sometimes detailed context coding agents need"*. The aim is to *"Keep READMEs concise and focused on human contributors."* (B15)
  - agents.md precedence: *"The closest AGENTS.md to the edited file wins; explicit user chat prompts override everything."* (B15)

### B.3 The description, triggering, and over-triggering

- **Say what the skill does and when to use it.**
  - Anthropic: *"Include both what the Skill does and specific triggers/contexts for when to use it."* It adds that Claude *"uses it to choose the right Skill from potentially 100+ available Skills."* (B1)
  - The spec (B10) agrees: *"Should include specific keywords that help agents identify relevant tasks."*
- **Put all "when to use" in the description.** OpenAI: *"Include all "when to use" information here - Not in the body. The body is only loaded after triggering, so "When to Use This Skill" sections in the body are not helpful"*. (B14) Anthropic's skill-creator says the same: *"All "when to use" info goes here, not in the body."* (B9)
- **Avoid vague descriptions.**
  - Anthropic: *"Helps with documents"*, *"Processes data"*, and *"Does stuff with files"* are given as bad examples. (B1)
  - The spec gives *"Helps with PDFs."* as a poor example. (B10)
- **Point of view. The sources disagree here.**
  - Anthropic (B1): *"Always write in third person. The description is injected into the system prompt, and inconsistent point-of-view can cause discovery problems."* Good: *"Processes Excel files and generates reports"*. Avoid: *"I can help you…"* and *"You can use this to…"*.
  - agentskills.io (B12): *"Use imperative phrasing. Frame the description as an instruction to the agent: "Use this skill when..." rather than "This skill does...""*.
  - The two only half agree. Both reject first person. Both examples contain the clause *"Use when…"*.
- **How pushy to be. The sources disagree here too.**
  - Anthropic's skill-creator (B9) wants more push: *"Claude has a tendency to "undertrigger" skills … please make the skill descriptions a little bit "pushy""*.
  - agentskills.io (B12) agrees: *"Err on the side of being pushy."*
  - Anthropic's prompting guide (B3) warns the other way: *"If your prompts were designed to reduce undertriggering on tools or skills, these models may now overtrigger. The fix is to dial back any aggressive language. Where you might have said "CRITICAL: You MUST use this tool when...", you can use more normal prompting like "Use this tool when...""*.
  - B3 again: *"Instructions like "If in doubt, use [tool]" will cause overtriggering."*
  - **Which way to lean depends on the model. The rule is to measure it, which B12 describes.**
- **When a skill should not trigger.**
  - Claude Code's fix for *"Skill triggers too often"*: *"Make the description more specific"*, or *"Add `disable-model-invocation: true` if you only want manual invocation"*. (B4)
  - B4 on side effects: *"Use this for workflows with side effects or that you want to control timing, like `/commit`, `/deploy` … You don't want Claude deciding to deploy because your code looks ready."*
  - Negative tests: *"The most valuable negative test cases are near-misses — queries that share keywords or concepts with your skill but actually need something different."* (B12; the same in B9)
  - Test set size: *"Aim for about 20 queries: 8-10 that should trigger and 8-10 that shouldn't."* Run each several times, *"3 is a reasonable starting point"*, and use a trigger-rate threshold where *"0.5 is a reasonable default"*. (B12)
- **Simple tasks may not trigger a skill at all.** *"A simple, one-step request like "read this PDF" may not trigger a PDF skill even if the description matches perfectly, because the agent can handle it with basic tools."* (B12)
- **Scope a skill like a function.** *"Skills scoped too narrowly force multiple skills to load for a single task, risking overhead and conflicting instructions. Skills scoped too broadly become hard to activate precisely."* (B11)
- **Naming.**
  - Name format: *"Maximum 64 characters … lowercase letters, numbers, and hyphens"*, with *"Cannot contain reserved words: "anthropic", "claude""*. (B1)
  - Names to avoid: *"Vague names: `helper`, `utils`, `tools`"* and *"Inconsistent patterns within your skill collection"*. (B1)

### B.4 How to phrase instructions

- **Be specific enough to verify.** Claude Code (B5): *"write instructions that are concrete enough to verify"*. Its examples:
  - *"Use 2-space indentation"* instead of *"Format code properly"*
  - *"Run `npm test` before committing"* instead of *"Test your changes"*
- **Say what to do, not only what not to do.** B3: *"Tell Claude what to do instead of what not to do"*. Instead of *"Do not use markdown in your response"*, try *"Your response should be composed of smoothly flowing prose paragraphs."*
- **Give the reason.**
  - B3: *"Providing context or motivation behind your instructions … can help Claude better understand your goals"*. Its example: the bare *"NEVER use ellipses"* versus the reasoned *"Your response will be read aloud by a text-to-speech engine, so never use ellipses"*. *"Claude is smart enough to generalize from the explanation."*
  - B9: *"If you find yourself writing ALWAYS or NEVER in all caps, or using super rigid structures, that's a yellow flag — if possible, reframe and explain the reasoning"*.
  - B9 also warns against *"oppressively constrictive MUSTs"*.
- **Use short imperatives in structure, not narrative.**
  - B17: *"Distinct headings that separate different topics. Bullet points for easy scanning and reference. Short, imperative directives rather than long narrative paragraphs."*
  - B5: *"use markdown headers and bullets … Claude scans structure the same way readers do: organized sections are easier to follow than dense paragraphs."*
  - B9: *"Prefer using the imperative form in instructions."*
- **Cut vague exhortations.**
  - B17: *"Vague quality improvements: Be more accurate / Don't miss any issues / Be consistent in your feedback. These types of instructions add noise without improving Copilot's effectiveness"*.
  - B11: generated skills fail by producing *"vague, generic procedures ("handle errors appropriately," "follow best practices for authentication")"*.
- **Remove contradictions.**
  - B5: *"if two rules contradict each other, Claude may pick one arbitrarily. Review your CLAUDE.md files … periodically to remove outdated or conflicting instructions."*
  - B5 on user versus project rules: *"if a user rule and a project rule conflict, Claude may follow either one, so keep the two consistent."*
  - B16: *"Whenever possible, try to avoid providing conflicting sets of instructions."*
- **Use one term for one thing.** B1: *"Choose one term and use it throughout the Skill"*. The bad example mixes *"API endpoint", "URL", "API route", "path"*. *"Consistency helps Claude parse and follow instructions."*
- **Offer defaults, not menus.**
  - B1: *"Don't present multiple approaches unless necessary"*. Bad: *"You can use pypdf, or pdfplumber, or PyMuPDF…"*. Good: a default plus one escape hatch.
  - B11: *"pick a default and mention alternatives briefly rather than presenting them as equal options."*
- **Match the level of freedom to how fragile the task is.** B1: *"Match the level of specificity to the task's fragility and variability"*.
  - Low freedom (*"Run exactly this script … Do not modify the command or add additional flags."*) is for operations that are *"fragile and error-prone"*.
  - High freedom is for when *"Multiple approaches are valid"*.
- **Pitch the instructions at the right altitude.**
  - B8 names two failure modes: *"hardcoding complex, brittle logic in their prompts"* and *"vague, high-level guidance that fails to give the LLM concrete signals … or falsely assumes shared context."*
  - B3's golden rule: *"Show your prompt to a colleague with minimal context on the task and ask them to follow it. If they'd be confused, Claude will be too."*
- **Examples beat adjectives.**
  - B1: *"Examples convey the desired style and level of detail to Claude more clearly than descriptions alone."*
  - B3: *"Include 3–5 examples"*, and make them *"Relevant"*, *"Diverse"*, and *"Structured"* (*"Wrap examples in `<example>` tags"*).
  - B8: *"teams will often stuff a laundry list of edge cases into a prompt … We do not recommend this. Instead, … curate a set of diverse, canonical examples"*.
  - B11: *"provide a template. This is more reliable than describing the format in prose"*.
- **Separate content types with XML tags.** B3: *"Wrapping each type of content in its own tag (for example, `<instructions>`, `<context>`, `<input>`) reduces misinterpretation."*
- **Avoid time-sensitive text.** B1: *"Don't include information that will become outdated"*. Put old material in an *"Old patterns"* section.
- **Don't over-cover.** B11: *"Overly comprehensive skills can hurt more than they help — the agent struggles to extract what's relevant and may pursue unproductive paths triggered by instructions that don't apply to the current task."*
- **Write standing instructions.** Claude Code (B4): the skill *"stays there across later turns … Claude Code does not re-read the skill file on later turns, so write guidance that should apply throughout a task as standing instructions rather than one-time steps."*
- **Use hooks for anything that must happen.**
  - B5: CLAUDE.md is *"context, not enforced configuration"*.
  - B5: *"If the instruction is something that must run at a specific point … write it as a hook instead."*
- **Don't point at external links.** B17 lists *"Follow external links"* as unsupported. Its workaround: *"Copy the relevant content directly into your instruction file instead"*.

### B.5 Scripts bundled with a skill

- **Run or read.** State whether the agent runs the script or reads it. B1: *"Make clear in your instructions whether Claude should: Execute the script … Read it as reference"*. B7 says the same.
- **Solve, don't defer.** B1: *"handle error conditions rather than deferring to Claude."*
- **No voodoo constants.** B1: *"No "voodoo constants" (all values justified)"*.
- **Make scripts agent-friendly** (B13):
  - *"Avoid interactive prompts. This is a hard requirement … A script that blocks on interactive input will hang indefinitely."*
  - *"`--help` output is the primary way an agent learns your script's interface."*
  - Error messages should *"say what went wrong, what was expected, and what to try"*.
  - *"Prefer structured formats — JSON, CSV, TSV"*.
  - Idempotency: *"Agents may retry commands."*
  - *"Dry-run support"* for destructive operations.
  - *"Meaningful exit codes"*.
  - *"Predictable output size"*, because harnesses *"truncate tool output beyond a threshold (e.g., 10-30K characters)"*.
  - *"Pin versions"*.
- **Validate before executing.** B1's plan-validate-execute pattern is for *"Batch operations, destructive changes, complex validation rules, high-stakes operations."* Validators should give specific errors, such as *"Field 'signature_date' not found. Available fields: …"*.

### B.6 Safety: prompt injection and supply chain through installed skills and plugins

- **Only install skills from trusted sources.**
  - Anthropic: *"Use Skills only from trusted sources … a malicious Skill can direct Claude to invoke tools or execute code in ways that don't match the Skill's stated purpose."* (B2)
  - B2's audit rule: *"Review all files bundled in the Skill: SKILL.md, scripts, images, and other resources. Look for unusual patterns such as unexpected network calls, file access patterns, or operations that don't match the Skill's stated purpose"*.
  - B2 on fetched content: *"Skills that fetch data from external URLs pose particular risk, as fetched content may contain malicious instructions. Even trustworthy Skills can be compromised if their external dependencies change over time"*.
  - B2: *"Treat like installing software"*.
- The blog agrees: *"pay attention to instructions or code within the skill that instruct Claude to connect to potentially untrusted external network sources."* (B7)
- **The authoring side** (B9): *"skills must not contain malware, exploit code, or any content that could compromise system security. A skill's contents should not surprise the user in their intent if described."* This is the *"Principle of Lack of Surprise"*.
- **Plugins and hooks.**
  - *"Plugins and marketplaces are highly trusted components that can execute arbitrary code on your machine with your user privileges."* (B6, *Discover plugins*)
  - *"Command hooks execute shell commands with your full user permissions."* (B6, *Hooks*)
  - Hooks and trust: in `-p` and SDK sessions, Claude Code *"treats the folder as trusted, so hooks committed in a repository's `.claude/settings.json` run in a folder you've never trusted"*. (B6)
  - Hook practices (B6): *"Validate and sanitize inputs"*, *"Always quote shell variables"*, *"Block path traversal"*, *"Use absolute paths"*, and *"Skip sensitive files"*.
- **Claude Code's own mitigation.** It sanitises descriptions: *"it also escapes angle brackets so the text can't imitate Claude Code's internal formatting."* (B4)
- **The OWASP LLM01 mitigation catalogue** (B18). It opens: *"it is unclear if there are fool-proof methods of prevention"*. The mitigations are:
  - *"Constrain model behavior"*
  - *"Define and validate expected output formats"*
  - *"Implement input and output filtering"*
  - *"Enforce privilege control and least privilege access"*
  - *"Require human approval for high-risk actions"*
  - *"Segregate and identify external content"*
  - *"Conduct adversarial testing"*
- The empirical prevalence studies of malicious skills were **not read** (arXiv blocked); see §0.

### B.7 How to test instructions

- **Build evaluations first.** B1: *"Create evaluations BEFORE writing extensive documentation."*
- **Test on every model you target.** B1's checklist: *"At least three evaluations created"* and *"Tested with Haiku, Sonnet, and Opus"*. The reason: *"What works perfectly for Opus might need more detail for Haiku."*
- **Watch how the agent navigates the skill** (B1):
  - *"Ignored content: If Claude never accesses a bundled file, it might be unnecessary or poorly signaled"*
  - *"Overreliance on certain sections"*
- **Start small with instruction files.** B17: *"Begin with 10–20 specific instructions"* and *"Add new instructions one at a time or in small groups"*.
- **Read transcripts, not just outputs.** B9: *"Keep the prompt lean. Remove things that aren't pulling their weight. Make sure to read the transcripts, not just the final outputs"*.

---

## Quality rubric for reader-facing docs and agent-facing skills

Each criterion is phrased so that a reviewer can answer yes or no by looking at the file.

### Reader-facing docs (README, package docs)

1. **The README opens with what the project is, what it does, and why it is useful, then how to get started.** GitHub lists these first among *"What the project does / Why … useful / How users can get started"* (A14). standard-readme puts Short Description right after Title and before Install (A12).
2. **The one-line description is under 120 characters.** It sits on its own line with no heading, and matches the package-manager and GitHub descriptions. (A12)
3. **The first screen carries the most important content, and no scroll is needed to learn what the thing is.** *"Content on the first screen … is the most likely to be read."* (A11)
4. **The basic install path is a code block of a couple of lines.** Caveats and alternatives are linked out, not inlined. (A12 *"Code block illustrating how to install"*; A13 *"Keep your install instructions to a couple of lines for the basic case. Link to a page with more information"*)
5. **Unusual or manual dependencies are stated in the install section.** (A12, the `Dependencies` subsection)
6. **Usage shows at least one runnable common example in a code block.** (A12; A13 *"Show a common example use case"*)
7. **The README says where to get help, whether contributions are accepted, and the licence.** The licence is given as an SPDX identifier in the last section. (A12, A13, A14)
8. **Every link resolves.** Links to files in the repository are relative, not absolute. (A12 *"Must not contain broken links"*; A14 relative links)
9. **A README over 100 lines has a table of contents covering every `##` heading.** (A12)
10. **The README is limited to getting started and contributing.** Longer material lives elsewhere and is linked. (A14 *"should only contain information necessary for developers to get started"*)
11. **Each page or section is one Diátaxis kind.** A how-to does not drift into explanation or exhaustive reference; those are linked. (A1 *"Crossing or blurring the boundaries … is at the heart of a vast number of problems"*; A3; A4)
12. **Reference sections describe and only describe.** They use a consistent pattern mirroring the structure of the thing described. (A4)
13. **Sentences average under about 26 words.** (A8 *"Try to use fewer than 26 words per sentence."*)
14. **Paragraphs are 3–7 lines, and no wall of text runs past that without a heading, list, or break.** (A11; A8 *"Break up walls of text"*)
15. **The first sentence of each paragraph carries its distinguishing information.** Headings and list items front-load their key word. (A8; A11)
16. **Headings are sentence case and descriptive.** Task headings start with a verb (not an -ing form), there is one H1 per page, and no heading repeats the page title. (A7 *Headings*)
17. **Lists hold 2–7 parallel items.** No list has a single item. Sequences are numbered, and the required status of each bulleted item is clear. (A11; A7 *Lists*)
18. **Tables are used only for two-dimensional data (three or more attributes per item) and are introduced by a sentence.** One-column tables become lists. (A7 *Tables*; A11)
19. **Conditions come before instructions** (*"To X, do Y"*), and procedures give one best way. (A7 *Sentence structure*, *Procedures*)
20. **No time-anchored words** (*"new"*, *"now"*, *"currently"*, *"soon"*) appear without a date or version. (A10; A6 *"Don't pre-announce anything"*)
21. **One term is used per concept throughout.** No word is reused with a second meaning. (A9; A11)
22. **The recognised community health files exist where GitHub looks for them.** These are `CONTRIBUTING`, `CODE_OF_CONDUCT`, and `SECURITY.md` (stating supported versions and how to report). `SUPPORT` is optional. Issue templates carry `name:` and `about:`. (A15; A16)

### Agent-facing skills and instruction files

23. **`name` is 1–64 characters of lowercase letters, digits, and hyphens.** It is not generic (`helper`, `utils`) and contains no reserved word. (B10; B1)
24. **`description` is under 1,024 characters and says both what the skill does and when to use it, with concrete trigger keywords.** It is not first person, and not vague (*"Helps with documents"*). (B10; B1; B12)
25. **The key use case is in the description's first sentence, so it survives listing truncation.** (B4 *"Put the key use case first"*, 1,536-character cap and budget truncation)
26. **No "When to use this skill" section sits in the body.** All trigger information is in the frontmatter. (B14; B9)
27. **A skill with side effects (deploy, publish, send) is not auto-invocable, or its description names the explicit request that triggers it.** (B4 `disable-model-invocation`, *"You don't want Claude deciding to deploy because your code looks ready."*)
28. **The body is under 500 lines and roughly 5,000 tokens.** Detail is moved to referenced files. (B1; B2; B4; B10; B14)
29. **Always-loaded instruction files (CLAUDE.md/AGENTS.md) stay under about 200 lines.** Task-specific material is moved into skills or path-scoped rules. (B5; B16 *"no longer than 2 pages"*)
30. **Every bundled reference file is linked directly from SKILL.md, one level deep, with a stated condition for when to read it.** (B1; B10; B11 *"Read `references/api-errors.md` if the API returns a non-200 status code"*)
31. **Reference files over 100 lines open with a table of contents.** (B1; B9 uses 300 lines)
32. **Nothing is stated in two places** (SKILL.md and a reference, or two rule files). No two rules contradict each other. (B14 *"not both"*; B5 *"Claude may pick one arbitrarily"*; B16)
33. **Every instruction is concrete enough to verify.** There are no vague quality exhortations (*"be accurate"*, *"follow best practices"*, *"handle errors appropriately"*). (B5; B17; B11)
34. **Prohibitions say what to do instead.** Hard rules carry their reason. All-caps ALWAYS/NEVER/CRITICAL is rare and justified. (B3 *"Tell Claude what to do instead of what not to do"*, *"dial back any aggressive language"*; B9 *"yellow flag"*)
35. **Each instruction contains only what the agent would get wrong without it.** There is no explanation of general knowledge. (B1 *"Does this paragraph justify its token cost?"*; B11)
36. **One default is given per choice, with at most one escape hatch.** No menu of equal options. (B1; B11)
37. **Output formats are shown by template or example, not described by adjectives.** Examples are relevant, diverse, and tagged. (B1; B3; B11; B8)
38. **Each bundled script is marked as either run or read.** Scripts are non-interactive, have `--help`, emit structured output and actionable errors, and pin their dependencies. (B1; B13)
39. **The skill and plugin contain nothing that would surprise a user who read the description.** No unexplained network calls or fetch-and-follow of external instructions, and hooks/scripts follow the hook security practices. (B9 *"Principle of Lack of Surprise"*; B2 security; B6)
40. **Triggering has been tested.** About 20 labelled queries, half of them near-miss negatives, each run about 3 times. Behaviour has been checked on each target model. (B12; B1 checklist)

---

### Disagreements between sources

- **Description voice.** Anthropic (B1) says third person (*"Processes Excel files…"*). agentskills.io (B12) says imperative (*"Use this skill when..."*). Both reject first and second person, and both examples include *"Use when…"*.
- **Pushiness.** Anthropic's skill-creator (B9) and agentskills.io (B12) push against under-triggering. Anthropic's prompting guide (B3) warns that the same pushiness causes over-triggering on newer models. The two are reconciled only by measurement (B12's trigger-rate evals).
- **Body budget units.** B2 and B10 say under 5k *tokens*. B14 says under 5k *words*. All four say 500 lines.
- **Table-of-contents threshold.** For skill reference files it is 100 lines (B1) or 300 lines (B9). For READMEs, standard-readme requires one above 100 lines (A12).
- **Inline or link out.** Google (A7) says inline a definition or a brief explanation. Diátaxis (A2, A3) says link out an extended explanation from a how-to or tutorial. The two agree on what goes where; they only look like they conflict.
