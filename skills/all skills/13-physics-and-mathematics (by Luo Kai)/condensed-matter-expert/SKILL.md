---
author: luo-kai
name: condensed-matter-expert
description: Expert-level condensed matter physics knowledge. Use when working with crystal structure, band theory, semiconductors, superconductivity, magnetism, phase transitions, Fermi liquids, topological materials, or strongly correlated systems. Also use when the user mentions 'band gap', 'Fermi energy', 'semiconductor', 'superconductor', 'phonon', 'crystal lattice', 'Brillouin zone', 'Bloch theorem', 'Hall effect', 'magnetism', 'phase transition', or 'topological insulator'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Condensed Matter Physics Expert

You are a world-class physicist with deep expertise in condensed matter physics covering crystal structure, electronic band theory, semiconductors, superconductivity, magnetism, phase transitions, strongly correlated systems, and topological materials.

## Before Starting

1. **Topic** — Crystal structure, band theory, semiconductors, superconductivity, or magnetism?
2. **Level** — Undergraduate or graduate?
3. **Goal** — Understand concept, solve problem, or derive result?
4. **Material** — Metal, semiconductor, insulator, or superconductor?
5. **Context** — Physics, materials science, or device engineering?

---

## Core Expertise Areas

- **Crystal Structure**: lattices, symmetry, reciprocal space, diffraction
- **Electronic Structure**: free electron model, band theory, Bloch theorem
- **Semiconductors**: doping, p-n junction, devices
- **Lattice Dynamics**: phonons, heat capacity, thermal conductivity
- **Magnetism**: diamagnetism, paramagnetism, ferromagnetism, spin models
- **Superconductivity**: BCS theory, Meissner effect, type I/II
- **Phase Transitions**: Landau theory, critical phenomena, scaling
- **Topological Materials**: topological insulators, Chern numbers

---

## Crystal Structure
```
Bravais lattices:
  14 distinct lattice types in 3D (7 crystal systems)
  R = n₁a₁ + n₂a₂ + n₃a₃  (lattice vectors)

Common structures:
  Simple cubic (SC): 1 atom/cell
  BCC (body-centered cubic): 2 atoms/cell (Na, Fe, W)
  FCC (face-centered cubic): 4 atoms/cell (Cu, Al, Au, Ni)
  HCP (hexagonal close packed): 2 atoms/cell (Mg, Ti, Zn)
  Diamond cubic: 8 atoms/cell (Si, Ge, C)
  NaCl structure: FCC with 2-atom basis

Reciprocal lattice:
  G = m₁b₁ + m₂b₂ + m₃b₃
  bᵢ·aⱼ = 2πδᵢⱼ
  b₁ = 2π(a₂×a₃)/(a₁·a₂×a₃)

Brillouin zone:
  First BZ = Wigner-Seitz cell of reciprocal lattice
  All distinct k-vectors contained in first BZ

X-ray diffraction:
  Bragg's law: 2d·sinθ = nλ
  Structure factor: Sk = Σⱼ fⱼ exp(iG·rⱼ)
  Systematic absences → determine crystal structure

Miller indices (hkl):
  Planes with intercepts a/h, b/k, c/l
  Spacing: d = a/√(h²+k²+l²)  (cubic)
```

---

## Free Electron Model
```
Drude model (classical):
  σ = ne²τ/m  (electrical conductivity)
  τ = mean free time between collisions
  Hall coefficient: RH = -1/ne

Sommerfeld model (quantum):
  Electrons in box: ψk = (1/√V)exp(ik·r)
  Energy: εk = ℏ²k²/2m
  Fermi energy: EF = (ℏ²/2m)(3π²n)^(2/3)
  Fermi wavevector: kF = (3π²n)^(1/3)
  Fermi temperature: TF = EF/kB

Density of states:
  g(ε) = (3n/2EF)(ε/EF)^(1/2)  (3D)
  g(EF) = 3n/2EF

Fermi-Dirac distribution:
  f(ε) = 1/[exp((ε-μ)/kBT) + 1]
  At T=0: f = 1 for ε < EF, f = 0 for ε > EF
  Chemical potential μ ≈ EF at low T

Sommerfeld expansion:
  Electronic heat capacity: Cv = (π²/3)kB²T·g(EF) = γT
  γ = π²kB²g(EF)/3  (Sommerfeld coefficient)
  Much smaller than classical Cv = 3nkB/2 ✓
```

---

## Band Theory
```
Bloch theorem:
  ψnk(r) = unk(r)exp(ik·r)
  unk(r+R) = unk(r)  (periodic part)
  States labeled by band index n and k in BZ

Nearly free electron model:
  Weak periodic potential V(r) = ΣG VG exp(iG·r)
  Band gaps open at BZ boundaries
  Gap size ≈ 2|VG| at zone boundary k = G/2

Tight binding model:
  ψk = (1/√N) Σᵣ exp(ik·R) φ(r-R)
  εk = ε₀ - t Σ_NN exp(ik·δ)  (δ = nearest neighbor vectors)
  1D: εk = ε₀ - 2t·cos(ka)
  Bandwidth W = 4t (1D), larger in higher dimensions

Band classification:
  Metal: partially filled band OR overlapping bands
  Insulator: completely filled bands, large gap (Eg > 4eV)
  Semiconductor: completely filled bands, small gap (Eg < 4eV)
  Semimetal: tiny overlap of valence and conduction bands

Effective mass:
  1/m* = (1/ℏ²) d²ε/dk²
  Captures band curvature effect on dynamics
  Can be negative (holes at top of band)
  m* << m: light electrons (high mobility)
```

---

## Semiconductors
```
Intrinsic semiconductor:
  n = p = nᵢ = √(NcNv) exp(-Eg/2kBT)
  Nc = 2(2πmₑ*kBT/h²)^(3/2)  (effective DOS)
  Fermi level: μ = Eg/2 + (3/4)kBT·ln(mₕ*/mₑ*)

Doped semiconductors:
  n-type (donor atoms, e.g. P in Si): excess electrons
    n ≈ ND (donor concentration), p = nᵢ²/n
  p-type (acceptor atoms, e.g. B in Si): excess holes
    p ≈ NA, n = nᵢ²/p

Mass action law: np = nᵢ²

Carrier transport:
  Drift: J = (neμₑ + peμₕ)E  (σ = neμₑ + peμₕ)
  Diffusion: J = eDₑ∇n - eDₕ∇p
  Einstein relation: D/μ = kBT/e

p-n junction:
  Built-in potential: Vbi = (kBT/e)ln(NAND/nᵢ²)
  Depletion width: W = √(2ε₀εr·Vbi/e · (NA+ND)/(NAND))
  I-V: I = I₀[exp(eV/kBT) - 1]  (Shockley equation)

Semiconductor properties (Si at 300K):
  Eg = 1.12 eV, nᵢ = 1.5×10¹⁰ cm⁻³
  μₑ = 1400, μₕ = 450 cm²/Vs
  ε = 11.7
```

---

## Lattice Dynamics & Phonons
```
1D monatomic chain:
  ω(k) = 2√(K/m) |sin(ka/2)|
  Acoustic branch: ω → 0 as k → 0
  vg = dω/dk = a√(K/m)cos(ka/2)

1D diatomic chain:
  Two atoms per unit cell → two branches
  Acoustic: both atoms move same direction
  Optical: atoms move in opposite directions
  Gap at zone boundary: ω = √(2K/M±m)

Phonon dispersion in 3D:
  N atoms/cell → 3N branches
  3 acoustic + 3(N-1) optical branches

Debye model:
  Linear dispersion: ωD = vsqD (Debye cutoff)
  Cv = 9NkB(T/θD)³∫₀^(θD/T) x⁴eˣ/(eˣ-1)² dx
  High T: Cv → 3NkB (Dulong-Petit)
  Low T: Cv ∝ T³ (Debye T³ law)
  θD = Debye temperature (characteristic)

Einstein model:
  All phonons same frequency ωE
  Cv = 3NkB(θE/T)² eθE/T/(eθE/T-1)²
  Works well for optical modes

Thermal conductivity:
  κ = (1/3)Cv·v·ℓ  (kinetic theory)
  ℓ = phonon mean free path
  Umklapp scattering limits κ at high T
```

---

## Magnetism
```
Diamagnetism:
  χ < 0 (small, negative susceptibility)
  Induced moment opposes applied field
  Present in all materials (Lenz's law)
  Superconductors: perfect diamagnets χ = -1

Paramagnetism:
  χ > 0, small
  Curie law: χ = C/T  (isolated magnetic moments)
  C = nμ₀μ²/3kB  (Curie constant)
  Pauli paramagnetism (metals): χ ∝ g(EF), T-independent

Ferromagnetism:
  Spontaneous magnetization below TC (Curie temperature)
  Weiss molecular field: Bmol = λM
  Mean field theory: M = nμ·tanh(μ(B+λM)/kBT)
  TC = nμ₀μ²λ/3kB
  Above TC: Curie-Weiss: χ = C/(T-TC)

Antiferromagnetism:
  Neighboring spins antiparallel
  Neel temperature TN: transition to disorder
  χ has maximum at TN

Ferrimagnetism:
  Antiparallel but unequal moments → net magnetization
  Example: magnetite Fe₃O₄

Ising model:
  H = -J Σ_<ij> SᵢSⱼ - B Σᵢ Sᵢ
  J > 0: ferromagnetic, J < 0: antiferromagnetic
  1D: no phase transition at T > 0 (Ising 1925)
  2D: TC = 2J/kB·ln(1+√2) (Onsager 1944)
  3D: requires numerical methods
```

---

## Superconductivity
```
Discovery: Onnes 1911 (mercury, 4.2 K)
Meissner effect: perfect diamagnetism (B = 0 inside)
Critical temperature TC, critical field HC(T)

London equations:
  ∂J/∂t = (nse²/m)E
  ∇×J = -(nse²/m)B
  London penetration depth: λL = √(m/μ₀nse²)
  Magnetic field decays inside: B(x) = B₀exp(-x/λL)

BCS Theory (Bardeen, Cooper, Schrieffer 1957):
  Cooper pairs: two electrons bound via phonon exchange
  Binding energy gap: Δ = 2ℏωD exp(-1/N(0)V)
  TC = 1.13 ℏωD/kB exp(-1/N(0)V)
  Energy gap: 2Δ(0) = 3.52 kBTC  (BCS universal ratio)

Coherence length: ξ = ℏvF/πΔ
Type I vs Type II:
  κ = λL/ξ < 1/√2: Type I (complete Meissner, single HC)
  κ > 1/√2: Type II (vortex phase, HC1 < H < HC2)

Josephson effect:
  Current through insulating barrier: I = IC sin(φ)
  DC Josephson: supercurrent with no voltage
  AC Josephson: V = ℏ/2e · dφ/dt = hf/2e
  SQUID: superconducting quantum interference device

High-temperature superconductors:
  Cuprates (YBCO): TC ~ 90-130 K
  Iron-based: TC ~ 55 K
  MgB₂: TC = 39 K
  Mechanism not fully understood (not BCS)
  Record: LaH₁₀ at high pressure, TC ~ 250 K
```

---

## Phase Transitions & Critical Phenomena
```
Order parameter η:
  η = 0 in disordered phase, η ≠ 0 in ordered phase
  Magnetization (magnetic), density difference (liquid-gas)

Landau theory:
  F = a₀ + a₂(T-TC)η² + a₄η⁴ + ...
  a₄ > 0: second order transition
  a₄ < 0: first order transition

Critical exponents:
  M ∝ |T-TC|^β         β ≈ 0.326 (3D Ising)
  χ ∝ |T-TC|^(-γ)      γ ≈ 1.237
  Cv ∝ |T-TC|^(-α)     α ≈ 0.110
  ξ ∝ |T-TC|^(-ν)      ν ≈ 0.630
  Mean field: β=1/2, γ=1, α=0, ν=1/2

Scaling and universality:
  Critical exponents depend only on:
  - Dimensionality d
  - Symmetry of order parameter
  NOT on microscopic details!

Renormalization group (Wilson, Nobel 1982):
  Systematic method to calculate critical exponents
  Key idea: integrate out short-wavelength fluctuations
  Fixed points → universality classes
```

---

## Topological Materials
```
Integer Quantum Hall Effect (IQHE):
  2D electron gas in magnetic field
  Hall conductance: σxy = ne²/h  (n = integer)
  Chern number: topological invariant
  Robust against disorder!

Topological insulators:
  Bulk insulating gap, but metallic surface states
  Protected by time-reversal symmetry
  Surface states: Dirac cone, spin-momentum locking
  Examples: Bi₂Se₃, Bi₂Te₃, HgTe quantum wells

Topological invariants:
  Z₂ invariant (time-reversal invariant systems)
  Chern number (breaks time-reversal)
  Calculated from Bloch wavefunctions in BZ

Weyl semimetals:
  Linear crossing of two bands in 3D (Weyl points)
  Topological charge (chirality) ±1
  Fermi arc surface states connecting Weyl points
  Examples: TaAs, WTe₂

Majorana fermions:
  Particles that are their own antiparticles
  Predicted in topological superconductors
  Non-Abelian anyons — topological quantum computing
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Free electron model for semiconductors | Need band theory — effective mass matters |
| Confusing phonons and photons | Phonons: quantized lattice vibrations (not light) |
| Type I vs II superconductors | Determined by κ = λ/ξ ratio |
| Mean field always valid | Fluctuations crucial near TC, especially in low d |
| Band gap = energy gap | In superconductors energy gap is different concept |
| All metals are Fermi liquids | Strongly correlated systems (Mott insulators) break down |

---

## Related Skills

- **quantum-mechanics-expert**: Foundation of band theory
- **electromagnetism-expert**: Maxwell equations in materials
- **statistical-mechanics**: Phase transitions and thermodynamics
- **semiconductor-materials-expert**: Device applications
- **quantum-computing-expert**: Topological qubits
- **materials-science-expert**: Crystal structure and properties
