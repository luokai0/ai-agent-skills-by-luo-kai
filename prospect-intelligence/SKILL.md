---
name: prospect-intelligence
description: Use when researching a specific prospective customer, partner, investor, or acquisition target to build an evidence-backed profile, qualify fit, identify buying triggers, and prepare outreach or meeting briefs from public and user-supplied information.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Prospect Intelligence

## Purpose and boundaries

This skill turns a named organization (and optionally named contacts) into a decision-ready brief: who they are, whether they fit, what has changed recently, who likely decides, and what a credible first conversation looks like. It covers B2B sales prospecting, partnership scouting, investor and acquirer screening, and vendor due diligence at a light level.

Out of scope: covert information gathering, accessing non-public records without authorization, scraping behind logins, personal profiling of individuals beyond professional role, inferring protected characteristics, generating bulk unsolicited outreach, and making legal, financial, or compliance determinations about the target.

## Inputs and assumptions

Required: target organization name, and the user's goal (sell, partner, invest, acquire, evaluate vendor).

Helpful: user's offering and ideal customer profile, known contacts and their titles, existing relationship status, geography constraints, and any internal notes the user is permitted to share.

Assumptions to state explicitly in the brief: the date of research, the sources consulted, and that facts are as of that date. If the target name is ambiguous (common names, subsidiaries, recent mergers), stop and confirm the correct entity before proceeding.

## Operating workflow

1. **Confirm entity.** Record legal name, domain, headquarters, parent or subsidiary relationships, and any prior name changes.
2. **Establish fit.** Compare the target against the user's ideal customer profile on firmographics (size band, industry, geography, revenue model, funding stage) and technographics only where publicly observable. Score each criterion as met, unmet, or unknown. Do not treat unknown as met.
3. **Collect recent signals.** Look for dated, primary-source events from the last 6–12 months: leadership changes, funding or debt announcements, product launches, regulatory filings, hiring concentrated in a relevant function, public statements about strategy, layoffs or restructuring, and new partnerships. Record each signal with date, source, and a one-line relevance note.
4. **Map the buying context.** Identify the function most likely to own the problem, typical decision roles (economic buyer, technical evaluator, champion, blocker), and any stated initiatives that the offering maps to. Use only roles visible in public company materials or user-provided contacts.
5. **Identify the wedge.** Name one specific, testable reason to engage now, tied to a signal. If no signal supports timing, say so and recommend a lower-intensity approach.
6. **Draft the approach.** Produce a short first-touch angle and two to three discovery questions. Reference only facts from the brief.
7. **Assemble the brief** using the deliverable contract below.

## Decision gates

- **Gate A (entity):** Proceed only if the entity is unambiguous. If two plausible entities exist, return both with a question.
- **Gate B (fit):** If three or more core criteria are unmet, recommend deprioritizing and stop deep research unless the user overrides with a stated reason.
- **Gate C (outreach):** Before any message is sent, drafted for sending, or contact data is exported to a CRM or sequencing tool, obtain explicit user approval. Confirm the recipient is a business contact and that the user has a lawful basis to contact them under applicable rules (for example, consent or legitimate-interest analysis for their jurisdiction). Do not state legal conclusions; flag the question for the user's counsel or compliance function when unclear.
- **Gate D (sensitive data):** Do not collect or store personal contact details, home addresses, family information, health or financial details of individuals, or anything the target has signaled it does not want shared. Stop and ask before handling any such data.
- **Gate E (external action):** Any step that submits forms, contacts the target, creates records in external systems, or posts publicly requires explicit approval for that specific action.

## Verification and evidence

- Every factual claim carries a source and an access date. Claims without a source are labeled "unverified" or removed.
- Prefer primary sources: company filings, official newsrooms, regulator databases, the company's own website, and direct user-provided documents. Treat aggregator summaries and AI-generated profiles as leads only.
- Corroborate any signal that would change the recommendation with a second independent source.
- Dates must be absolute (YYYY-MM-DD), not relative ("last month").
- Quality checks before delivery: at least 3 dated signals or an explicit statement that none were found; every fit criterion marked met, unmet, or unknown; no unsourced numbers; no individual personal details; discovery questions reference real gaps.
- Do not state revenue, headcount, or funding figures as current unless a dated source supports them.

## Failure handling

- **Sparse public information:** Deliver a partial brief marked with confidence level low, list what could not be found, and recommend specific user-provided inputs that would close gaps.
- **Conflicting sources:** Report both values with sources and dates; do not average or pick silently.
- **Stale sources (over 18 months for signals):** Mark as historical context, not current trigger.
- **Entity changed (acquisition, rename):** Re-run Gate A and report the transition.
- **Blocked or restricted access:** Do not circumvent. Note the limitation and continue with accessible sources.
- **User requests covert tactics or personal profiling:** Decline that element, explain the boundary briefly, and offer the compliant alternative.

Never invent contact names, titles, or email patterns. If a role is unknown, say "role not confirmed."

## Deliverable contract

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