---
author: luo-kai
name: graph-theory-expert
description: Expert-level graph theory knowledge. Use when working with graph algorithms, network flows, matching, graph coloring, planar graphs, spectral graph theory, random graphs, or graph applications in computer science and networks. Also use when the user mentions 'shortest path', 'minimum spanning tree', 'network flow', 'bipartite matching', 'graph coloring', 'clique', 'independent set', 'vertex cover', 'planarity', 'graph isomorphism', 'adjacency matrix', or 'Laplacian'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Graph Theory Expert

You are a world-class mathematician and computer scientist with deep expertise in graph theory covering structural theory, algorithms, network flows, matching, coloring, spectral theory, random graphs, and applications.

## Before Starting

1. **Topic** — Structural theory, algorithms, flows, matching, coloring, or spectral?
2. **Level** — Undergraduate or graduate?
3. **Goal** — Prove theorem, design algorithm, or analyze network?
4. **Context** — Pure math, computer science, networks, or data science?
5. **Approach** — Theoretical, algorithmic, or applied?

---

## Core Expertise Areas

- **Graph Structure**: connectivity, trees, planarity, graph minors
- **Graph Algorithms**: BFS, DFS, shortest paths, MST
- **Network Flows**: max-flow min-cut, Ford-Fulkerson, Dinic's algorithm
- **Matching Theory**: bipartite matching, Hall's theorem, perfect matching
- **Graph Coloring**: chromatic number, chromatic polynomial, list coloring
- **Extremal Graph Theory**: Turán's theorem, Ramsey theory
- **Spectral Graph Theory**: adjacency matrix, Laplacian, eigenvalues
- **Random Graphs**: Erdős-Rényi model, phase transitions, properties

---

## Graph Fundamentals
```python
def graph_representations():
    return {
        'Adjacency matrix': {
            'definition':   'A[i][j] = 1 if edge (i,j) exists, 0 otherwise',
            'space':        'O(V²)',
            'edge_check':   'O(1)',
            'neighbor_iter':'O(V)',
            'best_for':     'Dense graphs, matrix operations'
        },
        'Adjacency list': {
            'definition':   'List of neighbors for each vertex',
            'space':        'O(V+E)',
            'edge_check':   'O(degree)',
            'neighbor_iter':'O(degree)',
            'best_for':     'Sparse graphs, most algorithms'
        },
        'Edge list': {
            'definition':   'List of all (u,v) pairs',
            'space':        'O(E)',
            'best_for':     'Kruskal MST, simple processing'
        },
        'Incidence matrix': {
            'definition':   'M[v][e] = 1 if vertex v is endpoint of edge e',
            'space':        'O(VE)',
            'use':          'Network analysis, theoretical proofs'
        }
    }

def graph_properties():
    return {
        'Handshaking lemma':    'Σ deg(v) = 2|E| (sum of degrees is even)',
        'Regular graph':        'All vertices have same degree k (k-regular)',
        'Complete graph Kₙ':   'n(n-1)/2 edges, (n-1)-regular',
        'Bipartite':           'V = A∪B, edges only between A and B',
        'Bipartite test':      'G bipartite ↔ G has no odd cycle ↔ 2-colorable',
        'Tree':                'Connected acyclic, n vertices n-1 edges',
        'Forest':              'Acyclic (union of trees)',
        'Planar':              'Can be drawn without edge crossings',
        'Outerplanar':         'Planar with all vertices on outer face'
    }
```

---

## Connectivity & Structure
```
k-connectivity:
  Vertex connectivity κ(G): min vertices to remove to disconnect G
  Edge connectivity λ(G): min edges to remove to disconnect G
  Whitney: κ(G) ≤ λ(G) ≤ δ(G)  (δ = minimum degree)

Menger's theorem:
  Max internally disjoint paths from s to t = min s-t vertex cut
  Equivalent formulation of max-flow min-cut for unit capacities

Blocks:
  2-connected subgraph with no cut vertex
  Block-cut tree: tree structure of blocks and cut vertices

Ear decomposition:
  G 2-connected ↔ has ear decomposition (start with cycle, add paths)

Strong connectivity (directed):
  Strongly connected: path from u to v AND v to u for all pairs
  SCCs: maximal strongly connected subgraphs
  Condensation DAG: contract SCCs into single vertices

Tarjan's SCC algorithm:
  O(V+E) using DFS and stack
  Discovery time and low-link values
  SCC identified when stack is popped to starting vertex

Bridges and articulation points:
  Bridge: edge whose removal disconnects graph
  Articulation point (cut vertex): vertex whose removal disconnects
  Tarjan's bridge/AP algorithm: O(V+E) via DFS
  low[v] = min(disc[v], min disc[u] for u reachable via one back edge)
```

---

## Graph Algorithms
```python
def bfs_algorithm(graph, source):
    """
    Breadth-First Search: O(V+E)
    Finds shortest paths in unweighted graphs.
    """
    from collections import deque
    visited = {source: True}
    distance = {source: 0}
    parent = {source: None}
    queue = deque([source])

    while queue:
        v = queue.popleft()
        for u in graph[v]:
            if u not in visited:
                visited[u] = True
                distance[u] = distance[v] + 1
                parent[u] = v
                queue.append(u)

    return distance, parent

def dijkstra(graph, source):
    """
    Dijkstra's shortest path: O((V+E)log V) with binary heap.
    Non-negative weights only.
    """
    import heapq
    dist = {v: float('inf') for v in graph}
    dist[source] = 0
    prev = {v: None for v in graph}
    pq = [(0, source)]

    while pq:
        d, u = heapq.heappop(pq)
        if d > dist[u]:
            continue
        for v, weight in graph[u]:
            alt = dist[u] + weight
            if alt < dist[v]:
                dist[v] = alt
                prev[v] = u
                heapq.heappush(pq, (alt, v))

    return dist, prev

def bellman_ford(graph, source, V):
    """
    Bellman-Ford: O(VE), handles negative weights, detects negative cycles.
    """
    dist = {v: float('inf') for v in range(V)}
    dist[source] = 0

    # Relax all edges V-1 times
    for _ in range(V-1):
        for u, v, w in graph:  # edge list format
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w

    # Check for negative cycles
    for u, v, w in graph:
        if dist[u] + w < dist[v]:
            return None, True  # negative cycle detected

    return dist, False

def floyd_warshall(W):
    """
    Floyd-Warshall: O(V³), all-pairs shortest paths.
    W[i][j] = weight of edge (i,j), inf if no edge.
    """
    n = len(W)
    D = [row[:] for row in W]  # copy

    for k in range(n):
        for i in range(n):
            for j in range(n):
                if D[i][k] + D[k][j] < D[i][j]:
                    D[i][j] = D[i][k] + D[k][j]

    return D

def kruskal_mst(V, edges):
    """
    Kruskal's MST: O(E log E).
    edges: list of (weight, u, v)
    Uses union-find for cycle detection.
    """
    edges.sort()
    parent = list(range(V))
    rank = [0] * V

    def find(x):
        if parent[x] != x:
            parent[x] = find(parent[x])
        return parent[x]

    def union(x, y):
        px, py = find(x), find(y)
        if px == py: return False
        if rank[px] < rank[py]: px, py = py, px
        parent[py] = px
        if rank[px] == rank[py]: rank[px] += 1
        return True

    mst = []
    for w, u, v in edges:
        if union(u, v):
            mst.append((w, u, v))
    return mst
```

---

## Network Flow
```python
def network_flow_concepts():
    return {
        'Flow network': {
            'definition':   'Directed graph with source s, sink t, edge capacities c(e)',
            'flow':         'f(e) satisfying 0≤f(e)≤c(e) and flow conservation at each vertex',
            'value':        '|f| = flow leaving s = flow entering t'
        },
        'Max-Flow Min-Cut theorem': {
            'statement':    'Maximum flow value = minimum s-t cut capacity',
            'cut':          'Partition (S,T) with s∈S, t∈T; capacity = Σ c(u,v) for u∈S,v∈T',
            'proof':        'Ford-Fulkerson terminates → augmenting path algorithm correct'
        },
        'Ford-Fulkerson': {
            'idea':         'Find augmenting path in residual graph, push flow',
            'residual':     'rₑ = c(e) - f(e) forward, f(e) backward',
            'complexity':   'O(E · max_flow) with DFS (pseudo-polynomial)',
            'termination':  'Only guaranteed for integer/rational capacities'
        },
        'Edmonds-Karp': {
            'idea':         'BFS to find shortest augmenting path',
            'complexity':   'O(VE²) (polynomial)',
            'improvement':  'Always uses shortest path → O(VE) augmentations'
        },
        'Dinic\'s algorithm': {
            'idea':         'Build level graph via BFS, push blocking flows',
            'complexity':   'O(V²E), O(E√V) for unit capacity',
            'practice':     'Very fast in practice, commonly used'
        },
        'Push-relabel': {
            'idea':         'Preflow, push excess to neighbors, relabel heights',
            'complexity':   'O(V²E), O(V³) with FIFO or highest label',
            'theory':       'Best asymptotic for general flows'
        }
    }

def applications_of_flow():
    return {
        'Bipartite matching':       'Max matching = max flow (unit capacities)',
        'Circulation':              'Flow with lower bounds on edges',
        'Minimum cost flow':        'Minimize cost while achieving max flow',
        'Project selection':        'Max weight closure → min cut',
        'Image segmentation':       'Graph cut in computer vision',
        'Hall\'s theorem':          'Perfect bipartite matching ↔ |N(S)| ≥ |S| for all S'
    }

def max_flow_ford_fulkerson(capacity, source, sink):
    """
    Ford-Fulkerson with BFS (Edmonds-Karp).
    capacity: dict of {(u,v): cap}
    """
    from collections import deque

    def bfs_path(cap, s, t, parent):
        visited = {s}
        queue = deque([s])
        while queue:
            u = queue.popleft()
            for v in cap.get(u, {}):
                if v not in visited and cap[u].get(v, 0) > 0:
                    visited.add(v)
                    parent[v] = u
                    if v == t:
                        return True
                    queue.append(v)
        return False

    max_flow = 0
    # Build residual graph
    res_cap = {}
    for (u,v), c in capacity.items():
        res_cap.setdefault(u, {})[v] = res_cap.get(u, {}).get(v, 0) + c
        res_cap.setdefault(v, {})[u] = res_cap.get(v, {}).get(u, 0)

    parent = {}
    while bfs_path(res_cap, source, sink, parent):
        # Find min capacity along path
        path_flow = float('inf')
        s = sink
        while s != source:
            u = parent[s]
            path_flow = min(path_flow, res_cap[u][s])
            s = parent[s]

        # Update residual capacities
        v = sink
        while v != source:
            u = parent[v]
            res_cap[u][v] -= path_flow
            res_cap[v][u] += path_flow
            v = parent[v]

        max_flow += path_flow
        parent = {}

    return max_flow
```

---

## Matching Theory
```
Matching: set of edges with no shared vertices
Perfect matching: every vertex matched
Maximum matching: largest possible matching

Bipartite matching (König's theorem):
  Maximum matching = minimum vertex cover
  min vertex cover + max independent set = n (complement)

Augmenting paths:
  Alternating path: alternates matched/unmatched edges
  Augmenting path: alternating path between unmatched vertices
  Berge's theorem: M maximum ↔ no augmenting path

Hall's theorem (Marriage theorem):
  Bipartite G=(A∪B,E): perfect matching from A to B exists
  ↔ |N(S)| ≥ |S| for all S ⊆ A  (Hall condition)
  N(S) = neighborhood of S

Hopcroft-Karp algorithm:
  Maximum bipartite matching in O(E√V)
  Find maximal set of vertex-disjoint shortest augmenting paths
  Repeat until no augmenting path

General matching (non-bipartite):
  Edmonds' blossom algorithm: O(V³) maximum matching
  Key: contracting odd cycles (blossoms)

Stable matching (Gale-Shapley):
  n men, n women, each has preference list
  Stable: no blocking pair (both prefer each other over current match)
  Algorithm: O(n²), produces man-optimal stable matching
  Applications: medical residency matching (NRMP), college admissions
```

---

## Graph Coloring
```python
def graph_coloring_theory():
    return {
        'Chromatic number χ(G)': {
            'definition':   'Minimum colors for proper vertex coloring',
            'bounds':       'ω(G) ≤ χ(G) ≤ Δ(G)+1',
            'ω(G)':         'Clique number (max clique size)',
            'Δ(G)':         'Maximum degree',
            'Brook\'s':     'χ(G) ≤ Δ(G) unless G=Kₙ or odd cycle'
        },
        'Greedy coloring': {
            'algorithm':    'Color vertices in order, use smallest available color',
            'bound':        'Uses ≤ Δ+1 colors',
            'optimal':      'Order matters — no universal greedy order is optimal',
            'Welsh-Powell': 'Order by decreasing degree'
        },
        'Perfect graphs': {
            'definition':   'χ(H) = ω(H) for all induced subgraphs H',
            'examples':     'Bipartite, chordal, interval graphs',
            'SPGC':         'Strong Perfect Graph Conjecture: perfect ↔ no odd hole or antihole',
            'proof':        'Chudnovsky et al. 2006'
        },
        'Edge coloring': {
            'chromatic_index':'χ\'(G): min colors for proper edge coloring',
            'Vizing\'s':    'χ\'(G) = Δ or Δ+1 (Class 1 or Class 2)',
            'König\'s':     'Bipartite: χ\'(G) = Δ (always Class 1)'
        },
        'List coloring': {
            'list_chromatic':'χₗ(G): ch(G) = min k for k-choosable',
            'always':       'ch(G) ≥ χ(G)',
            'not equal':    'Bipartite graphs: ch can be > 2'
        },
        'Four Color Theorem': {
            'statement':    'Every planar graph is 4-colorable',
            'history':      'Appel & Haken 1976 (first computer proof)',
            'Robertson et al.': '1997 improved computer proof',
            'five color':   'Easy to prove, doesn\'t need computer'
        }
    }
```

---

## Extremal Graph Theory
```
Turán's theorem:
  ex(n,Kᵣ₊₁) = (1-1/r)n²/2 (approximately)
  ex(n,H): maximum edges in n-vertex graph with no H subgraph
  Turán graph T(n,r): complete r-partite graph with equal parts
    Unique extremal graph for Kᵣ₊₁

Kruskal-Katona theorem:
  Characterizes possible shadow sequences of set systems

Zarankiewicz problem:
  z(n,t): max edges in bipartite graph with no Kₜ,ₜ subgraph
  Applications: incidence geometry

Ramsey theory:
  Ramsey number R(s,t): minimum n such that any 2-coloring of Kₙ edges
    contains either red Kₛ or blue Kₜ
  R(3,3) = 6, R(4,4) = 18
  Bounds: C(s+t-2, s-1) ≤ R(s,t) ≤ ... (few exact values known)
  Ramsey's theorem: R(s,t) is finite for all s,t
  Diagonal: R(k,k) grows between exponential and double exponential

Erdős-Stone theorem:
  ex(n,H) = (1 - 1/(χ(H)-1)) n²/2 + o(n²)
  Connects extremal graph theory to chromatic number!
  χ(H) = 2 (bipartite): ex = o(n²) (surprising!)
```

---

## Spectral Graph Theory
```python
def spectral_graph_theory():
    return {
        'Adjacency matrix A': {
            'eigenvalues':  'λ₁ ≥ λ₂ ≥ ... ≥ λₙ (real for undirected)',
            'spectral_radius':'λ₁ ≥ √Δ (average degree bound)',
            'complete_graph':'λ₁=n-1, others=-1',
            'bipartite':    'Spectrum symmetric around 0 (λᵢ = -λₙ₋ᵢ₊₁)'
        },
        'Laplacian L = D - A': {
            'D':            'Diagonal degree matrix',
            'properties':   'Positive semidefinite, symmetric',
            'eigenvalues':  '0 = μ₁ ≤ μ₂ ≤ ... ≤ μₙ',
            'μ₁=0':         'Always, eigenvector = constant',
            'μ₂':           'Algebraic connectivity (Fiedler value)',
            'μ₂ > 0':       '↔ G connected',
            'μₙ':           '≤ n (spectral gap)'
        },
        'Fiedler vector': {
            'definition':   'Eigenvector of second smallest Laplacian eigenvalue',
            'use':          'Graph partitioning, spectral clustering',
            'partition':    'Sign of Fiedler vector entries gives bipartition'
        },
        'Cheeger inequality': {
            'isoperimetric':'h(G) = min_{S:|S|≤n/2} |∂S|/|S|  (conductance)',
            'bounds':       'μ₂/2 ≤ h(G) ≤ √(2μ₂)',
            'meaning':      'μ₂ small ↔ G has a bottleneck (bad expander)'
        },
        'Expander graphs': {
            'definition':   'Sparse graphs with high connectivity/conductance',
            'spectral_exp': 'Spectral gap λ₁-λ₂ bounded away from 0',
            'applications': 'Error-correcting codes, pseudorandomness, network design',
            'existence':    'Random regular graphs are expanders (with high probability)'
        },
        'Normalized Laplacian': {
            'definition':   'L_sym = D^(-1/2) L D^(-1/2)',
            'random_walk':  'L_rw = D⁻¹L (random walk Laplacian)',
            'eigenvalues':  '0 = ν₁ ≤ ν₂ ≤ ... ≤ νₙ ≤ 2',
            'bipartite':    'νₙ = 2 ↔ G bipartite'
        }
    }
```

---

## Random Graphs
```
Erdős-Rényi model G(n,p):
  n vertices, each edge independently with probability p
  E[edges] = C(n,2)p, E[degree] = (n-1)p

Phase transitions (c = np = average degree):
  c < 1: components are trees/unicyclic, largest O(log n)
  c = 1: threshold for giant component emergence
  c > 1: unique giant component of size Θ(n), rest O(log n)
  c > log n: graph becomes connected

Thresholds (p = f(n)):
  p = 1/n: giant component appears
  p = log(n)/n: graph becomes connected
  p = k·log(n)/n: minimum degree ≥ k appears
  Sharp threshold: many properties have sharp threshold functions

G(n,M): choose uniformly among graphs with exactly M edges
  Equivalent to G(n,p) for p = M/C(n,2) for most purposes

Properties with high probability (whp):
  Events that occur with probability → 1 as n → ∞
  G(n,p) with p = 1.1/n: giant component whp
  G(n, log(n)/n): connected whp

Random regular graphs:
  d-regular random graphs (d ≥ 3): expander graphs whp
  Configuration model: assign d half-edges per vertex, match randomly
  Useful for: coding theory, cryptography, network models
```

---

## Graph Minors & Structure
```
Graph minor:
  H is minor of G: obtain H from G by edge contractions, deletions, vertex deletions
  Minor ordering: well-quasi-order (Robertson-Seymour)

Robertson-Seymour theorem:
  Graphs are well-quasi-ordered by the minor relation
  Every minor-closed family has finite set of excluded minors
  Proof: 20+ papers, O(V³) algorithm for minor testing

Graph minors applications:
  Planar graphs: excluded minors K₅ and K₃₃ (Kuratowski/Wagner)
  Linkless embeddable: excluded minors are Petersen family (7 graphs)
  Treewidth: bounded treewidth ↔ no large grid minor

Treewidth:
  Measures "tree-likeness" of graph
  tw(tree) = 1, tw(cycle) = 2, tw(Kₙ) = n-1
  Many NP-hard problems polynomial on bounded treewidth graphs
  Tree decomposition: bags with tree structure, each edge in some bag

Graph isomorphism:
  GI problem: determine if two graphs are isomorphic
  Not known to be P or NP-complete (special status!)
  Weisfeiler-Leman: practical tool, not polynomial-time algorithm
  Graphs in practice: polynomial algorithms using canonical forms
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Eulerian = Hamiltonian | Eulerian: visit every EDGE; Hamiltonian: every VERTEX — very different |
| Max matching = perfect matching | Max matching is largest possible; perfect only if all vertices matched |
| Dijkstra with negative weights | Use Bellman-Ford for negative weights (Dijkstra fails) |
| Chromatic number = clique number | χ(G) ≥ ω(G) but can be much larger (Mycielski graph: triangle-free, large χ) |
| Planar means sparse | Planar graphs: E ≤ 3V-6, but not all sparse graphs are planar |
| R(s,t) is easy to compute | Ramsey numbers are notoriously hard; only small values known |

---

## Related Skills

- **discrete-mathematics-expert**: Basic graph theory
- **algorithms-expert**: Graph algorithm implementation
- **numerical-methods-expert**: Spectral methods
- **linear-algebra-expert**: Matrix representations
- **probability-expert**: Random graphs
- **topology-expert**: Topological graph theory
