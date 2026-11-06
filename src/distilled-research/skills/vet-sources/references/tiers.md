# Source tiers

Tiers are ordinal (A above B above C) and uncalibrated. A tier says how a source ranks against the others in the same list. It does not say how likely its claims are to be true. Each tier is a letter. A source with no tier yet reads `none`.

## Definitions

The Legend text column is what a reply copies.

| Tier | Kind of source | Evidence the rater needs | Legend text |
| :-- | :-- | :-- | :-- |
| A | A document of record, a standard or regulator text, official documentation by the maintainers of the thing described, a peer-reviewed paper or preprint that releases its data or method | The source states who wrote it and when, and it is the primary place the claim is made | Tier A: a record, standard, official documentation, or a peer-reviewed paper or preprint with its data or method. |
| B | A maintained personal or small-team repository, a news summary of primary material, a vendor blog about its own product | The source has a named author, a history of use, and at least one independent mention | Tier B: a maintained personal or small-team repository, a vendor blog about its own product, or a news summary of primary material. Each has a named author and history. |
| C | A forum thread, a listicle, an aggregator or directory listing, a content farm, a repository with no history or no outside mention | No evidence yet that moves it up | Tier C: weaker than B. |

Commentary is a source that repeats or discusses another source's measurement or document. A news summary is commentary.

## The test

Name who wrote the source and who stands behind it. Check whether it makes the claim first or repeats another source. Search for mentions made outside it (lateral reading), apart from listings and aggregators, which mirror their targets. Assign the highest tier whose row fits.

## What moves a source

A move up needs the evidence column of the destination tier.

- Up one tier: an independent mention by a higher-tier source.
- Up one tier: a record in an open catalogue, or a named author with a checkable record.
- Down one tier: no named author, or a claim copied from another source.
- Down one tier: a repository with stars but no forks or history.
- Down one tier: a catalogue flag on the source, such as low reliability, or a stale update (fast-moving topic).
- Down one tier: a correction notice that changes the source's results, data or conclusions.
- A correction of metadata (funding, affiliation, typo) goes in `reason` and moves no tier.
- A retraction or expression-of-concern notice moves no tier. It sets `keep` = `no`, as the keep rule in `briefs/vetter.md` says.
- Official authorship says who wrote a source, not that it was audited. A large vendor repository can stay tier B.
- "No mention found" is recorded as found. It does not move a source up or down.

## Without reading a page

Only host-class rules apply before a page is read. A hostname that is a government, standards-body or regulator domain, or the documentation host of the project the user named, may take tier A. A hostname that is a known listing, aggregator or user-posting host may take tier C. Everything else gets no tier until the vetter reads and checks it after the yes.
