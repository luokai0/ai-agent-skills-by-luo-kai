---
name: specialized-domains-engineering
description: Use when building, reviewing, or modifying code in regulated or high-stakes specialized domains such as embedded/firmware, safety-critical control, medical device software, financial trading or settlement, scientific numerical computing, geospatial, cryptography-adjacent, or hardware-facing systems where correctness, units, timing, or compliance constraints dominate ordinary software practice.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Specialized Domains Engineering

## Purpose and boundaries

This skill guides engineering work where ordinary web or CRUD practices are insufficient because errors have physical, financial, legal, or scientific consequences. It covers: identifying domain invariants, selecting correctness-preserving designs, verifying behavior with domain-appropriate evidence, and documenting what was and was not proven.

It does not cover: certifying software to a standard, providing legal or regulatory opinions, designing hardware, or replacing a qualified domain expert, safety engineer, or auditor. Where a deliverable would be relied upon for safety, patient, financial, or legal outcomes, state that a qualified reviewer must sign off.

## Inputs and assumptions

Before writing code, establish:

1. **Domain and consequence class**: what fails, who is harmed, and the worst credible outcome.
2. **Governing requirements**: specifications, interface control documents, applicable standards named by the user. Do not assume a standard applies; ask.
3. **Target environment**: MCU/OS/runtime, clock source, numeric precision, toolchain version, library versions.
4. **Units and coordinate conventions**: SI or otherwise, frames of reference, time base (UTC, TAI, monotonic, exchange time), timezone rules.
5. **Data provenance**: sensor calibration, market data source, dataset licensing and consent status.

If any of these is unknown and affects design, stop and list the open questions. Assumptions made to proceed must be labeled in the deliverable.

## Operating workflow

1. **Restate invariants.** Write 3–8 invariants in testable form, e.g., "actuator command never exceeds ±2.5 N," "order quantity is never negative after fill," "geodetic transforms round-trip within 1 mm over the service area."
2. **Model units and types.** Use distinct types or wrappers for physical quantities, currency, and time bases. Reject implicit conversions. Prefer explicit conversion functions with documented constants.
3. **Choose the numeric strategy.** Decide between fixed-point, floating-point, or arbitrary precision. For money, use integer minor units or decimal types, never binary floating point. For accumulation over long horizons, use compensated summation or wider accumulators and justify the choice.
4. **Design for bounded behavior.** Specify worst-case execution time, memory ceilings, and maximum latency where relevant. Avoid unbounded allocation, unbounded recursion, and blocking calls on real-time paths.
5. **Implement defensively at boundaries.** Validate every input crossing a trust, device, or unit boundary. Reject out-of-range values explicitly rather than clamping silently, unless the specification mandates clamping, in which case log and count it.
6. **Make failure states explicit.** Represent sensor faults, timeouts, stale data, and partial writes as first-class states with defined transitions to a safe state.
7. **Verify (see below) before declaring completion.**

## Decision gates

Stop and obtain explicit human approval before proceeding if the task involves:

- Deleting or overwriting calibration data, production configuration, ledgers, patient records, or firmware images.
- Flashing hardware, changing actuator limits, or altering safety interlocks.
- Sending live orders, transactions, messages, or commands to external systems.
- Modifying audit trails, logging retention, or consent records.
- Changing a numeric tolerance, rounding rule, or unit convention already used in production, since this changes historical results.
- Adding or upgrading a dependency in a certified or validated build.
- Handling personal health, financial, or location data beyond what the task requires.

Also gate on scope: if a fix requires changing a requirement rather than code, return the conflict to the requirement owner.

## Verification and evidence

Evidence must match the claim. Acceptable forms, in rough order of strength:

- **Property-based or exhaustive tests** over the invariants from step 1, with the generator ranges stated.
- **Hardware-in-the-loop or replay tests** using recorded real inputs, with the recording source identified.
- **Cross-checks** against an independent reference implementation or published worked examples, with tolerance stated.
- **Static analysis and sanitizers** (address, undefined behavior, thread) appropriate to the language; report the tool version and the configuration used.
- **Code review** by someone other than the author, focused on units, boundaries, and error paths.

Quality checks that must be reported with numbers:
- Invariant coverage: count of invariants with at least one executable test.
- Unit-consistency: zero untyped physical quantities crossing public interfaces (state the count checked).
- Worst-case timing or memory: measured value, method, and hardware used, or an explicit statement that it was not measured.
- Tolerance: maximum observed error against the reference, and the reference source.

Do not report results you did not obtain. Write "not run" where applicable.

## Failure handling

- **Test failure in an invariant:** treat as a defect in code or requirement; do not weaken the test. Identify which side is wrong with evidence.
- **Ambiguous unit or tolerance:** halt that component, record the ambiguity, and request clarification.
- **Missing reference data:** proceed only with a clearly labeled provisional result.
- **Environment mismatch** (different compiler, runtime, or timer resolution than the target): state the mismatch and what evidence it invalidates.
- **Discovered safety-relevant defect in shipped behavior:** stop, report it with reproduction steps, and do not patch production without the decision gate approval.

## Deliverable contract

Every deliverable must include:

1. Changed artifacts and a one-paragraph summary of behavior changes.
2. The invariant list with test mapping.
3. Unit, numeric, and timing decisions with rationale.
4. Verification performed, with exact commands or procedures, tool versions, and results.
5. Verification not performed, and the risk it leaves.
6. Open assumptions and required approvals.
7. A statement that domain or compliance sign-off is required before use in a regulated or safety context.

## What not to do

- Do not use binary floating point for currency or exact-rounding requirements.
- Do not silently clamp, coerce, or default out-of-range physical or financial values.
- Do not invent standard clauses, API names, flags, package versions, or benchmark numbers. Where a detail is version-sensitive, mark it "verify against current official documentation" and do not state it as fact.
- Do not claim compliance, certification, or safety guarantees.
- Do not use wall-clock time for interval measurement on control paths; use monotonic sources.
- Do not add unbounded dynamic allocation or blocking I/O to real-time paths.
- Do not weaken or delete failing tests to achieve a green build.
- Do not execute actions in the decision gates without explicit approval.