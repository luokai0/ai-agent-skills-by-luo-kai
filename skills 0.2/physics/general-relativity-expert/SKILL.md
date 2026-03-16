---
name: general-relativity-expert
description: Expert-level general relativity knowledge. Use when working with curved spacetime, Einstein field equations, geodesics, black holes, gravitational waves, cosmology, Schwarzschild metric, or tensor calculus. Also use when the user mentions 'Einstein field equations', 'curved spacetime', 'geodesic', 'black hole', 'event horizon', 'Schwarzschild', 'gravitational waves', 'spacetime curvature', 'Riemann tensor', 'metric tensor', 'cosmological constant', or 'gravitational lensing'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# General Relativity Expert

You are a world-class physicist with deep expertise in general relativity covering differential geometry, Einstein field equations, exact solutions, black holes, gravitational waves, cosmology, and the mathematical framework of tensor calculus on curved manifolds.

## Before Starting

1. **Topic** — Einstein equations, black holes, gravitational waves, cosmology, or geodesics?
2. **Level** — Conceptual, undergraduate, or graduate?
3. **Math level** — Conceptual, vector calculus, or full tensor notation?
4. **Goal** — Understand concept, solve problem, or derive result?
5. **Context** — Astrophysics, cosmology, or mathematical physics?

---

## Core Expertise Areas

- **Differential Geometry**: manifolds, tensors, covariant derivative, curvature
- **Einstein Field Equations**: derivation, interpretation, energy-momentum tensor
- **Geodesics**: equation of motion in curved spacetime
- **Exact Solutions**: Schwarzschild, Kerr, FLRW, de Sitter
- **Black Holes**: event horizon, Penrose diagrams, thermodynamics
- **Gravitational Waves**: linearized gravity, generation, detection
- **Cosmology**: Friedmann equations, expansion, dark energy
- **Experimental Tests**: perihelion precession, light bending, GPS

---

## Foundations & Philosophy
```
Key idea: Gravity is not a force — it is the curvature of spacetime.
          Massive objects curve spacetime.
          Objects follow geodesics (straightest paths) in curved spacetime.

Equivalence Principle:
  Weak EP:   Gravitational mass = Inertial mass
  Einstein EP: In a freely falling frame, physics is locally SR.
  Strong EP:  Laws of physics same in all frames (including gravity).

Mach's Principle:
  Inertia of objects determined by distribution of all matter.
  Motivated Einstein but not fully incorporated in GR.

Geometric units:
  G = c = 1 (often used in GR literature)
  Length = time = mass in these units.
```

---

## Tensor Calculus
```
Metric tensor gᵘᵛ:
  ds² = gᵘᵛ dxᵘ dxᵛ
  gᵘᵛ raises indices: Vᵘ = gᵘᵛ Vᵥ
  gᵘᵥ lowers indices: Vᵘ = gᵘᵛ Vᵥ
  gᵘᵛ gᵥᵨ = δᵘᵨ

Christoffel symbols (connection):
  Γᵨᵘᵛ = ½gᵨλ(∂ᵘgᵛλ + ∂ᵛgᵘλ - ∂λgᵘᵛ)
  Not a tensor — coordinate dependent.

Covariant derivative:
  ∇ᵘVᵛ = ∂ᵘVᵛ + ΓᵛᵘλVλ
  ∇ᵘVᵥ = ∂ᵘVᵥ - ΓλᵘᵥVλ
  ∇ᵘgᵥᵨ = 0 (metric compatibility)

Riemann curvature tensor:
  Rᵨᵘᵛλ = ∂ᵛΓᵨᵘλ - ∂λΓᵨᵘᵛ + ΓᵨᵛσΓσᵘλ - ΓᵨλσΓσᵘᵛ
  Measures failure of parallel transport around loop.
  Flat spacetime: Rᵨᵘᵛλ = 0

Ricci tensor:   Rᵘᵛ = Rλᵘλᵛ  (contraction)
Ricci scalar:   R = gᵘᵛRᵘᵛ
Einstein tensor: Gᵘᵛ = Rᵘᵛ - ½gᵘᵛR
∇ᵘGᵘᵛ = 0  (Bianchi identity — energy conservation)
```

---

## Einstein Field Equations
```
Einstein Field Equations (EFE):
  Gᵘᵛ = 8πG/c⁴ · Tᵘᵛ
  or with cosmological constant:
  Gᵘᵛ + Λgᵘᵛ = 8πG/c⁴ · Tᵘᵛ

Left side:  geometry (curvature of spacetime)
Right side: matter and energy content

Energy-momentum tensor Tᵘᵛ:
  T⁰⁰ = energy density
  T⁰ⁱ = energy flux / momentum density
  Tⁱʲ = stress tensor
  ∇ᵘTᵘᵛ = 0 (conservation of energy-momentum)

Perfect fluid:
  Tᵘᵛ = (ρ + P/c²)UᵘUᵛ + Pgᵘᵛ
  ρ = energy density, P = pressure, Uᵘ = four-velocity

Vacuum equations (Tᵘᵛ = 0):
  Rᵘᵛ = 0  (not flat spacetime — just Ricci flat)
  Gravitational waves, Schwarzschild are vacuum solutions.

Wheeler's summary:
  "Spacetime tells matter how to move;
   matter tells spacetime how to curve."
```

---

## Geodesic Equation
```
Geodesic: path of free-falling particle (no forces except gravity).
          Generalizes straight line to curved spacetime.

Equation:
  d²xᵘ/dτ² + Γᵘᵥλ (dxᵛ/dτ)(dxλ/dτ) = 0

Timelike geodesics: massive particles (dτ² > 0)
Null geodesics:     light rays (dτ = 0, ds² = 0)

Geodesic deviation:
  D²ξᵘ/dτ² = -Rᵘᵥλσ (dxᵛ/dτ) ξλ (dxσ/dτ)
  Describes tidal forces — nearby geodesics diverge/converge.
```

---

## Schwarzschild Solution
```
Vacuum solution outside spherical mass M:
  ds² = -(1-rs/r)c²dt² + dr²/(1-rs/r) + r²dΩ²
  dΩ² = dθ² + sin²θ dφ²

Schwarzschild radius: rs = 2GM/c²
  Sun:   rs = 2.95 km
  Earth: rs = 8.87 mm
  Proton: rs = 2.5×10⁻⁵⁴ m

Singularities:
  r = rs: coordinate singularity (event horizon)
           can be removed by coordinate change
  r = 0:  physical singularity (infinite curvature)

Gravitational redshift:
  f_obs/f_emit = √(1 - rs/r_emit) / √(1 - rs/r_obs)
  Clock near massive object ticks slower.
  GPS correction: ~45 μs/day faster (GR) - 7 μs/day slower (SR)
  Net: +38 μs/day must be corrected.

Orbital mechanics:
  Effective potential: Veff = -GM/r + L²/2μr² - GML²/μc²r³
  Extra term: purely GR — causes perihelion precession.
  Mercury precession: 43 arcsec/century (GR prediction ✓)
```

---

## Black Holes
```
Schwarzschild Black Hole:
  Event horizon at r = rs = 2GM/c²
  Nothing (including light) escapes from r < rs.
  Infinite time dilation at horizon for outside observer.
  Infalling observer crosses horizon in finite proper time.

Kerr Black Hole (rotating):
  Described by mass M and spin parameter a = J/Mc.
  Ergosphere: region outside horizon where frame dragging
              forces everything to rotate.
  Penrose process: extract rotational energy from ergosphere.

Reissner-Nordstrom (charged):
  Has inner and outer horizons.

Black hole thermodynamics:
  Temperature: TH = ℏc³/8πGMk  (Hawking temperature)
  Entropy:     S = kA/4lP²     (Bekenstein-Hawking)
               A = 4πrs², lP = √(Gℏ/c³) = Planck length
  First law:   dM = TH dS + ΩH dJ + ΦH dQ
  Second law:  Total black hole area never decreases (classically).

Hawking radiation:
  Black holes emit thermal radiation due to QFT in curved spacetime.
  Black hole evaporates over time: tevap ∝ M³
  Information paradox: unresolved fundamental problem.

Penrose diagrams:
  Conformal diagram showing causal structure.
  45° lines = light rays.
  Compresses infinite spacetime into finite diagram.
```

---

## Gravitational Waves
```
Linearized gravity: gᵘᵛ = ηᵘᵛ + hᵘᵛ  (|hᵘᵛ| << 1)

Wave equation (Lorenz gauge):
  □h̄ᵘᵛ = -16πG/c⁴ Tᵘᵛ
  h̄ᵘᵛ = hᵘᵛ - ½ηᵘᵛh  (trace-reversed)

Transverse-traceless (TT) gauge:
  Two polarizations: h₊ and h×
  h₊: stretches x, squeezes y (and vice versa)
  h×: 45° rotation of h₊

Quadrupole formula (leading order emission):
  Pᵍʷ = G/5c⁵ · ⟨Q̈ᵢⱼQ̈ᵢⱼ⟩  (power radiated)
  Qᵢⱼ = ∫ρ(xᵢxⱼ - ⅓δᵢⱼr²) dV  (quadrupole moment)

Detection:
  LIGO/Virgo: laser interferometers, arm length L ~ 4 km
  Strain: h = ΔL/L ~ 10⁻²¹ (GW150914 first detection 2015)
  Sources: binary black holes, neutron star mergers, supernovae

GW150914 (first detection):
  Two black holes: 36 M☉ and 29 M☉
  Merged to 62 M☉ — 3 M☉ radiated as gravitational waves!
  Peak luminosity: ~3.6×10⁴⁹ W (outshone all visible universe)
```

---

## Cosmology (FLRW)
```
Friedmann-Lemaitre-Robertson-Walker metric:
  ds² = -c²dt² + a(t)²[dr²/(1-kr²) + r²dΩ²]
  a(t) = scale factor, k = curvature (0,±1)

Friedmann equations:
  H² = (ȧ/a)² = 8πGρ/3 - kc²/a² + Λc²/3
  ä/a = -4πG/3(ρ + 3P/c²) + Λc²/3

Hubble parameter: H = ȧ/a = H₀ ≈ 67-74 km/s/Mpc

Density parameters:
  Ωm = 8πGρm/3H²  (matter)
  ΩΛ = Λc²/3H²    (dark energy)
  Ωk = -kc²/a²H²  (curvature)
  Ωm + ΩΛ + Ωk = 1

Current values:
  Ωm ≈ 0.31  (ordinary + dark matter)
  ΩΛ ≈ 0.69  (dark energy)
  Ωk ≈ 0     (spatially flat)

Cosmological redshift:
  1 + z = a(t_obs)/a(t_emit) = 1/a(t_emit)

Big Bang, inflation, dark energy expansion.
Age of universe: ~13.8 billion years.
```

---

## Experimental Tests of GR
```
Classical tests (Einstein's three):
1. Perihelion precession of Mercury:
   43 arcsec/century — predicted and confirmed ✓

2. Gravitational light bending:
   δθ = 4GM/c²b  (twice Newtonian prediction!)
   Confirmed by Eddington 1919 solar eclipse ✓

3. Gravitational redshift:
   Δf/f = gh/c²
   Confirmed by Pound-Rebka 1959 ✓

Modern tests:
4. Shapiro delay: light takes longer near massive objects
5. Frame dragging (Gravity Probe B 2011 ✓)
6. Gravitational waves (LIGO 2015 ✓)
7. Black hole image (EHT, M87* 2019, SgrA* 2022 ✓)
8. GPS corrections (daily practical application ✓)
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Gravity as a force | GR: gravity is spacetime curvature, no force |
| Schwarzschild radius = size of object | rs is event horizon only if all mass inside rs |
| Nothing special at event horizon locally | Infalling observer feels nothing special crossing horizon |
| Singularity theorem means GR breaks down | Singularities signal GR needs quantum gravity |
| Expansion means galaxies moving through space | Space itself expands — galaxies mostly at rest locally |
| Dark energy is energy in vacuum | Its nature is unknown — cosmological constant is one model |

---

## Related Skills

- **special-relativity-expert**: Foundation of GR
- **classical-mechanics-expert**: Newtonian limit
- **astrophysics-expert**: GR in stellar physics
- **cosmology-expert**: Large scale structure and expansion
- **black-holes-expert**: Detailed black hole physics
- **gravitational-waves-expert**: Detection and sources
