# Engineering and Robotics

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

## aerospace-vehicle-engineering

**Use when:** Use when analyzing, sizing, reviewing, or documenting aircraft, spacecraft, launch vehicle, or UAV design work, including mass and performance budgets, structural and thermal margins, flight-control and propulsion integration, and certification-oriented evidence packages.

### Purpose and boundaries

This skill guides engineering analysis and review of whole-vehicle or subsystem-level aerospace design: requirements allocation, mass properties, performance and sizing, loads and structural margins, thermal and environmental budgets, propulsion and flight-control interfaces, and verification planning. It produces traceable engineering assessments, not flight clearances.

In scope: preliminary and detailed design reviews, trade studies, margin audits, interface checks, and test-plan critique for fixed-wing, rotary-wing, UAV, launch, and orbital vehicles.

Out of scope: issuing airworthiness approvals, signing off flight readiness, certifying compliance with any regulation, or replacing a licensed authority's findings. Output is advisory until a qualified engineer of record accepts it.

### Inputs and assumptions

Before analysis, confirm:

1. Vehicle class, mission profile, and operating envelope (altitude, Mach or velocity, load factor, temperature, duration).
2. Governing requirements document and revision. Record the revision letter.
3. Baseline mass statement with CG and inertia, and its date and owner.
4. Geometry, material properties with source and allowables basis (design, A-basis, B-basis, or unspecified).
5. Propulsion data: thrust, Isp or specific fuel consumption, throttle range, and propellant or fuel density.
6. Aerodynamic and thermal data sources and the test or analysis they came from.

Mark every missing input as an explicit assumption with a sensitivity note. Never fill a gap silently. Do not assume standard-day atmosphere, material allowables, or regulation applicability without stating them.

### Operating workflow

1. **Frame the question.** Write one sentence: what decision does this analysis support?
2. **Allocate requirements.** Map each vehicle-level requirement to a subsystem owner and a verification method (analysis, test, inspection, demonstration).
3. **Build the mass budget.** Sum component masses with uncertainty and growth allowance. Track margin as a percentage of the allowable gross mass or the controlling limit.
4. **Check performance.** Compute range, endurance, climb, or delta-v with the stated model. Show the equation used and the input units.
5. **Assess loads and margins.** For each critical structure, compute limit and ultimate loads from the flight envelope, apply the factor convention from the requirements, and report margin of safety.
6. **Review thermal and environmental budgets.** Confirm heat-flux, temperature, vibration, and pressure envelopes against component ratings.
7. **Verify interfaces.** Check mechanical, electrical, data, and fluid interfaces with matching revisions on both sides.
8. **Summarize and flag.** Produce the deliverable contract below.

### Decision gates

Stop and escalate to the engineer of record if any of these hold:

- Mass margin falls below the program threshold, or no threshold is defined.
- Any structural margin of safety is negative or depends on an allowable of unknown basis.
- Propulsion or flight-control characteristics rely on an unverified model outside its validated range.
- A requirement conflicts with another requirement or with physics (for example, a range target incompatible with the stated fuel fraction).
- Results depend on an assumption that changes a go/no-go conclusion.

Proceed only when each gate is passed or the open item is recorded with an owner and due date.

### Verification and evidence

- Re-derive one independent value per major result (hand estimate or order-of-magnitude check). Disagreement beyond the stated tolerance blocks release of the result.
- Confirm units and frames of reference at every interface. Unit mismatch is the most common fatal error.
- Check that margins use the correct load factor convention (limit versus ultimate).
- Trace every number to a source document, test report, or analysis file with revision.
- Quality checks: all requirements have an owner and method; mass budget sums to within 0.1% of its components; every assumption has a sensitivity note; no result lacks a source.

### Failure handling

- If data is missing, report the gap and the bounding estimate, not a point answer.
- If two sources disagree, identify which is newer and better-characterized, present both, and escalate.
- If a calculation fails a sanity check, stop, identify the input error, and rerun before reporting.
- Mark any version-sensitive tool behavior, software API, or standard clause as requiring verification against current official documentation.

### Deliverable contract

Every output contains:

1. Question addressed and scope.
2. Inputs with revisions, plus explicit assumptions and their sensitivity.
3. Results with equations, units, and margins.
4. Traceability table linking each result to source.
5. Open items with owner, severity, and gate status.
6. Recommendation: proceed, proceed with conditions, or hold.
7. Statement that the result is advisory and requires review by the engineer of record.

### Explicit approvals and what not to do

Require explicit human approval before: releasing results into a configuration baseline, changing a controlled requirement or interface document, sharing outputs with external parties or regulators, or taking any action that alters flight hardware or software.

Do not: invent material allowables, regulatory citations, benchmark figures, or software function names; state that a design is compliant or airworthy; drop a failed check to meet a schedule; round margins upward; or present a single-point answer when the inputs support only a range.


## electrical-electronics-biomedical-systems

**Use when:** Use when designing, reviewing, or troubleshooting electrical, electronics, or biomedical systems, including analog front ends for physiological sensing, power and isolation for patient-connected devices, signal integrity in embedded hardware, and test or verification plans for medical-grade electronics.

### Purpose and boundaries

This skill guides engineering analysis of electrical and electronic circuits, power systems, signal chains, and embedded hardware, with emphasis on biomedical applications: biopotential acquisition (ECG, EMG, EEG), bioimpedance, pulse oximetry, infusion and monitoring electronics, and wearable sensing.

In scope: circuit analysis and sizing, sensor front-end design, noise and interference budgets, patient isolation and leakage concepts, power-supply and battery architecture, grounding and layout review, test-plan design, and failure diagnosis on bench hardware.

Out of scope: certifying a device to a regulatory standard, claiming compliance with any IEC, ISO, or FDA requirement, clinical efficacy claims, and therapeutic dosing decisions. Where a design touches a patient, state that formal compliance requires a qualified regulatory and safety process.

### Inputs and assumptions

Collect before analyzing:
- Application, signal of interest, bandwidth, amplitude range, and source impedance.
- Supply rails, battery chemistry and capacity, load profile (peak and average current).
- Connection to the patient or external mains, and whether an applied part is floating or earth-referenced.
- Operating environment: temperature, humidity, EMI sources (switching converters, RF, mains).
- Available parts and datasheets; record the exact part number and revision.

Assumptions must be written down with a stated basis. Mark any value taken from memory as unverified.

### Operating workflow

1. Define the signal chain as a block list: sensor, electrode or transducer, protection, amplification, filtering, conversion, processing, isolation, output.
2. Bound each stage: gain, bandwidth, input range, output swing, supply headroom.
3. Compute noise budget: input-referred voltage and current noise, resistor thermal noise (√(4kTRB)), and interference (50/60 Hz, switching harmonics). Compare against the minimum detectable signal.
4. Check DC paths: bias current return, offset drift over temperature, electrode half-cell potentials.
5. Check protection: input clamps, series resistance for limiting fault current, transient suppression on connected lines.
6. Check power: sum worst-case currents per rail, add margin, verify regulator dropout and thermal dissipation, confirm battery end-of-life voltage.
7. Check isolation barrier: creepage, clearance, and the path of leakage current under single-fault conditions. Flag any barrier as "requires standards review."
8. Review layout: return current paths, guard traces, separation of analog and digital grounds, decoupling placement.
9. Produce the test plan (see Verification).

### Decision gates

- **Gate A (signal feasibility):** Proceed only if the noise budget leaves at least 6 dB margin over the minimum detectable signal at worst-case temperature.
- **Gate B (patient connection):** Any path from patient-applied parts to mains or to a non-isolated supply requires explicit human review before proceeding.
- **Gate C (power):** Proceed only if worst-case current per rail is at most 80% of the source rating.
- **Gate D (stability):** Any amplifier with capacitive load or cable drive requires a stability check (phase margin estimate, or measured step response) before release.
- **Gate E (destructive tests):** Fault-injection, overvoltage, or short-circuit tests on real hardware require explicit user approval and a stated safe setup.

### Verification and evidence

Each claim must cite its evidence type: calculation, simulation, datasheet value, or measurement. Simulation is not measurement.

Measurable checks:
- Measured input noise floor versus calculated budget; deviation greater than 3 dB triggers investigation.
- Common-mode rejection measured at the mains frequency and its harmonics.
- Step response overshoot below 10% under the stated load.
- Supply ripple at the load under maximum current, reported in mV peak-to-peak with bandwidth stated.
- Temperature sweep of offset and gain at the operating extremes.

Mark any version-sensitive detail (device errata, tool flags, library calls, standard edition numbers) as "verify against current official documentation" rather than asserting it from memory.

### Failure handling

- Unexpected oscillation: check stability compensation, cable capacitance, and ground loops before changing gain.
- Excess 50/60 Hz pickup: inspect lead length, shield termination, and driven-right-leg or guard networks before adding filters that distort the band of interest.
- Drift or saturation: check electrode polarization and input bias return paths first.
- Brownouts under load: measure the rail under real load; do not infer from the datasheet alone.
- Repeated part failure: stop, record conditions, and escalate for root-cause review before further power-up attempts.

### Deliverable contract

Deliver:
1. Signal chain block diagram with stage parameters.
2. Calculation summary listing equations, inputs, results, and margins against each gate.
3. Assumption register with verification status.
4. Risk list, marking any patient-contact or isolation item for human safety review.
5. Test plan with pass criteria and required equipment described by class (for example, "isolated oscilloscope," not model numbers).
6. Open items list.

Do not: present a design as compliant or safe for patient use; invent part numbers, register values not derived from calculation, or datasheet figures; run destructive tests without approval; or omit the stated basis for any number.


## energy-generation-grid

**Use when:** Use when planning, analyzing, or reviewing grid-connected electricity generation projects (solar, wind, storage, hybrid plants) for interconnection, dispatch, capacity, or grid-impact questions, and when a deliverable must state assumptions, study results, and their limits.

### Purpose and boundaries

This skill guides structured analysis of how distributed and utility-scale generation connects to, and behaves on, an electric grid. It covers:

- Interconnection screening (capacity, voltage class, point of interconnection, protection needs).
- Generation profile and capacity-value estimation for variable and dispatchable resources.
- Grid-impact questions: hosting capacity, voltage rise, thermal loading, reverse power flow, frequency response, and curtailment exposure.
- Hybrid and storage sizing logic at the screening level.
- Review of vendor or consultant studies for completeness and internal consistency.

It does not produce stamped engineering designs, protection settings for energized equipment, regulatory filings, or legal compliance opinions. Those require a licensed professional and the governing utility or regulator. Use this skill to structure, check, and communicate the analysis, not to replace the study.

### Inputs and assumptions

Before analysis, collect and record:

1. Site: coordinates, nominal capacity (MW AC and MW DC for solar), resource data source and period.
2. Interconnection: nearest feeder or substation, voltage level, short-circuit strength at POI if known, existing queue position.
3. Equipment: inverter or turbine type, storage chemistry and power/energy rating, control mode (grid-following, grid-forming, PQ, Volt-VAR capability).
4. Load and network context: minimum and peak load on the feeder, existing generation on it, planned changes.
5. Governing requirements: the utility interconnection standard and applicable grid code. Record the document name, revision, and date. Mark every numeric limit taken from these as **to verify against current published revision**.

Label each assumption as *measured*, *vendor-stated*, or *estimated*. Any assumption without a source is treated as estimated and must be listed in the deliverable.

### Operating workflow

1. **Scope the question.** State the one decision the analysis supports (e.g., "Is 5 MW export viable at feeder F-12 without network upgrades?"). Vague scope produces unusable studies.
2. **Build the generation profile.** Use hourly or sub-hourly data for at least one full year where available. Compute capacity factor, monthly and diurnal profiles, and the coincidence of output with feeder minimum load.
3. **Screen the feeder.** Compare minimum load plus generation export against minimum load, and generation output against feeder thermal rating at the worst coincident hour. Flag reverse power flow conditions explicitly.
4. **Estimate voltage impact.** Use a simplified ΔV ≈ (R·P + X·Q)/V relationship for screening, then replace with a power-flow model for any site passing screening marginally.
5. **Assess protection and fault contribution.** Note whether added inverter-based or rotating fault current changes protection coordination. Escalate to a protection engineer rather than resolving here.
6. **Evaluate storage or hybrid options** only after the base export case is characterized. Model charge source, state-of-charge limits, round-trip efficiency (from vendor data, marked vendor-stated), and degradation assumptions.
7. **Quantify curtailment and value.** Estimate curtailment hours from export limits and congestion; report energy and capacity value separately.
8. **Prepare the grid engineering note** using the output schema below.

### Decision gates

- **Gate A (scope):** Proceed only if the decision question, deadline, and decision owner are named.
- **Gate B (data sufficiency):** Proceed to modeling only with at least one year of resource data and confirmed POI voltage class. If resource data is a single typical-meteorological-year or under 12 months, state that the energy estimate carries wide uncertainty.
- **Gate C (screening result):** If any worst-case hour shows feeder thermal loading above 80% of rating or ΔV exceeding the governing limit, stop screening and recommend a detailed power-flow study. Do not declare the site viable.
- **Gate D (external action):** Any submission to a utility, filing, customer commitment, or equipment purchase requires explicit human approval from the named decision owner. Do not proceed autonomously.

### Verification and evidence

- Reconcile annual energy from the profile against the simple capacity-factor estimate; differences above 10% must be explained.
- Confirm units on every figure (MW vs MWh, AC vs DC, per-unit base).
- Check that exported power never exceeds the approved or requested export limit in the modeled series.
- Verify timezone and daylight-saving handling in time-series joins.
- Spot-check three random hours by hand against the source data.
- Cross-check numeric limits against the current published interconnection standard; record revision and retrieval date.
- Do not state that a site "complies" with any standard. State which screened criteria were passed and which were not evaluated.

### Failure handling

- **Missing or gapped data:** Interpolate only gaps under three hours; flag and exclude longer gaps and report the excluded fraction.
- **Conflicting sources** (e.g., vendor and utility capacity figures): report both, use the more conservative value for screening, and request resolution.
- **Model non-convergence or unexplained results:** Stop, reduce to the simplest case that reproduces the issue, and report the failing condition rather than adjusting inputs to force a pass.
- **Standard not accessible:** Mark all dependent limits as unverified and do not substitute recalled values as fact.

### Deliverable contract

The output must contain, in order:

1. Decision question and conclusion, stated in one paragraph with its confidence level.
2. Input table with source and classification (measured, vendor-stated, estimated) for each value.
3. Method summary and model type, including the simplifications made.
4. Results: energy, capacity value, screening pass/fail per criterion, worst-case hour and its conditions.
5. Assumption register and unverified items, each with an owner and a verification action.
6. Limitations and the recommended next study (e.g., full power-flow, protection review).
7. Approval status: which external actions remain pending human sign-off.

Do not include unsupported compliance claims, invented equipment specifications, or results without a traceable input.


## energy-storage-hydrogen

**Use when:** Use when evaluating, sizing, specifying, or reviewing hydrogen-based energy storage (electrolysis, compression or liquid storage, fuel cell or turbine reconversion) for grid, microgrid, industrial, or renewable-integration projects, including round-trip efficiency, storage duration, and safety-case questions.

### Purpose and boundaries

This skill supports engineering and techno-economic work on power-to-hydrogen-to-power storage chains: electricity to hydrogen by electrolysis, hydrogen storage (compressed gas, liquid, or materials-based), and reconversion (fuel cell, combustion turbine, or engine). It covers sizing, efficiency accounting, cost comparison against batteries and other storage, site-level safety screening, and review of vendor or consultant claims.

Out of scope: detailed electrochemical stack design, pressure-vessel mechanical design, legal certification of installations, and final safety sign-off. Those require licensed engineers and the applicable codes in the jurisdiction. This skill produces analysis and recommendations, not stamped designs.

### Inputs and assumptions

Collect before analysis; record any missing value as an explicit assumption:

- Service requirement: discharge power (MW), energy (MWh), duration, cycles per year, response time, and required availability.
- Electricity supply: source profile (hourly or sub-hourly), curtailment availability, tariffs or price series, and grid connection limits.
- Electrolyzer: technology (PEM, alkaline, SOEC, AEM), nameplate capacity, stated system-level specific energy (kWh/kg H2 at the boundary used by the vendor), turndown ratio, and standby losses.
- Storage: pressure or liquefaction target, vessel or cavern type, hydrogen purity, boil-off or leakage assumptions, site footprint.
- Reconversion: fuel cell or turbine type, electrical efficiency at rated and part load, auxiliaries (compressors, chillers, water treatment).
- Financial: capex and opex basis year, discount rate, asset life, replacement intervals for stacks.
- Site: jurisdiction, hazardous-area classification basis, distance to occupied buildings, ventilation, and ignition sources.

Assume nothing about efficiency boundaries. Always state whether a figure is lower heating value or higher heating value, and whether it includes compression, cooling, and balance-of-plant.

### Operating workflow

1. Define the service in one sentence: what is delivered, to whom, at what power, energy, and duration.
2. Build the energy balance: electricity in, electrolyzer load, compression energy, storage losses, reconversion output. Compute round-trip efficiency at the grid boundary, stating each loss term.
3. Simulate dispatch against the supply profile. Report the number of charge-discharge cycles, seasonal storage carryover, and unserved energy.
4. Size components iteratively: electrolyzer first (absorbs surplus), then storage (covers the longest deficit window plus margin), then reconversion (meets peak power).
5. Compute levelized cost of storage on a stated basis and run sensitivities on electricity price, capacity factor, and stack life.
6. Screen safety: hydrogen flammability range (4–75 % vol in air), low ignition energy, high diffusivity, and embrittlement risk for certain steels. Identify the hazardous-area basis and required separation distances from applicable standards, flagged for verification.
7. Compare against alternatives (lithium-ion for short duration, pumped hydro for bulk, thermal storage) on the same service definition.
8. Write the recommendation with explicit assumptions, ranges, and open items.

### Decision gates

- **Gate A, service fit:** Proceed to hydrogen only if required duration exceeds roughly 8–12 hours or seasonal shifting is needed. For shorter service, batteries usually dominate on round-trip efficiency and cost; document the comparison before proceeding.
- **Gate B, efficiency:** If round-trip electricity-to-electricity efficiency at the grid boundary is below 30 % under realistic assumptions, the project needs a use case beyond storage (heat recovery, hydrogen sales) before proceeding.
- **Gate C, data sufficiency:** Do not produce an LCOS figure without a stated electricity price basis, a defined capacity factor, and stack replacement assumptions.
- **Gate D, safety:** Any site with occupied buildings within the calculated separation distance, or any indoor storage, requires explicit approval from the project's safety authority before design continues.
- **Gate E, external impact:** Any action that submits permit applications, communicates with utilities or regulators, orders equipment, or publishes figures to third parties requires explicit human approval.

### Verification and evidence

- Recompute efficiency independently from the energy balance; reconcile to within 1 percentage point or explain the gap.
- Check that the dispatch simulation conserves energy: stored energy change equals inputs minus outputs minus losses, at every timestep, within numerical tolerance.
- Confirm storage capacity is not exceeded and electrolyzer minimum load and turndown are respected in every simulated hour.
- Cross-check vendor specific-energy figures against thermodynamic minimum (about 33.3 kWh per kg H2 on a HHV basis) and state the gap.
- Cite the version and date of every standard, code, or price series used. Mark any standard edition or regulatory threshold as "verify against current official documentation."
- Do not state that a design "complies with" a code or standard unless a qualified reviewer has confirmed it.

### Failure handling

- If the dispatch shows unserved energy above the stated tolerance, increase the storage or reconversion size and rerun; do not silently reduce the service requirement.
- If sensitivities flip the recommendation, report the flip explicitly with the threshold value.
- If a vendor figure cannot be reconciled with thermodynamics or the stated boundary, reject it and request the boundary definition.
- If safety data is missing, stop at Gate D and list the missing items; do not estimate separation distances by analogy.

### Deliverable contract

Deliver a single report containing:

1. Service definition and boundary statement.
2. Assumptions table with source or "assumed" label for each value.
3. Energy balance and round-trip efficiency with loss breakdown.
4. Sizing results and dispatch summary (cycles, unserved energy, carryover).
5. Cost basis, LCOS, and sensitivity table.
6. Safety screening findings and open verification items.
7. Gate status (pass, fail, or pending) for Gates A through E.
8. Recommendation with stated conditions under which it changes.

Do not: present a single efficiency number without its boundary; use HHV and LHV interchangeably; treat hydrogen as cheaper than batteries without a validated duration argument; or claim regulatory compliance.


## environmental-and-civil-infrastructure

**Use when:** Use when planning, reviewing, or documenting civil infrastructure or environmental engineering work such as stormwater drainage, water and wastewater conveyance, grading and earthworks, erosion and sediment control, site hydrology, pavement and culvert design checks, or environmental impact screening, and an engineer needs structured calculations, criteria checks, or a reviewable deliverable.

### Purpose and boundaries

This skill guides engineering analysis and documentation for civil infrastructure and environmental systems: site hydrology and stormwater, gravity and pressure conveyance, grading and earthworks, erosion and sediment control (ESC), culverts and small drainage structures, pavement load screening, and environmental screening inputs.

It produces calculation packages, criteria checklists, design-review notes, and draft specifications. It does not replace a licensed engineer's stamp, a jurisdiction's permitting process, or a formal environmental assessment. Any output is a draft until a responsible professional checks it against local code, the project's design criteria, and site-specific data.

Out of scope unless the user supplies a qualified professional's direction: structural design of buildings, seismic design, dam safety classification, contaminated-site remediation, and potable water treatment process design.

### Inputs and assumptions

Before calculating, collect and record:

1. Governing standard or design manual and edition (for example, the local stormwater manual or agency standard). Mark the edition as needing verification against current official publication.
2. Design storm: return period, duration, rainfall intensity-duration-frequency (IDF) source, and climate adjustment policy if required.
3. Site data: survey or DEM source and date, soil classes or infiltration tests, groundwater observations, existing utilities, receiving water classification.
4. Land cover and runoff coefficients or curve numbers, with the basis for each value.
5. Constraints: outfall elevation, allowable release rate, minimum cover, slope limits, sediment-control requirements.

If any input is missing, state an explicit assumption, label it, and list it under open items. Never silently fill a value with a typical number.

### Operating workflow

1. **Define the question.** Write one sentence: what is being sized, checked, or screened, and against which criterion.
2. **Establish the catchment.** Delineate drainage areas from survey data. Record area in consistent units, and check that areas sum to the total site.
3. **Select the method.** Choose a method appropriate to catchment size and governing manual (for example, rational method for small urban areas, unit hydrograph or routing for larger or detained systems). Note the method's stated applicability limits.
4. **Compute flows.** Show each intermediate value: intensity, coefficient or curve number, time of concentration with its equation, peak flow.
5. **Size conveyance.** Use Manning's equation or the governing hydraulic method. Check velocity against minimum self-cleansing and maximum erosion limits, and check freeboard.
6. **Check hydraulic grade.** Confirm headwater, tailwater, and outlet control. Verify energy grade line does not exceed rim or ground elevations at design flow.
7. **Screen erosion and sediment.** Compare shear stress or velocity against permissible values for the lining or soil. Confirm ESC measures match disturbed area and slope.
8. **Run criteria checklist.** Compare each result to a stated limit. Record pass, fail, or not applicable.
9. **Write the package.** Follow the deliverable contract below.

### Decision gates

- **Gate A (data sufficiency):** Proceed only if catchment area, design storm, and at least one soil or infiltration basis are sourced. Otherwise stop and request data.
- **Gate B (method validity):** If the catchment exceeds the method's stated limit, or the system has storage, backwater, or tidal influence, switch to a routing method or flag for specialist review.
- **Gate C (criteria failure):** Any failed criterion must either be redesigned and rerun, or escalated with a documented variance request. Do not mark a failed check as passed.
- **Gate D (approval required):** Obtain explicit human approval before any of the following: issuing outputs for permit submission, changing a design basis or design storm, recommending work that alters receiving-water flows or wetlands, specifying demolition or excavation of existing utilities, or any action that sends documents to external parties.

### Verification and evidence

- Recompute at least one result independently, by hand or with a second tool, and record agreement within a stated tolerance (suggested: 2 percent for flow, 1 percent for hydraulic depth).
- Check units on every equation; carry units through the calculation.
- Confirm monotonic sanity: larger storms produce larger peaks; larger pipes produce lower head loss at equal flow.
- Cross-check the catchment area against an independent source such as GIS polygons.
- Keep a source register listing each input, its origin, date, and confidence.
- Equations and default coefficients must be cited to the governing manual by section, with edition. Do not cite from memory.

### Failure handling

- **Inconsistent inputs** (for example, ground lower than outlet invert): stop, list the conflict, request survey correction.
- **Method fails validation:** rerun with the next applicable method and document the change.
- **Result near a limit (within 5 percent):** flag as marginal and recommend sensitivity testing on rainfall intensity, roughness, and coefficient.
- **Unknown standard edition or local rule:** mark as requiring verification against current official documentation; do not assume.

### Deliverable contract

Output a calculation package containing, in order:

1. Scope statement and governing standard with edition (marked for verification).
2. Input table with sources, dates, and assumptions flagged.
3. Catchment and flow calculations with every intermediate step.
4. Hydraulic results with velocities, depths, freeboard, and grade checks.
5. Criteria checklist with pass, fail, or marginal status and limit values.
6. Open items and required approvals.
7. Reviewer sign-off block left blank for the responsible professional.

### What not to do

- Do not present draft calculations as stamped or permit-ready.
- Do not use typical coefficients without a cited basis.
- Do not round intermediate values in ways that change a pass or fail result.
- Do not invent code section numbers, equation constants from memory, or software commands.
- Do not recommend discharge, dewatering, or in-stream work without a gate D approval.


## mechanical-structural-design

**Use when:** Use when sizing, checking, or reviewing mechanical structures, brackets, frames, shafts, fasteners, weldments, or load paths, including stress, deflection, fatigue, and factor-of-safety justification for a design or drawing package.

### Purpose and boundaries

This skill guides structural sizing, load-path checking, and design review for mechanical parts and assemblies: machine frames, brackets, mounts, shafts, bolted joints, welded fabrications, and sheet-metal enclosures. It produces a traceable calculation record that a qualified engineer can check and sign.

In scope: load definition, free-body diagrams, hand calculations and FEA-readiness checks, stress and deflection limits, bolted joint preload checks, weld sizing, fatigue screening, and documentation of assumptions.

Out of scope: certification to a specific code (ASME, EN, AISC, pressure vessel or lifting standards) unless the user supplies the governing edition and the reviewer is qualified; life-safety sign-off; electrical, thermal-only, or control design. This skill does not replace a licensed professional engineer's stamp where one is required.

### Inputs and assumptions

Required inputs before calculating:
- Geometry or dimensioned sketch with units stated.
- Material designation and minimum guaranteed properties (yield, ultimate, modulus), with source.
- Load cases: static, dynamic, impact, thermal, preload, with magnitude, direction, duration, and frequency.
- Boundary conditions: supports, constraints, contact type (pinned, fixed, sliding).
- Service environment: temperature range, corrosion, cycle count target.
- Governing requirements: customer spec, internal standard, or code edition.

If any item is missing, list it as an assumption with a stated value and flag it as open. Never silently assume a material strength or load.

### Operating workflow

1. **Define the load cases.** Enumerate operating, transport, assembly, and misuse conditions. Apply a dynamic factor or shock multiplier only with a stated basis.
2. **Draw the free-body diagram** for each member and joint. Verify static equilibrium (sum of forces and moments equals zero) before computing stresses.
3. **Establish the load path.** Trace every load from application point to ground. Identify where it changes members, and check each transfer (bolt, weld, bearing, friction).
4. **Calculate section properties and stresses.** Use Mohr's circle or equivalent principal stress checks for combined loading. Note stress concentrations (holes, fillets, notches) and apply appropriate factors from a published source.
5. **Check deflection and stiffness** against function limits (alignment, gear mesh, seal gap), not just strength.
6. **Check bolted joints:** preload target, clamp load, separation load, and thread stripping. Confirm embedment and shear-out for threaded and bearing connections.
7. **Check welds:** effective throat, allowable shear, and fatigue category if cyclic.
8. **Screen fatigue** using stress range and an endurance estimate, applying surface, size, and reliability modifiers with sources.
9. **Run FEA only as confirmation.** Document mesh, element type, convergence, and boundary conditions; hand-check at least one critical location.
10. **Compile the record** (see Deliverable contract).

### Decision gates

- **Gate A (inputs complete):** Proceed only when all required inputs are present or explicitly marked as assumptions with owners. Otherwise stop and request data.
- **Gate B (equilibrium):** Reactions must balance within 1% of applied load. Failure returns to step 2.
- **Gate C (margins):** Static factor of safety on yield should be at least 1.5 for controlled loads and 2.0 for uncertain loads, unless the governing standard states otherwise. Fatigue factor should be at least 1.5 on the stress-life or strain-life basis used. Deflection must meet the function limit with margin.
- **Gate D (joint integrity):** Bolt preload must be between 60% and 75% of proof load for reusable joints, unless the fastener manufacturer's data supports otherwise; confirm with current manufacturer documentation.
- **Gate E (review):** A second engineer independently checks the critical path before release.

If any gate fails, do not release. Redesign or escalate.

### Verification and evidence

- Re-derive one stress value independently from a different method.
- Confirm units are consistent across every equation; carry units through calculations.
- Compare FEA peak stress to hand calculation; differences above 15% require explanation (singularities, mesh refinement, boundary assumptions).
- Check mass and center of gravity against the CAD model.
- Verify material properties against the cited datasheet, noting the revision date.
- Mark any value that depends on software version, standard edition, or catalog data as "verify against current official documentation" with the date checked.

### Failure handling

- **Negative margin:** Report the controlling location, load case, and margin. Propose at least two options (section increase, material change, load path change) with mass and cost impact. Do not hide the failure by lowering the load.
- **Unknown material or load:** Use the most conservative credible value and flag it; do not assume favorable properties.
- **FEA and hand calculation disagree:** Investigate boundary conditions first, then mesh, then assumptions. Do not average them.
- **Standard edition unavailable:** State the edition used by the team and request confirmation.

### Deliverable contract

Output a structural design record containing:

1. Scope, revision, and governing requirements.
2. Input table with sources and open assumptions.
3. Load case table and free-body diagrams.
4. Calculation sheets per critical member, joint, and weld, each with units.
5. Margin summary table: location, load case, stress or load, allowable, factor of safety, status.
6. Deflection summary against function limits.
7. Verification log: checks performed, results, reviewer, date.
8. Open issues and required approvals.

Each calculation must be reproducible from the stated inputs. Mark the release status as Draft, Reviewed, or Released, and release only after Gate E passes.

### Approval and safety controls

Obtain explicit human approval before: releasing drawings to manufacturing, issuing a stamped or certified statement, modifying a controlled drawing or revision, changing a load or safety factor to achieve a pass, or sending the record to external parties. Do not state that a design is safe, compliant, or certified; state the margins and checks performed.


## robot-motion-control

**Use when:** Use when designing, tuning, reviewing, or verifying motion control for robotic manipulators, mobile robots, or legged platforms, including trajectory generation, controller selection, motion safety limits, and simulation-to-hardware validation.

### Purpose and boundaries

This skill guides engineers through specifying, implementing, tuning, and verifying motion control for physical robots: joint-space and Cartesian trajectory generation, feedback control (PID, state feedback, impedance/admittance, model-based), velocity and torque limiting, and sim-to-real transfer of controllers.

In scope: kinematic and dynamic motion planning outputs consumed by a controller, low-level servo loops, motion profiles, limit checking, gain tuning procedures, and test plans for real hardware.

Out of scope: high-level task planning, perception pipelines, certification claims (CE, ISO 10218, IEC 61508 conformance is not asserted here; consult the relevant standard and a qualified assessor), and firmware changes to vendor drives beyond documented parameters.

### Inputs and assumptions

Collect before acting. If any item is missing, state the assumption explicitly in the deliverable.

- Robot model: DOF, joint limits (position, velocity, acceleration, jerk, torque), link inertias, gear ratios, encoder resolution, sensor placement.
- Actuator interface: command mode (position, velocity, torque, current), control loop rate, communication latency, and vendor-documented saturation behavior. Mark any driver-specific parameter names as requiring verification against the current vendor manual.
- Task requirements: path tolerance, cycle time, payload range, contact or non-contact operation, workspace obstacles.
- Environment: surrounding humans, fixtures, e-stop topology, safe-speed zones.
- Available tools: simulator, logging rate, measurement equipment (tracking laser, accelerometer, force sensor).

Assumptions to record: rigid-body model validity, friction model, sensor noise characteristics, and timing jitter.

### Operating workflow

1. Define the motion requirement as measurable quantities: max tracking error per axis, max Cartesian path deviation, peak joint velocity, acceleration, and jerk, plus cycle time.
2. Derive hard limits from the actuator and mechanical datasheets, then apply a margin (typically 10 to 20 percent below the lowest rated limit, unless the vendor specifies otherwise).
3. Select the trajectory profile: trapezoidal or S-curve for point-to-point joint moves; time-parameterized splines for Cartesian paths. Check that generated velocity, acceleration, and jerk stay within limits at the sampled rate.
4. Select the control law: start with joint-space PID plus feedforward (inverse dynamics or friction compensation) for position-controlled arms; use impedance or admittance control when contact is expected. Justify the choice in one paragraph.
5. Simulate in a model that includes actuator saturation, backlash or compliance if present, and sample delay. Record tracking error and torque profiles.
6. Tune gains in increasing order of risk: lower gains and reduced speed first, then scale speed in steps of no more than 25 percent per run.
7. Commission on hardware under reduced speed, with the e-stop verified before motion.

### Decision gates

- **Gate A (before hardware motion):** Simulation shows all limits respected with margin; e-stop and software limits verified by a second person; workspace clear.
- **Gate B (before increasing speed):** Tracking error within spec for three consecutive runs; no oscillation in torque or velocity; no thermal rise beyond drive guidance.
- **Gate C (before contact tasks):** Force limits configured and tested with a calibrated load or surrogate; collision detection response measured.
- **Gate D (before release):** Logged evidence reviewed; open issues accepted in writing by the robot owner.

If a gate fails, return to the earliest step that could cause the failure. Do not skip gates to meet a schedule.

### Verification and evidence

Each quality check must have a measured value and a pass threshold:

- Tracking error RMS and peak per joint, compared to the specified tolerance.
- Commanded versus achieved velocity and acceleration; peak jerk after filtering.
- Settling time and overshoot for point-to-point moves.
- Control loop jitter (standard deviation of period) below the threshold in the design requirement.
- Path deviation from the programmed Cartesian path, measured with an external reference where available.
- Torque or current peaks as a percentage of the rated limit, with thermal trend.

Log at least the sampling rate required to resolve the highest expected frequency content (generally 5 to 10 times the closed-loop bandwidth). Store raw logs, configuration hash, and gain values with each run.

### Failure handling

- **Oscillation or instability:** Stop, reduce gains by half, and check for unmodeled delay or filter lag before retuning.
- **Limit violation or fault trip:** Do not clear the fault and rerun. Inspect the log for the triggering sample, identify whether the cause is trajectory, load, or sensor, and correct before retrying.
- **Tracking error grows over time:** Suspect thermal drift, belt stretch, or payload change; measure before adjusting gains.
- **Unexpected contact:** Hold the robot in a safe state, preserve logs, and do not resume until the cause is documented.
- **Sim-to-real mismatch exceeding tolerance:** Re-identify friction and inertia parameters; do not compensate by inflating gains alone.

### Deliverable contract

Produce a motion control report containing:

1. Requirement table with measured targets and limits, including margins and their source.
2. Assumptions list with the owner and verification status of each.
3. Trajectory and controller description, including gains, filter settings, and saturation behavior.
4. Simulation results and the hardware test matrix, with pass/fail per gate.
5. Logged metrics against each quality check, with raw log references.
6. Open risks and the approver's name for any accepted deviation.
7. A list of vendor parameters marked "verify against current official documentation."

Do not state that a system is safe, certified, or compliant on the basis of this process alone. Do not report benchmark numbers that were not measured in the stated setup. Do not run hardware motion, change safety limits, or disable protective functions without explicit written approval from the responsible person; treat such actions as irreversible or external-impacting.


## robot-perception-integration

**Use when:** Use when integrating camera, lidar, radar, depth, or other sensor perception outputs into a robot's software stack, including calibration checks, timestamp alignment, detection-to-tracking handoff, and perception validation before planning or control consumes the data.

### Purpose and boundaries

This skill covers the engineering work of connecting perception modules (object detection, segmentation, depth estimation, localization inputs, occupancy mapping, tracking) to downstream consumers such as planners, controllers, and safety monitors. It applies to mobile robots, manipulators, and autonomous vehicles operating in ROS-based or equivalent middleware.

In scope: sensor-to-frame calibration verification, time synchronization, message contract definition, coordinate transform chains, confidence and uncertainty propagation, latency budgeting, and integration testing against recorded and live data.

Out of scope: training new perception models, selecting hardware procurement, certifying a system for safety standards, and writing planner logic beyond the interface contract.

### Inputs and assumptions

Collect before starting:
- Sensor list with model, mounting pose, intrinsics, and the driver's published frame IDs.
- Current calibration files and their generation date and method.
- Message definitions for each perception output (fields, units, frame, stamp semantics).
- Latency and rate targets for each consumer.
- At least one recorded log (rosbag or equivalent) covering nominal operation and at least one degraded case (occlusion, glare, rain, dropout).
- Ground truth source, if any, and its own error bound.

Assume nothing about timing or frame conventions until measured. Treat any undocumented unit or frame as a defect to resolve, not a default.

### Operating workflow

1. Build a frame graph. List every frame, its parent, and the source of each transform (static URDF, calibration file, dynamic estimator). Flag cycles, duplicate parents, and frames without a publisher.
2. Verify extrinsics. Project a known target (checkerboard or fiducial) through the chain and measure reprojection or point-to-plane error. Record the number and date of samples.
3. Measure timestamp offsets. For each sensor pair, compute the stamp difference distribution on the recorded log. Use the median and 99th percentile, not the mean alone.
4. Define message contracts. For each topic, state frame ID, stamp meaning (capture, processing, or publish time), units, covariance convention, valid ranges, and confidence semantics. Write this as a versioned document in the repository.
5. Implement adapters at the boundary, not inside consumers. Adapters handle frame conversion, interpolation to a common stamp, and rejection of stale or out-of-range messages.
6. Propagate uncertainty. Carry covariance or an explicit confidence score through the handoff. Do not collapse detections to booleans before the consumer needs them.
7. Replay the log through the integrated stack in simulated-time mode and compare outputs to the contract and to ground truth.
8. Run live bench tests at rate, then in the real environment at reduced speed, before any closed-loop authority is granted.

### Decision gates

- Extrinsic gate: proceed only if reprojection error is within the tolerance set by the consumer's accuracy requirement. If no tolerance is stated, stop and request it.
- Timing gate: proceed only if 99th percentile inter-sensor offset is below one third of the consumer's update period. Otherwise add interpolation or fix hardware triggering first.
- Contract gate: no consumer may read a topic that lacks a written contract.
- Degradation gate: the integrated stack must publish a validity flag or drop to a defined safe fallback when inputs go stale beyond the contract timeout.
- Authority gate: closed-loop actuation requires explicit human sign-off from the system owner after passing all prior gates on the target hardware.

### Verification and evidence

Each gate produces a recorded artifact: calibration residual report, timing histogram, contract diff, replay comparison, and bench test log. Store them alongside the code revision and the log identifiers used.

Quantitative checks to report:
- Reprojection RMS error in pixels, per camera, with sample count.
- Stamp offset median and 99th percentile, per sensor pair.
- Detection-to-track association rate on the replay log, compared to a baseline stated in advance.
- Maximum end-to-end latency from capture stamp to consumer receipt.
- Count of messages rejected by adapters, by reason, across the replay.

Do not report a result without the dataset it came from. Do not claim improvement without a same-dataset baseline.

### Failure handling

- Calibration residual exceeds tolerance: recalibrate with more diverse target poses. Do not hand-tune extrinsics to fit the log.
- Timestamps drift over a session: check clock source and driver timestamp mode. Verify against the driver's documentation for the installed version, since timestamp options vary by release.
- Dropped or stale messages: confirm the timeout matches the consumer's update period, then test whether the fallback engages.
- Ghost or duplicated tracks: inspect whether two detectors publish the same object in different frames before changing association thresholds.

Stop and escalate when a failure involves unexplained motion of the robot, a safety monitor disagreement, or a result you cannot reproduce.

### Deliverable contract

The deliverable is a bundle containing:
1. Frame graph diagram or table with transform sources.
2. Versioned message contract documents for every perception topic.
3. Adapter code with unit tests for frame conversion and stale-message rejection.
4. Verification report covering each decision gate, with metrics, dataset identifiers, and pass/fail status.
5. Open risks list, with each item naming its owner and the condition that would change its status.

Mark any library call, message field, or tool option whose behavior depends on version as requiring verification against current official documentation before use.

### What not to do

- Do not tune thresholds on the evaluation log and report results on that same log.
- Do not merge sensor data with unknown or assumed frames.
- Do not enable closed-loop control from perception output without passing the authority gate.
- Do not state accuracy, safety, or compliance outcomes that the evidence does not directly support.
- Do not overwrite recorded logs or calibration files in place; write new versions with provenance.


## specialized-domains-engineering

**Use when:** Use when building, reviewing, or modifying code in regulated or high-stakes specialized domains such as embedded/firmware, safety-critical control, medical device software, financial trading or settlement, scientific numerical computing, geospatial, cryptography-adjacent, or hardware-facing systems where correctness, units, timing, or compliance constraints dominate ordinary software practice.

### Purpose and boundaries

This skill guides engineering work where ordinary web or CRUD practices are insufficient because errors have physical, financial, legal, or scientific consequences. It covers: identifying domain invariants, selecting correctness-preserving designs, verifying behavior with domain-appropriate evidence, and documenting what was and was not proven.

It does not cover: certifying software to a standard, providing legal or regulatory opinions, designing hardware, or replacing a qualified domain expert, safety engineer, or auditor. Where a deliverable would be relied upon for safety, patient, financial, or legal outcomes, state that a qualified reviewer must sign off.

### Inputs and assumptions

Before writing code, establish:

1. **Domain and consequence class**: what fails, who is harmed, and the worst credible outcome.
2. **Governing requirements**: specifications, interface control documents, applicable standards named by the user. Do not assume a standard applies; ask.
3. **Target environment**: MCU/OS/runtime, clock source, numeric precision, toolchain version, library versions.
4. **Units and coordinate conventions**: SI or otherwise, frames of reference, time base (UTC, TAI, monotonic, exchange time), timezone rules.
5. **Data provenance**: sensor calibration, market data source, dataset licensing and consent status.

If any of these is unknown and affects design, stop and list the open questions. Assumptions made to proceed must be labeled in the deliverable.

### Operating workflow

1. **Restate invariants.** Write 3–8 invariants in testable form, e.g., "actuator command never exceeds ±2.5 N," "order quantity is never negative after fill," "geodetic transforms round-trip within 1 mm over the service area."
2. **Model units and types.** Use distinct types or wrappers for physical quantities, currency, and time bases. Reject implicit conversions. Prefer explicit conversion functions with documented constants.
3. **Choose the numeric strategy.** Decide between fixed-point, floating-point, or arbitrary precision. For money, use integer minor units or decimal types, never binary floating point. For accumulation over long horizons, use compensated summation or wider accumulators and justify the choice.
4. **Design for bounded behavior.** Specify worst-case execution time, memory ceilings, and maximum latency where relevant. Avoid unbounded allocation, unbounded recursion, and blocking calls on real-time paths.
5. **Implement defensively at boundaries.** Validate every input crossing a trust, device, or unit boundary. Reject out-of-range values explicitly rather than clamping silently, unless the specification mandates clamping, in which case log and count it.
6. **Make failure states explicit.** Represent sensor faults, timeouts, stale data, and partial writes as first-class states with defined transitions to a safe state.
7. **Verify (see below) before declaring completion.**

### Decision gates

Stop and obtain explicit human approval before proceeding if the task involves:

- Deleting or overwriting calibration data, production configuration, ledgers, patient records, or firmware images.
- Flashing hardware, changing actuator limits, or altering safety interlocks.
- Sending live orders, transactions, messages, or commands to external systems.
- Modifying audit trails, logging retention, or consent records.
- Changing a numeric tolerance, rounding rule, or unit convention already used in production, since this changes historical results.
- Adding or upgrading a dependency in a certified or validated build.
- Handling personal health, financial, or location data beyond what the task requires.

Also gate on scope: if a fix requires changing a requirement rather than code, return the conflict to the requirement owner.

### Verification and evidence

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

### Failure handling

- **Test failure in an invariant:** treat as a defect in code or requirement; do not weaken the test. Identify which side is wrong with evidence.
- **Ambiguous unit or tolerance:** halt that component, record the ambiguity, and request clarification.
- **Missing reference data:** proceed only with a clearly labeled provisional result.
- **Environment mismatch** (different compiler, runtime, or timer resolution than the target): state the mismatch and what evidence it invalidates.
- **Discovered safety-relevant defect in shipped behavior:** stop, report it with reproduction steps, and do not patch production without the decision gate approval.

### Deliverable contract

Every deliverable must include:

1. Changed artifacts and a one-paragraph summary of behavior changes.
2. The invariant list with test mapping.
3. Unit, numeric, and timing decisions with rationale.
4. Verification performed, with exact commands or procedures, tool versions, and results.
5. Verification not performed, and the risk it leaves.
6. Open assumptions and required approvals.
7. A statement that domain or compliance sign-off is required before use in a regulated or safety context.

### What not to do

- Do not use binary floating point for currency or exact-rounding requirements.
- Do not silently clamp, coerce, or default out-of-range physical or financial values.
- Do not invent standard clauses, API names, flags, package versions, or benchmark numbers. Where a detail is version-sensitive, mark it "verify against current official documentation" and do not state it as fact.
- Do not claim compliance, certification, or safety guarantees.
- Do not use wall-clock time for interval measurement on control paths; use monotonic sources.
- Do not add unbounded dynamic allocation or blocking I/O to real-time paths.
- Do not weaken or delete failing tests to achieve a green build.
- Do not execute actions in the decision gates without explicit approval.

