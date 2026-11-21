---
name: nodejs-server-runtime
description: Use when building, debugging, hardening, or operating a Node.js HTTP/API server process, including event loop blocking, memory growth, graceful shutdown, process supervision, configuration, and runtime upgrades.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Nodejs Server Runtime

## Purpose and boundaries

This skill covers the runtime behavior of a Node.js server process: startup and configuration, request concurrency on the event loop, worker and cluster topology, memory and handle lifecycle, signal handling and graceful shutdown, and observability hooks at the process level. It applies to HTTP APIs, background workers that share the same runtime, and long-running services managed by a supervisor.

It does not cover framework-specific routing or ORM design, frontend bundling, or infrastructure provisioning beyond what the process needs to run correctly. Use a separate skill for database schema work or container orchestration policy.

## Inputs and assumptions

Collect before acting:

- Node.js version in use and the target version. Treat release-line support windows and specific flags as version-sensitive; verify against the official Node.js release schedule and documentation for the exact version.
- Entry point, process manager (systemd, PM2, container runtime, or none), and number of instances.
- Symptoms with evidence: latency percentiles, RSS and heap trends, restart counts, error logs, exit codes.
- Whether the environment is production. Assume production unless told otherwise.
- Load profile: request rate, payload sizes, CPU-bound versus I/O-bound work.

If the Node.js version or process manager is unknown, state that conclusions are provisional.

## Operating workflow

1. **Reproduce or locate the signal.** Map each symptom to a measurable metric. Latency tail with flat CPU suggests blocking I/O or queueing; rising heap after load suggests retained references; exit code 1 on deploy suggests startup failure.
2. **Measure the event loop first.** Use built-in event loop delay histograms (`perf_hooks` monitorEventLoopDelay) and CPU profiles taken from a staging or canary instance. Do not attach a profiler to production without approval.
3. **Classify the bottleneck.** Synchronous CPU work (JSON of large payloads, regex backtracking, crypto with sync APIs, large `fs.*Sync` calls) blocks all requests; async leaks (unbounded promise chains, unclosed sockets, timers) grow over time.
4. **Apply the smallest change.** Move CPU work to worker threads or a separate process; replace sync filesystem calls on request paths; bound concurrency with explicit limits; add timeouts to outbound calls.
5. **Harden lifecycle.** Handle `SIGTERM` by stopping new connections, draining in-flight requests within a fixed deadline, closing pools, then exiting. Set `server.keepAliveTimeout` and `headersTimeout` deliberately; confirm current defaults in the official HTTP documentation.
6. **Verify under load** (see Verification).

## Decision gates

- **Use worker threads** when work is CPU-bound and stateless. **Use child processes or a separate service** when isolation or crash containment matters.
- **Increase instance count** only after confirming the bottleneck is per-process CPU, not a shared database or lock.
- **Raise heap limits** only after proving retention is legitimate (cache sized to working set). Otherwise fix the leak.
- **Change Node.js version** only with a canary, a rollback plan, and a changelog review for breaking changes in the target line.
- **Enable new runtime flags** only after verifying their exact names and behavior in current official docs for your version.

## Verification and evidence

Each change requires before-and-after evidence:

- Event loop delay p99 reduced or unchanged; no new blocking spans in CPU profile.
- Heap after forced GC (run under a diagnostic flag only in staging) returns to baseline within two load cycles.
- Shutdown test: send `SIGTERM` under load; zero requests dropped that were accepted before the signal; process exits before the configured deadline; no unhandled rejections in logs.
- Load test at 1.2x expected peak with error rate under the agreed threshold.
- Startup test: process reports ready only after configuration validation and dependency connections succeed.

Record the Node.js version, flags, instance count, and load parameters with every result.

## Failure handling

- If a metric regresses after a change, revert first, then investigate.
- If a memory profile is inconclusive, collect two heap snapshots separated by a steady load window before drawing conclusions.
- If shutdown exceeds the deadline, force exit with a logged reason; do not leave the process hanging.
- If `uncaughtException` or `unhandledRejection` occurs, log with context and exit; do not continue serving on corrupted state.

## Deliverable contract

Produce:

1. Diagnosis: symptom, metric evidence, classified bottleneck.
2. Change set: exact file-level edits, with rationale for each.
3. Verification results: numbers before and after, test conditions, Node.js version.
4. Rollback steps.
5. Open risks and items requiring version confirmation against official documentation.

Do not:

- Restart, kill, or redeploy production processes, or alter live configuration, without explicit approval.
- Run heap snapshots, CPU profiles, or debug inspectors on production without explicit approval, since they pause or slow the process.
- Invent flag names, API signatures, or version numbers; mark uncertain items for verification.
- Claim performance gains or compliance properties without measured evidence.
- Suppress errors with empty catch blocks or disable TLS verification to clear failures.

Require explicit human approval before any action that is destructive, irreversible, externally visible (traffic shifting, customer-facing config, third-party calls with side effects), or touches sensitive data such as credentials, tokens, or personal data in logs.