---
name: algebra-number-theory
description: Use when a task involves rigorous algebraic or number-theoretic reasoning: groups, rings, fields, Galois theory, modular arithmetic, primes, Diophantine equations, factorization, or computational checks of such claims in physics or mathematics work.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Algebra Number Theory

## Purpose and boundaries

This skill governs the construction, checking, and communication of results in abstract algebra and elementary-to-intermediate number theory. It covers: definitions and structure proofs (groups, rings, ideals, fields, modules at an introductory-to-graduate level); field extensions and Galois correspondence; congruences, residue arithmetic, quadratic reciprocity, and Diophantine problems; and computational verification of these claims, including the algebraic structures that arise in physics (symmetry groups, representation labels, lattice and finite-field models, error-correcting codes, discrete Fourier analysis on cyclic groups).

Out of scope: research-level claims presented as settled without literature check; cryptographic security assessments of real systems; and any statement that a standard result is "new" without evidence.

## Inputs and assumptions

Before working, establish:

1. The exact statement to prove, compute, or check, with all quantifiers and domains explicit (e.g., "for all integers n ≥ 2", "over ℚ", "in ℤ/mℤ").
2. The ambient structure: which group, ring, or field; whether commutative; characteristic.
3. The required output: proof, counterexample, computation, or classification.
4. The rigor level: informal explanation, full proof, or machine-checked argument.
5. Available tools (CAS, proof assistant, language runtime). Record the tool name and version; do not assume a function exists without checking current official documentation.

If any quantifier or domain is ambiguous, state the two most plausible readings and ask which applies before proceeding.

## Operating workflow

1. **Restate.** Write the claim in formal notation. Identify hypotheses and conclusion separately.
2. **Classify.** Determine the technique: direct algebra, induction, descent, Chinese Remainder Theorem, quadratic reciprocity, Galois theory, counting (Burnside/orbit-stabilizer), or computation.
3. **Test small cases.** Check at least three instances, including the smallest nontrivial one and one edge case (0, 1, identity, prime powers, characteristic 2). Record results in a table.
4. **Attempt proof or search for counterexample.** If a counterexample exists in the small-case search, stop and report it before attempting a proof.
5. **Write the argument.** Each step cites a definition, axiom, or previously established lemma. No step relies on "clearly" or "by symmetry" without justification.
6. **Independently verify.** Re-derive key identities by a second method, or compute them with a CAS over exact arithmetic (rationals, integers, finite fields), never floating point.
7. **Package** per the deliverable contract.

## Decision gates

- **Gate A (domain):** If the structure is not specified, stop and request it. Do not assume ℤ.
- **Gate B (counterexample):** If any small case fails, the claim is false as stated unless the hypotheses were misread. Report the failing case first.
- **Gate C (computation vs. proof):** A finite computation establishes only the finite cases checked. Use computation to find patterns, not to claim a general theorem, unless the domain is finite and fully enumerated, in which case state exactly what was enumerated.
- **Gate D (literature):** If the result resembles a named theorem (e.g., Sylow, Dirichlet, Wedderburn, Lagrange), cite the theorem by name and check its hypotheses rather than re-deriving with gaps.
- **Gate E (approval):** Obtain explicit user approval before any action that writes to shared repositories, publishes results, submits to external systems, or uses sensitive data.

## Verification and evidence

Quality checks, all required before delivery:

- Every quantifier and domain stated explicitly.
- Hypotheses used are listed; no unused hypothesis is silently assumed.
- At least three test instances reported with exact values.
- Exact arithmetic used for all computations; the tool and its version recorded.
- Each cited theorem stated with its hypotheses, and each hypothesis checked.
- A second derivation or independent computation agrees with the primary result.
- Any function, library call, or package name is marked "verify against current official documentation" unless confirmed in this session.

## Failure handling

- **Counterexample found:** report the instance, the step where the claim fails, and the corrected statement if one exists.
- **Stuck proof:** state the gap precisely (which lemma is missing), do not hide it with hedged wording, and propose the smallest lemma that would close it.
- **Computation disagrees with hand derivation:** assume an error in one of them until resolved; check indexing, modular reduction, and sign conventions first.
- **Tool unavailable or output ambiguous:** fall back to a hand-verifiable small case and say so.

## Deliverable contract

Return:

1. Formal statement with explicit domain.
2. Result: proof, counterexample, or computed classification, with a status label (Proven / Disproven / Verified-finite / Open-gap).
3. Proof or computation, step-numbered, each step justified.
4. Test-case table with exact values.
5. Verification log: method used, second check performed, tool and version.
6. Assumptions and unverified items listed explicitly.

Do not: round intermediate results; treat a finite check as a general proof; invent theorem names, function signatures, or version features; claim novelty; or present a conjecture as established.