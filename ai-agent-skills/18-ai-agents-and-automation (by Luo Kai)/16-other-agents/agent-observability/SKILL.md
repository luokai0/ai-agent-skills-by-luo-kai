---
name: agent-observability
description: Plans observability for AI agents and tool workflows using traces, structured events, quality signals, latency, token and cost measurements, and privacy-aware logging. Use when operating, debugging, or optimizing agents in development or production.
metadata:
  author: Luo Kai
  provenance: original
  version: "1.0.0"
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
