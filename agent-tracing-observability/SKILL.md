---
name: agent-tracing-observability
description: Use when instrumenting, debugging, or auditing LLM agent runs (tool calls, model calls, retrievals, sub-agent handoffs) and you need traces, spans, token and cost accounting, or evidence of what an agent actually did.
author: Luo Kai
provenance: original
version: 1.3.0
---

# Agent Tracing Observability

## Purpose and boundaries

This skill designs and reviews tracing for autonomous or semi-autonomous agent systems: capturing a structured record of each run so engineers can reconstruct decisions, diagnose failures, measure cost and latency, and verify behavior against expectations.

In scope: trace data model design, span boundaries, attribute schemas, redaction rules, sampling policy, cost and token attribution, trace-based evaluation, and incident reconstruction.

Out of scope: model selection, prompt authoring quality, general application APM unrelated to agent steps, and any claim that tracing guarantees safety or regulatory compliance.

## Inputs and assumptions

Gather before designing:
- Agent topology: single loop, planner/executor, multi-agent handoffs, or workflow graph.
- Step types: model calls, tool invocations, retrievals, memory reads/writes, human approvals, sub-agent calls.
- Data sensitivity: what prompts, tool arguments, and outputs may contain (personal data, credentials, customer records).
- Storage and retention constraints, and who may read traces.
- Existing telemetry stack. If you rely on a specific tracing standard or SDK, verify current attribute names and semantic conventions against its official documentation; they change between versions.

Assume nothing about provider token counting or pricing; use the values the provider returns and mark any price table as version-sensitive.

## Operating workflow

1. **Map the run.** Draw the actual execution graph from logs or code, not the intended design. Identify every point where control leaves the agent (tool, API, file write, message send).
2. **Define spans.** One root span per user-visible task or job. Child spans for each model call, tool call, retrieval, and handoff. Avoid spans for trivial in-memory string operations.
3. **Set the attribute schema.** For each span record: run ID, parent ID, step index, span kind, model or tool name, version identifier, start and end time, status, input and output size, token counts (input, output, cached if reported), and error class.
4. **Apply redaction before export.** Hash or drop secrets, credentials, and personal identifiers at the instrumentation point, not in the backend.
5. **Choose sampling.** Keep 100% of error and policy-flagged runs; sample successful high-volume runs. Record the sampling decision on the root span so analyses can correct for it.
6. **Attribute cost.** Sum token usage per run and per step. Compute cost only with a dated, versioned price table recorded alongside the data.
7. **Link to evaluation.** Store the expected outcome or rubric reference on the root span when one exists, so trace review can be scored.
8. **Validate with a replay.** Run a known task end to end and confirm the trace reconstructs the sequence, arguments, and results.

## Decision gates

Stop and request explicit approval before:
- Enabling capture of full prompts, tool arguments, or model outputs in any environment that holds real customer or personal data.
- Exporting traces to a third-party service or outside the current data boundary.
- Changing retention periods, deleting existing traces, or purging audit records.
- Turning on tracing in production for a system that performs writes, payments, messages, or other external actions, if the change alters runtime behavior or adds latency on the critical path.
- Adding any tool that lets the agent read its own traces, since this can create feedback loops and data exposure.

Proceed without a gate for: local development traces with synthetic data, span naming changes in a non-production branch, and dashboard construction on already-approved fields.

## Verification and evidence

Check each of the following and record results:
- **Completeness:** for a replayed run of N known steps, the trace contains N step spans with correct parent-child links. Target: zero missing or orphaned spans.
- **Ordering:** timestamps are monotonic within each parent; child spans fall inside parent intervals.
- **Token accounting:** sum of per-step tokens equals the run total within the provider's reported figures. Any discrepancy is logged, not averaged away.
- **Redaction:** a seeded canary string placed in a test input must not appear in any exported attribute. Zero occurrences required.
- **Error fidelity:** an injected tool failure appears as an error status with a classified error type, and the agent's subsequent step is linked to it.
- **Overhead:** measure added latency with and without instrumentation on the same workload; report the median and p95 difference. Do not claim a figure you have not measured.

## Failure handling

- **Missing spans:** check async context propagation first; spans created in detached tasks or callbacks often lose parent links.
- **Duplicated spans:** typically retries re-emitting spans. Give each attempt its own span with an attempt counter rather than suppressing it.
- **Oversized payloads:** store large inputs or outputs by reference (content hash plus a secured store) and record byte size inline.
- **Redaction false negatives:** treat any leaked sensitive value as a severity incident. Halt export, identify affected records, and request approval before deletion.
- **Clock skew across services:** record both local timestamps and the sequence index; do not reorder by timestamp alone.

## Deliverable contract

Deliver:
1. A span tree diagram for the agent's main flow.
2. An attribute table with field name, type, source, redaction class, and whether it is required.
3. Sampling and retention policy with the approval status of each setting.
4. Verification results from the checks above, with actual counts and measured values.
5. A list of open items, each marked as requiring verification against current official documentation where a version-specific detail applies.

Do not deliver a trace design that has not been replayed, claims tracing makes an agent correct or compliant, or contains unredacted sensitive fields in examples.
## End-to-end agent run evidence (v1.1)

Instrument the entire run, not just model calls. Connect the user request, run contract, plan revision, policy decisions, model turns, tool invocations, approvals, worker tasks, checkpoints, artifacts, and final verification. Use stable correlation identifiers for run, task, step, tool call, approval, and external operation.

Capture structured events for run creation and contract revisions; plan generation, validation, and rejection; policy decisions with policy version and reason; approval request, grant, denial, expiry, or invalidation; tool request, authorization, execution, retry, reconciliation, and verification; worker dispatch and acceptance; checkpoint save and restore; artifact digest; and terminal status.

Record timestamps plus a monotonic sequence number. Distinguish model intention from gateway authorization and downstream execution. Store large payloads by protected reference and digest; traces must not become a second database of sensitive content.

Measure verified task completion, tool error rate by class, approval wait time, duplicate suppression, retries per operation, recovery success, policy denials, injection detections, checkpoint restore success, and cost/latency per completed task. Segment by agent version, tool version, task family, and risk class. Faster execution achieved by skipping verification is a regression.

Alert on repeated denials, unusual tool sequences, unexpected privilege use, excessive retries, runaway spend, cross-tenant attempts, missing approval receipts, and abnormal side-effect volume. Define an owner, severity, response window, and disable action for each alert. Preserve security-critical events even when ordinary spans are sampled out.

For consequential workflows, maintain an append-only event ledger with hash-linked records or another suitable tamper-evident mechanism. Record hashes and references rather than raw sensitive payloads. Protect ledger access separately from the runtime. Define retention, access, export, and deletion rules before launch; immutability must not be used to evade retention or deletion requirements.

## Telemetry privacy, audit integrity, and evidence boundaries (v1.2)

Metrics, traces, logs, and audit records answer different questions. Do not treat them as interchangeable evidence.

### Signal responsibilities
- **Metrics** describe aggregate behavior such as latency, error classes, token use, tool-call rates, cost, and policy-denial rates. Use bounded dimensions and avoid request content or high-cardinality identifiers as metric labels.
- **Traces** connect stages of a request and help locate latency or failure across model calls, retrieval, policy checks, and tools. Sampling, missing instrumentation, and best-effort exporters mean a trace is not a complete audit ledger.
- **Operational logs** capture bounded diagnostic events and service errors. Prefer normalized error categories over raw provider messages that may contain user content or credentials.
- **Audit evidence** records attributable decisions and consequential actions for investigation. It requires explicit delivery, access, integrity, and retention guarantees beyond ordinary telemetry.

### Privacy-by-design capture
Before enabling content-bearing telemetry, define the purpose, data owner, approved fields, access roles, retention period, residency constraints, and redaction method. Default to metadata and digests rather than raw prompts, completions, tool arguments, documents, or retrieved passages.

Never emit passwords, API keys, bearer tokens, refresh tokens, private keys, session cookies, or authentication headers. Treat user identifiers, tenant identifiers, file paths, and correlation metadata as potentially sensitive even when message content is absent. Restrict access and retention accordingly.

Use allowlisted structured fields rather than serializing arbitrary request objects. Apply redaction before data leaves the process, not only in a downstream dashboard. Test redaction against nested errors, retries, exception traces, and malformed tool responses.

### Correlation and attribution
Use server-generated run and span identifiers. Treat caller-supplied correlation IDs as untrusted metadata, not identity or authorization. Preserve distinct fields for requested model, served model, agent version, skill digest, tool version, policy version, initiating subject, and task identity when available and permitted.

Record both admission and completion evidence for consequential operations:
- Admission: caller and task identity, policy version, action classification, normalized destination, decision, and approval reference.
- Completion: downstream operation identifier, outcome, postcondition verification, retries or reconciliation, and artifact digest where relevant.

A successful admission does not prove the action completed. A tool response does not prove the intended external state changed. Verify the postcondition through an authoritative read path.

### Durable audit delivery
For actions requiring durable evidence, use an append-only or tamper-evident store with explicit acknowledgement, access separation, retention, and export controls. Track dropped, delayed, duplicated, and rejected audit events. Define whether an action must fail closed when audit persistence is unavailable; do not imply that guarantee exists unless the execution path enforces it.

Keep audit integrity controls separate from the agent runtime so an agent cannot rewrite or erase its own evidence. Hash chaining can help detect alteration, but it does not by itself prove event completeness, truthful event generation, or correct retention.

### Verification tests
Test that:
- Secrets and personal content are absent from metrics, traces, logs, and error paths.
- Metric dimensions remain bounded under high-cardinality traffic.
- A sampled-out trace does not remove required audit evidence.
- Missing audit acknowledgement triggers the documented policy behavior.
- Correlation IDs cannot be used to impersonate another task or subject.
- Admission and completion records can be joined without exposing raw sensitive payloads.
- An agent runtime cannot modify or delete the durable audit record.

Report telemetry coverage, known blind spots, retention, redaction tests, and delivery guarantees separately. Do not claim compliance or complete forensic reconstruction from instrumentation alone.

## Ultron routing contract

**Choose this skill when:** instrumenting agent-specific execution: model turns, tool calls, handoffs, approvals, memory access, queue events, checkpoints, artifacts, and verified task outcomes.

**Choose `sre-observability-and-incidents` when:** the work concerns general service/platform telemetry, infrastructure health, SLOs, on-call alerting, or incident response across services rather than agent-run semantics.

**Choose `threat-hunting-incident-response` or the relevant security response skill when:** telemetry indicates a security incident that needs investigation and containment, not merely an observability dashboard.

**Handoff contract:** agent tracing emits bounded, privacy-reviewed run and action evidence with stable identifiers and policy/version context. The platform SRE skill consumes service-level signals and owns operational response. Security incident response consumes attributable events and owns investigation. Keep metrics, sampled traces, logs, and durable audit records distinct.

**Why the boundary exists:** agent behavior needs semantic traces, but platform reliability and security incident management require different owners, retention, and response guarantees.
