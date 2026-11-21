---
name: matter-thermal-plasma
description: Use when analyzing, estimating, or verifying properties of thermal (near local thermodynamic equilibrium) plasmas, such as ionization equilibrium, Debye shielding, LTE validity, collisionality, and equilibrium composition for arc, torch, or high-temperature gas problems.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Matter Thermal Plasma

## Purpose and boundaries

This skill supports quantitative analysis of thermal plasmas: partially or fully ionized gases whose electrons, ions, and heavy particles share a common temperature (or near-equal temperatures) and whose composition is governed mainly by collisional equilibrium. Typical cases include atmospheric-pressure arcs, plasma torches, equilibrium composition calculations, and screening estimates for laboratory or process plasmas.

In scope: Saha ionization balance, Debye length and plasma parameter, LTE validity checks, collision and equilibration time scales, order-of-magnitude transport estimates, and dimensional checks on published formulas.

Out of scope: non-equilibrium kinetic modeling (use a kinetic or collisional-radiative model), plasma-wall sheath design for hardware, radiation-safety or operational safety of high-voltage or high-temperature equipment, and any claim of experimental validation without measured data.

## Inputs and assumptions

Before calculating, record:

- Gas species and molecular or atomic data, including ionization energies χ and statistical weights g for each ionization stage.
- Temperature T (state whether it is electron, heavy-particle, or a common value) in K or eV. Use 1 eV ≈ 11604 K as a conversion, and verify this constant.
- Pressure or total number density, and whether the plasma is at atmospheric pressure, reduced pressure, or unspecified.
- Spatial scale L and the characteristic time scale of interest.
- Whether the system is steady, time-varying, or spatially inhomogeneous.

If any of these is missing, state the assumed value explicitly and show how the result changes across a plausible range. Do not silently assume a pressure or composition.

## Operating workflow

1. Normalize all units to SI, then convert to eV or K only at the final evaluation. Write every formula with symbols before substituting numbers.
2. Compute the ionization balance. Use the Saha relation for each adjacent stage pair: n_{i+1} n_e / n_i = (2 g_{i+1} / g_i) (2π m_e k_B T / h²)^{3/2} exp(−χ_i / k_B T). Solve jointly with charge neutrality and total particle density conservation.
3. Compute the Debye length λ_D = sqrt(ε₀ k_B T_e / (n_e e²)) and the plasma parameter N_D = (4π/3) n_e λ_D³. Confirm N_D ≫ 1 for a collective plasma.
4. Evaluate LTE validity using the McWhirter-type criterion: n_e ≥ 1.6 × 10¹² T^{1/2} (ΔE)³ (cm⁻³, T in K, ΔE in eV, largest relevant level spacing). Treat this as a necessary condition, not a sufficient one, and check spatial and temporal gradients separately.
5. Estimate the electron–heavy-particle equilibration time and the collision frequency, then compare with the time and length scales of interest.
6. Record the result with uncertainty propagated from input ranges.

## Decision gates

- **Gate A (collectivity):** If N_D < 10, stop and report that the plasma is not clearly collective; do not apply Debye-based screening conclusions.
- **Gate B (LTE):** If the McWhirter criterion fails by less than a factor of 10, present results as bounds only. If it fails by more, switch to a non-equilibrium method and say so.
- **Gate C (two-temperature):** If electron and heavy-particle equilibration time exceeds the process time, do not use a single temperature in the Saha calculation without justification.
- **Gate D (data provenance):** Atomic data, partition functions, and constants must come from a cited, current source. Mark any value taken from memory as requiring verification.

## Verification and evidence

- Dimensional check: every term in each equation must reduce to the same unit. Report the check result.
- Limit checks: as T → high, ionization fraction must approach 1; as n → high at fixed T, ionization must decrease. Confirm the trend.
- Charge neutrality residual must be below 10⁻⁶ relative after solving.
- Compare against a published tabulated composition at one reference condition. Report the relative difference; flag anything above 5% for review.
- Keep a calculation log with input values, constants used, source of each constant, and software or spreadsheet version if applicable.

## Failure handling

- If the Saha solver fails to converge, check whether χ or g values are mixed between stages, and whether the temperature unit was misread (K versus eV).
- If the result depends strongly on an unknown input, report sensitivity rather than a single number.
- If a required constant or dataset cannot be confirmed, stop and request it. Do not substitute an unverified value.

## Deliverable contract

Each deliverable contains:

1. Statement of problem, assumptions, and scope limits.
2. Equations used, with symbols defined.
3. Input table with units and sources.
4. Results with uncertainty ranges.
5. Gate outcomes (A through D) with pass, bound-only, or fail status.
6. Verification results from the checks above.
7. Explicit list of values requiring verification against current official data.

Do not present results as experimentally validated, guaranteed, or suitable for hardware design without independent review. Do not take any external-impacting, destructive, or irreversible action, such as publishing data or altering shared datasets, without explicit user approval.