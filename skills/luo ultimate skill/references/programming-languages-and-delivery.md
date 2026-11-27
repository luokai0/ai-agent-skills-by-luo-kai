# Programming Languages and Delivery

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

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

