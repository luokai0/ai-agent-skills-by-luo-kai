# PinkPixel Skills Collection notice

Source: https://github.com/pinkpixel-dev/skills-collection-1
Upstream license: Apache License 2.0
Upstream LICENSE addition: commit ddcadf5896a9cce6f79e296d8b070e5224690e6e, dated 2026-08-09
Imported snapshot revision: not recorded in this repository

The upstream repository's Apache-2.0 license is preserved in this directory. The imported snapshot's exact upstream commit is unknown, and individual files may carry separate notices or rights. Preserve all per-file attribution and license notices. This collection is not claimed as original work by Luo Kai.

## Modifications by Luo Kai

On 2026-11-19, the following files were adapted while retaining the upstream Apache-2.0 terms and original author attribution:

- conducting-memory-forensics-with-volatility/scripts/agent.py: added input and plugin validation, bounded subprocess execution, explicit no-shell invocation, timeout and process-start error handling, UTC timestamps, and protection against overwriting the evidence image.
- conducting-memory-forensics-with-volatility/SKILL.md: clarified authorized scope, evidence preservation, sensitive credential handling, safe helper usage, and limitations.
- hunting-for-scheduled-task-persistence/scripts/agent.py: added command failure handling, CSV schema validation, task-name validation, bounded read-only execution, and explicit collection-mode reporting.
- hunting-for-scheduled-task-persistence/SKILL.md: clarified authorized read-only scope, sensitive output handling, and validation steps.

These changes are modifications, not a claim of exclusive ownership over the original upstream work. The upstream copyright and license remain in force.
