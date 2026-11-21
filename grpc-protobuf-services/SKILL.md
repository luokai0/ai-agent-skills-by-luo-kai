---
name: grpc-protobuf-services
description: Use when designing, implementing, reviewing, or evolving gRPC services defined with Protocol Buffers, including .proto schema design, backward-compatibility checks, streaming choices, deadlines, error mapping, and service-to-service contract changes.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Grpc Protobuf Services

## Purpose and boundaries

Use this skill to design and review gRPC APIs and their Protocol Buffers (proto3 unless the project states otherwise) schemas, and to plan safe contract evolution across clients and servers. In scope: message and service design, field numbering, streaming modes, deadlines and cancellation, status code selection, interceptors and metadata conventions, code generation workflow, and wire-compatibility review.

Out of scope: general REST design, database schema work, load-testing results, and infrastructure provisioning (service mesh, load balancer configuration) except where they change contract behavior. Do not produce performance claims without measured data.

## Inputs and assumptions

Collect before proposing changes:
- Existing `.proto` files and the generated-code toolchain in use (name and version from the repository, not memory).
- Consumers: which services and languages call the API, and whether mobile or external clients exist.
- Compatibility requirement: internal-only, versioned public, or frozen.
- Traffic shape: unary, server-streaming, client-streaming, or bidirectional, and expected payload sizes.
- Required semantics: idempotency, ordering, timeout budgets, retry policy.

If any input is missing, state the assumption explicitly in the deliverable. Do not assume a generator plugin, runtime version, or library API; mark such details "verify against current official documentation."

## Operating workflow

1. Inventory the current contract: list services, RPCs, messages, and reserved fields.
2. Classify the requested change: additive, behavioral, breaking, or new service.
3. Draft the schema change using these rules:
   - Never reuse or renumber a field tag. Remove a field by `reserved` both its number and name.
   - Add new fields with new tags; give new enum values zero-compatible defaults and never rely on ordinal meaning.
   - Use wrapper or `optional` semantics only where presence matters; verify the presence behavior for the target language.
   - Prefer request/response wrapper messages per RPC so fields can be added later without breaking signatures.
   - Use `google.protobuf` well-known types for timestamps and durations; do not hand-roll them.
4. Choose the RPC shape: use streaming only when the payload is unbounded or incremental; otherwise prefer unary with pagination tokens.
5. Define per-RPC contract text: deadline expectation, idempotency, retry safety, and error codes returned.
6. Run the compatibility check (below) and the generation step in a clean working tree.
7. Produce the deliverable contract.

## Decision gates

- **Gate A: Breaking change?** Any removed or retyped field, changed field number, changed RPC signature, altered meaning of an existing value, or changed streaming mode is breaking. Stop and require explicit owner approval plus a versioned service (new package or new service name) with a migration window.
- **Gate B: External or public exposure?** If the API is reachable by external clients, require approval before publishing schema changes and a deprecation notice for removed behavior.
- **Gate C: Retry safety.** Mutating RPCs without an idempotency key must not be marked retryable. Require an idempotency key field or documented server-side dedupe before enabling client retries.
- **Gate D: Streaming justification.** Bidirectional streaming requires a stated reason (cancellation semantics, flow control, or long-lived push). Otherwise choose unary.
- **Gate E: Sensitive data.** Fields carrying credentials, personal data, or regulated data require approval and must not be logged in debug output or error details. Do not claim regulatory compliance.

## Verification and evidence

- Compatibility: run the repository's configured breaking-change detector if one exists; if none is configured, compare old and new descriptors manually against the rules in step 3 and record each field number checked.
- Generation: regenerate code from a clean checkout; the diff must contain only expected files. Record toolchain versions used.
- Tests: each new or changed RPC has at least one test for success, deadline exceeded, and the documented error codes. Tests must exercise a real serialized round trip, not only in-memory objects.
- Old-client check: decode a payload captured from the previous schema with the new code, and confirm defaults for missing fields.
- Quality thresholds: zero reused field numbers; every removed field reserved; every RPC has a documented deadline recommendation; every error code mapping is listed.

## Failure handling

- If a generator or detector fails, report the exact command output summary and do not hand-edit generated files.
- If compatibility is unclear (for example, a field's semantics changed without a type change), treat it as breaking and escalate to Gate A.
- If a requested behavior conflicts with gRPC status semantics, propose the nearest standard code and explain the mismatch rather than inventing a custom code.
- If evidence is missing (no tests, no toolchain version), mark the deliverable "unverified" and list the blocking items.

## Deliverable contract

Return:
1. Summary of the change and its classification (additive, behavioral, breaking).
2. Full proto diff with reserved ranges shown.
3. Per-RPC table: name, shape, deadline recommendation, idempotency, retry safety, status codes.
4. Compatibility evidence: tool output or manual checklist results.
5. Open items requiring approval, labeled by gate.
6. Toolchain versions used, or an explicit "verify against current official documentation" note for each version-sensitive detail.

Do not proceed with destructive actions such as deleting published proto files, rewriting history, or deploying schema changes to shared environments without explicit approval.