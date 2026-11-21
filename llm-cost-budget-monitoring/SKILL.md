---
name: llm-cost-budget-monitoring
description: Use when tracking, forecasting, capping, or alerting on LLM and agent token spend, reviewing per-task or per-tenant inference costs, or designing budget guardrails for multi-step AI agent workflows.
author: Luo Kai
provenance: original
version: 1.0.0
---

# LLM Cost Budget Monitoring

## Purpose and boundaries

This skill covers measuring, attributing, forecasting, and enforcing spend limits on LLM API usage in agent and automation systems. It applies to:

- Per-run, per-task, per-user, and per-tenant cost attribution.
- Budget thresholds, alerts, soft throttles, and hard stops.
- Cost regression review after model, prompt, or routing changes.

It does not cover model quality selection beyond cost trade-offs, infrastructure capacity planning, or negotiating vendor contracts. Pricing data changes often; treat any price in your notes as version-sensitive and confirm it against the provider's current pricing page before using it in a decision.

## Inputs and assumptions

Collect before analysis:

1. Usage records per call: timestamp, model identifier, input tokens, output tokens, cached or reused input tokens if reported, request or run ID, parent task ID, tenant or project tag.
2. The price table in effect for the period, with currency, unit (per million tokens is common but verify), and effective dates.
3. Budget definitions: period (daily, monthly), scope (global, project, tenant), and owner.
4. Agent topology: number of model calls per run, tool calls that trigger further model calls, retry policy, and maximum loop depth.

Assumptions must be stated explicitly. If token counts are estimated rather than returned by the provider, label cost figures as estimates. If records are missing for some calls, report coverage as a percentage and do not extrapolate silently.

## Operating workflow

1. **Reconcile the ledger.** Sum recorded costs per day and compare against the provider's invoice or usage export. Accept a variance under 2% for the same period; investigate anything larger before proceeding.
2. **Attribute cost.** Group by model, task type, tenant, and agent step. Identify the top 10% of runs by cost; these typically dominate spend.
3. **Detect anomalies.** Flag runs whose cost exceeds 3x the median for their task type, runs with more than the configured maximum model calls, and retry storms (same prompt hash repeated more than 3 times within 10 minutes).
4. **Decompose drivers.** For each cost increase, separate the contribution of volume, average input size, average output size, model mix, and retry rate. Report each as a percentage of the change.
5. **Forecast.** Project remaining-period spend using the trailing 14-day daily mean adjusted for known events. Present a range (low, expected, high) rather than a single number.
6. **Recommend controls.** Propose only changes whose expected savings are quantified against the decomposed drivers.

## Decision gates

- **Gate A, ledger mismatch:** If reconciliation variance exceeds 2%, stop and resolve before issuing any recommendation.
- **Gate B, threshold breach:** If projected spend exceeds 90% of budget, notify the budget owner and request a decision on throttling. Do not enable hard stops automatically.
- **Gate C, control change:** Changes that alter routing to a different model, cap production traffic, disable a tenant, or modify retry logic require explicit approval from the system owner before deployment. Present the expected cost impact, quality risk, and rollback path.
- **Gate D, data handling:** Do not export per-user prompt content or identifiers into reports. Use aggregated or hashed identifiers unless the requester has documented authorization.

## Verification and evidence

Every reported figure must trace to a query or export that can be re-run. Include:

- Date range, data source, and row count.
- Coverage: percentage of calls with complete token and cost fields.
- Reconciliation variance against the invoice or provider usage export.
- Before-and-after comparison for any proposed change, measured on the same traffic slice, minimum 7 days or enough runs for a stable median.

Quality checks before delivery:

- Totals equal the sum of their components within rounding.
- No cost figure uses a price not dated to the reporting period.
- Forecast range width is stated, and actual spend to date falls inside the prior forecast range for at least 80% of past periods when backtested.

## Failure handling

- **Missing token counts:** Estimate from tokenizer counts only if the tokenizer version matches the model, and label as estimated. Otherwise exclude and report the gap.
- **Price table gap:** Do not guess. Mark affected rows as unpriced and report them separately.
- **Runaway agent loop detected:** Recommend a pause for that run ID and escalate; do not delete logs or alter the run's state without approval.
- **Conflicting sources:** Prefer provider invoice data over internal estimates, and document the conflict.

## Deliverable contract

Return a report containing:

1. Summary: total spend, forecast range, budget status, top three drivers.
2. Attribution table: scope, cost, share of total, call count, median cost per run.
3. Anomaly list: run or task IDs, metric, threshold, observed value.
4. Recommendations: each with expected impact range, risk, required approval gate, and verification plan.
5. Data notes: coverage, reconciliation variance, unpriced rows, assumptions.

Do not state savings as guaranteed. Do not cite benchmark or vendor claims without a link to current official documentation, and mark any version-sensitive pricing or API detail as requiring verification.

## What not to do

- Do not apply hard budget stops, disable keys, or change model routing without Gate B or C approval.
- Do not present estimated costs as invoiced costs.
- Do not share raw prompts, outputs, or user identifiers in cost reports.
- Do not hardcode prices into logic; load them from a dated, versioned table.
- Do not average across models with different prices without weighting by actual call volume.