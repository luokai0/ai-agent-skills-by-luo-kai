---
name: dotnet-web-and-enterprise
description: Use when designing, building, reviewing, or debugging ASP.NET Core web applications, APIs, background services, or enterprise .NET systems involving dependency injection, middleware, authentication, data access, configuration, hosting, or deployment.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Dotnet Web And Enterprise

## Purpose and boundaries

This skill guides work on server-side .NET systems: ASP.NET Core web apps and HTTP APIs, hosted background workers, dependency injection composition, middleware pipelines, authentication and authorization, configuration and options, data access layers, logging and observability, and deployment to containers or managed hosts.

In scope: architecture review, implementation guidance, troubleshooting request and startup failures, performance and reliability reasoning, and migration planning between .NET versions.

Out of scope: desktop UI frameworks, mobile, game engines, and legal or certification claims about compliance. Do not assert that a design satisfies a regulation, standard, or audit requirement; describe controls and recommend review by the responsible party.

## Inputs and assumptions

Before advising, establish:

1. Target framework and SDK version (for example, the TFM in the project file and the output of the SDK version command).
2. Hosting model: IIS, Kestrel behind a reverse proxy, containers, serverless, or Windows services.
3. Data stores, their engines and versions, and whether migrations are already in use.
4. Identity provider and token format, if authentication is involved.
5. Traffic shape, latency targets, and whether the workload is stateless.
6. Existing conventions: solution layout, logging library, error contract, and test frameworks.

If any item is unknown, state the assumption explicitly in your output. Do not guess framework behavior for a version you have not confirmed.

## Operating workflow

1. Reproduce or read the evidence first. Obtain the exception text, stack trace, failing request, configuration section, or relevant log lines before proposing changes.
2. Map the request or startup path. Identify the host builder steps, registered services and their lifetimes, the middleware order, and the endpoint or controller that runs.
3. Classify the problem: composition (DI resolution, lifetime mismatch), pipeline (middleware order, short-circuiting), configuration (binding, environment overrides, secrets sourcing), data (query shape, connection scope, transactions), or runtime (threads, timeouts, cancellation).
4. Propose the smallest change that addresses the classified cause. Prefer framework-provided mechanisms over custom infrastructure.
5. Specify how the change is verified (Section below) and what rollback looks like.

## Decision gates

Stop and request explicit approval before any of the following:

- Running database migrations, schema drops, data deletion, or bulk updates against any environment other than a disposable local one.
- Changing authentication, authorization policies, token lifetimes, CORS origins, or certificate handling in a shared environment.
- Rotating, printing, or committing secrets, connection strings, or keys.
- Deploying, scaling, or altering production routing, DNS, or load balancer configuration.
- Calling third-party or externally visible APIs with real credentials or real customer data.
- Disabling security middleware, validation, or rate limits, even temporarily.

Proceed without approval only for read-only analysis, local code changes, and local test runs that touch no real data.

Choose lifetimes deliberately: a singleton must not capture scoped or transient services that hold request state or database contexts. If a design requires that capture, stop and redesign.

## Verification and evidence

- Build with warnings treated as review items, not ignored. Report the exact command and result.
- Run the relevant automated tests. For startup problems, validate the host builder in a test that resolves required services and fails fast on invalid scopes where the framework supports validation options; confirm the option names against current documentation.
- For API changes, verify status codes, response shapes, and error contracts with integration tests against the real pipeline (in-memory test hosts are acceptable when the data layer is isolated).
- For performance claims, provide measured numbers from a stated environment. Never state benchmark results you have not measured.
- For version-specific behavior, package names, and configuration keys, mark them "verify against current official documentation for the targeted version" unless confirmed in the repository.

Good output example: "Startup fails with an invalid scope error at `BuildServiceProvider` validation. Cause: `OrderRepository` (scoped) is injected into singleton `PricingCache`. Fix: change `PricingCache` to scoped, or inject `IServiceScopeFactory` and create a scope per operation. Verified by running `dotnet test` on the `Startup.Tests` project: passes. Not verified against production configuration."

Bad output example: "This will make the API 40% faster and is GDPR compliant." Both claims are unsupported.

## Failure handling

- If the reproduction is impossible, say so and list the minimum information needed to proceed.
- If the cause is ambiguous, present at most two ranked hypotheses with the evidence that would distinguish them.
- If a fix fails verification, revert to the last known good state and report what changed in the diagnosis.
- If an action touches a decision gate and approval is not given, stop and provide the exact command or change for the approver to review, without executing it.
- Never suppress exceptions with broad catch blocks to make an error disappear. Catch only where the handling is meaningful, and preserve the original exception as the cause.

## Deliverable contract

Every response on this topic ends with:

1. Summary of the finding or change, in two to four sentences.
2. Assumptions stated, including framework version and hosting model.
3. Changes proposed, as file-level or code-level diffs or snippets, each with its purpose.
4. Verification performed, with commands and observed results, and verification still required.
5. Risks and approval items, explicitly listing any decision gate that applies.
6. Rollback steps for any change that alters runtime behavior or configuration.

Keep prose concise. Prefer tables for option comparisons and numbered lists for ordered procedures. Do not claim tests passed unless they were run.