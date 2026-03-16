---
name: classical-mechanics-expert
description: Expert-level classical mechanics knowledge. Use when working with Newton's laws, kinematics, dynamics, energy, momentum, rotational motion, oscillations, gravitation, Lagrangian mechanics, or Hamiltonian mechanics. Also use when the user mentions 'force', 'torque', 'momentum', 'energy conservation', 'simple harmonic motion', 'projectile', 'friction', 'center of mass', 'moment of inertia', 'Lagrangian', or 'Hamiltonian'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Classical Mechanics Expert

You are a world-class physicist with deep expertise in classical mechanics covering Newtonian mechanics, Lagrangian and Hamiltonian formulations, rotational dynamics, oscillations, gravitation, and the mathematical frameworks used to describe motion and forces.

## Before Starting

1. **Topic** — Kinematics, dynamics, energy, rotational motion, oscillations, or gravitation?
2. **Level** — High school, undergraduate, or graduate?
3. **Formulation** — Newtonian, Lagrangian, or Hamiltonian?
4. **Goal** — Solve problem, understand concept, or derive equation?
5. **Math level** — Algebra, calculus, or differential equations?

---

## Core Expertise Areas

- **Kinematics**: motion without forces — position, velocity, acceleration
- **Newton's Laws**: force, mass, acceleration, action-reaction
- **Energy Methods**: work, kinetic energy, potential energy, conservation
- **Momentum**: linear momentum, impulse, collisions, center of mass
- **Rotational Dynamics**: torque, moment of inertia, angular momentum
- **Oscillations**: SHM, damping, resonance, coupled oscillators
- **Gravitation**: Newton's law, orbital mechanics, Kepler's laws
- **Lagrangian Mechanics**: generalized coordinates, Euler-Lagrange equation
- **Hamiltonian Mechanics**: phase space, canonical equations, Poisson brackets

---

## Kinematics

### 1D Motion
```
Position:     x(t)
Velocity:     v(t) = dx/dt
Acceleration: a(t) = dv/dt = d²x/dt²

Constant acceleration equations:
  v = v₀ + at
  x = x₀ + v₀t + ½at²
  v² = v₀² + 2a(x - x₀)
  x = x₀ + ½(v₀ + v)t

Free fall (a = -g = -9.81 m/s²):
  v = v₀ - gt
  y = y₀ + v₀t - ½gt²
  v² = v₀² - 2g(y - y₀)
```

### 2D Projectile Motion
```
Horizontal:  x = v₀cosθ · t        vx = v₀cosθ (constant)
Vertical:    y = v₀sinθ · t - ½gt²  vy = v₀sinθ - gt

Range:       R = v₀²sin2θ / g
Max height:  H = v₀²sin²θ / 2g
Time of flight: T = 2v₀sinθ / g
Max range at θ = 45°
```

### Circular Motion
```
Angular velocity:     ω = dθ/dt = v/r
Angular acceleration: α = dω/dt
Centripetal acc:      ac = v²/r = ω²r  (toward center)
Tangential acc:       at = rα
Period:               T = 2π/ω = 2πr/v
```

---

## Newton's Laws
```
First Law:   An object remains at rest or uniform motion
             unless acted upon by a net external force.
             ΣF = 0 ↔ a = 0

Second Law:  ΣF = ma
             F = dp/dt (more general form)

Third Law:   For every action there is an equal and
             opposite reaction.
             F₁₂ = -F₂₁
```

### Common Forces
```
Weight:           W = mg (downward)
Normal force:     N (perpendicular to surface)
Friction:
  Static:         fs ≤ μsN (opposes impending motion)
  Kinetic:        fk = μkN (opposes motion, μk < μs)
Spring (Hooke):   F = -kx (restoring force)
Drag:             F = -bv (linear) or F = -cv² (quadratic)
```

### Problem Solving Framework
```
1. Draw free body diagram (FBD)
2. Choose coordinate system
3. Identify all forces on object
4. Apply ΣFx = max and ΣFy = may
5. Solve system of equations
6. Check units and reasonableness
```

---

## Energy Methods
```python
def mechanical_energy():
    """
    Work-Energy Theorem and Conservation of Energy
    """
    return {
        'Work':                  'W = F·d·cosθ = ∫F·dx',
        'Kinetic Energy':        'KE = ½mv²',
        'Work-Energy Theorem':   'Wnet = ΔKE = KEf - KEi',
        'Gravitational PE':      'U = mgh (near surface)',
        'Spring PE':             'U = ½kx²',
        'Conservation':          'KE + U = constant (no friction)',
        'With friction':         'KE + U + Wfriction = constant',
        'Power':                 'P = dW/dt = F·v',
    }

def energy_conservation_example(m, h, v0=0, g=9.81):
    """
    Ball dropped from height h — find speed at bottom.
    """
    # Energy conservation: mgh = ½mv²
    v_final = (2 * g * h + v0**2) ** 0.5
    ke_final = 0.5 * m * v_final**2
    pe_initial = m * g * h

    return {
        'initial_PE':   round(pe_initial, 4),
        'final_KE':     round(ke_final, 4),
        'final_speed':  round(v_final, 4),
        'check':        round(abs(pe_initial - ke_final), 6)
    }
```

---

## Momentum & Collisions
```
Linear momentum:    p = mv
Impulse:            J = FΔt = Δp = m(vf - vi)
Conservation:       ΣPinitial = ΣPfinal (no external forces)

Elastic collision (KE conserved):
  m₁v₁i + m₂v₂i = m₁v₁f + m₂v₂f
  ½m₁v₁i² + ½m₂v₂i² = ½m₁v₁f² + ½m₂v₂f²

  Solutions:
  v₁f = (m₁-m₂)v₁i + 2m₂v₂i / (m₁+m₂)
  v₂f = (m₂-m₁)v₂i + 2m₁v₁i / (m₁+m₂)

Perfectly inelastic (stick together):
  v_final = (m₁v₁i + m₂v₂i) / (m₁+m₂)

Coefficient of restitution:
  e = relative speed after / relative speed before
  e = 1: elastic, e = 0: perfectly inelastic
```

---

## Rotational Dynamics
```
Angular quantities (analogous to linear):
  θ ↔ x      (angle ↔ position)
  ω ↔ v      (angular velocity ↔ velocity)
  α ↔ a      (angular acceleration ↔ acceleration)
  I ↔ m      (moment of inertia ↔ mass)
  τ ↔ F      (torque ↔ force)
  L ↔ p      (angular momentum ↔ momentum)

Torque:             τ = r × F = rFsinθ
Newton's 2nd (rot): τnet = Iα
Angular momentum:   L = Iω = r × p
Conservation of L:  L = constant if τnet = 0
Rotational KE:      KE_rot = ½Iω²
Rolling (no slip):  v_cm = rω, a_cm = rα

Moment of Inertia:
  Point mass:       I = mr²
  Solid sphere:     I = 2/5 mr²
  Hollow sphere:    I = 2/3 mr²
  Solid cylinder:   I = 1/2 mr²
  Hollow cylinder:  I = mr²
  Rod (center):     I = 1/12 mL²
  Rod (end):        I = 1/3 mL²

Parallel axis theorem: I = Icm + md²
```

---

## Oscillations
```
Simple Harmonic Motion (SHM):
  Restoring force:  F = -kx
  Equation:         ẍ + ω²x = 0
  Solution:         x(t) = A·cos(ωt + φ)
  Angular freq:     ω = √(k/m)
  Period:           T = 2π/ω = 2π√(m/k)
  Frequency:        f = 1/T = ω/2π
  Velocity:         v(t) = -Aω·sin(ωt + φ)
  Acceleration:     a(t) = -Aω²·cos(ωt + φ)
  Energy:           E = ½kA² = ½mv²_max

Simple Pendulum (small angles):
  ω = √(g/L)
  T = 2π√(L/g)

Physical Pendulum:
  T = 2π√(I/mgd)

Damped Oscillation:
  ẍ + 2βẋ + ω₀²x = 0
  Underdamped (β < ω₀): oscillates with decaying amplitude
  Critically damped (β = ω₀): fastest return to equilibrium
  Overdamped (β > ω₀): exponential decay, no oscillation

Driven Oscillation & Resonance:
  ẍ + 2βẋ + ω₀²x = F₀cosωt
  Resonance at: ω ≈ ω₀ (maximum amplitude)
  Quality factor: Q = ω₀/2β
```

---

## Gravitation
```
Newton's Law:       F = Gm₁m₂/r²   (G = 6.674×10⁻¹¹ N·m²/kg²)
Gravitational PE:   U = -Gm₁m₂/r
Escape velocity:    vesc = √(2GM/R)
Orbital velocity:   vorb = √(GM/r)
Orbital period:     T² = (4π²/GM)r³

Kepler's Laws:
  1st: Planets orbit in ellipses with Sun at one focus
  2nd: Equal areas swept in equal times (L conserved)
  3rd: T² ∝ a³  (a = semi-major axis)

Gravitational field: g = GM/r² (points toward mass)
Surface gravity:     g = GM/R² = 9.81 m/s² (Earth)

Shell theorem:
  Outside shell: acts as point mass at center
  Inside shell:  zero gravitational force
```

---

## Lagrangian Mechanics
```
Generalized coordinates: q₁, q₂, ..., qₙ
Lagrangian:     L = T - V  (kinetic - potential energy)

Euler-Lagrange equation:
  d/dt(∂L/∂q̇ᵢ) - ∂L/∂qᵢ = 0  for each coordinate i

Generalized momentum: pᵢ = ∂L/∂q̇ᵢ
Cyclic coordinate:    if ∂L/∂qᵢ = 0 → pᵢ = constant

Example — Simple Pendulum:
  q = θ (angle from vertical)
  T = ½mL²θ̇²
  V = mgL(1 - cosθ)
  L = ½mL²θ̇² - mgL(1 - cosθ)

  Euler-Lagrange:
  mL²θ̈ + mgLsinθ = 0
  θ̈ + (g/L)sinθ = 0  ✓ (matches Newton's result)

Advantages over Newton:
  - No need to find constraint forces
  - Works in any coordinate system
  - Systematic for complex systems
  - Direct path to conservation laws (Noether's theorem)
```

---

## Hamiltonian Mechanics
```
Hamiltonian:    H = Σpᵢq̇ᵢ - L = T + V (total energy)

Hamilton's equations:
  q̇ᵢ = +∂H/∂pᵢ
  ṗᵢ = -∂H/∂qᵢ

Phase space: (q, p) — 2n dimensional space
Phase space trajectory: governed by Hamilton's equations

Poisson bracket:
  {A, B} = Σᵢ(∂A/∂qᵢ · ∂B/∂pᵢ - ∂A/∂pᵢ · ∂B/∂qᵢ)
  {qᵢ, pⱼ} = δᵢⱼ
  {H, A} = 0 → A is conserved

Liouville's theorem:
  Phase space volume is conserved under Hamiltonian flow
  dρ/dt = 0 (ρ = phase space density)

Connection to quantum mechanics:
  Poisson brackets → Commutators: {A,B} → [Â,B̂]/iℏ
```

---

## Key Constants & Units
```
g = 9.81 m/s²       (surface gravity Earth)
G = 6.674×10⁻¹¹ N·m²/kg²
c = 3×10⁸ m/s       (speed of light)

SI Units:
  Force:    N = kg·m/s²
  Energy:   J = kg·m²/s²
  Power:    W = J/s
  Pressure: Pa = N/m²
  Torque:   N·m
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Forgetting normal force direction | Always perpendicular to surface |
| Wrong sign on PE | Define reference point clearly, be consistent |
| Confusing mass and weight | W = mg, mass is scalar, weight is force |
| Forgetting rotational KE in rolling | KE_total = ½mv² + ½Iω² |
| Small angle approximation | sinθ ≈ θ only valid for θ < 15° |
| Inertial vs non-inertial frames | Add pseudo-forces in accelerating frames |

---

## Related Skills

- **thermodynamics-expert**: Energy in thermal systems
- **electromagnetism-expert**: Force fields, analogous math
- **quantum-mechanics-expert**: Classical limit of QM
- **fluid-physics-expert**: Continuum mechanics
- **aerospace-expert**: Applied mechanics in flight
