---
name: session-continuity-recall
description: Use when an AI agent must resume work from a prior session, reconstruct earlier decisions and open tasks from notes, logs, or memory stores, or hand off a workflow to another agent or human without losing state.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Session Continuity Recall

## Purpose and boundaries

This skill restores working context across sessions. It reconstructs what was decided, what was done, what is pending, and what has changed since, then verifies that reconstruction against current reality before acting on it.

In scope: locating prior session artifacts (handoff notes, task logs, commit history, ticket comments, prior summaries), extracting decisions and open items, reconciling them with current state, and producing a resumption brief or handoff record.

Out of scope: inventing missing history, replaying prior external actions, making new decisions that the prior record does not support, and modifying memory stores beyond the designated handoff location.

## Inputs and assumptions

Required inputs:
- The goal of the resumed work, stated in one sentence by the requester.
- Access to the prior record (named files, log exports, ticket threads, or memory entries). If none exist, state that and stop at a gap report.
- Access to current state sources (repository, system status, data snapshot, ticket board).

Assumptions to state explicitly in the brief:
- The prior record is authoritative only as of its timestamp.
- Session summaries are lossy. Treat them as pointers, not truth.
- Tool access, permissions, and API behavior may have changed; verify against current official documentation before relying on any remembered command or endpoint.

## Operating workflow

1. **Define the recall question.** Write the specific thing to resume (for example, "finish the schema migration for invoices"). Broad recall produces noise.
2. **Inventory sources.** List every candidate record with its timestamp, author, and scope. Rank by recency and by proximity to the recall question.
3. **Extract state claims.** From the highest-ranked sources, pull out: decisions made (with rationale), tasks completed (with evidence), tasks open, blockers, and stated next steps. Tag each claim with its source and timestamp.
4. **Reconcile against current state.** For each claim, check the live source. Classify as CONFIRMED, CHANGED, CONTRADICTED, or UNVERIFIABLE.
5. **Resolve conflicts.** When sources disagree, prefer live system state over notes, and newer records over older ones. Record the resolution and reason.
6. **Build the resumption brief.** Include only confirmed or explicitly flagged items.
7. **Pause at the decision gate** before any action with side effects.

## Decision gates

Proceed autonomously when:
- The recall question is specific and sources are identified.
- Claims are CONFIRMED or clearly marked as stale with no action dependency.

Stop and request approval when:
- Any next step would delete, overwrite, migrate, or send data.
- Any next step affects external parties (messages, payments, published content, third-party systems).
- A CONTRADICTED claim changes the plan.
- Sensitive material (credentials, personal data, legal or medical records) appears in recalled records. Do not copy it into the brief; reference its location only.
- The prior record is older than the threshold the requester set, or the gap exceeds the decision scope.

## Verification and evidence

Each resumed item must carry:
- Source reference and timestamp.
- Current-state check result with the method used (for example, file hash comparison, ticket status read, query result date).
- Confidence label: high (live-confirmed), medium (source-consistent, not live-checked), low (single unverified source).

Quality checks before handoff:
- 100% of open tasks have a source and a live-check result or an explicit UNVERIFIABLE flag.
- No claim lacks a timestamp.
- Every CONTRADICTED item has a stated resolution.
- Brief length is under one page; recall that exceeds this should be split by workstream.

Domain example: a data engineering agent recalls that a backfill "completed" last Tuesday. Live check shows the job log ends at 60% of partitions. Classify as CONTRADICTED, report the partition gap, and gate any re-run behind approval because it writes to a warehouse table.

## Failure handling

- **No prior record found:** report the search scope and stop. Do not reconstruct history from assumptions.
- **Record is corrupted or truncated:** quote the readable portion, mark the boundary, and request the missing segment.
- **Live source unavailable:** downgrade affected claims to UNVERIFIABLE and block any gated action.
- **Conflicting authoritative sources:** present both with timestamps and ask the requester to designate the authority.
- **Recall drift** (the brief grows beyond the stated question): trim to the question and list excluded material as a separate appendix pointer.

## Deliverable contract

Produce a Resumption Brief containing, in order:
1. Recall question and scope.
2. Sources consulted, with timestamps.
3. Confirmed state (decisions, completed work, open tasks), each with confidence label.
4. Changed or contradicted items with resolutions.
5. Unverifiable items and what would verify them.
6. Proposed next actions, marked as gated or autonomous.
7. Information gaps and required approvals.

Do not:
- Present remembered content as current fact without a live check.
- Replay prior external actions to "catch up."
- Copy sensitive values into the brief.
- State version-specific commands, flags, or API behavior without marking them for verification against current official documentation.
## Session resume and continuity protocol (v1.1)

A resumed session must reconstruct state from durable evidence, not from an assistant's recollection of the previous conversation. Resolve the run ID, task contract revision, principal, tenant, policy version, agent and tool versions, checkpoint pointer, event history, artifacts, and outstanding approvals before continuing.

Build a resume brief with: objective and acceptance criteria; authority and exclusions; verified completed steps with receipts; actions attempted but not reconciled; pending dependencies; current artifact versions; unresolved assumptions; expired or still-valid approvals; budget remaining; and the next safe operation. Link to original evidence rather than copying sensitive payloads into the brief.

Reconcile every in-flight external effect against its system of record. Classify it as confirmed complete, confirmed absent, partially complete, or unknown. Unknown outcomes block automatic replay of non-idempotent actions. If the original approval expired or the target parameters changed, request a new approval.

Check for changed policy, revoked credentials, changed tool schemas, stale data, and incompatible agent versions. A resumed task must not inherit authority that is no longer valid. If a migration or upgrade changed the checkpoint schema, use a versioned migration with validation and rollback rather than best-effort parsing.

Test restart at every durable boundary, duplicate resume requests, expired approvals, deleted source artifacts, changed permissions, incompatible schemas, and concurrent resume attempts. Exactly one execution owner may continue a mutable task at a time.

