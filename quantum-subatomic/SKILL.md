---
name: quantum-subatomic
description: Use when working on quantum mechanics or quantum field theory calculations for subatomic systems, including particle decays, scattering amplitudes, nuclear states, angular momentum coupling, symmetry and group-theory reductions, and unit or convention checks.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Quantum Subatomic

## Purpose and boundaries

This skill supports rigorous analytical and numerical work on subatomic quantum systems: hadron and lepton decays, two-body and multi-body kinematics, scattering amplitudes at tree level, nuclear shell and angular momentum structure, isospin and flavor symmetry, and Clebsch-Gordan or Wigner coefficient bookkeeping.

It does not cover: experimental data acquisition, detector design, weapons-relevant nuclear engineering, handling of controlled radioactive material, or claims about real-world hazards. Decline and redirect those requests.

## Inputs and assumptions

Before calculating, record:

1. The system: particles or nucleons, their quantum numbers (spin, parity, charge, isospin, flavor, color if relevant).
2. The process and the observable requested (amplitude, width, cross section, branching ratio, spectrum, expectation value).
3. The unit system and metric signature. Default to natural units (ħ = c = 1) only if stated; otherwise carry SI or explicit factors.
4. The approximation level: tree level, leading order, nonrelativistic, perturbative order, or exact diagonalization.
5. Reference constants (masses, lifetimes, couplings). Mark each as sourced from the current Particle Data Group compilation or a named paper with its edition. Constants change between editions; verify against the current official release before reporting numbers.

If any input is missing and affects the result, stop and ask. Do not fill gaps with remembered values.

## Operating workflow

1. Restate the problem in one line with the quantum numbers and conserved quantities checked. Confirm charge, baryon number, lepton number, strangeness or flavor, and angular momentum conservation for each vertex.
2. Choose the formalism: Feynman rules, partial-wave expansion, Hamiltonian matrix, or group-theory reduction. State why.
3. Write the symbolic result before substituting numbers.
4. Track dimensions at every step. Check that the final quantity has the correct units.
5. Reduce angular structure using Wigner or Clebsch-Gordan coefficients. Verify coefficients against a standard table or a computed orthogonality check.
6. Evaluate numerically with stated constants and significant figures matched to input precision.
7. Run the verification checks below, then report.

## Decision gates

- **Gate A (conservation):** If any conservation law is violated at a vertex, stop. Either the process is forbidden or the particle assignment is wrong.
- **Gate B (approximation validity):** Proceed with a perturbative or nonrelativistic expansion only if the small parameter is quantified (for example, coupling constant or v/c). Report the estimate of the neglected term.
- **Gate C (convention):** If the source uses a different sign convention, metric, or normalization for amplitudes or states, convert explicitly before comparing results.
- **Gate D (numerical stiffness):** For matrix diagonalization with near-degenerate levels, require convergence in basis size and report the change.

## Verification and evidence

Each deliverable must include at least three of the following checks, with results shown:

- Dimensional analysis of the final expression.
- Limiting case: recover a known result (for example, a nonrelativistic or massless limit) within stated accuracy.
- Sum rule or unitarity check, such as branching ratios summing to unity within the quoted uncertainty.
- Symmetry check: swap identical particles, apply a parity or charge conjugation transformation, confirm sign behavior.
- Independent recalculation by a second method (different gauge, different basis, or numerical versus analytic).
- Coefficient orthogonality or normalization check.

Quote uncertainties propagated from input constants. Never report more significant figures than the inputs support.

## Failure handling

- If a check fails, locate the first step where the failing quantity departs from expectation; do not adjust constants to force agreement.
- If a required constant or coefficient cannot be verified, label the result conditional and name the missing value.
- If two methods disagree beyond uncertainty, report both and the discrepancy; do not average them silently.
- Version-sensitive details (current PDG values, software library functions, numerical package interfaces) must be marked for verification against current official documentation before use.

## Deliverable contract

Return:

1. Problem statement with quantum numbers and conventions.
2. Symbolic result.
3. Numerical result with units, uncertainties, and significant figures.
4. Verification table listing each check, method, and outcome.
5. Assumptions and open items, including any version-sensitive constants to re-verify.

Do not:

- Invent constants, coefficients, or benchmark numbers.
- Present a tree-level result as exact without stating the truncation.
- Omit sign or phase conventions.
- Claim a result has been validated against experiment unless the comparison data and source are cited.