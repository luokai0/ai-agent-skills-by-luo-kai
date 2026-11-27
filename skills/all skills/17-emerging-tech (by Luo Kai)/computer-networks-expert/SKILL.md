---
name: computer-networks-expert
version: 1.0.0
description: Expert-level computer networks covering OSI model, TCP/IP stack, routing protocols, transport layer, application protocols, network security, and software-defined networking.
author: luo-kai
tags: [networking, TCP/IP, routing, protocols, HTTP, DNS, security]
---

# Computer Networks Expert

## Before Starting
1. Which OSI layer?
2. LAN, WAN, or internet-scale?
3. Protocol design or troubleshooting?

## Core Expertise Areas

### OSI and TCP/IP Models
OSI 7 layers: physical, data link, network, transport, session, presentation, application.
TCP/IP 4 layers: network access, internet, transport, application.
Encapsulation: each layer adds header wrapping data from layer above.

### Network Layer
IP addressing: IPv4 32-bit, IPv6 128-bit, CIDR notation, subnetting.
Routing: distance vector (RIP, Bellman-Ford), link state (OSPF, Dijkstra), BGP path vector.
NAT: network address translation, maps private to public addresses.
ARP: maps IP address to MAC address on local network.

### Transport Layer
TCP: connection-oriented, reliable, ordered, flow control, congestion control.
TCP 3-way handshake: SYN, SYN-ACK, ACK.
TCP congestion control: slow start, congestion avoidance, fast retransmit, CUBIC.
UDP: connectionless, unreliable, low overhead, for latency-sensitive applications.
QUIC: UDP-based, 0-RTT, multiplexed streams, used by HTTP/3.

### Application Layer
HTTP/1.1: persistent connections, pipelining, text-based.
HTTP/2: binary, multiplexed, header compression, server push.
HTTP/3: QUIC-based, eliminates head-of-line blocking.
DNS: hierarchical, recursive and iterative resolution, TTL, caching.
TLS: record protocol, handshake, certificates, symmetric encryption.

### Network Security
Firewalls: stateless packet filter, stateful inspection, application layer gateway.
DDoS: volumetric, protocol, application layer attacks, mitigation strategies.
VPN: IPSec tunnel mode, SSL/TLS VPN, WireGuard.
Zero trust: never trust always verify, microsegmentation, identity-based access.

## Best Practices
- Always capture packets when debugging network issues
- Understand MTU and fragmentation at each layer
- Test both IPv4 and IPv6 code paths
- Monitor round-trip time and packet loss separately

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Confusing latency and bandwidth | Latency is delay, bandwidth is capacity |
| Ignoring TCP buffers in throughput | Buffer size limits throughput on high-latency links |
| DNS TTL too short or long | Balance freshness vs DNS load |
| Not handling partial TCP reads | Always loop until full message received |

## Related Skills
- operating-systems-expert
- devsecops-expert
- websockets-expert
