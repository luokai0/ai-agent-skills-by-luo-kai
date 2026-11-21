---
name: nosql-search-cache
description: Use when designing, reviewing, or troubleshooting NoSQL document/key-value stores used for search indexes, query result caches, or cache-aside layers, including TTL, invalidation, index sizing, and consistency tradeoffs.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Nosql Search Cache

## Purpose and boundaries

This skill guides work on three coupled concerns: (1) NoSQL stores used as primary search or secondary indexes, (2) caches of query results or derived documents sitting in front of a system of record, and (3) the invalidation and expiry logic that keeps (1) and (2) correct.

In scope: data modeling for lookup keys, index field selection, cache key design, TTL and eviction policy, invalidation strategy, staleness budgets, memory sizing, and load/consistency verification.

Out of scope: choosing a vendor from scratch, relational schema design unless it feeds the cache, full-text relevance tuning, and infrastructure provisioning. Route those to their own skills.

## Inputs and assumptions

Collect before proposing changes:
- Read/write ratio and query shapes (top 20 queries by frequency and latency).
- Source of truth and where writes land.
- Acceptable staleness per data class, in seconds, stated by the product owner.
- Current item size distribution (p50, p95, max) and working-set size.
- Store product and version, and cache product and version.
- Current TTLs, eviction policy, and hit ratio.

If any of these is missing, state the assumption explicitly and mark the output as provisional. Do not assume a specific product's feature flags, index types, or eviction names; verify them against current official documentation for the exact version in use.

## Operating workflow

1. **Classify each query and cache entry.** Label each as: exact-key lookup, filtered search, range scan, aggregation, or derived view. Record its staleness budget.
2. **Derive keys from the query, not the entity.** A cache key must include every parameter that changes the result: filters, sort, pagination cursor, locale, tenant, and permission scope. Omitting permission scope is a common data-leak defect.
3. **Choose the invalidation pattern per class:**
   - Time-bounded staleness: TTL only, with TTL set to the staleness budget.
   - Write-driven correctness: explicit invalidation or versioned keys (embed a version number from the source row, so stale entries are never read).
   - Search indexes: asynchronous reindex from a change stream or outbox, with a lag metric.
4. **Size the index and cache.** Estimate memory as items × (average size + per-entry overhead). Overhead varies by product; measure it in a staging copy rather than assuming a figure.
5. **Set TTL with jitter** for bulk-loaded entries to avoid synchronized expiry stampedes.
6. **Guard against stampedes.** Use single-flight loading (one request recomputes, others wait or receive a stale value) for hot keys.
7. **Write the rollout plan** with dual-read comparison before cutover.

## Decision gates

- **Gate A, staleness:** If the product owner cannot state a staleness budget, stop. Do not default to "as fresh as possible."
- **Gate B, correctness:** If a cached value gates money movement, access control, or inventory allocation, it must not be served from cache without a write-time or read-time version check. Require explicit sign-off.
- **Gate C, permission scope:** If any cached result varies by user or role, the key must include the scope or the value must be post-filtered. Reject shared keys otherwise.
- **Gate D, memory:** If projected working set exceeds 70% of allotted memory, require an eviction-impact analysis before going live.
- **Gate E, destructive operations:** Flushing caches, dropping or rebuilding indexes, changing key formats in production, and bulk deletes all require explicit written approval from the data owner, with a rollback path and a stated blast radius.
- **Gate F, external impact:** Changes that alter responses served to external customers or partners require approval and a canary plan.

## Verification and evidence

Measure before and after; record numbers, not impressions:
- Cache hit ratio per query class (target set by the owner; flag any drop greater than 5 points after deploy).
- Staleness observed: compare cached values to source at sampled intervals; the 99th percentile must be within the budget.
- Index lag: time from source commit to searchable visibility, reported as p95 and p99.
- Latency at p50/p95/p99 with cache on and off for the top queries.
- Stampede check: request count to the origin during forced expiry of a hot key in staging; it should approximate one recomputation.
- Correctness diff: shadow-read results for a sample of queries, reporting mismatch rate and root causes.

Any benchmark figure must come from your own measurement in your environment. Do not cite external numbers as expected performance.

## Failure handling

- **Hit ratio collapse:** Check key cardinality changes first (a new parameter in the key), then TTL changes, then eviction pressure.
- **Stale reads reported:** Confirm whether invalidation fired. Check outbox or change-stream lag before changing TTLs.
- **Memory eviction of hot keys:** Do not raise memory blindly; reduce entry size, split large documents, or narrow cached fields.
- **Cross-tenant data appearing:** Treat as a security incident. Disable the cache layer for the affected query class, notify the owner, and do not resume without approval.
- **Index rebuild failure:** Keep the old index serving; never drop it before the new one is verified.

## Deliverable contract

Return:
1. A query-class table: class, example query, key template, invalidation pattern, staleness budget, owner.
2. Key and TTL specification with jitter values and eviction policy as configured.
3. Memory estimate with stated assumptions and measurement method.
4. Verification results using the metrics above, with raw numbers and sample size.
5. Open approvals list: each gated action, approver, status.
6. Rollback procedure with a tested trigger condition.

Mark every product-specific setting as "verify against current official docs for version X." Do not present unverified settings as final.