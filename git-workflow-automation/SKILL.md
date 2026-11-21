---
name: git-workflow-automation
description: Use when designing, auditing, or scripting Git branching, commit, rebase, tagging, hook, or CI-triggered repository workflows that must stay safe for shared history and team review.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Git Workflow Automation

## Purpose and boundaries

This skill covers automating repeatable Git operations: branch creation and naming, commit message validation, pre-commit and pre-push hooks, scripted rebases onto a base branch, release tagging, changelog extraction from history, and status reporting for CI. It applies to local scripts, hook configurations, and repository-hosted pipeline steps that call Git.

It does not cover: hosting-platform administration (branch protection rules, access control, webhook setup), history rewriting of published branches, repository migration or history filtering across repositories, or cryptographic signing key management. Those require a separate review and explicit owner approval.

## Inputs and assumptions

Before writing automation, confirm:

- Git client version on target machines and runners. Command behavior and config keys differ across versions; verify flags and config options against current official Git documentation for that exact version.
- Branching model in use (trunk-based, release branches, or feature branches off a development branch) and the protected base branch name.
- Whether commits in scope have already been pushed to a shared remote.
- Commit message convention, if any, and whether it is enforced by a tool already present in the repository.
- Runner environment: whether the job has write credentials, whether the checkout is shallow, and whether submodules or LFS objects are involved.

If any assumption is unknown, stop and request it. Do not guess branch names, remote names, or convention rules.

## Operating workflow

1. Identify the operation class: read-only (status, log, diff, describe), local-mutating (commit, branch, rebase on unpushed commits), or remote-mutating (push, tag push, delete remote branch).
2. Run read-only inspection first: `git status --porcelain`, the current branch, the upstream tracking ref, and ahead/behind counts against the base branch. Record outputs as evidence.
3. For local-mutating steps, create a backup ref or branch before rewriting anything (for example, a timestamped `backup/` branch) and log its object name.
4. Prefer `--ff-only` merges for synchronization and explicit `--force-with-lease` only when a rewrite of an unshared branch has been approved. Never use bare `--force`.
5. Validate commit messages with a script that checks subject length, imperative mood heuristics only if the team has adopted them, and ticket reference format. Reject rather than auto-correct.
6. Generate tags and changelogs from commit ranges with an explicit `base..head` range. Never derive a release range from "latest" without printing the resolved SHAs.
7. Emit a structured log of every command executed, its exit code, and resolved object IDs.

## Decision gates

Do not advance a repository change without maintainer approval when any of these conditions is present:

- The action deletes a branch, tag, or file, or runs `git clean`, `git reset --hard`, or `git gc --prune=now`.
- The action pushes to, force-updates, or deletes any remote ref, including tags.
- The action rewrites commits reachable from a remote-tracked branch.
- The action changes hooks, `.gitattributes`, or repository configuration committed for all contributors.
- The action touches commits containing credentials, personal data, or license-restricted material, or any history-filtering operation.
- The action would run in a CI job holding deploy or publish credentials.
- Working tree state is dirty and the script would proceed without stashing or refusing.

Proceed without approval only for read-only commands and local, non-destructive commits on a newly created feature branch.

## Verification and evidence

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

## Failure handling

- Non-zero exit from any mutating command: stop, do not retry automatically, restore from the recorded backup ref only after confirming the cause.
- Rebase conflict: abort with `git rebase --abort`, report conflicting paths, and hand resolution to a human. Do not auto-resolve by choosing "ours" or "theirs".
- Rejected push (non-fast-forward): do not force. Fetch, inspect divergence, and report.
- Missing or unreadable remote: report the remote URL with credentials redacted; do not attempt alternative endpoints.
- Lock file present (`index.lock`): verify no Git process is running before any removal, and require approval to delete it.
- Hook failure in CI: fail the job; do not add bypass flags such as `--no-verify` to make it pass.

## Deliverable contract

The deliverable is a single bundle containing:

1. The script or configuration, with a header stating required Git version (marked for verification against official documentation) and required inputs.
2. A dry-run mode that prints intended commands and resolved SHAs without mutating state.
3. An execution log in structured form (JSON lines preferred) with timestamps, commands, exit codes, and object IDs.
4. A short operator note listing approval gates encountered and which were granted, by whom, and when.
5. A list of unverified version-sensitive items that the operator must confirm against current Git documentation before production use.

Do not deliver scripts that cannot be dry-run, that print secrets, or that silently skip failed checks.