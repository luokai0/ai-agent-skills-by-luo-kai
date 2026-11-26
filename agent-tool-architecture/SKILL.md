---
name: agent-tool-architecture
description: Use when designing, reviewing, or refactoring the tool layer of an LLM agent, including tool schemas, permission boundaries, error contracts, tool selection policies, and multi-step tool orchestration.
author: Luo Kai
provenance: original
version: 1.4.0
---

# Agent Tool Architecture

## Purpose and boundaries

This skill covers the interface between a model-driven agent and the external capabilities it invokes: function or tool schemas, argument validation, result shaping, permission scoping, retry and timeout policy, and orchestration of multi-call sequences.

In scope: designing tool catalogs, writing tool descriptions and schemas, deciding which tools an agent may see, sequencing dependent calls, defining structured error returns, and auditing a running tool layer for ambiguity or unsafe capability.

Out of scope: model selection, prompt tuning unrelated to tool use, general application architecture, and infrastructure hardening beyond what a tool boundary requires. Do not use this skill to justify granting broad capabilities; it exists to narrow and clarify them.

## Inputs and assumptions

Collect before designing:

1. The agent's task list, with the top 10 real user requests and their expected outcomes.
2. Every existing or proposed capability: system, owner, read or write nature, data sensitivity, and rollback path.
3. The identity under which each tool executes (agent service account, delegated user, or elevated role).
4. Latency and rate limits of each backend, from its own documentation.
5. The model and runtime that will call the tools. Tool-calling formats and parameter-schema support differ across providers and versions; mark any format-specific detail as requiring verification against current official documentation before implementation.

If any item is missing, state the assumption explicitly in the deliverable. Do not guess owner, sensitivity, or rollback path.

## Operating workflow

1. **Inventory capabilities.** List each underlying operation (for example, "read invoice by ID", "send email", "delete record"). Split compound operations into atomic tools.
2. **Classify each tool** on three axes: effect (read-only, reversible write, irreversible write, external send), data class (public, internal, personal, regulated), and cost (free, metered, rate-limited).
3. **Minimize the surface.** Remove tools the stated tasks do not need. Merge tools only when they share identical permissions and failure modes. Target fewer than roughly 15 tools per agent unless evidence shows more are needed; overlapping tools degrade selection accuracy.
4. **Write the contract for each tool:**
   - Name: verb-noun, unambiguous, stable.
   - Description: one sentence on what it does, one on when not to use it, and any precondition.
   - Parameters: typed, with enums where the domain is closed, explicit units and formats (ISO 8601 dates, minor currency units, and so on), and no free-form fields that could carry instructions or credentials.
   - Required versus optional: default optional only when a safe default exists and is documented.
5. **Define the result shape.** Success returns the minimal fields needed for the next decision. Failure returns a machine-readable code, a human-readable message, a `retryable` boolean, and the offending field where applicable.
6. **Specify orchestration.** For dependent calls, document the order, the data passed between steps, and the compensating action if a later step fails.
7. **Assign permissions** per tool, not per agent, using least privilege.
8. **Draft a test set** (see Verification).

## Decision gates

Stop and obtain explicit human approval before:

- Adding any tool that deletes, overwrites, or migrates data, or that cannot be rolled back.
- Adding any tool that sends messages, payments, or instructions outside the organization, or that changes external state.
- Granting write access to systems of record, production configuration, identity or access settings, or financial ledgers.
- Exposing personal, health, financial, or other regulated data to a tool whose output enters model context or logs.
- Letting an agent chain more than one irreversible action without a confirmation step in between.
- Using a tool whose vendor terms, data-retention behavior, or rate limits are unknown or unverified.

Proceed without a gate for read-only tools over internal non-sensitive data, and for reversible writes inside a sandbox or staging environment.

When in doubt about classification, classify higher-risk.

## Verification and evidence

Each tool must pass these checks before release:

- **Schema validity:** every argument is validated server-side regardless of model output. Reject, do not coerce, out-of-range or unknown fields.
- **Selection accuracy:** on a held-out set of at least 30 realistic requests per agent, measure the proportion where the correct tool (or correct "no tool") is chosen. Record the number; do not report it without the set size.
- **Argument accuracy:** measure exact-match rate for required parameters on the same set.
- **Failure paths:** each documented error code is triggered at least once in tests, including timeout, permission denied, not found, and validation failure.
- **Idempotency:** every write tool either is idempotent or accepts an idempotency key; test a duplicated call.
- **Rollback:** for reversible writes, demonstrate the compensating action in staging.
- **Audit logging:** every invocation logs tool name, caller identity, arguments with sensitive fields redacted, result status, and timestamp.

Benchmark claims must come from measurements in your own environment. Do not cite external accuracy figures as guarantees.

## Failure handling

- **Validation error:** return the field and reason; the agent may retry once with corrected arguments. Do not retry blindly with identical input.
- **Transient error (timeout, 429, 503):** retry with exponential backoff and jitter, capped at a small fixed attempt count. Respect any server-supplied retry hint.
- **Permission denied:** do not retry, do not attempt alternate tools to bypass it. Escalate to the user or operator.
- **Unknown state after a write timeout:** do not re-issue the write. Query the resource state using a read tool, then decide.
- **Partial multi-step failure:** execute the documented compensating action in reverse order, then report which steps completed.
- **Repeated tool loops** (same call with same arguments more than twice): halt and surface the trace.

## Deliverable contract

The deliverable is a single document containing:

1. Capability inventory table: operation, effect class, data class, identity, owner.
2. Tool catalog: for each tool, name, description, parameter schema, result and error schema, permission scope, retry policy.
3. Decision-gate register: which tools require approval and the approver role.
4. Orchestration diagrams or ordered lists for every multi-step flow, with compensating actions.
5. Evaluation report: test set size and composition, selection accuracy, argument accuracy, failure-path coverage, with measured numbers.
6. Open assumptions and items requiring verification against current official vendor documentation, each with an owner.

Do not deliver a catalog without the evaluation report. Do not present unmeasured quality as established.

## What not to do

- Do not expose a generic "execute query" or "run shell" tool when specific operations would suffice.
- Do not let tool descriptions contain instructions to the model that override system policy.
- Do not pass credentials, tokens, or secrets as tool arguments; resolve them server-side.
- Do not return entire raw records when a few fields answer the question.
- Do not add tools speculatively for future use.
- Do not treat model-supplied arguments as trusted.
## Tool capability engineering (v1.1)

Design tools as narrow capabilities, not wrappers around unrestricted systems. Each contract must specify stable name and purpose, caller identity, authorization rule, typed input and output schemas, error variants, side-effect class, resource scope, data classification, idempotency, concurrency, timeout, retry, rate limit, pagination, approval, audit receipt, owner, version, and deprecation policy.

Prefer bounded business operations such as get_invoice, draft_refund, and approve_refund over generic SQL, shell, or arbitrary HTTP tools. Split reads from writes and draft creation from final submission.

A robust gateway call follows this order: authenticate and bind the run/tenant; validate tool and schema; resolve canonical resource identifiers; verify ownership and scope; classify effects; evaluate policy; verify an exact, unexpired approval binding; enforce budgets, rate and concurrency limits; apply idempotency; execute with a scoped credential outside model context; capture the downstream receipt; read back the resulting state; return a minimal structured result and correlation ID.

Idempotency keys must be persisted at the system boundary. Replays return the original result or a safe conflict. Where the API lacks idempotency, reconcile state before retry and document race conditions. Use bounded pagination with stable ordering and explicit completeness markers. Long-running operations should return an operation handle and a separate status method. Use optimistic concurrency to reject stale writes. Multi-system workflows need explicit compensating actions; do not call compensation a true rollback when external effects cannot be undone.

Test each tool with valid, missing, extra, wrong-type, and boundary inputs; unauthorized principal; cross-tenant target; timeout before and after execution; duplicate key; stale version; rate limit; malformed downstream response; and partial failure. Verify stable error variants and minimal outputs without secrets.

## Ultron routing contract

**Choose this skill when:** designing the general tool boundary between an agent and external capabilities: capability granularity, schemas, authorization, idempotency, side-effect classes, error contracts, concurrency, and tool lifecycle.

**Choose `mcp-and-agent-tooling` when:** the task specifically implements MCP clients/servers, protocol negotiation, resources, prompts, or MCP tool interoperability.

**Choose `mcp-server-hardening` when:** an existing MCP server needs a security assessment or hardening pass. Use `agent-runtime-security-guardrails` for platform-wide identity, policy enforcement, and runtime isolation.

**Handoff contract:** provide the capability inventory, schemas, side effects, resource scope, caller identity, error behavior, and test obligations. The implementation or hardening skill returns protocol-specific evidence and negative tests; this skill checks that the resulting tool surface still follows the approved capability model.

**Why the boundary exists:** tool architecture defines the safe abstraction; protocol integration and security review are specialized implementations of that abstraction.

## Delegated identity and tenant isolation (v1.3)

### Bind every invocation to a principal and tenant

A tool call must carry a server-verified run identity, initiating principal, effective delegated principal (if any), tenant or workspace, environment, and policy decision reference. Never trust a tenant ID, user ID, role, or resource owner supplied only in model-generated arguments. Resolve identity from authenticated runtime context and bind the target resource to that identity before authorization.

For delegated user access, use the narrowest supported delegated scope and preserve the distinction between the service identity and the user on whose behalf it acts. Do not silently fall back to a service administrator when delegated authorization fails. A permission denial is a terminal policy result, not a cue to try a more powerful credential.

### Enforce tenant boundaries below the model

Apply tenant filtering in the authoritative data or service layer, not only in tool descriptions or prompt instructions. Every lookup, search, mutation, cache key, object-store path, and asynchronous operation must carry a verified tenant boundary. For indirect identifiers, confirm the resolved object belongs to the authorized tenant before returning whether it exists or exposing metadata. Avoid cross-tenant existence leaks through error messages or timing where practical.

Partition caches and idempotency records by tenant and principal where required. Ensure queued jobs retain the original authorized scope and revalidate it at execution time; permissions may have been revoked while a job waited. A worker must not inherit a broader scope merely because it runs under a shared service account.

### Test isolation as a negative property

Create two synthetic tenants with deliberately overlapping identifiers and similar records. Test reads, search, pagination, exports, writes, deletes, cache hits, retries, and resumed jobs from both identities. Verify a tenant-A caller cannot discover, infer, mutate, or receive tenant-B data, including through error details and audit records. Test stale delegation, revoked membership, changed ownership, and cross-tenant idempotency-key reuse.

### Audit without leaking data

Record authenticated principal, delegated principal, tenant, tool version, resource reference, policy decision, correlation ID, and outcome. Redact secrets and minimize personal data; use stable opaque references instead of copying full payloads into logs. Ensure the audit sink itself enforces tenant visibility and retention policy.


## Long-running tool operation contracts (v1.4)

### Separate request acceptance from operation completion

A tool that starts work which may outlive the request-response window must return a durable operation handle, not a success-shaped response that implies the work is finished. Define distinct outcomes for request rejected, operation accepted, operation running, operation succeeded, operation failed, operation cancellation requested, operation cancelled, and outcome unknown. The acceptance response confirms only that the service durably accepted responsibility for the operation.

Each operation record should bind an opaque operation ID to the initiating run, authenticated principal, tenant, tool and contract version, normalized request digest, idempotency key, creation time, expiry/retention policy, and current state. Do not expose sequential IDs or allow a caller to retrieve an operation merely by guessing its identifier; authorize every status, result, and cancellation request against the original scope.

### Make polling and notifications converge

Provide one authoritative status representation regardless of whether the caller learns about changes by polling, webhook, queue event, or agent message. Include a monotonic state revision or event sequence so consumers can ignore stale and duplicated notifications. Notifications are hints to fetch authoritative state, not proof that the operation reached a terminal state. Status reads should expose whether results are complete, partial, unavailable, or expired.

Define bounded polling intervals and backoff, Retry-After behavior, terminal-state retention, and what happens when the operation record expires before the caller retrieves the result. Do not make consumers infer completion from a missing queue message or a timed-out status request.

### Specify cancellation as a distributed operation

Cancellation is a request, not a guarantee that work stopped. Model cancellation-requested separately from cancelled. The worker must acknowledge that it stopped before the system reports cancellation as complete. If the operation crossed an irreversible side-effect boundary, return the actual effect state and the available compensation path rather than claiming the operation was undone.

Cancellation must be idempotent and race-safe against completion. Define precedence when completion and cancellation occur concurrently, and preserve the final authoritative outcome. If the worker is unreachable, mark the outcome unresolved and schedule reconciliation; do not silently mark the task cancelled.

### Reconcile retries and unknown outcomes

A client timeout can occur before acceptance, after durable acceptance, or after the side effect completed but before the response arrived. Reuse the same idempotency key for retries of the same logical request. Query by that key or operation handle before creating a replacement operation. Bind idempotency records to principal, tenant, tool version, and normalized request digest; reject reuse with different arguments or scope.

For external side effects, persist the downstream receipt and read back the target state where possible. Distinguish the operation's orchestration state from the external resource's effect state. If they disagree, surface a reconciliation-required state and prevent unsafe duplicate execution.

### Acceptance tests

- Client timeout before acceptance, after acceptance, and after downstream completion.
- Duplicate start request with the same key and identical request digest.
- Same key reused with changed arguments, tenant, or principal.
- Duplicate and out-of-order status notifications.
- Polling during state transition and after terminal-state expiry.
- Cancellation before execution, during execution, after an irreversible effect, and racing with completion.
- Worker crash after downstream success but before recording completion.
- Status or cancellation request from a different tenant or unauthorized principal.

The tool contract must document operation states, status consistency, idempotency scope, cancellation semantics, retention, notification behavior, reconciliation, and the exact meaning of every success response. Test that callers cannot mistake accepted, cancellation-requested, or unknown for completed or cancelled.

**Routing boundary:** this section owns the external tool contract for durable asynchronous operations. Use delegated-execution-queues for queue leases, delivery, retries, dead-lettering, and worker mechanics; use session-continuity-recall for restoring an agent's conversation/run context. A durable operation handle is the cross-boundary reference, not a substitute for either queue correctness or session recovery.
