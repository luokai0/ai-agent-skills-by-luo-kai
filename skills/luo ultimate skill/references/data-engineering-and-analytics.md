# Data Engineering and Analytics

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## app-data-layer-integration

**Use when:** Use when connecting an application to a database or storage backend, adding or changing a data access layer, repository, ORM mapping, connection handling, or migration path, and the work must preserve correctness, transactions, and operational safety.

### Purpose and boundaries

Use this skill to design, implement, and verify the seam between application code and a persistent store (relational database, document store, key-value cache of record, or object storage). It covers: access-layer structure, connection and pool configuration, query and transaction boundaries, schema-to-model mapping, error translation, and rollout of data-access changes.

Out of scope: choosing a database vendor from scratch, tuning cluster hardware, designing analytics warehouses, and writing business logic unrelated to persistence.

### Inputs and assumptions

Collect before editing:

- Store type, engine name, and exact server version. Record it; do not assume.
- Current access pattern: ORM, query builder, raw SQL, or driver calls.
- Existing transaction semantics and isolation level in use.
- Expected load: reads/writes per second, largest table row counts, p95 latency target.
- Schema ownership: who runs migrations, and whether a migration tool already exists.
- Environments available for testing (local, staging, production-like snapshot).

If any of these is unknown, state the assumption explicitly in the change summary.

### Operating workflow

1. **Map the current surface.** List every module that opens connections, builds queries, or starts transactions. Use search across the codebase, not memory.
2. **Define the boundary.** Place all persistence calls behind repository or data-access interfaces. Business code receives domain objects, never driver rows or ORM entities that leak lazy-loading behavior.
3. **Centralize configuration.** One place sets pool size, timeouts, statement timeouts, and TLS. Read credentials from the secret store, never from source or logs.
4. **Make transactions explicit.** Each unit of work opens and closes one transaction at the service layer. Repositories accept a transaction handle rather than opening their own.
5. **Translate errors.** Map driver errors to domain errors: unique violation, foreign key violation, serialization failure, timeout, connection loss. Retry only idempotent operations and only on transient classes.
6. **Write queries with bound parameters only.** Never concatenate user input into SQL. Keep queries reviewable as text.
7. **Plan the schema change separately.** Additive migrations first (new nullable column, new table), code that writes both shapes, backfill in batches, then switch reads, then remove the old shape in a later release.
8. **Test against a real engine.** Use the same engine family and version as production. In-memory substitutes do not validate SQL semantics.

### Decision gates

- **Gate A: ORM versus raw SQL.** Use the ORM for standard CRUD. Use explicit SQL for multi-table reporting, bulk updates, or queries where the plan matters. Document each raw query with the reason.
- **Gate B: Retry or fail.** Retry only on serialization conflicts and transient connection errors, with bounded attempts and jittered backoff, and only if the whole transaction is re-executed. Otherwise fail fast.
- **Gate C: Migration safety.** If a migration locks a table longer than the agreed window, or rewrites a large table, stop and request a review of the lock strategy and an approved maintenance window.
- **Gate D: Isolation changes.** Changing isolation level or adding locks requires a concurrency test that reproduces the anomaly being addressed.
- **Gate E: Data movement.** Any copy, export, or deletion of production data requires explicit human approval naming the dataset, the destination, and the retention rule.

### Verification and evidence

- Integration tests run against the target engine version and cover: create, read, update, delete, unique constraint violation, rollback on failure, and concurrent update conflict.
- Query plans checked with the engine's explain facility for any query touching tables above the agreed row threshold. Record the plan summary in the change notes.
- Pool behavior verified under load: no connection leak after a 10-minute soak at target concurrency; pool wait time stays under the agreed budget.
- Migration rehearsed on a production-sized snapshot; record duration and lock observations.
- Confirm that no secret, full row payload, or personal data appears in logs at the chosen log level.
- Version-sensitive settings (driver option names, default isolation levels, pool parameters) must be checked against current official documentation for the exact versions in use. Mark any unverified item as unverified.

Do not report performance numbers without a reproducible measurement method and recorded environment.

### Failure handling

- **Connection refused or timeout:** verify credentials source, network path, and TLS settings; do not raise pool size as a first response.
- **Deadlock or serialization error:** capture the statements and lock order; fix ordering in code before adding retries.
- **Migration fails midway:** stop, do not re-run blindly. Confirm the migration tool's recorded state, then apply the documented recovery path. Obtain approval before any manual repair.
- **Test passes locally, fails in staging:** compare engine version, collation, timezone setting, and isolation defaults first.
- **Unexpected data mismatch after rollout:** disable the new read path via the existing flag, preserve evidence, and escalate. Do not write corrective updates without approval.

### Deliverable contract

Deliver:

1. Changed files list with one-line purpose each.
2. Access-layer interface summary: operations exposed, transaction handling, error mapping.
3. Schema change description with the staged migration plan and rollback path.
4. Test results: engine and version, commands run, pass/fail counts, and any skipped checks with reasons.
5. Query plan notes for flagged queries.
6. Open risks and unverified version-specific settings.
7. Explicit list of actions awaiting approval (destructive, irreversible, external, or sensitive).

What not to do:

- Do not open transactions inside repositories that are called from within another transaction.
- Do not catch and swallow database exceptions.
- Do not run destructive DDL (drop, truncate, column removal) in the same release as the code that stops using it.
- Do not invent driver options, pool parameters, or benchmark figures; verify them.
- Do not connect to production data stores for experiments.
- Do not store credentials, connection strings with passwords, or raw personal data in code, fixtures, or logs.


## data-analysis-sql-and-databases

**Use when:** Use when writing, reviewing, or debugging SQL queries, designing analytical datasets, validating database-backed metrics, or answering business questions from relational data stores.

### Purpose and boundaries

Covers answering analytical questions from relational databases and warehouses: query authoring, joins and aggregation, metric definition, data quality checks, and reporting results with stated confidence. Out of scope: database administration (provisioning, production index tuning, user and role management), schema migrations, writes to production tables, and non-relational stores unless the user confirms the approach applies.

### Inputs and assumptions

Before querying, establish:
- The exact question and the decision it informs.
- Engine and dialect (for example PostgreSQL, MySQL, BigQuery, Snowflake, SQLite). Do not assume function names transfer between engines. Verify syntax against the current official documentation for the engine and version in use.
- Schema: table grain, primary and foreign keys, and timestamp semantics (event time versus load time, timezone).
- Access level. Read-only is the default. Confirm whether the target is production or a replica.
- Metric definitions from the owning team. If none exist, write a definition, state it, and get it confirmed.

List every assumption in the output.

### Operating workflow

1. Restate the question as a measurable target: metric, population, time window, grain, and comparison baseline.
2. Inspect schema and sample rows with a row limit, and bound partitioned tables by date. Record row counts and null rates for key columns.
3. Define the grain of the final result before writing joins. Express it as "one row per X per Y".
4. Build the query as named CTEs, one logical step each: filter, deduplicate, join, aggregate.
5. Check join cardinality by comparing row counts before and after each join. Unexpected row multiplication is the most common analytical error.
6. Reconcile the total against an independent source (a source table, a previously published figure, or a simpler query) within a stated tolerance.
7. Document the final query, assumptions, and result.

### Decision gates

- Execute only when grain and time window are explicit. If either is missing, ask.
- Estimate scan cost before running against large or partitioned tables. If the query would scan full history without a filter or exceed the agreed budget, narrow it first.
- Require explicit approval before any of the following:
  - Running statements that write, delete, update, or alter schema.
  - Querying production when a replica exists.
  - Exporting data containing personal, financial, health, or credential fields.
  - Sharing results outside the requesting team.
  - Changing a dashboard, scheduled job, or shared metric definition.
- If two metric definitions compete, stop and present both with their numeric difference.

### Verification and evidence

Each check must pass or be reported as failed:
- Row counts after each join match the expected cardinality, which you state in advance.
- Grain columns are unique in the final output.
- Join-key null rates are below the threshold you declared, or the nulls are reported.
- The date range covers the requested window without gaps, and timezone handling is consistent.
- Reconciliation difference is within the stated tolerance. Do not claim an exact match without proof.
- At least three result rows are traced back to source records.

Report the evidence: query text, row counts, and reconciliation figures. Never present a number without its population and filters.

### Failure handling

- Syntax or engine error: correct the specific error. Do not rewrite the whole query.
- Empty result: check filters, timezone boundaries, case sensitivity, and type mismatches (string versus integer identifiers) before concluding no data exists.
- Inflated result: suspect fan-out from a non-unique join key and check distinct counts on each side.
- Failed reconciliation: report the gap and candidate causes ranked by likelihood. Do not alter the query to force agreement.
- Permission denied: stop, report, and request access. Do not seek workarounds such as shared credentials.

### Deliverable contract

Return:
1. The answer, with metric value, population, time window, and grain.
2. Final SQL, formatted, with a comment on each CTE's purpose.
3. Assumptions list.
4. Verification results, pass or fail per check.
5. Limitations, and what new evidence would change the conclusion.

Do not:
- Use `SELECT *` in deliverable queries.
- Present correlation as causation.
- Round away material uncertainty.
- Invent table names, column names, or dialect functions. Confirm each one from the schema.

### Ultron routing contract

**Choose this skill when:** the objective is answering an analytical question from relational databases or warehouses through query design, joins, aggregation, metric definitions, data-quality checks, and interpretation.

**Choose sql-and-data-performance when:** the primary problem is query latency, throughput, resource use, execution plans, index strategy, or cost, and semantic correctness must be preserved while tuning.

**Handoff contract:** this skill supplies the intended metric, grain, population filters, expected result semantics, and representative query. The performance skill returns an equivalent optimized query and before/after measurements; this skill verifies that the optimized result is semantically identical and that no cohort or denominator changed.

**Why the boundary exists:** a fast query that answers the wrong question is a failure. Analytical meaning and performance optimization require separate acceptance checks.


## data-analytics-modeling

**Use when:** Use when building, reviewing, or validating analytical or statistical models over external registry data (government, public-sector, licensing, corporate, clinical, or standards registries), including entity resolution, dimensional modeling, forecasting, and metric definition from registry extracts.

### Purpose and boundaries

This skill governs analytical modeling performed on data pulled from external registries: public company filings, business licence rolls, professional certification lists, product or device registrations, vehicle or land registers, and similar authoritative-but-uncontrolled sources. The work covers source profiling, entity resolution, conformed modeling, metric definition, model fitting, and validation.

In scope: schema mapping, identifier reconciliation, slowly changing dimensions, cohort and survival framing, rate and count models, anomaly screening, and reproducible reporting.

Out of scope: operating or altering the registry itself, scraping against terms of service, re-identifying individuals in de-identified extracts, producing eligibility or enforcement decisions about named persons without a human owner, and legal conclusions about compliance.

### Inputs and assumptions

Before modeling, collect and record:

1. Source description: publisher, extract date, retrieval method, licence or usage terms, and update cadence.
2. Data dictionary: field definitions as published; note any fields whose meaning is inferred.
3. Analytical question stated as a decision or measurable outcome.
4. Grain: one row represents what (a filing, a licence, a registrant-year)?
5. Known gaps: late filings, retroactive corrections, deregistered records, duplicate issuance.

Assumptions must be written down with an owner and a test that would falsify them. Treat registry status codes as provisional until confirmed against documentation.

### Operating workflow

1. Snapshot the raw extract as received. Store checksum, row count, and extract timestamp. Never overwrite it.
2. Profile each field: null rate, distinct count, format pattern, min/max, and out-of-domain values. Record results as a table.
3. Build the identifier strategy. Prefer the registry's own stable key. Where none exists, resolve entities with normalized name plus jurisdiction plus a secondary attribute, and report the match precision on a labelled sample (target at least 200 pairs, reviewed by two people where feasible).
4. Model time explicitly. Separate event date, effective date, and recorded date. Use validity intervals for status changes rather than overwriting.
5. Define each metric in a single versioned specification: numerator, denominator, population filter, time window, and handling of reversals.
6. Fit the simplest model that answers the question. Use counts with exposure offsets (Poisson or negative binomial) for event rates across unequal registry coverage; use survival framing for time-to-event questions about registration duration.
7. Run the validation set in the verification section before any result leaves the working environment.
8. Publish with the snapshot identifier, code version, and assumption register attached.

### Decision gates

Stop and escalate if any of the following holds:

- Entity match precision on the labelled sample is below 95%, or recall is unknown.
- Null or out-of-domain rate for a key field exceeds 5% and the cause is unexplained.
- The source licence does not clearly permit the intended use.
- The result would be used to make a decision about an identifiable person or entity (approval, denial, sanction, flagging).
- A metric changes definition between extract versions without a documented reason.
- Backtest error exceeds the tolerance agreed in the analytical question, or results are unstable across reasonable window choices (more than 10% relative change).

Proceed only when each gate is passed or a named owner accepts the documented residual risk.

### Verification and evidence

Each deliverable must include:

- Reconciliation: row counts from raw to modeled tables, with every drop explained by a filter.
- Uniqueness test: the declared grain key is unique (zero duplicates) in each conformed table.
- Referential test: every foreign key resolves; report orphan counts.
- Temporal test: no validity interval overlaps for the same entity and attribute; no event precedes its registration date unless flagged as a correction.
- Sensitivity: report the metric under at least two alternative window and filter choices.
- Calibration or fit check: for predictive models, hold out the most recent period and report error against a naive baseline.
- Reproducibility: a fresh run from the snapshot reproduces headline figures exactly.

Mark any statement about current registry rules, field semantics, or library behaviour as requiring verification against the publisher's current official documentation. Do not cite benchmark figures or accuracy claims that were not produced in this work.

### Failure handling

- Checksum mismatch on re-read: halt, quarantine the extract, and request a re-pull.
- Sudden change in volume (beyond three standard deviations of the trailing series): treat as a possible publication change; investigate before modeling.
- Matching failure concentrated in one jurisdiction: segment the match rules for that jurisdiction rather than loosening global thresholds.
- Model fails the naive-baseline comparison: report the baseline result and do not ship the model.
- Unresolvable definition conflict: escalate to the metric owner with both definitions and the affected row count.

### Deliverable contract

A completed engagement delivers:

1. Methodology note (maximum two pages): question, grain, sources, metric specifications, and model choice with justification.
2. Assumption register: each entry with owner, evidence, and falsification test.
3. Data quality report: profiling tables, reconciliation, and the verification results above.
4. Reproducible pipeline and a run manifest recording snapshot ID, code revision, and run timestamp.
5. Results with uncertainty intervals and sensitivity ranges; no point estimates without spread.
6. Open-issues list with severity and owner.

Do not: overwrite raw snapshots; merge entities on name alone; report results without the denominator; present registry status as verified fact without a source date; or perform any deletion, bulk export, external transmission, or publication of record-level data without explicit written approval from the data owner.

### Ultron routing contract

**Choose this skill when:** the data is already available in a usable snapshot or curated dataset and the main question is analytical: entity modeling, metric definition, cohort or survival framing, rate/count modeling, anomaly analysis, statistical validation, or interpretation of registry-derived records.

**Choose `data-pipelines-analytics` when:** the main work is obtaining and moving registry data reliably: API/export extraction, raw landing, normalization, incremental loading, reconciliation, data-quality gates, and pipeline operations.

**Handoff contract:** the pipeline skill supplies immutable source snapshot identifiers, extraction timestamps, schema and grain, raw-to-normalized mappings, entity keys, quality results, missingness, and change/deletion semantics. This skill returns required analytical fields, metric definitions, modeling assumptions, validation requirements, and any data defects that must be fixed upstream. Do not rebuild ingestion logic inside an analysis notebook when a governed pipeline is the actual need.

**Why the boundary exists:** a correct model depends on trustworthy data, but data movement and statistical inference have different failure modes and acceptance tests.


## data-diagrams

**Use when:** Use when designing, implementing, or reviewing data visualizations in a frontend codebase, including chart type selection, data shaping for charts, interactive tooltips and legends, accessibility of graphics, and visual regression checks.

### Purpose and boundaries

Use this skill to turn a dataset and a question into a correct, readable, accessible chart inside a frontend application. It covers chart type selection, data preparation for rendering, component implementation, interaction design, and verification of the rendered output.

Out of scope: statistical modeling, backend query design, dashboard infrastructure, and architecture diagrams (UML, sequence, C4). If the request is primarily about one of those, say so and redirect.

### Inputs and assumptions

Before building, establish:

1. The question the viewer must answer, stated in one sentence.
2. The data shape: field names, types, cardinality, units, time zone for timestamps, null semantics, and expected row counts at p95 load.
3. The rendering target: framework, charting library, and whether output is SVG, canvas, or static image.
4. Constraints: supported browsers, minimum viewport, accessibility target (assume WCAG 2.2 AA unless told otherwise), and performance budget.

If any of these are missing and cannot be read from the repository, ask. Do not guess units or time zones.

Library APIs, option names, and version behavior change. Verify every option you use against the official documentation for the exact version pinned in the project's lockfile.

### Operating workflow

1. **Restate the question.** Write the comparison, trend, distribution, composition, or relationship the chart must show.
2. **Select the encoding.** Apply the decision gates below. Record the chosen chart type and why.
3. **Shape the data.** Write a pure function that converts raw records into the chart's input. Handle nulls explicitly, sort deterministically, aggregate before rendering when rows exceed what the chart can show legibly, and format numbers with the locale in use.
4. **Implement the component.** Keep data transformation separate from rendering. Set explicit axis domains where the data's range is meaningful; do not let a zero baseline be silently dropped for bar charts.
5. **Add semantics.** Provide a text title, a summary sentence stating the key takeaway, and a data table or accessible equivalent for screen readers.
6. **Add interaction only if it serves the question.** Tooltips must show exact values with units. Keyboard focus must reach the same information that hover reveals.
7. **Verify** using the checks below.

### Decision gates

- **Comparison across categories** (up to about 12): horizontal bar, sorted by value. Use vertical bars only for short labels.
- **Change over time** (one or few series): line chart. Use area only when the magnitude of the total matters and the baseline is zero.
- **Part-to-whole**: a stacked bar with at most five segments. Do not use pie or donut charts for more than three slices or for precise comparison.
- **Distribution**: histogram or box plot. State bin width.
- **Relationship between two continuous variables**: scatter plot. Use a log scale only when the data spans several orders of magnitude, and label it.
- **More than about 5,000 points**: aggregate, sample with disclosure, or use canvas rendering. Do not send raw large arrays to SVG.
- **Stop and ask** if the data is categorical with no ordering and the question requires ranking, or if the chart would mislead about causation.

### Verification and evidence

Report each check with its result:

- Rendered output matches the source data for at least three sampled points, including one null and one maximum value.
- Axis units, labels, and scale type are visible and correct.
- Color contrast of data marks and text meets 3:1 for graphics and 4.5:1 for text against background.
- Colors are distinguishable without hue (pattern, shape, or direct labels) and under common color-vision deficiency simulations.
- Keyboard navigation reaches tooltips and legend toggles.
- Chart redraws correctly at 320 px width and at the project's largest supported width.
- Render time for the p95 dataset is measured and within the project's budget. Report the measured number, not an estimate.
- Unit tests cover the data transformation function, including empty input, all-null series, and duplicate timestamps.

Attach screenshots or a test output as evidence. Do not claim a check passed without observing it.

### Failure handling

- **Data does not match the stated question**: report the mismatch and propose the nearest answerable question.
- **Library lacks a needed feature in the pinned version**: check the official changelog for that version before proposing an upgrade. Upgrades require approval.
- **Verification fails**: fix the cause, rerun the failing check, and report both runs. Do not weaken thresholds to pass.
- **Sensitive data appears in the dataset** (personal identifiers, health, financial): stop, do not render it into fixtures or screenshots, and request approval for handling.

### Approval required

Obtain explicit approval before: changing a shared chart library version, altering production data pipelines, committing sample data drawn from real users, publishing dashboards externally, or deleting existing visualizations.

### Deliverable contract

Provide:

1. Chosen chart type with the decision gate that justified it.
2. Files changed, with the transformation function separated from the component.
3. Summary sentence and accessible data alternative as shipped.
4. Verification table: check, method, observed result.
5. Open items, including any library behavior verified only against documentation and not in the running app.

Do not include unverified performance numbers, invented option names, or claims of compliance certification.


## data-modeling

**Use when:** Use when designing, reviewing, or migrating relational or analytical data models, including entity definitions, keys, normalization or dimensional choices, constraints, and schema change plans for databases and data warehouses.

### Purpose and boundaries

This skill produces and reviews data models: entities, attributes, keys, relationships, constraints, and their physical translation for a chosen engine. It covers transactional (OLTP) schemas, analytical (star or snowflake) schemas, and incremental changes to existing schemas.

Out of scope: choosing a database vendor, tuning query plans on production systems, writing ETL orchestration, and designing access control policies. Name these as adjacent work and stop at the model boundary.

### Inputs and assumptions

Collect before modeling. If any item is missing, record it as an assumption with a stated owner:

- Business processes and the questions the model must answer, with example queries.
- Grain: what one row in each table represents.
- Volume estimates, growth rate, and update frequency per entity.
- Source systems and their identifiers, including whether identifiers are reused or mutable.
- Target engine and version. Engine-specific types, index options, and DDL syntax must be checked against current official documentation for that version.
- Regulatory or sensitivity classification of fields (personal, financial, health). Flag these; do not decide retention or masking alone.

### Operating workflow

1. Write the grain statement for every table in one sentence. Reject any table whose grain cannot be stated.
2. List candidate entities from nouns in the business process. Mark each as entity (has independent identity and lifecycle), event (immutable occurrence), or attribute (no independent identity).
3. Assign a primary key per table. Prefer natural keys only when they are stable, unique, and issued by an authority the business trusts; otherwise use a surrogate key and keep the natural key as a unique constraint.
4. Define relationships with cardinality and optionality in both directions. Resolve every many-to-many relationship with an associative table that carries its own attributes and key.
5. Normalize OLTP models to third normal form as the default. Denormalize only under a documented reason (measured read cost, a fixed reporting requirement) and record which columns are derived and how they are refreshed.
6. For analytical models, use a dimensional design: one fact table per business process at a declared grain, conformed dimensions shared across facts, additive measures where possible, and explicit handling for slowly changing attributes (state the type chosen per attribute).
7. Specify constraints in the model, not only in application code: not-null, unique, foreign keys, check constraints for domains and ranges, and allowed-value lists.
8. Map each logical element to physical types for the target engine, recording precision for decimals, time zone semantics for timestamps, and maximum lengths for text.
9. Produce a change plan for any existing schema: additive changes first, backfill in batches, dual-read or dual-write only if the application requires it, and removal of old structures in a separate later release.

### Decision gates

- **Surrogate versus natural key:** use natural keys only if they are immutable and verified unique across all sources. Otherwise use surrogates.
- **Normalize versus denormalize:** denormalize only with a measured or stated read requirement and a named refresh mechanism. Absent both, keep normalized.
- **Slowly changing dimension type:** Type 1 (overwrite) only when history has no business value. Type 2 (versioned rows) when reports must reflect the value at the time of the event. Type 3 only for a single prior value that users explicitly need.
- **Soft versus hard delete:** soft delete requires a documented rule for every query that reads the table. Hard delete requires confirmation that no downstream consumer or audit requirement depends on the row.
- **Schema change type:** if a change drops, renames, or narrows a column or changes its type, it is a breaking change and needs approval from every consuming team before execution.

### Verification and evidence

- Every table has a stated grain, primary key, and at least one documented example row set.
- Every foreign key has a matching parent key, and orphan counts against sample production data are reported as zero or explained.
- Uniqueness claims are tested with a duplicate-count query on representative data; report the query and result.
- Fact tables: confirm the grain by checking that the primary key (or declared composite key) has zero duplicates.
- Each stated business question is answered by a written query against the model. Queries that cannot be written indicate a modeling gap.
- Migration plans include row-count reconciliation and checksum or aggregate comparison between old and new structures before cutover.
- Physical DDL is validated against the target engine version in a non-production environment. State the version tested.

### Failure handling

- If the grain cannot be agreed, stop and escalate to the business owner; do not model around ambiguity.
- If source identifiers collide, do not merge records automatically. Propose a reconciliation key and list collision samples for review.
- If a duplicate-count check fails, halt the design step and identify the upstream cause before revising the key.
- If a proposed change would lock or rewrite a large table, flag the operational risk and request a maintenance window decision.

### Deliverable contract

Return a document containing, in order:

1. Scope statement and assumptions with owners.
2. Entity list with grain, key, and classification for each table.
3. Relationship summary with cardinality and optionality.
4. Constraint list and physical type mapping for the named engine version.
5. Decisions log: each gate decision with rationale and alternatives rejected.
6. Verification results: queries run, row counts, duplicate and orphan checks, and open items.
7. Migration or change plan, if applicable, with rollback steps.

### Safety and approvals

Obtain explicit written approval before: dropping, renaming, or narrowing any production column or table; running any backfill or rewrite against production data; changing keys or constraints on populated tables; and classifying or moving personal, financial, or health data into new structures. Do not execute DDL against shared or production environments. Do not state that a design satisfies a regulation or certification; state only which controls it supports and flag the rest for compliance review.

### What not to do

- Do not model every field from a source system by default; model only what the stated questions and processes require.
- Do not use generic columns such as `data`, `attributes`, or `misc` to avoid design decisions.
- Do not add indexes, partitioning, or engine-specific features without a stated query pattern they serve.
- Do not invent performance figures; report only measured results.


## data-pipelines-analytics

**Use when:** Use when designing, building, validating, or auditing analytics pipelines that ingest, normalize, join, or report on data pulled from external registries (public records, company or product registries, package or model registries, open government datasets).

### Purpose and boundaries

This skill covers analytics pipelines whose source of truth is an external registry: extraction from registry APIs, bulk exports, or scraped public pages; staging; normalization; entity resolution; metric computation; and delivery of analytical outputs.

In scope: source assessment, ingestion design, schema mapping, incremental loads, data quality checks, reconciliation against registry totals, and documented analytical outputs.

Out of scope: writing to or modifying a registry, bypassing access controls or rate limits, re-identifying individuals in personal records, and making legal or compliance determinations on the registry's data. Route those to the appropriate owner.

### Inputs and assumptions

Before work begins, collect:

1. Registry name, operator, and the exact dataset or endpoint version used.
2. Published terms of use, licence, and rate limits. Record the date read.
3. Snapshot or release identifier, and whether the registry publishes change feeds, tombstones, or only full dumps.
4. Intended analytical question and consumers.
5. Target storage location and retention period.

Assumptions must be written down. Treat registry counts as unverified until reconciled. Treat field semantics as unverified until checked against the registry's own documentation.

### Operating workflow

1. **Profile the source.** Pull a bounded sample (for example, one page or one dated slice). Record field names, types, null rates, code lists, and encoding.
2. **Define the grain.** State what one row represents (a filing, a package version, a registration event). Every downstream join depends on this.
3. **Build raw landing.** Store responses unmodified with the request parameters, retrieval timestamp, and HTTP status. Never transform in the landing zone.
4. **Normalize in staging.** Cast types, trim strings, map code lists to a versioned lookup table, and keep the original value beside the normalized one.
5. **Resolve entities.** Use the registry's stable identifiers first. Fuzzy matching only with documented thresholds and a manual review sample.
6. **Load incrementally.** Use the registry's change markers if they exist. Otherwise, use full-snapshot diffs keyed on the natural identifier. Handle deletions explicitly.
7. **Compute metrics** from the staged layer only. Version metric definitions in a file kept alongside the pipeline code.
8. **Reconcile** against any published aggregate totals and record the variance.
9. **Publish** with lineage: source snapshot ID, pipeline version, run timestamp, and row counts per stage.

### Decision gates

For production data movement, require owner sign-off whenever any of these conditions apply:

- Bulk extraction would exceed published rate limits or terms, or the terms are unclear.
- The dataset contains personal data, and the analysis needs fields beyond the minimum required for the question.
- Output will be shared outside the owning team, published, or used to inform decisions affecting individuals or third parties.
- A step deletes or overwrites previously landed snapshots, or changes a published metric definition.
- Any job writes back to the registry or calls a write endpoint.
- Credentials, tokens, or access to restricted registry tiers are required.

Proceed without approval only for read-only sample pulls within published limits and local staging work.

### Verification and evidence

Quality checks must be measurable and recorded per run:

- Row count reconciliation: landed rows equal source-reported rows within a stated tolerance; any gap is explained.
- Key uniqueness: zero duplicate natural keys in the staged grain, or a documented dedupe rule with counts.
- Null and domain checks: null rate and out-of-code-list rate per critical field, compared with the profiling baseline. Flag changes above a set threshold (choose and document one, for example 2 percentage points).
- Referential checks: foreign keys resolve at a stated rate.
- Entity resolution: precision estimated from a reviewed random sample of at least 100 matches or the full set if fewer.
- Idempotence: rerunning the same snapshot produces identical staged output (compare checksums).
- Freshness: retrieval timestamp is within the agreed window.

Mark any version-sensitive detail (API paths, parameter names, rate limit values, schema versions) as "verify against current official documentation" in the run record. Do not assert these from memory.

### Failure handling

- **HTTP errors or throttling:** back off per the registry's guidance, resume from the last committed checkpoint, and never retry in a tight loop.
- **Schema drift:** halt the load, snapshot the new schema, and diff it against the mapping. Do not silently drop or coerce new fields.
- **Reconciliation mismatch above tolerance:** do not publish. Report the delta by stage to locate the loss.
- **Partial snapshot:** mark the run incomplete; never backfill metrics from it.
- **Upstream correction:** re-land affected snapshots and recompute dependent metrics; record the correction in the changelog.

### Deliverable contract

Each completed run delivers:

1. Run manifest: source, snapshot ID, parameters, timestamps, pipeline commit, metric definition version.
2. Stage row counts and reconciliation table.
3. Quality check results with pass/fail against the thresholds stated above.
4. List of open assumptions and unresolved field mismatches.
5. Approval log for any gated action taken.
6. Analytical output with the grain and filters stated in the first paragraph.

Do not present figures without the manifest. Do not describe output as authoritative for the registry; describe it as derived from a named snapshot.

### Ultron routing contract

**Choose this skill when:** the deliverable is a repeatable, auditable flow that retrieves data from an external registry and transforms it into a reliable analytical dataset. It owns extraction, raw preservation, staging, normalization, incremental changes, reconciliation, quality checks, and pipeline delivery.

**Choose `data-analytics-modeling` when:** the dataset is ready and the unresolved work is analytical design or interpretation: choosing a metric, modeling entities and time, estimating rates or trends, validating a statistical model, or explaining results.

**Handoff contract:** publish a dataset contract with source and snapshot digests, row grain, schema version, key strategy, time semantics, quality metrics, known gaps, and refresh cadence. Receive from the modeling skill the required fields, metric definitions, and analytical quality thresholds. Preserve raw data and do not silently change metric meaning in the pipeline.

**Why the boundary exists:** the pipeline is accountable for the lineage and quality of inputs; the modeling skill is accountable for the validity of conclusions drawn from those inputs.

#### Related boundary: general data-platform engineering

For reusable ingestion, transformation, database schema, backfill, indexing, or query-performance work that is not specific to an external registry, route to data-pipelines-and-databases. This skill remains responsible for registry-specific source provenance, extraction permissions and limits, immutable snapshots, registry identifiers, and reconciliation to the publisher's totals.

**Handoff to the general data-platform skill:** provide the source and snapshot contract, extraction timestamp, row grain, field mapping, identifier strategy, data-quality results, correction/deletion semantics, and refresh cadence. Require the general pipeline to preserve those fields and lineage. Return any storage or transformation defects that affect registry reconciliation for this skill to reassess.


## data-pipelines-and-databases

**Use when:** Use when designing, building, debugging, migrating, or reviewing data pipelines, ETL/ELT jobs, warehouse or lakehouse tables, database schemas, or query performance, and when a change could affect data correctness, freshness, lineage, or recoverability.

### Purpose and boundaries

This skill guides work on moving, transforming, storing, and serving structured and semi-structured data: ingestion jobs, transformation logic, schema design and migrations, indexing and query tuning, data quality checks, and operational reliability of pipelines.

In scope: pipeline design, idempotency and backfill strategy, schema and migration review, data contracts, quality tests, reconciliation, query plan analysis, and incident triage for data defects.

Out of scope: model training pipelines (use an ML-specific skill), application UI work, general cloud infrastructure provisioning, and compliance certification. This skill does not certify that a system meets any regulation.

### Inputs and assumptions

Before acting, establish:

1. Source systems, their owners, and update semantics (append-only, mutable, CDC, full snapshot).
2. Target system and engine, with its exact version. Treat engine features as version-sensitive until checked against current official documentation.
3. Freshness requirement, volume (rows and bytes per run), and retention rules.
4. Current schema, row-count and key-uniqueness baselines, and any existing tests.
5. Downstream consumers and the contract they rely on (columns, grain, latency, null semantics).

If any of these is unknown, state the assumption explicitly in the deliverable. Do not guess table names, column types, or engine capabilities.

### Operating workflow

1. **Define the grain.** Write one sentence stating what one row represents and the natural key. Every later check depends on this.
2. **Map lineage.** List each upstream input and each output table. Note which outputs are rebuilt versus incrementally updated.
3. **Choose load semantics.** Prefer deterministic overwrite of a partition or window over row-by-row patching. Require that re-running the same window yields the same result (idempotency).
4. **Specify late and out-of-order data.** Decide a lookback window or reprocessing rule and document what happens to records arriving after it.
5. **Design schema changes as expand-then-contract.** Add nullable columns or new tables first, backfill, switch readers, then remove old structures in a later release.
6. **Write quality checks before transformation code.** Minimum set: primary-key uniqueness, not-null on keys, referential coverage for joins, row-count delta against expected range, and freshness timestamp.
7. **Implement in small, reviewable steps.** One logical change per commit or migration file.
8. **Test on a bounded sample** (for example, one partition or a fixed date range) and compare against a trusted baseline before any full run.
9. **Plan backfill** in ordered windows with checkpoints, resource limits, and a stop condition.
10. **Document operations:** schedule, owner, alert thresholds, rerun procedure, and rollback path.

### Decision gates

Stop and request explicit human approval before:

- Dropping, truncating, or overwriting any table, partition, or dataset outside a disposable staging scope.
- Running a backfill that rewrites more than one partition of production data.
- Changing primary keys, grain, or the meaning of an existing column consumed by others.
- Altering access controls, masking rules, or retention settings.
- Sending data to an external service, third-party API, or any destination outside the approved environment.
- Running a migration that cannot be reversed from a verified backup or snapshot.
- Any action touching personal or otherwise sensitive data beyond what the task already authorized.

Proceed without a gate when work is read-only, runs against a dev or staging copy, or is confined to new objects that no consumer reads yet.

### Verification and evidence

A change is not complete until evidence exists for each item below:

- **Uniqueness:** zero duplicate natural keys in the output for the tested window.
- **Reconciliation:** source-to-target counts or sums match within a stated tolerance, with any difference explained (filters, dedup, late data).
- **Idempotency:** a second run over the same window produces identical row counts and a matching content hash or checksum.
- **Null and type behavior:** nulls and casts verified on at least the edge values present in the sample (empty strings, zero, out-of-range dates, unicode).
- **Query performance:** for changed queries, an execution plan or engine profile before and after, showing scanned volume and join strategy. Report measured numbers only.
- **Migration safety:** migration applied to a copy, rollback or forward-fix path tested, and old readers confirmed compatible.

Do not claim performance improvements, correctness, or compliance without the corresponding measurement. Record the commands run and their outputs.

### Failure handling

- **Count mismatch:** halt downstream publishing, identify the first filter or join where counts diverge, and report the delta with examples.
- **Duplicate keys:** do not silently deduplicate. Determine whether the source is wrong, the join fans out, or the grain was misdefined.
- **Failed backfill window:** stop at the failed window, keep completed windows, and resume from the checkpoint. Never restart from zero without approval.
- **Schema drift at source:** fail fast on unexpected types or missing required columns; quarantine bad records to a separate location with a reason code rather than coercing them.
- **Lock or timeout in production database:** cancel, do not retry in a loop, and reduce batch size or schedule off-peak after review.
- **Unknown root cause:** say so, list the hypotheses tested, and stop rather than applying a speculative fix.

### Deliverable contract

Every deliverable includes:

1. Grain statement and natural key.
2. Lineage summary (inputs, outputs, rebuild or incremental mode).
3. Code or migration artifacts, each with a stated purpose.
4. Quality checks implemented, with thresholds and alert destinations.
5. Verification results: counts, uniqueness, idempotency, and performance measurements with the exact method used.
6. Assumptions and open questions, listed explicitly.
7. Operational notes: schedule, owner, rerun and rollback steps.
8. Pending approvals, if any gate was reached.

What not to do: do not hard-code dates or environment names without parameters; do not use `SELECT *` in production transformations feeding shared tables; do not mix schema changes and data backfills in one unreviewed step; do not hide errors with broad exception handling; do not leave unfinished-work markers or unverified thresholds in delivered artifacts.

### Ultron routing contract

**Choose this skill when:** the task is general data engineering across sources and storage systems: ingestion and transformation pipelines, data contracts, schema changes, database operations, indexing/query plans, backfills, quality checks, and pipeline reliability.

**Choose `data-pipelines-analytics` when:** the source of truth is specifically an external registry and the deliverable is a reproducible analytics dataset with registry-aware extraction, source snapshots, entity resolution, and reconciliation against registry totals.

**Handoff contract:** this skill supplies reusable pipeline and database architecture, storage contracts, migration/backfill controls, and operational reliability. The registry analytics skill supplies source-specific extraction, publisher/usage constraints, registry identifiers, and snapshot reconciliation. Return a normalized data contract before statistical analysis begins.

**Why the boundary exists:** general data engineering provides the platform patterns; registry analytics adds source-specific provenance and reconciliation requirements that should not be generalized away.


## data-sourcing-and-quality

**Use when:** Use when selecting, acquiring, profiling, or validating datasets for analytics, machine learning, or AI evaluation, including assessing source provenance, licensing constraints, schema drift, label quality, and fitness for a stated use.

### Purpose and boundaries

This skill governs how a dataset is chosen, obtained, profiled, and judged fit for a specific use. It covers sourcing decisions, provenance and rights review, profiling, quality measurement, and a written fitness verdict.

In scope: candidate source comparison, acquisition plans, schema and content profiling, label and annotation quality review, leakage and bias screening for training or evaluation splits, and data quality reports.

Out of scope: building production ingestion pipelines (use a pipeline or ETL skill), model architecture choices, and legal opinions. Where licensing or privacy determinations matter, state the open question and route it to the accountable owner. Do not present a legal conclusion as settled.

### Inputs and assumptions

Before acting, confirm these inputs. If any is missing, ask for it or record it as an explicit assumption in the deliverable.

- Intended use: the decision, model, metric, or report the data will support.
- Unit of observation, time range, population, and geography required.
- Candidate sources, with access method and owner.
- Known constraints: license terms, consent basis, retention limits, residency, and sensitivity classification.
- Volume and freshness requirements, and acceptable latency.
- Ground-truth definition, if labels are involved, and who produced them.

Assume nothing about license terms, consent scope, or personal data presence until inspected. Assume a sample is representative only after comparison against the population definition.

### Operating workflow

1. **Restate the use.** Write one sentence stating what the data must support and the error that would matter most (false negatives, stale values, label noise, demographic gaps).
2. **Inventory candidates.** For each source record: origin, owner, collection method, update cadence, license or terms, known exclusions, and retrieval date.
3. **Screen provenance.** Trace each field to its origin. Flag derived fields, scraped content, synthetic data, and fields merged from multiple sources. Mark any source whose terms are unknown as blocked pending review.
4. **Acquire a bounded sample.** Pull a stratified sample sized to test the riskiest strata, not a convenience slice. Record the query, filters, and timestamp so the pull is reproducible.
5. **Profile structure.** Check types, nullability, cardinality, ranges, units, encodings, duplicate keys, and timezone handling. Compare against the documented schema and log every deviation.
6. **Profile content.** Examine distributions by key segments, missingness patterns (MCAR, MAR, or not-at-random where determinable), outliers, and temporal coverage gaps.
7. **Assess labels, if present.** Sample at least 200 labeled items or 5% of the set, whichever is larger, and have a second reviewer relabel them blind. Compute agreement (Cohen's kappa for two raters, Krippendorff's alpha for more) and document the guideline version.
8. **Check splits and leakage.** Confirm train, validation, and test partitions do not share entities, near-duplicates, or post-outcome fields. Split by entity or time where the deployment pattern requires it.
9. **Decide and document.** Produce the verdict per the deliverable contract.

### Decision gates

- **Gate A (rights):** Proceed only if the license, terms, or consent basis permits the stated use, as confirmed by the designated owner. Unknown terms block the source.
- **Gate B (sensitivity):** If personal, health, financial, or minors' data is detected or plausible, stop and obtain explicit approval before any further copying, export, or sharing. Prefer minimized extracts and aggregated views.
- **Gate C (coverage):** Proceed only if the sample covers every stratum the use requires. A stratum with fewer than 30 records is reported as unsupported, not averaged in.
- **Gate D (label reliability):** Labels with agreement below 0.6 kappa (or alpha below 0.67) require guideline revision and relabeling before use in evaluation. For training only, document the noise level and proceed with an explicit risk note.
- **Gate E (leakage):** Any detected train-test overlap above 1% of test records blocks evaluation use until repartitioned.

### Verification and evidence

Each claim in the verdict must cite a reproducible check. Minimum evidence set:

- Row counts, key uniqueness rate, and null rate per required field.
- Schema diff between documented and observed schema.
- Stratum counts against the coverage requirement.
- Agreement statistic and sample size for labels.
- Overlap counts for leakage checks, with method stated.
- Freshness: latest timestamp observed versus required latency.

Thresholds such as null-rate limits or acceptable drift must come from the stated use, not from generic defaults. Where a library, tool, or service behavior is referenced, mark it "verify against current official documentation" unless confirmed in this session.

### Failure handling

- **Schema drift:** Stop profiling, capture the diff, and report whether the change is additive or breaking. Do not coerce types silently.
- **Unexplained missingness above the required limit:** Report the pattern by segment; do not impute to hide it without disclosing the method.
- **Irreproducible pull:** Discard the sample and re-pull with recorded parameters.
- **Conflicting sources:** Keep both, document the disagreement rate, and name which source is authoritative and why.
- **Discovery of sensitive data:** Halt, do not quote values in output, and escalate under Gate B.

### Deliverable contract

Produce a single data fitness report containing:

1. Use statement and error priorities.
2. Source inventory table: source, owner, terms status, retrieval date, verdict.
3. Evidence summary with the metrics listed above and their methods.
4. Assumptions and open questions, each with an owner.
5. Verdict: Fit, Fit with stated limits, or Not fit, with the gate results.
6. Recommended next action with explicit approval requests where Gates A or B applied.

### What not to do

- Do not treat "publicly available" as "licensed for any use."
- Do not report averages over strata that failed coverage.
- Do not relabel a sample without recording guideline version and reviewer identity.
- Do not split data randomly when records share entities or timestamps that leak outcomes.
- Do not write raw sensitive values into reports, logs, or prompts.
- Do not state compliance, accuracy, or legal status as guaranteed.

