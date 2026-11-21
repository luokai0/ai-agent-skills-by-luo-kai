---
name: pattern-selection-and-implementation
description: Use when choosing, applying, or reviewing a software design pattern (creational, structural, behavioral, or architectural) for a concrete code change, and when a team needs to justify whether a pattern is warranted or should be avoided.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Pattern Selection And Implementation

## Purpose and boundaries

This skill guides selecting a design pattern for a specific problem, implementing it with minimal footprint, and verifying that it removes the forces it was chosen to address. It covers object-level patterns (factory, strategy, adapter, decorator, observer, state, command, repository), module-level boundaries (facade, anti-corruption layer, ports and adapters), and integration-level patterns (retry wrappers, circuit breakers, outbox) when they appear inside application code.

It does not cover: choosing a full system architecture (microservices versus monolith), selecting infrastructure products, or rewriting an existing codebase to a new paradigm. Route those to architecture decision work.

## Inputs and assumptions

Before selecting anything, collect:

- The concrete change: the behavior to add, modify, or isolate.
- The forces: what varies, what is stable, how often the variation occurs, and who changes it.
- Constraints: language, framework, team familiarity, performance budget, backward compatibility requirements.
- Existing idioms in the codebase. Match them unless they are the problem.

Assume the team has not yet committed to a pattern. If a pattern is already named in the request, verify it fits the forces before implementing it.

## Operating workflow

1. **State the forces in one paragraph.** Example: "Three payment providers with different request shapes; a fourth is planned within two quarters; callers must not branch on provider."
2. **Count the variants and their stability.** One variant plus a hypothetical future is not a pattern case. Two or more existing variants that change independently usually is.
3. **Enumerate candidate patterns (two to three).** For each, write the one-line mechanism and the cost it adds (new types, indirection, lifecycle complexity).
4. **Apply the decision gates below.** Select the simplest candidate that passes all gates.
5. **Implement at the seam, not everywhere.** Place the pattern at the boundary where variation enters. Keep the rest of the code direct.
6. **Write the characterization test first** for existing behavior when modifying legacy code, so the refactor can be checked.
7. **Refactor in small steps,** running tests after each step.
8. **Verify against the forces** (see Verification).

Domain examples:
- Payments: a Strategy selected by provider identifier, with a registry constructed at startup. Callers pass a domain request, never provider-specific payloads.
- Report export: a Template Method is overkill for two formats; a plain function per format plus a dispatch map suffices.
- Legacy SDK integration: an Adapter translating the SDK's model into the domain model, placed at the module edge, prevents SDK types leaking inward.
- Order state: an explicit state enumeration with a transition table often beats the State pattern when there are fewer than about five states and transitions are simple.

## Decision gates

Proceed with a pattern only if all apply:

- **Gate 1 - Variation is real:** at least two current variants, or one variant with a documented near-term second, with a named owner.
- **Gate 2 - Variation is isolated:** the variation can be confined to one seam without touching most callers.
- **Gate 3 - Indirection pays off:** the added types and indirection are fewer than the duplicated or conditional logic removed. Count both.
- **Gate 4 - Team can maintain it:** a developer unfamiliar with the pattern can locate the variant point within five minutes using names alone.

Reject the pattern and use plain code if: there is one variant with no evidence of a second; the switch has three or fewer cases and changes rarely; the pattern requires reflection or runtime magic the codebase does not already use; or the pattern duplicates a language feature (for example, a first-class function where a single-method interface is proposed).

## Verification and evidence

Each change must produce:

- Before/after count of conditional branches on the variant axis in callers (target: zero branches on variant identity outside the seam).
- Existing tests pass unchanged, except tests that assert on internal structure, which must be justified.
- A test per variant exercising the seam contract, plus one test for unknown-variant handling.
- A test demonstrating the new variant can be added by creating one new type and one registration, without editing existing callers. Build this as an executable check, not a claim.
- Performance check where the path is hot: measure before and after on the project's own benchmark harness; do not estimate.

Framework or library APIs used in the implementation are version-sensitive. Verify method signatures, lifecycle semantics, and dependency-injection registration rules against current official documentation for the pinned version before finalizing.

## Failure handling

- **Pattern makes callers harder to read:** revert to the simpler candidate from step 3 and record why.
- **Second variant turns out to differ in shape:** the interface was too narrow. Widen it deliberately, update all variants, and note the change; do not add optional parameters that only one variant uses.
- **Hidden coupling appears** (variant needs caller state): move that data into the request object rather than giving the variant a back-reference.
- **Tests fail only after refactor:** inspect whether behavior or ordering changed; restore the characterization baseline before proceeding.

## Deliverable contract

Return:

1. Forces summary (one paragraph).
2. Candidate table: pattern, mechanism, added types, gates passed or failed.
3. Chosen pattern with the rejection reason for each alternative.
4. Seam location (file and symbol names as they exist in the repository).
5. Diff or implementation plan, step-ordered.
6. Verification results: test outcomes, branch-count before/after, extension-test evidence.
7. Open risks and any version-sensitive items pending verification against official documentation.

Do not: introduce a pattern to satisfy a checklist; add abstractions for hypothetical future variants without an owner; change public interfaces without an explicit approval step; delete or rewrite existing tests to make them pass; or propagate provider-, vendor-, or framework-specific types beyond the seam. Changes that alter public APIs, data formats, persisted state, or deployed behavior require explicit approval from the code owner before implementation.