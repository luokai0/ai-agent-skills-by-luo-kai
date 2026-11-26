# Business, Product, and Strategy

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## architecture-decision-record-lifecycle

**Use when:** Use when proposing, reviewing, accepting, superseding, or retiring an architecture decision record (ADR), or when deciding whether a technical choice needs one.

### Purpose and boundaries

This skill governs how an architecture decision is captured as an ADR, moved through its statuses, linked to related decisions, and eventually superseded or retired. It covers the record itself, not the design work behind it, and not the implementation that follows.

In scope: deciding whether a choice warrants an ADR; drafting context, options, and consequences; running review; recording acceptance; handling supersession; maintaining the index.

Out of scope: writing system design documents, selecting vendors without a decision owner, editing ADRs after acceptance to change their substance, and recording decisions on behalf of people who have not agreed to them.

### Inputs and assumptions

Required inputs:
- The decision question in one sentence.
- The decision owner and the reviewers, by role or name.
- The ADR repository location and numbering scheme already in use. If none exists, propose one and get approval before creating files.
- Constraints: cost, compliance regime, latency or availability targets, team skills, existing platform commitments.
- Candidate options, at least two, including "do nothing" where it is viable.

Assumptions to state explicitly in the record if unverified: traffic or data volumes, vendor pricing, regulatory applicability, and staffing. Do not present assumed figures as measured facts.

### Operating workflow

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

### Decision gates

- **Gate 1, need:** Proceed only if the decision meets at least two classification triggers in step 1. Otherwise record the rationale in the design notes instead.
- **Gate 2, completeness:** Proceed to review only if the draft has at least two options, each with pros and cons, and consequences listing at least one risk.
- **Gate 3, acceptance:** Proceed to Accepted only if the named owner has approved, all blocking objections are resolved or recorded as accepted risk, and the date is filled in.
- **Gate 4, supersession:** Supersede only when the new decision contradicts the old one's decision text. Clarifications go into a dated note on the existing record only if the repository convention permits it.

### Verification and evidence

Before moving a record out of Proposed, check:
- Every option cites a source for its claims: a benchmark run, a vendor document, an internal incident, or a measured figure. Each external product claim must be checked against current official documentation, because product features, limits, and pricing change between versions. Mark any unverified claim as such.
- Links to related ADRs resolve.
- Status, date, and deciders fields are all populated.
- Consequences include at least one follow-up action with an owner.

Quality targets: a reviewer can restate the decision and its main trade-off in under 60 seconds; the record is under about four pages; no section is left unfinished.

### Failure handling

- **Disputed decision:** Pause, list the specific objections, and ask the owner to decide. Do not mark Accepted to unblock work.
- **Missing data:** Record the gap as an assumption with a validation task and a target date. Do not invent figures.
- **Discovered contradiction after acceptance:** Draft a superseding ADR and notify affected teams. Do not edit the accepted text.
- **Conflicting numbering:** Stop and reconcile with the repository maintainer before renumbering anything.

### Deliverable contract

The deliverable is one Markdown file per ADR in the agreed directory, plus an updated index listing number, title, status, and date. Each file must contain every section in the workflow template with no placeholders. The final status is Proposed, Accepted, Superseded, or Deprecated. Report back: the file path, the status, the open objections, and any assumptions still unverified.

### What not to do

- Do not create or change accepted ADRs without owner approval.
- Do not delete superseded records or rewrite their decisions.
- Do not record a decision as made when review is still open.
- Do not state vendor capabilities, versions, limits, or compliance coverage from memory; verify against current official documentation.
- Do not publish an ADR externally, or share it with outside parties, without explicit approval, because it may reveal confidential architecture or security posture.
- Do not invent benchmark results, cost figures, or adoption metrics.


## business-analytics-dashboards

**Use when:** Use when designing, building, reviewing, or troubleshooting business analytics dashboards that report KPIs from warehouses, BI tools, or spreadsheets, including metric definitions, data model checks, visual design, and stakeholder handoff.

### Purpose and boundaries

This skill guides the end-to-end production of decision-support dashboards: scoping the decision a dashboard serves, defining metrics unambiguously, validating the underlying data, laying out visuals, and handing off with documentation. It covers recurring operational dashboards, executive summaries, and ad hoc exploratory views that will be reused.

Out of scope: writing production ETL pipelines, changing source-system schemas, granting data access, making financial or compliance attestations, and forecasting models beyond simple trend context. Route those to data engineering, security, finance, or model-governance owners.

### Inputs and assumptions

Before building, collect:

1. **Decision and audience.** The specific recurring decision (e.g., "reallocate weekly paid-media budget"), who makes it, and how often.
2. **Metric dictionary.** Names, formulas, grain, filters, owners. If absent, draft one and mark it "unconfirmed" until a business owner signs off.
3. **Data sources.** Table or extract names, refresh cadence, known latency, and the system of record for each metric.
4. **Access constraints.** Which fields are personal, confidential, or restricted.
5. **Tooling.** The BI platform and version in use. Treat any feature, function, or connector behavior as version-sensitive; verify against the vendor's current official documentation before relying on it.

Assume data is imperfect until profiled. Assume the requester's stated metric may differ from what the business actually uses; confirm.

### Operating workflow

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

### Decision gates

- **Gate A (scope):** Proceed only when the decision, audience, and KPI list are approved by the requester.
- **Gate B (definitions):** Proceed only when the business owner confirms each metric formula. Unconfirmed metrics must be labeled as such on the dashboard.
- **Gate C (reconciliation):** Publish only when headline figures match the reference source within the agreed tolerance, or variances are explained and accepted in writing.
- **Gate D (access and sensitivity):** Stop and request explicit approval before sharing any dashboard that includes personal, health, financial-account, or otherwise restricted fields, or before publishing outside the original audience.
- **Gate E (publication):** Any action that overwrites a live dashboard, changes shared permissions, schedules external delivery, or alters source tables requires explicit approval from the owner. Do not perform these actions unilaterally.

### Verification and evidence

Record the following evidence with every release:

- Control-total comparison: source rows versus loaded rows, with the difference and reason.
- Null and duplicate rates for key dimensions and identifiers; target thresholds agreed in Gate B.
- Headline reconciliation table: dashboard value, reference value, absolute and percentage variance.
- Date-boundary check: confirm the most recent complete period and that partial periods are labeled.
- Filter test: apply each filter and confirm totals change as expected, including "all" selections.
- Drill-down test: confirm sums of components equal the parent total.

Measurable quality bar: headline reconciliation within the agreed tolerance (commonly 0.5% for revenue-type totals unless the owner specifies otherwise); zero unlabeled partial periods; every visible KPI traceable to a written definition.

### Failure handling

- **Reconciliation mismatch:** Halt publication. Check timezone, date basis, filter inclusion, and duplicate joins in that order. Do not adjust the dashboard formula to force agreement.
- **Missing or late data:** Show the last successful refresh time prominently and mark affected periods as incomplete. Do not impute values silently.
- **Conflicting definitions:** Escalate to the metric owner. Present both definitions with example records and their numeric impact.
- **Performance problems:** Reduce granularity, pre-aggregate at the agreed grain, or limit default date range. Avoid removing definitions to improve speed.
- **Unexpected sensitive fields discovered:** Stop, remove them from the working copy, and request Gate D approval before continuing.

### Deliverable contract

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


## business-content-and-enterprise-suites

**Use when:** Use when producing, reviewing, or migrating business content and enterprise suite artifacts (product copy, sales collateral, policy documents, knowledge base articles, templates, and content inside office or CMS suites) that must be accurate, on-brand, governed, and deployable into enterprise systems.

### Purpose and boundaries

This skill covers the full lifecycle of business-facing content inside enterprise suites: drafting and editing, structuring templates, localizing, reviewing for claims and compliance exposure, and publishing or migrating content into document, wiki, CMS, or collaboration platforms.

In scope: copy and documents, template and field design, content reuse and variables, approval routing, metadata and taxonomy, bulk transformation of existing content, and export/import between suite tools.

Out of scope: legal opinions, regulatory determinations, financial or medical advice, live pricing changes, and direct administration of identity, permissions, or tenant settings. Hand those to the accountable owner.

### Inputs and assumptions

Before drafting, establish:

1. Audience, channel, and purpose (internal enablement, customer-facing, partner, regulator-facing).
2. Source of truth for every factual claim: product specs, price sheets, policy versions, approved messaging.
3. Brand and style guide version, glossary, and prohibited terms.
4. Target system and its constraints: supported formats, field limits, template syntax, character encodings.
5. Owner, reviewer, and approver for each artifact.
6. Effective date and expiry. Content without a date is treated as unverified.

If a source of truth is missing, stop and request it. Do not infer prices, dates, feature availability, or certifications from memory.

### Operating workflow

1. **Inventory.** List every artifact, its channel, owner, and current version. Flag duplicates and conflicting versions.
2. **Extract claims.** Break content into atomic claims (a number, a date, a feature state, a comparison, an obligation). Map each to a source.
3. **Structure first.** Define sections, required fields, and variables before wording. Keep variable names stable and documented.
4. **Draft.** Write to the glossary. Prefer concrete verbs and specific nouns. Keep one idea per sentence in customer-facing text.
5. **Localize only after the source is approved.** Preserve variables, units, and legal phrasing exactly; flag idioms and culturally sensitive content for native review.
6. **Verify** (see below), then route for approval.
7. **Publish or migrate** in a staging space first. Compare rendered output against the approved source, not against the draft.
8. **Record** the version, approver, effective date, and rollback target.

For bulk migration: export a snapshot, run transformation on a copy, diff sample sets (at least 10% or 50 items, whichever is larger, plus every item containing a number, date, or legal term), and only then apply to production.

### Decision gates

Stop and request explicit human approval before:

- Publishing, sending, or emailing any content to external recipients.
- Overwriting, deleting, or moving a live document, page, or template, or any bulk operation touching more than 20 items.
- Changing a published price, claim, warranty, certification, or regulated statement.
- Writing into shared tenant-wide templates, master libraries, or content used by multiple teams.
- Handling personal data, customer records, or confidential deal terms in content.
- Any action that cannot be reverted from the suite's version history.

Proceed without a gate for drafting, internal review copies, and staging-only changes.

Escalate instead of deciding when a claim conflicts with its source, when two approved sources disagree, or when a required approver is unavailable.

### Verification and evidence

Each deliverable must carry a claim register: claim, source document and version, verifier, date checked.

Measurable checks:

- 100% of numeric values, dates, and product names match the cited source.
- 0 prohibited glossary terms or banned phrases from the style guide.
- All variables render with test data; zero unresolved placeholders or raw template tags in staging output.
- Reading level and sentence length meet the channel standard defined in the style guide; record the tool and score used.
- Links resolve; attachments open; accessibility basics pass (heading order, alt text, table headers).
- Localized copy: variables, units, and legal wording match the source in 100% of sampled strings.

Do not state that content is compliant, certified, or legally sufficient. Report only that it matches the listed sources and passed the listed checks.

### Failure handling

- **Rendering error after import:** roll back to the recorded version, do not patch live content by hand, and log the failing field.
- **Claim cannot be sourced:** remove it from the draft or mark it as pending with an owner and due date. Never keep an unsourced claim.
- **Conflicting sources:** present both with versions and dates; escalate.
- **Bulk transform mismatch above threshold (more than 2% of sampled items):** halt, restore snapshot, and revise the transformation rule.
- **Tool or format limit exceeded:** shorten by removing content, never by silently truncating mid-sentence or dropping legal text.

### Deliverable contract

Every delivery includes:

1. The artifact in the target format, with stable variable names documented in a short table.
2. The claim register.
3. A change summary against the prior version.
4. Verification results with the checks above, marked pass, fail, or not applicable.
5. Open items with owner and due date.
6. Approval status and the explicit gate(s) still awaiting a human decision.

Version-sensitive details (suite feature names, template syntax, import limits, accessibility tooling versions) must be verified against current official vendor documentation before use; do not rely on remembered specifics.

Do not: invent sources, fabricate metrics or testimonials, send or publish without approval, overwrite live content without a snapshot, or claim compliance on the team's behalf.


## business-finance-erp

**Use when:** Use when validating, enriching, or reconciling finance ERP master data (vendors, customers, legal entities, tax IDs, bank accounts) against external business registries, tax authority lookups, or identifier registries such as LEI or VAT databases.

### Purpose and boundaries

This skill governs how finance master data is checked against external registries and how the results are applied inside an ERP. It covers: confirming legal names, registration numbers, tax identifiers, registered addresses, and entity status; matching ERP records to registry entries; flagging discrepancies for finance review; and documenting the evidence behind each change.

It does not cover: making payments, changing bank details in production without dual approval, sanctions or AML screening decisions (hand these to compliance), tax filing, or credit decisions.

### Inputs and assumptions

Required inputs:
- Export or list of master records to check (ERP ID, legal name, country, registration number, tax ID, address, bank account reference, status).
- Access to the approved registry sources for each country or identifier type, with the access method the organization has authorized.
- The ERP's current field definitions and mandatory-field rules.

Assumptions to state explicitly in the output:
- Registry data may be stale, partial, or differently formatted by jurisdiction. Registry status is evidence, not proof of legal standing.
- Registry query methods, rate limits, and data licensing terms change. Verify current endpoints, field names, and terms against each registry's official documentation before running a batch.
- Personal data in sole-trader records requires the organization's data-protection basis; do not extract beyond the fields needed.

### Operating workflow

1. Scope the batch: record count, countries, identifier types, and the ERP fields allowed to change. Read-only mode is the default.
2. Normalize inputs: trim whitespace, standardize country codes to ISO 3166-1 alpha-2, strip punctuation from tax IDs per the jurisdiction's format, and record the original value alongside the normalized one.
3. Query registries using the identifier first (registration number, tax ID), then name plus country only as a fallback. Name-only matches are never sufficient for an update.
4. Score each match: identifier exact match plus legal-name similarity above your documented threshold plus active status = auto-confirm candidate. Any other combination = review.
5. Compare field by field: legal name, registration number, tax ID, registered address, entity status, date of incorporation where available.
6. Classify each record: CONFIRMED, DISCREPANCY (specify field), INACTIVE_OR_DISSOLVED, NOT_FOUND, AMBIGUOUS.
7. Produce a change proposal. Do not write to the ERP in this step.

### Decision gates

- **Gate 1, before any query:** Confirm the registry is authorized for this data purpose and jurisdiction. If not, stop.
- **Gate 2, before applying changes:** Any change to legal name, tax ID, or address requires a named approver from the finance master-data owner role. Changes affecting bank account details require a second approver independent of the requester and must be verified through a channel separate from the record itself (for example, a call-back to a number already on file).
- **Gate 3, external impact:** Sending correction requests to vendors or customers, or notifying third parties, requires explicit approval for each batch.
- **Gate 4, deactivation:** Blocking or deactivating a vendor because the registry shows dissolution requires approval. Open invoices and payments must be listed before the block is proposed.

Never auto-apply DISCREPANCY, INACTIVE_OR_DISSOLVED, or AMBIGUOUS results.

### Verification and evidence

Each proposed change must carry:
- Registry name, query timestamp (UTC), identifier used, and the registry's returned record reference.
- Before and after values for each field.
- Match score and the threshold applied.
- Reviewer identity and decision for gated items.

Quality checks, measured per batch:
- Identifier-matched rate: report it; a low rate signals poor source data, not a success.
- Zero auto-applied changes outside the confirmed class.
- Sample audit: re-check at least 5% of CONFIRMED records, or 20 records if fewer, against the registry manually. Any mismatch fails the batch.
- Reconciliation: count of input records equals the sum of all output classes.

### Failure handling

- Registry unavailable or rate-limited: pause, record the last completed index, resume later. Do not retry in a tight loop.
- Schema or field change returned by the registry: stop the batch and flag for verification against current documentation.
- Conflicting results from two registries: classify AMBIGUOUS and escalate.
- ERP write error mid-batch: halt writes, produce a rollback list from the before-values, and obtain approval before reversing.

### Deliverable contract

Return:
1. Batch summary: records in, records per class, identifier-matched rate, sample audit result.
2. Change proposal table: ERP ID, field, current value, proposed value, source reference, class, gate required.
3. Escalation list: every item needing approval, with the approver role.
4. Assumptions and unverified items, including any registry endpoint or field detail not confirmed against current official documentation.

Do not: invent registry field names; state that a vendor is legally compliant or creditworthy; apply bank changes from registry data; merge duplicate vendors without a separate approved merge review; or represent registry data as guaranteed accurate.


## business-saas-operations

**Use when:** Use when administering, auditing, or changing business SaaS tool configurations (CRM, helpdesk, HR, finance, collaboration suites) that are reached through external registries, marketplaces, or app directories, including vendor onboarding, app listing reviews, integration setup, and access reconciliation.

### Purpose and boundaries

This skill guides operators through the lifecycle of business SaaS tools that are discovered, installed, or connected via external registries: vendor marketplaces, app directories, package feeds for SaaS extensions, and third-party integration catalogs. It covers vetting listings, planning installs, configuring integrations, reconciling access, and documenting the result.

In scope: listing and publisher review, permission-scope analysis, sandbox trials, configuration changes in non-production tenants, access-role mapping, integration runbooks, and operational handoff.

Out of scope: writing vendor code, negotiating contracts, legal compliance determinations, and production changes that have not passed the decision gates below.

### Inputs and assumptions

Before acting, collect:
- Tool name, vendor, registry source, and the exact listing or identifier.
- Business owner and the process the tool supports.
- Target environment (sandbox, staging, production) and tenant identifiers.
- Requested permissions or scopes, and the data categories they would touch (customer PII, financial records, employee data, credentials).
- Current access-control model: roles, groups, admin owners.
- Change window and rollback owner.

Assume nothing about a listing's safety, publisher identity, or currency of documentation. Treat vendor claims as unverified until checked against the vendor's own official documentation.

### Operating workflow

1. **Record the request.** Write a one-paragraph statement: what the tool does for the business, who uses it, and what data it will touch.
2. **Verify the source.** Confirm the registry is the vendor's official marketplace or a vetted directory. Check publisher verification status, listing ownership history, and install counts only as weak signals. Note the listing's last-updated date.
3. **Map permissions.** List every requested scope or permission. For each, state the reason it is needed and the minimum alternative. Flag any scope granting write access to records, admin rights, or unrestricted data export.
4. **Assess data flow.** Draw the path: source system to tool to destination. Identify where data is stored, which region, and what retention the vendor documents. Mark anything the vendor does not document as unknown.
5. **Trial in a non-production tenant.** Install with the narrowest scope. Use synthetic or anonymized data. Record every API call, webhook, and outbound domain observed during the trial.
6. **Compare trial against declared behavior.** Any undeclared outbound destination, scope use beyond the stated purpose, or unexpected data volume is a stop condition.
7. **Draft the production change plan.** Include steps, owner, rollback procedure, role mapping, and monitoring checks.
8. **Obtain approval** at Gate C, then execute during the agreed window.
9. **Reconcile post-change.** Confirm access lists match the approved role map and remove trial credentials.

### Decision gates

- **Gate A (source):** Proceed only if the listing is from the vendor or a publisher the organization has already vetted. Unverified publishers require security review before any trial.
- **Gate B (scope):** Proceed to trial only if every scope maps to a documented business need. Reject or narrow any scope granting admin, bulk export, or cross-tenant access.
- **Gate C (production):** Requires explicit written approval from the business owner and the system administrator, plus a security reviewer for any tool touching customer, financial, or employee data. Approval must name the scopes, environment, and change window.
- **Stop condition:** Halt immediately on undeclared network destinations, credential requests outside the approved flow, or unexplained data volume spikes.

Example: a helpdesk add-in requests "read all tickets and all attachments" for a reporting need that only requires ticket status and category. Narrow the scope or reject; do not approve the broad request and rely on later policy.

### Verification and evidence

Each gate must produce a retained artifact:
- Listing review record: URL, publisher, verification status, capture date.
- Permission matrix: scope, justification, minimum alternative, decision.
- Trial log: observed endpoints, data fields sent, error rates.
- Approval record: approver names, date, scopes, environment.
- Post-change reconciliation: diff of expected versus actual role assignments, showing zero unexplained entries.

Quality checks:
- 100% of requested scopes have a documented justification.
- Zero undeclared outbound domains in trial logs.
- Access reconciliation shows no orphaned trial accounts after 24 hours.
- Rollback procedure has been rehearsed in the non-production tenant at least once.

Version-sensitive details (API scope names, permission identifiers, marketplace policies, vendor data-residency terms, and certification claims) must be checked against the vendor's current official documentation at the time of review. Record the documentation URL and access date. Do not rely on memory or on cached listing text.

### Failure handling

- **Trial fails:** Capture the error, the scope or endpoint involved, and the vendor's documented behavior. Do not broaden scopes to make the trial pass. Escalate to the vendor or reject the tool.
- **Undeclared behavior found:** Stop, preserve logs, notify the security reviewer, and disable the integration credential. Do not delete logs.
- **Production change causes errors:** Execute the rollback plan at once. Notify the business owner. Record the timeline.
- **Listing changes after approval:** Re-run Gates A and B before any further update.
- **Approver unavailable during window:** Postpone. Do not self-approve.

### Deliverable contract

Each engagement ends with a single review package containing:
1. Summary (under 150 words): tool, purpose, decision, and residual risk.
2. Listing review record and permission matrix.
3. Data flow diagram or table with unknowns explicitly marked.
4. Trial log summary and comparison to declared behavior.
5. Approval record and change plan with rollback steps.
6. Post-change reconciliation result.
7. Open items with named owners and due dates.

What not to do:
- Do not install from unverified listings or sideload packages into production.
- Do not grant admin or bulk-export scopes as a convenience.
- Do not test with real customer or employee records.
- Do not store vendor credentials in tickets, chat, or documentation; reference the secrets manager entry instead.
- Do not treat registry ratings or install counts as evidence of security.
- Do not state that a tool is compliant with any regulation or certification unless the vendor's current documentation and your internal assessment confirm it.


## domain-modeling

**Use when:** Use when designing or reviewing a domain model for a software system, including bounded contexts, aggregates, invariants, domain events, or context maps, or when code and data structures appear to disagree with the business rules they encode.

### Purpose and boundaries

Produce a model of the business domain that makes rules, vocabulary, and ownership explicit enough to drive design and code. In scope: identifying bounded contexts, naming concepts in the domain's own language, locating aggregates and their invariants, classifying entities versus value objects, defining domain events, and mapping relationships between contexts.

Out of scope: choosing infrastructure, selecting databases or frameworks, writing production code without a separate task, and estimating delivery effort. Do not treat a data-model diagram as a domain model; a domain model captures behavior and rules, not only tables.

### Inputs and assumptions

Required inputs: at least one of the following, with its source identified: domain experts' descriptions, existing requirements, process documents, current code or schemas, incident reports, or support tickets. Record which sources are authoritative for which rules.

Assumptions to state explicitly before modeling: who the domain experts are, which decisions the model must support, and which stakeholders will change the model later. If a rule has no identified owner, mark it as unverified rather than encoding it.

### Operating workflow

1. **Glossary first.** Collect the terms experts use for core concepts. Record each term with its definition and at least one counterexample of what it does not mean. Flag terms used with different meanings by different groups.
2. **Find context boundaries.** Look for places where the same word means different things, where different teams own different decisions, or where data is translated at a handoff. Draw one bounded context per coherent meaning. Name each context in domain language.
3. **Identify aggregates per context.** For each state change, ask which data must be consistent together in one transaction. Make the aggregate root the only entry point for changes.
4. **Write invariants as testable statements.** Example: "An order cannot be confirmed while its total is zero" or "A reservation's quantity never exceeds available stock at the time of confirmation." Each invariant names the aggregate that enforces it.
5. **Classify objects.** Use entities where identity matters across time (a customer account). Use value objects where equality by attributes is sufficient (a monetary amount with currency). Prefer value objects when in doubt.
6. **Define domain events** as past-tense facts emitted by an aggregate (for example, "PaymentCaptured"). Record the producer, the consumers, and what each consumer does with it.
7. **Map context relationships.** For each boundary crossing, record the direction of dependency, the translation direction, and the relationship type (for example, upstream/downstream, shared kernel, anticorruption layer, or published language). Use these labels as design vocabulary, not as a claim about any tool.

### Decision gates

- **Split a context** when two teams need to change the same rule for different reasons, or when a term's definition differs in a way that changes outcomes.
- **Merge contexts** when the translation between them is trivial and they always change together.
- **Create an aggregate boundary** only when the invariant truly requires atomic consistency. If consistency across the boundary is acceptable eventually, use an event instead.
- **Stop and escalate** when experts disagree on a rule that affects money, legal obligations, access rights, or personal data. Do not resolve these by assumption.

### Verification and evidence

Each model deliverable must satisfy these checks:

- Every glossary term appears in at least one rule or event, or is marked as unused.
- Every invariant names exactly one enforcing aggregate and cites its source.
- Every aggregate has a root and no external object mutates its internals.
- Every domain event has a named producer and at least one named consumer or an explicit "no consumer yet" note.
- Walkthrough check: a domain expert reviews three real scenarios (one normal, one edge, one failure) and confirms the model produces the expected outcome for each. Record the scenarios and the sign-off.
- Where existing code exists, compare each invariant against the code path that enforces it and list mismatches.

### Failure handling

- **Expert unavailable:** Keep the model in draft status, list the unverified rules, and do not promote them to specification.
- **Conflicting sources:** Record both versions, identify the owner, and request a decision. Do not silently pick one.
- **Code contradicts documented rules:** Report the discrepancy with file and location. Do not modify code to match the model without approval.
- **Model grows beyond the decision it serves:** Narrow the scope to the decisions currently needed and defer the rest in an explicit backlog list.

### Deliverable contract

Produce a single document with these sections in order: scope and decisions supported; glossary; bounded contexts with purpose and owner; aggregates with roots and invariants; entity and value object classification; domain events with producers and consumers; context map; open questions with owners; verification record listing the scenarios and sign-offs.

Mark any statement about a specific tool, notation standard, or framework feature as requiring verification against current official documentation before adoption.

### Approval controls

Obtain explicit approval before: altering or deleting existing production schemas, migrations, or event contracts; sharing domain documents containing personal, financial, or confidential data outside the approved group; and publishing a model that other teams will implement against. Do not make these changes as a side effect of modeling.


## executive-strategy-advisory

**Use when:** Use when a user needs structured strategic analysis for an executive decision, such as market entry, portfolio prioritization, build-versus-buy, pricing or restructuring options, or a board-ready recommendation grounded in evidence.

### Purpose and boundaries

This skill turns an ambiguous executive question into a decision-ready strategic analysis: framed options, explicit assumptions, quantified trade-offs, a recommendation with conditions, and a clear list of what would change the answer.

In scope: market entry and expansion, portfolio prioritization, build/buy/partner decisions, pricing and packaging strategy, cost restructuring, capital allocation, and preparation of board or leadership memos.

Out of scope: legal, tax, or securities advice; personnel decisions about named individuals; final financial figures presented as audited; any action that changes systems, contracts, public communications, or money. Recommendations are advisory; the executive owns the decision.

### Inputs and assumptions

Before analysis, establish:

1. Decision statement: the single choice to be made, the decider, and the decision date.
2. Objective and constraints: target metric (revenue, margin, share, risk reduction), time horizon, budget ceiling, regulatory or contractual limits.
3. Available evidence: data the user supplied, and its source and recency.
4. Stakeholders affected and their likely objections.
5. Reversibility: whether the decision can be undone and at what cost.

If the decision statement or objective is missing, ask one consolidated question set rather than assuming. Label every unverified input as an assumption with an owner and a confidence level (high, medium, low). Never fabricate market sizes, competitor figures, or customer counts; mark them "to be sourced" and state the estimation method if you use a proxy.

### Operating workflow

1. Frame the decision in one sentence and list success criteria as measurable thresholds.
2. Generate at least three options, including a status-quo or do-nothing baseline and one option the user has not proposed.
3. For each option, document: cost range, time to impact, dependencies, reversibility, risk exposure, and effect on the primary metric.
4. Build a simple comparison: score each option against weighted criteria. State weights before scoring and show the sensitivity: which weight change flips the ranking.
5. Stress-test the leading option with a pre-mortem: assume it failed in twelve months and list the three most likely causes.
6. Define leading indicators and kill criteria: the measurable signal that confirms progress and the threshold that triggers reconsideration.
7. Draft the recommendation with conditions, sequencing, and the first 30 days of actions.

### Decision gates

Proceed to recommendation only when:
- The decision statement and success metric are agreed.
- At least two options have quantified or bounded impact.
- Key assumptions with low confidence are either validated or explicitly accepted by the decider.

Escalate to the human decider (do not resolve independently) when:
- The recommended option is irreversible, exceeds the stated budget ceiling, or creates external commitments.
- Evidence conflicts materially and the conflict changes the ranking.
- The analysis touches legal exposure, safety, employee welfare, or regulated reporting. Flag these for specialist review.

Require explicit written approval from the user before any step that sends communications, modifies records or systems, signs or commits to vendors, or publishes figures externally. Default to drafting, not executing.

### Verification and evidence

Each claim in the deliverable must carry one of: a cited source supplied by the user, a calculation shown with inputs, or an assumption label. Checks before delivery:

- Arithmetic reproduced: every derived number traces to its inputs.
- Ranges, not single points, for forecasts; the spread is stated.
- Sensitivity check: the recommendation holds under at least one plausible adverse change to the top assumption, or the dependency is named.
- Contradiction scan: no option is evaluated on criteria it fails elsewhere.
- Recency: data older than the stated horizon is flagged.

Do not claim benchmark results, industry statistics, or regulatory compliance outcomes unless the user provided them or they are verifiable from a named current source. Any reference to product features, tool APIs, or software versions must be marked "verify against current official documentation."

### Failure handling

- Insufficient data: deliver a provisional analysis with a named list of the three data gaps that most affect the ranking, and the cost of obtaining each.
- Options tie within the margin of error: say so, and recommend the option with the lower reversibility cost or a staged test.
- User demands a single answer despite low confidence: give the recommendation, the confidence level, and the single assumption that would most change it.
- Request drifts into out-of-scope advice: state the boundary, provide the strategic framing only, and recommend qualified specialist review.

### Deliverable contract

Produce a memo of 500 to 650 words (excluding tables) with these sections in order:

1. Decision and success metric (one sentence each).
2. Recommendation (one paragraph, with conditions).
3. Options comparison table: option, cost range, time to impact, reversibility, primary metric effect, score.
4. Key assumptions with confidence and owner.
5. Top three risks with pre-mortem causes and mitigations.
6. Leading indicators and kill criteria with thresholds.
7. First 30 days: actions, owners as roles, approval-required items marked.
8. Open evidence gaps.

Quality bar: every number is traceable, every option is compared on identical criteria, and a reader can reverse the recommendation by changing a named assumption. Do not include filler summaries, unsupported superlatives, or generic management frameworks without application to the specific facts.


## gtm-strategy

**Use when:** Use when planning, reviewing, or rewriting a go-to-market strategy for a product, service, or market entry, including ICP definition, channel selection, pricing-to-channel fit, launch sequencing, and GTM metrics.

### Purpose and boundaries

This skill produces or audits a go-to-market (GTM) strategy: who the offer is for, why they buy now, how they will hear about it, how they will buy, who sells and supports it, and how success is measured. It covers B2B and B2C offers, new products, new segments, and new geographies.

Out of scope: brand identity design, legal review of contracts or regulated claims, financial audits, and executing paid campaigns or outbound sends. The skill recommends; a human owner approves and executes.

### Inputs and assumptions

Collect these before drafting. Mark any missing item as an explicit assumption with an owner and a validation date.

1. Offer: what is sold, price points, delivery model, and what is not included.
2. Evidence of demand: pipeline, waitlist, pilot results, win/loss notes, retention data. Distinguish stated interest from paid commitment.
3. Target market: candidate segments, firmographic or demographic criteria, and known exclusions.
4. Constraints: budget, headcount, sales cycle length, regulatory limits on claims or outreach, and deadline.
5. Competitive alternatives: what buyers use today, including "do nothing" and spreadsheets.
6. Unit economics: target CAC, payback period, gross margin, and average contract or order value.

If demand evidence is only opinion, label the strategy "hypothesis-stage" and limit commitments to tests.

### Operating workflow

1. **State the wedge in one sentence.** Format: "For [segment with a specific trigger], [offer] replaces [current alternative] by [measurable difference]." If you cannot write it, stop and return to segmentation.
2. **Define the ICP with disqualifiers.** List 3 to 5 firmographic or behavioral criteria and 2 disqualifiers. Example: "Logistics firms with 200–1,000 employees running more than one warehouse management system; disqualify those with an in-house platform team of 10+."
3. **Map buying committee and trigger events.** Name the economic buyer, champion, and blocker. List 2 to 4 triggers (new regulation, funding round, failed vendor, hiring spike) that move a prospect from passive to active.
4. **Select 2 to 3 primary channels** by scoring each candidate (1–5) on: reach into the ICP, expected CAC, time to first revenue, and control over timing. Drop any channel scoring below 3 on reach.
5. **Set pricing-to-channel fit.** Self-serve channels need low-friction prices and trial paths; enterprise channels need procurement-ready packaging and a discount floor. Do not sell an enterprise contract through a checkout flow.
6. **Sequence the launch in three phases:**
   - Pilot (4–8 weeks): 5–15 design partners, paid where possible, with a written success definition.
   - Controlled expansion (1–2 quarters): one channel scaled with weekly conversion review.
   - Broad availability: only after payback and retention thresholds in the gates below are met.
7. **Assign sales and support motions.** Specify who handles inbound, qualification, demo, close, onboarding, and expansion, with handoff criteria between them.
8. **Define metrics and review cadence.** Required metrics: qualified pipeline created per week, stage conversion rates, CAC by channel, win rate, sales cycle days, 90-day retention, and net revenue retention for recurring offers.

### Decision gates

Advance only when each gate is met with evidence.

- **Gate A, Problem:** At least 10 ICP interviews or 5 signed pilots show the problem is ranked top-3 by the buyer. Fail if the majority cite "nice to have."
- **Gate B, Channel:** One channel produces qualified opportunities at a cost within 1.5x target CAC for 6 consecutive weeks. Fail if no channel meets this after two test cycles; re-examine the ICP before adding spend.
- **Gate C, Economics:** Projected payback is within the agreed period using observed conversion, not planned conversion. Require a sensitivity check at 50% of expected win rate.
- **Gate D, Scale:** Pilot retention or usage meets the pre-agreed threshold and support load per customer is documented.

### Verification and evidence

- Every numeric claim in the strategy cites its source (CRM export, interview log, experiment ID) or is labeled an assumption.
- Test each channel assumption with a named experiment: hypothesis, metric, sample size, stop rule, and result.
- Check the ICP against actual closed-won accounts: at least 70% should match the stated criteria. If not, the ICP is wrong, not the buyers.
- Cross-check pricing against the three most common alternatives a buyer would consider.
- Re-verify any platform, tool, or ad-policy constraint against current official documentation before recommending it, since these change frequently.

### Failure handling

- **Low conversion:** Separate lead-quality problems (ICP mismatch) from offer problems (value unclear) from process problems (slow follow-up). Diagnose from stage-level data before changing anything.
- **Conflicting stakeholder priorities:** Surface the trade-off in writing with options and their metric impact; escalate to the decision owner. Do not silently pick one.
- **Missing data:** Replace the metric with a dated assumption and a collection plan. Do not infer numbers from comparable companies without labeling them as borrowed.
- **Gate failure:** Return to the earlier step the failed gate depends on. Do not skip ahead to spend more.

### Deliverable contract

The output is a single document containing, in order:

1. Wedge statement and ICP with disqualifiers.
2. Buying committee and trigger list.
3. Channel scorecard with selected channels and rationale.
4. Pricing and packaging mapped to each channel.
5. Three-phase launch plan with dates relative to start, owners, and gate criteria.
6. Metrics table: definition, target, source system, owner, review frequency.
7. Assumptions register: each assumption, confidence level, validation method, due date.
8. Risks and kill criteria.

Length: as long as needed to be executable, usually 4 to 8 pages. Every section must name an owner.

### What not to do

- Do not claim market size, growth rates, or competitor figures without a cited source.
- Do not recommend spend on a channel before the ICP is validated.
- Do not promise outcomes such as revenue, conversion, or compliance status.
- Do not launch outbound sends, paid campaigns, pricing changes, or customer communications without explicit human approval; these are external and often irreversible.
- Do not delete or overwrite existing CRM records, pipeline data, or prior strategy versions; create new versions instead.
- Do not present GTM tooling features, API parameters, or platform limits from memory; mark them for verification against current vendor documentation.


## knowledge-documents-legal-productivity

**Use when:** Use when drafting, summarizing, or maintaining legal knowledge documents (memos, clause libraries, precedent summaries, filing checklists, entity briefs) that rely on records from external registries such as corporate, IP, land, court, or regulatory registers.

### Purpose and boundaries

This skill produces and maintains legal knowledge documents whose factual claims come from external registries. It covers: extracting facts from registry records, reconciling them across sources, drafting reusable documents with traceable provenance, and flagging stale or conflicting entries.

It does not cover: giving a final legal opinion, filing or submitting anything to a registry, altering registry data, or advising on jurisdictions where the user has not confirmed applicable law. Output is a working draft for a qualified reviewer.

### Inputs and assumptions

Required inputs:
- The document purpose (memo, clause library entry, entity brief, deadline tracker, precedent note).
- The registry records or extracts supplied by the user, with source name, jurisdiction, and retrieval date.
- The intended audience and jurisdiction.

Assumptions to state explicitly in the document:
- Registry data reflects the record as of the retrieval date, not necessarily today.
- Registry field names, fee schedules, filing deadlines, and portal behavior change. Treat any such detail as version-sensitive and mark it "verify against current official documentation."
- Records are not guaranteed complete or accurate. Registries can lag filings, contain typos, or reflect pending changes.

If a required input is missing, ask for it. Do not fill gaps from memory.

### Operating workflow

1. **Scope the document.** Write one sentence stating the question the document answers and its jurisdiction. If it answers more than one question, split it.
2. **Inventory sources.** List each registry record with: registry name, jurisdiction, record identifier, retrieval date, and whether it is an official extract or a third-party copy.
3. **Extract facts into a table.** One row per fact: field, value, source ID, retrieval date. Quote values exactly, including punctuation and date formats.
4. **Reconcile conflicts.** Where two sources disagree, record both values and do not choose silently. Rank by authority: official registry extract over secondary compilation; more recent retrieval over older; filed document over summary.
5. **Draft the body.** Each factual sentence must cite a row in the fact table. Analysis sentences must be labelled as analysis.
6. **Add a freshness block.** Date of retrieval, date of next review, and triggers for re-check (filing events, statutory changes, name changes, insolvency notices).
7. **Run the verification checks** in the next section before presenting.

### Decision gates

Stop and request explicit approval before:
- Submitting, amending, or certifying anything with a registry or court.
- Sending the document to a counterparty, client, or regulator.
- Overwriting or deleting an existing knowledge document that other matters rely on; create a new version instead.
- Including personal data beyond what the purpose requires (identity numbers, home addresses, dates of birth). Redact by default.
- Relying on a single unofficial source for a fact that carries legal consequence (ownership, insolvency status, deadlines, sanctions screening).

Proceed without a gate when the task is internal drafting from supplied, cited records and no external action is taken.

### Verification and evidence

Before presenting, confirm:
- Every factual sentence maps to a fact-table row. Target: zero uncited facts.
- Every source row has an identifier and a retrieval date. Target: 100% completeness.
- All conflicts are listed in a "Discrepancies" section, not resolved silently.
- Dates are normalized to ISO 8601 in the table, with the original string preserved alongside.
- Deadlines are computed from a stated rule and anchor date, and shown with the rule text.
- Version-sensitive items are marked for verification.

Report the counts: facts extracted, sources used, discrepancies found, items marked for verification.

### Failure handling

- **Source unavailable or unreadable:** mark the affected section "unverified," do not infer content, and list what is needed to complete it.
- **Conflicting official sources:** present both, state the conflict, and escalate. Do not average or merge values.
- **Stale record (retrieval older than the document's review window):** flag in the freshness block and require re-retrieval before reuse.
- **Jurisdiction unclear:** stop and ask. Do not default to a home jurisdiction.
- **Requested conclusion exceeds the sources:** state what the sources do not establish.

### Deliverable contract

The final document contains, in order:
1. Title, question answered, jurisdiction, and author identity supplied by the reviewer before publication.
2. Summary (maximum 150 words), every claim cited.
3. Fact table with source IDs and retrieval dates.
4. Analysis, clearly labelled.
5. Discrepancies and open items.
6. Freshness block and re-check triggers.
7. Verification report with the counts listed above.

Do not include: unsourced legal conclusions, personal data beyond stated need, claims of registry or regulatory compliance, or any statement that a filing was made or approved.


## market-analysis

**Use when:** Use when a user asks for analysis of a financial market, asset, sector, or trading setup, including price and volume behavior, macro or sector context, positioning, or a written market view that must be checked against data before use.

### Purpose and boundaries

This skill produces structured, evidence-backed analysis of a named market, instrument set, or sector over a stated horizon. Typical outputs: a market briefing, a thesis with invalidation conditions, a comparison of instruments, or a review of a trading setup's risk profile.

In scope: descriptive analysis of price, volume, volatility, spreads, term structure, fundamentals, macro releases, and positioning data that the user supplies or that is publicly available and cited.

Out of scope: placing or modifying orders, giving personalized recommendations for a specific person's portfolio, using material non-public information, and asserting future returns as fact. Analysis is conditional: state what would make the view wrong.

### Inputs and assumptions

Before analysis, confirm and record:

1. **Instrument identifiers**: ticker, contract month, currency, exchange, and whether prices are adjusted for splits, dividends, or rolls.
2. **Horizon**: intraday, days, weeks, or quarters. Methods differ by horizon.
3. **Data vintage**: timestamp and source of every series. Flag any series older than the stated horizon warrants.
4. **Purpose**: research note, internal risk review, or idea generation. Each carries different disclosure needs.
5. **Constraints**: benchmark, sector, liquidity requirements, and any restricted-list status the user reports.

Assumptions must be written down explicitly. Do not assume data is clean, continuous, or survivorship-free. Do not assume a user's position size, cost basis, or mandate unless provided.

### Operating workflow

1. **Define the question** in one sentence, including the horizon and the decision it informs.
2. **Establish the regime**: trend versus range (e.g., moving-average slope and realized volatility relative to its 1-year range), volatility level, and correlation to a relevant benchmark.
3. **Analyze price and volume**: identify support and resistance only where price has reacted repeatedly; check whether volume confirms moves; note gaps and their fill status.
4. **Add context**: scheduled macro events within the horizon, earnings or guidance dates, rate and currency drivers, and sector rotation evidence.
5. **Check positioning and flows** if data is available: futures open interest changes, fund flow reports, options skew. Label inferred positioning as inference.
6. **Build the thesis**: state the base case, the bull and bear alternatives, and the observable conditions that would falsify the base case.
7. **Quantify risk**: give a historical drawdown range for the instrument over comparable windows, and the expected move implied by options or by realized volatility, naming which one is used.
8. **Compose the market analysis** in the required structure below.

### Decision gates

- **Gate A (data)**: If any core series has a missing span longer than 5% of the window, or prices are unadjusted across corporate actions, stop and request corrected data or disclose the limitation prominently.
- **Gate B (horizon mismatch)**: If the user asks for a multi-month view based only on intraday data, downgrade the conclusion to a short-horizon observation.
- **Gate C (approval required)**: Obtain explicit user approval before any of the following: sending analysis outside the user's organization, using licensed or paid data beyond what the user has confirmed they hold, producing content that names a specific security as a buy or sell for distribution, or any step that would transmit client or account information.
- **Gate D (sensitive information)**: If the input contains apparent non-public information, halt, do not use it, and tell the user to route the matter to their compliance function.

### Verification and evidence

Every quantitative claim needs a source, a date, and a calculation note. Before finalizing:

- Recompute at least two headline figures (returns, volatility, percentage moves) from raw data and confirm agreement within rounding.
- Confirm that date alignment across series is correct, especially across time zones and holidays.
- Check that each thesis has at least one explicit falsification condition that is observable and dated.
- Mark anything version-sensitive, such as exchange rules, contract specifications, index methodology, or regulatory thresholds, as requiring verification against current official documentation.
- Do not supply benchmark statistics, backtest results, or performance figures from memory. Use only figures the user provides or cited sources.

### Failure handling

- **Conflicting sources**: report both values, state which is primary and why, and do not average them silently.
- **Insufficient data**: narrow the claim to what the data supports and list the specific missing inputs.
- **User pushes for certainty**: restate the probabilistic nature of the view and the falsification conditions. Do not inflate confidence.
- **Stale data discovered after drafting**: revise, mark the change, and re-run the verification checks.

### Deliverable contract

The output must contain, in order:

1. Question, horizon, and data vintage.
2. Summary view in no more than five sentences.
3. Regime and evidence table with source and date per row.
4. Base, bull, and bear cases, each with its falsification condition.
5. Risk figures with stated method.
6. Assumptions and data limitations.
7. Verification log: checks performed and results.
8. Required approvals outstanding, if any.

Do not: present forecasts as certainties, omit the falsification conditions, use undated figures, recommend position sizes for unnamed accounts, or present the analysis as individualized investment advice.

### Ultron routing contract

**Choose this skill when:** the objective is to understand price and market behavior over a defined horizon: trend and structure, volume, volatility, spreads, liquidity, positioning, term structure, event reaction, scenario analysis, or a trading setup's risk and invalidation conditions.

**Choose `finance-market-analysis` when:** the question requires issuer-level financial statements, regulatory filings, corporate events, identifier reconciliation, accounting normalization, peer fundamentals, or valuation calculations grounded in reported records.

**Handoff contract:** receive verified issuer/instrument identifiers, filing periods, accounting basis, sourced fundamental metrics, and event dates from the finance skill when those facts matter. Return a conditional market view with horizon, observations, assumptions, risks, and explicit invalidation conditions. Never convert a market scenario into a guaranteed return or personalized order instruction.

#### Related boundary: commercial market intelligence

For competitor landscapes, vendor feature comparisons, commercial pricing and packaging, market sizing, or product positioning in data/AI markets, route to market-and-competitive-intelligence. This skill remains responsible for financial instrument and sector behavior over a defined horizon: price, volume, volatility, spreads, positioning, and conditional market theses. Keep commercial facts separate from traded-market observations.

**Why the boundary exists:** market behavior and issuer fundamentals inform each other, but they are different evidence classes with different time horizons and failure modes.


## market-and-competitive-intelligence

**Use when:** Use when researching markets, competitors, pricing, vendor positioning, or AI/data product landscapes and need a sourced, dated, decision-ready brief with explicit confidence levels.

### Purpose and boundaries

This skill produces sourced, dated, decision-oriented analysis of markets, competitors, and product landscapes in the data and AI domain: data platforms, analytics tools, ML/AI model providers, MLOps tooling, data infrastructure vendors, and AI application categories.

In scope: market sizing logic, competitor feature and positioning comparison, pricing and packaging analysis, go-to-market signals, partnership and integration mapping, hiring and roadmap signals drawn from public sources, and identification of gaps or threats.

Out of scope: non-public information obtained through deception, pretexting, or access to systems you are not authorized to use; reverse engineering of proprietary code; contacting competitor employees or customers under a false identity; investment or legal advice; guaranteed forecasts.

### Inputs and assumptions

Before starting, confirm:
- The decision the brief supports (e.g., enter a segment, price a tier, pick a partner, prioritize a feature).
- The geography, buyer segment (SMB, mid-market, enterprise, public sector), and time horizon.
- The competitor set. Ask for it if not given; propose a candidate set of 5 to 10 with reasons for inclusion and exclusion.
- Permitted sources: public websites, documentation, filings, pricing pages, changelogs, job postings, conference talks, analyst summaries the user has access to, and user-provided internal data.

Assumptions must be written down with a label. Pricing, feature availability, and certifications change frequently; treat any value captured more than 90 days ago as stale unless re-verified.

### Operating workflow

1. Define the question in one sentence and the decision it feeds. Reject open-ended "tell me about the market" requests until narrowed.
2. Build the competitor set. Include direct competitors, adjacent platforms that could expand into the segment, open-source alternatives, and the buyer's status quo (in-house build, spreadsheets, incumbent suite).
3. Create a fact register: one row per claim with columns for claim, value, source URL, capture date, and confidence (high: primary source and recent; medium: secondary or older than 90 days; low: inferred or single unverified source).
4. Collect across dimensions: target customer, core use case, architecture and deployment model (cloud, self-hosted, hybrid), integrations, data residency options, pricing model and published tiers, support and SLA terms as published, roadmap signals, partnerships, and customer proof points.
5. Triangulate. Any claim that drives a recommendation needs at least two independent sources or one primary source plus a dated corroborating signal.
6. Analyze: map positioning against buyer criteria, identify where competitors are weak or crowded, estimate sizing using explicit bottom-up inputs with stated ranges, and list threats with likelihood and impact.
7. Write the brief using the deliverable contract below.

### Decision gates

- Gate A (scope): Stop if the decision, segment, or geography is undefined. Do not proceed on assumptions alone.
- Gate B (sources): Stop before analysis if more than a third of decision-relevant claims are low confidence. Collect more sources or downgrade the conclusions.
- Gate C (sensitive collection): Require explicit user approval before accessing any login-gated competitor material, using scraping at volume, contacting third parties, or handling customer or employee personal data.
- Gate D (external use): Require explicit approval before publishing, sharing outside the requesting team, or sending the brief to vendors, partners, or investors.
- Gate E (pricing actions): Do not present a recommended price as final. Require approval from the accountable owner before any external pricing change.

### Verification and evidence

Quality checks, all required:
- Every quantitative claim has a source URL and capture date.
- Every competitor feature claim cites the vendor's current documentation or a dated changelog entry, not marketing copy alone.
- Each claim in the recommendations section maps to at least one fact register row.
- Sizing shows formula, inputs, ranges, and sensitivity to the largest input.
- Version-sensitive details (model names, tier limits, supported regions, certifications, API features) are marked "verify against current official documentation" unless confirmed in the last 30 days.
- No figures are rounded in a way that changes the conclusion.
- The brief distinguishes observed facts, vendor claims, and analyst inference.

### Failure handling

- Paywalled or unavailable source: record the gap, mark dependent claims low confidence, and do not infer the content.
- Conflicting figures: report both with sources, explain the likely reason (scope, date, currency, definition), and do not average them silently.
- Vendor pricing "contact sales": record as undisclosed. Do not estimate without flagging it as a model assumption.
- Stale data discovered mid-analysis: re-capture or downgrade confidence; do not patch with memory.
- Insufficient evidence for a recommendation: say so and state what evidence would change the conclusion.

### Deliverable contract

The brief contains, in order:
1. Decision and question (one paragraph).
2. Bottom line (three to five sentences, with confidence level).
3. Competitor set with inclusion rationale.
4. Comparison table: dimensions by competitor, each cell tied to a fact register ID.
5. Findings, each with evidence IDs and confidence.
6. Sizing, if requested, with formulas and ranges.
7. Risks and open questions, including what would change the conclusion.
8. Fact register appendix with source, date, and confidence per row.
9. Verification log: which checks passed, which items are pending re-verification.

State what not to do: do not treat marketing claims as capability proof, do not present estimates as measured figures, do not omit dates, and do not describe a competitor's internal intent as established fact.

### Ultron routing contract

**Choose this skill when:** researching a commercial market and its competitive landscape: market sizing, vendor positioning, features, pricing, packaging, integrations, customer segments, public roadmap signals, and opportunity/threat mapping in data and AI domains.

**Choose market-analysis when:** the subject is a financial instrument, asset set, or sector and the question concerns price, volume, volatility, spreads, positioning, term structure, or a conditional market/trading thesis over a stated horizon.

**Handoff contract:** this skill supplies sourced company/product identities, dated competitive facts, pricing observations, market structure assumptions, and uncertainty. The market-analysis skill may use relevant public sector or macro context, but must keep commercial positioning distinct from market-price evidence and must state the time horizon and invalidation conditions.

**Why the boundary exists:** commercial competition and financial market behavior can influence each other, but they require different data, methods, and conclusions.


## offer-pricing

**Use when:** Use when setting, revising, or stress-testing the price, packaging, discount rules, or tier structure of a product, service, or subscription offer for a business or entrepreneurial venture.

### Purpose and boundaries

This skill produces a defensible price and package structure for a single offer (one product, service, or subscription family), with the reasoning, assumptions, and test plan needed to validate it. It covers value-based price anchoring, tier design, discount governance, and pilot-based price testing.

Out of scope: tax or accounting treatment, legal terms of sale, consumer-protection disclosures, securities or investment pricing, regulated pricing (utilities, healthcare reimbursement, controlled goods), and any price change that will be communicated to existing customers without human approval.

### Inputs and assumptions

Collect before modeling. Mark any missing input as an explicit assumption with a stated confidence level.

- Target customer segment and the job the offer completes for them
- Current unit cost: variable cost per unit or per delivered hour, plus allocated fixed cost per unit at expected volume
- Alternatives the buyer actually uses: status quo, competitor offers, in-house effort, doing nothing; include their approximate prices
- Quantified value: time saved, revenue gained, cost avoided, risk reduced, with source or basis
- Sales channel and expected discount pressure
- Volume estimate and churn or repeat-purchase assumptions for subscriptions
- Minimum acceptable gross margin and payback target set by the owner

Assume nothing about willingness to pay without evidence. If evidence is absent, the output is a hypothesis, not a recommendation.

### Operating workflow

1. **Define the floor.** Compute cost-to-serve per unit. Set the absolute floor price at cost-to-serve plus the minimum contribution needed to cover fixed costs at target volume. Reject any proposed price below this floor unless the owner records a strategic reason and an end date.
2. **Quantify the value ceiling.** Estimate the buyer's value from the job, for example hours saved multiplied by loaded hourly cost, minus adoption effort. Discount this by your confidence (a 50% confidence on a value claim halves its weight). The ceiling is the value you can credibly claim, not the value you wish to claim.
3. **Identify the reference price.** Pick the most likely comparison the buyer makes. Price relative to that anchor, not relative to your cost.
4. **Set a target between floor and ceiling.** A common starting point is a price capturing 20–40% of the credible value gap, adjusted for differentiation proof. Document why.
5. **Design tiers only if buyers differ in need.** Use at most three tiers. Each tier must differ in a buyer-visible job, not only in volume quota. Anchor the highest tier to make the middle tier the default choice only when the middle tier is actually the target.
6. **Define discount rules.** Specify who may discount, maximum percentage, required trade (term length, prepayment, case-study, referral), and expiry. Discounts must be exchanged for something; none are unconditional.
7. **Build a sensitivity table.** Compute contribution margin, customer count needed to hit fixed-cost recovery, and revenue at price points 15% below and 15% above target, under low, base, and high conversion assumptions.
8. **Plan a controlled test.** Specify a price test with a fixed sample, a holdout or sequential design, a minimum observation window, and a predefined success metric (conversion, average revenue per account, or contribution). Do not declare a winner before reaching the sample size.

### Decision gates

- **Gate A (floor):** If target price is below the cost floor, stop and escalate. Do not proceed to tiering.
- **Gate B (value):** If the credible value ceiling is below the reference price, the offer cannot win on price. Recommend changing the value proposition or segment rather than cutting price.
- **Gate C (discount depth):** Any proposed discount above 25% of list, or any discount without an exchanged concession, requires owner approval.
- **Gate D (external change):** Any change visible to existing customers, any public price publication, or any change to contracted terms requires explicit human approval before drafting for release.
- **Gate E (test launch):** Pilot pricing shown to real prospects requires approval of the test design, the affected segment, and a rollback plan.

### Verification and evidence

Each recommendation must include:

- Cost floor calculation with each input listed and its source
- Value ceiling worksheet showing each claim, its basis, and its confidence weight
- Reference price with the source or the stated assumption behind it
- Sensitivity table covering at least three price points and three conversion scenarios
- Pass criteria: contribution margin at or above the owner's threshold in the base case, and no scenario where the offer loses money at expected volume
- Test success metric and minimum sample size, with the formula or tool used stated and flagged for verification against current documentation if it is version-specific

Quality checks: every number traces to an input or a stated assumption; no tier differs only by quantity without a stated reason; discount rules name the exchange given.

### Failure handling

- **Missing cost data:** Halt modeling of margin. Present a range using the best available bounds and label it provisional.
- **Conflicting value claims:** Report both, use the lower credible figure as the ceiling, and list what evidence would resolve the conflict.
- **No reference competitor:** Use the buyer's status quo cost as the reference and state that the anchor is weaker.
- **Test shows no clear winner:** Keep the current price, record the result, and do not extrapolate.
- **Owner requests a price below floor:** Document the trade-off, quantify the margin loss per period, and require approval with an end date.

### Deliverable contract

Return a single structured document with these sections in order:

1. Recommendation (one price per tier, with currency and billing period)
2. Floor, ceiling, and reference table
3. Tier definitions with buyer-visible differences
4. Discount policy with exchanged concessions and expiry
5. Sensitivity table
6. Test plan with success metric, sample size basis, and duration
7. Open assumptions ranked by impact, each with the evidence that would resolve it
8. Approvals required before any external action

Do not output a price without the floor and ceiling shown beside it. Do not state willingness-to-pay as fact; state it as an estimate with its basis.

