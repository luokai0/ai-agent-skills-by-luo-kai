---
name: research-retrieval
description: Use when an agent must find, gather, and synthesize evidence from documents, web sources, internal knowledge bases, or datasets to answer a research question, and the answer must be traceable to specific sources.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Research Retrieval

## Purpose and boundaries

This skill governs how an agent locates, filters, reads, and synthesizes sources to answer a bounded research question with citable evidence. It covers literature and document review, competitive or market scans, internal knowledge base lookups, and fact-finding for technical decisions.

In scope: query planning, source discovery, relevance triage, extraction of claims with provenance, cross-source comparison, and a sourced write-up.

Out of scope: making decisions on the user's behalf, publishing or sending findings externally, accessing systems the user has not authorized, scraping behind logins or paywalls, and producing legal, medical, or financial conclusions that require a licensed professional.

## Inputs and assumptions

Before searching, confirm:

1. The research question, stated as a question that can be answered or bounded.
2. Scope limits: time window, geography, languages, source types (for example peer-reviewed only, vendor docs, internal wiki).
3. Available retrieval tools and their access boundaries. Record what each tool can and cannot reach.
4. The intended audience and decision the findings will feed.
5. Freshness requirements. Any claim about software versions, pricing, regulations, or product features is version-sensitive and must be checked against the current official source at the time of work.

If the question is ambiguous, ask one clarifying question with a proposed default rather than guessing silently. Assume no source is current until its date is verified.

## Operating workflow

1. **Decompose.** Split the question into two to five sub-questions. Write each as a falsifiable statement or a specific lookup.
2. **Plan queries.** For each sub-question, write three to five query variants: exact terms, synonyms, the official product or standard name, and a negative variant that surfaces contrary evidence.
3. **Discover.** Run queries, collect candidate sources, and record URL or identifier, title, publisher, date, and retrieval timestamp in a source log.
4. **Triage.** Score each source on authority (primary over secondary), recency (against the freshness requirement), and directness (addresses the sub-question rather than a neighboring topic). Keep sources scoring well on at least two of three; discard the rest with a logged reason.
5. **Read and extract.** For each kept source, extract claims as atomic statements. Each claim record holds: the claim, the exact supporting passage or locator (section, page, timestamp), the source ID, and a confidence tag.
6. **Cross-check.** Group claims by sub-question. Mark each claim as corroborated (two or more independent primary sources), single-sourced, or conflicting.
7. **Synthesize.** Write the answer leading with the direct response, followed by supporting evidence, then conflicts and gaps.
8. **Stop.** Stop when the last two query rounds yield no new relevant primary sources, or when the time budget is reached. Report the stopping reason.

## Decision gates

- **Gate A (scope):** Proceed only when the question and scope limits are confirmed. If the user is unavailable and the question is still ambiguous, proceed on the stated default and label every assumption in the output.
- **Gate B (source access):** Before accessing any source requiring credentials, personal data, or a terms-of-service exception, stop and request explicit approval naming the source and the purpose.
- **Gate C (external impact):** Before sending messages, posting, submitting forms, filing tickets, or contacting third parties with findings or queries, obtain explicit approval. Drafting is permitted; sending is not.
- **Gate D (sensitive content):** If sources contain personal data, confidential material, or security-relevant detail (credentials, vulnerability specifics, unpublished financials), pause, minimize what is quoted, and ask for direction on handling.
- **Gate E (evidence sufficiency):** If a sub-question has zero primary sources, report it as unanswered rather than filling it from memory.

## Verification and evidence

Quality checks, all required before delivery:

- Every factual claim in the synthesis maps to at least one claim record with a locator. Target: 100 percent traceability; any untraced sentence is removed or flagged.
- Every source in the bibliography was actually opened and read at the cited locator. Snippets alone do not count as reading.
- Each source lists a retrieval date. Each version-sensitive claim names the version it applies to and states that it was checked against current official documentation, or marks it unverified.
- At least one contrary-evidence search was run per sub-question, and results are reported even when they are weak.
- Quotations match the source character for character. Spot-check at least three quotes per deliverable.
- Numbers are reported with units, date, and denominator. Do not convert or round without stating it.
- Do not present any benchmark result, statistic, or compliance status that was not found in a retrieved source.

## Failure handling

- **Paywalled, blocked, or unreachable source:** Log the failure, search for an accessible mirror or summary by the same publisher, and otherwise mark the claim as unverified. Do not reconstruct content from memory.
- **Conflicting primary sources:** Report both positions with dates and methods. Do not average or pick a winner without a stated criterion.
- **Stale source contradicted by newer one:** Prefer the newer primary source and note the change.
- **Empty results:** Broaden terms once, then report the gap. Do not loop indefinitely.
- **Tool error or rate limit:** Pause, record the error, retry at most twice with backoff, then report partial results.
- **Suspected fabricated or low-quality source:** Exclude it and log the reason. Do not cite it.

## Deliverable contract

Produce a single document with these parts, in order:

1. **Answer** (under 150 words), stating the direct response and confidence level (high, moderate, low, unanswered).
2. **Scope and assumptions**, including the stated default for any ambiguity.
3. **Findings by sub-question**, each claim followed by its source ID and locator.
4. **Conflicts and gaps**, listing unresolved disagreements and unanswered sub-questions.
5. **Source log**: ID, title, publisher, date, URL or identifier, retrieval date, authority and recency rating, and status (used, excluded with reason).
6. **Search record**: queries run, counts of candidates and kept sources, and stopping reason.

Do not include: unsourced claims, speculative recommendations presented as findings, or content copied beyond what is needed to support a claim.