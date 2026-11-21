---
name: computing-systems-software
description: Use when designing, reviewing, debugging, or documenting system software such as operating system components, runtimes, drivers, firmware interfaces, schedulers, memory managers, or emulators and virtualization layers, and when deciding how such software should be built, tested, and validated on real hardware.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Computing Systems Software

## Purpose and boundaries

This skill guides work on software that sits between hardware and application code: kernels and kernel modules, device drivers, bootloaders and firmware-facing interfaces, language runtimes and garbage collectors, hypervisors and emulators, schedulers, allocators, and inter-process communication layers.

In scope: architecture analysis, interface design, concurrency and memory-safety review, performance-critical path analysis, fault diagnosis, build and test strategy for low-level code, and documentation of system behavior.

Out of scope: application-level product features, cloud infrastructure operations, hardware circuit design, and security certification or regulatory sign-off. Where those are touched, state the gap and hand off.

## Inputs and assumptions

Collect before analysis:

1. Target platform: ISA, privilege levels, SoC or board, firmware version, and kernel or runtime version.
2. Source revision and build configuration (compiler, flags, kernel config, feature toggles).
3. Observed behavior: logs, traces, crash dumps, panic messages, reproduction steps, and frequency.
4. Constraints: latency budget, memory ceiling, real-time requirements, power envelope, certification or safety context.
5. Ownership boundaries: which components you may modify and which are vendor-supplied binaries.

Assumptions must be written down explicitly. Do not assume a hardware behavior, errata status, or ABI guarantee without a cited source. Treat any toolchain, kernel, or firmware version-specific detail as unverified until checked against current official documentation.

## Operating workflow

1. **Frame the problem.** Restate the goal as a testable statement: "Under workload W on platform P, metric M must stay below X." If no metric exists, define one before changing code.
2. **Map the boundary.** Identify every interface crossed: syscalls, MMIO regions, DMA buffers, interrupt contexts, shared memory, and locks. List the invariants each interface must preserve.
3. **Reproduce first.** Build a minimal reproducer. If it is intermittent, increase observation (tracing, sanitizers, lock statistics) before hypothesizing.
4. **Localize.** Bisect by revision, configuration, or code path. Prefer evidence from traces over reading code alone.
5. **Hypothesize and test one variable at a time.** Each hypothesis states the predicted observation if it is true and the observation that would falsify it.
6. **Change minimally.** Keep the patch scoped to the invariant that was violated. Avoid refactoring inside a fix.
7. **Verify** against the original reproducer, the regression suite, and the performance metric.
8. **Document** the invariant, the failure mode, and the verification evidence in the change record.

## Decision gates

Stop and request approval before proceeding if any of the following hold:

- The action erases, reflashes, or repartitions storage, or overwrites firmware or boot sectors.
- The action changes persistent hardware configuration (fuses, OTP, secure-boot keys, boot-order settings).
- The change affects a shared production fleet, a field-deployed device, or any external party.
- The fix requires disabling a security mechanism (MMU protections, signature checks, sandboxing, sanitizers in release builds).
- The work touches cryptographic code, key handling, or authentication paths.
- Evidence is insufficient to distinguish the root cause from two or more candidates.

Proceed without a gate only for local, reversible actions on a development target: rebuilding, running tests, adding tracing, and patching code in an isolated branch.

## Verification and evidence

A claim about system behavior requires one of: a reproducible test, a trace showing the sequence, a static analysis result with stated scope, or a cited specification section. Opinion is not evidence.

Measurable checks to apply:

- Reproducer passes in N consecutive runs (state N; use at least 100 for race-prone paths, and report the failure count if nonzero).
- Concurrency-sensitive changes run under a thread sanitizer or equivalent where available for the target, and under stress with varied scheduling.
- Memory changes run under an address or memory sanitizer, or a platform-appropriate leak and corruption checker, on the host and, where feasible, the target.
- Performance changes report before and after medians and tail latency (p99) over identical workloads, with run count and variance stated.
- Interface changes include a compatibility check against every known consumer of the ABI or API.
- Interrupt and atomic-context code is checked for sleeping calls and for lock ordering against documented rules.

Benchmark numbers are reported only from measurements you ran on the stated configuration. Never estimate them.

## Failure handling

- **Irreproducible failure:** increase logging at the boundary, record timing and resource state, and set a bounded trial count. Do not declare it fixed on absence of recurrence without the trial count.
- **Fix breaks another test:** treat the new failure as evidence about the invariant. Revert the patch and re-derive the invariant before retrying.
- **Sanitizer or verifier report with unclear cause:** reduce to the smallest input that triggers it; do not suppress the report without a written justification and owner sign-off.
- **Toolchain or firmware version mismatch:** record the exact versions, check the release notes of current official documentation, and state which result depends on the version.
- **Blocked by a gate:** write the proposed action, its reversibility, its blast radius, and the rollback path, then wait for approval.

## What not to do

- Do not disable assertions, lockdep-style checks, or sanitizers to make a build pass.
- Do not use `sleep`-based timing to hide races.
- Do not hard-code addresses, offsets, or register values without a source reference.
- Do not add global locks as a default fix without measuring contention.
- Do not claim a hardware errata workaround is complete without the specific erratum identifier and the verification against it.
- Do not present unverified performance, compliance, or security conclusions as settled.

## Deliverable contract

Every deliverable includes:

1. **Problem statement** with the measurable target and the platform identifier.
2. **Invariants** violated or preserved, listed per interface.
3. **Root cause** with the evidence chain (trace, test, or cited specification).
4. **Change summary** with files touched and the rationale tied to invariants.
5. **Verification table** listing each check, the configuration, run counts, and results, including failures.
6. **Open risks** and items marked for verification against current official documentation.
7. **Approvals obtained** for any gated action, or a statement that none was required.