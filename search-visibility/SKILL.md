---
name: search-visibility
description: Use when auditing, diagnosing, or improving how a business's website, pages, or listings appear in organic search results, including indexing problems, traffic drops, keyword and intent gaps, technical SEO issues, and local search profiles.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Search Visibility

## Purpose and boundaries

This skill produces evidence-based diagnoses and prioritized plans for organic search visibility of a business's owned properties: website pages, product or service catalogs, blog content, and business listings (such as local directory profiles). It covers crawlability, indexability, on-page relevance, search-intent fit, internal linking, structured data, page experience signals, and local listing accuracy.

It does not cover paid search management, guaranteed ranking outcomes, link acquisition campaigns involving outreach to third parties, reputation management, or legal compliance review of marketing claims. Do not promise rankings, traffic figures, or timelines. Search engine behavior changes; treat all ranking-factor assumptions as hypotheses to test.

## Inputs and assumptions

Gather before analysis:

1. Site or property list, with the primary business goal (leads, sales, bookings, calls) for each.
2. Search Console or equivalent webmaster data for the last 16 months, if available: queries, pages, impressions, clicks, average position, coverage/indexing status.
3. Analytics data for organic sessions and conversions, same window.
4. Crawl export (URL, status code, canonical, meta robots, title, H1, word count, internal inlinks).
5. Top 20 to 50 commercial and informational target queries the business cares about, with the page currently intended to rank for each.
6. Competitor set: three to five domains that rank for those queries.
7. For local work: the business's registered listing data (name, address, phone, category, hours) as the authoritative source.

If any input is missing, state the assumption explicitly in the report and label the affected conclusions as provisional. Do not infer traffic or revenue figures that were not supplied.

## Operating workflow

1. **Establish the baseline.** Record organic clicks, impressions, average position, and indexed page count per property for the most recent 28 days and the same period prior year or prior quarter. Note any known changes (migrations, redesigns, template updates, pricing changes) with dates.
2. **Classify the problem.** Assign each observed symptom to one category: (a) not discovered, (b) discovered but not indexed, (c) indexed but not relevant to queries, (d) relevant but outcompeted, (e) ranking but not clicked, (f) clicked but not converting. Diagnosis drives the fix; do not jump to content rewrites before classification.
3. **Audit technical access.** Check robots directives, HTTP status codes, redirect chains (flag chains longer than one hop), canonical consistency, duplicate host variants (www and non-www, http and https), sitemap accuracy, and noindex tags on pages that should rank.
4. **Audit indexability at scale.** Compare the sitemap URL set, crawled URL set, and indexed URL set. Identify pages that are indexed but low-value (thin, parameterized, filtered duplicates) and pages that are valuable but absent from the index.
5. **Map queries to pages.** For each target query, identify the page that should rank and check whether its title, H1, opening paragraph, and headings match the dominant intent. Intent types: informational (guides, definitions), commercial investigation (comparisons, reviews), transactional (product or booking pages), navigational (brand or location pages). A mismatch between intent and page type is a primary defect.
6. **Compare against competitors.** For each target query, list the top three ranking page types (format, length class, content depth, presence of tools or pricing). Identify concrete gaps; do not recommend "more content" without naming the missing element.
7. **Review click-through.** For queries with position 1 to 10 and impressions above a threshold you set in the report, compare observed CTR with the expected band for that position. Low CTR with adequate position points to title and snippet defects.
8. **Check local listings where applicable.** Verify name, address, phone, and category consistency across the business's listed profiles against the authoritative record. Inconsistency is a defect to fix; note that the business must control the listing to edit it.
9. **Prioritize.** Score each finding by estimated impact (affected queries or pages, conversion relevance) and effort. Sort into: fix now, schedule, monitor.

## Decision gates

- **Gate A, before recommending a migration or URL change:** Confirm the change is required by a measured defect, not preference. Require a redirect map covering every changed URL with one-hop 301 targets, and a rollback plan. Halt and request explicit approval from the site owner before any change that alters live URLs, robots rules, or sitemaps.
- **Gate B, before recommending noindex or removal of pages:** Require evidence that the page receives no meaningful organic entrances or conversions. Get explicit approval before recommending removal.
- **Gate C, before any content rewrite:** Confirm the classification in step 2 is "relevant but outcompeted" or "ranking but not clicked." Rewrites for pages classified as technically blocked are wasted effort.
- **Gate D, external actions:** Any recommendation involving publishing to third-party platforms, editing listings the business does not control, outreach, or sending data outside the organization requires explicit owner approval and is listed separately.
- **Gate E, sensitive data:** Do not include personal data from analytics or user-submitted content in the deliverable. Aggregate or redact before reporting.

## Verification and evidence

Every finding must cite its evidence: the URL, query, metric, date range, or crawl field. Quality checks before delivery:

- Each recommendation maps to one classified problem and one measurable success metric (e.g., indexed count of a page set, impressions for a query cluster, CTR band, crawl error count).
- Re-crawl or re-check each fixed item within a window you specify, and compare against the baseline.
- Confirm that any Search Console or platform feature names, report locations, or setting paths are verified against current official documentation, since interfaces change. Mark them "verify before use."
- State confidence per finding: high (directly observed in data), medium (inferred from consistent patterns), low (hypothesis requiring test).

## Failure handling

- **Missing data:** Proceed with the reduced scope, list what was unavailable, and state which conclusions are blocked.
- **Conflicting signals** (e.g., rankings rose while clicks fell): Report both, check for SERP feature changes or query mix shifts, and avoid a single causal claim.
- **Suspected penalty or manual action:** Stop optimization work. Report the evidence and recommend the owner check the official webmaster console messages and consult qualified help.
- **Sudden large drop:** Check for recent deployments, robots or noindex changes, and migration dates before analyzing content. Escalate if traffic loss is severe and the cause is unidentified.

## Deliverable contract

Return a single report with these sections in order:

1. Executive summary (five bullets max, each with a metric).
2. Baseline table: property, period, clicks, impressions, average position, indexed pages.
3. Findings table: ID, classification, affected URLs or queries, evidence, confidence.
4. Prioritized action plan: action, owner role, approval gate triggered (if any), success metric, check date.
5. Open questions and missing inputs.
6. Items marked "verify before use" with the specific documentation to consult.

Do not include unsupported forecasts, ranking guarantees, or claims about algorithm internals presented as fact.