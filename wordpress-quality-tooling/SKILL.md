---
name: wordpress-quality-tooling
description: Use when setting up, running, or interpreting quality tools for a WordPress plugin, theme, or site codebase, including coding standards, static analysis, unit and integration tests, end-to-end browser tests, and CI gating.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Wordpress Quality Tooling

## Purpose and boundaries

This skill covers the quality toolchain for WordPress code: coding-standard linting, static analysis, automated unit and integration tests, end-to-end browser tests, and the CI gates that enforce them. It produces a working, reproducible tooling configuration and a verified report of what passes, what fails, and why.

In scope: plugin and theme repositories, custom mu-plugins, and site-level code under version control; local and CI execution; baseline management for legacy code.

Out of scope: performance tuning, security penetration testing, accessibility audits beyond automated checks, hosting configuration, and rewriting application logic beyond what a failing check strictly requires.

## Inputs and assumptions

Collect before acting:
- Repository layout (plugin, theme, or site), root path, and whether a build step exists.
- Minimum supported PHP and WordPress versions (from the plugin header, `readme.txt`, or the project owner).
- Existing tooling files: `composer.json`, `package.json`, lint configs, test bootstrap, CI workflow files.
- CI platform and whether it has access to a database service.
- Target environment: local containers, CI runners, or both.

Assumptions to state explicitly in the report if unverified: the PHP version range, the WordPress test library installation method, and the browser testing framework version. Do not assume the project uses Composer or npm; detect it.

## Operating workflow

1. Inventory. List existing quality configuration and run nothing destructive. Record the current state of the default branch.
2. Pin the runtime. Determine the lowest and highest supported PHP versions. Test against both where the project claims support.
3. Establish a baseline. Run the existing linters and tests without modification. Save raw output to a log file. Count violations per tool and per file.
4. Configure coding standards. Use the WordPress coding standards ruleset via PHP_CodeSniffer, adding WordPress-specific sniffs for escaping, sanitization, and i18n text domain consistency. Set the text domain and prefix to the project's actual values. Verify current rule names against the official ruleset documentation before writing them.
5. Configure static analysis. Use PHPStan or Psalm at a conservative level first. Add the WordPress stubs package appropriate to the project. Start at a level where the baseline is manageable; raise it only after the baseline is clean.
6. Configure tests. Use PHPUnit with the WordPress test suite for integration tests that need a database, and Brain Monkey or similar for pure unit tests of logic that does not touch globals. Keep the two suites separate in configuration.
7. Configure end-to-end tests with a browser framework only for critical user flows (activation, checkout, form submission, login). Do not write E2E tests for every screen.
8. Wire CI. Run lint and static analysis on every push; run integration tests against a matrix of PHP and WordPress versions; run E2E on pull requests to the main branch or on demand.
9. Establish baselines for legacy violations. Commit a baseline file that suppresses existing issues. New code must pass with zero new violations.
10. Verify the pipeline end to end on a clean checkout before reporting.

## Decision gates

- Gate A, before modifying any file: confirm the target branch with the owner. Creating a branch is allowed; pushing to a shared remote requires approval.
- Gate B, before adding dependencies: state the package name, purpose, and license category. Require approval for any package that is not a standard WordPress or PHP ecosystem tool.
- Gate C, before raising a static analysis level or enabling a strict sniff set: proceed only if the baseline error count is zero or fully captured in the baseline file.
- Gate D, before changing CI secrets, database credentials, or deployment steps: stop and request explicit approval. Never write credentials into repository files.
- Gate E, before deleting or regenerating a baseline file: require approval, because regeneration can silently hide regressions.
- Gate F, before running tests against any non-local database or live site: stop. Tests must use disposable databases only.

## Verification and evidence

Each claim in the final report must cite a command and its exit code. Minimum checks:
- Coding standards: zero errors and zero warnings on changed files; zero new violations against the baseline on the full tree.
- Static analysis: exit code 0 at the configured level; baseline entries count does not increase.
- Unit tests: all pass; report the count of tests and assertions.
- Integration tests: pass on every PHP and WordPress combination in the matrix; record which combinations ran.
- E2E tests: pass three consecutive runs locally for any newly added spec, to detect flakiness.
- CI: a green run on a clean clone, with the workflow run identifier recorded.

Measurable thresholds: no test may depend on execution order; the full unit suite should complete within a stated time budget agreed with the owner; any test skipped must have a documented reason.

## Failure handling

- Tool version mismatch: pin the version in the lock file, then re-run. Do not silence the error by excluding the rule.
- Flaky E2E test: quarantine it with a tracked issue, do not retry-loop it into passing.
- Baseline growth: revert the offending change or fix it; do not regenerate the baseline.
- Database connection failure in integration tests: verify the test database service and credentials in the environment; do not hardcode fallbacks pointing to other databases.
- Unclear WordPress API behavior: check the current official developer documentation; do not infer function signatures from memory.

## Deliverable contract

Deliver:
1. The changed files, listed with paths and a one-line purpose each.
2. A tooling summary: tool names, configured versions, and how each is run locally (exact commands as used).
3. A baseline report: violation counts before and after, with the baseline file path.
4. Verification evidence: command, exit code, and summary per check.
5. Open items: unverified version details, skipped tests with reasons, and any gate awaiting approval.

Do not: suppress errors with blanket ignore directives, disable rules to pass, commit secrets, claim compliance or certification from passing tools, or state version numbers that were not verified against current official documentation.

## Test architecture and regression governance (v1.1)

### Assign each test to the narrowest useful layer

Use pure unit tests for deterministic business logic that can run without WordPress globals or a database. Use WordPress integration tests when behavior depends on hooks, capabilities, post/meta APIs, database queries, or plugin activation. Use REST request tests for route registration, schema validation, authentication, permission callbacks, and response contracts. Reserve browser E2E tests for a small number of high-value user journeys whose correctness depends on the full browser-to-server path.

Do not duplicate every assertion at every layer. Put detailed edge-case coverage at the cheapest layer that faithfully represents the behavior, then retain a smaller number of integration and E2E tests to verify wiring. A test that mocks the behavior it claims to verify is not evidence that the real integration works.

### Control test-environment risk

Every test environment must have an explicit identity and data boundary. Use disposable databases and synthetic fixtures. Before a test suite runs, assert that the database host/name matches the configured test target and fail closed if it resembles production. Block outbound email, payment, webhook, and other external side effects by default; replace them with local fakes or isolated test endpoints. Do not let tests use production credentials as convenient defaults.

Tests that create users, roles, content, or options must clean up after themselves even on failure. Prefer isolated fixtures and transactions where supported, but do not assume all WordPress hooks and storage operations are transaction-safe. Run a cleanup verification after destructive integration suites.

### Keep baselines honest

A baseline is a snapshot of accepted legacy debt, not a permanent exemption. Store its generation command and tool version, review changes to it like source code, and prohibit automatic baseline regeneration in ordinary CI. New or modified lines should be held to the current rule set even when untouched legacy files remain temporarily suppressed. Track baseline size and age, assign an owner, and set a reduction target.

### Make CI failures diagnostic

Split CI into fast feedback and deeper validation. Run formatting, lint, static analysis, and unit tests early. Run database-backed integration tests and browser tests in later jobs with explicit service readiness checks. Preserve machine-readable reports and test artifacts, but redact secrets and personal data before upload. Use caches only as performance aids: a cache hit must never replace dependency lockfile validation or clean-checkout verification.

When a job fails, classify it as product regression, test defect, environment failure, dependency/tool mismatch, or flaky behavior. Retry only when the failure class justifies it, record each retry, and do not convert intermittent success into a green result without root-cause tracking.

### Regression policy

- New code must not introduce new lint or static-analysis findings.
- Every bug fix should add a regression test at the narrowest faithful layer.
- Permission-sensitive routes need both allowed and denied cases, including object-level authorization.
- Critical E2E flows must be deterministic and use isolated test accounts.
- Skips, quarantines, and expected failures need owners, reasons, and expiry/review dates.
- CI must report the exact commit tested and runtime/tool versions used.

## Ultron routing contract

**Choose this skill when:** configuring, running, or interpreting WordPress-specific quality tooling, test layers, static analysis, CI gates, regression policy, or safe test environments.

**Choose wordpress-rest-api when:** defining endpoint semantics, request/response schemas, authentication, permission rules, pagination, or compatibility behavior. That skill owns the API contract and security expectations; this skill turns those expectations into repeatable route tests and pipeline gates.

**Handoff contract:** accept the WordPress/PHP support matrix, repository layout, API or feature contracts, test-environment boundaries, and required release gates. Return pinned tooling configuration, layered test coverage, clean-checkout results, exact command/exit-code evidence, and explicit gaps. A green pipeline is not proof of requirements that were never represented by a test.

**Why the boundary exists:** this skill owns the repeatable verification system; feature-specific skills own expected behavior. The separation keeps tests grounded in real contracts instead of letting available tooling dictate what correctness means.
