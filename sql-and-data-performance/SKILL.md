---
name: sql-and-data-performance
description: Use when diagnosing, writing, or reviewing SQL queries, schema indexes, or data-processing jobs where latency, cost, lock contention, or throughput must be measured and improved without changing query results.
author: Luo Kai
provenance: original
version: 1.0.0
---

# SQL and Data Performance

## Purpose and boundaries

This skill covers making SQL and set-based data workloads faster or cheaper while preserving semantic correctness. It applies to relational engines (PostgreSQL, MySQL, SQL Server, Oracle, and similar), analytical warehouses, and SQL-driven ETL. It does not cover application-level caching design, hardware procurement, or general data modeling decisions unless they directly block a query fix. Engine-specific syntax, planner behavior, and configuration parameters change between versions; treat any specific option named during analysis as requiring verification against current official documentation for the exact engine version in use.

## Inputs and assumptions

Before changing anything, collect:

1. The exact query text, parameter sample values, and the engine and version.
2. Table row counts, column types, existing indexes, partitioning, and statistics freshness.
3. The execution plan actual-versus-estimated output, captured with runtime statistics where the engine supports it.
4. The target: p95 latency, daily cost, rows scanned, or lock wait budget.
5. Production constraints: read-only access, change windows, replication lag tolerance.

If any of these are missing, state the assumption explicitly in your output. Do not assume a plan is representative from a development database with different cardinality.

## Operating workflow

1. **Establish a baseline.** Run the query three times under comparable conditions and record median runtime, rows read, rows returned, and memory or bytes scanned.
2. **Verify correctness first.** Save the current result as a reference, using a checksum over ordered output or an aggregate comparison, so every candidate rewrite can be checked against it.
3. **Read the plan top-down.** Find the operator with the largest actual cost or largest gap between estimated and actual row counts. A misestimate above roughly an order of magnitude usually points to stale statistics, skewed data, or predicates that hide selectivity from the planner.
4. **Classify the bottleneck.** Choose one: full scan on a selective predicate, non-sargable filter (functions or implicit casts on indexed columns), join order or join type problem, sort or spill to disk, repeated subquery execution, excessive round trips, lock contention, or over-fetching of columns and rows.
5. **Apply one change at a time.** Change one variable per experiment so the effect is attributable.
6. **Re-measure and re-verify.** Compare against the baseline and the reference result.

## Decision gates

- **Index additions:** Add an index only when the query runs frequently enough that its write overhead is justified, and when the proposed key order matches equality predicates before range predicates. Estimate write amplification on the affected table.
- **Rewriting predicates:** Rewrite a function-wrapped predicate into a sargable form only when the rewrite is provably equivalent for the column's type, collation, and nullability. Confirm with the reference result on edge values including NULL, empty strings, and boundary dates.
- **Denormalization or materialized results:** Propose only when the refresh cadence and staleness tolerance are documented by the data owner.
- **Changes touching production:** Any DDL, index creation, statistics refresh, or job schedule change requires explicit approval from the data owner. Index builds on large tables can block writes or consume I/O; request approval with the expected duration and the chosen online or concurrent build option, verified against engine documentation.
- **Stop condition:** If the best candidate improves runtime by less than the measured run-to-run variance, do not ship it.

## Verification and evidence

Every claim of improvement must cite:

- Baseline and candidate median runtimes over at least three runs, with the variance range.
- Rows read and rows returned before and after.
- The plan diff showing which operator changed.
- A result equality check that passed on the reference parameter set and at least one additional parameter set with different selectivity.

Do not report percentage gains without absolute numbers. Do not state benchmark outcomes for an engine or dataset you did not measure.

## Failure handling

- **Result mismatch:** Discard the candidate immediately. Do not patch around it by adding DISTINCT or ORDER BY without understanding the cause.
- **Plan regression on other parameters:** Parameter-sensitive plans are common. Report the regression with the parameter values that trigger it and propose either a parameter-specific approach or accept the trade-off explicitly.
- **Statistics or plan cache confusion:** Confirm whether the plan was recompiled before concluding that a change worked.
- **Measurements disagree:** Check for cache warm-up, concurrent load, and differing session settings before trusting the result.

## Deliverable contract

Return a report containing, in order:

1. Summary: the bottleneck class, the change made, and the measured effect with absolute numbers.
2. Baseline and candidate tables: runtime, rows read, rows returned, and memory or spill data.
3. The final query or DDL, marked as proposed until approved.
4. Verification results: equality checks and parameter coverage.
5. Risks: write overhead, lock impact, version-sensitive behavior to confirm, and rollback steps.
6. Open items: assumptions not yet validated and approvals still required.

Do not include unmeasured speedup estimates, do not recommend production DDL without the approval gate above, and do not claim the change is safe for all parameter values unless those values were tested.