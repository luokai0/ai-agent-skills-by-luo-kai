---
name: python-web-frameworks
description: Use when choosing, structuring, building, or reviewing a Python web backend on frameworks such as Django, Flask, FastAPI, or Starlette, including routing, request handling, data access boundaries, configuration, and deployment readiness.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Python Web Frameworks

## Purpose and boundaries

This skill guides professional work on server-side Python web applications and APIs: framework selection, project layout, request lifecycle design, persistence boundaries, authentication wiring, error handling, testing, and production readiness.

In scope: HTTP services, server-rendered sites, JSON APIs, and background-task integration points.
Out of scope: frontend build tooling, infrastructure provisioning beyond application configuration, model training, and general Python language instruction.

## Inputs and assumptions

Collect before recommending anything:

- Workload: request volume, latency targets, long-running work, streaming, WebSocket needs.
- Team: existing framework expertise, hiring constraints, maintenance horizon.
- Data: database engine, schema ownership, migration history, existing ORM.
- Constraints: deployment target, Python version policy, compliance obligations, existing auth provider.
- Existing code: repository, lockfile, framework version actually installed.

If the installed framework version is unknown, treat version-specific behavior as unverified. Do not assume a feature exists in a given release.

## Operating workflow

1. Read the lockfile or dependency manifest and record exact framework and server versions.
2. Map the request path: entry point, middleware or dependency chain, handler, data access, response serialization.
3. Identify the framework's native mechanisms for routing, validation, dependency injection, sessions or auth, and migrations. Use them rather than reimplementing them.
4. Separate concerns: HTTP layer handles parsing and status codes; service layer holds business rules; repository or ORM layer owns queries. Handlers must not contain raw SQL composed from request input.
5. Define configuration through environment variables or the framework's settings mechanism, with secrets read at runtime and never committed.
6. Write or update tests at the handler, service, and data layers before changing behavior.
7. Run the application under the production-intended server configuration, not only the development server.

## Decision gates

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

## Verification and evidence

Accept a change only when all of these hold:

- Test suite passes on the pinned Python and framework versions.
- Each endpoint has tests for success, validation failure, authorization failure, and not-found behavior, with asserted status codes and response shapes.
- Static analysis and type checks, where the project already uses them, report no new findings.
- Requests that touch the database are checked for query count against an expected bound on a representative fixture.
- Load or latency claims are backed by a measured run with recorded hardware, concurrency, and percentiles. Without measurement, state that performance is unverified.
- Security-relevant settings (debug mode off, allowed hosts or origins restricted, cookies marked secure and HTTP-only where applicable, CSRF protection active for session-authenticated forms) are confirmed from the effective runtime configuration, not from source defaults.

Cite the official documentation section for any framework-specific setting you rely on, and mark it for re-verification against the installed version.

## Failure handling

- Failing tests: fix the cause; do not weaken assertions or skip tests.
- Unknown framework behavior: consult the official documentation for the pinned version. If unavailable, report the uncertainty instead of guessing.
- Migration conflicts: stop, report the conflicting revisions, and wait for direction.
- Performance regressions: revert to the last measured baseline before tuning.

## Deliverable contract

Each deliverable includes:

1. A short design note: chosen framework and version, reasons, layer boundaries, and known limits.
2. The code change with tests.
3. A verification table: check name, command or method, result, and date.
4. A list of unverified items, each with the reason and the verification step needed.
5. Any migration, configuration, or rollback instructions.

## Approval requirements

Obtain explicit approval before any of the following:

- Dropping, truncating, or rewriting production data, or running irreversible migrations.
- Changing authentication, authorization, session, or secret-handling behavior.
- Deploying, rotating credentials, altering DNS, or changing externally visible endpoints or API contracts.
- Sending requests to third-party or production systems during testing.
- Adding dependencies that change licensing, runtime footprint, or security posture.

## What not to do

- Do not invent framework APIs, settings names, command-line flags, package versions, or benchmark figures.
- Do not run the development server as evidence of production behavior.
- Do not disable CSRF, CORS, or host validation to make a request succeed.
- Do not store secrets in source, fixtures, or logs.
- Do not put business logic in templates, serializers, or route decorators beyond thin delegation.
- Do not claim compliance or security guarantees; report which controls were verified and which were not.