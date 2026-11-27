---
name: data-structures-expert
version: 1.0.0
description: Expert-level data structures covering arrays, linked lists, trees, heaps, hash tables, graphs, and advanced structures like segment trees, tries, and union-find.
author: luo-kai
tags: [data structures, trees, graphs, hash tables, heaps]
---

# Data Structures Expert

## Before Starting
1. What operations need to be fast? (insert, delete, search, range query)
2. Memory constraints?
3. Ordered or unordered data?

## Core Expertise Areas

### Linear Structures
Array: O(1) random access, O(n) insert/delete middle, cache-friendly.
Linked list: O(1) insert/delete at known position, O(n) search, no random access.
Stack: LIFO, O(1) push/pop. Applications: function calls, expression parsing, DFS.
Queue: FIFO, O(1) enqueue/dequeue. Applications: BFS, scheduling, buffers.
Deque: double-ended queue, O(1) both ends. Sliding window problems.

### Trees
BST: O(log n) avg search/insert/delete, O(n) worst case (degenerate).
AVL tree: height-balanced BST, O(log n) guaranteed, rotation on insert/delete.
Red-black tree: O(log n) guaranteed, fewer rotations than AVL, used in STL map.
B-tree: multi-way tree for disk storage, minimizes disk reads, used in databases.
Segment tree: range queries and updates, O(log n), build O(n).
Trie: prefix tree for strings, O(m) operations where m is string length.

### Heaps
Binary heap: complete binary tree, O(log n) insert/delete-max, O(1) peek.
Min-heap vs max-heap: heap property direction determines which is O(1) to access.
Fibonacci heap: O(1) amortized insert and decrease-key, O(log n) delete-min.
Applications: priority queue, Dijkstra, Prim, heap sort, k-th largest.

### Hash Tables
Hash function: maps key to index, good function minimizes collisions.
Collision resolution: chaining (linked list per bucket), open addressing (probing).
Load factor: ratio of elements to buckets, resize when exceeds threshold.
O(1) average insert/search/delete, O(n) worst case with many collisions.

### Union-Find
Disjoint set union: tracks connected components.
Path compression and union by rank: nearly O(1) amortized per operation.
Applications: Kruskal MST, cycle detection, dynamic connectivity.

## Best Practices
- Choose structure based on dominant operations in your use case
- Consider cache performance for large datasets
- Use lazy deletion where appropriate
- Understand amortized vs worst-case complexity

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Using linked list for random access | Use array or dynamic array instead |
| Hash table with bad hash function | Test distribution of hash values |
| BST degenerating to O(n) | Use balanced variant like AVL or RB tree |
| Segment tree off-by-one | Use 1-indexed and carefully define ranges |

## Related Skills
- algorithms-cs-expert
- python-expert
- java-expert
