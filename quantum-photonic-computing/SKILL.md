---
name: quantum-photonic-computing
description: Use when designing, evaluating, or reviewing photonic quantum computing approaches (boson sampling, linear optical quantum computing, photonic qubit architectures, integrated photonic circuits for quantum information), including feasibility analysis, loss budgets, resource estimates, and claims validation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Quantum Photonic Computing

## Purpose and boundaries

Use this skill to analyze photonic quantum computing work at the level of physical architecture, component performance, resource scaling, and evidence quality. It covers:

- Photonic qubit encodings (polarization, time-bin, dual-rail, path, continuous-variable squeezed/cat states).
- Linear optical networks, boson sampling, and measurement-based or fusion-based photonic architectures.
- Integrated photonics platforms (waveguides, phase shifters, beam splitters, single-photon sources and detectors, multiplexing).
- Loss, indistinguishability, and detection-efficiency budgets; error-correction overhead for photonic loss.
- Vetting vendor, paper, or internal claims about advantage, fidelity, or throughput.

It does not cover: general quantum algorithm design unrelated to photonic hardware, cryptographic deployment decisions, export-control classification, or procurement advice. Refer those to appropriate specialists.

## Inputs and assumptions

Collect before analysis:

1. Target task: sampling, computation, communication, or sensing; the logical or physical operation count.
2. Encoding and architecture: qubit encoding, source type (SPDC, quantum dot, multiplexed heralded), network topology, detector type.
3. Component figures with conditions: source brightness and g2(0), detector efficiency and dark count rate, propagation and coupling loss (dB/cm or dB per facet), phase-shifter insertion loss and drift, two-photon interference visibility (HOM dip).
4. Claimed results with their measurement definitions: fidelity definition, post-selection rates, sample sizes, confidence intervals.
5. Stated assumptions about classical simulability and the comparison baseline.

If any input is missing, state the assumption explicitly and label conclusions as conditional on it. Do not fill gaps with typical literature values presented as facts.

## Operating workflow

1. **Define the object.** Write one sentence: what is being built, for what task, and what counts as success.
2. **Build the loss budget.** Multiply transmission across every element in the optical path: source-to-circuit coupling, circuit insertion loss, phase shifters, switches, fiber links, detector efficiency. Express total end-to-end efficiency η as a single number and as dB.
3. **Compute photon-rate and multi-photon yield.** For N-photon events, yield scales roughly as η^N times source emission probability^N; show the scaling explicitly and identify the dominant term.
4. **Assess indistinguishability.** Convert HOM visibility V into an effective mode-overlap penalty for multi-photon interference; note that small reductions compound with photon number.
5. **Assess noise sources.** Dark counts, multi-pair emission (g2), timing jitter, and temporal mode mismatch; estimate their contribution to error rate in the target observable.
6. **Evaluate error correction overhead** if fault tolerance is claimed: identify the photon-loss threshold assumed by the scheme, the loss budget against it, and the resource multiplier (multiplexing factor, fusion success probability, ancilla count). Provide these as parameter-dependent ranges, not single values.
7. **Check classical baselines.** State the best known classical method for the task and whether the claimed regime is tested against it, including its cost.
8. **Document conclusions** with explicit conditions and open questions.

## Decision gates

Proceed to design or investment review only if all hold:

- End-to-end efficiency is computed from measured or specified component values, not nominal datasheet figures alone.
- Multi-photon yield at the target photon number is nonzero and its scaling is stated.
- Claimed fidelity or advantage has a stated definition, sample size, and uncertainty.
- The classical baseline is named and was considered.

Halt and escalate if:

- A fault-tolerance claim lacks an explicit loss threshold and overhead model.
- Results rely on post-selection without reporting the post-selection rate and its effect on the claimed statistic.
- Comparison is made against a weakened classical baseline or an unstated one.

## Verification and evidence

Quality checks, each with a pass criterion:

- Loss budget sums to the stated η within 1 dB when recomputed from listed components.
- Yield table covers at least three photon numbers, with the scaling exponent reported.
- HOM visibility, g2(0), and detector efficiency are reported with measurement conditions (wavelength, temporal bin width, pump power).
- Sample size yields a confidence interval narrower than the claimed margin; otherwise the claim is unsupported.
- Every cited value has a source identifier (publication, datasheet revision, or internal test record) and date.

Mark any component figure, software interface, toolkit version, or standard as "verify against current official documentation" when it depends on a version or vendor release. Do not assert benchmark numbers from memory.

## Failure handling

- **Missing component data:** produce a bounded estimate with explicit low/high assumptions and list the measurement that would close the gap.
- **Inconsistent figures** (e.g., claimed rate exceeds source brightness times efficiency): flag the contradiction, identify the most likely faulty input, and request clarification. Do not average conflicting numbers.
- **Unverifiable advantage claims:** report what is verified, what is not, and what experiment would discriminate.
- **Out-of-scope request** (device fabrication instructions for restricted technology, procurement, export matters): decline the specific part and state the boundary.

## Deliverable contract

Return a report with these sections, in order:

1. Summary (three sentences maximum, including the main conditional conclusion).
2. Assumptions table (parameter, value, source, confidence).
3. Loss budget and yield table with computed η and scaling exponent.
4. Noise and indistinguishability assessment.
5. Baseline comparison.
6. Gate status (pass, halt, or escalate, per gate).
7. Open questions and required measurements.
8. Version-sensitive items flagged for verification.

Approval required before: committing procurement or experimental resources, sharing results externally, publishing performance claims, or taking any action that alters shared lab or production systems.

Do not: present estimates as measured results; omit the loss budget from advantage claims; accept fault-tolerance claims without an overhead model; or cite specific figures from memory without a verifiable source.