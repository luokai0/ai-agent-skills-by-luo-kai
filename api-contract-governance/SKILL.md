---
name: api-contract-governance
description: Use when defining, reviewing, versioning, or enforcing API contracts (OpenAPI, AsyncAPI, GraphQL schemas, protobuf/gRPC IDL, event schemas) across teams or services, especially when a change may break consumers or needs a compatibility decision.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Api Contract Governance

## Purpose and boundaries

This skill governs the lifecycle of machine-readable API contracts: authoring standards, compatibility classification, versioning and deprecation policy, review gates, and automated enforcement in CI. It produces decisions and evidence about whether a contract change is safe, what it breaks, and what must happen before it ships.

In scope: REST (OpenAPI), event and message schemas (AsyncAPI, Avro, JSON Schema, Protobuf topics), RPC IDL (Protobuf/gRPC, Thrift), and GraphQL schemas.

Out of scope: implementing service logic, choosing cloud infrastructure, designing business domain models beyond what the contract expresses, and security testing of endpoints (refer to a separate security review).

## Inputs and assumptions

Collect before judging any change:

1. The current published contract and the proposed contract (or diff), in their native format.
2. Inventory of known consumers: owning teams, client types (mobile apps, partners, internal services), and how they pin or generate code from the contract.
3. The organization's compatibility policy, if one exists. If none exists, state that you are applying the default policy in this document and flag it as an assumption.
4. Deployment model: whether producers and consumers deploy independently, and whether rollback is possible.
5. Traffic or usage data for affected operations, if available. Without it, assume every operation has live consumers.

Assumptions must be stated explicitly in the output. Do not assume a consumer does not exist because it is undocumented.

## Operating workflow

1. **Establish the baseline.** Identify the contract version currently live in each environment. A change is judged against what consumers actually run, not against the repository head.
2. **Produce a structural diff.** Use the schema tooling your organization already runs (for example a diff tool native to your spec format). Record the raw diff before interpreting it. Verify the tool's current behavior against its official documentation, since diff rule sets change between releases.
3. **Classify each change** using the table in Decision gates. Classify every hunk, not the overall PR.
4. **Map breakage to consumers.** For each breaking or risky change, list affected operations and the consumer groups known to use them.
5. **Choose a remedy:** reject, additive alternative, new major version, parallel operation with deprecation window, or documented breaking change with migration plan.
6. **Specify the migration path**: what consumers must change, by when, and how producers will detect remaining usage (logs, metrics, header telemetry).
7. **Run the verification checks** in the Verification section and attach evidence.
8. **Obtain the required approvals** from the decision gates before merge or publication.

## Decision gates

Classification of changes (producer perspective):

| Change | Class | Default action |
|---|---|---|
| Add optional request field | Compatible | Allow |
| Add response field (consumers must ignore unknown fields) | Compatible only if documented ignore-unknown policy exists | Allow with note |
| Add new operation or endpoint | Compatible | Allow |
| Add enum value to a response | Risky | Gate: confirm consumers tolerate unknown enum values |
| Make optional request field required | Breaking | Reject or new version |
| Remove or rename any field, operation, or enum value | Breaking | Reject or new version |
| Change field type or format | Breaking | Reject or new version |
| Tighten validation (lower max length, new pattern) | Breaking for existing clients | Gate: requires usage analysis |
| Change default value or semantics | Breaking, often silent | Gate: requires explicit consumer sign-off |
| Change error codes or status meanings | Breaking | Gate: treat as API change |

Approval rules:

- **Breaking change on a published contract:** requires owner of the producing service plus a representative from each affected consumer group, and a written deprecation or migration date.
- **Risky change:** requires the producing service owner and a documented check of consumer tolerance.
- **Compatible change:** requires only passing automated checks.
- **Any removal in a version still in its support window:** reject unless the sunset policy has been met and the sunset is approved.

## Verification and evidence

Each change must carry:

- Structural diff output with each hunk classified.
- Lint pass against the organization's style rules (naming, pagination, error model, required descriptions). Record the ruleset version.
- Contract validity check that the document parses and resolves all references.
- Consumer-facing examples or fixtures updated where the change affects them, and a passing run of those fixtures against the producer.
- For breaking changes, a usage measurement showing the share of traffic from each client version over the trailing window you choose. State the window; a one-day sample is insufficient for quarterly-release clients.
- A migration checklist with owners and dates.

Measurable quality checks:

- Zero unclassified hunks in the diff report.
- Zero unapproved breaking changes in the release.
- Every deprecated operation carries a sunset date and a deprecation marker in the contract.
- Usage of deprecated operations is reported weekly until it reaches the agreed threshold before removal.

Do not claim that a change is "backward compatible" without the diff and consumer evidence. Do not cite compliance or certification outcomes.

## Failure handling

- **Diff tool unavailable or output ambiguous:** stop classification, report which hunks are unresolved, and do not approve them by default.
- **Consumer inventory missing for an affected operation:** treat the operation as having unknown consumers, which triggers the breaking-change gate.
- **Usage data missing:** state that removal cannot be justified on usage grounds and recommend a deprecation window instead.
- **Conflicting policy and tooling results:** escalate to the contract owner; do not resolve by choosing the more permissive reading.
- **Published contract already changed incompatibly:** open an incident-style review, identify affected consumers, and propose a restoration or forward migration. Do not silently republish.

## Deliverable contract

Produce a governance record containing:

1. Summary verdict: approve, approve with conditions, or reject, with one-sentence rationale.
2. Baseline version and proposed version identifiers.
3. Classified change table (change, class, affected operations, consumer groups).
4. Required remedy and, if breaking, the migration plan with dates and owners.
5. Evidence list: diff output, lint result, validation result, fixture results, usage data window.
6. Explicit assumptions and unresolved items.
7. Required approvals, marked pending until obtained.

Version-sensitive details (tool flags, rule identifiers, spec-format features) must be marked "verify against current official documentation" when cited.

## Things not to do

- Do not publish, merge, or deprecate a contract without explicit approval from the gates above.
- Do not remove a published operation, field, or enum value to "clean up" without the breaking-change path.
- Do not treat internal-only status as permission to skip consumer mapping.
- Do not change production traffic routing, sunset dates, or client-facing notices on your own authority; these are external-impacting actions requiring named approval.
- Do not infer consumer behavior from the spec alone; confirm with usage evidence or owners.
- Do not invent rule names, tool flags, or benchmark figures.
## API contracts for agent-facing operations (v1.1)

An agent-facing API must be designed for uncertain callers, retries, partial completion, and asynchronous work. Define stable operation names, typed request and response schemas, explicit error classes, authorization requirements, side-effect descriptions, idempotency behavior, versioning rules, and compatibility guarantees. Avoid ambiguous generic endpoints that allow the model to construct arbitrary operations.

Use explicit task resources for long-running work: create task, retrieve task status, cancel task, and retrieve or stream artifacts. Define legal state transitions and terminal states. Return a stable operation or task identifier immediately rather than holding a connection open for unbounded reasoning. Distinguish accepted, running, completed, failed, cancelled, and partially completed states.

Use idempotency keys for creation and write operations. Define key scope, retention, collision behavior, and replay response. For updates, use version preconditions or ETags to prevent stale writes. Document pagination cursors, ordering guarantees, maximum page sizes, rate limits, and retry-after behavior. Errors must distinguish invalid input, authorization denial, conflict, rate limit, transient dependency failure, timeout with unknown outcome, and permanent failure.

Version schemas additively where possible. For breaking changes, publish a new version, define a migration window, and test old and new clients against the same contract. Validate generated SDKs and examples against the actual server implementation. Keep examples safe by default and avoid embedding real credentials.

For every operation, test schema validation, auth scopes, cross-tenant identifiers, duplicate requests, stale preconditions, partial failure, cancellation, oversized payloads, and backward compatibility. A valid OpenAPI or JSON schema document is not evidence that runtime behavior conforms; run contract tests against the deployed adapter.

