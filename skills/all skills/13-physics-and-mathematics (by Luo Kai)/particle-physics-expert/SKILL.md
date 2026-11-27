---
author: luo-kai
name: particle-physics-expert
description: Expert-level particle physics knowledge. Use when working with the Standard Model, quarks, leptons, bosons, fundamental forces, Feynman diagrams, quantum field theory, particle accelerators, or particle detectors. Also use when the user mentions 'Standard Model', 'quark', 'lepton', 'boson', 'Higgs', 'gluon', 'neutrino', 'antimatter', 'Feynman diagram', 'QCD', 'QED', 'electroweak', 'LHC', or 'particle accelerator'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Particle Physics Expert

You are a world-class physicist with deep expertise in particle physics covering the Standard Model, quantum field theory, fundamental forces, particle interactions, accelerator physics, detector technology, and physics beyond the Standard Model.

## Before Starting

1. **Topic** — Standard Model, specific particles, forces, interactions, or experiments?
2. **Level** — Conceptual, undergraduate, or graduate?
3. **Goal** — Understand concept, calculate amplitude, or analyze data?
4. **Math level** — Conceptual, relativistic kinematics, or QFT?
5. **Context** — Theory, experiment, or phenomenology?

---

## Core Expertise Areas

- **Standard Model**: particles, forces, symmetries, gauge theories
- **Quarks & Hadrons**: quark model, QCD, confinement, hadron spectroscopy
- **Leptons**: electron, muon, tau, neutrinos, lepton universality
- **Gauge Bosons**: photon, W, Z, gluons, Higgs mechanism
- **Feynman Diagrams**: vertices, propagators, amplitudes
- **Electroweak Theory**: unification, spontaneous symmetry breaking
- **QCD**: asymptotic freedom, confinement, parton model
- **Beyond SM**: supersymmetry, dark matter candidates, grand unification

---

## The Standard Model
```
The Standard Model: quantum field theory of strong, weak,
and electromagnetic interactions.
Gauge symmetry: SU(3)C × SU(2)L × U(1)Y

FERMIONS (spin-½, matter particles):

Quarks (6 flavors, 3 colors each):
  Generation 1: up (u, 2/3e), down (d, -1/3e)
  Generation 2: charm (c, 2/3e), strange (s, -1/3e)
  Generation 3: top (t, 2/3e), bottom (b, -1/3e)

Leptons (6 flavors):
  Generation 1: electron (e⁻, -e), electron neutrino (νe, 0)
  Generation 2: muon (μ⁻, -e), muon neutrino (νμ, 0)
  Generation 3: tau (τ⁻, -e), tau neutrino (ντ, 0)

Each fermion has antiparticle (opposite quantum numbers).

BOSONS (integer spin, force carriers):
  Photon (γ):      spin-1, massless, EM force
  W± bosons:       spin-1, mass ~80 GeV, weak force (charged current)
  Z⁰ boson:        spin-1, mass ~91 GeV, weak force (neutral current)
  Gluons (g):      spin-1, massless, 8 types, strong force
  Higgs (H):       spin-0, mass ~125 GeV, gives mass via Yukawa coupling
  Graviton:        spin-2, massless, gravity (NOT in SM)
```

---

## Fundamental Forces
```python
def fundamental_forces():
    return {
        'Electromagnetic': {
            'carrier':      'Photon (γ)',
            'range':        'Infinite (1/r²)',
            'strength':     'α = 1/137 (fine structure constant)',
            'theory':       'QED (Quantum Electrodynamics)',
            'acts_on':      'Charged particles',
            'gauge_group':  'U(1)'
        },
        'Weak': {
            'carrier':      'W±, Z⁰ bosons',
            'range':        '~10⁻¹⁸ m (heavy mediators)',
            'strength':     'GF = 1.17×10⁻⁵ GeV⁻² (Fermi constant)',
            'theory':       'Electroweak (Glashow-Salam-Weinberg)',
            'acts_on':      'All fermions, flavor changing',
            'gauge_group':  'SU(2)L × U(1)Y'
        },
        'Strong': {
            'carrier':      '8 gluons',
            'range':        '~10⁻¹⁵ m (confinement)',
            'strength':     'αs ≈ 1 at low energy, decreases at high E',
            'theory':       'QCD (Quantum Chromodynamics)',
            'acts_on':      'Quarks and gluons (color charge)',
            'gauge_group':  'SU(3)C'
        },
        'Gravity': {
            'carrier':      'Graviton (hypothetical)',
            'range':        'Infinite (1/r²)',
            'strength':     'GN = 6.67×10⁻¹¹ (weakest by far)',
            'theory':       'General Relativity (not quantized)',
            'acts_on':      'All energy-momentum',
            'gauge_group':  'Diffeomorphism invariance'
        }
    }
```

---

## Quarks & Hadrons
```
Quark properties:
  Color charge: red, green, blue (and anticolors)
  Fractional electric charge: +2/3 or -1/3
  Confinement: quarks never observed free
  Asymptotic freedom: αs → 0 at high energy

Hadrons (bound states of quarks):
  Mesons: quark-antiquark (qq̄)
    Pion: π+ = ud̄, π⁻ = ūd, π⁰ = (uū-dd̄)/√2
    Kaon: K+ = us̄, K⁻ = ūs
    J/ψ = cc̄, Υ = bb̄

  Baryons: three quarks (qqq)
    Proton: uud  (charge +1)
    Neutron: udd (charge 0)
    Λ: uds, Σ: uus/uds/dds, Ξ: uss/dss, Ω: sss

Quark model SU(3) flavor symmetry:
  Eightfold Way (Gell-Mann): organize hadrons into multiplets
  Predicted Ω⁻ baryon before discovery (1964) ✓

Quark masses (approximate):
  u: 2.2 MeV, d: 4.7 MeV, s: 96 MeV
  c: 1.27 GeV, b: 4.18 GeV, t: 173 GeV

Top quark:
  Heaviest known elementary particle: 173 GeV ≈ mass of gold atom!
  Too heavy to form hadrons — decays before hadronization.
  Discovered at Fermilab Tevatron 1995.
```

---

## QCD — Quantum Chromodynamics
```
QCD Lagrangian:
  L = -¼FᵃᵘᵛFᵃᵘᵛ + Σᶠ q̄ᶠ(iγᵘDᵘ - mᶠ)qᶠ
  Fᵃᵘᵛ = ∂ᵘAᵃᵛ - ∂ᵛAᵃᵘ + gfᵃᵇᶜAᵇᵘAᶜᵛ  (gluon field strength)
  Dᵘ = ∂ᵘ - igAᵃᵘTᵃ  (covariant derivative)
  Tᵃ = Gell-Mann matrices/2 (SU(3) generators)

Key properties:
  Asymptotic freedom: αs → 0 as Q² → ∞
    Discovered by Gross, Politzer, Wilczek (Nobel 2004)
    Quarks behave as free particles at very high energy
  Confinement: αs → large as Q² → 0
    String tension: ~1 GeV/fm
    Quark-antiquark potential: V(r) ≈ -αs/r + kr

Gluons:
  8 gluons (SU(3) has 8 generators)
  Carry color charge — gluons interact with each other!
  Self-interaction → confinement and asymptotic freedom

Running coupling:
  αs(Q²) = αs(μ²) / [1 + (αs(μ²)/2π)·b·ln(Q²/μ²)]
  b = (11Nc - 2Nf)/3  (Nc=3 colors, Nf=6 flavors)
  b > 0 → coupling decreases at high energy ✓

Parton model (Feynman):
  At high energy, proton seen as collection of partons
  Parton distribution functions (PDFs): f(x,Q²)
  x = fraction of proton momentum carried by parton
  DIS: deep inelastic scattering probes proton structure
```

---

## Electroweak Theory
```
Glashow-Salam-Weinberg model (Nobel 1979):
  Unifies EM and weak forces.
  Gauge group: SU(2)L × U(1)Y

Weak isospin (SU(2)L):
  Acts only on left-handed fermions
  Left-handed doublets: (νe,e)L, (u,d)L, etc.
  Right-handed singlets: eR, uR, dR, etc.

Weinberg angle θW:
  sin²θW = 0.231
  Relates W and Z masses: MW = MZ cosθW
  MW ≈ 80 GeV, MZ ≈ 91 GeV ✓

Parity violation:
  Weak force maximally violates parity (V-A theory)
  Only left-handed particles (right-handed antiparticles) couple to W±
  Wu experiment (1956): β decay of ⁶⁰Co showed asymmetry

CP violation:
  CKM matrix: mixing of quark generations
  Cabibbo-Kobayashi-Maskawa: 3×3 unitary matrix
  Complex phase → CP violation → matter-antimatter asymmetry
  Too small to explain observed baryon asymmetry of universe.
```

---

## Higgs Mechanism
```
Problem: gauge bosons must be massless for gauge invariance,
         but W and Z are massive (~80-91 GeV).

Higgs mechanism (spontaneous symmetry breaking):
  Higgs field φ has Mexican hat potential:
  V(φ) = -μ²|φ|² + λ|φ|⁴
  Minimum at |φ| = v/√2, v = 246 GeV (vacuum expectation value)

  Symmetry broken: SU(2)L × U(1)Y → U(1)EM
  W± and Z eat Goldstone bosons → gain mass
  Photon stays massless

Particle masses:
  MW = gv/2, MZ = MW/cosθW
  mf = yf·v/√2  (Yukawa coupling yf for each fermion)

Higgs boson:
  Discovered at LHC (ATLAS+CMS) July 4, 2012!
  Mass: mH = 125.09 GeV
  Spin-0 (scalar), CP-even
  Couples to particles proportional to their mass.

Higgs production at LHC:
  Gluon fusion: gg → H (dominant, via top quark loop)
  VBF: qq → qqH (vector boson fusion)
  Associated: pp → WH, ZH

Higgs decay:
  H → bb̄ (58%), H → WW* (21%), H → gg (9%)
  H → ττ (6%), H → ZZ* (3%), H → γγ (0.2%)
```

---

## Feynman Diagrams
```
Rules for QED (example):
  External lines: fermion in/out, photon in/out
  Vertex: -iqeγᵘ (fermion-fermion-photon)
  Fermion propagator: i(p̸+m)/(p²-m²+iε)
  Photon propagator: -igᵘᵛ/(k²+iε)

Reading diagrams:
  Time flows left to right (usually)
  Lines: fermions (arrows), bosons (wavy/curly/dashed)
  Vertices: interaction points
  Internal lines: virtual particles (off shell)
  Each diagram = one term in perturbation series

Example processes:
  e⁺e⁻ → μ⁺μ⁻: t-channel photon exchange
  Compton scattering: e⁻γ → e⁻γ (s and u channel)
  Møller scattering: e⁻e⁻ → e⁻e⁻ (t and u channel)
  Pair production: γγ → e⁺e⁻

Amplitude:  M = vertex × propagator × vertex × ...
Cross section: σ ∝ |M|²
Decay rate: Γ ∝ |M|²

Loop diagrams:
  Higher order corrections (αⁿ for nth loop)
  Require renormalization (infinities cancelled)
  Anomalous magnetic moment: g-2 = α/π + ... (QED prediction matches experiment to 12 decimal places!)
```

---

## Conservation Laws
```
Exact conservation laws:
  Energy-momentum (4-momentum)
  Electric charge
  Color charge
  Lepton number (Le, Lμ, Lτ separately)
  Baryon number B = (quarks - antiquarks)/3

Approximate/violated:
  Parity P: violated by weak force
  Charge conjugation C: violated by weak force
  CP: slightly violated (kaon, B meson systems)
  CPT: exact (theorem from QFT)
  Flavor (strangeness, charm, etc.): violated by weak

Selection rules:
  Strong: conserves all flavors
  EM: conserves all flavors, charge
  Weak: changes flavor (enables quark mixing, beta decay)
```

---

## Particle Accelerators & Detectors
```python
def accelerator_types():
    return {
        'Cyclotron': {
            'principle':  'Spiral path in magnetic field, RF acceleration',
            'limit':      'Relativistic mass increase (synchrocyclotron fixes this)',
            'use':        'Medical isotope production, low energy physics'
        },
        'Synchrotron': {
            'principle':  'Circular orbit, varying B and RF to keep radius constant',
            'examples':   'LHC (27 km), Tevatron, LEP',
            'LHC':        '13.6 TeV (2022), 27 km circumference, p-p collisions'
        },
        'Linear accelerator': {
            'principle':  'RF cavities accelerate particles in straight line',
            'examples':   'SLAC (Stanford), CERN LINAC, medical LINACs',
            'use':        'Electron acceleration, medical radiation therapy'
        },
        'Collider vs fixed target': {
            'collider':       'Both beams moving — higher CM energy: √s = 2E',
            'fixed_target':   'One beam, one target at rest: √s ≈ √(2mE)',
            'advantage':      'Colliders vastly more efficient for discovery'
        }
    }

def detector_components():
    return {
        'Tracking': 'Silicon pixels, drift chambers — measure particle paths',
        'Calorimetry': {
            'EM': 'Electromagnetic: electrons, photons (PbWO4, liquid Ar)',
            'Hadronic': 'Hadrons (iron/scintillator, liquid Ar)'
        },
        'Muon system': 'Outer detector — only muons penetrate calorimeters',
        'Magnet': 'Solenoid or toroid — curves tracks to measure momentum',
        'Trigger': 'Real-time selection of interesting events (~40 MHz → few Hz)',
        'Key detectors': 'ATLAS, CMS, ALICE, LHCb at LHC'
    }
```

---

## Beyond the Standard Model
```
Problems with SM:
  No gravity
  Dark matter (27% of universe — no SM candidate)
  Dark energy (68% of universe — unexplained)
  Matter-antimatter asymmetry
  Hierarchy problem: why mH << mPlanck?
  Neutrino masses (SM predicts massless ν)
  Strong CP problem

Neutrino masses:
  Neutrino oscillations confirm nonzero masses (Nobel 2015)
  Δm² ~ 10⁻³ - 10⁻⁵ eV²
  Mixing: PMNS matrix (analogous to CKM)
  Absolute mass scale unknown, Σmν < 0.12 eV

Supersymmetry (SUSY):
  Every SM particle has superpartner (differs by ½ spin)
  Quarks → squarks, leptons → sleptons
  Photon → photino, Higgs → higgsino
  Lightest SUSY particle (LSP): dark matter candidate?
  Not found at LHC (ruled out up to ~TeV scale)

Grand Unified Theories (GUT):
  Unify strong + electroweak: SU(5), SO(10)
  Predict proton decay: τp > 10³⁴ years (not yet observed)
  Gauge coupling unification at ~10¹⁶ GeV

String theory / M-theory:
  Replace point particles with 1D strings
  Naturally includes gravity
  Requires extra dimensions (10 or 11)
  No experimental confirmation yet
```

---

## Key Numbers
```
Fine structure constant: α = e²/4πε₀ℏc = 1/137.036
Strong coupling: αs(MZ) = 0.118
Fermi constant: GF/(ℏc)³ = 1.166×10⁻⁵ GeV⁻²
Weinberg angle: sin²θW = 0.2312
Higgs vev: v = 246 GeV
Proton mass: mp = 938.3 MeV
Neutron mass: mn = 939.6 MeV
Electron mass: me = 0.511 MeV
W mass: MW = 80.4 GeV
Z mass: MZ = 91.2 GeV
Higgs mass: mH = 125.1 GeV
Top mass: mt = 173 GeV
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Proton = 3 quarks always | Virtual quarks and gluons (sea quarks) also present |
| Neutrinos are massless | Oscillations prove they have mass (tiny but nonzero) |
| Antiparticles are rare | Equal amounts created in pair production |
| Gluons are like photons | Gluons carry color charge and self-interact |
| Higgs gives all mass | Strong nuclear force (QCD binding) gives most of proton mass |
| Virtual particles exist | Virtual particles are mathematical tools in perturbation theory |

---

## Related Skills

- **quantum-mechanics-expert**: Foundation of QFT
- **special-relativity-expert**: Relativistic kinematics
- **nuclear-physics-expert**: Quark content of nuclei
- **electromagnetism-expert**: QED is quantum EM
- **condensed-matter-expert**: Many techniques shared
