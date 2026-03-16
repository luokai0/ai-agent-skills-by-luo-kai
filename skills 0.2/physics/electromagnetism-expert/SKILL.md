---
name: electromagnetism-expert
description: Expert-level electromagnetism knowledge. Use when working with electric fields, magnetic fields, Maxwell's equations, electromagnetic waves, circuits, Coulomb's law, Gauss's law, Faraday's law, Ampere's law, or electromagnetic induction. Also use when the user mentions 'electric field', 'magnetic field', 'Maxwell', 'Gauss law', 'Faraday', 'Ampere', 'capacitor', 'inductor', 'electromagnetic wave', 'Lorentz force', 'Poynting vector', or 'dielectric'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Electromagnetism Expert

You are a world-class physicist with deep expertise in electromagnetism covering electrostatics, magnetostatics, electromagnetic induction, Maxwell's equations, electromagnetic waves, and the mathematical framework of vector calculus applied to fields.

## Before Starting

1. **Topic** — Electrostatics, magnetostatics, induction, waves, or circuits?
2. **Level** — High school, undergraduate, or graduate?
3. **Math level** — Algebra, vector calculus, or tensor notation?
4. **Goal** — Solve problem, derive equation, or understand concept?
5. **Context** — Physics, electrical engineering, or optics?

---

## Core Expertise Areas

- **Electrostatics**: Coulomb's law, electric field, Gauss's law, potential
- **Conductors & Dielectrics**: capacitance, polarization, boundary conditions
- **Magnetostatics**: Biot-Savart, Ampere's law, magnetic force
- **Electromagnetic Induction**: Faraday's law, Lenz's law, inductance
- **Maxwell's Equations**: full set, wave equation derivation
- **Electromagnetic Waves**: propagation, polarization, energy, radiation
- **Special Topics**: multipole expansion, vector potential, gauge theory

---

## Electrostatics

### Coulomb's Law & Electric Field
```
Coulomb's Law:
  F = kq₁q₂/r²  r̂   (k = 1/4πε₀ = 8.99×10⁹ N·m²/C²)
  ε₀ = 8.85×10⁻¹² C²/N·m² (permittivity of free space)

Electric Field:
  E = F/q = kq/r² r̂  (due to point charge q)
  F = qE            (force on charge q in field E)
  Superposition: E_total = ΣEᵢ (vector sum)

Electric field lines:
  Start on + charges, end on - charges
  Denser lines = stronger field
  Never cross
```

### Gauss's Law
```
Integral form:
  ∮E·dA = Q_enc/ε₀

Differential form:
  ∇·E = ρ/ε₀   (ρ = charge density)

Applications (use symmetry):
  Sphere of charge Q, r > R:  E = kQ/r²  (same as point charge)
  Infinite line charge λ:      E = λ/2πε₀r
  Infinite plane charge σ:     E = σ/2ε₀
  Inside conductor:            E = 0
```

### Electric Potential
```
Potential:      V = kq/r  (point charge)
                E = -∇V
                V = -∫E·dl

Potential energy: U = qV = kq₁q₂/r

Equipotential surfaces: perpendicular to E field lines

Poisson's equation:   ∇²V = -ρ/ε₀
Laplace's equation:   ∇²V = 0  (charge-free region)

Capacitance:
  C = Q/V
  Parallel plate: C = ε₀A/d
  Spherical:      C = 4πε₀R
  Energy stored:  U = ½CV² = Q²/2C = ½QV
```

---

## Magnetostatics

### Magnetic Force & Field
```
Lorentz Force:
  F = q(E + v×B)
  Magnetic force: F = qv×B
  On current:     F = IL×B

Biot-Savart Law:
  dB = (μ₀/4π) · I·dl×r̂/r²
  B due to long wire: B = μ₀I/2πr  (circular field lines)
  B at center of loop: B = μ₀I/2R

μ₀ = 4π×10⁻⁷ T·m/A (permeability of free space)

Magnetic dipole moment:
  m = IA n̂  (current loop)
  Torque: τ = m×B
  Energy: U = -m·B
```

### Ampere's Law
```
Integral form:
  ∮B·dl = μ₀I_enc  (magnetostatics)
  ∮B·dl = μ₀(I_enc + ε₀dΦE/dt)  (with displacement current)

Differential form:
  ∇×B = μ₀J  (static)
  ∇×B = μ₀J + μ₀ε₀∂E/∂t  (general)

Applications:
  Infinite solenoid: B = μ₀nI  (n = turns/length, inside)
  Toroid:           B = μ₀NI/2πr
  Outside solenoid: B = 0
```

---

## Electromagnetic Induction
```
Faraday's Law:
  EMF = -dΦB/dt
  ΦB = ∫B·dA  (magnetic flux)
  ∮E·dl = -dΦB/dt

Differential form:
  ∇×E = -∂B/∂t

Lenz's Law:
  Induced current opposes change in flux
  (negative sign in Faraday's law)

Motional EMF:
  EMF = BLv  (rod of length L moving at v in field B)

Self-Inductance:
  L = NΦB/I  (Henry)
  EMF = -L·dI/dt
  Energy: U = ½LI²

Solenoid inductance: L = μ₀N²A/ℓ

Mutual Inductance:
  EMF₂ = -M·dI₁/dt
  M = μ₀N₁N₂A/ℓ  (for coaxial solenoids)
```

---

## Maxwell's Equations
```
Complete set (SI units):

1. Gauss's Law (Electric):
   ∇·E = ρ/ε₀
   ∮E·dA = Q_enc/ε₀

2. Gauss's Law (Magnetic):
   ∇·B = 0   (no magnetic monopoles)
   ∮B·dA = 0

3. Faraday's Law:
   ∇×E = -∂B/∂t
   ∮E·dl = -dΦB/dt

4. Ampere-Maxwell Law:
   ∇×B = μ₀J + μ₀ε₀∂E/∂t
   ∮B·dl = μ₀(I_enc + ε₀dΦE/dt)

In vacuum (ρ=0, J=0):
   ∇·E = 0       ∇·B = 0
   ∇×E = -∂B/∂t  ∇×B = μ₀ε₀∂E/∂t
```

### Wave Equation Derivation
```
Take curl of Faraday: ∇×(∇×E) = -∂(∇×B)/∂t
Use vector identity:  ∇(∇·E) - ∇²E = -μ₀ε₀∂²E/∂t²
With ∇·E = 0:        ∇²E = μ₀ε₀∂²E/∂t²

Wave equation:  ∇²E = (1/c²)∂²E/∂t²
Speed of light: c = 1/√(μ₀ε₀) = 3×10⁸ m/s  ✓
```

---

## Electromagnetic Waves
```
Plane wave solution:
  E = E₀cos(k·r - ωt)  n̂
  B = B₀cos(k·r - ωt)  (k̂×n̂)
  B₀ = E₀/c

Relations:
  ω = ck   (dispersion relation in vacuum)
  k = 2π/λ  (wave vector)
  c = λf

Polarization:
  Linear:   E oscillates in fixed plane
  Circular: E rotates — E₀x = E₀y, phase diff = π/2
  Elliptical: general case

Energy & Intensity:
  Energy density: u = ε₀E² = B²/μ₀ = ε₀E²
  Poynting vector: S = (1/μ₀)E×B  (energy flux W/m²)
  Intensity: I = <S> = E₀²/2μ₀c = cε₀E₀²/2
  Radiation pressure: P = I/c (absorbed), P = 2I/c (reflected)

Electromagnetic spectrum:
  Radio:      λ > 1mm
  Microwave:  1mm - 1m
  Infrared:   700nm - 1mm
  Visible:    400-700nm
  UV:         10-400nm
  X-ray:      0.01-10nm
  Gamma:      λ < 0.01nm
```

---

## Matter in Fields
```
Dielectrics:
  D = ε₀E + P = εE = ε₀εᵣE
  P = ε₀χeE  (polarization)
  εᵣ = 1 + χe  (relative permittivity)
  Capacitance with dielectric: C = εᵣC₀

Magnetic materials:
  H = B/μ₀ - M = B/μ
  M = χmH  (magnetization)
  μᵣ = 1 + χm
  Diamagnetic: χm < 0 (weak, repelled)
  Paramagnetic: χm > 0 (weak, attracted)
  Ferromagnetic: χm >> 1 (strong, permanent magnets)

Boundary conditions:
  Normal D: D₁ₙ - D₂ₙ = σf
  Normal B: B₁ₙ = B₂ₙ
  Tangential E: E₁t = E₂t
  Tangential H: H₁t - H₂t = Kf
```

---

## Vector Calculus Tools
```
Gradient:    ∇f = (∂f/∂x, ∂f/∂y, ∂f/∂z)
Divergence:  ∇·F = ∂Fx/∂x + ∂Fy/∂y + ∂Fz/∂z
Curl:        ∇×F = (∂Fz/∂y-∂Fy/∂z, ∂Fx/∂z-∂Fz/∂x, ∂Fy/∂x-∂Fx/∂y)
Laplacian:   ∇²f = ∂²f/∂x² + ∂²f/∂y² + ∂²f/∂z²

Theorems:
  Divergence:  ∫∇·F dV = ∮F·dA  (volume→surface)
  Stokes:      ∫(∇×F)·dA = ∮F·dl (surface→line)

Identities:
  ∇×(∇f) = 0    (curl of gradient = 0)
  ∇·(∇×F) = 0   (div of curl = 0)
  ∇×(∇×F) = ∇(∇·F) - ∇²F
```

---

## Key Constants
```
ε₀ = 8.854×10⁻¹² C²/N·m²
μ₀ = 4π×10⁻⁷ T·m/A
c  = 2.998×10⁸ m/s
k  = 1/4πε₀ = 8.99×10⁹ N·m²/C²
e  = 1.602×10⁻¹⁹ C
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Wrong direction of B from wire | Use right-hand rule consistently |
| Forgetting displacement current | Include ε₀∂E/∂t in Ampere's law |
| Confusing E and V | E = -∇V, they have different units |
| Sign error in Faraday's law | Lenz's law: induced EMF opposes change |
| Forgetting ∇·B = 0 | No magnetic monopoles — B field lines always close |
| Units confusion | Check SI units carefully in every equation |

---

## Related Skills

- **classical-mechanics-expert**: Force and energy foundations
- **quantum-mechanics-expert**: QED builds on EM
- **optics-expert**: EM waves in optical regime
- **circuit-analysis-expert**: Applied EM in circuits
- **special-relativity-expert**: EM is inherently relativistic
