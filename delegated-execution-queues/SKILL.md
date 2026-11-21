---
name: delegated-execution-queues
description: Use when an agent must hand off, queue, schedule, or supervise tasks executed by other workers, tools, or agents, and needs ordered dispatch, ownership tracking, retries, and verifiable completion records.
author: Luo Kai
provenance: original
version: 1.2.0
---

# Delegated Execution Queues

## Purpose and boundaries

This skill governs how a coordinating agent packages work into queued units, dispatches them to executors (human operators, scripts, tool-using sub-agents, or external services), monitors them, and accepts or rejects results. It covers queue design, task contracts, ordering, idempotency, retry policy, and completion evidence.

It does not cover: writing the executor's internal logic, choosing models, designing general infrastructure, or making product decisions. If a task requires changing production systems, moving money, messaging customers, deleting data, or accessing personal or regulated data, stop at the approval gate below before dispatch.

## Inputs and assumptions

Before enqueuing, confirm:

1. The goal in one sentence, and the observable outcome that proves it.
2. The executor type and its documented capabilities. Do not assume a tool supports an operation unless its current documentation confirms it. Mark any version-specific behavior as "verify against current official documentation."
3. Access scope: which systems, paths, accounts, and environments the executor may touch.
4. Dependencies between tasks, and which tasks are safe to run concurrently.
5. Deadline or priority, and who owns the outcome.

If any item is unknown, record it as an open assumption in the queue manifest. Do not fill gaps with guesses.

## Operating workflow

1. **Decompose.** Split the goal into tasks where each has one owner, one primary output, and one verifiable success condition. A task that needs "and then" to describe itself should usually be two tasks.
2. **Write a task contract** for each unit: `id`, `objective`, `inputs` (with exact locations or identifiers), `allowed_actions`, `forbidden_actions`, `depends_on`, `idempotency_key`, `max_attempts`, `timeout`, `success_criteria`, `evidence_required`.
3. **Order the graph.** Build a dependency DAG. Reject any cycle. Mark concurrency-safe tasks explicitly; default to serial when shared state is involved.
4. **Classify risk.** Tag each task `read-only`, `reversible-write`, or `irreversible/external/sensitive`. Only the third class triggers approval.
5. **Dispatch.** Enqueue only tasks whose dependencies are complete and whose inputs are present. Record dispatch time and executor identity.
6. **Monitor.** Track state transitions: `queued → running → succeeded | failed | blocked | timed_out`. Do not infer success from silence.
7. **Accept or reject.** Verify each result against its success criteria (see Verification) before releasing dependents.
8. **Close.** Write the completion record and release resources.

## Decision gates

Proceed automatically when all are true:
- Task is `read-only` or `reversible-write` within its declared scope.
- Inputs match the contract and dependencies are accepted.
- Attempt count is below `max_attempts`.

Require explicit human approval before dispatch when any is true:
- The task deletes, overwrites, or migrates data without a verified backup or rollback path.
- It sends messages, publishes content, submits forms, or triggers payments or external API writes.
- It changes permissions, credentials, network exposure, or production configuration.
- It touches personal, health, financial, or other regulated data.
- It cannot be undone within a stated window.

Approval request must state: the exact action, target identifiers, expected effect, rollback method, and what happens if it is not approved. Approval applies only to that exact payload; re-approve if inputs change.

Stop the queue (do not skip) when two consecutive tasks fail the same way, or when an executor reports actions outside its `allowed_actions`.

## Verification and evidence

A task is complete only when its evidence exists and matches the contract. Acceptable evidence includes:
- Output artifact with checksum or record count compared against the expected value.
- Diff showing only the intended files or records changed.
- Log excerpt or status response that names the target and the result.
- Read-back of the changed state from an independent source.

Measurable checks:
- Record count in output equals the count predicted from input, or the discrepancy is explained.
- No task marked `succeeded` without an evidence reference.
- Zero actions executed outside `allowed_actions`.
- Retries never produce duplicate side effects; verify with the idempotency key.

Do not treat an executor's self-report as sufficient evidence for irreversible actions.

## Failure handling

Classify each failure before retrying:
- **Transient** (timeout, rate limit, temporary unavailability): retry with exponential backoff and jitter, up to `max_attempts`. Verify whether the first attempt partially applied before retrying.
- **Input defect** (missing or malformed input): block the task, return it to the coordinator, do not retry.
- **Permission defect**: block, report the missing scope, do not attempt escalation.
- **Logic defect** (executor produced output failing criteria): retry at most once with a corrected contract; otherwise escalate.

On partial completion, record exactly which subtasks finished, then mark dependents `blocked`, not `failed`. Never roll back automatically unless the rollback itself was pre-approved.

## Deliverable contract

The final output of a delegated run is a queue report containing:

1. Manifest: task list with ids, owners, dependencies, and final states.
2. Per-task record: attempts, timestamps, evidence references, and any approvals with their scope.
3. Open assumptions and unresolved blocks, each with a named owner.
4. Summary of irreversible actions taken, listed separately.
5. Statement of what was not verified and why.

Do not present the run as complete if any task is `blocked`, `timed_out`, or lacks evidence. Do not omit failed tasks from the report.

## What not to do

- Do not enqueue a task whose success condition is undefined.
- Do not let an executor choose its own scope or escalate its own permissions.
- Do not retry non-idempotent actions without checking for prior effects.
- Do not bundle unrelated irreversible actions into one approval.
- Do not state version-specific tool behavior as fact without verifying current documentation.
## Durable queues, leases, retries, and backpressure (v1.1)

A delegated execution queue is a stateful scheduler, not a list of prompts. Each task needs a stable ID, idempotency key, tenant and principal, contract revision, priority, dependency set, resource budget, deadline, lease policy, retry policy, cancellation state, and explicit success predicate. Persist the task before acknowledging enqueue.

Use visibility timeouts or leases so abandoned work can be reclaimed, but treat lease expiry as uncertain execution state. Before reassignment, inspect checkpoints and reconcile external side effects. Use heartbeats for long tasks and bounded lease renewal; prevent a worker from holding a lease indefinitely without progress evidence.

Apply exponential backoff with jitter only to retryable failures. Distinguish permanent validation errors, authorization denials, rate limits, transient transport failures, and unknown outcomes after a possible write. Use dead-letter handling with diagnostic context and an explicit replay approval path. Do not silently discard exhausted tasks.

Control throughput with per-tenant quotas, global concurrency caps, priority fairness, rate limits, and backpressure. Prevent one noisy tenant or runaway agent from starving other work. Propagate cancellation to workers and tools, while acknowledging that cancellation cannot undo an already completed external effect.

Track queue age, lease expiry, retry count, dead-letter volume, duplicate suppression, task latency, resource use, and verified completion. Test duplicate delivery, worker crash, queue restart, lease races, poison tasks, dependency failure, rate-limit storms, cancellation races, and partial side effects.

## Ultron routing contract

**Choose this skill when:** work must be dispatched and executed asynchronously with durable task state, leases, retry policy, idempotency, concurrency control, backpressure, cancellation, or dead-letter handling.

**Choose `workflow-planning-verification` when:** defining the task graph, prerequisites, action boundaries, and postconditions before queueing work.

**Choose `session-continuity-recall` when:** resuming a user-facing task or reconciling an uncertain external side effect after interruption.

**Choose `supervisor-swarm-coordination` when:** the queue is part of a multi-agent system with supervisor/worker ownership and shared-state coordination requirements.

**Handoff contract:** receive an explicit task contract, stable task ID, permitted operations, idempotency key, expiry, and completion predicate. Return durable state transitions, attempt history, terminal outcome, and authoritative postcondition evidence. Queue delivery is not proof that the task completed.

**Why the boundary exists:** queues guarantee controlled delivery and recovery; planning defines the meaning of the work, and supervisors own the broader coordination policy.
