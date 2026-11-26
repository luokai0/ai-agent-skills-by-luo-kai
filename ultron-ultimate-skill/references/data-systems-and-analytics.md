# Data Systems, Databases, and Analytics

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

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


## database-operations-and-dr

**Use when:** Use when planning, reviewing, or executing database operations work such as backup and restore design, disaster recovery runbooks, failover and replication checks, RPO/RTO validation, schema migration safety, or database incident recovery.

### Purpose and boundaries

This skill guides database operations (DBOps) and disaster recovery (DR) work for relational and managed database services. It covers: backup and restore design, point-in-time recovery, replication and failover topology, DR runbooks and drills, RPO/RTO measurement, migration rollout safety, and recovery from data-loss or corruption incidents.

It does not cover: application query tuning beyond recovery impact, database engine internals development, data warehouse modeling, or security policy authoring (refer those to the relevant owners). Do not execute production changes from this skill without the approvals defined in Decision gates.

### Inputs and assumptions

Collect before acting:

- Engine, version, and hosting model (self-managed, managed service, or hybrid). Treat exact feature availability as version-sensitive and verify against current vendor documentation.
- Data classification and business-declared RPO (maximum tolerable data loss) and RTO (maximum tolerable downtime) per system. If absent, stop and request them; do not assume.
- Current backup policy, retention period, storage location and region, encryption status, and last successful restore test date.
- Replication topology, failover mechanism, and whether failover is automatic or manual.
- Change window, rollback owner, and on-call contact for the affected service.
- Dependencies: connected applications, batch jobs, replicas consumers, and external integrations that may be affected by writes, failover, or restores.

Assume nothing about backup success. A backup that has not been restored is unverified.

### Operating workflow

1. **Scope the request.** Name the system, environment, data set, and objective (design, drill, migration, incident). Record the RPO and RTO targets being tested.
2. **Inventory protection.** List each backup mechanism (full, incremental, logical export, log archive, snapshot), its schedule, retention, and storage destination. Flag any single-region or single-account dependency.
3. **Map recovery paths.** For each failure mode (instance loss, zone loss, region loss, logical corruption, accidental delete, bad migration), write the recovery path, the data it recovers, and the expected time. Identify the path that needs the least time and the one that needs the most.
4. **Compute achievable RPO/RTO.** RPO is bounded by the newest recoverable log position, not the last snapshot time. RTO includes detection, decision, provisioning, restore, replay, validation, and application reconnection. Show each component with a measured or estimated value and its source.
5. **Design or update the runbook.** Each step needs an owner, a command or console action reference, an expected result, and a stop condition. Keep steps idempotent where possible.
6. **Rehearse.** Restore into an isolated environment, never over production. Time each stage. Compare actual results against targets.
7. **Record evidence and gaps.** Produce the deliverable contract output and open tracked actions for every gap.

For migrations: run expand-then-contract changes; take a verified backup or snapshot immediately before the change; rehearse on a recent restored copy; define the rollback (schema reversal or forward-fix) before execution.

### Decision gates

Stop and obtain explicit written approval from the data owner and on-call lead before any of the following:

- Restoring over, overwriting, or dropping any live database, table, or schema.
- Promoting a replica, forcing failover, or changing replication direction.
- Deleting backups, snapshots, log archives, or retention policies, or shortening retention.
- Running destructive or non-reversible DDL or DML (DROP, TRUNCATE, bulk DELETE/UPDATE without a verified rollback).
- Changing encryption keys, storage locations, or cross-region/cross-account replication (external-impacting).
- Any action that exposes data outside its authorized boundary, including copying production data to a lower environment.
- Any action during an active incident that is not already in the approved runbook.

Proceed without approval only for read-only inspection, restore tests into isolated throwaway environments with no connection to production, and dry-run validation.

### Verification and evidence

A recovery claim is valid only with evidence:

- Restore completed and integrity checks passed (engine consistency checks, row counts or checksums against a known reference for key tables, application smoke test passed against restored data).
- Measured restore duration and recovery point timestamp recorded, compared to RPO and RTO targets. Pass requires measured values at or below targets, with a margin stated.
- Backup jobs show success for the last N scheduled runs, and at least one restore test occurred within the agreed interval (set by the owner; commonly quarterly or per major change).
- Replication lag measured at the time of the check, and failover tested with observed promotion time and no unexpected data divergence.
- Retention and immutability settings confirmed against the stated policy, with the screenshot or configuration export as evidence.

Do not state compliance, durability, or availability guarantees. Describe only what was measured.

### Failure handling

- **Restore fails integrity check:** halt; do not serve the restored copy. Try the previous backup point, record the corruption signature, and escalate.
- **Restore exceeds RTO:** report the measured bottleneck (transfer, replay, index rebuild, provisioning) and propose a specific reduction; do not declare the test passed.
- **Backup job failing silently (no success record):** treat as unprotected from the last success timestamp; alert and compute the exposure window.
- **Failover produces divergence:** freeze writes if safe, capture both positions, and escalate. Do not reconcile manually without data owner approval.
- **Unexpected production impact during a drill:** abort the drill, restore original routing, and file an incident.
- **Missing inputs (RPO, RTO, owner):** report the gap and the plan's limits; do not fill values with defaults.

### Deliverable contract

Every output must contain, in this order:

1. System, environment, and scope statement.
2. Target RPO and RTO with their source.
3. Protection inventory table: mechanism, schedule, retention, location, last verified restore date.
4. Recovery path table: failure mode, procedure reference, measured or estimated RPO, RTO, owner.
5. Test results: measured values against targets, pass/fail per criterion, with evidence references.
6. Approval record for any gated action taken or proposed.
7. Gap register: each gap with severity, owner, and due date.
8. Version-sensitive items flagged for verification against current official documentation.

What not to do: do not restore over production as a test; do not treat snapshot existence as recoverability; do not delete backups to free space without approval; do not copy production data to non-production without approval and masking; do not claim targets were met from estimates alone; do not invent command flags or feature names.

### Ultron routing contract

**Choose this skill when:** the task is database operations and recovery across engines or platforms: backup policy, point-in-time recovery, replication/failover, DR drills, RPO/RTO evidence, corruption response, and safe migration or restoration planning.

**Choose `managed-postgres-hosting` when:** the target is PostgreSQL on a managed provider and the work depends on provider-specific service tiers, supported extensions, connection pooling, parameter limits, managed HA, upgrade windows, or vendor restore semantics.

**Handoff contract:** this skill supplies the recovery objective, data-loss tolerance, backup/replication design, and drill acceptance criteria. The managed-Postgres skill maps those requirements to the provider's supported capabilities and returns service-specific constraints and evidence. Bring provider-specific restore/failover results back here for DR sign-off.

**Why the boundary exists:** recovery principles are portable, but managed database behavior and limitations vary by provider and engine version.


## distributed-service-design

**Use when:** Use when designing, reviewing, or decomposing a distributed service system, choosing service boundaries, communication styles, consistency models, or resilience patterns for multi-service architectures.

### Purpose and boundaries

This skill guides architectural decisions for systems made of multiple independently deployed services that communicate over a network. It covers service decomposition, interface contracts, data ownership, communication style, consistency and failure semantics, and resilience patterns.

In scope: boundary definition, synchronous versus asynchronous interaction, data ownership and cross-service workflows, timeout and retry policy, idempotency, observability requirements, and migration from a monolith or from an existing service mesh of coupled services.

Out of scope: language-level code design, infrastructure provisioning details, vendor selection without stated requirements, and security threat modeling beyond the interface-level controls named below.

### Inputs and assumptions

Collect before recommending anything:

- Business capabilities and the operations that cross them.
- Expected traffic: request rate, fan-out per user action, peak-to-average ratio.
- Latency and availability targets per user-facing operation, stated as numbers.
- Data classes per entity: owner, sensitivity, retention, and required freshness.
- Existing platform constraints: messaging, service discovery, deployment model, observability stack.
- Team topology. Service boundaries that cross team lines create coordination cost; weigh it.

If a target is missing, state the assumption explicitly and label it as such. Do not fill in latency or availability numbers silently.

### Operating workflow

1. **Map capabilities to candidate services.** Group operations that change the same data and are usually performed together. A candidate boundary must have one owner for each piece of state.
2. **Enumerate cross-service operations.** For each user action, list every service call it triggers and whether the caller waits for the result.
3. **Classify each interaction.** Choose synchronous request/response only when the caller needs the answer to proceed. Use events or commands for notifications, fan-out, and work that can complete later.
4. **Define data ownership and consistency.** Assign each entity one writer. For workflows spanning owners, choose between a saga with compensating actions and a single-owner redesign. Specify the consistency level each read path tolerates.
5. **Specify contracts.** For each interface: schema, versioning rule, error taxonomy, idempotency key where writes can be retried, and maximum payload size.
6. **Set resilience parameters.** Per dependency: timeout derived from the parent's budget, retry count with backoff and jitter, circuit-breaker thresholds, and bulkhead limits. Retries only on operations proven idempotent.
7. **Define observability.** Required per-request correlation identifiers, per-dependency latency and error metrics, and the dashboards and alerts that indicate each failure mode.
8. **Plan migration** if replacing existing code: strangler routing, dual-running criteria, and rollback trigger.

### Decision gates

Stop and reassess if any gate fails:

- **Chatty boundary gate:** a single user operation requires more than three synchronous hops in the critical path. Merge services or move work off the path.
- **Shared-write gate:** two services write the same table or entity. Assign a single owner before proceeding.
- **Budget gate:** the sum of worst-case synchronous latencies along the critical path exceeds the user-facing target. Reduce hops, parallelize, or relax the target with stakeholder sign-off.
- **Retry gate:** any retried write lacks an idempotency mechanism. Do not add retries until it exists.
- **Distributed transaction gate:** a proposal requires two-phase commit across independently deployed services. Reject in favor of sagas or redesign.
- **Ownership gate:** no team owns a proposed service's on-call responsibility.

### Verification and evidence

Before sign-off, verify with evidence rather than assertion:

- Trace a representative set of user operations through the design; confirm the critical-path hop count and latency sum against the budget.
- For each write path, demonstrate duplicate delivery produces one effect (idempotency test under replayed requests).
- Inject dependency failure in a test environment: confirm timeouts fire within the budget and the circuit opens at the configured threshold.
- Confirm every cross-service call emits the correlation identifier in logs and traces.
- Check that each saga has a compensation step for every forward step that has external side effects.
- Record measured results with environment, load profile, and date. Do not report estimated numbers as measured.

### Failure handling

- If a latency target cannot be met by the design, present the trade-off options (reduce hops, cache with a stated staleness bound, relax target) and request a decision. Do not choose silently.
- If a dependency's behavior is unknown or version-specific (client libraries, broker delivery guarantees, mesh features), mark it as requiring verification against current official documentation and do not assume the guarantee.
- If a compensation step cannot be defined for an operation, escalate it as a design blocker.
- If ownership is disputed, record both proposals and the criteria that would decide between them.

### Deliverable contract

Produce a design document containing, in order:

1. Scope statement and stated assumptions, with unknowns labeled.
2. Service map with each service's owned entities and owning team.
3. Interaction table: caller, callee, style (sync, async, event), idempotency mechanism, timeout, retry policy.
4. Critical-path latency budget with arithmetic shown.
5. Consistency statement per read path and saga definitions with compensations.
6. Decision gate results, each marked pass or failed with reasoning.
7. Verification plan and any completed evidence.
8. Open risks and items requiring approval.

Do not include: unverified benchmark figures, claimed compliance outcomes, invented library or flag names, or recommendations that bypass a failed gate.

### Approval requirements

Obtain explicit human approval before: deleting or retiring any existing service, data, or endpoint; performing schema migrations on shared stores; changing production traffic routing; altering externally exposed contracts; or any action affecting customers, partners, or regulated data.


## event-architecture-patterns

**Use when:** Use when designing, reviewing, or migrating event-driven backend systems, including event schemas, topic or stream topology, publish/subscribe contracts, outbox and ordering guarantees, idempotent consumers, and event replay or versioning decisions.

### Purpose and boundaries

This skill guides the design and review of asynchronous, event-driven backend communication: what events exist, who produces and consumes them, how they are delivered, ordered, versioned, and recovered. It covers choreography versus orchestration, event notification versus event-carried state transfer, outbox-based publishing, consumer idempotency, dead-letter handling, and schema evolution.

It does not cover: choosing a specific vendor broker for a company without a stated requirement set, tuning cluster infrastructure, general synchronous API design, or frontend event handling.

### Inputs and assumptions

Collect before recommending anything:

- Business events and the state change each one reports (for example, `order.placed`, not `database.row.updated`).
- Producers and consumers, with their owning teams or services.
- Delivery expectations: at-least-once, effectively-once, or best-effort; acceptable duplicate and lag windows.
- Ordering requirements, expressed per aggregate or entity key, not globally.
- Retention and replay needs, and regulatory constraints on personal data in events.
- Current transport and its version. Broker feature availability and client library APIs are version-sensitive; verify against current official documentation before stating any capability.

For unresolved event contracts, record the assumed schema, ownership, and compatibility impact before proceeding.

### Operating workflow

1. Inventory events. List each event name, producer, consumers, and owning aggregate. Reject events named after CRUD operations or table changes unless the domain genuinely is CRUD.
2. Classify each flow: notification (payload carries identifiers only, consumers fetch state), event-carried state transfer (payload carries the fields consumers need), or command-like (intent to act, one intended handler). Command-like messages require explicit ownership of the handler.
3. Define the ordering key. Partition or key by the aggregate ID that needs ordering. Events for different keys should not be assumed ordered.
4. Choose the publication mechanism. For dual writes to a database and a broker, use a transactional outbox written in the same transaction as the state change, with a relay that publishes and marks rows sent. Never publish before commit.
5. Design each consumer: make handling idempotent using a processed-message record keyed by event ID, or by natural keys with conditional writes. Define retry policy with bounded attempts and backoff, then route to a dead-letter destination with the original payload, headers, and failure reason.
6. Version the schema. Additive, optional fields are compatible; renames, removals, and meaning changes are breaking and require a new event type or a versioned schema with a deprecation window.
7. Define replay procedure: which consumers may rebuild projections from history, how side effects are suppressed during replay, and how checkpoints are recorded.
8. Document the topology diagram and the contract for each event in a single reference table.

### Decision gates

Stop and request approval before proceeding when:

- A design requires changing retention, deleting or purging topics, streams, or dead-letter contents, or rewinding consumer offsets in production.
- A migration will dual-publish or cut over producers or consumers that affect live external partners or customers.
- Events contain personal, financial, health, or credential data, or cross a jurisdictional boundary.
- A consumer will perform an irreversible external action (payment, email, shipment, third-party API write) on an event that may be redelivered.

Proceed without approval only for design documents, schema drafts, and changes confined to a non-production environment that the user owns.

Choose orchestration over choreography when a business process has more than three steps with compensating actions, or when a single team needs to observe the full process state.

Choose event-carried state transfer over notification when consumers would otherwise make synchronous calls back to the producer on every event, and the payload size remains reasonable.

### Verification and evidence

Each recommendation must be backed by at least one of: a sequence diagram of a failure case (duplicate delivery, consumer crash mid-handling, out-of-order arrival), a test that injects duplicates and reorders messages, or a reconciliation query comparing producer state to projection state.

Quality checks, all measurable:

- Every event type has exactly one owning producer and a documented schema version.
- 100% of publishing paths use outbox or an equivalent transactional mechanism, verified by code search for direct broker sends inside service methods.
- Every consumer has a documented idempotency key and a test that delivers the same event twice with identical resulting state.
- Dead-letter queues have an alert threshold and an owner.
- Schema compatibility is checked in CI against the previous published version using the registry or tool your team has adopted; confirm its current command syntax from its official documentation.

### Failure handling

- If ordering is violated in testing, check the partition key first, then consumer concurrency settings, before changing application logic.
- If outbox lag grows, inspect relay throughput and locking on the outbox table before adding publisher instances, which can create duplicate sends that consumers must absorb.
- If a poison message blocks a partition, quarantine it to dead-letter after bounded retries; do not skip it silently.
- If a consumer has already performed an external side effect and then failed, record the compensation requirement and escalate instead of retrying blindly.
- If a schema change breaks a consumer in production, roll back the producer change first, then fix the contract.

### Do not

- Do not publish from inside a database transaction before commit.
- Do not treat broker delivery guarantees as application-level exactly-once.
- Do not use wall-clock time as the sole ordering mechanism.
- Do not put secrets or unnecessary personal data in event payloads or headers.
- Do not invent broker configuration values, retention periods, or throughput figures; request them from the operator.

### Deliverable contract

Produce a single document containing:

1. Event catalog table: name, version, producer, consumers, ordering key, delivery semantics, classification.
2. Topology diagram or textual flow for the reviewed scope.
3. Per-consumer idempotency and retry specification.
4. Schema compatibility rules and the deprecation plan for any breaking change.
5. Replay and recovery procedure.
6. Open assumptions list, with each item marked as verified or pending.
7. Approval requests for any gated action, stated as explicit questions.


## event-streaming-kafka

**Use when:** Use when designing, configuring, operating, or debugging Apache Kafka-based event streaming pipelines, including topic design, producer and consumer semantics, schema evolution, consumer lag, retention, and replay.

### Purpose and boundaries

This skill guides backend engineers through design, change, and incident work on Kafka-based event pipelines. It covers topic and partition design, producer delivery settings, consumer group behavior, offset management, schema compatibility, retention and compaction, dead-letter handling, and replay.

Out of scope: general message-queue selection, stream-processing framework internals beyond their Kafka interaction, cluster hardware sizing, and cloud provider billing. Do not use this skill to make compliance or durability guarantees on behalf of a vendor or regulator.

### Inputs and assumptions

Collect before recommending anything:

- Event producers and consumers, with their languages and client libraries and versions.
- Business ordering requirements: which entity must have ordered events (for example, per order ID).
- Delivery expectations: at-least-once is assumed unless the owner states otherwise. Exactly-once claims require evidence of transactional configuration end to end.
- Throughput, message size, and peak-to-average ratio.
- Retention and replay needs, and downstream storage constraints.
- Schema registry in use, and its compatibility mode.
- Current cluster version and managed or self-hosted status.

Assumptions must be stated explicitly. Exact configuration key names, default values, and client API signatures change across Kafka and client releases. Mark every version-sensitive detail as "verify against current official documentation for your version" rather than asserting it from memory.

### Operating workflow

1. **Define the event contract.** Name the topic by domain and event type. Record key, value schema, owner, and consumers. Events describe facts that already happened; commands belong elsewhere.
2. **Choose the key.** The key determines partition routing and therefore ordering. Use the entity ID whose ordering matters. A key with very few distinct values or heavy skew creates hot partitions.
3. **Size partitions.** Derive count from target parallelism (consumers in the largest group) and peak throughput per partition under measured load. Partition count can be increased later but this changes key-to-partition mapping; plan for it.
4. **Configure producers.** Set acknowledgment to all replicas, enable idempotence, and bound retries with a delivery timeout. Batch and compress deliberately; measure before tuning linger and batch size.
5. **Configure consumers.** Commit offsets only after the side effect is durable. Make handlers idempotent using an event ID or natural key stored with the effect.
6. **Plan failure paths.** Define retry topics with bounded attempts and backoff, and a dead-letter topic that carries original metadata, error class, and attempt count.
7. **Set retention and compaction.** Use time or size retention for event streams. Use compaction only for entity-state topics where the latest value per key is the truth.
8. **Document replay procedure** including target offsets or timestamps, consumer group handling, and idempotency assumptions.

### Decision gates

- **Ordering:** If strict ordering across keys is required, stop and reassess. Kafka guarantees order only within a partition. Global ordering implies a single partition and a throughput ceiling.
- **Exactly-once:** Proceed only if producer transactions, consumer isolation level, and sink idempotency are all confirmed. Otherwise design for at-least-once with deduplication.
- **Schema change:** Backward-compatible changes (adding optional fields with defaults) may proceed with registry validation. Removing fields, renaming, or changing types requires a new topic version and a migration plan.
- **Partition increase:** Requires explicit approval, a key-remapping impact note, and confirmation that consumers tolerate reordering during the transition.
- **Retention reduction or topic deletion:** Requires explicit approval. Deletion is irreversible and can destroy the replay source.
- **Replay into production consumers:** Requires explicit approval, a dry run on a non-production consumer group, and a rollback owner.
- **Offset reset on a live group:** Requires explicit approval and a documented expected duplicate or skip count.

### Verification and evidence

Each change must produce:

- Schema registry compatibility check result for the target subject.
- Test showing a redelivered event produces no duplicate side effect (target: zero duplicate effects across a replay test of at least one full partition's recent events).
- Consumer lag before, during, and after the change, measured per group and partition, with recovery to baseline within the agreed window.
- Under-replicated partition count and producer error rate during a broker restart drill in a non-production environment.
- For key changes or partition increases: a sample of 1,000 keys showing mapping before and after, and proof that per-key ordering consumers were updated or drained.

Do not report numeric benchmark results without a recorded run.

### Failure handling

- **Rising lag:** Check consumer throughput, rebalance frequency, poison messages, and downstream latency in that order. Do not simply add consumers beyond partition count; extra consumers sit idle.
- **Repeated rebalances:** Inspect session timeout versus processing time per poll. Long handlers must be moved off the poll thread or the poll interval adjusted per current client documentation.
- **Poison message:** Route to dead-letter after bounded retries. Never skip silently and never block the partition indefinitely.
- **Duplicate side effects:** Confirm the deduplication key is written atomically with the effect. Investigate commit ordering before changing producer settings.
- **Out-of-order events after a partition change:** Halt the affected consumers, drain, and reprocess from a defined point under approval.

### Deliverable contract

Deliver a single design or change record containing:

1. Topic name, key, partition count with rationale, retention or compaction setting.
2. Schema subject, compatibility mode, and change type.
3. Producer and consumer delivery configuration with version-verification notes.
4. Idempotency mechanism and its storage location.
5. Retry and dead-letter topology.
6. Verification results from the checklist above, with raw evidence attached.
7. Approval log for every gated action, with approver and timestamp.
8. Rollback steps and their owner.

### What not to do

- Do not claim exactly-once delivery from configuration alone.
- Do not increase partitions or change keys without the impact note.
- Do not use auto-commit with handlers that have external side effects.
- Do not delete topics, purge data, or reset offsets on production groups without approval.
- Do not place sensitive personal data in event payloads or keys without an approved classification and encryption plan.
- Do not invent configuration names, flags, or versions; verify them.


## managed-postgres-hosting

**Use when:** Use when selecting, provisioning, configuring, migrating to, or operating PostgreSQL on a managed cloud or vendor service, including instance sizing, high availability, backups and point-in-time recovery, connection pooling, extensions, upgrades, and cost or access-control review.

### Purpose and boundaries

This skill guides an agent through decisions and work for PostgreSQL running on a managed service (a cloud provider's database offering or a vendor platform). The provider operates the host OS, storage, and base engine; the team still owns schema, queries, roles, data retention, and recovery readiness.

In scope: vendor/tier selection, sizing, networking and private access, HA and failover design, backup and restore validation, pooling, parameter tuning within vendor limits, extension availability, major and minor upgrades, migration cutover planning, and cost review.

Out of scope: self-managed Postgres on VMs or Kubernetes operators (use a separate skill), application ORM design, and data warehouse engines.

### Inputs and assumptions

Collect before acting:
- Engine major version currently in use and target version.
- Workload profile: read/write ratio, peak connections, p95 query latency target, data size and monthly growth, largest tables.
- Recovery objectives: RPO and RTO stated in minutes, plus the retention period required by policy.
- Required extensions and whether each is available on the candidate service.
- Network model: public endpoint allowed or not, peering or private link requirements, client locations.
- Data classification of stored data (personal, financial, regulated). Do not assume a compliance certification applies; confirm it from vendor documentation.

If any of these are missing, record the assumption explicitly in the plan and flag it for the approver.

### Operating workflow

1. **Inventory current state.** Capture version, extensions, parameter overrides, connection counts (peak and steady), replication topology, backup schedule, and top 20 queries by total time from existing statistics.
2. **Map requirements to tier.** Compare CPU, memory, storage IOPS and throughput, max connections, and HA options against measured peaks with at least 40% headroom. Use vendor pricing and limits pages, verified on the day of decision.
3. **Design networking.** Prefer private connectivity. Restrict allowed source ranges to known egress points. Enforce TLS with certificate verification for all clients.
4. **Design pooling.** If peak client connections exceed what the instance supports comfortably, place a pooler in transaction mode in front of the database. Note that transaction pooling breaks session-level features (session `SET`, advisory session locks, prepared statements unless the pooler supports them). Verify application compatibility before cutover.
5. **Plan recovery.** Enable automated backups and point-in-time recovery. Document the restore path. Schedule a restore into a separate instance and run row-count and checksum comparisons against a known table set.
6. **Plan migration (if applicable).** Use logical replication or the vendor's managed migration tooling for near-zero-downtime moves; use dump and restore for small databases with an agreed maintenance window. Rehearse on a copy at production size.
7. **Stage and cut over.** Lower DNS TTL in advance, freeze schema changes, confirm replication lag is near zero, switch connection strings through a single config mechanism, and keep the source read-only for a fallback window.
8. **Operate.** Monitor replication lag, bloat, autovacuum activity, connection saturation, storage growth, and slow query rates. Review monthly.

### Decision gates

Stop and obtain explicit approval before:
- Deleting, downsizing, or detaching any instance, replica, backup, or snapshot.
- Changing retention periods in a way that shortens recoverability.
- Making a database publicly reachable or widening an allowlist to broad ranges.
- Performing a major version upgrade or any cutover that redirects production traffic.
- Enabling an extension that requires superuser-equivalent rights or that the vendor marks as restricted.
- Creating or rotating credentials that other systems depend on.
- Incurring recurring spend above the approved budget, or accepting a commitment term.
- Sharing data outside the approved environment, including to vendor support.

Proceed without approval only for read-only inspection, metrics queries, and dry-run plans.

### Verification and evidence

- **Restore test:** a restore completes within the stated RTO, and sampled tables match source row counts and aggregate checksums (for example, a sum over a numeric key plus a count per partition).
- **Failover test:** in a non-production environment, forced failover completes within target time, and the application reconnects without manual intervention. Record observed downtime.
- **Performance:** p95 latency on the top 20 queries is within 10% of baseline after migration, or differences are explained.
- **Capacity:** peak CPU under 70%, connection utilization under 75% of limit, storage projected to remain under 80% for six months.
- **Config drift:** parameters differ from the documented baseline only where justified in the change record.
- **Access:** every role has a named owner; no shared superuser login is used by applications.

Store evidence (command output, metrics screenshots exported as data, restore logs) with the change ticket.

### Failure handling

- **Replication lag grows during migration:** pause non-essential batch writes, check for long-running transactions and large unindexed updates, and do not cut over until lag is stable at near zero for at least 15 minutes.
- **Restore checksum mismatch:** halt, identify the first mismatched table, and check whether source writes occurred after the restore point before assuming corruption.
- **Connection exhaustion:** identify the client pools responsible, reduce pool sizes, and add a pooler before resizing. Resizing is a gated action.
- **Pooler incompatibility:** revert the affected service to direct connections and file the specific feature dependency.
- **Vendor limit reached (IOPS, storage, connections):** report the limit and the observed value; do not work around it by disabling safeguards.
- **Unexpected behavior from documentation:** treat the live service as authoritative and record the discrepancy.

### Deliverable contract

Every engagement returns:
1. A requirements summary with stated assumptions and open questions.
2. A tier and configuration recommendation with the sizing calculation shown.
3. An ordered runbook with rollback steps for each stage.
4. Gate list: each approval required, the requester, and the status.
5. Evidence bundle: restore test results, failover results, performance comparison, and capacity projection.
6. Version-sensitive items list: any vendor limit, parameter name, extension version, or pricing figure that must be re-checked against current official documentation before execution.

### Ultron routing contract

**Choose this skill when:** the database is managed PostgreSQL and the task depends on provider-specific choices or operations: tier/sizing, networking, extensions, pooling, parameters, HA/failover, backup/restore, upgrades, migration cutover, or cost.

**Choose `database-operations-and-dr` when:** the central objective is cross-engine or organization-wide recovery strategy, RPO/RTO design, DR governance, corruption response, or recovery drill acceptance.

**Handoff contract:** receive the required RPO/RTO, data integrity expectations, failover posture, retention, and recovery drill plan. Return the provider's actual backup/PITR limits, restore procedure, failover behavior, extension and version constraints, and measured recovery evidence. Never assume a managed-service backup feature is equivalent to a tested recovery plan.

**Why the boundary exists:** managed PostgreSQL operations require provider-specific expertise, while DR governance must remain consistent across all database platforms.


## nosql-search-cache

**Use when:** Use when designing, reviewing, or troubleshooting NoSQL document/key-value stores used for search indexes, query result caches, or cache-aside layers, including TTL, invalidation, index sizing, and consistency tradeoffs.

### Purpose and boundaries

This skill guides work on three coupled concerns: (1) NoSQL stores used as primary search or secondary indexes, (2) caches of query results or derived documents sitting in front of a system of record, and (3) the invalidation and expiry logic that keeps (1) and (2) correct.

In scope: data modeling for lookup keys, index field selection, cache key design, TTL and eviction policy, invalidation strategy, staleness budgets, memory sizing, and load/consistency verification.

Out of scope: choosing a vendor from scratch, relational schema design unless it feeds the cache, full-text relevance tuning, and infrastructure provisioning. Route those to their own skills.

### Inputs and assumptions

Collect before proposing changes:
- Read/write ratio and query shapes (top 20 queries by frequency and latency).
- Source of truth and where writes land.
- Acceptable staleness per data class, in seconds, stated by the product owner.
- Current item size distribution (p50, p95, max) and working-set size.
- Store product and version, and cache product and version.
- Current TTLs, eviction policy, and hit ratio.

If any of these is missing, state the assumption explicitly and mark the output as provisional. Do not assume a specific product's feature flags, index types, or eviction names; verify them against current official documentation for the exact version in use.

### Operating workflow

1. **Classify each query and cache entry.** Label each as: exact-key lookup, filtered search, range scan, aggregation, or derived view. Record its staleness budget.
2. **Derive keys from the query, not the entity.** A cache key must include every parameter that changes the result: filters, sort, pagination cursor, locale, tenant, and permission scope. Omitting permission scope is a common data-leak defect.
3. **Choose the invalidation pattern per class:**
   - Time-bounded staleness: TTL only, with TTL set to the staleness budget.
   - Write-driven correctness: explicit invalidation or versioned keys (embed a version number from the source row, so stale entries are never read).
   - Search indexes: asynchronous reindex from a change stream or outbox, with a lag metric.
4. **Size the index and cache.** Estimate memory as items × (average size + per-entry overhead). Overhead varies by product; measure it in a staging copy rather than assuming a figure.
5. **Set TTL with jitter** for bulk-loaded entries to avoid synchronized expiry stampedes.
6. **Guard against stampedes.** Use single-flight loading (one request recomputes, others wait or receive a stale value) for hot keys.
7. **Write the rollout plan** with dual-read comparison before cutover.

### Decision gates

- **Gate A, staleness:** If the product owner cannot state a staleness budget, stop. Do not default to "as fresh as possible."
- **Gate B, correctness:** If a cached value gates money movement, access control, or inventory allocation, it must not be served from cache without a write-time or read-time version check. Require explicit sign-off.
- **Gate C, permission scope:** If any cached result varies by user or role, the key must include the scope or the value must be post-filtered. Reject shared keys otherwise.
- **Gate D, memory:** If projected working set exceeds 70% of allotted memory, require an eviction-impact analysis before going live.
- **Gate E, destructive operations:** Flushing caches, dropping or rebuilding indexes, changing key formats in production, and bulk deletes all require explicit written approval from the data owner, with a rollback path and a stated blast radius.
- **Gate F, external impact:** Changes that alter responses served to external customers or partners require approval and a canary plan.

### Verification and evidence

Measure before and after; record numbers, not impressions:
- Cache hit ratio per query class (target set by the owner; flag any drop greater than 5 points after deploy).
- Staleness observed: compare cached values to source at sampled intervals; the 99th percentile must be within the budget.
- Index lag: time from source commit to searchable visibility, reported as p95 and p99.
- Latency at p50/p95/p99 with cache on and off for the top queries.
- Stampede check: request count to the origin during forced expiry of a hot key in staging; it should approximate one recomputation.
- Correctness diff: shadow-read results for a sample of queries, reporting mismatch rate and root causes.

Any benchmark figure must come from your own measurement in your environment. Do not cite external numbers as expected performance.

### Failure handling

- **Hit ratio collapse:** Check key cardinality changes first (a new parameter in the key), then TTL changes, then eviction pressure.
- **Stale reads reported:** Confirm whether invalidation fired. Check outbox or change-stream lag before changing TTLs.
- **Memory eviction of hot keys:** Do not raise memory blindly; reduce entry size, split large documents, or narrow cached fields.
- **Cross-tenant data appearing:** Treat as a security incident. Disable the cache layer for the affected query class, notify the owner, and do not resume without approval.
- **Index rebuild failure:** Keep the old index serving; never drop it before the new one is verified.

### Deliverable contract

Return:
1. A query-class table: class, example query, key template, invalidation pattern, staleness budget, owner.
2. Key and TTL specification with jitter values and eviction policy as configured.
3. Memory estimate with stated assumptions and measurement method.
4. Verification results using the metrics above, with raw numbers and sample size.
5. Open approvals list: each gated action, approver, status.
6. Rollback procedure with a tested trigger condition.

Mark every product-specific setting as "verify against current official docs for version X." Do not present unverified settings as final.


## postgres-performance-cost

**Use when:** Use when diagnosing PostgreSQL query latency, throughput, or infrastructure cost problems, or when evaluating schema, index, configuration, or capacity changes whose performance and cost impact must be measured before rollout.

### Purpose and boundaries

This skill guides evidence-based analysis of PostgreSQL performance and its cost footprint. It covers query plan analysis, index design trade-offs, configuration review for memory and I/O, write-amplification and bloat assessment, connection pressure, and right-sizing of compute and storage against measured workload.

It does not cover: application architecture redesign, choosing a different database engine, managed-provider billing negotiation, security hardening, or backup/restore design. Route those to the appropriate skill.

### Inputs and assumptions

Collect before recommending anything:

- PostgreSQL major and minor version, hosting type (self-managed, managed service, container), and instance class with storage type.
- The exact slow statements (normalized text plus one representative bound example), frequency, and the business path they serve.
- Output of `EXPLAIN (ANALYZE, BUFFERS)` on a representative dataset, or a clear reason it cannot be run in the target environment.
- Statistics snapshots from the statistics views (`pg_stat_statements` if enabled, table and index usage counters), with the reset timestamp.
- Current values of memory, parallelism, WAL, checkpoint, and autovacuum settings, and whether they were changed from defaults.
- Table sizes, row counts, growth rate, and write-to-read ratio.
- Cost data: monthly compute, storage (provisioned and used), I/O, and backup charges, with the billing period.

Assumptions must be stated explicitly. If the data came from a non-production copy, say so and state how statistics may differ.

### Operating workflow

1. Establish a baseline. Record p50, p95, and p99 latency and calls per minute for the top statements over a representative window. Note cache hit ratio and temp file usage.
2. Rank cost drivers. Multiply average time by call count to find total time consumed. Optimize the largest share first, not the single slowest query.
3. Read the plan. Compare estimated and actual row counts. A misestimate above roughly an order of magnitude is a statistics or correlation signal. Check for sequential scans on large tables, nested loops over large inputs, sorts or hashes spilling to disk, and repeated subplans.
4. Classify the root cause: missing or unusable index, stale statistics, poor join order from correlated columns, query shape, lock waits, bloat, memory misconfiguration, or undersized hardware.
5. Form one hypothesis per change. Write the expected effect as a measurable delta (for example, "buffers read drops substantially for the plan node on the orders table").
6. Test in a staging environment with comparable data volume and the same version and settings. Repeat runs to observe variance; discard cold-cache outliers unless cold-start behavior matters.
7. Quantify the trade-off. An index speeds reads but adds write cost, storage, and vacuum work. Measure write latency and table size before and after.
8. Prepare rollout and rollback steps, then request approval.

### Decision gates

- Adding an index: proceed only if the statement's total time share justifies it, the index serves multiple queries or a critical one, and write-path impact on the table is measured. Prefer a partial or covering index when the predicate or column set is narrow. Index creation on large live tables requires an approach that avoids long locks; confirm the concurrent build option and its limitations against current documentation before use.
- Changing configuration parameters: proceed only with a stated reason tied to observed metrics (for example, temp file spills indicating insufficient work memory for specific sessions). Change one parameter group at a time. Do not tune memory parameters by percentage rules alone.
- Rightsizing instance or storage: proceed only with at least one full business cycle of utilization data showing sustained headroom. Reducing capacity is a production-impacting change and requires approval.
- Statistics or vacuum tuning: proceed only after confirming dead tuple counts and last analyze times. Per-table settings are preferred over global changes.
- Any destructive action (dropping indexes or tables, resetting statistics, terminating sessions, deleting data, changing replication or failover settings) requires explicit written approval from the data owner.

### Verification and evidence

A recommendation is complete only when it includes:

- Before and after `EXPLAIN (ANALYZE, BUFFERS)` output for the target statement, with identical parameters and data state.
- Latency distribution and call rate before and after, over comparable windows.
- Write-side measurements for any index or trigger change: insert/update latency and index size growth.
- Projected cost delta, shown as a calculation from measured inputs, labeled as an estimate.
- A list of settings and versions verified against current official PostgreSQL documentation, and any provider-specific behavior that was not verified.

Reject claims such as "should be faster" without a measured or reproducible result.

### Failure handling

- If the plan changes but latency does not improve, re-check whether the statement is the real bottleneck; look at lock waits and client-side time.
- If staging results diverge from production, identify data skew, cache state, or settings drift before drawing conclusions.
- If statistics appear missing, do not reset them without approval; document the gap and collect a fresh window.
- If a change regresses write throughput beyond the agreed threshold, roll back and report the measured regression.
- If required data is unavailable, state which conclusions are blocked and what data would unblock them. Do not fill gaps with typical values.

### Deliverable contract

Produce a single report containing:

1. Summary: the top problem, its share of total database time or cost, and the recommended action.
2. Evidence table: statement, calls, mean and p95 latency, buffers, plan signature, before and after.
3. Proposed changes, ordered by expected impact, each with rationale, risk, rollback step, and approval status.
4. Cost impact: measured inputs, calculation method, and an explicit estimate label.
5. Open questions and unverified items, including version-sensitive details pending documentation check.

Do not: recommend changes based on generic rules of thumb, apply production changes without approval, drop or rebuild objects without a rollback plan, or present estimates as measured results.


## realtime-websocket-channels

**Use when:** Use when designing, implementing, debugging, or reviewing server-side realtime WebSocket channels, including connection lifecycle, authentication on upgrade, room or topic fan-out, backpressure, heartbeats, reconnection, and horizontal scaling across instances.

### Purpose and boundaries

This skill covers the server side of bidirectional, long-lived channels: the upgrade handshake, session state, subscription and fan-out logic, message schemas, flow control, liveness detection, graceful shutdown, and multi-instance delivery. It also covers the client contract the server must honor (reconnect, resume, idempotent handling).

Out of scope: browser UI rendering, one-shot HTTP APIs (use a request/response skill), WebRTC media transport, and choosing a cloud vendor. Do not design a channel when a polling endpoint or server-sent events satisfy the requirement with less operational risk; state the reason if you choose WebSockets.

### Inputs and assumptions

Collect before designing:

- Message rate per connection (msgs/sec, p99 size) and fan-out ratio (one message to N subscribers).
- Concurrency target (concurrent sockets per instance and cluster-wide) and delivery semantics required: at-most-once, at-least-once with dedupe, or ordered per channel.
- Auth model: token type, where it is issued, expiry, and revocation requirements.
- Deployment: reverse proxy or load balancer in front, idle timeouts on each hop, whether sticky sessions are available.
- Data sensitivity of channel payloads.

If any of these is unknown, state the assumption explicitly in the design document and mark it as unverified. Library names, frame options, and timeout defaults change between versions; verify every such detail against current official documentation for the exact runtime version in use before relying on it.

### Operating workflow

1. **Define the channel model.** Write each channel type as: name pattern, who may subscribe, who may publish, message types, and ordering guarantee. Example: `orders:{tenantId}` readable by tenant members with role `ops`, publish-only from server, per-key ordering by `orderId`.
2. **Authenticate on upgrade.** Validate credentials during the HTTP upgrade request, before accepting the socket. Reject with the proper HTTP status. Do not accept first and authorize later. Re-check authorization on every subscribe; never trust a channel name from the client.
3. **Specify the envelope.** Every frame carries `type`, `channel`, `id` (unique per message), `seq` (per channel, monotonic), and `payload`. Validate inbound frames against a schema and reject oversized frames at the parser, not after decoding.
4. **Implement subscription state.** Keep a per-connection set of subscribed channels and a server-side index from channel to connections. Remove all index entries on close, error, and timeout.
5. **Bound outbound memory.** Each connection gets a bounded send queue. When it fills, apply the policy chosen in the decision gate below. Never let an unbounded buffer grow per slow client.
6. **Add liveness.** Use protocol-level ping/pong or an application heartbeat at an interval shorter than the shortest idle timeout on the path. Close sockets that miss a configured number of heartbeats.
7. **Support resume.** Clients send the last `seq` they processed per channel; server replays from a bounded buffer or instructs the client to refetch state via HTTP snapshot.
8. **Plan multi-instance fan-out.** Route publishes through a shared bus or pub/sub layer; each instance delivers only to its local sockets. Include instance ID in logs.
9. **Shut down gracefully.** On termination signal, stop accepting upgrades, send a close frame with a reconnect hint, drain queues with a deadline, then exit.

### Decision gates

- **Slow consumer policy:** Drop oldest for lossy telemetry; disconnect with a close code for state streams where clients can resnapshot; block publisher only for internal, trusted pipelines with a short timeout. Pick one per channel type and document it.
- **Ordering:** Guarantee order only per channel key. Global ordering across channels requires a single sequencer and is usually not worth its throughput cost.
- **Delivery:** At-least-once requires client-side dedupe on `id`. Exactly-once is not achievable end to end over a socket; do not promise it.
- **Sticky sessions:** Required only if resume state lives in instance memory. Prefer externalized resume buffers so sticky routing is not a correctness dependency.
- **Auth expiry:** If tokens expire during a session, either close at expiry with a specific code or re-authenticate via an in-band message. Never let an expired credential keep receiving data.

### Verification and evidence

Provide evidence for each claim:

- Load test with the target concurrency and fan-out ratio; report p50/p99 delivery latency, memory per connection, and dropped-message counts. Record the hardware and test tool version. Do not report numbers you did not measure.
- Fault injection: kill an instance mid-stream, sever a connection without close frame, stall a consumer. Confirm sockets are released, index entries removed, and resume behaves per design.
- Authorization tests: unauthenticated upgrade, subscribe to a forbidden channel, publish from a client role without permission, token expiry during session.
- Frame fuzzing: oversized frames, malformed JSON, unknown types, out-of-order `seq`. Confirm no crash and bounded resource use.
- Check that idle timeouts on proxies exceed heartbeat interval, verified by configuration inspection and a test that holds an idle socket past the proxy timeout.

### Failure handling

- **Queue overflow:** Apply the documented slow-consumer policy, increment a metric, log channel and connection ID. Do not silently drop without a counter.
- **Bus outage:** Mark instance degraded, stop accepting new subscriptions if correctness depends on them, and surface the condition through health checks.
- **Resume gap:** If requested `seq` is older than the buffer, return a gap signal and require an HTTP snapshot. Never fabricate missing messages.
- **Auth failure mid-session:** Close with the defined code; do not retry server-side.
- **Repeated reconnect storms:** Ensure server returns retry hints with jitter guidance; do not rely on clients behaving.

### Deliverable contract

Produce a design or change record containing:

1. Channel catalog table: name pattern, subscribe rule, publish rule, ordering, delivery semantics, slow-consumer policy.
2. Envelope schema and close-code table with meanings.
3. Lifecycle diagram covering upgrade, auth, subscribe, heartbeat, close, and shutdown.
4. Capacity assumptions and measured results, labeled measured versus estimated.
5. List of version-sensitive settings with the documentation source checked and date.
6. Open risks and unverified assumptions, each with an owner.

Do not approve a channel for production until the authorization tests, fault injection, and proxy-timeout check pass, and a human owner has signed off on any change touching authentication, data exposure, or tenant isolation. Do not deploy load-balancer or proxy timeout changes, or run load tests against shared environments, without explicit approval.


## sql-and-data-performance

**Use when:** Use when diagnosing, writing, or reviewing SQL queries, schema indexes, or data-processing jobs where latency, cost, lock contention, or throughput must be measured and improved without changing query results.

### Purpose and boundaries

This skill covers making SQL and set-based data workloads faster or cheaper while preserving semantic correctness. It applies to relational engines (PostgreSQL, MySQL, SQL Server, Oracle, and similar), analytical warehouses, and SQL-driven ETL. It does not cover application-level caching design, hardware procurement, or general data modeling decisions unless they directly block a query fix. Engine-specific syntax, planner behavior, and configuration parameters change between versions; treat any specific option named during analysis as requiring verification against current official documentation for the exact engine version in use.

### Inputs and assumptions

Before changing anything, collect:

1. The exact query text, parameter sample values, and the engine and version.
2. Table row counts, column types, existing indexes, partitioning, and statistics freshness.
3. The execution plan actual-versus-estimated output, captured with runtime statistics where the engine supports it.
4. The target: p95 latency, daily cost, rows scanned, or lock wait budget.
5. Production constraints: read-only access, change windows, replication lag tolerance.

If any of these are missing, state the assumption explicitly in your output. Do not assume a plan is representative from a development database with different cardinality.

### Operating workflow

1. **Establish a baseline.** Run the query three times under comparable conditions and record median runtime, rows read, rows returned, and memory or bytes scanned.
2. **Verify correctness first.** Save the current result as a reference, using a checksum over ordered output or an aggregate comparison, so every candidate rewrite can be checked against it.
3. **Read the plan top-down.** Find the operator with the largest actual cost or largest gap between estimated and actual row counts. A misestimate above roughly an order of magnitude usually points to stale statistics, skewed data, or predicates that hide selectivity from the planner.
4. **Classify the bottleneck.** Choose one: full scan on a selective predicate, non-sargable filter (functions or implicit casts on indexed columns), join order or join type problem, sort or spill to disk, repeated subquery execution, excessive round trips, lock contention, or over-fetching of columns and rows.
5. **Apply one change at a time.** Change one variable per experiment so the effect is attributable.
6. **Re-measure and re-verify.** Compare against the baseline and the reference result.

### Decision gates

- **Index additions:** Add an index only when the query runs frequently enough that its write overhead is justified, and when the proposed key order matches equality predicates before range predicates. Estimate write amplification on the affected table.
- **Rewriting predicates:** Rewrite a function-wrapped predicate into a sargable form only when the rewrite is provably equivalent for the column's type, collation, and nullability. Confirm with the reference result on edge values including NULL, empty strings, and boundary dates.
- **Denormalization or materialized results:** Propose only when the refresh cadence and staleness tolerance are documented by the data owner.
- **Changes touching production:** Any DDL, index creation, statistics refresh, or job schedule change requires explicit approval from the data owner. Index builds on large tables can block writes or consume I/O; request approval with the expected duration and the chosen online or concurrent build option, verified against engine documentation.
- **Stop condition:** If the best candidate improves runtime by less than the measured run-to-run variance, do not ship it.

### Verification and evidence

Every claim of improvement must cite:

- Baseline and candidate median runtimes over at least three runs, with the variance range.
- Rows read and rows returned before and after.
- The plan diff showing which operator changed.
- A result equality check that passed on the reference parameter set and at least one additional parameter set with different selectivity.

Do not report percentage gains without absolute numbers. Do not state benchmark outcomes for an engine or dataset you did not measure.

### Failure handling

- **Result mismatch:** Discard the candidate immediately. Do not patch around it by adding DISTINCT or ORDER BY without understanding the cause.
- **Plan regression on other parameters:** Parameter-sensitive plans are common. Report the regression with the parameter values that trigger it and propose either a parameter-specific approach or accept the trade-off explicitly.
- **Statistics or plan cache confusion:** Confirm whether the plan was recompiled before concluding that a change worked.
- **Measurements disagree:** Check for cache warm-up, concurrent load, and differing session settings before trusting the result.

### Deliverable contract

Return a report containing, in order:

1. Summary: the bottleneck class, the change made, and the measured effect with absolute numbers.
2. Baseline and candidate tables: runtime, rows read, rows returned, and memory or spill data.
3. The final query or DDL, marked as proposed until approved.
4. Verification results: equality checks and parameter coverage.
5. Risks: write overhead, lock impact, version-sensitive behavior to confirm, and rollback steps.
6. Open items: assumptions not yet validated and approvals still required.

Do not include unmeasured speedup estimates, do not recommend production DDL without the approval gate above, and do not claim the change is safe for all parameter values unless those values were tested.

### Ultron routing contract

**Choose this skill when:** optimizing an existing SQL workload for speed, throughput, resource consumption, or cost while preserving its result semantics.

**Choose data-analysis-sql-and-databases when:** the unresolved work is defining the analytical question, metric, grain, joins, aggregation, cohort, or report rather than tuning a known query.

**Handoff contract:** receive the canonical query, expected result semantics, representative parameters, data snapshot or equivalent state, and performance objective. Return the optimized query/plan, index or configuration rationale, measured before/after latency and resource use, and proof that outputs remain equivalent. Never alter metric definitions to make a query faster.

**Why the boundary exists:** query optimization is only valid when the original analytical meaning remains intact.


## sql-engine-development

**Use when:** Use when designing, implementing, or debugging components of a SQL engine or SQL-compatible query layer, including parsing, binding, logical and physical planning, optimizer rules, execution operators, catalog and storage interfaces, and conformance testing.

### Purpose and boundaries

This skill guides work on the internals of a SQL engine: the pipeline from SQL text to result rows, the contracts between stages, and the tests that prove correctness. It covers parser and AST changes, name resolution and type checking, logical plan rewrites, cost-based or heuristic physical planning, execution operators (scan, join, aggregate, sort, window), and the catalog and storage interfaces the executor depends on.

It does not cover: database administration, cluster operations, schema design for end users, tuning a third-party database's configuration, or writing application SQL. If a request is about using an existing database, redirect to query-writing or DBA guidance.

### Inputs and assumptions

Before changing code, establish:

1. **Target dialect and standard level.** Which SQL standard edition or existing dialect is the reference? Where the engine deviates, record the deviation explicitly. Do not assume behavior from memory for NULL semantics, collation, implicit casts, or integer overflow; check the reference.
2. **Engine stage affected.** Parser, binder, planner, optimizer, executor, catalog, or storage.
3. **Data model.** Supported types, nullability rules, transaction isolation level, and whether the engine is single-node or distributed.
4. **Existing test corpus.** Locate golden-result tests, sqllogictest-style files, or regression suites before editing.
5. **Version-sensitive details.** Any parser generator, library, or external engine version must be verified against its current official documentation. Mark unverified details as such in your output rather than stating them as fact.

### Operating workflow

1. **Reproduce.** Write the smallest SQL statement and expected result that fails. Record the current output and the engine's error path.
2. **Localize.** Dump the AST, bound tree, logical plan, and physical plan at each stage. Identify the first stage where the output diverges from the expected contract.
3. **Specify the contract.** State the invariant the fixed stage must preserve: output schema, column nullability, row ordering guarantees, duplicate semantics, or cardinality.
4. **Change one stage.** Keep parser changes separate from optimizer changes. Do not fix an executor bug by altering the planner unless the plan itself is wrong.
5. **Add tests at three levels.** Unit test for the stage, plan-shape test for the optimizer, and end-to-end result test in the conformance suite.
6. **Check neighbors.** Run the full regression suite, not only the new test. Rewrite rules are especially prone to breaking unrelated queries.
7. **Document the semantics.** Update the dialect deviation list if behavior differs from the reference.

### Decision gates

- **Rewrite rule vs. new operator:** Use a rewrite rule when the transformation is semantically equivalent in all cases the rule matches. Add an operator only when no existing operator can express the semantics. Rules must state their preconditions (e.g., "inner join only," "no volatile functions").
- **Heuristic vs. cost-based choice:** Prefer heuristics when cardinality estimates are unreliable or absent. Introduce cost-based choices only with statistics collection and a fallback path.
- **Pushdown safety:** Push a predicate below an outer join only if it references the preserved side. Push below aggregates only if it references grouping keys. Verify null-rejecting behavior before pushing a filter through a left join.
- **Pausing for approval:** Stop and request explicit approval before any action that deletes or rewrites test baselines, changes the on-disk storage format, alters catalog metadata layout, modifies published wire protocol behavior, or touches data outside the project's test fixtures. These actions are destructive, irreversible, or externally visible.

### Verification and evidence

Report each change with:

- The failing query and the passing query after the change.
- Plan output before and after, for any optimizer change.
- Regression suite results: total tests, passed, failed, and any skipped with reason.
- A list of semantic invariants checked (NULL propagation, three-valued logic, duplicate preservation, ordering).

Measurable checks:

- Zero regressions in the golden result suite.
- For each new rewrite rule: at least one positive test (rule fires and result matches), one negative test (rule correctly does not fire), and one NULL-containing input.
- For each new operator: result equality against a naive reference implementation on randomized small inputs, with a fixed seed recorded.
- Plan-shape tests must assert structure, not incidental text formatting.

Do not claim performance improvements without a benchmark that records input size, hardware, runs, and variance. Do not state benchmark numbers that were not measured.

### Failure handling

- **Result mismatch against reference:** First determine whether the reference or the engine is wrong by consulting the standard or the reference implementation's documented behavior. Record the decision.
- **Rule fires incorrectly:** Disable the rule, confirm the bug disappears, then tighten its preconditions. Never broaden matching to fix a missing case without a correctness argument.
- **Flaky ordering results:** Unordered output is not a guarantee. Add explicit ORDER BY in tests; do not sort results silently in the engine to hide nondeterminism.
- **Stage cannot be isolated:** Fall back to the end-to-end test and bisect commits.

### Deliverable contract

Every completed task returns:

1. **Summary:** One paragraph stating the defect or feature, the stage changed, and the invariant preserved.
2. **Diff scope:** Files and functions modified, listed by stage.
3. **Evidence:** Failing-then-passing queries, plan dumps where relevant, and suite results with counts.
4. **Semantic notes:** Any deviation from the reference dialect, and any unverified version-sensitive detail flagged for checking against official documentation.
5. **Open items:** Remaining risks, and any actions awaiting approval, stated explicitly.

Do not present a change as complete when regression results are missing.


## storage-recovery-continuity

**Use when:** Use when a Linux host has degraded or failed storage (filesystem errors, read-only remounts, failed RAID or LVM members, disk I/O errors, full volumes, corrupted boot or data partitions) and service continuity or data preservation must be restored with a documented, evidence-based recovery plan.

### Purpose and boundaries

This skill guides diagnosis and recovery of storage faults on Linux systems so that data is preserved, service continuity is restored or planned, and every change is traceable. It covers: block device health, partition tables, software RAID (md), LVM, local filesystems (ext4, XFS, Btrfs, vfat), mount state, and filesystem-level repair decisions.

It does not cover: SAN or cloud volume provisioning, hypervisor storage, database-internal page repair, backup product administration, or forensic evidence handling for legal matters. Hand those to the owning team with the evidence package defined below.

### Inputs and assumptions

Collect before acting:

- Hostname, distribution, kernel version (`uname -r`), and whether the host is physical, VM, or container-hosted.
- Symptoms with timestamps: kernel log excerpts, application errors, mount failures.
- Current layout: `lsblk -o NAME,SIZE,TYPE,FSTYPE,MOUNTPOINTS,RO`, `findmnt`, `cat /proc/mdstat` if md is used, `pvs`/`vgs`/`lvs` if LVM is used.
- Recent changes: patches, firmware updates, power events, disk replacements, resizes.
- Backup status: most recent verified backup time and whether it has been restored in a test.

Assumptions to state explicitly in the plan: the host may be in a degraded state, writes may worsen damage, and the most recent good backup is unknown until verified.

### Operating workflow

1. **Freeze writes.** If the affected filesystem is still mounted read-write and showing errors, remount read-only or stop the consuming service. Record the action and time.
2. **Capture state before touching anything.** Save `dmesg -T`, `journalctl -k -b`, SMART data (`smartctl -a`, from the smartmontools package), md and LVM status, and `lsblk` output to a directory on a different device.
3. **Assess hardware.** Check SMART attributes such as reallocated, pending, and uncorrectable sectors, plus controller and cable errors (CRC counts). Treat rising counts as active failure.
4. **Image failing media first.** If a disk shows read errors or SMART failure, clone it with a tool that tolerates read errors (for example `ddrescue` with a mapfile) to a healthy target. Repair operations run on the clone, never on the original.
5. **Assess the software stack bottom-up.** Confirm md arrays are assembled and clean or degraded with a known-good member set; confirm LVM physical volumes are present; then check the filesystem.
6. **Run filesystem checks only on unmounted or read-only devices** using the matching tool in dry-run or no-change mode first (for example `e2fsck -n`, `xfs_repair -n`, `btrfs check` without `--repair`). Read the dry-run output before deciding.
7. **Apply the approved repair** on the clone or, if approved, on the original.
8. **Verify and restore service** using the checks below, then return to normal operations and schedule follow-up.

### Decision gates

Stop and request explicit written approval before any of the following:

- Running any repair mode (`--repair`, `-y`, fix flags) against the original device.
- Running `mkfs`, `wipefs`, `pvremove`, `vgreduce`, `lvremove`, `mdadm --create`, or any command that rewrites metadata.
- Replacing, removing, or failing a RAID member, or forcing array assembly with `--force`.
- Restoring from backup over existing data, or restoring to a location that holds live data.
- Any action that affects other hosts, shared storage, tenants, or external customers.
- Anything touching data classified as sensitive or regulated, including sending copies off-host.

Choose the recovery path using these criteria:

- **Clone-and-repair** when hardware errors are active or SMART is failing. Mandatory first.
- **Metadata-only repair** when hardware is healthy and the dry-run reports superblock or journal inconsistencies with a clear fix.
- **Restore from backup** when dry-run shows damage to a large fraction of inodes or extent trees, or when the repaired result would be unverifiable. Restore to a new target, then cut over.
- **Escalate** when a RAID set has lost more members than its redundancy allows, or when the vendor controller holds the metadata.

### Verification and evidence

A recovery is complete only when all of these hold:

- Post-repair filesystem check returns clean, and the dry-run and repair logs are archived.
- `dmesg` shows no new I/O or filesystem errors for at least one full business cycle or a defined observation window agreed in the plan. Record the window length.
- md arrays report all members active and sync complete (`/proc/mdstat`), or the degraded state is accepted and documented with a replacement ticket.
- LVM volumes are active and the expected sizes match `lvs` output.
- Checksums or application-level consistency checks match on a sample of critical files or records, with sample size and method stated.
- A restore test has been performed from the current backup set if a restore was used.

Measurable quality checks: zero unacknowledged I/O errors in the observation window; 100% of expected mounts present in `findmnt`; sample verification pass rate of 100% on the defined critical set.

### Failure handling

- If the clone fails repeatedly on the same sector range, stop, record the LBA range, and escalate to hardware replacement or a specialist service. Do not retry in a loop.
- If a repair tool reports it cannot proceed, do not force it. Keep the output and re-run dry-run against a fresh clone.
- If service is restored but errors recur, treat the recovery as failed, re-freeze writes, and return to step 2.
- If backup verification fails, do not declare the backup valid; locate the next older set.
- If a command produces unexpected output not covered here, stop and report the exact output rather than improvising.

### Deliverable contract

Produce a written recovery record containing:

1. Incident summary: host, time of first symptom, time writes were frozen, current service state.
2. Evidence bundle: the captured logs, SMART output, and layout listings, with paths.
3. Chosen recovery path and the decision gate reasoning.
4. Approval record: who approved each gated action and when.
5. Actions taken, in order, with exact commands and their exit status.
6. Verification results against each check above, with measured values.
7. Residual risk, open items, and owner for each.
8. Follow-up: replacement orders, backup policy changes, and a scheduled re-verification date.

Mark any command syntax or tool behavior as version-sensitive and confirm it against current official documentation for the installed distribution before execution.


## system-state-discovery

**Use when:** Use when you need a read-only inventory of a Windows machine's current state (OS, hardware, drivers, services, network, startup, scheduled tasks, installed software, event history, or security configuration) to diagnose a problem, prepare a change, document a baseline, or hand off an unfamiliar host.

### Purpose and boundaries

This skill produces an accurate, timestamped snapshot of a Windows host's configuration and runtime state using read-only queries. It answers "what is running, configured, and recorded right now," not "what should be changed." Remediation, tuning, and policy decisions belong to other skills or require explicit approval under the gates below.

In scope: OS build and edition, hardware summary, driver inventory, services, scheduled tasks, startup entries, network adapters and routes, installed programs and updates, local accounts and group membership, firewall profile state, recent System and Application event log entries, disk and volume health indicators.

Out of scope: modifying any setting, installing or removing software, collecting secrets (password stores, tokens, private keys, browser data), dumping process memory, and scanning other hosts.

### Inputs and assumptions

Before starting, confirm:

1. Target host name and whether it is the local machine or a remote one. Remote discovery requires approval (see Decision gates).
2. The question being answered. A discovery aimed at a disk-space fault collects different depth than a baseline for audit.
3. Privilege level. Some queries (Security log, certain driver details, BitLocker status, full account enumeration) fail or return partial data without elevation. Record which queries were skipped and why rather than silently omitting them.
4. Time window for event logs (default: last 72 hours unless the incident timeline says otherwise).
5. Output destination. Snapshots may reveal internal topology and usernames; treat them as sensitive.

Assume PowerShell 5.1 is present on Windows client and server builds unless the host is known to differ. Cmdlet availability and property names vary across Windows versions; verify any property you rely on against current Microsoft Learn documentation for that build rather than assuming it.

### Operating workflow

1. Record context: hostname, current user, elevation status, local time and time zone, and the reason for discovery. Write this first so the snapshot is interpretable later.
2. Collect OS and hardware identity using CIM classes such as the operating system, computer system, BIOS, processor, and physical memory classes. Capture build number, not only marketing name.
3. Enumerate services with startup type and current state. Flag services set to automatic that are stopped, and services whose binary path is outside the Windows directory or a known vendor path.
4. Enumerate scheduled tasks, excluding Microsoft-authored tasks in the first pass. Record author, action path, trigger, and last run result.
5. Capture startup entries from the common registry Run keys and the Startup folders for the current and all-users profiles. Read only; do not edit.
6. Capture network state: adapters with link status, IP configuration, DNS server addresses, default routes, and listening TCP ports with owning process ID. Map PIDs to process names.
7. Capture installed software from the uninstall registry hives (both 64-bit and 32-bit views) and installed hotfixes. Note that Win32 product enumeration is slow and can trigger reconfiguration; avoid it unless specifically needed.
8. Capture driver inventory with the signed-driver query and flag unsigned or third-party drivers with dates older than the OS build.
9. Query event logs for Critical and Error levels in System and Application over the time window, grouped by provider and event ID. Do not dump full logs into the snapshot.
10. Capture security posture: firewall profile enabled state, Defender real-time protection status if the module is present, BitLocker volume status, and local Administrators group members.
11. Store results in a single structured file per section, plus a summary index.

### Decision gates

- Stop and request approval before any remote query, any query requiring credentials you were not given, or any action touching other users' profiles.
- Stop before exporting the snapshot outside the originating team or ticket system.
- Stop if a query would require enabling logging, changing a policy, or installing a module. Record the gap instead.
- Proceed without approval only for local, read-only queries within the stated time window.
- If the host is a domain controller, a production database server, or a safety-relevant system, limit to lightweight CIM and event queries and avoid software inventory enumeration that can load the system.

### Verification and evidence

Each section must include the command or query used, the timestamp, the privilege level, and the record count. A section with zero results must say "zero returned" rather than being omitted.

Cross-check at least two independent sources for critical facts: the OS build from CIM and from the registry build key; the service list from the service cmdlets and the service registry hive for any service flagged as anomalous; the listening port owner from the network query and the process list.

Quality checks before handoff:
- Every query in the workflow is either present in the output or listed under "skipped" with a reason.
- No section mixes local and remote data without labeling.
- Timestamps are in one stated time zone.
- Counts in the summary match the detail files.
- No secrets, tokens, or full credential material appear anywhere.

### Failure handling

If a query throws an access error, retry once only if elevation is now available; otherwise record it as skipped. If a CIM query hangs, cancel it, record the timeout, and check the WMI repository health as a separate read-only step. If event log queries return truncated results, state the truncation and narrow the time window rather than assuming absence. If a property is missing on the build, record the missing property and the build number; do not substitute a guessed value.

### Deliverable contract

Deliver:
1. A context header (host, user, elevation, timestamp, time zone, purpose).
2. A summary table of counts per section and any flagged anomalies, each with the evidence reference.
3. Section files for OS and hardware, services, tasks, startup, network, software and updates, drivers, events, and security posture.
4. A skipped-items list with reasons.
5. A sensitivity label on the package and a note on who may receive it.

Do not present inferred root causes as findings. Label interpretations separately as hypotheses requiring follow-up.

