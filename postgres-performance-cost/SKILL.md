---
name: postgres-performance-cost
description: Use when diagnosing PostgreSQL query latency, throughput, or infrastructure cost problems, or when evaluating schema, index, configuration, or capacity changes whose performance and cost impact must be measured before rollout.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Postgres Performance Cost

## Purpose and boundaries

This skill guides evidence-based analysis of PostgreSQL performance and its cost footprint. It covers query plan analysis, index design trade-offs, configuration review for memory and I/O, write-amplification and bloat assessment, connection pressure, and right-sizing of compute and storage against measured workload.

It does not cover: application architecture redesign, choosing a different database engine, managed-provider billing negotiation, security hardening, or backup/restore design. Route those to the appropriate skill.

## Inputs and assumptions

Collect before recommending anything:

- PostgreSQL major and minor version, hosting type (self-managed, managed service, container), and instance class with storage type.
- The exact slow statements (normalized text plus one representative bound example), frequency, and the business path they serve.
- Output of `EXPLAIN (ANALYZE, BUFFERS)` on a representative dataset, or a clear reason it cannot be run in the target environment.
- Statistics snapshots from the statistics views (`pg_stat_statements` if enabled, table and index usage counters), with the reset timestamp.
- Current values of memory, parallelism, WAL, checkpoint, and autovacuum settings, and whether they were changed from defaults.
- Table sizes, row counts, growth rate, and write-to-read ratio.
- Cost data: monthly compute, storage (provisioned and used), I/O, and backup charges, with the billing period.

Assumptions must be stated explicitly. If the data came from a non-production copy, say so and state how statistics may differ.

## Operating workflow

1. Establish a baseline. Record p50, p95, and p99 latency and calls per minute for the top statements over a representative window. Note cache hit ratio and temp file usage.
2. Rank cost drivers. Multiply average time by call count to find total time consumed. Optimize the largest share first, not the single slowest query.
3. Read the plan. Compare estimated and actual row counts. A misestimate above roughly an order of magnitude is a statistics or correlation signal. Check for sequential scans on large tables, nested loops over large inputs, sorts or hashes spilling to disk, and repeated subplans.
4. Classify the root cause: missing or unusable index, stale statistics, poor join order from correlated columns, query shape, lock waits, bloat, memory misconfiguration, or undersized hardware.
5. Form one hypothesis per change. Write the expected effect as a measurable delta (for example, "buffers read drops substantially for the plan node on the orders table").
6. Test in a staging environment with comparable data volume and the same version and settings. Repeat runs to observe variance; discard cold-cache outliers unless cold-start behavior matters.
7. Quantify the trade-off. An index speeds reads but adds write cost, storage, and vacuum work. Measure write latency and table size before and after.
8. Prepare rollout and rollback steps, then request approval.

## Decision gates

- Adding an index: proceed only if the statement's total time share justifies it, the index serves multiple queries or a critical one, and write-path impact on the table is measured. Prefer a partial or covering index when the predicate or column set is narrow. Index creation on large live tables requires an approach that avoids long locks; confirm the concurrent build option and its limitations against current documentation before use.
- Changing configuration parameters: proceed only with a stated reason tied to observed metrics (for example, temp file spills indicating insufficient work memory for specific sessions). Change one parameter group at a time. Do not tune memory parameters by percentage rules alone.
- Rightsizing instance or storage: proceed only with at least one full business cycle of utilization data showing sustained headroom. Reducing capacity is a production-impacting change and requires approval.
- Statistics or vacuum tuning: proceed only after confirming dead tuple counts and last analyze times. Per-table settings are preferred over global changes.
- Any destructive action (dropping indexes or tables, resetting statistics, terminating sessions, deleting data, changing replication or failover settings) requires explicit written approval from the data owner.

## Verification and evidence

A recommendation is complete only when it includes:

- Before and after `EXPLAIN (ANALYZE, BUFFERS)` output for the target statement, with identical parameters and data state.
- Latency distribution and call rate before and after, over comparable windows.
- Write-side measurements for any index or trigger change: insert/update latency and index size growth.
- Projected cost delta, shown as a calculation from measured inputs, labeled as an estimate.
- A list of settings and versions verified against current official PostgreSQL documentation, and any provider-specific behavior that was not verified.

Reject claims such as "should be faster" without a measured or reproducible result.

## Failure handling

- If the plan changes but latency does not improve, re-check whether the statement is the real bottleneck; look at lock waits and client-side time.
- If staging results diverge from production, identify data skew, cache state, or settings drift before drawing conclusions.
- If statistics appear missing, do not reset them without approval; document the gap and collect a fresh window.
- If a change regresses write throughput beyond the agreed threshold, roll back and report the measured regression.
- If required data is unavailable, state which conclusions are blocked and what data would unblock them. Do not fill gaps with typical values.

## Deliverable contract

Produce a single report containing:

1. Summary: the top problem, its share of total database time or cost, and the recommended action.
2. Evidence table: statement, calls, mean and p95 latency, buffers, plan signature, before and after.
3. Proposed changes, ordered by expected impact, each with rationale, risk, rollback step, and approval status.
4. Cost impact: measured inputs, calculation method, and an explicit estimate label.
5. Open questions and unverified items, including version-sensitive details pending documentation check.

Do not: recommend changes based on generic rules of thumb, apply production changes without approval, drop or rebuild objects without a rollback plan, or present estimates as measured results.