---
name: cloud-infrastructure-cost
description: Use when analyzing, forecasting, or reducing cloud infrastructure spend that flows through external registries, such as container image registries, package mirrors, or artifact stores, including storage, egress, pull traffic, and retention costs.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Cloud Infrastructure Cost

## Purpose and boundaries

This skill covers cost attribution, analysis, and optimization for cloud resources whose spend is driven by external registries: image and artifact storage, cross-region or cross-cloud pulls, registry-to-compute egress, mirror synchronization, vulnerability-scan and replication features, and retention sprawl.

In scope: cost drivers, usage-to-cost mapping, retention and lifecycle policy proposals, pull-path redesign (caching, regional placement), and savings estimates with stated confidence.

Out of scope: general application performance tuning, changing production registry access controls, deleting or moving artifacts, purchasing commitments, and making claims about provider pricing without a current source.

## Inputs and assumptions

Collect before analysis:

- Billing exports for the review window (minimum 30 days; 90 preferred to capture release cycles).
- Registry inventory: repositories, artifact counts, total stored bytes, tag and digest counts.
- Pull and push telemetry: request counts, bytes transferred, source region, destination region or cluster.
- Topology: which compute environments pull from which registries, and across which network boundaries.
- Retention and lifecycle policies currently configured, and who owns each repository.

Assumptions must be written down explicitly. Pricing is version-sensitive: treat all unit prices as unverified until checked against the provider's current pricing documentation and the contracted rate card. Do not use remembered prices.

## Operating workflow

1. **Define the window and currency.** Fix the date range, currency, and whether figures are amortized or on-demand.
2. **Attribute spend.** Map each billing line item to a cost category: storage, inter-region transfer, internet egress, managed feature fees, or compute tied to pulls. Items without an owner go into an explicit "unattributed" bucket, which must stay under 10% of total spend before recommendations are finalized.
3. **Rank drivers.** Sort categories by monthly cost. For the top five repositories or paths, compute cost per pull and cost per stored GB-month.
4. **Diagnose waste patterns.** Check for: untagged or orphaned digests still referenced by nothing; excessive historical tags; the same image duplicated across regions; cross-region pulls where a regional replica would serve; CI pipelines pulling uncached base layers repeatedly; mirrors syncing content that is never consumed.
5. **Model options.** For each candidate change, estimate monthly savings as a range: low, expected, high. Show the formula and inputs.
6. **Rank by value and risk.** Prefer changes that remove stored bytes nobody references or that keep traffic within a region, over changes that alter how builds authenticate or resolve images.
7. **Draft the change plan**, staged so each step is reversible and measurable.

## Decision gates

- **Gate A (before any deletion or lifecycle enforcement):** Requires written owner approval per repository, a list of digests to be affected, and confirmation that no environment pins them. Obtain explicit approval; do not proceed on inference.
- **Gate B (before replication or regional changes):** Requires approval because it changes data residency and external-facing traffic. Confirm compliance owners have reviewed.
- **Gate C (before changing pull credentials, endpoints, or DNS):** Requires explicit approval and a rollback path. Treat as external-impacting.
- **Gate D (before committing spend commitments or sharing estimates externally):** Requires approval from the budget owner.

If a gate is not cleared, record the recommendation as "pending approval" and stop that branch.

## Verification and evidence

- Reconciliation: recomputed category totals must match billing totals within 2%.
- Savings claims require a before-and-after measurement plan, not just a projection.
- Every recommendation cites its evidence: billing line, telemetry query, or inventory record.
- Dry-run lifecycle rules where the platform supports it; if dry-run is unavailable, state that and reduce confidence.
- Confirm all version-sensitive product behavior, pricing, and feature availability against current official documentation, and record the retrieval date.

## Failure handling

- **Missing telemetry:** Lower confidence one tier and report the gap; do not backfill with estimates presented as measurements.
- **Unattributed spend above 10%:** Stop recommendations and report the attribution gap first.
- **Conflicting numbers between billing and telemetry:** Report both, identify the likely cause (timezone, currency, aggregation window), and resolve before ranking.
- **Owner unreachable for a gate:** Hold the change. Do not treat silence as approval.

## Deliverable contract

Produce a single report containing:

1. Scope and window, with currency and pricing verification date.
2. Spend attribution table: category, monthly cost, share, owner.
3. Top drivers with cost per pull and cost per stored GB-month.
4. Recommendations table: action, evidence reference, savings low/expected/high, confidence, gate required, status.
5. Staged change plan with rollback steps and success metrics.
6. Open questions and approvals outstanding.

Do not include unverified prices, invented tool flags, or guarantees of savings or compliance outcomes.