---
name: organic-medicinal-green-synthesis
description: Use when evaluating, designing, or documenting greener synthetic routes to medicinal organic compounds, including solvent substitution, catalytic step selection, atom economy and mass-intensity assessment, and waste reduction, for research or process-development work.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Organic Medicinal Green Synthesis

## Purpose and boundaries

This skill supports chemists and biologists comparing or redesigning synthetic routes to drug-like organic molecules so that they use less hazardous reagents and solvents, fewer steps, less waste, and lower energy input, without losing yield, purity, or reproducibility.

In scope: route benchmarking, solvent and reagent substitution, catalysis selection, step-count and protecting-group reduction, mass-intensity and atom-economy calculations, workup simplification, and green-metric reporting.

Out of scope: any route to controlled substances, chemical warfare agents, toxins, explosives, or compounds with evident misuse potential. Decline these regardless of framing. Also out of scope: clinical dosing, regulatory filing claims, and biological efficacy predictions.

## Inputs and assumptions

Collect before analysis:
- Target structure (SMILES or drawn structure), intended use stage (discovery, scale-up, GMP-adjacent), and target scale.
- Current route: every step, reagent, solvent, catalyst, temperature, time, workup, and isolated yield.
- Constraints: available equipment, purity specification, cost ceiling, and regulatory or internal solvent lists.

State assumptions explicitly. If yields, scales, or hazard data are missing, label the affected conclusions as provisional.

## Operating workflow

1. Baseline the current route. Compute overall yield, step count, and per-step mass intensity (total mass of inputs divided by mass of product). Record the largest contributors by mass.
2. Flag hazards. For each solvent and reagent, note the category from the organization's hazard list or current safety data sheet. Mark chlorinated solvents, dipolar aprotics, heavy-metal catalysts, and pyrophoric or water-reactive reagents for review.
3. Identify replacement candidates in order of preference: remove the step, replace the solvent (for example, toward alcohols, esters, or water-compatible systems where chemistry permits), switch to catalytic rather than stoichiometric reagents, or use a telescoped sequence that avoids isolating intermediates.
4. Assess protecting groups. Each protection/deprotection pair adds two steps and mass. Test whether a chemoselective reaction removes the need.
5. Evaluate energy and processing: prefer reactions that run near ambient temperature, avoid cryogenic steps where practical, and minimize chromatography by designing crystallization or extraction-based purification.
6. Run a small-scale comparison (typically 0.5 to 2 mmol for screening, with replicates) of the baseline and the proposed route at identical concentrations.
7. Recalculate metrics and record the result alongside purity and impurity profile.

## Decision gates

- **Gate A (proceed to screening):** Proposed change removes at least one hazardous reagent or solvent, or reduces mass intensity by at least 20% in a defined step, with no known safety regression.
- **Gate B (proceed to scale-up):** Screening yield within 5 percentage points of baseline, impurity profile equal or better by the analytical method used, and reproducible across at least three runs.
- **Gate C (stop and escalate):** Any new energetic intermediate, gas evolution not previously controlled, exotherm not characterized by calorimetry, or any step touching a regulated substance. Require explicit approval from the responsible safety and compliance owner before continuing.

Require explicit human approval before: running any reaction above the approved scale, disposing of waste streams in a way that differs from existing procedure, sharing routes outside the team, or submitting data externally.

## Verification and evidence

- Confirm product identity by at least two orthogonal methods (for example NMR and HRMS, or NMR and HPLC retention against a reference).
- Report purity by a validated method and state the method version and detection limits.
- Calculate: overall yield, process mass intensity, atom economy per step (stoichiometric basis), and solvent intensity (solvent mass per gram product). Show calculation inputs.
- Do not quote green-metric improvements as absolute values without the baseline and the calculation basis.
- Verify any safety or hazard classification against current official documentation, since classifications change between revisions.

## Failure handling

- Yield drop greater than 5 points or new impurity above the reporting threshold: revert to baseline conditions, then change one variable at a time (solvent, then catalyst loading, then temperature).
- Unexpected exotherm, gas, or color change suggesting decomposition: stop, quench per existing procedure, and report as a safety event. Do not scale.
- Conflicting literature or vendor data: record both, run a discriminating experiment, and do not average them.
- If a greener solvent fails only at scale, document the mixing, solubility, and heat-transfer differences rather than assuming the screen was representative.

## Deliverable contract

Produce a route comparison report containing:
1. Target, scale, and stated assumptions.
2. Table of baseline and proposed steps with reagents, solvents, temperatures, times, and isolated yields.
3. Metrics table: overall yield, PMI, atom economy, solvent intensity, step count.
4. Hazard changes, listed per substance, with the source and revision date of each classification.
5. Gate decisions (A, B, C) with the evidence behind each.
6. Open items, each with an owner and the approval required.

Do not present unverified claims, invented benchmark numbers, or compliance statements as established facts.