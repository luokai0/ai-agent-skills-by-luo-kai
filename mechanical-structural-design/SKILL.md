---
name: mechanical-structural-design
description: Use when sizing, checking, or reviewing mechanical structures, brackets, frames, shafts, fasteners, weldments, or load paths, including stress, deflection, fatigue, and factor-of-safety justification for a design or drawing package.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Mechanical Structural Design

## Purpose and boundaries

This skill guides structural sizing, load-path checking, and design review for mechanical parts and assemblies: machine frames, brackets, mounts, shafts, bolted joints, welded fabrications, and sheet-metal enclosures. It produces a traceable calculation record that a qualified engineer can check and sign.

In scope: load definition, free-body diagrams, hand calculations and FEA-readiness checks, stress and deflection limits, bolted joint preload checks, weld sizing, fatigue screening, and documentation of assumptions.

Out of scope: certification to a specific code (ASME, EN, AISC, pressure vessel or lifting standards) unless the user supplies the governing edition and the reviewer is qualified; life-safety sign-off; electrical, thermal-only, or control design. This skill does not replace a licensed professional engineer's stamp where one is required.

## Inputs and assumptions

Required inputs before calculating:
- Geometry or dimensioned sketch with units stated.
- Material designation and minimum guaranteed properties (yield, ultimate, modulus), with source.
- Load cases: static, dynamic, impact, thermal, preload, with magnitude, direction, duration, and frequency.
- Boundary conditions: supports, constraints, contact type (pinned, fixed, sliding).
- Service environment: temperature range, corrosion, cycle count target.
- Governing requirements: customer spec, internal standard, or code edition.

If any item is missing, list it as an assumption with a stated value and flag it as open. Never silently assume a material strength or load.

## Operating workflow

1. **Define the load cases.** Enumerate operating, transport, assembly, and misuse conditions. Apply a dynamic factor or shock multiplier only with a stated basis.
2. **Draw the free-body diagram** for each member and joint. Verify static equilibrium (sum of forces and moments equals zero) before computing stresses.
3. **Establish the load path.** Trace every load from application point to ground. Identify where it changes members, and check each transfer (bolt, weld, bearing, friction).
4. **Calculate section properties and stresses.** Use Mohr's circle or equivalent principal stress checks for combined loading. Note stress concentrations (holes, fillets, notches) and apply appropriate factors from a published source.
5. **Check deflection and stiffness** against function limits (alignment, gear mesh, seal gap), not just strength.
6. **Check bolted joints:** preload target, clamp load, separation load, and thread stripping. Confirm embedment and shear-out for threaded and bearing connections.
7. **Check welds:** effective throat, allowable shear, and fatigue category if cyclic.
8. **Screen fatigue** using stress range and an endurance estimate, applying surface, size, and reliability modifiers with sources.
9. **Run FEA only as confirmation.** Document mesh, element type, convergence, and boundary conditions; hand-check at least one critical location.
10. **Compile the record** (see Deliverable contract).

## Decision gates

- **Gate A (inputs complete):** Proceed only when all required inputs are present or explicitly marked as assumptions with owners. Otherwise stop and request data.
- **Gate B (equilibrium):** Reactions must balance within 1% of applied load. Failure returns to step 2.
- **Gate C (margins):** Static factor of safety on yield should be at least 1.5 for controlled loads and 2.0 for uncertain loads, unless the governing standard states otherwise. Fatigue factor should be at least 1.5 on the stress-life or strain-life basis used. Deflection must meet the function limit with margin.
- **Gate D (joint integrity):** Bolt preload must be between 60% and 75% of proof load for reusable joints, unless the fastener manufacturer's data supports otherwise; confirm with current manufacturer documentation.
- **Gate E (review):** A second engineer independently checks the critical path before release.

If any gate fails, do not release. Redesign or escalate.

## Verification and evidence

- Re-derive one stress value independently from a different method.
- Confirm units are consistent across every equation; carry units through calculations.
- Compare FEA peak stress to hand calculation; differences above 15% require explanation (singularities, mesh refinement, boundary assumptions).
- Check mass and center of gravity against the CAD model.
- Verify material properties against the cited datasheet, noting the revision date.
- Mark any value that depends on software version, standard edition, or catalog data as "verify against current official documentation" with the date checked.

## Failure handling

- **Negative margin:** Report the controlling location, load case, and margin. Propose at least two options (section increase, material change, load path change) with mass and cost impact. Do not hide the failure by lowering the load.
- **Unknown material or load:** Use the most conservative credible value and flag it; do not assume favorable properties.
- **FEA and hand calculation disagree:** Investigate boundary conditions first, then mesh, then assumptions. Do not average them.
- **Standard edition unavailable:** State the edition used by the team and request confirmation.

## Deliverable contract

Output a structural design record containing:

1. Scope, revision, and governing requirements.
2. Input table with sources and open assumptions.
3. Load case table and free-body diagrams.
4. Calculation sheets per critical member, joint, and weld, each with units.
5. Margin summary table: location, load case, stress or load, allowable, factor of safety, status.
6. Deflection summary against function limits.
7. Verification log: checks performed, results, reviewer, date.
8. Open issues and required approvals.

Each calculation must be reproducible from the stated inputs. Mark the release status as Draft, Reviewed, or Released, and release only after Gate E passes.

## Approval and safety controls

Obtain explicit human approval before: releasing drawings to manufacturing, issuing a stamped or certified statement, modifying a controlled drawing or revision, changing a load or safety factor to achieve a pass, or sending the record to external parties. Do not state that a design is safe, compliant, or certified; state the margins and checks performed.