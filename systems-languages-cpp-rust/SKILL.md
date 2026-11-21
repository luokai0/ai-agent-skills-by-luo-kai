---
name: systems-languages-cpp-rust
description: Use when writing, reviewing, migrating, or debugging C++ or Rust systems code, including memory safety, ownership and lifetime design, FFI boundaries, concurrency, undefined behavior, build and toolchain choices, and performance-sensitive components.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Systems Languages: C++ and Rust

## Purpose and boundaries

This skill guides engineering decisions and reviews for C++ and Rust code where memory layout, resource lifetimes, concurrency, and native interop matter. It covers:

- Designing ownership, lifetimes, and error propagation in new components.
- Reviewing C++ for undefined behavior, lifetime hazards, and modern idiom gaps.
- Reviewing Rust for `unsafe` soundness, borrow-driven API shape, and send/sync correctness.
- Designing and auditing FFI boundaries between C++, Rust, and C.
- Choosing between C++ and Rust for a component, and planning incremental migration.
- Diagnosing crashes, data races, leaks, and performance regressions.

It does not cover application-level product design, web frameworks, or language-theory research. It does not certify compliance with any safety standard.

## Inputs and assumptions

Before advising, establish:

1. Target standard: C++ standard level (for example C++17, C++20, C++23) and Rust edition and minimum supported Rust version (MSRV). Confirm exact feature availability against current official documentation, since support varies by compiler and version.
2. Platform, target triple, and whether the code runs in kernel, embedded, real-time, or hosted contexts.
3. Concurrency model and any real-time or latency budgets.
4. Existing codebase constraints: build system, sanitizers in use, allocator, exception and panic policy.
5. Whether the task involves untrusted input, network exposure, or privileged execution.

If any of these is unknown, state the assumption explicitly in the output rather than guessing silently.

## Operating workflow

1. **Restate the goal and invariants.** Write down what must always hold (for example, "buffer owned by X, freed exactly once," or "no `&mut` aliasing across await points").
2. **Map ownership.** For each resource, name the owner, the borrowers, and the lifetime bound. In C++, identify who calls `delete`, releases a lock, or closes a handle. In Rust, identify who holds `Box`, `Arc`, or borrowed slices.
3. **Identify trust boundaries.** Mark every point where data crosses from untrusted input, from C ABI, or from another thread.
4. **Choose the mechanism.** Prefer compiler-checked mechanisms over conventions (see Decision gates).
5. **Implement or review in small units.** One boundary or one invariant per change.
6. **Run verification** (see Verification and evidence) and attach results to the deliverable.

## Decision gates

Stop and seek explicit approval before proceeding if any of the following apply:

- The change introduces `unsafe` Rust, raw pointer arithmetic, `reinterpret_cast`, or manual memory management in a path that previously had none.
- The change alters an exported ABI, C header, symbol name, struct layout, or serialized format.
- The change modifies build flags that affect optimization, sanitizers, exception handling, or panic strategy.
- The change touches code that runs with elevated privileges, handles secrets, or parses untrusted network or file input.
- A migration would replace a working component in production, or delete existing code paths.
- Any action would publish artifacts, push to shared repositories, or change deployed services.

Otherwise, apply these criteria:

- **C++ ownership:** use value semantics, `std::unique_ptr` for single ownership, `std::shared_ptr` only with a demonstrated shared-ownership need, and non-owning `T*` or references for observation. Avoid raw `new`/`delete` outside low-level allocators.
- **C++ views:** `std::span` and `std::string_view` do not own data; never return them pointing to locals or temporaries.
- **Rust `unsafe`:** keep blocks minimal, wrap them in a safe API, and document every invariant the caller must uphold in a `# Safety` section.
- **Rust concurrency:** prefer message passing or `Arc<Mutex<T>>`-style sharing; verify `Send` and `Sync` bounds rather than adding `unsafe impl` to silence errors.
- **Errors:** C++ code uses exceptions or `std::expected`-style results consistently within a module; Rust uses `Result` and propagates with `?`. Never mix policies silently across an ABI boundary.
- **FFI:** expose a C-compatible surface with explicit lengths, explicit ownership transfer functions, and no Rust panics or C++ exceptions crossing the boundary.

## Verification and evidence

Each deliverable must include the checks that were actually run, with commands and outcomes. Use what the project already has; add only what is relevant:

- C++: compile with warnings enabled at the project's warning level and treat new warnings as failures; run AddressSanitizer and UndefinedBehaviorSanitizer on unit tests; run ThreadSanitizer for concurrent code; run clang-tidy checks already configured for the project.
- Rust: `cargo build` and `cargo test` on the MSRV and current stable; `cargo clippy` with warnings denied for changed crates; Miri on code containing `unsafe` where the project supports it; `cargo audit` or equivalent if dependencies changed.
- FFI: a test that calls each exported function from the other language, including null, zero-length, and maximum-length inputs.
- Performance claims: report the benchmark harness, input set, machine description, and before/after numbers with variance. Never state a speedup without measurement.

Measurable quality checks:

- Zero new sanitizer findings on the changed test set.
- Every `unsafe` block has a safety comment naming the invariant and the proof obligation.
- Every exported C function has a documented ownership rule for each pointer argument and return value.
- No new public API accepts a raw pointer without an accompanying length or documented non-null precondition.

Version-sensitive items (compiler flags, sanitizer support, Miri coverage, clippy lint names, standard library APIs) must be checked against current official documentation before being recommended. Mark unverified items as "to verify."

## Failure handling

- **Sanitizer or Miri finding:** reproduce with the minimal input, identify the violated invariant, fix the root cause, and add a regression test. Do not suppress findings without a documented justification and owner approval.
- **Compiler rejects a borrow or lifetime:** reconsider ownership before adding lifetimes or cloning. Restructure data ownership first; clone only when the cost is acceptable and stated.
- **Undefined behavior suspected in C++:** isolate the translation unit, compile with sanitizers, and check the standard's wording for the construct rather than relying on observed behavior.
- **Benchmark regression:** do not merge a tuned change that loses correctness margin; report the regression and the trade-off.
- **Unable to verify:** state exactly what was not checked and why. Do not claim success.

## Deliverable contract

Every response produces:

1. **Summary:** the goal, the chosen mechanism, and the principal trade-off, in no more than five sentences.
2. **Assumptions:** listed explicitly, including standard level, toolchain, and platform.
3. **Changes or findings:** code or review comments with file and symbol references, each tied to an invariant.
4. **Safety boundary notes:** every `unsafe` block, FFI function, or ownership transfer, with its invariant.
5. **Verification log:** commands run, results, and anything not verified, marked "to verify" where version-dependent.
6. **Approval requests:** any decision gate triggered, stated as a question awaiting explicit approval.

Do not:

- Assert that code is "safe," "secure," or "compliant" without the specific evidence supporting that claim.
- Invent API names, compiler flags, crate versions, or benchmark numbers.
- Suppress warnings or sanitizer findings to pass checks.
- Silence borrow-checker or `Send`/`Sync` errors with `unsafe` as a shortcut.
- Let panics or C++ exceptions unwind across a C ABI boundary.