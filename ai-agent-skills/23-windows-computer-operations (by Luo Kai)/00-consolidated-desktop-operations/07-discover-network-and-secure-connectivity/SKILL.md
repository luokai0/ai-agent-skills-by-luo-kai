---
name: "Windows Network and Secure Connectivity: Discover Current State"
description: "Inspect Wi-Fi and Ethernet adapters, connection profiles, signal and IP configuration, DNS resolution, firewall profiles, VPN state, routes, and approved connectivity checks without weakening security."
metadata:
  author: "Luo Kai"
  platform: "Windows 10 and Windows 11"
  category: "Windows Computer Operations"
  skill_id: "windows-consolidated-0007"
  version: "1.2.0"
---

# Windows Network and Secure Connectivity: Discover Current State

## Objective

Establish a verified baseline of Windows network adapters, Wi-Fi/Ethernet connection state, IP configuration, DNS resolution, firewall profiles, VPN state, and application-specific reachability. Preserve network security, organization policy, and private network details. This is read-only discovery: do not connect to unknown networks, reveal passwords, disable firewalls, bypass VPN, weaken TLS, or change corporate network settings.

## When to use

Use for:
- Wi-Fi and Ethernet adapters, connection profiles, signal, IP configuration, and connectivity checks.
- DNS resolution, firewall profile inspection, VPN state, routes, and secure connectivity diagnosis.

Applies to Windows 10 and Windows 11 desktops and laptops, including managed and remote devices.

## Required operating discipline

1. Identify the exact device, adapter, network profile, hostname, VPN connection, firewall profile, and target application.
2. Observe before acting. Record link state, profile type, signal where exposed, IP/gateway/DNS configuration, VPN status, and any network warning.
3. Use native Windows Settings and bounded read-only commands. Distinguish local link, gateway, DNS, VPN route, and application reachability.
4. Obtain explicit approval before externally visible, privacy-sensitive, elevated, or security-impacting changes. Managed network settings belong to the authorized administrator.
5. Never connect to unknown networks, reveal Wi-Fi passwords, expose internal routes, disable firewall, bypass VPN, weaken TLS, or reset the network stack as an initial diagnostic.
6. Redact IP addresses, SSIDs, internal hostnames, routes, and private DNS details in any external report.
7. Keep discovery read-only. Do not change adapter, DNS, firewall, VPN, proxy, or routing settings.

## Environment and target identification

Confirm Windows edition/build, current user/session, device type, and whether the device is local, remote, virtual, or organization-managed.

Identify adapters by name and stable hardware identity where available. Distinguish:
- Wi-Fi association from general internet access.
- Ethernet link from IP address assignment.
- Local IP configuration from gateway reachability.
- DNS resolution from application-level connectivity.
- VPN connection state from actual traffic routing.
- Firewall profile state from application permission.

## Domain profiles

### A. Wi-Fi and Ethernet

**Scope:** Adapter state, connection profiles, signal, IP configuration, and connectivity checks.

**Preferred tools:** Settings > Network, Get-NetAdapter, Get-NetIPConfiguration, ipconfig /all, and ping only to a user-approved endpoint.

**Inspection:** Confirm adapter state, SSID or Ethernet link, IP address, gateway, DNS server, and signal where exposed. Do not assume that a connected adapter proves internet reachability.

**Safety:** Do not connect to unknown networks, reveal Wi-Fi passwords, or change corporate network settings. Treat internal IPs and SSIDs as private.

**Verification:** Verify adapter, SSID or link state, IP, gateway, DNS, and reachability separately.

**Recovery:** Distinguish local link, gateway, DNS, and internet failure. Avoid resetting the network stack prematurely.

**Read-only examples:**
```powershell
Get-NetAdapter | Select-Object Name, Status, LinkSpeed, InterfaceDescription
Get-NetIPConfiguration
ipconfig /all
```

### B. DNS, firewall, VPN, and secure routes

**Scope:** Name resolution, firewall profile inspection, VPN state, and secure route diagnosis.

**Preferred tools:** Resolve-DnsName, Get-NetFirewallProfile, Get-NetIPConfiguration, and VPN Settings UI.

**Inspection:** Check DNS answer for a user-approved hostname, active firewall profile, VPN connection state, route selection, and application-specific reachability. Do not expose internal routes or hostnames unnecessarily.

**Safety:** Never disable firewall, bypass VPN, expose internal routes, or weaken TLS to make a connection work. Do not test arbitrary external hosts without user approval.

**Verification:** Check DNS answer, active profile, VPN connection, route, and application-specific reachability as separate observations.

**Recovery:** Preserve security controls. Collect exact errors and refer managed network settings to the network administrator.

**Read-only examples:**
```powershell
Resolve-DnsName <approved-hostname>
Get-NetFirewallProfile
Get-NetIPConfiguration
```

## Unified discovery workflow

1. **Bind the request.** Confirm device, adapter, network profile, hostname, VPN connection, and target application.
2. **Capture a baseline.** Observe native UI and record only relevant connection, address, gateway, DNS, firewall, and VPN state.
3. **Inspect by layer.** Check link, IP assignment, gateway, DNS, VPN route, and application reachability separately. Do not treat one successful layer as proof of another.
4. **Resolve ambiguity.** If several adapters, VPN profiles, hostnames, or routes match, stop and ask for clarification.
5. **Gate mutations.** For discovery, make no changes. If a separate action is requested, state exact target, security implications, impact, and rollback plan; obtain approval first.
6. **Verify independently.** Recheck the same adapter/profile and target in a second native surface where practical. A ping or DNS response alone is not proof of application connectivity.
7. **Close the loop.** Report the failing layer, evidence, blocked checks, and remaining uncertainty. Do not claim internet access or secure routing without evidence.

## Stop conditions and recovery

Stop if the network is managed and policy blocks access, the endpoint is not approved, firewall/VPN state is unclear, internal routes could be exposed, or a security warning appears.

Preserve the current configuration and exact error. Retry at most once through a lower-risk read-only route. Never disable firewall, bypass VPN, weaken TLS, alter DNS, connect to an unknown network, or reset the stack as an improvised workaround.

## Privacy-safe evidence and handoff

Report adapter and connection state using redacted identifiers, relevant IP/gateway/DNS status, firewall/VPN state, approved target tested, independent verification, and remaining risk. Do not expose passwords, private SSIDs, internal hostnames, full routes, tokens, or unnecessary IP details.

## Completion checklist

- [ ] Device, adapter, profile, hostname, and VPN identity were confirmed.
- [ ] Link, IP, gateway, DNS, VPN, and application connectivity were distinguished.
- [ ] Only approved endpoints were queried.
- [ ] Firewall, VPN, TLS, and organization policy remained intact.
- [ ] Private network details were redacted.
- [ ] No network settings were changed.
- [ ] Findings were independently verified and accurately reported.

---
Copyright (c) 2026 Luo Kai. All rights reserved for original material in this skill. Product names are used only to identify supported Windows networking surfaces and tools.
