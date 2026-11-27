---
name: operating-systems-expert
version: 1.0.0
description: Expert-level operating systems covering process management, memory management, file systems, synchronization, scheduling, virtualization, and OS security.
author: luo-kai
tags: [operating systems, processes, memory, file systems, scheduling, Linux]
---

# Operating Systems Expert

## Before Starting
1. Which OS or kernel? (Linux, Windows, embedded RTOS)
2. User-space or kernel-space concern?
3. Performance, correctness, or security focus?

## Core Expertise Areas

### Process Management
Process: program in execution — PCB, address space, open files, state.
Process states: new, ready, running, waiting, terminated.
Context switch: save/restore PCB, TLB flush, cache invalidation — expensive.
Threads: lightweight process sharing address space, cheaper context switch.
Fork and exec: Unix process creation — copy-on-write optimization.

### CPU Scheduling
FCFS: first-come first-served, simple, convoy effect.
SJF: shortest job first, optimal average wait, requires future knowledge.
Round robin: time quantum, preemptive, fair, context switch overhead.
Priority scheduling: starvation risk, aging solution.
CFS: Completely Fair Scheduler — Linux default, red-black tree by vruntime.

### Memory Management
Paging: fixed-size pages, page table, TLB for fast translation.
Segmentation: variable-size segments, segment table, external fragmentation.
Virtual memory: demand paging, page faults, swap space.
Page replacement: FIFO, LRU, clock algorithm, optimal (Belady).
TLB: translation lookaside buffer, O(1) virtual-to-physical translation cache.

### Synchronization
Race condition: outcome depends on scheduling order — must be prevented.
Mutex: mutual exclusion, binary semaphore, blocks waiting threads.
Semaphore: counting semaphore for resource counting, wait and signal.
Deadlock: four conditions — mutual exclusion, hold-and-wait, no preemption, circular wait.
Deadlock prevention: break one of four conditions.
Monitor: high-level synchronization with condition variables.

### File Systems
Inode: metadata structure — size, permissions, timestamps, block pointers.
Directory: maps names to inodes, hierarchical namespace.
Journaling: ext4, NTFS — write-ahead log for crash recovery.
Virtual file system: uniform interface across different file system types.

## Best Practices
- Always check return values of system calls
- Use RAII for resource management to prevent leaks
- Minimize time holding locks
- Prefer higher-level synchronization over raw mutexes

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Deadlock from lock ordering | Always acquire locks in consistent global order |
| False sharing in cache | Pad data structures to cache line boundaries |
| Zombie processes | Always wait on child processes |
| TLB shootdown overhead | Minimize cross-CPU address space changes |

## Related Skills
- linux-expert
- concurrency-expert
- computer-architecture-expert
