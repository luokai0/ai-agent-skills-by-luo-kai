---
name: electrical-electronics-biomedical-systems
description: Use when designing, reviewing, or troubleshooting electrical, electronics, or biomedical systems, including analog front ends for physiological sensing, power and isolation for patient-connected devices, signal integrity in embedded hardware, and test or verification plans for medical-grade electronics.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Electrical Electronics Biomedical Systems

## Purpose and boundaries

This skill guides engineering analysis of electrical and electronic circuits, power systems, signal chains, and embedded hardware, with emphasis on biomedical applications: biopotential acquisition (ECG, EMG, EEG), bioimpedance, pulse oximetry, infusion and monitoring electronics, and wearable sensing.

In scope: circuit analysis and sizing, sensor front-end design, noise and interference budgets, patient isolation and leakage concepts, power-supply and battery architecture, grounding and layout review, test-plan design, and failure diagnosis on bench hardware.

Out of scope: certifying a device to a regulatory standard, claiming compliance with any IEC, ISO, or FDA requirement, clinical efficacy claims, and therapeutic dosing decisions. Where a design touches a patient, state that formal compliance requires a qualified regulatory and safety process.

## Inputs and assumptions

Collect before analyzing:
- Application, signal of interest, bandwidth, amplitude range, and source impedance.
- Supply rails, battery chemistry and capacity, load profile (peak and average current).
- Connection to the patient or external mains, and whether an applied part is floating or earth-referenced.
- Operating environment: temperature, humidity, EMI sources (switching converters, RF, mains).
- Available parts and datasheets; record the exact part number and revision.

Assumptions must be written down with a stated basis. Mark any value taken from memory as unverified.

## Operating workflow

1. Define the signal chain as a block list: sensor, electrode or transducer, protection, amplification, filtering, conversion, processing, isolation, output.
2. Bound each stage: gain, bandwidth, input range, output swing, supply headroom.
3. Compute noise budget: input-referred voltage and current noise, resistor thermal noise (√(4kTRB)), and interference (50/60 Hz, switching harmonics). Compare against the minimum detectable signal.
4. Check DC paths: bias current return, offset drift over temperature, electrode half-cell potentials.
5. Check protection: input clamps, series resistance for limiting fault current, transient suppression on connected lines.
6. Check power: sum worst-case currents per rail, add margin, verify regulator dropout and thermal dissipation, confirm battery end-of-life voltage.
7. Check isolation barrier: creepage, clearance, and the path of leakage current under single-fault conditions. Flag any barrier as "requires standards review."
8. Review layout: return current paths, guard traces, separation of analog and digital grounds, decoupling placement.
9. Produce the test plan (see Verification).

## Decision gates

- **Gate A (signal feasibility):** Proceed only if the noise budget leaves at least 6 dB margin over the minimum detectable signal at worst-case temperature.
- **Gate B (patient connection):** Any path from patient-applied parts to mains or to a non-isolated supply requires explicit human review before proceeding.
- **Gate C (power):** Proceed only if worst-case current per rail is at most 80% of the source rating.
- **Gate D (stability):** Any amplifier with capacitive load or cable drive requires a stability check (phase margin estimate, or measured step response) before release.
- **Gate E (destructive tests):** Fault-injection, overvoltage, or short-circuit tests on real hardware require explicit user approval and a stated safe setup.

## Verification and evidence

Each claim must cite its evidence type: calculation, simulation, datasheet value, or measurement. Simulation is not measurement.

Measurable checks:
- Measured input noise floor versus calculated budget; deviation greater than 3 dB triggers investigation.
- Common-mode rejection measured at the mains frequency and its harmonics.
- Step response overshoot below 10% under the stated load.
- Supply ripple at the load under maximum current, reported in mV peak-to-peak with bandwidth stated.
- Temperature sweep of offset and gain at the operating extremes.

Mark any version-sensitive detail (device errata, tool flags, library calls, standard edition numbers) as "verify against current official documentation" rather than asserting it from memory.

## Failure handling

- Unexpected oscillation: check stability compensation, cable capacitance, and ground loops before changing gain.
- Excess 50/60 Hz pickup: inspect lead length, shield termination, and driven-right-leg or guard networks before adding filters that distort the band of interest.
- Drift or saturation: check electrode polarization and input bias return paths first.
- Brownouts under load: measure the rail under real load; do not infer from the datasheet alone.
- Repeated part failure: stop, record conditions, and escalate for root-cause review before further power-up attempts.

## Deliverable contract

Deliver:
1. Signal chain block diagram with stage parameters.
2. Calculation summary listing equations, inputs, results, and margins against each gate.
3. Assumption register with verification status.
4. Risk list, marking any patient-contact or isolation item for human safety review.
5. Test plan with pass criteria and required equipment described by class (for example, "isolated oscilloscope," not model numbers).
6. Open items list.

Do not: present a design as compliant or safe for patient use; invent part numbers, register values not derived from calculation, or datasheet figures; run destructive tests without approval; or omit the stated basis for any number.