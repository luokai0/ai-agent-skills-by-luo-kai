---
name: aerospace-vehicle-engineering
description: Use when analyzing, sizing, reviewing, or documenting aircraft, spacecraft, launch vehicle, or UAV design work, including mass and performance budgets, structural and thermal margins, flight-control and propulsion integration, and certification-oriented evidence packages.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Aerospace Vehicle Engineering

## Purpose and boundaries

This skill guides engineering analysis and review of whole-vehicle or subsystem-level aerospace design: requirements allocation, mass properties, performance and sizing, loads and structural margins, thermal and environmental budgets, propulsion and flight-control interfaces, and verification planning. It produces traceable engineering assessments, not flight clearances.

In scope: preliminary and detailed design reviews, trade studies, margin audits, interface checks, and test-plan critique for fixed-wing, rotary-wing, UAV, launch, and orbital vehicles.

Out of scope: issuing airworthiness approvals, signing off flight readiness, certifying compliance with any regulation, or replacing a licensed authority's findings. Output is advisory until a qualified engineer of record accepts it.

## Inputs and assumptions

Before analysis, confirm:

1. Vehicle class, mission profile, and operating envelope (altitude, Mach or velocity, load factor, temperature, duration).
2. Governing requirements document and revision. Record the revision letter.
3. Baseline mass statement with CG and inertia, and its date and owner.
4. Geometry, material properties with source and allowables basis (design, A-basis, B-basis, or unspecified).
5. Propulsion data: thrust, Isp or specific fuel consumption, throttle range, and propellant or fuel density.
6. Aerodynamic and thermal data sources and the test or analysis they came from.

Mark every missing input as an explicit assumption with a sensitivity note. Never fill a gap silently. Do not assume standard-day atmosphere, material allowables, or regulation applicability without stating them.

## Operating workflow

1. **Frame the question.** Write one sentence: what decision does this analysis support?
2. **Allocate requirements.** Map each vehicle-level requirement to a subsystem owner and a verification method (analysis, test, inspection, demonstration).
3. **Build the mass budget.** Sum component masses with uncertainty and growth allowance. Track margin as a percentage of the allowable gross mass or the controlling limit.
4. **Check performance.** Compute range, endurance, climb, or delta-v with the stated model. Show the equation used and the input units.
5. **Assess loads and margins.** For each critical structure, compute limit and ultimate loads from the flight envelope, apply the factor convention from the requirements, and report margin of safety.
6. **Review thermal and environmental budgets.** Confirm heat-flux, temperature, vibration, and pressure envelopes against component ratings.
7. **Verify interfaces.** Check mechanical, electrical, data, and fluid interfaces with matching revisions on both sides.
8. **Summarize and flag.** Produce the deliverable contract below.

## Decision gates

Stop and escalate to the engineer of record if any of these hold:

- Mass margin falls below the program threshold, or no threshold is defined.
- Any structural margin of safety is negative or depends on an allowable of unknown basis.
- Propulsion or flight-control characteristics rely on an unverified model outside its validated range.
- A requirement conflicts with another requirement or with physics (for example, a range target incompatible with the stated fuel fraction).
- Results depend on an assumption that changes a go/no-go conclusion.

Proceed only when each gate is passed or the open item is recorded with an owner and due date.

## Verification and evidence

- Re-derive one independent value per major result (hand estimate or order-of-magnitude check). Disagreement beyond the stated tolerance blocks release of the result.
- Confirm units and frames of reference at every interface. Unit mismatch is the most common fatal error.
- Check that margins use the correct load factor convention (limit versus ultimate).
- Trace every number to a source document, test report, or analysis file with revision.
- Quality checks: all requirements have an owner and method; mass budget sums to within 0.1% of its components; every assumption has a sensitivity note; no result lacks a source.

## Failure handling

- If data is missing, report the gap and the bounding estimate, not a point answer.
- If two sources disagree, identify which is newer and better-characterized, present both, and escalate.
- If a calculation fails a sanity check, stop, identify the input error, and rerun before reporting.
- Mark any version-sensitive tool behavior, software API, or standard clause as requiring verification against current official documentation.

## Deliverable contract

Every output contains:

1. Question addressed and scope.
2. Inputs with revisions, plus explicit assumptions and their sensitivity.
3. Results with equations, units, and margins.
4. Traceability table linking each result to source.
5. Open items with owner, severity, and gate status.
6. Recommendation: proceed, proceed with conditions, or hold.
7. Statement that the result is advisory and requires review by the engineer of record.

## Explicit approvals and what not to do

Require explicit human approval before: releasing results into a configuration baseline, changing a controlled requirement or interface document, sharing outputs with external parties or regulators, or taking any action that alters flight hardware or software.

Do not: invent material allowables, regulatory citations, benchmark figures, or software function names; state that a design is compliant or airworthy; drop a failed check to meet a schedule; round margins upward; or present a single-point answer when the inputs support only a range.