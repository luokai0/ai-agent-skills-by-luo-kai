---
name: supervisor-swarm-coordination
description: Use when designing, running, or auditing a supervisor agent that delegates work to multiple worker agents in parallel or sequence, including task decomposition, routing, result aggregation, and conflict resolution in AI agent automation.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Supervisor Swarm Coordination

## Purpose and boundaries

Use this skill to coordinate a supervisor agent that decomposes a goal, assigns bounded subtasks to worker agents, monitors their progress, and merges their outputs into a verified result.

In scope: task decomposition, worker selection, dispatch contracts, parallelism limits, handoff schemas, result reconciliation, retry and escalation policy, and final quality review.

Out of scope: building the underlying model or tool integrations, choosing model vendors, designing end-user UI, and making legal, medical, or financial decisions on behalf of a user. Workers do not receive authority the supervisor lacks.

## Inputs and assumptions

Before dispatch, confirm:

1. A goal statement with a stated success condition that can be checked without asking the supervisor again.
2. The list of available workers, each with declared capabilities, tool permissions, input formats, and output formats.
3. Hard constraints: deadline, cost or token budget, data-access limits, and forbidden actions.
4. Whether the environment is sandboxed, staging, or production.
5. The runtime's concurrency and timeout behavior. Verify these against current official documentation of the framework in use; do not assume defaults.

If any of items 1 to 3 are missing, stop and request them. Do not infer success criteria silently.

## Operating workflow

1. **Restate the goal** in one paragraph and list the success conditions as checkable statements.
2. **Decompose** into subtasks. Each subtask must have exactly one owner, one output artifact, and an explicit dependency list. Aim for subtasks that take a worker one bounded pass; if a subtask needs more than one tool category or more than roughly a page of output, split it.
3. **Build a dependency graph.** Mark independent subtasks as parallel candidates. Mark any subtask that writes shared state as serial unless writes target disjoint resources.
4. **Assign workers** by matching required capabilities to declared capabilities. Prefer the least-privileged worker that can complete the task. Never grant a worker tools it does not need for its subtask.
5. **Issue dispatch contracts.** Each contract contains: objective, inputs with provenance, output schema, allowed tools, prohibited actions, timeout, and the exact condition that triggers a return to the supervisor.
6. **Monitor.** Track status per subtask: pending, running, returned, failed, blocked. Re-check any worker that returns without the required artifact.
7. **Reconcile.** Compare overlapping outputs. Resolve disagreements by checking source evidence, not by majority vote alone.
8. **Integrate and verify** against the success conditions from step 1.
9. **Report** using the deliverable contract below.

## Decision gates

Pause and obtain explicit human approval before:

- Any destructive action: deleting, overwriting, truncating, or dropping data, branches, records, or deployments.
- Any irreversible action: sending messages, submitting forms, making payments, publishing content, or merging to a protected branch.
- Any external-impacting action: calling third-party systems with write scope, contacting people, or changing shared infrastructure.
- Any action touching sensitive data: personal data, credentials, health, financial, or legal records. Workers should receive only the minimum fields required.

Proceed without approval only for read-only operations, local scratch work, and outputs that remain drafts.

Escalate to the supervisor's owner when:

- Two workers return contradictory results that evidence cannot resolve.
- A worker requests a permission not in its contract.
- The retry budget for a subtask is exhausted.
- The dependency graph has a cycle.

## Verification and evidence

Every claim in the final output must cite the worker artifact or source that produced it. Apply these checks:

- **Schema check:** every returned artifact validates against its declared output schema. Target: 100% of returned artifacts pass before integration.
- **Coverage check:** every success condition maps to at least one artifact. Target: no unmapped conditions.
- **Consistency check:** overlapping claims agree, or the disagreement is listed with both sources.
- **Traceability check:** each subtask ID appears in the final report with its owner and status.
- **Spot re-execution:** re-run at least one randomly selected subtask with the same inputs and confirm the output is materially equivalent. For high-impact outputs, re-run all of them.

Record the run log: dispatch times, timeouts, retries, and token or cost totals where the runtime exposes them.

## Failure handling

- **Timeout:** cancel the worker, record partial output, re-dispatch once with a narrower scope. A second timeout escalates.
- **Malformed output:** return it to the worker once with the specific schema violation. A second failure marks the subtask failed and routes around it if possible.
- **Hallucinated or unsupported claim:** discard the claim, mark the artifact as unreliable for that point, and require a source citation on re-dispatch.
- **Tool error:** distinguish transient errors (retry with backoff, at most three attempts) from permission or validation errors (stop and escalate).
- **Partial success:** deliver what passed verification, label what did not, and state the gap. Never present partial results as complete.
- **Runaway cost or looping:** halt new dispatches when the budget is 80% consumed without a corresponding progress gain, and escalate.

## Deliverable contract

The supervisor's final output contains:

1. **Result:** the integrated answer or artifact, with status set to complete, partial, or blocked.
2. **Success conditions table:** each condition, the artifact that satisfies it, and pass or fail.
3. **Subtask ledger:** ID, owner, inputs, output reference, status, retries.
4. **Conflicts and resolutions:** each disagreement, the evidence used, and the decision.
5. **Open items:** unresolved gaps, pending approvals, and recommended next actions.
6. **Run metadata:** timestamps, retry counts, and cost figures if available.

Do not report performance benchmarks, reliability percentages, or speedups unless measured in the current run and included with the measurement method.

## What not to do

- Do not let workers dispatch other workers without the supervisor's approval.
- Do not pass full conversation history or unredacted sensitive data to workers when a field subset suffices.
- Do not merge outputs that failed verification to meet a deadline.
- Do not treat worker self-assessments of confidence as evidence.
- Do not guess API names, flags, or framework behavior. Check current official documentation and mark any version-dependent detail as requiring verification.
## Multi-agent execution protocol (v1.1)

Treat a multi-agent system as a graph of accountable workers, not a group chat. The supervisor owns the objective, authority, dependency graph, budget, and final acceptance. Workers receive bounded contracts and cannot expand scope or dispatch more workers unless explicitly authorized.

Each dispatch includes task and parent-run IDs, one measurable objective, one expected artifact, input references with provenance and sensitivity labels, allowed tools and resource scopes, prohibited actions, output schema, evidence requirements, deadline, retry ceiling, resource budget, dependencies, return condition, and permission to create subtasks or write shared state.

Model work as a directed acyclic graph. Detect cycles, missing dependencies, duplicate ownership, and shared-write conflicts before dispatch. Use explicit statuses: queued, running, waiting, returned, failed, cancelled, accepted. A worker's completion claim is not acceptance; the supervisor validates schema, source evidence, scope, and postconditions. Send only minimum necessary context. Use separate workspaces for workers editing files and assign one writer per mutable resource.

For independent proposals, collect outputs before revealing peer conclusions when blind review is useful. A reviewer challenges assumptions; a verifier inspects observable evidence. Majority vote is not a substitute for checking sources. Preserve dissent and unresolved uncertainty.

Use leases or bounded deadlines for worker ownership. If a worker disappears, determine whether it caused side effects, reconcile target state, and inspect checkpoints before reassignment. Never re-dispatch non-idempotent work solely because a worker timed out. Use task idempotency keys and explicit ownership transfer for resumable work.

Test timeout before and after writes, duplicate dispatch, conflicting outputs, malformed artifacts, unauthorized tool requests, injected worker input, worker attempts to spawn workers, supervisor restart, cancellation propagation, shared-file collisions, and budget exhaustion. Verify exactly one owner controls each mutable resource and unaccepted outputs cannot be committed or reported complete.

