---
name: probability-expert
description: Expert-level probability theory knowledge. Use when working with probability spaces, random variables, distributions, expectation, variance, conditional probability, stochastic processes, Markov chains, martingales, or measure-theoretic probability. Also use when the user mentions 'sample space', 'random variable', 'expected value', 'variance', 'conditional probability', 'independence', 'Markov chain', 'Poisson process', 'moment generating function', 'law of large numbers', 'central limit theorem', or 'stochastic process'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Probability Expert

You are a world-class mathematician with deep expertise in probability theory covering probability spaces, random variables, distributions, expectation, conditional probability, stochastic processes, Markov chains, and measure-theoretic foundations.

## Before Starting

1. **Topic** — Probability spaces, distributions, conditioning, or stochastic processes?
2. **Level** — Introductory, undergraduate, or graduate (measure theory)?
3. **Goal** — Solve problem, derive result, or understand concept?
4. **Context** — Pure math, statistics, finance, physics, or CS?
5. **Approach** — Discrete, continuous, or general measure-theoretic?

---

## Core Expertise Areas

- **Probability Spaces**: axioms, sample space, events, sigma-algebras
- **Random Variables**: PMF, PDF, CDF, transformations
- **Expectation & Variance**: moments, MGF, characteristic functions
- **Conditional Probability**: Bayes, independence, conditional expectation
- **Common Distributions**: discrete and continuous families
- **Limit Theorems**: LLN, CLT, convergence concepts
- **Stochastic Processes**: Markov chains, Poisson process, Brownian motion
- **Measure Theory**: Lebesgue integration, Radon-Nikodym, filtrations

---

## Probability Spaces
```
Probability space: (Ω, F, P)
  Ω = sample space (set of all outcomes)
  F = sigma-algebra (collection of measurable events)
  P = probability measure

Kolmogorov axioms:
  1. P(A) ≥ 0  for all A ∈ F
  2. P(Ω) = 1
  3. P(∪ᵢAᵢ) = ΣP(Aᵢ)  for pairwise disjoint events

Sigma-algebra F:
  Contains Ω
  Closed under complement: A ∈ F → Aᶜ ∈ F
  Closed under countable unions: Aᵢ ∈ F → ∪Aᵢ ∈ F

Derived properties:
  P(∅) = 0
  P(Aᶜ) = 1 - P(A)
  A ⊆ B → P(A) ≤ P(B)  (monotonicity)
  P(A ∪ B) = P(A) + P(B) - P(A ∩ B)  (inclusion-exclusion)
  P(∪ᵢAᵢ) ≤ ΣP(Aᵢ)  (union bound/Boole's inequality)

Inclusion-exclusion principle:
  P(∪ᵢ₌₁ⁿ Aᵢ) = Σ P(Aᵢ) - Σ P(Aᵢ∩Aⱼ) + Σ P(Aᵢ∩Aⱼ∩Aₖ) - ...
```

---

## Conditional Probability & Independence
```
Conditional probability:
  P(A|B) = P(A∩B)/P(B)  for P(B) > 0
  Multiplicative rule: P(A∩B) = P(A|B)P(B) = P(B|A)P(A)

Chain rule:
  P(A₁∩A₂∩...∩Aₙ) = P(A₁)P(A₂|A₁)P(A₃|A₁A₂)...P(Aₙ|A₁...Aₙ₋₁)

Law of total probability:
  {B₁,...,Bₙ} partition of Ω
  P(A) = Σᵢ P(A|Bᵢ)P(Bᵢ)

Bayes' theorem:
  P(Bᵢ|A) = P(A|Bᵢ)P(Bᵢ) / Σⱼ P(A|Bⱼ)P(Bⱼ)
  Posterior ∝ Likelihood × Prior

Independence:
  A and B independent: P(A∩B) = P(A)P(B)
  Equivalent: P(A|B) = P(A) (if P(B) > 0)
  Pairwise independence ≠ mutual independence!
  Counter-example: {H,T}² — many pairwise but not mutually independent events

Conditional independence:
  A ⊥ B | C: P(A∩B|C) = P(A|C)P(B|C)
  A and B independent given C (but may be dependent marginally)
```

---

## Random Variables
```
Random variable X: measurable function X: Ω → ℝ
  Discrete: takes countable values
  Continuous: has density function

PMF (discrete): p(x) = P(X = x)
PDF (continuous): f(x) such that P(a≤X≤b) = ∫ₐᵇ f(x)dx
CDF: F(x) = P(X ≤ x)
  Properties: right-continuous, non-decreasing, F(-∞)=0, F(∞)=1
  For continuous: F'(x) = f(x)

Transformations:
  Y = g(X): if g strictly increasing, fY(y) = fX(g⁻¹(y))|dg⁻¹/dy|
  General: P(Y ≤ y) = P(g(X) ≤ y) → differentiate CDF

Joint distributions:
  Joint PMF: p(x,y) = P(X=x, Y=y)
  Joint PDF: f(x,y), P(A) = ∬_A f(x,y)dxdy
  Marginals: fX(x) = ∫ f(x,y)dy, fY(y) = ∫ f(x,y)dx
  Independence: f(x,y) = fX(x)fY(y) for all (x,y)

Covariance and correlation:
  Cov(X,Y) = E[(X-μX)(Y-μY)] = E[XY] - E[X]E[Y]
  ρ = Cov(X,Y)/(σXσY)  (Pearson correlation, |ρ| ≤ 1)
  Independent → Cov = 0, but Cov = 0 ≠ independent!
  Var(X+Y) = Var(X) + Var(Y) + 2Cov(X,Y)
```

---

## Expectation & Moments
```
Expectation:
  Discrete: E[X] = Σ x·p(x)
  Continuous: E[X] = ∫ x·f(x)dx
  E[g(X)] = ∫ g(x)f(x)dx  (law of unconscious statistician)

Properties:
  Linearity: E[aX+bY] = aE[X] + bE[Y]  (always!)
  If X,Y independent: E[XY] = E[X]E[Y]
  Jensen's inequality: if g convex, E[g(X)] ≥ g(E[X])
  Markov inequality: P(X≥a) ≤ E[X]/a  for a>0, X≥0
  Chebyshev: P(|X-μ|≥kσ) ≤ 1/k²

Variance and moments:
  Var(X) = E[(X-μ)²] = E[X²] - (E[X])²
  Std(X) = √Var(X)
  Var(aX+b) = a²Var(X)
  nth moment: E[Xⁿ]
  Central moment: E[(X-μ)ⁿ]
  Skewness: E[(X-μ)³]/σ³
  Kurtosis: E[(X-μ)⁴]/σ⁴ - 3 (excess kurtosis)

Moment Generating Function (MGF):
  M(t) = E[eᵗˣ] = Σ E[Xⁿ]tⁿ/n!
  M⁽ⁿ⁾(0) = E[Xⁿ]  (nth moment)
  Uniquely determines distribution (if exists)
  MGF of sum: M_{X+Y}(t) = MX(t)MY(t)  if independent

Characteristic function:
  φ(t) = E[eⁱᵗˣ]  (always exists, unlike MGF)
  Fourier transform of density
  φ(t) = M(it)  (analytically continued)
```

---

## Common Distributions Deep Dive
```python
def distribution_relationships():
    return {
        'Normal family': {
            'Standard normal': 'Z ~ N(0,1), φ(z) = e^(-z²/2)/√(2π)',
            'General':         'X ~ N(μ,σ²): Z = (X-μ)/σ ~ N(0,1)',
            'Chi-squared':     'Z₁²+...+Zₖ² ~ χ²(k)',
            't-distribution':  'Z/√(χ²(k)/k) ~ t(k)',
            'F-distribution':  '(χ²(m)/m)/(χ²(n)/n) ~ F(m,n)',
            'Lognormal':       'X = e^Y where Y~N(μ,σ²)'
        },
        'Exponential family': {
            'Exponential':     'Special case Gamma(1,λ), memoryless',
            'Gamma':           'Sum of independent exponentials',
            'Chi-squared':     'Gamma(k/2, 1/2)',
            'Beta':            'X/(X+Y) where X~Gamma(α), Y~Gamma(β)',
            'Weibull':         'X = λ(-ln U)^(1/k), generalized exponential'
        },
        'Discrete family': {
            'Binomial':        'Sum of n Bernoulli(p)',
            'Poisson':         'Limit of Binomial(n,λ/n) as n→∞',
            'Negative Binomial':'Sum of r geometric(p)',
            'Hypergeometric':  'Sampling without replacement'
        },
        'Key MGFs': {
            'Bernoulli(p)':    'M(t) = 1-p+peᵗ',
            'Binomial(n,p)':   'M(t) = (1-p+peᵗ)ⁿ',
            'Poisson(λ)':      'M(t) = exp(λ(eᵗ-1))',
            'Normal(μ,σ²)':    'M(t) = exp(μt + σ²t²/2)',
            'Exponential(λ)':  'M(t) = λ/(λ-t) for t<λ',
            'Gamma(α,β)':      'M(t) = (β/(β-t))^α'
        }
    }
```

---

## Conditional Expectation
```
E[X|Y=y] = ∫ x·f(x|y)dx  (function of y)
E[X|Y] = g(Y)  (random variable)

Tower property (law of iterated expectation):
  E[X] = E[E[X|Y]]  (extremely useful!)
  E[g(X)|X] = g(X)

Conditional variance:
  Var(X|Y) = E[X²|Y] - (E[X|Y])²
  Law of total variance:
    Var(X) = E[Var(X|Y)] + Var(E[X|Y])
  "Variance = expected conditional variance + variance of conditional mean"

Best prediction:
  E[X|Y] minimizes E[(X-g(Y))²] over all functions g
  Best linear predictor: X̂ = μX + ρ(σX/σY)(Y-μY)

Double expectation examples:
  Random sums: S = X₁+...+Xₙ where N is random
    E[S] = E[N]·E[X]  (Wald's identity)
    Var(S) = E[N]Var(X) + (E[X])²Var(N)
```

---

## Limit Theorems
```
Modes of convergence (Xₙ → X):
  Almost surely (a.s.): P(lim Xₙ = X) = 1  (strongest)
  In probability: P(|Xₙ-X|>ε) → 0 for all ε>0
  In distribution: Fₙ(x) → F(x) at continuity points
  In L²: E[(Xₙ-X)²] → 0
  a.s. → in prob → in distribution (weaker)
  L² → in prob → in distribution

Weak Law of Large Numbers:
  X₁,...,Xₙ iid, E[X₁]=μ < ∞
  X̄ₙ = (X₁+...+Xₙ)/n →ₚ μ  (converges in probability)

Strong Law of Large Numbers:
  Same assumptions → X̄ₙ →ₐ.ₛ. μ  (almost surely)
  Requires: E[|X|] < ∞

Central Limit Theorem:
  √n(X̄ₙ - μ)/σ →_d N(0,1)
  Sₙ = X₁+...+Xₙ: P((Sₙ-nμ)/σ√n ≤ x) → Φ(x)
  Berry-Esseen: |P(Zₙ≤x)-Φ(x)| ≤ Cρ/(σ³√n)  (ρ=E[|X-μ|³])

CLT generalizations:
  Lindeberg-Feller: independent but non-identical, with Lindeberg condition
  Multivariate CLT: √n(X̄-μ) →_d N(0,Σ)
  Delta method: if √n(Xₙ-θ) →_d N(0,σ²), then √n(g(Xₙ)-g(θ)) →_d N(0,σ²[g'(θ)]²)

Continuity theorem (Lévy):
  Xₙ →_d X ↔ φₙ(t) → φ(t) pointwise  (characteristic functions)

Generating function tricks:
  If PGF Gₙ(s) → G(s), then Xₙ →_d X
  PGF: G(s) = E[sˣ] (discrete), |s|≤1
```

---

## Stochastic Processes

### Markov Chains
```
Discrete-time Markov chain: {Xₙ, n≥0}
  Markov property: P(Xₙ₊₁=j|X₀,...,Xₙ) = P(Xₙ₊₁=j|Xₙ)
  Transition matrix P: Pᵢⱼ = P(Xₙ₊₁=j|Xₙ=i)
  n-step: P(Xₙ=j|X₀=i) = (Pⁿ)ᵢⱼ

Classification:
  Accessible: j accessible from i if (Pⁿ)ᵢⱼ > 0 for some n
  Communicating: i↔j if i→j and j→i
  Irreducible: all states communicate
  Period: d(i) = gcd{n: (Pⁿ)ᵢᵢ > 0}
  Aperiodic: d(i) = 1

Recurrence/transience:
  Recurrent: P(Tᵢᵢ < ∞) = 1 (returns to i with probability 1)
  Transient: P(Tᵢᵢ < ∞) < 1 (may never return)
  Positive recurrent: E[Tᵢᵢ] < ∞ (finite mean return time)
  Null recurrent: E[Tᵢᵢ] = ∞

Stationary distribution:
  π = πP  (π is left eigenvector with eigenvalue 1)
  πⱼ = 1/E[Tⱼⱼ]
  For irreducible positive recurrent: unique π, Pⁿᵢⱼ → πⱼ

Convergence theorem:
  Irreducible + aperiodic + positive recurrent → Pⁿ → Π (each row = π)
  Geometric convergence: |P(Xₙ=j|X₀=i) - πⱼ| ≤ Crⁿ (r < 1)
```

### Poisson Process
```
Counting process N(t): number of events by time t
  N(0) = 0, independent increments
  N(t)-N(s) ~ Poisson(λ(t-s)) for t > s

Properties:
  E[N(t)] = λt, Var[N(t)] = λt
  Interarrival times Tᵢ ~ Exponential(λ) (iid)
  Waiting time for nth event Sₙ ~ Gamma(n,λ)

Superposition: sum of independent Poisson(λ₁) + Poisson(λ₂) = Poisson(λ₁+λ₂)
Thinning: each event retained with probability p → Poisson(λp)
Conditioning: given N(t)=n, event times uniform on [0,t]

Non-homogeneous Poisson process:
  Rate λ(t) varies with time
  N(t) ~ Poisson(∫₀ᵗ λ(s)ds)
  Mean = ∫₀ᵗ λ(s)ds
```

### Brownian Motion
```
Brownian motion {Bₜ, t≥0}:
  B₀ = 0
  Independent increments
  Bₜ - Bₛ ~ N(0, t-s) for t > s
  Continuous sample paths

Properties:
  E[Bₜ] = 0, Var[Bₜ] = t
  Cov(Bₛ,Bₜ) = min(s,t)
  Not differentiable (Hölder continuous with exponent < 1/2)
  Quadratic variation: Σ(Bₜᵢ-Bₜᵢ₋₁)² → t  (a.s.)

Geometric Brownian Motion (Black-Scholes):
  Sₜ = S₀ exp((μ-σ²/2)t + σBₜ)
  dSₜ = μSₜdt + σSₜdBₜ  (Ito's lemma)

Ito's lemma:
  If dXₜ = μdt + σdBₜ, f(t,X) twice differentiable:
  df = (∂f/∂t + μ∂f/∂X + σ²/2 ∂²f/∂X²)dt + σ∂f/∂X dBₜ
  Key: (dBₜ)² = dt  (quadratic variation)

Martingales:
  E[Xₙ|X₁,...,Xₙ₋₁] = Xₙ₋₁
  Bₜ, Bₜ²-t, exp(θBₜ-θ²t/2) are martingales
  Optional stopping theorem: E[X_T] = E[X₀]  (under conditions)
```

---

## Inequalities
```python
def probability_inequalities():
    return {
        'Markov': {
            'statement':    'P(X ≥ a) ≤ E[X]/a  for a>0, X≥0',
            'use':          'Bound tail probability using only mean'
        },
        'Chebyshev': {
            'statement':    'P(|X-μ| ≥ kσ) ≤ 1/k²',
            'use':          'Bound deviation using mean and variance'
        },
        'Chernoff': {
            'statement':    'P(X≥a) ≤ min_t E[eᵗˣ]/eᵗᵃ = min_t M(t)/eᵗᵃ',
            'use':          'Much tighter than Markov for sums'
        },
        'Hoeffding': {
            'statement':    'For bounded iid Xᵢ∈[aᵢ,bᵢ]: P(X̄-E[X̄]≥t) ≤ exp(-2n²t²/Σ(bᵢ-aᵢ)²)',
            'use':          'Concentration of bounded sums'
        },
        'Jensen': {
            'statement':    'g convex: E[g(X)] ≥ g(E[X])',
            'use':          'Relate function of expectation to expectation of function'
        },
        'Cauchy-Schwarz': {
            'statement':    '(E[XY])² ≤ E[X²]E[Y²]',
            'use':          'Bound covariance'
        },
        'Union bound': {
            'statement':    'P(∪ Aᵢ) ≤ Σ P(Aᵢ)',
            'use':          'Multiple testing, algorithm analysis'
        }
    }
```

---

## Generating Functions
```
Probability Generating Function (PGF) for discrete X≥0:
  G(s) = E[sˣ] = Σ P(X=k)sᵏ  for |s| ≤ 1
  P(X=k) = G⁽ᵏ⁾(0)/k!
  E[X] = G'(1), Var[X] = G''(1) + G'(1) - [G'(1)]²
  Sum of independent: G_{X+Y}(s) = G_X(s)G_Y(s)
  Branching processes: Z_n = sum of Z_{n-1} offspring
    G_n(s) = G(G_{n-1}(s)) (composition)
    Extinction probability = smallest root of s = G(s) in [0,1]

Moment Generating Function (MGF):
  M(t) = E[eᵗˣ]
  M⁽ⁿ⁾(0) = E[Xⁿ]
  Sum of independent: M_{X+Y}(t) = M_X(t)M_Y(t)
  Uniqueness: if M exists in neighborhood of 0, determines distribution

Characteristic function:
  φ(t) = E[eⁱᵗˣ]  (always exists)
  φ(t) = M(it) when M exists
  Inversion: f(x) = (1/2π)∫ e^(-itx)φ(t)dt
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Independence from zero covariance | Cov=0 does not imply independence (only for jointly normal) |
| Pairwise ≠ mutual independence | Need P(A∩B∩C)=P(A)P(B)P(C) for mutual |
| Confusing P(A\|B) and P(B\|A) | Prosecutor's fallacy; use Bayes' theorem |
| E[g(X)] = g(E[X]) | Only true for linear g; Jensen: E[g(X)] ≥ g(E[X]) for convex g |
| CLT applies for any n | Need sufficient n and finite variance; check assumptions |
| Memoryless property everywhere | Only exponential (continuous) and geometric (discrete) |

---

## Related Skills

- **statistics-expert**: Applied statistical methods
- **calculus-expert**: Integration for continuous distributions
- **linear-algebra-expert**: Multivariate probability
- **differential-equations-expert**: Stochastic differential equations
- **number-theory-expert**: Combinatorial probability
- **machine-learning-expert**: Probabilistic machine learning
