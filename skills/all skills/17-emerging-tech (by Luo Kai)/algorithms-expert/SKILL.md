---
name: algorithms-cs-expert
version: 1.0.0
description: Expert-level algorithms and complexity theory covering sorting, searching, graph algorithms, dynamic programming, greedy algorithms, NP-completeness, and algorithm design paradigms.
author: luo-kai
tags: [algorithms, complexity, graphs, dynamic programming, sorting]
---

# Algorithms CS Expert

## Before Starting
1. Which algorithm category?
2. Time or space optimization priority?
3. Exact or approximate solution needed?

## Core Expertise Areas

### Sorting Algorithms
Comparison sorts: quicksort O(n log n) avg, mergesort O(n log n) worst, heapsort O(n log n).
Non-comparison: counting sort O(n+k), radix sort O(nk), bucket sort O(n) avg.
Stability: mergesort and timsort stable, quicksort and heapsort not stable.
In-place: heapsort and quicksort in-place, mergesort requires O(n) extra space.

### Graph Algorithms
BFS: shortest path in unweighted graphs, O(V+E), uses queue.
DFS: topological sort, cycle detection, SCC, O(V+E), uses stack or recursion.
Dijkstra: shortest path weighted non-negative, O(E log V) with priority queue.
Bellman-Ford: handles negative weights, detects negative cycles, O(VE).
Floyd-Warshall: all-pairs shortest path, O(V3), dynamic programming.
Minimum spanning tree: Kruskal (sort edges + union-find), Prim (greedy + priority queue).

### Dynamic Programming
Optimal substructure: optimal solution contains optimal solutions to subproblems.
Overlapping subproblems: same subproblems solved multiple times without memoization.
Top-down memoization: recursive with cache.
Bottom-up tabulation: iterative filling of DP table.
Classic problems: LCS, LIS, knapsack, matrix chain, edit distance, coin change.

### Complexity Theory
Big-O classes: O(1) constant, O(log n) logarithmic, O(n) linear, O(n log n), O(n2), O(2n).
P vs NP: P decidable in polynomial time, NP verifiable in polynomial time.
NP-complete: NP-hard and in NP. First: SAT. Others via reduction.
Common NP-complete: SAT, 3-SAT, vertex cover, clique, TSP decision, subset sum.

## Best Practices
- Analyze both time and space complexity
- Consider average, worst, and best case separately
- Prove correctness before optimizing
- Use amortized analysis for data structure operations
- Reduce unknown problems to known ones

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Off-by-one in DP table | Carefully define base cases and indices |
| Dijkstra on negative edges | Use Bellman-Ford instead |
| Ignoring integer overflow | Use long or BigInteger for large inputs |
| Wrong complexity analysis | Account for all loops and recursive calls |

## Related Skills
- data-structures-expert
- algorithms-expert
- compiler-expert
