---
name: complex-analysis-expert
description: Expert-level complex analysis knowledge. Use when working with complex functions, holomorphic functions, Cauchy's theorem, contour integration, Laurent series, residues, conformal mappings, or analytic continuation. Also use when the user mentions 'holomorphic', 'analytic', 'Cauchy theorem', 'residue', 'contour integral', 'Laurent series', 'conformal map', 'Riemann mapping', 'Mobius transformation', 'harmonic function', 'entire function', or 'meromorphic'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Complex Analysis Expert

You are a world-class mathematician with deep expertise in complex analysis covering holomorphic functions, Cauchy theory, Laurent series, residues, conformal mappings, harmonic functions, and the deeper theory of analytic functions.

## Before Starting

1. **Topic** — Holomorphic functions, contour integration, residues, or conformal maps?
2. **Level** — Undergraduate or graduate?
3. **Goal** — Evaluate integral, prove theorem, understand concept, or apply mapping?
4. **Context** — Pure math, physics (QFT, fluid dynamics), or engineering?
5. **Approach** — Geometric, algebraic, or computational?

---

## Core Expertise Areas

- **Complex Differentiation**: Cauchy-Riemann equations, holomorphic functions
- **Elementary Functions**: exponential, trig, log, power functions in ℂ
- **Cauchy Theory**: Cauchy's theorem, integral formula, Liouville's theorem
- **Series**: Taylor, Laurent, classification of singularities
- **Residue Calculus**: residue theorem, real integral evaluation
- **Conformal Mappings**: Möbius transformations, Riemann mapping theorem
- **Harmonic Functions**: relationship to holomorphic functions
- **Advanced Topics**: analytic continuation, Riemann surfaces, entire functions

---

## Complex Numbers & Basic Topology
```
Complex number: z = x + iy (x,y ∈ ℝ, i² = -1)
  Real part: Re(z) = x, Imaginary part: Im(z) = y
  Modulus: |z| = √(x²+y²)
  Argument: arg(z) = θ where z = |z|e^(iθ)
  Complex conjugate: z̄ = x - iy

Properties:
  |z|² = zz̄
  |z₁z₂| = |z₁||z₂|
  arg(z₁z₂) = arg(z₁) + arg(z₂)
  Triangle inequality: |z₁+z₂| ≤ |z₁|+|z₂|

Euler's formula: e^(iθ) = cosθ + i sinθ
  e^(iπ) + 1 = 0  (Euler's identity)
  z = re^(iθ): polar form

De Moivre: (cosθ+i sinθ)ⁿ = cos(nθ)+i sin(nθ)
  nth roots: w = r^(1/n) e^(i(θ+2πk)/n) for k=0,1,...,n-1

Riemann sphere: ℂ ∪ {∞} (one-point compactification)
  Stereographic projection: sphere ↔ extended complex plane

Topology of ℂ:
  Open disk: Dᵣ(z₀) = {z: |z-z₀| < r}
  Connected, simply connected regions
  Winding number: n(γ,z₀) = (1/2πi)∮_γ dz/(z-z₀)
```

---

## Complex Differentiation
```
Derivative: f'(z₀) = lim_{z→z₀} [f(z)-f(z₀)]/(z-z₀)
  Limit must be same from ALL directions in ℂ

Cauchy-Riemann equations:
  f = u + iv holomorphic ↔ ∂u/∂x = ∂v/∂y  and  ∂u/∂y = -∂v/∂x
  In polar: ∂u/∂r = (1/r)∂v/∂θ, (1/r)∂u/∂θ = -∂v/∂r
  f'(z) = ∂u/∂x + i∂v/∂x = ∂v/∂y - i∂u/∂y

Holomorphic (analytic): f differentiable in open set U
  Much stronger than real differentiability!
  Holomorphic ↔ infinitely differentiable
  Holomorphic ↔ locally given by convergent power series

Entire function: holomorphic on all of ℂ
  Examples: polynomials, eˢ, sin z, cos z

Meromorphic: holomorphic except at isolated poles

CR equations and harmonicity:
  If f = u+iv holomorphic: u and v are harmonic
  ∂²u/∂x² + ∂²u/∂y² = 0  (Laplace equation)
  v is harmonic conjugate of u
  Given harmonic u, can find v by integrating CR equations
```

---

## Elementary Complex Functions
```
Exponential:
  eˢ = eˣ(cos y + i sin y)  for z = x+iy
  Periodic: e^(z+2πi) = eˢ
  Never zero: eˢ ≠ 0 for all z

Complex trig and hyperbolic:
  sin z = (e^(iz) - e^(-iz))/2i    cos z = (e^(iz) + e^(-iz))/2
  sinh z = (eˢ - e^(-z))/2         cosh z = (eˢ + e^(-z))/2
  sin(iz) = i sinh z,   cos(iz) = cosh z
  |sin z|² = sin²x + sinh²y  (can be > 1!)

Complex logarithm (multivalued):
  Log z = ln|z| + i Arg(z)  (principal value, Arg ∈ (-π,π])
  log z = ln|z| + i(Arg z + 2πk)  k ∈ ℤ
  Not defined at z = 0
  Branch cut: negative real axis for principal value
  d/dz Log z = 1/z  (on cut plane)

Complex power:
  z^w = exp(w log z)  (multivalued in general)
  z^n: unambiguous for integer n
  z^(1/n): n values (nth roots)
  i^i = e^(i·log i) = e^(i·iπ/2) = e^(-π/2) ≈ 0.2079 (real!)

Inverse trig:
  arcsin z = -i log(iz + √(1-z²))
  arctan z = (i/2)log((i+z)/(i-z)) = (i/2)log((1-iz)/(1+iz))
```

---

## Cauchy Theory
```
Contour integral:
  ∫_γ f(z)dz = ∫ₐᵇ f(γ(t))γ'(t)dt
  ML inequality: |∫_γ f dz| ≤ M·L  (M = max|f|, L = length of γ)

Cauchy's theorem (simply connected domain):
  f holomorphic in simply connected D
  γ closed curve in D → ∮_γ f(z)dz = 0

  Equivalent: ∫_γ₁ f = ∫_γ₂ f (path independence for holomorphic f)
  Antiderivative: F'(z) = f(z) exists → ∫ = F(endpoint) - F(startpoint)

Cauchy's Integral Formula:
  f holomorphic in D, γ simple closed curve in D, z₀ inside γ:
  f(z₀) = (1/2πi) ∮_γ f(z)/(z-z₀) dz

  Higher derivatives:
  f⁽ⁿ⁾(z₀) = (n!/2πi) ∮_γ f(z)/(z-z₀)^(n+1) dz

  Consequence: holomorphic → infinitely differentiable! (unlike real analysis)

Liouville's Theorem:
  Bounded entire function is constant
  Proof: Taylor coefficients bounded → all zero except constant

Fundamental Theorem of Algebra (consequence):
  Every non-constant polynomial has a root in ℂ
  Proof: if no root, 1/p(z) bounded entire function → constant

Maximum modulus principle:
  f non-constant holomorphic → |f| has no maximum in interior
  Maximum attained on boundary (for closed bounded region)
  Minimum: |f| has no interior minimum if f ≠ 0
```

---

## Taylor & Laurent Series
```
Taylor series (f holomorphic in disk |z-z₀|<R):
  f(z) = Σₙ₌₀^∞ aₙ(z-z₀)ⁿ
  aₙ = f⁽ⁿ⁾(z₀)/n! = (1/2πi)∮ f(z)/(z-z₀)^(n+1) dz
  Converges absolutely in |z-z₀| < R

Common Taylor series (centered at 0):
  eˢ = Σ zⁿ/n!  (entire)
  sin z = Σ (-1)ⁿz^(2n+1)/(2n+1)!  (entire)
  cos z = Σ (-1)ⁿz^(2n)/(2n)!  (entire)
  1/(1-z) = Σ zⁿ  (|z|<1)
  Log(1+z) = Σ (-1)^(n+1)zⁿ/n  (|z|<1)

Laurent series (f holomorphic in annulus r < |z-z₀| < R):
  f(z) = Σₙ₌₋∞^∞ cₙ(z-z₀)ⁿ
  cₙ = (1/2πi)∮ f(z)/(z-z₀)^(n+1) dz  (any circle in annulus)
  Principal part: Σₙ₌₋∞^(-1) cₙ(z-z₀)ⁿ (negative powers)
  Analytic part: Σₙ₌₀^∞ cₙ(z-z₀)ⁿ

Classification of isolated singularities:
  Removable: Laurent series has no negative powers
    lim_{z→z₀} f(z) exists and is finite
    Example: sin(z)/z at z=0 (has limit 1)
  Pole of order m: Laurent series starts at (z-z₀)^(-m)
    lim_{z→z₀} (z-z₀)ᵐ f(z) exists and ≠ 0
    Simple pole: m=1
  Essential singularity: infinitely many negative power terms
    Casorati-Weierstrass: f(D\{z₀}) dense in ℂ near essential singularity
    Example: e^(1/z) at z=0
```

---

## Residue Calculus
```
Residue of f at z₀:
  Res(f, z₀) = c₋₁ (coefficient of (z-z₀)^(-1) in Laurent series)

Computing residues:
  Simple pole z₀: Res = lim_{z→z₀} (z-z₀)f(z)
  Pole order m: Res = lim_{z→z₀} (1/(m-1)!) d^(m-1)/dz^(m-1) [(z-z₀)ᵐf(z)]
  f = p/q, simple zero of q at z₀: Res = p(z₀)/q'(z₀)

Residue Theorem:
  f meromorphic in D with poles z₁,...,zₙ, γ simple closed curve:
  ∮_γ f(z)dz = 2πi Σₖ n(γ,zₖ) Res(f,zₖ)
  For counterclockwise γ enclosing all poles:
  ∮_γ f(z)dz = 2πi Σₖ Res(f,zₖ)
```

### Real Integral Evaluation
```python
def real_integrals_via_residues():
    return {
        'Rational trig ∫₀²π R(cosθ,sinθ)dθ': {
            'substitution': 'z = e^(iθ): cosθ=(z+z⁻¹)/2, sinθ=(z-z⁻¹)/2i, dθ=dz/iz',
            'becomes':      '∮_{|z|=1} f(z)dz = 2πi × sum of residues inside unit circle'
        },
        'Rational ∫_{-∞}^∞ f(x)dx': {
            'condition':    'f analytic except poles, |zf(z)|→0 as |z|→∞',
            'contour':      'Semicircle in upper half-plane',
            'result':       '∫_{-∞}^∞ f(x)dx = 2πi × sum of residues in upper half-plane'
        },
        'Fourier type ∫_{-∞}^∞ f(x)e^(iax)dx': {
            'condition':    'a>0, f→0 as |z|→∞',
            'method':       'Jordan\'s lemma: integral over large semicircle → 0',
            'result':       '= 2πi × sum of residues of f(z)e^(iaz) in upper half-plane'
        },
        'Branch cut integrals ∫₀^∞ f(x)xˢdx': {
            'contour':      'Keyhole contour around branch cut on positive real axis',
            'result':       'Gives integral in terms of residues'
        },
        'Indented contours': {
            'use':          'When pole on real axis',
            'small_semicircle': 'Contributes πi × Res (half residue for simple pole)'
        }
    }
```

---

## Conformal Mappings
```
Conformal map: angle-preserving bijection between regions
  Holomorphic with f'(z) ≠ 0 → conformal
  Preserves angles AND orientation at non-critical points

Möbius transformations (linear fractional):
  f(z) = (az+b)/(cz+d)  with ad-bc ≠ 0
  Extended ℂ∞ → ℂ∞: maps circles/lines to circles/lines
  Three points determine unique Möbius transformation
  Composition forms group: PSL(2,ℂ)
  Fixed points: solve f(z) = z
  Cross-ratio preserved: (z₁,z₂;z₃,z₄) = (f(z₁),f(z₂);f(z₃),f(z₄))

Important Möbius transformations:
  Unit disk to upper half-plane: f(z) = (z-i)/(z+i)
  Upper half-plane to unit disk: f(z) = (z-i)/(z+i) inverse
  Translation: f(z) = z+c
  Rotation: f(z) = e^(iθ)z
  Dilation: f(z) = rz
  Inversion: f(z) = 1/z

Riemann Mapping Theorem:
  Any simply connected proper subset of ℂ is conformally equivalent to disk
  D = {z: |z|<1}
  f unique if we specify f(z₀) = 0 and f'(z₀) > 0 for some z₀
  Proof uses normal families, Montel's theorem

Standard conformal maps:
  z² : maps right half-plane to ℂ\(-∞,0] (doubles angles at origin)
  √z : inverse of z²
  eˢ : maps horizontal strip 0<Im(z)<π to upper half-plane
  Log z: inverse, maps ℂ\(-∞,0] to strip
  sin z: maps strip |Re(z)|<π/2 conformally
  Joukowski: z + 1/z (aerodynamics, transforms circles to airfoils)

Schwarz-Christoffel formula:
  Map upper half-plane to polygon with interior angles αₖπ:
  f(z) = A ∫ₛ^z Πₖ(t-xₖ)^(αₖ-1) dt + B
  xₖ: preimages of vertices on real axis
```

---

## Harmonic Functions
```
Harmonic: Δu = ∂²u/∂x² + ∂²u/∂y² = 0
  Real and imaginary parts of holomorphic functions are harmonic
  Conversely: given harmonic u, can find harmonic conjugate v (simply connected)
  u+iv then holomorphic

Mean value property:
  u(z₀) = (1/2π)∫₀²π u(z₀+re^(iθ))dθ  (average over circle)
  Maximum principle: harmonic maximum on boundary of bounded region

Poisson integral formula:
  Solve Dirichlet problem: Δu=0 in disk, u=f on boundary
  u(re^(iθ)) = (1/2π)∫₀²π P(r,φ-θ)f(e^(iφ))dφ
  Poisson kernel: P(r,θ) = (1-r²)/(1-2r cosθ+r²)

Green's functions:
  G(z,z₀): Δ_z G = δ(z-z₀), G=0 on boundary
  Solution: u(z₀) = ∫_∂D f(z)∂G/∂n ds

Dirichlet problem:
  Upper half-plane: u(x,y) = (y/π)∫_{-∞}^∞ f(t)/((x-t)²+y²) dt
  (Poisson formula for upper half-plane)
```

---

## Advanced Topics
```
Analytic continuation:
  Extend holomorphic function beyond original domain
  Unique continuation: if two analytic functions agree on open set, agree everywhere
  Monodromy theorem: continuation on simply connected domain is single-valued
  Log and zʷ: multi-valued due to topology

Riemann surfaces:
  Make multi-valued functions single-valued on larger domain
  log z: cover ℂ\{0} with infinite-sheeted surface
  √z: two-sheeted surface with branch point at 0
  Algebraic functions: compact Riemann surfaces ↔ algebraic curves

Infinite products:
  Weierstrass factorization: entire f with zeros {aₙ}:
  f(z) = zᵐeᵍ⁽ˢ⁾ Πₙ (1-z/aₙ)exp(z/aₙ+z²/2aₙ²+...)
  sin πz = πz Πₙ₌₁^∞ (1-z²/n²)  (famous example)

Entire functions:
  Liouville: bounded entire → constant
  Picard's little theorem: non-constant entire takes every value except at most one
  e^z misses 0; e^(e^z) doesn't miss any value

Gamma function:
  Γ(z) = ∫₀^∞ t^(z-1)e^(-t)dt  for Re(z)>0
  Meromorphic continuation to all z ≠ 0,-1,-2,...
  Γ(n+1) = n! (factorial generalization)
  Reflection formula: Γ(z)Γ(1-z) = π/sin(πz)
  Stirling: Γ(n+1) ~ √(2πn)(n/e)ⁿ

Argument principle:
  f meromorphic, γ simple closed curve:
  (1/2πi)∮_γ f'/f dz = Z - P  (zeros minus poles inside, with multiplicity)
  Rouché's theorem: |g|<|f| on γ → f and f+g have same number of zeros inside
```

---

## Computational Examples
```python
def contour_integral_examples():
    return {
        'Example 1: ∫₀^∞ dx/(1+x²) = π/2': {
            'setup':        'Semicircle contour, f(z) = 1/(1+z²)',
            'poles':        'z = ±i, only z=i in upper half-plane',
            'residue':      'Res(f,i) = lim_{z→i}(z-i)/(z²+1) = 1/2i',
            'result':       '2πi · (1/2i) = π, so ∫_{-∞}^∞ = π, ∫₀^∞ = π/2'
        },
        'Example 2: ∫₀^∞ x^(p-1)/(1+x)dx = π/sin(pπ), 0<p<1': {
            'setup':        'Keyhole contour, branch cut on positive real axis',
            'method':       'Integral contributes on both sides of cut',
            'poles':        'z = -1: simple pole of 1/(1+z)',
            'result':       'Connects to Γ(p)Γ(1-p) = π/sin(pπ)'
        },
        'Example 3: ∫_{-∞}^∞ e^(iax)/(x²+b²)dx = πe^(-ab)/b, a,b>0': {
            'setup':        'Semicircle in upper half-plane (a>0)',
            'poles':        'z = ib in upper half-plane',
            'residue':      'e^(ia(ib))/(2ib) = e^(-ab)/2ib',
            'result':       '2πi · e^(-ab)/2ib = πe^(-ab)/b'
        }
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Real differentiable = complex differentiable | Complex differentiability requires CR equations (much stronger) |
| Log z is single-valued | log z is multi-valued; use principal branch Log z carefully |
| Cauchy theorem applies anywhere | Requires holomorphic function in simply connected region |
| Residue = whole Laurent series | Residue is ONLY the c₋₁ coefficient |
| Semicircle integral always vanishes | Need Jordan's lemma conditions; check |f(z)|→0 on arc |
| Conformal = angle preserving only | Also requires bijection and holomorphicity |

---

## Related Skills

- **calculus-expert**: Real analysis foundations
- **real-analysis-expert**: Rigorous limits and continuity
- **differential-equations-expert**: Applications to PDEs
- **number-theory-expert**: Analytic number theory (Riemann zeta)
- **physics-electromagnetism**: Conformal maps in 2D problems
- **fluid-physics-expert**: Complex potential for 2D flow
