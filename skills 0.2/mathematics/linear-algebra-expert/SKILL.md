---
name: linear-algebra-expert
description: Expert-level linear algebra knowledge. Use when working with vectors, matrices, determinants, eigenvalues, linear transformations, vector spaces, inner products, decompositions, or applications in machine learning and physics. Also use when the user mentions 'matrix', 'determinant', 'eigenvalue', 'eigenvector', 'linear transformation', 'vector space', 'basis', 'orthogonality', 'SVD', 'PCA', 'least squares', 'null space', or 'rank'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Linear Algebra Expert

You are a world-class mathematician with deep expertise in linear algebra covering vectors, matrices, linear transformations, eigentheory, decompositions, inner product spaces, and applications in data science, physics, and engineering.

## Before Starting

1. **Topic** — Vectors, matrices, eigenvalues, decompositions, or applications?
2. **Level** — High school, undergraduate, or graduate?
3. **Goal** — Solve system, understand concept, or apply to ML/physics?
4. **Context** — Pure math, data science, physics, or engineering?
5. **Computation** — Theoretical or numerical/computational?

---

## Core Expertise Areas

- **Vectors & Matrices**: operations, properties, special matrices
- **Systems of Equations**: Gaussian elimination, row reduction, solutions
- **Determinants**: computation, properties, geometric meaning
- **Vector Spaces**: subspaces, basis, dimension, rank
- **Linear Transformations**: kernel, image, matrix representation
- **Eigentheory**: eigenvalues, eigenvectors, diagonalization
- **Inner Product Spaces**: dot product, orthogonality, Gram-Schmidt
- **Matrix Decompositions**: LU, QR, SVD, spectral theorem

---

## Vectors & Vector Operations
```
Vector: ordered list of numbers v = (v₁, v₂, ..., vₙ) ∈ ℝⁿ

Operations:
  Addition:      u + v = (u₁+v₁, u₂+v₂, ..., uₙ+vₙ)
  Scalar mult:   cv = (cv₁, cv₂, ..., cvₙ)
  Dot product:   u·v = Σuᵢvᵢ = |u||v|cosθ
  Cross product: u×v = (u₂v₃-u₃v₂, u₃v₁-u₁v₃, u₁v₂-u₂v₁)  (ℝ³ only)
  Norm:          |v| = √(v·v) = √(Σvᵢ²)

Properties of dot product:
  Commutative:  u·v = v·u
  Distributive: u·(v+w) = u·v + u·w
  u·v = 0 ↔ u ⊥ v  (orthogonal)
  Cauchy-Schwarz: |u·v| ≤ |u||v|
  Triangle inequality: |u+v| ≤ |u| + |v|

Projection:
  proj_v u = (u·v/v·v) v  (projection of u onto v)
  comp_v u = u·v/|v|  (scalar component)

Linear independence:
  {v₁,...,vₖ} linearly independent if:
  c₁v₁ + c₂v₂ + ... + cₖvₖ = 0 → all cᵢ = 0
  Dependent: one vector is linear combination of others
```

---

## Matrix Operations
```
Matrix A is m×n (m rows, n columns)
  Entry: aᵢⱼ (row i, column j)

Operations:
  Addition:      (A+B)ᵢⱼ = aᵢⱼ + bᵢⱼ  (same size)
  Scalar mult:   (cA)ᵢⱼ = c·aᵢⱼ
  Transpose:     (Aᵀ)ᵢⱼ = aⱼᵢ
  Multiplication: (AB)ᵢⱼ = Σₖ aᵢₖbₖⱼ  (A is m×p, B is p×n)

Matrix multiplication properties:
  NOT commutative: AB ≠ BA in general
  Associative:     (AB)C = A(BC)
  Distributive:    A(B+C) = AB + AC
  Transpose:       (AB)ᵀ = BᵀAᵀ
  Inverse:         (AB)⁻¹ = B⁻¹A⁻¹

Special matrices:
  Zero matrix: O (all zeros)
  Identity: I (1s on diagonal)
  Diagonal: D (nonzero only on diagonal)
  Symmetric: A = Aᵀ
  Skew-symmetric: A = -Aᵀ
  Orthogonal: AᵀA = I (columns are orthonormal)
  Unitary: A*A = I (complex: conjugate transpose)

Block matrices:
  Partition matrices into blocks for computation
  Block diagonal: [[A 0][0 B]]
  Block multiplication follows matrix multiplication rules
```

---

## Systems of Linear Equations
```
System: Ax = b
  A: m×n coefficient matrix
  x: n×1 unknown vector
  b: m×1 right-hand side

Augmented matrix: [A|b]

Row operations (preserve solution set):
  R1: Multiply row by nonzero scalar
  R2: Add multiple of one row to another
  R3: Swap two rows

Row Echelon Form (REF):
  Leading nonzero in each row to right of row above
  Zero rows at bottom

Reduced Row Echelon Form (RREF):
  Each pivot = 1
  Each pivot is only nonzero in its column

Solution types:
  Unique solution:   rref gives [I|c], n pivots
  Infinitely many:   free variables (fewer pivots than unknowns)
  No solution:       inconsistent row [0 0...0 | b≠0]

Rank-Nullity theorem:
  rank(A) + nullity(A) = n  (number of columns)
  rank = number of pivots
  nullity = dimension of null space (number of free variables)

Cramer's rule (n×n, det(A)≠0):
  xᵢ = det(Aᵢ)/det(A)  (Aᵢ = A with column i replaced by b)
  Impractical for large n (use Gaussian elimination)
```

---

## Determinants
```
2×2: det[[a b][c d]] = ad - bc

3×3 (cofactor expansion along row 1):
  det(A) = a₁₁C₁₁ + a₁₂C₁₂ + a₁₃C₁₃
  Cᵢⱼ = (-1)^(i+j) Mᵢⱼ  (cofactor, Mᵢⱼ = minor)

Properties:
  det(Aᵀ) = det(A)
  det(AB) = det(A)det(B)
  det(A⁻¹) = 1/det(A)
  det(cA) = cⁿdet(A)  (n×n matrix)
  Row swap: det changes sign
  Row multiply by k: det multiplied by k
  Add multiple of row to another: det unchanged
  Triangular matrix: det = product of diagonal entries

Geometric meaning:
  2×2: |det(A)| = area of parallelogram spanned by rows/columns
  3×3: |det(A)| = volume of parallelepiped
  det(A) > 0: orientation preserved
  det(A) < 0: orientation reversed
  det(A) = 0: matrix is singular (rows/columns linearly dependent)

Inverse formula:
  A⁻¹ = (1/det(A)) · adj(A)
  adj(A) = (Cᵢⱼ)ᵀ  (adjugate = transpose of cofactor matrix)
```

---

## Vector Spaces
```
Vector space V over field F:
  Satisfies 8 axioms (closure, commutativity, associativity,
  identity, inverse for + ; associativity, distributivity, identity for ·)

Examples:
  ℝⁿ: n-tuples of real numbers
  Mₘₙ: m×n matrices
  Pₙ: polynomials of degree ≤ n
  C[a,b]: continuous functions on [a,b]
  Solution set of Ax = 0 (null space)

Subspace: subset W of V satisfying:
  0 ∈ W
  u,v ∈ W → u+v ∈ W
  u ∈ W → cu ∈ W  (for all scalars c)

Four fundamental subspaces of A (m×n):
  Column space C(A): span of columns, subspace of ℝᵐ
  Row space R(A): span of rows, subspace of ℝⁿ
  Null space N(A): {x: Ax=0}, subspace of ℝⁿ
  Left null space N(Aᵀ): {y: Aᵀy=0}, subspace of ℝᵐ

  dim(C(A)) = dim(R(A)) = rank(A)  (fundamental theorem)
  N(A) ⊥ R(A) and N(Aᵀ) ⊥ C(A)

Basis and dimension:
  Basis: linearly independent spanning set
  Dimension: number of vectors in any basis
  Standard basis ℝⁿ: e₁=(1,0,...,0), ..., eₙ=(0,...,0,1)
  Change of basis: P·[x]_B = [x]_standard
```

---

## Eigentheory
```
Eigenvalue equation: Av = λv
  λ = eigenvalue (scalar)
  v = eigenvector (nonzero vector)
  (A - λI)v = 0 → det(A - λI) = 0

Characteristic polynomial:
  p(λ) = det(A - λI) = 0
  Degree n for n×n matrix → n eigenvalues (counting multiplicity)
  Roots may be complex even for real A

Finding eigenvectors:
  For each eigenvalue λᵢ: solve (A-λᵢI)v = 0
  Eigenspace = null space of (A-λᵢI)

Properties:
  Trace(A) = sum of eigenvalues = Σλᵢ
  det(A) = product of eigenvalues = Πλᵢ
  Similar matrices have same eigenvalues
  Symmetric A: real eigenvalues, orthogonal eigenvectors
  Symmetric A: positive definite ↔ all eigenvalues > 0

Diagonalization:
  A = PDP⁻¹  where D = diag(λ₁,...,λₙ)
  P = matrix of eigenvectors as columns
  Requires n linearly independent eigenvectors
  If A has n distinct eigenvalues → diagonalizable

Powers and functions of matrices:
  Aᵏ = PDᵏP⁻¹  (Dᵏ = diag(λ₁ᵏ,...,λₙᵏ))
  eᴬ = PeᴰP⁻¹  (eᴰ = diag(eˡ¹,...,eˡⁿ))

Spectral theorem:
  A symmetric → A = QΛQᵀ  (Q orthogonal, Λ diagonal)
  Eigenvectors orthonormal, eigenvalues real
```

---

## Inner Product Spaces
```
Inner product ⟨u,v⟩:
  Conjugate symmetry: ⟨u,v⟩ = ⟨v,u⟩* (or symmetric for real)
  Linearity: ⟨au+bw,v⟩ = a⟨u,v⟩ + b⟨w,v⟩
  Positive definite: ⟨v,v⟩ ≥ 0, = 0 ↔ v = 0

Standard inner product (dot product): ⟨u,v⟩ = u·v = Σuᵢvᵢ
Function inner product: ⟨f,g⟩ = ∫ₐᵇ f(x)g(x)dx

Norm: ||v|| = √⟨v,v⟩
Cauchy-Schwarz: |⟨u,v⟩| ≤ ||u|| ||v||
Angle: cosθ = ⟨u,v⟩/(||u|| ||v||)

Orthogonality:
  u ⊥ v ↔ ⟨u,v⟩ = 0
  Orthogonal set: mutually orthogonal
  Orthonormal set: orthogonal + each ||vᵢ|| = 1
  Pythagorean theorem: ||u+v||² = ||u||² + ||v||²  if u⊥v

Gram-Schmidt process:
  Input: {v₁,...,vₙ} linearly independent
  Output: {u₁,...,uₙ} orthonormal basis

  u₁ = v₁/||v₁||
  w₂ = v₂ - ⟨v₂,u₁⟩u₁
  u₂ = w₂/||w₂||
  wₖ = vₖ - Σᵢ₌₁^(k-1) ⟨vₖ,uᵢ⟩uᵢ
  uₖ = wₖ/||wₖ||

Orthogonal complement:
  W⊥ = {v: ⟨v,w⟩=0 ∀w∈W}
  V = W ⊕ W⊥ (direct sum)
  Projection: proj_W v = Σᵢ⟨v,uᵢ⟩uᵢ  (orthonormal basis {uᵢ} for W)
```

---

## Matrix Decompositions
```python
def matrix_decompositions():
    return {
        'LU Decomposition': {
            'form':         'A = LU  (L lower triangular, U upper triangular)',
            'use':          'Solve Ax=b: Ly=b, then Ux=y',
            'advantage':    'Reuse factorization for multiple b vectors',
            'with_pivoting':'PA = LU  (P = permutation, for numerical stability)',
            'complexity':   'O(n³) once, O(n²) per solve'
        },
        'QR Decomposition': {
            'form':         'A = QR  (Q orthogonal, R upper triangular)',
            'method':       'Gram-Schmidt, Householder, Givens rotations',
            'use':          'Least squares, eigenvalue algorithms',
            'stability':    'More numerically stable than LU for least squares'
        },
        'Eigendecomposition': {
            'form':         'A = PDP⁻¹  (only for diagonalizable A)',
            'symmetric':    'A = QΛQᵀ  (spectral theorem, Q orthogonal)',
            'use':          'Matrix powers, differential equations, PCA'
        },
        'SVD (Singular Value Decomposition)': {
            'form':         'A = UΣVᵀ  (any m×n matrix)',
            'U':            'm×m orthogonal (left singular vectors)',
            'Σ':            'm×n diagonal (singular values σ₁≥σ₂≥...≥0)',
            'V':            'n×n orthogonal (right singular vectors)',
            'rank':         'rank(A) = number of nonzero singular values',
            'uses': [
                'Low-rank approximation: Aₖ = UₖΣₖVₖᵀ (best rank-k approximation)',
                'PCA: SVD of centered data matrix',
                'Pseudoinverse: A⁺ = VΣ⁺Uᵀ',
                'Least squares: x = A⁺b',
                'Image compression, recommender systems, NLP (LSA)'
            ]
        },
        'Cholesky': {
            'form':         'A = LLᵀ  (A symmetric positive definite)',
            'advantage':    'Twice as fast as LU, numerically stable',
            'use':          'SPD systems, multivariate statistics'
        },
        'Jordan Normal Form': {
            'form':         'A = PJP⁻¹  (J = Jordan blocks)',
            'use':          'Non-diagonalizable matrices, theoretical analysis',
            'jordan_block':  'Jλ = [[λ 1 0][0 λ 1][0 0 λ]] (λ on diagonal, 1 above)'
        }
    }
```

---

## Least Squares & Applications
```
Least squares problem:
  Ax = b has no solution (overdetermined, m > n)
  Find x̂ minimizing ||Ax - b||²
  Normal equations: AᵀAx̂ = Aᵀb
  Solution: x̂ = (AᵀA)⁻¹Aᵀb  (if AᵀA invertible)
  Via SVD: x̂ = A⁺b = VΣ⁺Uᵀb

PCA (Principal Component Analysis):
  Center data: subtract mean
  Compute covariance matrix C = (1/n)XᵀX
  Eigendecompose: C = QΛQᵀ
  Or SVD of X: X = UΣVᵀ
  Principal components = columns of V (or Q)
  Variance explained by kth PC = σₖ²/Σσᵢ²

Linear transformations:
  T: ℝⁿ → ℝᵐ is linear if T(u+v)=T(u)+T(v), T(cu)=cT(u)
  Every linear transformation: T(x) = Ax for some matrix A
  Kernel (null space): ker(T) = {x: T(x)=0}
  Image (range): im(T) = {T(x): x∈ℝⁿ} = C(A)
  Rank-Nullity: dim(ker) + dim(im) = n

Quadratic forms:
  Q(x) = xᵀAx  (A symmetric)
  Positive definite: Q(x) > 0 ∀x≠0 ↔ all eigenvalues > 0
  Negative definite: all eigenvalues < 0
  Indefinite: mixed eigenvalue signs
  Classification by eigenvalues of A
```

---

## Numerical Linear Algebra
```python
def numerical_methods_linalg():
    return {
        'Condition number': {
            'definition':   'κ(A) = ||A|| · ||A⁻¹|| = σ_max/σ_min',
            'interpretation': 'How sensitive solution is to perturbations in b',
            'ill-conditioned': 'κ >> 1: small error in b → large error in x',
            'well-conditioned': 'κ ≈ 1: stable computation'
        },
        'Iterative methods (large sparse A)': {
            'Jacobi':       'Diagonal update, simple but slow',
            'Gauss-Seidel': 'Use updated values immediately, faster',
            'CG (Conjugate Gradient)': 'For SPD matrices, optimal convergence',
            'GMRES':        'For non-symmetric, Krylov subspace method',
            'Convergence':  'Depends on eigenvalue distribution and condition number'
        },
        'Power iteration (eigenvalues)': {
            'method':       'Repeatedly multiply by A and normalize',
            'finds':        'Largest eigenvalue and corresponding eigenvector',
            'QR algorithm': 'Standard for all eigenvalues, O(n³)',
            'Lanczos':      'For large sparse symmetric matrices'
        },
        'Floating point issues': {
            'loss_of_significance': 'Subtracting nearly equal numbers',
            'overflow_underflow':   'Extremely large/small intermediate values',
            'pivoting':             'Partial pivoting prevents division by small numbers'
        }
    }
```

---

## Key Theorems Summary
```
Invertible Matrix Theorem (all equivalent for n×n A):
  A is invertible ↔
  det(A) ≠ 0 ↔
  Ax = b has unique solution for every b ↔
  Ax = 0 has only trivial solution ↔
  rank(A) = n ↔
  columns of A are linearly independent ↔
  rows of A are linearly independent ↔
  0 is not an eigenvalue of A ↔
  AᵀA is invertible ↔
  A = product of elementary matrices

Rank-Nullity: rank(A) + nullity(A) = n  (# columns)
Dimension theorem: dim(C(A)) = dim(R(A)) = rank(A)
Spectral theorem: Symmetric A → orthogonally diagonalizable
SVD: Every A = UΣVᵀ (exists for any matrix)
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| AB = BA assumed | Matrix multiplication is NOT commutative |
| (A+B)² = A²+2AB+B² | Only if AB = BA; general: (A+B)² = A²+AB+BA+B² |
| det(A+B) = det(A)+det(B) | WRONG: determinant is NOT linear in this way |
| Eigenvalues of AB = product of eigenvalues | Only true if A and B share eigenvectors |
| Rank = number of nonzero rows | Rank = number of nonzero rows in REF |
| Orthogonal = perpendicular only | Orthogonal matrix has columns forming orthonormal set |

---

## Related Skills

- **calculus-expert**: Multivariable and vector calculus
- **statistics-expert**: PCA, regression, covariance matrices
- **quantum-mechanics-expert**: Linear operators in Hilbert space
- **machine-learning-expert**: SVD, PCA, neural networks
- **numerical-methods-expert**: Numerical linear algebra
- **differential-equations-expert**: Systems of ODEs using matrices
