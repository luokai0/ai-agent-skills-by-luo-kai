---
author: luo-kai
name: numerical-methods-expert
description: Expert-level numerical methods knowledge. Use when working with root finding, numerical integration, numerical differentiation, interpolation, numerical linear algebra, ODEs, PDEs, or optimization algorithms. Also use when the user mentions 'Newton method', 'bisection', 'Runge-Kutta', 'finite difference', 'finite element', 'interpolation', 'numerical integration', 'quadrature', 'iterative solvers', 'condition number', 'round-off error', or 'truncation error'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Numerical Methods Expert

You are a world-class numerical analyst with deep expertise in numerical algorithms, error analysis, root finding, interpolation, numerical integration, linear systems, ODEs, PDEs, and optimization.

## Before Starting

1. **Problem** — Root finding, integration, linear system, ODE, PDE, or optimization?
2. **Level** — Undergraduate or graduate/research?
3. **Goal** — Implement algorithm, analyze error, or choose method?
4. **Context** — Scientific computing, engineering simulation, or data science?
5. **Constraints** — Accuracy requirements, computational cost, or stability?

---

## Core Expertise Areas

- **Error Analysis**: floating point, round-off, truncation, condition number
- **Root Finding**: bisection, Newton-Raphson, secant, fixed-point iteration
- **Interpolation**: polynomial, spline, Lagrange, Newton divided differences
- **Numerical Integration**: trapezoidal, Simpson, Gaussian quadrature, adaptive
- **Numerical Differentiation**: finite differences, Richardson extrapolation
- **Linear Systems**: LU, Cholesky, iterative methods, least squares
- **Eigenvalue Problems**: power iteration, QR algorithm, Lanczos
- **ODEs & PDEs**: Runge-Kutta, stiff solvers, finite differences, finite elements

---

## Error Analysis
```python
def error_analysis():
    return {
        'Types of error': {
            'Round-off':    'Finite precision arithmetic (machine epsilon ε ≈ 2.2×10⁻¹⁶ for float64)',
            'Truncation':   'Approximating infinite process by finite one (Taylor series cutoff)',
            'Data error':   'Errors in input data',
            'Blunders':     'Programming mistakes'
        },
        'Absolute error':   '|x_approx - x_true|',
        'Relative error':   '|x_approx - x_true| / |x_true|',
        'Significant digits':'Number of reliable digits in result',
        'Machine epsilon':  'Smallest ε: fl(1+ε) > 1, ε ≈ 2.2×10⁻¹⁶ (double precision)',
        'Floating point':   'fl(x) = x(1+δ) where |δ| ≤ ε (relative error bounded)',
        'Catastrophic cancellation': 'Subtracting nearly equal numbers → massive relative error',
        'Example fix':      'x² - 1 near x=1: use (x-1)(x+1) instead',
    }

def condition_number():
    """
    Condition number measures sensitivity to perturbations.
    """
    return {
        'Definition':       'κ(A) = ||A|| · ||A⁻¹|| = σ_max/σ_min',
        'Interpretation':   'κ significant digits lost ≈ log₁₀(κ)',
        'Well-conditioned':  'κ ≈ 1: small perturbation → small change',
        'Ill-conditioned':   'κ >> 1: small perturbation → large change',
        'Relative error':    '||Δx||/||x|| ≤ κ(A) · ||Δb||/||b||',
        'Examples': {
            'Identity':     'κ = 1 (perfect)',
            'Hilbert matrix':'κ grows exponentially with size (pathological)',
            'Vandermonde':  'Often ill-conditioned for large n'
        }
    }

import numpy as np

def floating_point_pitfalls():
    """
    Demonstrate common floating point issues.
    """
    # Catastrophic cancellation
    x = 1.0 + 1e-15
    bad = x**2 - 1.0  # loses precision
    good = (x-1)*(x+1)  # algebraically equivalent, numerically better

    # Order of operations matters
    s_forward = sum(1.0/k for k in range(1, 1001))   # small numbers added to large
    s_backward = sum(1.0/k for k in range(1000, 0, -1))  # more accurate

    return {
        'cancellation_bad':  bad,
        'cancellation_good': good,
        'sum_forward':       round(s_forward, 10),
        'sum_backward':      round(s_backward, 10),
        'rule':              'Add small numbers first for better accuracy'
    }
```

---

## Root Finding
```python
def bisection_method(f, a, b, tol=1e-10, max_iter=100):
    """
    Bisection method: guaranteed convergence, linear rate.
    Requires f(a) and f(b) have opposite signs.
    """
    if f(a) * f(b) > 0:
        raise ValueError("f(a) and f(b) must have opposite signs")

    iterations = []
    for i in range(max_iter):
        c = (a + b) / 2
        fc = f(c)
        iterations.append({'iter': i+1, 'a': a, 'b': b, 'c': c, 'f(c)': fc})

        if abs(fc) < tol or (b-a)/2 < tol:
            break
        if f(a) * fc < 0:
            b = c
        else:
            a = c

    return c, iterations

def newton_raphson(f, df, x0, tol=1e-10, max_iter=50):
    """
    Newton-Raphson: quadratic convergence near simple root.
    xₙ₊₁ = xₙ - f(xₙ)/f'(xₙ)
    """
    x = x0
    history = [x0]

    for i in range(max_iter):
        fx = f(x)
        dfx = df(x)

        if abs(dfx) < 1e-15:
            raise ZeroDivisionError("Derivative too small")

        x_new = x - fx/dfx
        history.append(x_new)

        if abs(x_new - x) < tol:
            break
        x = x_new

    return x, history

def secant_method(f, x0, x1, tol=1e-10, max_iter=50):
    """
    Secant method: superlinear convergence (~1.618), no derivative needed.
    xₙ₊₁ = xₙ - f(xₙ)(xₙ-xₙ₋₁)/(f(xₙ)-f(xₙ₋₁))
    """
    for i in range(max_iter):
        f0, f1 = f(x0), f(x1)
        if abs(f1 - f0) < 1e-15:
            break
        x2 = x1 - f1*(x1-x0)/(f1-f0)
        if abs(x2 - x1) < tol:
            return x2
        x0, x1 = x1, x2
    return x1

def fixed_point_iteration(g, x0, tol=1e-10, max_iter=100):
    """
    Fixed point: x = g(x), converges if |g'(x*)| < 1.
    Linear convergence rate = |g'(x*)|.
    """
    x = x0
    for i in range(max_iter):
        x_new = g(x)
        if abs(x_new - x) < tol:
            return x_new, i+1
        x = x_new
    return x, max_iter

def convergence_rates():
    return {
        'Bisection':        'Linear, rate = 0.5 (1 bit per iteration)',
        'Newton-Raphson':   'Quadratic near simple root (doubles digits)',
        'Secant':           'Superlinear, order φ = (1+√5)/2 ≈ 1.618',
        'Fixed point':      'Linear, rate = |g\'(x*)|',
        'Müller\'s method': 'Order ≈ 1.84 (uses quadratic interpolation)',
        'Regula Falsi':     'Linear but faster than bisection in practice'
    }
```

---

## Interpolation
```python
def lagrange_interpolation(x_data, y_data, x_eval):
    """
    Lagrange polynomial interpolation.
    P(x) = Σ yᵢ · Lᵢ(x)
    Lᵢ(x) = Π_{j≠i} (x-xⱼ)/(xᵢ-xⱼ)
    """
    n = len(x_data)
    result = 0.0

    for i in range(n):
        L = 1.0
        for j in range(n):
            if j != i:
                L *= (x_eval - x_data[j]) / (x_data[i] - x_data[j])
        result += y_data[i] * L

    return result

def newton_divided_differences(x_data, y_data):
    """
    Newton's divided difference table.
    More numerically stable than Lagrange for adding points.
    """
    n = len(x_data)
    F = np.array([[0.0]*n for _ in range(n)])

    for i in range(n):
        F[i][0] = y_data[i]

    for j in range(1, n):
        for i in range(n-j):
            F[i][j] = (F[i+1][j-1] - F[i][j-1]) / (x_data[i+j] - x_data[i])

    # Coefficients = F[0][0], F[0][1], ..., F[0][n-1]
    coeffs = [F[0][j] for j in range(n)]
    return coeffs, F

def cubic_spline(x_data, y_data):
    """
    Natural cubic spline interpolation.
    C² continuous, minimizes oscillation (Runge's phenomenon avoidance).
    """
    n = len(x_data) - 1
    h = [x_data[i+1] - x_data[i] for i in range(n)]

    # Set up tridiagonal system for second derivatives
    # Natural spline: S''(x₀) = S''(xₙ) = 0
    # ... (tridiagonal solve)
    return "Cubic spline coefficients (solve tridiagonal system)"

def interpolation_concepts():
    return {
        'Runge\'s phenomenon': {
            'issue':        'High-degree polynomial oscillates wildly near endpoints',
            'example':      '1/(1+25x²) on [-1,1] with equally spaced nodes',
            'solutions':    'Use Chebyshev nodes, splines, or low-degree piecewise'
        },
        'Chebyshev nodes': {
            'formula':      'xₖ = cos((2k+1)π/(2n+2)) for k=0,...,n',
            'property':     'Minimize Lebesgue constant, reduce Runge\'s phenomenon',
            'optimal':      'Best node distribution for polynomial interpolation'
        },
        'Error bound': {
            'Lagrange':     '|f(x)-Pₙ(x)| ≤ max|f^(n+1)|/(n+1)! · |ω(x)|',
            'ω(x)':         'Πᵢ(x-xᵢ) (node polynomial)',
            'control':      'Better nodes (Chebyshev) → smaller |ω(x)|'
        }
    }
```

---

## Numerical Integration (Quadrature)
```python
def numerical_integration_methods():
    return {
        'Trapezoidal rule': {
            'formula':      '∫ₐᵇf dx ≈ h/2 [f(x₀)+2f(x₁)+...+2f(xₙ₋₁)+f(xₙ)]',
            'error':        'O(h²) per step, O(h²) global',
            'composite':    'n subintervals of width h=(b-a)/n'
        },
        'Simpson\'s 1/3 rule': {
            'formula':      '∫ₐᵇf dx ≈ h/3 [f(x₀)+4f(x₁)+2f(x₂)+...+4f(xₙ₋₁)+f(xₙ)]',
            'error':        'O(h⁴) global (requires even n)',
            'note':         'Exact for polynomials of degree ≤ 3'
        },
        'Simpson\'s 3/8 rule': {
            'formula':      '3h/8 [f₀+3f₁+3f₂+2f₃+...+fₙ] (n divisible by 3)',
            'error':        'O(h⁴) global'
        },
        'Gaussian quadrature': {
            'idea':         'Choose both nodes AND weights optimally',
            'n-point rule': 'Exact for polynomials of degree ≤ 2n-1',
            'Gauss-Legendre':'Nodes = roots of Legendre polynomials on [-1,1]',
            'transform':    '∫ₐᵇf(x)dx = (b-a)/2 ∫₋₁¹ f((b-a)t/2+(a+b)/2) dt',
            'points_weights': {
                'n=2': 'x=±1/√3, w=1',
                'n=3': 'x=0,±√(3/5), w=8/9, 5/9'
            }
        },
        'Adaptive quadrature': {
            'idea':         'Subdivide intervals where error estimate is large',
            'stopping':     '|coarse - fine| < tolerance',
            'Python':       'scipy.integrate.quad implements this'
        },
        'Monte Carlo integration': {
            'formula':      '∫f dx ≈ (b-a)/N Σf(xᵢ) where xᵢ uniform random',
            'error':        'O(1/√N) regardless of dimension',
            'best_for':     'High-dimensional integrals (d >> 1)'
        }
    }

def composite_simpson(f, a, b, n):
    """
    Composite Simpson's rule: n must be even.
    """
    if n % 2 != 0:
        n += 1
    h = (b - a) / n
    x = np.linspace(a, b, n+1)
    y = np.array([f(xi) for xi in x])

    result = y[0] + y[-1]
    result += 4 * np.sum(y[1:-1:2])   # odd indices
    result += 2 * np.sum(y[2:-2:2])   # even indices (not endpoints)
    return result * h / 3

def romberg_integration(f, a, b, max_rows=10):
    """
    Romberg integration: Richardson extrapolation applied to trapezoidal rule.
    R[n,m] = (4ᵐR[n,m-1] - R[n-1,m-1]) / (4ᵐ - 1)
    """
    R = np.zeros((max_rows, max_rows))

    # First column: trapezoidal with 2^n subintervals
    for n in range(max_rows):
        N = 2**n
        h = (b-a)/N
        x = np.linspace(a, b, N+1)
        R[n,0] = h/2 * (f(a) + f(b) + 2*sum(f(xi) for xi in x[1:-1]))

    # Richardson extrapolation
    for m in range(1, max_rows):
        for n in range(m, max_rows):
            R[n,m] = (4**m * R[n,m-1] - R[n-1,m-1]) / (4**m - 1)

    return R
```

---

## Numerical Differentiation
```python
def finite_differences():
    return {
        'Forward difference':   '(f(x+h) - f(x))/h — O(h) error',
        'Backward difference':  '(f(x) - f(x-h))/h — O(h) error',
        'Central difference':   '(f(x+h) - f(x-h))/(2h) — O(h²) error',
        'Second derivative':    '(f(x+h) - 2f(x) + f(x-h))/h² — O(h²) error',
        'Fourth order central': '(-f(x+2h)+8f(x+h)-8f(x-h)+f(x-2h))/(12h) — O(h⁴)',
        'Optimal h':            '~√ε_machine for first derivative ≈ 10⁻⁸',
        'Trade-off':            'Smaller h: less truncation, more round-off'
    }

def richardson_extrapolation(f, x, h, order=1):
    """
    Richardson extrapolation to improve accuracy.
    D(h) = f'(x) + C·hᵖ + O(h^(p+1))
    D(h/2) = f'(x) + C·(h/2)ᵖ + ...
    Extrapolated: f'(x) ≈ (2ᵖD(h/2) - D(h))/(2ᵖ-1)
    """
    D_h  = (f(x+h) - f(x-h)) / (2*h)        # O(h²)
    D_h2 = (f(x+h/2) - f(x-h/2)) / h        # O(h²)
    # Extrapolate to O(h⁴)
    extrapolated = (4*D_h2 - D_h) / 3
    return {
        'D(h)':         D_h,
        'D(h/2)':       D_h2,
        'extrapolated': extrapolated
    }
```

---

## Numerical Linear Algebra
```python
def numerical_linear_algebra():
    return {
        'LU decomposition': {
            'factorization':'A = LU (L lower triangular, U upper triangular)',
            'partial_pivot':'PA = LU for numerical stability',
            'solve':        'Ax=b: Ly=Pb (forward), Ux=y (backward)',
            'cost':         'O(n³) factorization, O(n²) per solve',
            'use':          'Multiple right-hand sides with same A'
        },
        'Cholesky': {
            'for':          'Symmetric positive definite A = LLᵀ',
            'cost':         'Half the cost of LU',
            'stability':    'Always stable for SPD matrices'
        },
        'QR decomposition': {
            'factorization':'A = QR (Q orthogonal, R upper triangular)',
            'methods':      'Gram-Schmidt, Householder (more stable), Givens',
            'use':          'Least squares (more stable than normal equations)',
            'eigenvalues':  'QR algorithm for all eigenvalues'
        },
        'Iterative methods (large sparse)': {
            'Jacobi':       'xᵢ^(k+1) = (bᵢ - Σⱼ≠ᵢ aᵢⱼxⱼ^(k)) / aᵢᵢ',
            'Gauss-Seidel': 'Use updated values immediately',
            'SOR':          'Over-relaxation: ω∈(1,2) speeds Gauss-Seidel',
            'CG':           'Conjugate Gradient for SPD (optimal Krylov)',
            'GMRES':        'General non-symmetric systems',
            'convergence':  'Depends on spectral radius ρ(iteration matrix)'
        },
        'Preconditioning': {
            'idea':         'Solve M⁻¹Ax = M⁻¹b (better conditioned)',
            'incomplete_LU':'ILU: sparse approximate factorization',
            'diagonal':     'Jacobi preconditioner: M = diag(A)'
        }
    }

def power_iteration(A, num_iterations=100, tol=1e-10):
    """
    Power iteration: finds largest eigenvalue and eigenvector.
    v_{k+1} = Av_k / ||Av_k||
    """
    n = A.shape[0]
    v = np.random.rand(n)
    v = v / np.linalg.norm(v)

    eigenvalue = 0
    for i in range(num_iterations):
        Av = A @ v
        eigenvalue_new = np.dot(v, Av)
        v = Av / np.linalg.norm(Av)

        if abs(eigenvalue_new - eigenvalue) < tol:
            break
        eigenvalue = eigenvalue_new

    return eigenvalue, v
```

---

## Numerical ODEs
```python
def ode_methods():
    return {
        'Euler (explicit)': {
            'formula':      'y_{n+1} = y_n + h·f(t_n, y_n)',
            'order':        '1st order: error O(h)',
            'stability':    'Conditionally stable: h < 2/|λ| for stiff',
            'use':          'Simple demonstration, not production'
        },
        'Runge-Kutta 4': {
            'k1':           'h·f(tₙ, yₙ)',
            'k2':           'h·f(tₙ+h/2, yₙ+k1/2)',
            'k3':           'h·f(tₙ+h/2, yₙ+k2/2)',
            'k4':           'h·f(tₙ+h, yₙ+k3)',
            'formula':      'y_{n+1} = y_n + (k1+2k2+2k3+k4)/6',
            'order':        '4th order: error O(h⁴)',
            'use':          'Standard for non-stiff problems'
        },
        'Dormand-Prince (RK45)': {
            'idea':         'Embedded 4th and 5th order for error estimation',
            'adaptive':     'Adjust h based on ||y₅-y₄||',
            'implementation':'scipy.integrate.solve_ivp default'
        },
        'Stiff equations': {
            'problem':      'Solution varies on multiple timescales',
            'symptom':      'Explicit methods require tiny h',
            'solution':     'Implicit methods (backward Euler, trapezoidal, BDF)',
            'backward_euler':'y_{n+1} = y_n + h·f(t_{n+1}, y_{n+1}) (solve nonlinear)',
            'BDF':          'Backward Differentiation Formulas (scipy ode15s equivalent)'
        },
        'Multistep methods': {
            'Adams-Bashforth':'Explicit, uses previous steps',
            'Adams-Moulton': 'Implicit, higher accuracy',
            'BDF':           'Stiff solvers, variable order'
        }
    }

def rk4_solver(f, y0, t_span, h):
    """
    Classic RK4 ODE solver.
    """
    t0, tf = t_span
    t = np.arange(t0, tf+h, h)
    y = np.zeros((len(t), len(np.atleast_1d(y0))))
    y[0] = y0

    for i in range(len(t)-1):
        k1 = h * np.array(f(t[i], y[i]))
        k2 = h * np.array(f(t[i]+h/2, y[i]+k1/2))
        k3 = h * np.array(f(t[i]+h/2, y[i]+k2/2))
        k4 = h * np.array(f(t[i]+h, y[i]+k3))
        y[i+1] = y[i] + (k1 + 2*k2 + 2*k3 + k4) / 6

    return t, y
```

---

## Numerical PDEs
```python
def pde_methods():
    return {
        'Finite Difference Method (FDM)': {
            'idea':         'Replace derivatives with finite differences on grid',
            'heat_explicit':'u^(n+1)_i = u^n_i + r(u^n_{i+1}-2u^n_i+u^n_{i-1}), r=αΔt/Δx²',
            'stability':    'Explicit heat: r ≤ 1/2 (CFL condition)',
            'implicit':     'Always stable (Crank-Nicolson, backward Euler)',
            'wave':         'CFL: c·Δt/Δx ≤ 1 for stability'
        },
        'Finite Element Method (FEM)': {
            'idea':         'Variational formulation, piecewise polynomial basis',
            'weak_form':    'Multiply PDE by test function, integrate by parts',
            'stiffness':    'Assemble global stiffness matrix K and load vector f',
            'solve':        'Ku = f (linear system)',
            'advantage':    'Complex geometry, natural boundary conditions',
            'software':     'FEniCS, COMSOL, ANSYS, Abaqus'
        },
        'Finite Volume Method (FVM)': {
            'idea':         'Integrate PDE over control volumes (conservation form)',
            'advantage':    'Exactly conservative (important for fluids)',
            'software':     'OpenFOAM, SU2'
        },
        'Spectral methods': {
            'idea':         'Represent solution as global basis functions (Fourier, Chebyshev)',
            'advantage':    'Exponential convergence for smooth solutions',
            'use':          'Smooth periodic or simple geometry problems'
        }
    }
```

---

## Optimization
```python
def optimization_methods():
    return {
        'Unconstrained optimization': {
            'Gradient descent':     'x_{k+1} = x_k - α∇f(x_k)',
            'Newton\'s method':     'x_{k+1} = x_k - [∇²f(x_k)]⁻¹∇f(x_k)',
            'BFGS':                 'Quasi-Newton: approximate Hessian update',
            'L-BFGS':               'Limited memory BFGS (large scale)',
            'Conjugate gradient':   'For quadratic problems and extensions',
            'Line search':          'Choose α to satisfy Wolfe conditions'
        },
        'Constrained optimization': {
            'Lagrange multipliers': '∇f = λ∇g (equality constraints)',
            'KKT conditions':       'First-order necessary for inequality constraints',
            'Penalty methods':      'Add constraint violation to objective',
            'Interior point':       'Stay strictly feasible, log barrier',
            'Active set':           'Identify which constraints are active'
        },
        'Global optimization': {
            'Simulated annealing':  'Accept worse solutions with decreasing probability',
            'Genetic algorithms':   'Evolutionary: selection, crossover, mutation',
            'Particle swarm':       'Swarm intelligence',
            'Basin hopping':        'Random perturbation + local optimization'
        }
    }
```

---

## Software & Libraries
```python
def numerical_software():
    return {
        'Python': {
            'NumPy':        'Array operations, linear algebra',
            'SciPy':        'Root finding, integration, ODEs, optimization, linear algebra',
            'Matplotlib':   'Visualization',
            'SymPy':        'Symbolic mathematics'
        },
        'Key SciPy functions': {
            'scipy.optimize.brentq':    'Root finding (robust)',
            'scipy.optimize.fsolve':    'System of nonlinear equations',
            'scipy.integrate.quad':     'Adaptive quadrature',
            'scipy.integrate.solve_ivp':'ODE solver (RK45 default)',
            'scipy.linalg.solve':       'Linear system (uses LAPACK)',
            'scipy.linalg.lstsq':       'Least squares',
            'scipy.linalg.eig':         'Eigenvalues',
            'scipy.sparse.linalg.spsolve': 'Sparse linear system'
        },
        'MATLAB equivalents': {
            'ode45':        'Non-stiff ODE (Dormand-Prince RK45)',
            'ode15s':       'Stiff ODE (BDF/NDF)',
            'fzero':        'Root finding',
            'fminunc':      'Unconstrained optimization',
            'linprog':      'Linear programming',
            '\\':           'Linear system solve (backslash operator)'
        }
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Small h always better for differentiation | Round-off increases as h→0; use h≈√ε for first derivative |
| Newton always converges | Needs good initial guess near root; can diverge or cycle |
| Large n polynomial interpolation | Use splines or Chebyshev nodes to avoid Runge's phenomenon |
| Explicit method for stiff ODE | Use implicit method (BDF, Crank-Nicolson) |
| Normal equations for least squares | Use QR decomposition; normal equations square the condition number |
| Ignoring condition number | κ ≈ 10⁸ means losing ~8 digits of accuracy |

---

## Related Skills

- **calculus-expert**: Mathematical foundations
- **linear-algebra-expert**: Theory behind numerical LA
- **differential-equations-expert**: ODE/PDE theory
- **statistics-expert**: Numerical optimization in statistics
- **computational-chemistry-expert**: Scientific computing applications
- **machine-learning-expert**: Gradient descent and optimization
