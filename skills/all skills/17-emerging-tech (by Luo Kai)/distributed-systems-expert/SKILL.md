---
name: distributed-systems-cs-expert
version: 1.0.0
description: Expert-level distributed systems theory covering consistency models, consensus algorithms, fault tolerance, replication, distributed transactions, and the CAP theorem.
author: luo-kai
tags: [distributed systems, consensus, CAP theorem, replication, Raft, Paxos]
---

# Distributed Systems CS Expert

## Before Starting
1. Consistency, availability, or partition tolerance priority?
2. Synchronous or asynchronous system model?
3. Crash-stop or Byzantine fault model?

## Core Expertise Areas

### Consistency Models
Strong consistency: linearizability — operations appear instantaneous and ordered.
Sequential consistency: all processes see same operation order, not necessarily real-time.
Causal consistency: causally related operations ordered, concurrent may differ.
Eventual consistency: replicas converge given no new updates — DNS, DynamoDB.
CRDT: conflict-free replicated data types — merge without coordination.

### CAP Theorem
Consistency: every read gets most recent write or error.
Availability: every request gets non-error response.
Partition tolerance: system works despite network partitions.
Cannot guarantee all three: choose CP or AP during partition.
PACELC: extends CAP to also consider latency vs consistency tradeoff.

### Consensus Algorithms
Paxos: classic consensus, complex to implement, single-decree and multi-Paxos.
Raft: leader election, log replication, safety — designed for understandability.
Raft terms: leader, follower, candidate — heartbeats prevent elections.
Byzantine fault tolerance: BFT requires 3f+1 nodes to tolerate f Byzantine faults.

### Replication
Single-leader: one primary accepts writes, replicas read — simple, sequential.
Multi-leader: multiple primaries accept writes — conflict resolution needed.
Leaderless: Dynamo-style — quorum reads and writes, sloppy quorum.
Replication lag: replica may serve stale data — monotonic read consistency.

### Distributed Transactions
2PC: two-phase commit — prepare and commit phases, blocking on coordinator failure.
Saga pattern: sequence of local transactions with compensating actions.
Distributed deadlock: cycle detection across nodes, timeout-based resolution.

## Best Practices
- Design for partial failure — any component can fail at any time
- Use idempotent operations to handle retries safely
- Implement circuit breakers to prevent cascade failures
- Prefer optimistic concurrency for read-heavy workloads

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Assuming network reliability | Handle timeouts and retries explicitly |
| Non-idempotent retries causing duplicates | Use idempotency keys |
| Two generals problem with 2PC | Accept that 2PC can block, use sagas for long transactions |
| Clock skew in ordering events | Use logical clocks or vector clocks |

## Related Skills
- system-design-expert
- microservices-expert
- database-design-expert
