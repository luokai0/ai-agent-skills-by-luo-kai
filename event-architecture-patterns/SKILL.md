---
name: event-architecture-patterns
description: Use when designing, reviewing, or migrating event-driven backend systems, including event schemas, topic or stream topology, publish/subscribe contracts, outbox and ordering guarantees, idempotent consumers, and event replay or versioning decisions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Event Architecture Patterns

## Purpose and boundaries

This skill guides the design and review of asynchronous, event-driven backend communication: what events exist, who produces and consumes them, how they are delivered, ordered, versioned, and recovered. It covers choreography versus orchestration, event notification versus event-carried state transfer, outbox-based publishing, consumer idempotency, dead-letter handling, and schema evolution.

It does not cover: choosing a specific vendor broker for a company without a stated requirement set, tuning cluster infrastructure, general synchronous API design, or frontend event handling.

## Inputs and assumptions

Collect before recommending anything:

- Business events and the state change each one reports (for example, `order.placed`, not `database.row.updated`).
- Producers and consumers, with their owning teams or services.
- Delivery expectations: at-least-once, effectively-once, or best-effort; acceptable duplicate and lag windows.
- Ordering requirements, expressed per aggregate or entity key, not globally.
- Retention and replay needs, and regulatory constraints on personal data in events.
- Current transport and its version. Broker feature availability and client library APIs are version-sensitive; verify against current official documentation before stating any capability.

For unresolved event contracts, record the assumed schema, ownership, and compatibility impact before proceeding.

## Operating workflow

1. Inventory events. List each event name, producer, consumers, and owning aggregate. Reject events named after CRUD operations or table changes unless the domain genuinely is CRUD.
2. Classify each flow: notification (payload carries identifiers only, consumers fetch state), event-carried state transfer (payload carries the fields consumers need), or command-like (intent to act, one intended handler). Command-like messages require explicit ownership of the handler.
3. Define the ordering key. Partition or key by the aggregate ID that needs ordering. Events for different keys should not be assumed ordered.
4. Choose the publication mechanism. For dual writes to a database and a broker, use a transactional outbox written in the same transaction as the state change, with a relay that publishes and marks rows sent. Never publish before commit.
5. Design each consumer: make handling idempotent using a processed-message record keyed by event ID, or by natural keys with conditional writes. Define retry policy with bounded attempts and backoff, then route to a dead-letter destination with the original payload, headers, and failure reason.
6. Version the schema. Additive, optional fields are compatible; renames, removals, and meaning changes are breaking and require a new event type or a versioned schema with a deprecation window.
7. Define replay procedure: which consumers may rebuild projections from history, how side effects are suppressed during replay, and how checkpoints are recorded.
8. Document the topology diagram and the contract for each event in a single reference table.

## Decision gates

Stop and request approval before proceeding when:

- A design requires changing retention, deleting or purging topics, streams, or dead-letter contents, or rewinding consumer offsets in production.
- A migration will dual-publish or cut over producers or consumers that affect live external partners or customers.
- Events contain personal, financial, health, or credential data, or cross a jurisdictional boundary.
- A consumer will perform an irreversible external action (payment, email, shipment, third-party API write) on an event that may be redelivered.

Proceed without approval only for design documents, schema drafts, and changes confined to a non-production environment that the user owns.

Choose orchestration over choreography when a business process has more than three steps with compensating actions, or when a single team needs to observe the full process state.

Choose event-carried state transfer over notification when consumers would otherwise make synchronous calls back to the producer on every event, and the payload size remains reasonable.

## Verification and evidence

Each recommendation must be backed by at least one of: a sequence diagram of a failure case (duplicate delivery, consumer crash mid-handling, out-of-order arrival), a test that injects duplicates and reorders messages, or a reconciliation query comparing producer state to projection state.

Quality checks, all measurable:

- Every event type has exactly one owning producer and a documented schema version.
- 100% of publishing paths use outbox or an equivalent transactional mechanism, verified by code search for direct broker sends inside service methods.
- Every consumer has a documented idempotency key and a test that delivers the same event twice with identical resulting state.
- Dead-letter queues have an alert threshold and an owner.
- Schema compatibility is checked in CI against the previous published version using the registry or tool your team has adopted; confirm its current command syntax from its official documentation.

## Failure handling

- If ordering is violated in testing, check the partition key first, then consumer concurrency settings, before changing application logic.
- If outbox lag grows, inspect relay throughput and locking on the outbox table before adding publisher instances, which can create duplicate sends that consumers must absorb.
- If a poison message blocks a partition, quarantine it to dead-letter after bounded retries; do not skip it silently.
- If a consumer has already performed an external side effect and then failed, record the compensation requirement and escalate instead of retrying blindly.
- If a schema change breaks a consumer in production, roll back the producer change first, then fix the contract.

## Do not

- Do not publish from inside a database transaction before commit.
- Do not treat broker delivery guarantees as application-level exactly-once.
- Do not use wall-clock time as the sole ordering mechanism.
- Do not put secrets or unnecessary personal data in event payloads or headers.
- Do not invent broker configuration values, retention periods, or throughput figures; request them from the operator.

## Deliverable contract

Produce a single document containing:

1. Event catalog table: name, version, producer, consumers, ordering key, delivery semantics, classification.
2. Topology diagram or textual flow for the reviewed scope.
3. Per-consumer idempotency and retry specification.
4. Schema compatibility rules and the deprecation plan for any breaking change.
5. Replay and recovery procedure.
6. Open assumptions list, with each item marked as verified or pending.
7. Approval requests for any gated action, stated as explicit questions.