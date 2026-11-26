# Marketing, Sales, and Communications

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

## communications-messaging

**Use when:** Use when drafting, reviewing, sending, or tracking messages exchanged with external registries (corporate, trademark, domain, package, product, or professional registries), including change notifications, status inquiries, correction requests, and deficiency responses.

### Purpose and boundaries

This skill governs correspondence between an organization and an external registry operator or its staff. It covers:

- Drafting outbound messages: change notices, status inquiries, correction requests, deficiency responses, and fee or document follow-ups.
- Reviewing inbound registry messages and extracting required actions and deadlines.
- Maintaining a correspondence log that ties each message to a registry record.

It does not cover filing the underlying registration itself, legal opinions on registry rules, or internal-only communications. Do not use it to contact a registry on a person's behalf without that person's written authorization.

### Inputs and assumptions

Before drafting, confirm:

1. Registry name, jurisdiction, and the specific record identifier (entity number, mark or application number, domain, package name, or listing ID).
2. The purpose of the message and the desired outcome.
3. The authorized sender and signatory, and whether they are allowed to speak for the organization.
4. The current correspondence history for that record.
5. Any deadline stated in an inbound message, and its time zone.
6. The channel the registry specifies (portal, email address, postal address, form). Use only channels listed on the registry's official site.

Assume nothing about current registry rules, fees, forms, or response times. Mark any such detail as "verify against current official registry documentation" in the draft and in the log.

### Operating workflow

1. **Classify the message**: notice, inquiry, correction, deficiency response, or complaint. The class determines the tone, evidence, and approval level.
2. **Pull the record context**: current status, last contact date, open deadlines, and prior commitments made to the registry.
3. **Extract facts**: list every factual claim the message will make, with its source document and date. Remove any claim without a source.
4. **Draft in plain structure**: opening line stating the record and purpose; numbered facts; a single explicit request or statement; attachments listed by name and version; contact details for follow-up.
5. **Check tone and scope**: one topic per message. No speculation, no admissions of liability, no disputes of registry decisions beyond the stated procedure.
6. **Route for approval** (see Decision gates).
7. **Send through the authorized channel**, then record the sent timestamp, channel, recipient, attachment hashes, and reference number returned by the registry.
8. **Diary the follow-up**: set a review date based on the registry's stated timeline, or flag it as unknown and requiring verification.

### Decision gates

Stop and obtain explicit written approval from the accountable owner before:

- Sending any message that changes, withdraws, or certifies a registry record.
- Submitting a payment, a sworn statement, or a signed declaration.
- Disclosing personal data, financial data, unpublished product or trademark information, or security details.
- Sending any message that concedes a fact, admits non-compliance, or commits to a remedy or deadline.
- Contacting a registry through a channel other than the one it publishes, or contacting staff directly outside the normal process.
- Sending a second message on a record that already has an unanswered inquiry less than the stated response window old.

Route an inbound message to a human reviewer without drafting a reply if it threatens enforcement, cites legal proceedings, or requests information you cannot verify.

### Verification and evidence

Before approval, check:

- Every factual statement traces to a dated source.
- The record identifier matches the registry's own record, not an internal name.
- Attachments open, match the stated version, and contain no unrelated personal or confidential data.
- The request is answerable: it names one action the registry can take.
- Deadlines are converted to the registry's stated time zone and recorded with the source citation.

After sending, confirm receipt through the registry's acknowledgment or reference number. Record a measurable closure target: for example, "response expected within the window stated in the registry's most recent published guidance; if none is stated, escalate after 10 business days of silence." Mark the window as requiring verification.

### Failure handling

- **Bounced or rejected message**: do not resend through a different channel. Log the rejection reason, verify the channel on the official site, and request approval before resending.
- **No response by the review date**: send one follow-up referencing the original reference number. Do not send a third message without escalation approval.
- **Inbound message with unclear or conflicting requirements**: stop, do not guess, and request clarification through the stated contact channel after approval.
- **Wrong record or misdirected message**: notify the registry promptly, do not forward the content further, and log the incident for the data-handling owner.
- **Missed deadline**: escalate immediately to the accountable owner with the original deadline, the source citation, and the current status. Do not characterize the miss in outbound messages without approval.

### Deliverable contract

Each completed task produces:

1. The final message text, marked with status: draft, approved, or sent.
2. A correspondence log entry: record identifier, registry name, message class, sender, approver, channel, send timestamp, reference number, attachments with versions, open deadlines, and source citations.
3. A list of items marked for verification against current official registry documentation.
4. A short handoff note stating the next action, its owner, and its date.

Quality is met when every claim is sourced, every send is approved where a gate applies, every log entry is complete, and no message contains unverified rules, fees, or timelines.


## content-distribution

**Use when:** Use when planning, scheduling, or executing the distribution of business content (blog posts, newsletters, case studies, product announcements, thought leadership) across owned and third-party channels, including channel selection, repurposing, timing, and performance attribution.

### Purpose and boundaries

This skill covers getting finished business content in front of the right audience through deliberate channel choices, sequencing, repurposing, and measurement. It applies to marketing teams, founders, sales enablement staff, and communications leads distributing B2B or B2C material.

In scope: channel mapping, distribution calendars, adaptation of one asset into channel-specific formats, partner and syndication outreach drafts, paid amplification planning, UTM and attribution setup review, and post-distribution reporting.

Out of scope: writing the underlying content (use a content creation skill), brand strategy, legal review of claims, press-relations negotiation, and actually publishing to external platforms without approval.

### Inputs and assumptions

Before starting, confirm:

1. The source asset: final text, approved claims, owner, and publication date.
2. Target audience segments and the single primary action desired (read, sign up, book a demo, forward to a colleague).
3. Available channels with access status: owned (site, email list, social accounts), earned (partners, press, communities), paid (ad accounts and budget).
4. Constraints: embargoes, regulated-claim restrictions, brand guidelines, contractual partner rules, and blackout dates.
5. Measurement baseline: current traffic, open rates, conversion rates, and attribution model in use.

If any item is missing, record it as an assumption with a stated owner and do not proceed on guessed values for budgets, audience sizes, or performance figures.

### Operating workflow

1. **Define the objective per asset.** Map one primary metric (qualified visits, signups, pipeline influenced, replies from target accounts). Reject vanity-only goals as primary metrics.
2. **Build the channel matrix.** For each candidate channel, record audience fit, expected reach, effort, lead time, and cost. Keep no more than five channels for a single asset unless the owner justifies more.
3. **Adapt, do not copy.** Produce channel-native versions: a newsletter lead with the single strongest insight, a LinkedIn post that opens with a concrete finding, a partner brief that states what the partner gains, a sales one-pager that names the buyer problem. Keep factual claims identical across versions.
4. **Sequence the rollout.** Order: owned channels first (establish the canonical URL), then partner and earned channels (which need the live link), then paid amplification (only after organic performance is observed for at least one cycle). Stagger so one channel does not cannibalize another.
5. **Set tracking before launch.** Every outbound link carries consistent UTM parameters (source, medium, campaign, content). Confirm the analytics tool receives a test event. Do not reuse campaign names across quarters.
6. **Schedule with time zone and audience checks.** Record the target audience's local time zone and avoid major holidays or known industry events unless the content is tied to them.
7. **Prepare the approval packet.** List every channel, exact copy, link, schedule, budget, and the person accountable.
8. **Execute, then monitor.** Check performance at 24 hours, 7 days, and 30 days against the baseline. Log deviations.
9. **Close the loop.** Record what drove qualified action, retire underperforming channel variants, and feed findings into the next calendar.

### Decision gates

Stop and request explicit approval before:

- Publishing or sending anything to an external audience, including partner platforms, press lists, and email sends to contacts.
- Any paid spend, budget increase, or new ad account.
- Deleting, unpublishing, or overwriting live posts or archived links (broken links harm search and referral equity).
- Sending messages to named individuals outside an existing consent relationship.
- Using customer names, logos, testimonials, or case data in any new channel.
- Making performance, security, compliance, or savings claims not already approved by the content owner.
- Changing a canonical URL, redirect, or tracking domain.

Proceed without a gate only for internal drafts, calendar planning, and analysis of data you have been given.

### Verification and evidence

Before the approval packet is marked ready:

- Every claim in channel variants matches the source asset, verified line by line.
- Every link resolves to a live URL and carries the UTM set defined in the plan. Check each link with a test click.
- Character limits, image dimensions, and format rules are checked against the current published specifications of each platform. Mark these as version-sensitive and verify against each platform's current official documentation, since limits change.
- Audience size estimates cite a named source or are labelled as estimates.
- Post-launch reports compare actuals against the baseline, state the sample size, and avoid attributing causation from a single channel without a control or a stated limitation.

Evidence to retain: the channel matrix, final copy per channel, UTM sheet, approval record with timestamp, and the 24-hour, 7-day, and 30-day reports.

### Failure handling

- **Broken link or tracking failure discovered after publishing:** pause further distribution, fix the link or tag, notify the owner, and log the affected window. Do not silently republish.
- **Partner declines or delays:** remove the partner from the active sequence, keep the relationship record, and do not chase beyond one follow-up.
- **Low performance at 24 hours:** diagnose before changing. Check delivery, link function, and timing first; edit copy only after ruling those out, and get approval for any edit to live material.
- **Conflicting data between tools:** report both figures, identify the likely cause (attribution window, deduplication, bot filtering), and do not average them into a single number.
- **Missing approval during a scheduled window:** hold the item. Never publish to fill a slot.

### Deliverable contract

Every engagement returns:

1. Objective statement with one primary metric and baseline value (or marked as unknown).
2. Channel matrix with ranking rationale.
3. Channel-specific copy variants with a claim-consistency note.
4. Dated rollout calendar with owners and dependencies.
5. UTM and tracking sheet.
6. Approval packet listing every gated action, status pending or approved.
7. Measurement plan with 24-hour, 7-day, and 30-day checkpoints.

Do not deliver: unverified performance projections, copy that introduces new factual claims, or any schedule that publishes externally without a recorded approval.


## copywriting-and-outreach-drafting

**Use when:** Use when drafting marketing copy, landing page text, product descriptions, cold outreach emails, follow-up sequences, or partnership pitches that must match a stated audience, offer, and claim set.

### Purpose and boundaries

Produce persuasive, accurate written material for a specific audience and goal. Covered: landing pages, product descriptions, ad variants, cold emails, follow-up sequences, partnership pitches, and short announcement text.

Not covered: sending messages, purchasing contact lists, scraping personal data, legal or regulatory opinions, and claims that require evidence the user has not supplied.

### Inputs and assumptions

Before drafting, confirm or state as an explicit assumption:

1. Audience: role, industry, stage, and what they already know.
2. Offer: what is provided, price or price range if relevant, delivery terms, and availability.
3. Goal: the single action wanted (reply, click, book, buy, reply to a question).
4. Proof: approved claims, metrics with sources and dates, customer quotes with permission.
5. Constraints: word limits, channel, brand voice, required disclosures, prohibited terms.
6. Recipient data: use only what the user provides. Do not infer personal details about named individuals.

If proof is missing, write claims as conditional or omit them. Never fill gaps with plausible numbers.

### Operating workflow

1. Restate the goal and audience in one sentence each. Stop if either is vague and ask one targeted question.
2. List every factual claim the draft will need. Mark each as supplied, supplied-with-source, or unsupported.
3. Choose one core message and one proof point. Cut the rest.
4. Draft the opening around the reader's situation, not the sender's history. For cold outreach, reference a specific, user-supplied observation about the recipient's context.
5. State the offer concretely: what, for whom, what happens next.
6. Write one clear call to action. Remove competing asks.
7. Produce variants only when requested or when testing is explicitly planned. Label each variant with its hypothesis (for example, "problem-led" versus "outcome-led").
8. Run the checks in the verification section, then deliver.

### Decision gates

- **Claim gate:** If a claim involves numbers, rankings, guarantees, health, financial returns, legal status, or comparisons to named competitors, require a source before including it. Otherwise remove it or flag it as needing approval.
- **Audience gate:** If the audience includes minors, patients, or regulated-profession members, stop and request approval of the approach and any required disclosures.
- **Send gate:** Any draft intended for external delivery requires explicit user approval of final text, recipient list, and timing. Do not state or imply that a message has been sent.
- **Data gate:** If the request includes personal contact data, confirm the user has a lawful basis for contacting those people and that consent or opt-out handling exists. Do not verify legal compliance; direct the user to qualified counsel or current official guidance for their jurisdiction.
- **Personalization gate:** Personalized openings may use only facts the user provided. Never generate "research" about a person.

### Verification and evidence

Run these checks and report results:

- Word count is within the stated limit (count, do not estimate).
- Every claim maps to a supplied proof item or has been removed.
- Exactly one call to action appears.
- Reading level suits the audience; flag sentences above roughly 25 words for splitting.
- No superlatives without evidence ("best," "guaranteed," "only," "#1").
- No urgency or scarcity language unless the offer deadline or inventory is user-confirmed.
- Subject lines are under about 60 characters and do not use deceptive prefixes such as "Re:" or "Fwd:" on first contact.
- Unsubscribe or opt-out language is present for bulk email when the user's context calls for it, with a note to verify requirements against current law.
- Placeholders are absent from final output, or are explicitly listed as fields the user must fill.

Report the checklist results beside the draft.

### Failure handling

- **Missing proof:** Deliver the draft with the claim removed and a note listing what evidence would allow it back.
- **Conflicting facts:** Stop and ask which source is authoritative. Do not average or pick silently.
- **Request to mislead** (fake testimonials, invented urgency, impersonation, misleading sender identity): decline that element, offer a truthful alternative.
- **Length cannot fit required content:** Report the conflict and propose which element to drop.
- **Version-sensitive platform rules** (ad policy, email sender requirements, character limits): state that these must be checked against current official platform documentation before use.

### Deliverable contract

Return:

1. Draft text, with subject line where applicable, in a clearly separated block.
2. Word or character count.
3. Claim ledger: each factual statement with status (supplied, sourced, removed, pending).
4. Check results from the verification list.
5. Open questions and approvals still required before use or sending.

Do not include unrequested variants, generic tips, or marketing commentary. Do not state that the copy is compliant, legal, or guaranteed to perform.


## customer-growth

**Use when:** Use when planning, diagnosing, or executing customer acquisition, activation, retention, expansion, or referral work for a product or service business, including funnel analysis, churn investigation, pricing-tier and onboarding changes, and growth experiment design.

### Purpose and boundaries

This skill turns customer growth questions into measured hypotheses, prioritized experiments, and decision-ready recommendations. It covers the lifecycle: acquisition, activation, retention, expansion, and referral. It produces analysis and plans; it does not itself launch campaigns, change live pricing, message customers, or alter production systems.

Out of scope: legal review of marketing claims, tax or accounting treatment, individual credit or financial advice, and guaranteed revenue forecasts. Refer those to the appropriate owner.

### Inputs and assumptions

Required before analysis:
- Business model (self-serve, sales-led, marketplace, subscription, transactional) and unit of growth (account, seat, household, order).
- Lifecycle definitions: what counts as signed up, activated, retained, churned, expanded. If undefined, propose definitions and mark them as assumptions.
- Time window, cohort granularity, and data source names.
- Current baseline metrics, with the date range and known data gaps.
- Constraints: budget, team capacity, contractual or regulatory limits on messaging, and brand rules.

State every assumption explicitly in the deliverable. Do not treat missing data as zero.

### Operating workflow

1. **Define the question.** Rewrite the request as one decision: for example, "Why did 90-day retention for trial-to-paid accounts fall 6 points in Q3?" Reject vague goals such as "grow revenue" until decomposed.
2. **Build the metric tree.** Decompose the outcome multiplicatively or additively (e.g., revenue = accounts × activation rate × conversion × ARPA). Identify which branch changed.
3. **Segment before concluding.** Split by channel, plan, region, acquisition cohort, company size, and product version. A blended change often hides one segment's shift. Require at least two segments to show the same pattern before calling it systemic.
4. **Separate correlation from mechanism.** For each candidate cause, list the observable it predicts and the observable that would falsify it. Check release dates, pricing changes, outages, and campaign timing against the metric curve.
5. **Generate and rank hypotheses.** Score each on expected impact, confidence, and cost (ICE or equivalent). Keep at most five active hypotheses.
6. **Design the test.** For each hypothesis: primary metric, guardrail metrics (e.g., support tickets, refund rate, unsubscribe rate), minimum detectable effect, sample size estimate, duration, and stop rule. Use randomized allocation where feasible; otherwise document a quasi-experimental design and its threats to validity.
7. **Recommend and hand off.** Provide the ranked plan, owners, and approval requests for any gated action.

### Decision gates

Stop and obtain explicit human approval before:
- Changing live prices, plan limits, or contract terms.
- Sending messages to customers or prospects, including win-back, re-engagement, or price-change notices.
- Launching paid acquisition spend above a stated threshold or changing bidding rules.
- Deleting, merging, or exporting customer records, or sharing personal data outside its approved scope.
- Any experiment that withholds a paid feature or discount from customers who would otherwise receive it.
- Any action with contractual, regulatory, or reputational consequences, including referral incentives involving payments.

Proceed without a gate only for read-only analysis, drafting, and proposing experiments in a document.

### Verification and evidence

Every quantitative claim must cite its source query, dataset, date range, and cohort definition. Before reporting a lift:
- Confirm sample sizes per arm meet the pre-registered minimum.
- Check for sample ratio mismatch in randomized tests; if present, halt interpretation.
- Compare the effect against guardrails and seasonality from the prior year or matched periods.
- Report confidence intervals or uncertainty ranges, not point estimates alone.
- Recheck that the metric definition did not change mid-window.

Mark any vendor-platform setting, analytics tool feature, or API detail as "verify against current official documentation" unless the user has supplied it in this session.

### Failure handling

- **Missing or inconsistent data:** Report the gap, quantify its likely effect on conclusions, and request the specific field or extract. Do not impute silently.
- **Metric conflicts across tools:** Identify the definitional difference (timezone, deduplication, attribution window) and present both values with the reconciled one labeled.
- **Inconclusive test:** Report the interval, state what effect size is now ruled out, and recommend either extension (only if pre-planned) or closing the hypothesis.
- **Guardrail breach:** Recommend halting the variant pending review, regardless of primary metric gains.
- **Insufficient evidence for a causal claim:** Downgrade the language to "associated with" and list the test that would establish causation.

### Deliverable contract

Produce a document with these sections, in order:

1. **Question and decision** (one sentence each)
2. **Baseline and metric tree** (table with values, periods, and sources)
3. **Findings** (segmented, each with evidence reference and confidence level: high, medium, low)
4. **Ranked hypotheses** (table: hypothesis, predicted observable, ICE score, cost)
5. **Experiment plan** (primary metric, guardrails, MDE, sample size, duration, stop rule, owner)
6. **Approval requests** (each gated action, the reason, and the requested decision)
7. **Assumptions and open data gaps**
8. **Next review date** and the metric that will trigger it

Quality check before delivery: every finding traces to a stated source; no hypothesis lacks a falsifiable prediction; no gated action is written as already done; all version-sensitive tool details are flagged.

### What not to do

- Do not report averages across segments that differ materially in size or behavior.
- Do not declare winners from peeking at unfinished tests.
- Do not recommend discounts or dark patterns (hidden fees, forced cancellation friction) as retention levers.
- Do not fabricate benchmark figures for "industry averages"; request the user's own history or cite a verified source.
- Do not expand scope into unrelated brand, product roadmap, or hiring decisions without flagging the boundary.

### Ultron routing contract

**Choose this skill when:** turning a customer growth objective into a measurable strategy and experiment plan across acquisition, activation, retention, expansion, and referral.

**Choose growth-marketing-customer-ops when:** the task is operationally reconciling and enriching customer/company records with external registry data, defining registry-derived segments or suppression lists, and maintaining provenance for those fields.

**Handoff contract:** this skill defines the growth hypothesis, target cohort, success metric, experiment design, and decision threshold. The customer-ops skill returns the available verified attributes, match confidence, status changes, and segment limitations. Do not treat a registry match as proof of customer intent or as permission to contact someone.

**Why the boundary exists:** growth strategy decides what should be tested; customer operations determines which records can be reliably and lawfully used to implement that test.


## email-calendar-and-team-messaging

**Use when:** Use when drafting, triaging, scheduling, or summarizing work email, calendar invitations, and team chat messages on the user's behalf, including reconciling availability across time zones and preparing follow-ups that need explicit sending approval.

### Purpose and boundaries

This skill covers professional communication work: reading and triaging inboxes, drafting replies, proposing or modifying calendar events, and composing team channel posts. It produces drafts, schedules, summaries, and action lists. It does not send, accept, decline, delete, or reschedule anything externally without explicit approval for that specific action.

Out of scope: personal or family correspondence unless the user states it is in scope, legal or HR notices, financial approvals, credential sharing, and bulk outreach to people outside the user's organization.

### Inputs and assumptions

Before acting, confirm or record:

- The user's time zone and working hours. Assume the user's calendar time zone is authoritative; never assume the recipient's.
- The objective of each message (inform, request, decide, confirm, apologize).
- The recipient list and whether any recipient is external.
- The deadline, if one exists, and whether it is a hard or soft constraint.
- Available tools. Note which capabilities exist (read mail, create draft, send, read calendar, query free/busy, post to channel). Do not assume a capability that was not provided.
- Any thread history needed for context. Read the full thread, not only the latest message.

If the thread contains conflicting instructions or unknown participants, list the ambiguity before drafting.

### Operating workflow

1. **Triage.** Sort items into: needs reply, needs decision, needs scheduling, informational, and ignorable. Flag anything mentioning a deadline, money, legal terms, access changes, or personnel matters as sensitive.
2. **Extract commitments.** For each item, record what was asked, by whom, and by when. Quote the exact deadline phrase.
3. **Check availability.** Use free/busy data when available. Convert every candidate slot to both the user's and the recipient's time zones and state both in the proposal. Exclude slots inside either party's non-working hours unless the user overrides.
4. **Draft.** Write in the register of the existing thread. Lead with the decision or request in the first two sentences. Keep messages under 150 words unless the content requires more. Put each question or ask on its own line.
5. **Stage, do not send.** Save as draft, or present the text for review. Include a one-line summary of what the message does and what response is expected.
6. **Calendar changes.** Draft the invitation with title, date and time in both zones, duration, location or video link only when the user supplies it, attendees, agenda of three bullets or fewer, and any prep requested of attendees.
7. **Log.** Produce a short record of what was drafted, staged, or scheduled and what awaits approval.

### Decision gates

Stop and request explicit approval before:

- Sending any email or channel message, including replies in existing threads.
- Creating, updating, moving, or canceling calendar events that invite others.
- Adding or removing attendees, or changing visibility or permissions.
- Any message to an external party, or one that commits the user to a deliverable, price, date, or policy.
- Any message containing personal data, credentials, health, HR, legal, financial, or confidential project details.
- Bulk actions: sending to more than five recipients, mass-deleting, mass-archiving, or applying rules to a whole mailbox.

Approval must name the specific action and recipients. A general "go ahead" covers only the item described in the preceding summary.

Proceed without a gate only for read-only work: summarizing, classifying, checking free/busy, and drafting unsent text.

### Verification and evidence

Before presenting a draft or schedule, check:

- Every date has a weekday and both time zones stated. Verify the weekday independently.
- Every name matches the recipient list and thread participants.
- Every deadline quoted in the draft appears in the source thread.
- No attachment is referenced unless it is attached or its location is given.
- Word count is within target; the ask appears in the first two sentences.
- Calendar proposals list at least two candidate slots unless the user specifies one.
- Summaries cite message identifiers or timestamps for each claim.

If a fact cannot be verified from the available sources, mark it "unverified" in the output rather than filling it in.

### Failure handling

- **Missing free/busy access:** ask the user for two or three windows instead of guessing.
- **Conflicting time zones or DST transitions:** state the offset explicitly and flag any slot falling within a daylight-saving change week.
- **Thread too long or truncated:** summarize what is visible, state what is missing, and ask for the rest.
- **Tool error on send, create, or update:** do not retry a write action automatically. Report the error, check whether the action partially succeeded, and ask before retrying.
- **Duplicate invitation risk:** search for an existing event with the same title and attendees before creating one.
- **Misdirected draft:** if a recipient is uncertain, hold the draft and confirm the address.

### Deliverable contract

Every response contains:

1. **Action summary:** one line per item, with status (drafted, staged, scheduled-pending-approval, no action).
2. **Drafts:** full text, labeled with recipient, subject or channel, and intended response.
3. **Schedule proposals:** candidate slots in both time zones, duration, attendees.
4. **Approval requests:** exact list of actions awaiting sign-off, numbered so the user can approve by number.
5. **Unverified items:** anything that depends on information not in the source material.

Do not state that a message was sent or an event created unless a tool result confirms it. Do not include guarantees about delivery, read receipts, or response times.

### What not to do

- Do not send, accept, decline, or cancel anything without the gate above.
- Do not invent meeting links, phone numbers, addresses, or attachments.
- Do not paraphrase deadlines or figures from memory; quote the source.
- Do not reveal content from one thread in a message to another recipient.
- Do not use urgency language, guilt, or pressure in drafts unless the user asks for it.
- Do not copy large blocks of external material into team channels without checking permission.
- Do not treat tool-specific option names or limits as fixed; confirm current behavior against the platform's official documentation before relying on it.


## growth-marketing-customer-ops

**Use when:** Use when a growth marketing or customer operations task requires matching, enriching, validating, or segmenting customer or prospect records against external registries (business registers, licensing bodies, identifier registries, partner directories), or when registry data drives campaign eligibility, suppression, or account routing.

### Purpose and boundaries

This skill governs how customer records are reconciled with external registries for marketing and customer operations: matching records to registry entries, appending registry attributes, validating status (active, dissolved, suspended, lapsed), and producing segments or suppression lists for campaigns.

In scope: match design, confidence scoring, enrichment field mapping, status validation, segment definition, change logging, and reconciliation reports.

Out of scope: legal determinations about a company's standing, credit or risk decisions, scraping registries in ways their terms prohibit, altering the system of record for registry data, and sending any outreach. Registry data is evidence for a marketing decision, not a substitute for legal or compliance review.

### Inputs and assumptions

Before starting, confirm:

1. Source extract: row count, date pulled, owner, and fields available (name, address, country, identifier, domain, contact role).
2. Registry sources: which registries are authorized, their jurisdiction, access method, and their stated refresh frequency. Record the timestamp of every pull.
3. Use case: campaign eligibility, deduplication, account routing, or suppression. Each use case has different tolerance for false matches.
4. Consent and lawful-basis rules that apply to the target market. Do not assume a registry record permits marketing contact.
5. Retention rules for enriched data.

Assume registry fields are incomplete, stale, and sometimes in local-language or non-standard formats. Assume duplicate legal entities exist under trading names.

### Operating workflow

1. Normalize inputs: trim whitespace, standardize country codes, lowercase domains, strip legal-form suffixes into a separate field, and preserve the original value.
2. Match in tiers: exact identifier match first, then normalized name plus postcode or country, then fuzzy name with address corroboration. Never match on name alone for an outreach segment.
3. Assign each match a confidence tier (High, Medium, Low) with the rule that produced it. Only High matches flow to automated segments.
4. Validate status against the registry record for each High match. Flag dissolved, suspended, or merged entities for suppression review.
5. Append only the agreed field list. Do not append personal data about individuals beyond what the use case and lawful basis allow.
6. Write a change log: record ID, field changed, old value, new value, source, pull timestamp, and rule ID.
7. Produce the segment with exclusion counts broken down by reason.

### Decision gates

Stop and request explicit approval before:

- Overwriting any field in the system of record, or deleting records.
- Sending any campaign or external message to a segment.
- Sharing registry-derived data with a third party or moving it across jurisdictions.
- Using a matching rule with expected false-match rate above the threshold the owner set. If no threshold exists, request one.
- Running bulk registry queries above the quota or rate limits in the source's current terms, which you must verify against the registry's official documentation.
- Enriching individual-level personal data.

### Verification and evidence

- Sample at least 50 High matches (or all, if fewer) and manually verify identifier and address agreement. Report the observed false-match rate with the sample size.
- Confirm row counts reconcile: input = matched + unmatched + excluded, with no unexplained gap.
- Check that every appended value carries a source and timestamp.
- Confirm suppression lists contain zero records that are also in the active send list.
- Cross-check segment size against the prior run; investigate any change above 10% without a documented cause.
- Mark any statement about registry coverage, update frequency, or API limits as "verify against current official documentation" unless you have checked it in this session.

### Failure handling

- Registry unavailable or rate-limited: pause, record the partial state, and resume from the last checkpoint. Do not substitute cached data without labeling its age.
- Conflicting registry values: keep both, mark the record Low confidence, and exclude it from automated segments.
- Matching produces unexpected concentration (for example, many customers mapped to one entity): halt and review; this often indicates a join error or a parent-subsidiary issue.
- Discovered personal data outside scope: stop enrichment on that field, report it, and do not propagate it.

### Deliverable contract

Return:

1. Run summary: sources, pull timestamps, input count, match tier counts, exclusion counts by reason.
2. Segment file or list with confidence tier and rule ID per row.
3. Change log as specified above.
4. Verification results: sample size, observed false-match rate, reconciliation totals.
5. Open items requiring approval, listed by gate.

Do not state that a segment is compliant or lawful. State only what was checked and what remains for review.

### Ultron routing contract

**Choose this skill when:** the task concerns customer/company record matching to external registries, enrichment, status verification, segmentation, suppression, or reconciliation of registry-derived attributes for marketing operations.

**Choose customer-growth when:** the central question is which growth lever to test, how to define a cohort and success metric, or whether an acquisition/activation/retention/expansion experiment should be prioritized.

**Handoff contract:** receive the proposed cohort definition and minimum attributes from the growth strategy skill. Return source provenance, match method and confidence, current status, freshness, permitted-use constraints, and records that remain ambiguous. The growth skill must incorporate uncertainty and not assume enrichment data proves consent or intent.

**Why the boundary exists:** customer data operations supplies trustworthy inputs; growth strategy decides how to use those inputs to learn and improve outcomes.


## outbound-sales

**Use when:** Use when planning, writing, or reviewing outbound prospecting work such as target account lists, cold email or LinkedIn sequences, call scripts, discovery-call prep, or outreach performance analysis for B2B sales.

### Purpose and boundaries

This skill produces and reviews outbound prospecting assets: ideal customer profiles, target account lists, prospect research briefs, multi-touch outreach sequences, call openers and discovery question sets, and post-campaign performance reviews. It is for B2B teams selling products or services to businesses.

Out of scope: inbound marketing strategy, pricing negotiation, contract terms, legal review of marketing claims, and sending any message or entering data into a live CRM or sequencing tool. Those actions require a human owner and explicit approval (see Decision gates).

### Inputs and assumptions

Before drafting, confirm these inputs. If any are missing, ask once, then proceed with labeled assumptions.

- Offer: what is sold, the problem it solves, and one or two proof points with sources.
- ICP: firmographics (industry, headcount band, region), trigger events, and disqualifiers.
- Buyer roles: economic buyer, champion, and blocker, with typical titles.
- Current motion: channels available (email, phone, LinkedIn), sending domain status, and daily volume limits.
- Constraints: regulated sectors, opt-out requirements, prohibited claims, and existing customer exclusions.
- Goal metric: meetings booked, opportunities created, or reply rate, with a target and time window.

Assume nothing about competitors, customer names, or results. Never fabricate case studies, statistics, or customer logos. If a proof point lacks a source, mark it as unverified and exclude it from outbound copy.

### Operating workflow

1. **Define the segment.** Write the ICP as a single sentence plus a disqualifier list. Test it: a rep should be able to classify a random account in under a minute.
2. **Build the account list.** Target 50 to 200 accounts per segment for a first wave. Record for each account: domain, segment, trigger event with date and source URL, and one verified observation about their business.
3. **Map the buying group.** For each account, identify two to three contacts by role. Record only business-role information from public sources.
4. **Write the value hypothesis.** Use this form: "[Role] at [segment] likely struggles with [specific problem] because [observable cause], which costs [measurable impact]." Reject hypotheses that name no observable signal.
5. **Draft the sequence.** Use four to six touches over 14 to 21 days: one personalized opener referencing the trigger, one short value message, one proof point, one alternative-angle message, and one breakup note. Keep each email under 120 words with one call to action.
6. **Prepare call assets.** Write a 20-second opener, three discovery questions tied to the hypothesis, and two objection responses drawn from actual objections in the segment.
7. **Set the review cadence.** Define the metric checkpoints (day 5, day 10, end of wave) and the thresholds that trigger a change.

### Decision gates

Stop and request explicit human approval before:

- Sending, scheduling, or queuing any outbound message, call, or LinkedIn action.
- Importing, deleting, or overwriting contacts or sequences in a CRM or sales tool.
- Purchasing or enriching contact data from a third party.
- Any claim about performance, ROI, security, or compliance that lacks a cited source.
- Targeting contacts in regions with consent or opt-out rules until the lawful basis has been confirmed by the owner.
- Adding a named customer, partner, or competitor to copy.

Proceed without approval only for drafting, research from public sources, and analysis of data the user has supplied.

### Verification and evidence

Check every deliverable against these criteria before presenting it:

- Every personalization line cites a trigger or observation with a date and source.
- Every factual claim about the prospect or the offer maps to a source in the inputs or is labeled as a hypothesis.
- Each email is under 120 words, has one call to action, and contains no unverifiable superlatives.
- Each sequence step has a distinct purpose; no two touches repeat the same value claim.
- Account list has no duplicate domains and no existing customers unless the user requested re-engagement.
- Performance analysis reports sample size, time window, and denominators (sent, delivered, replied, positive reply). Do not report a rate from fewer than 100 sends as a conclusion; label it directional.

Rule of thumb for interpreting results: a reply rate gap under about two percentage points on small samples is noise. Change one variable at a time.

### Failure handling

- **Missing trigger data:** downgrade the account to a tier-two list rather than writing a generic opener.
- **Contradictory ICP signals:** surface the conflict to the owner with two candidate definitions and the tradeoff.
- **Low reply rate after a full wave:** check deliverability and targeting before rewriting copy. Diagnose in this order: bounce rate, spam placement signals, list fit, offer relevance, copy.
- **Requested claim that cannot be sourced:** remove it and state what was removed and why.
- **Conflicting instructions about compliance:** stop drafting that segment and escalate.

### Deliverable contract

Each output must include:

1. A header stating the segment, date basis, and assumptions list.
2. The requested artifact in its final form (list, sequence, script, or analysis).
3. A source table for every factual claim, with source and date.
4. A "Needs approval" section listing any action from the decision gates that the user must authorize.
5. A short "Open questions" section with no more than three items.

Do not include generic sales advice, motivational language, unsourced statistics, invented names, or unfinished bracketed template text in final deliverables. Where a value must be supplied by the user, state it as a required input rather than leaving a blank.


## paid-growth-and-lead-operations

**Use when:** Use when designing, auditing, or troubleshooting paid acquisition data flows, conversion tracking, lead scoring pipelines, CRM lead routing, or attribution reporting for paid media campaigns.

### Purpose and boundaries

This skill covers the data operations behind paid acquisition: campaign taxonomy, conversion event definitions, lead capture and deduplication, lead scoring and routing, offline conversion uploads, and performance reporting that ties spend to downstream revenue.

In scope: tracking-plan review, UTM and naming conventions, lead-to-CRM mapping, qualification rules, conversion-value logic, reconciliation between ad platforms and the CRM, and diagnosis of discrepancies.

Out of scope: creative strategy, bid-strategy selection as a marketing decision, legal sign-off on consent language, and any direct change to live ad accounts or CRM records. This skill produces analysis, specifications, and change proposals; a human operator executes them.

### Inputs and assumptions

Request these before analysis:

1. Campaign inventory export: platform, campaign, ad group, UTM parameters, start and end dates, daily spend.
2. Lead records: unique ID, created timestamp, source fields, form or event type, consent status, qualification status, opportunity linkage.
3. Conversion definitions currently configured in each platform, with their trigger, value, and attribution window.
4. The CRM stage history for a sample of leads, including timestamps and owner changes.
5. The revenue or pipeline figure the business treats as truth, and its date basis.

Assumptions to state explicitly in every output: time zone used, currency and FX rate source, attribution model, and whether platform-reported and CRM-reported numbers are compared on the same date basis. If any assumption is unverified, label it as such.

### Operating workflow

1. **Define the question.** Write one sentence: what decision depends on this analysis (budget shift, channel cut, routing fix, tracking repair).
2. **Build the taxonomy map.** List every campaign source value and map it to a canonical channel. Count unmapped values; do not guess mappings for values that lack clear evidence.
3. **Audit conversion events.** For each platform event, record trigger, value logic, and window. Flag events that fire on page load rather than confirmed submission, events that double-fire, and values that are constant placeholders.
4. **Reconcile leads.** Deduplicate on normalized email or phone plus a time window (state the window used). Compare platform lead counts to CRM lead counts by day and by source. Accept a gap only if it is explained by a named cause such as consent suppression, spam filtering, or late CRM sync.
5. **Evaluate lead scoring and routing.** Check that every scoring rule references a field that is populated for at least 90 percent of leads in the sample; otherwise the rule is measuring data completeness, not lead quality. Confirm routing rules have a default owner for unmatched records.
6. **Test offline conversion matching.** For uploaded conversions, verify the match key type, the timestamp used (click or conversion time), and the share of records successfully matched. Report match rate as a number, not an adjective.
7. **Produce the reconciliation and recommendations.** Separate findings by confidence: confirmed (reproduced in data), probable (consistent with data, not reproduced), and hypothesis (requires a test).

### Decision gates

- **Gate A, before any recommendation to change spend:** reconciled lead or conversion gap is under 10 percent per source, or the gap has a named, quantified cause. If not, the output is limited to a tracking repair plan.
- **Gate B, before recommending a scoring change:** a holdout or historical back-test shows the new rule separates later-qualified from unqualified leads better than the current rule. Report both metrics.
- **Gate C, before proposing offline conversion uploads:** match rate is measured on a sample and consent basis is confirmed by the data owner.
- **Gate D, mandatory approval:** any action that deletes or merges CRM records, alters live conversion tracking, changes routing for active leads, uploads personal data to an external platform, or modifies budgets. Present the exact change, scope, affected record count, and rollback method, then stop until a named human approves.

### Verification and evidence

Every finding must cite the data slice it came from (table, date range, filter). Required checks before publishing:

- Row counts before and after each join or deduplication, with the number of dropped rows and the reason.
- Totals per source sum to the overall total within rounding.
- Date basis is identical across compared systems.
- Spot-check at least 10 individual leads end to end, from ad click to CRM stage, and record the outcome.

Platform-specific field names, event parameters, API endpoints, and upload formats change between versions. Mark any such detail as "verify against current official documentation" and do not state it as fact without that check.

### Failure handling

- **Mismatched totals:** stop, list the top three contributors to the gap by source and date, and state which system is considered authoritative. Do not average the two figures.
- **Missing key fields:** report the null rate per field and exclude affected rules from recommendations.
- **Ambiguous attribution:** present results under at least two attribution models and state that the choice changes the ranking.
- **Sample too small:** if fewer than 200 leads or 30 conversions per segment exist, report directional findings only.
- **Conflicting consent flags:** treat the record as non-contactable and escalate to the data owner.

Do not fill gaps with assumed values. Do not present a single-day spike as a trend.

### Deliverable contract

Return a document with these sections in order:

1. Decision supported and scope.
2. Assumptions with verification status.
3. Data sources and slices used, with row counts.
4. Findings table: finding, evidence, confidence level, estimated impact with units.
5. Reconciliation summary: platform versus CRM counts by source and date, gap percentage, named cause.
6. Recommended actions, each tagged with its gate status and whether human approval is required.
7. Open questions and the data needed to close them.
8. Version-sensitive items to verify against official documentation.

Do not include unverified benchmark figures, industry averages presented as targets, or claims of regulatory compliance. Do not recommend moving personal data between systems without naming the lawful basis as confirmed by the data owner.

### Ultron routing contract

**Choose this skill when:** the question is about paid acquisition measurement and the path from ad spend to qualified leads or revenue: campaign taxonomy, attribution, conversion events, offline conversion matching, lead-source reconciliation, and paid-channel performance diagnostics.

**Choose `saas-crm-marketing-automation` when:** the work changes or designs contact lifecycle behavior inside the CRM: deduplication, segmentation, scoring, nurture enrollment, suppression, lifecycle stages, ownership, and sales handoff.

**Handoff contract:** this skill defines the paid-source and conversion data contract, including campaign IDs, event names, attribution windows, value semantics, consent constraints, and reconciliation gaps. The CRM skill maps that contract to contact/account fields and automation rules. Any live spend, tracking, personal-data upload, or CRM mutation remains subject to its explicit approval gate.

**Why the boundary exists:** acquisition measurement determines where leads and revenue came from; CRM automation determines what happens to a contact after capture. A shared contact record does not make those responsibilities interchangeable.


## paid-partnerships

**Use when:** Use when planning, vetting, negotiating, contracting, disclosing, or measuring paid partnerships such as sponsorships, creator collaborations, co-marketing deals, or paid endorsements with businesses or individuals.

### Purpose and boundaries

This skill guides a business owner, marketer, or partnerships lead through a paid partnership from objective-setting to post-campaign evaluation. It covers sponsorships, creator and influencer collaborations, paid co-marketing, and paid endorsements.

Out of scope: equity or revenue-share deals that require securities or tax structuring, affiliate programs with no fixed fee, and final legal advice. Flag these for qualified counsel or an accountant.

### Inputs and assumptions

Collect these before drafting anything:

- Business objective, stated as one measurable outcome (for example, 400 qualified trial signups in 60 days).
- Budget ceiling, payment structure, and payment timing.
- Target audience, markets, and jurisdictions where content will be seen.
- Partner candidates with their platforms, audience size, and audience geography.
- Brand guidelines, prohibited claims, and product claims that already require substantiation.
- Existing contracts, prior partner history, and any exclusivity commitments.

If the objective is not measurable, stop and resolve it first. Do not assume an audience, budget, or claim that the user has not supplied.

### Operating workflow

1. **Define the outcome and the metric.** Pick one primary metric (conversions, qualified leads, reach within a defined audience) and up to two secondary metrics. Record the baseline.
2. **Shortlist partners.** Score each candidate 1 to 5 on audience fit, verified audience quality, content-style fit, past disclosure behavior, and brand-safety risk. Require at least three candidates for any spend above your standard threshold.
3. **Verify audience and authenticity.** Check audience geography, age split, and engagement consistency over at least 90 days. Look for sudden follower spikes, comment patterns that suggest automation, and engagement far below peers. Record the method and date of each check.
4. **Build the offer.** Specify deliverables (format, count, posting window, required links or codes), usage rights, exclusivity limits, approval rounds, and the metric definitions and tracking method.
5. **Draft the agreement.** Include scope, fees and milestones, approval deadlines, disclosure obligations, usage and licensing terms, termination conditions, and content takedown rules. Route the draft to counsel before signing.
6. **Set disclosure requirements.** Require clear, conspicuous disclosure of the material connection in the content itself, not only in a bio or a hashtag buried among others. Check the current guidance from the relevant authorities for each market, such as the US Federal Trade Commission's endorsement guidance and the UK Advertising Standards Authority's rules. Verify current wording against those official sources, since guidance changes.
7. **Review before publication.** Approve scripts or drafts before posting. Confirm every product claim has substantiation on file.
8. **Track and close.** Monitor live content, capture screenshots and metrics at fixed intervals, and compare results to the baseline and the target.

### Decision gates

Stop and obtain explicit user approval before:

- Committing or releasing any payment, deposit, or gift above the approved budget.
- Signing or sending any contract, or agreeing to exclusivity, perpetual usage rights, or non-compete terms.
- Publishing or requesting publication of content that makes health, financial, or performance claims.
- Contacting partners externally, or any outreach that names your company publicly.
- Requesting or storing partner personal data beyond business contact details.
- Requiring a partner to delete, edit, or take down published content.

Proceed without a gate only for internal drafting, research, and analysis.

### Verification and evidence

Each campaign must have:

- A signed document dated and stored, with all approved changes recorded.
- Screenshots of disclosure as published, captured at posting time.
- Audience verification records with method and date.
- A tracking plan using unique links or codes, with the tracking method documented before launch.
- A results table comparing actual results to the target, reporting the primary metric first.

Quality threshold: a campaign is complete only when the primary metric is reported against its baseline, every deliverable is verified as live with disclosure, and the write-up identifies at least one attribution limitation.

Do not state specific reach, conversion, or return figures unless they come from user-supplied data or a verifiable source.

### Failure handling

- **Missing disclosure:** Request correction immediately, record the request with a timestamp, and pause further payments until corrected.
- **Metric tracking failure:** Report the gap explicitly. Do not backfill with estimates presented as measurements.
- **Partner underdelivery:** Apply the contract's remedy terms. Escalate to counsel before withholding final payment.
- **Audience authenticity concern after signing:** Pause new deliverables, document evidence, and seek the user's decision before terminating.
- **Conflicting platform or regulatory guidance:** Follow the stricter standard and flag the conflict for counsel.

### Deliverable contract

Produce:

1. A one-page campaign brief with objective, primary metric, baseline, target, budget, and timeline.
2. A scored partner shortlist with the rationale for each score.
3. A draft offer or term sheet with all required fields listed in step 4.
4. A disclosure checklist for each target market, marked with the date verified against official sources.
5. A post-campaign report with measured results, evidence references, and open items.

Do not produce legal opinions, guaranteed outcomes, or unverified statistics. Do not present regulatory guidance as current without stating that it must be confirmed against official sources at the time of use.


## prospect-intelligence

**Use when:** Use when researching a specific prospective customer, partner, investor, or acquisition target to build an evidence-backed profile, qualify fit, identify buying triggers, and prepare outreach or meeting briefs from public and user-supplied information.

### Purpose and boundaries

This skill turns a named organization (and optionally named contacts) into a decision-ready brief: who they are, whether they fit, what has changed recently, who likely decides, and what a credible first conversation looks like. It covers B2B sales prospecting, partnership scouting, investor and acquirer screening, and vendor due diligence at a light level.

Out of scope: covert information gathering, accessing non-public records without authorization, scraping behind logins, personal profiling of individuals beyond professional role, inferring protected characteristics, generating bulk unsolicited outreach, and making legal, financial, or compliance determinations about the target.

### Inputs and assumptions

Required: target organization name, and the user's goal (sell, partner, invest, acquire, evaluate vendor).

Helpful: user's offering and ideal customer profile, known contacts and their titles, existing relationship status, geography constraints, and any internal notes the user is permitted to share.

Assumptions to state explicitly in the brief: the date of research, the sources consulted, and that facts are as of that date. If the target name is ambiguous (common names, subsidiaries, recent mergers), stop and confirm the correct entity before proceeding.

### Operating workflow

1. **Confirm entity.** Record legal name, domain, headquarters, parent or subsidiary relationships, and any prior name changes.
2. **Establish fit.** Compare the target against the user's ideal customer profile on firmographics (size band, industry, geography, revenue model, funding stage) and technographics only where publicly observable. Score each criterion as met, unmet, or unknown. Do not treat unknown as met.
3. **Collect recent signals.** Look for dated, primary-source events from the last 6–12 months: leadership changes, funding or debt announcements, product launches, regulatory filings, hiring concentrated in a relevant function, public statements about strategy, layoffs or restructuring, and new partnerships. Record each signal with date, source, and a one-line relevance note.
4. **Map the buying context.** Identify the function most likely to own the problem, typical decision roles (economic buyer, technical evaluator, champion, blocker), and any stated initiatives that the offering maps to. Use only roles visible in public company materials or user-provided contacts.
5. **Identify the wedge.** Name one specific, testable reason to engage now, tied to a signal. If no signal supports timing, say so and recommend a lower-intensity approach.
6. **Draft the approach.** Produce a short first-touch angle and two to three discovery questions. Reference only facts from the brief.
7. **Assemble the brief** using the deliverable contract below.

### Decision gates

- **Gate A (entity):** Proceed only if the entity is unambiguous. If two plausible entities exist, return both with a question.
- **Gate B (fit):** If three or more core criteria are unmet, recommend deprioritizing and stop deep research unless the user overrides with a stated reason.
- **Gate C (outreach):** Before any message is sent, drafted for sending, or contact data is exported to a CRM or sequencing tool, obtain explicit user approval. Confirm the recipient is a business contact and that the user has a lawful basis to contact them under applicable rules (for example, consent or legitimate-interest analysis for their jurisdiction). Do not state legal conclusions; flag the question for the user's counsel or compliance function when unclear.
- **Gate D (sensitive data):** Do not collect or store personal contact details, home addresses, family information, health or financial details of individuals, or anything the target has signaled it does not want shared. Stop and ask before handling any such data.
- **Gate E (external action):** Any step that submits forms, contacts the target, creates records in external systems, or posts publicly requires explicit approval for that specific action.

### Verification and evidence

- Every factual claim carries a source and an access date. Claims without a source are labeled "unverified" or removed.
- Prefer primary sources: company filings, official newsrooms, regulator databases, the company's own website, and direct user-provided documents. Treat aggregator summaries and AI-generated profiles as leads only.
- Corroborate any signal that would change the recommendation with a second independent source.
- Dates must be absolute (YYYY-MM-DD), not relative ("last month").
- Quality checks before delivery: at least 3 dated signals or an explicit statement that none were found; every fit criterion marked met, unmet, or unknown; no unsourced numbers; no individual personal details; discovery questions reference real gaps.
- Do not state revenue, headcount, or funding figures as current unless a dated source supports them.

### Failure handling

- **Sparse public information:** Deliver a partial brief marked with confidence level low, list what could not be found, and recommend specific user-provided inputs that would close gaps.
- **Conflicting sources:** Report both values with sources and dates; do not average or pick silently.
- **Stale sources (over 18 months for signals):** Mark as historical context, not current trigger.
- **Entity changed (acquisition, rename):** Re-run Gate A and report the transition.
- **Blocked or restricted access:** Do not circumvent. Note the limitation and continue with accessible sources.
- **User requests covert tactics or personal profiling:** Decline that element, explain the boundary briefly, and offer the compliant alternative.

Never invent contact names, titles, or email patterns. If a role is unknown, say "role not confirmed."

### Deliverable contract

Return one Markdown brief with these sections in order:

1. **Summary** (3 sentences max): entity, fit verdict (pursue / nurture / deprioritize / needs input), confidence level.
2. **Entity profile:** legal name, domain, HQ, relationships, research date.
3. **Fit scorecard:** table of criteria with met / unmet / unknown and evidence link.
4. **Dated signals:** table with date, event, source, relevance.
5. **Buying context:** likely owning function, decision roles (titles only, from public sources), stated initiatives.
6. **Recommended wedge and timing:** one primary angle with the signal it rests on.
7. **Approach:** first-touch angle (not sent) and up to three discovery questions. Marked "pending approval."
8. **Open questions and gaps:** what the user should verify or supply.
9. **Sources:** numbered list with URL or document reference and access date.

Keep the brief under 700 words excluding sources. Do not include speculation about individuals' motives or personal circumstances.


## saas-crm-marketing-automation

**Use when:** Use when designing, auditing, or building marketing automation on a SaaS CRM, including lead capture, lifecycle stages, segmentation, lead scoring, nurture sequences, and sync rules, especially when an AI agent will read or write CRM or marketing records.

### Purpose and boundaries

This skill covers designing, reviewing, and changing marketing automation that moves contacts, accounts, and opportunities through a SaaS CRM: capture, deduplication, lifecycle staging, segmentation, scoring, nurture sequencing, and sales handoff.

Out of scope: legal determination of consent or lawful basis (refer to counsel), paid media buying, product analytics instrumentation, and data-warehouse modeling beyond reconciling counts.

### Inputs and assumptions

Required before work begins:
- Platform names and the workspace or account identifiers the user owns.
- Lifecycle definitions with entry and exit criteria and a named owner per stage.
- Field dictionary for contact, account, and lead objects, including required fields and allowed picklist values.
- Consent and suppression fields, and the source of each consent record.
- A sample export of current records, minimized to the columns needed.
- Success metrics with a current baseline.

Record every assumption. If a platform feature, limit, or API behavior affects the design, mark it "verify against current vendor documentation." Do not state endpoint names, rate limits, or plan entitlements unless the user supplied them from current documentation.

### Operating workflow

1. **Map current state.** List every entry point (forms, imports, integrations, API writes), every stage transition, and every automated action. Record the system of record for each field.
2. **Find defects.** Check for duplicate contacts sharing a normalized email or phone, stage regressions, contacts enrolled in conflicting nurture tracks, fields written by two systems, and sends that ignore suppression.
3. **Write rules as explicit conditions.** Example: `MQL = lead_score >= 60 AND (pricing_form_submitted OR demo_requested) AND NOT marketing_suppressed`. Each rule needs an owner and at least one test record that should match and one that should not.
4. **Design sequences** with entry criteria, exit criteria, a maximum enrollment rule, and a suppression check before every send step.
5. **Build in a sandbox first** using synthetic or pseudonymized records.
6. **Present a reviewable diff:** rule, field, old value, new value, estimated affected count.
7. **After approval, apply in small batches** and monitor each batch before continuing.

### Decision gates

Obtain explicit user approval before:
- Bulk updates, merges, deletions, or stage changes affecting more than 100 records or any production segment.
- Enabling, editing, or pausing any live email, SMS, or ad audience sync.
- Changing consent, suppression, or opt-in fields, or importing a new contact list.
- Changing scoring thresholds that alter sales routing or lead ownership.
- Sending data to any new third-party tool.
- Any irreversible action, including field deletion, object archiving, or permanent record removal.

No gate is needed for read-only analysis, drafting documents, or testing against synthetic data in a sandbox.

### Verification and evidence

Before reporting a change as complete, check:
- **Counts:** record totals before and after, with the delta fully explained by the rule.
- **Duplicates:** zero new duplicate groups on the matching key.
- **Suppression:** a test set of suppressed contacts shows zero sends.
- **Routing:** five to ten representative test records traverse each path and land in the expected stage and owner.
- **Field integrity:** no required field is blank on written rows, and picklist values match the dictionary.
- **Rollback:** a full export was taken before the change, and the reversal steps are documented and tested on a sample.

Report results as a table: check, method or query used, expected result, observed result, pass or fail. Cite metrics only when observed in the current session.

### Failure handling

- **Count mismatch beyond the explained delta:** halt writes, do not retry, reconcile against the pre-change export.
- **Two systems writing the same field:** pause the lower-authority writer, document the conflict, and escalate to the field owner.
- **Unexpected sends or suppression breach:** stop the affected sequence immediately, report what was sent and to how many contacts, and escalate for incident handling. Do not attempt message recall.
- **Ambiguous lifecycle definition:** list the candidate interpretations with their effects and ask the owner to choose.
- **Unknown platform behavior:** state the uncertainty and mark the item for documentation verification.

### Deliverable contract

Produce:
1. Current-state map: entry points, transitions, system of record, owners.
2. Findings list ranked by revenue impact and compliance risk.
3. Rule specification: conditions, owners, match and non-match test records.
4. Change plan: diff, batch sizes, approval status per gate.
5. Verification report with evidence per check.
6. Rollback procedure.

Do not: include personal data in reports beyond record IDs; claim compliance or deliverability outcomes; invent integration names or limits; present unverified platform behavior as fact.

### Ultron routing contract

**Choose this skill when:** the task is designing or changing CRM lifecycle logic: contact/account capture, deduplication, field ownership, segmentation, lead scoring, nurture sequences, suppression, stage transitions, or sales handoff.

**Choose `paid-growth-and-lead-operations` when:** the central question concerns paid channel attribution, campaign taxonomy, ad-platform conversion events, offline conversion uploads, or reconciliation of spend and downstream revenue.

**Handoff contract:** receive a validated campaign/source/event mapping and consent-aware conversion contract from the paid-growth skill. Return CRM field mappings, lifecycle rules, suppression logic, scoring and routing tests, affected-record estimates, and a reviewable change diff. Do not alter campaign budgets or ad-platform tracking as a side effect of changing CRM automation.

**Why the boundary exists:** CRM automation owns contact state and communication eligibility; paid-growth analysis owns acquisition measurement. Their data must reconcile, but their actions and approvals differ.


## saas-workspace-messaging-automation

**Use when:** Use when designing, building, or auditing an agent or automation that sends, routes, summarizes, or reacts to messages in SaaS workspaces such as Slack, Microsoft Teams, Discord, or email-linked team chat, including alert routing, digest generation, and notification bots.

### Purpose and boundaries

This skill guides an agent through building messaging automation inside team collaboration platforms: posting status updates, routing alerts to the right channel, generating digests of channel activity, answering scoped queries, and triggering workflows from message events.

In scope:
- Designing message templates, routing rules, and digest logic.
- Choosing between webhooks, bot tokens, and platform event subscriptions at a conceptual level.
- Writing dry-run plans, test channels, and rollout steps.
- Auditing existing automations for noise, duplication, permission overreach, and privacy exposure.

Out of scope:
- Bulk messaging to external users, customers, or distribution lists.
- Reading direct messages or private channels without an explicit owner grant.
- Moderation, HR, legal, or investigative monitoring of employees.
- Storing or forwarding credentials, tokens, or personal data inside message bodies.

### Inputs and assumptions

Collect before acting:
1. Target workspace platform and tenant (name only; never paste tokens).
2. Exact purpose of each message: who must act, by when, and what action.
3. Channel list with owners and their stated purpose.
4. Event sources (e.g., CI results, ticket updates, monitoring alerts) and their volume per hour and per day.
5. Required identity: bot user, app, or incoming webhook. Record who owns it.
6. Retention and privacy constraints from the workspace admin or data owner.

Assume nothing about API method names, scopes, rate limits, or payload limits. Treat them as version-sensitive and verify them against the current official platform documentation before writing code or configuration. Record the verification date and doc URL in the design notes.

### Operating workflow

1. **Define the message contract.** For each message type, write: trigger, recipient channel, required fields, action expected, severity, and expiry. A message without a required action must be informational and labeled as such.
2. **Map routing.** Create a table from event source to channel. One event type maps to at most one primary channel. Secondary escalation requires a rule with a stated threshold (for example, unacknowledged for 30 minutes).
3. **Set deduplication and rate control.** Define a dedupe key (for example, incident ID plus state) and a suppression window. Collapse repeated events into one updating message where the platform allows edits, otherwise into a counted summary.
4. **Design digests separately.** Digests run on a schedule, summarize at most the agreed number of items, link to sources, and never quote full message bodies from private contexts.
5. **Build a dry run.** Send output to a sandbox or private test channel owned by the requester. Replay at least 20 recorded historical events, or the full set if fewer exist.
6. **Review with the channel owner.** Show sample outputs for each message type. Do not enable live posting until the owner approves in writing.
7. **Stage rollout.** Enable one channel, observe for a defined period (default: 3 business days or 100 messages, whichever is longer), then expand.
8. **Document operations.** Record owner, on-call contact, kill switch location, and rollback steps.

### Decision gates

Stop and request explicit human approval before:
- Posting to any channel that is not the requester's test channel.
- Any action that is destructive or irreversible: deleting messages, archiving or renaming channels, removing members, revoking or rotating tokens.
- Sending anything that reaches people outside the workspace or outside the approved channel list.
- Using broader permissions than the stated purpose requires, or adding scopes that read private content.
- Mentioning individuals or groups (@here, @channel, user groups) in automated messages. Approval must name the exact mention targets.
- Processing data classified as sensitive (credentials, health, financial, personnel matters, customer personal data).
- Turning on a live schedule with a frequency above the approved rate.

Proceed without a gate only for read-only analysis of data the requester already supplied, and drafting content in a non-posting context.

### Verification and evidence

Before declaring a flow ready, produce and attach:
- **Routing matrix:** every event type, target channel, owner, and escalation rule.
- **Replay results:** count of events in, messages out, suppressed duplicates, and misroutes. Target: zero misroutes and zero unintended mentions in the replay set.
- **Permission inventory:** each scope or permission requested, the reason, and a confirmation that no private-channel or DM read access is included unless approved.
- **Rate check:** projected messages per channel per hour at peak, compared against the platform's documented limits (verify current values).
- **Content check:** each template reviewed for leaked secrets, personal data, and raw stack traces or payloads.

Quality thresholds for go-live: duplicate rate under 2% in replay, every message has an owner and an action or an explicit "FYI" label, and rollback tested once in the sandbox.

### Failure handling

- **Post rejected or rate limited:** respect the retry-after guidance from the platform response; back off exponentially with a cap; do not retry more than the configured limit; log and alert the owner if the queue grows.
- **Authentication failure:** stop immediately. Do not attempt alternative credentials. Report the failure and request a credential owner to act.
- **Misrouted or duplicated message sent:** post a correction only in the affected channel and only after approval; do not delete the original without approval; record the incident.
- **Unexpected mention or external exposure:** halt the automation via the kill switch, notify the channel owner and workspace admin, and preserve logs.
- **Ambiguous routing rule:** default to the owner's test channel and ask for clarification rather than guessing a destination.

### Deliverable contract

Return a single bundle containing:
1. Message contract table (type, trigger, channel, action, severity, expiry).
2. Routing matrix and escalation thresholds.
3. Template set with variable names and sample rendered output.
4. Permission inventory and open approval requests, each marked pending.
5. Replay and rate-check results with measured numbers.
6. Rollout plan with stage gates, owner, rollback steps, and kill-switch location.
7. Version-sensitive items list: each API method, scope, limit, or payload detail, with the verification status "to verify against current official documentation" until confirmed.

Do not claim the automation is secure, compliant, or approved until the matching evidence and written approvals exist.


## search-visibility

**Use when:** Use when auditing, diagnosing, or improving how a business's website, pages, or listings appear in organic search results, including indexing problems, traffic drops, keyword and intent gaps, technical SEO issues, and local search profiles.

### Purpose and boundaries

This skill produces evidence-based diagnoses and prioritized plans for organic search visibility of a business's owned properties: website pages, product or service catalogs, blog content, and business listings (such as local directory profiles). It covers crawlability, indexability, on-page relevance, search-intent fit, internal linking, structured data, page experience signals, and local listing accuracy.

It does not cover paid search management, guaranteed ranking outcomes, link acquisition campaigns involving outreach to third parties, reputation management, or legal compliance review of marketing claims. Do not promise rankings, traffic figures, or timelines. Search engine behavior changes; treat all ranking-factor assumptions as hypotheses to test.

### Inputs and assumptions

Gather before analysis:

1. Site or property list, with the primary business goal (leads, sales, bookings, calls) for each.
2. Search Console or equivalent webmaster data for the last 16 months, if available: queries, pages, impressions, clicks, average position, coverage/indexing status.
3. Analytics data for organic sessions and conversions, same window.
4. Crawl export (URL, status code, canonical, meta robots, title, H1, word count, internal inlinks).
5. Top 20 to 50 commercial and informational target queries the business cares about, with the page currently intended to rank for each.
6. Competitor set: three to five domains that rank for those queries.
7. For local work: the business's registered listing data (name, address, phone, category, hours) as the authoritative source.

If any input is missing, state the assumption explicitly in the report and label the affected conclusions as provisional. Do not infer traffic or revenue figures that were not supplied.

### Operating workflow

1. **Establish the baseline.** Record organic clicks, impressions, average position, and indexed page count per property for the most recent 28 days and the same period prior year or prior quarter. Note any known changes (migrations, redesigns, template updates, pricing changes) with dates.
2. **Classify the problem.** Assign each observed symptom to one category: (a) not discovered, (b) discovered but not indexed, (c) indexed but not relevant to queries, (d) relevant but outcompeted, (e) ranking but not clicked, (f) clicked but not converting. Diagnosis drives the fix; do not jump to content rewrites before classification.
3. **Audit technical access.** Check robots directives, HTTP status codes, redirect chains (flag chains longer than one hop), canonical consistency, duplicate host variants (www and non-www, http and https), sitemap accuracy, and noindex tags on pages that should rank.
4. **Audit indexability at scale.** Compare the sitemap URL set, crawled URL set, and indexed URL set. Identify pages that are indexed but low-value (thin, parameterized, filtered duplicates) and pages that are valuable but absent from the index.
5. **Map queries to pages.** For each target query, identify the page that should rank and check whether its title, H1, opening paragraph, and headings match the dominant intent. Intent types: informational (guides, definitions), commercial investigation (comparisons, reviews), transactional (product or booking pages), navigational (brand or location pages). A mismatch between intent and page type is a primary defect.
6. **Compare against competitors.** For each target query, list the top three ranking page types (format, length class, content depth, presence of tools or pricing). Identify concrete gaps; do not recommend "more content" without naming the missing element.
7. **Review click-through.** For queries with position 1 to 10 and impressions above a threshold you set in the report, compare observed CTR with the expected band for that position. Low CTR with adequate position points to title and snippet defects.
8. **Check local listings where applicable.** Verify name, address, phone, and category consistency across the business's listed profiles against the authoritative record. Inconsistency is a defect to fix; note that the business must control the listing to edit it.
9. **Prioritize.** Score each finding by estimated impact (affected queries or pages, conversion relevance) and effort. Sort into: fix now, schedule, monitor.

### Decision gates

- **Gate A, before recommending a migration or URL change:** Confirm the change is required by a measured defect, not preference. Require a redirect map covering every changed URL with one-hop 301 targets, and a rollback plan. Halt and request explicit approval from the site owner before any change that alters live URLs, robots rules, or sitemaps.
- **Gate B, before recommending noindex or removal of pages:** Require evidence that the page receives no meaningful organic entrances or conversions. Get explicit approval before recommending removal.
- **Gate C, before any content rewrite:** Confirm the classification in step 2 is "relevant but outcompeted" or "ranking but not clicked." Rewrites for pages classified as technically blocked are wasted effort.
- **Gate D, external actions:** Any recommendation involving publishing to third-party platforms, editing listings the business does not control, outreach, or sending data outside the organization requires explicit owner approval and is listed separately.
- **Gate E, sensitive data:** Do not include personal data from analytics or user-submitted content in the deliverable. Aggregate or redact before reporting.

### Verification and evidence

Every finding must cite its evidence: the URL, query, metric, date range, or crawl field. Quality checks before delivery:

- Each recommendation maps to one classified problem and one measurable success metric (e.g., indexed count of a page set, impressions for a query cluster, CTR band, crawl error count).
- Re-crawl or re-check each fixed item within a window you specify, and compare against the baseline.
- Confirm that any Search Console or platform feature names, report locations, or setting paths are verified against current official documentation, since interfaces change. Mark them "verify before use."
- State confidence per finding: high (directly observed in data), medium (inferred from consistent patterns), low (hypothesis requiring test).

### Failure handling

- **Missing data:** Proceed with the reduced scope, list what was unavailable, and state which conclusions are blocked.
- **Conflicting signals** (e.g., rankings rose while clicks fell): Report both, check for SERP feature changes or query mix shifts, and avoid a single causal claim.
- **Suspected penalty or manual action:** Stop optimization work. Report the evidence and recommend the owner check the official webmaster console messages and consult qualified help.
- **Sudden large drop:** Check for recent deployments, robots or noindex changes, and migration dates before analyzing content. Escalate if traffic loss is severe and the cause is unidentified.

### Deliverable contract

Return a single report with these sections in order:

1. Executive summary (five bullets max, each with a metric).
2. Baseline table: property, period, clicks, impressions, average position, indexed pages.
3. Findings table: ID, classification, affected URLs or queries, evidence, confidence.
4. Prioritized action plan: action, owner role, approval gate triggered (if any), success metric, check date.
5. Open questions and missing inputs.
6. Items marked "verify before use" with the specific documentation to consult.

Do not include unsupported forecasts, ranking guarantees, or claims about algorithm internals presented as fact.

