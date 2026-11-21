---
name: functional-programming-paradigms
description: Use when designing, reviewing, refactoring, or teaching code that relies on pure functions, immutability, function composition, algebraic data types, or effect isolation, including choosing between functional and imperative styles in a mixed-paradigm codebase.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Functional Programming Paradigms

## Purpose and boundaries

This skill guides professional work applying functional programming (FP) principles: referential transparency, explicit data flow, immutable state, algebraic data modeling, and controlled side effects. It covers code design, review, refactoring toward FP patterns, and explaining trade-offs to teams.

In scope: pure function design, data modeling with sum and product types, pipelines and composition, folds and maps over collections, pushing I/O to the edges, error handling as values, and evaluating whether FP idioms fit a given language and team.

Out of scope: language-specific tutorials, performance tuning of runtimes, formal proof development, and rewriting working systems without a stated reason.

## Inputs and assumptions

Before acting, establish:

1. Language and version. Idioms differ across languages and standard library generations. Mark any version-dependent feature for verification against current official documentation.
2. Codebase constraints: existing paradigm mix, team familiarity, linting rules, and runtime characteristics (for example, deep recursion limits or lack of tail-call elimination).
3. The goal: correctness, testability, concurrency safety, readability, or a specific bug class.
4. The code or design under review, in full enough context to trace data flow.

If any input is missing, ask. Do not assume the language supports a construct (persistent collections, pattern matching, tail-call optimization) without checking.

## Operating workflow

1. Map effects. List every function that reads or writes external state: clocks, randomness, files, network, databases, globals, mutable arguments, logging.
2. Classify functions as pure (output depends only on inputs, no observable side effects) or effectful. Record the classification.
3. Model the domain with data. Replace boolean flags and nullable fields with sum types or tagged variants where the language supports them. Replace stringly-typed states with enumerations.
4. Push effects outward. Keep a pure core that computes decisions and returns descriptions of effects; a thin shell executes them. Do not refactor the shell and core in the same change unless tests cover both.
5. Replace mutation with transformation where the cost is acceptable. Prefer returning new values from folds, maps, and reducers. Keep local mutation when it is contained, measured, and clearer.
6. Compose small functions into pipelines. Name intermediate steps when a pipeline exceeds roughly five stages or mixes concerns.
7. Make failure explicit. Represent expected failures as result or option values rather than thrown exceptions inside the pure core.
8. Write tests against the pure core first, with table-driven inputs covering empty, boundary, and invalid cases.

## Decision gates

Proceed with a full FP refactor only when all hold:
- Existing tests cover the target behavior, or new characterization tests are written first.
- The language provides the needed constructs without awkward workarounds.
- The change does not alter a public interface consumed outside the repository, unless approved.

Stop and request approval before:
- Changing serialization formats, database schemas, or wire protocols that other systems read.
- Altering concurrency semantics, such as replacing locks with immutable state sharing, in production paths.
- Deleting or rewriting code in a way that cannot be reverted in one commit.
- Introducing a new library or dependency for persistent data structures or effect systems.

Prefer local FP idioms over architectural conversion when the team lacks shared experience. Recommend a paradigm change only with a written rationale.

## Verification and evidence

Every claimed improvement must be backed by one of:
- Test results showing the pure core passes existing and new cases.
- A demonstrated reduction in the count of functions with hidden inputs or outputs, listed before and after.
- A concrete bug or race condition that the new structure makes impossible, with the reasoning shown.

Measurable checks:
- Count of effectful calls inside functions classified as pure: target zero.
- Every new pure function has at least one test per branch.
- No new shared mutable state introduced.
- Diff review confirms behavior is unchanged for at least one representative production input set, where available.

Do not claim performance gains or regressions without a benchmark run in the target environment. Do not claim compliance or security guarantees from FP structure alone.

## Failure handling

- If a refactor changes test outcomes, revert the smallest unit and isolate the cause before continuing.
- If the language lacks tail-call elimination and recursion depth is a risk, convert to iterative folds or explicit loops and state the change.
- If performance degrades beyond the agreed threshold, restore the prior implementation for the hot path and document the trade-off.
- If an immutable-update pattern causes excessive copying in a large collection, use a contained mutable accumulator inside a pure function and verify that its external behavior is unchanged.
- If a team member rejects the style, present the concrete readability and testability differences with examples rather than arguing principles.

## Deliverable contract

Each delivery includes:
1. A summary of the effect map: which functions were pure, which were effectful, and what changed.
2. The revised code, or a diff, with the pure core and effect shell clearly separated.
3. Test additions and their results, with the exact commands run.
4. A list of open questions, version-sensitive constructs flagged for verification against current official documentation, and any approval requests raised under the decision gates.
5. Known trade-offs, including any performance or readability cost.

What not to do:
- Do not wrap imperative code in FP-named functions without changing its data flow.
- Do not hide I/O inside functions named as pure.
- Do not use monads, effect systems, or type-level machinery to impress; use them only when they remove a concrete defect class.
- Do not invent library functions, flags, or version numbers; verify each against official sources.
- Do not rewrite stable, well-tested imperative code solely for stylistic conformity.