---
name: discrete-logic
description: Use when analyzing, designing, or verifying discrete logic in physics or mathematics work, including Boolean and digital circuit reasoning, combinatorial state spaces, finite automata and transition systems, discrete-time or lattice models, and proofs over finite or countable structures.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Discrete Logic

## Purpose and boundaries

This skill guides rigorous work on problems whose state spaces are finite or countable: propositional and Boolean logic, combinatorial enumeration, finite-state and transition models, discrete-time simulation logic, lattice and spin-model bookkeeping, and discrete proofs (induction, pigeonhole, invariants, bijections). It produces verified formulas, truth tables, state machines, proof sketches, or counterexamples.

It does not cover continuous-field analysis, numerical-stability tuning of floating-point solvers, or hardware sign-off for fabricated chips. Hand those to the appropriate continuous or engineering skill.

## Inputs and assumptions

Before working, establish and write down:

1. The exact statement to prove, compute, or implement, in one sentence.
2. The domain: variables, their finite ranges, and the universe (e.g., bits, integers mod n, graph vertices).
3. Operators and their semantics. State conventions explicitly when ambiguous (e.g., XOR as exclusive or, implication as material conditional, whether 0 is natural).
4. Constraints: which states or transitions are forbidden, reachable, or initial.
5. The output form required: proof, table, minimal expression, count, automaton, or code.

If any item is missing and cannot be inferred without guessing, ask. Do not assume a convention that changes the answer.

## Operating workflow

1. **Formalize.** Restate the problem as symbols, sets, and relations. Name every variable with its type.
2. **Size the space.** Compute the number of cases. If it is at most about 2^16 assignments, enumerate exhaustively; otherwise reason structurally.
3. **Choose a method.** Truth tables for small propositional problems; Karnaugh or Quine–McCluskey for minimization; BFS/DFS on the transition graph for reachability; induction or invariants for infinite families; bijective counting or generating functions for enumeration.
4. **Derive.** Keep each step justified by a named law (De Morgan, distributivity, induction hypothesis, pigeonhole). Avoid unnamed leaps.
5. **Cross-check.** Verify by a second method (see Verification).
6. **Report** in the deliverable contract format.

## Decision gates

- **Gate A (scope):** If the problem mixes discrete and continuous quantities, isolate the discrete component and state what is excluded before proceeding.
- **Gate B (method):** If the exhaustive space exceeds about 2^20 cases and no structural argument exists, stop and report the need for a search tool or a restricted subproblem. Do not claim exhaustive coverage.
- **Gate C (equivalence claims):** Only assert two formulas or machines are equivalent after a truth-table or bisimulation check over the full space, or a complete proof.
- **Gate D (external impact):** Writing files outside the working artifact, executing code against shared systems, or publishing results requires explicit user approval. Destructive edits to existing artifacts also require approval.

## Verification and evidence

- Truth tables: row count must equal 2^n; spot-check at least three rows against the original expression.
- Minimization: the simplified form must match the original on every row, and the cover must be irredundant.
- Reachability: report the number of reachable states and show one witness path per claimed reachable state class.
- Counting: verify with a small-n brute force; the formula must match for n = 1 to 4 at minimum.
- Induction: state the base case, hypothesis, and step explicitly; check that the step uses the hypothesis.
- Counterexamples: give the concrete assignment or trace and evaluate it step by step.

Mark any claim that depends on a specific tool version, library function, or standard convention as "verify against current official documentation."

## Failure handling

- If a truth table disagrees with the claimed identity, report the first differing row and stop; do not adjust the claim to fit.
- If induction fails at the step, identify the gap and test whether the statement is false for small n.
- If a state space is larger than the method can handle, reduce by symmetry or invariant, and state the reduction as an assumption.
- If the problem statement is ambiguous, list the two readings, solve both briefly, and ask which applies.

## Deliverable contract

Return:

1. **Statement** restated in formal notation.
2. **Assumptions** and conventions used.
3. **Result** (formula, count, proof, automaton, or counterexample).
4. **Evidence**: method used, number of cases checked, and the cross-check performed.
5. **Limits**: what was not covered and what requires verification against current documentation.

Do not present a result as proven when only sampled. Do not omit failed cases that were found during checking.