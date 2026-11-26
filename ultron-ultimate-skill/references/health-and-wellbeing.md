# Health and Wellbeing

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

## biometric-health-analytics

**Use when:** Use when analyzing wearable or clinical biometric data (heart rate, HRV, sleep, activity, glucose, blood pressure, body composition) to build trends, cohort summaries, or wellness reports, and when deciding whether results are reliable enough to communicate.

### Purpose and boundaries

This skill guides analysis of time-series and episodic biometric data for wellness monitoring, research summaries, and clinical-support analytics. It covers data quality assessment, cleaning, feature derivation, trend and variability analysis, cohort comparison, and reporting with stated uncertainty.

It does not cover diagnosis, treatment recommendations, medication changes, or clinical decisions. Any finding that could alter care must be escalated to a licensed clinician. It does not authorize transmitting identifiable health data to any external service, model, or person.

### Inputs and assumptions

Before analysis, record:

1. **Source and device**: manufacturer, model, firmware or app version when known, sensor type (optical PPG, chest strap ECG, CGM, cuff, scale).
2. **Sampling**: nominal interval, timestamp timezone, whether values are raw, averaged, or device-derived scores (e.g., proprietary "readiness" or "sleep score" values are not directly comparable across vendors).
3. **Context**: wear-time expectations, known events (illness, travel, medication change, shift work), user-reported labels.
4. **Consent and purpose**: the stated use, and whether the data is identifiable, pseudonymized, or aggregated.
5. **Unit and definition checks**: confirm units (bpm, ms for RR/HRV, mg/dL or mmol/L for glucose, mmHg), and the HRV metric (RMSSD, SDNN, or other). Do not assume.

Assume timestamps may drift, sensors may be worn inconsistently, and vendor-derived scores may change without notice.

### Operating workflow

1. **Profile the data.** Count records per day, gaps longer than the nominal interval, duplicate timestamps, out-of-range values, and timezone transitions (DST, travel).
2. **Assess wear and coverage.** Compute per-day coverage fraction (valid samples / expected samples). Flag days below the coverage threshold set in Decision gates.
3. **Clean conservatively.** Remove physiologically impossible values using documented bounds (for example, resting heart rate outside 25–220 bpm is suspect; confirm bounds for the population). Mark removals; never silently impute. Interpolate only gaps shorter than a pre-declared limit, and record the count.
4. **Derive features.** Use daily aggregates with the same definition across the period: median resting HR, nightly RMSSD from a fixed sleep window, sleep duration and timing, step totals, glucose time-in-range against a stated target band.
5. **Analyze trends.** Use robust methods: rolling medians, 7- and 28-day baselines, and personal z-scores or percent deviation from the individual's own baseline. Test for change with a method suited to autocorrelated series; state the method. Avoid reporting p-values from naive tests on dependent daily data as if they were independent.
6. **Contextualize.** Annotate known events. Check whether an apparent shift coincides with a firmware update, device change, or wear-pattern change before attributing it to physiology.
7. **Report with uncertainty.** Provide ranges, coverage, and the number of days behind each claim.

### Decision gates

- **Gate A, data sufficiency:** Proceed to trend claims only if at least 70% of expected days meet the coverage threshold and the baseline window has at least 14 valid days. Otherwise report descriptive statistics only and state the limitation.
- **Gate B, cross-source comparison:** Do not compare vendor scores across devices or firmware versions without a documented calibration or a side-by-side overlap period of at least 14 days.
- **Gate C, clinical relevance:** If a result crosses a commonly cited clinical threshold (for example, sustained resting HR above 100 bpm at rest, glucose persistently above target, blood pressure elevations across readings), state the observation and recommend clinician review. Do not characterize it as a diagnosis.
- **Gate D, external sharing:** Stop before sending any data, figures containing identifiers, or model outputs outside the approved environment. Obtain explicit approval from the data owner.
- **Gate E, irreversible actions:** Deletion of source data, overwriting raw files, or altering retention settings requires explicit written approval and a verified backup.

### Verification and evidence

Each report must include:

- Coverage table: expected vs. valid samples per day, and total excluded records with reasons.
- Method statement: cleaning bounds, interpolation limit, metric definitions, baseline window, and statistical test used.
- Sensitivity check: rerun the headline trend with the most aggressive exclusion rule and confirm direction is unchanged; report if it is not.
- Reproducibility: a script or step list that regenerates every number from the raw export. Record library names and versions, and mark any version-sensitive API behavior for verification against current official documentation.
- Spot check: manually verify at least five randomly selected days against the raw export.

Do not state accuracy or validity of a device against a reference unless a validation study with a named reference method is provided.

### Failure handling

- **Timestamp anomalies:** If timestamps are non-monotonic or shifted, stop and request the export with timezone metadata. Do not reorder silently.
- **Unit mismatch:** If values fall outside expected ranges for the stated unit, check for mg/dL vs. mmol/L or ms vs. s before excluding.
- **Missing baseline:** Report current values without deviation scores and state that no baseline exists.
- **Conflicting sources:** Report both, identify which is primary, and do not average across sources without calibration.
- **Result contradicts user report:** Present both, flag the discrepancy, and suggest clinician discussion if it concerns symptoms.

### Deliverable contract

Return:

1. Data summary (source, period, coverage, exclusions).
2. Findings, each with magnitude, direction, uncertainty, and number of supporting days.
3. Limitations and gate outcomes (A through E), with pass or fail stated.
4. Method appendix sufficient for independent reproduction.
5. Escalation items requiring clinician or data-owner review.

Do not include diagnostic language, treatment advice, or guarantees of accuracy. Do not claim compliance with any regulation unless the user supplies the governing policy and it has been reviewed.


## fitness-performance-coaching

**Use when:** Use when designing, reviewing, or adjusting a training program, performance plan, or fitness progression for an individual or group, including strength, conditioning, endurance, mobility, and recovery planning, and when translating assessment data into weekly training decisions.

### Purpose and boundaries

This skill produces structured training plans, progression decisions, and performance reviews for adults training toward defined goals (strength, hypertrophy, endurance, sport-specific capacity, general fitness, return-to-training after a period of inactivity). It works from client-supplied data and coach-observed evidence.

In scope: goal definition, needs analysis, periodized weekly structure, load and volume prescription, exercise selection, progression and deload rules, recovery and sleep guidance within training, session review, and plan adjustment.

Out of scope: diagnosing injury or disease, prescribing treatment for pain, managing medication or nutrition for medical conditions, and clearing anyone for exercise after a cardiac, metabolic, or post-surgical event. Route these to a licensed clinician and state the referral explicitly.

### Inputs and assumptions

Required before planning:
- Goal statement, stated as a measurable outcome and a target date.
- Training history: current weekly sessions, years of consistent training, longest recent break.
- Available time: days per week, minutes per session, equipment access.
- Baseline measures: relevant tests (e.g., estimated 1RM or rep-max on two or three lifts, submaximal run or row time, mobility screen results, bodyweight trend).
- Health screen answers and any medical clearance status.
- Recovery context: sleep hours, occupational load, stress level as reported.

Assumptions you must label in the output: estimated maxes are derived from submaximal testing, not measured; recovery data is self-reported; progression rates are starting estimates.

If a required input is missing, plan conservatively and list the gap. Do not invent baseline numbers.

### Operating workflow

1. **Restate the goal** as a testable outcome with a timeframe. Reject vague goals ("get fitter") by proposing a specific replacement and asking for confirmation.
2. **Perform a needs analysis.** List the physical qualities the goal depends on (maximal strength, power, muscular endurance, aerobic capacity, speed, mobility) and rank them by importance.
3. **Check constraints.** Compare available days and time against the volume the goal needs. If the gap is larger than about 25 percent of required weekly volume, say so and offer two realistic options.
4. **Select the structure.** Use a block structure of 3 to 6 weeks: accumulation (higher volume, moderate intensity), intensification (lower volume, higher intensity), and realization or deload. Match frequency to training age: 2 to 3 sessions per muscle group per week for beginners and intermediates, with compound lifts as primary movements.
5. **Prescribe loads** as percentages of estimated 1RM or as reps in reserve (RIR). Use RIR 2 to 3 for most accessory work and RIR 0 to 2 for main lifts in intensification weeks.
6. **Define progression rules** in advance: add load when all prescribed reps are achieved with RIR at or above target for two consecutive sessions; add a rep when load is unchanged; hold when technique degrades.
7. **Write the deload trigger**: scheduled every 4th to 6th week, or earlier if two or more red flags appear (see Decision gates).
8. **Document the plan** in the deliverable format below.

Domain examples:
- A 45-year-old returning after 18 months off, goal of "carry 20 kg groceries and climb three flights without stopping": plan 3 full-body sessions, emphasize hip hinge, carries, and step-ups, start at RIR 4, no maximal testing for the first four weeks.
- A recreational runner targeting a 10 km time in 12 weeks: 3 running sessions (one interval, one tempo, one long run), 2 strength sessions emphasizing single-leg work, weekly volume increase capped at 10 percent.

### Decision gates

Stop and seek explicit approval from the client or supervising professional before proceeding when:
- Any health screen answer indicates chest pain, syncope, uncontrolled hypertension, recent surgery, pregnancy complications, or unexplained symptoms during exertion.
- The client requests maximal testing, a rapid weight-change target, or a training load increase over 10 percent per week.
- The plan would change medication timing, supplementation, or diet for a medical condition.
- Any action affects other people, such as booking a group session, sharing client data with a third party, or publishing progress images.

Red flags that trigger an automatic deload review: resting heart rate elevated 5 or more beats above baseline for three consecutive mornings, two or more missed sessions in a week without explanation, reported sleep under 6 hours on most nights, or a load drop of more than 10 percent on a main lift without a planned cause.

### Verification and evidence

Before delivering a plan, check each item:
- Every session has a stated purpose and a volume count (sets × reps × load or RIR).
- Weekly volume per muscle group falls within the chosen band and matches the needs analysis ranking.
- Progression rules are written as explicit conditions, not descriptions.
- Estimated maxes are labeled as estimates with the method named.
- The plan includes at least one retest point and the metric to compare.
- No exercise prescribed beyond the client's stated equipment and capability.

For session reviews, compare logged performance to the prescription and state the variance numerically. Attribute changes to a specific cause only when logs support it; otherwise write "cause unknown, monitor for two weeks."

Version-sensitive items, such as current guidance on tracking devices, app features, or published training-volume recommendations, must be marked "verify against current official documentation" rather than stated as fact.

### Failure handling

- **Missing baseline data:** proceed with a conservative two-week assessment block and flag the plan as provisional.
- **Client reports pain:** stop the prescribed movement, record location, intensity, and onset, and route to a qualified clinician. Do not offer substitute exercises for pain-driven decisions beyond removing the aggravating movement.
- **Conflicting goals** (for example, maximal strength and marathon training at high volume): state the interference trade-off and ask which goal takes priority for each block.
- **Logs are incomplete:** do not infer missing sets. Mark them as unrecorded and reduce confidence in trend conclusions.

### Deliverable contract

The output must contain, in order:
1. Goal statement with timeframe and measurable target.
2. Assumptions and data gaps, labeled.
3. Needs analysis ranking.
4. Block structure with week-by-week summary.
5. Session templates with exercise, sets, reps, load method, and rest.
6. Progression and deload rules as explicit conditions.
7. Retest schedule with metrics.
8. Safety notes and any referrals required.
9. Items marked for verification against current documentation.

Do not: guarantee outcomes, invent test results or population statistics, prescribe maximal testing without approval, give medical or nutritional treatment advice, or present estimated values as measured values.


## health-clinical-analytics

**Use when:** Use when analyzing clinical data drawn from external health registries (disease, device, cancer, vaccine, or patient-outcome registries) to build cohorts, compute outcome measures, assess data quality, or prepare registry-based evidence for research, quality improvement, or regulatory submissions.

### Purpose and boundaries

This skill covers analysis of data extracted from external clinical registries: the registry's own extracts, linked administrative data, or registry-derived aggregate tables. It produces cohort definitions, outcome tables, data-quality assessments, and analysis code or specifications with an audit trail.

In scope: cohort construction from registry fields, codebook mapping, denominator and numerator logic, survival and incidence calculations, risk adjustment design, missingness assessment, and reporting that states limitations.

Out of scope: individual patient re-identification, linking records to identifiers the user is not authorized to hold, making treatment recommendations for individual patients, and asserting causal effects without an explicit design that supports them.

### Inputs and assumptions

Required before starting:
- Registry name, version or data-release date, and the data use agreement or governance basis.
- Data dictionary or codebook. If absent, stop and request it.
- Study question stated as population, exposure or intervention, comparator, outcome, time window, and estimand.
- Intended use: research, internal quality improvement, or regulatory. Each requires different sign-off.

Assumptions to state explicitly in every deliverable: registry completeness is unknown unless the registry publishes a validated completeness figure; coding changes across release years are possible; field definitions may differ from clinical usage.

### Operating workflow

1. **Confirm governance.** Verify that the requested use matches the data use terms. Record the approver's name and date.
2. **Map the codebook.** Build a table: registry field, permitted values, meaning, and the study variable it feeds. Flag any value that has no mapping.
3. **Define the cohort in code-independent prose first.** Write inclusion and exclusion criteria with the index date rule. Then translate to logic. Keep both versions in the deliverable.
4. **Profile data quality.** For each analytic variable, compute missingness rate, out-of-range counts, impossible date sequences (for example, death before diagnosis), and duplicate record keys. Report by year and by reporting site if available.
5. **Resolve duplicates and conflicts.** Apply a documented rule, such as retaining the most recent record per patient-event key. Never silently drop records.
6. **Compute outcomes.** Use the pre-specified time windows. For time-to-event outcomes, state the censoring rule and handle competing risks explicitly.
7. **Run sensitivity checks** (see Verification).
8. **Write the limitations section** before the results, not after.

### Decision gates

- **Gate A, codebook complete?** Proceed only if every analytic variable maps to a documented definition. Otherwise return to step 2.
- **Gate B, missingness acceptable?** If a key exposure or outcome field exceeds 10% missing, do not impute without a pre-specified method and a missing-data sensitivity analysis. Above 30%, report the analysis as exploratory only.
- **Gate C, linkage valid?** If records are linked across sources, require a documented linkage method and an estimate of false match or missed match rates. Without these, do not present linked results as definitive.
- **Gate D, external impact?** Any output leaving the analyst's team (publication, regulator submission, public dashboard, patient-facing material) requires explicit written approval from the data steward and the responsible clinical lead. Small-cell counts (fewer than 11 in a reported cell, unless the governance terms specify otherwise) must be suppressed or aggregated before release.

### Verification and evidence

Measurable checks before release:
- Cohort size reconciles: starting population minus each exclusion equals the final N, with a flow table.
- Outcome rates recomputed independently by a second person or a second method match within rounding.
- Date sanity: zero records with event dates outside the registry coverage period, or each such record is listed with a disposition.
- Sensitivity analysis: at least one alternative definition of the primary outcome and one alternative handling of missing data. Report whether conclusions change.
- Temporal stability: compare rates across release years; explain any shift greater than the pre-stated threshold by coding change, policy, or true change.

Evidence to retain: codebook version, query or code hash, run date, data release identifier, and reviewer sign-off.

### Failure handling

- **Codebook ambiguity:** Stop. List the ambiguous codes with counts and request clarification from the registry maintainers. Do not guess a mapping.
- **Unexpected count change between runs:** Diff the input extracts before investigating the code. Most discrepancies come from data refresh, not logic.
- **Small cells breaching disclosure rules:** Aggregate categories or suppress. Do not report the value in a footnote or chart label.
- **Results contradict the registry's published figures:** Report the discrepancy with both calculations and do not choose the more favorable one.
- **Requested analysis implies individual-level disclosure:** Decline and offer aggregate alternatives.

### Deliverable contract

Every deliverable contains, in order:
1. Study question and estimand, governance reference, and intended use.
2. Data source identifier, release date, and codebook version.
3. Cohort definition in prose and logic, with a flow table.
4. Data-quality profile with missingness and conflicts.
5. Limitations and assumptions.
6. Results with confidence intervals and suppression notes.
7. Sensitivity analyses and verification results.
8. Approval status and reviewer names.

Do not include unverified external benchmark figures or claims of regulatory compliance. Where software functions, library versions, or registry-specific API endpoints are referenced, mark them "verify against current official documentation" unless confirmed in the current release notes.

### What not to do

- Do not merge registries or link identifiers without documented authorization.
- Do not report precision beyond the data's accuracy.
- Do not present registry rates as population rates without stating the coverage denominator.
- Do not treat absence of a record as absence of an event without checking reporting completeness.
- Do not alter outcome definitions after viewing results.


## medical-compliance-pharmacy

**Use when:** Use when reviewing, drafting, or auditing pharmacy compliance work in healthcare settings, including controlled-substance records, dispensing and verification workflows, sterile or non-sterile compounding documentation, recall and adverse-event handling, patient privacy in pharmacy operations, and preparation for inspections or internal audits.

### Purpose and boundaries

This skill supports compliance review of pharmacy operations: dispensing records, controlled-substance accountability, compounding documentation, recall and adverse-event workflows, privacy handling, and audit readiness. It produces findings, gap lists, corrective-action drafts, and checklists.

It does not replace a licensed pharmacist's clinical judgment, a compliance officer's legal determination, or counsel's interpretation of statutes. It does not certify that a facility is compliant.

### Inputs and assumptions

Before analysis, confirm:

1. Jurisdiction and facility type (retail, hospital, long-term care, compounding, specialty, mail-order).
2. Governing standards in scope. Typical sources include federal controlled-substance rules (21 CFR Parts 1300–1321), USP <797> and <800> for compounding, state board of pharmacy rules, HIPAA Privacy and Security Rules, and accreditation standards. Mark each citation as version-sensitive and verify against the current official text before relying on it.
3. Record type and period under review. Request actual records or redacted samples, not summaries alone.
4. Whether the task is internal self-assessment, pre-inspection preparation, or response to a regulator finding.

Assume nothing about a facility's policies. Ask for them.

### Operating workflow

1. Define the review scope in one sentence: process, time window, locations, and standards.
2. Build a control inventory: for each process, list the required record, owner, frequency, and retention period as stated in the source policy.
3. Reconcile records against the inventory. For controlled substances, reconcile receipts, dispensings, returns, waste, and on-hand counts over the window. Any unexplained variance is a finding until explained.
4. Sample transactions. Use a documented sampling method. For high-risk items (opioids, stimulants, high-alert injectables), review 100 percent where volume allows.
5. Trace exceptions: overrides, late verifications, voided prescriptions, emergency-kit use, and after-hours access.
6. Classify each finding (see Decision gates) and draft a corrective action with owner and due date placeholders for the facility to fill.
7. Prepare the deliverable contract output.

### Decision gates

Stop and request explicit human approval before:

- Altering, backdating, or "correcting" any dispensing, count, or waste record.
- Submitting any report to a regulator, DEA, state board, accreditor, insurer, or payer.
- Destroying, returning, or transferring controlled substances or patient-specific materials.
- Disclosing protected health information outside the minimum necessary for the review.
- Communicating a finding to an external party or to the public, including recall notices.
- Recommending suspension of a staff member's license, access, or duties.

Severity classification:

- Critical: unexplained controlled-substance variance, missing sterile-compounding batch records for released product, dispensing without valid prescription evidence, active privacy breach.
- Major: verification step skipped without documented override, expired or unverified compounding components in use, recall not traced to patients.
- Minor: incomplete signature fields, delayed logging within policy tolerance, labeling format deviations without patient impact.

Escalate Critical findings immediately to the responsible pharmacist-in-charge and compliance officer.

### Verification and evidence

Every finding must cite:

- The specific record identifiers reviewed (use internal IDs, not patient names).
- The governing requirement and its version or effective date.
- The observed condition and the expected condition.
- Whether the finding is confirmed by two sources (for example, dispensing log and inventory count).

Quality checks before delivery:

- Reconciliation totals balance to zero variance or every variance has a stated, evidenced explanation.
- Sample size and selection method are stated; the sampling frame is reproducible.
- No finding relies on a single unverified secondhand statement.
- Every citation is flagged for current-version verification.
- No recommendation claims guaranteed compliance or guaranteed inspection outcome.

### Failure handling

- Missing records: record as a finding of absence, do not infer the content. Request the record or a written explanation.
- Conflicting sources: report both, identify which is primary per policy, and do not resolve by assumption.
- Incomplete data window: narrow the conclusion to the covered period and state the gap.
- Ambiguous regulation: flag as requiring counsel or regulator clarification. Do not invent interpretation.
- Discovered potential diversion or patient harm: halt the review of that thread, escalate per Decision gates, preserve records unchanged.

### Deliverable contract

Return a document with these sections, in order:

1. Scope statement (process, period, locations, standards with version flags).
2. Summary: counts by severity and the top three risks.
3. Findings table: ID, severity, requirement, evidence references, observed versus expected condition, confirmation status.
4. Reconciliation results with stated variances.
5. Corrective-action drafts: action, owner assignment and target date, verification method.
6. Open items requiring human approval, listed separately.
7. Limitations: data gaps, sampling constraints, items outside scope.

Do not include patient identifiers in the deliverable. Do not state that the facility is compliant unless the scope and evidence explicitly support a bounded statement, and phrase it as such.


## nutrition-meal-planning

**Use when:** Use when drafting, adjusting, or reviewing multi-day meal plans that must meet stated energy, macronutrient, food-group, budget, or dietary-restriction requirements for a healthy adult or household, not for diagnosing or treating disease.

### Purpose and boundaries

This skill produces practical, multi-day meal plans with shopping lists, portion guidance, and a nutritional check against stated targets. It covers general healthy-adult eating, common preferences (vegetarian, lower-sodium, high-protein, budget-limited), and routine restrictions such as lactose avoidance or gluten avoidance for non-celiac preferences.

It does not cover: diagnosing conditions, prescribing therapeutic diets (renal, insulin-dependent diabetes management, enteral or tube feeding, oncology, eating-disorder recovery), planning for infants, pregnancy, or lactation, or adjusting medication-related intake. Route these to a registered dietitian or treating clinician and stop after producing only general, non-therapeutic guidance.

### Inputs and assumptions

Collect before planning:
1. Age band, sex, height, weight, activity level (or a stated energy target from a clinician or prior plan).
2. Number of people and meals per day to cover (for example, 3 meals plus 1 snack, 7 days).
3. Restrictions and allergies, stated separately from preferences. Treat allergies as hard exclusions.
4. Budget ceiling per week and cooking capacity (minutes per meal, equipment).
5. Region and available stores, so ingredients are realistic.

If a value is missing, state the assumption in the output header. Do not invent medical history. Estimated energy uses a stated equation (for example, Mifflin-St Jeor with an activity multiplier) and is labeled as an estimate.

### Operating workflow

1. Confirm scope against the boundaries above. If out of scope, stop and say so.
2. Set targets: energy, protein, fiber, sodium ceiling, and food-group servings. Cite the reference source used (for example, the national dietary guidance applicable to the user's region) and mark it "verify against current official guidance."
3. Build a template per day: breakfast, lunch, dinner, snacks, each with a protein source, vegetable or fruit, a whole-grain or starch, and a fat source.
4. Rotate ingredients across days to reduce waste and cost; reuse cooked components (for example, one batch of grains used twice).
5. Generate the consolidated shopping list, grouping by store section and summing quantities.
6. Compute daily totals using a stated nutrient database and record which database and version were used.
7. Run the verification checks below and revise.

### Decision gates

- Allergy or intolerance conflict with any recipe: remove the item; do not substitute silently.
- Daily energy estimate deviates more than 10% from target: adjust portions or add or remove a snack, then recheck.
- Sodium above the stated ceiling: swap processed items for fresh or low-sodium equivalents before finalizing.
- Plan requires more than 45 minutes of active cooking per meal, or exceeds stated budget: simplify or flag the trade-off.
- Request involves a clinical condition, medication interaction, or pediatric or pregnancy use: stop and refer.
- Requires explicit user approval before: sending a plan to a third party, saving or overwriting an existing plan or client record, sharing personal health data, publishing, or charging for a service.

### Verification and evidence

Measurable checks before delivery:
- Every day contains at least one protein source, two vegetable or fruit servings, and one whole-grain or fiber-rich starch.
- Daily fiber, protein, and sodium totals are reported with the database name and version.
- Shopping list total is within the stated budget, with the price basis stated.
- No ingredient appears in the exclusion list, including sauces, stocks, and processed items.
- Each recipe's stated portion count matches the shopping list quantity.
- Any figure that depends on a guideline or database version carries the note: "verify against current official documentation."

Do not claim the plan is guaranteed to produce weight change, disease prevention, or any health outcome.

### Failure handling

- Missing inputs: list them, proceed only with labeled assumptions, and ask for confirmation.
- Targets unreachable within budget or restrictions: report the gap numerically and offer two options.
- Nutrient database unavailable: state that totals are unverified rather than estimating silently.
- Conflicting user statements: ask rather than choose.

### Deliverable contract

Output one document containing, in order:
1. Header: scope, assumptions, targets with sources, nutrient database name and version.
2. Day-by-day plan in a table: meal, dish, portion, energy, protein, fiber, sodium.
3. Consolidated shopping list with quantities and estimated cost.
4. Verification summary: which checks passed and any open items.
5. Referral note if any out-of-scope element was encountered.

Keep prose minimal. Do not include unrequested medical advice, testimonials, or promotional language.


## wellbeing-symptom-tracking

**Use when:** Use when a user wants to log, structure, or review personal or client wellbeing symptoms over time, including symptom diaries, trend summaries, and handoff notes for a clinician or coach, and when red-flag symptoms may need escalation.

### Purpose and boundaries

This skill turns scattered symptom reports into a consistent, time-stamped record, summarizes patterns, and prepares accurate handoffs. It supports people who track their own wellbeing and professionals (coaches, wellness practitioners, care coordinators) who document client-reported symptoms.

It does not diagnose, prescribe, adjust medication, interpret lab results as clinical findings, or replace emergency care. It records and organizes; clinical judgment belongs to the qualified professional.

### Inputs and assumptions

Collect or confirm before logging:

- Symptom description in the person's own words, plus a short neutral restatement.
- Onset date or time, duration, and whether it is continuing.
- Severity on a stated scale (for example 0 to 10), with the scale's anchors defined by the person.
- Possible triggers, context, sleep, activity, and medications as reported. Record them as reported, not as causes.
- Who will read the output and for what purpose.

Assumptions to state explicitly in every output: entries reflect self-report, timing may be approximate, and the record is incomplete unless the person confirms otherwise.

### Operating workflow

1. Classify the request: single entry, longitudinal review, or handoff summary.
2. Screen for red flags before any other work (see Decision gates).
3. Normalize each entry into fixed fields: date/time, symptom, severity, duration, frequency, triggers reported, actions taken, outcome.
4. Keep the person's original wording in a separate field; never overwrite it with paraphrase.
5. For reviews, order entries chronologically and group by symptom, not by theme you have inferred.
6. Compute simple descriptive facts only: frequency per week, median severity, count of days with symptom present, change in average severity between two stated windows.
7. Describe patterns as observations with the number of supporting entries (for example "reported on 9 of 14 days, mostly after reported late nights"). Avoid causal language.
8. Produce the deliverable in the contract format.

### Decision gates

- **Immediate escalation gate:** If any entry describes chest pain, difficulty breathing, fainting, stroke-like signs, thoughts of self-harm or harming others, severe bleeding, or sudden severe headache, stop the summary work. Tell the user to contact emergency services or a crisis line in their region now, and flag the record for the responsible professional. Do not reassure or minimize.
- **Urgent review gate:** Worsening trend over three or more consecutive entries, new symptom in a person already on monitoring, or severity at the top of the stated scale for more than two consecutive days. Recommend prompt professional contact and mark the summary "needs clinician review."
- **Sharing gate:** Any export, transmission to a third party, or inclusion in a shared document requires explicit approval from the person whose data it is, naming the recipient and the content. Obtain it before producing a shareable version.
- **Deletion or alteration gate:** Editing or deleting past entries requires explicit confirmation. Prefer appending corrections with a dated note.
- **Scope gate:** If the user asks for a diagnosis, treatment change, or interpretation of medical tests, decline that part, give the supported summary, and recommend the appropriate professional.

### Verification and evidence

Before delivering, check:

- Every summary statistic traces to a listed entry. Show the entry count and date range.
- No symptom appears that was absent from the source entries.
- Original wording is preserved verbatim in the source field.
- Dates are consistent, in ISO format, with no entries out of sequence.
- Causal words ("caused," "due to," "because of") do not appear unless the person themselves attributed the cause, and then they are quoted as attributions.
- Red-flag screen was run and its result is stated.
- Limitations line is present.

### Failure handling

- Missing dates: record "date unknown," do not estimate silently; ask for approximate ranges.
- Conflicting entries for the same day: list both with sources; do not average them.
- Severity scale changed mid-record: report the two periods separately.
- Ambiguous symptom description: ask one clarifying question rather than guessing a category.
- Input suggests a medical emergency: follow the escalation gate first, then resume only if the person confirms they are safe and help is in progress.

### Deliverable contract

Return:

1. Header: subject label, date range, entry count, data source (self-report or professional entries).
2. Red-flag status: "none identified" or the flagged items with the action recommended.
3. Chronological log table: date, symptom, severity, duration, reported triggers, verbatim note.
4. Descriptive summary: 3 to 6 bullet observations, each with supporting entry count.
5. Open questions for the person or clinician.
6. Standard limitation statement: "This summary organizes self-reported information. It is not a diagnosis or treatment recommendation."

Do not include: diagnostic labels, treatment or dose advice, unsupported causal claims, invented normal ranges, or content from entries outside the requested date range.

