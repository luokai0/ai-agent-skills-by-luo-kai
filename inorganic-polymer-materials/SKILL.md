---
name: inorganic-polymer-materials
description: Use when planning, interpreting, or reviewing work on inorganic polymers such as polyphosphazenes, polysiloxane backbones, polysilanes, polyphosphates, sulfur-based polymers, geopolymers, alkali-activated binders, and silicate or phosphate glasses, including synthesis routes, structure-property analysis, and biological-interface claims.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Inorganic Polymer Materials

## Purpose and boundaries

This skill guides technical work on polymers whose backbone contains no continuous carbon-carbon chain: main-group chains (Si, P, S, Ge, Sn), mineral networks (aluminosilicate, phosphate), and biological inorganic polyphosphates. It covers:

- Route selection, stoichiometry, and reaction-condition reasoning
- Characterization planning and data interpretation (molecular weight, thermal, spectroscopic, structural)
- Property claims for thermal, mechanical, hydrolytic, and biological behavior
- Reporting that separates measured results from inference

It does not cover organic-backbone polymers with inorganic side groups unless the backbone chemistry is the question, nor clinical, regulatory, or occupational-safety certification. Treat hazardous reagents (chlorosilanes, phosphorus halides, polysulfides, alkali hydroxides at high concentration, elemental sulfur at high temperature) as requiring approved protocols.

## Inputs and assumptions

Collect before analysis:

1. Target backbone and end groups, with intended molecular weight or degree of polymerization.
2. Available precursors, purity grades, and moisture or oxygen sensitivity.
3. Intended use: structural, thermal, dielectric, matrix, biomaterial, or research standard.
4. Existing data: spectra, chromatograms, thermograms, mechanical curves, with instrument and calibration details.

State every assumption explicitly. If purity, water content, or calibration is unknown, label conclusions as provisional.

## Operating workflow

1. Define the target property and the failure mode you must avoid (e.g., hydrolysis of P-N or Si-O-Si bonds, chain scission, phase separation).
2. Choose the route. Ring-opening polymerization suits phosphazenes and siloxanes when cyclic monomers are accessible; polycondensation suits silicates and phosphates; alkali activation suits aluminosilicate binders. Justify the choice against moisture tolerance and byproduct removal.
3. Calculate stoichiometry from measured precursor purity, not nominal labels. Record the water and residual-solvent budget.
4. Specify a characterization set before synthesis: NMR of relevant nuclei (²⁹Si, ³¹P, ²⁷Al where applicable), FTIR or Raman for bond identity, SEC or GPC for molar mass with a stated calibration standard, TGA/DSC for decomposition and transitions, XRD for crystallinity.
5. Execute in controlled conditions, logging atmosphere, temperature, and time.
6. Compare results to the target against pre-stated acceptance criteria.
7. Document provenance of every number.

## Decision gates

- **Gate A (route):** Proceed only if the chosen route avoids reagents that produce uncontrolled byproducts (e.g., HCl or HF release) without an approved ventilation and neutralization plan.
- **Gate B (molar mass):** Molar mass from SEC on a polymer with a different chemistry than the calibration standard is relative, not absolute. Report it as relative unless an absolute method (light scattering, end-group NMR) confirms it.
- **Gate C (hydrolytic stability):** Any claim of stability in water, body fluid, or humid environments requires time-series data under stated conditions. Without it, claim only the measured condition.
- **Gate D (biological interface):** Claims of biocompatibility, degradation products, or ion release need cytotoxicity or release data from a qualified laboratory. Do not extrapolate from polyphosphate chemistry alone.
- **Gate E (scale-up):** Move beyond gram scale only after reproducibility over at least three independent runs with spread reported.

## Verification and evidence

- Confirm backbone identity with at least two orthogonal techniques.
- Check mass balance and integration ratios in NMR against expected repeat-unit composition; a deviation above the stated tolerance triggers re-analysis.
- Report SEC dispersity (Đ) with the calibration basis.
- Compare TGA residue against the calculated inorganic fraction.
- For geopolymers, report the Si/Al ratio, alkali concentration, curing temperature, and age at test.
- Mark every database value, literature property, or instrument specification as requiring verification against current official documentation or the original source when versions, calibrations, or standards may have changed.

## Failure handling

- **Unexpected hydrolysis or gelation:** Stop, check moisture and solvent water content, and repeat with dried reagents before changing the route.
- **Broad or bimodal SEC trace:** Test for oligomers, cyclics, or crosslinking before reporting an average molar mass.
- **NMR shifts disagree with literature:** Verify referencing and solvent; do not reassign peaks without a second method.
- **Inconsistent mechanical data:** Check specimen geometry, aging, and humidity history before attributing differences to chemistry.

Do not average results across incompatible conditions.

## Deliverable contract

Every deliverable must contain:

1. Target, route, and key assumptions.
2. A table of measured values with method, conditions, and replicate count.
3. Explicit separation of measured results, calculated values, and literature-based statements.
4. Pass/fail status against each acceptance criterion.
5. Items requiring approval (hazardous procedures, external sharing, biological or clinical claims, scale-up).
6. A list of values flagged for verification against current official documentation.

Do not state compliance, safety certification, or regulatory suitability. Do not invent instrument settings, reference values, or benchmark results.