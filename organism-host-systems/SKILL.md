---
name: organism-host-systems
description: Use when selecting, comparing, or operating a biological host organism or cell system (bacterial, yeast, fungal, insect, plant, or mammalian cell) for recombinant expression, biotransformation, or culture-based chemical production, and when troubleshooting host performance.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Organism Host Systems

## Purpose and boundaries

This skill covers the practical choice and management of a living host system used to produce a protein, metabolite, or chemical transformation. It spans host selection, construct compatibility, culture operation, expression measurement, contamination control, and host-specific troubleshooting.

It does not cover: clinical or diagnostic use, in vivo animal work, enhancement of pathogen traits, field or environmental release, or regulatory submissions. Route those to the appropriate institutional committee or specialist.

## Inputs and assumptions

Before proceeding, collect:

1. Target product, its required form (soluble, secreted, membrane-bound, glycosylated, cofactor-dependent), and minimum yield or titer.
2. Biosafety class of the proposed host and any inserted sequences. Confirm the institutional biosafety approval covers this host and construct.
3. Available genetic tools and their current status (plasmid systems, markers, inducible promoters). Note that tool availability changes; verify against current official vendor and lab documentation.
4. Facility constraints: incubation, bioreactor scale, containment level, and waste handling.
5. Prior data: growth curves, failed runs, sequence files, and strain provenance.

Assume nothing about strain identity or purity until verified.

## Operating workflow

1. **Define the product requirement.** Write the target as a measurable specification (e.g., mg per liter of purified, active protein; conversion percentage at a given time).
2. **Shortlist hosts.** Compare at least two candidates against: post-translational needs, secretion capacity, codon and cofactor compatibility, growth rate, and known toxicity of the product to the host.
3. **Verify the construct.** Sequence-confirm the full expression cassette, including promoter, tags, and selection marker. Check for internal restriction or reading-frame errors.
4. **Establish a small-scale pilot.** Use a minimum of three biological replicates in parallel with a positive and empty-vector control. Sample at fixed intervals for OD or cell density, product readout, and viability.
5. **Optimize one variable at a time** or use a designed factorial screen. Typical variables: inducer concentration, induction temperature and timing, medium composition, and feeding strategy.
6. **Scale only after reproducibility.** Move up one scale step at a time, rechecking product quality at each step.
7. **Document lineage.** Record strain ID, passage number, glycerol stock location, and every culture parameter.

## Decision gates

- **Gate A (host choice):** Proceed with a host only if it meets the product's folding and modification requirements, or a documented engineering path exists.
- **Gate B (construct):** Do not induce a culture until sequence identity is confirmed and the stock is shown to be free of contamination by streak purity or equivalent.
- **Gate C (scale-up):** Advance only if pilot results show replicate coefficient of variation below 20% for the primary readout, and product identity is confirmed.
- **Gate D (containment change):** Stop and seek approval before changing host class, adding a new resistance marker, altering containment level, or introducing sequences from a higher-risk organism.

## Verification and evidence

- Product identity: intact mass or equivalent identity check, plus activity or conversion assay against a reference standard.
- Purity: a separation method appropriate to the product, reported with lane or trace images or raw values.
- Host health: growth curve, viability fraction, and absence of unexpected morphology under microscopy.
- Contamination: plating on non-selective and selective media, and a periodic check of a no-inoculum control.
- Reproducibility: report mean and spread across at least three independent cultures. Never report a single best run as the result.

## Failure handling

- **No expression:** Check the construct sequence, then inducer activity, then host toxicity by comparing growth with and without induction. Do not raise inducer concentration above the manufacturer's stated range without a dose series.
- **Insoluble product:** Test lower temperature, a solubility tag, and co-expression of chaperones in one comparative set. Record each change.
- **Growth collapse after induction:** Reduce expression strength or induction duration before changing host.
- **Unexpected band or mass:** Suspect proteolysis, truncation, or plasmid loss; confirm with a second method before revising the hypothesis.
- **Contamination:** Discard the affected culture and its shared reagents. Re-streak from the last verified stock. Do not reuse working stocks from a contaminated run.

## Deliverable contract

Each report must include:

1. Product specification and host rationale, with the decision gate outcomes stated.
2. Construct verification record with sequence identity evidence.
3. Growth and product data tables, with replicate counts, units, and variance.
4. Raw data file locations and any deviations from the protocol.
5. Open risks and the next gated step.

Do not state yields, activities, or optimal conditions that were not measured in this work. Do not describe a host as "safe" or "compliant"; state only the containment level and approval status on record.