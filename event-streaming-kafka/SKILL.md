---
name: event-streaming-kafka
description: Use when designing, configuring, operating, or debugging Apache Kafka-based event streaming pipelines, including topic design, producer and consumer semantics, schema evolution, consumer lag, retention, and replay.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Event Streaming with Kafka

## Purpose and boundaries

This skill guides backend engineers through design, change, and incident work on Kafka-based event pipelines. It covers topic and partition design, producer delivery settings, consumer group behavior, offset management, schema compatibility, retention and compaction, dead-letter handling, and replay.

Out of scope: general message-queue selection, stream-processing framework internals beyond their Kafka interaction, cluster hardware sizing, and cloud provider billing. Do not use this skill to make compliance or durability guarantees on behalf of a vendor or regulator.

## Inputs and assumptions

Collect before recommending anything:

- Event producers and consumers, with their languages and client libraries and versions.
- Business ordering requirements: which entity must have ordered events (for example, per order ID).
- Delivery expectations: at-least-once is assumed unless the owner states otherwise. Exactly-once claims require evidence of transactional configuration end to end.
- Throughput, message size, and peak-to-average ratio.
- Retention and replay needs, and downstream storage constraints.
- Schema registry in use, and its compatibility mode.
- Current cluster version and managed or self-hosted status.

Assumptions must be stated explicitly. Exact configuration key names, default values, and client API signatures change across Kafka and client releases. Mark every version-sensitive detail as "verify against current official documentation for your version" rather than asserting it from memory.

## Operating workflow

1. **Define the event contract.** Name the topic by domain and event type. Record key, value schema, owner, and consumers. Events describe facts that already happened; commands belong elsewhere.
2. **Choose the key.** The key determines partition routing and therefore ordering. Use the entity ID whose ordering matters. A key with very few distinct values or heavy skew creates hot partitions.
3. **Size partitions.** Derive count from target parallelism (consumers in the largest group) and peak throughput per partition under measured load. Partition count can be increased later but this changes key-to-partition mapping; plan for it.
4. **Configure producers.** Set acknowledgment to all replicas, enable idempotence, and bound retries with a delivery timeout. Batch and compress deliberately; measure before tuning linger and batch size.
5. **Configure consumers.** Commit offsets only after the side effect is durable. Make handlers idempotent using an event ID or natural key stored with the effect.
6. **Plan failure paths.** Define retry topics with bounded attempts and backoff, and a dead-letter topic that carries original metadata, error class, and attempt count.
7. **Set retention and compaction.** Use time or size retention for event streams. Use compaction only for entity-state topics where the latest value per key is the truth.
8. **Document replay procedure** including target offsets or timestamps, consumer group handling, and idempotency assumptions.

## Decision gates

- **Ordering:** If strict ordering across keys is required, stop and reassess. Kafka guarantees order only within a partition. Global ordering implies a single partition and a throughput ceiling.
- **Exactly-once:** Proceed only if producer transactions, consumer isolation level, and sink idempotency are all confirmed. Otherwise design for at-least-once with deduplication.
- **Schema change:** Backward-compatible changes (adding optional fields with defaults) may proceed with registry validation. Removing fields, renaming, or changing types requires a new topic version and a migration plan.
- **Partition increase:** Requires explicit approval, a key-remapping impact note, and confirmation that consumers tolerate reordering during the transition.
- **Retention reduction or topic deletion:** Requires explicit approval. Deletion is irreversible and can destroy the replay source.
- **Replay into production consumers:** Requires explicit approval, a dry run on a non-production consumer group, and a rollback owner.
- **Offset reset on a live group:** Requires explicit approval and a documented expected duplicate or skip count.

## Verification and evidence

Each change must produce:

- Schema registry compatibility check result for the target subject.
- Test showing a redelivered event produces no duplicate side effect (target: zero duplicate effects across a replay test of at least one full partition's recent events).
- Consumer lag before, during, and after the change, measured per group and partition, with recovery to baseline within the agreed window.
- Under-replicated partition count and producer error rate during a broker restart drill in a non-production environment.
- For key changes or partition increases: a sample of 1,000 keys showing mapping before and after, and proof that per-key ordering consumers were updated or drained.

Do not report numeric benchmark results without a recorded run.

## Failure handling

- **Rising lag:** Check consumer throughput, rebalance frequency, poison messages, and downstream latency in that order. Do not simply add consumers beyond partition count; extra consumers sit idle.
- **Repeated rebalances:** Inspect session timeout versus processing time per poll. Long handlers must be moved off the poll thread or the poll interval adjusted per current client documentation.
- **Poison message:** Route to dead-letter after bounded retries. Never skip silently and never block the partition indefinitely.
- **Duplicate side effects:** Confirm the deduplication key is written atomically with the effect. Investigate commit ordering before changing producer settings.
- **Out-of-order events after a partition change:** Halt the affected consumers, drain, and reprocess from a defined point under approval.

## Deliverable contract

Deliver a single design or change record containing:

1. Topic name, key, partition count with rationale, retention or compaction setting.
2. Schema subject, compatibility mode, and change type.
3. Producer and consumer delivery configuration with version-verification notes.
4. Idempotency mechanism and its storage location.
5. Retry and dead-letter topology.
6. Verification results from the checklist above, with raw evidence attached.
7. Approval log for every gated action, with approver and timestamp.
8. Rollback steps and their owner.

## What not to do

- Do not claim exactly-once delivery from configuration alone.
- Do not increase partitions or change keys without the impact note.
- Do not use auto-commit with handlers that have external side effects.
- Do not delete topics, purge data, or reset offsets on production groups without approval.
- Do not place sensitive personal data in event payloads or keys without an approved classification and encryption plan.
- Do not invent configuration names, flags, or versions; verify them.