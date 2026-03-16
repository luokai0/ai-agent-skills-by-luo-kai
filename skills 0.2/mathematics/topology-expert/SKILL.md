---
name: topology-expert
description: Expert-level topology knowledge. Use when working with topological spaces, continuity, compactness, connectedness, metric spaces, homeomorphisms, fundamental groups, homology, manifolds, or algebraic topology. Also use when the user mentions 'open set', 'closed set', 'compactness', 'connectedness', 'homeomorphism', 'homotopy', 'fundamental group', 'covering space', 'manifold', 'homology', 'Euler characteristic', or 'topological invariant'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Topology Expert

You are a world-class mathematician with deep expertise in point-set topology, metric spaces, algebraic topology, differential topology, and the classification of topological spaces.

## Before Starting

1. **Topic** — Point-set, metric spaces, algebraic topology, or differential topology?
2. **Level** — Undergraduate or graduate?
3. **Goal** — Prove theorem, solve problem, or understand concept?
4. **Context** — Pure math, physics, or data science (TDA)?
5. **Approach** — General topology or specific spaces (manifolds, surfaces)?

---

## Core Expertise Areas

- **Point-Set Topology**: open/closed sets, bases, subspaces, quotient spaces
- **Metric Spaces**: convergence, completeness, compactness, Baire category
- **Continuity & Homeomorphisms**: topological equivalence, invariants
- **Compactness**: Heine-Borel, sequential compactness, Tychonoff
- **Connectedness**: path-connectedness, components, intermediate value
- **Algebraic Topology**: fundamental group, covering spaces, homology
- **Manifolds**: surfaces, classification, smooth structures
- **Applications**: TDA, persistent homology, topological data analysis

---

## Topological Spaces
```
Topological space (X, τ):
  X = set of points
  τ = collection of open sets (topology on X)

Axioms for τ:
  1. ∅ ∈ τ and X ∈ τ
  2. Arbitrary unions: {Uα} ⊆ τ → ∪Uα ∈ τ
  3. Finite intersections: U,V ∈ τ → U∩V ∈ τ

Closed sets: complements of open sets
  ∅, X are both open and closed
  Finite unions of closed sets are closed
  Arbitrary intersections of closed sets are closed

Examples of topologies:
  Discrete topology: τ = P(X) (all subsets open)
  Indiscrete topology: τ = {∅, X}  (coarsest)
  Euclidean: standard open sets in ℝⁿ (usual topology)
  Subspace: if A ⊆ X, τ_A = {U∩A: U∈τ}
  Product: X×Y with basis {U×V: U∈τX, V∈τY}
  Quotient: X/~ where U open ↔ π⁻¹(U) open in X

Basis for topology:
  B is a basis if: covers X, B₁∩B₂ contains basis element around each point
  τ = all unions of elements of B
  ℝ: basis = open intervals (a,b)
  ℝⁿ: basis = open balls B(x,r)

Closure and interior:
  cl(A) = smallest closed set containing A = ∩{C: C closed, A⊆C}
  int(A) = largest open set contained in A = ∪{U: U open, U⊆A}
  boundary: ∂A = cl(A) \ int(A)
  Dense: cl(A) = X
  Nowhere dense: int(cl(A)) = ∅
```

---

## Metric Spaces
```
Metric space (X, d):
  d: X×X → [0,∞) satisfying:
  1. d(x,y) = 0 ↔ x = y  (positive definite)
  2. d(x,y) = d(y,x)  (symmetry)
  3. d(x,z) ≤ d(x,y) + d(y,z)  (triangle inequality)

Topology from metric:
  Open ball: B(x,r) = {y: d(x,y) < r}
  Open set: U open ↔ every point has open ball contained in U
  All metric spaces are Hausdorff (T2) and normal (T4)

Convergence in metric spaces:
  xₙ → x: d(xₙ,x) → 0
  Cauchy sequence: ∀ε>0 ∃N: m,n>N → d(xₘ,xₙ) < ε
  Complete: every Cauchy sequence converges
  Examples: ℝⁿ complete, ℚ not complete

Important metric spaces:
  ℝⁿ: Euclidean metric d(x,y) = √Σ(xᵢ-yᵢ)²
  C[a,b]: supremum metric d(f,g) = sup|f(x)-g(x)|  (complete)
  ℓ²: sequences with Σxᵢ² < ∞, d² = Σ(xᵢ-yᵢ)²  (Hilbert space)
  Discrete metric: d(x,y) = 0 if x=y, 1 if x≠y

Baire Category Theorem:
  Complete metric space (or locally compact Hausdorff):
  Countable intersection of dense open sets is dense
  X cannot be written as countable union of nowhere dense sets
  Applications: existence proofs, continuous nowhere differentiable functions

Banach fixed point theorem:
  T: X→X contraction (d(Tx,Ty) ≤ cd(x,y), c<1) on complete metric space
  → Unique fixed point, xₙ = Tⁿx₀ converges to it
  Applications: existence of ODEs, iterative methods
```

---

## Continuity & Homeomorphisms
```
Continuous function f: X→Y:
  Equivalent definitions:
  1. Preimage of open set is open: f⁻¹(V) open ∀V open in Y
  2. Preimage of closed set is closed
  3. Sequential continuity: xₙ→x → f(xₙ)→f(x)  (metric spaces)
  4. ε-δ definition (metric spaces)

Homeomorphism:
  f: X→Y bijective, f continuous, f⁻¹ continuous
  X and Y are homeomorphic (X ≅ Y): topologically identical
  Key insight: topology studies properties preserved under homeomorphism

Topological invariants (preserved by homeomorphism):
  Compactness, connectedness, path-connectedness
  Hausdorff property, metrizability
  Fundamental group, homology groups
  Euler characteristic
  NOT: distances, angles, areas, being a manifold of specific dimension

Examples of homeomorphic spaces:
  (0,1) ≅ ℝ  (via x↦tan(π(x-1/2)))
  Open disk ≅ ℝ²
  Circle ≅ boundary of square
  Coffee cup ≅ donut (torus) — one hole each!
  NOT: circle ≇ line segment (circle has no endpoints)
  NOT: sphere ≇ torus (different homology)

Quotient spaces:
  X/~ identifies equivalent points
  [0,1]/(0~1) ≅ S¹ (circle)
  [0,1]²/(boundary) ≅ S² (sphere)
  Möbius band: [0,1]×[0,1] with (0,y)~(1,1-y)
  Torus: [0,1]² with (x,0)~(x,1) and (0,y)~(1,y)
  Klein bottle: (x,0)~(x,1) and (0,y)~(1,1-y)  (non-orientable)
  RP²: sphere with antipodal points identified
```

---

## Compactness
```
Compact space:
  Every open cover has a finite subcover
  U₁∪U₂∪...=X → finitely many Uᵢ cover X

Heine-Borel theorem (ℝⁿ):
  A ⊆ ℝⁿ compact ↔ A closed and bounded
  ↔ every sequence has convergent subsequence (sequential compactness)

Properties of compact spaces:
  Compact ⊆ Hausdorff → closed
  Continuous image of compact set is compact
  Continuous f: compact → ℝ attains max and min (EVT)
  Compact metric space: complete and totally bounded
  Product of compact spaces is compact (Tychonoff's theorem)

Tychonoff's theorem:
  Arbitrary product of compact spaces is compact
  Proof uses Axiom of Choice (actually equivalent to AC)

Sequential compactness:
  Every sequence has a convergent subsequence
  In metric spaces: equivalent to compactness
  Bolzano-Weierstrass: bounded sequence in ℝⁿ has convergent subsequence

Local compactness:
  Every point has compact neighborhood
  ℝⁿ locally compact (but not compact)
  One-point compactification: X* = X ∪ {∞}  (Alexandroff)
```

---

## Connectedness
```
Connected space:
  Cannot be written as union of two disjoint nonempty open sets
  Equivalently: only clopen (open and closed) sets are ∅ and X

Connected subsets of ℝ:
  A ⊆ ℝ connected ↔ A is an interval

Intermediate Value Theorem (topological form):
  f: X→ℝ continuous, X connected
  f takes every value between f(a) and f(b)

Path-connectedness:
  Path: continuous γ: [0,1] → X
  Path-connected: any two points connected by path
  Path-connected → connected (but not conversely!)
  Counter-example: topologist's sine curve {(x,sin(1/x)): x>0} ∪ {(0,0)}

Connected components:
  Maximal connected subsets (partition X)
  Number of components: topological invariant

Local connectedness:
  Every point has arbitrarily small connected neighborhoods
  ℝⁿ locally connected

Simply connected:
  Path-connected + every loop can be contracted to a point
  π₁(X) = {e} (trivial fundamental group)
  ℝⁿ, spheres Sⁿ (n≥2) are simply connected
  Circle S¹, torus are NOT simply connected
```

---

## Algebraic Topology

### Fundamental Group
```
Homotopy: continuous deformation between paths
  f,g: [0,1]→X paths with same endpoints
  Homotopic: F(s,0)=f(s), F(s,1)=g(s), F(0,t)=x₀, F(1,t)=x₁

Fundamental group π₁(X, x₀):
  Elements: homotopy classes of loops based at x₀
  Operation: concatenation of loops [f]·[g] = [f*g]
  Identity: constant loop [cx₀]
  Inverse: reverse traversal [f⁻¹]

Key fundamental groups:
  π₁(ℝⁿ) = {e}  (contractible)
  π₁(S¹) = ℤ   (winding number)
  π₁(S²) = {e}  (simply connected)
  π₁(T²) = ℤ×ℤ  (torus)
  π₁(RP²) = ℤ/2ℤ
  π₁(figure eight) = F₂ (free group on 2 generators)

Van Kampen's theorem:
  X = U ∪ V (open, path-connected, U∩V path-connected)
  π₁(X) = π₁(U) *_{π₁(U∩V)} π₁(V)  (amalgamated free product)

Covering spaces:
  p: X̃ → X continuous, every x has evenly covered neighborhood
  Fundamental groups related: p₊: π₁(X̃) → π₁(X) injective
  Universal cover X̃: simply connected cover
  π₁(X) acts on fiber p⁻¹(x) freely and transitively
```

### Homology
```
Simplicial homology:
  Triangulate space, compute chain groups and boundary maps
  Hₙ(X) = ker(∂ₙ)/im(∂ₙ₊₁)  (cycles mod boundaries)

Euler characteristic:
  χ(X) = Σₙ (-1)ⁿ rank(Hₙ(X))
  For polyhedra: χ = V - E + F  (vertices - edges + faces)
  Sphere: V-E+F = 2  (Euler formula)
  Torus: V-E+F = 0

Key homology groups:
  Hₙ(Sᵏ) = ℤ if n=0 or n=k, 0 otherwise
  H₀(X) = ℤ^(# connected components)
  Hₙ(Tᵏ) = ℤ^C(k,n)  (torus k-dimensional)

Betti numbers:
  βₙ = rank(Hₙ(X))  (number of n-dimensional holes)
  β₀: connected components
  β₁: independent loops (handles)
  β₂: enclosed voids

Cohomology:
  Hⁿ(X; R): dual to homology (with coefficients in ring R)
  Cup product: Hᵖ⊗Hq → Hᵖ⁺q  (ring structure)
  Poincaré duality: Hₖ(Mⁿ) ≅ Hⁿ⁻ᵏ(Mⁿ) for closed orientable n-manifold
```

---

## Manifolds
```
n-manifold:
  Topological space locally homeomorphic to ℝⁿ
  Hausdorff, second-countable

Surface classification (compact, connected):
  Orientable: connected sum of g tori (genus g)
    g=0: sphere S²
    g=1: torus T²
    g=2: double torus
    Euler characteristic: χ = 2-2g
  Non-orientable: connected sum of k projective planes
    k=1: RP² (projective plane)
    k=2: Klein bottle
    χ = 2-k

Smooth manifolds:
  Atlas: collection of charts (overlapping homeomorphisms to ℝⁿ)
  Smooth: transition maps Cᵢⱼ = φⱼ∘φᵢ⁻¹ are C∞
  Tangent space TₓM: vectors at x (n-dimensional vector space)
  Tangent bundle TM: disjoint union of all tangent spaces

de Rham cohomology:
  Differential forms on smooth manifold
  dω: exterior derivative
  HᵏdR(M) = closed k-forms / exact k-forms
  de Rham theorem: HᵏdR(M) ≅ Hᵏ(M;ℝ)
  Stokes theorem: ∫_M dω = ∫_{∂M} ω

Characteristic classes:
  Obstructions to certain geometric structures
  Stiefel-Whitney (ℤ/2), Chern (complex), Pontryagin (real)
  Classify vector bundles, detect non-orientability
```

---

## Separation Axioms
```
T₀ (Kolmogorov): distinct points topologically distinguishable
T₁: every singleton {x} is closed
T₂ (Hausdorff): distinct points have disjoint open neighborhoods
  Limits of sequences are unique
  Most spaces in analysis are Hausdorff
T₃ (Regular + T₁): point and closed set have disjoint neighborhoods
T₃½ (Tychonoff/completely regular + T₁)
T₄ (Normal + T₁): two disjoint closed sets have disjoint neighborhoods
  Urysohn's lemma: T₄ ↔ continuous function separating closed sets
  Tietze extension theorem: continuous f on closed A extends to all X

Hierarchy: T₄ → T₃½ → T₃ → T₂ → T₁ → T₀
Metric spaces: normal (T₄)
Compact Hausdorff: normal
```

---

## Topological Data Analysis (TDA)
```python
def tda_concepts():
    return {
        'Persistent Homology': {
            'idea':         'Track topological features (holes) across scales',
            'filtration':   'Sequence of nested spaces X₀ ⊆ X₁ ⊆ ... ⊆ Xₙ',
            'birth_death':  'Feature born at ε_birth, dies at ε_death',
            'barcode':      'Collection of intervals [birth, death)',
            'persistence':  'death - birth (longer = more significant)',
            'diagram':      'Points (birth, death) in ℝ²',
            'stability':    'Bottleneck distance: small data perturbation → small change'
        },
        'Vietoris-Rips Complex': {
            'from_data':    'Given point cloud X and scale ε',
            'simplices':    'Add k-simplex if all pairwise distances ≤ ε',
            'computation':  'Compute homology at each ε, track through filtration'
        },
        'Mapper Algorithm': {
            'idea':         'Low-dimensional graph summarizing high-dim data',
            'steps': [
                '1. Apply filter function f: X → ℝ',
                '2. Cover range of f with overlapping intervals',
                '3. Cluster preimages of each interval',
                '4. Build graph: clusters = nodes, overlaps = edges'
            ],
            'applications': 'Shape of data, identify subgroups, anomalies'
        },
        'Applications': [
            'Cancer subtype identification (topology of gene expression)',
            'Material science (structure of amorphous materials)',
            'Neuroscience (shape of neural data)',
            'Time series analysis (sliding window persistence)',
            'Shape analysis and comparison'
        ],
        'Software': {
            'Ripser':       'Fast persistent homology computation (C++/Python)',
            'Gudhi':        'Comprehensive TDA library (Python/C++)',
            'Giotto-tda':   'Sklearn-compatible TDA pipeline',
            'TDA R package':'R implementation'
        }
    }
```

---

## Key Theorems
```
Urysohn's lemma: X normal ↔ ∀ disjoint closed A,B ∃ continuous f: X→[0,1] with f(A)=0, f(B)=1
Tietze extension: X normal, f: A→ℝ continuous on closed A → extends to F: X→ℝ
Tychonoff: Arbitrary product of compact spaces is compact
Heine-Borel: In ℝⁿ: compact ↔ closed and bounded
Brouwer fixed point: f: Dⁿ→Dⁿ continuous → has fixed point
Invariance of domain: f: U⊆ℝⁿ→ℝⁿ injective continuous open map
Jordan curve theorem: Simple closed curve in ℝ² divides into two components
Seifert-Van Kampen: Computes π₁ of union
Mayer-Vietoris: Long exact sequence for homology of union
Poincaré duality: Hₖ(M) ≅ Hⁿ⁻ᵏ(M) for closed orientable n-manifold
Classification of surfaces: Orientable ↔ sum of tori; non-orientable ↔ sum of RP²
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Path-connected = connected | Path-connected → connected, NOT converse |
| Compact = closed and bounded | Only in ℝⁿ (Heine-Borel); general: use open cover definition |
| Homeomorphic = isometric | Homeomorphism preserves topology only, not distances |
| Continuous = open map | Continuous maps need not send open sets to open sets |
| Simply connected = contractible | S² is simply connected but not contractible |
| π₁ detects all holes | π₁ only detects 1D holes; need higher homotopy/homology for others |

---

## Related Skills

- **real-analysis-expert**: Metric spaces, rigorous foundations
- **abstract-algebra-expert**: Groups, rings used in algebraic topology
- **differential-equations-expert**: Manifolds in dynamics
- **calculus-expert**: Differential forms, vector calculus
- **machine-learning-expert**: TDA applications in data science
