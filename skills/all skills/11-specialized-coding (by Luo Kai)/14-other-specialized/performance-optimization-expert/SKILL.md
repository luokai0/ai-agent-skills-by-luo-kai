---
author: luo-kai
name: performance-optimization-expert
description: Expert-level performance optimization across languages and systems. Use when profiling apps, identifying bottlenecks, optimizing algorithms, reducing memory usage, improving throughput, cutting latency, tuning databases, or speeding up frontend/backend/CLI code. Also use when the user mentions 'slow', 'bottleneck', 'profiling', 'benchmark', 'lag', 'high CPU', 'memory leak', 'cache miss', 'O(n²)', or 'how do I make this faster'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Performance Optimization Expert

You are an expert performance engineer with deep, production-tested knowledge of profiling, algorithmic optimization, memory management, concurrency tuning, and system-level performance across multiple languages and platforms.

## Before Starting

1. **What's slow?** — Which operation, endpoint, or function? Is it user-facing latency, throughput, memory, CPU, or I/O?
2. **Have you profiled?** — Do you have a flame graph, profiler output, or benchmark numbers? If not, we should get them first.
3. **Language & runtime** — Python, Go, Rust, JS/Node, Java, C++, SQL, or other?
4. **Scale & constraints** — How much data? What's the SLA target? Is memory more important than speed?
5. **What's already been tried?** — Avoid re-suggesting things that didn't work.

---

## Core Expertise Areas

- **Profiling**: flame graphs, CPU/memory profilers, sampling vs. instrumentation, perf, py-spy, pprof, JProfiler, Chrome DevTools
- **Algorithmic complexity**: Big-O analysis, choosing right data structures, eliminating redundant work
- **Memory optimization**: allocation patterns, GC pressure, object pooling, arena allocators, cache locality
- **I/O & concurrency**: async/await, thread pools, connection pooling, lock contention, lock-free patterns
- **Database performance**: query plans, index design, N+1 queries, connection pooling, read replicas, caching layers
- **Frontend performance**: bundle size, render blocking, lazy loading, virtual DOM, layout thrashing, Web Vitals
- **Caching strategies**: in-process, Redis/Memcached, CDN, HTTP cache headers, cache invalidation
- **Compiler & language-specific**: SIMD, branch prediction, inlining, zero-copy, escape analysis

---

## Key Patterns & Code

### Profile First — Never Guess

```python
# Python: always profile before optimizing
import cProfile, pstats, io

def profile(func):
    def wrapper(*args, **kwargs):
        pr = cProfile.Profile()
        pr.enable()
        result = func(*args, **kwargs)
        pr.disable()
        s = io.StringIO()
        ps = pstats.Stats(pr, stream=s).sort_stats('cumulative')
        ps.print_stats(20)  # top 20 slowest calls
        print(s.getvalue())
        return result
    return wrapper

# For production sampling: py-spy top --pid <PID>
# Flame graph: py-spy record -o profile.svg --pid <PID>
```

```go
// Go: built-in pprof
import _ "net/http/pprof"
// go tool pprof http://localhost:6060/debug/pprof/profile?seconds=30
// go tool pprof http://localhost:6060/debug/pprof/heap
```

### Algorithmic: Replace O(n²) with O(n log n) or O(n)

```python
# BAD: O(n²) — nested loop lookup
def find_duplicates_slow(items):
    dupes = []
    for i, x in enumerate(items):
        for j, y in enumerate(items):
            if i != j and x == y:
                dupes.append(x)
    return dupes

# GOOD: O(n) — hash map
def find_duplicates_fast(items):
    seen = {}
    dupes = set()
    for x in items:
        if x in seen:
            dupes.add(x)
        seen[x] = True
    return list(dupes)

# BAD: O(n) list lookup inside loop → O(n²) total
def process_slow(users, allowed_ids):
    return [u for u in users if u.id in allowed_ids]  # list `in` is O(n)

# GOOD: Convert to set first → O(n) total
def process_fast(users, allowed_ids):
    allowed = set(allowed_ids)  # O(n) once
    return [u for u in users if u.id in allowed]  # O(1) lookup
```

### Memory: Reduce Allocations

```python
# BAD: creates intermediate lists
result = list(map(str, filter(lambda x: x > 0, range(1_000_000))))

# GOOD: lazy generators, no intermediate allocation
result = [str(x) for x in range(1_000_000) if x > 0]

# BETTER for large data: use generator, don't materialize
def positive_strings(n):
    return (str(x) for x in range(n) if x > 0)
```

```go
// Go: sync.Pool to reuse allocations
var bufPool = sync.Pool{
    New: func() interface{} { return new(bytes.Buffer) },
}

func processRequest(data []byte) string {
    buf := bufPool.Get().(*bytes.Buffer)
    buf.Reset()
    defer bufPool.Put(buf)
    buf.Write(data)
    return buf.String()
}
```

### Caching: Memoize Expensive Computation

```python
from functools import lru_cache
import time

# Simple in-process cache
@lru_cache(maxsize=1024)
def expensive_compute(n: int) -> int:
    time.sleep(0.1)  # simulate work
    return n * n

# TTL-based cache (use cachetools for this)
from cachetools import TTLCache, cached
cache = TTLCache(maxsize=100, ttl=300)

@cached(cache)
def get_user(user_id: int):
    return db.fetch_user(user_id)
```

### Database: Fix N+1 Queries

```python
# BAD: N+1 — 1 query for orders + N queries for users
orders = Order.objects.all()  # 1 query
for order in orders:
    print(order.user.name)  # N queries — one per order

# GOOD: 2 queries total (JOIN)
orders = Order.objects.select_related('user').all()
for order in orders:
    print(order.user.name)  # no extra query

# For M2M or reverse FK: prefetch_related
orders = Order.objects.prefetch_related('items').all()
```

```sql
-- Always EXPLAIN ANALYZE before and after
EXPLAIN ANALYZE
SELECT u.name, COUNT(o.id) as order_count
FROM users u
LEFT JOIN orders o ON u.id = o.user_id
GROUP BY u.id;

-- Add index for the join column if missing
CREATE INDEX CONCURRENTLY idx_orders_user_id ON orders(user_id);
```

### Concurrency: Saturate I/O Without Blocking

```python
import asyncio
import httpx

# BAD: sequential I/O — total time = sum of all requests
def fetch_all_slow(urls):
    results = []
    for url in urls:
        r = requests.get(url)
        results.append(r.text)
    return results

# GOOD: concurrent I/O — total time ≈ slowest single request
async def fetch_all_fast(urls):
    async with httpx.AsyncClient() as client:
        tasks = [client.get(url) for url in urls]
        responses = await asyncio.gather(*tasks)
        return [r.text for r in responses]
```

```go
// Go: worker pool pattern for CPU-bound work
func workerPool(jobs []Job, numWorkers int) []Result {
    jobCh := make(chan Job, len(jobs))
    resultCh := make(chan Result, len(jobs))

    for i := 0; i < numWorkers; i++ {
        go func() {
            for job := range jobCh {
                resultCh <- process(job)
            }
        }()
    }

    for _, job := range jobs {
        jobCh <- job
    }
    close(jobCh)

    results := make([]Result, 0, len(jobs))
    for range jobs {
        results = append(results, <-resultCh)
    }
    return results
}
```

### Frontend: Eliminate Layout Thrashing

```javascript
// BAD: read-write-read-write causes multiple reflows
elements.forEach(el => {
    const height = el.offsetHeight;  // forces reflow
    el.style.height = height + 10 + 'px';  // triggers reflow again
    const newHeight = el.offsetHeight;  // forces reflow again
});

// GOOD: batch reads, then batch writes
const heights = elements.map(el => el.offsetHeight);  // one reflow
elements.forEach((el, i) => {
    el.style.height = heights[i] + 10 + 'px';  // one repaint
});

// Use requestAnimationFrame for animations
function animate() {
    requestAnimationFrame(() => {
        element.style.transform = `translateX(${x}px)`;
    });
}
```

---

## Best Practices

- **Measure before and after** — if you can't benchmark it, you don't know you improved it
- **Optimize the hot path** — 20% of code causes 80% of slowness; find it with a profiler
- **Cache at the right layer** — in-process > Redis > DB; evict aggressively
- **Batch I/O** — bulk inserts, bulk API calls, async gather; avoid one-at-a-time patterns
- **Avoid premature optimization** — correctness first, readability second, speed third
- **Watch GC pressure** — many short-lived small allocations destroy throughput
- **Use the right data structure** — dict/HashMap over list for lookups, deque over list for queues
- **Lazy evaluation** — compute only what you need, when you need it

---

## Common Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| N+1 queries | DB query count = record count | `select_related`, `JOIN`, batch fetch |
| Missing indexes | Slow queries, high `Seq Scan` | `EXPLAIN ANALYZE`, add index |
| Unbounded cache | OOM, growing memory | Set `maxsize` / TTL on all caches |
| GIL in Python threads | CPU-bound threads don't parallelize | Use `multiprocessing` or async for I/O |
| Synchronous I/O in async code | Event loop blocks | Use `asyncio.run_in_executor` or async libs |
| Premature optimization | Wasted time, unreadable code | Profile first, optimize only hot paths |
| String concatenation in loop | O(n²) memory copies | Use `join()` or `StringBuilder` |
| Copying large arrays | High memory & CPU | Use views/slices, in-place ops, generators |

---

## Related Skills

- `algorithms-expert` — Big-O analysis and data structure selection
- `concurrency-expert` — Lock-free patterns, thread safety, async models
- `postgresql-expert` / `mysql-expert` — Query plan analysis and index design
- `debugging-expert` — Finding root cause before optimizing
- `webperf-expert` — Web Vitals, Core Web Vitals, Lighthouse
