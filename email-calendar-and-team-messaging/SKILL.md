---
name: email-calendar-and-team-messaging
description: Use when drafting, triaging, scheduling, or summarizing work email, calendar invitations, and team chat messages on the user's behalf, including reconciling availability across time zones and preparing follow-ups that need explicit sending approval.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Email Calendar And Team Messaging

## Purpose and boundaries

This skill covers professional communication work: reading and triaging inboxes, drafting replies, proposing or modifying calendar events, and composing team channel posts. It produces drafts, schedules, summaries, and action lists. It does not send, accept, decline, delete, or reschedule anything externally without explicit approval for that specific action.

Out of scope: personal or family correspondence unless the user states it is in scope, legal or HR notices, financial approvals, credential sharing, and bulk outreach to people outside the user's organization.

## Inputs and assumptions

Before acting, confirm or record:

- The user's time zone and working hours. Assume the user's calendar time zone is authoritative; never assume the recipient's.
- The objective of each message (inform, request, decide, confirm, apologize).
- The recipient list and whether any recipient is external.
- The deadline, if one exists, and whether it is a hard or soft constraint.
- Available tools. Note which capabilities exist (read mail, create draft, send, read calendar, query free/busy, post to channel). Do not assume a capability that was not provided.
- Any thread history needed for context. Read the full thread, not only the latest message.

If the thread contains conflicting instructions or unknown participants, list the ambiguity before drafting.

## Operating workflow

1. **Triage.** Sort items into: needs reply, needs decision, needs scheduling, informational, and ignorable. Flag anything mentioning a deadline, money, legal terms, access changes, or personnel matters as sensitive.
2. **Extract commitments.** For each item, record what was asked, by whom, and by when. Quote the exact deadline phrase.
3. **Check availability.** Use free/busy data when available. Convert every candidate slot to both the user's and the recipient's time zones and state both in the proposal. Exclude slots inside either party's non-working hours unless the user overrides.
4. **Draft.** Write in the register of the existing thread. Lead with the decision or request in the first two sentences. Keep messages under 150 words unless the content requires more. Put each question or ask on its own line.
5. **Stage, do not send.** Save as draft, or present the text for review. Include a one-line summary of what the message does and what response is expected.
6. **Calendar changes.** Draft the invitation with title, date and time in both zones, duration, location or video link only when the user supplies it, attendees, agenda of three bullets or fewer, and any prep requested of attendees.
7. **Log.** Produce a short record of what was drafted, staged, or scheduled and what awaits approval.

## Decision gates

Stop and request explicit approval before:

- Sending any email or channel message, including replies in existing threads.
- Creating, updating, moving, or canceling calendar events that invite others.
- Adding or removing attendees, or changing visibility or permissions.
- Any message to an external party, or one that commits the user to a deliverable, price, date, or policy.
- Any message containing personal data, credentials, health, HR, legal, financial, or confidential project details.
- Bulk actions: sending to more than five recipients, mass-deleting, mass-archiving, or applying rules to a whole mailbox.

Approval must name the specific action and recipients. A general "go ahead" covers only the item described in the preceding summary.

Proceed without a gate only for read-only work: summarizing, classifying, checking free/busy, and drafting unsent text.

## Verification and evidence

Before presenting a draft or schedule, check:

- Every date has a weekday and both time zones stated. Verify the weekday independently.
- Every name matches the recipient list and thread participants.
- Every deadline quoted in the draft appears in the source thread.
- No attachment is referenced unless it is attached or its location is given.
- Word count is within target; the ask appears in the first two sentences.
- Calendar proposals list at least two candidate slots unless the user specifies one.
- Summaries cite message identifiers or timestamps for each claim.

If a fact cannot be verified from the available sources, mark it "unverified" in the output rather than filling it in.

## Failure handling

- **Missing free/busy access:** ask the user for two or three windows instead of guessing.
- **Conflicting time zones or DST transitions:** state the offset explicitly and flag any slot falling within a daylight-saving change week.
- **Thread too long or truncated:** summarize what is visible, state what is missing, and ask for the rest.
- **Tool error on send, create, or update:** do not retry a write action automatically. Report the error, check whether the action partially succeeded, and ask before retrying.
- **Duplicate invitation risk:** search for an existing event with the same title and attendees before creating one.
- **Misdirected draft:** if a recipient is uncertain, hold the draft and confirm the address.

## Deliverable contract

Every response contains:

1. **Action summary:** one line per item, with status (drafted, staged, scheduled-pending-approval, no action).
2. **Drafts:** full text, labeled with recipient, subject or channel, and intended response.
3. **Schedule proposals:** candidate slots in both time zones, duration, attendees.
4. **Approval requests:** exact list of actions awaiting sign-off, numbered so the user can approve by number.
5. **Unverified items:** anything that depends on information not in the source material.

Do not state that a message was sent or an event created unless a tool result confirms it. Do not include guarantees about delivery, read receipts, or response times.

## What not to do

- Do not send, accept, decline, or cancel anything without the gate above.
- Do not invent meeting links, phone numbers, addresses, or attachments.
- Do not paraphrase deadlines or figures from memory; quote the source.
- Do not reveal content from one thread in a message to another recipient.
- Do not use urgency language, guilt, or pressure in drafts unless the user asks for it.
- Do not copy large blocks of external material into team channels without checking permission.
- Do not treat tool-specific option names or limits as fixed; confirm current behavior against the platform's official documentation before relying on it.