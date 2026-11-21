---
name: business-analytics-dashboards
description: Use when designing, building, reviewing, or troubleshooting business analytics dashboards that report KPIs from warehouses, BI tools, or spreadsheets, including metric definitions, data model checks, visual design, and stakeholder handoff.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Business Analytics Dashboards

## Purpose and boundaries

This skill guides the end-to-end production of decision-support dashboards: scoping the decision a dashboard serves, defining metrics unambiguously, validating the underlying data, laying out visuals, and handing off with documentation. It covers recurring operational dashboards, executive summaries, and ad hoc exploratory views that will be reused.

Out of scope: writing production ETL pipelines, changing source-system schemas, granting data access, making financial or compliance attestations, and forecasting models beyond simple trend context. Route those to data engineering, security, finance, or model-governance owners.

## Inputs and assumptions

Before building, collect:

1. **Decision and audience.** The specific recurring decision (e.g., "reallocate weekly paid-media budget"), who makes it, and how often.
2. **Metric dictionary.** Names, formulas, grain, filters, owners. If absent, draft one and mark it "unconfirmed" until a business owner signs off.
3. **Data sources.** Table or extract names, refresh cadence, known latency, and the system of record for each metric.
4. **Access constraints.** Which fields are personal, confidential, or restricted.
5. **Tooling.** The BI platform and version in use. Treat any feature, function, or connector behavior as version-sensitive; verify against the vendor's current official documentation before relying on it.

Assume data is imperfect until profiled. Assume the requester's stated metric may differ from what the business actually uses; confirm.

## Operating workflow

1. **State the decision in one sentence.** If you cannot, stop and clarify. A dashboard without a decision becomes a catalogue of charts.
2. **Limit scope.** Select no more than 5–7 primary KPIs plus supporting diagnostics. Each KPI must map to the decision.
3. **Write metric specifications.** For each KPI record: name, business definition, numerator and denominator, grain (e.g., order line, customer-day), time basis (order date vs. ship date), inclusion and exclusion rules, timezone, and owner.
4. **Profile source data.** Check row counts against a known control total, null rates on key fields, duplicate keys, date range gaps, and late-arriving records. Record results.
5. **Reconcile.** Compare at least one headline figure to an independent source (finance ledger, system report, or manual sample of 20–50 records). Document any variance above an agreed tolerance.
6. **Build the model layer.** Prefer a single curated dataset or semantic-layer definition per metric so every visual uses identical logic. Do not recompute the same KPI differently on different sheets.
7. **Lay out the dashboard.** Place the headline KPIs top-left, trend context beside them, and diagnostic breakdowns below. Use one chart type per question: lines for change over time, bars for comparison across categories, tables only when exact values matter.
8. **Add context.** Show period-over-period or target comparison, the data refresh timestamp, and metric definitions reachable from the page.
9. **Test with real users.** Ask the decision-maker to state what the dashboard says and what they would do. Revise where answers diverge from intent.
10. **Hand off** using the deliverable contract below.

## Decision gates

- **Gate A (scope):** Proceed only when the decision, audience, and KPI list are approved by the requester.
- **Gate B (definitions):** Proceed only when the business owner confirms each metric formula. Unconfirmed metrics must be labeled as such on the dashboard.
- **Gate C (reconciliation):** Publish only when headline figures match the reference source within the agreed tolerance, or variances are explained and accepted in writing.
- **Gate D (access and sensitivity):** Stop and request explicit approval before sharing any dashboard that includes personal, health, financial-account, or otherwise restricted fields, or before publishing outside the original audience.
- **Gate E (publication):** Any action that overwrites a live dashboard, changes shared permissions, schedules external delivery, or alters source tables requires explicit approval from the owner. Do not perform these actions unilaterally.

## Verification and evidence

Record the following evidence with every release:

- Control-total comparison: source rows versus loaded rows, with the difference and reason.
- Null and duplicate rates for key dimensions and identifiers; target thresholds agreed in Gate B.
- Headline reconciliation table: dashboard value, reference value, absolute and percentage variance.
- Date-boundary check: confirm the most recent complete period and that partial periods are labeled.
- Filter test: apply each filter and confirm totals change as expected, including "all" selections.
- Drill-down test: confirm sums of components equal the parent total.

Measurable quality bar: headline reconciliation within the agreed tolerance (commonly 0.5% for revenue-type totals unless the owner specifies otherwise); zero unlabeled partial periods; every visible KPI traceable to a written definition.

## Failure handling

- **Reconciliation mismatch:** Halt publication. Check timezone, date basis, filter inclusion, and duplicate joins in that order. Do not adjust the dashboard formula to force agreement.
- **Missing or late data:** Show the last successful refresh time prominently and mark affected periods as incomplete. Do not impute values silently.
- **Conflicting definitions:** Escalate to the metric owner. Present both definitions with example records and their numeric impact.
- **Performance problems:** Reduce granularity, pre-aggregate at the agreed grain, or limit default date range. Avoid removing definitions to improve speed.
- **Unexpected sensitive fields discovered:** Stop, remove them from the working copy, and request Gate D approval before continuing.

## Deliverable contract

Deliver:

1. Decision statement and audience (one paragraph).
2. Metric dictionary with status (confirmed or unconfirmed) for each KPI.
3. Source inventory with refresh cadence and system of record.
4. Dashboard artifact link or file, referencing the tool version used.
5. Verification evidence per the section above.
6. Known limitations and open questions, each with an owner.
7. Maintenance notes: refresh schedule, owner contact, and the procedure for changing a definition.

What not to do:

- Do not present unconfirmed metrics as authoritative.
- Do not mix time bases (order date and payment date) within one KPI without labeling.
- Do not use dual axes or truncated bar baselines to exaggerate change.
- Do not include more than seven primary KPIs.
- Do not claim accuracy, compliance, or security certification the evidence does not support.
- Do not state specific tool features, function names, or version behaviors as fact without checking current official documentation.