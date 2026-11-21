---
name: agent-design-patterns
description: Use when designing, reviewing, or refactoring an LLM-based agent or multi-step automation, including choosing between single-call, workflow, and autonomous loop architectures, defining tool contracts, planning memory and state, or adding guardrails and evaluation.
author: Luo Kai
provenance: original
version: 1.2.0
---

# Agent Design Patterns

## Purpose and boundaries

This skill guides the selection, composition, and review of agent architectures: systems where a language model decides steps, calls tools, reads results, and continues until a goal is met or a stop condition fires.

In scope:
- Choosing the lowest-complexity architecture that meets the requirement.
- Specifying tool contracts, state handling, control flow, and stop conditions.
- Reviewing an existing agent design for failure modes.
- Defining verification and handoff points.

Out of scope:
- Model training, fine-tuning, or benchmarking claims.
- Vendor-specific SDK usage (verify current official documentation before writing code).
- General prompt copywriting unrelated to control flow.

## Inputs and assumptions

Before designing, establish:
1. Goal: the observable outcome, stated as a checkable condition.
2. Tools: each external capability, its read or write nature, and its owner.
3. Data sensitivity: what personal, financial, credential, or confidential data may enter context.
4. Volume and latency: runs per day, acceptable time per run, cost ceiling.
5. Error cost: what a wrong action costs, and whether it can be reversed.

If any item is unknown, record it as an assumption and list it in the deliverable. Do not silently assume production access, write permissions, or unlimited budget.

## Operating workflow

1. **Classify the task.** Mark it as deterministic (fixed steps known in advance), branching (steps known, choice among paths), or open-ended (steps must be discovered). Most business automation is deterministic or branching.
2. **Pick the pattern.** Use the cheapest that fits:
   - Single call with structured output: classification, extraction, drafting.
   - Prompt chain: fixed sequence, each step validated before the next.
   - Router: one classifier selects among specialized handlers.
   - Orchestrator-worker: a planner splits work across bounded sub-tasks.
   - Autonomous loop: model chooses the next action each turn. Use only when open-ended discovery is genuinely required.
3. **Define tool contracts.** For each tool: name, purpose, typed input schema, typed output schema, error shape, idempotency behavior, and whether it mutates state. Reject tools whose purpose cannot be stated in one sentence.
4. **Design state.** Separate working context (per-run), durable state (checkpointed to storage), and reference data (retrieved on demand). Never let the model be the only record of a completed external action.
5. **Set limits.** Specify maximum steps, maximum tool calls per tool, wall-clock timeout, and token or cost budget. Each limit needs a defined behavior when hit: stop, summarize, or escalate.
6. **Write stop conditions.** Success condition, failure condition, and escalation condition, each checkable from state rather than from model self-report.
7. **Draft the control flow** as an explicit diagram or ordered list, then trace two happy-path and two failure-path runs by hand.

## Decision gates

Proceed to the next stage only when:
- **Gate A (pattern):** You can justify the chosen pattern against a simpler one in one sentence. If an autonomous loop is chosen, document why a workflow fails.
- **Gate B (tools):** Every write-capable tool has an idempotency key or a documented duplicate-safety strategy.
- **Gate C (data):** Sensitive fields are identified and excluded from prompts, logs, and traces unless a reviewer approves inclusion.
- **Gate D (limits):** Every loop has a numeric ceiling.

Require explicit human approval before:
- Any destructive action (delete, overwrite, revoke, cancel).
- Any irreversible action (payments, sent messages, published content, filed legal or regulatory submissions).
- Any action with external impact on customers, vendors, or regulators.
- Any use of credentials with broader scope than the task needs.
- Any action touching regulated or sensitive data categories.

Approval must name the specific action and parameters, not a general "proceed."

## Verification and evidence

Each run must produce evidence that can be checked without re-running the model:
- Tool call log with inputs, outputs, timestamps, and status.
- State snapshots at each checkpoint.
- Final output validated against its schema.
- For write actions, a read-back confirmation from the target system.

Measurable quality checks for the design:
- Step ceiling defined and tested at the boundary (run one case at limit minus one and at limit).
- Duplicate-trigger test: replay the same input twice; confirm no duplicate external effect.
- Injection test: include instructions inside retrieved documents and tool outputs; confirm the agent does not execute them as commands.
- Tool-error test: force each tool to return a timeout, a malformed response, and an authorization error; confirm each produces the defined behavior.
- Evaluation set: at least 20 representative cases, including edge and adversarial cases, with expected outcomes written before running.

Report pass rates as counts (for example, 17 of 20), never as percentages without the denominator.

Do not claim accuracy, reliability, or compliance levels not measured in this project. Benchmark figures from external sources are not evidence for this system.

## Failure handling

- **Tool timeout:** retry at most twice with backoff for read operations; for write operations, check state before any retry.
- **Malformed output:** one repair attempt with the schema error supplied; then fall back to the defined default or escalate.
- **Step ceiling reached:** stop, save state, and return a partial result labeled as partial with completed steps listed.
- **Conflicting tool results:** do not average or guess; stop and escalate with both sources cited.
- **Suspected prompt injection:** halt write actions, record the source, and escalate.
- **Unknown error class:** treat as failure; do not continue on model judgment.

## Deliverable contract

The design deliverable must contain, in this order:
1. Goal statement and success condition.
2. Chosen pattern with the one-sentence justification and the rejected alternative.
3. Tool table: name, purpose, read or write, schema summary, idempotency approach, approval required (yes or no).
4. State model: what is stored, where, and the checkpoint frequency.
5. Limits table: steps, calls per tool, timeout, budget, and behavior at each limit.
6. Control flow listing with stop, failure, and escalation conditions.
7. Approval gates: the list of actions requiring named human approval.
8. Evaluation plan: case count, categories, expected outcomes, and the measured results with denominators.
9. Open assumptions and items marked for verification against current official documentation of any framework, API, or model feature referenced.

Do not deliver a design that lacks any of these sections, uses unresolved sample values, or leaves a write-capable tool without an approval classification.
## Agent lifecycle engineering (v1.1)

Treat an agent as a controlled execution system, not a prompt with tools attached. Model its lifecycle as explicit states: INTAKE, CONTEXT, PLAN, AUTHORIZE, EXECUTE, VERIFY, COMMIT, REPORT, with WAITING_FOR_APPROVAL, BLOCKED, RECOVERY, and CANCELLED as alternate states. Define legal transitions and the evidence required for each. A model response cannot mark a run complete; the runtime decides completion from verified postconditions.

Create an immutable run contract containing the objective, principal, tenant, environment, allowed tools and operations, excluded actions, input provenance and freshness, dependency graph, expected artifacts, numeric limits, commit policy, and completion proof. If scope or authority changes, create a new contract revision and re-evaluate approvals.

Separate proposal from execution. The model proposes; deterministic policy validates identity, scope, arguments, target, risk, budget, and approval. A tool adapter executes and returns a structured receipt with operation ID, target, result, side-effect status, and read-back evidence. Reject unknown tools, undeclared fields, ambiguous targets, and arguments derived from untrusted instructions.

Checkpoint after plan acceptance, approval, side-effect attempt, side-effect confirmation, and artifact commit. On restart, reconcile checkpoints with external state before continuing. Never infer an interrupted write failed merely because its response was lost.

Choose deterministic workflows for known sequences, routers for bounded task families, and autonomous loops only when discovery cannot be represented as a finite workflow. Add workers only for separable, independently verifiable tasks. A critic or verifier must have independent evidence and a distinct responsibility.

Acceptance tests must cover duplicate delivery, response loss after successful writes, stale inputs, expired approvals, revoked identity, malformed tool output, conflicting system-of-record values, worker disagreement, budget exhaustion, cancellation, and restart from every checkpoint. Record results against the contract revision.

## Ultron routing contract

**Choose this skill when:** designing the overall shape of an AI agent: whether it should be a single agent, tool-using loop, planner/executor, router, supervisor, specialist group, or event-driven workflow. It owns pattern selection, control ownership, state transitions, and the tradeoffs between autonomy and coordination.

**Route prompt and application-boundary work to `llm-app-agents-and-prompts` when:** the topology is already chosen and the task concerns prompt/runtime separation, structured outputs, model integration, or application-level orchestration.

**Route tool-interface design to `agent-tool-architecture` when:** the unresolved problem is how capabilities are exposed, authorized, versioned, or invoked.

**Handoff contract:** state the task class, chosen pattern, alternatives rejected, control owner, state machine, tool/delegation boundaries, failure recovery, and acceptance tests. A specialist implementation skill must not silently change the system's orchestration pattern.

**Why the boundary exists:** architecture selects the coordination model; implementation skills make that model reliable in their respective layers.
