---
name: commerce-payments-revenue
description: Use when reconciling, validating, or reporting payment and revenue records sourced from external registries such as payment processors, marketplaces, app stores, or payout ledgers, including settlement matching, refund and chargeback handling, fee attribution, and revenue recognition inputs.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Commerce Payments Revenue

## Purpose and boundaries

This skill covers turning payment and revenue records from external registries into a reconciled, auditable view of gross sales, fees, refunds, disputes, payouts, and net revenue. It applies to exports, reports, and API extracts from processors, marketplaces, app stores, and payout providers.

In scope: matching transactions to settlements, classifying events (sale, refund, chargeback, reversal, fee, adjustment), currency normalization using the rate source the registry itself reports, variance analysis, and producing a reconciliation package.

Out of scope: tax filing, legal revenue-recognition opinions, accounting entries posted to a live ledger, and any action that moves money, changes registry state, or contacts a counterparty. Do not provide compliance certifications or guarantee that outputs satisfy a given accounting standard.

## Inputs and assumptions

Required before starting:
- Source extracts with period boundaries, time zone, and currency stated.
- Registry-native identifiers (transaction, payout, dispute, order IDs).
- Fee schedules or fee lines as reported by the registry.
- The internal order or invoice record, if matching to internal sales.

Assumptions to state explicitly in the output: whether amounts are gross or net of tax, whether refunds posted in the period belong to the original sale period, and which timestamp (authorization, capture, settlement, or payout) defines the period.

Mark any field name, report format, or API behavior as "verify against current official registry documentation" unless you have confirmed it in the supplied files. Do not infer schema from memory.

## Operating workflow

1. Inventory each source: row count, date range, currency set, and control totals reported by the registry. Record them before transforming anything.
2. Normalize: convert amounts to minor units, unify sign conventions (refunds and fees negative), and tag each row with its event type.
3. Match primary keys first: transaction to settlement, settlement to payout. Use exact ID matches before any fuzzy matching on amount, date, or reference text.
4. Attach secondary events: refunds, chargebacks, reversals, and reissued payments link to their original transaction via registry references, not by amount alone.
5. Attribute fees to their parent transaction or to a period-level bucket if the registry does not itemize them. Label unattributed fees explicitly.
6. Compute the bridge: gross sales − refunds − chargebacks − fees ± adjustments = net settled, and net settled − payouts in transit = closing balance difference.
7. Investigate every residual above the tolerance threshold before closing the period.

## Decision gates

- Gate A (source trust): If control totals from the registry do not match the extract row sums, stop and request a re-export. Do not reconcile against a partial file.
- Gate B (currency): If a single settlement mixes currencies without a stated conversion, hold that settlement and escalate. Do not apply a rate you sourced yourself without approval.
- Gate C (tolerance): Residuals at or below the agreed tolerance (default: zero for minor-unit exact matches, with rounding differences listed separately) may be closed with a note. Anything larger requires root cause.
- Gate D (external action): Any request to issue refunds, submit disputes, change payout settings, or send reconciled figures to a counterparty requires explicit written approval from the account owner. Prepare the request; do not execute it.
- Gate E (sensitive data): Mask card fragments, bank account numbers, and personal identifiers in all outputs. Retain only the registry reference IDs needed for traceability.

## Verification and evidence

Quality checks, all required:
- Sum of classified rows equals source control total to the minor unit, per source and per currency.
- Every net-settled amount traces to at least one payout ID or an explicitly listed pending status.
- Zero duplicate transaction IDs after normalization, unless the registry documents legitimate reissues, which must be listed.
- Refund and chargeback totals reconcile to registry-reported dispute and refund summaries.
- Residual count and value reported as a percentage of gross volume; target under 0.1% unless the owner sets another threshold.

Evidence to retain: source file hashes, row counts before and after each step, matching rules applied in order, and a list of every manual override with reason and approver.

## Failure handling

- Missing or duplicate IDs: quarantine the rows, report counts, and request clarification. Do not generate substitute keys silently.
- Control total mismatch: report the delta and the first divergent date or batch; do not force a balance.
- Timezone boundary shifts: test whether moving the cutoff by the stated offset clears the variance; if so, document the cutoff issue rather than adjusting amounts.
- Registry format change: halt parsing, diff the header against the last validated version, and mark outputs as provisional.

## Deliverable contract

Produce one package containing:
1. Summary: period, sources, currencies, gross, net, fees, refunds, disputes, payouts, and residual value with percentage.
2. Reconciliation table by settlement and payout, with status (matched, pending, exception).
3. Exception register: each open item with ID, amount, cause hypothesis, owner, and required approval if any.
4. Assumptions and verification results against each quality check above.
5. Approval requests for any Gate D actions, listed but not executed.

Do not present unverified figures as final. Label provisional outputs clearly.