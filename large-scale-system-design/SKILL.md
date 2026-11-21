---
name: large-scale-system-design
description: Use when designing, reviewing, or re-architecting a system expected to serve high traffic, large data volumes, multiple teams, or multi-region availability, and a decision on partitioning, consistency, scaling, or failure domains must be made or justified.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Large Scale System Design

## Purpose and boundaries

This skill produces architecture decisions for distributed systems whose scale, availability, or organizational complexity makes single-node intuitions unreliable. It covers capacity modeling, service decomposition, data partitioning, replication and consistency choices, failure-domain isolation, and migration sequencing.

It does not cover: line-level code review, UI design, vendor procurement, or compliance certification. Compliance-sensitive designs are flagged for specialist review, not declared compliant.

## Inputs and assumptions

Collect before designing. If an input is missing, record it as an assumption with an owner and a date to resolve.

- Functional scope: the top five user-facing operations and their business invariants (for example, "a seat is sold at most once").
- Load: peak read and write rates, fan-out per request, payload sizes, growth rate over 12 months, and burst pattern.
- Data: total size, growth, retention, access pattern (point lookup, range scan, analytics), and cardinality of the main partition key.
- Service levels: availability target, latency percentiles per operation, durability target, and acceptable staleness per read path.
- Failure tolerance: which failure domains must survive (instance, rack, zone, region) and the recovery time and recovery point objectives.
- Organization: number of teams touching each data set and deployment cadence.
- Constraints: existing stack, data residency, budget ceiling, and migration window.

Assumptions must be stated as numbers where possible. "Traffic grows moderately" is not an assumption; "peak writes 12k/s, growing 40%/year" is.

## Operating workflow

1. Restate the invariants. For each, mark whether it requires strong consistency, bounded staleness, or eventual convergence. Most design errors originate here.
2. Build a capacity model from the inputs. Compute steady-state and peak load per component, then apply a headroom factor agreed with the owner (commonly 2x for peak on stateful tiers, stated explicitly). Show arithmetic.
3. Choose the partition key. Require that the key (a) distributes load without hot keys under the observed skew, (b) keeps the frequent query for a single operation within one partition, and (c) is stable over time. Test skew against real or sampled key distributions, not assumed uniformity.
4. Decompose by data ownership, not by function. Each entity has one writing service. Cross-service reads go through owned projections or APIs, not shared tables.
5. Select replication and consistency per data path. Map each invariant from step 1 to a mechanism: single-writer per partition, consensus-backed transactions, idempotent writes with deduplication keys, or asynchronous projections with a published staleness bound.
6. Design failure isolation. Define cell or shard boundaries so one failing unit affects a bounded fraction of users. Specify timeouts, retry budgets, bulkheads, and load-shedding priority. Retries without a budget are prohibited.
7. Plan migration as a sequence of reversible steps: dual write or change data capture, shadow reads with comparison, percentage cutover, then decommission. Each step has an abort criterion.
8. Write the decision record (see Deliverable contract) before review.

## Decision gates

Proceed past each gate only when its condition holds.

- Gate A (invariants): every write path has a named consistency level. Any path marked "best effort" needs an explicit owner sign-off.
- Gate B (capacity): peak load and headroom are computed with arithmetic shown, and the bottleneck tier is named.
- Gate C (partitioning): skew analysis exists. Maximum partition share under observed distribution is below the threshold the owner sets (state it, e.g., no partition above 5% of traffic).
- Gate D (cross-region): if multi-region, each region's write authority is defined. Active-active writes to the same entity require a conflict resolution rule that is written down and tested.
- Gate E (irreversible change): schema drops, data deletion, traffic cutover above 10%, region or vendor exit, and changes affecting external partners require explicit human approval with a named approver before execution.

## Verification and evidence

Every claim in the design needs one of: a calculation, a test result, a reference to the vendor's current documentation, or a labeled assumption.

- Run a load test at 1.5x projected peak against the proposed partition layout; record p50, p99, error rate, and the hottest partition's share.
- Inject failures in staging: kill one node per tier, partition one zone, and delay the replication stream. Record recovery time and any invariant violation.
- Verify idempotency by replaying a duplicated message batch and comparing final state.
- Check staleness bounds by measuring projection lag under peak load.
- Version-sensitive details (service limits, replication semantics, client library behavior, pricing tiers) must be checked against current official documentation for the version in use and recorded with the access date. Do not rely on memory for these values.

## Failure handling

- If capacity arithmetic and load test disagree, trust the test and revise the model; document the gap.
- If a hot partition appears after launch, first apply a load-shedding limit on the key, then split the key space. Do not change the partition key on a live system without a migration plan under Gate E.
- If an invariant cannot be met under a required failure mode, return to Inputs and renegotiate the availability or consistency target with the owner. Do not silently weaken the invariant.
- If a required measurement is unavailable, mark the decision provisional with an expiry and a named measurement owner.

## Deliverable contract

Produce a single decision record containing, in order:

1. Scope and invariants table (invariant, consistency level, owner).
2. Capacity model with arithmetic and headroom factor.
3. Partition key choice with skew evidence and rejected alternatives.
4. Service and data ownership map.
5. Failure domains, isolation boundaries, and timeout and retry budgets.
6. Migration steps with abort criteria and approval points.
7. Open assumptions, each with owner and resolution date.
8. Verification results, or the list of tests still required before go-live.

Do not include: unexplained diagrams, unquantified adjectives such as "highly scalable," unnamed "industry standard" claims, or guarantees of availability or compliance.