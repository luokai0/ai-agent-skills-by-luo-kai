---
name: algorithms-core
description: Use when designing, selecting, implementing, reviewing, or debugging algorithms and data structures for correctness, complexity, and performance, including choosing between approaches, proving invariants, and writing tests for edge cases.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Algorithms Core

## Purpose and boundaries

This skill covers the design and validation of algorithms and data structures: problem modeling, choosing a technique (greedy, dynamic programming, graph search, divide and conquer, two pointers, sorting, hashing, heaps, union-find, tries, interval handling), deriving time and space complexity, establishing correctness arguments, and producing tested implementations.

In scope: algorithmic code in any general-purpose language, complexity analysis, benchmark design, correctness reasoning, and reviewing existing algorithmic code.

Out of scope: distributed consensus design, cryptographic primitives (use vetted libraries and specialist review), ML model training, and production capacity planning. If a request reaches those areas, state the boundary and limit the answer to the algorithmic core.

## Inputs and assumptions

Before proceeding, establish:

1. Problem statement with precise input domain, output contract, and error behavior.
2. Scale: expected n, value ranges, memory limits, latency budget, and whether input is streamed or static.
3. Query pattern: one-shot, repeated queries, online updates, or mixed.
4. Language and runtime constraints (recursion depth limits, integer width, standard library availability).
5. Whether exact results are required or approximation is acceptable, and the error tolerance if so.

If any of these is missing and materially changes the choice, state the assumption explicitly and name the input that would invalidate it. Do not assume unbounded input sizes.

## Operating workflow

1. Restate the problem as a formal mapping from inputs to outputs. List edge cases: empty input, single element, duplicates, negative values, overflow, disconnected graphs, cycles.
2. Derive a brute-force baseline and its complexity. This anchors correctness checks and reveals the bottleneck.
3. Identify structure: monotonicity, optimal substructure, overlapping subproblems, sortedness, graph properties (DAG, weighted, nonnegative edges), or a constrained query pattern.
4. Select the technique using the decision gates below. Write down the recurrence, invariant, or greedy-choice argument before coding.
5. Implement with named invariants in comments only where they are non-obvious.
6. Verify (see Verification and evidence), then analyze complexity including constant-factor hotspots such as allocation and cache-unfriendly access.
7. Report the result using the deliverable contract.

## Decision gates

- Greedy: proceed only if you can state an exchange argument or matroid-like property showing local choices extend to a global optimum. If a counterexample exists for a small case, reject greedy.
- Dynamic programming: use when subproblems repeat and the state is small enough. Define the state, transition, base case, and evaluation order. If state space exceeds memory, look for a dimension reduction or switch technique.
- Graph search: BFS for unweighted shortest paths; Dijkstra only with nonnegative weights; Bellman-Ford when negative edges exist and cycles must be detected; topological sort only on DAGs, with cycle detection as a failure path.
- Sorting plus sweep: use when intervals or pairwise relations can be ordered so a single pass suffices. State the sort key and tie-breaking rule.
- Hashing: acceptable for average-case expected bounds. If adversarial input is possible, say so and note the worst-case alternative. Do not claim worst-case O(1) for hash tables.
- Approximation or randomization: require explicit approval from the user before substituting an approximate or probabilistic answer for an exact one.

## Verification and evidence

- Write a brute-force reference and compare against the optimized version on randomized small inputs (for example, several hundred cases with n up to about 10), using a fixed seed so failures reproduce.
- Test the edge cases enumerated in step 1, plus maximal-size inputs for runtime and memory.
- Check invariants at loop boundaries in a debug build.
- For performance claims, measure on the stated scale with warm-up and repeated runs; report median and spread. Never report a speedup without the baseline and hardware description.
- Complexity claims must be derived from the code's operations, not inferred from its shape.
- Mark any language, library, or runtime behavior that is version-sensitive as requiring verification against current official documentation. Do not state library function names, flags, or package versions from memory without that check.

## Failure handling

- Counterexample found: stop, record the input, identify which assumption or invariant failed, and revise the technique rather than patching the output.
- Timeout on target scale: profile first; distinguish algorithmic cost from implementation overhead before changing the approach.
- Stack overflow from recursion: convert to an explicit stack or bottom-up order, and state the depth bound.
- Ambiguous specification (for example, tie-breaking or whether output must be unique): ask before implementing.

## Deliverable contract

Return:

1. The chosen technique and one-paragraph justification referencing the decision gate used.
2. Complexity: time and space, stated as functions of named parameters, with worst-case and average-case distinguished where relevant.
3. Implementation with explicit input validation at the boundary.
4. Test evidence: edge cases covered, randomized comparison result, and any measured runtimes with setup described.
5. Known limitations and the input conditions that would break the solution.

## What not to do

- Do not present a heuristic as exact, or an expected-time bound as a worst-case guarantee.
- Do not skip the brute-force baseline for non-trivial problems.
- Do not invent benchmark numbers, library APIs, or version compatibility.
- Do not change the output contract (ordering, uniqueness, tie-breaking) without explicit confirmation.
- Do not run code that modifies files, consumes external services, or sends data outside the environment without explicit approval from the user.
- Do not delete or overwrite existing project code, test fixtures, or data files without explicit approval.
- Do not add dependencies to a project without approval.