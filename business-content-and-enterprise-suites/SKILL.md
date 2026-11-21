---
name: business-content-and-enterprise-suites
description: Use when producing, reviewing, or migrating business content and enterprise suite artifacts (product copy, sales collateral, policy documents, knowledge base articles, templates, and content inside office or CMS suites) that must be accurate, on-brand, governed, and deployable into enterprise systems.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Business Content And Enterprise Suites

## Purpose and boundaries

This skill covers the full lifecycle of business-facing content inside enterprise suites: drafting and editing, structuring templates, localizing, reviewing for claims and compliance exposure, and publishing or migrating content into document, wiki, CMS, or collaboration platforms.

In scope: copy and documents, template and field design, content reuse and variables, approval routing, metadata and taxonomy, bulk transformation of existing content, and export/import between suite tools.

Out of scope: legal opinions, regulatory determinations, financial or medical advice, live pricing changes, and direct administration of identity, permissions, or tenant settings. Hand those to the accountable owner.

## Inputs and assumptions

Before drafting, establish:

1. Audience, channel, and purpose (internal enablement, customer-facing, partner, regulator-facing).
2. Source of truth for every factual claim: product specs, price sheets, policy versions, approved messaging.
3. Brand and style guide version, glossary, and prohibited terms.
4. Target system and its constraints: supported formats, field limits, template syntax, character encodings.
5. Owner, reviewer, and approver for each artifact.
6. Effective date and expiry. Content without a date is treated as unverified.

If a source of truth is missing, stop and request it. Do not infer prices, dates, feature availability, or certifications from memory.

## Operating workflow

1. **Inventory.** List every artifact, its channel, owner, and current version. Flag duplicates and conflicting versions.
2. **Extract claims.** Break content into atomic claims (a number, a date, a feature state, a comparison, an obligation). Map each to a source.
3. **Structure first.** Define sections, required fields, and variables before wording. Keep variable names stable and documented.
4. **Draft.** Write to the glossary. Prefer concrete verbs and specific nouns. Keep one idea per sentence in customer-facing text.
5. **Localize only after the source is approved.** Preserve variables, units, and legal phrasing exactly; flag idioms and culturally sensitive content for native review.
6. **Verify** (see below), then route for approval.
7. **Publish or migrate** in a staging space first. Compare rendered output against the approved source, not against the draft.
8. **Record** the version, approver, effective date, and rollback target.

For bulk migration: export a snapshot, run transformation on a copy, diff sample sets (at least 10% or 50 items, whichever is larger, plus every item containing a number, date, or legal term), and only then apply to production.

## Decision gates

Stop and request explicit human approval before:

- Publishing, sending, or emailing any content to external recipients.
- Overwriting, deleting, or moving a live document, page, or template, or any bulk operation touching more than 20 items.
- Changing a published price, claim, warranty, certification, or regulated statement.
- Writing into shared tenant-wide templates, master libraries, or content used by multiple teams.
- Handling personal data, customer records, or confidential deal terms in content.
- Any action that cannot be reverted from the suite's version history.

Proceed without a gate for drafting, internal review copies, and staging-only changes.

Escalate instead of deciding when a claim conflicts with its source, when two approved sources disagree, or when a required approver is unavailable.

## Verification and evidence

Each deliverable must carry a claim register: claim, source document and version, verifier, date checked.

Measurable checks:

- 100% of numeric values, dates, and product names match the cited source.
- 0 prohibited glossary terms or banned phrases from the style guide.
- All variables render with test data; zero unresolved placeholders or raw template tags in staging output.
- Reading level and sentence length meet the channel standard defined in the style guide; record the tool and score used.
- Links resolve; attachments open; accessibility basics pass (heading order, alt text, table headers).
- Localized copy: variables, units, and legal wording match the source in 100% of sampled strings.

Do not state that content is compliant, certified, or legally sufficient. Report only that it matches the listed sources and passed the listed checks.

## Failure handling

- **Rendering error after import:** roll back to the recorded version, do not patch live content by hand, and log the failing field.
- **Claim cannot be sourced:** remove it from the draft or mark it as pending with an owner and due date. Never keep an unsourced claim.
- **Conflicting sources:** present both with versions and dates; escalate.
- **Bulk transform mismatch above threshold (more than 2% of sampled items):** halt, restore snapshot, and revise the transformation rule.
- **Tool or format limit exceeded:** shorten by removing content, never by silently truncating mid-sentence or dropping legal text.

## Deliverable contract

Every delivery includes:

1. The artifact in the target format, with stable variable names documented in a short table.
2. The claim register.
3. A change summary against the prior version.
4. Verification results with the checks above, marked pass, fail, or not applicable.
5. Open items with owner and due date.
6. Approval status and the explicit gate(s) still awaiting a human decision.

Version-sensitive details (suite feature names, template syntax, import limits, accessibility tooling versions) must be verified against current official vendor documentation before use; do not rely on remembered specifics.

Do not: invent sources, fabricate metrics or testimonials, send or publish without approval, overwrite live content without a snapshot, or claim compliance on the team's behalf.