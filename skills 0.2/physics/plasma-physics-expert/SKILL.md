---
name: plasma-physics-expert
description: Expert-level plasma physics knowledge. Use when working with plasma state, Debye shielding, plasma oscillations, magnetohydrodynamics, plasma confinement, fusion plasmas, space plasmas, plasma waves, or plasma instabilities. Also use when the user mentions 'plasma', 'Debye length', 'plasma frequency', 'MHD', 'magnetic confinement', 'tokamak', 'plasma instability', 'Alfven wave', 'Langmuir probe', 'ionosphere', or 'solar wind'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Plasma Physics Expert

You are a world-class physicist with deep expertise in plasma physics covering plasma fundamentals, magnetohydrodynamics, plasma waves, instabilities, magnetic confinement fusion, space plasmas, and plasma applications.

## Before Starting

1. **Topic** — Plasma fundamentals, MHD, waves, confinement, or space plasmas?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Understand concept, solve problem, or analyze system?
4. **Context** — Fusion energy, space physics, or industrial plasma?
5. **Geometry** — Unmagnetized, magnetized, or specific configuration?

---

## Core Expertise Areas

- **Plasma Fundamentals**: Debye shielding, plasma frequency, criteria
- **Single Particle Motion**: guiding center, drifts, magnetic mirror
- **Fluid Description**: MHD equations, pressure balance, equilibria
- **Plasma Waves**: electromagnetic, electrostatic, Alfven waves
- **Instabilities**: Rayleigh-Taylor, kink, interchange, drift waves
- **Magnetic Confinement**: tokamak, stellarator, mirror machines
- **Space Plasmas**: solar wind, magnetosphere, ionosphere
- **Plasma Applications**: processing, thrusters, lighting

---

## Plasma Fundamentals
```
Definition of plasma:
  Fourth state of matter: ionized gas where collective
  electromagnetic effects dominate individual particle behavior.

Plasma criteria (all three must hold):
  1. λD << L  (Debye length << system size)
  2. ND >> 1  (many particles in Debye sphere)
  3. ωpτ >> 1  (plasma frequency × collision time >> 1)

Debye shielding:
  Plasma screens electric fields over Debye length.
  Potential: φ(r) = (q/4πε₀r)exp(-r/λD)
  λD = √(ε₀kBTe/nee²)  (electron Debye length)
  λD(m) ≈ 69√(Te(K)/ne(m⁻³))

Plasma frequency:
  Natural oscillation frequency of electrons.
  ωpe = √(nee²/ε₀me)
  fpe(Hz) ≈ 9√ne(m⁻³)
  Ion plasma frequency: ωpi = √(ne²/ε₀mi) << ωpe

Plasma parameter:
  ND = (4π/3)nλD³  (particles in Debye sphere)
  Weakly coupled (ideal) plasma: ND >> 1
  Coupling parameter: Γ = e²/4πε₀λDkBT = 1/(3ND)^(1/3)

Ionization:
  Saha equation: ne²/nn = (2πmekBT/h²)^(3/2) exp(-χ/kBT)
  χ = ionization energy
  Temperatures needed: few thousand to million K
```

---

## Single Particle Motion
```
Equation of motion:
  m dv/dt = q(E + v×B)

Circular motion in B field:
  Cyclotron frequency: ωc = qB/m
  Gyroradius (Larmor radius): rL = mv⊥/qB = v⊥/ωc
  Electrons: faster, smaller rL
  Ions: slower, larger rL

Guiding center drifts:
  E×B drift: vE = E×B/B²  (same for all particles, no current)
  Grad-B drift: v∇B = ±(mv⊥²/2qB³)B×∇B  (sign depends on charge)
  Curvature drift: vR = (mv∥²/qB⁴)B×(B·∇)B
  Polarization drift: vp = (m/qB²)dE⊥/dt

Magnetic mirror:
  Conserved quantity: μ = mv⊥²/2B (magnetic moment, adiabatic invariant)
  Mirror condition: v⊥²(0)/v²(0) < B(0)/Bmax
  Loss cone: particles with v∥/v⊥ > √(Bmax/B₀-1) escape
  Applications: mirror machines, radiation belts

Adiabatic invariants:
  First: μ = mv⊥²/2B (fast gyration)
  Second: J = ∮mv∥ dl (bounce motion)
  Third: Φ = ∮B·dA (drift motion)
```

---

## Magnetohydrodynamics (MHD)
```
MHD equations (single fluid):
  ∂ρ/∂t + ∇·(ρv) = 0           (continuity)
  ρ(∂v/∂t + v·∇v) = J×B - ∇P  (momentum, J×B = magnetic force)
  ∂B/∂t = ∇×(v×B) - ∇×(η∇×B) (induction, η = resistivity)
  ∂P/∂t + v·∇P = -γP∇·v        (energy/adiabatic)
  J = (1/μ₀)∇×B                (Ampere, ∂E/∂t neglected)
  ∇·B = 0

Ideal MHD (η = 0):
  Magnetic flux frozen into fluid (Alfven's theorem)
  Flux tubes move with plasma

MHD equilibrium:
  J×B = ∇P  (pressure gradient balanced by magnetic force)
  β = 2μ₀P/B²  (ratio of plasma to magnetic pressure)
  High β: plasma dominated, Low β: field dominated

Pinch configurations:
  Z-pinch: current along z → Bθ → inward J×B force
  θ-pinch: current in θ → Bz → radial force
  Screw pinch: combination of both

Magnetic pressure and tension:
  Magnetic pressure: B²/2μ₀  (pushes field lines apart)
  Magnetic tension: B²/μ₀R  (like stretched elastic band)
  These two balance in equilibrium configurations.
```

---

## Plasma Waves
```python
def plasma_wave_modes():
    return {
        'Electromagnetic (unmagnetized)': {
            'dispersion':   'ω² = ωpe² + c²k²',
            'cutoff':       'ω = ωpe (k=0, no propagation below)',
            'phase_vel':    'vph = c/√(1-ωpe²/ω²) > c',
            'group_vel':    'vg = c√(1-ωpe²/ω²) < c',
            'application':  'Ionospheric reflection of radio waves'
        },
        'Langmuir waves (electrostatic electron)': {
            'dispersion':   'ω² = ωpe²(1 + 3k²λD²)',
            'character':    'Longitudinal electron oscillations',
            'damping':      'Landau damping when vph ≈ vte'
        },
        'Ion acoustic waves': {
            'dispersion':   'ω = kcs, cs = √(γkBTe/mi)',
            'condition':    'Te >> Ti (else heavily damped)',
            'analogous_to': 'Sound waves in neutral gas'
        },
        'Alfven waves': {
            'dispersion':   'ω = kvA, vA = B/√(μ₀ρ)',
            'character':    'Field line bending — like elastic string',
            'polarization': 'Transverse, along B',
            'application':  'Solar corona, magnetosphere'
        },
        'Magnetosonic waves': {
            'dispersion':   'ω² = k²(vA² + cs²) (perpendicular to B)',
            'character':    'Compressional waves across B field'
        },
        'Whistler waves': {
            'dispersion':   'ω = ωce·cos(θ)·c²k²/ωpe²',
            'character':    'Right-hand circularly polarized',
            'application':  'Lightning → ionosphere, heard as whistle'
        }
    }
```

### Landau Damping
```
Wave-particle resonance: vph = ω/k ≈ vparticle
Particles moving slightly slower than wave:
  Gain energy from wave → wave damps (more slow than fast particles)
Landau damping: collisionless damping of plasma waves
  γ ∝ df/dv|v=vph  (growth if slope positive)
  Fundamental QM-free result from kinetic theory

Inverse Landau damping:
  If df/dv > 0 at resonance: wave grows!
  Beam-plasma instability: electron beam → Langmuir waves
```

---

## Plasma Instabilities
```
Classification:
  Macroscopic (MHD): involve bulk fluid motion
  Microscopic (kinetic): involve velocity distribution

Key MHD instabilities:
  Rayleigh-Taylor: heavy fluid on top of light (gravitational)
    Growth rate: γ = √(kg·Atwood number)
    Relevant: inertial confinement fusion

  Kink (m=1) instability:
    Current-carrying plasma column bends and kinks
    Kruskal-Shafranov condition for stability:
    q = rBz/RBθ > 1  (safety factor must exceed 1)

  Sausage (m=0) instability:
    Plasma column pinches and expands alternately

  Interchange instability:
    Magnetic field lines and plasma interchange position
    Stabilized by magnetic shear

  Ballooning instability:
    Pressure-driven, occurs on bad curvature side

Kinetic instabilities:
  Beam-plasma: electron beam → Langmuir waves
  Weibel: filamentation of current sheets
  Buneman: relative drift between electrons and ions
  Ion acoustic: when electron drift exceeds ion sound speed

Tokamak-specific:
  Tearing modes: magnetic reconnection, form islands
  Neoclassical tearing modes (NTMs): bootstrap current driven
  Edge-localized modes (ELMs): periodic bursts at plasma edge
  Disruptions: catastrophic loss of plasma confinement
```

---

## Magnetic Confinement Fusion
```
Requirements for fusion:
  Temperature: T ~ 10⁸ K (10 keV)
  Lawson criterion: nτE > 10²⁰ m⁻³s (D-T reaction)
  Triple product: nTτE > 3×10²¹ m⁻³·keV·s

Tokamak:
  Toroidal geometry — plasma confined by combination of:
    Toroidal field BT (external coils)
    Poloidal field BP (from plasma current)
  Safety factor: q(r) = rBT/RBP ≈ 1 at center, ~3 at edge
  H-mode: high confinement mode with edge transport barrier

Key tokamak parameters:
  ITER: R=6.2m, a=2m, BT=5.3T, IP=15MA, Q=10 goal
  JET (record): Q~0.67, 16MW fusion power (1997)
  NIF (inertial): Q~1.5 achieved (2022) via laser compression

Stellarator:
  No net plasma current → no disruptions
  More complex 3D coil geometry
  Example: Wendelstein 7-X (Germany)

Energy confinement:
  τE = Wthermal/Ploss  (energy confinement time)
  Empirical scaling: τE ∝ n^a T^b B^c R^d ...
  IPB98: τE ∝ H·R^1.97·B^0.15·...

Plasma heating:
  Ohmic heating: I²R (limited by decreasing resistivity at high T)
  Neutral beam injection (NBI): fast neutrals → charge exchange
  RF heating: ICRH (ion), ECRH (electron), LH (lower hybrid)
```

---

## Space Plasmas
```
Solar wind:
  Continuous flow of plasma from Sun's corona
  Speed: 300-800 km/s, density: 5-10 cm⁻³ at Earth
  Carries frozen-in solar magnetic field (IMF)
  Parker spiral: rotation + radial flow → spiral IMF

Magnetosphere:
  Earth's magnetic field deflects solar wind
  Magnetopause: ~10 RE on dayside, long tail on nightside
  Van Allen radiation belts: trapped energetic particles
  Outer belt: electrons (3-7 RE), Inner belt: protons (1.5-2 RE)

Magnetic reconnection:
  Oppositely directed field lines break and reconnect
  Converts magnetic energy to particle kinetic energy
  Drives: substorms, solar flares, coronal mass ejections
  Rate: Alfvenic (fast reconnection) or resistive (slow)

Ionosphere:
  Partially ionized atmosphere: 60-1000 km altitude
  Layers: D (60-90km), E (90-150km), F (150-1000km)
  Radio wave reflection below critical frequency
  Aurora: energetic particles from magnetosphere → light emission

Heliosphere:
  Solar wind bubble extending to ~100 AU
  Termination shock: solar wind slows to subsonic (~90 AU)
  Heliopause: boundary with interstellar medium (~120 AU)
  Voyager 1 crossed heliopause in 2012!
```

---

## Plasma Diagnostics
```python
def plasma_diagnostics():
    return {
        'Langmuir probe': {
            'measures':     'ne, Te, plasma potential',
            'method':       'Current-voltage characteristic in plasma',
            'limitation':   'Perturbs plasma, limited to cold plasmas'
        },
        'Thomson scattering': {
            'measures':     'ne, Te profiles',
            'method':       'Laser scattered by electrons',
            'advantage':    'Non-perturbative, spatially resolved'
        },
        'Interferometry': {
            'measures':     'Line-integrated electron density',
            'method':       'Phase shift of microwave/laser beam',
            'types':        'Microwave, CO₂ laser, visible'
        },
        'Spectroscopy': {
            'measures':     'Ti, vflow, Zeff, impurity content',
            'method':       'Doppler broadening and shift of spectral lines',
            'range':        'Visible to X-ray'
        },
        'Magnetic diagnostics': {
            'measures':     'Plasma current, equilibrium, MHD activity',
            'method':       'Rogowski coils, flux loops, Mirnov coils',
            'use':          'Real-time control of tokamak'
        },
        'Neutron diagnostics': {
            'measures':     'Fusion power, ion temperature',
            'method':       'Count DD/DT fusion neutrons',
            'detector':     'Scintillators, fission chambers'
        }
    }
```

---

## Applications
```
Industrial plasma:
  Semiconductor manufacturing: plasma etching, CVD deposition
  Surface treatment: hardening, cleaning, coating
  Plasma spray: thermal spray coatings
  Plasma cutting and welding
  Sterilization: cold atmospheric plasma

Electric propulsion:
  Hall thruster: E×B drift accelerates ions
  Ion thruster: electrostatic acceleration
  Specific impulse: 1000-10000 s (vs ~450s chemical)
  Used on: Dawn, Hayabusa, Starlink satellites

Plasma lighting:
  Fluorescent lamps: Hg plasma + phosphor
  HID (high-intensity discharge): metal halide, sodium
  Plasma displays: noble gas + phosphor pixels

Plasma medicine:
  Cold atmospheric plasma: wound healing, cancer treatment
  Reactive oxygen/nitrogen species → therapeutic effects
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Plasma = hot gas | Plasma requires collective behavior (ND >> 1) |
| E×B drift carries current | E×B is same for all species — no net current |
| Alfven speed > c possible | Only in low-density plasmas — no information faster than c |
| MHD valid always | Need λ << L and collision-dominated for MHD |
| Magnetic mirror reflects all particles | Loss cone exists — particles with large v∥ escape |
| Fusion = solved problem | Q > 1 achieved but net electricity still engineering challenge |

---

## Key Parameters
```
Electron plasma frequency: ωpe = √(ne²/ε₀me) ≈ 56.4√n rad/s
Electron cyclotron freq:   ωce = eB/me ≈ 1.76×10¹¹B rad/s
Debye length:              λD = 69√(Te/n) m (T in K, n in m⁻³)
Alfven speed:              vA = B/√(μ₀ρ) m/s
Ion sound speed:           cs = √(γkBTe/mi) m/s
Thermal velocity:          vte = √(2kBTe/me) m/s
```

---

## Related Skills

- **nuclear-physics-expert**: Fusion reactions
- **electromagnetism-expert**: Maxwell equations in plasma
- **fluid-mechanics-expert**: MHD as conducting fluid
- **astrophysics-expert**: Solar and space plasmas
- **fusion-energy-expert**: Plasma confinement for energy
