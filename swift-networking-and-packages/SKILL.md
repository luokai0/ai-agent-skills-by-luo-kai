---
name: swift-networking-and-packages
description: Use when designing, reviewing, or debugging Swift networking layers (URLSession, async/await requests, decoding, auth, retries, caching) or managing Swift Package Manager dependencies for iOS, macOS, or server-side Swift projects.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Swift Networking And Packages

## Purpose and boundaries

This skill covers two linked concerns in Swift mobile and Apple-platform work:

1. **Networking layer**: request construction, transport via URLSession, concurrency, error modeling, decoding, authentication handoff, retry and cancellation, and response caching.
2. **Package management**: adding, pinning, resolving, and reviewing Swift Package Manager (SwiftPM) dependencies, including the effect of third-party packages on binary size, build time, privacy manifests, and licensing.

Out of scope: backend API design, UI state management beyond the call boundary, push notification infrastructure, and CocoaPods or Carthage migrations (note them only as migration sources).

## Inputs and assumptions

Before acting, establish:

- Target platforms and minimum OS versions (these gate which URLSession and concurrency APIs are available).
- Swift language version and Xcode version in use.
- Whether the project uses a `Package.resolved` file and whether it is committed.
- Existing networking abstraction, if any, and its error type.
- Auth model (bearer token, cookie, mTLS, none) and where credentials are stored.
- Data sensitivity: personal, health, financial, or regulated data changes what may be logged or cached.

If any of these is unknown, ask. Do not assume a minimum OS version.

## Operating workflow

1. **Map the call path.** Trace one request from call site to wire: request builder, session configuration, delegate or interceptor, decoder, error mapping, caller.
2. **Classify the change.** Networking-only, dependency-only, or both. Dependency changes require the gates below.
3. **Define the contract.** Write the expected status codes, decodable shapes, error cases, and timeout values before editing code.
4. **Implement behind one seam.** Route all requests through a single client protocol so tests can substitute a fake transport. Prefer `async throws` functions over completion handlers in new code.
5. **Model errors explicitly.** Separate transport failure, HTTP status failure, decoding failure, and cancellation into distinct cases. Never collapse them into a generic string.
6. **Handle cancellation.** Propagate task cancellation to URLSession calls. Do not swallow `CancellationError`.
7. **Retry narrowly.** Retry only idempotent requests, only on transient failures (timeouts, 429 or 503 with backoff honoring `Retry-After`), with a bounded attempt count and jitter.
8. **For packages,** add the minimum product needed, pin via `Package.resolved`, and record the reason in the PR description.

## Decision gates

Stop and obtain explicit user approval before:

- Adding any new third-party package, or upgrading a major version of an existing one.
- Changing the committed `Package.resolved` other than through a normal resolve.
- Deleting, force-resetting, or rewriting caches, keychains, or stored tokens.
- Changing TLS settings, certificate pinning, or disabling ATS exceptions.
- Adding logging of request or response bodies, headers containing credentials, or personal data.
- Altering server-facing behavior: new endpoints, changed retry semantics on non-idempotent methods (POST, PATCH without idempotency keys), or changed rate of calls.
- Any change that alters a privacy manifest or data-collection declaration.

Proceed without a gate for: local refactors within the seam, adding unit tests, and fixing decoding errors against a documented contract.

## Verification and evidence

Each change must show:

- **Build**: clean build on the minimum supported OS target and the current toolchain.
- **Tests**: unit tests with a fake transport covering success, each HTTP error class, malformed JSON, cancellation mid-request, and retry exhaustion. Target all branches of the error mapper.
- **Dependency audit**: `swift package show-dependencies` output (or the Xcode equivalent) attached to dependency PRs, with each new package's license and privacy manifest status checked by reading its repository. Confirm the exact current command syntax against official SwiftPM documentation.
- **Binary impact**: for new packages, measured app-size delta from an archive, reported as measured, not estimated.
- **Concurrency check**: build with strict concurrency checking enabled at the level the project uses; report any new warnings.

Do not state performance improvements, benchmark numbers, or compliance status without a measurement or a document reference.

## Failure handling

- **Resolution conflict**: report the conflicting version requirements verbatim, identify the dependent package, and propose either a version range change or a fork. Do not force a version with overrides without approval.
- **Unexpected status codes**: map to a generic server error case, preserve status and a redacted body excerpt for debugging, and flag for contract review.
- **Decoding failure**: surface the decoding path (key path) to the developer; do not silently default missing fields unless the contract marks them optional.
- **Flaky retries or duplicate writes**: stop retry, check idempotency, and escalate.
- **Uncertain API availability**: if an API's availability or signature is unverified, mark it "verify against current Apple documentation" rather than guessing.

## Deliverable contract

Every deliverable includes:

1. A short statement of what changed and why, in two to four sentences.
2. The file list with each file's role.
3. The error model and call contract for any new endpoint, as a table: method, path, success type, error cases, retry policy.
4. For package changes: package name, requested version rule, products added, license, reason, and approval reference.
5. Test results and the verification items above, with unverified items explicitly labeled.
6. Open questions and any gated actions awaiting approval.

## What not to do

- Do not use `try!` or force-unwrap response data in production paths.
- Do not disable certificate validation for debugging and leave it in code.
- Do not store tokens in UserDefaults or plain files; use the platform keychain.
- Do not retry POST requests without an idempotency mechanism agreed with the server.
- Do not add a package to solve a problem the standard library or URLSession already solves.
- Do not invent API names, flags, or package versions; verify against current official documentation.