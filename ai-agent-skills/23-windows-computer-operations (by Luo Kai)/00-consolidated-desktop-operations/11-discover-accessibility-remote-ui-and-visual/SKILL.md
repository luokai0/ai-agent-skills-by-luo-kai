---
name: "Windows Accessibility, Remote Support, UI Automation, and Visual Evidence: Discover Current State"
description: "Inspect assistive technologies, remote support sessions, UI Automation controls, focus and selectors, screenshots, OCR, and visual evidence while preserving consent, privacy, and user preferences."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0011"
  version: "1.2.0"
---

# Windows Accessibility, Remote Support, UI Automation, and Visual Evidence: Discover Current State

## Objective

Establish a verified baseline of accessibility settings, remote support sessions, UI Automation controls, focus and selectors, screenshots, OCR, and visual evidence. Preserve the user's established assistive setup, privacy, consent, and local access. This is a read-only discovery workflow: do not change assistive settings, enable remote access, record people, bypass security prompts, or capture unrelated screen content without explicit permission.

## When to use

Use for:
- Narrator, Magnifier, captions, contrast, keyboard access, voice access, and input assistance.
- Remote Desktop, Quick Assist, remote support, session handoff, and connectivity.
- UI Automation trees, selectors, focus, keyboard/mouse actions, waits, and resilient workflows.
- Screen capture, OCR, visual grounding, region selection, and evidence handling.

Applies to interactive Windows 10 and Windows 11 desktops and laptops, including remote and managed sessions.

## Required operating discipline

1. Identify the exact device, user/session, assistive modality, remote endpoint, UI control, window, screenshot region, and requested outcome.
2. Observe before acting. Record the user's current modality, focus, session owner, consent state, visible window, and any sensitive content.
3. Prefer supported accessibility/UI Automation controls and application-native APIs. Use screenshots only when necessary and approved.
4. Do not assume a user's disability, preferred modality, or consent to remote access or recording.
5. Obtain explicit approval before changing assistive settings, enabling remote access, sharing a screen, recording, or capturing sensitive content.
6. Never bypass UAC, sign-in, MFA, CAPTCHA, security prompts, or visible consent.
7. Keep discovery read-only. Do not conceal actions or use stale coordinate clicks.

## Environment and target identification

Confirm Windows edition/build, current user/session, and whether the device is local, remote, virtual, shared, or organization-managed. Distinguish host from remote endpoint and local access from remote session state.

Identify controls by stable accessibility name, automation ID, control type, enabled state, and focus where available. For screenshots, confirm the exact window or region and whether secrets, private messages, credentials, or personal data are visible.

## Domain profiles

### A. Accessibility and assistive technology

**Scope:** Narrator, Magnifier, captions, contrast, keyboard access, voice access, and input assistance.

**Preferred tools:** Settings > Accessibility, Narrator, Magnifier, UI Automation, and on-screen keyboard.

**Inspection:** Establish the requested modality and inspect relevant settings without changing them. Test focus order, speech/caption output, and reversibility only in a way that does not disrupt the user's established setup.

**Safety:** Do not change assistive settings without consent. Never assume a user's disability or preferred modality.

**Verification:** Ask or observe the requested modality, test focus order and output, and confirm settings remain unchanged.

**Recovery:** Use keyboard-only navigation or restore the previous setting; preserve the user's established accessibility setup.

### B. Remote Desktop and support sessions

**Scope:** Remote Desktop, Quick Assist, remote support, session handoff, and connectivity.

**Preferred tools:** Windows Remote Desktop UI, Quick Assist, and read-only Get-NetTCPConnection where relevant.

**Inspection:** Verify endpoint identity, session owner, encryption/organization policy, visible consent, and disconnect path. Distinguish a configured remote feature from an active support session.

**Safety:** No covert remote access, unattended persistence, credential sharing, or enabling remote access without explicit consent.

**Verification:** Confirm endpoint identity, session owner, consent, applicable policy, and visible disconnect path.

**Recovery:** Stop if identity or consent is unclear; end the session visibly and preserve local access.

### C. UI Automation and resilient interaction

**Scope:** UI Automation trees, selectors, focus, keyboard/mouse actions, waits, and resilient workflows.

**Preferred tools:** Supported UIA framework, accessibility tree, screenshots, keyboard shortcuts, and application-native APIs.

**Inspection:** Identify the target control using stable properties. Confirm control identity, enabled state, focus, expected text/value, and the current screen state before any separately approved action.

**Safety:** No hidden clicks, security prompt bypass, CAPTCHA circumvention, or actions that conceal activity.

**Verification:** Assert control identity, enabled state, focus, expected text/value, and post-action screen state. Reacquire controls after layout changes.

**Recovery:** Reacquire controls after layout changes; stop rather than clicking by stale coordinates.

### D. Screenshots, screen reading, and OCR

**Scope:** Screen capture, OCR, visual grounding, region selection, and evidence handling.

**Preferred tools:** Approved screenshot API, Snipping Tool, Windows OCR, and UI Automation names.

**Inspection:** Capture only the relevant window or region after confirming what is visible. Compare OCR output with the visible source and use UI Automation for ambiguous labels or values.

**Safety:** Capture only relevant windows; redact secrets and personal content; do not record without permission.

**Verification:** Compare OCR with visible source. Use UIA for ambiguous labels, values, or control identity. Report uncertainty instead of inventing text.

**Recovery:** Retake a focused crop at readable scale; report uncertainty rather than inventing text.

## Safe diagnostic commands

These optional read-only probes provide basic environment context. Check availability first.

```powershell
Get-ComputerInfo | Select-Object WindowsProductName, WindowsVersion, OsArchitecture
Get-Process | Select-Object -First 10 Name, Id
```

Do not enumerate unrelated user files, dump clipboard contents, capture private windows, or export screenshots to unapproved locations. Avoid including account names, private paths, IP addresses, document titles, or personal information in external reports.

## Unified discovery workflow

1. **Bind the request.** Select relevant profile(s). Confirm exact device/session, assistive modality, remote endpoint, UI control, window, or screenshot region.
2. **Capture a baseline.** Observe native UI. Record current assistive settings, session owner/consent, control identity, focus, and visible content only as needed.
3. **Inspect narrowly.** Use named UI Automation controls before coordinate-only interaction. Capture only the minimum visual evidence necessary.
4. **Resolve ambiguity.** If endpoint identity, consent, control identity, or visible content is unclear, stop and ask for clarification.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, effect, privacy implications, consent requirements, and rollback route; obtain approval first.
6. **Verify independently.** Recheck focus, control identity, modality, endpoint/consent, or OCR against the visible source. A click response is not proof.
7. **Close the loop.** Report observed state, what remained unchanged, evidence, blocked checks, and remaining risk.

## Stop conditions and recovery

Stop if assistive settings may be disrupted, remote identity or consent is unclear, a security prompt appears, the target control cannot be identified reliably, a stale coordinate would be required, or sensitive screen content would be captured.

Preserve the current state and local access. Retry at most once through a lower-risk documented route. Never bypass security prompts, CAPTCHA, visible consent, or privacy indicators; never conceal remote actions or record people without permission.

## Privacy-safe evidence and handoff

Report the minimum redacted device/session, modality, endpoint identity, control properties, and screenshot/OCR verification needed. Do not include private screen content, credentials, clipboard data, biometric data, private messages, tokens, or unrelated filenames. Mark uncertain OCR or UI state as uncertain.

## Completion checklist

- [ ] Device/session and exact target were confirmed.
- [ ] User's assistive modality and established preferences were respected.
- [ ] Remote endpoint and visible consent were verified where relevant.
- [ ] UI controls were identified by stable properties where available.
- [ ] No security prompt, CAPTCHA, or consent control was bypassed.
- [ ] Screenshots were limited to approved relevant regions and redacted.
- [ ] OCR was compared with visible source and uncertainty was reported.
- [ ] No assistive, remote-access, or privacy setting was changed.
- [ ] Findings and limitations were independently verified.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows accessibility and remote-support surfaces.
