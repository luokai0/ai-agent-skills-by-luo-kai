---
name: api-observability-reliability
description: Use when designing, auditing, or troubleshooting observability and reliability for APIs that depend on, publish to, or mirror external registries (package indexes, container registries, schema or API catalogs, plugin marketplaces).
author: Luo Kai
provenance: original
version: 1.1.0
---

# Api Observability Reliability

## Purpose and boundaries

This skill covers the operational health of API traffic between your systems and external registries: measuring it, alerting on it, degrading gracefully when it fails, and producing evidence that the integration works. It does not cover registry content governance, package security review, or licensing. Hand those off to the owning teams.

## Inputs and assumptions

Collect before acting:
- Registry inventory: each external registry, its role (read, publish, or both), and the endpoints your code calls.
- Current telemetry: existing logs, metrics, traces, and dashboards for those calls, if any.
- Traffic profile: request volume, peak periods, and which workloads depend on each registry.
- Published limits and error semantics: rate limits, retry guidance, and status code meanings. Treat these as version-sensitive and verify them against the registry's current official documentation before encoding them.
- Recovery objectives agreed with the service owner (latency and availability targets for dependent flows).

Assume nothing about undocumented headers, quotas, or SLAs. If a value is unknown, record it as unknown and ask.

## Operating workflow

1. **Map dependencies.** List every outbound call to an external registry, with caller, purpose, frequency, and criticality (blocking, degradable, or background).
2. **Define signals.** For each call class define:
   - Availability: proportion of successful responses, separating client errors (4xx) from server or network errors (5xx, timeouts, connection resets).
   - Latency: p50, p95, p99 measured at the client boundary.
   - Freshness: age of cached registry metadata used at decision time.
   - Throttling: count of rate-limit responses and time spent waiting.
3. **Instrument the boundary.** Emit one structured log line and one metric series per registry call. Tag by registry, operation, and outcome class. Never tag by raw URL with user or artifact identifiers (cardinality risk). Propagate a correlation ID into logs, and attach trace spans where tracing exists.
4. **Redact.** Strip credentials, tokens, signed URLs, and personal identifiers from logs before they leave the process.
5. **Set reliability controls.**
   - Timeouts on every call, sized from measured p99 with headroom, not defaults.
   - Retries only for idempotent reads, with exponential backoff and jitter, capped in count and total elapsed time.
   - Honour explicit retry or wait guidance from the registry before applying your own backoff.
   - Circuit breakers that open on sustained error-rate thresholds and probe half-open at a fixed interval.
   - Local caches with a defined maximum staleness per data type.
   - A fallback path (mirror, last-known-good cache, or deferred queue) for each degradable call.
6. **Build alerts on symptoms.** Alert on SLO burn rate for the dependent user-facing flow, not on every registry error. Use a separate low-severity signal for throttling trends.
7. **Write runbooks.** Each alert links to a runbook covering: confirm registry status from its official status channel, check throttling, check credential expiry, enable or verify fallback, and communicate impact.

## Decision gates

- **Retry or not:** Retry only if the operation is idempotent and the error is transient (timeout, 429, 503). Never retry publish operations without an idempotency key or a confirmed server-side deduplication behaviour.
- **Fallback choice:** Use stale cache only where staleness is within the agreed bound. Use a queue only where the operation can complete later without user-visible inconsistency.
- **Alert threshold change:** Requires baseline data covering at least one full traffic cycle.
- **Mirror or failover to a second registry:** Requires explicit approval from the service owner, because it changes trust and provenance of artifacts.
- **Any change that alters publish behaviour, credentials, or traffic routing to a production registry:** Requires explicit human approval before execution.

## Verification and evidence

- Load test or replay representative traffic against a non-production stub or sandbox the registry provides; confirm timeouts, retries, and breaker transitions behave as configured.
- Inject faults (timeouts, 429s, malformed responses) and record breaker state, retry count, and user-facing outcome.
- Confirm each metric and log field appears in the dashboard within the expected ingestion delay.
- Quality checks: no unbounded metric labels; zero credentials in log samples; every blocking call has an explicit timeout; every degradable call has a documented fallback; every alert has a runbook link.
- Record evidence as: test date, configuration version, fault scenario, observed metric values, and pass or fail against the stated target. Do not report results you did not measure.

## Failure handling

- If telemetry is missing for a call class, treat reliability as unknown and block sign-off on that class.
- If the registry's documentation conflicts with observed behaviour, record both, prefer observed behaviour for safety settings, and flag for verification.
- If a fallback path fails, escalate; do not silently fall through to an unbounded retry loop.
- If redaction cannot be confirmed, disable the log field and report the gap.

## Deliverable contract

Produce:
1. Dependency inventory table: registry, operation, criticality, timeout, retry policy, fallback, owner.
2. Signal definitions with metric names, labels, and SLO targets.
3. Configuration summary for timeouts, retries, breakers, and cache staleness bounds.
4. Alert list with severity, burn-rate basis, and runbook reference.
5. Verification record per the evidence format above.
6. Open items list, including every version-sensitive detail still awaiting confirmation against official documentation.

Do not claim compliance certification, guaranteed availability, or performance figures that were not measured. Do not change production registry configuration, credentials, or publish behaviour without explicit approval.

## Ultron routing contract

**Choose this skill when:** operating the reliability of an API integration with an external registry or service: request/response telemetry, rate limits, retries, timeouts, circuit breaking, graceful degradation, and evidence that the integration is healthy.

**Choose sre-observability-and-incidents when:** the problem concerns service-wide SLOs, platform telemetry, alert ownership, incident command, mitigation, communications, or post-incident learning across multiple services.

**Handoff contract:** this skill supplies API-specific request metrics, upstream error classes, retry and latency distributions, dependency health, and integration failure modes. The SRE skill uses those signals in service-level objectives and incident timelines, then returns operational thresholds and response ownership.

**Why the boundary exists:** an API client can be healthy or unhealthy independently of the wider service; service-level reliability needs a broader view and incident process.
