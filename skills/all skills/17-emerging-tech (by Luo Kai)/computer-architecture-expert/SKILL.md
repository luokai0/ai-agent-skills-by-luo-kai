---
name: computer-architecture-expert
version: 1.0.0
description: Expert-level computer architecture covering CPU design, instruction sets, pipelining, cache hierarchy, memory systems, parallel architectures, and GPU computing.
author: luo-kai
tags: [computer architecture, CPU, cache, pipeline, RISC-V, GPU, memory]
---

# Computer Architecture Expert

## Before Starting
1. RISC or CISC architecture?
2. Single-core performance or parallel throughput?
3. Hardware design or software optimization focus?

## Core Expertise Areas

### Instruction Set Architecture
RISC: few simple instructions, load-store, uniform format, many registers.
CISC: many complex instructions, memory operands, variable length, fewer registers.
RISC-V: open standard ISA, modular extensions, growing adoption.
ARM: dominant in mobile and embedded, energy efficient, RISC-based.
x86-64: dominant in servers and desktop, CISC with RISC-like microops internally.

### CPU Pipeline
Classic 5-stage: fetch, decode, execute, memory, writeback.
Pipeline hazards: structural (resource conflict), data (RAW/WAW/WAR), control (branches).
Hazard solutions: stalling, forwarding, branch prediction, out-of-order execution.
Superscalar: multiple execution units, issue multiple instructions per cycle.
Out-of-order execution: Tomasulo algorithm, reorder buffer, register renaming.

### Cache Hierarchy
L1/L2/L3: smaller and faster closer to CPU, larger and slower further.
Cache mapping: direct-mapped, set-associative, fully associative.
Replacement: LRU, pseudo-LRU, random.
Write policy: write-through vs write-back, write-allocate vs no-write-allocate.
Cache coherence: MESI protocol for multi-core systems.

### Memory Systems
DRAM: row and column access, refresh cycles, banks and ranks.
Memory hierarchy: registers, L1, L2, L3, DRAM, SSD, HDD — latency increases.
Virtual memory: TLB, page tables, huge pages for performance.
NUMA: non-uniform memory access in multi-socket systems.

### GPU Architecture
SIMT: single instruction multiple threads, thousands of lightweight threads.
Streaming multiprocessors: groups of CUDA cores sharing instruction unit.
Memory hierarchy: registers, shared memory, L1, L2, global memory (DRAM).
Warp divergence: different control flow paths stall efficiency.

## Best Practices
- Profile before optimizing — measure actual bottleneck
- Optimize for cache locality — access memory sequentially
- Avoid branch mispredictions in hot paths
- Use SIMD intrinsics for data-parallel operations

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Cache thrashing | Improve spatial and temporal locality |
| False sharing | Align concurrent data to separate cache lines |
| Branch misprediction in tight loops | Profile and restructure to help predictor |
| Memory bandwidth saturation | Reduce data movement, use compression |

## Related Skills
- operating-systems-expert
- embedded-expert
- linux-expert
