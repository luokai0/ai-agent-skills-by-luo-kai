---
author: luo-kai
name: nuclear-physics-expert
description: Expert-level nuclear physics knowledge. Use when working with nuclear structure, radioactive decay, nuclear reactions, fission, fusion, binding energy, nuclear models, radiation, or nuclear applications. Also use when the user mentions 'radioactive decay', 'half life', 'binding energy', 'fission', 'fusion', 'alpha decay', 'beta decay', 'gamma decay', 'nuclear reaction', 'cross section', 'Q value', 'nuclear reactor', or 'radiation dose'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Nuclear Physics Expert

You are a world-class physicist with deep expertise in nuclear physics covering nuclear structure, radioactive decay, nuclear reactions, fission, fusion, nuclear models, radiation detection, and nuclear applications in energy and medicine.

## Before Starting

1. **Topic** — Nuclear structure, decay, reactions, fission/fusion, or applications?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Solve problem, understand concept, or calculate quantity?
4. **Context** — Physics, nuclear engineering, or medical physics?
5. **Focus** — Theory, experiment, or applications?

---

## Core Expertise Areas

- **Nuclear Structure**: protons, neutrons, binding energy, nuclear size
- **Nuclear Models**: liquid drop, shell model, collective model
- **Radioactive Decay**: alpha, beta, gamma, decay laws, half-life
- **Nuclear Reactions**: Q-value, cross sections, reaction types
- **Fission**: mechanism, chain reaction, criticality, reactors
- **Fusion**: thermonuclear, plasma confinement, stellar fusion
- **Radiation**: types, interactions with matter, detection, dosimetry
- **Applications**: nuclear power, medical imaging, radiation therapy

---

## Nuclear Structure Basics
```
Notation: ᴬzX
  A = mass number (protons + neutrons)
  Z = atomic number (protons)
  N = neutron number = A - Z

Nuclear radius:
  R = R₀A^(1/3)   R₀ = 1.2 fm = 1.2×10⁻¹⁵ m
  Nuclear density: ρ ≈ 2.3×10¹⁷ kg/m³ (same for all nuclei)

Nuclear force properties:
  Short range: ~1-2 fm
  Strongly attractive at 1-2 fm
  Repulsive at < 0.5 fm (hard core)
  Charge independent (same for p-p, n-n, p-n)
  Spin dependent
  Saturates: each nucleon interacts only with neighbors

Magic numbers: 2, 8, 20, 28, 50, 82, 126
  Nuclei with magic N or Z are especially stable.
  Doubly magic (both N and Z magic): ⁴He, ¹⁶O, ⁴⁰Ca, ²⁰⁸Pb
```

---

## Binding Energy
```
Mass defect:
  Δm = Zmp + Nmn - M(A,Z)
  mp = 1.007276 u, mn = 1.008665 u, 1 u = 931.5 MeV/c²

Binding energy:
  BE = Δm·c² = [Zmp + Nmn - M(A,Z)] × 931.5 MeV/u

Binding energy per nucleon: BE/A
  Maximum at ⁵⁶Fe (~8.8 MeV/nucleon) — most stable nucleus
  Fission releases energy: heavy nuclei split toward Fe
  Fusion releases energy: light nuclei combine toward Fe

Semi-empirical mass formula (Bethe-Weizsäcker):
  BE = avA - asA^(2/3) - ac·Z(Z-1)/A^(1/3) - aa(A-2Z)²/A ± δ

  Volume term:    av = 15.5 MeV  (bulk binding)
  Surface term:   as = 16.8 MeV  (surface nucleons less bound)
  Coulomb term:   ac = 0.72 MeV  (p-p repulsion)
  Asymmetry term: aa = 23 MeV    (N=Z preferred)
  Pairing term:   δ = ±12/√A MeV (even-even more stable)
```

---

## Radioactive Decay

### Decay Law
```
N(t) = N₀e^(-λt)
Activity: A(t) = λN(t) = A₀e^(-λt)
Half-life: t₁/₂ = ln2/λ = 0.693/λ
Mean lifetime: τ = 1/λ

Units:
  1 Becquerel (Bq) = 1 decay/second
  1 Curie (Ci) = 3.7×10¹⁰ Bq

Decay chain: parent → daughter → granddaughter...
Secular equilibrium: A_parent = A_daughter (if t₁/₂_parent >> t₁/₂_daughter)
```

### Alpha Decay
```
Parent → Daughter + ⁴₂He (alpha particle)
ᴬzX → ᴬ⁻⁴z₋₂Y + ⁴₂He

Q-value: Qα = [M(A,Z) - M(A-4,Z-2) - M(⁴He)] × 931.5 MeV
Alpha energy: Eα = Q·(A-4)/A  (daughter recoils)

Gamow theory (tunneling):
  Alpha tunnels through Coulomb barrier.
  λ ∝ exp(-2G)  G = Gamow factor
  G = 2π Z_d e² / (ℏvα)  (approximate)
  Geiger-Nuttall law: log(t₁/₂) ∝ 1/√Eα

Alpha emitters: heavy nuclei A > 210
Range in air: 2-10 cm (easily stopped by paper)
```

### Beta Decay
```
β⁻ decay (neutron-rich):
  n → p + e⁻ + ν̄e
  ᴬzX → ᴬz₊₁Y + e⁻ + ν̄e
  Q = [M(A,Z) - M(A,Z+1)] × 931.5 MeV

β⁺ decay (proton-rich):
  p → n + e⁺ + νe
  ᴬzX → ᴬz₋₁Y + e⁺ + νe
  Q = [M(A,Z) - M(A,Z-1) - 2me] × 931.5 MeV

Electron capture (EC):
  p + e⁻ → n + νe
  Competes with β⁺, always possible if Q_EC > 0

Continuous spectrum:
  Energy shared between e and ν → continuous β spectrum
  Neutrino hypothesis (Pauli 1930) explained missing energy

Fermi theory:
  Transition rate ∝ |Mfi|² × phase space
  Fermi integral: f(Z,Q) depends on endpoint energy
```

### Gamma Decay
```
Excited nucleus → ground state + γ photon
No change in A or Z.
Eγ = Eᵢ - Ef (nuclear transition energy)

Internal conversion:
  Alternative to γ emission.
  Nucleus transfers energy directly to atomic electron.
  Conversion electron emitted instead of γ.

Isomeric transitions:
  Long-lived excited states (isomers): t₁/₂ > 10⁻⁹ s
  Example: ⁹⁹ᵐTc (6 hr half-life) — used in medical imaging

Mössbauer effect:
  Recoil-free gamma emission/absorption in solids.
  Extremely precise energy measurement.
  Applications: test of GR, hyperfine interactions.
```

---

## Nuclear Reactions
```
General: a + A → B + b  or  A(a,b)B

Conservation laws:
  Mass number A (conserved)
  Charge Z (conserved)
  Energy (including rest mass energy)
  Momentum, angular momentum, parity

Q-value:
  Q = (M_reactants - M_products) × 931.5 MeV
  Q > 0: exothermic (energy released)
  Q < 0: endothermic (energy required, threshold reaction)

Threshold energy:
  Eth = |Q|(1 + ma/MA) / 2  (approximately)

Cross section σ:
  Probability of reaction: σ = R/(n·I)
  Units: barn = 10⁻²⁸ m² = 10⁻²⁴ cm²
  Total: σtotal = σelastic + σreaction

Breit-Wigner resonance:
  σ(E) = σ₀ · (Γ²/4) / [(E-E₀)² + Γ²/4]
  Resonance at E = E₀, width Γ = ℏ/τ
```

---

## Nuclear Fission
```
Discovery: Hahn, Strassmann, Meitner, Frisch (1938)

Mechanism:
  Heavy nucleus (U-235, Pu-239) absorbs neutron
  → Compound nucleus oscillates → splits into two fragments
  + 2-3 neutrons + ~200 MeV energy + gamma rays

U-235 fission:
  ²³⁵U + n → ²³⁶U* → ⁹²Kr + ¹⁴¹Ba + 3n + Q
  Q ≈ 200 MeV per fission
  Compare to chemical: ~few eV per reaction!

Energy release: mostly kinetic energy of fragments (~167 MeV)
  Fragment KE: 167 MeV
  Neutrons: 5 MeV
  Prompt γ: 7 MeV
  Delayed β,γ: 21 MeV
  Total: ~200 MeV

Chain reaction:
  k = multiplication factor = neutrons produced/neutrons absorbed
  k < 1: subcritical (reaction dies out)
  k = 1: critical (steady state)
  k > 1: supercritical (exponential growth → weapon or meltdown)

Neutron moderation:
  Fast neutrons → thermal neutrons (more efficient for fission)
  Moderators: water (H₂O, D₂O), graphite
  Slowing mechanism: elastic collisions

Nuclear reactor components:
  Fuel: enriched U-235 or Pu-239
  Moderator: slow down neutrons
  Control rods: absorb neutrons (B, Cd, Hf)
  Coolant: remove heat (water, CO₂, Na)
  Reflector: reduce neutron leakage
```

---

## Nuclear Fusion
```
Light nuclei + light nuclei → heavier nucleus + energy

Key reactions:
  D + T → ⁴He + n + 17.6 MeV  (most promising for reactors)
  D + D → T + p + 4.03 MeV
  D + D → ³He + n + 3.27 MeV
  p + p → D + e⁺ + ν + 0.42 MeV (solar pp chain)

Lawson criterion (ignition condition):
  nτ > 10²⁰ m⁻³s  (for D-T at optimal temperature)
  n = plasma density, τ = energy confinement time
  Temperature needed: T ~ 10⁸ K

Stellar fusion (pp chain in Sun):
  4p → ⁴He + 2e⁺ + 2ν + 26.7 MeV
  Powers Sun for ~10 billion years

Confinement approaches:
  Magnetic: Tokamak (ITER, JET), Stellarator
  Inertial: laser compression (NIF)
  Gravitational: stars!

Advantages over fission:
  Abundant fuel (deuterium from seawater)
  No long-lived radioactive waste
  Inherently safe (no chain reaction)
  Challenges: achieving net energy gain (Q > 1)

ITER: International Thermonuclear Experimental Reactor
  Q = 10 goal (10× more energy out than in)
  Located in France, first plasma ~2025
```

---

## Radiation & Dosimetry
```python
def radiation_types():
    return {
        'Alpha (α)': {
            'particle':     'Helium nucleus (2p + 2n)',
            'charge':       '+2',
            'penetration':  'Few cm in air, stopped by paper/skin',
            'ionization':   'High (dangerous if inhaled/ingested)',
            'shielding':    'Paper, thin aluminum'
        },
        'Beta (β)': {
            'particle':     'Electron (β⁻) or positron (β⁺)',
            'charge':       '-1 or +1',
            'penetration':  'Meters in air, mm in tissue',
            'ionization':   'Medium',
            'shielding':    'Plastic, aluminum (avoid lead — bremsstrahlung)'
        },
        'Gamma (γ)': {
            'particle':     'High energy photon',
            'charge':       '0',
            'penetration':  'Very penetrating — cm of lead to stop',
            'ionization':   'Low per unit length but deep penetration',
            'shielding':    'Lead, thick concrete'
        },
        'Neutron (n)': {
            'particle':     'Neutral hadron',
            'charge':       '0',
            'penetration':  'Very penetrating',
            'ionization':   'Indirect (activate nuclei)',
            'shielding':    'Water, polyethylene (hydrogen-rich)'
        }
    }

def radiation_dose():
    return {
        'Activity':     'A = λN (Bq = decays/second)',
        'Exposure':     'Charge created in air per unit mass (C/kg)',
        'Absorbed dose':'D = energy deposited/mass (Gray: 1 Gy = 1 J/kg)',
        'Equivalent dose':'H = D × wR (Sievert: Sv)',
        'Effective dose':'E = Σ wT × HT (accounts for organ sensitivity)',
        'wR factors': {
            'X-ray/gamma/beta': 1,
            'Protons':          2,
            'Neutrons':         '5-20 (energy dependent)',
            'Alpha':            20
        },
        'Background radiation': '~3 mSv/year (natural)',
        'Chest X-ray':          '~0.1 mSv',
        'CT scan':              '~10 mSv',
        'Annual limit (workers)': '20 mSv/year'
    }
```

---

## Nuclear Applications
```
Nuclear Power:
  ~10% of world electricity from nuclear
  ~440 reactors worldwide
  Types: PWR, BWR, CANDU, AGR, RBMK

Nuclear Medicine:
  PET scan: ¹⁸F-FDG (positron emission)
  SPECT: ⁹⁹ᵐTc (gamma emission, 6 hr half-life)
  Therapy: ¹³¹I (thyroid cancer), ⁹⁰Y (cancer treatment)
  Bone scans, cardiac imaging, brain studies

Radiation Therapy:
  External beam: X-rays, gamma rays, proton therapy
  Brachytherapy: radioactive seeds implanted in tumor
  Proton therapy: Bragg peak — dose deposited at specific depth

Nuclear Dating:
  ¹⁴C dating: t₁/₂ = 5730 yr (up to ~50,000 years)
  U-Pb dating: t₁/₂ = 4.47 Gyr (geological timescales)
  K-Ar dating: t₁/₂ = 1.25 Gyr

Food irradiation:
  Kills bacteria, extends shelf life
  Does NOT make food radioactive

Smoke detectors:
  ²⁴¹Am ionizes air — smoke disrupts ion current
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Confusing activity and dose | Activity = decays/sec, dose = energy deposited in tissue |
| Mass number changes in beta decay | A unchanged in β decay, only Z changes |
| Q-value sign | Q > 0 means energy released (exothermic) |
| Fission vs fusion confusion | Fission: heavy splits, Fusion: light combines — both release energy |
| Half-life vs mean lifetime | τ = t₁/₂/ln2 = 1.443 × t₁/₂ |
| Nuclear vs atomic mass | Use atomic masses consistently in Q-value calculations |

---

## Key Constants & Data
```
1 u = 931.494 MeV/c² = 1.661×10⁻²⁷ kg
mp = 1.007276 u
mn = 1.008665 u
me = 0.000549 u
1 fm = 10⁻¹⁵ m
R₀ = 1.2 fm
NA = 6.022×10²³ /mol
1 barn = 10⁻²⁸ m²
```

---

## Related Skills

- **particle-physics-expert**: Quark structure of nucleons
- **quantum-mechanics-expert**: Quantum tunneling in alpha decay
- **thermodynamics-expert**: Nuclear reactor thermodynamics
- **plasma-physics-expert**: Fusion plasma confinement
- **nuclear-energy-expert**: Reactor design and safety
