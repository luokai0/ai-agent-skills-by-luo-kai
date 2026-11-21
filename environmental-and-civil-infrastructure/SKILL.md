---
name: environmental-and-civil-infrastructure
description: Use when planning, reviewing, or documenting civil infrastructure or environmental engineering work such as stormwater drainage, water and wastewater conveyance, grading and earthworks, erosion and sediment control, site hydrology, pavement and culvert design checks, or environmental impact screening, and an engineer needs structured calculations, criteria checks, or a reviewable deliverable.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Environmental And Civil Infrastructure

## Purpose and boundaries

This skill guides engineering analysis and documentation for civil infrastructure and environmental systems: site hydrology and stormwater, gravity and pressure conveyance, grading and earthworks, erosion and sediment control (ESC), culverts and small drainage structures, pavement load screening, and environmental screening inputs.

It produces calculation packages, criteria checklists, design-review notes, and draft specifications. It does not replace a licensed engineer's stamp, a jurisdiction's permitting process, or a formal environmental assessment. Any output is a draft until a responsible professional checks it against local code, the project's design criteria, and site-specific data.

Out of scope unless the user supplies a qualified professional's direction: structural design of buildings, seismic design, dam safety classification, contaminated-site remediation, and potable water treatment process design.

## Inputs and assumptions

Before calculating, collect and record:

1. Governing standard or design manual and edition (for example, the local stormwater manual or agency standard). Mark the edition as needing verification against current official publication.
2. Design storm: return period, duration, rainfall intensity-duration-frequency (IDF) source, and climate adjustment policy if required.
3. Site data: survey or DEM source and date, soil classes or infiltration tests, groundwater observations, existing utilities, receiving water classification.
4. Land cover and runoff coefficients or curve numbers, with the basis for each value.
5. Constraints: outfall elevation, allowable release rate, minimum cover, slope limits, sediment-control requirements.

If any input is missing, state an explicit assumption, label it, and list it under open items. Never silently fill a value with a typical number.

## Operating workflow

1. **Define the question.** Write one sentence: what is being sized, checked, or screened, and against which criterion.
2. **Establish the catchment.** Delineate drainage areas from survey data. Record area in consistent units, and check that areas sum to the total site.
3. **Select the method.** Choose a method appropriate to catchment size and governing manual (for example, rational method for small urban areas, unit hydrograph or routing for larger or detained systems). Note the method's stated applicability limits.
4. **Compute flows.** Show each intermediate value: intensity, coefficient or curve number, time of concentration with its equation, peak flow.
5. **Size conveyance.** Use Manning's equation or the governing hydraulic method. Check velocity against minimum self-cleansing and maximum erosion limits, and check freeboard.
6. **Check hydraulic grade.** Confirm headwater, tailwater, and outlet control. Verify energy grade line does not exceed rim or ground elevations at design flow.
7. **Screen erosion and sediment.** Compare shear stress or velocity against permissible values for the lining or soil. Confirm ESC measures match disturbed area and slope.
8. **Run criteria checklist.** Compare each result to a stated limit. Record pass, fail, or not applicable.
9. **Write the package.** Follow the deliverable contract below.

## Decision gates

- **Gate A (data sufficiency):** Proceed only if catchment area, design storm, and at least one soil or infiltration basis are sourced. Otherwise stop and request data.
- **Gate B (method validity):** If the catchment exceeds the method's stated limit, or the system has storage, backwater, or tidal influence, switch to a routing method or flag for specialist review.
- **Gate C (criteria failure):** Any failed criterion must either be redesigned and rerun, or escalated with a documented variance request. Do not mark a failed check as passed.
- **Gate D (approval required):** Obtain explicit human approval before any of the following: issuing outputs for permit submission, changing a design basis or design storm, recommending work that alters receiving-water flows or wetlands, specifying demolition or excavation of existing utilities, or any action that sends documents to external parties.

## Verification and evidence

- Recompute at least one result independently, by hand or with a second tool, and record agreement within a stated tolerance (suggested: 2 percent for flow, 1 percent for hydraulic depth).
- Check units on every equation; carry units through the calculation.
- Confirm monotonic sanity: larger storms produce larger peaks; larger pipes produce lower head loss at equal flow.
- Cross-check the catchment area against an independent source such as GIS polygons.
- Keep a source register listing each input, its origin, date, and confidence.
- Equations and default coefficients must be cited to the governing manual by section, with edition. Do not cite from memory.

## Failure handling

- **Inconsistent inputs** (for example, ground lower than outlet invert): stop, list the conflict, request survey correction.
- **Method fails validation:** rerun with the next applicable method and document the change.
- **Result near a limit (within 5 percent):** flag as marginal and recommend sensitivity testing on rainfall intensity, roughness, and coefficient.
- **Unknown standard edition or local rule:** mark as requiring verification against current official documentation; do not assume.

## Deliverable contract

Output a calculation package containing, in order:

1. Scope statement and governing standard with edition (marked for verification).
2. Input table with sources, dates, and assumptions flagged.
3. Catchment and flow calculations with every intermediate step.
4. Hydraulic results with velocities, depths, freeboard, and grade checks.
5. Criteria checklist with pass, fail, or marginal status and limit values.
6. Open items and required approvals.
7. Reviewer sign-off block left blank for the responsible professional.

## What not to do

- Do not present draft calculations as stamped or permit-ready.
- Do not use typical coefficients without a cited basis.
- Do not round intermediate values in ways that change a pass or fail result.
- Do not invent code section numbers, equation constants from memory, or software commands.
- Do not recommend discharge, dewatering, or in-stream work without a gate D approval.