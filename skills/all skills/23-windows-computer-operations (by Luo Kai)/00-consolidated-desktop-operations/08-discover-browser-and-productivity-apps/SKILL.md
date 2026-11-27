---
name: "Windows Browser and Productivity Applications: Discover Current State"
description: "Inspect browser profiles, tabs, downloads, site permissions, web sessions, documents, spreadsheets, presentations, mail, calendars, collaboration tools, save state, and sharing scope without exposing secrets or sending content."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0008"
  version: "1.2.0"
---

# Windows Browser and Productivity Applications: Discover Current State

## Objective

Establish the current state of browser tabs, profiles, downloads, site permissions, web app sessions, productivity documents, mail, calendars, collaboration tools, autosave, and sharing scope. Preserve private sessions, credentials, user content, and unsent work. This is a read-only discovery workflow: do not install extensions, send messages, share documents, delete content, or overwrite files without a separate request and explicit confirmation.

## When to use

Use for:
- Browser tabs, profiles, downloads, permissions, web app sessions, and browser troubleshooting.
- Documents, spreadsheets, presentations, mail clients, calendars, and collaboration tools.

Applies to Windows 10 and Windows 11 desktops and laptops.

## Required operating discipline

1. Identify the exact browser, profile, domain, tab, download, application, document, recipient, calendar, or collaboration space.
2. Observe before acting. Note private tabs, unsaved changes, autosave status, active drafts, downloads, and permission prompts.
3. Prefer native application UI and supported accessibility/UI Automation controls. Use read-only metadata and built-in status panels where relevant.
4. Never reveal passwords, session cookies, recovery codes, private tabs, or clipboard contents. Do not inspect unrelated user content.
5. Obtain explicit confirmation before sending, sharing, deleting, overwriting, installing, or changing access permissions. A visible draft is not authorization to send it.
6. Do not install unknown extensions or run downloaded files. Preserve the user's existing session.
7. Keep discovery read-only and report uncertainty honestly.

## Environment and target identification

Confirm the active device, signed-in account/session, browser or application identity, and exact target. Distinguish browser profiles and domains. For productivity content, identify the file or conversation, current recipient, sharing scope, save status, and version history without exposing content unnecessarily.

## Domain profiles

### A. Browsers and web applications

**Scope:** Browser tabs, profiles, downloads, permissions, web app sessions, and browser troubleshooting.

**Preferred tools:** Browser UI, built-in task manager, download history, and site permission panels.

**Inspection:** Verify domain, browser profile, active tab, permission state, download origin, and final page state. Distinguish a logged-in web app session from a browser profile or a saved password.

**Safety:** Never reveal passwords, session cookies, recovery codes, or private tabs. Do not install unknown extensions, copy session tokens, or expose private browsing history.

**Verification:** Recheck the exact domain, profile, tab, permission, download origin, and page state. A page title alone is not proof of domain identity.

**Recovery:** Use a clean tab or supported private session only when appropriate; preserve the user's existing session.

### B. Office and productivity applications

**Scope:** Documents, spreadsheets, presentations, mail clients, calendars, and collaboration tools.

**Preferred tools:** Native application UI, accessibility tree, file properties, autosave, and version history.

**Inspection:** Confirm document identity, current save/sync state, recipient, sharing scope, version history, and whether a message is a draft or already sent. Distinguish local files from cloud-backed documents.

**Safety:** Do not send, share, delete, or overwrite documents or messages without explicit confirmation. Do not infer a send or save from an enabled button or a draft preview.

**Verification:** Verify file identity, recipient, sharing scope, save status, and version history. Confirm send/share status through the application's own activity or sent-item surface only when the user asks.

**Recovery:** Recover from autosave or version history. Do not claim a send or save succeeded without visible confirmation.

## Unified discovery workflow

1. **Bind the request.** Select the applicable profile(s). Confirm exact browser/profile/domain/tab or productivity app/document/recipient.
2. **Capture a baseline.** Observe native UI. Record only relevant identity, permission, download, save, draft, and sharing metadata.
3. **Inspect narrowly.** Do not open private content, expose history, or read message/document bodies unless specifically requested and necessary.
4. **Resolve ambiguity.** If multiple profiles, tabs, files, recipients, or sharing targets match, stop and ask for clarification.
5. **Gate mutations.** For discovery, make no changes. For a separately requested action, confirm exact target, recipient, content, access scope, and expected external effect before proceeding.
6. **Verify independently.** Recheck domain/profile, file identity, save state, or sharing state through the native application. A click response or transient toast is not proof.
7. **Close the loop.** Report inspected state, what remained unchanged, evidence, blocked checks, and remaining uncertainty.

## Stop conditions and recovery

Stop if the domain or account is ambiguous, a sign-in/MFA/security prompt appears, a private tab or credential could be exposed, a download looks suspicious, a document is unsaved, or a recipient/sharing scope is unclear.

Preserve the existing session and unsaved content. Retry at most once through a lower-risk documented route. Never reveal tokens, install unknown extensions, submit forms, send drafts, change sharing, or overwrite content as an improvised workaround.

## Privacy-safe evidence and handoff

Report only the minimum redacted browser/app identity, domain, permission or save status, recipient/sharing scope when needed, checks performed, independent verification, and remaining risk. Do not include passwords, cookies, tokens, recovery codes, private tab titles, message bodies, document content, or unrelated filenames.

## Completion checklist

- [ ] User intent and exact browser/app/profile/document were confirmed.
- [ ] Correct profile(s) were selected.
- [ ] Inspection remained read-only and used least privilege.
- [ ] Passwords, cookies, recovery codes, and private tabs were protected.
- [ ] Downloads were not executed and unknown extensions were not installed.
- [ ] Drafts were not sent and documents were not shared or overwritten.
- [ ] Save state, recipient, and sharing scope were verified where relevant.
- [ ] Findings and limitations were accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows applications and tools.
