# Chemistry, Biology, and Materials

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

## ai-research-life-sciences

**Use when:** Use when an AI-assisted task needs to search, retrieve, cross-check, or summarize life-sciences evidence from external registries and databases such as literature indexes, clinical trial registries, sequence and structure archives, bioactivity databases, and preprint servers.

### Purpose and boundaries

This skill governs how to find, verify, and synthesize life-sciences records from external registries for research support: literature reviews, trial landscape scans, target or variant lookups, compound and bioactivity checks, and dataset discovery.

In scope: query design, record retrieval, deduplication, provenance tracking, cross-registry reconciliation, and evidence-graded summaries.

Out of scope: clinical decisions for individual patients, dosing recommendations, regulatory submissions, wet-lab protocol design, and any output presented as validated medical advice. Route those to qualified humans.

### Inputs and assumptions

Before searching, establish:

1. The research question in one sentence, with population, intervention or entity, comparator, and outcome where applicable.
2. The decision the output will inform (e.g., shortlisting targets, scoping a review, checking prior trials).
3. Date window and recency requirement.
4. Which registries the user has access to. Do not assume institutional subscriptions or API keys.
5. Whether the user has supplied data files, which may contain confidential or patient-level content.

If any item is missing and changes the search, ask once. Otherwise state the assumption in the output.

### Operating workflow

1. **Decompose the question** into entity sets (genes, proteins, compounds, diseases, outcomes) and map each to registry-specific identifiers. Record the mapping table.
2. **Draft queries per registry** using controlled vocabularies where available (e.g., MeSH for literature, condition and intervention fields for trial registries, gene symbols plus species for sequence archives). Save each query string verbatim.
3. **Retrieve in tiers**: broad recall first, then filter by study design, date, and identifier validity. Log hit counts at each step.
4. **Deduplicate** using stable identifiers (DOI, PMID, NCT number, accession, InChIKey) before fuzzy title matching. Merge preprint and peer-reviewed versions and flag the relationship.
5. **Extract structured fields** into a table: source, identifier, date, design or assay type, population or system, key quantitative result, limitations stated by authors.
6. **Cross-check** claims against at least one independent registry where possible (e.g., a trial result against its registry entry and the published report; a bioactivity value against the original assay source).
7. **Grade evidence** (see Verification).
8. **Write the synthesis** separating what the sources report from what you infer.

### Decision gates

- **Gate A, scope:** If the question yields more than roughly 2,000 candidate records, narrow with the user before extracting. Do not silently sample.
- **Gate B, source quality:** Preprints, predatory-venue articles, and unregistered trials are reported only with an explicit quality flag. Never cite them as established.
- **Gate C, conflicts:** If registries disagree (e.g., enrollment counts, accession versions, compound identifiers), report both values with sources and do not pick one without a stated rule.
- **Gate D, external actions:** Submitting queries at volume, using credentials, downloading restricted or licensed data, or posting results to any external system requires explicit user approval. Rate-limit and respect terms of use.
- **Gate E, sensitive data:** If inputs contain identifiable patient data, stop and confirm the handling basis and whether the data may leave the local environment.

### Verification and evidence

- Every factual claim carries a source identifier. Claims without one are labeled "unverified inference."
- Verify each identifier resolves to the record cited, and that the record date and version match what is quoted.
- Quantitative values are copied with units and denominators; never rounded silently.
- Benchmark or performance statements are reported only from the source, never recalled from memory.
- Evidence labels: *primary report*, *registry entry*, *secondary review*, *preprint*, *model-generated inference*.
- Quality checks before delivery: 100% of cited identifiers resolved; zero duplicate records in the final table; every excluded record has a logged reason; every conflict is listed.
- API names, parameters, field names, and schema versions change. Mark any such detail "verify against current official documentation" and do not state it from memory as current.

### Failure handling

- **Registry unavailable or rate-limited:** Record the timestamp and endpoint attempted, pause, and report partial coverage with the gap named explicitly.
- **Zero hits:** Broaden one dimension at a time (synonyms, parent terms, species), logging each attempt. Report the null result as a finding with the queries used.
- **Identifier mismatch:** Do not guess the correct record. Mark it unresolved.
- **Retracted or withdrawn source discovered:** Remove it from supporting evidence, list it in a separate exclusions section, and check dependent conclusions.

### Deliverable contract

Return:

1. **Question and scope** (restated, with assumptions).
2. **Query log** (registry, query string, date run, hit count).
3. **Evidence table** (source ID, date, design or type, key result, evidence label, quality flag).
4. **Conflicts and gaps** (listed, not resolved by fiat).
5. **Synthesis** (short, with inferences marked).
6. **Limitations and verification items** (version-sensitive details, unresolved identifiers, access limits).

Do not include: uncited numerical claims, invented accession numbers, recalled benchmark figures, guarantees of completeness, or clinical recommendations.


## analytical-spectroscopic-electrochemical-analysis

**Use when:** Use when designing, running, or interpreting coupled spectroscopic and electrochemical measurements (spectroelectrochemistry, UV-Vis/fluorescence/Raman/IR monitored voltammetry, EIS with optical readout) on chemical or biological systems, including redox mechanism assignment, quantitative calibration, and data QC.

### Purpose and boundaries

This skill guides analysis where an electrochemical perturbation (potential, current, or impedance) is paired with a spectroscopic readout to identify species, redox states, reaction intermediates, or adsorption behavior, and to quantify analytes. It covers experimental design, data validation, mechanistic interpretation, and reporting.

It does not cover: clinical diagnosis or decisions on patient samples, industrial process release, regulatory submissions (these require the governing guideline and a qualified reviewer), or synthesis planning unrelated to the measurement.

### Inputs and assumptions

Collect before starting:
- Analyte identity, expected redox couples, and literature or prior E° estimates with source.
- Solvent, supporting electrolyte and concentration, pH (aqueous) or water content (non-aqueous), dissolved oxygen treatment.
- Electrode configuration: working material and area, counter, reference type and filling solution, cell path length for optical work.
- Optical setup: source, wavelength or Raman shift range, detector, spectral resolution, and whether the optical path passes through the electrode region.
- Biological samples: matrix, handling history, biosafety classification, and institutional approval status.

Assumptions to state explicitly: electrode stability window, analyte stability on the timescale of the scan, and that the optical signal is proportional to concentration over the working range (verify, do not assume).

### Operating workflow

1. **Baseline the system.** Record background voltammogram and spectrum of electrolyte alone. Subtract only when the background is stable across repeats.
2. **Verify the reference.** Measure an internal standard (ferrocene/ferrocenium is common in non-aqueous work; report potentials against it) or a known couple in the same cell. Record the offset.
3. **Scan rate series.** Run CV at multiple scan rates (e.g., at least five, spanning a decade). Plot peak current versus ν^1/2 and versus ν. Diffusion control shows linearity with ν^1/2; adsorption shows linearity with ν.
4. **Couple spectra.** Acquire spectra at defined potentials (potential-step or during slow scans), holding the cell at each potential until current decays to a stated threshold before recording.
5. **Isosbestic and band analysis.** Identify isosbestic points for two-species interconversion. Track band intensity versus potential and fit to Nernstian or Butler-Volmer-derived forms as appropriate.
6. **Calibration (quantitative work).** Prepare at least five standards bracketing the expected concentration, plus blanks. Use matrix-matched standards for biological samples.
7. **Impedance (if used).** Measure EIS at the formal potential and at off-peak potentials; check validity before fitting equivalent circuits.

### Decision gates

- **Gate A (reversibility):** Peak separation ΔEp near 59/n mV at 25 °C indicates a fast one-electron reversible couple. Larger separation or ΔEp varying with scan rate indicates quasi-reversible or irreversible kinetics; do not apply reversible equations.
- **Gate B (mass transport):** Proceed with diffusion-based quantification only if peak current scales with ν^1/2 (R² ≥ 0.98 across the series). Otherwise investigate adsorption or coupled chemistry.
- **Gate C (spectral assignment):** Assign a species to a spectral feature only when the spectrum changes with potential in step with the electrochemical wave and a reference spectrum or independent measurement supports it.
- **Gate D (calibration validity):** Accept a calibration only if R² ≥ 0.995, residuals show no systematic trend, and blank signal is below one-third of the LOQ target.
- **Gate E (instrument drift):** Halt and re-reference if the reference offset changes by more than 10 mV between start and end of a run.
- **Gate F (approval):** Stop before any step that exposes a live biological specimen to uncharacterized potentials, discharges electroactive or hazardous material, or transmits data containing identifiable or proprietary information outside the approved system. Obtain explicit written approval from the responsible person first.

### Verification and evidence

- Report every potential against a stated reference, with offset applied and recorded.
- Provide raw data, instrument settings, and the scan-rate or concentration series used for each conclusion.
- For quantitative results, report LOD and LOQ with the method used (state the method; do not claim it satisfies any specific regulation).
- Check background-subtracted spectra for artifacts: solvent band shifts, electrode-induced absorbance, and bubble formation.
- Run at least three independent replicates for any reported value; report mean and standard deviation.
- Mark version-sensitive instrument, software, or database details as requiring verification against current official vendor documentation.

### Failure handling

- **Drifting baseline or unstable current:** Check reference junction, degas again, and confirm cell connections. Do not average unstable runs.
- **Non-linear calibration:** Test for adsorption, matrix suppression, or photodegradation under the light path. Reduce concentration range or change path length.
- **Spectral change without electrochemical wave:** Likely chemical or photochemical; run a no-potential control under identical illumination.
- **Electrode fouling:** Document the fouling signature, polish or replace per the electrode protocol, and exclude runs performed on a fouled surface.

### Deliverable contract

Produce a report containing: objective; system and reference description; experimental parameters; raw and processed data references; gate outcomes with the evidence for each; mechanistic or quantitative conclusion with stated uncertainty; limitations; and a list of items still requiring verification. Do not present a mechanism as established when only one gate is passed.


## bio-genomics-lookup

**Use when:** Use when a user needs to look up gene, variant, transcript, or genome-annotation information from public genomics databases and return verified, source-cited answers for research or analysis work.

### Purpose and boundaries

This skill resolves biological identifiers and retrieves annotation facts (gene symbols, coordinates, transcripts, protein products, variant records, clinical-significance labels, cross-references) from public reference databases, then reports them with provenance. It covers lookup and reconciliation, not interpretation of patient data, clinical decisions, or novel bioinformatic pipelines.

In scope: symbol-to-identifier mapping, genome build conversion checks, canonical transcript selection, variant identifier normalization, reporting of database-asserted annotations, and flagging conflicts between sources.

Out of scope: diagnosing conditions, recommending treatments, classifying variants for clinical reports without a qualified reviewer, uploading identifiable genetic data to external services, and asserting results that were not retrieved in the current session.

### Inputs and assumptions

Collect before querying:

1. The query type: gene, transcript, protein, variant, region, or cross-reference.
2. The identifier as given (symbol, Ensembl ID, RefSeq accession, HGVS string, rsID, genomic coordinate).
3. The target genome assembly (for example GRCh38 or GRCh37). If absent, state the assumption explicitly and report both builds when coordinates matter.
4. The intended use: exploratory, manuscript, or input to a downstream tool. Higher stakes require stricter gates.
5. Whether the query includes any personal or patient-linked data. If yes, stop and see Decision gates.

Assumptions to state in every output: the database versions consulted and the retrieval date. Symbols are mutable; accessions are more stable. Prefer stable identifiers for reporting.

### Operating workflow

1. **Classify the identifier.** Match the string against known formats: HGNC symbol, Ensembl gene (ENSG), transcript (ENST), protein (ENSP), RefSeq (NM_, NP_, NC_), dbSNP rsID, HGVS notation, or coordinates. Ambiguous symbols (for example names that collide with aliases) require a check against the official nomenclature authority.
2. **Resolve to a stable identifier.** Map the input to one gene record and one assembly. Record the mapping path.
3. **Retrieve core fields.** Symbol, full name, chromosome, start, end, strand, biotype, canonical transcript, and cross-references.
4. **Retrieve variant fields if applicable.** Reference and alternate alleles, HGVS forms (genomic, coding, protein), consequence terms, population frequency summaries, and submitted clinical-significance records, each labeled with its source and review status.
5. **Cross-check.** Compare coordinates and symbols across at least two sources where feasible. Note discrepancies rather than silently choosing one.
6. **Compose the answer** using the Deliverable contract.

### Decision gates

- **Gate A: Identifier ambiguity.** If the input matches more than one record, stop and present candidates with assembly and biotype. Do not pick silently.
- **Gate B: Assembly mismatch.** If a user's coordinates lack a build, or they conflict with the requested build, request confirmation before conversion. Use an official liftover tool and report the chain used.
- **Gate C: Sensitive data.** If the query contains patient identifiers, individual genotypes, or any data that could identify a person, pause and request explicit approval before any external lookup. Prefer offline reference files supplied by the user.
- **Gate D: External submission.** Sending identifiers to a remote service is an external action. Confirm with the user first when the query includes non-public variants or unpublished gene lists.
- **Gate E: Clinical use.** If the stated purpose is clinical reporting, return the retrieved records only, label them as unreviewed database assertions, and recommend review by a certified professional. Do not produce a pathogenicity call.

### Verification and evidence

Every factual claim in the output must trace to a retrieved record. Include for each claim: source database, record identifier, assembly, and retrieval date.

Quality checks before delivery:
- Symbol, Ensembl ID, and chromosome location agree across the cited records (or the disagreement is reported).
- Coordinates satisfy start less than or equal to end, and strand is one of plus or minus.
- Canonical transcript is named by the source's canonical flag, not by inference.
- Variant HGVS strings re-parse against the reference allele at the stated position where a validator is available.
- No field is filled from memory. If a field could not be retrieved, write "not retrieved."

Version-sensitive details (database release numbers, API endpoints, field names, query parameters, rate limits) must be checked against current official documentation before being stated. Do not present them from memory.

### Failure handling

- **Service unreachable or rate-limited:** retry once after a short wait, then report the failure and the partial results. Do not fill gaps from prior knowledge.
- **No match found:** check for outdated symbols, retired accessions, and alias tables. Report the search steps taken.
- **Conflicting sources:** present both values with their sources and state which the user should adopt for their assembly.
- **Assembly mismatch discovered after answering:** issue a correction stating the affected fields and the corrected values.

### Deliverable contract

Return a structured answer with these parts, in order:

1. **Query:** the input exactly as received, with query type and assumed assembly.
2. **Resolved record:** stable identifiers, symbol, coordinates, strand, biotype, canonical transcript.
3. **Findings:** labeled fields, each with source, record ID, and retrieval date.
4. **Discrepancies:** conflicts or "none found."
5. **Limitations:** unretrieved fields, version caveats, and any gate that was triggered.

Do not state that results are clinically valid, guaranteed, or complete. Do not invent identifiers, frequencies, or significance labels. Do not reproduce large sequence blocks unless the user explicitly requests them and the gate for external submission has been cleared.


## chemical-process-engineering

**Use when:** Use when designing, reviewing, simulating, or troubleshooting chemical process flowsheets, unit operations, mass and energy balances, equipment sizing, process safety reviews, or process control strategies for continuous or batch chemical plants.

### Purpose and boundaries

This skill guides engineering analysis of chemical process systems: material and energy balances, unit operation selection and sizing, thermodynamic feasibility, flowsheet integration, preliminary hazard identification, and control-structure review.

In scope: steady-state and short-horizon dynamic analysis, screening-level equipment sizing, reactor and separation selection, utility and heat integration, and HAZOP-style prompts.

Out of scope: final stamped design, pressure-vessel code calculations that require a licensed engineer of record, regulatory filings, and operating instructions for live plants. Outputs are engineering analyses for review by a qualified professional.

### Inputs and assumptions

Before analysis, collect or explicitly assume:

1. Basis: production rate, feed composition, feed temperature and pressure, product specifications, operating hours.
2. Thermodynamic model and property source (e.g., equation of state, activity model). State the model; do not assume ideality for polar, associating, or high-pressure systems.
3. Kinetics or reaction stoichiometry, with source and temperature range.
4. Constraints: materials of construction, utilities available, site elevation, environmental limits.
5. Units. Convert everything to one consistent system and record it.

Label every assumption as **[A]** with a short justification. Unlabelled assumptions are defects.

### Operating workflow

1. **Define the basis and closure.** Write the overall mass balance for each component. Confirm degrees of freedom: count streams, variables, and specifications. A flowsheet with more specifications than degrees of freedom is over-constrained; flag it.
2. **Screen thermodynamics.** Check phase behavior at operating conditions. Identify azeotropes, two-phase regions, and decomposition or polymerization risk.
3. **Select unit operations.** Compare candidates on separation difficulty (relative volatility, feed-to-product ratio), energy demand, and fouling. Prefer simpler equipment when performance is equivalent.
4. **Perform balances unit by unit.** Compute outlet streams, duties, and recycle loops. Iterate recycles to a stated tolerance (for example, 0.1% on the recycled flow).
5. **Size equipment at screening level.** Use standard correlations and state their source. Examples: flash drum vapor disengagement, heat exchanger LMTD with a correction factor for multipass units, column diameter from flooding fraction (target typically 70–80% of flood).
6. **Integrate energy.** Build a pinch-style summary of hot and cold streams with a stated minimum approach temperature (ΔTmin). Report utility demand before and after integration.
7. **Review control and safety.** Propose a control structure with controlled, manipulated, and measured variables. Run a HAZOP-style deviation review (more/less/no/reverse/other) on critical nodes.
8. **Document.** Produce the deliverable contract below.

### Decision gates

- **Gate 1 (basis):** Do not proceed past balances if feed composition or a product specification is missing. Request it.
- **Gate 2 (thermodynamics):** If the chosen property model is outside its validated range (pressure, temperature, composition), stop and recommend experimental data or a validated model.
- **Gate 3 (separation):** If relative volatility is below about 1.05 in distillation, consider extractive or azeotropic distillation, membranes, or crystallization before accepting conventional columns.
- **Gate 4 (safety):** Any reactor with exothermic reaction, flammable inventory above screening thresholds, or high-pressure operation requires a formal PHA (HAZOP, LOPA) before results are used. Recommend this; do not declare the design safe.
- **Gate 5 (approval):** Explicit user approval is required before issuing anything that changes equipment specifications, operating setpoints, or safety interlocks, and before any output that would be sent to a regulator, vendor, or operator.

### Verification and evidence

Check each result with at least one independent method:

- Overall and component balances close within 0.5% (state the actual residual).
- Energy balance closes within 1% of the largest duty.
- Equilibrium stage counts agree with a shortcut method (Fenske–Underwood–Gilliland) within about 20%; larger gaps indicate an error or a poor model.
- Pressure drops are consistent with velocity limits (for example, typical liquid line velocities 1–3 m/s; confirm against project standards).
- Units are dimensionally checked in every equation.

Mark any value taken from memory or a correlation as **[VERIFY]** with the source to check. Property constants, correlation coefficients, code limits, and regulatory thresholds change with version and jurisdiction; confirm them against current official standards or documentation before use.

### Failure handling

- **Balance does not close:** Locate the discrepancy by checking one unit at a time; check recycle initialization, hidden streams (purges, vents, leaks), and unit basis (mass vs. molar).
- **Non-convergence in recycle:** Check the tear stream choice, damping factor, and whether the process has multiple steady states.
- **Model disagreement:** Report both results and the range. Do not average them silently.
- **Missing data:** Stop and list the specific missing items. Do not fill them with plausible values.

### Deliverable contract

Every deliverable contains, in this order:

1. Scope and basis statement with unit system.
2. Assumptions table (ID, assumption, justification, verification status).
3. Flowsheet summary with stream table (T, P, flow, composition).
4. Balance closure results with residuals.
5. Equipment sizing table with method and source for each correlation.
6. Energy integration summary with ΔTmin and utility targets.
7. Risk list from deviation review, with recommended next study (HAZOP, LOPA, control review).
8. Open items and required approvals.

### What not to do

- Do not present screening results as final design or as a safety certification.
- Do not invent property values, kinetic constants, or code requirements.
- Do not use ideal-gas or ideal-solution assumptions at high pressure or for strongly nonideal mixtures without stating the error.
- Do not omit recycle or purge streams from balances.
- Do not change setpoints, interlocks, or specifications without explicit approval.


## engineered-biology-materials

**Use when:** Use when designing, reviewing, or planning work on engineered biology materials (biologically produced or biologically templated materials such as biofabricated composites, living or engineered-cell-based materials, mycelium and protein-based materials, biomineralized structures, and microbially produced polymers), including process feasibility, characterization planning, scale-up risk, and biosafety-aware documentation.

### Purpose and boundaries

This skill supports professionals who turn biological systems into functional materials. In scope: feasibility assessment of a biologically produced or templated material; defining organism or cell-system, feedstock, and growth or fabrication conditions; selecting material characterization methods; planning pilot-to-scale transitions; and writing batch records and evidence packages.

Out of scope: wet-lab protocol execution without a qualified operator and institutional biosafety review; genetic design of organisms intended for release; uses in humans or food-contact applications (route to specialized regulatory review); performance or regulatory compliance claims; and any gene-drive or pathogen-enhancement work, which must be refused.

### Inputs and assumptions

Collect before analysis:
1. Target function and performance envelope (e.g., compressive modulus range, water uptake limit, degradation time, thermal limit, service life).
2. Production route: organism or cell line (identity, source, biosafety level as assigned by the institution), growth or culture medium, fabrication method (solid-state, submerged, scaffold-templated, mineralization, spinning).
3. Feedstock composition and variability, including waste or agricultural inputs.
4. Scale target and facility constraints (containment class, sterilization capacity, curing space).
5. Existing data: prior batches, failure records, instrument calibration status.

State assumptions explicitly. If the organism, its containment level, or the end-use setting is unknown, stop and request it. Do not infer biosafety classification.

### Operating workflow

1. **Define the functional requirement** as measurable properties with acceptance ranges and test conditions. Reject vague goals such as "strong" or "sustainable."
2. **Map the process chain** from inoculum to finished material. Mark each step as biological (growth, metabolism, cell differentiation), physical (curing, drying, pressing), or chemical (crosslinking, mineral deposition).
3. **Identify control variables** for each biological step: temperature, pH, dissolved oxygen, moisture content, time-to-harvest, contamination indicators. Assign a tolerance to each.
4. **Select characterization methods** matched to properties: density and porosity (gravimetric, micro-CT), mechanical behavior (compression or tensile testing under stated humidity), water sorption (gravimetric uptake at fixed relative humidity), microstructure (SEM with sample-prep disclosure), composition (FTIR or elemental analysis where applicable).
5. **Plan the pilot** with a minimum of three independent batches per condition, randomized run order, and retained controls.
6. **Assess scale-up risk**: heat and mass transfer changes, gradient formation in thick parts, contamination exposure, and cycle-time impact on throughput.
7. **Write the evidence package** (see Deliverable contract).

### Decision gates

- **Gate A (Biosafety):** Organism and containment class confirmed by the institutional biosafety committee or equivalent. Proceed only with written approval. Otherwise halt.
- **Gate B (Feasibility):** Proceed to pilot only if the functional requirement can be expressed as at least three measurable properties and the control variables have defined tolerances.
- **Gate C (Reproducibility):** Pilot batches must show coefficient of variation within the pre-registered limit for the primary property (set this limit before testing; a common starting point is ≤15% for bulk mechanical properties, but justify it for the application). Failing batches trigger root-cause review, not parameter tweaking.
- **Gate D (Scale-up):** Proceed to larger batches only if small-batch results hold after one parameter-controlled replicate and the gradient analysis shows no property variation exceeding the acceptance band across the part.
- **Gate E (External action):** Any shipment, public claim, field deployment, or submission requires explicit human approval and a named responsible owner.

### Verification and evidence

- Record every batch with: organism or cell-line identifier and passage number, medium lot, environmental log, feedstock lot, fabrication date, and operator.
- Include negative and positive controls for contamination (sterility check, non-inoculated substrate) in each batch.
- Report mean, standard deviation, sample size, and test standard or method for every property. Do not report a single best specimen.
- Separate measured results from interpretation. Label extrapolations as such.
- Verify any standard numbers, instrument settings, or test-method revisions against current official standards documentation before citing them; do not rely on memory.
- Quote no literature performance figures unless the source is retrieved and checked during the task.

### Failure handling

- **Contamination detected:** quarantine the batch, record the contaminant indicator, do not reuse inoculum, and review sterilization and transfer steps before the next run.
- **Property below range:** check control-variable logs first; compare to tolerance; repeat with one variable changed only if the root cause is identified.
- **High variance:** examine feedstock lot and specimen preparation before the biology. Increase replicates only after the measurement is shown to be stable.
- **Unexpected morphology or growth:** halt production, inspect for organism drift or mixed culture, and escalate to biosafety review if containment could be affected.
- **Missing data:** mark as missing; never backfill or estimate values in the record.

### Deliverable contract

Every output must contain:
1. A one-paragraph scope statement with the functional requirement and boundaries.
2. A process chain table listing step, type (biological, physical, chemical), control variables, and tolerances.
3. A characterization plan listing property, method, standard reference (to be verified), sample size, and acceptance range.
4. Decision gate status (A through E) with the evidence supporting each status.
5. A risk register with at least five entries, each with likelihood, impact, and mitigation.
6. A list of open items, including all version-sensitive details flagged for verification against current official documentation.
7. An explicit approval request section listing any actions needing human authorization.

Do not include unverified performance claims, invented equipment settings, or statements of regulatory compliance.


## gene-information-genomics

**Use when:** Use when retrieving, reconciling, curating, or interpreting gene-level information (identifiers, coordinates, sequences, annotations, orthologs, variants, expression, pathway or compound-target links) across chemistry and biology resources, or when preparing gene-annotation tables for analysis.

### Purpose and boundaries

This skill covers the practical handling of gene-level facts: which gene a name or identifier refers to, where it sits in a specified genome build, which transcripts and proteins it produces, what it is orthologous to, and which compounds, pathways, or variants are linked to it. It produces reconciled, traceable gene annotation tables and short evidence-backed interpretations.

It does not cover wet-lab design, clinical diagnosis, treatment decisions, or de novo genome assembly. Output is research support and must be checked by a qualified domain expert before use in decisions affecting people, animals, or regulated submissions.

### Inputs and assumptions

Before acting, establish and record:

1. **Organism and taxon ID.** Gene symbols are only meaningful within a species. Never assume human.
2. **Genome build or release.** Coordinates are build-specific. Record the assembly name and annotation release for every coordinate.
3. **Identifier type supplied.** Symbol, Entrez-style ID, Ensembl-style gene or transcript ID, UniProt accession, RefSeq accession, HGNC ID, or chemical–target identifier.
4. **Question type.** Identity lookup, coordinate mapping, ortholog mapping, compound–target linkage, variant annotation, or expression context.
5. **Data sensitivity.** Determine whether any input contains human individual-level genotypes, patient identifiers, or unpublished proprietary sequences.

If the organism, build, or identifier type is missing and cannot be inferred from the file headers or the user's context, stop and ask.

### Operating workflow

1. Normalize identifiers. Strip whitespace, fix case according to the nomenclature authority for that species, and flag symbols that are known aliases or previous symbols.
2. Resolve each identifier to a stable primary key (for example, a curated nomenclature ID plus a stable gene ID). Store every raw input alongside its resolved key.
3. Map coordinates only within a single declared build. If a conversion between builds is needed, use the official mapping tool or chain file for that pair, and label the result as converted.
4. Expand to transcripts and proteins by selecting a canonical transcript using a named rule (for example, the database's canonical flag or longest coding isoform), and report the rule used.
5. For orthology, record the method and source (curated versus inferred). Report one-to-many relationships rather than forcing one-to-one.
6. For chemistry links, record the compound identifier, the interaction type (inhibitor, agonist, substrate, binder, unknown), the assay or evidence class, and the source. Keep "binds" distinct from "modulates activity."
7. Write the table, a provenance log (source, retrieval date, release version), and a list of unresolved records.

### Decision gates

- **Build mismatch:** if inputs mix builds, stop and reconcile before any coordinate-based analysis.
- **Ambiguous symbol:** if a symbol maps to more than one gene, do not pick one silently. Keep all candidates and request confirmation.
- **Sensitive data:** do not send individual-level human genotype data, patient identifiers, or unpublished sequences to any external web service or API without explicit user approval and a confirmed data-use basis.
- **Overwrite or delete:** do not overwrite existing curated annotation files, merge into shared databases, or delete records without explicit approval. Write to new versioned outputs.
- **External-impacting actions:** submitting data to public repositories, emailing collaborators, or publishing annotations requires explicit approval.
- **Clinical or regulatory use:** if the output is intended for diagnosis, dosing, or a regulatory filing, stop and state that expert and validated-pipeline review is required.

### Verification and evidence

- Round-trip check: resolved IDs must map back to the original symbol or accession in the same organism. Target 100% for unambiguous inputs; report every exception.
- Coordinate sanity check: start is less than or equal to end, chromosome name matches the build's naming convention, and gene length is consistent with the annotation.
- Count reconciliation: rows in equals rows out, plus a documented list of dropped or flagged records.
- Evidence tagging: every assertion carries one of: curated, computed-from-release, inferred, or user-supplied.
- Version-sensitive details (release numbers, API endpoints, tool flags, database schema fields) must be checked against current official documentation before being stated as fact. Mark any unverified detail as such.
- Do not report performance figures or database coverage statistics unless they were measured in the current session.

### Failure handling

- If a resource is unreachable, report the failure, the query attempted, and the time. Do not substitute memory for live data without labeling it as unverified.
- If a symbol is withdrawn or renamed, report the current symbol and the previous one, and keep both.
- If canonical transcript rules conflict between sources, report both and do not average or merge them.
- If results contradict across sources, present the disagreement with each source's evidence class; do not resolve it by choosing the more convenient answer.

### Deliverable contract

Return:

1. Summary: organism, build, identifier type, record counts (resolved, ambiguous, unresolved).
2. Annotation table with raw input, resolved primary key, symbol, coordinates (with build), canonical transcript and rule, ortholog or compound links with evidence class.
3. Provenance log: sources, release versions, retrieval dates, mapping tools used.
4. Open items: ambiguous records, required approvals, and claims that need expert verification.

Do not present unverified specifics as settled. Do not generate identifiers, coordinates, or interaction claims that were not retrieved or supplied.


## inorganic-polymer-materials

**Use when:** Use when planning, interpreting, or reviewing work on inorganic polymers such as polyphosphazenes, polysiloxane backbones, polysilanes, polyphosphates, sulfur-based polymers, geopolymers, alkali-activated binders, and silicate or phosphate glasses, including synthesis routes, structure-property analysis, and biological-interface claims.

### Purpose and boundaries

This skill guides technical work on polymers whose backbone contains no continuous carbon-carbon chain: main-group chains (Si, P, S, Ge, Sn), mineral networks (aluminosilicate, phosphate), and biological inorganic polyphosphates. It covers:

- Route selection, stoichiometry, and reaction-condition reasoning
- Characterization planning and data interpretation (molecular weight, thermal, spectroscopic, structural)
- Property claims for thermal, mechanical, hydrolytic, and biological behavior
- Reporting that separates measured results from inference

It does not cover organic-backbone polymers with inorganic side groups unless the backbone chemistry is the question, nor clinical, regulatory, or occupational-safety certification. Treat hazardous reagents (chlorosilanes, phosphorus halides, polysulfides, alkali hydroxides at high concentration, elemental sulfur at high temperature) as requiring approved protocols.

### Inputs and assumptions

Collect before analysis:

1. Target backbone and end groups, with intended molecular weight or degree of polymerization.
2. Available precursors, purity grades, and moisture or oxygen sensitivity.
3. Intended use: structural, thermal, dielectric, matrix, biomaterial, or research standard.
4. Existing data: spectra, chromatograms, thermograms, mechanical curves, with instrument and calibration details.

State every assumption explicitly. If purity, water content, or calibration is unknown, label conclusions as provisional.

### Operating workflow

1. Define the target property and the failure mode you must avoid (e.g., hydrolysis of P-N or Si-O-Si bonds, chain scission, phase separation).
2. Choose the route. Ring-opening polymerization suits phosphazenes and siloxanes when cyclic monomers are accessible; polycondensation suits silicates and phosphates; alkali activation suits aluminosilicate binders. Justify the choice against moisture tolerance and byproduct removal.
3. Calculate stoichiometry from measured precursor purity, not nominal labels. Record the water and residual-solvent budget.
4. Specify a characterization set before synthesis: NMR of relevant nuclei (²⁹Si, ³¹P, ²⁷Al where applicable), FTIR or Raman for bond identity, SEC or GPC for molar mass with a stated calibration standard, TGA/DSC for decomposition and transitions, XRD for crystallinity.
5. Execute in controlled conditions, logging atmosphere, temperature, and time.
6. Compare results to the target against pre-stated acceptance criteria.
7. Document provenance of every number.

### Decision gates

- **Gate A (route):** Proceed only if the chosen route avoids reagents that produce uncontrolled byproducts (e.g., HCl or HF release) without an approved ventilation and neutralization plan.
- **Gate B (molar mass):** Molar mass from SEC on a polymer with a different chemistry than the calibration standard is relative, not absolute. Report it as relative unless an absolute method (light scattering, end-group NMR) confirms it.
- **Gate C (hydrolytic stability):** Any claim of stability in water, body fluid, or humid environments requires time-series data under stated conditions. Without it, claim only the measured condition.
- **Gate D (biological interface):** Claims of biocompatibility, degradation products, or ion release need cytotoxicity or release data from a qualified laboratory. Do not extrapolate from polyphosphate chemistry alone.
- **Gate E (scale-up):** Move beyond gram scale only after reproducibility over at least three independent runs with spread reported.

### Verification and evidence

- Confirm backbone identity with at least two orthogonal techniques.
- Check mass balance and integration ratios in NMR against expected repeat-unit composition; a deviation above the stated tolerance triggers re-analysis.
- Report SEC dispersity (Đ) with the calibration basis.
- Compare TGA residue against the calculated inorganic fraction.
- For geopolymers, report the Si/Al ratio, alkali concentration, curing temperature, and age at test.
- Mark every database value, literature property, or instrument specification as requiring verification against current official documentation or the original source when versions, calibrations, or standards may have changed.

### Failure handling

- **Unexpected hydrolysis or gelation:** Stop, check moisture and solvent water content, and repeat with dried reagents before changing the route.
- **Broad or bimodal SEC trace:** Test for oligomers, cyclics, or crosslinking before reporting an average molar mass.
- **NMR shifts disagree with literature:** Verify referencing and solvent; do not reassign peaks without a second method.
- **Inconsistent mechanical data:** Check specimen geometry, aging, and humidity history before attributing differences to chemistry.

Do not average results across incompatible conditions.

### Deliverable contract

Every deliverable must contain:

1. Target, route, and key assumptions.
2. A table of measured values with method, conditions, and replicate count.
3. Explicit separation of measured results, calculated values, and literature-based statements.
4. Pass/fail status against each acceptance criterion.
5. Items requiring approval (hazardous procedures, external sharing, biological or clinical claims, scale-up).
6. A list of values flagged for verification against current official documentation.

Do not state compliance, safety certification, or regulatory suitability. Do not invent instrument settings, reference values, or benchmark results.


## materials-science-engineering

**Use when:** Use when selecting, specifying, or qualifying engineering materials, interpreting material test data, diagnosing material-related failures, or reviewing heat treatment, joining, or corrosion-protection decisions for metals, polymers, ceramics, and composites.

### Purpose and boundaries

This skill supports engineering judgment on material selection, property interpretation, process-structure-property reasoning, and failure analysis for structural, thermal, and environmental service. It covers metals (steels, aluminum, titanium, nickel alloys), polymers, ceramics, glasses, and fiber-reinforced composites.

It does not replace a licensed engineer's sign-off, a certified materials laboratory, or applicable code compliance (for example pressure vessel, aerospace, medical, or nuclear codes). It does not certify that any material meets a standard. Outputs are recommendations requiring qualification by the responsible engineer.

### Inputs and assumptions

Before recommending anything, establish:

1. Service envelope: load type (static, cyclic, impact), temperature range, environment (chemistry, humidity, UV, radiation), design life.
2. Geometry and manufacturing route: section thickness, welding, machining, forming, additive, casting.
3. Governing requirements: specification, code, customer drawing, or regulatory class.
4. Available data: certified mill test reports, supplier datasheets (note the test condition and orientation), prior test results, failure photographs, fractography.
5. Constraints: cost ceiling, lead time, recyclability, supply chain restrictions.

Record any missing input as an explicit assumption. Do not fill gaps with typical values presented as guaranteed.

### Operating workflow

1. Define the function in measurable terms: required yield strength, fatigue life at stress amplitude, maximum service temperature, allowable corrosion rate.
2. Shortlist two to four candidate material families using service envelope limits. Eliminate any candidate that fails a hard constraint before comparing soft ones.
3. Map processing to structure: identify heat treatment state, grain size, phase content, residual stress, and surface condition that the supplier must control.
4. Compare candidates on a weighted table covering strength at temperature, toughness at minimum service temperature, corrosion or oxidation resistance, fabricability, and cost per functional unit.
5. For welded or joined parts, evaluate heat-affected zone properties and filler compatibility, not parent metal alone.
6. Specify verification tests matched to the failure mode (see Verification).
7. Write the recommendation with stated assumptions and open risks.

### Decision gates

- Gate A (temperature): if service temperature exceeds about 0.4 times the absolute melting temperature for a metal, evaluate creep explicitly. Do not rely on room-temperature yield data.
- Gate B (brittleness): for ferritic steels, aluminum alloys in cryogenic service, or polymers near glass transition, require notched toughness data at the minimum service temperature before approval.
- Gate C (fatigue): if the part sees cyclic loading, require fatigue data at the relevant stress ratio and surface finish, and check notch sensitivity at all geometric discontinuities.
- Gate D (corrosion): if chloride, sulfide, or acidic exposure is present, require a documented corrosion test or service history from comparable conditions. Galvanic couples require an explicit mismatch assessment.
- Gate E (composites): do not approve laminate designs without void content, fiber volume fraction, and moisture conditioning data.
- Gate F (novel or unqualified material): stop and escalate to a qualified materials engineer if no existing standard or service history supports the choice.

### Verification and evidence

- Traceability: every property value must cite its source document, test standard, specimen orientation, and test temperature. Unsourced values are not evidence.
- Heat lot match: confirm mill certificates match the heat and heat treatment lot used in production.
- Acceptance tests: tensile, hardness, impact, and microstructure checks sized to the specification. Hardness-to-strength conversions are approximate and must be labeled as such.
- Failure analysis: preserve the fracture surface. Document macro photos, fracture origin, beach marks or striations where present, and chemical composition at the origin. Do not clean or section the fracture before documentation.
- Quantitative quality checks: grain size within specified ASTM or equivalent range, weld hardness below the specified maximum, porosity or void fraction within the specified limit.

Version-sensitive items (standard revision letters, current alloy designations, code edition years, supplier property sheets) must be verified against current official documentation before use.

### Failure handling

- If test data conflict with supplier values, do not average them. Investigate specimen orientation, heat treatment, and test rate first.
- If a failure origin is unidentified, state the leading hypotheses and the discriminating test for each. Do not assert a root cause without fractographic or chemical evidence.
- If a required property is unavailable, mark the recommendation conditional and list the test that would close the gap.
- If a requested approval would cross a decision gate without evidence, decline the approval and state which evidence is missing.

### Deliverable contract

Produce a single report with these sections:

1. Summary recommendation (one paragraph, with conditions).
2. Service envelope and assumptions (table).
3. Candidate comparison (weighted table with sources cited).
4. Gate results (pass, fail, or escalate for each applicable gate).
5. Verification plan (tests, acceptance criteria, responsible party).
6. Open risks and required approvals.

Do not state that a material is "certified," "compliant," or "guaranteed" unless a named document demonstrates it. Do not present unverified numeric values as design allowables. Actions that destroy or alter evidence (sectioning fractures, scrapping lots, changing specifications, sending specifications to suppliers or customers) require explicit written approval from the responsible engineer before execution.


## metabolic-cell-biochemistry

**Use when:** Use when analyzing, designing, or interpreting cell metabolism work, including pathway mapping, flux and stoichiometry reasoning, enzyme kinetics, metabolite measurements, isotope tracing, and metabolic experiment or model review.

### Purpose and boundaries

This skill supports professional work on cellular metabolism: reconstructing pathways, checking stoichiometry and thermodynamic feasibility, interpreting enzyme kinetics, designing and reviewing metabolomics and isotope-tracing experiments, and judging whether metabolic data support a stated conclusion.

In scope: central carbon metabolism (glycolysis, TCA cycle, pentose phosphate pathway, oxidative phosphorylation), amino acid and lipid metabolism, cofactor balance (NAD(P)H, ATP, acetyl-CoA, one-carbon units), compartmentalization, and genome-scale or kinetic model sanity checks.

Out of scope: clinical treatment decisions, dosing, wet-lab protocols that could cause harm without a supervising qualified scientist, and claims about human patients drawn from cell-line data alone.

### Inputs and assumptions

Request the following before drawing conclusions:
- Organism or cell system, medium composition (glucose, glutamine, serum, oxygen tension), and growth phase.
- Measurement type: absolute or relative metabolite levels, extracellular exchange rates, isotope labeling pattern and tracer identity, enzyme activity assays.
- Units, normalization basis (cell number, protein, volume, DNA), and replicate count.
- Model source and version if a stoichiometric or kinetic model is used.

State assumptions explicitly. Default assumptions to flag: metabolic steady state unless shown otherwise; intracellular metabolite pools are well mixed within a compartment; isotopic steady state only if labeling plateau was measured.

### Operating workflow

1. Define the question as a testable claim (for example, "knockdown of enzyme X redirects carbon from glycolysis to serine synthesis").
2. Draw the relevant network: list reactions, substrates, products, cofactors, compartments, and reversibility.
3. Check mass balance per reaction (atoms C, N, H, O, P, and charge where applicable). Reject any reaction that does not balance without an explicit transporter or exchange term.
4. Check thermodynamic direction using reported standard free energies and plausible metabolite concentration ranges. Mark reactions whose direction depends on unmeasured concentrations.
5. For kinetics, compare the observed rate with Km and Vmax ranges from the same organism and conditions where available; flag extrapolations.
6. For tracing, map each labeled fragment to atom transitions and predict mass isotopologue distributions before comparing with data.
7. Compare prediction against observation and enumerate alternative explanations (compartment exchange, salvage pathways, medium contribution, dilution by unlabeled pools).
8. Write the conclusion with its evidence grade and remaining uncertainty.

### Decision gates

- **Gate A, data sufficiency:** Proceed to flux or pathway conclusions only if at least three biological replicates exist, normalization is stated, and a blank or extraction control is reported. Otherwise report as exploratory.
- **Gate B, steady state:** If labeling or concentrations were measured at a single time point, do not claim steady-state flux. Request a time course or label the claim as a snapshot.
- **Gate C, compartment ambiguity:** If a metabolite is measured as whole-cell but the claim concerns a specific organelle, downgrade the claim unless fractionation data support it.
- **Gate D, model conclusions:** A model prediction may be reported as a hypothesis only. Require experimental or independent-data support before calling it a finding.
- **Gate E, external or consequential action:** Any step that orders reagents, modifies a shared dataset or model repository, submits to an external party, or generates protocols for live animal or human work requires explicit user approval and confirmation of the responsible investigator.

### Verification and evidence

Quality checks to report with every conclusion:
- Atom mapping balances for every reaction used (100% of reactions in the argument).
- Isotopologue predictions sum to 1 (within rounding) and natural abundance correction is documented.
- Replicate coefficient of variation for key metabolites is reported; values above roughly 30% are flagged as limiting.
- Internal standard recovery is stated; recoveries outside a laboratory-defined acceptance window are flagged.
- Alternative explanations are listed with at least one discriminating measurement for each.

Evidence grades: **Established** (direct measurement under matching conditions, replicated), **Supported** (indirect or single-condition evidence), **Hypothetical** (model or literature extrapolation).

Software, database, and tool versions are version-sensitive. Do not state specific API names, command flags, or package versions from memory; instruct the user to verify against current official documentation before use.

### Failure handling

- If mass balance fails, identify the missing cofactor, transporter, or water/CO2 term, and report the reaction as unresolved rather than forcing balance.
- If predicted and observed labeling disagree, test in order: incomplete isotopic steady state, unlabeled medium sources, compartment exchange, incorrect atom mapping, then measurement error.
- If kinetic parameters conflict across sources, report the range and do not average without disclosure.
- If the user requests a conclusion the data cannot support, state the strongest supported statement instead and name what measurement would close the gap.

### Deliverable contract

Produce a structured report containing:
1. Claim tested, stated as one sentence.
2. Network table: reaction, atoms balanced (yes/no), direction confidence, source.
3. Evidence table: observation, grade, conditions, replicate count.
4. Alternatives and discriminating experiments.
5. Verification checklist results with any failed items.
6. Open uncertainties and version-sensitive items needing confirmation.

Do not: report flux values without stated tracer and steady-state justification; present model output as measurement; extrapolate cell-line results to organisms or patients without a stated bridge; invent literature citations or database identifiers; omit negative or failed controls from the report.


## organic-medicinal-green-synthesis

**Use when:** Use when evaluating, designing, or documenting greener synthetic routes to medicinal organic compounds, including solvent substitution, catalytic step selection, atom economy and mass-intensity assessment, and waste reduction, for research or process-development work.

### Purpose and boundaries

This skill supports chemists and biologists comparing or redesigning synthetic routes to drug-like organic molecules so that they use less hazardous reagents and solvents, fewer steps, less waste, and lower energy input, without losing yield, purity, or reproducibility.

In scope: route benchmarking, solvent and reagent substitution, catalysis selection, step-count and protecting-group reduction, mass-intensity and atom-economy calculations, workup simplification, and green-metric reporting.

Out of scope: any route to controlled substances, chemical warfare agents, toxins, explosives, or compounds with evident misuse potential. Decline these regardless of framing. Also out of scope: clinical dosing, regulatory filing claims, and biological efficacy predictions.

### Inputs and assumptions

Collect before analysis:
- Target structure (SMILES or drawn structure), intended use stage (discovery, scale-up, GMP-adjacent), and target scale.
- Current route: every step, reagent, solvent, catalyst, temperature, time, workup, and isolated yield.
- Constraints: available equipment, purity specification, cost ceiling, and regulatory or internal solvent lists.

State assumptions explicitly. If yields, scales, or hazard data are missing, label the affected conclusions as provisional.

### Operating workflow

1. Baseline the current route. Compute overall yield, step count, and per-step mass intensity (total mass of inputs divided by mass of product). Record the largest contributors by mass.
2. Flag hazards. For each solvent and reagent, note the category from the organization's hazard list or current safety data sheet. Mark chlorinated solvents, dipolar aprotics, heavy-metal catalysts, and pyrophoric or water-reactive reagents for review.
3. Identify replacement candidates in order of preference: remove the step, replace the solvent (for example, toward alcohols, esters, or water-compatible systems where chemistry permits), switch to catalytic rather than stoichiometric reagents, or use a telescoped sequence that avoids isolating intermediates.
4. Assess protecting groups. Each protection/deprotection pair adds two steps and mass. Test whether a chemoselective reaction removes the need.
5. Evaluate energy and processing: prefer reactions that run near ambient temperature, avoid cryogenic steps where practical, and minimize chromatography by designing crystallization or extraction-based purification.
6. Run a small-scale comparison (typically 0.5 to 2 mmol for screening, with replicates) of the baseline and the proposed route at identical concentrations.
7. Recalculate metrics and record the result alongside purity and impurity profile.

### Decision gates

- **Gate A (proceed to screening):** Proposed change removes at least one hazardous reagent or solvent, or reduces mass intensity by at least 20% in a defined step, with no known safety regression.
- **Gate B (proceed to scale-up):** Screening yield within 5 percentage points of baseline, impurity profile equal or better by the analytical method used, and reproducible across at least three runs.
- **Gate C (stop and escalate):** Any new energetic intermediate, gas evolution not previously controlled, exotherm not characterized by calorimetry, or any step touching a regulated substance. Require explicit approval from the responsible safety and compliance owner before continuing.

Require explicit human approval before: running any reaction above the approved scale, disposing of waste streams in a way that differs from existing procedure, sharing routes outside the team, or submitting data externally.

### Verification and evidence

- Confirm product identity by at least two orthogonal methods (for example NMR and HRMS, or NMR and HPLC retention against a reference).
- Report purity by a validated method and state the method version and detection limits.
- Calculate: overall yield, process mass intensity, atom economy per step (stoichiometric basis), and solvent intensity (solvent mass per gram product). Show calculation inputs.
- Do not quote green-metric improvements as absolute values without the baseline and the calculation basis.
- Verify any safety or hazard classification against current official documentation, since classifications change between revisions.

### Failure handling

- Yield drop greater than 5 points or new impurity above the reporting threshold: revert to baseline conditions, then change one variable at a time (solvent, then catalyst loading, then temperature).
- Unexpected exotherm, gas, or color change suggesting decomposition: stop, quench per existing procedure, and report as a safety event. Do not scale.
- Conflicting literature or vendor data: record both, run a discriminating experiment, and do not average them.
- If a greener solvent fails only at scale, document the mixing, solubility, and heat-transfer differences rather than assuming the screen was representative.

### Deliverable contract

Produce a route comparison report containing:
1. Target, scale, and stated assumptions.
2. Table of baseline and proposed steps with reagents, solvents, temperatures, times, and isolated yields.
3. Metrics table: overall yield, PMI, atom economy, solvent intensity, step count.
4. Hazard changes, listed per substance, with the source and revision date of each classification.
5. Gate decisions (A, B, C) with the evidence behind each.
6. Open items, each with an owner and the approval required.

Do not present unverified claims, invented benchmark numbers, or compliance statements as established facts.


## organism-host-systems

**Use when:** Use when selecting, comparing, or operating a biological host organism or cell system (bacterial, yeast, fungal, insect, plant, or mammalian cell) for recombinant expression, biotransformation, or culture-based chemical production, and when troubleshooting host performance.

### Purpose and boundaries

This skill covers the practical choice and management of a living host system used to produce a protein, metabolite, or chemical transformation. It spans host selection, construct compatibility, culture operation, expression measurement, contamination control, and host-specific troubleshooting.

It does not cover: clinical or diagnostic use, in vivo animal work, enhancement of pathogen traits, field or environmental release, or regulatory submissions. Route those to the appropriate institutional committee or specialist.

### Inputs and assumptions

Before proceeding, collect:

1. Target product, its required form (soluble, secreted, membrane-bound, glycosylated, cofactor-dependent), and minimum yield or titer.
2. Biosafety class of the proposed host and any inserted sequences. Confirm the institutional biosafety approval covers this host and construct.
3. Available genetic tools and their current status (plasmid systems, markers, inducible promoters). Note that tool availability changes; verify against current official vendor and lab documentation.
4. Facility constraints: incubation, bioreactor scale, containment level, and waste handling.
5. Prior data: growth curves, failed runs, sequence files, and strain provenance.

Assume nothing about strain identity or purity until verified.

### Operating workflow

1. **Define the product requirement.** Write the target as a measurable specification (e.g., mg per liter of purified, active protein; conversion percentage at a given time).
2. **Shortlist hosts.** Compare at least two candidates against: post-translational needs, secretion capacity, codon and cofactor compatibility, growth rate, and known toxicity of the product to the host.
3. **Verify the construct.** Sequence-confirm the full expression cassette, including promoter, tags, and selection marker. Check for internal restriction or reading-frame errors.
4. **Establish a small-scale pilot.** Use a minimum of three biological replicates in parallel with a positive and empty-vector control. Sample at fixed intervals for OD or cell density, product readout, and viability.
5. **Optimize one variable at a time** or use a designed factorial screen. Typical variables: inducer concentration, induction temperature and timing, medium composition, and feeding strategy.
6. **Scale only after reproducibility.** Move up one scale step at a time, rechecking product quality at each step.
7. **Document lineage.** Record strain ID, passage number, glycerol stock location, and every culture parameter.

### Decision gates

- **Gate A (host choice):** Proceed with a host only if it meets the product's folding and modification requirements, or a documented engineering path exists.
- **Gate B (construct):** Do not induce a culture until sequence identity is confirmed and the stock is shown to be free of contamination by streak purity or equivalent.
- **Gate C (scale-up):** Advance only if pilot results show replicate coefficient of variation below 20% for the primary readout, and product identity is confirmed.
- **Gate D (containment change):** Stop and seek approval before changing host class, adding a new resistance marker, altering containment level, or introducing sequences from a higher-risk organism.

### Verification and evidence

- Product identity: intact mass or equivalent identity check, plus activity or conversion assay against a reference standard.
- Purity: a separation method appropriate to the product, reported with lane or trace images or raw values.
- Host health: growth curve, viability fraction, and absence of unexpected morphology under microscopy.
- Contamination: plating on non-selective and selective media, and a periodic check of a no-inoculum control.
- Reproducibility: report mean and spread across at least three independent cultures. Never report a single best run as the result.

### Failure handling

- **No expression:** Check the construct sequence, then inducer activity, then host toxicity by comparing growth with and without induction. Do not raise inducer concentration above the manufacturer's stated range without a dose series.
- **Insoluble product:** Test lower temperature, a solubility tag, and co-expression of chaperones in one comparative set. Record each change.
- **Growth collapse after induction:** Reduce expression strength or induction duration before changing host.
- **Unexpected band or mass:** Suspect proteolysis, truncation, or plasmid loss; confirm with a second method before revising the hypothesis.
- **Contamination:** Discard the affected culture and its shared reagents. Re-streak from the last verified stock. Do not reuse working stocks from a contaminated run.

### Deliverable contract

Each report must include:

1. Product specification and host rationale, with the decision gate outcomes stated.
2. Construct verification record with sequence identity evidence.
3. Growth and product data tables, with replicate counts, units, and variance.
4. Raw data file locations and any deviations from the protocol.
5. Open risks and the next gated step.

Do not state yields, activities, or optimal conditions that were not measured in this work. Do not describe a host as "safe" or "compliant"; state only the containment level and approval status on record.

