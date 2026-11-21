---
name: energy-storage-hydrogen
description: Use when evaluating, sizing, specifying, or reviewing hydrogen-based energy storage (electrolysis, compression or liquid storage, fuel cell or turbine reconversion) for grid, microgrid, industrial, or renewable-integration projects, including round-trip efficiency, storage duration, and safety-case questions.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Energy Storage Hydrogen

## Purpose and boundaries

This skill supports engineering and techno-economic work on power-to-hydrogen-to-power storage chains: electricity to hydrogen by electrolysis, hydrogen storage (compressed gas, liquid, or materials-based), and reconversion (fuel cell, combustion turbine, or engine). It covers sizing, efficiency accounting, cost comparison against batteries and other storage, site-level safety screening, and review of vendor or consultant claims.

Out of scope: detailed electrochemical stack design, pressure-vessel mechanical design, legal certification of installations, and final safety sign-off. Those require licensed engineers and the applicable codes in the jurisdiction. This skill produces analysis and recommendations, not stamped designs.

## Inputs and assumptions

Collect before analysis; record any missing value as an explicit assumption:

- Service requirement: discharge power (MW), energy (MWh), duration, cycles per year, response time, and required availability.
- Electricity supply: source profile (hourly or sub-hourly), curtailment availability, tariffs or price series, and grid connection limits.
- Electrolyzer: technology (PEM, alkaline, SOEC, AEM), nameplate capacity, stated system-level specific energy (kWh/kg H2 at the boundary used by the vendor), turndown ratio, and standby losses.
- Storage: pressure or liquefaction target, vessel or cavern type, hydrogen purity, boil-off or leakage assumptions, site footprint.
- Reconversion: fuel cell or turbine type, electrical efficiency at rated and part load, auxiliaries (compressors, chillers, water treatment).
- Financial: capex and opex basis year, discount rate, asset life, replacement intervals for stacks.
- Site: jurisdiction, hazardous-area classification basis, distance to occupied buildings, ventilation, and ignition sources.

Assume nothing about efficiency boundaries. Always state whether a figure is lower heating value or higher heating value, and whether it includes compression, cooling, and balance-of-plant.

## Operating workflow

1. Define the service in one sentence: what is delivered, to whom, at what power, energy, and duration.
2. Build the energy balance: electricity in, electrolyzer load, compression energy, storage losses, reconversion output. Compute round-trip efficiency at the grid boundary, stating each loss term.
3. Simulate dispatch against the supply profile. Report the number of charge-discharge cycles, seasonal storage carryover, and unserved energy.
4. Size components iteratively: electrolyzer first (absorbs surplus), then storage (covers the longest deficit window plus margin), then reconversion (meets peak power).
5. Compute levelized cost of storage on a stated basis and run sensitivities on electricity price, capacity factor, and stack life.
6. Screen safety: hydrogen flammability range (4–75 % vol in air), low ignition energy, high diffusivity, and embrittlement risk for certain steels. Identify the hazardous-area basis and required separation distances from applicable standards, flagged for verification.
7. Compare against alternatives (lithium-ion for short duration, pumped hydro for bulk, thermal storage) on the same service definition.
8. Write the recommendation with explicit assumptions, ranges, and open items.

## Decision gates

- **Gate A, service fit:** Proceed to hydrogen only if required duration exceeds roughly 8–12 hours or seasonal shifting is needed. For shorter service, batteries usually dominate on round-trip efficiency and cost; document the comparison before proceeding.
- **Gate B, efficiency:** If round-trip electricity-to-electricity efficiency at the grid boundary is below 30 % under realistic assumptions, the project needs a use case beyond storage (heat recovery, hydrogen sales) before proceeding.
- **Gate C, data sufficiency:** Do not produce an LCOS figure without a stated electricity price basis, a defined capacity factor, and stack replacement assumptions.
- **Gate D, safety:** Any site with occupied buildings within the calculated separation distance, or any indoor storage, requires explicit approval from the project's safety authority before design continues.
- **Gate E, external impact:** Any action that submits permit applications, communicates with utilities or regulators, orders equipment, or publishes figures to third parties requires explicit human approval.

## Verification and evidence

- Recompute efficiency independently from the energy balance; reconcile to within 1 percentage point or explain the gap.
- Check that the dispatch simulation conserves energy: stored energy change equals inputs minus outputs minus losses, at every timestep, within numerical tolerance.
- Confirm storage capacity is not exceeded and electrolyzer minimum load and turndown are respected in every simulated hour.
- Cross-check vendor specific-energy figures against thermodynamic minimum (about 33.3 kWh per kg H2 on a HHV basis) and state the gap.
- Cite the version and date of every standard, code, or price series used. Mark any standard edition or regulatory threshold as "verify against current official documentation."
- Do not state that a design "complies with" a code or standard unless a qualified reviewer has confirmed it.

## Failure handling

- If the dispatch shows unserved energy above the stated tolerance, increase the storage or reconversion size and rerun; do not silently reduce the service requirement.
- If sensitivities flip the recommendation, report the flip explicitly with the threshold value.
- If a vendor figure cannot be reconciled with thermodynamics or the stated boundary, reject it and request the boundary definition.
- If safety data is missing, stop at Gate D and list the missing items; do not estimate separation distances by analogy.

## Deliverable contract

Deliver a single report containing:

1. Service definition and boundary statement.
2. Assumptions table with source or "assumed" label for each value.
3. Energy balance and round-trip efficiency with loss breakdown.
4. Sizing results and dispatch summary (cycles, unserved energy, carryover).
5. Cost basis, LCOS, and sensitivity table.
6. Safety screening findings and open verification items.
7. Gate status (pass, fail, or pending) for Gates A through E.
8. Recommendation with stated conditions under which it changes.

Do not: present a single efficiency number without its boundary; use HHV and LHV interchangeably; treat hydrogen as cheaper than batteries without a validated duration argument; or claim regulatory compliance.