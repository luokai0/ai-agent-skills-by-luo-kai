---
name: ai-generated-change-verification
description: Independently verifies code and configuration changes produced by AI agents before merge or release. Use for reviewing diffs, checking requirements, running tests, detecting regressions, and preventing unsupported claims of completion.
metadata:
  author: Luo Kai
  provenance: original
  version: "1.1.0"
---
# AI-Generated Change Verification

## Principle

The agent that produced a change should not be the only authority declaring it correct. Verify the diff, requirements, tests, and resulting state independently.

## 1. Freeze the review inputs

Record the original user request and acceptance criteria; base and candidate commits; complete changed-file list and diff; relevant repository instructions and architecture constraints; build environment, dependency versions, and available test commands.

Do not rely solely on the implementation agent's summary. Read the actual diff and inspect generated, renamed, deleted, and binary files.

## 2. Map requirements to evidence

Create a requirement matrix:

| Requirement | Changed location | Verification | Result |
|---|---|---|---|
| User-visible behavior | File and symbol | Test or reproducible observation | Pass / Fail / Unknown |
| Compatibility | Platform or API | Build and compatibility test | Pass / Fail / Unknown |
| Security constraint | Boundary or permission | Negative test and code inspection | Pass / Fail / Unknown |
| Regression prevention | Existing behavior | Regression test | Pass / Fail / Unknown |

Every important requirement needs evidence. “Looks correct” is not evidence.

## 3. Review the diff adversarially

Look for scope creep and unrelated modifications; removed validation, permissions, error handling, or tests; hardcoded secrets, tokens, credentials, or personal data; unsafe shell commands, dynamic code execution, injection, or untrusted deserialization; broken authorization, tenant isolation, or data ownership; unhandled nulls, races, cancellation, retries, and partial failures; dependency additions, lockfile drift, install scripts, and supply-chain changes; platform-specific paths, casing, line endings, and unsupported APIs; and documentation or generated indexes that no longer match implementation.

Trace changed code into callers and dependencies. A locally correct function can still break its contract.

## 4. Validate in increasing cost order

1. Formatting, lint, and static checks.
2. Unit tests for changed behavior.
3. Integration tests at affected boundaries.
4. Build and package validation.
5. Cross-platform tests where applicable.
6. End-to-end tests for critical user journeys.
7. Security and permission tests.
8. Manual verification of high-impact behavior.

Run the repository's documented commands. Do not invent a passing result if a tool or dependency is unavailable. Record skipped checks as Not run, not Passed.

## 5. Verify external side effects

For changes that affect a remote service, deployment, database, or account, inspect the exact target and environment; confirm authorization and approval; capture pre-change state where appropriate; execute only the approved operation; read back the resulting state independently; and verify rollback or recovery options.

A successful command exit code does not always prove the intended state changed.

## 6. Separate findings from speculation

Each finding includes severity, file and line, concrete evidence, impact, reproduction steps, and a suggested fix. Distinguish confirmed defects from risks that need further testing.

Do not invent vulnerabilities to make a review appear thorough. Do not suppress a confirmed issue because the build passes.

## 7. Release decision

- PASS: requirements are met, required checks pass, and no blocking findings remain.
- FAIL: a critical requirement or safety boundary is violated.
- PARTIAL: some requirements pass, but a required check is missing or a non-blocking issue remains.
- NOT VERIFIED: evidence is insufficient to make a reliable decision.

Never report fixed, built, deployed, or released unless the corresponding result was observed. Include exact commit, build, test, and deployment references.

## 8. Final verification report

Summarize scope, commit range, changed files, requirement coverage, commands run, test results, security findings, skipped checks, residual risks, and release decision. Keep the report concise but make every conclusion traceable to evidence.

## 9. Verify generated and non-text artifacts

Do not assume a text diff covers the entire change.

- Inspect images, archives, compiled outputs, database snapshots, model files, and other binary artifacts using appropriate metadata and safe inspection tools.
- Compare generated files with their source inputs and documented build process. Regenerate them when practical and compare outputs.
- Check archive contents for unexpected files, path traversal entries, symlinks, embedded executables, and oversized payloads.
- Inspect lockfiles, package manifests, generated API clients, schemas, migrations, and indexes for unintended drift.
- Verify checksums or signatures for downloaded build artifacts when available. Record the exact artifact digest used for testing.
- Treat opaque or uninspectable artifacts as an evidence gap. Do not approve them merely because the source diff looks harmless.

## 10. Review data, schema, and migration changes

For database, storage, or data-transformation changes:

1. Identify affected tables, records, indexes, constraints, access policies, and downstream consumers.
2. Review migration ordering, compatibility with old and new application versions, and behavior during rolling deployment.
3. Test migrations against representative synthetic data, including empty, large, malformed, and boundary cases.
4. Check whether retries are safe and whether operations are idempotent.
5. Verify backup, restore, rollback, and forward-fix procedures. Some destructive migrations cannot be reversed by simply rolling back application code.
6. Confirm row-level authorization, tenant boundaries, retention, and deletion behavior remain intact.
7. Compare pre-change and post-change state using independent queries or checksums where appropriate.

Never run an unreviewed destructive migration against production as a verification shortcut.

## 11. Check concurrency and failure recovery

Test the changed behavior under realistic interruption and concurrency:

- Duplicate requests, retries, delayed responses, and out-of-order events.
- Concurrent writes, stale reads, lock contention, and race conditions.
- Cancellation before, during, and after a side effect.
- Partial completion across multiple services and compensation behavior.
- Rate limits, timeouts, network loss, and dependency unavailability.
- Process restart and recovery of queued or persisted work.

Verify idempotency keys and transaction boundaries where relevant. A retry must not duplicate a payment, message, account mutation, or deployment.

## 12. Verify security properties with negative tests

For every changed trust boundary, test both the allowed path and the denied path.

Include unauthorized callers, cross-tenant identifiers, malformed schemas, oversized inputs, path traversal, untrusted URLs, redirect abuse, secret leakage, unsafe deserialization, and prompt injection in external content where relevant.

Confirm that security controls are enforced by the server or platform boundary, not merely described in prompts or UI copy. Verify that logs and error messages do not disclose credentials or private records.

## 13. Establish an evidence hierarchy

Prefer evidence in this order:

1. Independently observed resulting state and reproducible end-to-end behavior.
2. Automated tests, integration checks, and build outputs from the exact candidate revision.
3. Static analysis, code inspection, and dependency/security reports.
4. Logs and telemetry with traceable provenance.
5. Implementation-agent explanations or summaries.

Lower-level evidence can guide investigation but cannot replace stronger evidence. Record the exact command, tool, environment, revision, and output for every decisive check.

If a check depends on an external service or unavailable environment, mark it Not run or Partially verified and state what remains unknown.

## 14. Verify CI and release gates

Before approval, confirm that required checks ran against the exact commit being merged or released. Check workflow definitions, trigger conditions, permissions, secrets exposure, artifact provenance, and whether jobs can be skipped or bypassed.

- Require protected checks for critical paths and ensure a failed required job blocks release.
- Do not trust a green status from a different commit, branch, environment, or stale workflow run.
- Inspect the final commit after any automated formatter, generator, merge, or release step.
- Verify that release artifacts correspond to the reviewed commit and that deployment targets are correct.
- Record manual approvals and any accepted risk with an owner and expiration or review date.

## 15. Preserve review independence

The implementation agent may propose tests and explain design decisions, but the verifier must inspect evidence independently.

For high-impact changes, use a separate reviewer or execution context that did not generate the patch. Give the verifier the acceptance criteria and artifacts, not only the implementation agent's narrative. Disclose shared assumptions, unavailable test environments, and any checks performed by the same agent that authored the change.

A successful verification applies only to the reviewed commit, configuration, environment, and test scope. Re-review after any material change.
