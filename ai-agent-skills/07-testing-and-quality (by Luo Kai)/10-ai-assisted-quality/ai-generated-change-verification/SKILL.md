---
name: ai-generated-change-verification
description: Independently verifies code and configuration changes produced by AI agents before merge or release. Use for reviewing diffs, checking requirements, running tests, detecting regressions, and preventing unsupported claims of completion.
license: Proprietary. See repository LICENSE
metadata:
  author: Luo Kai
  provenance: original
  version: "1.0.0"
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
