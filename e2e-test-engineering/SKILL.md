---
name: e2e-test-engineering
description: Use when designing, writing, stabilizing, or reviewing end-to-end tests that exercise a deployed or near-production system through its user-facing or integration boundaries, including test environment setup, data seeding strategy, flake triage, and CI gating decisions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# E2E Test Engineering

## Purpose and boundaries

This skill covers end-to-end (E2E) tests: automated tests that drive a running system across real process, network, and storage boundaries to verify a user journey or business-critical flow. It guides journey selection, test design, environment and data strategy, flake diagnosis, and CI gating.

Out of scope: unit and component test design (use a unit-testing skill), load and performance testing, penetration testing, and production monitoring. Do not run E2E suites against production data or third-party live services without explicit approval (see Decision gates).

## Inputs and assumptions

Collect before starting:

- Target journeys: the user or system flows the business cares about, ranked by revenue, risk, or support volume.
- Environment: URL or endpoint, deployment topology, feature flags, and whether a dedicated test environment exists.
- Test framework and runner already in use. Do not introduce a second framework without a stated reason.
- Data ownership: who creates, reads, and deletes test data, and which systems hold it.
- Existing failure history: last 30 days of CI runs, flake rates, and open quarantine items.
- Run budget: maximum acceptable suite duration and parallelism limits.

When an input is unavailable, document the exact assumption in the test report and mark its effect on confidence.

## Operating workflow

1. **Select journeys.** Choose 5 to 15 critical paths for the first suite. Each journey must map to a business outcome (e.g., "customer completes checkout and receives confirmation"). Reject journeys that duplicate what a lower-level test already proves.
2. **Define the oracle.** For each journey, specify observable pass conditions: UI state, API response contract, persisted record, emitted event. Prefer assertions on durable outcomes over transient spinners or animation timing.
3. **Design isolation.** Each test creates its own uniquely named data (e.g., suffix with run ID plus test ID) and does not depend on execution order. Shared fixtures are read-only.
4. **Control dependencies.** Stub or sandbox third-party services (payment, email, SMS) using the vendor's documented test mode or a local fake. Verify the stub contract against vendor documentation before relying on it.
5. **Write selectors by contract.** Use dedicated test attributes (e.g., `data-testid`) or accessible roles and labels. Never select by generated class names or deep positional XPath.
6. **Replace fixed sleeps.** Wait on explicit conditions: network idle for a named request, element state, or a polled API status with a timeout.
7. **Run locally, then in CI, then repeat.** Execute each new test at least 20 times in a loop on CI-equivalent hardware. Record pass rate.
8. **Gate and report.** Wire the suite into the pipeline per the decision gates below.

## Decision gates

Stop and request explicit approval before:

- Running any test that writes to, deletes from, or migrates a shared, staging-shared, or production database.
- Sending real emails, SMS, payments, or webhooks to external recipients.
- Modifying CI pipeline required-check settings, branch protection, or secrets.
- Adding credentials to test code or repository files. Use the organization's secret store.
- Retrying a failing test in a way that masks a failure (e.g., automatic retry on any failure in a required gate).
- Introducing a new framework, browser grid vendor, or paid service.

Proceed without asking when work is read-only, runs against an isolated ephemeral environment, or edits test files only.

Quarantine rule: a test may be quarantined (excluded from the blocking gate, still run and reported) only with an owner, a linked defect, and an expiry of no more than 14 days.

## Verification and evidence

Measurable checks for every deliverable:

- Stability: each new or modified test passes at least 20 consecutive runs in CI-equivalent conditions. Any intermittent failure blocks merge until root cause is identified.
- Isolation: the suite passes when run in random order and when each test runs alone.
- Duration: the blocking suite finishes within the agreed budget; report p50 and p95 durations, not single runs.
- Coverage of journeys: a traceability table maps each journey to its test IDs and to the business requirement.
- Failure quality: a deliberately broken build (e.g., changed API field name) causes the relevant test to fail with a message naming the broken contract.
- Artifacts: failures produce screenshots, traces or HAR logs, and server logs correlated by test run ID, retained for at least the agreed window.

Record evidence as run links, pass-rate tables, and duration figures. Do not report pass rates from runs you did not perform.

## Failure handling

Triage flakes in this order:

1. Reproduce with the captured trace. If the failure cannot be reproduced in 10 attempts, record it as environmental and check infrastructure logs.
2. Classify the cause: timing (missing wait), data (shared state, leftover records), environment (service unavailable, rate limits), or product defect.
3. Fix timing and data causes in the test. Do not raise timeouts above the documented maximum to hide a race; find the condition to wait on.
4. For product defects, file a defect with the trace attached and keep the test blocking if the journey is critical.
5. If the root cause is an external dependency, escalate to its owner with the failing request and timestamp.

Do not disable tests silently, delete assertions to make a run green, or hard-code expected values copied from a failing output without verifying correctness against the specification.

## Deliverable contract

Every E2E engagement delivers:

- Journey inventory with priority, owner, and business requirement reference.
- Test code changes, with each test's ID, oracle, and data strategy documented in a header comment or adjacent README.
- Environment and data notes: required services, seed and teardown procedure, and stubbed dependencies with their verification source.
- Stability report: run counts, pass rates, and p50/p95 duration for the blocking suite.
- Open risks: quarantined tests with owners and expiry dates, unverified assumptions, and any version-sensitive framework or vendor behavior flagged for confirmation against current official documentation.
- Explicit list of approvals obtained and actions deferred pending approval.

Version-sensitive details (runner flags, browser versions, vendor test-mode behavior, API names) must be confirmed against current official documentation before being written into code or reports.