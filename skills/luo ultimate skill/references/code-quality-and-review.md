# Code Quality and Review

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## ai-change-verification

**Use when:** Use when an AI-generated or AI-assisted code, configuration, prompt, or documentation change must be checked before merge or release, to confirm it does what was intended, breaks nothing, and leaves an auditable evidence trail.

### Purpose and boundaries

This skill verifies changes produced or substantially shaped by an AI model. The goal is to establish, with evidence, that a change (1) implements the stated intent, (2) does not regress existing behavior, (3) introduces no unreviewed security, data, or dependency risk, and (4) is reproducible by a human reviewer.

In scope: diffs to source code, tests, infrastructure-as-code, SQL migrations, prompts and prompt templates, evaluation configs, and technical documentation that describes behavior.

Out of scope: deciding product direction, authoring net-new features from scratch (use a design skill for that), and certifying regulatory compliance. Do not claim compliance; report only what was checked.

### Inputs and assumptions

Required before starting:
- The change: diff or commit range, plus the base revision.
- Intent: a ticket, issue, or plain statement of expected behavior. If absent, write one from the diff and get the author to confirm it. Do not verify against an intent you invented without confirmation.
- Affected surfaces: services, public interfaces, data stores, and configuration keys touched.
- Existing test and check commands for the repository. Discover them from project files and CI config; do not assume.

Assumptions to state explicitly in the report: the base revision was green before the change; the test environment resembles production in the dimensions the change touches.

### Operating workflow

1. **Scope the diff.** List every changed file. Classify each as behavior, test, config, dependency, generated, or documentation. Flag generated files and confirm their source of truth was changed instead.
2. **Restate intent as testable claims.** Produce 3 to 10 numbered claims in the form "Given X, when Y, then Z." Each claim must map to at least one check.
3. **Read, do not trust.** Review the diff line by line for: silent exception swallowing, hardcoded credentials or environment values, widened permissions, removed validation, altered defaults, deleted or weakened assertions, and unexplained new dependencies.
4. **Check tests against claims.** For each claim, confirm a test exists and would fail on the base revision. A test that passes on both revisions does not verify the claim. Run it against base to confirm.
5. **Run the existing suite** on the change, then the new or modified tests in isolation, then once more with a fixed random seed or repeated runs if the code has concurrency or ordering sensitivity.
6. **Run static and security checks** the repository already uses (linter, type checker, dependency audit, secret scanner). Record new findings only; pre-existing findings go in an appendix.
7. **Exercise the boundary.** For changed interfaces, test at least: a valid nominal input, one invalid input, one empty or null input, and one boundary value.
8. **Verify migrations and config** on a disposable copy: apply forward, confirm, and where a rollback path is claimed, apply and confirm it.
9. **For prompts or model-facing text**, run the fixed evaluation set before and after the change, using identical model settings. Report the per-case diff, not only the aggregate.
10. **Write the report** using the deliverable contract below.

### Decision gates

- **Gate A (scope):** If the diff exceeds roughly 400 changed lines or mixes unrelated concerns, request a split before deep review.
- **Gate B (intent):** If intent cannot be confirmed by a human, stop and mark the result "unverified: intent unconfirmed."
- **Gate C (regression):** Any previously passing test that now fails blocks approval until the cause is explained and the change or test is corrected with justification.
- **Gate D (security):** Any new secret-like string, widened IAM or ACL scope, disabled certificate check, or new network egress target requires explicit human approval.
- **Gate E (destructive operations):** Any migration that drops, truncates, or rewrites data, any force-push, any production command, and any action that sends data to an external service requires explicit written approval from the owning maintainer before execution. Do not run such steps on shared or production resources under any circumstances without that approval.
- **Gate F (model drift):** If the evaluation shows a regression on more than 5% of previously passing cases, or on any case tagged safety-critical, block and escalate.

### Verification and evidence

Each claim receives one status: **verified** (test fails on base, passes on change, and was run), **partially verified** (covered by reasoning or a weaker test only), or **unverified**.

Evidence to record per check: exact command, revision hash, environment identifier, exit status, and the relevant output excerpt. Do not paraphrase results as passing without the command that produced them.

Quality thresholds:
- Every claim has a status and at least one evidence item.
- Zero new unexplained static-analysis or secret-scan findings.
- Changed lines have line or branch coverage not lower than the base for the touched modules, as reported by the project's own tool.
- Flaky tests: a test that fails then passes on rerun is reported as flaky, not as passing.

Do not state benchmark numbers, performance improvements, or security guarantees unless measured in this review and reported with method.

### Failure handling

- **Test fails on change, passes on base:** Treat as a regression. Identify the smallest failing input, bisect the diff if multiple edits are involved, and report the root cause before proposing a fix.
- **Test passes on both:** The test does not verify the claim. Mark the claim partially verified and propose a discriminating test.
- **Environment cannot reproduce:** Record the missing dependency or access, do not substitute assumptions silently, and downgrade affected claims.
- **Evaluation results are noisy:** Rerun identical settings at least three times, report the spread, and do not claim improvement inside the noise band.
- **Reviewer disagrees with a status:** Keep the status with the evidence attached, and escalate rather than editing the report to match the disagreement.

### Deliverable contract

Produce a single report with these sections, in this order:

1. **Summary:** one of APPROVE, APPROVE WITH CONDITIONS, BLOCK, or UNVERIFIED, with one sentence of reasoning.
2. **Scope:** file classification table and total changed lines.
3. **Claims:** numbered list, each with status and evidence references.
4. **Findings:** new issues by severity (blocking, major, minor), each with file, line, and reproduction.
5. **Commands run:** exact commands, revision hashes, environment identifiers, and exit codes.
6. **Approvals requested:** every gate triggered, with the approver required.
7. **Limitations:** what was not checked and why.
8. **Appendix:** pre-existing findings, clearly separated from new ones.

Do not omit the limitations section. A review with no stated limitations is not credible.
### AI change provenance and release evidence (v1.1)

Treat every AI-assisted change as a traceable transformation. Bind the change request, accepted intent, base revision, candidate revision, tool/model configuration, generated artifacts, test run, reviewer decision, and release decision into one change record. Keep generated output distinguishable from human-authored edits where practical; authorship labels must not be used as a substitute for review.

For every changed behavior, write a claim and a discriminating test that fails on the base revision and passes on the candidate. Add negative assertions for forbidden behavior, permission expansion, unintended network access, secret exposure, and unexpected file or data mutation. A test that passes on both revisions does not prove the change.

Review generated dependencies, migrations, configuration defaults, and scripts as carefully as application code. Check that examples and documentation do not introduce unsafe commands or claim unsupported capabilities. For prompt or skill changes, compare trajectories under a frozen evaluation suite and inspect regressions case by case.

Before release, produce a reproducibility bundle: exact revisions, commands, environment, test outputs, static-analysis findings, approvals, and known limitations. If any result cannot be reproduced, downgrade its status. Keep rollback instructions and identify the exact artifact or configuration to restore.

### Ultron routing contract

**Choose this skill when:** approving a concrete AI-generated or AI-assisted change to code, configuration, documentation, infrastructure, or data transformation. It owns provenance, baseline-versus-candidate comparison, discriminating tests, negative assertions, reproducibility, and rollback evidence.

**Choose `code-review-and-test-generation` when:** the change needs a structured diff review and new regression tests.

**Choose `code-review-execution` when:** an independent reviewer must assess the patch and issue a merge recommendation without authoring the change.

**Choose `agent-evaluation-design` when:** the question is whether an agent/model behavior or release should pass a reusable evaluation policy, rather than whether one specific artifact is correct.

**Handoff contract:** receive the exact candidate diff and base identity, test evidence, affected surfaces, and expected external postconditions. Return a traceable change decision with tests, failures, residual risks, and rollback artifact. Do not treat a model's explanation of its own change as verification.

**Why the boundary exists:** artifact correctness, independent code review, and agent capability evaluation are related but distinct assurance claims.


## code-quality-maintenance

**Use when:** Use when reviewing, refactoring, or stabilizing an existing codebase for readability, maintainability, lint and type cleanliness, dead code, duplication, complexity, or test health, without changing intended behavior.

### Purpose and boundaries

This skill covers incremental improvement of existing code: reducing complexity, removing dead and duplicated code, tightening types and lint compliance, clarifying naming and structure, and repairing flaky or misleading tests. The governing constraint is behavior preservation. Every change must be justified by a measurable quality signal and verified against existing or newly added tests.

In scope: refactors within a module or service, lint and type remediation, dead-code removal confirmed by reference search, test cleanup, dependency hygiene inside a single repository, and documentation of invariants that the code already relies on.

Out of scope: new features, architectural rewrites, performance tuning without a profile, security-policy changes, dependency upgrades that change major versions, and anything touching production infrastructure or data.

### Inputs and assumptions

Before starting, establish:

1. The repository, branch, and a clean working tree. Record the base commit.
2. The quality target: a specific module, a metric threshold, a lint rule set, or a named pain point (for example, "the billing module has 40 duplicated validation blocks").
3. The project's existing toolchain: linters, formatters, type checker, test runner, coverage tool. Read the configuration files rather than assuming defaults. Version-specific flags and rule names must be checked against the tool's current official documentation before use.
4. Whether a reliable test suite exists for the target area. If coverage is absent or the suite is flaky, treat that as the first finding, not a license to refactor blindly.
5. Public interfaces that external consumers depend on (exported functions, HTTP contracts, serialized schemas, CLI arguments). These are frozen unless the owner approves change.

If any assumption is unverified, state it in the deliverable.

### Operating workflow

1. **Baseline.** Run the full test suite, type checker, and linter on the untouched tree. Record pass/fail counts, warning counts, and coverage for the target scope. Save the output.
2. **Measure.** Collect concrete signals: cyclomatic complexity per function where the toolchain provides it, function length, duplicate-block counts, unused exports and imports, `any` or untyped usages, and skipped or quarantined tests. Rank findings by impact-to-risk ratio.
3. **Select a batch.** Choose one cohesive batch of 3 to 10 related changes in one module. Small batches keep review and rollback cheap.
4. **Characterize before changing.** For code with weak tests, write characterization tests that pin current observable behavior, including odd behavior, and mark them as characterization. Do not "fix" pinned behavior in the same batch.
5. **Refactor in small steps.** Apply one transformation at a time (extract function, rename, inline single-use helper, replace conditional chain with lookup, narrow a type). Run the relevant tests after each step.
6. **Remove dead code only with evidence.** Confirm no references exist via static search, and check dynamic access patterns (reflection, string-based dispatch, configuration references, generated code). Dead code that is referenced by configuration is not dead.
7. **Re-measure.** Repeat the baseline commands and compare.
8. **Commit in logical units.** One commit per transformation type, with messages stating what changed and why.

### Decision gates

Stop and request approval before proceeding when any of the following apply:

- The change alters a public interface, serialized format, database schema, or message contract.
- Removing code would delete a path that tests do not cover and that cannot be confirmed as unreachable.
- The change requires a dependency upgrade, a new dependency, or a change to build or CI configuration.
- Lint or type rules would be disabled, loosened globally, or suppressed in bulk rather than per line with a reason.
- Coverage on the target scope would drop.
- Any action would touch data stores, deploy artifacts, rotate credentials, or alter shared CI resources. These require explicit human approval; do not proceed on inference.

Proceed without asking only for changes that are internal, covered by passing tests, and reversible by reverting a commit.

### Verification and evidence

A change is accepted only when all of the following hold:

- Full test suite passes with no new skips, and no test was weakened (assertions removed, tolerance widened, or timeouts raised to mask failures).
- Type checker and linter report no new errors; warning count in scope is equal or lower.
- Target metric improved: for example, function count above complexity threshold dropped, or duplicated blocks reduced, measured with the same tool and settings as the baseline.
- Public API diff is empty, verified by comparing exported symbols or generated signatures.
- For dead-code removal: search results show zero references across source, tests, configuration, and documentation, and the build succeeds.

Record evidence as a table: metric, baseline, after, command used.

### Failure handling

- **Test fails after a refactor step:** revert that step, not the batch. Diagnose whether the test encodes an assumption the refactor violated. Fix the refactor, not the test, unless the test is demonstrably wrong and the owner agrees.
- **Flaky test appears:** rerun in isolation to classify. Quarantine only with an owner-approved ticket reference; never silently delete.
- **Metric regresses:** a tool may flag new issues caused by a rename or extraction. Address them within the batch or revert.
- **Unexpected behavior discovered:** stop, document the observation with a reproduction, and escalate. Do not patch behavior under a quality label.

### Deliverable contract

Produce:

1. A summary of baseline and final metrics with exact commands.
2. A list of changes grouped by batch, each with its rationale and commit reference.
3. An explicit list of deferred items with reasons (approval needed, unclear behavior, out of scope).
4. Any unverified assumptions, including tool versions and configuration details requiring confirmation against current official documentation.
5. Residual risks, stated plainly.

What not to do: do not bundle behavior changes with cleanup, do not suppress warnings to pass gates, do not reformat entire files unrelated to the batch (this inflates diffs and hides real changes), do not invent tool flags or rule identifiers, and do not claim quality improvements that were not measured.


## code-review-and-test-generation

**Use when:** Use when reviewing code changes for correctness, risk, and maintainability, or when generating, extending, or repairing automated tests for a defined change set in a repository.

### Purpose and boundaries

This skill produces two artifacts for a given change: a structured review of the diff, and tests that exercise the behavior the change introduces or modifies. It covers reading code, identifying defects and risks, proposing or writing tests, running them, and reporting results.

In scope: diffs, pull requests, single files, and modules within a checked-out repository; unit and integration tests written in the project's existing test framework; regression tests for reported bugs.

Out of scope: rewriting unrelated code, changing production behavior beyond what a fix requires, load or security penetration testing, certifying compliance, and deploying anything.

### Inputs and assumptions

Before starting, establish:

1. The change under review: diff range, commit hashes, or file list. If none is given, use the working tree diff and state that choice.
2. The stated intent: ticket text, PR description, or the bug report. If absent, infer intent from the code and label it as inferred.
3. The language, framework, and test runner, read from manifest and lockfiles and existing test files. Do not assume a framework that the repository does not already use.
4. The build and test commands documented in the repository. Prefer the documented command over guessed flags.
5. Whether network access, databases, or external services are reachable. Tests must not depend on live external systems unless the repository already does so in its test setup.

Record every assumption in the final report.

### Operating workflow

1. **Map the change.** List touched files, public interfaces altered, and data shapes changed. Group changes by behavior, not by file.
2. **Derive expected behavior.** Write one to five plain-language behavior statements the change must satisfy. Mark any that come from inference.
3. **Review for defects.** Check each category in order: input validation and boundary values; error paths and exception handling; null, empty, and zero-length inputs; concurrency and shared state; resource cleanup; off-by-one and time-zone or encoding handling; backward compatibility of public signatures and serialized formats; security-relevant handling of untrusted input.
4. **Classify findings.** Use severity levels: blocker (incorrect behavior or data loss), major (likely failure under realistic input), minor (clarity, naming, dead code), nit (style only, optional).
5. **Check existing coverage.** Locate current tests touching the changed code. Note which new behaviors have no coverage.
6. **Design tests.** For each behavior statement and each blocker or major finding, define at least one test: arrange, act, assert. Include one negative or error-path case per behavior. Use the repository's fixtures and helpers.
7. **Write tests.** Place them beside existing tests following the project's naming convention. Do not modify existing assertions to make tests pass unless the old assertion encoded the defect, and say so explicitly.
8. **Run.** Execute the narrowest test target first, then the full suite for the affected package.
9. **Report.** Summarize findings using the review output structure below.

### Decision gates

- **Gate A, before writing tests:** If the expected behavior is ambiguous and two reasonable interpretations produce different results, stop and ask the requester which is correct. Do not encode a guess as an assertion.
- **Gate B, before modifying production code:** The task is review and tests. Changing production code requires explicit approval, except for a one-line fix the requester has already asked for.
- **Gate C, before any action that deletes files, rewrites history, force-pushes, alters CI configuration, changes dependency versions, or touches credentials, migrations, or production data:** Require explicit approval with the exact command or file list shown.
- **Gate D, before contacting external services or posting comments to a remote review system:** Require explicit approval and show the text first.
- **Gate E, flaky tests:** If a test fails intermittently on rerun, quarantine it only with approval and record the reproduction rate.

### Verification and evidence

- Every blocker and major finding cites file path and line range, plus a concrete input that triggers the problem.
- Every new test is run and its pass or fail result is recorded. A test not executed is reported as not executed.
- Confirm each new test fails on the pre-change code where practical (by stashing the fix or checking out the base commit). Report which tests failed before and passed after. If this is not feasible, say why.
- Report the exact test command used and its summary line: total, passed, failed, skipped.
- Coverage numbers are reported only if the repository's own coverage tool produced them in this run. Do not estimate coverage.
- Mark any statement about library behavior or API signatures as requiring verification against current official documentation when the version is not confirmed from the lockfile.

### Failure handling

- **Build fails before tests run:** Report the first error verbatim, do not guess fixes to build configuration, and stop unless the fix is within the change under review.
- **Existing tests fail unrelated to the change:** Record them as pre-existing with the failing names. Do not fix them without approval.
- **New test cannot be made to pass without changing production behavior:** Report it as a candidate defect with the failing assertion. Do not weaken the assertion.
- **Missing dependency or tool:** Report the name and the repository's documented install step. Do not install globally without approval.
- **Time or resource limits reached:** Report what finished, what did not, and the next command to run.

### Deliverable contract

Return one report with these sections, in order:

1. **Scope:** change identifier, files reviewed, assumptions list.
2. **Findings:** table with severity, location, description, triggering input, and suggested fix.
3. **Tests added or changed:** file paths, test names, behavior each covers.
4. **Execution:** exact commands, pass/fail/skip counts, pre-change versus post-change results.
5. **Open items:** unresolved ambiguities, pre-existing failures, approvals needed.

Keep prose short. Use a finding only when it is specific enough for an author to act on without re-deriving it. Quality check: every finding has a location and a reproducer, every test has been executed, and no assertion was weakened silently.

### Ultron routing contract

**Choose this skill when:** the task asks for a constructive review of a change together with tests that cover the changed behavior. It may propose or author regression tests, identify missing cases, run the relevant suite, and produce a structured review artifact.

**Choose `code-review-execution` when:** an independent reviewer must assess an existing patch or pull request, challenge its claims, identify defects, and issue a merge recommendation without taking ownership of implementing the feature or writing its repair.

**Handoff contract:** this skill returns the reviewed diff, findings with file/line evidence, tests added or proposed, test outcomes, and unresolved risks. The independent review skill checks the change and the adequacy of the evidence from a separate reviewer perspective. Do not count self-review by the change author as independent approval.

**Why the boundary exists:** producing review/test artifacts and independently deciding whether a change is ready to merge are different accountability roles.


## code-review-execution

**Use when:** Use when performing, coordinating, or structuring a code review of a change set, pull request, or patch, including triaging findings, deciding merge readiness, and writing actionable review comments.

### Purpose and boundaries

This skill covers executing a code review: reading a change, testing its claims, finding defects and risks, and producing a merge recommendation with traceable findings. It applies to pull requests, patches, and staged diffs in application, library, infrastructure, and data code.

Out of scope: writing the feature itself, designing architecture from scratch, security penetration testing, and performance benchmarking beyond reading existing evidence. Route those to the appropriate skill or owner.

### Inputs and assumptions

Required before starting:
- The diff or change reference, and the base it targets.
- The stated intent: linked ticket, PR description, or commit messages.
- Access to the repository at the change's head commit, so surrounding code can be read.
- The project's contribution guidelines, style rules, and CI status.

Assumptions to state explicitly if unverified: that CI results correspond to the current head commit; that the described behavior matches the ticket; that no generated or vendored files are being reviewed as hand-written code.

If intent is missing, reconstruct it from the diff, record the reconstruction as an assumption, and ask the author to confirm before issuing a final verdict.

### Operating workflow

1. **Scope the change.** Count files and lines changed. Separate generated, lockfile, vendored, and formatting-only changes from logic changes. Review logic first.
2. **State the claim.** Write one or two sentences describing what the change is supposed to do. Every later check tests this claim.
3. **Read the diff in two passes.** Pass one: structure, interfaces, data flow, and file layout. Pass two: line-level correctness, edge cases, error paths, and concurrency.
4. **Read context, not just the diff.** Open each modified function in full. Check callers of changed signatures, and check tests that cover the touched behavior.
5. **Check the specific risk classes** (see Verification).
6. **Run or inspect evidence.** Confirm CI results, run the test suite locally when the change is non-trivial, and reproduce any bug you claim.
7. **Classify each finding** (see Decision gates) and write it as a comment with location, reasoning, and a suggested direction.
8. **Issue a verdict** with a summary of blocking items, non-blocking items, and what you did not verify.

### Decision gates

Classify every finding:
- **Blocking:** incorrect behavior for a reachable input, data loss or corruption, a security or privacy regression, a broken public contract, a missing migration or rollback path, or a failing required check.
- **Non-blocking (should fix):** unclear naming, missing edge-case test, duplicated logic likely to drift, misleading comment.
- **Nit:** style or preference the project does not enforce. Prefix with "nit:" and never block on it.
- **Question:** you do not understand the intent. Ask before judging.

Approve only when: no blocking findings remain, required CI passes on the head commit, and the claim in step 2 is supported by code or tests. Request changes when any blocking finding exists. Escalate to a domain owner when the change touches authentication, payments, personal data, schema migrations on large tables, or infrastructure with production blast radius.

Size gate: if the change exceeds roughly 400 changed lines of logic, recommend splitting, unless it is a mechanical change such as a rename or generated update.

### Verification and evidence

Check these risk classes for every review:
- **Boundaries:** empty, null, zero, maximum, and off-by-one inputs; unicode and timezone handling where relevant.
- **Errors:** every new error path returns, logs, or propagates as the surrounding code expects; no swallowed exceptions; no partial writes without cleanup.
- **Concurrency:** shared mutable state, check-then-act sequences, missing locks or transactions, retry safety and idempotency.
- **Data:** schema changes are backward compatible during rolling deploys; migrations are reversible or have a documented forward-only plan; indexes exist for new query paths.
- **Contracts:** public function, API, and event shapes are unchanged or versioned; callers in the repository are updated.
- **Tests:** new behavior has tests that would fail without the change; tests assert outcomes, not implementation details; no disabled or skipped tests without a tracked reason.
- **Dependencies:** new packages have justified need, acceptable license per project policy, and pinned versions. Verify current version and advisory status against the registry or official documentation. Do not assume a version is safe or current from memory.

Evidence standard: every blocking finding must cite a file and line, and state a concrete input or sequence that triggers it. "This might be slow" is not a finding; "this loops over all rows per request, and the endpoint is called per item" is.

Measurable quality checks: the review records files read, checks completed from the list above, and CI run identifier. Coverage claims must come from the project's reported tool output, not estimates.

### Failure handling

- **CI red or missing:** do not approve. Record the failing job and whether it reproduces locally.
- **Cannot reproduce a claimed bug:** ask for a failing test or steps; do not block on speculation.
- **Scope too large to review properly:** say which parts were reviewed in depth and which were skimmed, and recommend splitting.
- **Disagreement with author:** restate the concrete input that causes the issue. If unresolved, escalate to the module owner rather than repeating the argument.
- **Insufficient access:** list what was not inspected in the verdict.

### Deliverable contract

The review output contains, in order:
1. Verdict: approve, request changes, or comment-only.
2. Change claim and whether it was verified.
3. Blocking findings, each with location, trigger, and suggested direction.
4. Non-blocking findings and nits, grouped by file.
5. Questions for the author.
6. Evidence reviewed: CI run, commands executed, files read in depth.
7. Unverified areas and assumptions.

Do not:
- Approve with unresolved blocking items or red required checks.
- Block on personal style preference.
- Rewrite the author's change wholesale in comments.
- Post comments that cannot be acted on without further explanation.
- Share credentials, internal URLs, or customer data found in a diff; flag them and request explicit approval from the owner before any further external disclosure.
- Merge or push changes to the author's branch without explicit approval from the author or maintainer.

### Ultron routing contract

**Choose this skill when:** the task is an independent assessment of a proposed change and needs a traceable review, evidence-backed defect findings, risk classification, and merge recommendation. The reviewer should challenge assumptions and verify behavior without becoming the feature author.

**Choose `code-review-and-test-generation` when:** the requested deliverable includes creating regression tests or improving test coverage alongside the review.

**Handoff contract:** receive the diff, stated intent, test results, and relevant requirements. Return prioritized findings with exact locations and reproduction evidence, missing proof, and a clear recommendation. If new tests are needed, delegate their construction and then independently inspect whether they actually cover the reported risk.

**Why the boundary exists:** review independence is weakened when the same agent both authors a change and approves it. Test generation can be delegated without surrendering independent judgment.


## review-feedback-handling

**Use when:** Use when processing code review, test review, or QA feedback on a change, to triage comments, decide what to act on or push back on, implement fixes, and verify each resolution with evidence before closing the thread.

### Purpose and boundaries

This skill governs how you respond to feedback on test code, test plans, test results, and related quality artifacts (pull request review comments, QA defect reviews, test-plan sign-off notes). The goal is to resolve each point correctly: accept valid feedback with a verified change, decline or redirect invalid feedback with a stated reason, and surface disagreements that need a human decision.

In scope: triaging comments, reproducing claimed defects, applying fixes to tests or test-related code, writing reply text, and recording verification evidence.

Out of scope: rewriting the product feature under review beyond what a comment requires, changing CI policy or branch protection, deleting tests to make a suite pass, editing reviewer comments, and closing threads on another person's behalf.

### Inputs and assumptions

Before acting, collect:

- The full list of comments with author, location (file, line, test name), and status.
- The change under review (diff, commit range, or test plan version).
- How to run the relevant tests locally and in CI. If unknown, ask; do not guess commands.
- Project conventions documented in contributing or testing guides.

Assume reviewers may be wrong, incomplete, or referring to an earlier revision. Assume your own prior work may contain the defect being raised until you prove otherwise.

### Operating workflow

1. **Snapshot the state.** Record the current commit, branch, and a list of all open comments. Work from this snapshot so later edits do not blur what was addressed.
2. **Classify each comment** into one of: defect (behavior is wrong), test gap (missing coverage or assertion), flakiness or determinism, readability or naming, style nit, question, or disagreement.
3. **Reproduce before changing.** For defects and test gaps, write or run the smallest check that demonstrates the claim. If you cannot reproduce it, record the exact steps you tried and the output.
4. **Decide the response** using the gates below.
5. **Implement one logical fix per comment** where practical, so each can be reverted or reviewed independently.
6. **Re-run the affected tests**, then the broader suite the change touches.
7. **Reply on each thread** with what changed (commit or line reference), the evidence, or the reasoning for declining.
8. **Re-check for regressions** introduced by the fix, especially around shared fixtures, test ordering, and mocks.

Batch comments that touch the same code, but still reply to each individually.

### Decision gates

Apply these in order:

- **Gate 1: Reproduces?** If the claimed failure reproduces, fix it. If it does not reproduce after a documented good-faith attempt, ask the reviewer for the exact input, environment, or command. Do not apply speculative changes.
- **Gate 2: Correct?** If it reproduces but the reviewer's proposed fix is wrong or would weaken coverage, implement a better fix and explain why.
- **Gate 3: Scope?** If the fix requires changing product behavior, a shared test utility used by other teams, a public interface, or test data that others depend on, stop and request explicit approval before proceeding.
- **Gate 4: Cost?** For style nits, apply if the change is under the project's formatting rules or takes under a few minutes. Otherwise accept the point as a follow-up issue with a link, and say so.
- **Gate 5: Disagreement?** If you believe the comment is incorrect after reproduction, reply with the evidence and the specific question. Leave the thread open for the reviewer to resolve.

Require explicit approval before any of the following: deleting or skipping tests, lowering assertion strictness or coverage thresholds, adding retries to hide flakiness, changing shared fixtures or test data used elsewhere, posting replies or resolving threads on behalf of others, and any action touching production data, credentials, or external services.

### Verification and evidence

A thread is resolved only when you can state:

- The command run and its result (pass/fail counts, relevant output excerpt).
- For a defect fix: the test that failed before the change and passes after it.
- For a coverage claim: the coverage report or assertion added, not a percentage alone.
- For a flakiness fix: the number of repeated runs and their results, stated as observed, not guaranteed.

Use the project's own test runner and coverage tool; verify exact flags and option names against the current official documentation for the version in use, since these change between releases. Do not claim a fix is "verified in CI" until CI has actually run.

Quality checks before marking the review complete:

- Every comment has a reply and a status: fixed, declined with reason, deferred with link, or awaiting reviewer.
- No test was weakened, skipped, or retried to pass unless approved.
- The affected test suite passes locally and the diff contains no unrelated changes.
- Assertions check specific expected values, not only absence of exceptions.

### Failure handling

- **Fix breaks other tests:** Revert that single change, isolate the coupling, and re-apply in a narrower form. Report the coupling in the thread.
- **Cannot reproduce:** Document steps, environment, and output. Ask the reviewer; keep the thread open.
- **Flaky result after fix:** Do not merge a retry as the fix. Identify the nondeterminism source (timing, shared state, ordering, unseeded randomness) and report it.
- **Conflicting reviewer comments:** Summarize both positions with evidence and request a decision from the reviewer or maintainer.
- **Time pressure:** Fix blocking defects first, then correctness gaps, then readability. Defer nits explicitly rather than silently skipping them.

### Deliverable contract

Produce a feedback resolution log containing:

1. A table: comment ID or link, author, classification, gate outcome, action taken, commit reference, evidence summary.
2. The full test commands executed and their final results.
3. A list of items awaiting approval or reviewer input, each with the specific question.
4. A list of deferred items with follow-up references.
5. A short statement of residual risk, such as untested environments or unverified CI results.

Do not state that feedback has been fully addressed unless every comment is in a terminal state (fixed with evidence, declined with reason, deferred with reference, or explicitly awaiting a named person).


## software-quality-and-security-review

**Use when:** Use when reviewing source code, pull requests, diffs, or modules in any programming language for correctness, maintainability, and security defects, and when producing a prioritized, evidence-backed review report.

### Purpose and boundaries

This skill guides a structured review of code for defects in three areas: correctness and reliability, maintainability and design, and security. It produces findings ranked by severity, each tied to a file location, a reproduction or reasoning trace, and a concrete fix direction.

In scope: diffs, pull requests, single files, modules, and small services; language-idiom issues (memory safety, concurrency, error handling, type misuse, injection, deserialization, secrets handling, authorization checks, dependency risk indicators).

Out of scope: rewriting the codebase, performance tuning without a measured bottleneck, style-only feedback unless it hides a defect, and certifying compliance with any standard. Do not claim the code is "secure" or "bug-free"; state only what was checked.

### Inputs and assumptions

Required inputs: the code or diff, the language and runtime version if known, and the intended behavior (ticket, docstring, or stated purpose). If intent is missing, infer it from tests and call sites, and label the inference as an assumption.

Optional inputs: existing test results, linter or static analyzer output, dependency manifests, threat model, deployment context (public-facing, internal, batch).

Assumptions must be listed explicitly in the report. Never assume that code is unreachable, that input is trusted, or that a framework provides protection unless the framework behavior is confirmed in its current official documentation.

### Operating workflow

1. **Scope the review.** List the files and the changed line ranges. Identify entry points: HTTP handlers, CLI arguments, message consumers, file parsers, deserializers, environment reads.
2. **Map data flow.** For each entry point, trace untrusted input to sinks: SQL/shell/template construction, file paths, deserialization, eval-like constructs, outbound requests, logs, and persistent storage.
3. **Check trust boundaries.** Confirm where authentication, authorization, validation, and encoding occur, and whether they run on every path, including error and retry paths.
4. **Review correctness.** Examine null/none handling, integer overflow and truncation, off-by-one ranges, resource release on all exits, race conditions on shared state, time-of-check/time-of-use gaps, partial failure and retry idempotency, and silent error swallowing.
5. **Review language-specific hazards.** Examples: unchecked casts or unsafe blocks in Rust and C#; goroutine leaks and unsynchronized maps in Go; mutable default arguments and pickle or yaml unsafe loading in Python; prototype pollution and unhandled promise rejections in JavaScript; `unsafe` pointer arithmetic and unchecked buffer sizes in C/C++.
6. **Review maintainability.** Flag duplicated logic that has already diverged, functions whose behavior cannot be stated in one sentence, hidden global state, and tests that assert implementation rather than behavior. Keep these findings at low severity unless they cause a defect.
7. **Verify each candidate finding** before reporting (see Verification and evidence).
8. **Rank and write the report** using the Deliverable contract.

### Decision gates

- **Gate A, severity:** Critical if exploitable without authentication or causes data loss or corruption in normal use. High if exploitable with ordinary user privileges or causes a crash or incorrect results on a common path. Medium if the defect requires an unusual input, race window, or misconfiguration. Low for maintainability and hardening suggestions.
- **Gate B, reachability:** Report a finding as confirmed only if a concrete path from an entry point reaches the defect. Otherwise report it as "suspected, reachability unknown" and state what would confirm it.
- **Gate C, scope of fix:** If the fix requires changing a public interface, schema, persisted data format, or dependency version, flag it and request approval before recommending it as a default.
- **Gate D, sensitive material:** If the code or diff contains credentials, tokens, private keys, personal data, or production connection strings, stop quoting them. Report location and type only, and recommend rotation. Obtain explicit approval before reproducing any such value in output.
- **Gate E, active testing:** Do not run exploit payloads, network scans, load tests, or code that writes to shared, production, or third-party systems without explicit approval and a stated isolated environment.

### Verification and evidence

Every finding must include:
- File path and line range.
- The input or condition that triggers the defect.
- The observed or derived behavior, with the reasoning chain.
- A reproduction: a minimal failing unit test or a command in an isolated environment, if approved. If reproduction is not performed, say so.

Use static analyzers and linters as evidence sources, but do not report their output verbatim; confirm each hit. Discard hits you cannot reproduce or reason through, and list them under "Dismissed with reason" for transparency.

Quality checks before finalizing:
- Every Critical and High finding has a reproduction or a complete reasoning trace.
- No finding cites a line that does not exist in the reviewed revision.
- Each recommendation is checked against the language version in use.
- Any library, function, or flag name is verified against current official documentation. Mark version-sensitive details as "verify against current official documentation" rather than asserting them.

### Failure handling

- **Missing context:** Proceed with stated assumptions, and mark affected findings as provisional.
- **Analyzer unavailable or failing:** Continue manual review and note the gap in the report.
- **Conflicting intent and behavior:** Report the conflict as a finding; do not resolve it by choosing the more convenient reading.
- **Reproduction blocked by approval gate:** Record the finding as unverified and state the approval needed.
- **Large diff:** Prioritize entry points and security-relevant modules; state the unreviewed portion explicitly.

### Deliverable contract

Produce one report with these sections, in order:

1. **Summary:** scope, revision reviewed, overall risk statement limited to what was checked, counts by severity.
2. **Assumptions and gaps:** list.
3. **Findings:** ordered by severity, each with ID, severity, location, trigger, evidence, impact, and recommended fix.
4. **Dismissed with reason:** candidate issues rejected and why.
5. **Approvals needed:** any pending decisions under Gates C, D, or E.
6. **Verification performed:** what was run, what was only read.

Do not include praise, filler, or compliance claims. Do not paste secrets. Do not state that a fix is verified unless it was tested.

### Ultron routing contract

**Choose this skill when:** reviewing a change or codebase across the combined dimensions of correctness, reliability, maintainability, design quality, and security, with prioritized findings and concrete fix direction.

**Choose appsec-code-review when:** the central question is whether authentication, authorization, secrets, session/token handling, or data trust boundaries contain security defects requiring threat-oriented analysis.

**Handoff contract:** request the security skill's findings with affected code paths, exploit preconditions, privilege/data impact, and regression cases. Integrate them into the broader review without downgrading security severity. If the review discovers a security-only issue, route the deeper analysis rather than improvising an exploitability claim.

**Why the boundary exists:** broad quality review provides system-level change assessment; focused AppSec review provides deeper security reasoning at trust boundaries.


## software-quality-devops

**Use when:** Use when designing, reviewing, or repairing CI/CD pipelines, test gates, release checks, or deployment safeguards for software projects, including when an AI agent must make or recommend changes to build, test, or deploy automation.

### Purpose and boundaries

This skill covers the quality and delivery path between a committed change and a running artifact: build reproducibility, automated test gates, static and security checks, artifact promotion, deployment safeguards, and rollback readiness. It produces findings, pipeline changes, and release recommendations backed by evidence.

Out of scope: product feature design, infrastructure cost optimization, incident commander duties, and writing application code beyond what a pipeline fix requires.

### Inputs and assumptions

Collect before acting:
- Repository layout, default branch, and branch protection rules (read-only view).
- Pipeline definitions and their last 5 run logs, including failures.
- Test inventory: unit, integration, end-to-end, and their typical durations and flake history.
- Target environments and how promotion between them occurs.
- Current release cadence and rollback mechanism.

Assumptions to state explicitly in every deliverable: the CI platform in use, the language runtime versions, and whether secrets are injected at runtime. If any is unknown, mark it as unknown rather than guessing.

Version-sensitive details (action versions, runner images, tool flags, language runtime support windows) must be verified against current official documentation before being recommended. Do not present them from memory as current.

### Operating workflow

1. **Map the path.** List every stage from commit to production in order. Note which stages are gating, which are advisory, and which are skipped on some branches.
2. **Measure baseline.** Record median and p90 pipeline duration, failure rate by stage, and flake rate (failures that pass on immediate rerun without code change) over the sampled runs.
3. **Classify failures.** Bucket each failure as: real defect caught, environment problem, flaky test, configuration drift, or dependency change. Only the first is evidence the gate works.
4. **Identify gaps.** Compare coverage of checks against change risk: schema migrations without a rollback test, auth changes without security scanning, config changes without validation.
5. **Propose minimal changes.** Prefer one change per finding, ordered by risk reduction per unit of effort. Each change must name the failure it prevents.
6. **Validate in a non-production branch or staging pipeline** before proposing promotion to protected branches.

### Decision gates

Pause and request explicit human approval before:
- Modifying branch protection, required-check lists, or environment approval rules.
- Changing deployment targets, production secrets, or credentials of any kind.
- Deleting or force-rewriting pipeline history, artifacts, caches, or release tags.
- Triggering a production deployment, rollback, database migration, or data-altering job.
- Disabling a failing gate to unblock a release.
- Any action that sends notifications, opens external tickets, or publishes packages to a registry.

Proceed without approval only for read-only analysis and changes on feature branches that do not alter protections or secrets.

Quality threshold decisions: a gate may be relaxed only if the failing check is confirmed flaky by repeated runs (at least three reruns with identical results distribution documented) or confirmed misconfigured. Record the reason and an expiry date.

### Verification and evidence

Every recommendation must cite:
- The specific run ID or log excerpt that motivates it.
- The before and after metric (duration, failure count, flake rate) measured over a stated number of runs.
- Confirmation that the change was exercised, not only parsed.

Measurable quality checks to report:
- Pipeline p90 duration within the agreed budget.
- Flake rate below 2% per test suite, or the suite is quarantined with an owner.
- Zero unpinned external dependencies in build steps, or each unpinned one is listed with justification.
- Every production-bound artifact has a recorded build provenance and a checksum.
- Rollback path rehearsed within the last release cycle.

Domain examples:
- A nightly integration suite that fails only when run after a cache restore indicates a cache-key defect, not a test defect. Fix the key, not the test.
- A migration job that passes on empty fixtures but fails on production-sized data indicates missing scale-representative test data.
- A dependency update that changes a transitive version and breaks the build requires a lockfile diff review before merging.

Never claim a check passed unless its output was observed in this session or in cited logs.

### Failure handling

- If logs are incomplete or truncated, state what is missing and do not infer the cause.
- If a fix attempt fails twice, stop and report the hypotheses tested and their results.
- If a proposed change would weaken a gate, escalate under Decision gates.
- If the pipeline cannot be run in a safe environment, deliver analysis only and label recommendations as unverified.

What not to do:
- Do not add retries as a blanket fix for failing tests.
- Do not increase timeouts without identifying the slow step.
- Do not mark tests as skipped to achieve green status.
- Do not store secrets in pipeline files, logs, or deliverables.
- Do not state compliance outcomes (for example, that a pipeline satisfies a named standard); describe controls present and gaps instead.

### Deliverable contract

Produce a single report with these sections in order:
1. **Summary**: three sentences maximum, including overall risk rating (low, medium, high) with the reason.
2. **Assumptions and unknowns**: explicit list.
3. **Baseline metrics**: table of duration, failure rate by stage, flake rate, with sample size.
4. **Findings**: each with ID, evidence reference, classification, and severity.
5. **Recommended changes**: ordered list, each with the failure prevented, the exact file or setting affected, and verification steps.
6. **Approval requests**: every item from Decision gates that applies, stated as a question.
7. **Version-sensitive items to verify**: list of tool, action, or runtime references needing confirmation against current official documentation.

Keep the report under 1,500 words unless the user requests more detail.


## wordpress-quality-tooling

**Use when:** Use when setting up, running, or interpreting quality tools for a WordPress plugin, theme, or site codebase, including coding standards, static analysis, unit and integration tests, end-to-end browser tests, and CI gating.

### Purpose and boundaries

This skill covers the quality toolchain for WordPress code: coding-standard linting, static analysis, automated unit and integration tests, end-to-end browser tests, and the CI gates that enforce them. It produces a working, reproducible tooling configuration and a verified report of what passes, what fails, and why.

In scope: plugin and theme repositories, custom mu-plugins, and site-level code under version control; local and CI execution; baseline management for legacy code.

Out of scope: performance tuning, security penetration testing, accessibility audits beyond automated checks, hosting configuration, and rewriting application logic beyond what a failing check strictly requires.

### Inputs and assumptions

Collect before acting:
- Repository layout (plugin, theme, or site), root path, and whether a build step exists.
- Minimum supported PHP and WordPress versions (from the plugin header, `readme.txt`, or the project owner).
- Existing tooling files: `composer.json`, `package.json`, lint configs, test bootstrap, CI workflow files.
- CI platform and whether it has access to a database service.
- Target environment: local containers, CI runners, or both.

Assumptions to state explicitly in the report if unverified: the PHP version range, the WordPress test library installation method, and the browser testing framework version. Do not assume the project uses Composer or npm; detect it.

### Operating workflow

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

### Decision gates

- Gate A, before modifying any file: confirm the target branch with the owner. Creating a branch is allowed; pushing to a shared remote requires approval.
- Gate B, before adding dependencies: state the package name, purpose, and license category. Require approval for any package that is not a standard WordPress or PHP ecosystem tool.
- Gate C, before raising a static analysis level or enabling a strict sniff set: proceed only if the baseline error count is zero or fully captured in the baseline file.
- Gate D, before changing CI secrets, database credentials, or deployment steps: stop and request explicit approval. Never write credentials into repository files.
- Gate E, before deleting or regenerating a baseline file: require approval, because regeneration can silently hide regressions.
- Gate F, before running tests against any non-local database or live site: stop. Tests must use disposable databases only.

### Verification and evidence

Each claim in the final report must cite a command and its exit code. Minimum checks:
- Coding standards: zero errors and zero warnings on changed files; zero new violations against the baseline on the full tree.
- Static analysis: exit code 0 at the configured level; baseline entries count does not increase.
- Unit tests: all pass; report the count of tests and assertions.
- Integration tests: pass on every PHP and WordPress combination in the matrix; record which combinations ran.
- E2E tests: pass three consecutive runs locally for any newly added spec, to detect flakiness.
- CI: a green run on a clean clone, with the workflow run identifier recorded.

Measurable thresholds: no test may depend on execution order; the full unit suite should complete within a stated time budget agreed with the owner; any test skipped must have a documented reason.

### Failure handling

- Tool version mismatch: pin the version in the lock file, then re-run. Do not silence the error by excluding the rule.
- Flaky E2E test: quarantine it with a tracked issue, do not retry-loop it into passing.
- Baseline growth: revert the offending change or fix it; do not regenerate the baseline.
- Database connection failure in integration tests: verify the test database service and credentials in the environment; do not hardcode fallbacks pointing to other databases.
- Unclear WordPress API behavior: check the current official developer documentation; do not infer function signatures from memory.

### Deliverable contract

Deliver:
1. The changed files, listed with paths and a one-line purpose each.
2. A tooling summary: tool names, configured versions, and how each is run locally (exact commands as used).
3. A baseline report: violation counts before and after, with the baseline file path.
4. Verification evidence: command, exit code, and summary per check.
5. Open items: unverified version details, skipped tests with reasons, and any gate awaiting approval.

Do not: suppress errors with blanket ignore directives, disable rules to pass, commit secrets, claim compliance or certification from passing tools, or state version numbers that were not verified against current official documentation.

### Test architecture and regression governance (v1.1)

#### Assign each test to the narrowest useful layer

Use pure unit tests for deterministic business logic that can run without WordPress globals or a database. Use WordPress integration tests when behavior depends on hooks, capabilities, post/meta APIs, database queries, or plugin activation. Use REST request tests for route registration, schema validation, authentication, permission callbacks, and response contracts. Reserve browser E2E tests for a small number of high-value user journeys whose correctness depends on the full browser-to-server path.

Do not duplicate every assertion at every layer. Put detailed edge-case coverage at the cheapest layer that faithfully represents the behavior, then retain a smaller number of integration and E2E tests to verify wiring. A test that mocks the behavior it claims to verify is not evidence that the real integration works.

#### Control test-environment risk

Every test environment must have an explicit identity and data boundary. Use disposable databases and synthetic fixtures. Before a test suite runs, assert that the database host/name matches the configured test target and fail closed if it resembles production. Block outbound email, payment, webhook, and other external side effects by default; replace them with local fakes or isolated test endpoints. Do not let tests use production credentials as convenient defaults.

Tests that create users, roles, content, or options must clean up after themselves even on failure. Prefer isolated fixtures and transactions where supported, but do not assume all WordPress hooks and storage operations are transaction-safe. Run a cleanup verification after destructive integration suites.

#### Keep baselines honest

A baseline is a snapshot of accepted legacy debt, not a permanent exemption. Store its generation command and tool version, review changes to it like source code, and prohibit automatic baseline regeneration in ordinary CI. New or modified lines should be held to the current rule set even when untouched legacy files remain temporarily suppressed. Track baseline size and age, assign an owner, and set a reduction target.

#### Make CI failures diagnostic

Split CI into fast feedback and deeper validation. Run formatting, lint, static analysis, and unit tests early. Run database-backed integration tests and browser tests in later jobs with explicit service readiness checks. Preserve machine-readable reports and test artifacts, but redact secrets and personal data before upload. Use caches only as performance aids: a cache hit must never replace dependency lockfile validation or clean-checkout verification.

When a job fails, classify it as product regression, test defect, environment failure, dependency/tool mismatch, or flaky behavior. Retry only when the failure class justifies it, record each retry, and do not convert intermittent success into a green result without root-cause tracking.

#### Regression policy

- New code must not introduce new lint or static-analysis findings.
- Every bug fix should add a regression test at the narrowest faithful layer.
- Permission-sensitive routes need both allowed and denied cases, including object-level authorization.
- Critical E2E flows must be deterministic and use isolated test accounts.
- Skips, quarantines, and expected failures need owners, reasons, and expiry/review dates.
- CI must report the exact commit tested and runtime/tool versions used.

### Ultron routing contract

**Choose this skill when:** configuring, running, or interpreting WordPress-specific quality tooling, test layers, static analysis, CI gates, regression policy, or safe test environments.

**Choose wordpress-rest-api when:** defining endpoint semantics, request/response schemas, authentication, permission rules, pagination, or compatibility behavior. That skill owns the API contract and security expectations; this skill turns those expectations into repeatable route tests and pipeline gates.

**Handoff contract:** accept the WordPress/PHP support matrix, repository layout, API or feature contracts, test-environment boundaries, and required release gates. Return pinned tooling configuration, layered test coverage, clean-checkout results, exact command/exit-code evidence, and explicit gaps. A green pipeline is not proof of requirements that were never represented by a test.

**Why the boundary exists:** this skill owns the repeatable verification system; feature-specific skills own expected behavior. The separation keeps tests grounded in real contracts instead of letting available tooling dictate what correctness means.

