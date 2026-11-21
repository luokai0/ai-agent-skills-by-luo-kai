---
name: language-internals-engineering
description: Use when analyzing, modifying, debugging, or designing language runtime, compiler, interpreter, garbage collector, VM, or parser internals, including bytecode, memory layout, JIT, and calling-convention work.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Language Internals Engineering

## Purpose and boundaries

This skill guides work on the internal machinery of programming languages: lexers and parsers, intermediate representations, bytecode and interpreter loops, code generation and JIT tiers, garbage collectors and allocators, object layout, calling conventions, foreign function boundaries, and runtime support libraries.

In scope: reading and changing runtime or compiler source, diagnosing crashes and miscompilations, performance work on hot runtime paths, adding opcodes or IR passes, GC tuning and correctness, and writing differential or fuzz tests for language implementations.

Out of scope: writing application code in a language, language design proposals without an implementation, and kernel or hardware bring-up except where the runtime depends on it directly.

## Inputs and assumptions

Before acting, establish:

1. The exact commit or release of the implementation, and whether the task targets a fork or upstream.
2. Target platforms, architectures, and word size. Layout and ABI conclusions do not transfer across them.
3. The reproducer: a minimal program, failing test, crash log, or benchmark. If none exists, creating one is the first deliverable.
4. The build configuration (optimization level, debug assertions, sanitizers, GC mode). Record it verbatim.
5. Toolchain versions. Any flag, API, or tool behavior named from memory must be verified against current official documentation for that version before use.

If any of these is unknown, state the assumption explicitly in the output.

## Operating workflow

1. **Reproduce.** Build the unmodified tree in the recorded configuration and run the reproducer. Record exit status, output, and timing. Do not proceed on a failure you cannot reproduce.
2. **Localize.** Bisect the failing input (delta-reduce the program), or bisect history when a regression is involved. Identify the first pass, opcode, or runtime function where state first diverges from the expected model.
3. **Model the invariant.** Write down the invariant that is violated, for example "the nursery pointer is never older than the card table entry," "stack maps match live slots at every safepoint," or "constant folding preserves evaluation order of side effects."
4. **Inspect evidence, not intuition.** Dump the relevant IR, bytecode, or disassembly at the failing and last-good points and diff them.
5. **Change minimally.** Make the smallest edit that restores the invariant. Avoid opportunistic refactors in the same change.
6. **Verify** (see below), then document the invariant in a code comment or design note at the point it is enforced.

## Decision gates

- **Gate A: Fix location.** Fix at the layer that owns the invariant. Patching a symptom in a caller (for example, nulling a pointer after a GC crash) is rejected unless the owning layer is out of your control, in which case document the workaround and its scope.
- **Gate B: Undefined behavior.** If the cause is undefined behavior in C or C++ runtime code, the fix must eliminate the UB, not depend on a compiler happening to tolerate it. Confirm with a sanitizer or a documented analysis tool run.
- **Gate C: Performance claims.** A performance change requires before-and-after measurements on the same machine, with variance across at least five runs, and a stated workload. Without this, the change is labeled unverified.
- **Gate D: Optimization soundness.** A new or modified optimization must preserve semantics on the existing test corpus and on a differential run against the unoptimized path. Any case where behavior differs is a blocker.
- **Gate E: ABI or layout change.** Changing object layout, calling conventions, serialized formats, or exported symbols is a compatibility decision. Stop and obtain explicit approval before proceeding.
- **Gate F: Destructive or external actions.** Force-pushing, deleting branches or artifacts, modifying shared CI, publishing packages, or filing upstream issues or pull requests requires explicit user approval for each action.

## Verification and evidence

Minimum evidence set for a change:

- The reproducer now passes, with the command and output recorded.
- The full existing test suite passes in the recorded configuration, plus the configuration with debug assertions enabled.
- Sanitizers (address, undefined behavior, thread) run on the affected components when the language and toolchain support them. Name the exact sanitizer flags only after confirming them in current documentation.
- For GC changes: a stress run that forces frequent collections, with heap verification enabled if the implementation provides it. Report collection count and any verifier failures.
- For compiler or JIT changes: differential execution between interpreted or unoptimized and optimized modes over the corpus, with zero mismatches as the pass condition.
- For parsers: round-trip or reject-tests on malformed input, and a fuzzing run of stated duration. Report the corpus size and crash count.
- Benchmarks: a table of baseline and changed results with machine description and variance. Never state a speedup percentage without its variance.

Do not claim compliance, security certification, or correctness beyond what the tests cover.

## Failure handling

- **Cannot reproduce:** Check configuration, toolchain version, and environment differences. Report what was tried. Do not guess a fix.
- **Reproduces only under optimization:** Suspect undefined behavior, missing safepoints, or incorrect stack maps. Compare IR before and after the suspect pass.
- **Verifier or sanitizer fails in unrelated code:** Record it as a pre-existing failure with its baseline status; do not silently widen scope.
- **Fix breaks other tests:** Revert to the last clean state, reexamine the invariant, and do not suppress tests to pass.
- **Documentation conflicts with observed behavior:** Trust the observed behavior with evidence, and flag the discrepancy for the user.

## Deliverable contract

Each deliverable must include:

1. Summary of the defect or goal, in two to four sentences.
2. Environment: commit, platform, configuration, toolchain versions.
3. The violated or established invariant, stated precisely.
4. The change as a diff, with the file and function for each hunk.
5. Verification results per the evidence set, with exact commands and outcomes.
6. Unverified items, assumptions, and version-sensitive details flagged for confirmation against official documentation.
7. Open risks and any decisions requiring the user's approval under the decision gates.

Do not present a fix as complete while any required evidence item is missing. Do not include unrequested refactors, speculative optimizations, or changes outside the owning layer.