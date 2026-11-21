---
name: metabolic-cell-biochemistry
description: Use when analyzing, designing, or interpreting cell metabolism work, including pathway mapping, flux and stoichiometry reasoning, enzyme kinetics, metabolite measurements, isotope tracing, and metabolic experiment or model review.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Metabolic Cell Biochemistry

## Purpose and boundaries

This skill supports professional work on cellular metabolism: reconstructing pathways, checking stoichiometry and thermodynamic feasibility, interpreting enzyme kinetics, designing and reviewing metabolomics and isotope-tracing experiments, and judging whether metabolic data support a stated conclusion.

In scope: central carbon metabolism (glycolysis, TCA cycle, pentose phosphate pathway, oxidative phosphorylation), amino acid and lipid metabolism, cofactor balance (NAD(P)H, ATP, acetyl-CoA, one-carbon units), compartmentalization, and genome-scale or kinetic model sanity checks.

Out of scope: clinical treatment decisions, dosing, wet-lab protocols that could cause harm without a supervising qualified scientist, and claims about human patients drawn from cell-line data alone.

## Inputs and assumptions

Request the following before drawing conclusions:
- Organism or cell system, medium composition (glucose, glutamine, serum, oxygen tension), and growth phase.
- Measurement type: absolute or relative metabolite levels, extracellular exchange rates, isotope labeling pattern and tracer identity, enzyme activity assays.
- Units, normalization basis (cell number, protein, volume, DNA), and replicate count.
- Model source and version if a stoichiometric or kinetic model is used.

State assumptions explicitly. Default assumptions to flag: metabolic steady state unless shown otherwise; intracellular metabolite pools are well mixed within a compartment; isotopic steady state only if labeling plateau was measured.

## Operating workflow

1. Define the question as a testable claim (for example, "knockdown of enzyme X redirects carbon from glycolysis to serine synthesis").
2. Draw the relevant network: list reactions, substrates, products, cofactors, compartments, and reversibility.
3. Check mass balance per reaction (atoms C, N, H, O, P, and charge where applicable). Reject any reaction that does not balance without an explicit transporter or exchange term.
4. Check thermodynamic direction using reported standard free energies and plausible metabolite concentration ranges. Mark reactions whose direction depends on unmeasured concentrations.
5. For kinetics, compare the observed rate with Km and Vmax ranges from the same organism and conditions where available; flag extrapolations.
6. For tracing, map each labeled fragment to atom transitions and predict mass isotopologue distributions before comparing with data.
7. Compare prediction against observation and enumerate alternative explanations (compartment exchange, salvage pathways, medium contribution, dilution by unlabeled pools).
8. Write the conclusion with its evidence grade and remaining uncertainty.

## Decision gates

- **Gate A, data sufficiency:** Proceed to flux or pathway conclusions only if at least three biological replicates exist, normalization is stated, and a blank or extraction control is reported. Otherwise report as exploratory.
- **Gate B, steady state:** If labeling or concentrations were measured at a single time point, do not claim steady-state flux. Request a time course or label the claim as a snapshot.
- **Gate C, compartment ambiguity:** If a metabolite is measured as whole-cell but the claim concerns a specific organelle, downgrade the claim unless fractionation data support it.
- **Gate D, model conclusions:** A model prediction may be reported as a hypothesis only. Require experimental or independent-data support before calling it a finding.
- **Gate E, external or consequential action:** Any step that orders reagents, modifies a shared dataset or model repository, submits to an external party, or generates protocols for live animal or human work requires explicit user approval and confirmation of the responsible investigator.

## Verification and evidence

Quality checks to report with every conclusion:
- Atom mapping balances for every reaction used (100% of reactions in the argument).
- Isotopologue predictions sum to 1 (within rounding) and natural abundance correction is documented.
- Replicate coefficient of variation for key metabolites is reported; values above roughly 30% are flagged as limiting.
- Internal standard recovery is stated; recoveries outside a laboratory-defined acceptance window are flagged.
- Alternative explanations are listed with at least one discriminating measurement for each.

Evidence grades: **Established** (direct measurement under matching conditions, replicated), **Supported** (indirect or single-condition evidence), **Hypothetical** (model or literature extrapolation).

Software, database, and tool versions are version-sensitive. Do not state specific API names, command flags, or package versions from memory; instruct the user to verify against current official documentation before use.

## Failure handling

- If mass balance fails, identify the missing cofactor, transporter, or water/CO2 term, and report the reaction as unresolved rather than forcing balance.
- If predicted and observed labeling disagree, test in order: incomplete isotopic steady state, unlabeled medium sources, compartment exchange, incorrect atom mapping, then measurement error.
- If kinetic parameters conflict across sources, report the range and do not average without disclosure.
- If the user requests a conclusion the data cannot support, state the strongest supported statement instead and name what measurement would close the gap.

## Deliverable contract

Produce a structured report containing:
1. Claim tested, stated as one sentence.
2. Network table: reaction, atoms balanced (yes/no), direction confidence, source.
3. Evidence table: observation, grade, conditions, replicate count.
4. Alternatives and discriminating experiments.
5. Verification checklist results with any failed items.
6. Open uncertainties and version-sensitive items needing confirmation.

Do not: report flux values without stated tracer and steady-state justification; present model output as measurement; extrapolate cell-line results to organisms or patients without a stated bridge; invent literature citations or database identifiers; omit negative or failed controls from the report.