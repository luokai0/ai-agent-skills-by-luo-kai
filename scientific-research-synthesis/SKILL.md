---
name: scientific-research-synthesis
description: Use when collecting, screening, and synthesizing scientific studies, trial records, or preprints from external registries and bibliographic databases into a sourced evidence summary, review input, or research brief.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Scientific Research Synthesis

## Purpose and boundaries

This skill produces a traceable synthesis of research findings drawn from external sources such as bibliographic databases, clinical trial registries, funder repositories, preprint servers, and regulatory summaries. It covers question framing, search design, screening, data extraction, evidence appraisal, and reporting.

It does not produce clinical recommendations, legal or regulatory conclusions, or new statistical results beyond simple pooling that the user explicitly requests. It does not submit, edit, or post anything to external registries.

## Inputs and assumptions

Required before starting:
- A research question stated as population, exposure or intervention, comparator, outcomes, and study designs of interest (PICO or an equivalent frame).
- The purpose of the output: internal brief, systematic review draft, or decision memo.
- Date range, languages, and geographic scope.
- Access status of each registry or database. Credentials, API keys, and terms of use are the user's responsibility; never request or store them in outputs.

Assumptions to state explicitly in the deliverable: the search snapshot date, the sources actually reachable, and any source that could not be queried.

## Operating workflow

1. **Frame.** Restate the question in one sentence and list inclusion and exclusion criteria. Freeze them before searching.
2. **Map sources.** Choose registries matching the question: trial registries for ongoing or unpublished work, bibliographic databases for published literature, preprint servers for recent work (flagged as unreviewed). Record each source's coverage limits.
3. **Search.** Build one query per source with the same concepts. Log the exact query string, field restrictions, and the date run. Do not invent field tags or syntax; confirm them against each source's current documentation.
4. **Deduplicate.** Match records by identifier first (DOI, registry ID), then by normalized title, first author, and year. Record the merge count.
5. **Screen.** Apply title/abstract screening, then full-text screening, each by two passes where feasible. Record a reason code for every exclusion.
6. **Extract.** Use a fixed extraction sheet: design, sample size, population, intervention, outcome definitions, effect estimate with interval, follow-up, funding, conflicts, registration ID and whether reported outcomes match the registered ones.
7. **Appraise.** Rate risk of bias with an instrument appropriate to the design (for example, a randomized-trial or observational-study tool). Name the tool and version, and verify the version against its current official source.
8. **Synthesize.** Describe findings narratively, grouped by outcome. Pool only when studies are comparable in population, measure, and design. Report heterogeneity rather than hiding it.
9. **Draft and cite.** Attribute every claim to a record ID. Separate what registries say from what publications report.

## Decision gates

- **Gate A (before searching):** Question and criteria frozen and approved by the requester.
- **Gate B (before pooling):** Stop if fewer than two comparable studies exist, or if heterogeneity makes a single estimate misleading. Report narratively instead.
- **Gate C (before external sharing):** Any output containing unpublished registry data, personal data, or proprietary material requires explicit approval before it leaves the working context.
- **Gate D (before posting anywhere):** Any submission, registry update, or message to a third party requires explicit approval, with the exact text shown first.

## Verification and evidence

Quality checks, each must pass or be reported as failed:
- Every included study has a stable identifier and a link or retrieval note.
- Search logs are reproducible: source, query, date, record count.
- Two independent screening decisions agree on at least 90% of records, or disagreements are resolved and logged.
- Each effect estimate is traceable to a specific table, figure, or registry field.
- Outcomes reported in publications are compared with those registered; discrepancies are listed.
- Preprints and non-peer-reviewed sources are labeled.

## Failure handling

- **Source unreachable or rate-limited:** Record the failure, do not substitute memory or recall, and mark the gap in the deliverable.
- **Conflicting numbers across sources:** Report both with sources; do not average silently.
- **Retracted or corrected records:** Check the retraction notice and exclude or annotate.
- **Ambiguous eligibility:** Log the record in an uncertain list and ask the requester rather than deciding alone.

## Deliverable contract

Return:
1. Question, criteria, and snapshot date.
2. Source list with coverage limits and access status.
3. Search logs and PRISMA-style flow counts.
4. Extraction table with record IDs.
5. Risk-of-bias summary with tool names and versions flagged for verification.
6. Narrative synthesis with explicit uncertainty and contradictions.
7. Gaps, limitations, and open questions.

Do not:
- Present unverified citations or identifiers.
- Claim completeness of a search.
- Imply regulatory approval or clinical endorsement.
- Fabricate effect sizes, benchmark results, or version numbers.

## Ultron routing contract

**Choose this skill when:** conducting a structured scientific literature or registry review: framing a research question, designing searches, screening sources, extracting findings, appraising study quality, and synthesizing results with traceable provenance.

**Choose scientific-evidence-review when:** the task is to test a specific claim or artifact against the evidence it cites, rather than discover and synthesize a whole body of research.

**Handoff contract:** this skill supplies the search strategy, inclusion/exclusion criteria, source log, extracted findings, and synthesis. The evidence-review skill returns claim-level support and limitations for important conclusions; integrate those verdicts without overstating certainty or implying causal conclusions unsupported by study design.

**Why the boundary exists:** synthesis answers what the body of evidence suggests; evidence review tests whether an individual claim follows from its stated support.
