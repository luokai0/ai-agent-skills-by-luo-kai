# Skill Consolidation Audit

**Repository:** `luokai0/ai-agent-skills-by-luo-kai`  
**Branch:** `main`  
**Audit date:** 2026-11-20  
**Status:** Structural and representative-content audit completed; migration not yet applied.

## Findings

### Collection 23: Windows Computer Operations

- 40 domain folders were checked.
- Every domain contains the same 30 workflow names, from `01-discover-current-state` through `30-hand-off-a-verified-outcome`.
- The current structure contains 1,200 files arranged as 40 repetitions of 30 generic workflow patterns.
- Representative comparison across all 40 domains found extensive repeated operating discipline, workflow, execution-contract, evidence, and recovery text.
- Domain-specific information still matters: target surfaces, preferred tools, safety boundaries, diagnostic commands, and verification criteria differ. These must become explicit domain profiles in consolidated skills.

### Collection 24: Linux System Operations

- All 25 distribution folders were checked.
- Every distribution contains the same 50 workflow names.
- The current structure contains 1,250 files arranged as 25 repetitions of 50 task patterns.
- Representative package-install comparison across 25 distributions showed approximately 97.9% textual similarity between the Ubuntu and Garuda variants.
- The meaningful differences are distribution-specific package managers, release models, repository rules, init systems, and exceptional operating models such as NixOS, Tails, Qubes OS, and SteamOS. Those distinctions must remain explicit and must never be flattened into one generic command path.

## Recommended consolidation architecture

The objective is to reduce repeated files while preserving every useful capability, example, safety rule, diagnostic, and recovery path.

### Windows

Organize the 40 domains into eight related groups of up to five domains. Each consolidated workflow will include:
- One shared task procedure.
- A domain selector and explicit domain profiles.
- The preferred native UI, accessibility, and PowerShell tools for each profile.
- Profile-specific safety boundaries, verification, and recovery.
- A migration map for every retired skill ID.

Target after full validation: approximately 240 consolidated workflows instead of 1,200 repeated variants.

### Linux

Organize the 25 distributions into five related groups of up to five distributions. Each consolidated workflow will include:
- One shared task procedure.
- A strict distribution and execution-environment detector.
- A native package/init/tooling profile for each supported distribution.
- Explicit special-case handling for immutable, declarative, amnesic, isolated, and non-systemd systems.
- A migration map for every retired skill ID.

Target after full validation: approximately 250 consolidated workflows instead of 1,250 repeated variants.

These are structural targets, not permission to remove useful distinctions. If a task cannot be combined safely, it remains separate.

## Required migration gates

No original skill is deleted until all of the following pass:

1. Every old skill has been assigned to a specific consolidated replacement or explicitly retained as unique.
2. All unique task instructions, commands, examples, preconditions, warnings, and recovery details are represented in the replacement.
3. The replacement has valid YAML frontmatter, a unique stable ID, and an accurate author field.
4. Commands are checked for platform validity, privilege assumptions, destructive effects, and policy bypasses.
5. Distribution and domain profiles are checked against the actual target systems.
6. The consolidated skill is tested for ambiguity, missing branches, unsafe defaults, and false success claims.
7. Catalogs, installation references, collection counts, README content, and validation workflows are updated.
8. The final diff is reviewed before any redundant files are removed.

## Repository-wide scope

The Windows and Linux findings are confirmed. The same duplicate and authorship audit must be run across the remaining collections before making repository-wide ownership or consolidation claims.

## Authorship and rights boundary

Newly authored and independently rewritten material may identify Luo Kai as its author. An author field must not be changed on material that Luo Kai did not independently author or does not have the right to relicense. Required notices and third-party rights must not be erased. A missing license is not permission to copy, modify, or redistribute.

A repository-wide claim that every skill is exclusively owned by Luo Kai is valid only after the remaining material has been independently authored or its rights have been lawfully resolved.
