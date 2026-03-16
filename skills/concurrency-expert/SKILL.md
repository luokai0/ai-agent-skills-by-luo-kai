---
name: concurrency-expert
description: Expert-level concurrency and parallelism. Use when working with threads, async/await, coroutines, race conditions, deadlocks, mutexes, semaphores, actor models, parallel algorithms, or concurrent data structures. Also use when the user mentions 'race condition', 'deadlock', 'mutex', 'async/await', 'thread pool', 'concurrent', 'parallel', 'atomics', 'lock-free', or 'goroutine'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Concurrency Expert

You are an expert in concurrency and parallelism with deep knowledge of threading models, synchronization primitives, async patterns, lock-free data structures, and diagnosing concurrency bugs.

## Before Starting

1. **Language** — Python, Go, Rust, Java, C++, JavaScript?
2. **Problem type** — design, debugging race condition, performance, deadlock?
3. **Concurrency model** — threads, async/await, actors, CSP (channels)?
4. **Scale** — single machine or distributed?
5. **Goal** — throughput, latency, resource efficiency?

---

## Core Expertise Areas

- **Threading models**: OS threads, green threads, thread pools, work stealing
- **Synchronization**: mutex, RWMutex, semaphore, condition variables, barriers
- **Async/await**: event loops, futures/promises, structured concurrency
- **Lock-free**: atomics, CAS operations, memory ordering, ABA problem
- **Patterns**: producer-consumer, pipeline, fan-out/fan-in, worker pool
- **Debugging**: race detectors, deadlock analysis, happens-before reasoning
- **Go concurrency**: goroutines, channels, select, sync package
- **Python async**: asyncio, event loop, tasks, gather, shields

---

## Key Patterns & Code

### Concurrency Mental Model
```
Threading models:
  OS Threads:      1:1 mapping to kernel threads
                   Expensive to create (1-8MB stack)
                   True parallelism on multiple CPUs
                   Languages: C, C++, Java, Go (goroutines map to these)

  Green Threads:   M:N mapping (many user threads to few OS threads)
                   Cheap to create (2KB stack in Go)
                   Runtime manages scheduling
                   Languages: Go goroutines, Erlang processes

  Async/Await:     Single-threaded (or thread pool) event loop
                   No true parallelism for CPU work
                   Excellent for I/O-bound work
                   Languages: JavaScript, Python asyncio, Rust tokio

When to use which:
  I/O bound (network, disk):  async/await or threads — both work well
  CPU bound (computation):    OS threads or processes — need true parallelism
  Many connections:           async/await — 10k+ concurrent connections
  Simple parallelism:         thread pool
```

### Python — asyncio Patterns
```python
import asyncio
import aiohttp
import time
from typing import Any

# Basic async/await
async def fetch_user(session: aiohttp.ClientSession, user_id: int) -> dict:
    async with session.get(f'https://api.example.com/users/{user_id}') as resp:
        resp.raise_for_status()
        return await resp.json()

# Concurrent fetches — gather runs all coroutines concurrently
async def fetch_all_users(user_ids: list[int]) -> list[dict]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user(session, uid) for uid in user_ids]
        # gather runs all concurrently, returns results in order
        return await asyncio.gather(*tasks)

# With error handling per task
async def fetch_all_safe(user_ids: list[int]) -> list[dict | None]:
    async with aiohttp.ClientSession() as session:
        tasks = [fetch_user(session, uid) for uid in user_ids]
        results = await asyncio.gather(*tasks, return_exceptions=True)
        return [
            None if isinstance(r, Exception) else r
            for r in results
        ]

# Timeout
async def fetch_with_timeout(url: str, timeout_seconds: float = 5.0) -> dict:
    async with aiohttp.ClientSession() as session:
        try:
            async with asyncio.timeout(timeout_seconds):
                async with session.get(url) as resp:
                    return await resp.json()
        except asyncio.TimeoutError:
            raise TimeoutError(f'Request to {url} timed out after {timeout_seconds}s')

# Semaphore — limit concurrency
async def fetch_with_rate_limit(urls: list[str], max_concurrent: int = 10) -> list[dict]:
    semaphore = asyncio.Semaphore(max_concurrent)

    async def fetch_one(session, url):
        async with semaphore:  # only max_concurrent at a time
            async with session.get(url) as resp:
                return await resp.json()

    async with aiohttp.ClientSession() as session:
        tasks = [fetch_one(session, url) for url in urls]
        return await asyncio.gather(*tasks)

# Producer-consumer with asyncio.Queue
async def producer(queue: asyncio.Queue, items: list):
    for item in items:
        await queue.put(item)
        await asyncio.sleep(0)  # yield to event loop
    await queue.put(None)  # sentinel to stop consumer

async def consumer(queue: asyncio.Queue, results: list):
    while True:
        item = await queue.get()
        if item is None:
            break
        result = await process_item(item)
        results.append(result)
        queue.task_done()

async def pipeline(items: list) -> list:
    queue = asyncio.Queue(maxsize=100)
    results = []

    # Run producer and multiple consumers concurrently
    await asyncio.gather(
        producer(queue, items),
        consumer(queue, results),
        consumer(queue, results),  # two consumers
    )
    return results

# Worker pool pattern
async def worker_pool(tasks: list, num_workers: int = 10) -> list:
    queue = asyncio.Queue()
    results = []

    for task in tasks:
        await queue.put(task)

    async def worker():
        while True:
            try:
                task = queue.get_nowait()
            except asyncio.QueueEmpty:
                break
            result = await process(task)
            results.append(result)
            queue.task_done()

    workers = [asyncio.create_task(worker()) for _ in range(num_workers)]
    await asyncio.gather(*workers)
    return results
```

### Python — Threading for CPU Work
```python
import threading
import concurrent.futures
import multiprocessing
from typing import Callable, TypeVar

T = TypeVar('T')

# Thread pool for I/O bound work
def fetch_urls_threaded(urls: list[str]) -> list[str]:
    with concurrent.futures.ThreadPoolExecutor(max_workers=20) as executor:
        futures = {executor.submit(requests.get, url): url for url in urls}
        results = []
        for future in concurrent.futures.as_completed(futures):
            url = futures[future]
            try:
                response = future.result(timeout=10)
                results.append(response.text)
            except Exception as e:
                print(f'Failed {url}: {e}')
        return results

# Process pool for CPU bound work
def cpu_intensive(data: list) -> list:
    with concurrent.futures.ProcessPoolExecutor(max_workers=multiprocessing.cpu_count()) as executor:
        return list(executor.map(process_chunk, data))

# Thread-safe data structures
import queue
import threading

class ThreadSafeCounter:
    def __init__(self):
        self._value = 0
        self._lock = threading.Lock()

    def increment(self):
        with self._lock:
            self._value += 1

    def get(self) -> int:
        with self._lock:
            return self._value

# RLock for reentrant locking
class ThreadSafeCache:
    def __init__(self):
        self._cache: dict = {}
        self._lock = threading.RLock()  # reentrant

    def get(self, key: str):
        with self._lock:
            return self._cache.get(key)

    def set(self, key: str, value) -> None:
        with self._lock:
            self._cache[key] = value

    def get_or_set(self, key: str, factory: Callable) -> Any:
        with self._lock:
            if key not in self._cache:
                self._cache[key] = factory()  # safe: reentrant
            return self._cache[key]
```

### Go — Goroutines and Channels
```go
package main

import (
    "context"
    "fmt"
    "sync"
    "time"
)

// Worker pool with channels
func workerPool(jobs <-chan int, results chan<- int, numWorkers int) {
    var wg sync.WaitGroup
    for i := 0; i < numWorkers; i++ {
        wg.Add(1)
        go func() {
            defer wg.Done()
            for job := range jobs {
                results <- process(job)
            }
        }()
    }
    wg.Wait()
    close(results)
}

func runPipeline(items []int) []int {
    jobs := make(chan int, len(items))
    results := make(chan int, len(items))

    go workerPool(jobs, results, 10)

    for _, item := range items {
        jobs <- item
    }
    close(jobs)

    var output []int
    for result := range results {
        output = append(output, result)
    }
    return output
}

// Fan-out / fan-in
func fanOut(input <-chan int, numWorkers int) []<-chan int {
    channels := make([]<-chan int, numWorkers)
    for i := 0; i < numWorkers; i++ {
        ch := make(chan int)
        channels[i] = ch
        go func(out chan<- int) {
            for v := range input {
                out <- process(v)
            }
            close(out)
        }(ch)
    }
    return channels
}

func fanIn(channels ...<-chan int) <-chan int {
    merged := make(chan int)
    var wg sync.WaitGroup

    for _, ch := range channels {
        wg.Add(1)
        go func(c <-chan int) {
            defer wg.Done()
            for v := range c {
                merged <- v
            }
        }(ch)
    }

    go func() {
        wg.Wait()
        close(merged)
    }()
    return merged
}

// Context cancellation
func fetchWithCancel(ctx context.Context, url string) ([]byte, error) {
    req, err := http.NewRequestWithContext(ctx, "GET", url, nil)
    if err != nil {
        return nil, err
    }
    resp, err := http.DefaultClient.Do(req)
    if err != nil {
        return nil, err
    }
    defer resp.Body.Close()
    return io.ReadAll(resp.Body)
}

// Timeout pattern
func withTimeout(duration time.Duration, fn func() error) error {
    ctx, cancel := context.WithTimeout(context.Background(), duration)
    defer cancel()

    done := make(chan error, 1)
    go func() { done <- fn() }()

    select {
    case err := <-done:
        return err
    case <-ctx.Done():
        return ctx.Err()
    }
}

// Once — initialization that runs exactly once
var (
    instance *Service
    once     sync.Once
)

func GetService() *Service {
    once.Do(func() {
        instance = newService()
    })
    return instance
}

// RWMutex — multiple readers, single writer
type SafeMap struct {
    mu sync.RWMutex
    m  map[string]int
}

func (s *SafeMap) Get(key string) (int, bool) {
    s.mu.RLock()
    defer s.mu.RUnlock()
    v, ok := s.m[key]
    return v, ok
}

func (s *SafeMap) Set(key string, value int) {
    s.mu.Lock()
    defer s.mu.Unlock()
    s.m[key] = value
}
```

### Rust — Fearless Concurrency
```rust
use std::sync::{Arc, Mutex, RwLock};
use std::thread;
use tokio::sync::{mpsc, Semaphore};
use std::sync::atomic::{AtomicUsize, Ordering};

// Arc<Mutex<T>> — shared mutable state across threads
fn shared_counter() {
    let counter = Arc::new(Mutex::new(0u64));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        let handle = thread::spawn(move || {
            let mut c = counter.lock().unwrap();
            *c += 1;
        });
        handles.push(handle);
    }

    for handle in handles {
        handle.join().unwrap();
    }

    println!("Counter: {}", *counter.lock().unwrap());
}

// Atomic operations — lock-free counter
fn atomic_counter() {
    let counter = Arc::new(AtomicUsize::new(0));
    let mut handles = vec![];

    for _ in 0..10 {
        let counter = Arc::clone(&counter);
        handles.push(thread::spawn(move || {
            counter.fetch_add(1, Ordering::Relaxed);
        }));
    }

    for h in handles { h.join().unwrap(); }
    println!("Counter: {}", counter.load(Ordering::SeqCst));
}

// Tokio async — concurrent HTTP requests
#[tokio::main]
async fn fetch_all(urls: Vec<String>) -> Vec<Result<String, reqwest::Error>> {
    let semaphore = Arc::new(Semaphore::new(10)); // max 10 concurrent
    let client = reqwest::Client::new();

    let tasks: Vec<_> = urls.into_iter().map(|url| {
        let sem = Arc::clone(&semaphore);
        let client = client.clone();
        tokio::spawn(async move {
            let _permit = sem.acquire().await.unwrap();
            client.get(&url).send().await?.text().await
        })
    }).collect();

    futures::future::join_all(tasks)
        .await
        .into_iter()
        .map(|r| r.unwrap())
        .collect()
}

// Channel-based worker pool
async fn worker_pool(items: Vec<String>, num_workers: usize) -> Vec<String> {
    let (tx, mut rx) = mpsc::channel::<String>(100);
    let (result_tx, mut result_rx) = mpsc::channel::<String>(100);

    // Spawn workers
    for _ in 0..num_workers {
        let mut rx_clone = /* clone receiver */ todo!();
        let result_tx = result_tx.clone();
        tokio::spawn(async move {
            while let Some(item) = rx_clone.recv().await {
                let result = process(item).await;
                result_tx.send(result).await.unwrap();
            }
        });
    }

    // Send work
    for item in items {
        tx.send(item).await.unwrap();
    }
    drop(tx);

    // Collect results
    let mut results = vec![];
    while let Some(r) = result_rx.recv().await {
        results.push(r);
    }
    results
}
```

### Diagnosing Concurrency Bugs
```
Race Condition:
  Symptom: intermittent wrong results, crashes, data corruption
  Cause: two threads read-modify-write shared state without synchronization
  Detection:
    Go:   go test -race ./...
    Rust: compiler prevents most races
    Python: no race on GIL-protected types, but file/socket operations can race
  Fix: protect shared state with mutex, use atomic operations, or avoid sharing

Deadlock:
  Symptom: program hangs forever, threads blocked
  Cause: circular lock dependency (A waits for B, B waits for A)
  Detection: thread dump, Go deadlock detector (runtime panic)
  Fix:
    - Always acquire locks in the same order
    - Use tryLock with timeout
    - Prefer message passing over shared state
    - Use sync.RWMutex when reads are frequent

Livelock:
  Symptom: threads keep running but make no progress
  Cause: threads keep reacting to each other's state changes
  Example: two people in hallway both stepping aside in the same direction
  Fix: add randomness to retry logic, use backoff

Starvation:
  Symptom: some goroutines/threads never make progress
  Cause: high-priority threads monopolize resources
  Fix: use fair scheduling, limit priority inversion

Priority Inversion:
  Symptom: high-priority task blocked by low-priority task
  Cause: low-priority holds lock needed by high-priority
  Fix: priority inheritance, avoid long critical sections
```

---

## Best Practices

- Prefer message passing over shared memory — channels over mutexes when possible
- Keep critical sections (locked regions) as small as possible
- Always acquire multiple locks in the same order to prevent deadlocks
- Use context/cancellation for timeout and graceful shutdown
- Never ignore errors from goroutines or async tasks — use error channels
- Use race detectors (go -race, ThreadSanitizer) in CI
- Prefer immutable data structures — no shared state = no race conditions
- Document which fields are protected by which lock

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Goroutine leak | Goroutine blocked forever, memory grows | Always have a way to cancel/stop goroutines |
| Capturing loop variable | All goroutines share last value | Pass variable as argument or shadow it |
| Unlock without defer | Panic skips unlock, deadlock | Always use defer mu.Unlock() |
| WaitGroup.Add after go | Race condition in WaitGroup | Call Add before launching goroutine |
| Closing channel twice | Panic | Only sender should close, use sync.Once |
| asyncio.gather ignoring errors | Silent failures | Use return_exceptions=True and check |
| Mutex in hot path | Contention kills performance | Use RWMutex, atomics, or sharding |
| No timeout on locks | Deadlock hangs forever | Use TryLock with timeout |

---

## Related Skills

- **go-expert**: For Go-specific concurrency patterns
- **rust-expert**: For Rust ownership and fearless concurrency
- **python-expert**: For Python asyncio and threading
- **performance-optimization**: For profiling concurrent code
- **system-design**: For distributed concurrency patterns
- **apache-kafka-expert**: For concurrent event processing
