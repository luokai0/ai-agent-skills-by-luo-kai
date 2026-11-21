---
name: engineered-biology-materials
description: Use when designing, reviewing, or planning work on engineered biology materials (biologically produced or biologically templated materials such as biofabricated composites, living or engineered-cell-based materials, mycelium and protein-based materials, biomineralized structures, and microbially produced polymers), including process feasibility, characterization planning, scale-up risk, and biosafety-aware documentation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Engineered Biology Materials

## Purpose and boundaries

This skill supports professionals who turn biological systems into functional materials. In scope: feasibility assessment of a biologically produced or templated material; defining organism or cell-system, feedstock, and growth or fabrication conditions; selecting material characterization methods; planning pilot-to-scale transitions; and writing batch records and evidence packages.

Out of scope: wet-lab protocol execution without a qualified operator and institutional biosafety review; genetic design of organisms intended for release; uses in humans or food-contact applications (route to specialized regulatory review); performance or regulatory compliance claims; and any gene-drive or pathogen-enhancement work, which must be refused.

## Inputs and assumptions

Collect before analysis:
1. Target function and performance envelope (e.g., compressive modulus range, water uptake limit, degradation time, thermal limit, service life).
2. Production route: organism or cell line (identity, source, biosafety level as assigned by the institution), growth or culture medium, fabrication method (solid-state, submerged, scaffold-templated, mineralization, spinning).
3. Feedstock composition and variability, including waste or agricultural inputs.
4. Scale target and facility constraints (containment class, sterilization capacity, curing space).
5. Existing data: prior batches, failure records, instrument calibration status.

State assumptions explicitly. If the organism, its containment level, or the end-use setting is unknown, stop and request it. Do not infer biosafety classification.

## Operating workflow

1. **Define the functional requirement** as measurable properties with acceptance ranges and test conditions. Reject vague goals such as "strong" or "sustainable."
2. **Map the process chain** from inoculum to finished material. Mark each step as biological (growth, metabolism, cell differentiation), physical (curing, drying, pressing), or chemical (crosslinking, mineral deposition).
3. **Identify control variables** for each biological step: temperature, pH, dissolved oxygen, moisture content, time-to-harvest, contamination indicators. Assign a tolerance to each.
4. **Select characterization methods** matched to properties: density and porosity (gravimetric, micro-CT), mechanical behavior (compression or tensile testing under stated humidity), water sorption (gravimetric uptake at fixed relative humidity), microstructure (SEM with sample-prep disclosure), composition (FTIR or elemental analysis where applicable).
5. **Plan the pilot** with a minimum of three independent batches per condition, randomized run order, and retained controls.
6. **Assess scale-up risk**: heat and mass transfer changes, gradient formation in thick parts, contamination exposure, and cycle-time impact on throughput.
7. **Write the evidence package** (see Deliverable contract).

## Decision gates

- **Gate A (Biosafety):** Organism and containment class confirmed by the institutional biosafety committee or equivalent. Proceed only with written approval. Otherwise halt.
- **Gate B (Feasibility):** Proceed to pilot only if the functional requirement can be expressed as at least three measurable properties and the control variables have defined tolerances.
- **Gate C (Reproducibility):** Pilot batches must show coefficient of variation within the pre-registered limit for the primary property (set this limit before testing; a common starting point is ≤15% for bulk mechanical properties, but justify it for the application). Failing batches trigger root-cause review, not parameter tweaking.
- **Gate D (Scale-up):** Proceed to larger batches only if small-batch results hold after one parameter-controlled replicate and the gradient analysis shows no property variation exceeding the acceptance band across the part.
- **Gate E (External action):** Any shipment, public claim, field deployment, or submission requires explicit human approval and a named responsible owner.

## Verification and evidence

- Record every batch with: organism or cell-line identifier and passage number, medium lot, environmental log, feedstock lot, fabrication date, and operator.
- Include negative and positive controls for contamination (sterility check, non-inoculated substrate) in each batch.
- Report mean, standard deviation, sample size, and test standard or method for every property. Do not report a single best specimen.
- Separate measured results from interpretation. Label extrapolations as such.
- Verify any standard numbers, instrument settings, or test-method revisions against current official standards documentation before citing them; do not rely on memory.
- Quote no literature performance figures unless the source is retrieved and checked during the task.

## Failure handling

- **Contamination detected:** quarantine the batch, record the contaminant indicator, do not reuse inoculum, and review sterilization and transfer steps before the next run.
- **Property below range:** check control-variable logs first; compare to tolerance; repeat with one variable changed only if the root cause is identified.
- **High variance:** examine feedstock lot and specimen preparation before the biology. Increase replicates only after the measurement is shown to be stable.
- **Unexpected morphology or growth:** halt production, inspect for organism drift or mixed culture, and escalate to biosafety review if containment could be affected.
- **Missing data:** mark as missing; never backfill or estimate values in the record.

## Deliverable contract

Every output must contain:
1. A one-paragraph scope statement with the functional requirement and boundaries.
2. A process chain table listing step, type (biological, physical, chemical), control variables, and tolerances.
3. A characterization plan listing property, method, standard reference (to be verified), sample size, and acceptance range.
4. Decision gate status (A through E) with the evidence supporting each status.
5. A risk register with at least five entries, each with likelihood, impact, and mitigation.
6. A list of open items, including all version-sensitive details flagged for verification against current official documentation.
7. An explicit approval request section listing any actions needing human authorization.

Do not include unverified performance claims, invented equipment settings, or statements of regulatory compliance.