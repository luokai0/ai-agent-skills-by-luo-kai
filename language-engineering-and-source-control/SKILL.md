---
name: language-engineering-and-source-control
description: Use when designing, modifying, or reviewing language tooling (parsers, grammars, DSL syntax, compilers, interpreters, formatters, linters, language servers) or when organizing, branching, reviewing, or recovering history in a source repository that contains such tooling.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Language Engineering And Source Control

## Purpose and boundaries

This skill covers two linked concerns: (1) changing language artifacts (grammar, syntax definitions, parser and lowering code, type or semantic rules, code generators, diagnostics, formatters) safely, and (2) managing the repository history and workflow those changes travel through. It does not cover product feature design unrelated to the language, general infrastructure, or deployment of runtime services. Use it for work where a syntax or semantic change can break existing source files, downstream tools, or published packages.

## Inputs and assumptions

Before acting, establish:

- The language version or grammar revision in scope and whether it is published.
- A corpus of representative source files (valid and invalid) with expected outputs.
- The branching model in use and the protected branches on the remote.
- Who consumes the output: editors, build systems, external users, or other teams.
- Whether the repository has history that must be preserved for audit or for other clones.

If any of these are unknown, state the assumption explicitly in your output. Do not infer remote permissions or release schedules.

## Operating workflow

1. Inspect current state. Record the branch, uncommitted changes, and whether the working tree is clean. Do not stash, reset, or discard changes you did not create.
2. Reproduce the behavior. Run the existing parser or test suite against the corpus and capture the baseline output.
3. Classify the change: additive (new construct that previously was a syntax error), behavioral (existing valid input now parses or evaluates differently), or breaking (previously valid input is rejected or changes meaning).
4. Make the smallest change that satisfies the classification. Keep grammar edits, generated files, and hand-written logic in separate commits.
5. Regenerate derived artifacts with the project's documented generator. Commit generated output only if the project tracks it, and confirm the generator version matches the one recorded in the repository.
6. Add corpus cases: one positive case, one negative case, and one boundary case per new construct.
7. Commit in logical units with messages that state the language-level effect (for example, "Reject bare trailing commas in list literals; previously parsed as empty element").
8. Prepare the branch for review: rebase onto the current base only if the branch is private and unpublished; otherwise merge the base.

## Decision gates

Stop and request explicit approval before any of the following:

- Force-pushing, rewriting published history, or deleting branches or tags on a shared remote.
- Changing a grammar or semantic rule classified as breaking, or any change that alters the meaning of existing valid programs.
- Publishing, tagging a release, or uploading a package or grammar to an external registry.
- Editing protected branch settings, CI secrets, or signing configuration.
- Regenerating and committing artifacts that other teams consume without a version bump.
- Deleting corpus files, golden outputs, or test cases to make a suite pass.

For breaking changes, the required record is: affected constructs, migration example, and the version number under which the break ships. Confirm the version scheme with the maintainers rather than choosing one.

## Verification and evidence

A change is complete only when:

- The full corpus produces the expected output; any diff from baseline is listed and justified.
- Round-trip checks pass where the language supports printing and reparsing: parse, print, reparse yields an equivalent tree.
- Error recovery is tested: invalid input yields diagnostics with correct locations and does not crash or hang. Include at least one input that is truncated mid-token.
- Generated code is reproducible: regenerating from a clean checkout produces no diff.
- The commit history reads cleanly and each commit builds and passes its own tests where feasible.

Report results as counts: corpus cases passed, cases changed from baseline, diagnostics added or removed. Do not claim performance improvements or coverage figures without measuring them in the same environment.

## Failure handling

- If the baseline already fails, do not start the change. Report the pre-existing failure with its reproduction steps.
- If a generator fails or produces a different diff than the committed output, stop and identify the tool version difference. Do not hand-edit generated files to match.
- If a merge conflict touches grammar tables, resolve by regenerating from the merged grammar, not by merging generated text.
- If a test is flaky, record its failure rate across repeated runs and treat it as failing until diagnosed.
- If a history rewrite was accidental, stop, record the reflog or remote state, and ask for approval before any recovery action.

## Deliverable contract

Return:

1. A summary of the change classification (additive, behavioral, or breaking) with one-sentence justification.
2. The list of commits with their purpose.
3. The corpus results: pass counts, baseline diffs, and new cases added.
4. Any version-sensitive tool, generator, or dependency detail marked "verify against current official documentation."
5. A list of pending approvals required before merge or release.
6. Explicit assumptions and open questions.

Do not include unverified benchmark numbers, invented command flags, or statements that a change is compliant with any standard.