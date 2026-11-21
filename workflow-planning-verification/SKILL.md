---
name: workflow-planning-verification
description: Use when planning or reviewing an automated multi-step agent workflow before execution, to check step ordering, tool permissions, failure paths, approval gates, and success criteria so the workflow can be run safely and its results verified.
author: Luo Kai
provenance: original
version: 1.1.0
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

