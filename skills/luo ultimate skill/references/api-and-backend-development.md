# API and Backend Development

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## api-contract-governance

**Use when:** Use when defining, reviewing, versioning, or enforcing API contracts (OpenAPI, AsyncAPI, GraphQL schemas, protobuf/gRPC IDL, event schemas) across teams or services, especially when a change may break consumers or needs a compatibility decision.

### Purpose and boundaries

This skill governs the lifecycle of machine-readable API contracts: authoring standards, compatibility classification, versioning and deprecation policy, review gates, and automated enforcement in CI. It produces decisions and evidence about whether a contract change is safe, what it breaks, and what must happen before it ships.

In scope: REST (OpenAPI), event and message schemas (AsyncAPI, Avro, JSON Schema, Protobuf topics), RPC IDL (Protobuf/gRPC, Thrift), and GraphQL schemas.

Out of scope: implementing service logic, choosing cloud infrastructure, designing business domain models beyond what the contract expresses, and security testing of endpoints (refer to a separate security review).

### Inputs and assumptions

Collect before judging any change:

1. The current published contract and the proposed contract (or diff), in their native format.
2. Inventory of known consumers: owning teams, client types (mobile apps, partners, internal services), and how they pin or generate code from the contract.
3. The organization's compatibility policy, if one exists. If none exists, state that you are applying the default policy in this document and flag it as an assumption.
4. Deployment model: whether producers and consumers deploy independently, and whether rollback is possible.
5. Traffic or usage data for affected operations, if available. Without it, assume every operation has live consumers.

Assumptions must be stated explicitly in the output. Do not assume a consumer does not exist because it is undocumented.

### Operating workflow

1. **Establish the baseline.** Identify the contract version currently live in each environment. A change is judged against what consumers actually run, not against the repository head.
2. **Produce a structural diff.** Use the schema tooling your organization already runs (for example a diff tool native to your spec format). Record the raw diff before interpreting it. Verify the tool's current behavior against its official documentation, since diff rule sets change between releases.
3. **Classify each change** using the table in Decision gates. Classify every hunk, not the overall PR.
4. **Map breakage to consumers.** For each breaking or risky change, list affected operations and the consumer groups known to use them.
5. **Choose a remedy:** reject, additive alternative, new major version, parallel operation with deprecation window, or documented breaking change with migration plan.
6. **Specify the migration path**: what consumers must change, by when, and how producers will detect remaining usage (logs, metrics, header telemetry).
7. **Run the verification checks** in the Verification section and attach evidence.
8. **Obtain the required approvals** from the decision gates before merge or publication.

### Decision gates

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

### Verification and evidence

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

### Failure handling

- **Diff tool unavailable or output ambiguous:** stop classification, report which hunks are unresolved, and do not approve them by default.
- **Consumer inventory missing for an affected operation:** treat the operation as having unknown consumers, which triggers the breaking-change gate.
- **Usage data missing:** state that removal cannot be justified on usage grounds and recommend a deprecation window instead.
- **Conflicting policy and tooling results:** escalate to the contract owner; do not resolve by choosing the more permissive reading.
- **Published contract already changed incompatibly:** open an incident-style review, identify affected consumers, and propose a restoration or forward migration. Do not silently republish.

### Deliverable contract

Produce a governance record containing:

1. Summary verdict: approve, approve with conditions, or reject, with one-sentence rationale.
2. Baseline version and proposed version identifiers.
3. Classified change table (change, class, affected operations, consumer groups).
4. Required remedy and, if breaking, the migration plan with dates and owners.
5. Evidence list: diff output, lint result, validation result, fixture results, usage data window.
6. Explicit assumptions and unresolved items.
7. Required approvals, marked pending until obtained.

Version-sensitive details (tool flags, rule identifiers, spec-format features) must be marked "verify against current official documentation" when cited.

### Things not to do

- Do not publish, merge, or deprecate a contract without explicit approval from the gates above.
- Do not remove a published operation, field, or enum value to "clean up" without the breaking-change path.
- Do not treat internal-only status as permission to skip consumer mapping.
- Do not change production traffic routing, sunset dates, or client-facing notices on your own authority; these are external-impacting actions requiring named approval.
- Do not infer consumer behavior from the spec alone; confirm with usage evidence or owners.
- Do not invent rule names, tool flags, or benchmark figures.
### API contracts for agent-facing operations (v1.1)

An agent-facing API must be designed for uncertain callers, retries, partial completion, and asynchronous work. Define stable operation names, typed request and response schemas, explicit error classes, authorization requirements, side-effect descriptions, idempotency behavior, versioning rules, and compatibility guarantees. Avoid ambiguous generic endpoints that allow the model to construct arbitrary operations.

Use explicit task resources for long-running work: create task, retrieve task status, cancel task, and retrieve or stream artifacts. Define legal state transitions and terminal states. Return a stable operation or task identifier immediately rather than holding a connection open for unbounded reasoning. Distinguish accepted, running, completed, failed, cancelled, and partially completed states.

Use idempotency keys for creation and write operations. Define key scope, retention, collision behavior, and replay response. For updates, use version preconditions or ETags to prevent stale writes. Document pagination cursors, ordering guarantees, maximum page sizes, rate limits, and retry-after behavior. Errors must distinguish invalid input, authorization denial, conflict, rate limit, transient dependency failure, timeout with unknown outcome, and permanent failure.

Version schemas additively where possible. For breaking changes, publish a new version, define a migration window, and test old and new clients against the same contract. Validate generated SDKs and examples against the actual server implementation. Keep examples safe by default and avoid embedding real credentials.

For every operation, test schema validation, auth scopes, cross-tenant identifiers, duplicate requests, stale preconditions, partial failure, cancellation, oversized payloads, and backward compatibility. A valid OpenAPI or JSON schema document is not evidence that runtime behavior conforms; run contract tests against the deployed adapter.

### Ultron routing contract

**Choose this skill when:** defining or evolving stable APIs for agent-facing operations, including asynchronous tasks, idempotency, versioning, preconditions, error categories, lifecycle states, and compatibility guarantees.

**Choose `mcp-and-agent-tooling` when:** exposing capabilities through MCP tool/resource/prompt contracts and implementing protocol-level interoperability.

**Choose `agent-messaging-channels` when:** the contract is an agent-to-agent message or task exchange rather than a conventional service API.

**Handoff contract:** return the canonical request/response schema, state machine, authorization assumptions, idempotency behavior, error taxonomy, compatibility policy, and contract tests. MCP or messaging adapters must preserve those semantics instead of inventing different retry, identity, or completion rules.

**Why the boundary exists:** service API contracts, tool invocation protocols, and agent messages may carry similar data but have different lifecycle and delivery guarantees.


## api-design-security-and-app-scaffolding

**Use when:** Use when designing or reviewing an HTTP API, generating a new application scaffold, or hardening an existing service's authentication, authorization, input validation, and configuration before code is written or merged.

### Purpose and boundaries

This skill covers three linked tasks: (1) specifying an HTTP API contract, (2) producing a secure application skeleton that implements that contract, and (3) reviewing the security posture of the contract and skeleton. It applies to REST and JSON-over-HTTP services, and to scaffolds for web backends that expose them.

It does not cover: frontend UI design, infrastructure provisioning in live cloud accounts, penetration testing of systems you do not own, compliance certification (SOC 2, PCI, HIPAA, and similar, which require auditors), or choosing business logic. Where a task crosses those lines, produce the artifact within scope and flag the rest for a human owner.

### Inputs and assumptions

Before working, collect or state explicitly:

- Consumers of the API (first-party, partner, public) and their trust level.
- Data classification of each resource: public, internal, personal, or regulated.
- Authentication method in use or required (for example, OAuth 2.0 / OpenID Connect via an existing identity provider, or API keys for machine clients).
- Expected scale, latency targets, and rate-limit needs, stated as numbers if known.
- Target language and framework. Record the exact version. Do not assume a framework's current API surface; mark any version-sensitive call for verification against its current official documentation.
- Deployment target (container, serverless, VM), since it changes secret handling and logging.

If any item is missing and affects security or data handling, mark it as an assumption in the deliverable and list it under open questions. Do not silently default to permissive behavior.

### Operating workflow

1. **Model resources and actions.** List nouns (resources), their identifiers, and the operations on them. Map each operation to the minimum role or scope that may invoke it.
2. **Write the contract first.** Use an OpenAPI-style description. For every operation define: path, method, request schema, response schemas for success and each error class, idempotency behavior for unsafe methods, pagination for collections, and authentication requirement.
3. **Define errors uniformly.** Use one error envelope across the service with a stable machine-readable code, a human message that never echoes secrets or stack traces, and a correlation ID. Map validation failures to 400 or 422 consistently, authentication failures to 401, authorization failures to 403, and avoid leaking existence of resources a caller cannot see (return 404 where appropriate).
4. **Specify authorization per object.** Authentication alone is insufficient. For each resource-scoped operation, state the ownership or tenancy check performed against the server-side record, not against client-supplied fields.
5. **Specify validation at the boundary.** Enforce maximum body size, maximum string length, allowed character sets, numeric ranges, enum membership, and rejection of unknown fields for write operations. Validate content type; reject mismatches.
6. **Generate the scaffold.** Structure: entry point, configuration loader, router, middleware chain (request ID, authentication, authorization helpers, validation, rate limiting, structured logging, error handler), service layer, data access layer, tests. Load secrets from the environment or a secret manager; never from committed files.
7. **Apply secure defaults.** TLS terminated at the edge with redirect from plaintext; security headers set; CORS restricted to an explicit origin list; debug mode disabled by default; parameterized queries only; passwords and tokens hashed or stored by the identity provider, never logged.
8. **Add tests alongside.** Write tests for each authorization rule (allowed and denied cases), each validation rule, and each error path.

### Decision gates

Stop and obtain explicit human approval before proceeding when any of the following applies:

- The change deletes or migrates data, alters a schema in place, or rotates credentials.
- The change exposes a new public endpoint, changes an existing public contract in a breaking way, or alters CORS or authentication rules.
- The change stores or transmits regulated or personal data in a new location or to a third party.
- The change would call an external production system, send messages, or trigger payments.
- The chosen authentication scheme is custom rather than a standard protocol implementation.

Proceed without a gate only for additive, internal, reversible work that stays within the declared scope.

### Verification and evidence

Each deliverable must include evidence for these checks. Report the result, not an assumption:

- Every operation in the contract has an explicit auth requirement; zero operations are marked "none" without justification.
- Every resource-scoped read and write has a server-side ownership or role check, with a test for a denied cross-tenant request.
- Validation tests cover oversize input, unknown fields, wrong content type, and out-of-range values; each returns the uniform error envelope.
- No secret literals appear in the repository; run a secret-scanning tool and record its version and output summary.
- Dependencies are pinned to versions recorded in the lockfile; known-vulnerability scan results are attached with the tool name and date.
- Logs for a sample failing request contain the correlation ID and no tokens, passwords, or full personal data.
- Rate limits and body-size limits are configured with stated numeric values, and a test demonstrates rejection beyond the limit.

Do not state performance figures, throughput, or compliance status unless measured in the stated environment.

### Failure handling

- If a required input is missing and it affects security, halt and ask. Otherwise record the assumption.
- If a framework feature needed is uncertain in the pinned version, mark it "verify against current official documentation" and write the smallest verifiable alternative.
- If a test or scan fails, do not weaken the test. Fix the cause or report it as an open defect with severity.
- If an authorization rule cannot be expressed cleanly, default to deny and escalate.

### Deliverable contract

Deliver exactly these items:

1. OpenAPI-style contract covering all operations, with auth, errors, pagination, and idempotency specified.
2. Scaffold file tree and the code for entry point, configuration, middleware chain, error handler, and one fully implemented resource with its authorization and validation.
3. Test suite covering the verification checks above.
4. Configuration reference listing each environment variable, its purpose, its default, and whether it is a secret. Do not invent variables beyond those the code reads.
5. Security notes: assumptions, decision gates triggered and their approval status, open risks with severity, and items requiring verification against current official documentation.

Do not present the output as production-ready until every verification check is either passed with evidence or listed as an open risk with an owner.

### Ultron routing contract

**Choose this skill when:** the deliverable combines an HTTP API contract with a secure application skeleton that implements it. It owns resource and endpoint shape, request/response conventions, initial application structure, and the security posture of that contract and scaffold.

**Choose rest-api-design-security when:** the API already exists or the task is specifically to assess its HTTP/JSON security boundary: authentication, authorization, validation, response shaping, rate limits, transport, and logging.

**Handoff contract:** provide the API schema, trust boundaries, identity assumptions, scaffold implementation, and known risks. The REST security skill returns prioritized boundary findings and controls; this skill integrates required contract/scaffold changes and reruns the end-to-end API contract checks.

**Why the boundary exists:** creating a usable API skeleton and independently reviewing an API's security properties are related but different deliverables.


## backend-web-frameworks

**Use when:** Use when designing, building, reviewing, or debugging server-side web applications or HTTP APIs in a backend framework, including routing, middleware, request validation, data access wiring, authentication hooks, and deployment-readiness checks.

### Purpose and boundaries

This skill covers choosing, structuring, and reviewing server-side web code built on a backend framework: request lifecycle, routing, middleware or interceptors, validation, error mapping, configuration, and the seams to databases, caches, queues, and identity providers. It does not cover frontend rendering, infrastructure provisioning, or language-level design beyond what the framework requires. Treat framework-specific names, flags, and versions as unverified until checked against the current official documentation for the exact version in use.

### Inputs and assumptions

Before acting, establish:

- Language, framework, and exact version from the lockfile or manifest, not from memory.
- Runtime target (container, serverless, long-running process) and expected concurrency model.
- Existing conventions: router style, error envelope, logging format, test harness.
- Traffic and latency expectations, if stated. If absent, state that performance claims are unmeasured.
- Data sensitivity: personal data, credentials, payment data, or regulated records.

If any of these are missing and they change the design, ask rather than assume.

### Operating workflow

1. Map the request path: entry point, global middleware, route matching, authentication, validation, handler, data call, response serialization, error handler.
2. Identify the framework's documented extension points (middleware, guards, dependency injection, lifecycle hooks) and place each concern in exactly one of them.
3. Define input contracts first: schema for path, query, headers, and body, with explicit maximum sizes and rejection of unknown fields where the API is strict.
4. Keep handlers thin. Business rules belong in plain functions or services that can be tested without starting the server.
5. Centralize error mapping so that internal exceptions never reach clients with stack traces, SQL text, or secret values.
6. Set timeouts on outbound calls and database operations. Make them configurable and document defaults.
7. Confirm graceful shutdown: stop accepting new requests, drain in-flight work, close pools.
8. Add structured logs with request identifiers; exclude credentials, tokens, and personal fields.

### Decision gates

- **Sync vs. offloaded work:** If an operation exceeds the request timeout budget or depends on an unreliable third party, move it to a queue or background job with idempotency keys. Do not extend timeouts to hide it.
- **Middleware vs. handler logic:** Cross-cutting behavior (auth, rate limits, tracing) goes in middleware. Resource-specific authorization stays with the resource.
- **Framework upgrade:** Before changing major versions, read the migration notes for every breaking change touching used features, then run the full test suite on a branch.
- **Custom vs. built-in:** Use the framework's built-in parser, validator, or session support unless it is documented as unable to meet a stated requirement.
- **Stop and request approval** before: deleting or rewriting migrations, altering authentication or authorization logic, changing public API contracts, modifying production configuration, rotating secrets, or deploying. These require explicit human approval with the diff or plan shown first.

### Verification and evidence

- Run the project's existing test and lint commands; report exact output summaries, not paraphrased success.
- For each new endpoint: test success, validation failure, unauthenticated access, unauthorized access, and oversized input.
- Confirm that error responses match the documented envelope and contain no internal details, checked with a deliberately failing request.
- Verify timeouts with a test that exceeds them, and confirm the resulting status code.
- Check that secrets are read from the environment or a secret store, and that no literal credentials appear in the diff.
- Any performance statement must cite a measurement with method, load shape, and environment. Otherwise write "not measured."
- Confirm compatibility claims against the pinned framework version's official documentation.

### Failure handling

- If a framework behavior contradicts its documentation, pin the version, record the observed behavior with a minimal reproduction, and report it rather than working around it silently.
- If tests fail after a change, revert the smallest unit that caused it and explain the cause before retrying.
- If required documentation is unavailable, mark the affected design decision as unverified and list it in the deliverable.
- If a security-relevant defect is found, stop feature work, document it, and escalate for approval before fixing.

### Deliverable contract

Every result must include:

1. A short summary of the change and its affected routes or modules.
2. The request-path map, with the extension point used for each concern.
3. Test and lint results with exact commands and outcomes.
4. A list of assumptions, unverified version-specific details, and unmeasured claims.
5. Explicit approval requests for any gated action not yet approved.
6. Known limitations and follow-up items, each with an owner or "unassigned" stated plainly.

Do not claim production readiness, compliance, or security guarantees. Do not invent library names, configuration keys, or benchmark figures.

### Ultron routing contract

**Choose this skill when:** the task is framework-neutral backend engineering: comparing server frameworks across languages, designing request lifecycles, middleware/interceptor boundaries, routing, validation, error mapping, configuration, or integration seams to storage, queues, caches, and identity providers.

**Choose `python-web-frameworks` when:** the application is implemented in Python and the work depends on Python-specific framework selection, idioms, dependency injection, ASGI/WSGI behavior, async integration, or Python production conventions.

**Handoff contract:** this skill supplies the backend architecture and required behavior; the Python specialization maps it to the verified Python runtime and framework version, then returns implementation constraints and test evidence. If the codebase is not Python, do not route it to the Python skill merely because an API framework is involved.

**Why the boundary exists:** backend principles transfer across languages, but framework lifecycle, concurrency, typing, and deployment semantics do not.


## dotnet-web-and-enterprise

**Use when:** Use when designing, building, reviewing, or debugging ASP.NET Core web applications, APIs, background services, or enterprise .NET systems involving dependency injection, middleware, authentication, data access, configuration, hosting, or deployment.

### Purpose and boundaries

This skill guides work on server-side .NET systems: ASP.NET Core web apps and HTTP APIs, hosted background workers, dependency injection composition, middleware pipelines, authentication and authorization, configuration and options, data access layers, logging and observability, and deployment to containers or managed hosts.

In scope: architecture review, implementation guidance, troubleshooting request and startup failures, performance and reliability reasoning, and migration planning between .NET versions.

Out of scope: desktop UI frameworks, mobile, game engines, and legal or certification claims about compliance. Do not assert that a design satisfies a regulation, standard, or audit requirement; describe controls and recommend review by the responsible party.

### Inputs and assumptions

Before advising, establish:

1. Target framework and SDK version (for example, the TFM in the project file and the output of the SDK version command).
2. Hosting model: IIS, Kestrel behind a reverse proxy, containers, serverless, or Windows services.
3. Data stores, their engines and versions, and whether migrations are already in use.
4. Identity provider and token format, if authentication is involved.
5. Traffic shape, latency targets, and whether the workload is stateless.
6. Existing conventions: solution layout, logging library, error contract, and test frameworks.

If any item is unknown, state the assumption explicitly in your output. Do not guess framework behavior for a version you have not confirmed.

### Operating workflow

1. Reproduce or read the evidence first. Obtain the exception text, stack trace, failing request, configuration section, or relevant log lines before proposing changes.
2. Map the request or startup path. Identify the host builder steps, registered services and their lifetimes, the middleware order, and the endpoint or controller that runs.
3. Classify the problem: composition (DI resolution, lifetime mismatch), pipeline (middleware order, short-circuiting), configuration (binding, environment overrides, secrets sourcing), data (query shape, connection scope, transactions), or runtime (threads, timeouts, cancellation).
4. Propose the smallest change that addresses the classified cause. Prefer framework-provided mechanisms over custom infrastructure.
5. Specify how the change is verified (Section below) and what rollback looks like.

### Decision gates

Stop and request explicit approval before any of the following:

- Running database migrations, schema drops, data deletion, or bulk updates against any environment other than a disposable local one.
- Changing authentication, authorization policies, token lifetimes, CORS origins, or certificate handling in a shared environment.
- Rotating, printing, or committing secrets, connection strings, or keys.
- Deploying, scaling, or altering production routing, DNS, or load balancer configuration.
- Calling third-party or externally visible APIs with real credentials or real customer data.
- Disabling security middleware, validation, or rate limits, even temporarily.

Proceed without approval only for read-only analysis, local code changes, and local test runs that touch no real data.

Choose lifetimes deliberately: a singleton must not capture scoped or transient services that hold request state or database contexts. If a design requires that capture, stop and redesign.

### Verification and evidence

- Build with warnings treated as review items, not ignored. Report the exact command and result.
- Run the relevant automated tests. For startup problems, validate the host builder in a test that resolves required services and fails fast on invalid scopes where the framework supports validation options; confirm the option names against current documentation.
- For API changes, verify status codes, response shapes, and error contracts with integration tests against the real pipeline (in-memory test hosts are acceptable when the data layer is isolated).
- For performance claims, provide measured numbers from a stated environment. Never state benchmark results you have not measured.
- For version-specific behavior, package names, and configuration keys, mark them "verify against current official documentation for the targeted version" unless confirmed in the repository.

Good output example: "Startup fails with an invalid scope error at `BuildServiceProvider` validation. Cause: `OrderRepository` (scoped) is injected into singleton `PricingCache`. Fix: change `PricingCache` to scoped, or inject `IServiceScopeFactory` and create a scope per operation. Verified by running `dotnet test` on the `Startup.Tests` project: passes. Not verified against production configuration."

Bad output example: "This will make the API 40% faster and is GDPR compliant." Both claims are unsupported.

### Failure handling

- If the reproduction is impossible, say so and list the minimum information needed to proceed.
- If the cause is ambiguous, present at most two ranked hypotheses with the evidence that would distinguish them.
- If a fix fails verification, revert to the last known good state and report what changed in the diagnosis.
- If an action touches a decision gate and approval is not given, stop and provide the exact command or change for the approver to review, without executing it.
- Never suppress exceptions with broad catch blocks to make an error disappear. Catch only where the handling is meaningful, and preserve the original exception as the cause.

### Deliverable contract

Every response on this topic ends with:

1. Summary of the finding or change, in two to four sentences.
2. Assumptions stated, including framework version and hosting model.
3. Changes proposed, as file-level or code-level diffs or snippets, each with its purpose.
4. Verification performed, with commands and observed results, and verification still required.
5. Risks and approval items, explicitly listing any decision gate that applies.
6. Rollback steps for any change that alters runtime behavior or configuration.

Keep prose concise. Prefer tables for option comparisons and numbered lists for ordered procedures. Do not claim tests passed unless they were run.


## graphql-api-design

**Use when:** Use when designing, reviewing, or evolving a GraphQL schema, resolver layer, or GraphQL API contract for a backend service, including schema modeling, pagination, error handling, authorization placement, and breaking-change management.

### Purpose and boundaries

Use this skill to produce or review GraphQL schemas and their backend contracts: type modeling, field design, pagination, mutations, error semantics, authorization placement, N+1 prevention, and schema evolution.

In scope: SDL design, resolver responsibilities, DataLoader-style batching, input and mutation design, error modeling, deprecation and evolution policy, and schema checks in CI.

Out of scope: client UI code, database schema migrations, infrastructure sizing, and REST or gRPC design except where a GraphQL field wraps them. Do not use this skill to approve a production schema change without the owning team's review.

### Inputs and assumptions

Collect before designing:
- Consumers: each client application, its primary screens or workflows, and its release cadence.
- Domain entities, their identifiers, ownership boundaries, and existing REST or database shapes.
- Read/write access patterns and expected list sizes.
- Authentication mechanism and the authorization rules per entity.
- Current schema file, if any, and the list of deployed clients that query it.
- Target GraphQL specification and server library. Treat their specific directives, features, and tooling flags as version-sensitive: verify against current official documentation before relying on them.

If any of these are missing, state the assumption explicitly in the deliverable. Do not invent consumer needs.

### Operating workflow

1. **Map the domain.** List entities, relationships, and the queries clients actually run. Model from consumer use cases, not database tables.
2. **Draft types as nouns, operations as verbs.** Use object types for entities, enums for closed sets, and input types for mutation arguments. Prefer `Order.status: OrderStatus` over string fields.
3. **Design identifiers.** Use a single opaque `ID` scalar for global identity. Do not expose internal auto-increment keys as the only identity.
4. **Design connections for every list that can grow.** Use cursor-based connections (`edges`, `node`, `cursor`, `pageInfo`). Plain lists are acceptable only for bounded collections with a documented maximum.
5. **Design mutations as payload-returning operations.** Each mutation takes one input object and returns a payload type containing the changed entity and a `userErrors`-style list (or a typed union, see decision gates).
6. **Place authorization in resolvers or a service layer, never only in the client.** Hide unauthorized fields by returning a defined error, not by omitting fields silently.
7. **Plan batching.** For every object field that loads related data, identify its loader key and batch window. Confirm the resolver does not query per parent item.
8. **Define evolution rules.** Mark fields as deprecated with a reason and replacement before removal. Record the removal date and the consumer sign-off.
9. **Write the contract tests** described under Verification.

### Decision gates

- **Nullable or non-null:** Mark a field non-null only if the server guarantees a value for every object that can be returned. Making a field non-null later is a breaking change for clients that handle null, so default to nullable for fields derived from external services.
- **Expose a field or not:** Expose only fields that at least one named consumer uses or is committed to using. Speculative fields are a schema commitment.
- **Errors as payload fields vs. GraphQL errors:** Use payload-level user errors for validation and business rule failures the client can act on. Reserve top-level GraphQL `errors` for unexpected system failures and authorization failures on whole operations.
- **Union result vs. error list:** Use a union (e.g., `CreateOrderResult = Order | ValidationError`) when the failure shape differs materially from success. Use an error list when a single payload type suffices. Document the choice per mutation.
- **Custom scalars:** Introduce a scalar (e.g., `DateTime`, `Money`) only with a documented serialization format and parsing rule.
- **Breaking change:** Adding a nullable field, optional argument with default, or new enum value that clients can ignore is non-breaking. Removing or renaming fields, changing types, making a nullable field non-null, or changing enum meaning is breaking. Breaking changes require a deprecation cycle and approval from the consuming teams.
- **Depth and complexity limits:** Require a query depth and complexity policy for any public endpoint. Values must be chosen from observed query data, not guessed.

### Verification and evidence

Each deliverable must include:
- **Schema lint** passing against the team's chosen linter, with the rule set named.
- **Schema diff** against the last released schema, classified as breaking or non-breaking, with the diff output attached.
- **N+1 check:** a test or trace showing query count stays constant (or bounded by batch count) as list size grows, for at least the three largest connection fields. Report measured counts, not estimates.
- **Authorization matrix:** a table of entity × role × operation with expected allowed/denied outcome, each backed by a test.
- **Pagination tests:** forward and backward traversal, empty page, last page, and invalid cursor handling.
- **Example operations:** at least one real query per consumer use case, executed against a test environment, with results recorded.

Do not claim performance improvements or compliance properties without measured evidence.

### Failure handling

- If a consumer use case cannot be served without an N+1 pattern, stop and propose a batching or denormalization option with its trade-offs; do not ship the naive resolver.
- If the schema diff shows an unintended breaking change, revert the change and reintroduce it as an additive field with deprecation of the old one.
- If authorization rules are ambiguous for an entity, mark the field as restricted and request a decision from the domain owner. Do not default to allow.
- If the version of the GraphQL specification or server library behaves differently from documented expectations, record the observed behavior and the version, and verify against current official documentation before proceeding.

### Safety and approval controls

Obtain explicit human approval before:
- Removing, renaming, or changing the type of any field or argument in a published schema.
- Deploying a schema change to production or to any environment consumed by external partners.
- Exposing a new field that returns personal, financial, or credential data.
- Changing authorization rules, including loosening them.
- Enabling introspection or disabling depth or complexity limits on a public endpoint.

### Deliverable contract

Return:
1. The SDL for changed or new types, with comments on non-obvious nullability and error decisions.
2. A decision log: each gate applied, the choice made, and the rationale.
3. Schema diff classification (breaking / non-breaking) with the affected consumers.
4. Verification results: lint, N+1 counts, authorization matrix, pagination test outcomes.
5. Open assumptions and items requiring approval, listed explicitly.

Do not include unsupported claims, unverified version-specific behavior presented as fact, or unresolved sample fields.


## grpc-protobuf-services

**Use when:** Use when designing, implementing, reviewing, or evolving gRPC services defined with Protocol Buffers, including .proto schema design, backward-compatibility checks, streaming choices, deadlines, error mapping, and service-to-service contract changes.

### Purpose and boundaries

Use this skill to design and review gRPC APIs and their Protocol Buffers (proto3 unless the project states otherwise) schemas, and to plan safe contract evolution across clients and servers. In scope: message and service design, field numbering, streaming modes, deadlines and cancellation, status code selection, interceptors and metadata conventions, code generation workflow, and wire-compatibility review.

Out of scope: general REST design, database schema work, load-testing results, and infrastructure provisioning (service mesh, load balancer configuration) except where they change contract behavior. Do not produce performance claims without measured data.

### Inputs and assumptions

Collect before proposing changes:
- Existing `.proto` files and the generated-code toolchain in use (name and version from the repository, not memory).
- Consumers: which services and languages call the API, and whether mobile or external clients exist.
- Compatibility requirement: internal-only, versioned public, or frozen.
- Traffic shape: unary, server-streaming, client-streaming, or bidirectional, and expected payload sizes.
- Required semantics: idempotency, ordering, timeout budgets, retry policy.

If any input is missing, state the assumption explicitly in the deliverable. Do not assume a generator plugin, runtime version, or library API; mark such details "verify against current official documentation."

### Operating workflow

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

### Decision gates

- **Gate A: Breaking change?** Any removed or retyped field, changed field number, changed RPC signature, altered meaning of an existing value, or changed streaming mode is breaking. Stop and require explicit owner approval plus a versioned service (new package or new service name) with a migration window.
- **Gate B: External or public exposure?** If the API is reachable by external clients, require approval before publishing schema changes and a deprecation notice for removed behavior.
- **Gate C: Retry safety.** Mutating RPCs without an idempotency key must not be marked retryable. Require an idempotency key field or documented server-side dedupe before enabling client retries.
- **Gate D: Streaming justification.** Bidirectional streaming requires a stated reason (cancellation semantics, flow control, or long-lived push). Otherwise choose unary.
- **Gate E: Sensitive data.** Fields carrying credentials, personal data, or regulated data require approval and must not be logged in debug output or error details. Do not claim regulatory compliance.

### Verification and evidence

- Compatibility: run the repository's configured breaking-change detector if one exists; if none is configured, compare old and new descriptors manually against the rules in step 3 and record each field number checked.
- Generation: regenerate code from a clean checkout; the diff must contain only expected files. Record toolchain versions used.
- Tests: each new or changed RPC has at least one test for success, deadline exceeded, and the documented error codes. Tests must exercise a real serialized round trip, not only in-memory objects.
- Old-client check: decode a payload captured from the previous schema with the new code, and confirm defaults for missing fields.
- Quality thresholds: zero reused field numbers; every removed field reserved; every RPC has a documented deadline recommendation; every error code mapping is listed.

### Failure handling

- If a generator or detector fails, report the exact command output summary and do not hand-edit generated files.
- If compatibility is unclear (for example, a field's semantics changed without a type change), treat it as breaking and escalate to Gate A.
- If a requested behavior conflicts with gRPC status semantics, propose the nearest standard code and explain the mismatch rather than inventing a custom code.
- If evidence is missing (no tests, no toolchain version), mark the deliverable "unverified" and list the blocking items.

### Deliverable contract

Return:
1. Summary of the change and its classification (additive, behavioral, breaking).
2. Full proto diff with reserved ranges shown.
3. Per-RPC table: name, shape, deadline recommendation, idempotency, retry safety, status codes.
4. Compatibility evidence: tool output or manual checklist results.
5. Open items requiring approval, labeled by gate.
6. Toolchain versions used, or an explicit "verify against current official documentation" note for each version-sensitive detail.

Do not proceed with destructive actions such as deleting published proto files, rewriting history, or deploying schema changes to shared environments without explicit approval.


## nodejs-server-runtime

**Use when:** Use when building, debugging, hardening, or operating a Node.js HTTP/API server process, including event loop blocking, memory growth, graceful shutdown, process supervision, configuration, and runtime upgrades.

### Purpose and boundaries

This skill covers the runtime behavior of a Node.js server process: startup and configuration, request concurrency on the event loop, worker and cluster topology, memory and handle lifecycle, signal handling and graceful shutdown, and observability hooks at the process level. It applies to HTTP APIs, background workers that share the same runtime, and long-running services managed by a supervisor.

It does not cover framework-specific routing or ORM design, frontend bundling, or infrastructure provisioning beyond what the process needs to run correctly. Use a separate skill for database schema work or container orchestration policy.

### Inputs and assumptions

Collect before acting:

- Node.js version in use and the target version. Treat release-line support windows and specific flags as version-sensitive; verify against the official Node.js release schedule and documentation for the exact version.
- Entry point, process manager (systemd, PM2, container runtime, or none), and number of instances.
- Symptoms with evidence: latency percentiles, RSS and heap trends, restart counts, error logs, exit codes.
- Whether the environment is production. Assume production unless told otherwise.
- Load profile: request rate, payload sizes, CPU-bound versus I/O-bound work.

If the Node.js version or process manager is unknown, state that conclusions are provisional.

### Operating workflow

1. **Reproduce or locate the signal.** Map each symptom to a measurable metric. Latency tail with flat CPU suggests blocking I/O or queueing; rising heap after load suggests retained references; exit code 1 on deploy suggests startup failure.
2. **Measure the event loop first.** Use built-in event loop delay histograms (`perf_hooks` monitorEventLoopDelay) and CPU profiles taken from a staging or canary instance. Do not attach a profiler to production without approval.
3. **Classify the bottleneck.** Synchronous CPU work (JSON of large payloads, regex backtracking, crypto with sync APIs, large `fs.*Sync` calls) blocks all requests; async leaks (unbounded promise chains, unclosed sockets, timers) grow over time.
4. **Apply the smallest change.** Move CPU work to worker threads or a separate process; replace sync filesystem calls on request paths; bound concurrency with explicit limits; add timeouts to outbound calls.
5. **Harden lifecycle.** Handle `SIGTERM` by stopping new connections, draining in-flight requests within a fixed deadline, closing pools, then exiting. Set `server.keepAliveTimeout` and `headersTimeout` deliberately; confirm current defaults in the official HTTP documentation.
6. **Verify under load** (see Verification).

### Decision gates

- **Use worker threads** when work is CPU-bound and stateless. **Use child processes or a separate service** when isolation or crash containment matters.
- **Increase instance count** only after confirming the bottleneck is per-process CPU, not a shared database or lock.
- **Raise heap limits** only after proving retention is legitimate (cache sized to working set). Otherwise fix the leak.
- **Change Node.js version** only with a canary, a rollback plan, and a changelog review for breaking changes in the target line.
- **Enable new runtime flags** only after verifying their exact names and behavior in current official docs for your version.

### Verification and evidence

Each change requires before-and-after evidence:

- Event loop delay p99 reduced or unchanged; no new blocking spans in CPU profile.
- Heap after forced GC (run under a diagnostic flag only in staging) returns to baseline within two load cycles.
- Shutdown test: send `SIGTERM` under load; zero requests dropped that were accepted before the signal; process exits before the configured deadline; no unhandled rejections in logs.
- Load test at 1.2x expected peak with error rate under the agreed threshold.
- Startup test: process reports ready only after configuration validation and dependency connections succeed.

Record the Node.js version, flags, instance count, and load parameters with every result.

### Failure handling

- If a metric regresses after a change, revert first, then investigate.
- If a memory profile is inconclusive, collect two heap snapshots separated by a steady load window before drawing conclusions.
- If shutdown exceeds the deadline, force exit with a logged reason; do not leave the process hanging.
- If `uncaughtException` or `unhandledRejection` occurs, log with context and exit; do not continue serving on corrupted state.

### Deliverable contract

Produce:

1. Diagnosis: symptom, metric evidence, classified bottleneck.
2. Change set: exact file-level edits, with rationale for each.
3. Verification results: numbers before and after, test conditions, Node.js version.
4. Rollback steps.
5. Open risks and items requiring version confirmation against official documentation.

Do not:

- Restart, kill, or redeploy production processes, or alter live configuration, without explicit approval.
- Run heap snapshots, CPU profiles, or debug inspectors on production without explicit approval, since they pause or slow the process.
- Invent flag names, API signatures, or version numbers; mark uncertain items for verification.
- Claim performance gains or compliance properties without measured evidence.
- Suppress errors with empty catch blocks or disable TLS verification to clear failures.

Require explicit human approval before any action that is destructive, irreversible, externally visible (traffic shifting, customer-facing config, third-party calls with side effects), or touches sensitive data such as credentials, tokens, or personal data in logs.


## python-web-frameworks

**Use when:** Use when choosing, structuring, building, or reviewing a Python web backend on frameworks such as Django, Flask, FastAPI, or Starlette, including routing, request handling, data access boundaries, configuration, and deployment readiness.

### Purpose and boundaries

This skill guides professional work on server-side Python web applications and APIs: framework selection, project layout, request lifecycle design, persistence boundaries, authentication wiring, error handling, testing, and production readiness.

In scope: HTTP services, server-rendered sites, JSON APIs, and background-task integration points.
Out of scope: frontend build tooling, infrastructure provisioning beyond application configuration, model training, and general Python language instruction.

### Inputs and assumptions

Collect before recommending anything:

- Workload: request volume, latency targets, long-running work, streaming, WebSocket needs.
- Team: existing framework expertise, hiring constraints, maintenance horizon.
- Data: database engine, schema ownership, migration history, existing ORM.
- Constraints: deployment target, Python version policy, compliance obligations, existing auth provider.
- Existing code: repository, lockfile, framework version actually installed.

If the installed framework version is unknown, treat version-specific behavior as unverified. Do not assume a feature exists in a given release.

### Operating workflow

1. Read the lockfile or dependency manifest and record exact framework and server versions.
2. Map the request path: entry point, middleware or dependency chain, handler, data access, response serialization.
3. Identify the framework's native mechanisms for routing, validation, dependency injection, sessions or auth, and migrations. Use them rather than reimplementing them.
4. Separate concerns: HTTP layer handles parsing and status codes; service layer holds business rules; repository or ORM layer owns queries. Handlers must not contain raw SQL composed from request input.
5. Define configuration through environment variables or the framework's settings mechanism, with secrets read at runtime and never committed.
6. Write or update tests at the handler, service, and data layers before changing behavior.
7. Run the application under the production-intended server configuration, not only the development server.

### Decision gates

Framework selection:
- Admin panels, auth, and ORM-integrated CRUD with a large team: Django is usually the fit.
- Small services, server-rendered pages, or extensions-driven apps: Flask.
- Typed JSON APIs with automatic schema documentation and async I/O: FastAPI.
- Minimal ASGI toolkit where you want to assemble components yourself: Starlette.
- Record the reason in the design note. "Popular" is not a reason.

Sync versus async:
- Use async handlers only when I/O dominates and all libraries in the call path are async-safe. A blocking call inside an async handler stalls the event loop; move it to a thread pool or a worker.

Background work:
- Offload anything exceeding the request latency budget to a task queue. Do not spawn unmanaged threads or processes inside request handlers.

Schema changes:
- Require a reversible migration plus a rollback note. Stop if the migration drops or rewrites data.

### Verification and evidence

Accept a change only when all of these hold:

- Test suite passes on the pinned Python and framework versions.
- Each endpoint has tests for success, validation failure, authorization failure, and not-found behavior, with asserted status codes and response shapes.
- Static analysis and type checks, where the project already uses them, report no new findings.
- Requests that touch the database are checked for query count against an expected bound on a representative fixture.
- Load or latency claims are backed by a measured run with recorded hardware, concurrency, and percentiles. Without measurement, state that performance is unverified.
- Security-relevant settings (debug mode off, allowed hosts or origins restricted, cookies marked secure and HTTP-only where applicable, CSRF protection active for session-authenticated forms) are confirmed from the effective runtime configuration, not from source defaults.

Cite the official documentation section for any framework-specific setting you rely on, and mark it for re-verification against the installed version.

### Failure handling

- Failing tests: fix the cause; do not weaken assertions or skip tests.
- Unknown framework behavior: consult the official documentation for the pinned version. If unavailable, report the uncertainty instead of guessing.
- Migration conflicts: stop, report the conflicting revisions, and wait for direction.
- Performance regressions: revert to the last measured baseline before tuning.

### Deliverable contract

Each deliverable includes:

1. A short design note: chosen framework and version, reasons, layer boundaries, and known limits.
2. The code change with tests.
3. A verification table: check name, command or method, result, and date.
4. A list of unverified items, each with the reason and the verification step needed.
5. Any migration, configuration, or rollback instructions.

### Approval requirements

Obtain explicit approval before any of the following:

- Dropping, truncating, or rewriting production data, or running irreversible migrations.
- Changing authentication, authorization, session, or secret-handling behavior.
- Deploying, rotating credentials, altering DNS, or changing externally visible endpoints or API contracts.
- Sending requests to third-party or production systems during testing.
- Adding dependencies that change licensing, runtime footprint, or security posture.

### What not to do

- Do not invent framework APIs, settings names, command-line flags, package versions, or benchmark figures.
- Do not run the development server as evidence of production behavior.
- Do not disable CSRF, CORS, or host validation to make a request succeed.
- Do not store secrets in source, fixtures, or logs.
- Do not put business logic in templates, serializers, or route decorators beyond thin delegation.
- Do not claim compliance or security guarantees; report which controls were verified and which were not.

### Ultron routing contract

**Choose this skill when:** the target service is written in Python and the task concerns a Python web framework, application layout, request lifecycle, async behavior, persistence boundary, authentication wiring, error handling, testing, or production readiness.

**Choose `backend-web-frameworks` when:** the framework decision or server architecture is language-neutral, the target language is not yet selected, or the task spans several backend stacks.

**Handoff contract:** receive the required backend behavior, traffic and latency constraints, identity/data boundaries, and runtime target. Return the Python-specific framework/version choice, application structure, concurrency model, integration contracts, and runnable verification evidence. Do not present Python framework conventions as universal backend rules.

**Why the boundary exists:** this skill supplies language-specific implementation expertise while preserving a common backend architecture vocabulary.


## rest-api-design-security

**Use when:** Use when designing, reviewing, or hardening REST API endpoints for authentication, authorization, input validation, rate limiting, data exposure, or transport security before implementation or release.

### Purpose and boundaries

This skill covers the security design of HTTP/JSON REST APIs: resource modeling as it affects access control, authentication and authorization, input validation, response shaping, error handling, rate limiting, transport configuration, and logging of API traffic.

It does not cover: GraphQL or gRPC specifics, front-end XSS, infrastructure hardening beyond the API boundary, cryptographic protocol design, or formal compliance certification. Where a finding touches those areas, record it and hand it off.

### Inputs and assumptions

Collect before reviewing:
- Endpoint inventory: method, path, request and response schemas, and caller type (end user, service, partner, public).
- Authentication mechanism in use or proposed (session, bearer token, API key, mutual TLS, OAuth 2.x flows).
- Data classification for each resource (public, internal, personal, financial, credentials).
- Existing gateway, WAF, or rate-limit configuration, if any.
- Deployment topology: which endpoints are internet-facing.

Assumptions must be stated explicitly in the deliverable. If an input is missing, mark the affected checks as "not verified" rather than passing them.

### Operating workflow

1. **Map trust boundaries.** List each entry point and the identity it accepts. Flag any endpoint callable without authentication.
2. **Enumerate resources and actions.** For every endpoint, record the object it reads or mutates and the owner relationship (user, tenant, organization).
3. **Check authorization per object.** For each endpoint that accepts an identifier, confirm the server verifies that the authenticated principal may access that specific object, not just the route. Test for broken object-level authorization by substituting identifiers belonging to other principals.
4. **Check authorization per function.** Confirm administrative and privileged operations require a distinct role or scope, and that role fields cannot be set by the client.
5. **Validate input.** Verify schema-level validation: types, lengths, enumerations, ranges, and maximum body size. Reject unknown fields on write endpoints unless explicitly allowed. Check that path, query, and header values are validated and never interpolated into queries, shell commands, or file paths.
6. **Shape responses.** Confirm responses return only fields the caller needs. Flag fields such as password hashes, internal IDs of other tenants, stack traces, internal hostnames, and full database records.
7. **Review errors.** Errors must not disclose whether a resource exists to unauthorized callers. Use consistent status codes for authentication failure and for not-found-or-forbidden cases where existence is sensitive.
8. **Check rate limiting and abuse controls.** Identify endpoints for login, password reset, token issuance, search, file upload, and expensive queries. Each needs a documented limit keyed to an appropriate identity (account, token, IP with caveats).
9. **Check transport and token handling.** Confirm TLS for all endpoints, tokens not placed in URLs, secure cookie attributes where cookies are used, and short token lifetimes with a revocation path.
10. **Check logging.** Logs must record authentication events and authorization denials with correlation IDs, and must not record secrets, tokens, or full request bodies containing personal data.

### Decision gates

- **Gate A (authentication):** If any state-changing or data-returning endpoint lacks authentication, stop and require an explicit justification signed off by the owner before proceeding.
- **Gate B (object access):** If an identifier-based endpoint does not verify ownership or tenancy, classify as high severity. Do not accept a "the UI prevents it" argument.
- **Gate C (sensitive change):** Changes to authentication flows, token signing, key management, CORS policy on credentialed routes, or public exposure of an internal endpoint require explicit approval from the system owner before implementation or deployment.
- **Gate D (testing against live systems):** Do not send attack traffic, fuzzing, or credential-guessing tests against production or third-party systems without written approval naming the target, window, and rate limit.
- **Gate E (data handling):** Do not copy real personal or credential data into test artifacts, tickets, or reports. Use redacted or synthetic samples.

### Verification and evidence

For each finding, record:
- Endpoint, method, and affected parameter.
- Reproduction steps using a test account pair (principal A owns object X; principal B attempts access).
- Observed status code and response excerpt with sensitive values redacted.
- Expected behavior and the rule violated.

Quality checks before closing a review:
- 100% of endpoints in the inventory have an authentication classification and an authorization rule recorded.
- Every identifier-accepting endpoint has at least one cross-principal test result.
- Every write endpoint has a documented schema with rejection of unknown fields, or a recorded exception.
- Rate-limit values for authentication endpoints are documented and tested for a lockout or throttle response.
- No secret, token, or personal data appears in the deliverable.

Version-sensitive items (framework middleware names, OAuth grant availability, TLS version defaults, header recommendations, library behavior) must be marked "verify against current official documentation" and must not be stated as fact from memory.

### Failure handling

- If a test environment is unavailable, perform static review of the schemas and code paths, and label every finding as "static, unconfirmed."
- If reproduction is ambiguous, report the uncertainty and the next test needed; do not upgrade severity or downgrade it without evidence.
- If a fix would break a known client, propose a versioned migration with a deprecation window rather than an in-place breaking change, and request approval (Gate C).
- If you discover an active exploitation indicator or exposed secret, stop, do not attempt further probing, and escalate to the system owner immediately.

### Deliverable contract

Produce a single report containing:
1. Scope, assumptions, and inputs received, with missing inputs listed.
2. Endpoint inventory table: endpoint, auth requirement, object scope, rate limit, sensitivity.
3. Findings ordered by severity, each with evidence fields above, a rule reference, and a concrete remediation.
4. Approval requests raised under the decision gates, with status.
5. Verification status for each quality check: passed, failed, or not verified, with reason.
6. Version-sensitive items flagged for documentation verification.

Do not: approve a design on partial inventory; use live third-party systems for testing; propose security through obscurity (hidden routes, unguessable paths) as the control; state that an API is "secure" or "compliant" as a conclusion; or omit negative results.

### Ultron routing contract

**Choose this skill when:** the task is to secure or review an existing HTTP/JSON REST API boundary, especially resource authorization, authentication, validation, response exposure, error behavior, rate limits, transport, and API-specific logging.

**Choose api-design-security-and-app-scaffolding when:** the work starts with a new API or requires a complete API contract plus an application skeleton that implements it.

**Handoff contract:** return endpoint/resource findings, abuse cases, authorization and validation requirements, safe response rules, rate-limit policy, and negative security tests. The scaffold skill owns implementation of any required new application structure; this skill independently verifies the resulting API boundary.

**Why the boundary exists:** a secure REST API review should not silently become a full application scaffolding project, and a scaffold generator should not be treated as independent security assurance.


## sdk-and-api-docs

**Use when:** Use when writing, reviewing, or restructuring documentation for an SDK, public API, or developer-facing library, including reference docs, quickstarts, error catalogs, migration guides, and code samples.

### Purpose and boundaries

This skill produces and audits developer documentation for SDKs, HTTP/RPC APIs, CLIs exposed to developers, and client libraries. It covers: conceptual overviews, authentication setup, quickstarts, endpoint or method reference, parameter and response schemas, error catalogs, pagination and rate-limit guidance, versioning and deprecation notices, migration guides, and runnable code samples.

Out of scope: end-user product help, marketing copy, internal engineering runbooks, and changes to the API or SDK behavior itself. If documentation reveals a behavior bug, report it; do not document the bug as intended behavior.

### Inputs and assumptions

Before writing, collect:

1. The source of truth: OpenAPI/API schema, SDK source, type definitions, changelog, or test suite. Prefer generated reference from schema where the project already does so.
2. Target audience and skill level (for example, backend integrator versus mobile developer).
3. The exact version(s) documented. Each page must state which version it describes.
4. Supported languages, runtimes, and minimum platform versions.
5. Existing doc structure, style guide, and terminology glossary.

Assumptions must be written down explicitly. If a fact cannot be traced to a source, mark it `UNVERIFIED` and list it in the handoff note. Do not infer parameter types, defaults, limits, or error codes from naming conventions.

### Operating workflow

1. **Map the surface.** List every public operation, class, method, option, and error. Diff against the previous documented version if one exists.
2. **Classify each item** as stable, beta, experimental, or deprecated, using the project's own labels. Note the removal target for deprecated items if one is published.
3. **Write the concept layer first:** what the resource or client does, its object model, and the lifecycle of key objects (for example, created, pending, completed, failed).
4. **Write the auth and setup section** with the minimum steps to make one successful call. Show where credentials are obtained and where they must never be placed (client-side bundles, logs, version control).
5. **Write one quickstart** that completes end to end, then reference pages for each operation: purpose, parameters (name, type, required, default, constraints), request example, response example, errors, and idempotency or side-effect notes.
6. **Write the error catalog:** each error code or exception class, its HTTP status or type, cause, whether retry is safe, and the recommended client action.
7. **Write cross-cutting guidance:** pagination, rate limits, timeouts, retries with backoff, webhooks or event verification, and rate-limit headers as documented by the source.
8. **Write the migration guide** for any breaking change: old form, new form, one before/after example per change, and a removal date only if confirmed.
9. **Run the verification pass** (below) and produce the deliverable.

### Decision gates

- **Schema vs. handwritten:** If an OpenAPI or typed spec exists and is current, generate reference sections from it and hand-write only concepts and guides. If the spec disagrees with the implementation, stop and escalate; do not publish either version as correct.
- **Sample code:** Include a sample only if it has been executed against the documented version, or the project's test suite exercises the same call. Otherwise label it "illustrative, not executed."
- **Behavior ambiguity:** If a default, limit, or ordering rule is not stated in source, mark `UNVERIFIED` and request confirmation from the owning team. Never publish a guessed value.
- **Version-sensitive details** (package names, minimum runtime versions, flag names, endpoint paths, rate limits): add a note "verify against current official documentation for version X" unless the value is pulled directly from the versioned source.
- **Breaking change publication:** Requires explicit owner approval before the migration guide and deprecation notice are published, because they shape customer behavior and commitments.
- **Publishing or overwriting live docs:** Requires explicit approval. Drafts go to a review branch or staging location.

### Verification and evidence

- Every parameter, response field, and error code in the reference traces to a schema, type, or test. Record the source path for each section in the review notes.
- Run every quickstart and runnable sample against the documented version in a sandbox or test environment. Record command, version, and result.
- Link-check all internal and external references. Zero broken links is the pass bar.
- Check that every required parameter in the reference is marked required in the source. Mismatches count as defects.
- Confirm terminology is consistent: one term per concept across all pages (a glossary term list helps).
- Confirm each page states its version and last-verified date.
- Measurable target: 100% of documented operations have a reference entry; 100% of error codes in the catalog are reachable or marked as reserved; 0 samples that fail execution in the documented environment.

### Failure handling

- **Source and implementation disagree:** Stop, document the discrepancy with both sources cited, and escalate to the API owner. Do not publish a reconciled guess.
- **Sample fails:** Record the exact error and environment. Fix the sample if the doc is wrong; file a defect if the API is wrong. Remove or label the sample if the fix is not available before release.
- **Missing information from owners:** Leave the `UNVERIFIED` marker in place, list open questions in the handoff, and do not fill gaps with plausible defaults.
- **Conflicting versions in one page:** Split into version-specific pages or add an explicit version selector. Do not mix behaviors in one table.

### Deliverable contract

Return:

1. The documentation files (Markdown) for the requested scope, organized by the section structure above.
2. A review note containing: source references per section, sample execution log summary, list of `UNVERIFIED` items with owners, list of version-sensitive values flagged for verification, and open questions.
3. A change summary for any updated page: what changed, why, and whether it affects existing customers.

Do not:
- Invent endpoint names, parameters, error codes, package versions, flags, rate limits, or latency or benchmark figures.
- State compliance, security certification, or uptime guarantees the source does not state.
- Publish or overwrite live documentation, or announce deprecations, without explicit approval.
- Embed real credentials, tokens, or customer data in samples; use clearly fake placeholders such as `YOUR_API_KEY` and note where to supply them.
- Document internal-only endpoints or undocumented behavior as public API.


## wordpress-rest-api

**Use when:** Use when designing, building, debugging, or securing custom endpoints, consuming, or auditing the WordPress REST API (wp-json routes, controllers, schemas, authentication, and permission callbacks) in a theme or plugin.

### Purpose and boundaries

This skill covers work against the WordPress REST API: registering routes with `register_rest_route`, extending core resources, validating and sanitizing input, enforcing permissions, shaping responses, and consuming endpoints from external clients or server-side code.

In scope: custom plugin/theme endpoints, extending core post types or meta exposure, authentication choices (cookie with nonce, application passwords, OAuth-based plugins), error shapes, pagination, and performance of list endpoints.

Out of scope: front-end block editor internals, WooCommerce-specific REST namespaces beyond general patterns, hosting configuration, and legal or compliance certification of any data flow.

### Inputs and assumptions

Collect before writing code:

- WordPress core version and PHP version. Treat all REST behaviour details as version-sensitive; verify against the current official Developer Handbook for the target release.
- Whether the consumer is browser JavaScript (same origin), a server-to-server client, or a mobile/third-party app.
- Resource type: core object, custom post type, taxonomy, user, options, or non-WordPress data.
- Required operations (read, create, update, delete) and data sensitivity.
- Existing namespace conventions. Use a vendor-specific namespace such as `acme/v1`; never reuse `wp/v2`.

Assume nothing about auth state. Assume production traffic and multisite is possible unless stated otherwise.

### Operating workflow

1. **Map the contract first.** Write the route list: method, path, arguments, response shape, and required capability for each. Get this reviewed before implementation.
2. **Register routes on `rest_api_init`**, never earlier. Call `register_rest_route` with an explicit `methods` value, a `permission_callback` on every route (never omit it; a missing callback triggers a deprecation notice and is a security defect), and an `args` array.
3. **Declare argument schemas.** For each argument set `type`, `required`, `sanitize_callback`, and `validate_callback` or `enum`. Use `sanitize_text_field`, `absint`, `sanitize_key`, or `wp_kses_post` as appropriate to the field.
4. **Implement permission callbacks** using capability checks such as `current_user_can( 'edit_post', $id )` against the specific object, not a blanket `is_user_logged_in()`.
5. **Build responses** with `WP_REST_Response` or return arrays/`WP_Error`. Return only fields the consumer needs; never expose password hashes, internal meta keys, or unfiltered `$wpdb` rows.
6. **Paginate every collection.** Accept `per_page` (cap at 100) and `page`; return `X-WP-Total` and `X-WP-TotalPages` headers.
7. **Expose meta deliberately.** Use `register_post_meta` with `show_in_rest` and an explicit `auth_callback`. Do not set `show_in_rest` on sensitive keys.
8. **Verify** using the checklist below before handing over.

### Decision gates

- **Authentication choice.** Cookie auth plus `X-WP-Nonce` (`wp_rest` action) only for same-origin logged-in browser requests. Application passwords for trusted server-to-server integrations over HTTPS. Anything requiring third-party delegated access: use a vetted OAuth implementation and confirm current support with its documentation.
- **Write operations.** Any endpoint that deletes, overwrites, changes roles, sends email, charges money, or calls an external service requires explicit user approval of the route design and a rollback path before deployment.
- **Public read endpoints.** Allowed only for data already public on the site. Confirm with the data owner.
- **Schema expansion.** Adding fields to core responses via `register_rest_field` or filters is a breaking-change risk for consumers; require a version bump in the namespace for removals or type changes.
- **Heavy queries.** If a list endpoint would exceed roughly 500 ms on realistic data, stop and redesign: add indexed filters, caching, or a dedicated table.

### Verification and evidence

Run and record:

- `curl` or HTTP client requests for each route, showing status codes for: anonymous, under-privileged, authorized, and malformed input. Expected: 401/403 for denied, 400 for invalid arguments, 200/201 for success.
- A check that every registered route has a non-empty `permission_callback` (grep the codebase; no route may lack one).
- Confirmation that unauthenticated `OPTIONS` and `GET` responses contain no fields marked sensitive.
- Pagination test: request page boundaries and verify header totals match a direct query count.
- Response schema comparison against the documented contract, field by field.
- Logs or query monitor output showing no N+1 query pattern on list endpoints (target: query count does not grow linearly with item count).
- Confirm version-sensitive behaviour (argument handling, auth defaults) against the current official documentation and cite the page reviewed.

### Failure handling

- **400 unexpected on valid input:** check `required` and type coercion; numeric strings and booleans are commonly mishandled.
- **403 for admins:** the capability check is on the wrong object or context; test with the exact role.
- **Nonce failures (403 `rest_cookie_invalid_nonce`):** the nonce is stale, missing, or sent for a different action. Re-issue via `wp_create_nonce( 'wp_rest' )` in the rendering context.
- **Route not found:** `rest_api_init` ran too late, the namespace or path has a typo, or permalinks/rewrite rules need flushing after activation. Flush only on activation or after explicit approval.
- **Caching layer serving stale or private responses:** exclude `wp-json` from page caching and never cache authenticated responses publicly.
- If a fix requires changing a published contract, stop and present options to the owner.

### Deliverable contract

Provide:

1. Route contract table: method, path, auth, arguments, response fields, capability.
2. Complete PHP for the registration and callbacks, with no placeholders.
3. Verification log: request/response pairs and results for each checklist item.
4. List of version-sensitive assumptions with the documentation page used to confirm them.
5. Known limitations and any operations awaiting approval.

Do not: expose `show_in_rest` on credentials or personal data without review; use `__return_true` as a permission callback on write routes; disable SSL verification in client code; hardcode secrets in source; or claim compliance with any regulation based on this work.

### Contract evolution and consumer safety (v1.1)

#### Treat the route schema as a public interface

Maintain a route inventory containing namespace/version, method, path, argument schema, permission rule, response schema, pagination behavior, and side effects. Compare the proposed contract with the deployed contract before release. Classify changes as additive, behavior-changing, or breaking. Adding an optional response field is usually additive only if consumers tolerate unknown fields; changing nullability, enum values, ordering guarantees, defaults, or error semantics may still break clients.

Do not assume a namespace version alone makes an incompatible change safe. Keep old consumers working during a migration window when practical, publish a deprecation date, measure old-version usage, and remove the old route only after owner approval and evidence that supported clients have migrated.

#### Test authorization as a matrix

For each route, test anonymous access, authenticated users with no relevant capability, users with the capability on a different object, users with the capability on the target object, and administrators where applicable. Include multisite roles and object ownership rules if the site uses them. A successful test by an administrator does not prove that the permission callback is correctly scoped.

For write routes, test cross-user object IDs, unexpected fields, empty and oversized values, duplicate submissions, stale updates, and repeated DELETE/POST requests. Verify denied requests leave persistent state unchanged. Use disposable fixtures and a test database; never probe production data to establish authorization behavior.

#### Make list endpoints predictable

Define stable ordering with a deterministic tie-breaker, document maximum page size, and reject or normalize invalid pagination values consistently. If clients need cursor pagination, define the cursor from stable sort keys and bind it to the filter set; do not use an offset cursor while rows can change in ways that cause silent skips. Add query-count and response-size checks for representative data volumes.

#### Idempotency and concurrency

For operations that may be retried by mobile clients, queues, or gateways, define whether repeated requests are safe. Where a repeated request could create duplicate records or trigger repeated external side effects, use a client idempotency key with bounded retention and bind it to the authenticated principal and normalized request body. For updates, use version checks or conditional requests where lost updates matter. A request that times out after a side effect must be reconciled before it is retried.

#### API release checklist

- Diff the intended schema against the last released contract.
- Verify every method has an explicit permission callback and least-privilege object check.
- Confirm response fields do not disclose private meta, internal identifiers, or secrets.
- Run compatibility tests against at least one existing consumer fixture.
- Verify pagination order, bounds, and totals on realistic fixtures.
- Confirm retry behavior for every write operation and external side effect.
- Record route version, deprecation plan, and rollback/reconciliation steps.

### Ultron routing contract

**Choose this skill when:** designing or changing WordPress REST route behavior, endpoint schemas, authentication, permission callbacks, response compatibility, pagination, or REST consumer integration.

**Choose wordpress-quality-tooling when:** configuring or operating linters, static analysis, PHPUnit/integration/E2E tests, or CI quality gates for a WordPress codebase. That skill owns test-toolchain setup; this skill owns what the REST API must do and the route-specific contract cases that should be tested.

**Handoff contract:** give the quality-tooling skill the route inventory, expected authorization matrix, representative fixtures, schema compatibility cases, and commands or environments needed to run tests. Receive reproducible test results and CI evidence; do not treat a green generic lint job as proof that endpoint authorization or contract behavior is correct.

**Why the boundary exists:** API design defines behavioral and security expectations; quality tooling provides repeatable mechanisms to test them. Separating the contract from the test runner prevents tool configuration from becoming a substitute for API correctness.

