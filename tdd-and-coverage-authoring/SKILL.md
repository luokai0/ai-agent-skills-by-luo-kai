---
name: tdd-and-coverage-authoring
description: Use when writing or revising tests test-first (red-green-refactor), designing unit or integration test suites, or interpreting and improving code coverage metrics in a software project.
author: Luo Kai
provenance: original
version: 1.0.0
---

# TDD and Coverage Authoring

## Purpose and boundaries

This skill guides an agent through test-driven development (TDD) and the authoring of meaningful coverage. It covers: writing failing tests before implementation, choosing test granularity, structuring test suites, reading coverage reports, and closing gaps that matter.

It does not cover: load or performance testing, security penetration testing, UI visual regression infrastructure, CI pipeline provisioning, or changing production behavior beyond what a failing test demands. If a request is primarily one of these, state that and hand off.

## Inputs and assumptions

Before acting, establish:

1. The language, test framework, and assertion library in use. Read the existing test configuration and one or two existing tests to match conventions. Do not introduce a new framework without approval.
2. The behavior under change: a bug report, a feature specification, or a refactoring goal. Write the expected behavior in one sentence before touching code.
3. The current coverage baseline, if any, produced by the project's own tooling. If none exists, say so and do not invent a number.
4. Whether the target code has external dependencies (network, database, clock, filesystem, queues). Identify them; they determine test doubles.

Assume the repository is under version control and tests can be run locally. If they cannot, stop and report.

## Operating workflow

1. **Locate the seam.** Find the smallest public interface that exhibits the behavior. Prefer testing through public functions or endpoints over private helpers.
2. **Write one failing test.** Name it after the behavior ("returns 0 when cart is empty"), not the method. Use Arrange-Act-Assert. Run only that test and confirm it fails for the expected reason (an assertion mismatch, not a syntax or import error). A test that passes before implementation proves nothing unless it guards existing behavior, in which case label it as a characterization test.
3. **Implement the minimum.** Write only enough production code to pass the failing test. Resist adding untested branches.
4. **Run the full affected suite.** Confirm green and no regressions.
5. **Refactor under green.** Remove duplication, rename, extract. Re-run tests after each change.
6. **Repeat** for the next behavior. Keep each cycle small enough to finish in minutes.
7. **Edge cases in a batch.** After the happy path, enumerate boundaries (empty, zero, maximum, null, duplicate, concurrent, timezone or locale edges) and add one failing test per case through steps 2 to 5.
8. **Coverage pass.** Only after behavior tests exist, generate the coverage report with the project's configured command. Inspect uncovered lines in changed files first.

## Decision gates

- **Mock or real?** Use real in-memory implementations for pure logic and collaborators with no I/O. Use test doubles for network, clock, randomness, and paid or rate-limited services. Use real databases only in integration tests with a disposable instance. Never point tests at shared or production data stores.
- **Unit or integration?** A test that needs more than one process or external service is integration. Keep the count of integration tests low and mark them so they can be run separately.
- **Coverage gap: write a test or exclude?** Write a test if the line encodes business logic, validation, or error handling. Exclude only generated code, trivial re-exports, or framework boilerplate, and record the exclusion rule in the project's configuration with a comment.
- **Test change or code change?** If a previously passing test now fails, determine whether the requirement changed. If it did, update the test and state the requirement change. If it did not, the code change is a regression; fix the code.
- **Snapshot tests?** Use only for stable serialized output. Never accept a snapshot update without reviewing the diff.

## Verification and evidence

Report the following, with actual command output:

- Test counts before and after: total, passing, failing, skipped. Skipped tests require a stated reason.
- The red run: the failing assertion text for each new test.
- The green run: full suite result.
- Coverage: line and branch percentages for changed files, compared to baseline. Report the tool and configuration used.
- Mutation or fault check, if the project has a mutation tool: report surviving mutants in changed code. If no such tool exists, state that the check was not performed.

Quality checks:
- Every new test fails before the fix and passes after.
- No test asserts only that a function was called unless the call itself is the requirement.
- No test depends on execution order, wall-clock time, or random seeds without pinning them.
- Changed files reach the project's configured threshold, or the shortfall is explained.

Do not claim a coverage percentage, speed improvement, or defect-reduction figure that was not measured in this session.

## Failure handling

- **Test fails for an unexpected reason** (import error, fixture missing): fix the harness first; this is not a valid red state.
- **Cannot make a test fail first:** the behavior may already exist. Verify, then label the test as characterization.
- **Flaky test:** rerun to confirm. Do not add retries or sleeps as a fix. Identify the nondeterministic input and inject control.
- **Coverage tool produces inconsistent numbers:** verify the configuration path and the tool version against current official documentation before trusting figures.
- **Existing suite is too slow to run per cycle:** run the affected test file only during red-green, and run the full suite before reporting. Report the timing.

## Deliverable contract

Provide:

1. A list of behaviors added or changed, each with its test file and test name.
2. Red and green evidence as described above.
3. Coverage summary for changed files with the exact command used.
4. Open gaps: untested edge cases, excluded lines with justification, and any skipped tests.
5. Any change requiring approval, such as new dependencies, configuration changes to coverage thresholds, or deletion of existing tests, listed as pending and not applied.

Do not delete or weaken existing assertions to make the suite pass. Do not lower coverage thresholds, add exclusions, or install packages without explicit approval. Do not run tests against production systems or shared data stores. Mark any version-specific flag or tool behavior as requiring verification against current official documentation.