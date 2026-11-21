---
name: knowledge-documents-legal-productivity
description: Use when drafting, summarizing, or maintaining legal knowledge documents (memos, clause libraries, precedent summaries, filing checklists, entity briefs) that rely on records from external registries such as corporate, IP, land, court, or regulatory registers.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Knowledge Documents Legal Productivity

## Purpose and boundaries

This skill produces and maintains legal knowledge documents whose factual claims come from external registries. It covers: extracting facts from registry records, reconciling them across sources, drafting reusable documents with traceable provenance, and flagging stale or conflicting entries.

It does not cover: giving a final legal opinion, filing or submitting anything to a registry, altering registry data, or advising on jurisdictions where the user has not confirmed applicable law. Output is a working draft for a qualified reviewer.

## Inputs and assumptions

Required inputs:
- The document purpose (memo, clause library entry, entity brief, deadline tracker, precedent note).
- The registry records or extracts supplied by the user, with source name, jurisdiction, and retrieval date.
- The intended audience and jurisdiction.

Assumptions to state explicitly in the document:
- Registry data reflects the record as of the retrieval date, not necessarily today.
- Registry field names, fee schedules, filing deadlines, and portal behavior change. Treat any such detail as version-sensitive and mark it "verify against current official documentation."
- Records are not guaranteed complete or accurate. Registries can lag filings, contain typos, or reflect pending changes.

If a required input is missing, ask for it. Do not fill gaps from memory.

## Operating workflow

1. **Scope the document.** Write one sentence stating the question the document answers and its jurisdiction. If it answers more than one question, split it.
2. **Inventory sources.** List each registry record with: registry name, jurisdiction, record identifier, retrieval date, and whether it is an official extract or a third-party copy.
3. **Extract facts into a table.** One row per fact: field, value, source ID, retrieval date. Quote values exactly, including punctuation and date formats.
4. **Reconcile conflicts.** Where two sources disagree, record both values and do not choose silently. Rank by authority: official registry extract over secondary compilation; more recent retrieval over older; filed document over summary.
5. **Draft the body.** Each factual sentence must cite a row in the fact table. Analysis sentences must be labelled as analysis.
6. **Add a freshness block.** Date of retrieval, date of next review, and triggers for re-check (filing events, statutory changes, name changes, insolvency notices).
7. **Run the verification checks** in the next section before presenting.

## Decision gates

Stop and request explicit approval before:
- Submitting, amending, or certifying anything with a registry or court.
- Sending the document to a counterparty, client, or regulator.
- Overwriting or deleting an existing knowledge document that other matters rely on; create a new version instead.
- Including personal data beyond what the purpose requires (identity numbers, home addresses, dates of birth). Redact by default.
- Relying on a single unofficial source for a fact that carries legal consequence (ownership, insolvency status, deadlines, sanctions screening).

Proceed without a gate when the task is internal drafting from supplied, cited records and no external action is taken.

## Verification and evidence

Before presenting, confirm:
- Every factual sentence maps to a fact-table row. Target: zero uncited facts.
- Every source row has an identifier and a retrieval date. Target: 100% completeness.
- All conflicts are listed in a "Discrepancies" section, not resolved silently.
- Dates are normalized to ISO 8601 in the table, with the original string preserved alongside.
- Deadlines are computed from a stated rule and anchor date, and shown with the rule text.
- Version-sensitive items are marked for verification.

Report the counts: facts extracted, sources used, discrepancies found, items marked for verification.

## Failure handling

- **Source unavailable or unreadable:** mark the affected section "unverified," do not infer content, and list what is needed to complete it.
- **Conflicting official sources:** present both, state the conflict, and escalate. Do not average or merge values.
- **Stale record (retrieval older than the document's review window):** flag in the freshness block and require re-retrieval before reuse.
- **Jurisdiction unclear:** stop and ask. Do not default to a home jurisdiction.
- **Requested conclusion exceeds the sources:** state what the sources do not establish.

## Deliverable contract

The final document contains, in order:
1. Title, question answered, jurisdiction, and author placeholder left for the reviewer to complete.
2. Summary (maximum 150 words), every claim cited.
3. Fact table with source IDs and retrieval dates.
4. Analysis, clearly labelled.
5. Discrepancies and open items.
6. Freshness block and re-check triggers.
7. Verification report with the counts listed above.

Do not include: unsourced legal conclusions, personal data beyond stated need, claims of registry or regulatory compliance, or any statement that a filing was made or approved.