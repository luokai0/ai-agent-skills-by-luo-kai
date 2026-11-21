---
name: concurrency-performance-engineering
description: Use when diagnosing, designing, or tuning concurrent or parallel code for throughput, latency, contention, or scalability, including thread pools, async runtimes, locks, lock-free structures, actor systems, and shared-state services.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Concurrency Performance Engineering

## Purpose and boundaries

This skill covers measurable performance work on concurrent code: identifying bottlenecks caused by contention, scheduling, synchronization, blocking I/O inside async paths, false sharing, queue saturation, and unbounded parallelism. It produces evidence-backed changes and a verification record.

In scope: profiling concurrent workloads, reasoning about lock hold times and critical sections, sizing pools and queues, batching and sharding shared state, reducing synchronization granularity, and validating correctness is preserved after tuning.

Out of scope: general algorithm selection with no concurrency component, infrastructure capacity planning, cost optimization, and formal proofs of correctness (recommend a specialist review when correctness proofs are required). Do not treat this skill as a source of correctness guarantees for lock-free code.

## Inputs and assumptions

Required before acting:
- The code path under study, the runtime and language version, and the target platform (core count, memory model, container CPU limits).
- A representative workload description: request mix, concurrency level, data sizes, and arrival pattern.
- Current metrics: throughput, p50/p95/p99 latency, CPU utilization, run-queue length, lock wait time, GC pauses if applicable.
- Service-level targets, if any.

Assumptions to state explicitly in the deliverable when not provided: single-tenant benchmark host, steady-state load, and that production-like data is available. Do not assume a benchmark result applies to production without a comparison run.

## Operating workflow

1. **Define the metric and the target.** Write one primary metric (for example, p99 latency at fixed offered load) and a guardrail metric (for example, error rate or memory ceiling). Reject vague goals like "make it faster."
2. **Establish a baseline.** Run the workload at three or more concurrency levels. Record variance across at least five runs. Discard runs with obvious environmental noise and document why.
3. **Classify the bottleneck.** Use profiler and runtime evidence to place the constraint into one category:
   - CPU-bound with idle cores (serialization point, lock convoy, single-threaded stage).
   - CPU-bound with saturated cores (algorithmic cost, spinning, excessive context switching).
   - Blocked threads (lock waits, synchronous I/O on async workers, pool exhaustion).
   - Memory or cache-bound (false sharing, cache-line bouncing, allocation pressure).
   - Queueing-bound (unbounded queues, backpressure absent, tail amplification).
4. **Form one hypothesis per bottleneck** and state the predicted effect size.
5. **Apply the smallest change** that tests the hypothesis: shrink a critical section, move I/O out of a lock, replace a global lock with striped locks, bound a queue, or set pool size from measured service time.
6. **Re-measure under identical conditions** and compare against the baseline with the same load profile.
7. **Repeat** only from the new profile, never from intuition.

Domain-specific examples:
- An async service calling a blocking database driver on runtime worker threads: move the call to a dedicated blocking pool, then measure event-loop lag.
- A cache guarded by one mutex showing 40% lock wait: shard into 16 segments keyed by hash, verify hit ratio and eviction behavior are unchanged.
- Counters incremented by many threads on adjacent memory: pad per-thread slots to cache-line size and confirm with hardware counters where available.

## Decision gates

- **Gate A (before changing code):** Is the bottleneck reproduced in a controlled run? If not, stop and improve the harness.
- **Gate B (before lock-free or custom synchronization):** Has a simpler change (smaller critical section, sharding, immutable snapshots, message passing) been measured and rejected? Custom lock-free structures require explicit approval and a specialist review.
- **Gate C (before enlarging a pool or queue):** Does the change increase tail latency or memory under overload? If yes, require a bounded design with explicit rejection behavior.
- **Gate D (before merging):** Do tests pass under the race detector or equivalent sanitizer where the toolchain provides one, and does stress testing show no new deadlocks or livelocks?
- **Gate E (approval required):** Any change that alters production configuration, rolls out to live traffic, modifies shared state schema, or changes consistency guarantees requires explicit human approval before execution.

## Verification and evidence

Every claim of improvement needs:
- Baseline and candidate numbers for the primary and guardrail metrics, with run counts and variance.
- The identical workload definition and environment description.
- Profiler evidence showing the bottleneck moved or shrank, not just that the number changed.
- Correctness evidence: existing test suite, added concurrency tests for the changed region, and sanitizer or stress results.

Quality checks:
- Primary metric improves beyond run-to-run variance.
- Guardrail metrics do not regress beyond the agreed threshold.
- No new lock ordering violations; document lock hierarchy for any newly touched locks.
- Queue depth remains bounded under 2x expected peak load.

Version-sensitive details (runtime flags, profiler options, scheduler parameters, library APIs, sanitizer flags) must be checked against current official documentation for the exact version in use. Do not rely on remembered flag names.

## Failure handling

- **Improvement within noise:** Report as no measurable change. Do not ship it as an optimization.
- **Regression in a guardrail:** Revert the candidate, record the result, and return to classification.
- **Deadlock, data race, or lost update observed:** Stop immediately, preserve logs and the reproducer, and escalate. Do not patch around it by adding timeouts alone.
- **Benchmark cannot reproduce production shape:** Report the gap and mark conclusions as provisional.
- **Conflicting measurements:** Re-run with pinned CPU and fixed seed before drawing conclusions.

## Deliverable contract

Produce a report containing:
1. Metric definitions, targets, and guardrails.
2. Environment, runtime version, and workload description.
3. Baseline table (mean, p95/p99, variance, run count).
4. Bottleneck classification with profiler evidence.
5. Changes made, each tied to a single hypothesis, with a rationale.
6. Candidate results versus baseline under identical conditions.
7. Correctness and sanitizer results, and any residual risk.
8. A list of items requiring approval (Gate E) and version-sensitive details pending verification.

Do not claim production impact, compliance outcomes, or absolute speedups without the measurements that support them.