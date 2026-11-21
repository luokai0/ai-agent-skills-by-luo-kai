---
name: realtime-websocket-channels
description: Use when designing, implementing, debugging, or reviewing server-side realtime WebSocket channels, including connection lifecycle, authentication on upgrade, room or topic fan-out, backpressure, heartbeats, reconnection, and horizontal scaling across instances.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Realtime WebSocket Channels

## Purpose and boundaries

This skill covers the server side of bidirectional, long-lived channels: the upgrade handshake, session state, subscription and fan-out logic, message schemas, flow control, liveness detection, graceful shutdown, and multi-instance delivery. It also covers the client contract the server must honor (reconnect, resume, idempotent handling).

Out of scope: browser UI rendering, one-shot HTTP APIs (use a request/response skill), WebRTC media transport, and choosing a cloud vendor. Do not design a channel when a polling endpoint or server-sent events satisfy the requirement with less operational risk; state the reason if you choose WebSockets.

## Inputs and assumptions

Collect before designing:

- Message rate per connection (msgs/sec, p99 size) and fan-out ratio (one message to N subscribers).
- Concurrency target (concurrent sockets per instance and cluster-wide) and delivery semantics required: at-most-once, at-least-once with dedupe, or ordered per channel.
- Auth model: token type, where it is issued, expiry, and revocation requirements.
- Deployment: reverse proxy or load balancer in front, idle timeouts on each hop, whether sticky sessions are available.
- Data sensitivity of channel payloads.

If any of these is unknown, state the assumption explicitly in the design document and mark it as unverified. Library names, frame options, and timeout defaults change between versions; verify every such detail against current official documentation for the exact runtime version in use before relying on it.

## Operating workflow

1. **Define the channel model.** Write each channel type as: name pattern, who may subscribe, who may publish, message types, and ordering guarantee. Example: `orders:{tenantId}` readable by tenant members with role `ops`, publish-only from server, per-key ordering by `orderId`.
2. **Authenticate on upgrade.** Validate credentials during the HTTP upgrade request, before accepting the socket. Reject with the proper HTTP status. Do not accept first and authorize later. Re-check authorization on every subscribe; never trust a channel name from the client.
3. **Specify the envelope.** Every frame carries `type`, `channel`, `id` (unique per message), `seq` (per channel, monotonic), and `payload`. Validate inbound frames against a schema and reject oversized frames at the parser, not after decoding.
4. **Implement subscription state.** Keep a per-connection set of subscribed channels and a server-side index from channel to connections. Remove all index entries on close, error, and timeout.
5. **Bound outbound memory.** Each connection gets a bounded send queue. When it fills, apply the policy chosen in the decision gate below. Never let an unbounded buffer grow per slow client.
6. **Add liveness.** Use protocol-level ping/pong or an application heartbeat at an interval shorter than the shortest idle timeout on the path. Close sockets that miss a configured number of heartbeats.
7. **Support resume.** Clients send the last `seq` they processed per channel; server replays from a bounded buffer or instructs the client to refetch state via HTTP snapshot.
8. **Plan multi-instance fan-out.** Route publishes through a shared bus or pub/sub layer; each instance delivers only to its local sockets. Include instance ID in logs.
9. **Shut down gracefully.** On termination signal, stop accepting upgrades, send a close frame with a reconnect hint, drain queues with a deadline, then exit.

## Decision gates

- **Slow consumer policy:** Drop oldest for lossy telemetry; disconnect with a close code for state streams where clients can resnapshot; block publisher only for internal, trusted pipelines with a short timeout. Pick one per channel type and document it.
- **Ordering:** Guarantee order only per channel key. Global ordering across channels requires a single sequencer and is usually not worth its throughput cost.
- **Delivery:** At-least-once requires client-side dedupe on `id`. Exactly-once is not achievable end to end over a socket; do not promise it.
- **Sticky sessions:** Required only if resume state lives in instance memory. Prefer externalized resume buffers so sticky routing is not a correctness dependency.
- **Auth expiry:** If tokens expire during a session, either close at expiry with a specific code or re-authenticate via an in-band message. Never let an expired credential keep receiving data.

## Verification and evidence

Provide evidence for each claim:

- Load test with the target concurrency and fan-out ratio; report p50/p99 delivery latency, memory per connection, and dropped-message counts. Record the hardware and test tool version. Do not report numbers you did not measure.
- Fault injection: kill an instance mid-stream, sever a connection without close frame, stall a consumer. Confirm sockets are released, index entries removed, and resume behaves per design.
- Authorization tests: unauthenticated upgrade, subscribe to a forbidden channel, publish from a client role without permission, token expiry during session.
- Frame fuzzing: oversized frames, malformed JSON, unknown types, out-of-order `seq`. Confirm no crash and bounded resource use.
- Check that idle timeouts on proxies exceed heartbeat interval, verified by configuration inspection and a test that holds an idle socket past the proxy timeout.

## Failure handling

- **Queue overflow:** Apply the documented slow-consumer policy, increment a metric, log channel and connection ID. Do not silently drop without a counter.
- **Bus outage:** Mark instance degraded, stop accepting new subscriptions if correctness depends on them, and surface the condition through health checks.
- **Resume gap:** If requested `seq` is older than the buffer, return a gap signal and require an HTTP snapshot. Never fabricate missing messages.
- **Auth failure mid-session:** Close with the defined code; do not retry server-side.
- **Repeated reconnect storms:** Ensure server returns retry hints with jitter guidance; do not rely on clients behaving.

## Deliverable contract

Produce a design or change record containing:

1. Channel catalog table: name pattern, subscribe rule, publish rule, ordering, delivery semantics, slow-consumer policy.
2. Envelope schema and close-code table with meanings.
3. Lifecycle diagram covering upgrade, auth, subscribe, heartbeat, close, and shutdown.
4. Capacity assumptions and measured results, labeled measured versus estimated.
5. List of version-sensitive settings with the documentation source checked and date.
6. Open risks and unverified assumptions, each with an owner.

Do not approve a channel for production until the authorization tests, fault injection, and proxy-timeout check pass, and a human owner has signed off on any change touching authentication, data exposure, or tenant isolation. Do not deploy load-balancer or proxy timeout changes, or run load tests against shared environments, without explicit approval.