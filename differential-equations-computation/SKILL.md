---
name: differential-equations-computation
description: Use when solving, analyzing, or numerically approximating ordinary or partial differential equations for physics or mathematics work, including model setup, boundary and initial conditions, analytic solution checks, stability and convergence assessment, and reporting of numerical results.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Differential Equations Computation

## Purpose and boundaries

This skill governs the end-to-end computation of solutions to ordinary differential equations (ODEs) and partial differential equations (PDEs) arising in physics and applied mathematics: classical mechanics, heat and diffusion, wave propagation, fluid flow at the model level, electrostatics, population and reaction kinetics, and control systems.

In scope: formulating the problem well-posedly, choosing an analytic or numerical method, implementing or checking a solution, verifying accuracy, and reporting results with uncertainty.

Out of scope: proving new existence theorems, production simulation of safety-critical systems (requires a qualified engineering review), and any task that would run code or access data outside the user's stated environment without explicit approval.

## Inputs and assumptions

Before computing, confirm and record:

1. The governing equation(s), with every term defined and units stated.
2. Dependent and independent variables, domain, and dimensionality.
3. Boundary conditions (type: Dirichlet, Neumann, Robin, periodic) and initial conditions, each with a value or function.
4. Parameter values with units and source or assumption label.
5. Required output: closed form, a value at a point, a trajectory, a field, or a convergence study.
6. Accuracy target (e.g., relative error below 1e-6, or qualitative shape only).

If any item is missing, state the assumption explicitly and flag it. Do not silently pick parameter values.

## Operating workflow

1. **Classify the problem.** Order, linearity, coefficient type (constant or variable), dimension, and time dependence. A linear constant-coefficient ODE gets characteristic-equation treatment; a nonlinear or variable-coefficient problem gets a numerical or series approach first.
2. **Check well-posedness.** Count conditions against order: an nth-order ODE needs n conditions at the same point (initial value) or at boundary points (boundary value). For PDEs, verify the boundary-condition type matches the equation class (elliptic, parabolic, hyperbolic).
3. **Non-dimensionalize** where scales are clear. This reveals the governing dimensionless groups and reduces parameter sweeps.
4. **Attempt an analytic solution** when the structure allows (separation of variables, integrating factors, Laplace transforms, Green's functions, method of characteristics). Stop and record why if the attempt fails.
5. **Select a numerical method** if needed:
   - Non-stiff ODE: adaptive Runge–Kutta or a comparable explicit solver.
   - Stiff ODE: implicit or stiff-aware solver.
   - Elliptic PDE: finite differences, finite elements, or spectral methods depending on geometry.
   - Parabolic/hyperbolic PDE: check the CFL-type stability condition before choosing step sizes.
6. **Implement** with the minimum code needed. Check the exact function names and signatures of any library against its current official documentation, since these change between versions.
7. **Run verification** (see below) before reporting any number.
8. **Write the deliverable** using the contract below.

## Decision gates

- **Gate A (well-posedness):** Proceed only if the condition count and type are consistent. Otherwise stop and request the missing condition.
- **Gate B (analytic vs. numeric):** Use closed form if it is verified by substitution and matches a limiting case. Otherwise go numeric.
- **Gate C (stability):** For explicit time-stepping, confirm the step size satisfies the stability bound for the discretization. If the problem is stiff and the step size is forced very small, switch to an implicit method.
- **Gate D (convergence):** Accept results only after a refinement study shows the error decreases at the expected order. If not, do not report the value as converged.
- **Gate E (external impact):** Any action that writes files outside the working directory, overwrites prior results, submits jobs to shared compute, sends data externally, or uses personal or restricted data requires explicit user approval first.

## Verification and evidence

Apply these checks and record the outcome:

- **Substitution check:** Plug the analytic or numeric solution back into the equation; residual should be at machine-level or discretization-level tolerance.
- **Boundary and initial condition check:** Evaluate the solution at each boundary and at t=0; report the maximum deviation.
- **Limiting-case check:** Reduce a parameter (e.g., damping to zero, domain to infinity) and compare against a known result.
- **Conservation check:** Where physics implies it (energy, mass, charge), report drift over the simulation.
- **Grid or step refinement:** Halve the step size (or double resolution) and report the change; estimate observed order as log2 of the error ratio.
- **Independent cross-check:** Where feasible, solve with a second method and compare.

Report every check with its numeric result, not a qualitative word such as "good."

## Failure handling

- **Divergence or blow-up:** Reduce the step size, check the stability bound, verify sign conventions in source terms, and confirm boundary conditions are not inconsistent with the initial data.
- **Non-convergence under refinement:** Suspect a bug, a discontinuity not resolved by the grid, or a singularity. Locate it before tuning tolerances.
- **Mismatch with analytic check:** Assume the implementation is wrong first, then the derivation, then the model.
- **Ambiguous input:** Stop and ask rather than guessing parameters or condition types.

## Deliverable contract

Every result must include:

1. Problem statement with equation, domain, conditions, and parameters with units.
2. Method used and the reason for choosing it (including why analytic was rejected if applicable).
3. Result with stated accuracy, error estimate, and the verification checks above with their numbers.
4. Assumptions list and any unverified version-sensitive tool details flagged for checking against official documentation.
5. Limitations, including regimes where the model or method is not valid.

## What not to do

- Do not report a numerical value without a convergence or residual check.
- Do not present a stiff problem's explicit-solver output as accurate without a step-size study.
- Do not invent library functions, flags, or version numbers; mark them for verification.
- Do not claim physical validity beyond the stated model.
- Do not run jobs, overwrite files, or transmit data without approval under Gate E.