---
name: clean-code-boundaries
description: Use when designing or reviewing module, service, or layer boundaries, deciding where a dependency should be inverted, wrapping third-party libraries, or untangling code where domain logic leaks into infrastructure, UI, or persistence.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Clean Code Boundaries

## Purpose and boundaries

This skill guides decisions about where one part of a codebase ends and another begins: which side owns a concept, which direction dependencies point, and what shape crosses the seam. It covers module and package boundaries, layer boundaries (domain, application, adapters, infrastructure), service interfaces, and wrappers around external systems such as databases, message brokers, payment or identity providers, and SDKs.

It does not cover: choosing a deployment topology, picking a framework, performance tuning of a single function, or rewriting a system wholesale. Redirect those to the appropriate skill or to a human architect.

## Inputs and assumptions

Before acting, gather:

- The module graph or import/dependency listing for the affected area.
- The concepts crossing the seam (entities, DTOs, events, errors, configuration).
- Known change pressures: which parts change often, which are stable, which are regulated.
- Whether the external system is owned by the team or a third party.
- Current test coverage at the seam.

Assume the codebase is in version control and that changes are reviewable. If the dependency graph cannot be obtained, state that the analysis is based on partial evidence and list what is unknown.

## Operating workflow

1. **Map the crossing.** List every import or call that crosses the candidate boundary, in both directions. Count them and group by concept.
2. **Classify each crossing.** Mark it as domain rule, orchestration, data shape, configuration, or side effect.
3. **Find inverted arrows.** Flag any domain or application code that imports infrastructure, framework types, ORM models, HTTP request objects, or vendor SDK types.
4. **Choose the owner.** The side that defines the meaning of a concept owns its type. Consumers depend on an interface or a port defined by the owner.
5. **Design the port.** Express the port in the owner's vocabulary (for example `PaymentCapture` with `capture(orderId, amount)`), not the vendor's (for example a raw SDK charge object). Keep it narrow: only operations the caller actually uses.
6. **Place translation at the edge.** Adapters convert between vendor types and owner types. Translation of errors belongs here too: vendor error codes become owner-defined failure categories.
7. **Migrate incrementally.** Introduce the port, route one call path through it, verify, then move the next. Do not change the boundary and its callers in one unreviewed step.
8. **Record the decision** in the module's documentation or an architecture decision record: the owner, the direction, and the reason.

## Decision gates

Proceed with inversion only if at least two hold:
- The external dependency is replaceable or already has more than one implementation or test double in use.
- Domain logic depends on it in more than one place.
- The vendor type appears in public signatures of domain code.

Do not introduce a boundary when:
- The seam has one caller, one implementation, and no expected change. Document it and leave it.
- The abstraction would simply mirror the vendor API method-for-method.
- The change would require coordinated releases across teams without an agreed owner.

Stop and request explicit approval before:
- Deleting or renaming a public interface, schema, queue topic, or API route.
- Changing data formats persisted or exchanged with external parties.
- Any migration that touches production data, or that changes behavior for external customers.
- Modifying authentication, authorization, payment, or audit-logging code paths.

## Verification and evidence

Each boundary change must produce:

- **Dependency evidence:** before and after import listing showing domain packages no longer import adapter or vendor packages. Target: zero such imports in the domain layer, verified by a repeatable command or lint rule available in the project's toolchain.
- **Behavioral evidence:** existing tests pass unchanged where behavior should be preserved. Where behavior is intentionally changed, the change is listed with its test.
- **Contract tests:** the port has a test suite that runs against both the real adapter (in a controlled environment) and an in-memory fake, asserting identical observable results for the operations the domain uses.
- **Coverage at the seam:** adapter translation logic has tests for each mapped error category and each mapped field.

Do not claim a reduction in coupling without the before-and-after dependency listing. Do not state that a change improves maintainability or performance without measurement.

## Failure handling

- If the dependency listing reveals a cycle that cannot be broken without a redesign, stop, document the cycle, and propose options with trade-offs rather than introducing a workaround interface that hides it.
- If a port leaks vendor concepts discovered late, revise the port in its own change; do not patch callers with vendor-specific branches.
- If tests fail after migration, revert the single step, identify whether the fault is in translation, port semantics, or a hidden side effect, and fix that before continuing.
- If the vendor's documented behavior is unclear or version-dependent, mark the adapter behavior as "to be verified against current official documentation" and do not encode assumptions as fact.

## Deliverable contract

The final output of this skill is a boundary report containing:

1. Scope: the seam, the modules involved, and what was excluded.
2. Crossing inventory: a table of crossings with classification and direction.
3. Proposed or applied ownership decisions, each with the owner, port signature, and adapter responsibility.
4. Verification results: dependency listings before and after, test results, and contract test status.
5. Open risks and items requiring approval, listed explicitly.
6. Unknowns and any version-sensitive details flagged for verification against current official documentation.

What not to do:
- Do not create interfaces for every class by reflex.
- Do not let adapters contain business rules.
- Do not expose ORM entities, HTTP request objects, or SDK types across the port.
- Do not hide circular dependencies behind generic "manager" or "service locator" abstractions.
- Do not present unmeasured improvements as results.