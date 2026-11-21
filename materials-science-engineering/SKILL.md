---
name: materials-science-engineering
description: Use when selecting, specifying, or qualifying engineering materials, interpreting material test data, diagnosing material-related failures, or reviewing heat treatment, joining, or corrosion-protection decisions for metals, polymers, ceramics, and composites.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Materials Science Engineering

## Purpose and boundaries

This skill supports engineering judgment on material selection, property interpretation, process-structure-property reasoning, and failure analysis for structural, thermal, and environmental service. It covers metals (steels, aluminum, titanium, nickel alloys), polymers, ceramics, glasses, and fiber-reinforced composites.

It does not replace a licensed engineer's sign-off, a certified materials laboratory, or applicable code compliance (for example pressure vessel, aerospace, medical, or nuclear codes). It does not certify that any material meets a standard. Outputs are recommendations requiring qualification by the responsible engineer.

## Inputs and assumptions

Before recommending anything, establish:

1. Service envelope: load type (static, cyclic, impact), temperature range, environment (chemistry, humidity, UV, radiation), design life.
2. Geometry and manufacturing route: section thickness, welding, machining, forming, additive, casting.
3. Governing requirements: specification, code, customer drawing, or regulatory class.
4. Available data: certified mill test reports, supplier datasheets (note the test condition and orientation), prior test results, failure photographs, fractography.
5. Constraints: cost ceiling, lead time, recyclability, supply chain restrictions.

Record any missing input as an explicit assumption. Do not fill gaps with typical values presented as guaranteed.

## Operating workflow

1. Define the function in measurable terms: required yield strength, fatigue life at stress amplitude, maximum service temperature, allowable corrosion rate.
2. Shortlist two to four candidate material families using service envelope limits. Eliminate any candidate that fails a hard constraint before comparing soft ones.
3. Map processing to structure: identify heat treatment state, grain size, phase content, residual stress, and surface condition that the supplier must control.
4. Compare candidates on a weighted table covering strength at temperature, toughness at minimum service temperature, corrosion or oxidation resistance, fabricability, and cost per functional unit.
5. For welded or joined parts, evaluate heat-affected zone properties and filler compatibility, not parent metal alone.
6. Specify verification tests matched to the failure mode (see Verification).
7. Write the recommendation with stated assumptions and open risks.

## Decision gates

- Gate A (temperature): if service temperature exceeds about 0.4 times the absolute melting temperature for a metal, evaluate creep explicitly. Do not rely on room-temperature yield data.
- Gate B (brittleness): for ferritic steels, aluminum alloys in cryogenic service, or polymers near glass transition, require notched toughness data at the minimum service temperature before approval.
- Gate C (fatigue): if the part sees cyclic loading, require fatigue data at the relevant stress ratio and surface finish, and check notch sensitivity at all geometric discontinuities.
- Gate D (corrosion): if chloride, sulfide, or acidic exposure is present, require a documented corrosion test or service history from comparable conditions. Galvanic couples require an explicit mismatch assessment.
- Gate E (composites): do not approve laminate designs without void content, fiber volume fraction, and moisture conditioning data.
- Gate F (novel or unqualified material): stop and escalate to a qualified materials engineer if no existing standard or service history supports the choice.

## Verification and evidence

- Traceability: every property value must cite its source document, test standard, specimen orientation, and test temperature. Unsourced values are not evidence.
- Heat lot match: confirm mill certificates match the heat and heat treatment lot used in production.
- Acceptance tests: tensile, hardness, impact, and microstructure checks sized to the specification. Hardness-to-strength conversions are approximate and must be labeled as such.
- Failure analysis: preserve the fracture surface. Document macro photos, fracture origin, beach marks or striations where present, and chemical composition at the origin. Do not clean or section the fracture before documentation.
- Quantitative quality checks: grain size within specified ASTM or equivalent range, weld hardness below the specified maximum, porosity or void fraction within the specified limit.

Version-sensitive items (standard revision letters, current alloy designations, code edition years, supplier property sheets) must be verified against current official documentation before use.

## Failure handling

- If test data conflict with supplier values, do not average them. Investigate specimen orientation, heat treatment, and test rate first.
- If a failure origin is unidentified, state the leading hypotheses and the discriminating test for each. Do not assert a root cause without fractographic or chemical evidence.
- If a required property is unavailable, mark the recommendation conditional and list the test that would close the gap.
- If a requested approval would cross a decision gate without evidence, decline the approval and state which evidence is missing.

## Deliverable contract

Produce a single report with these sections:

1. Summary recommendation (one paragraph, with conditions).
2. Service envelope and assumptions (table).
3. Candidate comparison (weighted table with sources cited).
4. Gate results (pass, fail, or escalate for each applicable gate).
5. Verification plan (tests, acceptance criteria, responsible party).
6. Open risks and required approvals.

Do not state that a material is "certified," "compliant," or "guaranteed" unless a named document demonstrates it. Do not present unverified numeric values as design allowables. Actions that destroy or alter evidence (sectioning fractures, scrapping lots, changing specifications, sending specifications to suppliers or customers) require explicit written approval from the responsible engineer before execution.