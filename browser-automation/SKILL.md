---
name: browser-automation
description: Use when designing, writing, debugging, or reviewing scripted browser interactions for end-to-end testing, UI regression checks, or repeatable web workflows, including selector strategy, waits, test data, and evidence capture.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Browser Automation

## Purpose and boundaries

This skill guides building and maintaining automated browser test flows that exercise a web application the way a user does, and that report reliable pass/fail results with evidence. It covers test scripts, page interaction design, assertions, flake diagnosis, and CI-oriented execution.

In scope: end-to-end test authoring, page object or component abstractions, selector and wait strategy, network stubbing for test isolation, screenshot and trace capture, and reviewing existing browser tests.

Out of scope: load testing, scraping third-party sites, bypassing authentication or bot protections, automating actions on production systems with real customer data, and security exploitation. Refuse or escalate these.

## Inputs and assumptions

Before writing anything, establish:

1. Target environment: URL, staging vs. production, and whether test accounts exist.
2. Framework and language already used by the project. Do not introduce a second framework without approval.
3. Browsers and viewports required by the project's support matrix.
4. Critical user journeys, ranked by business impact.
5. Test data ownership: who creates, resets, and deletes records.
6. Existing selectors, test IDs, and accessibility labels.

If any item is unknown, state the assumption explicitly in the deliverable. Do not assume production access.

Version-sensitive details (driver versions, browser channels, CLI flags, library APIs) must be checked against current official documentation before use. Mark any unverified detail as "verify against current docs."

## Operating workflow

1. **Map the journey.** Write the flow as numbered user actions with one observable outcome per step. Stop if a step requires an unavailable system.
2. **Choose the locator order.** Prefer, in order: dedicated test attributes, ARIA role plus accessible name, visible label text, then stable structural selectors. Never use auto-generated class names, deep XPath chains, or nth-child positions for core flows.
3. **Drive state through the interface sparingly.** Set up preconditions through APIs or seeded fixtures when the UI path under test is not the setup. Reserve UI interaction for the behavior being verified.
4. **Wait on conditions, not time.** Wait for a visible element, an enabled control, a URL change, or a specific network response. Fixed sleeps are prohibited.
5. **Assert outcomes.** Each test ends with at least one assertion on user-visible state or persisted effect. Assertions on the mere absence of errors are insufficient.
6. **Isolate.** Each test creates its own data with unique identifiers, runs independently, and cleans up or uses a disposable environment.
7. **Capture evidence on failure.** Configure trace, screenshot, and console/network log capture for failing runs only, to limit storage and noise.
8. **Run repeatedly.** Execute the suite in a loop (for example, several consecutive runs in CI or locally) before declaring it stable.

## Decision gates

Stop and request explicit approval before:

- Running any test against production or any environment holding real customer data.
- Creating, modifying, or deleting data outside a test-owned namespace.
- Sending real emails, SMS, payments, webhooks, or third-party API calls.
- Storing credentials, session tokens, or cookies in source files or logs.
- Disabling or deleting existing tests, or marking them skipped to pass a pipeline.
- Changing shared CI configuration, browser grids, or secrets.
- Adding a new dependency, framework, or paid service.

Proceed without approval only for read-only inspection, local runs against an isolated test environment, and edits to test files the user has asked you to change.

## Verification and evidence

A browser test change is complete only when:

- The test passes on at least three consecutive runs in the target environment, with the flake rate recorded (target: zero flakes across those runs).
- The test fails when the behavior it covers is deliberately broken (mutation check). Record what was broken and that the test caught it.
- Execution time is recorded; any single test over the project's budget is flagged. Do not invent a budget; use the one the project defines, or ask.
- Failure artifacts (trace, screenshot) are produced and are openable.
- No secrets appear in committed files or logs. Search the diff for tokens, passwords, and personal data before reporting completion.

When reporting results, state the exact environment, browser, commit or build identifier, number of runs, and pass/fail counts. Do not report "all tests pass" without these.

## Failure handling

- **Timeout waiting for element:** Check whether the element exists in the DOM, is hidden by an overlay, is behind a loading state, or has changed its accessible name. Fix the locator or wait condition, not the timeout value.
- **Intermittent failure:** Reproduce by running the single test in a loop. Compare passing and failing traces for differences in network timing, animations, or data state. Quarantine only with approval and a tracking note.
- **Data collision:** Confirm unique identifiers are used and cleanup ran. Do not delete shared records to unblock a run.
- **Authentication failure:** Stop. Do not attempt to circumvent login, CAPTCHA, or MFA. Request a sanctioned test account or session setup method.
- **Environment unreachable:** Report the blocker with the URL and error; do not switch targets without approval.

## Deliverable contract

Each deliverable contains:

1. The test file(s) or diff, with the journey steps mapped to test steps in comments only where the mapping is non-obvious.
2. A short assumptions list, including unverified version-sensitive details.
3. The verification record: environment, browser, run count, pass/fail results, flake observations, mutation check result.
4. Known gaps: journeys not covered, environments not tested, and anything deferred pending approval.
5. Required approvals outstanding, if any.

Keep the report factual and brief. State what was run, what was observed, and what was not verified.