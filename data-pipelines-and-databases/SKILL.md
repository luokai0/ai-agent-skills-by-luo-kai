---
name: data-pipelines-and-databases
description: Use when designing, building, debugging, migrating, or reviewing data pipelines, ETL/ELT jobs, warehouse or lakehouse tables, database schemas, or query performance, and when a change could affect data correctness, freshness, lineage, or recoverability.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Data Pipelines And Databases

## Purpose and boundaries

This skill guides work on moving, transforming, storing, and serving structured and semi-structured data: ingestion jobs, transformation logic, schema design and migrations, indexing and query tuning, data quality checks, and operational reliability of pipelines.

In scope: pipeline design, idempotency and backfill strategy, schema and migration review, data contracts, quality tests, reconciliation, query plan analysis, and incident triage for data defects.

Out of scope: model training pipelines (use an ML-specific skill), application UI work, general cloud infrastructure provisioning, and compliance certification. This skill does not certify that a system meets any regulation.

## Inputs and assumptions

Before acting, establish:

1. Source systems, their owners, and update semantics (append-only, mutable, CDC, full snapshot).
2. Target system and engine, with its exact version. Treat engine features as version-sensitive until checked against current official documentation.
3. Freshness requirement, volume (rows and bytes per run), and retention rules.
4. Current schema, row-count and key-uniqueness baselines, and any existing tests.
5. Downstream consumers and the contract they rely on (columns, grain, latency, null semantics).

If any of these is unknown, state the assumption explicitly in the deliverable. Do not guess table names, column types, or engine capabilities.

## Operating workflow

1. **Define the grain.** Write one sentence stating what one row represents and the natural key. Every later check depends on this.
2. **Map lineage.** List each upstream input and each output table. Note which outputs are rebuilt versus incrementally updated.
3. **Choose load semantics.** Prefer deterministic overwrite of a partition or window over row-by-row patching. Require that re-running the same window yields the same result (idempotency).
4. **Specify late and out-of-order data.** Decide a lookback window or reprocessing rule and document what happens to records arriving after it.
5. **Design schema changes as expand-then-contract.** Add nullable columns or new tables first, backfill, switch readers, then remove old structures in a later release.
6. **Write quality checks before transformation code.** Minimum set: primary-key uniqueness, not-null on keys, referential coverage for joins, row-count delta against expected range, and freshness timestamp.
7. **Implement in small, reviewable steps.** One logical change per commit or migration file.
8. **Test on a bounded sample** (for example, one partition or a fixed date range) and compare against a trusted baseline before any full run.
9. **Plan backfill** in ordered windows with checkpoints, resource limits, and a stop condition.
10. **Document operations:** schedule, owner, alert thresholds, rerun procedure, and rollback path.

## Decision gates

Stop and request explicit human approval before:

- Dropping, truncating, or overwriting any table, partition, or dataset outside a disposable staging scope.
- Running a backfill that rewrites more than one partition of production data.
- Changing primary keys, grain, or the meaning of an existing column consumed by others.
- Altering access controls, masking rules, or retention settings.
- Sending data to an external service, third-party API, or any destination outside the approved environment.
- Running a migration that cannot be reversed from a verified backup or snapshot.
- Any action touching personal or otherwise sensitive data beyond what the task already authorized.

Proceed without a gate when work is read-only, runs against a dev or staging copy, or is confined to new objects that no consumer reads yet.

## Verification and evidence

A change is not complete until evidence exists for each item below:

- **Uniqueness:** zero duplicate natural keys in the output for the tested window.
- **Reconciliation:** source-to-target counts or sums match within a stated tolerance, with any difference explained (filters, dedup, late data).
- **Idempotency:** a second run over the same window produces identical row counts and a matching content hash or checksum.
- **Null and type behavior:** nulls and casts verified on at least the edge values present in the sample (empty strings, zero, out-of-range dates, unicode).
- **Query performance:** for changed queries, an execution plan or engine profile before and after, showing scanned volume and join strategy. Report measured numbers only.
- **Migration safety:** migration applied to a copy, rollback or forward-fix path tested, and old readers confirmed compatible.

Do not claim performance improvements, correctness, or compliance without the corresponding measurement. Record the commands run and their outputs.

## Failure handling

- **Count mismatch:** halt downstream publishing, identify the first filter or join where counts diverge, and report the delta with examples.
- **Duplicate keys:** do not silently deduplicate. Determine whether the source is wrong, the join fans out, or the grain was misdefined.
- **Failed backfill window:** stop at the failed window, keep completed windows, and resume from the checkpoint. Never restart from zero without approval.
- **Schema drift at source:** fail fast on unexpected types or missing required columns; quarantine bad records to a separate location with a reason code rather than coercing them.
- **Lock or timeout in production database:** cancel, do not retry in a loop, and reduce batch size or schedule off-peak after review.
- **Unknown root cause:** say so, list the hypotheses tested, and stop rather than applying a speculative fix.

## Deliverable contract

Every deliverable includes:

1. Grain statement and natural key.
2. Lineage summary (inputs, outputs, rebuild or incremental mode).
3. Code or migration artifacts, each with a stated purpose.
4. Quality checks implemented, with thresholds and alert destinations.
5. Verification results: counts, uniqueness, idempotency, and performance measurements with the exact method used.
6. Assumptions and open questions, listed explicitly.
7. Operational notes: schedule, owner, rerun and rollback steps.
8. Pending approvals, if any gate was reached.

What not to do: do not hard-code dates or environment names without parameters; do not use `SELECT *` in production transformations feeding shared tables; do not mix schema changes and data backfills in one unreviewed step; do not hide errors with broad exception handling; do not leave TODO markers or placeholder thresholds in delivered artifacts.