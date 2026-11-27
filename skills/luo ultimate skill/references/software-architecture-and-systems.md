# Software Architecture and Systems

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## algorithms-core

**Use when:** Use when designing, selecting, implementing, reviewing, or debugging algorithms and data structures for correctness, complexity, and performance, including choosing between approaches, proving invariants, and writing tests for edge cases.

### Purpose and boundaries

This skill covers the design and validation of algorithms and data structures: problem modeling, choosing a technique (greedy, dynamic programming, graph search, divide and conquer, two pointers, sorting, hashing, heaps, union-find, tries, interval handling), deriving time and space complexity, establishing correctness arguments, and producing tested implementations.

In scope: algorithmic code in any general-purpose language, complexity analysis, benchmark design, correctness reasoning, and reviewing existing algorithmic code.

Out of scope: distributed consensus design, cryptographic primitives (use vetted libraries and specialist review), ML model training, and production capacity planning. If a request reaches those areas, state the boundary and limit the answer to the algorithmic core.

### Inputs and assumptions

Before proceeding, establish:

1. Problem statement with precise input domain, output contract, and error behavior.
2. Scale: expected n, value ranges, memory limits, latency budget, and whether input is streamed or static.
3. Query pattern: one-shot, repeated queries, online updates, or mixed.
4. Language and runtime constraints (recursion depth limits, integer width, standard library availability).
5. Whether exact results are required or approximation is acceptable, and the error tolerance if so.

If any of these is missing and materially changes the choice, state the assumption explicitly and name the input that would invalidate it. Do not assume unbounded input sizes.

### Operating workflow

1. Restate the problem as a formal mapping from inputs to outputs. List edge cases: empty input, single element, duplicates, negative values, overflow, disconnected graphs, cycles.
2. Derive a brute-force baseline and its complexity. This anchors correctness checks and reveals the bottleneck.
3. Identify structure: monotonicity, optimal substructure, overlapping subproblems, sortedness, graph properties (DAG, weighted, nonnegative edges), or a constrained query pattern.
4. Select the technique using the decision gates below. Write down the recurrence, invariant, or greedy-choice argument before coding.
5. Implement with named invariants in comments only where they are non-obvious.
6. Verify (see Verification and evidence), then analyze complexity including constant-factor hotspots such as allocation and cache-unfriendly access.
7. Report the result using the deliverable contract.

### Decision gates

- Greedy: proceed only if you can state an exchange argument or matroid-like property showing local choices extend to a global optimum. If a counterexample exists for a small case, reject greedy.
- Dynamic programming: use when subproblems repeat and the state is small enough. Define the state, transition, base case, and evaluation order. If state space exceeds memory, look for a dimension reduction or switch technique.
- Graph search: BFS for unweighted shortest paths; Dijkstra only with nonnegative weights; Bellman-Ford when negative edges exist and cycles must be detected; topological sort only on DAGs, with cycle detection as a failure path.
- Sorting plus sweep: use when intervals or pairwise relations can be ordered so a single pass suffices. State the sort key and tie-breaking rule.
- Hashing: acceptable for average-case expected bounds. If adversarial input is possible, say so and note the worst-case alternative. Do not claim worst-case O(1) for hash tables.
- Approximation or randomization: require explicit approval from the user before substituting an approximate or probabilistic answer for an exact one.

### Verification and evidence

- Write a brute-force reference and compare against the optimized version on randomized small inputs (for example, several hundred cases with n up to about 10), using a fixed seed so failures reproduce.
- Test the edge cases enumerated in step 1, plus maximal-size inputs for runtime and memory.
- Check invariants at loop boundaries in a debug build.
- For performance claims, measure on the stated scale with warm-up and repeated runs; report median and spread. Never report a speedup without the baseline and hardware description.
- Complexity claims must be derived from the code's operations, not inferred from its shape.
- Mark any language, library, or runtime behavior that is version-sensitive as requiring verification against current official documentation. Do not state library function names, flags, or package versions from memory without that check.

### Failure handling

- Counterexample found: stop, record the input, identify which assumption or invariant failed, and revise the technique rather than patching the output.
- Timeout on target scale: profile first; distinguish algorithmic cost from implementation overhead before changing the approach.
- Stack overflow from recursion: convert to an explicit stack or bottom-up order, and state the depth bound.
- Ambiguous specification (for example, tie-breaking or whether output must be unique): ask before implementing.

### Deliverable contract

Return:

1. The chosen technique and one-paragraph justification referencing the decision gate used.
2. Complexity: time and space, stated as functions of named parameters, with worst-case and average-case distinguished where relevant.
3. Implementation with explicit input validation at the boundary.
4. Test evidence: edge cases covered, randomized comparison result, and any measured runtimes with setup described.
5. Known limitations and the input conditions that would break the solution.

### What not to do

- Do not present a heuristic as exact, or an expected-time bound as a worst-case guarantee.
- Do not skip the brute-force baseline for non-trivial problems.
- Do not invent benchmark numbers, library APIs, or version compatibility.
- Do not change the output contract (ordering, uniqueness, tie-breaking) without explicit confirmation.
- Do not run code that modifies files, consumes external services, or sends data outside the environment without explicit approval from the user.
- Do not delete or overwrite existing project code, test fixtures, or data files without explicit approval.
- Do not add dependencies to a project without approval.


## build-dependency-devx

**Use when:** Use when diagnosing, redesigning, or hardening developer experience for build systems and dependency management, including slow or flaky builds, lockfile drift, version conflicts, monorepo dependency graphs, cache misconfiguration, and onboarding friction.

### Purpose and boundaries

This skill covers the developer-facing health of a project's build and dependency layer: how dependencies are declared, resolved, locked, cached, and consumed, and how quickly and reliably a developer can go from clone to passing build. It applies to single packages, multi-package workspaces, and monorepos across common language ecosystems.

In scope: dependency declaration hygiene, lockfile policy, version range strategy, build graph and task caching, incremental build correctness, reproducibility of local builds, toolchain pinning, developer bootstrap scripts, and build-time diagnostics.

Out of scope: application feature code, runtime performance tuning, CI vendor billing, and security policy decisions (flag these and route them to the owning team).

### Inputs and assumptions

Collect before changing anything:
- Manifests and lockfiles (exact filenames present).
- Build tool and version, runtime versions, and any version managers in use.
- Clean-clone build time, incremental rebuild time, and a representative failure log.
- Cache configuration (local and remote), and whether remote cache is shared across branches or trust levels.
- Who owns each package or directory.

Assume nothing about registry mirrors, private registries, or network access. Verify them. If the environment cannot be reproduced, state that the findings are unverified.

### Operating workflow

1. **Baseline.** Record clean build time, incremental build time, and count of distinct resolved versions per major dependency. Capture these in a table; they are the before-metrics.
2. **Classify failures.** Group issues into: resolution (conflicting ranges), drift (manifest and lockfile disagree), hidden inputs (build reads undeclared files, env vars, or clock), cache poisoning or misses, toolchain mismatch, and bootstrap gaps.
3. **Trace the graph.** For each failing task, identify its declared inputs and outputs. Compare against what it actually reads. Undeclared inputs are the most common cause of incorrect cache hits and flaky builds.
4. **Propose minimal changes**, ordered by reversibility: pin toolchain versions, fix declarations, adjust ignore patterns, then restructure task graphs. Do not bundle unrelated changes.
5. **Apply in a branch**, one concern per commit, each with its before/after metric.
6. **Verify** using the checks below, then document the bootstrap path.

### Decision gates

Stop and request explicit approval before:
- Deleting or regenerating a lockfile, or running a major dependency upgrade.
- Changing remote cache write permissions or sharing cache entries across trust boundaries.
- Altering publish, release, or registry configuration.
- Modifying shared CI pipeline definitions used by other teams.
- Adding or removing dependencies that carry license, security, or export-control implications.
- Any action that affects other developers' machines (global installs, shared volumes).

Proceed without approval only for: local, reversible edits on a branch; adding declared inputs to a task; pinning a toolchain to a version already in use by the majority of developers; and documentation.

Choose a version range strategy by criteria: libraries use permissive ranges with a lockfile for applications and tests; applications pin exactly; monorepo internal packages use workspace protocols rather than published versions.

### Verification and evidence

Each change must show:
- Clean-clone build succeeds on a fresh checkout (no cached artifacts, no global state).
- Incremental build after touching one source file rebuilds only dependent tasks. Verify with the tool's task-explanation output, not assumption.
- Running the build twice with no changes produces zero task execution.
- `lockfile check` in CI-equivalent mode passes without modifying files. Use the tool's frozen or immutable install mode; confirm the exact flag against current official docs, as names vary by version.
- Dependency duplicate count does not increase. Report the count before and after.
- Bootstrap steps executed in a clean container or fresh user account, timed.

Quality targets (set as project goals, not guarantees): clean build under the agreed baseline, zero flaky reruns across five consecutive runs, and every task's inputs enumerated.

Mark any command syntax, flag, or version-specific behavior as "verify against current official documentation" unless confirmed in this repository.

### Failure handling

- If a clean build fails after a change, revert that commit rather than patching forward silently.
- If a cache hit produces wrong output, disable that cache entry scope, record the reproduction, and widen declared inputs before re-enabling.
- If lockfile regeneration changes many unrelated versions, stop and report the diff summary; do not commit it.
- If the failure cannot be reproduced, record environment details (OS, runtime versions, tool versions, network state) and mark the finding unverified.
- Never suppress warnings or skip tasks to make a build green.

### Deliverable contract

Produce:
1. Findings table: issue, category, evidence (log excerpt or command output), severity, owner.
2. Change list: one entry per commit with rationale and before/after metric.
3. Verification record: the checks above with pass/fail and environment.
4. Bootstrap document: ordered steps a new developer runs, with expected duration and known failure modes.
5. Open items: approval requests, unverified findings, and items routed to other owners.

Do not claim improvements without measured before/after data. Do not present unverified version or flag details as fact.


## clean-code-boundaries

**Use when:** Use when designing or reviewing module, service, or layer boundaries, deciding where a dependency should be inverted, wrapping third-party libraries, or untangling code where domain logic leaks into infrastructure, UI, or persistence.

### Purpose and boundaries

This skill guides decisions about where one part of a codebase ends and another begins: which side owns a concept, which direction dependencies point, and what shape crosses the seam. It covers module and package boundaries, layer boundaries (domain, application, adapters, infrastructure), service interfaces, and wrappers around external systems such as databases, message brokers, payment or identity providers, and SDKs.

It does not cover: choosing a deployment topology, picking a framework, performance tuning of a single function, or rewriting a system wholesale. Redirect those to the appropriate skill or to a human architect.

### Inputs and assumptions

Before acting, gather:

- The module graph or import/dependency listing for the affected area.
- The concepts crossing the seam (entities, DTOs, events, errors, configuration).
- Known change pressures: which parts change often, which are stable, which are regulated.
- Whether the external system is owned by the team or a third party.
- Current test coverage at the seam.

Assume the codebase is in version control and that changes are reviewable. If the dependency graph cannot be obtained, state that the analysis is based on partial evidence and list what is unknown.

### Operating workflow

1. **Map the crossing.** List every import or call that crosses the candidate boundary, in both directions. Count them and group by concept.
2. **Classify each crossing.** Mark it as domain rule, orchestration, data shape, configuration, or side effect.
3. **Find inverted arrows.** Flag any domain or application code that imports infrastructure, framework types, ORM models, HTTP request objects, or vendor SDK types.
4. **Choose the owner.** The side that defines the meaning of a concept owns its type. Consumers depend on an interface or a port defined by the owner.
5. **Design the port.** Express the port in the owner's vocabulary (for example `PaymentCapture` with `capture(orderId, amount)`), not the vendor's (for example a raw SDK charge object). Keep it narrow: only operations the caller actually uses.
6. **Place translation at the edge.** Adapters convert between vendor types and owner types. Translation of errors belongs here too: vendor error codes become owner-defined failure categories.
7. **Migrate incrementally.** Introduce the port, route one call path through it, verify, then move the next. Do not change the boundary and its callers in one unreviewed step.
8. **Record the decision** in the module's documentation or an architecture decision record: the owner, the direction, and the reason.

### Decision gates

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

### Verification and evidence

Each boundary change must produce:

- **Dependency evidence:** before and after import listing showing domain packages no longer import adapter or vendor packages. Target: zero such imports in the domain layer, verified by a repeatable command or lint rule available in the project's toolchain.
- **Behavioral evidence:** existing tests pass unchanged where behavior should be preserved. Where behavior is intentionally changed, the change is listed with its test.
- **Contract tests:** the port has a test suite that runs against both the real adapter (in a controlled environment) and an in-memory fake, asserting identical observable results for the operations the domain uses.
- **Coverage at the seam:** adapter translation logic has tests for each mapped error category and each mapped field.

Do not claim a reduction in coupling without the before-and-after dependency listing. Do not state that a change improves maintainability or performance without measurement.

### Failure handling

- If the dependency listing reveals a cycle that cannot be broken without a redesign, stop, document the cycle, and propose options with trade-offs rather than introducing a workaround interface that hides it.
- If a port leaks vendor concepts discovered late, revise the port in its own change; do not patch callers with vendor-specific branches.
- If tests fail after migration, revert the single step, identify whether the fault is in translation, port semantics, or a hidden side effect, and fix that before continuing.
- If the vendor's documented behavior is unclear or version-dependent, mark the adapter behavior as "to be verified against current official documentation" and do not encode assumptions as fact.

### Deliverable contract

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


## computing-systems-software

**Use when:** Use when designing, reviewing, debugging, or documenting system software such as operating system components, runtimes, drivers, firmware interfaces, schedulers, memory managers, or emulators and virtualization layers, and when deciding how such software should be built, tested, and validated on real hardware.

### Purpose and boundaries

This skill guides work on software that sits between hardware and application code: kernels and kernel modules, device drivers, bootloaders and firmware-facing interfaces, language runtimes and garbage collectors, hypervisors and emulators, schedulers, allocators, and inter-process communication layers.

In scope: architecture analysis, interface design, concurrency and memory-safety review, performance-critical path analysis, fault diagnosis, build and test strategy for low-level code, and documentation of system behavior.

Out of scope: application-level product features, cloud infrastructure operations, hardware circuit design, and security certification or regulatory sign-off. Where those are touched, state the gap and hand off.

### Inputs and assumptions

Collect before analysis:

1. Target platform: ISA, privilege levels, SoC or board, firmware version, and kernel or runtime version.
2. Source revision and build configuration (compiler, flags, kernel config, feature toggles).
3. Observed behavior: logs, traces, crash dumps, panic messages, reproduction steps, and frequency.
4. Constraints: latency budget, memory ceiling, real-time requirements, power envelope, certification or safety context.
5. Ownership boundaries: which components you may modify and which are vendor-supplied binaries.

Assumptions must be written down explicitly. Do not assume a hardware behavior, errata status, or ABI guarantee without a cited source. Treat any toolchain, kernel, or firmware version-specific detail as unverified until checked against current official documentation.

### Operating workflow

1. **Frame the problem.** Restate the goal as a testable statement: "Under workload W on platform P, metric M must stay below X." If no metric exists, define one before changing code.
2. **Map the boundary.** Identify every interface crossed: syscalls, MMIO regions, DMA buffers, interrupt contexts, shared memory, and locks. List the invariants each interface must preserve.
3. **Reproduce first.** Build a minimal reproducer. If it is intermittent, increase observation (tracing, sanitizers, lock statistics) before hypothesizing.
4. **Localize.** Bisect by revision, configuration, or code path. Prefer evidence from traces over reading code alone.
5. **Hypothesize and test one variable at a time.** Each hypothesis states the predicted observation if it is true and the observation that would falsify it.
6. **Change minimally.** Keep the patch scoped to the invariant that was violated. Avoid refactoring inside a fix.
7. **Verify** against the original reproducer, the regression suite, and the performance metric.
8. **Document** the invariant, the failure mode, and the verification evidence in the change record.

### Decision gates

Stop and request approval before proceeding if any of the following hold:

- The action erases, reflashes, or repartitions storage, or overwrites firmware or boot sectors.
- The action changes persistent hardware configuration (fuses, OTP, secure-boot keys, boot-order settings).
- The change affects a shared production fleet, a field-deployed device, or any external party.
- The fix requires disabling a security mechanism (MMU protections, signature checks, sandboxing, sanitizers in release builds).
- The work touches cryptographic code, key handling, or authentication paths.
- Evidence is insufficient to distinguish the root cause from two or more candidates.

Proceed without a gate only for local, reversible actions on a development target: rebuilding, running tests, adding tracing, and patching code in an isolated branch.

### Verification and evidence

A claim about system behavior requires one of: a reproducible test, a trace showing the sequence, a static analysis result with stated scope, or a cited specification section. Opinion is not evidence.

Measurable checks to apply:

- Reproducer passes in N consecutive runs (state N; use at least 100 for race-prone paths, and report the failure count if nonzero).
- Concurrency-sensitive changes run under a thread sanitizer or equivalent where available for the target, and under stress with varied scheduling.
- Memory changes run under an address or memory sanitizer, or a platform-appropriate leak and corruption checker, on the host and, where feasible, the target.
- Performance changes report before and after medians and tail latency (p99) over identical workloads, with run count and variance stated.
- Interface changes include a compatibility check against every known consumer of the ABI or API.
- Interrupt and atomic-context code is checked for sleeping calls and for lock ordering against documented rules.

Benchmark numbers are reported only from measurements you ran on the stated configuration. Never estimate them.

### Failure handling

- **Irreproducible failure:** increase logging at the boundary, record timing and resource state, and set a bounded trial count. Do not declare it fixed on absence of recurrence without the trial count.
- **Fix breaks another test:** treat the new failure as evidence about the invariant. Revert the patch and re-derive the invariant before retrying.
- **Sanitizer or verifier report with unclear cause:** reduce to the smallest input that triggers it; do not suppress the report without a written justification and owner sign-off.
- **Toolchain or firmware version mismatch:** record the exact versions, check the release notes of current official documentation, and state which result depends on the version.
- **Blocked by a gate:** write the proposed action, its reversibility, its blast radius, and the rollback path, then wait for approval.

### What not to do

- Do not disable assertions, lockdep-style checks, or sanitizers to make a build pass.
- Do not use `sleep`-based timing to hide races.
- Do not hard-code addresses, offsets, or register values without a source reference.
- Do not add global locks as a default fix without measuring contention.
- Do not claim a hardware errata workaround is complete without the specific erratum identifier and the verification against it.
- Do not present unverified performance, compliance, or security conclusions as settled.

### Deliverable contract

Every deliverable includes:

1. **Problem statement** with the measurable target and the platform identifier.
2. **Invariants** violated or preserved, listed per interface.
3. **Root cause** with the evidence chain (trace, test, or cited specification).
4. **Change summary** with files touched and the rationale tied to invariants.
5. **Verification table** listing each check, the configuration, run counts, and results, including failures.
6. **Open risks** and items marked for verification against current official documentation.
7. **Approvals obtained** for any gated action, or a statement that none was required.


## concurrency-performance-engineering

**Use when:** Use when diagnosing, designing, or tuning concurrent or parallel code for throughput, latency, contention, or scalability, including thread pools, async runtimes, locks, lock-free structures, actor systems, and shared-state services.

### Purpose and boundaries

This skill covers measurable performance work on concurrent code: identifying bottlenecks caused by contention, scheduling, synchronization, blocking I/O inside async paths, false sharing, queue saturation, and unbounded parallelism. It produces evidence-backed changes and a verification record.

In scope: profiling concurrent workloads, reasoning about lock hold times and critical sections, sizing pools and queues, batching and sharding shared state, reducing synchronization granularity, and validating correctness is preserved after tuning.

Out of scope: general algorithm selection with no concurrency component, infrastructure capacity planning, cost optimization, and formal proofs of correctness (recommend a specialist review when correctness proofs are required). Do not treat this skill as a source of correctness guarantees for lock-free code.

### Inputs and assumptions

Required before acting:
- The code path under study, the runtime and language version, and the target platform (core count, memory model, container CPU limits).
- A representative workload description: request mix, concurrency level, data sizes, and arrival pattern.
- Current metrics: throughput, p50/p95/p99 latency, CPU utilization, run-queue length, lock wait time, GC pauses if applicable.
- Service-level targets, if any.

Assumptions to state explicitly in the deliverable when not provided: single-tenant benchmark host, steady-state load, and that production-like data is available. Do not assume a benchmark result applies to production without a comparison run.

### Operating workflow

1. **Define the metric and the target.** Write one primary metric (for example, p99 latency at fixed offered load) and a guardrail metric (for example, error rate or memory ceiling). Reject vague goals like "make it faster."
2. **Establish a baseline.** Run the workload at three or more concurrency levels. Record variance across at least five runs. Discard runs with obvious environmental noise and document why.
3. **Classify the bottleneck.** Use profiler and runtime evidence to place the constraint into one category:
   - CPU-bound with idle cores (serialization point, lock convoy, single-threaded stage).
   - CPU-bound with saturated cores (algorithmic cost, spinning, excessive context switching).
   - Blocked threads (lock waits, synchronous I/O on async workers, pool exhaustion).
   - Memory or cache-bound (false sharing, cache-line bouncing, allocation pressure).
   - Queueing-bound (unbounded queues, backpressure absent, tail amplification).
4. **Form one hypothesis per bottleneck** and state the predicted effect size.
5. **Apply the smallest change** that tests the hypothesis: shrink a critical section, move I/O out of a lock, replace a global lock with striped locks, bound a queue, or set pool size from measured service time.
6. **Re-measure under identical conditions** and compare against the baseline with the same load profile.
7. **Repeat** only from the new profile, never from intuition.

Domain-specific examples:
- An async service calling a blocking database driver on runtime worker threads: move the call to a dedicated blocking pool, then measure event-loop lag.
- A cache guarded by one mutex showing 40% lock wait: shard into 16 segments keyed by hash, verify hit ratio and eviction behavior are unchanged.
- Counters incremented by many threads on adjacent memory: pad per-thread slots to cache-line size and confirm with hardware counters where available.

### Decision gates

- **Gate A (before changing code):** Is the bottleneck reproduced in a controlled run? If not, stop and improve the harness.
- **Gate B (before lock-free or custom synchronization):** Has a simpler change (smaller critical section, sharding, immutable snapshots, message passing) been measured and rejected? Custom lock-free structures require explicit approval and a specialist review.
- **Gate C (before enlarging a pool or queue):** Does the change increase tail latency or memory under overload? If yes, require a bounded design with explicit rejection behavior.
- **Gate D (before merging):** Do tests pass under the race detector or equivalent sanitizer where the toolchain provides one, and does stress testing show no new deadlocks or livelocks?
- **Gate E (approval required):** Any change that alters production configuration, rolls out to live traffic, modifies shared state schema, or changes consistency guarantees requires explicit human approval before execution.

### Verification and evidence

Every claim of improvement needs:
- Baseline and candidate numbers for the primary and guardrail metrics, with run counts and variance.
- The identical workload definition and environment description.
- Profiler evidence showing the bottleneck moved or shrank, not just that the number changed.
- Correctness evidence: existing test suite, added concurrency tests for the changed region, and sanitizer or stress results.

Quality checks:
- Primary metric improves beyond run-to-run variance.
- Guardrail metrics do not regress beyond the agreed threshold.
- No new lock ordering violations; document lock hierarchy for any newly touched locks.
- Queue depth remains bounded under 2x expected peak load.

Version-sensitive details (runtime flags, profiler options, scheduler parameters, library APIs, sanitizer flags) must be checked against current official documentation for the exact version in use. Do not rely on remembered flag names.

### Failure handling

- **Improvement within noise:** Report as no measurable change. Do not ship it as an optimization.
- **Regression in a guardrail:** Revert the candidate, record the result, and return to classification.
- **Deadlock, data race, or lost update observed:** Stop immediately, preserve logs and the reproducer, and escalate. Do not patch around it by adding timeouts alone.
- **Benchmark cannot reproduce production shape:** Report the gap and mark conclusions as provisional.
- **Conflicting measurements:** Re-run with pinned CPU and fixed seed before drawing conclusions.

### Deliverable contract

Produce a report containing:
1. Metric definitions, targets, and guardrails.
2. Environment, runtime version, and workload description.
3. Baseline table (mean, p95/p99, variance, run count).
4. Bottleneck classification with profiler evidence.
5. Changes made, each tied to a single hypothesis, with a rationale.
6. Candidate results versus baseline under identical conditions.
7. Correctness and sanitizer results, and any residual risk.
8. A list of items requiring approval (Gate E) and version-sensitive details pending verification.

Do not claim production impact, compliance outcomes, or absolute speedups without the measurements that support them.


## development-ecology-evolution

**Use when:** Use when analyzing, designing, or reviewing studies that connect developmental mechanisms (chemical signaling, gene regulation, morphogenesis) with ecological context (environment, interactions, resources) and evolutionary change (plasticity, heritability, selection), including eco-evo-devo literature synthesis, experimental design, and chemical-ecology data interpretation.

### Purpose and boundaries

This skill supports professional work at the intersection of developmental biology, ecology, evolutionary biology, and the chemistry that mediates them: morphogen and hormone gradients, metabolite-driven signaling, environmentally induced phenotypes, semiochemicals, and reaction-network reasoning about developmental outcomes.

In scope:
- Reviewing and synthesizing evidence on developmental plasticity, genotype-by-environment effects, and evolutionary developmental change.
- Designing or critiquing factorial experiments that separate genetic, environmental, and developmental variance.
- Interpreting chemical-ecology and metabolomic datasets in a developmental or evolutionary frame.
- Writing analysis plans, reports, and protocol reviews.

Out of scope: clinical or human-subject interventions, wet-lab protocols for hazardous synthesis, field releases of organisms, and regulatory or biosafety determinations. Route these to qualified personnel and institutional committees.

### Inputs and assumptions

Before analysis, establish:
1. The question type: mechanistic (how), ecological (under what conditions), or evolutionary (what changed across lineages or generations).
2. Study system: organism, life stage, tissue, and taxonomic reference.
3. Data provenance: raw versus processed, instrument or method, units, and sample size per treatment.
4. Environmental variables: which were manipulated, which were measured, and which are confounded.
5. Explicit assumptions, such as additivity, linearity of reaction rates, or stationarity of selection.

State any assumption you cannot verify as an assumption. Do not fill gaps with typical values from memory.

### Operating workflow

1. Restate the question in one sentence and classify it by level (molecular, organismal, population, lineage).
2. Map the causal chain: signal or chemical input, receptor or pathway, developmental process, phenotype, ecological consequence, fitness-relevant outcome. Mark each link as observed, inferred, or assumed.
3. Check design adequacy: are treatment and control matched in timing and stage? Is there a reciprocal or cross-environment component? Are maternal or parental effects separated from direct effects?
4. For data, run unit and scale checks, identify missing values and batch effects, and record normalization steps.
5. Choose an analysis matched to the question. Use mixed models for nested or repeated measures; reaction-norm analysis for plasticity; variance partitioning for heritability versus environmental contribution; multivariate methods for chemical profiles, with compositional care.
6. Interpret effect sizes with confidence intervals, not only p-values.
7. Separate what the data show from what the mechanism would predict and from what the evolutionary history would require.

### Decision gates

Proceed to conclusions only when:
- Treatment assignment is documented and randomized or justified.
- Sample size supports the claimed effect size, or the report states the power limitation.
- Chemical identities are confirmed by standard or reference data, not spectral match alone.
- Confounds (stage, batch, density, maternal environment) are either controlled or explicitly bounded.

Stop and request approval before:
- Any wet-lab, animal, or field action, including sampling protocols beyond the approved design.
- Deleting, overwriting, or re-processing shared raw datasets.
- Publishing or sharing sequence, specimen location, or unpublished data outside the project team.
- Making claims about human health, pesticides, or environmental release.

### Verification and evidence

Quality checks, each with a measurable criterion:
- Every quantitative claim traces to a named table, figure, or dataset row.
- Reaction-norm or interaction claims report the interaction term and its interval, not just main effects.
- Chemical assignments list the confidence level and reference used.
- Replication: at least the biological replicates stated in the design; pseudoreplication flagged if present.
- Sensitivity check: conclusions hold after excluding the single most influential sample or batch.

Version-sensitive items (statistical package functions, instrument software, database accession formats, reference genome builds, metabolomic library versions): verify against current official documentation before stating a specific setting. Do not cite function names or flags from memory as authoritative.

### Failure handling

- Missing metadata: list the missing fields, state which conclusions are blocked, and request them.
- Confounded design: report the confound, downgrade the claim to association, and propose the minimal additional treatment that would resolve it.
- Contradictory evidence across studies: compare system, life stage, and environment before attributing conflict to biology.
- Unidentified compounds: report as features with mass or retention information only; do not assign structures.

### Deliverable contract

A completed deliverable contains:
1. One-paragraph summary with the question, the answer's strength, and the main limitation.
2. Causal chain table: link, evidence, classification (observed, inferred, assumed).
3. Analysis description sufficient for reproduction, including model structure and software versions to verify.
4. Verification checklist results with pass, fail, or not-applicable per item.
5. Open items requiring approval or additional data.

Do not: invent citations, benchmark values, or compliance statements; present inferred mechanisms as measured; or extend conclusions beyond the studied system and life stage.


## functional-programming-paradigms

**Use when:** Use when designing, reviewing, refactoring, or teaching code that relies on pure functions, immutability, function composition, algebraic data types, or effect isolation, including choosing between functional and imperative styles in a mixed-paradigm codebase.

### Purpose and boundaries

This skill guides professional work applying functional programming (FP) principles: referential transparency, explicit data flow, immutable state, algebraic data modeling, and controlled side effects. It covers code design, review, refactoring toward FP patterns, and explaining trade-offs to teams.

In scope: pure function design, data modeling with sum and product types, pipelines and composition, folds and maps over collections, pushing I/O to the edges, error handling as values, and evaluating whether FP idioms fit a given language and team.

Out of scope: language-specific tutorials, performance tuning of runtimes, formal proof development, and rewriting working systems without a stated reason.

### Inputs and assumptions

Before acting, establish:

1. Language and version. Idioms differ across languages and standard library generations. Mark any version-dependent feature for verification against current official documentation.
2. Codebase constraints: existing paradigm mix, team familiarity, linting rules, and runtime characteristics (for example, deep recursion limits or lack of tail-call elimination).
3. The goal: correctness, testability, concurrency safety, readability, or a specific bug class.
4. The code or design under review, in full enough context to trace data flow.

If any input is missing, ask. Do not assume the language supports a construct (persistent collections, pattern matching, tail-call optimization) without checking.

### Operating workflow

1. Map effects. List every function that reads or writes external state: clocks, randomness, files, network, databases, globals, mutable arguments, logging.
2. Classify functions as pure (output depends only on inputs, no observable side effects) or effectful. Record the classification.
3. Model the domain with data. Replace boolean flags and nullable fields with sum types or tagged variants where the language supports them. Replace stringly-typed states with enumerations.
4. Push effects outward. Keep a pure core that computes decisions and returns descriptions of effects; a thin shell executes them. Do not refactor the shell and core in the same change unless tests cover both.
5. Replace mutation with transformation where the cost is acceptable. Prefer returning new values from folds, maps, and reducers. Keep local mutation when it is contained, measured, and clearer.
6. Compose small functions into pipelines. Name intermediate steps when a pipeline exceeds roughly five stages or mixes concerns.
7. Make failure explicit. Represent expected failures as result or option values rather than thrown exceptions inside the pure core.
8. Write tests against the pure core first, with table-driven inputs covering empty, boundary, and invalid cases.

### Decision gates

Proceed with a full FP refactor only when all hold:
- Existing tests cover the target behavior, or new characterization tests are written first.
- The language provides the needed constructs without awkward workarounds.
- The change does not alter a public interface consumed outside the repository, unless approved.

Stop and request approval before:
- Changing serialization formats, database schemas, or wire protocols that other systems read.
- Altering concurrency semantics, such as replacing locks with immutable state sharing, in production paths.
- Deleting or rewriting code in a way that cannot be reverted in one commit.
- Introducing a new library or dependency for persistent data structures or effect systems.

Prefer local FP idioms over architectural conversion when the team lacks shared experience. Recommend a paradigm change only with a written rationale.

### Verification and evidence

Every claimed improvement must be backed by one of:
- Test results showing the pure core passes existing and new cases.
- A demonstrated reduction in the count of functions with hidden inputs or outputs, listed before and after.
- A concrete bug or race condition that the new structure makes impossible, with the reasoning shown.

Measurable checks:
- Count of effectful calls inside functions classified as pure: target zero.
- Every new pure function has at least one test per branch.
- No new shared mutable state introduced.
- Diff review confirms behavior is unchanged for at least one representative production input set, where available.

Do not claim performance gains or regressions without a benchmark run in the target environment. Do not claim compliance or security guarantees from FP structure alone.

### Failure handling

- If a refactor changes test outcomes, revert the smallest unit and isolate the cause before continuing.
- If the language lacks tail-call elimination and recursion depth is a risk, convert to iterative folds or explicit loops and state the change.
- If performance degrades beyond the agreed threshold, restore the prior implementation for the hot path and document the trade-off.
- If an immutable-update pattern causes excessive copying in a large collection, use a contained mutable accumulator inside a pure function and verify that its external behavior is unchanged.
- If a team member rejects the style, present the concrete readability and testability differences with examples rather than arguing principles.

### Deliverable contract

Each delivery includes:
1. A summary of the effect map: which functions were pure, which were effectful, and what changed.
2. The revised code, or a diff, with the pure core and effect shell clearly separated.
3. Test additions and their results, with the exact commands run.
4. A list of open questions, version-sensitive constructs flagged for verification against current official documentation, and any approval requests raised under the decision gates.
5. Known trade-offs, including any performance or readability cost.

What not to do:
- Do not wrap imperative code in FP-named functions without changing its data flow.
- Do not hide I/O inside functions named as pure.
- Do not use monads, effect systems, or type-level machinery to impress; use them only when they remove a concrete defect class.
- Do not invent library functions, flags, or version numbers; verify each against official sources.
- Do not rewrite stable, well-tested imperative code solely for stylistic conformity.


## large-scale-system-design

**Use when:** Use when designing, reviewing, or re-architecting a system expected to serve high traffic, large data volumes, multiple teams, or multi-region availability, and a decision on partitioning, consistency, scaling, or failure domains must be made or justified.

### Purpose and boundaries

This skill produces architecture decisions for distributed systems whose scale, availability, or organizational complexity makes single-node intuitions unreliable. It covers capacity modeling, service decomposition, data partitioning, replication and consistency choices, failure-domain isolation, and migration sequencing.

It does not cover: line-level code review, UI design, vendor procurement, or compliance certification. Compliance-sensitive designs are flagged for specialist review, not declared compliant.

### Inputs and assumptions

Collect before designing. If an input is missing, record it as an assumption with an owner and a date to resolve.

- Functional scope: the top five user-facing operations and their business invariants (for example, "a seat is sold at most once").
- Load: peak read and write rates, fan-out per request, payload sizes, growth rate over 12 months, and burst pattern.
- Data: total size, growth, retention, access pattern (point lookup, range scan, analytics), and cardinality of the main partition key.
- Service levels: availability target, latency percentiles per operation, durability target, and acceptable staleness per read path.
- Failure tolerance: which failure domains must survive (instance, rack, zone, region) and the recovery time and recovery point objectives.
- Organization: number of teams touching each data set and deployment cadence.
- Constraints: existing stack, data residency, budget ceiling, and migration window.

Assumptions must be stated as numbers where possible. "Traffic grows moderately" is not an assumption; "peak writes 12k/s, growing 40%/year" is.

### Operating workflow

1. Restate the invariants. For each, mark whether it requires strong consistency, bounded staleness, or eventual convergence. Most design errors originate here.
2. Build a capacity model from the inputs. Compute steady-state and peak load per component, then apply a headroom factor agreed with the owner (commonly 2x for peak on stateful tiers, stated explicitly). Show arithmetic.
3. Choose the partition key. Require that the key (a) distributes load without hot keys under the observed skew, (b) keeps the frequent query for a single operation within one partition, and (c) is stable over time. Test skew against real or sampled key distributions, not assumed uniformity.
4. Decompose by data ownership, not by function. Each entity has one writing service. Cross-service reads go through owned projections or APIs, not shared tables.
5. Select replication and consistency per data path. Map each invariant from step 1 to a mechanism: single-writer per partition, consensus-backed transactions, idempotent writes with deduplication keys, or asynchronous projections with a published staleness bound.
6. Design failure isolation. Define cell or shard boundaries so one failing unit affects a bounded fraction of users. Specify timeouts, retry budgets, bulkheads, and load-shedding priority. Retries without a budget are prohibited.
7. Plan migration as a sequence of reversible steps: dual write or change data capture, shadow reads with comparison, percentage cutover, then decommission. Each step has an abort criterion.
8. Write the decision record (see Deliverable contract) before review.

### Decision gates

Proceed past each gate only when its condition holds.

- Gate A (invariants): every write path has a named consistency level. Any path marked "best effort" needs an explicit owner sign-off.
- Gate B (capacity): peak load and headroom are computed with arithmetic shown, and the bottleneck tier is named.
- Gate C (partitioning): skew analysis exists. Maximum partition share under observed distribution is below the threshold the owner sets (state it, e.g., no partition above 5% of traffic).
- Gate D (cross-region): if multi-region, each region's write authority is defined. Active-active writes to the same entity require a conflict resolution rule that is written down and tested.
- Gate E (irreversible change): schema drops, data deletion, traffic cutover above 10%, region or vendor exit, and changes affecting external partners require explicit human approval with a named approver before execution.

### Verification and evidence

Every claim in the design needs one of: a calculation, a test result, a reference to the vendor's current documentation, or a labeled assumption.

- Run a load test at 1.5x projected peak against the proposed partition layout; record p50, p99, error rate, and the hottest partition's share.
- Inject failures in staging: kill one node per tier, partition one zone, and delay the replication stream. Record recovery time and any invariant violation.
- Verify idempotency by replaying a duplicated message batch and comparing final state.
- Check staleness bounds by measuring projection lag under peak load.
- Version-sensitive details (service limits, replication semantics, client library behavior, pricing tiers) must be checked against current official documentation for the version in use and recorded with the access date. Do not rely on memory for these values.

### Failure handling

- If capacity arithmetic and load test disagree, trust the test and revise the model; document the gap.
- If a hot partition appears after launch, first apply a load-shedding limit on the key, then split the key space. Do not change the partition key on a live system without a migration plan under Gate E.
- If an invariant cannot be met under a required failure mode, return to Inputs and renegotiate the availability or consistency target with the owner. Do not silently weaken the invariant.
- If a required measurement is unavailable, mark the decision provisional with an expiry and a named measurement owner.

### Deliverable contract

Produce a single decision record containing, in order:

1. Scope and invariants table (invariant, consistency level, owner).
2. Capacity model with arithmetic and headroom factor.
3. Partition key choice with skew evidence and rejected alternatives.
4. Service and data ownership map.
5. Failure domains, isolation boundaries, and timeout and retry budgets.
6. Migration steps with abort criteria and approval points.
7. Open assumptions, each with owner and resolution date.
8. Verification results, or the list of tests still required before go-live.

Do not include: unexplained diagrams, unquantified adjectives such as "highly scalable," unnamed "industry standard" claims, or guarantees of availability or compliance.


## pattern-selection-and-implementation

**Use when:** Use when choosing, applying, or reviewing a software design pattern (creational, structural, behavioral, or architectural) for a concrete code change, and when a team needs to justify whether a pattern is warranted or should be avoided.

### Purpose and boundaries

This skill guides selecting a design pattern for a specific problem, implementing it with minimal footprint, and verifying that it removes the forces it was chosen to address. It covers object-level patterns (factory, strategy, adapter, decorator, observer, state, command, repository), module-level boundaries (facade, anti-corruption layer, ports and adapters), and integration-level patterns (retry wrappers, circuit breakers, outbox) when they appear inside application code.

It does not cover: choosing a full system architecture (microservices versus monolith), selecting infrastructure products, or rewriting an existing codebase to a new paradigm. Route those to architecture decision work.

### Inputs and assumptions

Before selecting anything, collect:

- The concrete change: the behavior to add, modify, or isolate.
- The forces: what varies, what is stable, how often the variation occurs, and who changes it.
- Constraints: language, framework, team familiarity, performance budget, backward compatibility requirements.
- Existing idioms in the codebase. Match them unless they are the problem.

Assume the team has not yet committed to a pattern. If a pattern is already named in the request, verify it fits the forces before implementing it.

### Operating workflow

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

### Decision gates

Proceed with a pattern only if all apply:

- **Gate 1 - Variation is real:** at least two current variants, or one variant with a documented near-term second, with a named owner.
- **Gate 2 - Variation is isolated:** the variation can be confined to one seam without touching most callers.
- **Gate 3 - Indirection pays off:** the added types and indirection are fewer than the duplicated or conditional logic removed. Count both.
- **Gate 4 - Team can maintain it:** a developer unfamiliar with the pattern can locate the variant point within five minutes using names alone.

Reject the pattern and use plain code if: there is one variant with no evidence of a second; the switch has three or fewer cases and changes rarely; the pattern requires reflection or runtime magic the codebase does not already use; or the pattern duplicates a language feature (for example, a first-class function where a single-method interface is proposed).

### Verification and evidence

Each change must produce:

- Before/after count of conditional branches on the variant axis in callers (target: zero branches on variant identity outside the seam).
- Existing tests pass unchanged, except tests that assert on internal structure, which must be justified.
- A test per variant exercising the seam contract, plus one test for unknown-variant handling.
- A test demonstrating the new variant can be added by creating one new type and one registration, without editing existing callers. Build this as an executable check, not a claim.
- Performance check where the path is hot: measure before and after on the project's own benchmark harness; do not estimate.

Framework or library APIs used in the implementation are version-sensitive. Verify method signatures, lifecycle semantics, and dependency-injection registration rules against current official documentation for the pinned version before finalizing.

### Failure handling

- **Pattern makes callers harder to read:** revert to the simpler candidate from step 3 and record why.
- **Second variant turns out to differ in shape:** the interface was too narrow. Widen it deliberately, update all variants, and note the change; do not add optional parameters that only one variant uses.
- **Hidden coupling appears** (variant needs caller state): move that data into the request object rather than giving the variant a back-reference.
- **Tests fail only after refactor:** inspect whether behavior or ordering changed; restore the characterization baseline before proceeding.

### Deliverable contract

Return:

1. Forces summary (one paragraph).
2. Candidate table: pattern, mechanism, added types, gates passed or failed.
3. Chosen pattern with the rejection reason for each alternative.
4. Seam location (file and symbol names as they exist in the repository).
5. Diff or implementation plan, step-ordered.
6. Verification results: test outcomes, branch-count before/after, extension-test evidence.
7. Open risks and any version-sensitive items pending verification against official documentation.

Do not: introduce a pattern to satisfy a checklist; add abstractions for hypothetical future variants without an owner; change public interfaces without an explicit approval step; delete or rewrite existing tests to make them pass; or propagate provider-, vendor-, or framework-specific types beyond the seam. Changes that alter public APIs, data formats, persisted state, or deployed behavior require explicit approval from the code owner before implementation.


## performance-and-architecture

**Use when:** Use when designing, reviewing, or tuning the performance and architecture of authentication, authorization, session, or security-critical request paths, including latency budgets for login and token validation, caching of auth decisions, hashing cost tuning, rate limiting placement, and scaling of identity services.

### Purpose and boundaries

This skill guides engineers through making security-relevant components fast, scalable, and still correct. It covers the performance characteristics and architectural placement of:

- Credential verification (password hashing, MFA checks, passkey/WebAuthn verification)
- Token issuance and validation (JWT, opaque tokens, introspection)
- Session stores and revocation propagation
- Authorization decision points (policy engines, RBAC/ABAC lookups, permission caches)
- Rate limiting, lockout, and abuse controls on auth endpoints
- Identity provider dependencies (JWKS fetches, directory lookups, SSO round trips)

It does not cover general application performance unrelated to security, cryptographic algorithm design, or certifying compliance with any standard. Security correctness takes priority over latency: never trade away a check to meet a budget. Trade-offs must be stated, not hidden.

### Inputs and assumptions

Before acting, collect:

1. The request path diagram, including which components are on the critical path for each auth operation.
2. Current measurements: p50/p95/p99 latency, throughput, error rates, and resource use for each auth operation, from production or a representative load test.
3. Traffic shape: peak logins per second, token validations per second, ratio of cached to uncached decisions, and burst patterns.
4. Revocation requirements: maximum acceptable time between revoking access and enforcement.
5. Security requirements: which checks are non-negotiable and which data may be cached, and for how long.
6. Target environment constraints: hardware, managed service limits, regional topology.

If measurements are absent, state that all proposed budgets are estimates and must be validated. Do not assume a library's default cost parameters are appropriate for the hardware.

### Operating workflow

1. **Map the critical path.** List every network hop, store read, and crypto operation between the client request and the authorization decision. Mark each as mandatory or optional for correctness.
2. **Attribute latency.** Break the measured p95 into components. Typically the largest contributors are password hashing, remote JWKS or introspection calls, and synchronous policy or directory lookups.
3. **Set budgets per operation.** Example: token validation at the edge under 5 ms p95 with local verification; interactive login under a budget agreed with product, dominated by intentional hashing cost.
4. **Select the lever.** Choose from: caching verified results, moving checks to local verification, batching lookups, reducing hop count, tuning hashing parameters, or relocating rate limiters closer to the edge. Apply one lever per change.
5. **Quantify the security impact.** For each lever, state what revocation delay, staleness, or weakened check it introduces.
6. **Implement behind a flag or canary,** then compare against the baseline with identical load profiles.
7. **Record the decision** in an architecture note: problem, options, chosen option, measured result, residual risk.

### Decision gates

Stop and seek explicit approval before proceeding when any of these apply:

- Reducing hashing cost parameters, changing the password hashing algorithm, or migrating stored credentials. These affect every user and may require a rehash-on-login plan.
- Extending cache lifetime for authorization decisions beyond the agreed revocation window.
- Skipping signature verification, audience/issuer checks, or expiry checks for any path, even for internal traffic.
- Moving session or token state to a store with different durability, replication, or data residency characteristics.
- Changing rate limits or lockout thresholds in production, since this can lock out legitimate users or open brute-force paths.
- Any rollout that affects all users at once rather than a canary cohort.
- Deleting or flushing session, token, or revocation stores.

Proceed without approval only for changes in a non-production environment, read-only measurement, and adding instrumentation.

### Verification and evidence

Each change must show:

- Baseline and post-change p50/p95/p99 under the same load profile, with sample size and duration stated.
- Error rate and authentication failure rate unchanged within a defined tolerance (for example, no increase in false denials beyond the agreed margin).
- A revocation test: revoke a credential or role and measure the time until denial, compared against the requirement.
- Negative tests confirming that invalid signatures, expired tokens, wrong audiences, and revoked sessions are still rejected after the change.
- Cache hit ratio and staleness metrics, with eviction and TTL behavior documented.
- Resource metrics for hashing workers (CPU saturation, queue depth) to confirm the bottleneck moved as predicted.

Mark any library-specific parameter, cost factor, or API behavior as version-sensitive. Verify against current official documentation before recommending values. Do not state benchmark numbers that were not measured in this environment.

### Failure handling

- **Latency regression after change:** roll back the flag first, then investigate. Do not tune further under production load.
- **Cache causing stale denials or stale grants:** shorten TTL, add explicit invalidation on revocation events, and re-run the revocation test.
- **Identity provider or JWKS endpoint unavailable:** verify that the system fails closed for protected operations, and that cached keys are used only within their documented validity window. Never accept unverifiable tokens to preserve availability.
- **Hashing queue saturation during login spikes:** shed or queue requests with clear user-facing retry guidance; do not lower hashing cost to clear the queue.
- **Measurement inconsistent between runs:** increase run duration and repeat, and check for warm-up effects before drawing conclusions.

### Deliverable contract

Produce a design or review note containing, in order:

1. Scope: which operations and components were analyzed.
2. Baseline table: operation, p50, p95, p99, throughput, and the environment and load profile used.
3. Critical path diagram or ordered list with latency attribution.
4. Proposed changes, each with the lever used, expected gain, and the security trade-off stated explicitly.
5. Approval status for each gated item.
6. Verification results: performance comparison, revocation timing, negative test outcomes.
7. Residual risks and open questions, including any version-sensitive items pending documentation check.
8. Rollback plan with the exact flag or configuration to revert.

Do not present expected gains as achieved results. Do not omit security trade-offs to make a proposal look favorable. Do not recommend weakening verification to meet a latency target.

