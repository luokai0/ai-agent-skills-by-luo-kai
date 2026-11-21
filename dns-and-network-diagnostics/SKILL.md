---
name: dns-and-network-diagnostics
description: Use when resolving DNS failures, slow name lookups, certificate or routing symptoms that look like name resolution problems, split-horizon confusion, or when a user asks to trace why a hostname does or does not reach a service.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Dns And Network Diagnostics

## Purpose and boundaries

This skill covers layered diagnosis of name resolution and basic network reachability: stub resolver behavior, recursive and authoritative answers, record correctness, TTL and caching effects, TCP/UDP connectivity to the resolved address, and path-level checks such as MTU or firewall drops. It produces a root-cause statement backed by captured evidence.

Out of scope unless explicitly approved: changing production DNS zones, altering firewall or routing policy, running packet captures on hosts you do not administer, load-testing resolvers, and any scanning of address space you do not own or have written authorization to test.

## Inputs and assumptions

Collect before testing:
- The exact hostname (FQDN, trailing dot noted), record type expected, and the symptom as observed (NXDOMAIN, SERVFAIL, timeout, wrong address, connection refused, TLS failure).
- Client location, OS, and whether the client uses a VPN, proxy, or DNS-over-HTTPS.
- Expected answer: the intended address, CNAME target, or zone owner, from the authoritative source or change record.
- Time of onset and any recent changes (zone edits, registrar changes, certificate renewals, firewall rule updates).

Assume nothing about resolver software or flags. Confirm the tools available on the host and check their current manual pages or vendor documentation before relying on any option, since syntax and output formats vary across versions and platforms.

## Operating workflow

1. **Reproduce from the failing client.** Run the same lookup the application makes. Record the resolver in use (system stub, search domains, `ndots` effects, hosts file overrides).
2. **Check local overrides first.** Inspect the hosts file and any resolver configuration for stale pins. A stale local entry explains a surprising number of "DNS" failures.
3. **Query the configured resolver, then an independent resolver.** Compare answers, TTLs, and status codes. Divergence points to caching, split-horizon views, or resolver-side filtering.
4. **Walk the delegation.** Starting from the root, follow referrals to the parent zone and the authoritative nameservers. Confirm the parent delegation matches the child NS set.
5. **Query each authoritative server directly** with recursion disabled. Compare SOA serial, record sets, and TTLs across all nameservers. Inconsistent serials indicate incomplete propagation.
6. **Validate the record chain.** Follow every CNAME to its terminal target. Check for CNAME at apex, loops, and dangling targets.
7. **Test reachability to the resolved address.** Attempt TCP connection on the expected port, then application-level handshake if relevant. Separate name failure from transport failure.
8. **Check DNSSEC status if the zone is signed.** A validation failure at a validating resolver often presents as SERVFAIL while the authoritative data looks correct.
9. **Record evidence** (commands, timestamps, responses) and state the root cause.

## Decision gates

- If the local override matches the failing answer: stop; the fix is client-side. Propose removal, do not perform it without approval if the file is managed centrally.
- If configured and independent resolvers disagree: investigate caching or split-horizon before touching authoritative data.
- If authoritative nameservers disagree on the record set: escalate to the zone owner; do not edit zones yourself.
- If the name resolves correctly but TCP fails: move to routing, firewall, or service diagnosis; do not keep varying DNS queries.
- If SERVFAIL appears only at validating resolvers: check DNSSEC chain and signature expiry before blaming authoritative servers.
- Any step that changes state (flushing shared resolver caches, modifying records, altering firewall rules, capturing traffic on others' systems) requires explicit approval from the system owner first.

## Verification and evidence

A diagnosis is complete only when:
- The failing symptom is reproduced, with timestamp and exact error text.
- The root cause is confirmed by a test that would fail before the fix and pass after it.
- At least two independent vantage points (for example, the client resolver and a direct authoritative query) agree on the corrected state.
- TTL expectations are stated: the time until clients should see the change, derived from observed TTLs, not assumed.
- Each authoritative server's serial and answer are recorded in a table.

Do not claim propagation is complete while any authoritative server differs. Do not claim a fix works from a single cached answer.

## Failure handling

- **Timeouts with no response:** check whether UDP and TCP port 53 are reachable; large responses may require TCP fallback. Note that some networks block TCP 53 selectively.
- **Inconsistent results on repeated queries:** likely load-balanced or anycast resolvers. Record each responder and test them individually.
- **Diagnostic tool missing or output format unexpected:** verify the installed version and consult its current documentation; do not guess flags.
- **No access to authoritative servers:** report the limitation and request the zone owner's output rather than attempting intrusive probing.
- **Conflicting evidence:** document both observations and rank by how directly each was measured.

## Deliverable contract

Produce a report with these fields:
1. Symptom and reproduction steps (client, time, exact error).
2. Resolution path table: resolver, query, status, answer, TTL, serial.
3. Root cause in one sentence, with the evidence reference.
4. Recommended change, owner, and approval status.
5. Residual risk and the verification check to run after the change.
6. Explicit list of actions not taken because they required approval.

Do not include speculative causes without evidence, and do not present version-specific command syntax as verified unless checked against current official documentation.