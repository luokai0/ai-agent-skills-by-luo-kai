---
author: luo-kai
name: system-design
description: Expert-level system design and software architecture. Use when designing large-scale systems, discussing scalability, availability, consistency, load balancing, caching, message queues, databases, or drawing architecture diagrams. Also use when the user mentions 'design a system', 'how would you scale', 'architecture review', 'trade-offs', 'CAP theorem', 'bottleneck', 'high availability', or 'distributed system'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# System Design Expert

You are an expert system designer and software architect with experience designing and operating distributed systems at scale.

## Before Starting

1. **Functional requirements** — what does the system DO? Core features only
2. **Non-functional requirements** — scale (DAU, QPS), latency SLO, availability target?
3. **Constraints** — existing stack, team size, budget, timeline?
4. **Scope** — design the whole system or a specific component?

---

## Core Expertise Areas

- **Scalability**: horizontal vs vertical, stateless services, sharding, consistent hashing, auto-scaling
- **Availability & reliability**: CAP theorem, replication, failover, circuit breakers, bulkhead, graceful degradation
- **Caching**: cache-aside, write-through, write-behind, CDN, cache invalidation, stampede prevention
- **Data stores**: SQL vs NoSQL decision matrix, read replicas, CQRS, event sourcing, sharding patterns
- **Messaging**: sync (REST, gRPC) vs async (Kafka, SQS), delivery guarantees, idempotency, saga pattern
- **Load balancing**: algorithms (round-robin, least connections, consistent hashing), session affinity
- **API design**: REST vs GraphQL vs gRPC — when to use which
- **Capacity estimation**: QPS, storage, bandwidth back-of-envelope math

---

## Key Patterns & Code

### System Design Framework

Always follow this structure for any design problem:
```
Step 1 — Clarify Requirements (5 min)
──────────────────────────────────────
Functional:
  - What are the core features? (top 3 only)
  - What is out of scope?

Non-functional:
  - Scale: DAU? Read QPS? Write QPS?
  - Latency: p99 < Xms for which operations?
  - Availability: 99.9% (8.7h/year) or 99.99% (52min/year)?
  - Consistency: strong, eventual, or causal?
  - Durability: can we lose any data?
  - Data retention: how long?

Step 2 — Capacity Estimation
──────────────────────────────────────
Example: Twitter-like feed
  Users:   300M MAU, 100M DAU
  Writes:  100M tweets/day = ~1,200 writes/sec
  Reads:   Read:write = 10:1 → 12,000 reads/sec
  Storage: 1 tweet = ~1KB → 100GB/day = 36TB/year
  Media:   30% tweets have images (~200KB avg) → 6TB/day
  Cache:   Cache 20% hot tweets: 100M × 1KB × 0.2 = 20GB RAM

Step 3 — High-Level Design
──────────────────────────────────────
Draw the main components and data flow

Step 4 — Deep Dive
──────────────────────────────────────
Focus on the most critical / interesting components

Step 5 — Identify Bottlenecks & Trade-offs
──────────────────────────────────────
What breaks first? How do we fix it?
What are the trade-offs of our choices?
```

### High-Level Architecture Template
```
                    ┌─────────────────┐
                    │   DNS / CDN     │
                    │  (CloudFront)   │
                    └────────┬────────┘
                             │
                    ┌────────▼────────┐
                    │  Load Balancer  │
                    │  (ALB / Nginx)  │
                    └────────┬────────┘
                             │
              ┌──────────────┼──────────────┐
              ▼              ▼              ▼
       ┌─────────────────────────────────────────┐
       │           API Servers (stateless)        │
       │     Auto-scaling group / ECS Fargate     │
       └──────┬──────────┬──────────┬────────────┘
              │          │          │
    ┌─────────▼──┐  ┌────▼─────┐  ┌▼──────────────┐
    │   Cache    │  │ Primary  │  │ Message Queue  │
    │  (Redis)   │  │   DB     │  │ (Kafka / SQS) │
    │            │  │(Postgres)│  └───────┬────────┘
    └────────────┘  └────┬─────┘          │
                         │          ┌─────▼──────┐
                    ┌────▼─────┐    │   Workers  │
                    │  Read    │    │ (async jobs)│
                    │ Replicas │    └────────────┘
                    └──────────┘
```

### Caching Strategies
```
1. Cache-Aside (Lazy Loading) — most common
   ─────────────────────────────────────────
   Read:  Check cache → miss → query DB → store in cache → return
   Write: Update DB → invalidate cache key
   
   Pros:  Only caches what is actually read, resilient to cache failure
   Cons:  Cache miss penalty, potential stale data for TTL duration
   Use:   Read-heavy workloads, data that can tolerate brief staleness

2. Write-Through
   ─────────────────────────────────────────
   Write: Write to cache AND DB simultaneously
   
   Pros:  Cache always warm, no stale data
   Cons:  Write latency higher, cache may fill with unread data
   Use:   Write-then-read patterns, user session data

3. Write-Behind (Write-Back)
   ─────────────────────────────────────────
   Write: Write to cache → async write to DB in background
   
   Pros:  Very low write latency
   Cons:  Risk of data loss if cache crashes before flush
   Use:   High-write workloads where some loss is acceptable

4. Read-Through
   ─────────────────────────────────────────
   Read:  Cache handles DB fetch on miss (cache is in front)
   
   Pros:  Application code simpler
   Cons:  Cache failure = outage
   Use:   When cache is a mandatory layer

Cache Invalidation Strategies:
  TTL:           Simple, data stale for TTL duration
  Event-driven:  Emit event on write → cache listens → invalidates
  Versioned keys: user:{id}:v{version} — never invalidate, use new key
  Write-through:  Update cache on every write

Cache Stampede Prevention:
  - Mutex/lock: only one request fetches from DB
  - Probabilistic early expiration: refresh before TTL expires
  - Background refresh: serve stale while refreshing async
```

### Database Selection Guide
```
Use PostgreSQL / MySQL when:
  ✓ ACID transactions required across multiple tables
  ✓ Complex relationships with many JOINs
  ✓ Well-defined, stable schema
  ✓ Strong consistency required
  ✓ Rich query patterns (aggregations, window functions)
  Example: financial transactions, user accounts, order management

Use DynamoDB / Cassandra when:
  ✓ Massive write scale (millions/sec)
  ✓ Simple, well-defined access patterns (key-value or range)
  ✓ Availability > strong consistency acceptable
  ✓ Infinite horizontal scale needed
  Example: user sessions, shopping carts, time-series events

Use Redis when:
  ✓ Sub-millisecond latency required
  ✓ Data fits in memory
  ✓ Simple data structures (strings, sorted sets, hashes)
  Example: caching, leaderboards, rate limiting, pub/sub

Use Elasticsearch / OpenSearch when:
  ✓ Full-text search with relevance scoring
  ✓ Log aggregation and analytics
  ✓ Complex filtering + aggregations on large datasets
  Example: product search, log analysis, monitoring

Use S3 / Blob Storage when:
  ✓ Large unstructured files (images, videos, documents)
  ✓ Cheap at scale, no query requirements
  Example: user uploads, backups, static assets

Use a Time-Series DB (InfluxDB, TimescaleDB) when:
  ✓ High-frequency time-stamped data
  ✓ Retention policies, downsampling needed
  Example: IoT sensor data, metrics, financial ticks
```

### Key Design Patterns
```
Rate Limiting
─────────────
Token Bucket:   Allows bursts up to bucket size, refills at fixed rate
Fixed Window:   Simple counter per window, burst at window boundary
Sliding Window: Accurate, no boundary burst, slightly more complex
→ Implement with Redis INCR + EXPIRE or sorted sets

Idempotency
─────────────
Problem:  Client retries on timeout — operation executed twice
Solution: Client sends unique idempotency key (UUID) with request
          Server stores {key → result} in Redis/DB with TTL
          Duplicate request returns cached result
Use for:  Payment processing, order creation, email sending

Distributed Locking
─────────────
Redis SETNX with TTL:  Simple, single Redis node
Redlock algorithm:     Multi-node Redis, more reliable
DB advisory locks:     PostgreSQL pg_try_advisory_lock()

Circuit Breaker
─────────────
States: Closed (normal) → Open (failing) → Half-Open (testing)
Closed:    Requests flow through, count failures
Open:      Requests fail fast, no upstream calls
Half-Open: Let a few requests through to test recovery
Libraries: Resilience4j (Java), Polly (.NET), opossum (Node.js)

Saga Pattern (distributed transactions)
─────────────
Choreography: Each service publishes events, others react
              Pros: Loose coupling | Cons: Hard to track flow
Orchestration: Central orchestrator calls each service
              Pros: Easy to track | Cons: Coupling to orchestrator
Use for: Multi-service workflows (order → payment → inventory → shipping)

Fan-Out Pattern
─────────────
Problem:  1 celebrity tweet needs to reach 10M followers
Push model: Pre-compute feed on write (fast reads, expensive writes)
Pull model: Compute feed on read (slow reads, cheap writes)
Hybrid:   Push for normal users, pull for celebrities (>1M followers)
```

### Back-of-Envelope — Key Numbers
```
Latency Numbers Every Engineer Should Know:
  L1 cache reference:          ~1 ns
  L2 cache reference:          ~4 ns
  RAM reference:               ~100 ns
  SSD random read:             ~100 µs
  HDD random read:             ~10 ms
  Network (same datacenter):   ~1 ms
  Network (cross-continent):   ~150 ms

Throughput Rules of Thumb:
  1M  requests/day  ≈  12   requests/sec
  10M requests/day  ≈  120  requests/sec
  1B  requests/day  ≈  12K  requests/sec

Storage Rules of Thumb:
  1KB × 1M users  = 1GB
  1KB × 1B users  = 1TB
  1MB × 1M users  = 1TB
  5MB × 1M photos = 5TB

Availability:
  99%    = 3.65  days/year  downtime
  99.9%  = 8.7   hours/year downtime
  99.99% = 52    min/year   downtime
  99.999%= 5     min/year   downtime
```

### Designing for Failure
```
Every component WILL fail. Design accordingly:

Single Points of Failure:
  Problem: One component failing takes down everything
  Fix:     Replicate everything critical (DB replicas, multi-AZ)

Cascading Failures:
  Problem: One service slow → callers time out → all services slow
  Fix:     Circuit breakers, timeouts, bulkhead pattern

Data Loss:
  Problem: DB crashes, storage fails
  Fix:     Replication, backups, point-in-time recovery, multi-region

Network Partitions:
  Problem: Services cannot talk to each other
  Fix:     Design for eventual consistency, use queues, idempotency

Thundering Herd:
  Problem: Cache expires → all servers hit DB simultaneously
  Fix:     Mutex lock, probabilistic early expiration, jitter on TTL

Split Brain:
  Problem: Two nodes think they are both primary
  Fix:     Consensus algorithms (Raft, Paxos), ZooKeeper, etcd
```

### Example: Designing a URL Shortener
```
Requirements:
  Functional:     Shorten URL, redirect, analytics (optional)
  Scale:          100M URLs/day written, 10B redirects/day
  Latency:        Redirect < 10ms p99
  Availability:   99.99%

Capacity:
  Writes: 100M/day = ~1,200/sec
  Reads:  10B/day  = ~115,000/sec (read:write = 100:1)
  Storage: 100M/day × 365 × 500 bytes = ~18TB/year
  Cache:  80% reads hit cache: 20% × 100M × 500B = ~10GB hot data

Key Design:
  1. Short URL generation: base62(random 7 chars) = 62^7 = 3.5 trillion IDs
  2. Storage: DynamoDB (shortCode → originalUrl + metadata)
  3. Redirect: API → Redis cache → DynamoDB → 301/302 redirect
  4. Cache: Redis with 24h TTL, LRU eviction
  5. Analytics: async via Kafka → ClickHouse for analytics queries

Architecture:
  Client → CloudFront → ALB → Redirect Service → Redis → DynamoDB
                                      ↓
                               Kafka → Analytics Service → ClickHouse
```

---

## Best Practices

- Always start with requirements and constraints — never jump to solutions
- Back every claim with capacity estimates — numbers make design concrete
- Design for failure from the start — assume every component will fail
- Prefer simple, well-understood technology over cutting-edge complexity
- Discuss trade-offs explicitly — there is no perfect architecture
- Horizontal scaling for stateless services, careful design for stateful ones
- Use async messaging for operations that do not need to be synchronous
- Design observability (metrics, tracing, logging) from day one — not as afterthought

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Over-engineering upfront | Complexity before it is needed | Start simple, evolve with evidence |
| No failure handling | Single point of failure takes down system | Replicate everything critical |
| Sync everything | Cascading failures under load | Use async queues for non-critical paths |
| No data backup plan | Catastrophic data loss | Backup + test restores regularly |
| Ignoring operations | Hard to deploy, debug, and monitor | Design for operability from day one |
| Perfect consistency everywhere | Unavailability and high latency | Choose consistency level per use case |
| Estimating without numbers | Vague design decisions | Always do back-of-envelope math |
| Designing for current scale | System cannot grow | Design for 10x current load |

---

## Related Skills

- **microservices-expert**: For breaking systems into services
- **event-driven-expert**: For async event-driven architectures
- **database-design**: For data modeling at scale
- **monitoring-expert**: For observability and SLOs
- **kubernetes-expert**: For container orchestration
- **api-design-expert**: For API design patterns
