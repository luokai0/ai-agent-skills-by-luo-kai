---
name: agents-md-and-ai-instructions
description: Use when creating, reviewing, or updating AGENTS.md or similar repository-level instruction files that guide AI coding agents on build, test, style, and safety conventions for a codebase.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Agents Md And Ai Instructions

## Purpose and boundaries

This skill covers writing instruction files that AI coding agents read before working in a repository. These files tell an agent how to build, test, lint, navigate, and change the code safely. It does not cover prompt engineering for end-user chat products, model training, or policy documents for organizational AI use. Treat the instruction file as versioned engineering documentation: it must be accurate, short enough to be followed, and verifiable against the repository.

## Inputs and assumptions

Gather before drafting:

- The repository's actual build, test, lint, and format commands, read from manifests and CI configuration, not from memory.
- Language and framework versions, and where they are pinned.
- Directory ownership, generated-code locations, and vendored code that must not be edited.
- Existing instruction files (AGENTS.md, tool-specific equivalents, contributing guides). Note conflicts.
- Which agent tools the team uses. File names and precedence rules are tool-specific and version-sensitive; verify against each tool's current official documentation before relying on them.

If any command cannot be confirmed by running it or reading CI, mark it unverified rather than stating it as fact.

## Operating workflow

1. Inventory: list manifests, CI jobs, Makefile or task-runner targets, and existing docs.
2. Extract commands: record each verified command with its working directory and expected runtime.
3. Map boundaries: identify generated files, protected branches, migration directories, and secrets locations.
4. Draft in this order: setup, build, test, lint/format, code layout, conventions, boundaries, pull request expectations.
5. Keep each rule imperative and checkable ("Run `<verified command>` before committing"), not aspirational ("Write clean code").
6. Cut anything an agent would ignore or that duplicates a linter's job. Linters enforce style; the file should point to them.
7. Verify every command by running it in a clean checkout, or record why it could not be run.

## Decision gates

- Include a rule only if it changes agent behavior in this repository. Generic advice is removed.
- Put a fact in the file only if it is verifiable from the repo. Otherwise, omit it or flag it.
- Nested files are justified only when a subdirectory has materially different toolchains or rules. Otherwise, keep one root file.
- Require explicit human approval before the agent-facing file grants permissions, such as allowing deletion, force-pushes, dependency upgrades, or network calls to external services. Instructions that loosen safety controls are a sensitive change.
- Do not write secrets, tokens, internal hostnames, or customer data into the file.

## Verification and evidence

- Run every documented command from a clean state; record the exit code and approximate duration.
- Confirm each referenced path exists (`ls` or equivalent) and each named test target exists in the build configuration.
- Check that the file does not contradict CI configuration or contributing guides.
- Ask a teammate unfamiliar with the repo to perform one small task using only the file; note every point where they had to guess.
- Re-verify after any toolchain upgrade.

## Failure handling

- Command fails: record the exact error, the environment, and whether the failure is in documentation or in the repo. Fix the documentation if the command is wrong; report the repo issue separately if it is broken.
- Conflicting sources: CI configuration is the source of truth for commands. Flag the conflict for the owning team rather than silently choosing.
- Unknown tool behavior (precedence, supported file names, size limits): state the uncertainty and point to current official documentation; do not guess.
- Scope creep: if the requested file would encode policy or permissions the author cannot approve, stop and escalate.

## Deliverable contract

The deliverable is one or more Markdown instruction files plus a short verification note containing:

- The list of commands verified, with exit status.
- Items marked unverified, with reasons.
- Open questions requiring owner decisions.
- The date of verification and the toolchain versions used.

Good output looks like: a root file of roughly one to three screens, each command in a code block with its working directory, explicit "do not edit" paths, and a pre-commit checklist that maps to real CI jobs. Poor output looks like: restated language documentation, unverified commands, invented flags, and vague directives such as "follow best practices."

Do not invent API names, flags, package versions, benchmark figures, or compliance claims. Do not quote or reproduce other projects' instruction files. Write each file from this repository's own facts.