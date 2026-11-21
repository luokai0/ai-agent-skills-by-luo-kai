---
name: wellbeing-symptom-tracking
description: Use when a user wants to log, structure, or review personal or client wellbeing symptoms over time, including symptom diaries, trend summaries, and handoff notes for a clinician or coach, and when red-flag symptoms may need escalation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Wellbeing Symptom Tracking

## Purpose and boundaries

This skill turns scattered symptom reports into a consistent, time-stamped record, summarizes patterns, and prepares accurate handoffs. It supports people who track their own wellbeing and professionals (coaches, wellness practitioners, care coordinators) who document client-reported symptoms.

It does not diagnose, prescribe, adjust medication, interpret lab results as clinical findings, or replace emergency care. It records and organizes; clinical judgment belongs to the qualified professional.

## Inputs and assumptions

Collect or confirm before logging:

- Symptom description in the person's own words, plus a short neutral restatement.
- Onset date or time, duration, and whether it is continuing.
- Severity on a stated scale (for example 0 to 10), with the scale's anchors defined by the person.
- Possible triggers, context, sleep, activity, and medications as reported. Record them as reported, not as causes.
- Who will read the output and for what purpose.

Assumptions to state explicitly in every output: entries reflect self-report, timing may be approximate, and the record is incomplete unless the person confirms otherwise.

## Operating workflow

1. Classify the request: single entry, longitudinal review, or handoff summary.
2. Screen for red flags before any other work (see Decision gates).
3. Normalize each entry into fixed fields: date/time, symptom, severity, duration, frequency, triggers reported, actions taken, outcome.
4. Keep the person's original wording in a separate field; never overwrite it with paraphrase.
5. For reviews, order entries chronologically and group by symptom, not by theme you have inferred.
6. Compute simple descriptive facts only: frequency per week, median severity, count of days with symptom present, change in average severity between two stated windows.
7. Describe patterns as observations with the number of supporting entries (for example "reported on 9 of 14 days, mostly after reported late nights"). Avoid causal language.
8. Produce the deliverable in the contract format.

## Decision gates

- **Immediate escalation gate:** If any entry describes chest pain, difficulty breathing, fainting, stroke-like signs, thoughts of self-harm or harming others, severe bleeding, or sudden severe headache, stop the summary work. Tell the user to contact emergency services or a crisis line in their region now, and flag the record for the responsible professional. Do not reassure or minimize.
- **Urgent review gate:** Worsening trend over three or more consecutive entries, new symptom in a person already on monitoring, or severity at the top of the stated scale for more than two consecutive days. Recommend prompt professional contact and mark the summary "needs clinician review."
- **Sharing gate:** Any export, transmission to a third party, or inclusion in a shared document requires explicit approval from the person whose data it is, naming the recipient and the content. Obtain it before producing a shareable version.
- **Deletion or alteration gate:** Editing or deleting past entries requires explicit confirmation. Prefer appending corrections with a dated note.
- **Scope gate:** If the user asks for a diagnosis, treatment change, or interpretation of medical tests, decline that part, give the supported summary, and recommend the appropriate professional.

## Verification and evidence

Before delivering, check:

- Every summary statistic traces to a listed entry. Show the entry count and date range.
- No symptom appears that was absent from the source entries.
- Original wording is preserved verbatim in the source field.
- Dates are consistent, in ISO format, with no entries out of sequence.
- Causal words ("caused," "due to," "because of") do not appear unless the person themselves attributed the cause, and then they are quoted as attributions.
- Red-flag screen was run and its result is stated.
- Limitations line is present.

## Failure handling

- Missing dates: record "date unknown," do not estimate silently; ask for approximate ranges.
- Conflicting entries for the same day: list both with sources; do not average them.
- Severity scale changed mid-record: report the two periods separately.
- Ambiguous symptom description: ask one clarifying question rather than guessing a category.
- Input suggests a medical emergency: follow the escalation gate first, then resume only if the person confirms they are safe and help is in progress.

## Deliverable contract

Return:

1. Header: subject label, date range, entry count, data source (self-report or professional entries).
2. Red-flag status: "none identified" or the flagged items with the action recommended.
3. Chronological log table: date, symptom, severity, duration, reported triggers, verbatim note.
4. Descriptive summary: 3 to 6 bullet observations, each with supporting entry count.
5. Open questions for the person or clinician.
6. Standard limitation statement: "This summary organizes self-reported information. It is not a diagnosis or treatment recommendation."

Do not include: diagnostic labels, treatment or dose advice, unsupported causal claims, invented normal ranges, or content from entries outside the requested date range.