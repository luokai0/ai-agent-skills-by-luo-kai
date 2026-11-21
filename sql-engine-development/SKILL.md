---
name: sql-engine-development
description: Use when designing, implementing, or debugging components of a SQL engine or SQL-compatible query layer, including parsing, binding, logical and physical planning, optimizer rules, execution operators, catalog and storage interfaces, and conformance testing.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Sql Engine Development

## Purpose and boundaries

This skill guides work on the internals of a SQL engine: the pipeline from SQL text to result rows, the contracts between stages, and the tests that prove correctness. It covers parser and AST changes, name resolution and type checking, logical plan rewrites, cost-based or heuristic physical planning, execution operators (scan, join, aggregate, sort, window), and the catalog and storage interfaces the executor depends on.

It does not cover: database administration, cluster operations, schema design for end users, tuning a third-party database's configuration, or writing application SQL. If a request is about using an existing database, redirect to query-writing or DBA guidance.

## Inputs and assumptions

Before changing code, establish:

1. **Target dialect and standard level.** Which SQL standard edition or existing dialect is the reference? Where the engine deviates, record the deviation explicitly. Do not assume behavior from memory for NULL semantics, collation, implicit casts, or integer overflow; check the reference.
2. **Engine stage affected.** Parser, binder, planner, optimizer, executor, catalog, or storage.
3. **Data model.** Supported types, nullability rules, transaction isolation level, and whether the engine is single-node or distributed.
4. **Existing test corpus.** Locate golden-result tests, sqllogictest-style files, or regression suites before editing.
5. **Version-sensitive details.** Any parser generator, library, or external engine version must be verified against its current official documentation. Mark unverified details as such in your output rather than stating them as fact.

## Operating workflow

1. **Reproduce.** Write the smallest SQL statement and expected result that fails. Record the current output and the engine's error path.
2. **Localize.** Dump the AST, bound tree, logical plan, and physical plan at each stage. Identify the first stage where the output diverges from the expected contract.
3. **Specify the contract.** State the invariant the fixed stage must preserve: output schema, column nullability, row ordering guarantees, duplicate semantics, or cardinality.
4. **Change one stage.** Keep parser changes separate from optimizer changes. Do not fix an executor bug by altering the planner unless the plan itself is wrong.
5. **Add tests at three levels.** Unit test for the stage, plan-shape test for the optimizer, and end-to-end result test in the conformance suite.
6. **Check neighbors.** Run the full regression suite, not only the new test. Rewrite rules are especially prone to breaking unrelated queries.
7. **Document the semantics.** Update the dialect deviation list if behavior differs from the reference.

## Decision gates

- **Rewrite rule vs. new operator:** Use a rewrite rule when the transformation is semantically equivalent in all cases the rule matches. Add an operator only when no existing operator can express the semantics. Rules must state their preconditions (e.g., "inner join only," "no volatile functions").
- **Heuristic vs. cost-based choice:** Prefer heuristics when cardinality estimates are unreliable or absent. Introduce cost-based choices only with statistics collection and a fallback path.
- **Pushdown safety:** Push a predicate below an outer join only if it references the preserved side. Push below aggregates only if it references grouping keys. Verify null-rejecting behavior before pushing a filter through a left join.
- **Pausing for approval:** Stop and request explicit approval before any action that deletes or rewrites test baselines, changes the on-disk storage format, alters catalog metadata layout, modifies published wire protocol behavior, or touches data outside the project's test fixtures. These actions are destructive, irreversible, or externally visible.

## Verification and evidence

Report each change with:

- The failing query and the passing query after the change.
- Plan output before and after, for any optimizer change.
- Regression suite results: total tests, passed, failed, and any skipped with reason.
- A list of semantic invariants checked (NULL propagation, three-valued logic, duplicate preservation, ordering).

Measurable checks:

- Zero regressions in the golden result suite.
- For each new rewrite rule: at least one positive test (rule fires and result matches), one negative test (rule correctly does not fire), and one NULL-containing input.
- For each new operator: result equality against a naive reference implementation on randomized small inputs, with a fixed seed recorded.
- Plan-shape tests must assert structure, not incidental text formatting.

Do not claim performance improvements without a benchmark that records input size, hardware, runs, and variance. Do not state benchmark numbers that were not measured.

## Failure handling

- **Result mismatch against reference:** First determine whether the reference or the engine is wrong by consulting the standard or the reference implementation's documented behavior. Record the decision.
- **Rule fires incorrectly:** Disable the rule, confirm the bug disappears, then tighten its preconditions. Never broaden matching to fix a missing case without a correctness argument.
- **Flaky ordering results:** Unordered output is not a guarantee. Add explicit ORDER BY in tests; do not sort results silently in the engine to hide nondeterminism.
- **Stage cannot be isolated:** Fall back to the end-to-end test and bisect commits.

## Deliverable contract

Every completed task returns:

1. **Summary:** One paragraph stating the defect or feature, the stage changed, and the invariant preserved.
2. **Diff scope:** Files and functions modified, listed by stage.
3. **Evidence:** Failing-then-passing queries, plan dumps where relevant, and suite results with counts.
4. **Semantic notes:** Any deviation from the reference dialect, and any unverified version-sensitive detail flagged for checking against official documentation.
5. **Open items:** Remaining risks, and any actions awaiting approval, stated explicitly.

Do not present a change as complete when regression results are missing.