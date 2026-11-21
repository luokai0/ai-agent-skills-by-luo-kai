---
name: classical-mechanics-fields-waves
description: Use when solving, checking, or documenting problems in classical mechanics, electromagnetic fields, or wave phenomena, including derivations, boundary-value setups, dispersion and mode analysis, and numerical verification of analytic results.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Classical Mechanics, Fields, and Waves

## Purpose and boundaries

Use this skill to set up, solve, and verify problems in Newtonian and Lagrangian/Hamiltonian mechanics, rigid bodies, continuum mechanics limited to linear elasticity and fluids at the level of wave propagation, Maxwell's equations in media, and linear wave equations (strings, membranes, acoustics, electromagnetic guides, dispersive media).

Out of scope: quantum treatments, relativistic general theory beyond special-relativistic kinematics, nonlinear turbulence closure, and design sign-off for structures, aircraft, medical devices, or radiation-emitting equipment. For those, produce analysis only and state that a licensed engineer or domain authority must review it.

## Inputs and assumptions

Before solving, record:

- Governing system: particle, rigid body, continuum, or field.
- Coordinates, units system (SI or Gaussian; never mix), and sign conventions.
- Constraints, boundary conditions, and initial conditions, each stated explicitly.
- Material parameters and their validity range (linear, isotropic, lossless, nondispersive, etc.).
- Required output: closed form, numerical value, mode table, dispersion relation, or plot.

If any of these is missing and cannot be inferred without changing the answer, ask. Do not silently assume a medium is lossless or a boundary is perfectly conducting.

## Operating workflow

1. Restate the problem in one paragraph with all assumptions listed.
2. Choose a formulation: Newton for simple force balance, Lagrange when constraints or symmetry dominate, Hamilton for conserved-quantity or canonical analysis, field equations with boundary conditions for wave problems.
3. Nondimensionalize where scales are clear. Identify the small parameter if a perturbation is used.
4. Derive symbolically. Keep intermediate expressions; do not jump to numbers.
5. Check limits: zero coupling, large-time behavior, symmetric cases, known textbook recovery.
6. Verify numerically when a closed form is unavailable or as a cross-check (see Verification).
7. Write the result with units, validity conditions, and an uncertainty or neglected-term statement.

## Decision gates

- **Gate A, formulation:** Use Lagrangian when more than two coupled degrees of freedom or holonomic constraints exist. Use direct Newtonian force balance for single-body problems with clear free-body diagrams.
- **Gate B, linearity:** Linearize only if displacements or fields are small relative to the scale that matters, and state the criterion (e.g., amplitude ratio below a stated threshold). If not justified, solve nonlinearly or bound the error.
- **Gate C, dispersion:** If phase and group velocities differ, report both and specify which governs energy or signal transport.
- **Gate D, numerical method:** Use analytic solution first. Adopt a numerical solver only when the analytic form is intractable, and record discretization, tolerance, and convergence evidence.
- **Gate E, external impact:** Stop and request explicit approval before any result is used for safety-critical design, regulatory filing, publication with third-party data, or overwriting shared simulation or lab files.

## Verification and evidence

- Dimensional analysis of every final expression. Reject any result failing it.
- Conservation checks: energy, momentum, angular momentum, or charge where applicable, with the source of each conserved quantity named.
- Limit recovery: at least two independent limits matching known results.
- Numerical cross-check: agreement within a stated tolerance (for example, relative error below 1% for smooth solutions) and a grid or timestep refinement showing convergence.
- For solver code, record library name and version, and verify all function signatures and option names against current official documentation before use. Do not rely on remembered APIs.
- Report any benchmark or literature value only with its citation; never fabricate reference numbers.

## Failure handling

- If dimensions fail, locate the first inconsistent term and re-derive from that step.
- If a numerical result diverges from analytic limits, reduce timestep or grid spacing, then check boundary implementation before revising physics.
- If conservation is violated beyond tolerance, suspect integrator choice or sign errors in forcing terms.
- If conditions are ambiguous, return a conditional answer with each branch labeled rather than choosing silently.

## Deliverable contract

Every deliverable contains:

1. Problem statement and assumptions table.
2. Derivation with numbered equations.
3. Final result with units and validity range.
4. Verification record: dimensional check, limits checked, numerical tolerance achieved.
5. Open items and neglected effects.
6. Approval status line: "Analysis only; not approved for design or external use" unless a named reviewer has approved.

Do not present unverified results as final. Do not omit validity ranges. Do not claim compliance with any standard or code unless the user supplies the standard text and asks for a check against it.