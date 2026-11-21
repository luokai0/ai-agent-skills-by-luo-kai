---
name: terraform-iac-authoring
description: Use when writing, refactoring, reviewing, or planning Terraform configurations (HCL) for cloud infrastructure, including module design, state-safe changes, plan review, and provider upgrades.
author: Luo Kai
provenance: original
version: 1.1.0
---

# Terraform IaC Authoring

## Purpose and boundaries

This skill covers authoring and changing Terraform root configurations and reusable modules written in HCL. It includes resource and data source design, variable and output contracts, module composition, remote state usage, plan interpretation, and safe refactoring with `moved`, `import`, and `removed` blocks.

It does not cover: cloud account bootstrap or organization policy, CI/CD pipeline engineering beyond the plan/apply handoff, configuration management tools, Kubernetes manifests, or runtime application code. Hand those to the relevant skill.

## Inputs and assumptions

Before writing code, establish:

1. Target providers and their pinned version constraints (read `required_providers` and `.terraform.lock.hcl`).
2. Terraform CLI version constraint in `required_version`. Confirm the installed version matches.
3. Backend type and state location, and who holds write access.
4. Environment layout: single root per environment, or shared modules consumed by multiple roots.
5. Whether the change touches existing, live resources. If yes, treat it as a stateful change.

If any item is unknown, ask. Do not guess account IDs, regions, ARNs, CIDRs, or secret paths. Use variables or clearly marked input requirements instead.

Version-sensitive details (provider argument names, lifecycle behavior, CLI flags, backend options, and deprecations) must be checked against current official Terraform and provider documentation before being relied on.

## Operating workflow

1. **Read before writing.** Inspect the existing root module, the lock file, and any remote state data sources. Map which resources are managed where.
2. **Classify the change.** Label it as additive (new resources), in-place update, replacement (destroy then create), refactor (address change only), or state operation (import, removal from state).
3. **Design the interface first.** Define input variables with `type`, `description`, and `validation` where a value has a constrained domain. Define outputs only for values consumers need. Mark sensitive outputs with `sensitive = true`.
4. **Write resources with explicit intent.** Prefer named arguments over inferred defaults for anything that affects cost, network exposure, encryption, or deletion protection. Use `for_each` over `count` when items have stable identities.
5. **Refactor with declarative moves.** When renaming or moving resources between modules, use `moved` blocks rather than manual `terraform state mv`. Use `import` blocks for adopting existing infrastructure.
6. **Format and validate locally.** Run formatting, validation, and linting available in the repository. Do not invent tool names; use what the project already declares.
7. **Produce a plan and read it.** Run plan against the correct workspace or state. Review every action line, not just the summary counts.
8. **Hand off** with the plan summary, risk notes, and rollback posture (see Deliverable contract).

## Decision gates

Stop and request explicit human approval before proceeding if any of the following hold:

- The plan contains any destroy or replace action on stateful resources (databases, storage buckets, encryption keys, DNS zones, identity objects, persistent volumes).
- The change alters IAM policies, network ingress rules, public exposure, or encryption settings.
- The change modifies or removes state, runs `import` against live resources, or edits backend configuration.
- The change upgrades a provider across a major version or raises `required_version`.
- The target workspace or state file is ambiguous, or appears to be production when the request suggested otherwise.
- The change would apply to infrastructure owned by another team.

Approval must name the specific actions being approved. A general "go ahead" does not cover new destroy actions discovered later in the plan. Re-plan and re-request if the plan changes.

Do not run `apply`, `destroy`, `state rm`, or `force-unlock` without this explicit approval. Do not suggest `-target` as a routine fix; it bypasses dependency analysis and requires justification in the handoff.

## Verification and evidence

Each change must carry:

- **Format check:** the repository's formatter reports no diff.
- **Validation:** configuration validates without errors in every affected root.
- **Plan review:** the plan is attached or quoted with resource addresses for every create, update, replace, and delete. Count of each action type matches what was described.
- **Expected-no-op check:** for refactors, the plan shows zero resource changes apart from moved addresses. Any other action indicates a bug.
- **Drift note:** if plan shows changes unrelated to the request, report them as drift and do not silently absorb them.
- **Lock file:** if providers changed, the lock file diff is included and reviewed.

Measurable checks: every variable without a default is documented; no resource uses hardcoded credentials, account IDs, or region strings that belong in variables; every module input has a type; every stateful resource has the protections the repository standard defines (for example, deletion protection or `prevent_destroy` lifecycle where appropriate). Confirm these by searching the diff, not by memory.

## Failure handling

- **Plan errors on dependency cycles:** restructure references or split the root. Do not add `depends_on` to paper over an unclear graph without explaining it.
- **Unexpected replacement:** stop. Identify the argument that forces replacement from the plan output and the provider documentation for that argument. Options are usually to revert the argument, use a `moved` block if the change is a rename, or obtain approval for a planned replacement with a data-preservation step.
- **State lock held:** do not force unlock. Confirm with the owner whether the lock is stale.
- **Apply partially failed:** do not re-run blindly. Re-plan, compare with the failed apply output, and report which resources reached which state.
- **Provider upgrade breaks plan:** pin the previous version, record the failing argument, and check the provider upgrade guide before retrying.

## Deliverable contract

Every completed change returns:

1. Summary of intent in one paragraph.
2. Change classification (additive, update, replacement, refactor, state operation).
3. Files changed, with a one-line reason per file.
4. Plan summary: counts per action type, and every replace or destroy listed by resource address.
5. Verification results from the checks above, with any failures stated plainly.
6. Approval status for each gated action, and what remains unapproved.
7. Rollback posture: how to revert the code, and whether reverting state is possible or requires restore from backup.
8. Open questions and version-sensitive items flagged for verification against current documentation.

## What not to do

- Do not hardcode secrets, passwords, tokens, or private keys in configuration or variable defaults. Reference the secret store the repository uses.
- Do not use `-target`, `-replace`, `state rm`, or `force-unlock` as routine workflow steps.
- Do not disable lifecycle protections to get a plan to pass.
- Do not wildcard IAM actions or resources without an explicit, recorded justification.
- Do not invent provider arguments, module sources, or version numbers. Verify them.
- Do not merge modules that serve different ownership or change cadence.
- Do not claim a configuration is compliant, secure, or cost-optimal. Report what was checked and what was not.

## Ultron routing contract

**Choose this skill when:** the deliverable is authoring or changing Terraform configuration: HCL resources, modules, variable/output contracts, providers, state references, composition, refactoring, and review of plan changes.

**Choose `terraform-test-and-import` when:** the task is writing Terraform native tests and assertions, validating behavior, or importing existing infrastructure into state without recreating it.

**Handoff contract:** this skill supplies the intended resource/module design and expected plan. The test/import skill returns test coverage, import mapping, state-address reconciliation, and evidence that adoption will not create or destroy unintended resources. Feed any required HCL corrections back here. Do not use import as a substitute for designing the desired configuration.

**Why the boundary exists:** authoring defines the desired infrastructure; tests and import workflows prove that the configuration behaves as intended and safely adopts existing resources.
