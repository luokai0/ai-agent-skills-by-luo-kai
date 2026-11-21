---
name: unit-and-component-testing
description: Use when writing, reviewing, or repairing unit tests or component tests for application code, including test design, isolation of dependencies, fixture strategy, coverage interpretation, and flaky-test diagnosis.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Unit And Component Testing

## Purpose and boundaries

This skill guides the design and maintenance of tests that verify a single unit (a function, class, or module) or a single component (a module or service boundary with its real internal collaborators but external systems replaced). It covers test structure, dependency substitution, assertion quality, and test-suite health.

Out of scope: end-to-end browser flows, load and performance testing, security penetration testing, and contract verification across independently deployed services. Redirect those to their own practices.

## Inputs and assumptions

Before writing tests, establish:

1. The unit or component under test, its public interface, and its documented behavior. If behavior is undocumented, derive it from the code and state the derived contract explicitly.
2. The language, test framework, and mocking library in use. Do not assume APIs; check the project's lockfile and existing test files. Mark any framework-specific syntax you are unsure of for verification against the current official documentation.
3. Existing test conventions: file location, naming, fixture style, and how the suite is run in CI.
4. External boundaries: databases, network calls, clocks, filesystem, randomness, message queues. Each must be classified as substitute, fake, or real (see Decision gates).

If the target cannot be run locally, stop and report that the suite cannot be verified.

## Operating workflow

1. **Map behaviors.** List observable behaviors as statements: "given X, when Y, then Z." Include error paths, boundary values, and invalid inputs. Aim for one behavior per test.
2. **Classify dependencies.** For each collaborator, choose a strategy from the decision gates.
3. **Write the failing test first when fixing a defect.** Confirm it fails for the stated reason before changing production code.
4. **Structure each test in arrange, act, assert.** Keep one act per test. Name tests after the behavior, not the method: `rejects negative quantity with ValidationError` rather than `test_add_item_2`.
5. **Build minimal fixtures.** Construct only the state the behavior needs. Prefer inline builders with overridable defaults over large shared fixtures.
6. **Assert on outcomes.** Check return values, persisted state through a fake, emitted events, or raised errors. Avoid asserting on the exact sequence of internal calls unless the call itself is the contract.
7. **Run the suite in isolation and in random or reversed order** if the runner supports it, to expose hidden shared state.
8. **Measure.** Run coverage for the changed files and review uncovered branches.

## Decision gates

- **Real versus substitute:** Use the real implementation for pure logic and in-process value objects. Use a fake (in-memory repository, deterministic clock) for stateful collaborators where behavior matters. Use a mock or stub only to verify an interaction that is itself the contract, such as "payment gateway is charged exactly once."
- **Mock count:** If a test needs more than three substitutes, the unit likely has too many responsibilities. Report this as a design finding rather than adding more mocks.
- **Time, randomness, and identifiers:** Inject them. Never rely on wall-clock time or unseeded randomness in assertions.
- **Coverage target:** Require branch coverage on changed lines, not a global percentage. Do not raise thresholds as part of a test change unless the owner asks.
- **Integration boundary:** If a behavior depends on real database semantics (transactions, constraint behavior, query planning), it belongs in an integration test, not a unit test. Do not simulate those semantics with a fake and claim verification.
- **Destructive or external actions:** Running tests that write to shared databases, call paid or production APIs, send messages, or delete files requires explicit user approval. Default to local, in-memory, or sandboxed resources.

## Verification and evidence

Report the following for every change:

- The exact test command run and its exit status.
- Count of tests added, modified, and removed, with the reason for each removal.
- Evidence that a new regression test failed before the fix and passed after.
- Branch coverage for changed files, stated as a measured number from the tool output.
- Results of at least one re-run to detect flakiness. Any test that fails intermittently is treated as a defect, not retried into passing.

Quality checks:

- No test sleeps for a fixed duration to wait for asynchronous work; use explicit completion signals.
- No test depends on execution order or on another test's side effects.
- Assertions name specific expected values; no bare truthiness checks on complex objects.
- Test runtime for the unit suite is recorded; flag any individual test over one second for review.

## Failure handling

- **Test fails after a behavior change:** Determine whether the old behavior was the contract. If the contract changed intentionally, update the test and state the change. If not, fix the code.
- **Flaky test:** Capture the seed, timing, and ordering. Remove the nondeterminism source (usually time, shared state, or real I/O). Do not add retries or increase timeouts as the fix.
- **Cannot isolate a dependency:** Stop and report the coupling. Propose a seam, such as extracting an interface, but do not restructure production code without approval.
- **Framework API uncertainty:** Mark the call as unverified, check the current official documentation for the pinned version, and note the verification in the deliverable.

## What not to do

- Do not write tests that merely execute code without asserting behavior.
- Do not snapshot large objects as the primary assertion.
- Do not delete or skip failing tests to achieve a green run.
- Do not mock the unit under test or its own private helpers.
- Do not invent framework functions, flags, or version compatibility claims.
- Do not claim coverage or correctness beyond what the executed tools reported.

## Deliverable contract

Return:

1. The changed or new test files, complete and runnable.
2. A short summary table: behavior tested, substitution strategy, and result.
3. The verification evidence listed above.
4. A list of open findings: design issues, unverified API usage, and coverage gaps, each with a recommended next step.

## Ultron routing contract

**Choose this skill when:** testing a bounded unit or component in isolation, including functions, classes, modules, and components with their internal collaborators while external services are replaced by controlled fakes or mocks.

**Choose `e2e-test-engineering` when:** the requirement depends on real process, network, storage, browser, identity, or multi-service behavior and must be proven as an end-to-end journey.

**Handoff contract:** return deterministic local tests with clear assertions, fixtures, boundary coverage, and fast failure diagnostics. Escalate only the behaviors that depend on real system composition to E2E tests; do not copy every unit case into a slow browser journey.

**Why the boundary exists:** isolated tests make local reasoning cheap and precise; end-to-end tests validate integration and user-visible outcomes. A healthy test strategy needs both layers.
