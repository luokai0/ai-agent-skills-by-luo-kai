---
name: workflow-planning-verification
description: Use when planning or reviewing an automated multi-step agent workflow before execution, to check step ordering, tool permissions, failure paths, approval gates, and success criteria so the workflow can be run safely and its results verified.
author: Luo Kai
provenance: original
version: 1.4.0
---

# Workflow Planning Verification

## Purpose and boundaries

This skill verifies a workflow plan before any agent or automation runs it. It covers multi-step plans that call tools, APIs, databases, file systems, messaging systems, or other agents. Typical inputs are a plan draft, a runbook, a pipeline definition, or a natural-language task description that will be converted into steps.

In scope: step decomposition, dependency ordering, input and output contracts, tool permission scoping, decision gates, rollback and retry logic, and evidence required to declare each step complete.

Out of scope: writing the production code of the tools themselves, choosing vendors, legal or compliance certification, and performance benchmarking. Do not claim that a plan is compliant with any regulation or standard. Report only what was checked.

## Inputs and assumptions

Before verifying, collect:

1. The goal in one sentence, and who or what consumes the result.
2. The full step list, including any branches, loops, and parallel steps.
3. For each step: the tool or API, the operation type (read, write, delete, send, execute, spend), the input source, and the expected output shape.
4. Available credentials and their scopes, described by role rather than secret value.
5. Data sensitivity classes present (for example personal data, financial records, credentials, unreleased source code).
6. Environment: sandbox, staging, or production.

If any item is missing, record it as an open assumption. Do not fill gaps with guesses about system behavior. Mark any statement about a specific tool's parameters, limits, or behavior as "verify against current official documentation" unless the user has supplied the documentation text.

## Operating workflow

1. **Restate the goal.** Write the goal and the observable success condition. If the success condition cannot be observed, the plan is not verifiable; flag it.
2. **Build the step graph.** Number every step. Mark dependencies explicitly ("needs output of step 3"). Identify steps with no dependency that could run in parallel, and confirm parallelism does not share writable resources.
3. **Classify each step** by operation type and reversibility: read-only, reversible write, irreversible write, external send, or spend/commit.
4. **Check the contracts.** For each edge between steps, confirm the producer's output fields match the consumer's required inputs in name, type, and units. Example failure: step 2 outputs `amount_cents`, step 4 expects `amount` in dollars.
5. **Check permissions.** Each step should use the narrowest credential that works. Flag any step that has write access where only read is needed, or a single shared admin token used across unrelated steps.
6. **Check failure paths** (see Failure handling below).
7. **Apply decision gates** to every step classified as irreversible or external.
8. **Define evidence** for each step (see Verification and evidence).
9. **Produce the deliverable** in the required format.

## Decision gates

Stop and request explicit human approval before executing any step that:

- Deletes, overwrites, or migrates data, or changes schemas or permissions.
- Sends messages, emails, notifications, or publishes content to people or external systems.
- Moves money, places orders, or creates commitments with a cost.
- Touches production systems or customer-facing configuration.
- Handles personal, financial, health, or credential data beyond what the stated goal requires.
- Uses a credential broader than the step needs.

Approval must name the specific step, the action, the target, and the reversal path. A general "go ahead" for the whole workflow does not cover later irreversible steps. Re-request approval if the plan changes after approval.

Proceed without a gate only for read-only steps and reversible writes in a sandbox or staging environment, and only when the rollback is written down.

## Verification and evidence

For each step, define:

- **Pass condition**: a checkable statement, such as "row count in target table equals source row count," "HTTP response status is 200 and returned ID is stored," or "file hash matches manifest."
- **Evidence artifact**: the log entry, diff, query result, or screenshot that proves the condition, and where it is stored.
- **Timeout and retry budget**: maximum attempts and total elapsed time. Retries must be idempotent or guarded by an idempotency key; otherwise a retry can duplicate a write.

Whole-workflow checks:

- Every step has a pass condition. Count them; a step without one is a defect.
- Every irreversible step has a pre-action snapshot or confirmation read.
- The final output is compared against the stated goal's success condition, not merely against "all steps succeeded."
- Spot-check at least one output by an independent method (for example recomputing a total from raw records).

## Failure handling

Classify each failure as transient (network timeout, rate limit), input (malformed or missing data), permission (denied scope), or logic (the plan assumed something false). Then:

- Transient: retry within budget with backoff; then escalate.
- Input: halt dependent steps; report the offending record; do not silently skip records.
- Permission: halt; do not attempt to escalate privileges or find alternative credentials.
- Logic: halt the workflow and return to planning. Do not improvise new steps during execution.
- Partial completion: record which steps committed, and provide the compensating action for each, or state that none exists.

Never continue past a failed irreversible step to "finish the job."

## Deliverable contract

Return a verification report with these sections, in order:

1. **Verdict**: approved to run, approved with conditions, or blocked. One line.
2. **Blocking defects**: numbered, each with step number, the defect, and the fix.
3. **Step table**: step number, operation type, reversibility, credential scope, pass condition, evidence artifact, approval required (yes or no).
4. **Open assumptions**: each marked for verification against current documentation where relevant.
5. **Approval requests**: one entry per gated step, with the exact action and reversal path.
6. **Residual risk**: what the check did not cover.

Do not state that the workflow is secure, compliant, or guaranteed to succeed. Report what was checked and what remains unverified.
## Executable workflow contract and recovery design (v1.1)

Represent the approved workflow as a machine-checkable contract rather than a prose-only checklist. Each step has a stable ID, owner, dependency IDs, typed inputs and outputs, effect classification, target resource, authority scope, timeout, retry policy, idempotency strategy, approval requirement, pass condition, and evidence reference. Reject cycles, unresolved dependencies, ambiguous targets, and steps without observable completion conditions before execution.

Define the workflow's consistency model. Identify which steps are safe to run concurrently, which require serial execution, and which share mutable state. For each external side effect, record the idempotency key and the system-of-record field used for reconciliation. For multi-system work, define the saga order and compensating action for every completed step that may need reversal; explicitly mark effects that cannot be compensated.

Use a durable state machine with transitions such as READY, RUNNING, WAITING, RETRYABLE_FAILURE, BLOCKED, COMPENSATING, SUCCEEDED, PARTIAL, and CANCELLED. Persist the transition before dispatching the next external action. On resume, inspect both workflow state and downstream systems; a timeout is an unknown outcome until reconciled.

The final acceptance gate checks the user's postconditions independently of the step ledger. A sequence of successful API responses does not prove the intended outcome. Preserve partial completion and unresolved compensation in the final report.

## Ultron routing contract

**Choose this skill when:** turning a user goal into a bounded, executable plan with dependencies, preconditions, expected postconditions, decision gates, side-effect handling, and evidence-based completion checks.

**Choose `delegated-execution-queues` when:** plan steps must run asynchronously or durably across process restarts, with leases, retries, backpressure, cancellation, and dead-letter recovery.

**Choose `session-continuity-recall` when:** an interrupted plan must be resumed and reconciled with current external state before any step is repeated.

**Choose `agent-evaluation-design` when:** defining reusable tests to establish whether this planning/execution behavior is safe and reliable across many cases.

**Handoff contract:** produce a task contract with dependencies, permitted actions, stop conditions, idempotency expectations, verification source, and completion evidence. Queue or resume skills must preserve those semantics rather than treating each step as an unstructured job.

**Why the boundary exists:** planning defines what should happen and what counts as done; durable execution and session recovery preserve that plan across time.

## Workflow invariants, provenance, and safe joins (v1.3)

### Declare invariants that must remain true

In addition to step-level pass conditions, define workflow-wide invariants: totals reconcile, each source record is handled exactly once or explicitly classified, no resource is mutated outside its owner scope, no external action occurs before approval, and no terminal state is reported while required work remains unresolved. State the invariant, authoritative evidence source, check frequency, and failure transition. If an invariant cannot be observed, mark it as an unresolved risk rather than asserting it.

### Preserve provenance across step boundaries

Every material output should carry a provenance envelope: originating step ID, source record or artifact IDs, source timestamp/version, transformation identifier, and validation status. A downstream step should consume the declared artifact version, not an ambiguous mutable path such as “latest”. When data is transformed, preserve mapping back to source records and record dropped, rejected, or redacted items with reason codes. This makes reconciliation and selective replay possible.

### Make parallel joins deterministic

For each fan-out, define the expected child set, completion condition, timeout behavior, and join policy before execution. Specify whether the join requires all children, a quorum, a threshold, or an explicit partial result. Reject duplicate child IDs and unexpected results. Do not let the first completed worker win unless the contract explicitly defines that policy and establishes that late results cannot change the committed outcome.

If workers can write shared state, assign a single writer or use versioned compare-and-set semantics. Parallel reads may be merged only with a documented conflict policy. When child results disagree, preserve each result and its provenance; do not average categorical or incompatible outputs.

### Make compensation honest

For each compensation, define its preconditions, idempotency behavior, expected postcondition, and evidence. Distinguish a true reversal from a corrective follow-up: a sent email cannot be unsent, a payment reversal is a new transaction, and a published artifact may already have been copied. If the original effect is irreversible, the recovery plan must state residual impact, containment action, notification owner, and reconciliation evidence. Never report “rolled back” when only a compensating action was attempted.

### Validate workflow-level invariants

Test empty input, partial input, duplicate source records, delayed and out-of-order child results, worker disagreement, a child that never completes, stale artifact versions, a failed compensation, and a process restart during a join. Verify the workflow either reaches a valid terminal state or remains explicitly blocked/partial with enough provenance to resume safely.


## Handoff contract validation and execution-boundary integrity (v1.4)

A handoff between skills, agents, queues, or workflow stages is a contract boundary, not a conversational suggestion. The sender must provide enough structured information for the receiver to continue the same task without inventing missing scope, evidence, authority, or completion state. The receiver must validate the handoff before acting.

### Required handoff envelope

Every material handoff must carry:
- Stable task and parent-run identifiers, handoff ID, originating step, sender identity, intended receiver, and creation time.
- Goal, requested deliverable, explicit exclusions, current plan revision, and the exact next-step objective.
- Typed inputs and immutable artifact references, including content digests, source versions, timestamps, and provenance. Do not substitute mutable names such as latest for a pinned artifact.
- Preconditions, dependencies, completed steps, failed or skipped steps, pending work, and unresolved decisions.
- Resource targets, environment, data classifications, tenant scope, and allowed operation classes.
- Approval records with the exact action and target they authorize, approver identity, policy revision, expiry, and evidence reference. Never pass a vague statement such as approved without its bound action.
- Required postconditions, verification method, evidence location, retry/idempotency rules, stop conditions, and escalation owner.

### Receiver acceptance protocol

Before execution, the receiver must:
1. Validate the envelope schema and required fields; reject malformed, ambiguous, or internally inconsistent values.
2. Authenticate the sender and verify that the receiver is the intended recipient for this task and tenant.
3. Re-read authoritative state for mutable facts, resource existence, current permissions, revocation status, and external side effects that may have occurred after the handoff was created.
4. Verify artifact digests and source versions; mark missing or changed artifacts stale and request a refreshed handoff.
5. Revalidate each approval against the proposed action, canonical arguments, target, environment, principal, policy revision, and expiry. Approval does not transfer the sender's identity or privileges.
6. Confirm that dependencies are complete and that the declared next step is still valid under the current workflow revision.
7. Accept with a recorded receiver, accepted envelope digest, timestamp, and execution owner, or reject with specific reason codes and required corrections.

No side effect may occur before acceptance. A handoff can be accepted for analysis while remaining blocked for execution if authority or evidence is incomplete.

### Prevent duplicate, stale, and split-brain execution

Use a unique handoff ID and idempotency key bound to task, sender, receiver, contract revision, and payload digest. Repeated delivery of the same accepted handoff must return the existing disposition rather than create a second execution. A changed payload requires a new handoff revision and fresh validation.

Transfer execution ownership atomically. The sender must stop dispatching the transferred step after the receiver accepts it; use a monotonic ownership or fencing revision so a delayed sender cannot later commit a competing result. If ownership transfer cannot be confirmed, do not run both sides concurrently.

Treat timeout, lost acknowledgement, and process restart as unknown delivery outcomes. Query the handoff ledger and downstream system of record before resending or repeating an external operation. Preserve the original idempotency identity when reconciling the same logical operation; create a new identity only for a genuinely new action.

### Revalidate on change

Re-run acceptance when the payload, task scope, resource target, tenant, skill version, dependency digest, policy revision, approval, environment, or next-step operation changes. A previously accepted envelope does not authorize a materially changed action. If new evidence contradicts the handoff, suspend the affected branch, preserve both records, and reconcile against the authoritative source.

### Handoff acceptance tests

- Missing or malformed required fields are rejected with actionable diagnostics.
- A valid approval for one target cannot authorize a changed target or argument set.
- A stale artifact digest or revoked skill blocks execution.
- Duplicate delivery creates one logical execution and one terminal disposition.
- A lost acknowledgement is reconciled before retry; no duplicate external effect occurs.
- Sender and receiver cannot both hold valid write ownership for the same step.
- A policy or task revision invalidates only the affected approvals and dependent work, while independent completed evidence remains traceable.
- Rejected handoffs preserve the reason, evidence, and correction path without silently dropping pending work.

**Routing boundary:** this section owns the contract at a workflow-stage boundary. Use agent-messaging-channels for message transport and delivery semantics, delegated-execution-queues for durable scheduling and worker lifecycle, and session-continuity-recall for reconstructing interrupted execution. Transport delivery is not acceptance, acceptance is not authorization, and authorization is not proof of completion.
