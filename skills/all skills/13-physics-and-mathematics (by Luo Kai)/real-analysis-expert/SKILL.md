---
author: luo-kai
name: real-analysis-expert
description: Expert-level real analysis knowledge. Use when working with limits, continuity, differentiability, Riemann and Lebesgue integration, sequences and series of functions, metric spaces, measure theory, or functional analysis foundations. Also use when the user mentions 'epsilon-delta', 'uniform continuity', 'uniform convergence', 'Lebesgue integral', 'measure theory', 'sigma-algebra', 'Banach space', 'Hilbert space', 'completeness', 'compactness', 'Heine-Borel', or 'dominated convergence'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Real Analysis Expert

You are a world-class mathematician with deep expertise in real analysis covering the rigorous foundations of calculus, measure theory, Lebesgue integration, sequences of functions, and introductory functional analysis.

## Before Starting

1. **Topic** — Limits, continuity, integration, measure theory, or functional analysis?
2. **Level** — Undergraduate or graduate?
3. **Goal** — Prove theorem, construct counterexample, or understand concept?
4. **Context** — Pure analysis, probability theory, or functional analysis?
5. **Rigor** — Epsilon-delta proofs or higher-level arguments?

---

## Core Expertise Areas

- **Real Number System**: completeness, supremum, Archimedean property
- **Sequences & Series**: convergence, Cauchy criterion, absolute convergence
- **Limits & Continuity**: epsilon-delta, uniform continuity, intermediate value
- **Differentiation**: mean value theorem, Taylor's theorem, inverse function
- **Riemann Integration**: Darboux sums, FTC, improper integrals
- **Sequences of Functions**: pointwise vs uniform convergence, interchange of limits
- **Lebesgue Theory**: measure theory, Lebesgue integral, convergence theorems
- **Metric & Normed Spaces**: completeness, compactness, Banach and Hilbert spaces

---

## Real Number System
```
Completeness axiom:
  Every nonempty set bounded above has a least upper bound (supremum)
  sup S: least upper bound (infimum: greatest lower bound)
  ℝ is complete; ℚ is not (√2 is limit of rational Cauchy sequence)

Archimedean property:
  ∀x,y > 0: ∃n ∈ ℕ: nx > y
  Equivalently: inf{1/n: n∈ℕ} = 0

Density: ℚ dense in ℝ: ∀a<b ∃q∈ℚ: a<q<b
  Similarly: irrationals dense in ℝ

Nested interval property:
  [a₁,b₁] ⊇ [a₂,b₂] ⊇ ... with length→0 → unique common point
  Equivalent to completeness

Cantor's theorem: ℝ uncountable (diagonal argument)
  [0,1] uncountable even though ℚ∩[0,1] countable
  Cantor set: closed, uncountable, measure zero, nowhere dense
```

---

## Sequences & Series
```
Sequence convergence: lim_{n→∞} aₙ = L means:
  ∀ε>0 ∃N: n>N → |aₙ-L| < ε

Cauchy criterion:
  {aₙ} Cauchy ↔ ∀ε>0 ∃N: m,n>N → |aₘ-aₙ| < ε
  In ℝ: Cauchy ↔ convergent (completeness!)

Subsequences:
  Every bounded sequence has convergent subsequence (Bolzano-Weierstrass)
  lim sup, lim inf: limits of suprema/infima of tails
  aₙ → L ↔ lim sup aₙ = lim inf aₙ = L

Series Σaₙ:
  Partial sums Sₙ = a₁+...+aₙ
  Converges: Sₙ → S (finite limit)
  Necessary: aₙ → 0 (but not sufficient!)
  Cauchy criterion: Σaₙ converges ↔ |aₘ₊₁+...+aₙ| → 0

Absolute convergence:
  Σ|aₙ| < ∞ → Σaₙ converges (absolutely)
  Absolutely convergent: can rearrange terms
  Conditionally convergent: Σaₙ converges but Σ|aₙ| = ∞
  Riemann rearrangement: conditionally convergent series can sum to any real or ±∞

Convergence tests (summary):
  Comparison: 0≤aₙ≤bₙ, Σbₙ < ∞ → Σaₙ < ∞
  Ratio: L = lim|aₙ₊₁/aₙ|: L<1 abs conv, L>1 diverges
  Root: L = lim sup|aₙ|^(1/n): same
  Integral: Σf(n) ↔ ∫f convergent (f decreasing positive)
  Alternating series: bₙ↓0 → Σ(-1)ⁿbₙ converges
```

---

## Limits & Continuity
```
Limit: lim_{x→a} f(x) = L means:
  ∀ε>0 ∃δ>0: 0<|x-a|<δ → |f(x)-L| < ε

Continuity at a: lim_{x→a} f(x) = f(a)
  Equivalent: f(aₙ) → f(a) whenever aₙ → a (sequential)
  Equivalent: f⁻¹(U) open for every open U (topological)

Properties of continuous functions:
  Intermediate Value Theorem: f:[a,b]→ℝ continuous, f(a)<c<f(b) → ∃x: f(x)=c
  Extreme Value Theorem: f:[a,b]→ℝ continuous → attains max and min
  Continuous image of compact set is compact
  Continuous image of connected set is connected

Uniform continuity:
  ∀ε>0 ∃δ>0: |x-y|<δ → |f(x)-f(y)| < ε  (same δ for all x,y)
  Stronger than pointwise continuity
  Continuous on closed bounded interval → uniformly continuous (Heine-Cantor)
  Lipschitz continuous: |f(x)-f(y)| ≤ K|x-y| → uniformly continuous

Monotone functions:
  Increasing f: f(x)≤f(y) when x<y
  Monotone functions have at most countably many discontinuities
  Every monotone function has left and right limits everywhere

Nowhere continuous: Dirichlet function f(x) = {1 if x∈ℚ, 0 if x∉ℚ}
Continuous only at 0: Thomae's function f(p/q)=1/q, f(irr)=0
```

---

## Differentiation
```
Derivative: f'(a) = lim_{h→0} [f(a+h)-f(a)]/h

Differentiable → continuous (but not conversely)
Weierstrass function: continuous everywhere, differentiable nowhere!

Mean Value Theorem:
  f continuous on [a,b], differentiable on (a,b)
  → ∃c∈(a,b): f'(c) = [f(b)-f(a)]/(b-a)

Generalized MVT (Cauchy):
  ∃c: [f(b)-f(a)]g'(c) = [g(b)-g(a)]f'(c)

Rolle's theorem: f(a)=f(b) → ∃c: f'(c)=0

L'Hopital's rule: rigorous version
  0/0 or ∞/∞ form, f,g differentiable, g'≠0 near a:
  lim f'/g' = L → lim f/g = L

Taylor's theorem:
  f has (n+1) derivatives on [a,x]:
  f(x) = Σₖ₌₀ⁿ f⁽ᵏ⁾(a)/k! (x-a)ᵏ + Rₙ(x)
  Lagrange remainder: Rₙ(x) = f⁽ⁿ⁺¹⁾(c)/(n+1)! (x-a)^(n+1) for some c∈(a,x)
  Cauchy remainder: Rₙ(x) = f⁽ⁿ⁺¹⁾(c)/n! (x-c)ⁿ(x-a)

Inverse function theorem:
  f differentiable, f'(a)≠0 → f⁻¹ differentiable at f(a)
  (f⁻¹)'(f(a)) = 1/f'(a)

Darboux's theorem:
  Derivatives have intermediate value property (even without continuity)
```

---

## Riemann Integration
```
Partition P = {a=x₀<x₁<...<xₙ=b}
Lower sum: L(f,P) = Σ mᵢΔxᵢ  (mᵢ = inf f on [xᵢ₋₁,xᵢ])
Upper sum: U(f,P) = Σ Mᵢ Δxᵢ  (Mᵢ = sup f on [xᵢ₋₁,xᵢ])

Riemann integrable: sup L(f,P) = inf U(f,P) = ∫ₐᵇ f(x)dx
Equivalent: ∀ε>0 ∃P: U(f,P) - L(f,P) < ε

Riemann's criterion:
  f integrable ↔ set of discontinuities has measure zero
  (Lebesgue criterion)
  Continuous → integrable
  Monotone → integrable
  Bounded with finitely many discontinuities → integrable

Fundamental Theorem of Calculus:
  Part 1: F(x) = ∫ₐˣ f(t)dt → F'(x) = f(x) at continuity points
  Part 2: ∫ₐᵇ f(x)dx = F(b)-F(a) if F'=f

Improper integrals:
  ∫ₐ^∞ f(x)dx = lim_{b→∞} ∫ₐᵇ f(x)dx
  ∫ₐᵇ f (f unbounded): lim_{c→a⁺} ∫ᶜᵇ f
  Comparison test: 0≤f≤g, ∫g < ∞ → ∫f < ∞

Riemann vs Lebesgue:
  Riemann integrates by partitioning domain
  Lebesgue integrates by partitioning range
  Lebesgue is more powerful: integrates more functions
  Agrees with Riemann for Riemann-integrable functions
```

---

## Sequences of Functions
```
Pointwise convergence: fₙ → f pointwise if fₙ(x) → f(x) for each x
Uniform convergence: fₙ → f uniformly if sup_x|fₙ(x)-f(x)| → 0

Pointwise ← Uniform (uniform implies pointwise, not conversely)
Counter-example: fₙ(x) = xⁿ on [0,1]
  Pointwise: f(x) = 0 for x∈[0,1), f(1)=1
  Not uniform: discontinuous limit of continuous functions!

Uniform convergence preserves:
  Continuity: fₙ continuous + uniform convergence → f continuous
  Integrability: ∫fₙ → ∫f
  Differentiability: if fₙ' uniformly converge and fₙ converge at one point
    → fₙ → f uniformly and fₙ' → f'

Weierstrass M-test:
  |fₙ(x)| ≤ Mₙ and Σ Mₙ < ∞ → Σfₙ converges uniformly and absolutely

Power series Σaₙ(x-a)ⁿ:
  Radius of convergence R = 1/lim sup|aₙ|^(1/n)
  Converges absolutely on (a-R, a+R)
  Uniformly on [a-r, a+r] for any r < R
  Can differentiate and integrate term by term inside interval

Equicontinuity:
  Family F equicontinuous: ∀ε∃δ: |x-y|<δ → |f(x)-f(y)|<ε (same δ for all f∈F)
  Arzelà-Ascoli theorem: uniformly bounded equicontinuous family has uniformly convergent subsequence
```

---

## Measure Theory
```
Sigma-algebra on X:
  Collection M of subsets: X∈M, closed under complement and countable union
  (X,M): measurable space

Measure μ: M → [0,∞]
  μ(∅) = 0
  Countable additivity: μ(∪ disjoint Aₙ) = Σμ(Aₙ)
  (X,M,μ): measure space

Lebesgue measure on ℝ:
  m([a,b]) = b-a  (length of interval)
  Extends uniquely to all Borel sets
  Null sets (measure zero): countable sets, Cantor set
  f = g a.e. (almost everywhere): f(x)=g(x) except on null set

Measurable functions:
  f: X → ℝ measurable if f⁻¹(B) ∈ M for all Borel B ⊆ ℝ
  Continuous functions measurable
  Monotone functions measurable
  Limit of measurable functions is measurable

Lebesgue integral:
  Simple functions: s = Σaᵢ1_{Aᵢ}: ∫s dμ = Σaᵢμ(Aᵢ)
  Nonneg: ∫f = sup{∫s: 0≤s≤f, s simple}
  General: ∫f = ∫f⁺ - ∫f⁻ (if at least one finite)
  Integrable (f∈L¹): ∫|f| < ∞

Lᵖ spaces:
  Lᵖ = {f measurable: ∫|f|ᵖ < ∞}
  ||f||_p = (∫|f|ᵖ)^(1/p)  (norm)
  L² = Hilbert space with inner product ⟨f,g⟩ = ∫fg
  L∞ = essentially bounded functions, ||f||_∞ = ess sup|f|
  Hölder: ||fg||₁ ≤ ||f||_p ||g||_q (1/p+1/q=1)
  Minkowski: ||f+g||_p ≤ ||f||_p + ||g||_p
```

---

## Convergence Theorems (Lebesgue)
```
Monotone Convergence Theorem (MCT):
  0 ≤ f₁ ≤ f₂ ≤ ..., fₙ → f pointwise a.e.
  → ∫fₙ → ∫f  (including ∫f = ∞)

Fatou's Lemma:
  fₙ ≥ 0 measurable:
  ∫(lim inf fₙ) ≤ lim inf ∫fₙ

Dominated Convergence Theorem (DCT):
  fₙ → f pointwise a.e.
  |fₙ| ≤ g for all n, g ∈ L¹
  → ∫fₙ → ∫f  (and ∫|fₙ-f| → 0)

Applications of DCT:
  Differentiation under integral: d/dt∫f(x,t)dx = ∫∂f/∂t dx (if bounded)
  Series integration: Σ∫fₙ = ∫Σfₙ (if Σ∫|fₙ| < ∞)

Comparison Riemann vs Lebesgue:
  Lebesgue handles:
    Limits of functions
    L∞ with indicator functions
    Functions like sin(x)/x (conditionally but not absolutely integrable)
  Dirichlet: Lebesgue integrable (∫₀¹1_ℚ = 0)
    Not Riemann integrable (L≠U for any partition)
```

---

## Metric & Normed Spaces
```
Normed vector space (V, ||·||):
  ||v|| ≥ 0, = 0 ↔ v=0
  ||αv|| = |α|||v||
  ||u+v|| ≤ ||u||+||v||
  Induces metric: d(u,v) = ||u-v||

Banach space: complete normed vector space
  Cauchy sequences converge
  Examples: ℝⁿ, Lᵖ(μ), C[a,b] with sup norm, ℓᵖ (sequence spaces)
  Not Banach: C[a,b] with L¹ norm

Hilbert space: complete inner product space
  ⟨u,v⟩: bilinear (or sesquilinear for complex), ⟨v,v⟩ ≥ 0
  ||v||² = ⟨v,v⟩
  Examples: L²(μ), ℓ², ℝⁿ
  Cauchy-Schwarz: |⟨u,v⟩| ≤ ||u|| ||v||
  Pythagorean: u⊥v → ||u+v||² = ||u||²+||v||²
  Parallelogram: ||u+v||²+||u-v||² = 2(||u||²+||v||²)

Orthonormal basis {eₙ}:
  ⟨eₘ,eₙ⟩ = δₘₙ
  Bessel: Σ|⟨f,eₙ⟩|² ≤ ||f||²
  Parseval: Σ|⟨f,eₙ⟩|² = ||f||² (complete orthonormal set)
  f = Σ⟨f,eₙ⟩eₙ (convergence in L² norm)

Bounded linear operators:
  T: V→W linear, ||T|| = sup{||Tv||/||v||: v≠0} < ∞
  Continuous ↔ bounded (for linear maps)
  Dual space V* = {bounded linear functionals V→ℝ}

Riesz representation theorem:
  Hilbert space H: every L∈H* has form L(f) = ⟨f,g⟩ for unique g∈H
  L²(μ)* ≅ L²(μ) via ⟨f,g⟩ = ∫fg dμ
```

---

## Important Counterexamples
```python
def key_counterexamples():
    return {
        'Continuous but not differentiable': {
            'function':     'Weierstrass: Σ aⁿcos(bⁿπx) for a<1, ab>1+3π/2',
            'property':     'Continuous everywhere, differentiable nowhere'
        },
        'Differentiable but derivative not continuous': {
            'function':     'f(x) = x²sin(1/x) for x≠0, f(0)=0',
            'property':     'f\'(0)=0 but f\'(x) oscillates near 0'
        },
        'Uniform convergence fails': {
            'function':     'fₙ(x) = xⁿ on [0,1]',
            'property':     'Pointwise to discontinuous limit, not uniform'
        },
        'Riemann not Lebesgue integrable': {
            'function':     '1_ℚ (Dirichlet function)',
            'property':     'Lebesgue integral = 0; no Riemann integral'
        },
        'Cantor set': {
            'property':     'Closed, uncountable, measure zero, nowhere dense, perfect',
            'construction': 'Remove middle thirds iteratively from [0,1]'
        },
        'Volterra function': {
            'property':     'Differentiable everywhere, bounded derivative, but FTC fails',
            'lesson':       'Need absolutely continuous for FTC'
        }
    }
```

---

## Key Theorems Summary
```
Bolzano-Weierstrass: bounded sequence has convergent subsequence
Heine-Cantor: continuous on compact → uniformly continuous
IVT: continuous f on [a,b] takes all intermediate values
EVT: continuous f on [a,b] attains max and min
MVT: f'(c) = (f(b)-f(a))/(b-a) for some c
Taylor: f(x) = Σf⁽ᵏ⁾(a)/k!(x-a)ᵏ + remainder
FTC: derivative of integral is function; integral of derivative is change
DCT: dominated convergence allows limit inside integral
MCT: monotone convergence theorem
Arzelà-Ascoli: bounded equicontinuous family has convergent subsequence
Riesz representation: L²* ≅ L²
Baire category: complete metric space not countable union of nowhere dense sets
Stone-Weierstrass: polynomials dense in C[a,b]
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Pointwise convergence preserves continuity | Need UNIFORM convergence to preserve continuity |
| Differentiable → continuously differentiable (C¹) | Darboux: derivative has IVP but need not be continuous |
| Compact = bounded | In ℝⁿ: compact ↔ closed AND bounded (Heine-Borel); infinite dimensions: need more |
| Riemann and Lebesgue always agree | Agree for Riemann integrable functions; Lebesgue integrates more |
| Limit and integral always interchange | Need uniform convergence OR dominated convergence theorem |
| Absolute convergence = convergence | Absolute convergence is stronger; conditionally convergent can be rearranged |

---

## Related Skills

- **calculus-expert**: Computational calculus (less rigorous)
- **complex-analysis-expert**: Complex version of analysis
- **topology-expert**: Metric space topology
- **probability-expert**: Measure-theoretic probability
- **differential-equations-expert**: Analysis applied to ODEs/PDEs
- **functional-analysis**: Advanced operator theory
