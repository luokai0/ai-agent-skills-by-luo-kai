---
name: web-search-retrieval-and-live-data
description: Use when a task requires current, time-sensitive, or externally verifiable facts from the web, such as prices, availability, news, regulations, software release status, or public records, and the answer must cite sources and state how fresh the data is.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Web Search Retrieval And Live Data

## Purpose and boundaries

This skill covers finding, retrieving, checking, and reporting live or recent information from public web sources. It produces answers that show where each fact came from, when it was observed, and how confident the evidence makes you.

In scope: query formulation, source selection, page retrieval, extraction of specific values, cross-source comparison, freshness labeling, and cited summaries.

Out of scope: answering from memory when the question is time-sensitive, accessing private or authenticated accounts, bypassing paywalls or access controls, bulk scraping that conflicts with a site's terms or robots directives, and making decisions with legal, medical, or financial consequences without stating that a qualified professional must confirm them.

## Inputs and assumptions

Before searching, pin down:

1. The exact question, including entity names, jurisdiction, and date range.
2. The required output form: a number, a list, a yes/no status, or a narrative.
3. The freshness requirement: "as of today," "in the last 30 days," or "any recent version."
4. The acceptable source tier. Primary sources (official filings, vendor documentation, government registers, original datasets) outrank secondary sources (news, aggregators, forums).

Assume the current date is unknown unless the user or the retrieval tool states it. Record the access date of every retrieved page.

## Operating workflow

1. **Restate the claim to verify** as a single falsifiable sentence.
2. **Plan 2 to 4 queries** that vary terminology: the official name, the product or regulation identifier, and a site-restricted form if the domain is known. Do not repeat near-identical queries.
3. **Rank candidates.** Prefer primary sources, then recent dated pages, then reputable secondary coverage.
4. **Retrieve and read** the relevant sections. Extract the exact value, its unit, its effective date, and the page's publication or update date.
5. **Cross-check** with at least one independent source for any claim that will be relied upon.
6. **Record evidence** in a table: claim, value, source URL, publisher, date observed, date published or updated, source tier.
7. **Resolve conflicts** using the decision gates below.
8. **Write the answer** using the deliverable contract.

## Decision gates

- **Gate A: Is the source primary?** If the only source is secondary, label the finding "reported, not confirmed by primary source."
- **Gate B: Is it fresh enough?** If the page lacks a date, or the date falls outside the required window, do not present it as current. Search again or state the gap.
- **Gate C: Do sources agree?** Two independent agreeing sources support a finding. A single source supports only a tentative finding. Disagreement triggers a note listing both values and likely reasons (different dates, units, regions, or definitions).
- **Gate D: Does the action go beyond reading?** Stop and request explicit approval before any of the following: submitting forms, creating accounts, logging in, posting or messaging, purchasing, downloading files of uncertain origin, running code found online, or sending retrieved personal data elsewhere. Approval must name the specific action.
- **Gate E: Is the data personal?** If results expose identifiable private individuals, limit output to what the user's stated purpose requires and do not compile profiles.

## Verification and evidence

Quality checks before delivering:

- Every numeric or dated claim has a citation with URL and observed date.
- Every "current" claim states its as-of date.
- Each quoted value matches the source text exactly, including units and currency.
- At least one claim per answer was checked against a second source, or the answer says it was not.
- Software versions, prices, legal thresholds, and product specifications are marked "verify against current official documentation before use," because these change frequently.
- No inferred value is presented as retrieved.

## Failure handling

- **No results or blocked page:** Try one alternate query and one alternate source type. If still blocked, report the blocker and what was attempted. Do not guess the content.
- **Paywalled or login-gated:** Use only the visible public abstract or cached public summary, labeled as partial.
- **Conflicting primary sources:** Report both, with dates, and do not pick one silently.
- **Stale results only:** Say so in the first sentence of the answer.
- **Tool or time uncertainty:** State that the date could not be confirmed.

## Deliverable contract

The answer contains, in order:

1. A direct answer in one to three sentences, with the as-of date.
2. An evidence table: claim, value, source, publisher, observed date, confidence (confirmed, single-source, or unresolved).
3. Caveats: conflicts, gaps, and version-sensitive items.
4. Next actions requiring approval, if any, listed separately.

Do not include uncited statistics, invented URLs, or unverified recommendations. Do not present search snippets as full-page findings.