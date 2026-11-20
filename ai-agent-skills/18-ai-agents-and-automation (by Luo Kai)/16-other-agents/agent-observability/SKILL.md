---
name: agent-observability
description: Plans observability for AI agents and tool workflows using traces, structured events, quality signals, latency, token and cost measurements, and privacy-aware logging. Use when operating, debugging, or optimizing agents in development or production.
metadata:
  author: Luo Kai
  provenance: original
  version: "1.1.0"
---
# Agent Observability

## Goal

Make agent behavior understandable without collecting more private data than necessary. Observability should answer what happened, why a workflow failed, which tools were involved, and what it cost.

## 1. Define the operating model

Map the lifecycle: request received and authenticated; context assembled and retrieval performed; model invocation and response; tool selection, authorization, and execution; retries, handoffs, and subagent activity; validation, final response, and user-visible side effects.

Assign a correlation ID to each user request and propagate it across model calls, tools, queues, and downstream services. Use separate identifiers for users, tenants, sessions, and spans; do not put raw personal identifiers into metric labels.

## 2. Capture structured events

Recommended fields include timestamp and correlation ID; service, agent, model, prompt/template version; task category and workflow stage; tool name, normalized operation, and authorization result; outcome, error category, retry count, and duration; input/output size, token counts, and estimated cost when available; safety intervention and human approval state; and deployment and dependency versions.

Record content only when there is a documented need, legal basis, and retention policy. Prefer hashes, redacted summaries, schema metadata, or references to controlled storage.

## 3. Build traces around decisions

Represent each request as a trace with child spans for retrieval, model calls, tool calls, and validation.

- Record timing and status for each span.
- Preserve parent-child relationships during agent handoffs.
- Capture tool arguments only after redaction and minimization.
- Distinguish a tool being proposed, authorized, attempted, and successfully completed.
- Record whether the final state was independently verified.
- Avoid storing hidden reasoning or private chain-of-thought. Log observable decisions, evidence references, and action metadata instead.

## 4. Measure service and agent quality

| Area | Signals |
|---|---|
| Reliability | Success rate, error rate, timeout rate, retry recovery |
| Latency | End-to-end duration and per-stage percentiles |
| Tool behavior | Calls per task, authorization denials, tool failure rate |
| Quality | Evaluation pass rate, verified outcome rate, user corrections |
| Safety | Blocked unsafe actions, confirmed incidents, data exposure |
| Cost | Tokens, model cost, tool cost, cost per successful task |
| Capacity | Queue depth, concurrency, rate-limit events |

Define service-level indicators and objectives for important workflows. Segment by task type and model version so a global average cannot hide a failing feature.

## 5. Track cost responsibly

- Record actual provider usage when returned by the provider.
- Label estimates as estimates.
- Include retries, retrieval, tools, and background work where measurable.
- Calculate cost per successful task, not only cost per request.
- Set budgets and alert thresholds by workflow or tenant.
- Do not silently switch models or reduce quality to satisfy a budget; make fallback behavior explicit.

## 6. Protect privacy and secrets

- Never log passwords, API keys, authorization headers, session cookies, private keys, or full payment credentials.
- Redact personal data and sensitive file content before export.
- Apply access controls to telemetry and separate tenants.
- Define retention, deletion, and incident-response procedures.
- Avoid sending user content to analytics vendors without an approved data-processing basis.
- Test redaction using synthetic secrets and known patterns.

## 7. Alert on actionable conditions

Alert on sudden rises in task failures or latency; tool errors or authorization denials above baseline; repeated retries or runaway agent loops; cost spikes and budget exhaustion; increased safety blocks or confirmed incidents; missing telemetry or broken correlation propagation; and cross-tenant access attempts or unexpected destinations.

Every alert needs an owner, severity, runbook, and expected response. Avoid alerting on every model variation.

## 8. Debug with evidence

1. Locate the request by correlation ID.
2. Reconstruct the trace and tool sequence.
3. Identify the first failed or unexpected transition.
4. Compare prompt, model, tool, and dependency versions.
5. Check authorization decisions and state changes.
6. Reproduce with sanitized fixtures.
7. Add a regression evaluation before closing the issue.

Do not infer success from a natural-language claim. Verify the external state or downstream record.

## 9. Operational checklist

Before launch, confirm trace propagation, event schemas, redaction, access control, retention, dashboards, alert ownership, cost accounting, incident runbooks, and evaluation coverage. Test telemetry failure modes so an unavailable observability backend does not silently disable core authorization or safety controls.

## 10. Define reliable service-level indicators

For each critical workflow, define the event that starts the measurement, the event that counts as completion, the eligible population, and the exclusions. Use explicit denominators and consistent time windows.

- Separate availability from task correctness. A service can respond successfully while the agent completes the wrong task.
- Measure end-to-end task success alongside stage-level latency and failure rates.
- Use percentiles and distributions for latency; averages alone hide long-tail failures.
- Track verified completion separately from claimed completion.
- Define objectives over rolling windows and specify how missing telemetry affects the measurement.
- Avoid changing the metric definition during an incident or comparison without recording a new revision.

## 11. Control telemetry volume and metric cardinality

- Use metrics for bounded dimensions such as service, workflow type, model family, tool name, region, and outcome category.
- Keep request IDs, user IDs, tenant IDs, raw URLs, prompt text, and arbitrary error messages out of metric labels.
- Use traces or access-controlled event stores for high-cardinality diagnostic context.
- Apply head or tail sampling deliberately. Preserve error, timeout, safety, and high-impact action traces where policy permits.
- Record sampling rates and sampling decisions so dashboards do not imply complete capture when only a fraction of events were retained.
- Bound event sizes and drop or truncate oversized content safely, while retaining a clear indicator that truncation occurred.

## 12. Instrument retries, loops, and asynchronous work

Record retry reason, attempt number, backoff, idempotency key reference, cancellation state, and terminal outcome. Track agent-loop iterations, handoff depth, subagent count, and elapsed time against explicit limits.

For queued or background operations, propagate trace context through message metadata and record enqueue, dequeue, processing, retry, dead-letter, and completion events. Do not reuse one trace ID for unrelated user requests. If context propagation is unavailable, create a linked trace and preserve a safe correlation reference.

## 13. Make telemetry failure safe

Observability must not become a hidden dependency that changes security behavior.

- Define which telemetry failures may be buffered, sampled, dropped, or cause a workflow to stop.
- Never bypass authorization, approval, audit requirements, or safety checks because the telemetry backend is unavailable.
- Use bounded local buffers and backpressure to prevent telemetry outages from exhausting memory or blocking critical request paths indefinitely.
- Protect queued telemetry as sensitive data, including access control, encryption, retention, and deletion.
- Emit a safe health signal when telemetry is degraded, and alert when critical event streams disappear.

## 14. Connect runtime signals to evaluation and change history

Attach deployment, prompt, model, tool-schema, policy, and dependency revisions to traces where possible. Link production incidents and recurring user corrections to evaluation cases without copying unnecessary private content.

Compare quality and cost by comparable task cohorts. Annotate rollouts, experiments, traffic shifts, and model changes so operational changes are not mistaken for model improvements. Use controlled experiments for causal claims and keep benchmark results separate from noisy production indicators.

## 15. Maintain dashboards and incident runbooks

Create separate views for service health, agent task outcomes, tool behavior, safety events, cost, and capacity. Each panel should have a defined metric, denominator, time window, owner, and useful drill-down path.

For every actionable alert, document severity, triage steps, evidence to preserve, containment actions, escalation owner, recovery criteria, and post-incident evaluation updates. Test runbooks periodically using synthetic events.

## 16. Review observability changes as data-access changes

Before adding a field, destination, exporter, dashboard, or vendor integration, document its purpose, sensitivity, access scope, retention, residency requirements, and deletion behavior. Review changes to sampling and redaction with the same care as changes to application data handling.

Do not export raw prompts, tool payloads, or customer records merely because a telemetry platform can accept them. Collect the minimum evidence needed to operate and improve the system.
