---
name: saas-finance-commerce-automation
description: Use when designing, auditing, or operating agent-driven workflows that touch SaaS billing, subscription lifecycle, invoicing, refunds, revenue reconciliation, or commerce order-to-cash data, where an agent reads or proposes changes to financial records.
author: Luo Kai
provenance: original
version: 1.0.0
---

# SaaS Finance Commerce Automation

## Purpose and boundaries

This skill guides an agent through automation of subscription and commerce finance operations: plan and price changes, trial conversions, dunning and payment recovery, invoice generation and corrections, refund and credit handling, deferred revenue schedules, and reconciliation between billing, payment processor, ledger, and CRM records.

In scope: reading financial state, classifying discrepancies, drafting corrective actions, preparing reconciliation reports, and executing pre-approved low-risk operations through an approved integration.

Out of scope: tax filing or tax advice, accounting policy decisions (revenue recognition judgments, reserve estimates), legal interpretation of contracts, credit decisions, and any action that moves money or changes a ledger of record without explicit human approval.

## Inputs and assumptions

Before acting, confirm and record:

1. Source systems: billing platform, payment processor, general ledger, CRM, and their read/write scopes.
2. Accounting period, currency set, and timezone used for cutoffs.
3. Authoritative source for each entity (for example, the billing platform owns subscription state; the processor owns settlement status; the ledger owns posted balances).
4. Pricing and plan catalog version in effect for the period.
5. Approval matrix: who approves refunds, credits, write-offs, and cancellations, and at what thresholds.
6. Whether the environment is sandbox or production. Assume production unless told otherwise.

If any input is missing, stop and request it. Do not infer thresholds or approvers.

## Operating workflow

1. **Snapshot.** Pull read-only data for the defined scope (customer, subscription, or batch window). Record timestamps and record counts. Use a fixed cutoff.
2. **Normalize.** Convert amounts to minor currency units, map statuses to a single internal vocabulary, and tag each record with its source system.
3. **Match.** Join records on stable identifiers (subscription ID, invoice ID, processor charge ID). Never join on email or name alone. Flag unmatched records on both sides.
4. **Classify discrepancies.** Assign each to one category: timing (settlement lag under the agreed window), duplicate, missing invoice, amount mismatch, status mismatch, currency mismatch, or unknown.
5. **Propose actions.** For each discrepancy, draft the smallest corrective step, its expected ledger effect, its reversibility, and its approver.
6. **Simulate.** Where the platform offers a dry-run or preview, use it. Otherwise compute the expected before/after balances in a separate calculation and show the delta.
7. **Request approval.** Present the batch as a table with totals. Wait for explicit approval per action class.
8. **Execute and confirm.** Apply approved actions one at a time or in small idempotent batches. Re-read each changed record and compare to the expected state.
9. **Report.** Return the transaction plan in the required output structure below.

## Decision gates

Stop and obtain human approval before any of the following:

- Any refund, credit note, chargeback response, write-off, or voided invoice.
- Any change to price, plan entitlement, or billing cycle on a live subscription.
- Any cancellation or pause that affects revenue or customer access.
- Any posted ledger entry, journal adjustment, or period reopening.
- Any outbound customer communication about charges, failures, or cancellations.
- Any batch where affected amount exceeds the approval threshold or affected record count exceeds 50 without prior sampling.
- Any action where source systems disagree on the authoritative state.
- Any operation that cannot be reversed by a documented compensating action.

Proceed without a gate only for read-only queries and generation of draft reports.

## Verification and evidence

- Reconciliation balance: for every batch, sum(source amounts) minus sum(target amounts) equals the listed discrepancy total, to the minor unit. Zero unexplained residual is the pass condition.
- Idempotency: re-running the same batch after success produces zero new changes.
- Sampling: before executing any batch over 50 records, manually verify at least 10 percent, minimum 5, against source documents.
- Post-change read-back: each modified record matches the approved expected state.
- Evidence retained: record IDs, pre- and post-state, timestamps, actor identity, and approval reference for every write.
- Version-sensitive details (API endpoints, field names, webhook event types, rate limits, and rounding behavior) must be checked against current official vendor documentation before use. Do not rely on memory for these.

Do not claim compliance with any tax, accounting standard, or payment card rule. State only what was verified in the data.

## Failure handling

- **Partial failure:** stop the batch. Record which actions completed, which failed, and the error text. Do not retry writes automatically unless the operation is confirmed idempotent in current documentation.
- **Ambiguous state:** when a write response is missing or a timeout occurs, re-read the record before any retry. If state is unknown, escalate.
- **Rate limit or auth error:** pause, report, and wait. Do not rotate credentials or widen scopes.
- **Source conflict:** do not resolve by picking the larger or newer value. Escalate with both values and their sources.
- **Compensating action needed:** draft it, mark it as requiring approval, and never apply it silently.

## Deliverable contract

Every run returns:

1. Scope statement: systems, period, cutoff timestamp, record counts per source.
2. Summary table: discrepancy category, count, total amount, status (proposed, approved, executed, failed, escalated).
3. Action log: record ID, action, expected effect, approver, execution result, read-back result.
4. Reconciliation statement showing the residual (must be zero or explicitly listed).
5. Open items: escalations, unmatched records, and verification steps not yet completed.
6. Assumptions and unverified version-sensitive details, listed explicitly.

## What not to do

- Do not issue refunds, credits, or cancellations to resolve a mismatch you have not classified.
- Do not treat processor-reported status as ledger truth without the ledger's posting confirmation.
- Do not batch unrelated customers into a single approval.
- Do not round amounts to hide differences.
- Do not hardcode plan prices, tax rates, or API field names from memory.
- Do not send customer-facing messages about payment failures without approval of the wording and recipient list.
- Do not reopen a closed accounting period.