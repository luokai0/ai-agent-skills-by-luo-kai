---
author: luo-kai
name: algorithms-expert
description: Expert-level algorithms and data structures. Use when implementing or explaining sorting, searching, graph algorithms (BFS, DFS, Dijkstra, A*), dynamic programming, greedy algorithms, trees, heaps, hash maps, or Big O analysis. Also use when the user mentions 'Big O', 'BFS', 'DFS', 'dynamic programming', 'binary search', 'graph algorithm', 'time complexity', 'space complexity', or 'leetcode'.
license: MIT
metadata:
  author: luokai0
  version: "1.0"
  category: coding
---

# Algorithms & Data Structures Expert

You are an expert in algorithms and data structures with deep knowledge of time/space complexity, problem-solving patterns, and practical implementation across languages.

## Before Starting

1. **Problem type** — sorting, searching, graph, DP, greedy, string, math?
2. **Language** — Python, JavaScript, Go, Java, C++?
3. **Constraints** — time limit, space limit, input size?
4. **Goal** — solve a specific problem, understand a concept, optimize existing code?
5. **Level** — learning fundamentals or optimizing for interviews/production?

---

## Core Expertise Areas

- **Complexity analysis**: Big O time and space, amortized analysis, best/worst/average case
- **Sorting**: QuickSort, MergeSort, HeapSort, TimSort, counting/radix sort
- **Searching**: binary search, BFS, DFS, A*, bidirectional search
- **Graph algorithms**: Dijkstra, Bellman-Ford, Floyd-Warshall, Kruskal, Prim, topological sort
- **Dynamic programming**: memoization, tabulation, space optimization, common patterns
- **Data structures**: arrays, linked lists, stacks, queues, heaps, trees, tries, graphs, union-find
- **String algorithms**: KMP, Rabin-Karp, Z-algorithm, suffix arrays, edit distance
- **Problem patterns**: two pointers, sliding window, divide and conquer, backtracking

---

## Key Patterns & Code

### Complexity Reference
```
Data Structure Operations:
  Array:          Access O(1)  Search O(n)  Insert O(n)  Delete O(n)
  Linked List:    Access O(n)  Search O(n)  Insert O(1)  Delete O(1)
  Hash Map:       Access O(1)  Search O(1)  Insert O(1)  Delete O(1)  [avg]
  Binary Search Tree: All O(log n) average, O(n) worst
  Balanced BST:   All O(log n) guaranteed
  Heap:           Insert O(log n)  Extract-min O(log n)  Peek O(1)
  Trie:           Insert/Search O(m) where m = key length

Sorting Algorithms:
  QuickSort:   O(n log n) avg,  O(n^2) worst,   O(log n) space  — in-place, not stable
  MergeSort:   O(n log n) all,  O(n) space       — stable, divide and conquer
  HeapSort:    O(n log n) all,  O(1) space       — in-place, not stable
  TimSort:     O(n log n) all,  O(n) space       — stable, Python/Java default
  CountSort:   O(n + k),        O(k) space       — integer keys only
  RadixSort:   O(nk),           O(n + k) space   — integer/string keys

Graph Algorithms:
  BFS:              O(V + E)  — shortest path (unweighted), level order
  DFS:              O(V + E)  — cycle detection, topological sort, connected components
  Dijkstra:         O((V + E) log V)  — shortest path (non-negative weights)
  Bellman-Ford:     O(VE)            — shortest path (negative weights)
  Floyd-Warshall:   O(V^3)           — all-pairs shortest path
  Kruskal MST:      O(E log E)       — minimum spanning tree
  Prim MST:         O((V + E) log V) — minimum spanning tree
```

### Binary Search — Template
```python
# Standard binary search
def binary_search(nums: list[int], target: int) -> int:
    left, right = 0, len(nums) - 1
    while left <= right:
        mid = left + (right - left) // 2  # avoid overflow
        if nums[mid] == target:
            return mid
        elif nums[mid] < target:
            left = mid + 1
        else:
            right = mid - 1
    return -1

# Find leftmost position (first occurrence)
def lower_bound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] < target:
            left = mid + 1
        else:
            right = mid
    return left

# Find rightmost position (last occurrence)
def upper_bound(nums: list[int], target: int) -> int:
    left, right = 0, len(nums)
    while left < right:
        mid = left + (right - left) // 2
        if nums[mid] <= target:
            left = mid + 1
        else:
            right = mid
    return left - 1

# Binary search on answer — when you can check feasibility
def min_days_to_bloom(bloomDay, m, k):
    def can_bloom(day):
        flowers = bouquets = 0
        for d in bloomDay:
            if d <= day:
                flowers += 1
                if flowers == k:
                    bouquets += 1
                    flowers = 0
            else:
                flowers = 0
        return bouquets >= m

    left, right = min(bloomDay), max(bloomDay)
    while left < right:
        mid = left + (right - left) // 2
        if can_bloom(mid):
            right = mid
        else:
            left = mid + 1
    return left if can_bloom(left) else -1
```

### Two Pointers & Sliding Window
```python
# Two pointers — sorted array, find pair with target sum
def two_sum_sorted(nums: list[int], target: int) -> tuple[int, int]:
    left, right = 0, len(nums) - 1
    while left < right:
        s = nums[left] + nums[right]
        if s == target:
            return (left, right)
        elif s < target:
            left += 1
        else:
            right -= 1
    return (-1, -1)

# Sliding window — longest substring without repeating chars
def length_of_longest_substring(s: str) -> int:
    char_index = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_index and char_index[char] >= left:
            left = char_index[char] + 1
        char_index[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len

# Sliding window — minimum window substring
from collections import Counter
def min_window(s: str, t: str) -> str:
    need = Counter(t)
    have = {}
    formed = 0
    required = len(need)
    left = 0
    best = (float('inf'), 0, 0)

    for right, char in enumerate(s):
        have[char] = have.get(char, 0) + 1
        if char in need and have[char] == need[char]:
            formed += 1
        while formed == required:
            if right - left + 1 < best[0]:
                best = (right - left + 1, left, right)
            left_char = s[left]
            have[left_char] -= 1
            if left_char in need and have[left_char] < need[left_char]:
                formed -= 1
            left += 1

    return '' if best[0] == float('inf') else s[best[1]:best[2]+1]
```

### Graph Algorithms
```python
from collections import deque
import heapq

# BFS — shortest path in unweighted graph
def bfs_shortest_path(graph: dict, start: int, end: int) -> int:
    if start == end:
        return 0
    visited = {start}
    queue = deque([(start, 0)])
    while queue:
        node, dist = queue.popleft()
        for neighbor in graph.get(node, []):
            if neighbor == end:
                return dist + 1
            if neighbor not in visited:
                visited.add(neighbor)
                queue.append((neighbor, dist + 1))
    return -1

# DFS — detect cycle in directed graph
def has_cycle(graph: dict, n: int) -> bool:
    WHITE, GRAY, BLACK = 0, 1, 2
    color = [WHITE] * n

    def dfs(node):
        color[node] = GRAY
        for neighbor in graph.get(node, []):
            if color[neighbor] == GRAY:
                return True  # back edge = cycle
            if color[neighbor] == WHITE and dfs(neighbor):
                return True
        color[node] = BLACK
        return False

    return any(dfs(i) for i in range(n) if color[i] == WHITE)

# Dijkstra — shortest path with non-negative weights
def dijkstra(graph: dict, start: int) -> dict:
    dist = {start: 0}
    heap = [(0, start)]  # (distance, node)

    while heap:
        d, node = heapq.heappop(heap)
        if d > dist.get(node, float('inf')):
            continue  # stale entry
        for neighbor, weight in graph.get(node, []):
            new_dist = d + weight
            if new_dist < dist.get(neighbor, float('inf')):
                dist[neighbor] = new_dist
                heapq.heappush(heap, (new_dist, neighbor))

    return dist

# Topological sort — Kahn's algorithm (BFS-based)
def topological_sort(n: int, edges: list[tuple]) -> list[int]:
    graph = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    queue = deque(i for i in range(n) if indegree[i] == 0)
    result = []
    while queue:
        node = queue.popleft()
        result.append(node)
        for neighbor in graph[node]:
            indegree[neighbor] -= 1
            if indegree[neighbor] == 0:
                queue.append(neighbor)

    return result if len(result) == n else []  # empty = cycle detected

# Union-Find (Disjoint Set Union)
class UnionFind:
    def __init__(self, n: int):
        self.parent = list(range(n))
        self.rank = [0] * n
        self.components = n

    def find(self, x: int) -> int:
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])  # path compression
        return self.parent[x]

    def union(self, x: int, y: int) -> bool:
        px, py = self.find(x), self.find(y)
        if px == py:
            return False  # already connected
        # Union by rank
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        self.components -= 1
        return True

    def connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
```

### Dynamic Programming — Core Patterns
```python
# Pattern 1: 1D DP — Fibonacci / Climbing Stairs
def climb_stairs(n: int) -> int:
    if n <= 2:
        return n
    prev2, prev1 = 1, 2
    for _ in range(3, n + 1):
        prev2, prev1 = prev1, prev2 + prev1
    return prev1

# Pattern 2: 2D DP — Longest Common Subsequence
def lcs(s1: str, s2: str) -> int:
    m, n = len(s1), len(s2)
    dp = [[0] * (n + 1) for _ in range(m + 1)]
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if s1[i-1] == s2[j-1]:
                dp[i][j] = dp[i-1][j-1] + 1
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
    return dp[m][n]

# Pattern 3: Knapsack — 0/1 Knapsack
def knapsack(weights: list[int], values: list[int], capacity: int) -> int:
    n = len(weights)
    dp = [0] * (capacity + 1)
    for i in range(n):
        # Iterate backwards to avoid using item twice
        for w in range(capacity, weights[i] - 1, -1):
            dp[w] = max(dp[w], dp[w - weights[i]] + values[i])
    return dp[capacity]

# Pattern 4: Interval DP — Burst Balloons
def max_coins(nums: list[int]) -> int:
    nums = [1] + nums + [1]
    n = len(nums)
    dp = [[0] * n for _ in range(n)]
    for length in range(2, n):
        for left in range(0, n - length):
            right = left + length
            for k in range(left + 1, right):
                dp[left][right] = max(
                    dp[left][right],
                    dp[left][k] + nums[left] * nums[k] * nums[right] + dp[k][right]
                )
    return dp[0][n - 1]

# Pattern 5: Memoization template
from functools import lru_cache

def solve_with_memo(n: int) -> int:
    @lru_cache(maxsize=None)
    def dp(state):
        if state == 0:
            return base_case
        # Try all choices
        return min(dp(state - choice) + cost for choice in choices if choice <= state)
    return dp(n)
```

### Trees — Essential Patterns
```python
from collections import deque
from typing import Optional

class TreeNode:
    def __init__(self, val=0, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

# Inorder traversal (iterative — avoids recursion limit)
def inorder(root: Optional[TreeNode]) -> list[int]:
    result, stack = [], []
    curr = root
    while curr or stack:
        while curr:
            stack.append(curr)
            curr = curr.left
        curr = stack.pop()
        result.append(curr.val)
        curr = curr.right
    return result

# Level order traversal (BFS)
def level_order(root: Optional[TreeNode]) -> list[list[int]]:
    if not root:
        return []
    result = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:  queue.append(node.left)
            if node.right: queue.append(node.right)
        result.append(level)
    return result

# Lowest Common Ancestor
def lca(root: Optional[TreeNode], p: TreeNode, q: TreeNode) -> Optional[TreeNode]:
    if not root or root == p or root == q:
        return root
    left  = lca(root.left, p, q)
    right = lca(root.right, p, q)
    if left and right:
        return root  # p and q are in different subtrees
    return left or right

# Validate BST
def is_valid_bst(root: Optional[TreeNode]) -> bool:
    def validate(node, min_val, max_val):
        if not node:
            return True
        if not (min_val < node.val < max_val):
            return False
        return (validate(node.left, min_val, node.val) and
                validate(node.right, node.val, max_val))
    return validate(root, float('-inf'), float('inf'))

# Trie
class Trie:
    def __init__(self):
        self.children = {}
        self.is_end = False

    def insert(self, word: str) -> None:
        node = self
        for char in word:
            if char not in node.children:
                node.children[char] = Trie()
            node = node.children[char]
        node.is_end = True

    def search(self, word: str) -> bool:
        node = self
        for char in word:
            if char not in node.children:
                return False
            node = node.children[char]
        return node.is_end

    def starts_with(self, prefix: str) -> bool:
        node = self
        for char in prefix:
            if char not in node.children:
                return False
            node = node.children[char]
        return True
```

### Heap Patterns
```python
import heapq

# Min heap — Python's heapq is a min heap
heap = []
heapq.heappush(heap, 3)
heapq.heappush(heap, 1)
heapq.heappush(heap, 2)
smallest = heapq.heappop(heap)  # 1

# Max heap — negate values
max_heap = []
heapq.heappush(max_heap, -3)
heapq.heappush(max_heap, -1)
largest = -heapq.heappop(max_heap)  # 3

# K largest elements
def k_largest(nums: list[int], k: int) -> list[int]:
    return heapq.nlargest(k, nums)

# K smallest elements
def k_smallest(nums: list[int], k: int) -> list[int]:
    return heapq.nsmallest(k, nums)

# Kth largest — O(n log k) with min heap of size k
def kth_largest(nums: list[int], k: int) -> int:
    heap = []
    for num in nums:
        heapq.heappush(heap, num)
        if len(heap) > k:
            heapq.heappop(heap)
    return heap[0]

# Merge k sorted lists
def merge_k_sorted(lists: list[list[int]]) -> list[int]:
    heap = []
    for i, lst in enumerate(lists):
        if lst:
            heapq.heappush(heap, (lst[0], i, 0))

    result = []
    while heap:
        val, i, j = heapq.heappop(heap)
        result.append(val)
        if j + 1 < len(lists[i]):
            heapq.heappush(heap, (lists[i][j+1], i, j+1))
    return result
```

### Backtracking Template
```python
# General backtracking template
def backtrack(state, choices, result):
    # Base case: valid complete solution
    if is_complete(state):
        result.append(state[:])
        return

    for choice in choices:
        if is_valid(state, choice):
            state.append(choice)       # make choice
            backtrack(state, choices, result)
            state.pop()                # undo choice

# Example: generate all permutations
def permutations(nums: list[int]) -> list[list[int]]:
    result = []
    used = [False] * len(nums)

    def backtrack(current):
        if len(current) == len(nums):
            result.append(current[:])
            return
        for i, num in enumerate(nums):
            if not used[i]:
                used[i] = True
                current.append(num)
                backtrack(current)
                current.pop()
                used[i] = False

    backtrack([])
    return result

# Example: N-Queens
def solve_n_queens(n: int) -> list[list[str]]:
    result = []
    cols = set()
    diag1 = set()  # row - col
    diag2 = set()  # row + col
    board = [['.' ] * n for _ in range(n)]

    def backtrack(row):
        if row == n:
            result.append([''.join(r) for r in board])
            return
        for col in range(n):
            if col in cols or (row - col) in diag1 or (row + col) in diag2:
                continue
            cols.add(col)
            diag1.add(row - col)
            diag2.add(row + col)
            board[row][col] = 'Q'
            backtrack(row + 1)
            cols.remove(col)
            diag1.remove(row - col)
            diag2.remove(row + col)
            board[row][col] = '.'

    backtrack(0)
    return result
```

### Problem-Solving Framework
```
Step 1: Understand (2 min)
  - Restate the problem in your own words
  - Identify input/output types and constraints
  - Ask: what are the edge cases?

Step 2: Examples (2 min)
  - Work through 2-3 examples manually
  - Include edge cases: empty input, single element, duplicates

Step 3: Brute Force (2 min)
  - State the naive O(n^2) or O(2^n) solution
  - Explain why it is too slow

Step 4: Optimize (5 min)
  - Identify the bottleneck
  - Apply a technique: hash map, two pointers, DP, sorting, heap
  - State new time and space complexity

Step 5: Implement (10 min)
  - Write clean, readable code
  - Use meaningful variable names
  - Handle edge cases

Step 6: Test (3 min)
  - Trace through your examples
  - Test edge cases: empty, single, max size
  - Check for off-by-one errors

Pattern Recognition:
  Use hash map when:       need O(1) lookup, counting, two-sum style
  Use two pointers when:   sorted array, palindrome, container problem
  Use sliding window when: subarray/substring with constraint
  Use BFS when:            shortest path, level-by-level, unweighted
  Use DFS when:            explore all paths, tree traversal, cycle detection
  Use DP when:             overlapping subproblems, optimal substructure
  Use greedy when:         local optimal = global optimal, interval problems
  Use heap when:           k-th element, top-k, streaming median
  Use union-find when:     connected components, cycle detection, MST
  Use trie when:           prefix matching, word search, autocomplete
```

---

## Best Practices

- Always analyze time AND space complexity before coding
- Start with brute force and explain trade-offs before optimizing
- Draw out examples on paper/whiteboard before writing code
- Use mid = left + (right - left) // 2 to avoid integer overflow
- In Python use collections.deque for O(1) popleft, not list.pop(0)
- Prefer iterative DFS over recursive to avoid stack overflow on large inputs
- Always handle edge cases: empty input, single element, all same values
- Name variables clearly: left/right not i/j for two pointers

---

## Common Pitfalls

| Pitfall | Problem | Fix |
|---|---|---|
| Integer overflow | mid = (left + right) // 2 overflows | Use left + (right - left) // 2 |
| Modifying list while iterating | Skips elements or crashes | Iterate over copy or use index |
| Off-by-one in binary search | Infinite loop or wrong result | Use invariant: left <= right |
| Not handling empty/null input | Runtime error | Check edge cases first |
| Exponential recursion without memo | TLE on overlapping subproblems | Add memoization or use tabulation |
| Wrong BFS vs DFS choice | Finds path but not shortest | Use BFS for shortest unweighted path |
| Mutating input | Breaks test cases, side effects | Work on copy or document mutation |
| Incorrect base case in DP | Wrong results for small inputs | Verify base cases manually |

---

## Related Skills

- **python-expert**: For Python-specific algorithm implementation
- **concurrency-expert**: For parallel algorithm patterns
- **system-design**: For applying algorithms in system design
- **rust-expert**: For high-performance algorithm implementation in Rust
- **performance-optimization**: For profiling and optimizing algorithms