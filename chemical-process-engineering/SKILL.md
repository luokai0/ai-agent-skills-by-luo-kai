---
name: chemical-process-engineering
description: Use when designing, reviewing, simulating, or troubleshooting chemical process flowsheets, unit operations, mass and energy balances, equipment sizing, process safety reviews, or process control strategies for continuous or batch chemical plants.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Chemical Process Engineering

## Purpose and boundaries

This skill guides engineering analysis of chemical process systems: material and energy balances, unit operation selection and sizing, thermodynamic feasibility, flowsheet integration, preliminary hazard identification, and control-structure review.

In scope: steady-state and short-horizon dynamic analysis, screening-level equipment sizing, reactor and separation selection, utility and heat integration, and HAZOP-style prompts.

Out of scope: final stamped design, pressure-vessel code calculations that require a licensed engineer of record, regulatory filings, and operating instructions for live plants. Outputs are engineering analyses for review by a qualified professional.

## Inputs and assumptions

Before analysis, collect or explicitly assume:

1. Basis: production rate, feed composition, feed temperature and pressure, product specifications, operating hours.
2. Thermodynamic model and property source (e.g., equation of state, activity model). State the model; do not assume ideality for polar, associating, or high-pressure systems.
3. Kinetics or reaction stoichiometry, with source and temperature range.
4. Constraints: materials of construction, utilities available, site elevation, environmental limits.
5. Units. Convert everything to one consistent system and record it.

Label every assumption as **[A]** with a short justification. Unlabelled assumptions are defects.

## Operating workflow

1. **Define the basis and closure.** Write the overall mass balance for each component. Confirm degrees of freedom: count streams, variables, and specifications. A flowsheet with more specifications than degrees of freedom is over-constrained; flag it.
2. **Screen thermodynamics.** Check phase behavior at operating conditions. Identify azeotropes, two-phase regions, and decomposition or polymerization risk.
3. **Select unit operations.** Compare candidates on separation difficulty (relative volatility, feed-to-product ratio), energy demand, and fouling. Prefer simpler equipment when performance is equivalent.
4. **Perform balances unit by unit.** Compute outlet streams, duties, and recycle loops. Iterate recycles to a stated tolerance (for example, 0.1% on the recycled flow).
5. **Size equipment at screening level.** Use standard correlations and state their source. Examples: flash drum vapor disengagement, heat exchanger LMTD with a correction factor for multipass units, column diameter from flooding fraction (target typically 70–80% of flood).
6. **Integrate energy.** Build a pinch-style summary of hot and cold streams with a stated minimum approach temperature (ΔTmin). Report utility demand before and after integration.
7. **Review control and safety.** Propose a control structure with controlled, manipulated, and measured variables. Run a HAZOP-style deviation review (more/less/no/reverse/other) on critical nodes.
8. **Document.** Produce the deliverable contract below.

## Decision gates

- **Gate 1 (basis):** Do not proceed past balances if feed composition or a product specification is missing. Request it.
- **Gate 2 (thermodynamics):** If the chosen property model is outside its validated range (pressure, temperature, composition), stop and recommend experimental data or a validated model.
- **Gate 3 (separation):** If relative volatility is below about 1.05 in distillation, consider extractive or azeotropic distillation, membranes, or crystallization before accepting conventional columns.
- **Gate 4 (safety):** Any reactor with exothermic reaction, flammable inventory above screening thresholds, or high-pressure operation requires a formal PHA (HAZOP, LOPA) before results are used. Recommend this; do not declare the design safe.
- **Gate 5 (approval):** Explicit user approval is required before issuing anything that changes equipment specifications, operating setpoints, or safety interlocks, and before any output that would be sent to a regulator, vendor, or operator.

## Verification and evidence

Check each result with at least one independent method:

- Overall and component balances close within 0.5% (state the actual residual).
- Energy balance closes within 1% of the largest duty.
- Equilibrium stage counts agree with a shortcut method (Fenske–Underwood–Gilliland) within about 20%; larger gaps indicate an error or a poor model.
- Pressure drops are consistent with velocity limits (for example, typical liquid line velocities 1–3 m/s; confirm against project standards).
- Units are dimensionally checked in every equation.

Mark any value taken from memory or a correlation as **[VERIFY]** with the source to check. Property constants, correlation coefficients, code limits, and regulatory thresholds change with version and jurisdiction; confirm them against current official standards or documentation before use.

## Failure handling

- **Balance does not close:** Locate the discrepancy by checking one unit at a time; check recycle initialization, hidden streams (purges, vents, leaks), and unit basis (mass vs. molar).
- **Non-convergence in recycle:** Check the tear stream choice, damping factor, and whether the process has multiple steady states.
- **Model disagreement:** Report both results and the range. Do not average them silently.
- **Missing data:** Stop and list the specific missing items. Do not fill them with plausible values.

## Deliverable contract

Every deliverable contains, in this order:

1. Scope and basis statement with unit system.
2. Assumptions table (ID, assumption, justification, verification status).
3. Flowsheet summary with stream table (T, P, flow, composition).
4. Balance closure results with residuals.
5. Equipment sizing table with method and source for each correlation.
6. Energy integration summary with ΔTmin and utility targets.
7. Risk list from deviation review, with recommended next study (HAZOP, LOPA, control review).
8. Open items and required approvals.

## What not to do

- Do not present screening results as final design or as a safety certification.
- Do not invent property values, kinetic constants, or code requirements.
- Do not use ideal-gas or ideal-solution assumptions at high pressure or for strongly nonideal mixtures without stating the error.
- Do not omit recycle or purge streams from balances.
- Do not change setpoints, interlocks, or specifications without explicit approval.