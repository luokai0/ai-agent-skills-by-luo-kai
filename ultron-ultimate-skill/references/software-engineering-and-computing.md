# Software Engineering and Computing

This reference module belongs to the single **Ultron Ultimate Skill**. Load it only when a task requires one or more listed capabilities. The parent `SKILL.md` defines the shared task lifecycle, authorization rules, routing policy, and delivery contract.

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


## git-workflow-automation

**Use when:** Use when designing, auditing, or scripting Git branching, commit, rebase, tagging, hook, or CI-triggered repository workflows that must stay safe for shared history and team review.

### Purpose and boundaries

This skill covers automating repeatable Git operations: branch creation and naming, commit message validation, pre-commit and pre-push hooks, scripted rebases onto a base branch, release tagging, changelog extraction from history, and status reporting for CI. It applies to local scripts, hook configurations, and repository-hosted pipeline steps that call Git.

It does not cover: hosting-platform administration (branch protection rules, access control, webhook setup), history rewriting of published branches, repository migration or history filtering across repositories, or cryptographic signing key management. Those require a separate review and explicit owner approval.

### Inputs and assumptions

Before writing automation, confirm:

- Git client version on target machines and runners. Command behavior and config keys differ across versions; verify flags and config options against current official Git documentation for that exact version.
- Branching model in use (trunk-based, release branches, or feature branches off a development branch) and the protected base branch name.
- Whether commits in scope have already been pushed to a shared remote.
- Commit message convention, if any, and whether it is enforced by a tool already present in the repository.
- Runner environment: whether the job has write credentials, whether the checkout is shallow, and whether submodules or LFS objects are involved.

If any assumption is unknown, stop and request it. Do not guess branch names, remote names, or convention rules.

### Operating workflow

1. Identify the operation class: read-only (status, log, diff, describe), local-mutating (commit, branch, rebase on unpushed commits), or remote-mutating (push, tag push, delete remote branch).
2. Run read-only inspection first: `git status --porcelain`, the current branch, the upstream tracking ref, and ahead/behind counts against the base branch. Record outputs as evidence.
3. For local-mutating steps, create a backup ref or branch before rewriting anything (for example, a timestamped `backup/` branch) and log its object name.
4. Prefer `--ff-only` merges for synchronization and explicit `--force-with-lease` only when a rewrite of an unshared branch has been approved. Never use bare `--force`.
5. Validate commit messages with a script that checks subject length, imperative mood heuristics only if the team has adopted them, and ticket reference format. Reject rather than auto-correct.
6. Generate tags and changelogs from commit ranges with an explicit `base..head` range. Never derive a release range from "latest" without printing the resolved SHAs.
7. Emit a structured log of every command executed, its exit code, and resolved object IDs.

### Decision gates

Do not advance a repository change without maintainer approval when any of these conditions is present:

- The action deletes a branch, tag, or file, or runs `git clean`, `git reset --hard`, or `git gc --prune=now`.
- The action pushes to, force-updates, or deletes any remote ref, including tags.
- The action rewrites commits reachable from a remote-tracked branch.
- The action changes hooks, `.gitattributes`, or repository configuration committed for all contributors.
- The action touches commits containing credentials, personal data, or license-restricted material, or any history-filtering operation.
- The action would run in a CI job holding deploy or publish credentials.
- Working tree state is dirty and the script would proceed without stashing or refusing.

Proceed without approval only for read-only commands and local, non-destructive commits on a newly created feature branch.

### Verification and evidence

Each run must produce:

- Pre- and post-state: branch name, HEAD SHA, upstream SHA, and `git status --porcelain` output.
- For rebases: the list of rewritten SHAs mapped to originals (from reflog or recorded before-state), and a test or build result on the rewritten tip.
- For tags: the tag object type (annotated), target SHA, and confirmation that the tag does not already exist locally or on the remote.
- For hooks: a passing run against one known-good and one known-bad sample commit message or diff.

Quality checks:

- Zero commands use bare `--force`.
- Zero destructive commands run without a logged approval reference.
- Every automated commit message passes the repository's validator with no warnings suppressed.
- Hook execution time stays within the team's agreed budget; measure it, do not assume.

### Failure handling

- Non-zero exit from any mutating command: stop, do not retry automatically, restore from the recorded backup ref only after confirming the cause.
- Rebase conflict: abort with `git rebase --abort`, report conflicting paths, and hand resolution to a human. Do not auto-resolve by choosing "ours" or "theirs".
- Rejected push (non-fast-forward): do not force. Fetch, inspect divergence, and report.
- Missing or unreadable remote: report the remote URL with credentials redacted; do not attempt alternative endpoints.
- Lock file present (`index.lock`): verify no Git process is running before any removal, and require approval to delete it.
- Hook failure in CI: fail the job; do not add bypass flags such as `--no-verify` to make it pass.

### Deliverable contract

The deliverable is a single bundle containing:

1. The script or configuration, with a header stating required Git version (marked for verification against official documentation) and required inputs.
2. A dry-run mode that prints intended commands and resolved SHAs without mutating state.
3. An execution log in structured form (JSON lines preferred) with timestamps, commands, exit codes, and object IDs.
4. A short operator note listing approval gates encountered and which were granted, by whom, and when.
5. A list of unverified version-sensitive items that the operator must confirm against current Git documentation before production use.

Do not deliver scripts that cannot be dry-run, that print secrets, or that silently skip failed checks.

### Ultron routing contract

**Choose this skill when:** the requested deliverable is repeatable automation around Git itself: scripts, hooks, reusable command sequences, commit validation, branch automation, changelog extraction, or Git operations embedded in a pipeline.

**Choose `version-control-delivery` instead when:** the task is a one-off or interactive repository workflow such as inspecting a working tree, creating and preparing a feature branch, staging a specific change, resolving conflicts, preparing a review, recovering local work, or deciding how to integrate a change.

**Handoff contract:** the delivery workflow defines the repository policy and approved state transitions. This skill encodes only those approved transitions into automation, with explicit inputs, dry-run behavior, refusal conditions, idempotency, logs, and tests. Automation must not silently broaden the human-approved operation.

**Why the boundary exists:** automating a workflow is not the same as deciding which repository action is appropriate. The policy and recovery rules must exist before they are encoded in a script or hook.


## hardware-kernel-diagnostics

**Use when:** Use when investigating Linux hardware faults, kernel log errors, device driver failures, PCIe/NVMe/storage/network/GPU anomalies, thermal or power events, or machine check errors on a Linux host and a root cause or safe mitigation is needed.

### Purpose and boundaries

This skill guides read-first diagnosis of hardware-related faults visible to the Linux kernel: kernel log (dmesg/journal) errors, device enumeration problems, driver resets, storage and filesystem I/O errors, PCIe link and AER events, memory error reports (EDAC/MCE), thermal throttling, and power or firmware-correlated anomalies.

In scope: collecting evidence, classifying fault domains, correlating events with time and hardware identity, recommending reversible mitigations, and producing a diagnostic report with confidence levels.

Out of scope: physical component replacement decisions without evidence, firmware flashing, BIOS/UEFI setting changes, kernel rebuilds, driver source patching, RAID or filesystem repair writes, and vendor warranty claims. These require the approval gates below.

### Inputs and assumptions

Required before starting:
- Host identity, kernel version (`uname -r`), distribution, and whether the host is production.
- Symptom statement with approximate start time and timezone.
- Access level: confirm whether you have read-only, sudo, or console access.
- Recent changes: kernel updates, firmware updates, hardware moves, driver installs, workload changes.

Assumptions to verify rather than accept: clock sync (NTP state), log retention (journal may be volatile), and whether the host runs a hypervisor (faults may belong to the host, not the guest).

### Operating workflow

1. **Freeze context.** Record kernel version, uptime, boot ID, and the current time. Note whether logs persist across boots (`journalctl --list-boots` shows availability).
2. **Capture kernel errors.** Pull warnings and errors for the relevant window, e.g. `journalctl -k -p warning --since "<start>"`, and for the previous boot if a reboot occurred (`-b -1`). Save raw output before filtering.
3. **Inventory hardware.** Use `lspci -nnk`, `lsblk -o NAME,MODEL,SERIAL,TRAN,HCTL`, and `lscpu`. Map each error-reporting device to a bus address or block device.
4. **Classify the fault domain.** Assign each event to one of: storage, PCIe/link, memory, CPU/machine check, thermal/power, network, GPU/accelerator, firmware/ACPI, or software-induced (driver bug, misconfiguration).
5. **Check counters and health.** Read device-native health data where a read-only tool exists: SMART/NVMe log pages (`smartctl -a` or `nvme smart-log`), EDAC counters under `/sys/devices/system/edac/`, AER counters under `/sys/bus/pci/devices/*/aer_dev_*`, and thermal zones under `/sys/class/thermal/`. Record values with timestamps; a single snapshot is weak evidence.
6. **Correlate.** Align kernel events, workload spikes, and maintenance windows on one timeline. A fault that starts at the same second as a firmware update or a cooling change is a lead, not a conclusion.
7. **Reproduce only when safe.** Repeat a read-only trigger (e.g., `fio` read-only job against a non-critical device) only after approval.
8. **Rank hypotheses** and state the discriminating test for each.

### Decision gates

- **Gate A (scope):** If the host is production and the symptom is data-affecting (I/O errors, corruption, unexpected reset), stop non-read actions until the owner approves.
- **Gate B (writes):** Any command that modifies state requires explicit approval: driver unload/reload, device reset (`echo 1 > .../reset`), PCI remove/rescan, `nvme format`, `smartctl -t` self-tests (they add load), filesystem check with repair, sysctl changes, module parameter changes, reboot, firmware update.
- **Gate C (external impact):** Opening vendor tickets, sending logs or serial numbers outside the organization, or contacting the hardware vendor requires approval and data-minimization review (strip hostnames, IPs, user data).
- **Gate D (sensitive data):** Kernel logs can contain usernames, IPs, and file paths. Redact before sharing.
- **Escalate to hardware replacement** only when at least two independent indicators agree (e.g., rising SMART media errors plus repeated AER correctable errors on the same slot) and the failure reproduces across a boot or a re-seat-free check.

Decision criteria examples:
- Corrected memory errors rising on one DIMM across days: replacement candidate after confirmation via EDAC per-DIMM counters.
- Single `AER: Corrected error` with no recurrence over a week: monitor, do not act.
- `nvme nvme0: I/O ... timeout` followed by controller reset with clean SMART: investigate driver, firmware level, and power states before blaming media.
- `mce: [Hardware Error]` with CPU temperature events: correlate with cooling and load before concluding CPU fault.

### Verification and evidence

Quality checks for a completed diagnosis:
- Every claim cites a log line or counter with timestamp and boot ID.
- Each hypothesis lists one confirming and one refuting observation.
- At least two independent data sources support any hardware-fault conclusion.
- Counters were sampled at least twice with an interval, and deltas are reported.
- Tool versions and output formats are recorded. Smartctl, nvme-cli, and kernel EDAC/AER interfaces change across releases; confirm flag names and output fields against the current official man pages and kernel documentation before relying on them.
- Benchmark or throughput numbers are reported only as measured in this environment, never as expected vendor figures.

### Failure handling

- **No logs available:** State that the window is unobservable; recommend enabling persistent journaling as a proposed change requiring approval.
- **Tool missing or restricted:** Fall back to sysfs and procfs reads; do not install packages without approval.
- **Contradictory evidence:** Keep both hypotheses open, identify the single test that separates them, and request approval if that test is a write.
- **Error storm hides signal:** Rate-limit by device and time bucket before counting.
- **Host becomes unstable during diagnosis:** Stop active tests, preserve logs, and escalate to the owner immediately.

### Deliverable contract

Produce a report containing:
1. Summary: symptom, affected components, current status, and confidence (high, medium, low).
2. Timeline: ordered events with timestamps, boot IDs, and sources.
3. Evidence table: observation, source command or path, value, delta over time.
4. Fault domain classification and ranked hypotheses with discriminating tests.
5. Actions taken, with approval references for any write operation.
6. Recommended next steps: reversible first, each tagged with its gate.
7. Open items and unverified assumptions, including any version-sensitive command details flagged for official-documentation confirmation.

Do not state a root cause without evidence meeting the verification checks. Do not recommend hardware replacement without Gate E-level evidence. Do not run destructive commands, reboot, or alter firmware or BIOS settings on your own initiative, and do not share unredacted logs outside the owning team.


## language-engineering-and-source-control

**Use when:** Use when designing, modifying, or reviewing language tooling (parsers, grammars, DSL syntax, compilers, interpreters, formatters, linters, language servers) or when organizing, branching, reviewing, or recovering history in a source repository that contains such tooling.

### Purpose and boundaries

This skill covers two linked concerns: (1) changing language artifacts (grammar, syntax definitions, parser and lowering code, type or semantic rules, code generators, diagnostics, formatters) safely, and (2) managing the repository history and workflow those changes travel through. It does not cover product feature design unrelated to the language, general infrastructure, or deployment of runtime services. Use it for work where a syntax or semantic change can break existing source files, downstream tools, or published packages.

### Inputs and assumptions

Before acting, establish:

- The language version or grammar revision in scope and whether it is published.
- A corpus of representative source files (valid and invalid) with expected outputs.
- The branching model in use and the protected branches on the remote.
- Who consumes the output: editors, build systems, external users, or other teams.
- Whether the repository has history that must be preserved for audit or for other clones.

If any of these are unknown, state the assumption explicitly in your output. Do not infer remote permissions or release schedules.

### Operating workflow

1. Inspect current state. Record the branch, uncommitted changes, and whether the working tree is clean. Do not stash, reset, or discard changes you did not create.
2. Reproduce the behavior. Run the existing parser or test suite against the corpus and capture the baseline output.
3. Classify the change: additive (new construct that previously was a syntax error), behavioral (existing valid input now parses or evaluates differently), or breaking (previously valid input is rejected or changes meaning).
4. Make the smallest change that satisfies the classification. Keep grammar edits, generated files, and hand-written logic in separate commits.
5. Regenerate derived artifacts with the project's documented generator. Commit generated output only if the project tracks it, and confirm the generator version matches the one recorded in the repository.
6. Add corpus cases: one positive case, one negative case, and one boundary case per new construct.
7. Commit in logical units with messages that state the language-level effect (for example, "Reject bare trailing commas in list literals; previously parsed as empty element").
8. Prepare the branch for review: rebase onto the current base only if the branch is private and unpublished; otherwise merge the base.

### Decision gates

Stop and request explicit approval before any of the following:

- Force-pushing, rewriting published history, or deleting branches or tags on a shared remote.
- Changing a grammar or semantic rule classified as breaking, or any change that alters the meaning of existing valid programs.
- Publishing, tagging a release, or uploading a package or grammar to an external registry.
- Editing protected branch settings, CI secrets, or signing configuration.
- Regenerating and committing artifacts that other teams consume without a version bump.
- Deleting corpus files, golden outputs, or test cases to make a suite pass.

For breaking changes, the required record is: affected constructs, migration example, and the version number under which the break ships. Confirm the version scheme with the maintainers rather than choosing one.

### Verification and evidence

A change is complete only when:

- The full corpus produces the expected output; any diff from baseline is listed and justified.
- Round-trip checks pass where the language supports printing and reparsing: parse, print, reparse yields an equivalent tree.
- Error recovery is tested: invalid input yields diagnostics with correct locations and does not crash or hang. Include at least one input that is truncated mid-token.
- Generated code is reproducible: regenerating from a clean checkout produces no diff.
- The commit history reads cleanly and each commit builds and passes its own tests where feasible.

Report results as counts: corpus cases passed, cases changed from baseline, diagnostics added or removed. Do not claim performance improvements or coverage figures without measuring them in the same environment.

### Failure handling

- If the baseline already fails, do not start the change. Report the pre-existing failure with its reproduction steps.
- If a generator fails or produces a different diff than the committed output, stop and identify the tool version difference. Do not hand-edit generated files to match.
- If a merge conflict touches grammar tables, resolve by regenerating from the merged grammar, not by merging generated text.
- If a test is flaky, record its failure rate across repeated runs and treat it as failing until diagnosed.
- If a history rewrite was accidental, stop, record the reflog or remote state, and ask for approval before any recovery action.

### Deliverable contract

Return:

1. A summary of the change classification (additive, behavioral, or breaking) with one-sentence justification.
2. The list of commits with their purpose.
3. The corpus results: pass counts, baseline diffs, and new cases added.
4. Any version-sensitive tool, generator, or dependency detail marked "verify against current official documentation."
5. A list of pending approvals required before merge or release.
6. Explicit assumptions and open questions.

Do not include unverified benchmark numbers, invented command flags, or statements that a change is compliant with any standard.


## language-internals-engineering

**Use when:** Use when analyzing, modifying, debugging, or designing language runtime, compiler, interpreter, garbage collector, VM, or parser internals, including bytecode, memory layout, JIT, and calling-convention work.

### Purpose and boundaries

This skill guides work on the internal machinery of programming languages: lexers and parsers, intermediate representations, bytecode and interpreter loops, code generation and JIT tiers, garbage collectors and allocators, object layout, calling conventions, foreign function boundaries, and runtime support libraries.

In scope: reading and changing runtime or compiler source, diagnosing crashes and miscompilations, performance work on hot runtime paths, adding opcodes or IR passes, GC tuning and correctness, and writing differential or fuzz tests for language implementations.

Out of scope: writing application code in a language, language design proposals without an implementation, and kernel or hardware bring-up except where the runtime depends on it directly.

### Inputs and assumptions

Before acting, establish:

1. The exact commit or release of the implementation, and whether the task targets a fork or upstream.
2. Target platforms, architectures, and word size. Layout and ABI conclusions do not transfer across them.
3. The reproducer: a minimal program, failing test, crash log, or benchmark. If none exists, creating one is the first deliverable.
4. The build configuration (optimization level, debug assertions, sanitizers, GC mode). Record it verbatim.
5. Toolchain versions. Any flag, API, or tool behavior named from memory must be verified against current official documentation for that version before use.

If any of these is unknown, state the assumption explicitly in the output.

### Operating workflow

1. **Reproduce.** Build the unmodified tree in the recorded configuration and run the reproducer. Record exit status, output, and timing. Do not proceed on a failure you cannot reproduce.
2. **Localize.** Bisect the failing input (delta-reduce the program), or bisect history when a regression is involved. Identify the first pass, opcode, or runtime function where state first diverges from the expected model.
3. **Model the invariant.** Write down the invariant that is violated, for example "the nursery pointer is never older than the card table entry," "stack maps match live slots at every safepoint," or "constant folding preserves evaluation order of side effects."
4. **Inspect evidence, not intuition.** Dump the relevant IR, bytecode, or disassembly at the failing and last-good points and diff them.
5. **Change minimally.** Make the smallest edit that restores the invariant. Avoid opportunistic refactors in the same change.
6. **Verify** (see below), then document the invariant in a code comment or design note at the point it is enforced.

### Decision gates

- **Gate A: Fix location.** Fix at the layer that owns the invariant. Patching a symptom in a caller (for example, nulling a pointer after a GC crash) is rejected unless the owning layer is out of your control, in which case document the workaround and its scope.
- **Gate B: Undefined behavior.** If the cause is undefined behavior in C or C++ runtime code, the fix must eliminate the UB, not depend on a compiler happening to tolerate it. Confirm with a sanitizer or a documented analysis tool run.
- **Gate C: Performance claims.** A performance change requires before-and-after measurements on the same machine, with variance across at least five runs, and a stated workload. Without this, the change is labeled unverified.
- **Gate D: Optimization soundness.** A new or modified optimization must preserve semantics on the existing test corpus and on a differential run against the unoptimized path. Any case where behavior differs is a blocker.
- **Gate E: ABI or layout change.** Changing object layout, calling conventions, serialized formats, or exported symbols is a compatibility decision. Stop and obtain explicit approval before proceeding.
- **Gate F: Destructive or external actions.** Force-pushing, deleting branches or artifacts, modifying shared CI, publishing packages, or filing upstream issues or pull requests requires explicit user approval for each action.

### Verification and evidence

Minimum evidence set for a change:

- The reproducer now passes, with the command and output recorded.
- The full existing test suite passes in the recorded configuration, plus the configuration with debug assertions enabled.
- Sanitizers (address, undefined behavior, thread) run on the affected components when the language and toolchain support them. Name the exact sanitizer flags only after confirming them in current documentation.
- For GC changes: a stress run that forces frequent collections, with heap verification enabled if the implementation provides it. Report collection count and any verifier failures.
- For compiler or JIT changes: differential execution between interpreted or unoptimized and optimized modes over the corpus, with zero mismatches as the pass condition.
- For parsers: round-trip or reject-tests on malformed input, and a fuzzing run of stated duration. Report the corpus size and crash count.
- Benchmarks: a table of baseline and changed results with machine description and variance. Never state a speedup percentage without its variance.

Do not claim compliance, security certification, or correctness beyond what the tests cover.

### Failure handling

- **Cannot reproduce:** Check configuration, toolchain version, and environment differences. Report what was tried. Do not guess a fix.
- **Reproduces only under optimization:** Suspect undefined behavior, missing safepoints, or incorrect stack maps. Compare IR before and after the suspect pass.
- **Verifier or sanitizer fails in unrelated code:** Record it as a pre-existing failure with its baseline status; do not silently widen scope.
- **Fix breaks other tests:** Revert to the last clean state, reexamine the invariant, and do not suppress tests to pass.
- **Documentation conflicts with observed behavior:** Trust the observed behavior with evidence, and flag the discrepancy for the user.

### Deliverable contract

Each deliverable must include:

1. Summary of the defect or goal, in two to four sentences.
2. Environment: commit, platform, configuration, toolchain versions.
3. The violated or established invariant, stated precisely.
4. The change as a diff, with the file and function for each hunk.
5. Verification results per the evidence set, with exact commands and outcomes.
6. Unverified items, assumptions, and version-sensitive details flagged for confirmation against official documentation.
7. Open risks and any decisions requiring the user's approval under the decision gates.

Do not present a fix as complete while any required evidence item is missing. Do not include unrequested refactors, speculative optimizations, or changes outside the owning layer.


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


## programming-language-experts

**Use when:** Use when a task involves choosing, comparing, explaining, migrating between, or reviewing programming languages, language semantics, type systems, runtimes, or language-specific idioms and pitfalls.

### Purpose and boundaries

This skill guides analysis of programming languages as engineering tools: selecting a language for a workload, explaining semantics and runtime behavior, reviewing code for language-specific defects, planning ports between languages, and evaluating type-system or concurrency trade-offs.

In scope: language semantics, type systems, memory and concurrency models, standard library idioms, toolchain and runtime characteristics, interop boundaries, and migration strategy.

Out of scope: writing a full application without a stated requirement, legal or licensing judgments, performance claims without measurement, and security certification of any language or runtime.

### Inputs and assumptions

Before answering, establish:

1. The concrete workload: throughput, latency, memory ceiling, deployment target, or correctness constraint.
2. Team constraints: existing languages, hiring reality, maintenance horizon.
3. Ecosystem constraints: required libraries, platform support, regulated toolchains.
4. The language version in use. Treat any statement about features, defaults, or library behavior as version-sensitive unless the version is named.

If these are missing and they change the answer, ask. If they do not, state the assumption explicitly at the top of the response.

### Operating workflow

1. Restate the question as a decision, explanation, review, or migration.
2. Identify the semantic property that actually matters (ownership, evaluation order, null handling, concurrency model, error propagation, numeric width, GC pauses, startup cost).
3. Compare candidates only on that property and on the stated constraints. Do not rank languages in general.
4. For code review, read for language-specific hazards first: silent conversions, mutable default arguments, shared mutable state across threads, unchecked error returns, lifetime escapes, integer overflow, locale-dependent string operations, and implicit coercions.
5. For migration, map idioms rather than syntax: exceptions to result types, classes to traits or structs with functions, GC reliance to explicit resource scopes.
6. Produce the deliverable in the required contract format.

### Decision gates

Stop and request confirmation before proceeding when:

- A recommendation would require rewriting a production system, changing a deployed runtime, or altering a shared build toolchain.
- A migration touches data formats, serialization schemas, or persisted state that cannot be rolled back.
- The analysis would involve credentials, production hostnames, customer data, or executing code against external services.
- Any action would delete, overwrite, or publish artifacts.

Within analysis itself, proceed freely. Running experiments in a sandbox the user owns is permitted when they explicitly approve it.

### Verification and evidence

- Label each factual claim as one of: established semantics (stable across versions), version-sensitive (must be checked against current official documentation for the named version), or opinion/heuristic.
- Never invent API names, function signatures, compiler or interpreter flags, package versions, release dates, benchmark numbers, or certification or compliance guarantees. If a detail is unknown, say so and name where to verify it.
- Performance statements require a measurement plan: input size, warm-up, repetitions, hardware description, and the metric. Without measurement, describe expected trade-offs qualitatively.
- For semantic claims about undefined, unspecified, or implementation-defined behavior, cite the relevant specification section name or the language's official reference by title, and flag uncertainty if unsure.
- When reviewing code, show the minimal reproducing snippet for each reported defect and state the expected versus observed behavior.

### Failure handling

- If the language or version is ambiguous, list the two or three plausible interpretations and answer each briefly.
- If a question mixes multiple languages with no shared context, separate the analysis per language before comparing.
- If evidence contradicts a prior claim, correct it explicitly and state which part changed.
- If the request requires a guarantee you cannot establish (safety certification, formal correctness, regulatory fit), state the limit and recommend a qualified review.
- Do not pad an uncertain answer with confident prose. Shorter and honest beats long and wrong.

### Deliverable contract

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


## services-packages-desktop-workloads

**Use when:** Use when installing, removing, upgrading, or auditing Linux system services, software packages, or desktop workloads (login sessions, autostart entries, user units, display-manager-launched apps) on a workstation or server and needing a safe, verifiable change with rollback.

### Purpose and boundaries

This skill governs changes to three layers of a Linux system:

1. **Packages**: installation, removal, upgrade, pinning, and inventory via the host's native package manager (for example apt, dnf, zypper, pacman, or a Flatpak/Snap runtime when one is in use).
2. **Services**: systemd system units and user units, including enable/disable state, runtime start/stop, drop-in overrides, and unit ordering.
3. **Desktop workloads**: per-user graphical applications, XDG autostart entries, session-scoped processes, and display-manager-launched components.

In scope: diagnosing why a service or app misbehaves, planning a package change, executing it in a reversible order, and proving the end state.

Out of scope: kernel changes, bootloader edits, disk partitioning, network firewall policy, identity or access policy, and fleet-wide configuration management design. Refer those to the owning procedure.

### Inputs and assumptions

Before acting, collect:

- Distribution, release, and init system (confirm systemd with `systemctl --version`; do not assume).
- Target: host name, role (workstation, server, container host), and whether it is production.
- Requested change in one sentence, plus the business reason.
- Current state snapshot: installed package versions, enabled and active units, autostart entries for affected users.
- Whether a recent backup or VM snapshot exists and its restore path.
- Whether the package source is an official repository, a vendor repository, or a local file.

Assume nothing about flags, unit names, or package names. Verify them on the host with `--help`, `man`, `apt-cache policy`, `systemctl list-unit-files`, or equivalent. Treat any command syntax recalled from memory as unverified until checked against the installed version's documentation.

### Operating workflow

1. **Snapshot.** Record `systemctl list-unit-files --state=enabled`, `systemctl --failed`, the package list for affected names, and the relevant user's `~/.config/autostart/` contents. Save output to a dated file outside the change path.
2. **Identify dependencies.** For packages, query reverse dependencies before removal (apt: `apt-cache rdepends`; rpm-based: `rpm -q --whatprovides` and `dnf repoquery --whatrequires`, verifying syntax locally). For units, check `systemctl list-dependencies` and `Wants=`/`Requires=`/`WantedBy=` relations.
3. **Stage the change.** Prefer a drop-in override (`systemctl edit <unit>`) over editing vendor unit files under `/usr/lib/systemd`. Prefer disabling over masking unless masking is required to block activation.
4. **Dry run where supported.** Use simulation modes the package manager provides, and review the full list of packages to be removed or upgraded, not just the requested one.
5. **Execute one step at a time.** Apply the package change, then reload systemd only if unit files changed (`systemctl daemon-reload`), then restart the affected unit.
6. **Verify** (see the verification section), then record the post-change snapshot.

Desktop workloads follow the same order, but verification occurs inside the user session. Confirm the target user is logged in before testing graphical behavior, and never run session-scoped commands as root on the user's behalf without stating why.

### Decision gates

Stop and request explicit approval before proceeding when any of the following holds:

- The action removes packages, purges configuration, deletes data directories, or disables a unit that other units require.
- The change touches a production host, a shared server, or a host you do not control.
- The action sends data externally, opens network listeners, or changes repository trust (adding keys or sources).
- The package change would upgrade a library that multiple services link against, or the reverse-dependency list is longer than the change's stated scope.
- A service is a security control (audit, endpoint protection, authentication agent, backup agent).
- Restart would interrupt active user sessions or running jobs.
- Any step is irreversible or its rollback path is unknown.

Proceed without a gate only for read-only inspection, reversible enablement of a unit on a non-production host, and installation of an already-approved package in a test environment.

### Verification and evidence

A change is complete only when all of these hold, with evidence captured:

- `systemctl is-active <unit>` and `systemctl is-enabled <unit>` return the intended values; `systemctl --failed` shows no new entries.
- `journalctl -u <unit> --since "<change start>"` contains no new errors or repeated restart loops within a defined observation window (for example, 10 minutes for services, one full login for desktop autostart).
- Package state matches the plan: the package manager reports the expected version, and no unintended removals appear in the transaction log.
- For desktop workloads, the application launches in the target user's session, its autostart entry produces a process owned by that user, and the process is absent when the entry is disabled.
- A reboot test is performed when boot ordering or enablement changed, and the result is recorded.

Evidence means saved command output with timestamps, not a claim of success.

### Failure handling

- **Failed restart:** capture `systemctl status` and the journal, revert the override or re-enable the previous state, and run `systemctl daemon-reload` if unit files changed.
- **Broken dependency during install:** do not force resolution with flags that ignore dependencies. Roll back the transaction using the package manager's history mechanism where available.
- **Desktop app crashes at login:** disable its autostart entry for that user, confirm the session is clean, then diagnose from the user's session journal and application logs.
- **Unknown behavior after upgrade:** restore from the snapshot or VM image rather than patching piecemeal on a production host.

Do not retry a failing action more than twice without new information.

### Deliverable contract

Every completed task returns:

1. Change summary: what was changed, on which host, by which user, and why.
2. Before and after snapshot references.
3. Exact commands executed, with the verified flag syntax noted.
4. Verification results against each criterion above, with pass or fail.
5. Rollback procedure, tested or explicitly marked untested.
6. Open risks and any item that required approval, with the approver's recorded confirmation.
7. Version-sensitive details (package versions, command options, unit behaviors) marked "verify against current official documentation" where they were not confirmed on the host.

### What not to do

- Do not use `rm -rf`, purge flags, or `--force` options to clear obstacles without approval.
- Do not edit files under `/usr/lib/systemd` or other vendor-owned paths.
- Do not mask units or disable security agents on a production host without a gate.
- Do not add third-party repositories or import signing keys without approval.
- Do not restart shared services during active business hours without approval.
- Do not report a change as successful based only on the command exiting zero.
- Do not state compliance, security, or performance outcomes that were not measured.


## software-delivery-apis

**Use when:** Use when integrating with external software registries and delivery endpoints (package indexes, container registries, artifact repositories, release and publishing APIs) to discover, validate, publish, promote, or retrieve software artifacts.

### Purpose and boundaries

This skill covers programmatic interaction with external registries that store and distribute software: package indexes, container image registries, binary artifact repositories, and release/publishing endpoints. Typical tasks are resolving a version, checking whether an artifact exists, publishing a build, promoting an artifact between channels, yanking or deprecating a release, and fetching metadata for audit.

It does not cover: designing a registry server, writing general CI pipelines unrelated to registry calls, managing signing keys beyond referencing them, or making legal or licensing determinations about packages.

### Inputs and assumptions

Before acting, establish:

1. **Registry identity**: exact host, repository or namespace, and ecosystem (for example npm, PyPI, Maven, OCI, NuGet, or a generic artifact store).
2. **Operation**: read-only query, publish, promote, deprecate, or delete.
3. **Credentials scope**: which token or role is used, and whether it is read, write, or admin. Never assume write rights.
4. **Target artifact**: name, version or digest, and platform or classifier where relevant.
5. **Environment**: staging or production registry. Treat any ambiguity as production.

Assumptions must be stated explicitly in your output. Do not assume a registry supports a feature because a sibling ecosystem does.

**Version-sensitive details**: endpoint paths, authentication schemes, rate limits, required headers, and CLI flags change over time. Verify each against the registry's current official documentation before use and record the documentation version or date consulted.

### Operating workflow

1. **Classify the operation.** Read-only operations proceed directly. Any write, overwrite, promotion, deprecation, or deletion enters the decision gates below.
2. **Discover capabilities.** Query the registry's documented metadata or service-description endpoint if one exists. Confirm the artifact type, naming rules, and immutability policy.
3. **Resolve identifiers before mutating.** Convert names, tags, or ranges into an immutable reference: a content digest for containers, an exact version for packages, a checksum for binaries. Mutable tags such as `latest` must never be the sole reference in a published record.
4. **Read current state.** Fetch existing metadata for the target. Record the response, timestamp, and identifier.
5. **Plan the change.** Write the exact request(s) you intend to send, the expected resulting state, and the rollback path.
6. **Obtain approval** if any gate below applies.
7. **Execute with idempotency in mind.** Use dry-run or validation modes where the registry offers them. Send one change at a time and check each response.
8. **Verify** (see the Verification section) and produce the deliverable.

### Decision gates

Require explicit human approval before proceeding when any of the following hold:

- The operation writes to production, or the environment is unclear.
- The operation deletes, yanks, unpublishes, overwrites an existing version, or retags an existing digest. Most registries treat published versions as immutable; attempting to overwrite them is an incident, not a retry.
- The operation makes an artifact publicly visible or changes its visibility or license metadata.
- The operation uses credentials broader than the task requires, or credentials you were not explicitly given.
- The request would transmit proprietary source, customer data, secrets, or unreleased internal identifiers to an external service.
- Promotion skips a stage (for example, staging to production with no verification record).

Proceed without approval only for read-only queries against a registry the user identified, and for writes to a clearly designated sandbox or staging namespace the user named.

### Verification and evidence

A change is not complete until you have evidence of all of the following:

- **Existence check**: a read request returns the artifact at the expected identifier.
- **Integrity check**: the returned digest or checksum matches the locally computed value of the artifact you intended to publish. Compute it locally with a standard tool and record the algorithm.
- **Metadata check**: name, version, platform, and declared dependencies match the intended release notes or manifest.
- **Resolution check**: a consuming client or a fresh read resolves the version to the same digest.
- **Audit record**: the request, response status, identifiers, timestamps, and approver (if gated) are logged.

Quality thresholds: zero checksum mismatches are acceptable; any mismatch halts the workflow. Each write must have a corresponding read-back confirmation before reporting success.

### Failure handling

- **401 or 403**: stop. Do not try alternative credentials or escalate privileges. Report the scope required.
- **404 on a read**: confirm the namespace, ecosystem, and case sensitivity before concluding absence. Do not create the artifact to resolve it.
- **409 or version-exists conflict**: compare digests. If identical, the operation is already complete; report success with evidence. If different, stop and escalate; do not overwrite.
- **429 or 5xx**: back off with jitter, retry a bounded number of times, then stop. Do not retry non-idempotent writes without first reading state.
- **Partial success** (for example, an image pushed but a manifest list not updated): treat the system as inconsistent. Report the exact state and request approval for repair.
- **Unexpected response shape**: do not infer meaning from it. Capture it verbatim and escalate.

### Deliverable contract

Every completed task produces a report with these fields:

1. Registry, ecosystem, environment, and operation.
2. Documentation consulted for version-sensitive details, with date or version.
3. Target identifiers before and after: digests, versions, and channels.
4. Commands or requests executed, with redacted credentials.
5. Verification results for each check listed above, with pass or fail.
6. Gates triggered, approvals obtained, and the approver's identity as stated by the user.
7. Open risks and any steps left for the user to perform.

State what was not verified. Do not report success on partial evidence.

### What not to do

- Do not overwrite or delete published versions to "fix" them; publish a new version instead, after approval.
- Do not use mutable tags as the only record of what shipped.
- Do not hardcode or echo tokens, passwords, or signing keys into logs, reports, or committed files.
- Do not invent endpoints, flags, or package versions; verify them.
- Do not treat a successful HTTP status alone as proof of correct publication.
- Do not publish to a registry the user did not name.

### Ultron routing contract

**Choose this skill when:** the task is specifically about interacting with a software artifact registry or release endpoint through its API, CLI, or protocol: querying metadata, resolving versions and digests, authenticating, publishing a registry operation, promoting, deprecating, or verifying a registry-side state change.

**Do not use it as the sole release playbook when:** the task begins with source code and requires the complete release lifecycle: clean build, artifact assembly, provenance, signing checks, package-content review, approval, publication, installation test, and release record. Route that lifecycle to `software-engineering-delivery`.

**Handoff contract:** the release skill supplies the approved artifact identity, digest/version, target namespace, environment, allowed operation, and approval record. This skill returns the exact registry request or command, response, resolved artifact identity, resulting state, and any API-specific failure. Never infer permission to publish from the ability to call an endpoint.

**Why the boundary exists:** registry protocol execution is a reusable integration capability; release engineering is the end-to-end decision and assurance process that may call it.


## software-engineering-delivery

**Use when:** Use when preparing, publishing, deprecating, or consuming software artifacts through external registries such as package indexes, container registries, or artifact repositories, including release versioning, credential handling, and post-publish verification.

### Purpose and boundaries

This skill governs the path from a built, tested artifact to a version that is published to, or consumed from, an external registry. It covers version selection, artifact assembly, publish execution, post-publish verification, deprecation, and rollback-by-supersession.

In scope: npm, PyPI, Maven Central, crates.io, container and OCI registries, Helm chart repositories, and internal mirrors of these.

Out of scope: application deployment to runtime environments, source-code review policy, and general CI pipeline design, except where they produce or gate the artifact.

### Inputs and assumptions

Before acting, confirm:

- Target registry, namespace or owner, and package name. Check that the name is not already claimed by an unrelated party.
- Source commit or tag, and that the artifact was built from it.
- Current published versions in the registry, fetched live, not from memory.
- Release type: patch, minor, major, or prerelease, per the project's declared versioning scheme.
- Publishing identity: which account, token scope, or trusted-publisher configuration will be used.
- Changelog or release notes exist and match the commit range.

If any input is unverified, stop and record it as an open item.

### Operating workflow

1. Reconcile versions. Compare the version in manifest files against the registry's existing versions. Reject any version that already exists; published versions are immutable on most registries.
2. Verify the artifact. Build from a clean checkout at the tagged commit. Compare the file list and manifest metadata (name, version, license field, entry points, declared dependencies) against expectations. Remove development-only files that would leak into the package.
3. Scan for leaks. Search the artifact contents for credentials, environment files, private keys, internal hostnames, and test fixtures containing real data.
4. Dry run where the tool supports it. Confirm the dry-run output lists exactly the intended files and version. Verify the exact dry-run flag against current official documentation before use.
5. Request approval (see Decision gates).
6. Publish with the approved identity. Record the exact command, registry URL, and timestamp.
7. Verify from the registry, not the local build: fetch the published metadata, download the artifact into an empty directory, and compare checksums against the local build output.
8. Install the artifact into a clean environment and run the smoke test defined by the project.
9. Tag the release commit if not already tagged, and attach the checksums and release notes.

### Decision gates

Require explicit human approval, recorded with the approver's name and date, before:

- Any publish, because it is external-impacting and usually irreversible.
- Any unpublish, yank, or deletion of a version. Prefer deprecation or yanking where the registry supports it, and verify its semantics in current documentation first, since yanked artifacts may still resolve for existing lockfiles.
- Changing package ownership, maintainers, access tokens, or trusted-publisher bindings.
- Publishing under a new package name or namespace.
- Any change to license metadata.

Proceed without a gate only for read-only operations: listing versions, downloading for comparison, and running local builds.

Stop and escalate if the dry-run file list contains unexpected files, if checksums mismatch between local and registry copies, or if the token has broader scope than the release requires.

### Verification and evidence

A release is complete only when all of the following hold:

- The registry reports the new version as the latest or intended channel.
- Downloaded checksum equals the local build checksum.
- Clean-environment install succeeds with no resolution warnings.
- Smoke test passes against the installed artifact, not the source tree.
- Release record contains: commit hash, version, registry, publish identity (name only, never the secret), checksum, timestamp, and approver.

Do not claim provenance or signing guarantees unless signature or attestation verification was actually performed and the verification output is recorded.

### Failure handling

- Publish rejected as duplicate version: do not retry with the same number. Increment per the versioning scheme and rebuild.
- Publish partially succeeded (artifact uploaded, metadata missing): query the registry state before any retry. Do not republish blindly.
- Auth failure: rotate or reissue the token through the owner. Never paste secrets into logs or chat.
- Bad release discovered after publish: publish a fixed higher version and deprecate the broken one. Obtain gate approval for each step.
- Name squatting or ownership conflict: stop, document, and escalate to the registry's support process.

### Deliverable contract

The delivery returns:

1. Release record as described above.
2. Dry-run and final file lists.
3. Checksum table for each artifact.
4. Verification log summary with pass or fail per check.
5. Open items, each with an owner.

Do not:

- Publish from an uncommitted working tree or an unreviewed branch.
- Use long-lived personal tokens where scoped automation identities exist.
- Assert version-specific registry behavior, flags, or limits from memory. Verify against current official registry documentation and mark the verified date in the release record.
- Modify a published artifact in place.

### Ultron routing contract

**Choose this skill when:** the objective is to produce and release a package, image, chart, or binary as a complete, verifiable lifecycle. It owns release readiness, version reconciliation, clean artifact construction, package-content inspection, provenance and checksum evidence, approval, publication sequencing, post-publish installation checks, and rollback-by-supersession.

**Delegate registry-specific mechanics to `software-delivery-apis` when:** the work requires provider-specific API or CLI behavior, registry authentication semantics, metadata queries, promotion endpoints, or precise interpretation of a registry response.

**Handoff contract:** send the registry skill the approved registry, namespace, immutable artifact identity, exact operation, environment, credential scope, and approval reference. Require it to return request/response evidence and the authoritative resulting registry state. This skill remains accountable for the overall release decision and must independently verify the published artifact.

**Why the boundary exists:** a successful API call is not a successful release. Release readiness, artifact integrity, and post-publication verification remain separate obligations.


## systems-languages-cpp-rust

**Use when:** Use when writing, reviewing, migrating, or debugging C++ or Rust systems code, including memory safety, ownership and lifetime design, FFI boundaries, concurrency, undefined behavior, build and toolchain choices, and performance-sensitive components.

### Purpose and boundaries

This skill guides engineering decisions and reviews for C++ and Rust code where memory layout, resource lifetimes, concurrency, and native interop matter. It covers:

- Designing ownership, lifetimes, and error propagation in new components.
- Reviewing C++ for undefined behavior, lifetime hazards, and modern idiom gaps.
- Reviewing Rust for `unsafe` soundness, borrow-driven API shape, and send/sync correctness.
- Designing and auditing FFI boundaries between C++, Rust, and C.
- Choosing between C++ and Rust for a component, and planning incremental migration.
- Diagnosing crashes, data races, leaks, and performance regressions.

It does not cover application-level product design, web frameworks, or language-theory research. It does not certify compliance with any safety standard.

### Inputs and assumptions

Before advising, establish:

1. Target standard: C++ standard level (for example C++17, C++20, C++23) and Rust edition and minimum supported Rust version (MSRV). Confirm exact feature availability against current official documentation, since support varies by compiler and version.
2. Platform, target triple, and whether the code runs in kernel, embedded, real-time, or hosted contexts.
3. Concurrency model and any real-time or latency budgets.
4. Existing codebase constraints: build system, sanitizers in use, allocator, exception and panic policy.
5. Whether the task involves untrusted input, network exposure, or privileged execution.

If any of these is unknown, state the assumption explicitly in the output rather than guessing silently.

### Operating workflow

1. **Restate the goal and invariants.** Write down what must always hold (for example, "buffer owned by X, freed exactly once," or "no `&mut` aliasing across await points").
2. **Map ownership.** For each resource, name the owner, the borrowers, and the lifetime bound. In C++, identify who calls `delete`, releases a lock, or closes a handle. In Rust, identify who holds `Box`, `Arc`, or borrowed slices.
3. **Identify trust boundaries.** Mark every point where data crosses from untrusted input, from C ABI, or from another thread.
4. **Choose the mechanism.** Prefer compiler-checked mechanisms over conventions (see Decision gates).
5. **Implement or review in small units.** One boundary or one invariant per change.
6. **Run verification** (see Verification and evidence) and attach results to the deliverable.

### Decision gates

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

### Verification and evidence

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

### Failure handling

- **Sanitizer or Miri finding:** reproduce with the minimal input, identify the violated invariant, fix the root cause, and add a regression test. Do not suppress findings without a documented justification and owner approval.
- **Compiler rejects a borrow or lifetime:** reconsider ownership before adding lifetimes or cloning. Restructure data ownership first; clone only when the cost is acceptable and stated.
- **Undefined behavior suspected in C++:** isolate the translation unit, compile with sanitizers, and check the standard's wording for the construct rather than relying on observed behavior.
- **Benchmark regression:** do not merge a tuned change that loses correctness margin; report the regression and the trade-off.
- **Unable to verify:** state exactly what was not checked and why. Do not claim success.

### Deliverable contract

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


## version-control-delivery

**Use when:** Use when preparing, reviewing, or shipping code changes through Git branches, commits, tags, pull or merge requests, and release refs, including history cleanup, conflict resolution, and safe rollback planning.

### Purpose and boundaries

This skill covers getting a change from a local working tree to a reviewable, verifiable, and traceable state in a shared repository: branch strategy, commit structure, history hygiene, integration, tagging, and rollback planning.

In scope: Git-based workflows, commit message quality, rebasing private branches, resolving merge conflicts, preparing pull or merge requests, release tagging, cherry-picks and reverts, and recovering from mistaken local operations.

Out of scope: CI pipeline design, deployment infrastructure, code authoring beyond what a conflict requires, and repository administration (branch protection rules, permissions, hosting settings).

### Inputs and assumptions

Before acting, establish:

- The target branch and its protection policy (required reviews, linear history, signed commits).
- Whether the working branch is private to you or shared with others. Rewriting shared history is a gated action.
- The change's intent in one sentence, and the issue or ticket it serves.
- The release line, if the change is a fix to a supported older version.
- Repository state: run read-only inspection first (status, current branch, upstream, recent log, stash list).

Assume nothing about remote names, default branch names, or hooks. Confirm them from the repository. Tool flags and hosting-platform features change; verify any non-trivial command syntax against the current official Git and hosting-provider documentation before use.

### Operating workflow

1. **Inspect.** Record branch, upstream, `HEAD` position, uncommitted changes, untracked files, and any in-progress rebase, merge, or cherry-pick. If an operation is in progress, resolve or abort it deliberately before starting new work.
2. **Isolate.** Confirm changes belong to one logical purpose. Split unrelated edits into separate branches or commits. Stage with explicit paths or interactive hunk selection, never a blanket add of unreviewed files.
3. **Commit by intent.** Each commit should compile and pass the project's relevant tests on its own, where practical. Write a subject line in the imperative mood, under roughly 72 characters, followed by a body explaining why the change exists and any non-obvious tradeoff.
4. **Synchronize.** Update from the target branch using rebase for private branches or merge when the policy or shared history requires it. Resolve conflicts by understanding both sides' intent, then re-run tests. Never resolve by blindly choosing one side.
5. **Clean history.** Squash fixups, reword unclear messages, and remove debugging artifacts, only on private branches and only after the Decision gates below.
6. **Publish.** Push the branch with an explicit remote and refspec. Open the review request with a description containing: purpose, change summary, test evidence, risk, rollback approach, and linked issue.
7. **Integrate and tag.** After approval, integrate using the policy-mandated method. Tag releases with annotated tags on the exact merged commit. Verify the tag points where intended before pushing it.

### Decision gates

Stop and obtain explicit user approval before any of the following:

- Force-pushing, or any history rewrite on a branch others may have fetched.
- Deleting branches, tags, stashes, or reflogs; running garbage collection or pruning.
- Discarding uncommitted changes (`reset --hard`, checkout overwrites, `clean`).
- Pushing to a protected, default, or release branch, or pushing any tag.
- Merging into the target branch or creating a release.
- Changing remote URLs, credentials, signing keys, or commit author identity.
- Any operation that affects an external system (opening, closing, or commenting on review requests on the user's behalf).
- Committing files that may contain secrets, credentials, personal data, or large binaries. Check with `git status` and a diff review first; if found, stop and report.

Before a rebase or history rewrite, create a backup ref or branch at the current `HEAD` so recovery is possible.

### Verification and evidence

Quality checks, each required before publishing:

- `git diff --check` reports no whitespace errors.
- Every commit in the range builds and passes the relevant test subset, or the exception is stated in the review request.
- Commit count and scope match the stated intent; no unrelated files appear in `git diff --stat <target>...HEAD`.
- No conflict markers remain (search for `<<<<<<<`, `=======`, `>>>>>>>`).
- Author and committer identity match the expected user.
- After any rewrite, the patch-equivalence check (comparing `git range-diff` output against the pre-rewrite range) shows only intended changes.
- Tags: the tagged commit is an ancestor of the release line, and the tag is annotated.

Record the actual commands run and their results in the review request. Do not claim tests passed unless they were executed in this session.

### Failure handling

- **Push rejected (non-fast-forward):** Fetch and inspect the remote commits. Do not force. Ask the user whether to integrate or rewrite.
- **Conflict during rebase:** Resolve per file, `git add` the resolved file, continue. If the resolution is unclear, abort to the backup ref and report the conflict.
- **Wrong commit or branch pushed:** Stop. Report the exact commit hash and remote state. Revert propose options; do not rewrite shared history without approval.
- **Lost commits:** Check the reflog for the prior `HEAD` and recover into a new branch before any cleanup.
- **Hook or signing failure:** Do not bypass hooks or signature requirements. Report the message and ask for direction.
- **Uncertain command behavior:** Stop, verify against current official documentation, and only then proceed.

### Deliverable contract

Every delivery returns:

1. Branch name, base commit, and head commit hash.
2. Ordered list of commits with hashes and subjects.
3. Summary of changed paths and any excluded files, with reasons.
4. Verification record: commands run, outcomes, and any unverified items.
5. Risk statement and rollback plan (for example: revert commit hash, or tag to restore).
6. Pending approvals: each gated action not yet performed, listed explicitly.

Do not perform the publish, merge, or tag step without the approvals required by the Decision gates.

### Ultron routing contract

**Choose this skill when:** an agent must perform or guide a concrete Git workflow in a repository: inspect state, isolate changes, prepare commits, synchronize branches, resolve conflicts, prepare review, recover work, or plan a release ref transition.

**Delegate to `git-workflow-automation` when:** the user wants a reusable script, hook, bot, or CI step that will perform the same Git operation repeatedly across runs or repositories.

**Handoff contract:** provide the approved workflow, repository policy, permitted refs, exact path scope, dirty-state behavior, recovery point, and expected outputs. The automation skill must implement refusal behavior for unapproved destructive or remote-mutating operations and return a testable execution log.

**Why the boundary exists:** a safe one-time operation should not automatically become a general-purpose automation, and an automation request should not be answered with a fragile sequence of manual commands.

