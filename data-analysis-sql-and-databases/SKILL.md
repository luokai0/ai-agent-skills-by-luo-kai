---
name: data-analysis-sql-and-databases
description: Use when writing, reviewing, or debugging SQL queries, designing analytical datasets, validating database-backed metrics, or answering business questions from relational data stores.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Data Analysis: SQL and Databases

## Purpose and boundaries

Covers answering analytical questions from relational databases and warehouses: query authoring, joins and aggregation, metric definition, data quality checks, and reporting results with stated confidence. Out of scope: database administration (provisioning, production index tuning, user and role management), schema migrations, writes to production tables, and non-relational stores unless the user confirms the approach applies.

## Inputs and assumptions

Before querying, establish:
- The exact question and the decision it informs.
- Engine and dialect (for example PostgreSQL, MySQL, BigQuery, Snowflake, SQLite). Do not assume function names transfer between engines. Verify syntax against the current official documentation for the engine and version in use.
- Schema: table grain, primary and foreign keys, and timestamp semantics (event time versus load time, timezone).
- Access level. Read-only is the default. Confirm whether the target is production or a replica.
- Metric definitions from the owning team. If none exist, write a definition, state it, and get it confirmed.

List every assumption in the output.

## Operating workflow

1. Restate the question as a measurable target: metric, population, time window, grain, and comparison baseline.
2. Inspect schema and sample rows with a row limit, and bound partitioned tables by date. Record row counts and null rates for key columns.
3. Define the grain of the final result before writing joins. Express it as "one row per X per Y".
4. Build the query as named CTEs, one logical step each: filter, deduplicate, join, aggregate.
5. Check join cardinality by comparing row counts before and after each join. Unexpected row multiplication is the most common analytical error.
6. Reconcile the total against an independent source (a source table, a previously published figure, or a simpler query) within a stated tolerance.
7. Document the final query, assumptions, and result.

## Decision gates

- Execute only when grain and time window are explicit. If either is missing, ask.
- Estimate scan cost before running against large or partitioned tables. If the query would scan full history without a filter or exceed the agreed budget, narrow it first.
- Require explicit approval before any of the following:
  - Running statements that write, delete, update, or alter schema.
  - Querying production when a replica exists.
  - Exporting data containing personal, financial, health, or credential fields.
  - Sharing results outside the requesting team.
  - Changing a dashboard, scheduled job, or shared metric definition.
- If two metric definitions compete, stop and present both with their numeric difference.

## Verification and evidence

Each check must pass or be reported as failed:
- Row counts after each join match the expected cardinality, which you state in advance.
- Grain columns are unique in the final output.
- Join-key null rates are below the threshold you declared, or the nulls are reported.
- The date range covers the requested window without gaps, and timezone handling is consistent.
- Reconciliation difference is within the stated tolerance. Do not claim an exact match without proof.
- At least three result rows are traced back to source records.

Report the evidence: query text, row counts, and reconciliation figures. Never present a number without its population and filters.

## Failure handling

- Syntax or engine error: correct the specific error. Do not rewrite the whole query.
- Empty result: check filters, timezone boundaries, case sensitivity, and type mismatches (string versus integer identifiers) before concluding no data exists.
- Inflated result: suspect fan-out from a non-unique join key and check distinct counts on each side.
- Failed reconciliation: report the gap and candidate causes ranked by likelihood. Do not alter the query to force agreement.
- Permission denied: stop, report, and request access. Do not seek workarounds such as shared credentials.

## Deliverable contract

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