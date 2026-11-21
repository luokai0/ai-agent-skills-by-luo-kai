---
name: version-control-delivery
description: Use when preparing, reviewing, or shipping code changes through Git branches, commits, tags, pull or merge requests, and release refs, including history cleanup, conflict resolution, and safe rollback planning.
author: Luo Kai
provenance: original
version: 1.1.1
---

# Version Control Delivery

## Purpose and boundaries

This skill covers getting a change from a local working tree to a reviewable, verifiable, and traceable state in a shared repository: branch strategy, commit structure, history hygiene, integration, tagging, and rollback planning.

In scope: Git-based workflows, commit message quality, rebasing private branches, resolving merge conflicts, preparing pull or merge requests, release tagging, cherry-picks and reverts, and recovering from mistaken local operations.

Out of scope: CI pipeline design, deployment infrastructure, code authoring beyond what a conflict requires, and repository administration (branch protection rules, permissions, hosting settings).

## Inputs and assumptions

Before acting, establish:

- The target branch and its protection policy (required reviews, linear history, signed commits).
- Whether the working branch is private to you or shared with others. Rewriting shared history is a gated action.
- The change's intent in one sentence, and the issue or ticket it serves.
- The release line, if the change is a fix to a supported older version.
- Repository state: run read-only inspection first (status, current branch, upstream, recent log, stash list).

Assume nothing about remote names, default branch names, or hooks. Confirm them from the repository. Tool flags and hosting-platform features change; verify any non-trivial command syntax against the current official Git and hosting-provider documentation before use.

## Operating workflow

1. **Inspect.** Record branch, upstream, `HEAD` position, uncommitted changes, untracked files, and any in-progress rebase, merge, or cherry-pick. If an operation is in progress, resolve or abort it deliberately before starting new work.
2. **Isolate.** Confirm changes belong to one logical purpose. Split unrelated edits into separate branches or commits. Stage with explicit paths or interactive hunk selection, never a blanket add of unreviewed files.
3. **Commit by intent.** Each commit should compile and pass the project's relevant tests on its own, where practical. Write a subject line in the imperative mood, under roughly 72 characters, followed by a body explaining why the change exists and any non-obvious tradeoff.
4. **Synchronize.** Update from the target branch using rebase for private branches or merge when the policy or shared history requires it. Resolve conflicts by understanding both sides' intent, then re-run tests. Never resolve by blindly choosing one side.
5. **Clean history.** Squash fixups, reword unclear messages, and remove debugging artifacts, only on private branches and only after the Decision gates below.
6. **Publish.** Push the branch with an explicit remote and refspec. Open the review request with a description containing: purpose, change summary, test evidence, risk, rollback approach, and linked issue.
7. **Integrate and tag.** After approval, integrate using the policy-mandated method. Tag releases with annotated tags on the exact merged commit. Verify the tag points where intended before pushing it.

## Decision gates

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

## Verification and evidence

Quality checks, each required before publishing:

- `git diff --check` reports no whitespace errors.
- Every commit in the range builds and passes the relevant test subset, or the exception is stated in the review request.
- Commit count and scope match the stated intent; no unrelated files appear in `git diff --stat <target>...HEAD`.
- No conflict markers remain (search for `<<<<<<<`, `=======`, `>>>>>>>`).
- Author and committer identity match the expected user.
- After any rewrite, the patch-equivalence check (comparing `git range-diff` output against the pre-rewrite range) shows only intended changes.
- Tags: the tagged commit is an ancestor of the release line, and the tag is annotated.

Record the actual commands run and their results in the review request. Do not claim tests passed unless they were executed in this session.

## Failure handling

- **Push rejected (non-fast-forward):** Fetch and inspect the remote commits. Do not force. Ask the user whether to integrate or rewrite.
- **Conflict during rebase:** Resolve per file, `git add` the resolved file, continue. If the resolution is unclear, abort to the backup ref and report the conflict.
- **Wrong commit or branch pushed:** Stop. Report the exact commit hash and remote state. Revert propose options; do not rewrite shared history without approval.
- **Lost commits:** Check the reflog for the prior `HEAD` and recover into a new branch before any cleanup.
- **Hook or signing failure:** Do not bypass hooks or signature requirements. Report the message and ask for direction.
- **Uncertain command behavior:** Stop, verify against current official documentation, and only then proceed.

## Deliverable contract

Every delivery returns:

1. Branch name, base commit, and head commit hash.
2. Ordered list of commits with hashes and subjects.
3. Summary of changed paths and any excluded files, with reasons.
4. Verification record: commands run, outcomes, and any unverified items.
5. Risk statement and rollback plan (for example: revert commit hash, or tag to restore).
6. Pending approvals: each gated action not yet performed, listed explicitly.

Do not perform the publish, merge, or tag step without the approvals required by the Decision gates.

## Ultron routing contract

**Choose this skill when:** an agent must perform or guide a concrete Git workflow in a repository: inspect state, isolate changes, prepare commits, synchronize branches, resolve conflicts, prepare review, recover work, or plan a release ref transition.

**Delegate to `git-workflow-automation` when:** the user wants a reusable script, hook, bot, or CI step that will perform the same Git operation repeatedly across runs or repositories.

**Handoff contract:** provide the approved workflow, repository policy, permitted refs, exact path scope, dirty-state behavior, recovery point, and expected outputs. The automation skill must implement refusal behavior for unapproved destructive or remote-mutating operations and return a testable execution log.

**Why the boundary exists:** a safe one-time operation should not automatically become a general-purpose automation, and an automation request should not be answered with a fragile sequence of manual commands.
