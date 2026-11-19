<!-- Copyright (c) 2026 Luo Kai. All rights reserved for original work. -->
# Windows Skill Quality Standard — v1.1

This standard defines the quality bar for the 1,200 Windows computer-operation skills. “150 times more useful” is treated as a demand for a major practical improvement, not a word-count multiplier. More text without better decisions is not quality.

## Required skill behavior

Every skill preserves its original objective, stable ID, native tools, and domain-specific instructions, and includes an **Agent execution contract — v1.1**. That contract binds the agent to the exact domain and task; identifies the target device, user session, application, and object; establishes a read-only baseline; classifies risk; gives task-specific control points; states when explicit approval is required; defines independent success evidence; and describes stop/recovery and handoff behavior.

## Execution rules

- Prefer native Windows UI and accessibility names for GUI operations; use PowerShell for bounded inspection and repeatable checks.
- Verify optional commands and modules exist before use. Do not assume administrator rights, edition features, or policy access.
- Preserve unsaved work, user sessions, and data. Never bypass UAC, sign-in, MFA, CAPTCHA, consent, or organization policy.
- Require approval for create, rename, move, copy-overwrite, remove, restore, configuration changes, automation execution, cleanup, and other consequential changes.
- Use reversible operations where available. Never use permanent deletion, broad wildcards, hidden persistence, untrusted remote scripts, or opaque elevated commands.
- Verify outcomes independently and report only minimum necessary, redacted evidence.

## Acceptance checklist

1. YAML frontmatter parses and the original `windows-####` ID is unchanged.
2. The task objective and domain scope remain intact.
3. The v1.1 execution contract names the exact task and domain.
4. Read-only diagnostics are distinguished from state-changing actions.
5. Approval gates, success criteria, stop conditions, recovery, and privacy controls are explicit.
6. No credentials, personal data, malware, hidden network calls, or policy-bypass instructions are introduced.
7. Windows 10/11 differences and optional-tool availability are handled without assuming one build.

Original instructional material is authored for Luo Kai. Microsoft and third-party names are descriptive references; their owners retain their respective rights.
