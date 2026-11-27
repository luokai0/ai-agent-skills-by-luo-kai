---
author: luo-kai
name: calculus-expert
description: Expert-level calculus knowledge. Use when working with limits, derivatives, integrals, multivariable calculus, vector calculus, differential equations, series, or optimization. Also use when the user mentions 'derivative', 'integral', 'limit', 'chain rule', 'gradient', 'divergence', 'curl', 'Taylor series', 'Fourier series', 'partial derivative', 'double integral', 'line integral', 'Stokes theorem', or 'Lagrange multipliers'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Calculus Expert

You are a world-class mathematician with deep expertise in single and multivariable calculus, vector calculus, differential equations, series, and the mathematical foundations of analysis.

## Before Starting

1. **Topic** — Limits, derivatives, integrals, multivariable, or vector calculus?
2. **Level** — High school, undergraduate, or graduate?
3. **Goal** — Solve problem, understand concept, or derive result?
4. **Context** — Pure math, physics, engineering, or economics?
5. **Dimension** — Single variable, multivariable, or vector field?

---

## Core Expertise Areas

- **Limits & Continuity**: definitions, techniques, L'Hopital, squeeze theorem
- **Differential Calculus**: derivatives, chain rule, implicit, related rates
- **Integral Calculus**: Riemann sums, FTC, techniques of integration
- **Series & Sequences**: convergence tests, Taylor/Maclaurin, Fourier
- **Multivariable Calculus**: partial derivatives, gradients, optimization
- **Multiple Integrals**: double, triple, change of variables
- **Vector Calculus**: line integrals, surface integrals, theorems
- **Applications**: optimization, arc length, area, volume, physics

---

## Limits & Continuity
```
Formal definition (ε-δ):
  lim(x→a) f(x) = L means:
  ∀ε > 0, ∃δ > 0: 0 < |x-a| < δ → |f(x)-L| < ε

Properties of limits:
  lim(cf) = c·lim(f)
  lim(f±g) = lim(f) ± lim(g)
  lim(f·g) = lim(f)·lim(g)
  lim(f/g) = lim(f)/lim(g)  if lim(g) ≠ 0

Special limits:
  lim(x→0) sinx/x = 1
  lim(x→0) (1-cosx)/x = 0
  lim(x→∞) (1+1/x)^x = e
  lim(x→0) (1+x)^(1/x) = e
  lim(x→0) eˣ-1/x = 1
  lim(x→0) ln(1+x)/x = 1

L'Hopital's Rule (0/0 or ∞/∞):
  lim f(x)/g(x) = lim f'(x)/g'(x)  if indeterminate form
  Other forms: 0·∞, ∞-∞, 0⁰, 1^∞, ∞⁰ → convert to 0/0 or ∞/∞

Squeeze theorem:
  g(x) ≤ f(x) ≤ h(x) and lim g = lim h = L → lim f = L
  Classic: lim(x→0) x²sin(1/x) = 0

Continuity:
  f continuous at a: lim(x→a)f(x) = f(a)
  Three conditions: f(a) defined, limit exists, limit equals f(a)
  IVT: f continuous on [a,b], f(a) < c < f(b) → ∃x: f(x) = c
  EVT: f continuous on [a,b] → attains max and min
```

---

## Differential Calculus
```
Definition:
  f'(x) = lim(h→0) [f(x+h)-f(x)]/h
  Geometric: slope of tangent line
  Physical: instantaneous rate of change

Basic rules:
  (c)' = 0               Power: (xⁿ)' = nxⁿ⁻¹
  (cf)' = cf'            Sum: (f±g)' = f'±g'
  Product: (fg)' = f'g + fg'
  Quotient: (f/g)' = (f'g-fg')/g²
  Chain: (f(g(x)))' = f'(g(x))·g'(x)

Common derivatives:
  (sin x)' = cos x        (cos x)' = -sin x
  (tan x)' = sec²x        (cot x)' = -csc²x
  (sec x)' = sec x tan x  (csc x)' = -csc x cot x
  (eˣ)' = eˣ              (aˣ)' = aˣ ln a
  (ln x)' = 1/x           (logₐx)' = 1/(x ln a)
  (arcsin x)' = 1/√(1-x²) (arccos x)' = -1/√(1-x²)
  (arctan x)' = 1/(1+x²)  (sinh x)' = cosh x

Implicit differentiation:
  Differentiate both sides with respect to x.
  Remember: d/dx[f(y)] = f'(y)·dy/dx  (chain rule)

Related rates:
  Variables change with time: differentiate implicitly wrt t.
  Pythagorean, geometric, or physical relationships.

Mean Value Theorem:
  f continuous on [a,b], differentiable on (a,b)
  → ∃c ∈ (a,b): f'(c) = [f(b)-f(a)]/(b-a)
  Rolle: f(a)=f(b) → ∃c: f'(c) = 0

Second derivative test:
  f'(c) = 0 and f''(c) > 0: local minimum
  f'(c) = 0 and f''(c) < 0: local maximum
  f''(c) = 0: inconclusive (check higher derivatives)
```

---

## Integral Calculus
```
Riemann sum:
  ∫ₐᵇ f(x)dx = lim(n→∞) Σᵢ f(xᵢ*)Δx
  Left, right, midpoint Riemann sums

Fundamental Theorem of Calculus:
  Part 1: G(x) = ∫ₐˣ f(t)dt → G'(x) = f(x)
  Part 2: ∫ₐᵇ f(x)dx = F(b) - F(a)  where F'=f
  (F is any antiderivative of f)

Common antiderivatives:
  ∫xⁿdx = xⁿ⁺¹/(n+1) + C  (n ≠ -1)
  ∫1/x dx = ln|x| + C
  ∫eˣdx = eˣ + C
  ∫sin x dx = -cos x + C
  ∫cos x dx = sin x + C
  ∫sec²x dx = tan x + C
  ∫1/√(1-x²) dx = arcsin x + C
  ∫1/(1+x²) dx = arctan x + C
```

### Integration Techniques
```python
def integration_techniques():
    return {
        'u-substitution': {
            'use':      'Composite functions, chain rule in reverse',
            'method':   'u = g(x), du = g\'(x)dx',
            'example':  '∫2x·sin(x²)dx: u=x², du=2xdx → ∫sin(u)du = -cos(u) = -cos(x²)'
        },
        'Integration by parts': {
            'formula':  '∫u dv = uv - ∫v du',
            'LIATE':    'Choose u: Logarithm, Inverse trig, Algebraic, Trig, Exponential',
            'example':  '∫x·eˣdx: u=x, dv=eˣdx → xeˣ - ∫eˣdx = xeˣ - eˣ + C',
            'tabular':  'Useful for repeated IBP (polynomial × trig/exp)'
        },
        'Partial fractions': {
            'use':      'Rational functions P(x)/Q(x)',
            'method':   'Factor denominator, decompose into partial fractions',
            'cases': {
                'linear factors':       'A/(x-a)',
                'repeated linear':      'A/(x-a) + B/(x-a)²',
                'irreducible quadratic':'(Ax+B)/(x²+bx+c)'
            }
        },
        'Trig substitution': {
            '√(a²-x²)': 'x = a·sinθ',
            '√(a²+x²)': 'x = a·tanθ',
            '√(x²-a²)': 'x = a·secθ'
        },
        'Trig integrals': {
            '∫sinⁿx cosᵐx': 'If m odd: u=sinx; if n odd: u=cosx; both even: half-angle',
            '∫tanⁿx':       'Reduce using tan²x = sec²x - 1',
            'Half-angle':   'sin²x = (1-cos2x)/2, cos²x = (1+cos2x)/2'
        }
    }
```

---

## Series & Sequences
```
Sequence: {aₙ} converges if lim(n→∞) aₙ = L
Series: Σaₙ = a₁ + a₂ + ... = lim(n→∞) Sₙ  (partial sums)

Geometric series:
  Σₙ₌₀^∞ arⁿ = a/(1-r)  for |r| < 1
  Diverges if |r| ≥ 1

p-series:
  Σ 1/nᵖ converges if p > 1, diverges if p ≤ 1

Convergence tests:
  Divergence test:  lim aₙ ≠ 0 → Σaₙ diverges
  Integral test:    Σf(n) converges ↔ ∫f(x)dx converges
  Comparison:       0 ≤ aₙ ≤ bₙ: Σbₙ converges → Σaₙ converges
  Limit comparison: lim(aₙ/bₙ) = L > 0: same convergence
  Ratio test:       L = lim|aₙ₊₁/aₙ|: L<1 converge, L>1 diverge
  Root test:        L = lim|aₙ|^(1/n): same as ratio
  Alternating:      Σ(-1)ⁿbₙ converges if bₙ→0 decreasingly

Taylor/Maclaurin series:
  f(x) = Σₙ₌₀^∞ f⁽ⁿ⁾(a)/n! · (x-a)ⁿ  (Taylor at a)
  f(x) = Σₙ₌₀^∞ f⁽ⁿ⁾(0)/n! · xⁿ  (Maclaurin, a=0)

Important Maclaurin series:
  eˣ = Σ xⁿ/n! = 1 + x + x²/2! + x³/3! + ...
  sin x = Σ (-1)ⁿx^(2n+1)/(2n+1)! = x - x³/6 + x⁵/120 - ...
  cos x = Σ (-1)ⁿx^(2n)/(2n)! = 1 - x²/2 + x⁴/24 - ...
  ln(1+x) = Σ (-1)ⁿ⁺¹xⁿ/n = x - x²/2 + x³/3 - ...  |x| ≤ 1
  1/(1-x) = Σ xⁿ = 1 + x + x² + ...  |x| < 1
  (1+x)^k = Σ C(k,n)xⁿ  (binomial series)
```

---

## Multivariable Calculus
```
Partial derivatives:
  fₓ = ∂f/∂x: differentiate wrt x, treat y as constant
  fᵧ = ∂f/∂y: differentiate wrt y, treat x as constant
  Clairaut: fₓᵧ = fᵧₓ  (if continuous second partials)

Gradient:
  ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)
  Points in direction of steepest increase
  Magnitude = rate of steepest increase
  Perpendicular to level curves/surfaces

Directional derivative:
  Dᵤf = ∇f · û  (û = unit vector in direction u)
  Maximum: in direction of ∇f, magnitude |∇f|

Total differential:
  df = fₓdx + fᵧdy + f_zdz
  Chain rule: dz/dt = fₓ(dx/dt) + fᵧ(dy/dt)

Critical points and optimization:
  Find: fₓ = 0 and fᵧ = 0
  Second derivative test: D = fₓₓfᵧᵧ - (fₓᵧ)²
    D > 0, fₓₓ > 0: local minimum
    D > 0, fₓₓ < 0: local maximum
    D < 0: saddle point
    D = 0: inconclusive

Lagrange multipliers:
  Optimize f(x,y,z) subject to g(x,y,z) = 0
  ∇f = λ∇g  and  g = 0
  Gives system: fₓ=λgₓ, fᵧ=λgᵧ, f_z=λg_z, g=0
  Multiple constraints: ∇f = λ∇g + μ∇h
```

---

## Multiple Integrals
```
Double integral:
  ∬_R f(x,y) dA = ∫∫ f(x,y) dy dx  (iterated)
  Geometric: volume under surface z=f(x,y) over region R

Fubini's theorem:
  If f continuous on R=[a,b]×[c,d]:
  ∬f dA = ∫ₐᵇ[∫_c^d f(x,y)dy]dx = ∫_c^d[∫ₐᵇ f(x,y)dx]dy

Polar coordinates:
  x = r cosθ, y = r sinθ, dA = r dr dθ
  ∬f(x,y)dA = ∫∫f(rcosθ,rsinθ) r dr dθ

Triple integral:
  ∭_E f(x,y,z) dV = ∫∫∫ f dz dy dx

Cylindrical coordinates:
  x = r cosθ, y = r sinθ, z = z
  dV = r dz dr dθ

Spherical coordinates:
  x = ρsinφcosθ, y = ρsinφsinθ, z = ρcosφ
  dV = ρ² sinφ dρ dφ dθ
  ρ = distance from origin, φ = polar angle from z-axis

Change of variables:
  ∬f(x,y)dA = ∬f(x(u,v),y(u,v))|J| du dv
  Jacobian: J = ∂(x,y)/∂(u,v) = |xᵤ xᵥ|
                                   |yᵤ yᵥ|
```

---

## Vector Calculus
```
Vector field: F(x,y,z) = P i + Q j + R k
Gradient field: F = ∇f (conservative field)

Divergence: ∇·F = ∂P/∂x + ∂Q/∂y + ∂R/∂z  (scalar)
  Positive: source, Negative: sink, Zero: incompressible

Curl: ∇×F = (Rᵧ-Q_z)i + (P_z-Rₓ)j + (Qₓ-Pᵧ)k  (vector)
  Measures rotation of field
  Conservative field: ∇×F = 0  (curl-free)

Line integral (work):
  ∫_C F·dr = ∫ₐᵇ F(r(t))·r'(t) dt
  Conservative: ∫_C F·dr = f(B) - f(A)  (path independent)

Fundamental theorem for line integrals:
  If F = ∇f: ∫_C F·dr = f(terminal) - f(initial)

Green's theorem (2D, simple closed curve C):
  ∮_C P dx + Q dy = ∬_D (Qₓ - Pᵧ) dA
  Relates line integral around C to double integral over D

Stokes' theorem (3D, surface S with boundary C):
  ∮_C F·dr = ∬_S (∇×F)·dS
  Generalizes Green's theorem to 3D

Divergence theorem (Gauss):
  ∯_S F·dS = ∭_E (∇·F) dV
  Relates flux through closed surface to volume integral
```

---

## Applications
```python
def calculus_applications():
    return {
        'Optimization': {
            'method':   'Find critical points (f\'=0), check endpoints/second derivative',
            'examples': 'Maximize area with fixed perimeter, minimize cost'
        },
        'Arc length': {
            '2D':       'L = ∫ₐᵇ √(1+(dy/dx)²) dx',
            'parametric':'L = ∫ₐᵇ √((dx/dt)²+(dy/dt)²) dt',
            '3D curve': 'L = ∫ₐᵇ |r\'(t)| dt'
        },
        'Surface area': {
            'rotation': 'S = 2π∫ₐᵇ f(x)√(1+f\'(x)²) dx',
            'surface':  'S = ∬_D √(1+fₓ²+fᵧ²) dA'
        },
        'Volume': {
            'disk method':      'V = π∫ₐᵇ [f(x)]² dx',
            'washer method':    'V = π∫ₐᵇ [R(x)²-r(x)²] dx',
            'shell method':     'V = 2π∫ₐᵇ x·f(x) dx',
            'triple integral':  'V = ∭_E dV'
        },
        'Physics': {
            'work':             'W = ∫F·dr',
            'center of mass':   'x̄ = ∬x·ρ dA / ∬ρ dA',
            'moment of inertia':'I = ∬r²·ρ dA'
        }
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Chain rule forgotten | Every composite function needs chain rule |
| Constant of integration missing | Always add +C for indefinite integrals |
| Wrong substitution back | After u-sub, substitute back to original variable |
| Forgetting Jacobian | Change of variables in multiple integrals always needs |J| |
| Confusing ∇f (gradient) with f (function) | ∇f is a vector field, f is a scalar |
| L'Hopital applied incorrectly | Only for 0/0 or ∞/∞ forms; convert other indeterminate forms first |

---

## Related Skills

- **differential-equations-expert**: ODEs and PDEs using calculus
- **linear-algebra-expert**: Vectors and matrices
- **real-analysis-expert**: Rigorous foundations of calculus
- **complex-analysis-expert**: Complex variable calculus
- **numerical-methods-expert**: Numerical integration and differentiation
- **physics-classical-mechanics**: Calculus in physics applications
