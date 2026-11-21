---
name: agent-platform-and-learning-workflows
description: Use when designing, reviewing, or operating an AI agent platform or a learning workflow (agent orchestration, tool-use integration, evaluation loops, feedback-driven improvement, fine-tuning or retrieval updates) and a decision must be made about scope, data handling, promotion of changes, or evidence of quality.
author: Luo Kai
provenance: original
version: 1.2.0
---

# Agent Platform And Learning Workflows

## Purpose and boundaries

This skill guides the design and review of production AI agent systems and the workflows that let them learn from use: collecting feedback, building evaluation sets, updating prompts, retrieval indexes, or model weights, and promoting those changes safely.

In scope: agent task decomposition, tool and permission design, orchestration state, evaluation harnesses, feedback capture, dataset curation, regression gating, rollout and rollback plans, and monitoring for drift.

Out of scope: general model architecture research, selecting a vendor contract, legal interpretation of data rights, and clinical, financial, or legal decisions made by the agent itself. Route those to the accountable human owner.

## Inputs and assumptions

Collect before proposing anything:

1. Task inventory: each agent task, its trigger, expected output, and failure cost.
2. Tool catalog: every action the agent can take, with read/write classification and credential scope.
3. Data sources: origin, owner, retention rule, and whether it contains personal or confidential material.
4. Current baseline: success rate, cost per task, latency, and escalation rate on a fixed evaluation set. If none exists, building one is step one.
5. Change mechanism: how prompts, indexes, or weights are versioned and deployed today.

Assume nothing about model versions, context limits, pricing, or SDK behavior. Mark any such detail as "verify against current official documentation" in the deliverable.

## Operating workflow

1. Classify each task by blast radius: read-only, internal write, external-facing write, or financial/legal/safety-relevant.
2. Decompose the task into steps with explicit inputs, outputs, and a stop condition. A step that cannot state its stop condition is not ready for automation.
3. Bind tools with least privilege. Give each tool a narrow scope, argument validation, and a dry-run or preview mode where the platform supports it.
4. Define the state record the orchestrator persists: task id, step, tool calls, outputs, confidence signals, and human decisions. Store enough to replay a run.
5. Build the evaluation set from real traces, not synthetic cases alone. Target at least 50 labeled cases per task class before trusting aggregate metrics, and stratify by user segment and edge type.
6. Capture feedback with structured labels (accepted, edited, rejected, reason code), not free text alone.
7. Convert feedback into candidate changes: prompt revision, retrieval corpus fix, tool description fix, or fine-tuning example. Tag each candidate with its source traces.
8. Run candidates against the frozen evaluation set and a held-out regression set. Compare against the current production version on the same data.
9. Promote through staged exposure: shadow mode, then a small percentage of traffic, then full rollout, with a predefined rollback trigger.

## Decision gates

- Gate A (scope): Proceed to automation only if the task's worst-case failure is recoverable or a human reviews every output before it takes effect.
- Gate B (data): Use production traces for training or evaluation only after confirming the retention basis and removing personal identifiers. Escalate if this is unclear.
- Gate C (promotion): Promote a candidate only if it improves the primary metric, does not regress any stratum by more than the pre-agreed margin, and holds cost and latency within budget.
- Gate D (autonomy): Expand tool permissions or remove human review only after two consecutive evaluation cycles meet the bar on live shadow traffic.

## Verification and evidence

Quality checks must be measurable:

- Task success rate on the frozen set, with confidence intervals reported when sample size is below 200.
- Tool-call precision: proportion of write calls that were correct on review. Target set per task by the owner.
- Unsafe-action rate: count of attempted actions outside permitted scope. Target: zero, with every instance investigated.
- Regression delta by stratum, not only overall.
- Feedback label agreement between two reviewers on a 10% sample. Below 80% agreement means the labeling guide must be revised before the labels are used.

Record every promotion with: candidate id, source traces, evaluation results, approver, and rollback criteria.

## Failure handling

- Tool error or timeout: retry only idempotent reads. Never auto-retry a write without an idempotency key or a state check.
- Repeated low-confidence outputs on one task class: pause automation for that class and route to human review.
- Evaluation regression after promotion: roll back first, then diagnose.
- Suspected data leakage in training or retrieval: halt the pipeline and escalate for incident review.
- Conflicting feedback: do not average it away. Sample, adjudicate, and update the labeling guide.

## Deliverable contract

Every deliverable must include:

1. Task classification table with blast-radius rating and autonomy level.
2. Tool permission matrix with scopes and approval requirements.
3. Evaluation plan with metrics, thresholds, dataset provenance, and sample sizes.
4. Promotion and rollback plan with named gates.
5. Open risks, unresolved data questions, and version-sensitive items flagged for verification.

Do not:

- Deploy write-capable tools, expand permissions, or use production data for training without explicit approval from the accountable owner.
- Treat aggregate accuracy as sufficient evidence.
- Claim compliance, safety certification, or benchmark performance that has not been measured in this environment.
- Invent platform features, flags, or library versions.
## Agent platform capability lifecycle (v1.1)

Design the platform as separable control-plane and execution-plane responsibilities. The control plane owns identity, task contracts, policy, skill discovery, version pinning, routing, budgets, approval state, and audit metadata. The execution plane runs isolated agent sessions, tool adapters, retrieval, memory access, and task workers under the authority issued by the control plane. A worker must not be able to rewrite its own policy or grant itself new tools.

Define capability registration as a governed lifecycle: proposed, inspected, tested, approved, published, deprecated, revoked. Each capability record includes owner, version, digest, declared purpose, activation conditions, input/output contract, dependencies, permissions, data classes, runtime compatibility, evaluation results, and rollback or retirement path.

Resolve capabilities by matching the task contract to declared capability metadata, then enforce permissions independently at execution time. Skill selection is not authorization. Pin versions for a run so an update cannot change behavior mid-task. For critical workflows, require compatibility checks before upgrading dependencies or skills.

Separate agent identity from user identity and from the downstream service identity. Bind delegated authority to a task, tenant, allowed operations, and expiry. Track budget and concurrency across the entire run, not only per worker. Provide global stop controls and narrower kill switches for individual tools, agents, tenants, and routes.

Treat the platform as incomplete until it can resume interrupted work, reconcile uncertain side effects, explain why a capability was selected, prove which version ran, and produce evidence for every consequential action.

## Skill registry contracts and reproducible activation (v1.2)

A skill catalog is a governed software supply chain, not a folder of names. Discovery may suggest a capability, but activation must validate its exact artifact, contract, compatibility, and permissions before execution.

### Canonical skill record
For every publishable skill, maintain a normalized record containing:
- Stable skill identifier and human-readable name.
- Immutable version and content digest.
- Declared purpose, activation conditions, inputs, outputs, and failure modes.
- Required tools, permissions, data classes, and external destinations.
- Runtime and protocol compatibility ranges.
- Dependencies with explicit version constraints.
- Security review, evaluation, and approval evidence.
- Owner, publication time, deprecation state, and revocation reason where applicable.

Keep descriptive metadata separate from executable authority. A skill description may help route a task, but it must never grant the permissions it describes.

### Resolution and lock discipline
1. Resolve the complete dependency graph before execution.
2. Detect cycles, incompatible version ranges, missing dependencies, and conflicting permissions.
3. Produce a deterministic lock record containing every selected skill and dependency version plus content digest.
4. Reject mutable references such as latest for production or reproducible runs.
5. Verify the retrieved artifact digest and publisher signature against an independently trusted key policy before loading it.
6. Validate the skill manifest against a versioned schema; reject unknown security-critical fields, ambiguous permission declarations, and malformed values.
7. Pin the resolved set for the lifetime of a task. An update must not silently change a running task's behavior.

### Compatibility and rollout
Treat runtime, model interface, tool schema, protocol, and dependency compatibility as separate dimensions. A skill can be syntactically loadable and still be behaviorally incompatible. Require a compatibility test against the target runtime and the declared tool contracts.

Promote a new skill version through isolated evaluation, internal or shadow use, limited canary exposure, and staged expansion. Keep the previous known-good digest available for rollback. Revocation must block new activation immediately and define how active sessions are stopped or allowed to finish safely.

### Registry acceptance tests
Verify that:
- Reordering registry responses does not change dependency resolution.
- A digest mismatch or invalid signature prevents activation.
- A revoked version cannot be loaded from a cache.
- Dependency cycles and incompatible versions fail with actionable diagnostics.
- A skill cannot request undeclared tools or broaden its permissions at runtime.
- A running task remains pinned while a new version is published.
- Rollback restores the exact prior digest and dependency closure.

Record the resolved lock, validation result, signature identity, compatibility report, and activation decision with each run. Do not report a skill as trusted solely because it is present in the registry.
