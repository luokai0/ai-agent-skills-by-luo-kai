---
name: architecture-decision-record-lifecycle
description: Use when proposing, reviewing, accepting, superseding, or retiring an architecture decision record (ADR), or when deciding whether a technical choice needs one.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Architecture Decision Record Lifecycle

## Purpose and boundaries

This skill governs how an architecture decision is captured as an ADR, moved through its statuses, linked to related decisions, and eventually superseded or retired. It covers the record itself, not the design work behind it, and not the implementation that follows.

In scope: deciding whether a choice warrants an ADR; drafting context, options, and consequences; running review; recording acceptance; handling supersession; maintaining the index.

Out of scope: writing system design documents, selecting vendors without a decision owner, editing ADRs after acceptance to change their substance, and recording decisions on behalf of people who have not agreed to them.

## Inputs and assumptions

Required inputs:
- The decision question in one sentence.
- The decision owner and the reviewers, by role or name.
- The ADR repository location and numbering scheme already in use. If none exists, propose one and get approval before creating files.
- Constraints: cost, compliance regime, latency or availability targets, team skills, existing platform commitments.
- Candidate options, at least two, including "do nothing" where it is viable.

Assumptions to state explicitly in the record if unverified: traffic or data volumes, vendor pricing, regulatory applicability, and staffing. Do not present assumed figures as measured facts.

## Operating workflow

1. **Classify the decision.** Write an ADR when the choice is hard to reverse, affects multiple teams or components, introduces a new dependency or protocol, changes a data boundary, or sets a standard others will follow. Skip the ADR for reversible local choices such as a library inside one module.
2. **Check for overlap.** Search existing ADRs for the same question. If one is accepted and still valid, reference it rather than duplicating it. If one conflicts, plan a supersession, not a silent contradiction.
3. **Assign identity.** Use the next free number and a short imperative title, for example "Use message queue for order events." Do not reuse numbers of withdrawn drafts.
4. **Draft the record.** Use these sections: Status, Date, Deciders, Context, Decision drivers, Options considered, Decision, Consequences (positive, negative, and risks), Follow-up actions, Related records.
5. **State the options honestly.** For each option, record at least one concrete advantage and one concrete drawback. Name the criterion that eliminated rejected options.
6. **Set status to Proposed** and circulate for review with a stated deadline.
7. **Resolve review comments** by revising the draft or recording a dissent with reasons. Do not delete objections.
8. **Accept.** Change status to Accepted with the date and deciders. Only the named decision owner or delegated body may do this.
9. **Maintain.** When reality diverges, write a new ADR that supersedes the old one. Mark the old record "Superseded by ADR-NNNN" and link both ways. Do not rewrite its decision text.
10. **Retire** when the decision no longer applies and nothing replaces it. Mark it "Deprecated" with the reason.

## Decision gates

- **Gate 1, need:** Proceed only if the decision meets at least two classification triggers in step 1. Otherwise record the rationale in the design notes instead.
- **Gate 2, completeness:** Proceed to review only if the draft has at least two options, each with pros and cons, and consequences listing at least one risk.
- **Gate 3, acceptance:** Proceed to Accepted only if the named owner has approved, all blocking objections are resolved or recorded as accepted risk, and the date is filled in.
- **Gate 4, supersession:** Supersede only when the new decision contradicts the old one's decision text. Clarifications go into a dated note on the existing record only if the repository convention permits it.

## Verification and evidence

Before moving a record out of Proposed, check:
- Every option cites a source for its claims: a benchmark run, a vendor document, an internal incident, or a measured figure. Each external product claim must be checked against current official documentation, because product features, limits, and pricing change between versions. Mark any unverified claim as such.
- Links to related ADRs resolve.
- Status, date, and deciders fields are all populated.
- Consequences include at least one follow-up action with an owner.

Quality targets: a reviewer can restate the decision and its main trade-off in under 60 seconds; the record is under about four pages; no section is left unfinished.

## Failure handling

- **Disputed decision:** Pause, list the specific objections, and ask the owner to decide. Do not mark Accepted to unblock work.
- **Missing data:** Record the gap as an assumption with a validation task and a target date. Do not invent figures.
- **Discovered contradiction after acceptance:** Draft a superseding ADR and notify affected teams. Do not edit the accepted text.
- **Conflicting numbering:** Stop and reconcile with the repository maintainer before renumbering anything.

## Deliverable contract

The deliverable is one Markdown file per ADR in the agreed directory, plus an updated index listing number, title, status, and date. Each file must contain every section in the workflow template with no placeholders. The final status is Proposed, Accepted, Superseded, or Deprecated. Report back: the file path, the status, the open objections, and any assumptions still unverified.

## What not to do

- Do not create or change accepted ADRs without owner approval.
- Do not delete superseded records or rewrite their decisions.
- Do not record a decision as made when review is still open.
- Do not state vendor capabilities, versions, limits, or compliance coverage from memory; verify against current official documentation.
- Do not publish an ADR externally, or share it with outside parties, without explicit approval, because it may reveal confidential architecture or security posture.
- Do not invent benchmark results, cost figures, or adoption metrics.