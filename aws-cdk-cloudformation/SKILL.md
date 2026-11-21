---
name: aws-cdk-cloudformation
description: Use when authoring, reviewing, synthesizing, diffing, or deploying AWS infrastructure defined with the AWS Cloud Development Kit (CDK) or raw CloudFormation templates, including stack design, construct choices, change set review, drift handling, and rollback planning.
author: Luo Kai
provenance: original
version: 1.0.0
---

# AWS CDK and CloudFormation

## Purpose and boundaries

This skill covers infrastructure-as-code work on AWS using CDK (TypeScript, Python, or other supported languages) that synthesizes to CloudFormation, and hand-written CloudFormation templates (YAML or JSON). It covers stack structure, resource configuration, change review, deployment sequencing, drift investigation, and rollback.

It does not cover application code inside Lambda functions, runtime container images, non-AWS clouds, Terraform, or account-level governance such as AWS Organizations policy design. Route those to the appropriate skill.

## Inputs and assumptions

Collect these before acting:

- Target account ID, region, and environment label (dev, staging, prod). Never assume the account from ambient credentials alone; confirm it appears in the synth or deploy output.
- CDK app entry point and language, or the template path.
- Current deployed state: stack names, last successful deploy time, and whether a change set or drift report exists.
- Ownership: who approves production changes and which stacks hold stateful resources (databases, buckets, KMS keys, log groups with retention requirements).
- Toolchain versions. CDK CLI, construct library, and CloudFormation resource type versions change; treat any specific property name, default, or limit as **version-sensitive: verify against current AWS documentation** before relying on it.

If stateful resources or production targets are involved and ownership is unclear, stop and ask.

## Operating workflow

1. **Establish the target.** Confirm account, region, and stack names. Print the caller identity the tooling resolves and compare it with the intended account.
2. **Synthesize.** Run synthesis to produce the CloudFormation template. Save the output. Do not edit generated templates by hand; change the source.
3. **Lint the template.** Run a static checker (for example cfn-lint or the CDK-native rule set) and record findings. Fail the workflow on new errors; triage warnings explicitly.
4. **Review resource-level impact.** Identify every resource with `Replacement` or `Delete` behavior in the diff. Replacement of a stateful resource is a blocking finding.
5. **Generate a change set.** Create a change set rather than deploying directly. Review added, modified, removed, and replaced resources.
6. **Check IAM changes separately.** Any new or broadened IAM role, policy, or resource-based policy is reviewed line by line.
7. **Obtain approval** (see decision gates), then execute the change set.
8. **Verify post-deploy** (see verification section) and record outputs.
9. **Detect drift** on a schedule or after incidents: compare live state to template and classify each difference before remediating.

## Decision gates

For infrastructure changes, halt for human sign-off whenever any of the following conditions apply:

- The change set contains any Replacement or Delete on a stateful resource: databases, S3 buckets, DynamoDB tables, KMS keys, EFS file systems, log groups holding data needed for audit.
- The change modifies IAM permissions, resource policies, security group ingress rules, or public access settings.
- The target is production, or the account is shared across environments.
- The change alters DNS records, certificates, load balancer listeners, or anything that affects external traffic.
- A stack update requires disabling termination protection, deletion protection, or retention policies.
- Drift shows manual changes you cannot attribute to a known owner.
- Any action would delete a stack or empty a bucket.

Proceed without a gate only for additive, non-stateful, non-IAM changes in non-production environments that the diff confirms.

## Verification and evidence

Record evidence at each stage:

- Synthesis: template hash and size, count of resources by type.
- Lint: tool version, rule set, zero new errors.
- Change set: exported JSON or console summary showing exact action per resource. Expected action counts must match what the author predicted in the change description; any mismatch blocks execution.
- Post-deploy: stack status is a completed-success state; stack outputs match expected values; a health check or smoke test against the changed resource passes.
- Drift: detection status per stack, list of drifted resource IDs with property-level differences.

A deployment without a reviewed change set, or without a post-deploy check, is incomplete.

## Failure handling

- **Stack update fails and rolls back:** read the first failed event, not the last. Fix the root cause in source, re-synthesize, and generate a new change set. Do not force-continue rollback on a stack you have not diagnosed.
- **Stack stuck in an UPDATE_ROLLBACK_FAILED or similar state:** stop. Identify the blocking resource. Recovery options that skip resources or retain them can orphan infrastructure; they require approval and a written rollback note.
- **Resource creation fails due to quota or name collision:** do not rename or delete existing resources to make room without approval.
- **Lint or synth error:** fix the source. Do not suppress rules to pass the pipeline without a documented, scoped justification.
- **Drift found:** do not auto-revert. Determine whether the manual change was intentional, then either codify it in source or revert it through a reviewed change set.

## Deliverable contract

Every completed task returns:

1. Target: account, region, stack names, environment.
2. Change summary: resource-level actions (create, update, replace, delete) with counts.
3. Risk list: each gated item and its approval status.
4. Evidence: synthesis hash, lint result, change set reference, post-deploy check results.
5. Rollback plan: the specific previous template version or commit and the expected rollback behavior for stateful resources.
6. Open items: anything version-sensitive that was not verified against current documentation.

## What not to do

- Do not deploy directly from a local working tree with uncommitted changes.
- Do not hand-edit synthesized templates or live stacks through the console to "fix" them.
- Do not use retain or skip options on failed deletes as a shortcut without approval.
- Do not hardcode account IDs, secrets, or credentials in source; use parameters or secure references.
- Do not state a resource property, default, or quota as fact without checking current documentation.
- Do not disable rollback or termination protection to get a change through.
- Do not treat a successful deploy as proof of correctness; verify the behavior.