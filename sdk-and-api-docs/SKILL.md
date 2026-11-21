---
name: sdk-and-api-docs
description: Use when writing, reviewing, or restructuring documentation for an SDK, public API, or developer-facing library, including reference docs, quickstarts, error catalogs, migration guides, and code samples.
author: Luo Kai
provenance: original
version: 1.0.0
---

# SDK and API Docs

## Purpose and boundaries

This skill produces and audits developer documentation for SDKs, HTTP/RPC APIs, CLIs exposed to developers, and client libraries. It covers: conceptual overviews, authentication setup, quickstarts, endpoint or method reference, parameter and response schemas, error catalogs, pagination and rate-limit guidance, versioning and deprecation notices, migration guides, and runnable code samples.

Out of scope: end-user product help, marketing copy, internal engineering runbooks, and changes to the API or SDK behavior itself. If documentation reveals a behavior bug, report it; do not document the bug as intended behavior.

## Inputs and assumptions

Before writing, collect:

1. The source of truth: OpenAPI/API schema, SDK source, type definitions, changelog, or test suite. Prefer generated reference from schema where the project already does so.
2. Target audience and skill level (for example, backend integrator versus mobile developer).
3. The exact version(s) documented. Each page must state which version it describes.
4. Supported languages, runtimes, and minimum platform versions.
5. Existing doc structure, style guide, and terminology glossary.

Assumptions must be written down explicitly. If a fact cannot be traced to a source, mark it `UNVERIFIED` and list it in the handoff note. Do not infer parameter types, defaults, limits, or error codes from naming conventions.

## Operating workflow

1. **Map the surface.** List every public operation, class, method, option, and error. Diff against the previous documented version if one exists.
2. **Classify each item** as stable, beta, experimental, or deprecated, using the project's own labels. Note the removal target for deprecated items if one is published.
3. **Write the concept layer first:** what the resource or client does, its object model, and the lifecycle of key objects (for example, created, pending, completed, failed).
4. **Write the auth and setup section** with the minimum steps to make one successful call. Show where credentials are obtained and where they must never be placed (client-side bundles, logs, version control).
5. **Write one quickstart** that completes end to end, then reference pages for each operation: purpose, parameters (name, type, required, default, constraints), request example, response example, errors, and idempotency or side-effect notes.
6. **Write the error catalog:** each error code or exception class, its HTTP status or type, cause, whether retry is safe, and the recommended client action.
7. **Write cross-cutting guidance:** pagination, rate limits, timeouts, retries with backoff, webhooks or event verification, and rate-limit headers as documented by the source.
8. **Write the migration guide** for any breaking change: old form, new form, one before/after example per change, and a removal date only if confirmed.
9. **Run the verification pass** (below) and produce the deliverable.

## Decision gates

- **Schema vs. handwritten:** If an OpenAPI or typed spec exists and is current, generate reference sections from it and hand-write only concepts and guides. If the spec disagrees with the implementation, stop and escalate; do not publish either version as correct.
- **Sample code:** Include a sample only if it has been executed against the documented version, or the project's test suite exercises the same call. Otherwise label it "illustrative, not executed."
- **Behavior ambiguity:** If a default, limit, or ordering rule is not stated in source, mark `UNVERIFIED` and request confirmation from the owning team. Never publish a guessed value.
- **Version-sensitive details** (package names, minimum runtime versions, flag names, endpoint paths, rate limits): add a note "verify against current official documentation for version X" unless the value is pulled directly from the versioned source.
- **Breaking change publication:** Requires explicit owner approval before the migration guide and deprecation notice are published, because they shape customer behavior and commitments.
- **Publishing or overwriting live docs:** Requires explicit approval. Drafts go to a review branch or staging location.

## Verification and evidence

- Every parameter, response field, and error code in the reference traces to a schema, type, or test. Record the source path for each section in the review notes.
- Run every quickstart and runnable sample against the documented version in a sandbox or test environment. Record command, version, and result.
- Link-check all internal and external references. Zero broken links is the pass bar.
- Check that every required parameter in the reference is marked required in the source. Mismatches count as defects.
- Confirm terminology is consistent: one term per concept across all pages (a glossary term list helps).
- Confirm each page states its version and last-verified date.
- Measurable target: 100% of documented operations have a reference entry; 100% of error codes in the catalog are reachable or marked as reserved; 0 samples that fail execution in the documented environment.

## Failure handling

- **Source and implementation disagree:** Stop, document the discrepancy with both sources cited, and escalate to the API owner. Do not publish a reconciled guess.
- **Sample fails:** Record the exact error and environment. Fix the sample if the doc is wrong; file a defect if the API is wrong. Remove or label the sample if the fix is not available before release.
- **Missing information from owners:** Leave the `UNVERIFIED` marker in place, list open questions in the handoff, and do not fill gaps with plausible defaults.
- **Conflicting versions in one page:** Split into version-specific pages or add an explicit version selector. Do not mix behaviors in one table.

## Deliverable contract

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