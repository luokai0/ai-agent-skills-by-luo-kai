---
name: differential-equations-expert
description: Expert-level differential equations knowledge. Use when working with ordinary differential equations, partial differential equations, systems of ODEs, Laplace transforms, Fourier methods, boundary value problems, stability analysis, or numerical methods for ODEs. Also use when the user mentions 'ODE', 'PDE', 'initial value problem', 'boundary value problem', 'Laplace transform', 'separation of variables', 'eigenvalue problem', 'heat equation', 'wave equation', 'Laplace equation', 'stability', or 'phase plane'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Differential Equations Expert

You are a world-class mathematician with deep expertise in ordinary and partial differential equations, covering analytical methods, transform techniques, stability theory, boundary value problems, and numerical methods.

## Before Starting

1. **Type** — ODE, PDE, system, or stochastic DE?
2. **Level** — Undergraduate, graduate, or research?
3. **Goal** — Find solution, analyze behavior, or apply numerical method?
4. **Context** — Pure math, physics, engineering, or biology?
5. **Method** — Analytical, transform, series, or numerical?

---

## Core Expertise Areas

- **First-Order ODEs**: separable, linear, exact, Bernoulli, Riccati
- **Higher-Order ODEs**: constant coefficients, variation of parameters, Cauchy-Euler
- **Systems of ODEs**: phase plane, stability, linearization
- **Laplace & Fourier Transforms**: solving IVPs, convolution
- **Series Solutions**: power series, Frobenius method, special functions
- **PDEs**: heat, wave, Laplace equations; separation of variables
- **Boundary Value Problems**: Sturm-Liouville, eigenfunction expansions
- **Stability Theory**: Lyapunov, phase portraits, bifurcations

---

## First-Order ODEs
```
General form: dy/dx = f(x,y)

Separable: dy/dx = g(x)h(y)
  → ∫ dy/h(y) = ∫ g(x)dx
  Example: dy/dx = xy → ∫dy/y = ∫x dx → ln|y| = x²/2 + C

Linear: dy/dx + P(x)y = Q(x)
  Integrating factor: μ(x) = exp(∫P(x)dx)
  Solution: y = (1/μ)[∫μQ dx + C]
  Example: dy/dx + 2y = 4x
    μ = e²ˣ, d(e²ˣy)/dx = 4xe²ˣ → y = 2x-1 + Ce^(-2x)

Exact: M dx + N dy = 0 where ∂M/∂y = ∂N/∂x
  Solution: F(x,y) = C where ∂F/∂x = M, ∂F/∂y = N

Bernoulli: dy/dx + P(x)y = Q(x)yⁿ
  Substitution: v = y^(1-n) → linear in v

Riccati: dy/dx = P(x) + Q(x)y + R(x)y²
  If particular solution y₁ known: y = y₁ + 1/v (linear in v)

Existence and uniqueness (Picard-Lindelof):
  f continuous and Lipschitz in y → unique solution to IVP y(x₀) = y₀
  |f(x,y₁) - f(x,y₂)| ≤ L|y₁-y₂|  (Lipschitz condition)

Autonomous: dy/dx = f(y)
  Equilibria: f(y*) = 0
  Stable: f'(y*) < 0, Unstable: f'(y*) > 0
  Direction field analysis
```

---

## Higher-Order Linear ODEs
```
General: aₙy⁽ⁿ⁾ + ... + a₁y' + a₀y = g(x)

Homogeneous (g=0): characteristic equation
  aₙrⁿ + ... + a₁r + a₀ = 0
  Roots determine solution:
    Real distinct r₁,r₂: y = C₁e^(r₁x) + C₂e^(r₂x)
    Repeated root r: y = (C₁+C₂x)e^(rx)
    Complex r = α±βi: y = eᵅˣ(C₁cosβx + C₂sinβx)

Method of undetermined coefficients:
  For g(x) = polynomial, exponential, sin/cos, or products:
  Guess yₚ of same form (modify if guess solves homogeneous)
  g = xⁿ → guess Aₙxⁿ+...+A₀
  g = eᵅˣ → guess Aeᵅˣ (or Axeᵅˣ if α is characteristic root)
  g = sin(βx) or cos(βx) → guess A cosβx + B sinβx

Variation of parameters:
  y = y₁u₁ + y₂u₂ where y₁,y₂ fundamental solutions
  u₁' = -y₂g(x)/W, u₂' = y₁g(x)/W
  W = Wronskian = y₁y₂' - y₁'y₂
  Works for any continuous g(x)

Cauchy-Euler equation:
  axⁿy⁽ⁿ⁾ + ... + a₁xy' + a₀y = 0
  Substitution x = eᵗ → constant coefficient equation
  Try y = xʳ → characteristic equation in r

Reduction of order:
  If y₁ known: y = v(x)y₁
  Substitution reduces to first-order for v'

Abel's identity:
  W(x) = W(x₀)exp(-∫ₓ₀ˣ P(t)dt)  for y'' + P(x)y' + Q(x)y = 0
```

---

## Systems of ODEs
```
System: x' = Ax (constant coefficient)
  A: n×n matrix, x: n-vector of unknowns

Eigenvalue method:
  Find eigenvalues λ and eigenvectors v of A
  If A has n linearly independent eigenvectors:
    x = Σ Cᵢvᵢe^(λᵢt)

Cases:
  Real distinct eigenvalues: straightforward sum
  Complex eigenvalues α±βi with eigenvector a±bi:
    x₁ = eᵅᵗ(a cosβt - b sinβt)
    x₂ = eᵅᵗ(a sinβt + b cosβt)
  Repeated eigenvalue λ:
    If defective: x₁=veˡᵗ, x₂=(vt+w)eˡᵗ where (A-λI)w=v

Matrix exponential:
  x(t) = e^(At)x₀  (fundamental matrix solution)
  e^(At) = Σ (At)ⁿ/n!
  For diagonalizable A: e^(At) = Pe^(Dt)P⁻¹

Phase plane (2D autonomous):
  x' = f(x,y), y' = g(x,y)
  Equilibrium: f(x*,y*) = g(x*,y*) = 0
  Nullclines: f=0 and g=0 curves
  Linearization at (x*,y*): Jacobian J = [[∂f/∂x, ∂f/∂y],[∂g/∂x, ∂g/∂y]]

Classification of equilibria (eigenvalues of J):
  λ₁,λ₂ real, same sign:   Node (stable: both neg, unstable: both pos)
  λ₁,λ₂ real, opposite:    Saddle (always unstable)
  Complex α±βi, α<0:        Stable spiral
  Complex α±βi, α>0:        Unstable spiral
  Pure imaginary ±βi:       Center (neutrally stable)
```

---

## Laplace Transform
```python
def laplace_transforms():
    return {
        'Definition':   'L{f(t)} = F(s) = ∫₀^∞ e^(-st)f(t)dt',
        'Common pairs': {
            '1':            '1/s',
            't':            '1/s²',
            'tⁿ':           'n!/s^(n+1)',
            'eᵅᵗ':          '1/(s-a)',
            'sin(bt)':      'b/(s²+b²)',
            'cos(bt)':      's/(s²+b²)',
            'eᵅᵗsin(bt)':   'b/((s-a)²+b²)',
            'eᵅᵗcos(bt)':   '(s-a)/((s-a)²+b²)',
            'unit step u(t-a)': 'e^(-as)/s',
            'δ(t)':         '1',
            'δ(t-a)':       'e^(-as)',
            't f(t)':       '-F\'(s)',
            'f\'(t)':       'sF(s) - f(0)',
            'f\'\'(t)':     's²F(s) - sf(0) - f\'(0)'
        },
        'Properties': {
            'Linearity':        'L{af+bg} = aF+bG',
            's-shifting':       'L{eᵃᵗf(t)} = F(s-a)',
            't-shifting':       'L{u(t-a)f(t-a)} = e^(-as)F(s)',
            'Convolution':      'L{(f*g)(t)} = F(s)G(s)',
            'Periodic':         'L{f} = ∫₀ᵀe^(-st)f dt / (1-e^(-sT))'
        },
        'Solving IVPs': [
            '1. Take Laplace transform of both sides',
            '2. Use initial conditions to eliminate constants',
            '3. Solve algebraically for Y(s) = L{y(t)}',
            '4. Invert using partial fractions + table',
            '5. Use convolution theorem if needed'
        ]
    }

def partial_fractions_laplace():
    return {
        'Distinct real roots':      'A/(s-r₁) + B/(s-r₂) + ...',
        'Repeated real roots':      'A/(s-r) + B/(s-r)² + ...',
        'Complex conjugate roots':  '(As+B)/(s²+bs+c)',
        'Heaviside cover-up':       'For distinct linear factors: multiply by (s-rᵢ), set s=rᵢ'
    }
```

---

## Fourier Series & Transform
```
Fourier series (periodic function, period 2L):
  f(x) = a₀/2 + Σₙ₌₁^∞ [aₙcos(nπx/L) + bₙsin(nπx/L)]
  a₀ = (1/L)∫₋ₗᴸ f(x)dx
  aₙ = (1/L)∫₋ₗᴸ f(x)cos(nπx/L)dx
  bₙ = (1/L)∫₋ₗᴸ f(x)sin(nπx/L)dx

Complex form:
  f(x) = Σ cₙe^(inπx/L), cₙ = (1/2L)∫₋ₗᴸ f(x)e^(-inπx/L)dx

Convergence:
  Dirichlet conditions: piecewise smooth → converges to f at continuity
  At jump: converges to average (f(x⁺)+f(x⁻))/2
  Gibbs phenomenon: ~9% overshoot near jump (doesn't decrease with more terms)
  Parseval's theorem: (1/L)∫|f|² = a₀²/2 + Σ(aₙ²+bₙ²)

Fourier transform:
  F̂(ω) = ∫₋∞^∞ f(x)e^(-iωx)dx
  f(x) = (1/2π)∫₋∞^∞ F̂(ω)e^(iωx)dω
  Convolution: F{f*g} = F{f}·F{g}
  Plancherel: ∫|f|² dx = (1/2π)∫|F̂|² dω
```

---

## Partial Differential Equations

### Heat Equation
```
∂u/∂t = α²∂²u/∂x²  (α² = thermal diffusivity)

Separation of variables on [0,L]:
  u(x,t) = X(x)T(t)
  T'/α²T = X''/X = -λ  (separation constant)

Boundary conditions u(0,t)=u(L,t)=0:
  Eigenvalue problem: X'' + λX = 0, X(0)=X(L)=0
  Eigenvalues: λₙ = (nπ/L)², n=1,2,3,...
  Eigenfunctions: Xₙ = sin(nπx/L)

Solution:
  u(x,t) = Σₙ Bₙ sin(nπx/L)e^(-α²(nπ/L)²t)
  Bₙ = (2/L)∫₀ᴸ f(x)sin(nπx/L)dx  (from initial condition u(x,0)=f(x))

Interpretation: Each mode decays exponentially; higher modes decay faster
```

### Wave Equation
```
∂²u/∂t² = c²∂²u/∂x²  (c = wave speed)

D'Alembert solution (infinite domain):
  u(x,t) = f(x+ct) + g(x-ct)
  From ICs: u(x,0)=p(x), uₜ(x,0)=q(x):
  u = (p(x+ct)+p(x-ct))/2 + (1/2c)∫_{x-ct}^{x+ct} q(s)ds

Separation on [0,L] with u(0,t)=u(L,t)=0:
  u(x,t) = Σₙ sin(nπx/L)[Aₙcos(nπct/L) + Bₙsin(nπct/L)]
  Aₙ from p(x), Bₙ from q(x) via Fourier sine series
  Standing waves: nodes at fixed positions
```

### Laplace Equation
```
∇²u = ∂²u/∂x² + ∂²u/∂y² = 0  (steady state, potential theory)

On rectangle [0,a]×[0,b]:
  Separate: X''Y + XY'' = 0 → X''/X = -Y''/Y = λ
  Choose BCs to fix λ

Circular domain (polar):
  ∇²u = (1/r)∂/∂r(r∂u/∂r) + (1/r²)∂²u/∂θ² = 0
  Solution: u = A₀ + Σ rⁿ(Aₙcosnθ + Bₙsinnθ)

Mean value property:
  u harmonic: u(x₀) = (1/|∂B|)∫_{∂B} u dS  (average on any sphere)
  Maximum principle: harmonic function attains max/min on boundary
```

---

## Sturm-Liouville Theory
```
Sturm-Liouville problem:
  [p(x)y']' + [q(x) + λw(x)]y = 0  on [a,b]
  with boundary conditions
  p, q, w continuous, p,w > 0

Properties:
  Eigenvalues: real, countably infinite, λ₁<λ₂<λ₃<...→∞
  Eigenfunctions: orthogonal with weight w
    ∫ₐᵇ yₘyₙw dx = 0 for m≠n
  Completeness: can expand any piecewise smooth f in eigenfunctions

Regular examples:
  y'' + λy = 0, y(0)=y(L)=0: λₙ=(nπ/L)², yₙ=sin(nπx/L)
  y'' + λy = 0, y'(0)=y'(L)=0: λₙ=(nπ/L)², yₙ=cos(nπx/L)

Singular examples:
  Bessel equation: xy'' + y' + (λx-n²/x)y = 0 → Jₙ(√λ x)
  Legendre equation: (1-x²)y'' - 2xy' + λy = 0 → Pₙ(x)
  Chebyshev, Hermite, Laguerre equations
```

---

## Stability Theory
```python
def stability_analysis():
    return {
        'Lyapunov stability': {
            'stable':           'Solutions starting near x* stay near x*',
            'asymptotically':   'Solutions starting near x* approach x*',
            'Lyapunov function':'V(x) > 0, dV/dt ≤ 0 → stable',
            'finding V':        'Try V = xᵀPx (quadratic), then verify dV/dt'
        },
        'Linear stability (x\' = Ax)': {
            'stable':           'All eigenvalues have Re(λ) ≤ 0',
            'asymptotically':   'All eigenvalues have Re(λ) < 0',
            'unstable':         'Any eigenvalue has Re(λ) > 0'
        },
        'Nonlinear stability (x\' = f(x))': {
            'method':           'Linearize at equilibrium x*: A = Df(x*)',
            'hyperbolic':       'No eigenvalue on imaginary axis → linear determines stability',
            'non-hyperbolic':   'Need Lyapunov or center manifold theory'
        },
        'Bifurcation theory': {
            'saddle-node':      'Two equilibria collide and disappear (fold bifurcation)',
            'transcritical':    'Two equilibria exchange stability',
            'pitchfork':        'One equilibrium splits into three',
            'Hopf':             'Equilibrium loses stability → limit cycle appears',
            'normal_form':      'Canonical form near bifurcation point'
        },
        'Poincare-Bendixson (2D)': {
            'theorem':          'Bounded orbit in ℝ² → equilibrium or limit cycle',
            'index theory':     'Sum of indices of equilibria inside closed orbit = +1',
            'Dulac criterion':  'If div(fB) has one sign → no closed orbits'
        }
    }
```

---

## Numerical Methods for ODEs
```python
def numerical_ode_methods():
    return {
        'Euler method': {
            'formula':  'yₙ₊₁ = yₙ + h·f(tₙ,yₙ)',
            'order':    'First order: error O(h)',
            'use':      'Simple, educational; not for precision'
        },
        'Runge-Kutta 4 (RK4)': {
            'k1': 'h·f(tₙ, yₙ)',
            'k2': 'h·f(tₙ+h/2, yₙ+k1/2)',
            'k3': 'h·f(tₙ+h/2, yₙ+k2/2)',
            'k4': 'h·f(tₙ+h, yₙ+k3)',
            'formula': 'yₙ₊₁ = yₙ + (k1+2k2+2k3+k4)/6',
            'order':   'Fourth order: error O(h⁴), gold standard explicit method'
        },
        'Stiff equations': {
            'definition':   'Solution varies on vastly different timescales',
            'problem':      'Explicit methods require tiny h → slow',
            'solution':     'Implicit methods (Backward Euler, trapezoidal, BDF)',
            'BDF':          'Backward Differentiation Formulas (MATLAB ode15s)',
            'example':      'Chemical kinetics, electrical circuits'
        },
        'Adaptive step size': {
            'idea':         'Estimate error, adjust h automatically',
            'RK45':         'Dormand-Prince: 4th and 5th order, compare for error',
            'tolerance':    'rtol (relative), atol (absolute)',
            'MATLAB':       'ode45 (non-stiff), ode15s (stiff)'
        },
        'Boundary value problems': {
            'shooting':     'Convert to IVP, shoot from one end, adjust to hit BC',
            'finite difference': 'Discretize derivatives, solve linear system',
            'collocation':  'Approximate with polynomials, match at collocation points'
        }
    }
```

---

## Series Solutions
```
Power series method:
  Assume y = Σ aₙxⁿ (or Σ aₙ(x-x₀)ⁿ)
  Substitute, match coefficients of xⁿ
  Find recurrence relation for aₙ

Ordinary point x₀: P(x₀) ≠ 0 in y'' + P(x)y' + Q(x)y = 0
  Two linearly independent power series solutions

Regular singular point x₀:
  (x-x₀)P(x) and (x-x₀)²Q(x) have convergent series at x₀
  Frobenius method: y = Σ aₙ(x-x₀)^(n+r)  (r = indicial roots)
  Indicial equation: r(r-1) + p₀r + q₀ = 0  (p₀,q₀ = limits at x₀)

Cases (r₁ ≥ r₂):
  r₁-r₂ ∉ ℤ: two independent Frobenius series
  r₁-r₂ = 0: second solution involves log term
  r₁-r₂ ∈ ℤ⁺: second solution may involve log term

Bessel equation:
  x²y'' + xy' + (x²-ν²)y = 0
  Jν(x) = Σ (-1)ᵐ/(m!Γ(m+ν+1)) (x/2)^(2m+ν)  (Bessel function first kind)
  Yν(x): second kind (singular at x=0)
  Applications: cylindrical problems (heat, vibration, waves)

Legendre equation:
  (1-x²)y'' - 2xy' + n(n+1)y = 0
  Pₙ(x): Legendre polynomials (bounded at ±1)
  P₀=1, P₁=x, P₂=(3x²-1)/2, P₃=(5x³-3x)/2
  Rodrigues: Pₙ(x) = (1/2ⁿn!) dⁿ/dxⁿ[(x²-1)ⁿ]
  Applications: spherical problems
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Forgetting +C in first-order | Always add arbitrary constant, apply IC to find it |
| Undetermined coefficients for resonance | Multiply guess by x (or x²) if guess solves homogeneous |
| Wrong Laplace of derivative | L{y'} = sY-y(0); L{y''} = s²Y-sy(0)-y'(0) |
| Fourier series convergence | At jumps: converges to average, not to function value |
| PDE separation fails | Check all boundary conditions match the separated form |
| Stability from eigenvalues | Real part of eigenvalue determines stability, not magnitude |

---

## Related Skills

- **calculus-expert**: Integration techniques, series
- **linear-algebra-expert**: Systems of ODEs, matrix exponential
- **numerical-methods-expert**: Numerical PDE solvers
- **physics-classical-mechanics**: ODEs in mechanics
- **physics-electromagnetism**: PDEs in EM theory
- **probability-expert**: Stochastic differential equations
