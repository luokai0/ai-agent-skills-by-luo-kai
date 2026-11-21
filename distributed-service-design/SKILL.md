---
name: distributed-service-design
description: Use when designing, reviewing, or decomposing a distributed service system, choosing service boundaries, communication styles, consistency models, or resilience patterns for multi-service architectures.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Distributed Service Design

## Purpose and boundaries

This skill guides architectural decisions for systems made of multiple independently deployed services that communicate over a network. It covers service decomposition, interface contracts, data ownership, communication style, consistency and failure semantics, and resilience patterns.

In scope: boundary definition, synchronous versus asynchronous interaction, data ownership and cross-service workflows, timeout and retry policy, idempotency, observability requirements, and migration from a monolith or from an existing service mesh of coupled services.

Out of scope: language-level code design, infrastructure provisioning details, vendor selection without stated requirements, and security threat modeling beyond the interface-level controls named below.

## Inputs and assumptions

Collect before recommending anything:

- Business capabilities and the operations that cross them.
- Expected traffic: request rate, fan-out per user action, peak-to-average ratio.
- Latency and availability targets per user-facing operation, stated as numbers.
- Data classes per entity: owner, sensitivity, retention, and required freshness.
- Existing platform constraints: messaging, service discovery, deployment model, observability stack.
- Team topology. Service boundaries that cross team lines create coordination cost; weigh it.

If a target is missing, state the assumption explicitly and label it as such. Do not fill in latency or availability numbers silently.

## Operating workflow

1. **Map capabilities to candidate services.** Group operations that change the same data and are usually performed together. A candidate boundary must have one owner for each piece of state.
2. **Enumerate cross-service operations.** For each user action, list every service call it triggers and whether the caller waits for the result.
3. **Classify each interaction.** Choose synchronous request/response only when the caller needs the answer to proceed. Use events or commands for notifications, fan-out, and work that can complete later.
4. **Define data ownership and consistency.** Assign each entity one writer. For workflows spanning owners, choose between a saga with compensating actions and a single-owner redesign. Specify the consistency level each read path tolerates.
5. **Specify contracts.** For each interface: schema, versioning rule, error taxonomy, idempotency key where writes can be retried, and maximum payload size.
6. **Set resilience parameters.** Per dependency: timeout derived from the parent's budget, retry count with backoff and jitter, circuit-breaker thresholds, and bulkhead limits. Retries only on operations proven idempotent.
7. **Define observability.** Required per-request correlation identifiers, per-dependency latency and error metrics, and the dashboards and alerts that indicate each failure mode.
8. **Plan migration** if replacing existing code: strangler routing, dual-running criteria, and rollback trigger.

## Decision gates

Stop and reassess if any gate fails:

- **Chatty boundary gate:** a single user operation requires more than three synchronous hops in the critical path. Merge services or move work off the path.
- **Shared-write gate:** two services write the same table or entity. Assign a single owner before proceeding.
- **Budget gate:** the sum of worst-case synchronous latencies along the critical path exceeds the user-facing target. Reduce hops, parallelize, or relax the target with stakeholder sign-off.
- **Retry gate:** any retried write lacks an idempotency mechanism. Do not add retries until it exists.
- **Distributed transaction gate:** a proposal requires two-phase commit across independently deployed services. Reject in favor of sagas or redesign.
- **Ownership gate:** no team owns a proposed service's on-call responsibility.

## Verification and evidence

Before sign-off, verify with evidence rather than assertion:

- Trace a representative set of user operations through the design; confirm the critical-path hop count and latency sum against the budget.
- For each write path, demonstrate duplicate delivery produces one effect (idempotency test under replayed requests).
- Inject dependency failure in a test environment: confirm timeouts fire within the budget and the circuit opens at the configured threshold.
- Confirm every cross-service call emits the correlation identifier in logs and traces.
- Check that each saga has a compensation step for every forward step that has external side effects.
- Record measured results with environment, load profile, and date. Do not report estimated numbers as measured.

## Failure handling

- If a latency target cannot be met by the design, present the trade-off options (reduce hops, cache with a stated staleness bound, relax target) and request a decision. Do not choose silently.
- If a dependency's behavior is unknown or version-specific (client libraries, broker delivery guarantees, mesh features), mark it as requiring verification against current official documentation and do not assume the guarantee.
- If a compensation step cannot be defined for an operation, escalate it as a design blocker.
- If ownership is disputed, record both proposals and the criteria that would decide between them.

## Deliverable contract

Produce a design document containing, in order:

1. Scope statement and stated assumptions, with unknowns labeled.
2. Service map with each service's owned entities and owning team.
3. Interaction table: caller, callee, style (sync, async, event), idempotency mechanism, timeout, retry policy.
4. Critical-path latency budget with arithmetic shown.
5. Consistency statement per read path and saga definitions with compensations.
6. Decision gate results, each marked pass or failed with reasoning.
7. Verification plan and any completed evidence.
8. Open risks and items requiring approval.

Do not include: unverified benchmark figures, claimed compliance outcomes, invented library or flag names, or recommendations that bypass a failed gate.

## Approval requirements

Obtain explicit human approval before: deleting or retiring any existing service, data, or endpoint; performing schema migrations on shared stores; changing production traffic routing; altering externally exposed contracts; or any action affecting customers, partners, or regulated data.