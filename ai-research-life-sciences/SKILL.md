---
name: ai-research-life-sciences
description: Use when an AI-assisted task needs to search, retrieve, cross-check, or summarize life-sciences evidence from external registries and databases such as literature indexes, clinical trial registries, sequence and structure archives, bioactivity databases, and preprint servers.
author: Luo Kai
provenance: original
version: 1.0.0
---

# AI Research for Life Sciences

## Purpose and boundaries

This skill governs how to find, verify, and synthesize life-sciences records from external registries for research support: literature reviews, trial landscape scans, target or variant lookups, compound and bioactivity checks, and dataset discovery.

In scope: query design, record retrieval, deduplication, provenance tracking, cross-registry reconciliation, and evidence-graded summaries.

Out of scope: clinical decisions for individual patients, dosing recommendations, regulatory submissions, wet-lab protocol design, and any output presented as validated medical advice. Route those to qualified humans.

## Inputs and assumptions

Before searching, establish:

1. The research question in one sentence, with population, intervention or entity, comparator, and outcome where applicable.
2. The decision the output will inform (e.g., shortlisting targets, scoping a review, checking prior trials).
3. Date window and recency requirement.
4. Which registries the user has access to. Do not assume institutional subscriptions or API keys.
5. Whether the user has supplied data files, which may contain confidential or patient-level content.

If any item is missing and changes the search, ask once. Otherwise state the assumption in the output.

## Operating workflow

1. **Decompose the question** into entity sets (genes, proteins, compounds, diseases, outcomes) and map each to registry-specific identifiers. Record the mapping table.
2. **Draft queries per registry** using controlled vocabularies where available (e.g., MeSH for literature, condition and intervention fields for trial registries, gene symbols plus species for sequence archives). Save each query string verbatim.
3. **Retrieve in tiers**: broad recall first, then filter by study design, date, and identifier validity. Log hit counts at each step.
4. **Deduplicate** using stable identifiers (DOI, PMID, NCT number, accession, InChIKey) before fuzzy title matching. Merge preprint and peer-reviewed versions and flag the relationship.
5. **Extract structured fields** into a table: source, identifier, date, design or assay type, population or system, key quantitative result, limitations stated by authors.
6. **Cross-check** claims against at least one independent registry where possible (e.g., a trial result against its registry entry and the published report; a bioactivity value against the original assay source).
7. **Grade evidence** (see Verification).
8. **Write the synthesis** separating what the sources report from what you infer.

## Decision gates

- **Gate A, scope:** If the question yields more than roughly 2,000 candidate records, narrow with the user before extracting. Do not silently sample.
- **Gate B, source quality:** Preprints, predatory-venue articles, and unregistered trials are reported only with an explicit quality flag. Never cite them as established.
- **Gate C, conflicts:** If registries disagree (e.g., enrollment counts, accession versions, compound identifiers), report both values with sources and do not pick one without a stated rule.
- **Gate D, external actions:** Submitting queries at volume, using credentials, downloading restricted or licensed data, or posting results to any external system requires explicit user approval. Rate-limit and respect terms of use.
- **Gate E, sensitive data:** If inputs contain identifiable patient data, stop and confirm the handling basis and whether the data may leave the local environment.

## Verification and evidence

- Every factual claim carries a source identifier. Claims without one are labeled "unverified inference."
- Verify each identifier resolves to the record cited, and that the record date and version match what is quoted.
- Quantitative values are copied with units and denominators; never rounded silently.
- Benchmark or performance statements are reported only from the source, never recalled from memory.
- Evidence labels: *primary report*, *registry entry*, *secondary review*, *preprint*, *model-generated inference*.
- Quality checks before delivery: 100% of cited identifiers resolved; zero duplicate records in the final table; every excluded record has a logged reason; every conflict is listed.
- API names, parameters, field names, and schema versions change. Mark any such detail "verify against current official documentation" and do not state it from memory as current.

## Failure handling

- **Registry unavailable or rate-limited:** Record the timestamp and endpoint attempted, pause, and report partial coverage with the gap named explicitly.
- **Zero hits:** Broaden one dimension at a time (synonyms, parent terms, species), logging each attempt. Report the null result as a finding with the queries used.
- **Identifier mismatch:** Do not guess the correct record. Mark it unresolved.
- **Retracted or withdrawn source discovered:** Remove it from supporting evidence, list it in a separate exclusions section, and check dependent conclusions.

## Deliverable contract

Return:

1. **Question and scope** (restated, with assumptions).
2. **Query log** (registry, query string, date run, hit count).
3. **Evidence table** (source ID, date, design or type, key result, evidence label, quality flag).
4. **Conflicts and gaps** (listed, not resolved by fiat).
5. **Synthesis** (short, with inferences marked).
6. **Limitations and verification items** (version-sensitive details, unresolved identifiers, access limits).

Do not include: uncited numerical claims, invented accession numbers, recalled benchmark figures, guarantees of completeness, or clinical recommendations.