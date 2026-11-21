---
name: communications-messaging
description: Use when drafting, reviewing, sending, or tracking messages exchanged with external registries (corporate, trademark, domain, package, product, or professional registries), including change notifications, status inquiries, correction requests, and deficiency responses.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Communications Messaging

## Purpose and boundaries

This skill governs correspondence between an organization and an external registry operator or its staff. It covers:

- Drafting outbound messages: change notices, status inquiries, correction requests, deficiency responses, and fee or document follow-ups.
- Reviewing inbound registry messages and extracting required actions and deadlines.
- Maintaining a correspondence log that ties each message to a registry record.

It does not cover filing the underlying registration itself, legal opinions on registry rules, or internal-only communications. Do not use it to contact a registry on a person's behalf without that person's written authorization.

## Inputs and assumptions

Before drafting, confirm:

1. Registry name, jurisdiction, and the specific record identifier (entity number, mark or application number, domain, package name, or listing ID).
2. The purpose of the message and the desired outcome.
3. The authorized sender and signatory, and whether they are allowed to speak for the organization.
4. The current correspondence history for that record.
5. Any deadline stated in an inbound message, and its time zone.
6. The channel the registry specifies (portal, email address, postal address, form). Use only channels listed on the registry's official site.

Assume nothing about current registry rules, fees, forms, or response times. Mark any such detail as "verify against current official registry documentation" in the draft and in the log.

## Operating workflow

1. **Classify the message**: notice, inquiry, correction, deficiency response, or complaint. The class determines the tone, evidence, and approval level.
2. **Pull the record context**: current status, last contact date, open deadlines, and prior commitments made to the registry.
3. **Extract facts**: list every factual claim the message will make, with its source document and date. Remove any claim without a source.
4. **Draft in plain structure**: opening line stating the record and purpose; numbered facts; a single explicit request or statement; attachments listed by name and version; contact details for follow-up.
5. **Check tone and scope**: one topic per message. No speculation, no admissions of liability, no disputes of registry decisions beyond the stated procedure.
6. **Route for approval** (see Decision gates).
7. **Send through the authorized channel**, then record the sent timestamp, channel, recipient, attachment hashes, and reference number returned by the registry.
8. **Diary the follow-up**: set a review date based on the registry's stated timeline, or flag it as unknown and requiring verification.

## Decision gates

Stop and obtain explicit written approval from the accountable owner before:

- Sending any message that changes, withdraws, or certifies a registry record.
- Submitting a payment, a sworn statement, or a signed declaration.
- Disclosing personal data, financial data, unpublished product or trademark information, or security details.
- Sending any message that concedes a fact, admits non-compliance, or commits to a remedy or deadline.
- Contacting a registry through a channel other than the one it publishes, or contacting staff directly outside the normal process.
- Sending a second message on a record that already has an unanswered inquiry less than the stated response window old.

Route an inbound message to a human reviewer without drafting a reply if it threatens enforcement, cites legal proceedings, or requests information you cannot verify.

## Verification and evidence

Before approval, check:

- Every factual statement traces to a dated source.
- The record identifier matches the registry's own record, not an internal name.
- Attachments open, match the stated version, and contain no unrelated personal or confidential data.
- The request is answerable: it names one action the registry can take.
- Deadlines are converted to the registry's stated time zone and recorded with the source citation.

After sending, confirm receipt through the registry's acknowledgment or reference number. Record a measurable closure target: for example, "response expected within the window stated in the registry's most recent published guidance; if none is stated, escalate after 10 business days of silence." Mark the window as requiring verification.

## Failure handling

- **Bounced or rejected message**: do not resend through a different channel. Log the rejection reason, verify the channel on the official site, and request approval before resending.
- **No response by the review date**: send one follow-up referencing the original reference number. Do not send a third message without escalation approval.
- **Inbound message with unclear or conflicting requirements**: stop, do not guess, and request clarification through the stated contact channel after approval.
- **Wrong record or misdirected message**: notify the registry promptly, do not forward the content further, and log the incident for the data-handling owner.
- **Missed deadline**: escalate immediately to the accountable owner with the original deadline, the source citation, and the current status. Do not characterize the miss in outbound messages without approval.

## Deliverable contract

Each completed task produces:

1. The final message text, marked with status: draft, approved, or sent.
2. A correspondence log entry: record identifier, registry name, message class, sender, approver, channel, send timestamp, reference number, attachments with versions, open deadlines, and source citations.
3. A list of items marked for verification against current official registry documentation.
4. A short handoff note stating the next action, its owner, and its date.

Quality is met when every claim is sourced, every send is approved where a gate applies, every log entry is complete, and no message contains unverified rules, fees, or timelines.