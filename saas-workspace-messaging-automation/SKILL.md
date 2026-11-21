---
name: saas-workspace-messaging-automation
description: Use when designing, building, or auditing an agent or automation that sends, routes, summarizes, or reacts to messages in SaaS workspaces such as Slack, Microsoft Teams, Discord, or email-linked team chat, including alert routing, digest generation, and notification bots.
author: Luo Kai
provenance: original
version: 1.0.0
---

# SaaS Workspace Messaging Automation

## Purpose and boundaries

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

## Inputs and assumptions

Collect before acting:
1. Target workspace platform and tenant (name only; never paste tokens).
2. Exact purpose of each message: who must act, by when, and what action.
3. Channel list with owners and their stated purpose.
4. Event sources (e.g., CI results, ticket updates, monitoring alerts) and their volume per hour and per day.
5. Required identity: bot user, app, or incoming webhook. Record who owns it.
6. Retention and privacy constraints from the workspace admin or data owner.

Assume nothing about API method names, scopes, rate limits, or payload limits. Treat them as version-sensitive and verify them against the current official platform documentation before writing code or configuration. Record the verification date and doc URL in the design notes.

## Operating workflow

1. **Define the message contract.** For each message type, write: trigger, recipient channel, required fields, action expected, severity, and expiry. A message without a required action must be informational and labeled as such.
2. **Map routing.** Create a table from event source to channel. One event type maps to at most one primary channel. Secondary escalation requires a rule with a stated threshold (for example, unacknowledged for 30 minutes).
3. **Set deduplication and rate control.** Define a dedupe key (for example, incident ID plus state) and a suppression window. Collapse repeated events into one updating message where the platform allows edits, otherwise into a counted summary.
4. **Design digests separately.** Digests run on a schedule, summarize at most the agreed number of items, link to sources, and never quote full message bodies from private contexts.
5. **Build a dry run.** Send output to a sandbox or private test channel owned by the requester. Replay at least 20 recorded historical events, or the full set if fewer exist.
6. **Review with the channel owner.** Show sample outputs for each message type. Do not enable live posting until the owner approves in writing.
7. **Stage rollout.** Enable one channel, observe for a defined period (default: 3 business days or 100 messages, whichever is longer), then expand.
8. **Document operations.** Record owner, on-call contact, kill switch location, and rollback steps.

## Decision gates

Stop and request explicit human approval before:
- Posting to any channel that is not the requester's test channel.
- Any action that is destructive or irreversible: deleting messages, archiving or renaming channels, removing members, revoking or rotating tokens.
- Sending anything that reaches people outside the workspace or outside the approved channel list.
- Using broader permissions than the stated purpose requires, or adding scopes that read private content.
- Mentioning individuals or groups (@here, @channel, user groups) in automated messages. Approval must name the exact mention targets.
- Processing data classified as sensitive (credentials, health, financial, personnel matters, customer personal data).
- Turning on a live schedule with a frequency above the approved rate.

Proceed without a gate only for read-only analysis of data the requester already supplied, and drafting content in a non-posting context.

## Verification and evidence

Before declaring a flow ready, produce and attach:
- **Routing matrix:** every event type, target channel, owner, and escalation rule.
- **Replay results:** count of events in, messages out, suppressed duplicates, and misroutes. Target: zero misroutes and zero unintended mentions in the replay set.
- **Permission inventory:** each scope or permission requested, the reason, and a confirmation that no private-channel or DM read access is included unless approved.
- **Rate check:** projected messages per channel per hour at peak, compared against the platform's documented limits (verify current values).
- **Content check:** each template reviewed for leaked secrets, personal data, and raw stack traces or payloads.

Quality thresholds for go-live: duplicate rate under 2% in replay, every message has an owner and an action or an explicit "FYI" label, and rollback tested once in the sandbox.

## Failure handling

- **Post rejected or rate limited:** respect the retry-after guidance from the platform response; back off exponentially with a cap; do not retry more than the configured limit; log and alert the owner if the queue grows.
- **Authentication failure:** stop immediately. Do not attempt alternative credentials. Report the failure and request a credential owner to act.
- **Misrouted or duplicated message sent:** post a correction only in the affected channel and only after approval; do not delete the original without approval; record the incident.
- **Unexpected mention or external exposure:** halt the automation via the kill switch, notify the channel owner and workspace admin, and preserve logs.
- **Ambiguous routing rule:** default to the owner's test channel and ask for clarification rather than guessing a destination.

## Deliverable contract

Return a single bundle containing:
1. Message contract table (type, trigger, channel, action, severity, expiry).
2. Routing matrix and escalation thresholds.
3. Template set with variable names and sample rendered output.
4. Permission inventory and open approval requests, each marked pending.
5. Replay and rate-check results with measured numbers.
6. Rollout plan with stage gates, owner, rollback steps, and kill-switch location.
7. Version-sensitive items list: each API method, scope, limit, or payload detail, with the verification status "to verify against current official documentation" until confirmed.

Do not claim the automation is secure, compliant, or approved until the matching evidence and written approvals exist.