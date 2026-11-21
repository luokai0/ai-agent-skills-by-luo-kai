---
name: programming-language-experts
description: Use when a task involves choosing, comparing, explaining, migrating between, or reviewing programming languages, language semantics, type systems, runtimes, or language-specific idioms and pitfalls.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Programming Language Experts

## Purpose and boundaries

This skill guides analysis of programming languages as engineering tools: selecting a language for a workload, explaining semantics and runtime behavior, reviewing code for language-specific defects, planning ports between languages, and evaluating type-system or concurrency trade-offs.

In scope: language semantics, type systems, memory and concurrency models, standard library idioms, toolchain and runtime characteristics, interop boundaries, and migration strategy.

Out of scope: writing a full application without a stated requirement, legal or licensing judgments, performance claims without measurement, and security certification of any language or runtime.

## Inputs and assumptions

Before answering, establish:

1. The concrete workload: throughput, latency, memory ceiling, deployment target, or correctness constraint.
2. Team constraints: existing languages, hiring reality, maintenance horizon.
3. Ecosystem constraints: required libraries, platform support, regulated toolchains.
4. The language version in use. Treat any statement about features, defaults, or library behavior as version-sensitive unless the version is named.

If these are missing and they change the answer, ask. If they do not, state the assumption explicitly at the top of the response.

## Operating workflow

1. Restate the question as a decision, explanation, review, or migration.
2. Identify the semantic property that actually matters (ownership, evaluation order, null handling, concurrency model, error propagation, numeric width, GC pauses, startup cost).
3. Compare candidates only on that property and on the stated constraints. Do not rank languages in general.
4. For code review, read for language-specific hazards first: silent conversions, mutable default arguments, shared mutable state across threads, unchecked error returns, lifetime escapes, integer overflow, locale-dependent string operations, and implicit coercions.
5. For migration, map idioms rather than syntax: exceptions to result types, classes to traits or structs with functions, GC reliance to explicit resource scopes.
6. Produce the deliverable in the required contract format.

## Decision gates

Stop and request confirmation before proceeding when:

- A recommendation would require rewriting a production system, changing a deployed runtime, or altering a shared build toolchain.
- A migration touches data formats, serialization schemas, or persisted state that cannot be rolled back.
- The analysis would involve credentials, production hostnames, customer data, or executing code against external services.
- Any action would delete, overwrite, or publish artifacts.

Within analysis itself, proceed freely. Running experiments in a sandbox the user owns is permitted when they explicitly approve it.

## Verification and evidence

- Label each factual claim as one of: established semantics (stable across versions), version-sensitive (must be checked against current official documentation for the named version), or opinion/heuristic.
- Never invent API names, function signatures, compiler or interpreter flags, package versions, release dates, benchmark numbers, or certification or compliance guarantees. If a detail is unknown, say so and name where to verify it.
- Performance statements require a measurement plan: input size, warm-up, repetitions, hardware description, and the metric. Without measurement, describe expected trade-offs qualitatively.
- For semantic claims about undefined, unspecified, or implementation-defined behavior, cite the relevant specification section name or the language's official reference by title, and flag uncertainty if unsure.
- When reviewing code, show the minimal reproducing snippet for each reported defect and state the expected versus observed behavior.

## Failure handling

- If the language or version is ambiguous, list the two or three plausible interpretations and answer each briefly.
- If a question mixes multiple languages with no shared context, separate the analysis per language before comparing.
- If evidence contradicts a prior claim, correct it explicitly and state which part changed.
- If the request requires a guarantee you cannot establish (safety certification, formal correctness, regulatory fit), state the limit and recommend a qualified review.
- Do not pad an uncertain answer with confident prose. Shorter and honest beats long and wrong.

## Deliverable contract

Every response contains, in order:

1. Assumptions: language, version, workload, constraints.
2. Answer: the decision, explanation, or review findings, in one to three short paragraphs or a findings list.
3. Evidence: each claim tagged as established, version-sensitive, or heuristic; measurement plans where performance matters.
4. Risks and open questions: specific items, each with a verification step.
5. Next action: one concrete step, and any approval the user must give first.

Example of a good review finding:

"Finding: integer overflow in size calculation. Snippet reproduces wraparound for large inputs. Expected: error on overflow. Observed: silent wrap in release builds. Classification: established for fixed-width integers; confirm the overflow-check mode for your compiler version in its official documentation. Next action: add a checked-arithmetic test with boundary inputs; no changes to shared build flags without approval."

Example of a poor output: "Rust is faster and safer than Go, so use it." This states an unmeasured comparison as fact and ignores the workload.

Do not recommend languages on fashion, claim a language is universally faster or safer, or present version-specific behavior as timeless.