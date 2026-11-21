---
name: energy-generation-grid
description: Use when planning, analyzing, or reviewing grid-connected electricity generation projects (solar, wind, storage, hybrid plants) for interconnection, dispatch, capacity, or grid-impact questions, and when a deliverable must state assumptions, study results, and their limits.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Energy Generation Grid

## Purpose and boundaries

This skill guides structured analysis of how distributed and utility-scale generation connects to, and behaves on, an electric grid. It covers:

- Interconnection screening (capacity, voltage class, point of interconnection, protection needs).
- Generation profile and capacity-value estimation for variable and dispatchable resources.
- Grid-impact questions: hosting capacity, voltage rise, thermal loading, reverse power flow, frequency response, and curtailment exposure.
- Hybrid and storage sizing logic at the screening level.
- Review of vendor or consultant studies for completeness and internal consistency.

It does not produce stamped engineering designs, protection settings for energized equipment, regulatory filings, or legal compliance opinions. Those require a licensed professional and the governing utility or regulator. Use this skill to structure, check, and communicate the analysis, not to replace the study.

## Inputs and assumptions

Before analysis, collect and record:

1. Site: coordinates, nominal capacity (MW AC and MW DC for solar), resource data source and period.
2. Interconnection: nearest feeder or substation, voltage level, short-circuit strength at POI if known, existing queue position.
3. Equipment: inverter or turbine type, storage chemistry and power/energy rating, control mode (grid-following, grid-forming, PQ, Volt-VAR capability).
4. Load and network context: minimum and peak load on the feeder, existing generation on it, planned changes.
5. Governing requirements: the utility interconnection standard and applicable grid code. Record the document name, revision, and date. Mark every numeric limit taken from these as **to verify against current published revision**.

Label each assumption as *measured*, *vendor-stated*, or *estimated*. Any assumption without a source is treated as estimated and must be listed in the deliverable.

## Operating workflow

1. **Scope the question.** State the one decision the analysis supports (e.g., "Is 5 MW export viable at feeder F-12 without network upgrades?"). Vague scope produces unusable studies.
2. **Build the generation profile.** Use hourly or sub-hourly data for at least one full year where available. Compute capacity factor, monthly and diurnal profiles, and the coincidence of output with feeder minimum load.
3. **Screen the feeder.** Compare minimum load plus generation export against minimum load, and generation output against feeder thermal rating at the worst coincident hour. Flag reverse power flow conditions explicitly.
4. **Estimate voltage impact.** Use a simplified ΔV ≈ (R·P + X·Q)/V relationship for screening, then replace with a power-flow model for any site passing screening marginally.
5. **Assess protection and fault contribution.** Note whether added inverter-based or rotating fault current changes protection coordination. Escalate to a protection engineer rather than resolving here.
6. **Evaluate storage or hybrid options** only after the base export case is characterized. Model charge source, state-of-charge limits, round-trip efficiency (from vendor data, marked vendor-stated), and degradation assumptions.
7. **Quantify curtailment and value.** Estimate curtailment hours from export limits and congestion; report energy and capacity value separately.
8. **Prepare the grid engineering note** using the output schema below.

## Decision gates

- **Gate A (scope):** Proceed only if the decision question, deadline, and decision owner are named.
- **Gate B (data sufficiency):** Proceed to modeling only with at least one year of resource data and confirmed POI voltage class. If resource data is a single typical-meteorological-year or under 12 months, state that the energy estimate carries wide uncertainty.
- **Gate C (screening result):** If any worst-case hour shows feeder thermal loading above 80% of rating or ΔV exceeding the governing limit, stop screening and recommend a detailed power-flow study. Do not declare the site viable.
- **Gate D (external action):** Any submission to a utility, filing, customer commitment, or equipment purchase requires explicit human approval from the named decision owner. Do not proceed autonomously.

## Verification and evidence

- Reconcile annual energy from the profile against the simple capacity-factor estimate; differences above 10% must be explained.
- Confirm units on every figure (MW vs MWh, AC vs DC, per-unit base).
- Check that exported power never exceeds the approved or requested export limit in the modeled series.
- Verify timezone and daylight-saving handling in time-series joins.
- Spot-check three random hours by hand against the source data.
- Cross-check numeric limits against the current published interconnection standard; record revision and retrieval date.
- Do not state that a site "complies" with any standard. State which screened criteria were passed and which were not evaluated.

## Failure handling

- **Missing or gapped data:** Interpolate only gaps under three hours; flag and exclude longer gaps and report the excluded fraction.
- **Conflicting sources** (e.g., vendor and utility capacity figures): report both, use the more conservative value for screening, and request resolution.
- **Model non-convergence or unexplained results:** Stop, reduce to the simplest case that reproduces the issue, and report the failing condition rather than adjusting inputs to force a pass.
- **Standard not accessible:** Mark all dependent limits as unverified and do not substitute recalled values as fact.

## Deliverable contract

The output must contain, in order:

1. Decision question and conclusion, stated in one paragraph with its confidence level.
2. Input table with source and classification (measured, vendor-stated, estimated) for each value.
3. Method summary and model type, including the simplifications made.
4. Results: energy, capacity value, screening pass/fail per criterion, worst-case hour and its conditions.
5. Assumption register and unverified items, each with an owner and a verification action.
6. Limitations and the recommended next study (e.g., full power-flow, protection review).
7. Approval status: which external actions remain pending human sign-off.

Do not include unsupported compliance claims, invented equipment specifications, or results without a traceable input.