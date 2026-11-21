---
name: gene-information-genomics
description: Use when retrieving, reconciling, curating, or interpreting gene-level information (identifiers, coordinates, sequences, annotations, orthologs, variants, expression, pathway or compound-target links) across chemistry and biology resources, or when preparing gene-annotation tables for analysis.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Gene Information Genomics

## Purpose and boundaries

This skill covers the practical handling of gene-level facts: which gene a name or identifier refers to, where it sits in a specified genome build, which transcripts and proteins it produces, what it is orthologous to, and which compounds, pathways, or variants are linked to it. It produces reconciled, traceable gene annotation tables and short evidence-backed interpretations.

It does not cover wet-lab design, clinical diagnosis, treatment decisions, or de novo genome assembly. Output is research support and must be checked by a qualified domain expert before use in decisions affecting people, animals, or regulated submissions.

## Inputs and assumptions

Before acting, establish and record:

1. **Organism and taxon ID.** Gene symbols are only meaningful within a species. Never assume human.
2. **Genome build or release.** Coordinates are build-specific. Record the assembly name and annotation release for every coordinate.
3. **Identifier type supplied.** Symbol, Entrez-style ID, Ensembl-style gene or transcript ID, UniProt accession, RefSeq accession, HGNC ID, or chemical–target identifier.
4. **Question type.** Identity lookup, coordinate mapping, ortholog mapping, compound–target linkage, variant annotation, or expression context.
5. **Data sensitivity.** Determine whether any input contains human individual-level genotypes, patient identifiers, or unpublished proprietary sequences.

If the organism, build, or identifier type is missing and cannot be inferred from the file headers or the user's context, stop and ask.

## Operating workflow

1. Normalize identifiers. Strip whitespace, fix case according to the nomenclature authority for that species, and flag symbols that are known aliases or previous symbols.
2. Resolve each identifier to a stable primary key (for example, a curated nomenclature ID plus a stable gene ID). Store every raw input alongside its resolved key.
3. Map coordinates only within a single declared build. If a conversion between builds is needed, use the official mapping tool or chain file for that pair, and label the result as converted.
4. Expand to transcripts and proteins by selecting a canonical transcript using a named rule (for example, the database's canonical flag or longest coding isoform), and report the rule used.
5. For orthology, record the method and source (curated versus inferred). Report one-to-many relationships rather than forcing one-to-one.
6. For chemistry links, record the compound identifier, the interaction type (inhibitor, agonist, substrate, binder, unknown), the assay or evidence class, and the source. Keep "binds" distinct from "modulates activity."
7. Write the table, a provenance log (source, retrieval date, release version), and a list of unresolved records.

## Decision gates

- **Build mismatch:** if inputs mix builds, stop and reconcile before any coordinate-based analysis.
- **Ambiguous symbol:** if a symbol maps to more than one gene, do not pick one silently. Keep all candidates and request confirmation.
- **Sensitive data:** do not send individual-level human genotype data, patient identifiers, or unpublished sequences to any external web service or API without explicit user approval and a confirmed data-use basis.
- **Overwrite or delete:** do not overwrite existing curated annotation files, merge into shared databases, or delete records without explicit approval. Write to new versioned outputs.
- **External-impacting actions:** submitting data to public repositories, emailing collaborators, or publishing annotations requires explicit approval.
- **Clinical or regulatory use:** if the output is intended for diagnosis, dosing, or a regulatory filing, stop and state that expert and validated-pipeline review is required.

## Verification and evidence

- Round-trip check: resolved IDs must map back to the original symbol or accession in the same organism. Target 100% for unambiguous inputs; report every exception.
- Coordinate sanity check: start is less than or equal to end, chromosome name matches the build's naming convention, and gene length is consistent with the annotation.
- Count reconciliation: rows in equals rows out, plus a documented list of dropped or flagged records.
- Evidence tagging: every assertion carries one of: curated, computed-from-release, inferred, or user-supplied.
- Version-sensitive details (release numbers, API endpoints, tool flags, database schema fields) must be checked against current official documentation before being stated as fact. Mark any unverified detail as such.
- Do not report performance figures or database coverage statistics unless they were measured in the current session.

## Failure handling

- If a resource is unreachable, report the failure, the query attempted, and the time. Do not substitute memory for live data without labeling it as unverified.
- If a symbol is withdrawn or renamed, report the current symbol and the previous one, and keep both.
- If canonical transcript rules conflict between sources, report both and do not average or merge them.
- If results contradict across sources, present the disagreement with each source's evidence class; do not resolve it by choosing the more convenient answer.

## Deliverable contract

Return:

1. Summary: organism, build, identifier type, record counts (resolved, ambiguous, unresolved).
2. Annotation table with raw input, resolved primary key, symbol, coordinates (with build), canonical transcript and rule, ortholog or compound links with evidence class.
3. Provenance log: sources, release versions, retrieval dates, mapping tools used.
4. Open items: ambiguous records, required approvals, and claims that need expert verification.

Do not present unverified specifics as settled. Do not generate identifiers, coordinates, or interaction claims that were not retrieved or supplied.