---
name: data-modeling
description: Use when designing, reviewing, or migrating relational or analytical data models, including entity definitions, keys, normalization or dimensional choices, constraints, and schema change plans for databases and data warehouses.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Data Modeling

## Purpose and boundaries

This skill produces and reviews data models: entities, attributes, keys, relationships, constraints, and their physical translation for a chosen engine. It covers transactional (OLTP) schemas, analytical (star or snowflake) schemas, and incremental changes to existing schemas.

Out of scope: choosing a database vendor, tuning query plans on production systems, writing ETL orchestration, and designing access control policies. Name these as adjacent work and stop at the model boundary.

## Inputs and assumptions

Collect before modeling. If any item is missing, record it as an assumption with a stated owner:

- Business processes and the questions the model must answer, with example queries.
- Grain: what one row in each table represents.
- Volume estimates, growth rate, and update frequency per entity.
- Source systems and their identifiers, including whether identifiers are reused or mutable.
- Target engine and version. Engine-specific types, index options, and DDL syntax must be checked against current official documentation for that version.
- Regulatory or sensitivity classification of fields (personal, financial, health). Flag these; do not decide retention or masking alone.

## Operating workflow

1. Write the grain statement for every table in one sentence. Reject any table whose grain cannot be stated.
2. List candidate entities from nouns in the business process. Mark each as entity (has independent identity and lifecycle), event (immutable occurrence), or attribute (no independent identity).
3. Assign a primary key per table. Prefer natural keys only when they are stable, unique, and issued by an authority the business trusts; otherwise use a surrogate key and keep the natural key as a unique constraint.
4. Define relationships with cardinality and optionality in both directions. Resolve every many-to-many relationship with an associative table that carries its own attributes and key.
5. Normalize OLTP models to third normal form as the default. Denormalize only under a documented reason (measured read cost, a fixed reporting requirement) and record which columns are derived and how they are refreshed.
6. For analytical models, use a dimensional design: one fact table per business process at a declared grain, conformed dimensions shared across facts, additive measures where possible, and explicit handling for slowly changing attributes (state the type chosen per attribute).
7. Specify constraints in the model, not only in application code: not-null, unique, foreign keys, check constraints for domains and ranges, and allowed-value lists.
8. Map each logical element to physical types for the target engine, recording precision for decimals, time zone semantics for timestamps, and maximum lengths for text.
9. Produce a change plan for any existing schema: additive changes first, backfill in batches, dual-read or dual-write only if the application requires it, and removal of old structures in a separate later release.

## Decision gates

- **Surrogate versus natural key:** use natural keys only if they are immutable and verified unique across all sources. Otherwise use surrogates.
- **Normalize versus denormalize:** denormalize only with a measured or stated read requirement and a named refresh mechanism. Absent both, keep normalized.
- **Slowly changing dimension type:** Type 1 (overwrite) only when history has no business value. Type 2 (versioned rows) when reports must reflect the value at the time of the event. Type 3 only for a single prior value that users explicitly need.
- **Soft versus hard delete:** soft delete requires a documented rule for every query that reads the table. Hard delete requires confirmation that no downstream consumer or audit requirement depends on the row.
- **Schema change type:** if a change drops, renames, or narrows a column or changes its type, it is a breaking change and needs approval from every consuming team before execution.

## Verification and evidence

- Every table has a stated grain, primary key, and at least one documented example row set.
- Every foreign key has a matching parent key, and orphan counts against sample production data are reported as zero or explained.
- Uniqueness claims are tested with a duplicate-count query on representative data; report the query and result.
- Fact tables: confirm the grain by checking that the primary key (or declared composite key) has zero duplicates.
- Each stated business question is answered by a written query against the model. Queries that cannot be written indicate a modeling gap.
- Migration plans include row-count reconciliation and checksum or aggregate comparison between old and new structures before cutover.
- Physical DDL is validated against the target engine version in a non-production environment. State the version tested.

## Failure handling

- If the grain cannot be agreed, stop and escalate to the business owner; do not model around ambiguity.
- If source identifiers collide, do not merge records automatically. Propose a reconciliation key and list collision samples for review.
- If a duplicate-count check fails, halt the design step and identify the upstream cause before revising the key.
- If a proposed change would lock or rewrite a large table, flag the operational risk and request a maintenance window decision.

## Deliverable contract

Return a document containing, in order:

1. Scope statement and assumptions with owners.
2. Entity list with grain, key, and classification for each table.
3. Relationship summary with cardinality and optionality.
4. Constraint list and physical type mapping for the named engine version.
5. Decisions log: each gate decision with rationale and alternatives rejected.
6. Verification results: queries run, row counts, duplicate and orphan checks, and open items.
7. Migration or change plan, if applicable, with rollback steps.

## Safety and approvals

Obtain explicit written approval before: dropping, renaming, or narrowing any production column or table; running any backfill or rewrite against production data; changing keys or constraints on populated tables; and classifying or moving personal, financial, or health data into new structures. Do not execute DDL against shared or production environments. Do not state that a design satisfies a regulation or certification; state only which controls it supports and flag the rest for compliance review.

## What not to do

- Do not model every field from a source system by default; model only what the stated questions and processes require.
- Do not use generic columns such as `data`, `attributes`, or `misc` to avoid design decisions.
- Do not add indexes, partitioning, or engine-specific features without a stated query pattern they serve.
- Do not invent performance figures; report only measured results.