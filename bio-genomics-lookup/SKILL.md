---
name: bio-genomics-lookup
description: Use when a user needs to look up gene, variant, transcript, or genome-annotation information from public genomics databases and return verified, source-cited answers for research or analysis work.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Bio Genomics Lookup

## Purpose and boundaries

This skill resolves biological identifiers and retrieves annotation facts (gene symbols, coordinates, transcripts, protein products, variant records, clinical-significance labels, cross-references) from public reference databases, then reports them with provenance. It covers lookup and reconciliation, not interpretation of patient data, clinical decisions, or novel bioinformatic pipelines.

In scope: symbol-to-identifier mapping, genome build conversion checks, canonical transcript selection, variant identifier normalization, reporting of database-asserted annotations, and flagging conflicts between sources.

Out of scope: diagnosing conditions, recommending treatments, classifying variants for clinical reports without a qualified reviewer, uploading identifiable genetic data to external services, and asserting results that were not retrieved in the current session.

## Inputs and assumptions

Collect before querying:

1. The query type: gene, transcript, protein, variant, region, or cross-reference.
2. The identifier as given (symbol, Ensembl ID, RefSeq accession, HGVS string, rsID, genomic coordinate).
3. The target genome assembly (for example GRCh38 or GRCh37). If absent, state the assumption explicitly and report both builds when coordinates matter.
4. The intended use: exploratory, manuscript, or input to a downstream tool. Higher stakes require stricter gates.
5. Whether the query includes any personal or patient-linked data. If yes, stop and see Decision gates.

Assumptions to state in every output: the database versions consulted and the retrieval date. Symbols are mutable; accessions are more stable. Prefer stable identifiers for reporting.

## Operating workflow

1. **Classify the identifier.** Match the string against known formats: HGNC symbol, Ensembl gene (ENSG), transcript (ENST), protein (ENSP), RefSeq (NM_, NP_, NC_), dbSNP rsID, HGVS notation, or coordinates. Ambiguous symbols (for example names that collide with aliases) require a check against the official nomenclature authority.
2. **Resolve to a stable identifier.** Map the input to one gene record and one assembly. Record the mapping path.
3. **Retrieve core fields.** Symbol, full name, chromosome, start, end, strand, biotype, canonical transcript, and cross-references.
4. **Retrieve variant fields if applicable.** Reference and alternate alleles, HGVS forms (genomic, coding, protein), consequence terms, population frequency summaries, and submitted clinical-significance records, each labeled with its source and review status.
5. **Cross-check.** Compare coordinates and symbols across at least two sources where feasible. Note discrepancies rather than silently choosing one.
6. **Compose the answer** using the Deliverable contract.

## Decision gates

- **Gate A: Identifier ambiguity.** If the input matches more than one record, stop and present candidates with assembly and biotype. Do not pick silently.
- **Gate B: Assembly mismatch.** If a user's coordinates lack a build, or they conflict with the requested build, request confirmation before conversion. Use an official liftover tool and report the chain used.
- **Gate C: Sensitive data.** If the query contains patient identifiers, individual genotypes, or any data that could identify a person, pause and request explicit approval before any external lookup. Prefer offline reference files supplied by the user.
- **Gate D: External submission.** Sending identifiers to a remote service is an external action. Confirm with the user first when the query includes non-public variants or unpublished gene lists.
- **Gate E: Clinical use.** If the stated purpose is clinical reporting, return the retrieved records only, label them as unreviewed database assertions, and recommend review by a certified professional. Do not produce a pathogenicity call.

## Verification and evidence

Every factual claim in the output must trace to a retrieved record. Include for each claim: source database, record identifier, assembly, and retrieval date.

Quality checks before delivery:
- Symbol, Ensembl ID, and chromosome location agree across the cited records (or the disagreement is reported).
- Coordinates satisfy start less than or equal to end, and strand is one of plus or minus.
- Canonical transcript is named by the source's canonical flag, not by inference.
- Variant HGVS strings re-parse against the reference allele at the stated position where a validator is available.
- No field is filled from memory. If a field could not be retrieved, write "not retrieved."

Version-sensitive details (database release numbers, API endpoints, field names, query parameters, rate limits) must be checked against current official documentation before being stated. Do not present them from memory.

## Failure handling

- **Service unreachable or rate-limited:** retry once after a short wait, then report the failure and the partial results. Do not fill gaps from prior knowledge.
- **No match found:** check for outdated symbols, retired accessions, and alias tables. Report the search steps taken.
- **Conflicting sources:** present both values with their sources and state which the user should adopt for their assembly.
- **Assembly mismatch discovered after answering:** issue a correction stating the affected fields and the corrected values.

## Deliverable contract

Return a structured answer with these parts, in order:

1. **Query:** the input exactly as received, with query type and assumed assembly.
2. **Resolved record:** stable identifiers, symbol, coordinates, strand, biotype, canonical transcript.
3. **Findings:** labeled fields, each with source, record ID, and retrieval date.
4. **Discrepancies:** conflicts or "none found."
5. **Limitations:** unretrieved fields, version caveats, and any gate that was triggered.

Do not state that results are clinically valid, guaranteed, or complete. Do not invent identifiers, frequencies, or significance labels. Do not reproduce large sequence blocks unless the user explicitly requests them and the gate for external submission has been cleared.