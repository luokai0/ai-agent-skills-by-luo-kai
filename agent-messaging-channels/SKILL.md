---
name: agent-messaging-channels
description: Use when designing, routing, or debugging messages between AI agents, tools, humans, and external channels (queues, chat surfaces, webhooks, email, shared task boards), including deciding who may send what, to whom, and how delivery is confirmed.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Agent Messaging Channels

## Purpose and boundaries

This skill governs how agents exchange messages over channels: defining message envelopes, choosing channel types, routing between agents and humans, handling acknowledgments, retries, and ordering, and keeping an auditable record. It covers design reviews, implementation guidance, and incident triage of messaging behavior.

Out of scope: model prompt engineering, general API integration unrelated to messaging, and infrastructure provisioning. Do not use this skill to send live messages to real recipients during analysis unless the user has explicitly approved that send.

## Inputs and assumptions

Collect before acting:
- Channel inventory: each channel's type (queue, pub/sub topic, direct call, chat, email, webhook, shared store), owner, and whether it crosses a trust boundary.
- Participants: each agent, human, and external system, with its allowed send and receive scopes.
- Delivery expectations: at-most-once, at-least-once, or effectively-once, and the tolerated latency.
- Payload sensitivity: personal data, credentials, financial or medical content, and regulated data.
- Current platform documentation for each channel. Delivery semantics, size limits, retention, and ordering guarantees vary by product and version. Mark any such detail as "verify against current official documentation" unless confirmed in this session.

If any of these is missing, state the assumption explicitly in your output.

## Operating workflow

1. **Map the flow.** List every sender, receiver, channel, and message type. Draw it as a table: sender, channel, receiver, purpose, frequency, sensitivity.
2. **Define the envelope.** Every message must carry: `message_id` (unique), `correlation_id` (links the request chain), `sender`, `recipient`, `type`, `created_at` (UTC), `schema_version`, `reply_to` (if applicable), and `expires_at`. Payloads reference data by ID rather than embedding large or sensitive content.
3. **Choose the channel per message class.**
   - Commands that must run once: queue with idempotency keys.
   - Events for many subscribers: pub/sub topic, no reliance on ordering across topics.
   - Human-facing requests: chat or task board with an explicit approval state.
   - External-facing output: treat as a gated action (see Decision gates).
4. **Specify acknowledgment.** Define what counts as received, processed, and failed. A receiver acknowledges only after its side effect is durable or explicitly rejected.
5. **Specify retry and dead-letter behavior.** Set bounded retry counts, backoff intent, and a dead-letter destination with an owner.
6. **Specify ordering.** Name the ordering key where order matters (for example, per task ID). Do not assume global order.
7. **Write the contract.** Give each message type a schema, required fields, and a version policy: additive changes only within a version; breaking changes create a new `type` or version.

## Decision gates

Stop and request explicit human approval before:
- Sending any message to a person outside the working team, a customer, or a public surface.
- Any action that is destructive or irreversible: purging a queue, replaying a dead-letter backlog into production, deleting message history, or revoking a subscription.
- Routing payloads containing credentials, personal data, or regulated data across a new trust boundary.
- Changing a live channel's schema, ordering key, or delivery guarantee.
- Auto-replying to external senders.

Proceed without approval for read-only inspection, design documents, and dry-run schema validation against sample data that contains no real personal data.

Decide a channel is unsuitable if it cannot provide the required acknowledgment, cannot carry the envelope fields, or has retention shorter than the business need for audit.

## Verification and evidence

Check each item and record the result:
- Every message type has a schema, an owner, and a version.
- Every `message_id` is unique within its channel over the retention window. Duplicate delivery is handled by an idempotency check, tested with a deliberate redelivery.
- Each consumer's side effect is idempotent. Test by processing the same message twice; the second run must produce no additional effect.
- A correlation trace exists for at least one end-to-end flow, from initiating request to final acknowledgment.
- Dead-letter count and age have alert thresholds defined. Target: zero messages older than the agreed processing window without an owner assigned.
- Retry ceiling is finite and documented. Target: no unbounded retry loops in any code path.
- Sensitive fields are absent from logs. Sample ten recent log lines and confirm.

Report numbers measured, not estimated. If you could not measure, say so.

## Failure handling

- **Duplicate delivery:** check `message_id` against the idempotency store; if already applied, acknowledge and stop.
- **Out-of-order arrival:** hold the message against its ordering key until predecessors arrive or a timeout is reached; then route to review, do not guess.
- **Schema mismatch:** reject to the dead-letter channel with the validation error; never coerce silently.
- **Consumer crash after side effect but before acknowledgment:** the idempotency check must absorb the redelivery. If it cannot, escalate as a defect.
- **Unknown recipient:** do not broadcast as a fallback. Dead-letter and notify the sender's owner.
- **Suspected leak:** halt the channel, preserve evidence, and escalate to a human owner. Do not delete messages to contain it without approval.

## Deliverable contract

Produce one document containing:
1. Flow table (sender, channel, receiver, purpose, sensitivity).
2. Envelope definition and per-type schemas with versions.
3. Channel choice with justification per message class.
4. Acknowledgment, retry, dead-letter, and ordering specification.
5. List of decision gates that apply to this system, with named approvers where known.
6. Verification results with measured values and the commands or procedures used.
7. Open assumptions and items marked "verify against current official documentation."

Do not claim delivery guarantees, compliance status, or performance figures that were not measured or confirmed from current documentation. Do not invent field names, endpoint paths, or library functions; mark unknown items as unknown.