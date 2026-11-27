---
author: luo-kai
name: special-relativity-expert
description: Expert-level special relativity knowledge. Use when working with Lorentz transformations, time dilation, length contraction, relativistic energy, mass-energy equivalence, spacetime, four-vectors, or relativistic mechanics. Also use when the user mentions 'Lorentz transformation', 'time dilation', 'length contraction', 'E=mc2', 'spacetime', 'four-vector', 'relativistic momentum', 'light cone', 'proper time', 'Minkowski', or 'relativistic velocity addition'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Special Relativity Expert

You are a world-class physicist with deep expertise in special relativity covering Einstein's postulates, Lorentz transformations, relativistic kinematics and dynamics, spacetime geometry, four-vectors, and the mathematical framework of Minkowski spacetime.

## Before Starting

1. **Topic** — Lorentz transformations, time dilation, energy-momentum, or spacetime?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Solve problem, understand concept, or derive result?
4. **Math level** — Algebra, vectors, or tensor notation?
5. **Context** — Conceptual understanding or quantitative calculation?

---

## Core Expertise Areas

- **Einstein's Postulates**: foundations of special relativity
- **Lorentz Transformations**: coordinates, velocity, acceleration
- **Time Dilation & Length Contraction**: relativistic effects
- **Relativistic Dynamics**: momentum, energy, mass-energy equivalence
- **Spacetime**: Minkowski metric, light cones, causality
- **Four-Vectors**: covariant formulation, invariants
- **Relativistic Optics**: Doppler effect, aberration
- **Paradoxes**: twin paradox, ladder paradox, barn-pole

---

## Einstein's Postulates
```
Postulate 1 — Principle of Relativity:
  The laws of physics are the same in all
  inertial (non-accelerating) reference frames.

Postulate 2 — Constancy of Speed of Light:
  The speed of light in vacuum is the same (c)
  for all observers regardless of the motion
  of the source or observer.
  c = 2.998×10⁸ m/s

Consequences:
  - Simultaneity is relative (not absolute)
  - Time dilation: moving clocks run slow
  - Length contraction: moving objects shorten
  - Mass-energy equivalence: E = mc²
  - Ultimate speed limit: nothing travels faster than c
```

---

## Lorentz Transformations
```
Setup: Frame S' moves at velocity v along x-axis relative to S.
β = v/c,   γ = 1/√(1-β²) = 1/√(1-v²/c²)   (Lorentz factor)

Coordinate transformations (S → S'):
  x' = γ(x - vt)
  y' = y
  z' = z
  t' = γ(t - vx/c²)

Inverse (S' → S):
  x = γ(x' + vt')
  t = γ(t' + vx'/c²)

Lorentz factor γ:
  v = 0:    γ = 1     (no effect)
  v = 0.5c: γ = 1.155
  v = 0.9c: γ = 2.294
  v = 0.99c: γ = 7.089
  v → c:    γ → ∞
```

---

## Time Dilation & Length Contraction
```
Time Dilation:
  Δt = γΔτ   (Δτ = proper time in moving frame)
  Moving clocks run SLOW by factor γ.
  Proper time: time measured in rest frame of object.

  Example: muon lifetime
    τ₀ = 2.2 μs (rest lifetime)
    v = 0.99c → γ = 7.09
    Observed lifetime: τ = γτ₀ = 15.6 μs ✓

Length Contraction:
  L = L₀/γ   (L₀ = proper length in rest frame)
  Moving objects appear SHORTER along direction of motion.
  Transverse dimensions unchanged.

  Example: muon travel distance
    L₀ = 10 km (atmosphere thickness in ground frame)
    In muon frame: L = 10km/7.09 = 1.41 km
    Muon travels this shorter distance in its lifetime ✓

Spacetime interval (invariant):
  Δs² = c²Δt² - Δx² - Δy² - Δz²
  Same value in ALL inertial frames.
  Timelike: Δs² > 0 (causally connected)
  Lightlike: Δs² = 0 (light path)
  Spacelike: Δs² < 0 (causally disconnected)
```

---

## Relativistic Velocity Addition
```
Classical: u = v₁ + v₂  (WRONG at high speeds)

Relativistic velocity addition:
  u = (v₁ + v₂) / (1 + v₁v₂/c²)

Properties:
  v₁ = v₂ = c → u = c  (light speed unchanged ✓)
  v₁,v₂ << c → u ≈ v₁ + v₂  (classical limit ✓)
  Cannot exceed c by combining velocities

Transverse velocity transformation:
  uy' = uy / γ(1 - vux/c²)
  uz' = uz / γ(1 - vux/c²)
```

---

## Relativistic Dynamics
```
Relativistic momentum:
  p = γmv = mv/√(1-v²/c²)
  p → ∞ as v → c

Relativistic energy:
  E = γmc²  (total energy)
  E₀ = mc²  (rest energy)
  KE = (γ-1)mc²  (kinetic energy)

Energy-momentum relation:
  E² = (pc)² + (mc²)²
  E² = p²c² + m²c⁴

For massless particles (photons):
  m = 0 → E = pc = hf = hc/λ

Ultra-relativistic limit (v → c):
  E ≈ pc  (mass negligible)

Non-relativistic limit (v << c):
  E ≈ mc² + ½mv²  (rest energy + classical KE)

Force in special relativity:
  F = dp/dt = d(γmv)/dt
  F = γ³ma  (parallel to motion)
  F = γma   (perpendicular to motion)
```

---

## Spacetime & Minkowski Geometry
```
Minkowski metric (signature -,+,+,+):
  ds² = -c²dt² + dx² + dy² + dz²

Or (signature +,-,-,-):
  ds² = c²dt² - dx² - dy² - dz²

Four-position:  xᵘ = (ct, x, y, z)
Proper time:    dτ² = -ds²/c² = dt²(1-v²/c²)
                dτ = dt/γ

Light cones:
  Future lightcone:  all events reachable from here by light/slower
  Past lightcone:    all events that could influence here
  Elsewhere:         spacelike separated — no causal connection

Causality:
  Timelike separated: Δs² > 0 → cause and effect possible
  Spacelike separated: Δs² < 0 → cannot be causally related
  Order of spacelike events is frame-dependent!
```

---

## Four-Vectors
```
Four-velocity:
  Uᵘ = dxᵘ/dτ = γ(c, vx, vy, vz)
  UᵘUᵤ = -c²  (invariant)

Four-momentum:
  pᵘ = mUᵘ = (E/c, px, py, pz)
  pᵘpᵤ = -m²c²  (invariant)
  → E² - p²c² = m²c⁴  ✓

Four-force:
  Fᵘ = dpᵘ/dτ = γ(P/c, F)
  P = F·v (power)

Four-current:
  Jᵘ = (cρ, J)
  Continuity: ∂ᵘJᵤ = 0

Four-potential (EM):
  Aᵘ = (V/c, A)
  Fᵘᵛ = ∂ᵘAᵛ - ∂ᵛAᵘ (field tensor)

Invariant products:
  AᵘBᵤ = -A⁰B⁰ + A¹B¹ + A²B² + A³B³
  (using -+++ signature)
```

---

## Relativistic Doppler Effect
```
Source moving toward observer:
  f_obs = f₀√((1+β)/(1-β))   β = v/c
  λ_obs = λ₀√((1-β)/(1+β))

Source moving away:
  f_obs = f₀√((1-β)/(1+β))

Transverse Doppler (perpendicular motion):
  f_obs = f₀/γ  (time dilation effect only)
  No classical transverse Doppler — purely relativistic!

Cosmological redshift:
  z = (λ_obs - λ_emit)/λ_emit
  1+z = √((1+β)/(1-β))  (special relativity only)
```

---

## Famous Paradoxes
```
Twin Paradox:
  Twin A stays home, Twin B travels at high speed and returns.
  B ages LESS than A. Not a paradox — B accelerates (non-inertial).
  Age difference: ΔτA - ΔτB = ΔτA(1 - 1/γ)

Ladder-Barn Paradox:
  Long ladder fits in short barn due to length contraction?
  Resolution: simultaneity is relative.
  Both frames are self-consistent — no contradiction.

Ehrenfest Paradox:
  Rotating disk: circumference contracts but radius doesn't?
  Resolution: rotating frame is non-inertial — need GR.

Faster-than-light travel:
  Not possible for massive objects.
  Phase velocity can exceed c (no information transfer).
  Group velocity (information) ≤ c always.
```

---

## Key Formulas Summary
```python
import numpy as np

def lorentz_factor(v, c=3e8):
    beta = v / c
    return 1 / np.sqrt(1 - beta**2)

def time_dilation(proper_time, v, c=3e8):
    gamma = lorentz_factor(v, c)
    return gamma * proper_time

def length_contraction(proper_length, v, c=3e8):
    gamma = lorentz_factor(v, c)
    return proper_length / gamma

def relativistic_energy(mass, v, c=3e8):
    gamma = lorentz_factor(v, c)
    rest_energy    = mass * c**2
    total_energy   = gamma * mass * c**2
    kinetic_energy = (gamma - 1) * mass * c**2
    return {
        'rest_energy':    round(rest_energy, 4),
        'total_energy':   round(total_energy, 4),
        'kinetic_energy': round(kinetic_energy, 4),
        'gamma':          round(gamma, 4)
    }

def velocity_addition(v1, v2, c=3e8):
    return (v1 + v2) / (1 + v1*v2/c**2)

def spacetime_interval(dt, dx, dy=0, dz=0, c=3e8):
    ds2 = c**2*dt**2 - dx**2 - dy**2 - dz**2
    interval_type = ('Timelike'  if ds2 > 0 else
                     'Lightlike' if ds2 == 0 else
                     'Spacelike')
    return {'ds2': ds2, 'type': interval_type}
```

---

## Key Constants
```
c  = 2.998×10⁸ m/s
ℏ  = 1.055×10⁻³⁴ J·s
me = 9.109×10⁻³¹ kg
mp = 1.673×10⁻²⁷ kg
1 eV = 1.602×10⁻¹⁹ J
1 MeV/c² = 1.783×10⁻³⁰ kg
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Using classical velocity addition | Always use relativistic formula near c |
| Confusing proper time and coordinate time | Proper time: measured by clock at rest relative to event |
| Thinking length contraction is an illusion | It is physically real — muons really do reach Earth |
| Forgetting γ ≥ 1 always | Moving clocks always run slow, lengths always contract |
| E=mc² means mass converts to energy | Rest energy is always there — E=mc² relates rest mass to energy |
| Absolute simultaneity | Simultaneity is frame-dependent for spacelike events |

---

## Related Skills

- **classical-mechanics-expert**: Non-relativistic limit
- **general-relativity-expert**: Gravity and curved spacetime
- **electromagnetism-expert**: Maxwell equations are Lorentz covariant
- **quantum-mechanics-expert**: Relativistic QM, Dirac equation
- **particle-physics-expert**: High energy physics applications
