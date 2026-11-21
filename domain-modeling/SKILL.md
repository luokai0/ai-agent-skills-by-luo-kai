---
name: domain-modeling
description: Use when designing or reviewing a domain model for a software system, including bounded contexts, aggregates, invariants, domain events, or context maps, or when code and data structures appear to disagree with the business rules they encode.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Domain Modeling

## Purpose and boundaries

Produce a model of the business domain that makes rules, vocabulary, and ownership explicit enough to drive design and code. In scope: identifying bounded contexts, naming concepts in the domain's own language, locating aggregates and their invariants, classifying entities versus value objects, defining domain events, and mapping relationships between contexts.

Out of scope: choosing infrastructure, selecting databases or frameworks, writing production code without a separate task, and estimating delivery effort. Do not treat a data-model diagram as a domain model; a domain model captures behavior and rules, not only tables.

## Inputs and assumptions

Required inputs: at least one of the following, with its source identified: domain experts' descriptions, existing requirements, process documents, current code or schemas, incident reports, or support tickets. Record which sources are authoritative for which rules.

Assumptions to state explicitly before modeling: who the domain experts are, which decisions the model must support, and which stakeholders will change the model later. If a rule has no identified owner, mark it as unverified rather than encoding it.

## Operating workflow

1. **Glossary first.** Collect the terms experts use for core concepts. Record each term with its definition and at least one counterexample of what it does not mean. Flag terms used with different meanings by different groups.
2. **Find context boundaries.** Look for places where the same word means different things, where different teams own different decisions, or where data is translated at a handoff. Draw one bounded context per coherent meaning. Name each context in domain language.
3. **Identify aggregates per context.** For each state change, ask which data must be consistent together in one transaction. Make the aggregate root the only entry point for changes.
4. **Write invariants as testable statements.** Example: "An order cannot be confirmed while its total is zero" or "A reservation's quantity never exceeds available stock at the time of confirmation." Each invariant names the aggregate that enforces it.
5. **Classify objects.** Use entities where identity matters across time (a customer account). Use value objects where equality by attributes is sufficient (a monetary amount with currency). Prefer value objects when in doubt.
6. **Define domain events** as past-tense facts emitted by an aggregate (for example, "PaymentCaptured"). Record the producer, the consumers, and what each consumer does with it.
7. **Map context relationships.** For each boundary crossing, record the direction of dependency, the translation direction, and the relationship type (for example, upstream/downstream, shared kernel, anticorruption layer, or published language). Use these labels as design vocabulary, not as a claim about any tool.

## Decision gates

- **Split a context** when two teams need to change the same rule for different reasons, or when a term's definition differs in a way that changes outcomes.
- **Merge contexts** when the translation between them is trivial and they always change together.
- **Create an aggregate boundary** only when the invariant truly requires atomic consistency. If consistency across the boundary is acceptable eventually, use an event instead.
- **Stop and escalate** when experts disagree on a rule that affects money, legal obligations, access rights, or personal data. Do not resolve these by assumption.

## Verification and evidence

Each model deliverable must satisfy these checks:

- Every glossary term appears in at least one rule or event, or is marked as unused.
- Every invariant names exactly one enforcing aggregate and cites its source.
- Every aggregate has a root and no external object mutates its internals.
- Every domain event has a named producer and at least one named consumer or an explicit "no consumer yet" note.
- Walkthrough check: a domain expert reviews three real scenarios (one normal, one edge, one failure) and confirms the model produces the expected outcome for each. Record the scenarios and the sign-off.
- Where existing code exists, compare each invariant against the code path that enforces it and list mismatches.

## Failure handling

- **Expert unavailable:** Keep the model in draft status, list the unverified rules, and do not promote them to specification.
- **Conflicting sources:** Record both versions, identify the owner, and request a decision. Do not silently pick one.
- **Code contradicts documented rules:** Report the discrepancy with file and location. Do not modify code to match the model without approval.
- **Model grows beyond the decision it serves:** Narrow the scope to the decisions currently needed and defer the rest in an explicit backlog list.

## Deliverable contract

Produce a single document with these sections in order: scope and decisions supported; glossary; bounded contexts with purpose and owner; aggregates with roots and invariants; entity and value object classification; domain events with producers and consumers; context map; open questions with owners; verification record listing the scenarios and sign-offs.

Mark any statement about a specific tool, notation standard, or framework feature as requiring verification against current official documentation before adoption.

## Approval controls

Obtain explicit approval before: altering or deleting existing production schemas, migrations, or event contracts; sharing domain documents containing personal, financial, or confidential data outside the approved group; and publishing a model that other teams will implement against. Do not make these changes as a side effect of modeling.