---
name: analysis-topology
description: Use when a task requires verifying or applying topological arguments in mathematics or physics, such as checking continuity, compactness, connectedness, or manifold claims, computing homotopy or homology invariants, or interpreting winding numbers, Chern numbers, or other topological invariants in a physical model.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Analysis Topology

## Purpose and boundaries

This skill covers rigorous topological reasoning used in analysis, geometry, and theoretical physics: point-set topology, metric and topological continuity, compactness and connectedness, manifolds, fundamental groups, homology, and the invariants physicists extract from them (winding numbers, Chern numbers, Z2 indices, Berry phases, band topology). It supports three activities: checking a topological claim, computing an invariant, and mapping a physical system onto a topological framework.

It does not cover numerical convergence of solvers, general measure theory, or empirical claims about real materials. Those require other skills or specialist review.

## Inputs and assumptions

Before reasoning, establish and state:

1. **The space**: its underlying set, the topology (open-set definition, metric, or induced structure), and any separation axioms assumed (Hausdorff, second countable, paracompact).
2. **The maps**: domain, codomain, and regularity class (continuous, smooth, holomorphic).
3. **The claim**: the exact statement to verify, with quantifiers.
4. **The physical model, if any**: Hamiltonian or action, symmetry group, boundary conditions, parameter space, and the gap condition under which invariants are defined.
5. **The scalar field and dimension.**

If any item is ambiguous, list the candidate interpretations and resolve each, or ask. Never silently choose a topology or a smoothness class that changes the answer.

## Operating workflow

1. **Restate the claim** in one formal sentence with all quantifiers explicit.
2. **Identify the governing theorem family**: intermediate value and connectedness arguments, Heine-Borel or Tychonoff for compactness, covering-space or van Kampen for fundamental groups, Mayer-Vietoris or cellular homology for homology, Stokes-type or Gauss-Bonnet-type integrals for Chern and Euler characteristics.
3. **Check every hypothesis** of that theorem against the stated space. Record pass, fail, or unknown for each.
4. **Compute or construct the object**: explicit open cover, explicit loop, explicit chain complex, or explicit integral over a closed parameter manifold.
5. **Test with a boundary case**: a trivial map, a degenerate parameter, or a dimension-one reduction.
6. **Cross-check by a second route** where possible (for example, winding number computed both as an integral and as a count of zeros with signs).
7. **State the conclusion with its exact scope**, including what was not established.

## Decision gates

- **Gate A (hypotheses):** If any hypothesis of the applicable theorem is unverified, do not assert the conclusion. Either prove the missing hypothesis or downgrade to a conditional statement.
- **Gate B (invariance):** An invariant may be reported as a property of a physical system only if the gap or regularity condition that makes it well defined holds across the entire parameter path. If the gap closes anywhere on the path, report the invariant as undefined there and say so.
- **Gate C (integrality):** A Chern number or winding number must evaluate to an integer within numerical or symbolic tolerance. A non-integer result indicates a flaw in the setup, not a finding.
- **Gate D (scope escalation):** If the result will be used for experimental prediction, engineering design, or publication of a physical claim, require explicit review by a domain specialist before it is presented as established.

## Verification and evidence

Each result must come with:

- The hypothesis checklist with status for each item.
- The explicit construction (cover, loop, cycle, or integrand) used.
- At least one independent check (alternative method, known special case, or symmetry argument).
- For physics invariants: the gap value on the path, the integration domain, and the discretization or limit used if numerical.

Measurable checks: the Chern number is integer-valued to within 1e-6 relative error under refinement, or the discrepancy is explained; winding numbers match the zero-count formula; Euler characteristic from a cell count matches the alternating sum of homology ranks.

## Failure handling

- **Hypothesis fails:** Report the specific failed hypothesis and the counterexample if one exists. Propose the weakest corrected statement that holds.
- **Non-integer invariant:** Re-check the gap, the orientation convention, the branch cut, and the integration grid before reporting anything.
- **Conflicting routes:** Locate the first step where they diverge. Do not average results.
- **Insufficient information:** Stop and list the missing inputs from the section above.

## Deliverable contract

Return:

1. Formal restatement of the claim.
2. Hypothesis table (hypothesis, status, justification).
3. Construction and computation, step by step.
4. Verification checks with results.
5. Conclusion with explicit scope and unresolved items.
6. Any items requiring approval under Decision Gate D.

## What not to do

- Do not assume compactness, Hausdorffness, or smoothness without stating it.
- Do not report a physical invariant from a single parameter point.
- Do not round or force an integer invariant.
- Do not cite theorem names or numerical results from memory without flagging them for verification against the primary reference.
- Do not state software function names, flags, or library versions from memory; mark any version-sensitive detail for verification against current official documentation.
- Do not present conditional results as unconditional.
- Do not take any external action (publishing, submitting results to third parties, altering shared files or data) without explicit user approval.