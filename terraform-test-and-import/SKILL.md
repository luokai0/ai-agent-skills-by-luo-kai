---
name: terraform-test-and-import
description: Use when writing or running Terraform test suites (.tftest.hcl), adding assertions to modules, or bringing existing cloud resources under Terraform management through import blocks or state adoption.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Terraform Test And Import

## Purpose and boundaries

This skill covers two tasks: (1) verifying Terraform configuration behavior with native test files and assertions, and (2) adopting existing infrastructure into Terraform state without recreating it. It does not cover provider authoring, multi-cloud architecture design, or general CI/CD pipeline setup. It does not authorize applying changes to shared environments.

## Inputs and assumptions

Collect before starting:
- Terraform version and provider version constraints from `required_providers` and the lock file. Treat all syntax below as version-sensitive; confirm `terraform test`, `run` blocks, `assert`, and `import` blocks against current official Terraform documentation for the pinned version.
- Module source and its variables, outputs, and resource graph.
- For imports: the resource addresses to create, the provider-specific import ID format (look it up in the provider's resource documentation; never guess), and the current remote state of each resource.
- Backend type and state location. Confirm whether it is local, remote, or shared.

If any input is missing, stop and request it.

## Operating workflow

**Testing**
1. Read the module's variables and outputs. List behaviors worth asserting: naming rules, encryption flags, CIDR validity, conditional resource counts, output shape.
2. Create `tests/` with one `.tftest.hcl` file per behavior group. Use `command = plan` for logic and input validation. Use `command = apply` only against disposable sandbox accounts and only with explicit approval.
3. Write each `run` block with explicit `variables`, then add `assert` blocks whose `condition` references concrete attributes. Prefer one assertion per property so failures are diagnosable.
4. Run `terraform test` with verbose output. Confirm test count and assertion count match your plan.
5. Add a negative case for every validation rule, using `expect_failures` where the version supports it.

**Importing**
1. Run `terraform plan` on the current configuration and confirm zero unexpected changes before adding anything.
2. Write the resource block with the minimum arguments needed to match the live resource.
3. Declare an `import` block with the target address and provider ID. Alternatively, use the CLI import path if the pinned version or workflow requires it.
4. Generate a draft configuration only where the version supports it, then review and edit it manually. Generated code is a starting point, not a deliverable.
5. Run `terraform plan`. Iterate on arguments until the plan shows no changes for the imported resource. Attribute diffs that Terraform wants to correct need a decision, not silent acceptance.
6. Remove the `import` block after the state is recorded, and keep it only when the workflow requires it for other team members.

## Decision gates

- **Stop and request approval** before any `apply`, state modification (`terraform state` subcommands, `import` into a shared backend), or any action touching production, shared, or billing-relevant accounts.
- **Stop** if the plan after import shows destroy or replace actions. Do not apply to clear them. Investigate the attribute mismatch first.
- **Stop** if the import ID format cannot be verified against provider documentation.
- **Proceed** with plan-only tests on any account without approval.
- **Escalate** if a resource contains sensitive attributes (keys, passwords, tokens) that would be written to state or plan output.

## Verification and evidence

Record the following before reporting success:
- `terraform test` output showing pass count equal to the number of `run` blocks, and zero failures.
- For each import: a plan with zero changes for that address, captured in a file.
- Confirmation that every validation rule has at least one failing-input test.
- State list output showing each imported address exists exactly once.
- Pinned versions of Terraform and the provider.

Do not claim coverage percentages or security compliance from these tests. They verify only what the assertions state.

## Failure handling

- **Assertion fails:** Determine whether the code or the expectation is wrong by reading the module logic. Fix the wrong side, then rerun. Do not weaken assertions to pass.
- **Import plan shows drift:** Compare the live attribute with the configuration. Update the configuration to match reality unless the drift is a defect to remediate, which requires approval.
- **Import ID rejected:** Re-check provider docs for the exact format. Do not try multiple IDs against live resources.
- **Partial import:** Use state inspection to identify what was recorded. Do not re-import blindly; that can duplicate or conflict.

## Deliverable contract

Return:
1. Changed files list with paths.
2. Test file contents or diff, plus the exact `terraform test` result.
3. Import table: address, provider ID format source, plan result.
4. Open items requiring approval, listed separately.
5. Tool versions used, with a note that version-specific syntax was checked against official docs for those versions.

Do not include credentials, account identifiers beyond what is necessary, or unredacted state contents in deliverables.