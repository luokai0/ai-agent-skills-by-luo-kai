---
name: thermal-fluid-energy-systems
description: Use when sizing, analyzing, troubleshooting, or documenting thermal-fluid energy systems such as heat exchangers, pumps, piping networks, boilers, chillers, cooling loops, and heat recovery circuits, where hydraulic and thermal performance must be verified against design intent.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Thermal Fluid Energy Systems

## Purpose and boundaries

This skill supports engineering analysis of closed and open thermal-fluid circuits: pumped liquid loops, steam and condensate systems, air-side and water-side heat exchange, boiler and chiller plant, and heat recovery arrangements. It covers steady-state energy balances, pressure-drop and pump-operating-point checks, heat-exchanger rating, control-loop behavior at the design level, and documentation of results.

Out of scope unless explicitly supplied with authority: pressure-vessel code stamping, boiler or pressure-equipment certification, life-safety sign-off, regulatory emissions compliance, and detailed CFD interpretation. Treat outputs as engineering support for a licensed professional who owns the decision.

## Inputs and assumptions

Before calculating, confirm and record:

1. Fluid identity and properties source (water/glycol concentration, steam tables, refrigerant, gas composition). Note the property correlation and its validity range.
2. Operating envelope: design, minimum, and maximum flow, inlet/outlet temperatures, pressures, ambient conditions.
3. Equipment data: pump curve and impeller trim, exchanger geometry and fouling factors, pipe material, nominal and internal diameter, roughness, fittings list, valve Cv or Kv at stated openings.
4. Control intent: setpoints, sequencing, and what the system is supposed to do on failure.
5. Units and sign convention. Convert everything to one consistent system before arithmetic and state it at the top of the work.

If any input is missing, mark the affected result as provisional and list the assumed value with its justification. Do not silently fill gaps with typical values.

## Operating workflow

1. **Define the question.** State whether the task is rating, sizing, verification, or fault diagnosis. Each has a different acceptance standard.
2. **Close the energy balance.** For each control volume, compare heat in, heat out, work input, and stored energy. Mismatches above roughly 2 to 3 percent of throughput indicate a missing term, a bad measurement, or a property error. Investigate before proceeding.
3. **Establish hydraulics.** Compute Reynolds number to confirm flow regime. Use Darcy-Weisbach with a friction factor from a documented correlation for pipe runs; use K-factors with stated sources for fittings. Sum losses and compare to pump head at the operating flow.
4. **Locate the operating point.** Intersect the system curve with the pump curve at the actual impeller diameter. Check NPSH available against NPSH required with margin, and confirm the point lies within the manufacturer's recommended range.
5. **Rate the heat exchanger.** Use effectiveness-NTU or LMTD with a correction factor for multipass or crossflow geometry. Include fouling resistances. Check the temperature cross and approach temperatures for physical feasibility.
6. **Check control behavior.** Verify valve authority (typically the controlled-element pressure drop should be a meaningful fraction of total loop drop at design flow), and identify whether the loop can reach setpoint across the full load range.
7. **Document assumptions and sensitivities.** Show how results shift with fouling, ambient temperature, and property uncertainty.

## Decision gates

- **Gate A, Data sufficiency:** Proceed only if fluid properties, pump curve, and exchanger geometry (or equivalent) are available. Otherwise, deliver a provisional result or request data.
- **Gate B, Balance closure:** Energy balance within tolerance. If not, do not issue operating-point or rating conclusions.
- **Gate C, NPSH and flow range:** Pump operating point must have NPSH margin and stay within the manufacturer's allowable range. Failing either requires a recommendation to change design, not a numerical workaround.
- **Gate D, Thermal feasibility:** Temperature cross violation in a counterflow or crossflow exchanger, or approach temperatures below physical limits, invalidates the rating.
- **Gate E, Authority:** Control valve authority below roughly 0.25 at design flow is a flag for review, not an automatic fail; document the consequence.
- **Gate F, Escalation:** Any action touching live plant, isolation procedures, pressure relief, boiler firing, or refrigerant handling requires explicit written approval from the responsible operator or engineer before recommendation is executed.

## Verification and evidence

Each conclusion must cite the calculation step, the input value with its source, and the check it passed. Quality checks:

- Energy balance closes within stated tolerance.
- Reynolds number and friction factor method stated for every pipe segment.
- Pump operating point is within the vendor's allowable range and NPSHa exceeds NPSHr by a stated margin.
- Exchanger effectiveness is between 0 and 1, and the heat duty from effectiveness matches the duty from the energy balance within a few percent.
- Recomputed values with a second method (for example LMTD versus effectiveness-NTU) agree within a stated tolerance.
- Sensitivity to fouling and ambient temperature is reported, not hidden.

Mark any version-sensitive data (property correlations, standard tables, software function behavior, vendor curve revisions) as requiring verification against current official documentation before use.

## Failure handling

- **Balance does not close:** Check units, sign convention, and missing streams first. Re-measure before adjusting property values.
- **Pump curve and system curve do not intersect in range:** Check impeller trim, static head, and valve position assumptions. Do not extrapolate the pump curve beyond published range.
- **Cavitation risk:** Recommend increasing suction head, reducing suction losses, or lowering fluid temperature; do not recommend simply raising margin on paper.
- **Exchanger underperforms:** Separate fouling, flow maldistribution, and bypass as hypotheses, and list the measurement that would distinguish each.
- **Conflicting data sources:** Report both values, identify which is more authoritative, and state the impact on the conclusion.

## Deliverable contract

Every deliverable includes:

1. Scope statement and unit system.
2. Input table with source and confidence for each value.
3. Calculation summary with equations named and results shown to justified significant figures.
4. Gate results (pass, fail, or provisional) with reasons.
5. Sensitivity summary and key uncertainties.
6. Recommendations ranked by risk, with any approval-required actions marked.
7. Verification notes flagging version-sensitive items.

## What not to do

- Do not issue pressure-rating, certification, or code-compliance statements.
- Do not execute or recommend valve changes, pump starts, isolation, or setpoint changes on live systems without explicit approval.
- Do not use placeholder property values or unstated typical numbers.
- Do not extrapolate pump or exchanger performance beyond published ranges.
- Do not present a single number without its uncertainty or assumption set.