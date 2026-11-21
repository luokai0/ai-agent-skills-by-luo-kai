---
name: sre-observability-and-incidents
description: Use when designing or reviewing observability (metrics, logs, traces, alerts, SLOs, dashboards) or when triaging, coordinating, mitigating, or writing up production incidents for cloud-hosted services.
author: Luo Kai
provenance: original
version: 1.0.0
---

# SRE Observability and Incidents

## Purpose and boundaries

This skill covers two linked activities: making production services observable enough to detect and diagnose problems, and running incidents from detection through post-incident review. It produces alert rules, SLO definitions, triage notes, incident timelines, mitigation plans, and postmortems.

In scope: service-level indicators and objectives, alert design, dashboard structure, telemetry gap analysis, incident triage, communication cadence, mitigation selection, and blameless review.

Out of scope: writing application features, general security incident forensics (hand off to the security team), capacity procurement, and legal or regulatory breach determinations.

## Inputs and assumptions

Before acting, confirm:

- Service name, owner, tier, and user-facing journeys it supports.
- Current telemetry sources (metrics backend, log store, tracing system) and their retention. Do not assume names; ask or inspect configuration.
- Existing SLOs, alert rules, and runbooks, with their last review date.
- For incidents: start time (or best estimate), severity, customer impact signals, recent changes (deploys, config, flags, dependencies, traffic events).
- Access constraints. Assume read-only access unless the incident commander explicitly grants change access.

If telemetry is absent for a critical path, state that as a finding rather than inferring health.

## Operating workflow

**Observability design**
1. Map each user journey to 1–3 SLIs (for example, availability as good requests divided by valid requests; latency as proportion under a threshold; freshness for data pipelines).
2. Set SLO targets from observed baseline data over a representative window, then review with the product owner. Derive error budgets from them.
3. Write burn-rate alerts: a fast-burn page and a slow-burn ticket, each using multiple windows to reduce noise. Every page must map to a runbook entry with a first action.
4. Check instrumentation coverage: RED or golden-signal metrics per service, trace propagation across service boundaries, structured logs with request or trace identifiers, and deploy or config change events on dashboards.
5. Remove or downgrade alerts that fired repeatedly without action in the last 30 days.

**Incident response**
1. Declare or confirm severity. Assign roles: incident commander, operations lead, communications owner, scribe. One person may hold several roles at low severity.
2. Open a timeline immediately. Record timestamps in UTC, observations, hypotheses, and actions, each labeled with who took it.
3. Establish impact: affected journeys, error rate or latency versus SLO, customer counts or regions where measurable.
4. Correlate with changes: list deploys, flag flips, config pushes, dependency status pages, and traffic shifts in the last 2 hours.
5. Form one hypothesis at a time. Test it with the least invasive query or check that could falsify it.
6. Choose mitigation before root cause. Preferred order: revert the recent change, disable the feature flag, fail over, shed load, scale. Root-cause work continues after impact stops.
7. Update stakeholders on a fixed cadence (for example every 30 minutes for high severity) even when nothing has changed.
8. Confirm recovery against the same SLI that alerted, sustained for a stated observation period, before resolving.
9. Within an agreed window after resolution, produce a blameless postmortem.

## Decision gates

- **Paging versus ticketing:** Page only if a user-facing SLO is burning at a rate that exhausts budget within hours, or if a safety-critical function is down. Otherwise create a ticket.
- **Rollback versus forward-fix:** Roll back when the change is the most likely cause and rollback is tested and low-risk. Forward-fix only when rollback would cause data loss, schema incompatibility, or is unavailable.
- **Mitigation requiring approval:** Obtain explicit approval from the incident commander and service owner before any of the following: deleting or truncating data, altering production databases, modifying IAM or network policy, disabling security controls, failing over cross-region, changing customer-facing communications, or sending external status page updates. Record the approver and time.
- **External communication:** Draft status updates; do not publish them without approval from the communications owner. Do not state root cause externally until confirmed.
- **Closing an incident:** Close only when the SLI is back within target for the observation window and no mitigation remains temporary without a tracking ticket.

## Verification and evidence

- Every alert change includes a test: replay historical data or use a synthetic signal to show it would have fired at the intended time and not during a known-good window.
- Every root-cause claim cites at least one primary signal (metric graph, log query result, trace) with the query or link preserved.
- Dashboards show the SLI, the SLO line, error budget remaining, and change markers.
- Quality checks for observability work: alert-to-runbook coverage at 100% for pages; zero pages without a named owner; trace sampling rates and log retention documented; no alert based solely on CPU without a user-impact companion.
- Quality checks for incidents: timeline gaps under 15 minutes during active response; stakeholder updates on cadence; time-to-mitigate and time-to-detect recorded from timeline timestamps, not memory.
- Metric backends, query languages, and alert syntax differ by vendor and version. Verify any query or rule syntax against current official documentation before deploying.

## Failure handling

- **Missing telemetry:** State the gap, use the nearest proxy (for example load balancer status codes), and add instrumentation as a follow-up action.
- **Conflicting signals:** Prefer user-facing SLIs over internal resource metrics. Note the conflict in the timeline.
- **Hypothesis stalls for 30 minutes:** Escalate to a second responder or pivot to mitigation.
- **Mitigation makes things worse:** Revert the mitigation immediately, record it, and re-assess.
- **Scope uncertainty:** Assume broader impact until narrowed by evidence.

## Deliverable contract

Return one of the following, depending on request:

- **Alert or SLO package:** SLI definitions with query logic described in plain language, SLO targets with rationale, burn-rate alert specifications, runbook links, test evidence, and a list of items marked for version verification.
- **Incident record:** Severity, impact summary, role assignments, timestamped timeline, hypotheses tested with outcomes, mitigation actions with approvers, recovery verification, and open follow-ups with owners and due dates.
- **Postmortem:** Summary, customer impact, detection and response analysis, contributing factors (systemic, not individual), what went well, action items with owners and priority, and a statement of confidence in the root cause.

Do not include fabricated metrics, unverified tool behavior, or compliance claims. Mark every unverified item explicitly.