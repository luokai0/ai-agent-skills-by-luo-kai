# Documents and Productivity

This reference module is part of the single **Ultron Ultimate Skill**. Load only the chapter needed for the current task. The parent `SKILL.md` governs routing, authority, planning, execution, verification, and delivery.

## document-authoring-publishing

**Use when:** Use when preparing documentation, README files, changelogs, model or dataset cards, or package metadata for release to an external registry or documentation host, including checking that published text matches the artifact version and passes registry rules.

### Purpose and boundaries

This skill covers writing user-facing documentation and metadata for an artifact, then publishing that text to an external registry or documentation host (package indexes, container or model hubs, documentation sites, artifact repositories). It covers the document set, its version alignment, and the publish readiness check.

Out of scope: writing the software itself, designing registry infrastructure, and changing organization-wide publishing policy. Do not use this skill to publish anything without the approval gate below.

### Inputs and assumptions

Before writing, confirm:

- Artifact name, version, and the exact registry or host target.
- Target audience (end users, integrators, maintainers, auditors).
- Existing documents and their owners.
- Licensing and sensitivity status supplied by the owner. Do not infer these.
- Whether the registry is public, private, or mirrored. Mirrors often cache metadata and cannot be fully retracted.

Assume nothing about registry metadata rules, field limits, rendering engines, or accepted file formats. Check the current official documentation for each target and record the URL and date consulted. Treat any field name, size limit, or syntax from memory as unverified.

### Operating workflow

1. **Freeze the version.** Record the exact version string that will be published. Every version reference in the documents must match it.
2. **Inventory existing text.** List every README, changelog, example, badge, install command, and metadata field. Mark each as current, stale, or unknown.
3. **Draft in layers.** Write in this order: one-paragraph summary, install or access steps, minimal working example, configuration reference, limitations, changelog entry, contact and support path.
4. **Make examples executable.** Every command or code sample must run against the frozen version in a clean environment. Record the environment used.
5. **Translate to registry fields.** Map each piece to the target's metadata fields. Note any field that is truncated, rendered differently, or unsupported.
6. **Run the verification checklist** (below).
7. **Prepare a publish package** containing the final text, a diff against the previous published version, and the verification evidence.
8. **Request approval** (see Decision gates) before any publish, overwrite, deletion, or visibility change.

### Decision gates

Stop and obtain explicit owner approval before:

- Publishing a new version, or any version to a public or shared registry.
- Overwriting, editing, or replacing an already published document or version page.
- Yanking, deprecating, deleting, or changing visibility of any release.
- Adding a license, copyright notice, or attribution claim that the owner did not supply.
- Including contact details, internal hostnames, customer names, credentials, or unreleased feature names.
- Publishing a model or dataset card that describes evaluation results, safety properties, or data provenance without supporting records.

If an action is irreversible or mirrors externally, state that explicitly in the approval request.

### Verification and evidence

Pass all of the following before requesting approval:

- Version strings in all documents equal the frozen version (zero mismatches across grep-style search of the package).
- Every command or code block was executed and the result recorded.
- All links resolve; relative links work from the published location.
- Metadata fields are within the target's current documented limits; cite the source checked.
- No unresolved sample text or unfinished sections, or unresolved status markers remain.
- No secrets or credentials appear in examples (scan for token-like strings and private hostnames).
- Changelog entry lists user-visible changes only and matches the diff.
- Benchmarks or quantitative claims include the method, environment, and date, or are removed.

Record results as a table: check, method, result, evidence location.

### Failure handling

- **Version mismatch found:** fix in the source, re-freeze if the version itself was wrong, and rerun all checks. Do not patch only the published copy.
- **Example fails:** correct the example or the documented prerequisites. Do not hide the failing step.
- **Registry rejects metadata:** shorten or restructure the field without changing meaning, then recheck limits against current documentation. Report any content lost.
- **Publish already occurred with an error:** stop, report the exact state, and ask for approval on the corrective action (edit, deprecate, or yank). Do not take corrective action unilaterally.
- **Documentation source is ambiguous:** ask the owner rather than inferring behavior.

### Deliverable contract

Return to the requester:

1. Final document set, one file per document, with the frozen version stated at the top of the changelog entry.
2. Registry field mapping with any truncations or omissions listed.
3. Diff against the last published version.
4. Verification table with evidence locations.
5. A list of documentation sources consulted, with dates.
6. A pending-approval section listing each gated action, its reversibility, and its external impact.

Do not state that the artifact is compliant, secure, or certified. Describe only what was checked and how.

### Ultron routing contract

**Choose this skill when:** producing version-aligned documentation or metadata for an artifact and preparing or performing its approved publication to a registry, documentation host, package index, container/model hub, or artifact repository.

**Choose technical-documentation-ops when:** the work is the broader lifecycle of technical documentation: deciding what documentation is needed, maintaining runbooks/ADRs/API guides, validating content against a running system, and keeping documents current.

**Handoff contract:** the documentation-ops skill supplies verified source content, version identity, review status, and internal publication policy. This skill packages the external-facing document set with the artifact version, checks registry/host-specific publication requirements, obtains the required approval, and verifies the published result.

**Why the boundary exists:** maintaining trustworthy documentation and publishing documentation alongside an artifact have different release and external-impact controls.


## google-workspace-media-and-files

**Use when:** Use when handling images, video, audio, PDFs, Docs, Sheets, Slides, or Drive files stored in or exchanged through Google Workspace, especially for organizing, converting, extracting, auditing, or migrating media and file assets.

### Purpose and boundaries

This skill governs work on file-level assets in Google Drive and the media embedded in or attached to Docs, Sheets, and Slides: inventory, naming, format conversion, extraction of embedded media, deduplication, permission-aware sharing review, and migration staging. It does not cover drafting document content, building spreadsheet models, or designing slide narratives. Hand those to the relevant content skill.

Treat every file operation as one of three classes: read-only (listing, metadata, export to a scratch location), reversible (rename, move within a shared drive, add a label), or destructive/external (delete, trash, overwrite, change sharing, publish, bulk export outside the organization). Only the first two may proceed on your own judgment; the third requires explicit user approval per action batch.

### Inputs and assumptions

Before acting, establish:

- Scope: the folder, shared drive, or file IDs in question. Do not infer scope from file names alone.
- Target outcome: inventory, conversion, extraction, cleanup, or migration.
- Access: which account is in use and whether it has read, edit, or manager rights on the scope. Note any files owned by other users.
- Constraints: retention obligations, confidentiality labels, deadlines, and whether originals must be preserved.
- Tooling: the exact connector or API surface available. Google Drive, Docs, Sheets, and Slides interfaces and export formats change. Verify method names, parameters, supported MIME types, and quota limits against current official Google Workspace documentation before relying on them.

Assume originals must be preserved unless the user states otherwise. Assume sharing settings are in force and must not be widened.

### Operating workflow

1. Inventory. List items in scope with ID, name, MIME type, size, owner, last modified, parent path, and sharing status. Record counts by type. Save the inventory as a reference artifact before any change.
2. Classify. Tag each item: native Google format (Docs, Sheets, Slides), uploaded binary (PDF, image, video, audio, Office file), shortcut, or folder. Native formats require export; binaries may be downloaded directly.
3. Plan. Write a numbered change plan listing each operation, its class (read, reversible, destructive/external), item count, and expected output location.
4. Gate. Submit the plan for approval where required (see Decision gates).
5. Execute in batches of no more than 50 items, logging each item ID and result.
6. Verify each batch against the verification checklist before starting the next.
7. Produce the deliverable contract output.

For conversion: export to a new folder, never overwrite the source. Record source ID, output ID, format, and page or slide count. For PDF extraction of images, keep original resolution and note any lossy re-encoding.

For embedded media in Docs and Slides: extract by exporting or inspecting the document structure; do not re-save the document, because re-saving can alter layout, comments, and revision history.

### Decision gates

Stop and request approval when any of these hold:

- Any delete, trash, empty-trash, overwrite, or move out of a shared drive.
- Any change to sharing, link visibility, or ownership transfer.
- Any export or copy to a location outside the organization or to a personal account.
- Any operation affecting more than 50 items or more than 1 GB of data.
- Files flagged as confidential, legal hold, HR, financial, health, or credential-bearing (inspect filenames and content headers; do not open content beyond what the task needs).
- Format conversion that discards information: Sheets to CSV (drops formulas, formatting, multiple tabs), Slides to PDF with speaker notes omitted, video transcoding.

Proceed without approval only for read-only operations and reversible renames or label additions within the approved scope.

### Verification and evidence

Each batch must pass:

- Count match: items out equals items in, minus documented skips. Record skips with reasons.
- Checksum or size match for binary copies where the platform exposes one; otherwise compare size and page or slide count.
- Page and slide counts match for document exports; sheet count and row totals match for spreadsheet exports.
- Spot-check at least 5 percent of converted items, minimum 3, by opening the output and comparing against source.
- Permissions unchanged on source items after operations: record before and after sharing state.
- Naming conforms to the agreed convention with no collisions and no characters that break the target system.

Report evidence as counts and IDs, not assertions. Say "42 of 42 PDFs exported, 2 skipped (permission denied: IDs listed)" rather than "export complete."

### Failure handling

- Permission error: do not escalate access or attempt workarounds. Record the item ID and owner, and report it.
- Quota or rate limit: pause, back off, resume from the last logged ID. Do not restart the batch and risk duplicates.
- Unsupported export format: choose the nearest supported format, label the output as a substitute, and flag it for approval.
- Partial batch failure: retry only failed IDs once; escalate if still failing.
- Duplicate outputs detected: do not delete. Report the duplicates and wait for approval.
- Any unexpected deletion or sharing change: stop all operations immediately and report with the affected IDs.

### Deliverable contract

Return:

1. Scope summary: folder or IDs, item counts by type, and owner distribution.
2. Executed operations: class, count, and output location for each.
3. Verification results: pass or fail per check, with evidence counts and IDs.
4. Exceptions: skipped, failed, or substituted items, each with reason and recommended next action.
5. Pending approvals: a numbered list of gated operations awaiting sign-off.
6. Change log: the inventory and operation log saved as a file or attached artifact.

Do not state that migration is complete, that data is fully preserved, or that compliance requirements are met unless the verification evidence explicitly supports each claim. Scope the claim to what was checked.


## item-lifecycle-and-recovery

**Use when:** Use when a Windows user or administrator must trace, retain, restore, or recover deleted, overwritten, moved, or misplaced files and folders, or must define how items move through create, modify, archive, delete, and purge stages on a Windows machine or user profile.

### Purpose and boundaries

This skill covers the lifecycle of user files and folders on Windows endpoints and user profiles: where items live, how they are removed or overwritten, what recovery paths exist, and how to restore them with evidence. It applies to local NTFS volumes, user profiles, and OneDrive or network shares as they affect a local item.

It does not cover: forensic imaging for legal matters, ransomware incident response beyond restoring affected items, server-side mailbox or database recovery, or changing retention policy for an organization. Those require a different owner.

### Inputs and assumptions

Collect before acting:

- Item path, name pattern, and approximate time of loss or change.
- Last known state: created, edited, moved, renamed, or deleted.
- Storage location: local fixed disk, removable media, OneDrive folder, mapped share.
- Available recovery sources: Recycle Bin, File History, Windows Backup or image backups, Previous Versions (shadow copies), application autosave or version history, cloud recycle bins.
- Whether the volume has been written to since the event. Every write reduces recovery odds.
- Authority to restore: owner of the data, and whether the restore overwrites current data.

Assume nothing about which recovery features are enabled. Verify each one.

### Operating workflow

1. Freeze writes. Ask the user to stop saving to the affected volume or folder. If the loss is recent and on a system disk, recommend no further installs or large downloads.
2. Identify the lifecycle stage. Determine whether the item was deleted (sent to Recycle Bin or removed permanently), overwritten, moved, renamed, or corrupted.
3. Check sources in order of cost and fidelity:
   a. Recycle Bin: restore in place if the original path is intact. Check the original location for name conflicts first.
   b. Previous Versions: right-click the parent folder, open Properties, and review the Previous Versions tab. This depends on prior restore points or shadow copies existing. Confirm availability on the specific volume.
   c. File History or backup target: browse by date to the nearest point before the event. Restore to an alternate location first.
   d. Application version history, OneDrive version history, or cloud recycle bin: follow the provider's current documented steps, since interfaces change.
4. Restore to a staging folder, not the original path, unless the user has approved overwriting.
5. Compare the recovered item against the expected state (size, modified time, hash if a reference exists, opens without error).
6. Promote the verified item to its final location only after approval.
7. Record the event: source used, timestamps, paths, and any remaining gaps.

### Decision gates

- Gate A, stop and escalate: the loss involves encrypted volumes without available recovery keys, a suspected malware-driven change, or regulated or personal sensitive data outside the user's authority. Do not attempt bulk file scanning or third-party recovery tools without explicit approval.
- Gate B, approval required: any restore that overwrites existing data, any purge of Recycle Bin or shadow copies, any disk cleanup, any change to backup or File History settings, and any action that uploads data to external services.
- Gate C, choose the source: prefer the source with the smallest time gap to the event and the highest fidelity. A Previous Versions copy from the right hour beats a backup from last week. If two candidates conflict, restore both to separate staging folders and compare.
- Gate D, partial recovery: if only part of a folder tree is recoverable, report exact counts recovered versus expected and do not present the result as complete.

### Verification and evidence

- Name, path, and size match the expected item or the user confirms the version.
- Modified timestamp matches the chosen restore point.
- File opens in its native application without repair prompts.
- For folders: item count matches the source inventory where one exists. Record counts before and after.
- Keep a short log: source, restore point timestamp, staging path, final path, verifier, and outstanding items.
- Do not claim recovery is guaranteed or complete without these checks.

Mark version-sensitive behavior (menu labels, File History defaults, shadow copy schedules, OneDrive retention windows) as requiring verification against current Microsoft documentation before stating it to the user.

### Failure handling

- Recycle Bin item missing: check whether it was permanently deleted, emptied, or excluded by size settings. Move to the next source without retrying the same one.
- No Previous Versions entries: the volume may lack restore points or shadow copies. Do not create new ones to "force" recovery without approval, since that writes to the disk.
- Restored file is corrupt: retain the copy, try the next older restore point, and do not overwrite the original attempt.
- Backup restore fails midway: stop, keep the partial output, and report the error text and time.
- Recovery tool suggests bulk scanning: decline without approval. Scanning writes logs and increases the risk of overwriting unrecovered data.

### Deliverable contract

Provide:

1. Summary of the loss stage and the chosen recovery source with timestamp.
2. Ordered list of actions taken, with approvals obtained.
3. Verification results against each check above.
4. Final locations of recovered items, and staging copies retained.
5. Remaining gaps, the reason for each, and the next recommended source.
6. Any version-sensitive steps flagged for documentation verification.

Do not: restore over originals without approval, empty Recycle Bin or delete shadow copies as cleanup, run unverified third-party recovery software, promise full recovery, or store recovered sensitive data outside the approved location.


## manuscript-and-grant-writing

**Use when:** Use when drafting, restructuring, or reviewing research manuscripts, grant proposals, or technical reports in data science, machine learning, or AI, including claims, evidence tables, reproducibility and data statements, and funder or venue compliance checks.

### Purpose and boundaries

This skill produces and revises written research artifacts in data and AI: journal and conference papers, workshop papers, preprints, grant proposals, specific aims pages, project narratives, and technical reports. It covers structure, argument, claim-evidence alignment, figures and tables, reproducibility statements, and submission-readiness checks.

It does not cover fabricating results, writing text that misrepresents authorship or funding, drafting legal or ethics approvals on an institution's behalf, or predicting funding outcomes.

### Inputs and assumptions

Required inputs before drafting:
- Target venue or funder, and its current call, template, and page or word limits.
- The core contribution stated in one sentence, plus the experiments or analyses that support it.
- Result files, logs, or tables. Numbers are copied from source artifacts, never from memory.
- Dataset provenance, licenses, and any consent or privacy constraints.
- Author list, contribution roles, and funding sources, as provided by the user.

Assume the user is responsible for scientific claims. If inputs are missing, ask; do not fill gaps with plausible values.

### Operating workflow

1. **Pin the contribution.** Write a single claim sentence and a list of two to four supporting claims. Reject any claim the artifacts do not directly support.
2. **Build a claim-evidence map.** For each claim, list the figure, table, or section that supports it, the metric, the dataset split, and the number of runs or seeds. Flag claims with no evidence.
3. **Check the template.** Confirm the venue's current template, anonymization rules, page limit, and required sections. Mark these as version-sensitive and verify against the official call before finalizing.
4. **Draft in this order:** methods, results, introduction, related work, discussion, abstract. Introduction and abstract come last because they must match what the results show.
5. **Write the reproducibility and data statements.** Include data sources with versions or access dates, preprocessing steps, hyperparameter search ranges, compute description, random seeds, and code availability status.
6. **For grants,** map each aim to a measurable objective, a method, a timeline milestone, and a deliverable. Include data management, risk, and broader-impact or ethics sections as the funder requires.
7. **Revise for tone.** Replace superlatives and unhedged causal language with the strength the evidence supports.

### Decision gates

- **Claim gate:** Proceed only if every headline claim maps to at least one artifact. Otherwise, narrow the claim or request the missing experiment.
- **Statistics gate:** Report variance across seeds or folds. If only single runs exist, state this and avoid ranking methods by differences smaller than the observed spread.
- **Novelty gate:** Compare against the closest three to five prior works by name. If the contribution overlaps heavily, reframe around the actual difference.
- **Sensitive-data gate:** If the work uses personal, health, or restricted data, stop and request explicit approval from the user before including any sample, identifier, or quoted record.
- **Submission gate:** Do not declare a document ready until the template, limits, and anonymization are checked against the current official source.

### Verification and evidence

- Every number in the text matches its source artifact. Record the artifact path next to each table entry during drafting.
- Metric names, dataset versions, and baseline configurations are consistent across abstract, results, and tables.
- Figures have labeled axes, units, error bars or a stated uncertainty measure, and captions readable without the body text.
- Abbreviations are defined on first use. References resolve to real, retrievable publications; never generate citation entries from memory without a check.
- Word and page counts are measured on the final formatted document, not the draft.

### Failure handling

- **Missing result:** Insert a clearly marked gap in the draft listing the required experiment. Never estimate the number.
- **Conflicting numbers:** Stop, list the conflicting sources, and ask which is authoritative.
- **Template uncertainty:** State which version was assumed and ask the user to confirm.
- **Over-length draft:** Cut related-work detail first, then repetitive method description, never the limitations.

### Deliverable contract

Each deliverable includes:
1. The revised document in the requested format.
2. A claim-evidence table linking each claim to its artifact.
3. A list of open items: missing evidence, unverified template rules, and decisions requiring the author's approval.
4. A limitations paragraph suitable for the document itself.

Do not invent benchmark results, funding amounts, deadlines, compliance certifications, or software version numbers. Do not present unverified tool or policy details as current facts.


## preference-and-default-configuration

**Use when:** Use when changing Windows user preferences, default applications, file associations, environment variables, or shell profiles on a workstation or managed endpoint, and the change must be scoped, reversible, and verified.

### Purpose and boundaries

This skill covers changing user-level and machine-level Windows preferences: default apps and file associations, user environment variables, PowerShell profiles, display and input preferences, and similar settings. It produces a recorded, reversible change with evidence that the change took effect.

Out of scope: driver installation, OS feature enablement, domain policy authoring, security baseline changes, and anything that edits system files. Those require their own review path.

### Inputs and assumptions

Before acting, confirm:

- Target scope: current user only, or all users on the machine.
- Windows edition and build number (`winver` or Settings > System > About). Settings paths and registry layout vary by build; verify against current Microsoft documentation before relying on a specific path.
- Whether the device is managed by Intune, Group Policy, or another MDM. Managed settings may be reverted or locked.
- The exact desired value, the application or tool affected, and who requested it.
- Whether a backup of the current state is possible.

Assume nothing about the current value. Read it first.

### Operating workflow

1. **Capture current state.** Record the present value of every setting you will touch, with its location (registry key, environment scope, file path, or Settings page).
2. **Export a backup.** For registry keys, export the specific key to a dated `.reg` file. For environment variables, record the full before-value. For profiles, copy the file.
3. **Check for enforcement.** Look for policy keys under `HKLM\SOFTWARE\Policies` and `HKCU\SOFTWARE\Policies`, or MDM-managed indicators in Settings. If a policy controls the value, stop and report rather than overriding it.
4. **Choose the least-privileged mechanism.** Prefer the Settings UI or the supported application setting over direct registry edits. Use direct edits only when no supported path exists.
5. **Apply the single change.** Change one setting per step so failures are attributable.
6. **Verify** (see the verification section).
7. **Record the result** in the deliverable contract format.

Domain examples:

- Default browser or PDF viewer: use Settings > Apps > Default apps. Do not hand-edit the `UserChoice` registry values; Windows protects them with a hash, and manual edits are unreliable and may be reverted.
- User environment variable `EDITOR`: set at user scope, then open a new process to confirm it is inherited. Existing processes will not see the change.
- PowerShell profile: back up the file, append or edit only the target lines, and test by starting a new shell session with `-NoProfile` absent and confirming no errors.

### Decision gates

Stop and request explicit approval before:

- Deleting any registry key, value, file, or environment variable.
- Changing any setting at machine scope (`HKLM`, system environment variables) or for other users.
- Modifying a setting that is controlled by policy, MDM, or a corporate baseline.
- Any change that alters network, proxy, certificate, firewall, or credential behavior.
- Any change affecting remote systems, shared profiles, or settings synced to a cloud account.
- Any action that will require a restart or sign-out of a user session in use.

Proceed without further approval only when the change is user-scope, reversible from the backup, non-policy, and within the stated request.

### Verification and evidence

- Re-read the setting from its source location and compare to the intended value. Quote the observed value.
- For environment variables, start a new process and confirm the value is visible there.
- For default apps, open a file of the affected type and confirm the handler; record the application name shown.
- For profiles, confirm a new shell starts without error output.
- Confirm the backup file exists and is readable.

A change without a before-value, an after-value, and a confirming read is not complete.

### Failure handling

- If verification fails, restore from the backup immediately and re-verify the restored state.
- If a policy reverts the change, report the policy source; do not attempt to bypass it.
- If an export or backup fails, stop before making the change.
- If a restart is needed to confirm, state that explicitly and ask before restarting.
- Never retry a failing registry write in a loop or with escalated privileges without approval.

### Deliverable contract

Return:

1. Scope and mechanism used (Settings page, registry path, environment scope, or file).
2. Before-value and after-value for each setting.
3. Backup location and filename.
4. Verification performed and its observed result.
5. Any items requiring approval, unresolved policy controls, or build-specific paths still to be checked against current official documentation.

Do not state that a setting is "secure," "compliant," or "fixed" unless a verified check demonstrates it. Do not guess registry paths, cmdlet names, or flags; mark any unverified detail for confirmation.


## technical-documentation-ops

**Use when:** Use when creating, restructuring, auditing, or maintaining technical documentation for software systems, APIs, runbooks, architecture records, or developer onboarding, and when documentation must stay accurate against code, configuration, or operational reality.

### Purpose and boundaries

This skill governs the lifecycle of technical documentation: deciding what must be written, writing it against verifiable sources, validating that it matches the running system, and keeping it current. It covers API references, READMEs, setup and contributor guides, architecture decision records (ADRs), runbooks, incident postmortems, configuration references, and changelogs.

It does not cover marketing copy, end-user product manuals, legal or compliance documents, or authoring application code. If a request requires asserting security, compliance, or performance guarantees, stop and route that claim to the owning team.

### Inputs and assumptions

Before writing, collect:

- **Audience**: who reads this (new engineer, on-call responder, integrator, auditor) and what task they must complete.
- **Source of truth**: code, OpenAPI/schema files, config templates, infrastructure definitions, tests, or a named human expert. Documentation is derived from these, never the reverse.
- **Scope and version**: the exact system, service, or release the document describes.
- **Existing docs**: current content, its last-verified date, and known gaps.
- **Target location and format**: repo path, docs site generator, or wiki. Confirm the format's syntax against its current official documentation, since generator directives and front-matter keys are version-sensitive.

Assumptions must be written at the top of the draft under "Assumptions" with the reason. Unverified claims are labeled `UNVERIFIED`.

### Operating workflow

1. **Classify the document** by type (reference, how-to, explanation, runbook, decision record). Each type has one job. Do not mix a tutorial with a reference table.
2. **Build an evidence list.** Map every factual claim to a source: a file path, a command output, a test, or a stakeholder confirmation. Claims with no source are removed or marked `UNVERIFIED`.
3. **Outline by task**, not by code structure. Runbooks follow symptom → diagnosis → remediation. Setup guides follow prerequisite → install → configure → verify.
4. **Draft with concrete values.** Use real parameter names, real endpoints from the schema, and real example payloads that were executed or validated. Mark sample values explicitly as `SAMPLE` and state each one's meaning once.
5. **Run verification** (see below) before submitting.
6. **Record metadata**: owner, last-verified date, source commit or revision, and review cadence.

### Decision gates

- **Gate A: Source conflict.** If code and existing docs disagree, the code is authoritative for behavior; the owner is consulted for intent. Do not silently pick one.
- **Gate B: Undocumentable behavior.** If behavior is undefined, ambiguous, or appears to be a bug, document the observed behavior flagged as such and open a question to the owner. Do not document intent as fact.
- **Gate C: Sensitive content.** Before including hostnames, internal IPs, account identifiers, tokens, customer data, incident details naming individuals, or vulnerability specifics, require explicit approval from the document owner and the security or privacy contact. Never reproduce a live secret, even partially.
- **Gate D: Externally published docs.** Publishing to public sites, partner portals, or changing a shared API contract requires explicit approval from a named accountable person.
- **Gate E: Destructive edits.** Deleting or replacing published pages, redirects, or version archives requires explicit approval and a recorded rollback path (prior revision identifier).
- **Gate F: Compliance or guarantee language.** Statements about certification, uptime, SLAs, data residency, or regulatory status are out of scope unless the owning function supplies the approved wording.

### Verification and evidence

- **Command check**: every command in a how-to is executed in a clean environment matching the documented prerequisites; record the exit code and the key output line.
- **Example check**: every request/response example is replayed against the target version. Mismatched fields fail the check.
- **Link check**: all internal links resolve; all external links are checked for redirects and deprecation notices.
- **Name check**: every identifier (flag, key, environment variable, endpoint, function) appears in the source file it claims to come from. Use search, not memory.
- **Version check**: any tool version, package version, or generator directive is confirmed against current official documentation and labeled with the version it was verified against. Never state a version number from memory without this check.
- **Freshness check**: no doc is marked verified more than its review cadence allows (default 90 days for references, 30 days for runbooks).
- **Readability check**: a reviewer who did not write the document completes the task using only the document. Record the number of points where they needed to ask for help; target zero for runbooks.

Evidence is recorded in a short verification table in the pull request or ticket: check name, method, result, date.

### Failure handling

- If a command fails in verification, do not edit the doc to match the failure silently. Record the failure, determine whether the doc or the system is wrong, and fix the correct one.
- If a source cannot be found for a required claim, leave the section with `UNVERIFIED` and a named owner; do not fill it with plausible content.
- If a reviewer disputes accuracy and evidence is inconclusive, escalate to the system owner rather than resolving by majority opinion.
- If a runbook step has side effects (data deletion, traffic change, failover), mark it as requiring approval and do not present it as a routine step.

### Deliverable contract

Each deliverable contains:

1. Front matter: title, type, owner, audience, scope/version, last-verified date, source revision.
2. Assumptions and `UNVERIFIED` items, listed explicitly.
3. The document body, structured by its type.
4. Verification table with checks run, method, and result.
5. Open questions with named owners.
6. A changelog entry describing what changed and why.

Do not deliver a document with unresolved `UNVERIFIED` items in any section presented as authoritative. Do not deliver prose without at least one traceable source per factual section.

### What not to do

- Do not write documentation from memory of an API, library, or configuration you have not checked.
- Do not paste secrets, credentials, real customer identifiers, or internal topology without Gate C approval.
- Do not state performance numbers, benchmark results, or uptime figures without a cited measurement.
- Do not restate the code line by line; document contracts, constraints, and failure modes.
- Do not duplicate content across documents; link to a single authoritative page.
- Do not change published URLs or delete pages without Gate E approval.
- Do not add generic introductions, filler, or unverified best-practice claims.

### Ultron routing contract

**Choose this skill when:** managing the full lifecycle of technical documentation: scope, authoring, source verification, consistency, maintenance, runbooks, ADRs, API references, changelogs, and documentation quality across a product or engineering system.

**Choose document-authoring-publishing when:** documentation must be packaged and published as part of an artifact or external registry release, with version alignment and publication approval.

**Handoff contract:** provide the verified document content, version, source references, review status, and unresolved caveats. The publishing skill returns the published URL/version, artifact linkage, and publication evidence. Reconcile the published copy against the approved source and update the documentation inventory.

**Why the boundary exists:** technical documentation operations own accuracy over time; the publishing skill owns the controlled external release of a particular document set.

