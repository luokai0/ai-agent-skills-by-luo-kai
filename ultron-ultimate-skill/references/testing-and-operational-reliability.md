# Testing and Operational Reliability

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## api-observability-reliability

**Use when:** Use when designing, auditing, or troubleshooting observability and reliability for APIs that depend on, publish to, or mirror external registries (package indexes, container registries, schema or API catalogs, plugin marketplaces).

### Purpose and boundaries

This skill covers the operational health of API traffic between your systems and external registries: measuring it, alerting on it, degrading gracefully when it fails, and producing evidence that the integration works. It does not cover registry content governance, package security review, or licensing. Hand those off to the owning teams.

### Inputs and assumptions

Collect before acting:
- Registry inventory: each external registry, its role (read, publish, or both), and the endpoints your code calls.
- Current telemetry: existing logs, metrics, traces, and dashboards for those calls, if any.
- Traffic profile: request volume, peak periods, and which workloads depend on each registry.
- Published limits and error semantics: rate limits, retry guidance, and status code meanings. Treat these as version-sensitive and verify them against the registry's current official documentation before encoding them.
- Recovery objectives agreed with the service owner (latency and availability targets for dependent flows).

Assume nothing about undocumented headers, quotas, or SLAs. If a value is unknown, record it as unknown and ask.

### Operating workflow

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

### Decision gates

- **Retry or not:** Retry only if the operation is idempotent and the error is transient (timeout, 429, 503). Never retry publish operations without an idempotency key or a confirmed server-side deduplication behaviour.
- **Fallback choice:** Use stale cache only where staleness is within the agreed bound. Use a queue only where the operation can complete later without user-visible inconsistency.
- **Alert threshold change:** Requires baseline data covering at least one full traffic cycle.
- **Mirror or failover to a second registry:** Requires explicit approval from the service owner, because it changes trust and provenance of artifacts.
- **Any change that alters publish behaviour, credentials, or traffic routing to a production registry:** Requires explicit human approval before execution.

### Verification and evidence

- Load test or replay representative traffic against a non-production stub or sandbox the registry provides; confirm timeouts, retries, and breaker transitions behave as configured.
- Inject faults (timeouts, 429s, malformed responses) and record breaker state, retry count, and user-facing outcome.
- Confirm each metric and log field appears in the dashboard within the expected ingestion delay.
- Quality checks: no unbounded metric labels; zero credentials in log samples; every blocking call has an explicit timeout; every degradable call has a documented fallback; every alert has a runbook link.
- Record evidence as: test date, configuration version, fault scenario, observed metric values, and pass or fail against the stated target. Do not report results you did not measure.

### Failure handling

- If telemetry is missing for a call class, treat reliability as unknown and block sign-off on that class.
- If the registry's documentation conflicts with observed behaviour, record both, prefer observed behaviour for safety settings, and flag for verification.
- If a fallback path fails, escalate; do not silently fall through to an unbounded retry loop.
- If redaction cannot be confirmed, disable the log field and report the gap.

### Deliverable contract

Produce:
1. Dependency inventory table: registry, operation, criticality, timeout, retry policy, fallback, owner.
2. Signal definitions with metric names, labels, and SLO targets.
3. Configuration summary for timeouts, retries, breakers, and cache staleness bounds.
4. Alert list with severity, burn-rate basis, and runbook reference.
5. Verification record per the evidence format above.
6. Open items list, including every version-sensitive detail still awaiting confirmation against official documentation.

Do not claim compliance certification, guaranteed availability, or performance figures that were not measured. Do not change production registry configuration, credentials, or publish behaviour without explicit approval.

### Ultron routing contract

**Choose this skill when:** operating the reliability of an API integration with an external registry or service: request/response telemetry, rate limits, retries, timeouts, circuit breaking, graceful degradation, and evidence that the integration is healthy.

**Choose sre-observability-and-incidents when:** the problem concerns service-wide SLOs, platform telemetry, alert ownership, incident command, mitigation, communications, or post-incident learning across multiple services.

**Handoff contract:** this skill supplies API-specific request metrics, upstream error classes, retry and latency distributions, dependency health, and integration failure modes. The SRE skill uses those signals in service-level objectives and incident timelines, then returns operational thresholds and response ownership.

**Why the boundary exists:** an API client can be healthy or unhealthy independently of the wider service; service-level reliability needs a broader view and incident process.


## debugging-and-root-cause

**Use when:** Use when a defect, test failure, crash, regression, or unexpected behavior needs diagnosis to a verified root cause before a fix is proposed or merged, including flaky tests and intermittent production symptoms.

### Purpose and boundaries

This skill turns a symptom into a verified root cause and a minimal, tested correction. It covers reproduction, isolation, hypothesis testing, causal explanation, and regression protection for application code, tests, build pipelines, and configuration.

In scope: failing tests, regressions after a change, crashes with stack traces, wrong outputs, intermittent or flaky failures, performance regressions traced to a specific change.

Out of scope: feature design, broad refactoring not required by the fix, incident communication, and security vulnerability disclosure (route those to their owners). Do not use this skill to justify a workaround as a fix without naming the underlying cause.

### Inputs and assumptions

Collect before acting:
- Exact symptom: error text, stack trace, expected versus actual output, timestamps.
- Environment: commit or build identifier, runtime and dependency versions from the lock file, OS, configuration, feature flags.
- Reproduction data: inputs, seed values, request payloads, sanitized sample records.
- Change history: commits, deploys, or dependency updates within the suspect window.

Assumptions must be written down. If the environment cannot be matched, record the gap and treat conclusions as provisional.

### Operating workflow

1. **State the symptom precisely.** Write one sentence: "Given X, the system does Y, but expected Z." Reject vague phrasing such as "it's broken."
2. **Reproduce deterministically.** Find the smallest input and environment that fails every time. For intermittent failures, run the case in a loop (for example 100 iterations) and record the failure rate before and after any change.
3. **Bisect the space.** Narrow by commit (binary search over history with a reliable pass/fail check), by input (delta-minimize the failing input), or by component (add boundary assertions or logs at interfaces).
4. **Form ranked hypotheses.** List at least two candidate causes. For each, state a prediction that would be false if the hypothesis were wrong.
5. **Test one hypothesis at a time.** Change one variable, observe, and record the result. Do not stack speculative edits.
6. **Explain the mechanism.** A root cause answers: what condition, in which code path, produced the wrong state, and why the symptom appeared where it did.
7. **Apply the minimal fix** at the cause, not at the symptom location.
8. **Add a regression guard** that fails before the fix and passes after.

### Decision gates

- **Gate A, reproduction:** Proceed to fixing only when the failure reproduces reliably, or when the failure rate is measured and documented for intermittent cases. If it cannot be reproduced after reasonable effort, stop and report what was tried; do not guess a fix.
- **Gate B, cause identification:** Proceed only when a single hypothesis is confirmed by evidence that the alternatives fail to explain. Correlation alone does not qualify.
- **Gate C, scope:** If the fix requires changing more than the failing module's contract, schema, public API, or data, stop and seek approval.
- **Gate D, flaky tests:** Do not increase timeouts, add retries, or delete assertions as the primary fix until a race, ordering dependency, shared state, or time dependency has been ruled in or out.

### Verification and evidence

Each conclusion must cite evidence:
- Reproduction command and observed output, before and after.
- The regression test name and its failure on the unfixed commit.
- Full existing test suite for the affected package passes, with the count of tests run recorded.
- For performance causes, measured timings from at least five runs with the same method before and after.

Quality checks:
- The regression test fails on the pre-fix code. Confirm this explicitly; a test that passed before the fix proves nothing.
- The fix diff touches the minimum set of files; record the line count.
- No new skips, disabled tests, broadened exception handlers, or widened tolerances unless justified in writing.

Mark version-sensitive details (runtime flags, debugger commands, library behavior changes) as requiring verification against current official documentation before relying on them.

### Failure handling

- **Cannot reproduce:** Report the attempted environments, inputs, and the gap. Request production-equivalent data or logs. Do not ship speculative changes.
- **Multiple causes found:** Fix them separately, each with its own test and evidence, and state which symptom each explains.
- **Fix breaks other tests:** Revert the hypothesis, re-examine whether the existing tests encoded incorrect behavior, and escalate that question rather than silently editing expectations.
- **Evidence contradicts hypothesis:** Discard it explicitly and return to step 4.

### Deliverable contract

Produce a report containing:
1. Symptom statement and environment identifiers.
2. Reproduction steps and measured failure rate.
3. Ranked hypotheses with the evidence for and against each.
4. Root cause in one paragraph naming the code path and triggering condition.
5. Patch summary, changed files, and minimal diff rationale.
6. Regression test name and before/after results.
7. Open risks and unverified assumptions, including any version-sensitive items.

### What not to do

- Do not apply a fix before a cause is confirmed.
- Do not catch and suppress the exception to make the symptom disappear.
- Do not add sleeps, retries, or longer timeouts to hide races.
- Do not run destructive commands (dropping databases, force-resetting shared branches, deleting production data or logs) without explicit approval.
- Do not send sanitized or unsanitized production data, credentials, or customer records to external tools or services without explicit approval.
- Do not deploy, roll back, or change feature flags in shared environments without explicit approval.
- Do not invent flags, API names, or benchmark numbers; verify them against current documentation.


## diagnostics-and-verification

**Use when:** Use when diagnosing a Windows machine problem (crashes, slowness, service failures, network or driver faults, update errors) or verifying that a change actually fixed it, and the work needs read-only evidence collection, a hypothesis, and a measured before-and-after result.

### Purpose and boundaries

This skill covers finding the cause of a Windows fault from evidence and confirming the result with measurements. It covers the investigation phase, the decision to change anything, and the post-change check.

It does not cover building new automation, hardening policy, forensic imaging, or incident response on a suspected compromise. If evidence points to malicious activity, stop and escalate.

### Inputs and assumptions

Collect before acting:

- Exact symptom, with timestamps and frequency.
- Windows edition and build (`winver` or `Get-ComputerInfo`), and what changed recently (updates, drivers, software, hardware, policy).
- Whether the session is elevated, and whether the machine is managed (domain, MDM, endpoint agent). Managed devices may have a change process you must follow.
- Whether a restore point, backup, or recovery media exists.

Assume nothing about cmdlet parameters or tool switches. Confirm them with `Get-Help <cmdlet> -Full` or the current Microsoft Learn documentation, because behavior varies across Windows builds and PowerShell versions. Mark any detail you could not verify as unverified in your report.

### Operating workflow

1. **Reproduce or bound the symptom.** Write a one-line problem statement: what, when, how often, who is affected.
2. **Collect read-only evidence.** Use Event Viewer or `Get-WinEvent` filtered by time window and level (System, Application, and relevant operational logs), Reliability Monitor, `Get-Service` state, `Get-CimInstance` for hardware and OS data, Device Manager or `pnputil /enum-devices` for driver status, `Test-NetConnection` for connectivity, and Task Manager or Resource Monitor for resource pressure. For crashes, note bugcheck codes and faulting modules from minidump metadata.
3. **Form ranked hypotheses.** List at most three candidate causes, each tied to a specific log entry or measurement. Rank by evidence strength, not by familiarity.
4. **Test the cheapest discriminating hypothesis.** Prefer a check that separates two hypotheses over one that merely confirms a favorite. Examples: boot into safe mode to test a driver; compare behavior on a second user profile to test profile corruption; check whether the fault follows the network or the machine.
5. **Stop at the decision gate** before any change.
6. **Apply the minimal reversible fix**, one change at a time, recording the exact command or setting and the prior state.
7. **Verify** using the criteria in the verification section.
8. **Document** cause, evidence, change, and residual risk.

### Decision gates

Pause and obtain explicit user approval before:

- Deleting, moving, or overwriting files, registry keys, or user data.
- Changing boot configuration, BitLocker state, partitions, or firmware.
- Installing, uninstalling, or rolling back drivers, updates, or security software.
- Altering services, scheduled tasks, firewall rules, or startup items on a shared or managed device.
- Anything that restarts a production system, disconnects a user, or sends data off the machine.
- Running repair tools that modify system files (for example, `sfc /scannow` or DISM repair operations) on a machine without a current backup.

Proceed without approval only for read-only collection and for reversible changes to your own test user profile.

### Verification and evidence

A fix is verified only when:

- The original symptom no longer reproduces across the same conditions, over a defined observation window (for example, 24 hours of normal use or a specific number of repeated operations).
- The triggering error event does not recur in the same log channel within that window.
- The metric that was abnormal (CPU, disk latency, boot time, connection success rate) returns to a baseline you recorded before the change.
- Unrelated services and functions still work.

Record evidence as: command or query used, timestamp, raw output excerpt, and interpretation. Separate observed facts from inferences.

### Failure handling

- **No cause found after evidence collection:** report what was checked and ruled out, state confidence, and recommend the next data to collect. Do not guess-and-change.
- **Change made but symptom persists:** revert the change, confirm reversion, then test the next hypothesis.
- **Change made and something else breaks:** revert immediately, then check whether the regression was your change or a pre-existing fault.
- **Insufficient access (not elevated, missing logs):** report the access gap; do not work around permissions.

### Deliverable contract

Return a report containing:

1. Problem statement and scope.
2. Evidence table: source, query, timestamp, key finding.
3. Ranked hypotheses with the result of each test.
4. Action taken, with approval reference, exact change, and rollback procedure.
5. Verification results against the criteria above, with observation window stated.
6. Residual risks, unverified details, and recommended follow-up.

Do not claim a fix is permanent, complete, or compliant unless the verification evidence supports that specific claim.


## e2e-test-engineering

**Use when:** Use when designing, writing, stabilizing, or reviewing end-to-end tests that exercise a deployed or near-production system through its user-facing or integration boundaries, including test environment setup, data seeding strategy, flake triage, and CI gating decisions.

### Purpose and boundaries

This skill covers end-to-end (E2E) tests: automated tests that drive a running system across real process, network, and storage boundaries to verify a user journey or business-critical flow. It guides journey selection, test design, environment and data strategy, flake diagnosis, and CI gating.

Out of scope: unit and component test design (use a unit-testing skill), load and performance testing, penetration testing, and production monitoring. Do not run E2E suites against production data or third-party live services without explicit approval (see Decision gates).

### Inputs and assumptions

Collect before starting:

- Target journeys: the user or system flows the business cares about, ranked by revenue, risk, or support volume.
- Environment: URL or endpoint, deployment topology, feature flags, and whether a dedicated test environment exists.
- Test framework and runner already in use. Do not introduce a second framework without a stated reason.
- Data ownership: who creates, reads, and deletes test data, and which systems hold it.
- Existing failure history: last 30 days of CI runs, flake rates, and open quarantine items.
- Run budget: maximum acceptable suite duration and parallelism limits.

When an input is unavailable, document the exact assumption in the test report and mark its effect on confidence.

### Operating workflow

1. **Select journeys.** Choose 5 to 15 critical paths for the first suite. Each journey must map to a business outcome (e.g., "customer completes checkout and receives confirmation"). Reject journeys that duplicate what a lower-level test already proves.
2. **Define the oracle.** For each journey, specify observable pass conditions: UI state, API response contract, persisted record, emitted event. Prefer assertions on durable outcomes over transient spinners or animation timing.
3. **Design isolation.** Each test creates its own uniquely named data (e.g., suffix with run ID plus test ID) and does not depend on execution order. Shared fixtures are read-only.
4. **Control dependencies.** Stub or sandbox third-party services (payment, email, SMS) using the vendor's documented test mode or a local fake. Verify the stub contract against vendor documentation before relying on it.
5. **Write selectors by contract.** Use dedicated test attributes (e.g., `data-testid`) or accessible roles and labels. Never select by generated class names or deep positional XPath.
6. **Replace fixed sleeps.** Wait on explicit conditions: network idle for a named request, element state, or a polled API status with a timeout.
7. **Run locally, then in CI, then repeat.** Execute each new test at least 20 times in a loop on CI-equivalent hardware. Record pass rate.
8. **Gate and report.** Wire the suite into the pipeline per the decision gates below.

### Decision gates

Stop and request explicit approval before:

- Running any test that writes to, deletes from, or migrates a shared, staging-shared, or production database.
- Sending real emails, SMS, payments, or webhooks to external recipients.
- Modifying CI pipeline required-check settings, branch protection, or secrets.
- Adding credentials to test code or repository files. Use the organization's secret store.
- Retrying a failing test in a way that masks a failure (e.g., automatic retry on any failure in a required gate).
- Introducing a new framework, browser grid vendor, or paid service.

Proceed without asking when work is read-only, runs against an isolated ephemeral environment, or edits test files only.

Quarantine rule: a test may be quarantined (excluded from the blocking gate, still run and reported) only with an owner, a linked defect, and an expiry of no more than 14 days.

### Verification and evidence

Measurable checks for every deliverable:

- Stability: each new or modified test passes at least 20 consecutive runs in CI-equivalent conditions. Any intermittent failure blocks merge until root cause is identified.
- Isolation: the suite passes when run in random order and when each test runs alone.
- Duration: the blocking suite finishes within the agreed budget; report p50 and p95 durations, not single runs.
- Coverage of journeys: a traceability table maps each journey to its test IDs and to the business requirement.
- Failure quality: a deliberately broken build (e.g., changed API field name) causes the relevant test to fail with a message naming the broken contract.
- Artifacts: failures produce screenshots, traces or HAR logs, and server logs correlated by test run ID, retained for at least the agreed window.

Record evidence as run links, pass-rate tables, and duration figures. Do not report pass rates from runs you did not perform.

### Failure handling

Triage flakes in this order:

1. Reproduce with the captured trace. If the failure cannot be reproduced in 10 attempts, record it as environmental and check infrastructure logs.
2. Classify the cause: timing (missing wait), data (shared state, leftover records), environment (service unavailable, rate limits), or product defect.
3. Fix timing and data causes in the test. Do not raise timeouts above the documented maximum to hide a race; find the condition to wait on.
4. For product defects, file a defect with the trace attached and keep the test blocking if the journey is critical.
5. If the root cause is an external dependency, escalate to its owner with the failing request and timestamp.

Do not disable tests silently, delete assertions to make a run green, or hard-code expected values copied from a failing output without verifying correctness against the specification.

### Deliverable contract

Every E2E engagement delivers:

- Journey inventory with priority, owner, and business requirement reference.
- Test code changes, with each test's ID, oracle, and data strategy documented in a header comment or adjacent README.
- Environment and data notes: required services, seed and teardown procedure, and stubbed dependencies with their verification source.
- Stability report: run counts, pass rates, and p50/p95 duration for the blocking suite.
- Open risks: quarantined tests with owners and expiry dates, unverified assumptions, and any version-sensitive framework or vendor behavior flagged for confirmation against current official documentation.
- Explicit list of approvals obtained and actions deferred pending approval.

Version-sensitive details (runner flags, browser versions, vendor test-mode behavior, API names) must be confirmed against current official documentation before being written into code or reports.

### Ultron routing contract

**Choose this skill when:** the behavior under test crosses real application boundaries: browser or client, running service, network, database, queue, identity provider, or external dependency. Use it for user journeys, business-critical workflows, deployment smoke tests, and integration behavior that cannot be proven by isolated tests.

**Choose `unit-and-component-testing` when:** the behavior can be verified inside a function, class, module, or component with external systems replaced by controlled test doubles.

**Handoff contract:** the unit/component layer supplies fast checks for local logic and contracts; this skill verifies that the assembled system actually works across boundaries. When an E2E failure occurs, isolate the failing boundary and return a minimal reproducible case to the owning unit, component, or integration test layer.

**Why the boundary exists:** E2E tests prove that components cooperate in a realistic environment; they are slower and less diagnostic, so they should not replace fast isolated tests.


## engineering-workflow-and-release

**Use when:** Use when planning, reviewing, or executing a software delivery workflow, branching and merge strategy, build-to-release pipeline, or release cutover for an engineering team, including release readiness checks, rollback planning, and release notes.

### Purpose and boundaries

This skill governs how a change moves from proposal to production: branching, review, integration, build, verification, release, and rollback. It produces workflow designs, release plans, readiness assessments, and release records.

In scope: branching model selection, merge policy, required checks, versioning scheme, release train or cadence, environment promotion, change freeze rules, rollback and roll-forward plans, release notes, and post-release review.

Out of scope: application architecture decisions (use a design-review skill), incident command during a live outage, security policy authoring, and vendor-specific CI syntax without checking current official documentation.

### Inputs and assumptions

Collect before advising:
- Team size, number of services or deployable units, and deployment targets.
- Current branching and merge practice, and the pain it causes (conflicts, late integration, unreleased work piling up).
- Existing CI stages, test suites with approximate runtime and flake rate, and artifact types.
- Release frequency goal and customer or regulatory constraints on change windows.
- Data stores and schema change practices, since these dominate rollback difficulty.

If any of these are missing, state the assumption explicitly in the deliverable. Do not assume a specific CI product, cloud provider, or tool version. Mark any tool-specific behavior as "verify against current official documentation."

### Operating workflow

1. Map the current path from commit to production. Record each stage, owner, average duration, and failure rate.
2. Identify the dominant bottleneck: integration delay, unreliable tests, manual approvals, environment drift, or schema coupling.
3. Select a branching model matched to release cadence. Short-lived trunk-based branches suit frequent deploys; release branches suit multiple supported versions. Do not adopt a long-lived integration branch to hide unfinished work.
4. Define merge requirements: review count, required status checks, linear or merge-commit policy, and who may bypass checks (ideally nobody).
5. Define versioning: state the scheme and where the version is derived (tag, manifest, or build metadata). Confirm it is unique per artifact.
6. Design promotion: build once, promote the same immutable artifact through environments. Rebuilding per environment is a defect.
7. Separate deploy from release. Use flags, traffic shifting, or staged rollout where the platform supports them; verify exact mechanisms against current documentation.
8. Write the rollback path for each release, classified by reversibility (see Decision gates).
9. Draft release notes from merged change records, grouped by user impact, with breaking changes first.

### Decision gates

Proceed to release only when all hold:
- All required checks pass on the exact artifact being promoted.
- Migration review is complete: schema changes are backward compatible with the previous application version (expand, migrate, contract).
- Rollback is classified and tested or rehearsed for the release's reversibility class.
- On-call owner and release lead are named, and the change window is confirmed.

Escalate for explicit human approval before:
- Any irreversible data migration, deletion, or column drop.
- Changes that affect external partners, public APIs, billing, or customer data.
- Bypassing a required check, force-pushing to protected branches, or deleting release tags.
- Releasing outside an agreed change window or during a declared freeze.
- Handling credentials, personal data, or regulated records in release tooling.

Reversibility classes:
- R1: code-only, stateless; roll back by redeploying prior artifact.
- R2: backward-compatible schema change; roll back by code redeploy, keep schema.
- R3: one-way data transformation or contract step; rollback requires a restore plan and explicit approval before release.

### Verification and evidence

Each release must carry evidence, not assertions:
- Artifact identifier and digest matching what was tested and promoted.
- Test results for the candidate, with failing or quarantined tests listed and justified.
- Canary or staged metrics compared against a stated baseline: error rate, latency percentile, and saturation signals. Set thresholds before rollout.
- Migration dry run result against a production-like copy, with duration measured.
- Rollback rehearsal result or a dated statement that it was not rehearsed, with reason.

Quality checks for the workflow itself:
- Median commit-to-production time and change failure rate are measured, not estimated. Report both with the measurement window.
- Flaky-test quarantine count is tracked and trending down; no test stays quarantined beyond an agreed period.
- Zero manual edits to artifacts between build and production.

Do not state benchmark figures, DORA tier placements, or compliance guarantees unless the user supplies the measured data.

### Failure handling

- Check failure on candidate: stop promotion, do not waive. Route to owner with failing evidence.
- Metric regression during rollout: halt traffic increase, execute the classified rollback, preserve logs and artifact identifiers.
- Migration fails midway: stop, do not retry destructively; assess whether the application can run on current schema, then escalate for approval.
- Missing rollback path discovered late: block release until one exists or the change is reclassified and approved.
- Ambiguous tool behavior: record the uncertainty and the documentation to verify; do not guess flags or syntax.

### Deliverable contract

Produce a single document containing:
1. Current-state map with measured stage durations and the identified bottleneck.
2. Recommended branching, merge, versioning, and promotion policy with rationale tied to cadence.
3. Per-release checklist with reversibility class, gate status, named owners, and window.
4. Approval requests, listed separately, for every action in the escalation list.
5. Evidence index linking artifact digest, test results, migration dry run, and rollout metrics.
6. Assumptions list and items marked for verification against current official documentation.
7. Release notes draft, breaking changes first.

Do not produce: unverified tool commands, invented metrics, or a plan that deploys unbuilt or untested artifacts.


## quality-assurance

**Use when:** Use when planning, executing, or reviewing quality assurance for authentication and security controls, including login, session, MFA, password reset, token handling, authorization checks, and security regression testing.

### Purpose and boundaries

This skill defines how to test authentication and security-relevant functionality so that defects are found, reproduced, classified, and verified with evidence. It covers test design, execution, triage, and sign-off for:

- Credential login, lockout, and rate limiting
- Multi-factor enrollment, challenge, and recovery
- Password reset, account recovery, and email or phone verification
- Session creation, expiry, rotation, and logout invalidation
- Token issuance, validation, audience, expiry, and revocation
- Authorization boundaries (object-level and function-level access)
- Security headers, cookie attributes, and transport settings as observed by a tester

It does not cover writing production code, performing penetration tests against systems without written authorization, or certifying compliance. Compliance statements require the owning compliance function.

### Inputs and assumptions

Before testing, confirm:

1. A written scope naming environments, hostnames, accounts, and permitted test types.
2. Test accounts with defined roles, created for testing only. Do not use real customer or employee credentials.
3. Requirements or acceptance criteria. If none exist, record assumed behavior and mark it as assumed.
4. The version or build under test, and the current official documentation for any protocol, library, or identity provider involved. Version-sensitive behavior must be checked against that documentation; do not rely on memory.

If any input is missing, stop and request it.

### Operating workflow

1. **Map the surface.** List every entry point for the feature: UI flows, API endpoints, redirects, callbacks, and admin paths. Record each as a row in a test matrix.
2. **Derive cases from threats and requirements.** For each row, write cases for the expected path, each documented failure path, and at least these abuse cases: credential stuffing response, replayed tokens or codes, expired session reuse, parameter tampering, missing-authorization access, and user enumeration through response differences or timing.
3. **Assign priority.** Rate each case by impact and likelihood: P1 for authentication bypass, account takeover, or privilege escalation; P2 for information disclosure or weakened controls; P3 for hardening gaps.
4. **Execute in a controlled order.** Run positive baseline tests first, then negative tests, then abuse tests. Record environment, build, account, timestamp, and request or screen evidence for each result.
5. **Reproduce before reporting.** Every failure must reproduce at least twice from a clean state.
6. **Triage and report.** Classify each defect, attach evidence, and state the expected and observed behavior.
7. **Verify fixes.** Retest the original case plus adjacent cases in the same control family.

### Decision gates

- **Gate A (scope):** Proceed only if scope is written and covers the target. Otherwise halt.
- **Gate B (data):** Proceed only with test accounts. If production data appears in responses, stop, record the exposure, and escalate.
- **Gate C (destructive or external actions):** Requires explicit named approval before: account lockout of shared accounts, mass login attempts beyond the agreed rate limit, testing against third-party identity providers, sending real emails or SMS to non-test recipients, deleting or modifying user records, rotating shared secrets or signing keys, or any action that could affect other users or external parties.
- **Gate D (severity escalation):** Any confirmed authentication bypass, exposed credential, or cross-account data access is escalated immediately to the named security owner, before the full report is complete.
- **Gate E (sign-off):** Release is recommended only when all P1 cases pass, no open P2 defects lack an accepted risk record, and retests are complete.

### Verification and evidence

Each result must include:

- Case ID, priority, environment, build, account role
- Exact steps and inputs (credentials redacted to role labels)
- Expected result with source reference
- Observed result with timestamped evidence (status code, response shape, screen capture with secrets masked)
- Pass, fail, blocked, or not-applicable with reason

Quality measures for the test cycle:

- 100% of P1 cases executed and passed or formally waived.
- Every failure reproduced twice.
- Every defect has a severity, a single root-cause hypothesis, and a retest result.
- Test matrix covers 100% of listed entry points; uncovered entry points are reported as gaps.

### Failure handling

- **Environment instability:** Record it, pause, and do not count results from unstable runs.
- **Account lockout during testing:** Stop, record, and request unlock through the approved process (Gate C).
- **Unexpected production impact:** Stop immediately, notify the owner, and document the timeline.
- **Ambiguous requirement:** Mark the case blocked and request a decision. Do not invent expected behavior.
- **Tool or library behavior differs from documentation:** Record the discrepancy with the version, and verify against current official documentation before filing.

### Deliverable contract

Deliver a single report containing:

1. Scope, environments, builds, and test accounts (by role)
2. Test matrix with case IDs, priorities, and results
3. Defect list ordered by severity, each with reproduction steps and evidence
4. Coverage gaps and assumptions
5. Gate decisions taken and approvals obtained, with dates
6. Release recommendation: approve, approve with accepted risks (named owner), or reject

Do not include in the report: raw passwords, tokens, session identifiers, private keys, or real personal data. Mask all secrets as role labels or truncated hashes.

### What not to do

- Do not test beyond the written scope or against unauthorized systems.
- Do not declare a control "secure" or "compliant"; report only what was tested.
- Do not state tool flags, API names, or library versions from memory; verify them against current official documentation.
- Do not run credential guessing against real accounts.
- Do not mark a P1 case as passed without retest evidence.

### Ultron routing contract

**Choose this skill when:** the task is to design or execute planned functional and security-focused verification of authentication and authorization behavior: login, MFA, recovery, sessions, tokens, rate limits, lockout, and access-control boundaries. It owns test coverage, reproducible cases, expected outcomes, and release/sign-off evidence.

**Choose `reliability-and-debugging` when:** a specific authentication or authorization defect is already observed and the main task is reproducing it, tracing the root cause, repairing the implementation, and proving the security properties remain intact.

**Handoff contract:** QA supplies a failing case with setup, exact steps, expected/actual result, affected identity state, and severity. Debugging returns the root cause, minimal fix, regression test, and evidence that no security control was weakened. QA then reruns the relevant suite and records the disposition.

**Why the boundary exists:** testing establishes whether behavior is correct; debugging explains and repairs why it is not. A passing test after a security downgrade is never an acceptable result.


## reliability-and-debugging

**Use when:** Use when diagnosing intermittent or failing authentication, authorization, session, token, MFA, or SSO behavior in production or staging, or when fixing reliability in auth components without weakening security controls.

### Purpose and boundaries

Locate, reproduce, and fix faults in authentication and authorization paths: login, MFA, token issuance and validation, session lifecycle, federation, password reset, account recovery, rate limiting, and lockout. Preserve every security property while restoring correct behavior.

Out of scope: designing new cryptographic primitives, bypassing controls to make a flow pass, and testing systems without owner authorization.

A fix that restores availability by weakening verification is a failed fix. Examples: disabling signature checks, widening accepted issuers or audiences, extending token lifetimes without justification, or removing lockout.

### Inputs and assumptions

Required before work begins:
- Symptom statement: affected population, error text or code, first-seen time, failure rate, environment.
- Component map: identity provider, gateway, application, session store, key source, time sources.
- Recent changes: deployments, configuration, certificate or key rotations, dependency upgrades, IdP tenant changes.
- Access: read-only logs and metrics by default.

Assumptions to state explicitly: clocks are NTP-synchronized unless shown otherwise; logs use UTC; user-facing errors are generic while internal logs are detailed.

### Operating workflow

1. Write one falsifiable sentence: "For [population], [operation] fails with [observable] since [time]." Refuse vague reports until narrowed.
2. Establish a baseline of success and failure rates by client, region, IdP, and build.
3. Trace one failing request end to end using correlation identifiers. Record each hop's decision and timestamp.
4. Classify the fault (see Decision gates) and form one hypothesis.
5. Reproduce in staging or a local harness using synthetic accounts only.
6. Test the hypothesis by changing one variable at a time. Log every change.
7. Apply the smallest fix that restores correct behavior, not merely a passing request.
8. Verify, deploy through a canary or flag where available, and compare against the baseline.

High-yield checks:
- "Not yet valid" or "expired" errors: compare issuer and verifier clocks, and confirm the configured skew tolerance and its unit.
- Intermittent 401s across replicas: signing key sets differ between instances, or a key cache did not refresh after rotation.
- Redirect loops: cookie attributes (domain, path, Secure, SameSite) or redirect URI mismatch after a host or proxy change. Check forwarded headers.
- SSO failing for some tenants: metadata or claim mapping differences. Compare claim names and structure, never claim values.
- Lockout spikes: a retry storm from one client, or shared NAT addresses hitting per-IP limits.

### Decision gates

- Gate 1, security-relevant? Any change to validation, key handling, token lifetime, redirect rules, or rate limits requires security review and explicit approval before deployment.
- Gate 2, reversible? Code and configuration rollbacks need a tested rollback path. Key deletion, mass session revocation, bulk lockout resets, schema migrations, and IdP setting changes require explicit approval with a stated blast radius.
- Gate 3, externally visible? Changes affecting relying parties, tenant settings, or customer notifications require approval from the system owner.
- Gate 4, evidence sufficient? If the hypothesis is not reproduced after two focused attempts, stop and collect targeted telemetry instead of guessing.

### Verification and evidence

Acceptance requires all of the following:
- The reproduced failure now succeeds, and at least one control case per affected client type succeeds.
- Negative cases still fail: expired token, wrong audience, wrong issuer, bad signature, replayed authorization code, locked account.
- Failure rate returns to baseline within the agreed window (for example, 30 minutes on canary) with no new error classes.
- Logs contain no tokens, passwords, secrets, raw assertions, or full personal identifiers.
- Any product- or library-specific setting cited in the fix is verified against current official documentation for the deployed version before it is relied on.

### Failure handling

- If the fix increases security-relevant signals (accepted invalid tokens, successful logins from unexpected sources), roll back immediately and open a security incident.
- If rollback is unavailable, disable only the changed component and notify the owner.
- Do not repeatedly trigger production authentication flows to reproduce a bug. Use labeled test accounts with rate limits.
- If root cause is unknown after the evidence gate, report the narrowed scope and open an investigation item rather than shipping a speculative change.

### Deliverable contract

Produce:
1. Defect summary: symptom, population, time window, root cause, confidence level.
2. Evidence: correlation identifiers, timestamps, redacted log excerpts.
3. Change record: code or configuration diff reference, rollback procedure, named approvers.
4. Verification results mapped to the acceptance checklist.
5. Residual risk and follow-up items, each with an owner.

What not to do:
- Do not disable signature, audience, issuer, expiry, or lockout checks as a diagnostic step in production.
- Do not paste secrets, tokens, or raw assertions into tickets, chat, or commits.
- Do not claim a compliance outcome from a debugging fix.
- Do not invent flag names, parameters, or version behavior. Verify them first.

### Ultron routing contract

**Choose this skill when:** an authentication or authorization path is failing, flaky, slow, or inconsistent and the task requires reproduction, trace analysis, root-cause isolation, a minimal repair, and regression proof.

**Choose `quality-assurance` when:** the task is to define or run a systematic test plan for authentication/security behavior, establish coverage, or produce formal verification and sign-off evidence rather than diagnose one known defect.

**Handoff contract:** accept a reproducible case or observed symptom. Return the causal chain, affected state transitions, smallest safe fix, regression test, and explicit evidence that signatures, issuers, audiences, expiry, MFA, lockout, and authorization checks remain enforced as applicable. Send the repaired case back to QA for broader suite validation.

**Why the boundary exists:** incident diagnosis and test assurance are complementary. Do not make the debugger invent broad release coverage or ask QA to guess at root cause.


## sre-observability-and-incidents

**Use when:** Use when designing or reviewing observability (metrics, logs, traces, alerts, SLOs, dashboards) or when triaging, coordinating, mitigating, or writing up production incidents for cloud-hosted services.

### Purpose and boundaries

This skill covers two linked activities: making production services observable enough to detect and diagnose problems, and running incidents from detection through post-incident review. It produces alert rules, SLO definitions, triage notes, incident timelines, mitigation plans, and postmortems.

In scope: service-level indicators and objectives, alert design, dashboard structure, telemetry gap analysis, incident triage, communication cadence, mitigation selection, and blameless review.

Out of scope: writing application features, general security incident forensics (hand off to the security team), capacity procurement, and legal or regulatory breach determinations.

### Inputs and assumptions

Before acting, confirm:

- Service name, owner, tier, and user-facing journeys it supports.
- Current telemetry sources (metrics backend, log store, tracing system) and their retention. Do not assume names; ask or inspect configuration.
- Existing SLOs, alert rules, and runbooks, with their last review date.
- For incidents: start time (or best estimate), severity, customer impact signals, recent changes (deploys, config, flags, dependencies, traffic events).
- Access constraints. Assume read-only access unless the incident commander explicitly grants change access.

If telemetry is absent for a critical path, state that as a finding rather than inferring health.

### Operating workflow

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

### Decision gates

- **Paging versus ticketing:** Page only if a user-facing SLO is burning at a rate that exhausts budget within hours, or if a safety-critical function is down. Otherwise create a ticket.
- **Rollback versus forward-fix:** Roll back when the change is the most likely cause and rollback is tested and low-risk. Forward-fix only when rollback would cause data loss, schema incompatibility, or is unavailable.
- **Mitigation requiring approval:** Obtain explicit approval from the incident commander and service owner before any of the following: deleting or truncating data, altering production databases, modifying IAM or network policy, disabling security controls, failing over cross-region, changing customer-facing communications, or sending external status page updates. Record the approver and time.
- **External communication:** Draft status updates; do not publish them without approval from the communications owner. Do not state root cause externally until confirmed.
- **Closing an incident:** Close only when the SLI is back within target for the observation window and no mitigation remains temporary without a tracking ticket.

### Verification and evidence

- Every alert change includes a test: replay historical data or use a synthetic signal to show it would have fired at the intended time and not during a known-good window.
- Every root-cause claim cites at least one primary signal (metric graph, log query result, trace) with the query or link preserved.
- Dashboards show the SLI, the SLO line, error budget remaining, and change markers.
- Quality checks for observability work: alert-to-runbook coverage at 100% for pages; zero pages without a named owner; trace sampling rates and log retention documented; no alert based solely on CPU without a user-impact companion.
- Quality checks for incidents: timeline gaps under 15 minutes during active response; stakeholder updates on cadence; time-to-mitigate and time-to-detect recorded from timeline timestamps, not memory.
- Metric backends, query languages, and alert syntax differ by vendor and version. Verify any query or rule syntax against current official documentation before deploying.

### Failure handling

- **Missing telemetry:** State the gap, use the nearest proxy (for example load balancer status codes), and add instrumentation as a follow-up action.
- **Conflicting signals:** Prefer user-facing SLIs over internal resource metrics. Note the conflict in the timeline.
- **Hypothesis stalls for 30 minutes:** Escalate to a second responder or pivot to mitigation.
- **Mitigation makes things worse:** Revert the mitigation immediately, record it, and re-assess.
- **Scope uncertainty:** Assume broader impact until narrowed by evidence.

### Deliverable contract

Return one of the following, depending on request:

- **Alert or SLO package:** SLI definitions with query logic described in plain language, SLO targets with rationale, burn-rate alert specifications, runbook links, test evidence, and a list of items marked for version verification.
- **Incident record:** Severity, impact summary, role assignments, timestamped timeline, hypotheses tested with outcomes, mitigation actions with approvers, recovery verification, and open follow-ups with owners and due dates.
- **Postmortem:** Summary, customer impact, detection and response analysis, contributing factors (systemic, not individual), what went well, action items with owners and priority, and a statement of confidence in the root cause.

Do not include fabricated metrics, unverified tool behavior, or compliance claims. Mark every unverified item explicitly.

### Ultron routing contract

**Choose this skill when:** designing or operating production observability and incident response across services: SLIs/SLOs, alerting, dashboards, incident triage, mitigation, communication, and postmortems.

**Choose api-observability-reliability when:** the work is limited to a specific API dependency or external registry integration and needs endpoint-level retries, rate-limit behavior, timeout policy, or upstream health measurement.

**Handoff contract:** receive API-level error/latency/availability evidence and dependency behavior. Incorporate it into service SLOs and incident timelines without confusing upstream failure with local service failure. Return explicit alert thresholds, escalation owner, and incident actions to the API integration owner.

**Why the boundary exists:** API dependency health is one input to service reliability; it is not a replacement for system-level SLOs and incident management.


## tdd-and-coverage-authoring

**Use when:** Use when writing or revising tests test-first (red-green-refactor), designing unit or integration test suites, or interpreting and improving code coverage metrics in a software project.

### Purpose and boundaries

This skill guides an agent through test-driven development (TDD) and the authoring of meaningful coverage. It covers: writing failing tests before implementation, choosing test granularity, structuring test suites, reading coverage reports, and closing gaps that matter.

It does not cover: load or performance testing, security penetration testing, UI visual regression infrastructure, CI pipeline provisioning, or changing production behavior beyond what a failing test demands. If a request is primarily one of these, state that and hand off.

### Inputs and assumptions

Before acting, establish:

1. The language, test framework, and assertion library in use. Read the existing test configuration and one or two existing tests to match conventions. Do not introduce a new framework without approval.
2. The behavior under change: a bug report, a feature specification, or a refactoring goal. Write the expected behavior in one sentence before touching code.
3. The current coverage baseline, if any, produced by the project's own tooling. If none exists, say so and do not invent a number.
4. Whether the target code has external dependencies (network, database, clock, filesystem, queues). Identify them; they determine test doubles.

Assume the repository is under version control and tests can be run locally. If they cannot, stop and report.

### Operating workflow

1. **Locate the seam.** Find the smallest public interface that exhibits the behavior. Prefer testing through public functions or endpoints over private helpers.
2. **Write one failing test.** Name it after the behavior ("returns 0 when cart is empty"), not the method. Use Arrange-Act-Assert. Run only that test and confirm it fails for the expected reason (an assertion mismatch, not a syntax or import error). A test that passes before implementation proves nothing unless it guards existing behavior, in which case label it as a characterization test.
3. **Implement the minimum.** Write only enough production code to pass the failing test. Resist adding untested branches.
4. **Run the full affected suite.** Confirm green and no regressions.
5. **Refactor under green.** Remove duplication, rename, extract. Re-run tests after each change.
6. **Repeat** for the next behavior. Keep each cycle small enough to finish in minutes.
7. **Edge cases in a batch.** After the happy path, enumerate boundaries (empty, zero, maximum, null, duplicate, concurrent, timezone or locale edges) and add one failing test per case through steps 2 to 5.
8. **Coverage pass.** Only after behavior tests exist, generate the coverage report with the project's configured command. Inspect uncovered lines in changed files first.

### Decision gates

- **Mock or real?** Use real in-memory implementations for pure logic and collaborators with no I/O. Use test doubles for network, clock, randomness, and paid or rate-limited services. Use real databases only in integration tests with a disposable instance. Never point tests at shared or production data stores.
- **Unit or integration?** A test that needs more than one process or external service is integration. Keep the count of integration tests low and mark them so they can be run separately.
- **Coverage gap: write a test or exclude?** Write a test if the line encodes business logic, validation, or error handling. Exclude only generated code, trivial re-exports, or framework boilerplate, and record the exclusion rule in the project's configuration with a comment.
- **Test change or code change?** If a previously passing test now fails, determine whether the requirement changed. If it did, update the test and state the requirement change. If it did not, the code change is a regression; fix the code.
- **Snapshot tests?** Use only for stable serialized output. Never accept a snapshot update without reviewing the diff.

### Verification and evidence

Report the following, with actual command output:

- Test counts before and after: total, passing, failing, skipped. Skipped tests require a stated reason.
- The red run: the failing assertion text for each new test.
- The green run: full suite result.
- Coverage: line and branch percentages for changed files, compared to baseline. Report the tool and configuration used.
- Mutation or fault check, if the project has a mutation tool: report surviving mutants in changed code. If no such tool exists, state that the check was not performed.

Quality checks:
- Every new test fails before the fix and passes after.
- No test asserts only that a function was called unless the call itself is the requirement.
- No test depends on execution order, wall-clock time, or random seeds without pinning them.
- Changed files reach the project's configured threshold, or the shortfall is explained.

Do not claim a coverage percentage, speed improvement, or defect-reduction figure that was not measured in this session.

### Failure handling

- **Test fails for an unexpected reason** (import error, fixture missing): fix the harness first; this is not a valid red state.
- **Cannot make a test fail first:** the behavior may already exist. Verify, then label the test as characterization.
- **Flaky test:** rerun to confirm. Do not add retries or sleeps as a fix. Identify the nondeterministic input and inject control.
- **Coverage tool produces inconsistent numbers:** verify the configuration path and the tool version against current official documentation before trusting figures.
- **Existing suite is too slow to run per cycle:** run the affected test file only during red-green, and run the full suite before reporting. Report the timing.

### Deliverable contract

Provide:

1. A list of behaviors added or changed, each with its test file and test name.
2. Red and green evidence as described above.
3. Coverage summary for changed files with the exact command used.
4. Open gaps: untested edge cases, excluded lines with justification, and any skipped tests.
5. Any change requiring approval, such as new dependencies, configuration changes to coverage thresholds, or deletion of existing tests, listed as pending and not applied.

Do not delete or weaken existing assertions to make the suite pass. Do not lower coverage thresholds, add exclusions, or install packages without explicit approval. Do not run tests against production systems or shared data stores. Mark any version-specific flag or tool behavior as requiring verification against current official documentation.


## test-repair-and-plan-execution

**Use when:** Use when a test suite has failing, flaky, or broken tests and a written repair plan or migration plan must be executed step by step, verified, and reported without weakening coverage or hiding real defects.

### Purpose and boundaries

This skill covers executing a defined plan to repair failing or broken tests: fixing test code, test fixtures, environment wiring, and test-data assumptions, then proving the suite is healthy again. It also covers executing a multi-step plan (for example, a framework upgrade or test-layer migration) where each step must be checked before the next begins.

In scope: diagnosing failure causes, classifying them, applying the smallest correct fix, re-running affected tests, and recording evidence.

Out of scope: inventing new product requirements, changing production behavior to make tests pass without a confirmed defect, deleting coverage to reduce failure counts, and rewriting the test strategy unless the plan explicitly asks for it.

### Inputs and assumptions

Before acting, confirm:
- The failing test list or the plan document, with its ordered steps and acceptance criteria.
- The exact command used to run tests, the runner version, and the CI configuration, read from the repository rather than assumed.
- Whether the goal is "suite green" or "plan step N complete." These differ and must be stated.
- Baseline results: the last known passing commit, if any, and current failure output.

If version-sensitive APIs, runner options, or library behaviors are involved, verify them against current official documentation for the pinned version. Do not rely on memory for flag names or deprecation status.

### Operating workflow

1. **Reproduce.** Run the failing tests in isolation and then as part of the full suite. Record the command, exit code, and the first failure message. A failure that does not reproduce is classified as flaky, not fixed.
2. **Classify each failure** into one of: test defect (wrong assertion, stale expectation, bad fixture), environment defect (missing service, port collision, timezone, locale), dependency drift (changed library behavior), data defect (order-dependent state, shared database rows), or product defect (correct test exposing a real bug).
3. **Group failures** by root cause. Ten failures from one missing fixture is one repair.
4. **Apply the smallest fix** per group. Prefer correcting setup and isolation over loosening assertions. If an assertion must change, state the old and new expected behavior and why the old one was wrong.
5. **Execute plan steps in order.** Complete one step, run its verification, record evidence, then start the next. Do not batch steps whose verification would be ambiguous together.
6. **Re-run** the isolated tests, then the full suite, then any gating CI stage.
7. **Repeat the full suite** at least three times for any test that was flaky, to check stability.

### Decision gates

Stop and request explicit approval before:
- Deleting, skipping (`skip`, `xfail`, disabled marks), or quarantining any test. Skipping requires an owner and a tracking reference.
- Changing production code. A test that exposes a product defect is reported, not silently "fixed" in test code.
- Modifying shared fixtures, seed data, or databases used by other suites.
- Running commands against shared, staging, or production systems, or anything that sends external messages, charges, or writes to third-party services.
- Deleting snapshot files, golden files, or recorded fixtures. Regenerating them is allowed only after reviewing the diff.
- Any action that is irreversible or affects data outside the repository.

Proceed without asking for: editing test files in the working branch, local test runs, adding diagnostic logging in test code, and reverting your own uncommitted changes.

### Verification and evidence

Each repair must have:
- A failing-before and passing-after run of the same command.
- For flaky tests, at least three consecutive passing runs, with the seed or ordering recorded if randomized.
- A diff confined to the planned scope. Flag any change outside it.
- Coverage that does not decrease for the touched modules. Measure with the project's existing tool and report the number before and after.

Quality checks, all measurable:
- Zero newly skipped or deleted tests unless approved.
- Failure count strictly decreasing across steps, or an explained increase.
- Every assertion change has a written rationale.
- No test sleeps longer than a fixed wait introduced to hide a race; race conditions are fixed with explicit synchronization.

Do not claim performance numbers, pass rates across environments, or compliance status unless measured and shown.

### Failure handling

- If a fix makes a different test fail, revert it and reclassify the group.
- If reproduction fails inconsistently, capture logs, seed, and timing for three runs before changing code.
- If a plan step is blocked by a missing dependency or unclear acceptance criterion, stop at that step, state the blocker, and list the specific information needed.
- If the root cause is a product defect, produce a minimal reproduction and escalate instead of patching around it.

### Deliverable contract

Produce a report containing:
1. Summary: starting failure count, ending failure count, and the goal stated in Inputs.
2. Table of root-cause groups: cause, affected tests, fix applied, files changed.
3. Plan step status: each step marked complete, blocked, or deferred, with its verification evidence.
4. Assertion or expectation changes with rationale.
5. Open items requiring approval, with the specific decision needed.
6. Exact commands run and their results.

Do not state the suite is healthy unless the final full-suite run in the recorded environment passed.


## unit-and-component-testing

**Use when:** Use when writing, reviewing, or repairing unit tests or component tests for application code, including test design, isolation of dependencies, fixture strategy, coverage interpretation, and flaky-test diagnosis.

### Purpose and boundaries

This skill guides the design and maintenance of tests that verify a single unit (a function, class, or module) or a single component (a module or service boundary with its real internal collaborators but external systems replaced). It covers test structure, dependency substitution, assertion quality, and test-suite health.

Out of scope: end-to-end browser flows, load and performance testing, security penetration testing, and contract verification across independently deployed services. Redirect those to their own practices.

### Inputs and assumptions

Before writing tests, establish:

1. The unit or component under test, its public interface, and its documented behavior. If behavior is undocumented, derive it from the code and state the derived contract explicitly.
2. The language, test framework, and mocking library in use. Do not assume APIs; check the project's lockfile and existing test files. Mark any framework-specific syntax you are unsure of for verification against the current official documentation.
3. Existing test conventions: file location, naming, fixture style, and how the suite is run in CI.
4. External boundaries: databases, network calls, clocks, filesystem, randomness, message queues. Each must be classified as substitute, fake, or real (see Decision gates).

If the target cannot be run locally, stop and report that the suite cannot be verified.

### Operating workflow

1. **Map behaviors.** List observable behaviors as statements: "given X, when Y, then Z." Include error paths, boundary values, and invalid inputs. Aim for one behavior per test.
2. **Classify dependencies.** For each collaborator, choose a strategy from the decision gates.
3. **Write the failing test first when fixing a defect.** Confirm it fails for the stated reason before changing production code.
4. **Structure each test in arrange, act, assert.** Keep one act per test. Name tests after the behavior, not the method: `rejects negative quantity with ValidationError` rather than `test_add_item_2`.
5. **Build minimal fixtures.** Construct only the state the behavior needs. Prefer inline builders with overridable defaults over large shared fixtures.
6. **Assert on outcomes.** Check return values, persisted state through a fake, emitted events, or raised errors. Avoid asserting on the exact sequence of internal calls unless the call itself is the contract.
7. **Run the suite in isolation and in random or reversed order** if the runner supports it, to expose hidden shared state.
8. **Measure.** Run coverage for the changed files and review uncovered branches.

### Decision gates

- **Real versus substitute:** Use the real implementation for pure logic and in-process value objects. Use a fake (in-memory repository, deterministic clock) for stateful collaborators where behavior matters. Use a mock or stub only to verify an interaction that is itself the contract, such as "payment gateway is charged exactly once."
- **Mock count:** If a test needs more than three substitutes, the unit likely has too many responsibilities. Report this as a design finding rather than adding more mocks.
- **Time, randomness, and identifiers:** Inject them. Never rely on wall-clock time or unseeded randomness in assertions.
- **Coverage target:** Require branch coverage on changed lines, not a global percentage. Do not raise thresholds as part of a test change unless the owner asks.
- **Integration boundary:** If a behavior depends on real database semantics (transactions, constraint behavior, query planning), it belongs in an integration test, not a unit test. Do not simulate those semantics with a fake and claim verification.
- **Destructive or external actions:** Running tests that write to shared databases, call paid or production APIs, send messages, or delete files requires explicit user approval. Default to local, in-memory, or sandboxed resources.

### Verification and evidence

Report the following for every change:

- The exact test command run and its exit status.
- Count of tests added, modified, and removed, with the reason for each removal.
- Evidence that a new regression test failed before the fix and passed after.
- Branch coverage for changed files, stated as a measured number from the tool output.
- Results of at least one re-run to detect flakiness. Any test that fails intermittently is treated as a defect, not retried into passing.

Quality checks:

- No test sleeps for a fixed duration to wait for asynchronous work; use explicit completion signals.
- No test depends on execution order or on another test's side effects.
- Assertions name specific expected values; no bare truthiness checks on complex objects.
- Test runtime for the unit suite is recorded; flag any individual test over one second for review.

### Failure handling

- **Test fails after a behavior change:** Determine whether the old behavior was the contract. If the contract changed intentionally, update the test and state the change. If not, fix the code.
- **Flaky test:** Capture the seed, timing, and ordering. Remove the nondeterminism source (usually time, shared state, or real I/O). Do not add retries or increase timeouts as the fix.
- **Cannot isolate a dependency:** Stop and report the coupling. Propose a seam, such as extracting an interface, but do not restructure production code without approval.
- **Framework API uncertainty:** Mark the call as unverified, check the current official documentation for the pinned version, and note the verification in the deliverable.

### What not to do

- Do not write tests that merely execute code without asserting behavior.
- Do not snapshot large objects as the primary assertion.
- Do not delete or skip failing tests to achieve a green run.
- Do not mock the unit under test or its own private helpers.
- Do not invent framework functions, flags, or version compatibility claims.
- Do not claim coverage or correctness beyond what the executed tools reported.

### Deliverable contract

Return:

1. The changed or new test files, complete and runnable.
2. A short summary table: behavior tested, substitution strategy, and result.
3. The verification evidence listed above.
4. A list of open findings: design issues, unverified API usage, and coverage gaps, each with a recommended next step.

### Ultron routing contract

**Choose this skill when:** testing a bounded unit or component in isolation, including functions, classes, modules, and components with their internal collaborators while external services are replaced by controlled fakes or mocks.

**Choose `e2e-test-engineering` when:** the requirement depends on real process, network, storage, browser, identity, or multi-service behavior and must be proven as an end-to-end journey.

**Handoff contract:** return deterministic local tests with clear assertions, fixtures, boundary coverage, and fast failure diagnostics. Escalate only the behaviors that depend on real system composition to E2E tests; do not copy every unit case into a slow browser journey.

**Why the boundary exists:** isolated tests make local reasoning cheap and precise; end-to-end tests validate integration and user-visible outcomes. A healthy test strategy needs both layers.


## workflow-planning-verification

**Use when:** Use when planning or reviewing an automated multi-step agent workflow before execution, to check step ordering, tool permissions, failure paths, approval gates, and success criteria so the workflow can be run safely and its results verified.

### Purpose and boundaries

This skill verifies a workflow plan before any agent or automation runs it. It covers multi-step plans that call tools, APIs, databases, file systems, messaging systems, or other agents. Typical inputs are a plan draft, a runbook, a pipeline definition, or a natural-language task description that will be converted into steps.

In scope: step decomposition, dependency ordering, input and output contracts, tool permission scoping, decision gates, rollback and retry logic, and evidence required to declare each step complete.

Out of scope: writing the production code of the tools themselves, choosing vendors, legal or compliance certification, and performance benchmarking. Do not claim that a plan is compliant with any regulation or standard. Report only what was checked.

### Inputs and assumptions

Before verifying, collect:

1. The goal in one sentence, and who or what consumes the result.
2. The full step list, including any branches, loops, and parallel steps.
3. For each step: the tool or API, the operation type (read, write, delete, send, execute, spend), the input source, and the expected output shape.
4. Available credentials and their scopes, described by role rather than secret value.
5. Data sensitivity classes present (for example personal data, financial records, credentials, unreleased source code).
6. Environment: sandbox, staging, or production.

If any item is missing, record it as an open assumption. Do not fill gaps with guesses about system behavior. Mark any statement about a specific tool's parameters, limits, or behavior as "verify against current official documentation" unless the user has supplied the documentation text.

### Operating workflow

1. **Restate the goal.** Write the goal and the observable success condition. If the success condition cannot be observed, the plan is not verifiable; flag it.
2. **Build the step graph.** Number every step. Mark dependencies explicitly ("needs output of step 3"). Identify steps with no dependency that could run in parallel, and confirm parallelism does not share writable resources.
3. **Classify each step** by operation type and reversibility: read-only, reversible write, irreversible write, external send, or spend/commit.
4. **Check the contracts.** For each edge between steps, confirm the producer's output fields match the consumer's required inputs in name, type, and units. Example failure: step 2 outputs `amount_cents`, step 4 expects `amount` in dollars.
5. **Check permissions.** Each step should use the narrowest credential that works. Flag any step that has write access where only read is needed, or a single shared admin token used across unrelated steps.
6. **Check failure paths** (see Failure handling below).
7. **Apply decision gates** to every step classified as irreversible or external.
8. **Define evidence** for each step (see Verification and evidence).
9. **Produce the deliverable** in the required format.

### Decision gates

Stop and request explicit human approval before executing any step that:

- Deletes, overwrites, or migrates data, or changes schemas or permissions.
- Sends messages, emails, notifications, or publishes content to people or external systems.
- Moves money, places orders, or creates commitments with a cost.
- Touches production systems or customer-facing configuration.
- Handles personal, financial, health, or credential data beyond what the stated goal requires.
- Uses a credential broader than the step needs.

Approval must name the specific step, the action, the target, and the reversal path. A general "go ahead" for the whole workflow does not cover later irreversible steps. Re-request approval if the plan changes after approval.

Proceed without a gate only for read-only steps and reversible writes in a sandbox or staging environment, and only when the rollback is written down.

### Verification and evidence

For each step, define:

- **Pass condition**: a checkable statement, such as "row count in target table equals source row count," "HTTP response status is 200 and returned ID is stored," or "file hash matches manifest."
- **Evidence artifact**: the log entry, diff, query result, or screenshot that proves the condition, and where it is stored.
- **Timeout and retry budget**: maximum attempts and total elapsed time. Retries must be idempotent or guarded by an idempotency key; otherwise a retry can duplicate a write.

Whole-workflow checks:

- Every step has a pass condition. Count them; a step without one is a defect.
- Every irreversible step has a pre-action snapshot or confirmation read.
- The final output is compared against the stated goal's success condition, not merely against "all steps succeeded."
- Spot-check at least one output by an independent method (for example recomputing a total from raw records).

### Failure handling

Classify each failure as transient (network timeout, rate limit), input (malformed or missing data), permission (denied scope), or logic (the plan assumed something false). Then:

- Transient: retry within budget with backoff; then escalate.
- Input: halt dependent steps; report the offending record; do not silently skip records.
- Permission: halt; do not attempt to escalate privileges or find alternative credentials.
- Logic: halt the workflow and return to planning. Do not improvise new steps during execution.
- Partial completion: record which steps committed, and provide the compensating action for each, or state that none exists.

Never continue past a failed irreversible step to "finish the job."

### Deliverable contract

Return a verification report with these sections, in order:

1. **Verdict**: approved to run, approved with conditions, or blocked. One line.
2. **Blocking defects**: numbered, each with step number, the defect, and the fix.
3. **Step table**: step number, operation type, reversibility, credential scope, pass condition, evidence artifact, approval required (yes or no).
4. **Open assumptions**: each marked for verification against current documentation where relevant.
5. **Approval requests**: one entry per gated step, with the exact action and reversal path.
6. **Residual risk**: what the check did not cover.

Do not state that the workflow is secure, compliant, or guaranteed to succeed. Report what was checked and what remains unverified.
### Executable workflow contract and recovery design (v1.1)

Represent the approved workflow as a machine-checkable contract rather than a prose-only checklist. Each step has a stable ID, owner, dependency IDs, typed inputs and outputs, effect classification, target resource, authority scope, timeout, retry policy, idempotency strategy, approval requirement, pass condition, and evidence reference. Reject cycles, unresolved dependencies, ambiguous targets, and steps without observable completion conditions before execution.

Define the workflow's consistency model. Identify which steps are safe to run concurrently, which require serial execution, and which share mutable state. For each external side effect, record the idempotency key and the system-of-record field used for reconciliation. For multi-system work, define the saga order and compensating action for every completed step that may need reversal; explicitly mark effects that cannot be compensated.

Use a durable state machine with transitions such as READY, RUNNING, WAITING, RETRYABLE_FAILURE, BLOCKED, COMPENSATING, SUCCEEDED, PARTIAL, and CANCELLED. Persist the transition before dispatching the next external action. On resume, inspect both workflow state and downstream systems; a timeout is an unknown outcome until reconciled.

The final acceptance gate checks the user's postconditions independently of the step ledger. A sequence of successful API responses does not prove the intended outcome. Preserve partial completion and unresolved compensation in the final report.

### Ultron routing contract

**Choose this skill when:** turning a user goal into a bounded, executable plan with dependencies, preconditions, expected postconditions, decision gates, side-effect handling, and evidence-based completion checks.

**Choose `delegated-execution-queues` when:** plan steps must run asynchronously or durably across process restarts, with leases, retries, backpressure, cancellation, and dead-letter recovery.

**Choose `session-continuity-recall` when:** an interrupted plan must be resumed and reconciled with current external state before any step is repeated.

**Choose `agent-evaluation-design` when:** defining reusable tests to establish whether this planning/execution behavior is safe and reliable across many cases.

**Handoff contract:** produce a task contract with dependencies, permitted actions, stop conditions, idempotency expectations, verification source, and completion evidence. Queue or resume skills must preserve those semantics rather than treating each step as an unstructured job.

**Why the boundary exists:** planning defines what should happen and what counts as done; durable execution and session recovery preserve that plan across time.

### Workflow invariants, provenance, and safe joins (v1.3)

#### Declare invariants that must remain true

In addition to step-level pass conditions, define workflow-wide invariants: totals reconcile, each source record is handled exactly once or explicitly classified, no resource is mutated outside its owner scope, no external action occurs before approval, and no terminal state is reported while required work remains unresolved. State the invariant, authoritative evidence source, check frequency, and failure transition. If an invariant cannot be observed, mark it as an unresolved risk rather than asserting it.

#### Preserve provenance across step boundaries

Every material output should carry a provenance envelope: originating step ID, source record or artifact IDs, source timestamp/version, transformation identifier, and validation status. A downstream step should consume the declared artifact version, not an ambiguous mutable path such as “latest”. When data is transformed, preserve mapping back to source records and record dropped, rejected, or redacted items with reason codes. This makes reconciliation and selective replay possible.

#### Make parallel joins deterministic

For each fan-out, define the expected child set, completion condition, timeout behavior, and join policy before execution. Specify whether the join requires all children, a quorum, a threshold, or an explicit partial result. Reject duplicate child IDs and unexpected results. Do not let the first completed worker win unless the contract explicitly defines that policy and establishes that late results cannot change the committed outcome.

If workers can write shared state, assign a single writer or use versioned compare-and-set semantics. Parallel reads may be merged only with a documented conflict policy. When child results disagree, preserve each result and its provenance; do not average categorical or incompatible outputs.

#### Make compensation honest

For each compensation, define its preconditions, idempotency behavior, expected postcondition, and evidence. Distinguish a true reversal from a corrective follow-up: a sent email cannot be unsent, a payment reversal is a new transaction, and a published artifact may already have been copied. If the original effect is irreversible, the recovery plan must state residual impact, containment action, notification owner, and reconciliation evidence. Never report “rolled back” when only a compensating action was attempted.

#### Validate workflow-level invariants

Test empty input, partial input, duplicate source records, delayed and out-of-order child results, worker disagreement, a child that never completes, stale artifact versions, a failed compensation, and a process restart during a join. Verify the workflow either reaches a valid terminal state or remains explicitly blocked/partial with enough provenance to resume safely.


### Handoff contract validation and execution-boundary integrity (v1.4)

A handoff between skills, agents, queues, or workflow stages is a contract boundary, not a conversational suggestion. The sender must provide enough structured information for the receiver to continue the same task without inventing missing scope, evidence, authority, or completion state. The receiver must validate the handoff before acting.

#### Required handoff envelope

Every material handoff must carry:
- Stable task and parent-run identifiers, handoff ID, originating step, sender identity, intended receiver, and creation time.
- Goal, requested deliverable, explicit exclusions, current plan revision, and the exact next-step objective.
- Typed inputs and immutable artifact references, including content digests, source versions, timestamps, and provenance. Do not substitute mutable names such as latest for a pinned artifact.
- Preconditions, dependencies, completed steps, failed or skipped steps, pending work, and unresolved decisions.
- Resource targets, environment, data classifications, tenant scope, and allowed operation classes.
- Approval records with the exact action and target they authorize, approver identity, policy revision, expiry, and evidence reference. Never pass a vague statement such as approved without its bound action.
- Required postconditions, verification method, evidence location, retry/idempotency rules, stop conditions, and escalation owner.

#### Receiver acceptance protocol

Before execution, the receiver must:
1. Validate the envelope schema and required fields; reject malformed, ambiguous, or internally inconsistent values.
2. Authenticate the sender and verify that the receiver is the intended recipient for this task and tenant.
3. Re-read authoritative state for mutable facts, resource existence, current permissions, revocation status, and external side effects that may have occurred after the handoff was created.
4. Verify artifact digests and source versions; mark missing or changed artifacts stale and request a refreshed handoff.
5. Revalidate each approval against the proposed action, canonical arguments, target, environment, principal, policy revision, and expiry. Approval does not transfer the sender's identity or privileges.
6. Confirm that dependencies are complete and that the declared next step is still valid under the current workflow revision.
7. Accept with a recorded receiver, accepted envelope digest, timestamp, and execution owner, or reject with specific reason codes and required corrections.

No side effect may occur before acceptance. A handoff can be accepted for analysis while remaining blocked for execution if authority or evidence is incomplete.

#### Prevent duplicate, stale, and split-brain execution

Use a unique handoff ID and idempotency key bound to task, sender, receiver, contract revision, and payload digest. Repeated delivery of the same accepted handoff must return the existing disposition rather than create a second execution. A changed payload requires a new handoff revision and fresh validation.

Transfer execution ownership atomically. The sender must stop dispatching the transferred step after the receiver accepts it; use a monotonic ownership or fencing revision so a delayed sender cannot later commit a competing result. If ownership transfer cannot be confirmed, do not run both sides concurrently.

Treat timeout, lost acknowledgement, and process restart as unknown delivery outcomes. Query the handoff ledger and downstream system of record before resending or repeating an external operation. Preserve the original idempotency identity when reconciling the same logical operation; create a new identity only for a genuinely new action.

#### Revalidate on change

Re-run acceptance when the payload, task scope, resource target, tenant, skill version, dependency digest, policy revision, approval, environment, or next-step operation changes. A previously accepted envelope does not authorize a materially changed action. If new evidence contradicts the handoff, suspend the affected branch, preserve both records, and reconcile against the authoritative source.

#### Handoff acceptance tests

- Missing or malformed required fields are rejected with actionable diagnostics.
- A valid approval for one target cannot authorize a changed target or argument set.
- A stale artifact digest or revoked skill blocks execution.
- Duplicate delivery creates one logical execution and one terminal disposition.
- A lost acknowledgement is reconciled before retry; no duplicate external effect occurs.
- Sender and receiver cannot both hold valid write ownership for the same step.
- A policy or task revision invalidates only the affected approvals and dependent work, while independent completed evidence remains traceable.
- Rejected handoffs preserve the reason, evidence, and correction path without silently dropping pending work.

**Routing boundary:** this section owns the contract at a workflow-stage boundary. Use agent-messaging-channels for message transport and delivery semantics, delegated-execution-queues for durable scheduling and worker lifecycle, and session-continuity-recall for reconstructing interrupted execution. Transport delivery is not acceptance, acceptance is not authorization, and authorization is not proof of completion.

