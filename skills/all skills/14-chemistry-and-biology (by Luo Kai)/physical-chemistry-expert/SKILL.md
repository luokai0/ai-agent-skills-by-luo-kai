---
author: luo-kai
name: physical-chemistry-expert
description: Expert-level physical chemistry knowledge. Use when working with thermodynamics, chemical kinetics, quantum chemistry, statistical mechanics, spectroscopy, electrochemistry, or surface chemistry. Also use when the user mentions 'Gibbs energy', 'equilibrium constant', 'reaction kinetics', 'rate law', 'activation energy', 'Arrhenius', 'partition function', 'Schrodinger equation', 'molecular orbital', 'electrochemistry', 'Nernst equation', or 'surface adsorption'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Physical Chemistry Expert

You are a world-class physical chemist with deep expertise in chemical thermodynamics, kinetics, quantum chemistry, statistical mechanics, spectroscopy, electrochemistry, and the mathematical framework underlying chemical phenomena.

## Before Starting

1. **Topic** — Thermodynamics, kinetics, quantum chemistry, spectroscopy, or electrochemistry?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Solve problem, derive equation, or understand concept?
4. **Context** — Chemical equilibrium, reaction rates, molecular structure, or surfaces?
5. **Math level** — Algebra, calculus, or differential equations?

---

## Core Expertise Areas

- **Chemical Thermodynamics**: Gibbs energy, equilibrium, phase equilibria
- **Chemical Kinetics**: rate laws, mechanisms, transition state theory
- **Quantum Chemistry**: molecular orbitals, Hartree-Fock, DFT
- **Statistical Mechanics**: partition functions, Boltzmann distribution
- **Molecular Spectroscopy**: rotational, vibrational, electronic spectra
- **Electrochemistry**: electrode potentials, Nernst equation, kinetics
- **Surface Chemistry**: adsorption isotherms, catalysis, surface reactions
- **Transport Phenomena**: diffusion, viscosity, thermal conductivity

---

## Chemical Thermodynamics
```
Fundamental relations:
  dU = TdS - PdV + Σμᵢdnᵢ
  dH = TdS + VdP + Σμᵢdnᵢ
  dA = -SdT - PdV + Σμᵢdnᵢ
  dG = -SdT + VdP + Σμᵢdnᵢ

Maxwell relations:
  (∂T/∂V)S = -(∂P/∂S)V
  (∂T/∂P)S = (∂V/∂S)P
  (∂S/∂V)T = (∂P/∂T)V
  (∂S/∂P)T = -(∂V/∂T)P

Chemical potential:
  μᵢ = (∂G/∂nᵢ)T,P,nⱼ
  μ = μ° + RT·ln(a)  (activity a)
  Ideal gas: μ = μ° + RT·ln(P/P°)
  Solution: μ = μ° + RT·ln(x)  (Raoult)

Gibbs energy of reaction:
  ΔrG = ΔrG° + RT·ln(Q)
  At equilibrium: ΔrG = 0 → ΔrG° = -RT·ln(K)
  K = exp(-ΔrG°/RT)

Temperature dependence:
  Van't Hoff: d(lnK)/dT = ΔrH°/RT²
  Integration: ln(K₂/K₁) = -ΔrH°/R · (1/T₂ - 1/T₁)
  Exothermic: K decreases with T
  Endothermic: K increases with T

Gibbs-Helmholtz:
  (∂(G/T)/∂T)P = -H/T²
  ΔG = ΔH - TΔS
  Spontaneous: ΔG < 0 at constant T, P
```

---

## Phase Equilibria
```
Chemical potential equality at equilibrium:
  μ(phase 1) = μ(phase 2)

Clausius-Clapeyron:
  dP/dT = ΔH_trs/(TΔV)
  Liquid-gas (ideal): d(lnP)/dT = ΔvapH/RT²
  → ln(P₂/P₁) = -(ΔvapH/R)(1/T₂ - 1/T₁)

Phase rule (Gibbs):
  F = C - P + 2
  F = degrees of freedom, C = components, P = phases
  Triple point: F = 1 - 3 + 2 = 0  (fixed T,P) ✓
  Two phases: F = 1  (specify T → P fixed)

Activity and fugacity:
  Real gas: μ = μ° + RT·ln(f/f°)
  f = γP  (γ → 1 as P → 0)
  Solution: aᵢ = γᵢxᵢ
  Ideal solution: aᵢ = xᵢ (Raoult's law, γᵢ = 1)

Colligative properties (dilute solutions):
  Boiling point elevation: ΔTb = Kb·m  (Kb = ebullioscopic constant)
  Freezing point depression: ΔTf = Kf·m  (Kf = cryoscopic constant)
  Osmotic pressure: Π = MRT  (M = molarity)
  Vapor pressure lowering: ΔP = xsolute·P*

Raoult's law: P_total = Σ xᵢPᵢ*  (ideal solution)
Henry's law: P = KH·x  (dilute solute, different constant)
```

---

## Chemical Kinetics
```
Rate law:
  Rate = k[A]^m[B]^n...
  m, n = reaction orders (must be determined experimentally!)
  Overall order = m + n + ...

Integrated rate laws:
  Zero order: [A] = [A]₀ - kt
    t₁/₂ = [A]₀/2k

  First order: [A] = [A]₀e^(-kt)
    ln[A] = ln[A]₀ - kt
    t₁/₂ = ln2/k = 0.693/k

  Second order: 1/[A] = 1/[A]₀ + kt
    t₁/₂ = 1/(k[A]₀)

Temperature dependence (Arrhenius):
  k = A·exp(-Ea/RT)
  ln(k) = ln(A) - Ea/RT
  ln(k₂/k₁) = -(Ea/R)(1/T₂ - 1/T₁)
  Ea = activation energy (J/mol)
  A = pre-exponential/frequency factor
  Rule of thumb: rate doubles for each 10°C rise (∼50 kJ/mol Ea)

Transition State Theory (Eyring):
  k = (kBT/h)·exp(-ΔG‡/RT) = (kBT/h)·K‡
  ΔG‡ = ΔH‡ - TΔS‡
  ΔH‡ ≈ Ea - RT  (small difference)
  Entropy of activation: negative for bimolecular (more ordered TS)

Steady-state approximation:
  d[intermediate]/dt ≈ 0  (intermediate concentration constant)
  Applies when intermediate is short-lived

Pre-equilibrium approximation:
  Fast equilibrium before slow step
  K = k₁/k₋₁  (rapid equilibrium)
  Rate = k₂·K·[A][B]  (overall rate)

Michaelis-Menten (enzyme kinetics):
  E + S ⇌ ES → E + P
  v = Vmax[S]/(Km + [S])
  Km = (k₋₁ + k₂)/k₁  (Michaelis constant)
  Lineweaver-Burk: 1/v = Km/Vmax · 1/[S] + 1/Vmax
```

---

## Quantum Chemistry
```
Born-Oppenheimer approximation:
  Separate nuclear and electronic motion.
  Electronic Schrodinger: Ĥelψel = Eelψel
  Nuclei move on potential energy surface (PES).

Hartree-Fock (HF) theory:
  Each electron moves in average field of all others.
  Ĥ_HF ψᵢ = εᵢψᵢ  (eigenvalue equation)
  HF energy: E_HF = Σεᵢ - Σ(Jᵢⱼ - Kᵢⱼ)/2
  Correlation energy: E_corr = E_exact - E_HF  (missing in HF)

Post-HF methods:
  MP2: Møller-Plesset 2nd order perturbation
  CISD: Configuration interaction singles and doubles
  CCSD(T): gold standard for accuracy
  Cost: HF (N⁴), MP2 (N⁵), CCSD(T) (N⁷)

Density Functional Theory (DFT):
  Hohenberg-Kohn: E is functional of electron density ρ(r)
  E[ρ] = T[ρ] + Vne[ρ] + J[ρ] + Exc[ρ]
  Exc = exchange-correlation functional (approximated)
  Kohn-Sham: solve HF-like equations with effective potential
  Cost: N³ (formally), very popular for large molecules
  Functionals: B3LYP, PBE, M06, ωB97X-D

Basis sets:
  Minimal: STO-3G (one basis function per orbital)
  Split-valence: 6-31G, 6-311G
  Polarization: 6-31G*, 6-31G** (adds d on heavy atoms, p on H)
  Diffuse: 6-31+G* (adds diffuse functions for anions, lone pairs)
  Correlation consistent: cc-pVDZ, cc-pVTZ, cc-pVQZ (for correlated methods)
```

---

## Statistical Mechanics
```
Boltzmann distribution:
  Pᵢ = exp(-εᵢ/kBT) / q
  q = molecular partition function = Σᵢ exp(-εᵢ/kBT)

Partition function factorization:
  q = qtrans · qrot · qvib · qelec

Translational:
  qtrans = V(2πmkBT/h²)^(3/2)  (particle in 3D box)
  Thermal de Broglie wavelength: Λ = h/√(2πmkBT)

Rotational (linear molecule):
  qrot = T/σΘrot  (high T limit)
  Θrot = ℏ²/2IkB  (characteristic temperature)
  σ = symmetry number (1 for HCl, 2 for H₂, O₂)

Vibrational:
  qvib = 1/(1-exp(-hν/kBT))  (harmonic oscillator, per mode)
  Θvib = hν/kB  (characteristic temperature)
  High T limit: qvib → kBT/hν

Electronic:
  qelec = g₀ (usually ground state degeneracy only)

Thermodynamic properties from q:
  A = -NkBT(ln q - ln N + 1)  (Helmholtz)
  U = NkBT² (∂lnq/∂T)V
  S = NkB[ln q - ln N + 1 + T(∂lnq/∂T)V]
  Cv = (∂U/∂T)V

Heat capacities:
  Translation: (3/2)R per mole
  Rotation: R (linear), (3/2)R (nonlinear)
  Vibration: R per mode (high T) → 0 (low T, quantum frozen out)
  Equipartition: (1/2)R per quadratic term

Canonical ensemble:
  Q = Σ_states exp(-E_total/kBT)
  For N identical molecules: Q = qN/N! (distinguishable/N!)
  Grand canonical, microcanonical, isothermal-isobaric: other ensembles
```

---

## Molecular Spectroscopy
```python
def spectroscopy_selection_rules():
    return {
        'Microwave (rotational)': {
            'condition':    'Permanent dipole moment required',
            'selection':    'ΔJ = ±1',
            'spacing':      'B = h/8π²Ic, lines equally spaced at 2B',
            'info':         'Molecular geometry, bond lengths',
            'example':      'HCl: lines at 2B intervals'
        },
        'IR (vibrational)': {
            'condition':    'Change in dipole moment during vibration',
            'selection':    'Δv = ±1 (harmonic), Δv = ±2,±3... (overtones)',
            'fundamentals': '3N-6 modes (nonlinear), 3N-5 (linear)',
            'info':         'Functional groups, force constants',
            'example':      'CO₂: 4 modes, 2 IR active (asymm stretch, bends)'
        },
        'Raman': {
            'condition':    'Change in polarizability during vibration',
            'selection':    'Δv = ±1',
            'complement':   'Often complementary to IR (mutual exclusion for centrosymmetric)',
            'info':         'Symmetric stretches, ring breathing modes'
        },
        'UV-Vis (electronic)': {
            'selection':    'ΔS = 0 (spin allowed), Laporte: Δl = ±1',
            'transitions':  'σ→σ*, n→σ*, π→π*, n→π*, d→d, charge transfer',
            'Beer-Lambert': 'A = εlc  (absorbance = ε × path × concentration)',
            'info':         'Electronic structure, conjugation'
        },
        'NMR': {
            'condition':    'Spin ½ nuclei in magnetic field: ¹H, ¹³C, ¹⁵N, ³¹P',
            'selection':    'ΔmI = ±1',
            'frequency':    'ν = γB₀/2π  (Larmor frequency)',
            'info':         'Chemical environment, connectivity, 3D structure'
        }
    }

def spectroscopic_constants():
    return {
        'Vibrational frequency': 'ν̃ = (1/2πc)√(k/μ)  (k=force constant, μ=reduced mass)',
        'Rotational constant':   'B = ℏ/4πcI  (I=moment of inertia)',
        'Beer-Lambert':          'A = εlc = log(I₀/I)',
        'Einstein coefficients': 'Aᵢⱼ (spontaneous emission), Bᵢⱼ (stimulated)',
        'Franck-Condon':         'Intensity ∝ |⟨v′|v⟩|²  (overlap of vibrational wavefunctions)'
    }
```

---

## Electrochemistry
```
Standard electrode potential:
  Half-reaction: Ox + ne⁻ → Red  (E°)
  Standard: 25°C, 1 M concentration, 1 atm
  SHE (standard hydrogen electrode): 2H⁺ + 2e⁻ → H₂, E° = 0.000 V

EMF of cell:
  E_cell = E_cathode - E_anode
  Spontaneous: E_cell > 0 → ΔG < 0
  ΔG° = -nFE°  (n = electrons transferred, F = 96485 C/mol)
  K = exp(nFE°/RT)

Nernst equation:
  E = E° - (RT/nF)ln(Q)
  E = E° - (0.05916/n)log(Q)  at 25°C
  At equilibrium: E = 0, Q = K

Concentration cells:
  Both electrodes same material, different concentrations
  E = (RT/nF)ln(c₂/c₁)

pH measurement:
  Glass electrode: E = const - 0.05916·pH  at 25°C

Butler-Volmer equation:
  i = i₀[exp(αnFη/RT) - exp(-(1-α)nFη/RT)]
  η = E - Eeq (overpotential)
  i₀ = exchange current density
  α = transfer coefficient (~0.5)
  Large anodic η: i ≈ i₀exp(αnFη/RT)  (Tafel equation)

Electrolysis:
  Faraday's laws: m = MIt/nF  (mass deposited)
  Decomposition voltage: E_min = E_cell + overpotentials

Common standard potentials (E°/V):
  Li⁺/Li: -3.04  Na⁺/Na: -2.71  Zn²⁺/Zn: -0.76
  Fe²⁺/Fe: -0.44  H⁺/H₂: 0.00   Cu²⁺/Cu: +0.34
  O₂/H₂O: +1.23   Cl₂/Cl⁻: +1.36  F₂/F⁻: +2.87
```

---

## Surface Chemistry
```
Adsorption:
  Physisorption: van der Waals, weak, reversible, multilayer possible
  Chemisorption: chemical bonds, strong, irreversible, monolayer

Langmuir isotherm:
  θ = KP/(1+KP)
  θ = fractional coverage, K = adsorption constant, P = pressure
  Linearized: P/θ = P + 1/K
  Assumptions: monolayer, equivalent sites, no lateral interactions

BET isotherm (Brunauer-Emmett-Teller):
  Extends Langmuir to multilayer
  Used to measure surface area: SA = nmNA·σ
  P/(n(P*-P)) = 1/nm·c + (c-1)/nm·c · P/P*

Freundlich isotherm (heterogeneous surfaces):
  θ = KP^(1/n)  (empirical)
  log(θ) = log(K) + (1/n)log(P)

Catalysis:
  Catalyst lowers activation energy, increases rate
  Not consumed overall
  Langmuir-Hinshelwood: both reactants adsorb, react on surface
  Eley-Rideal: one adsorbed, one from gas phase
  Sabatier principle: optimal catalyst binds neither too weak nor too strong
  Volcano plot: rate vs adsorption energy has maximum

Rates on surfaces:
  Rate = kₛ·θ_A·θ_B  (bimolecular surface reaction)
  TPD (temperature-programmed desorption): measure Ea_des
  LEED: surface structure determination
```

---

## Transport Properties
```
Diffusion (Fick's laws):
  First: J = -D·(dc/dx)  (flux proportional to gradient)
  Second: ∂c/∂t = D·∂²c/∂x²
  D = kBT/6πηr  (Stokes-Einstein, sphere radius r)

Viscosity:
  Newton's law: τ = η·(dv/dy)  (shear stress)
  Ideal gas: η = (1/3)ρ⟨v⟩λ  (kinetic theory)
  η increases with T for gases (more collisions)
  η decreases with T for liquids (less intermolecular order)

Thermal conductivity:
  Fourier's law: q = -κ·(dT/dx)
  κ = (1/3)ρCv⟨v⟩λ  (kinetic theory)

Ionic conductivity:
  Λm = κ/c  (molar conductivity)
  Kohlrausch: Λm = Λ°m - K√c  (weak electrolytes)
  Λ°m = Σλ°±  (limiting molar conductivity, additive)
  Mobility: u = v/E (drift velocity per unit field)
  Λ = F(u₊+u₋)

Diffusion coefficient and mobility:
  D = ukBT/ze  (Einstein relation)
  D = RT/NA·ze·friction  (general)
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Confusing K and Kp | Kc uses concentrations, Kp uses partial pressures: Kp = Kc(RT)^Δn |
| Rate law from stoichiometry | Rate law must be determined experimentally, not from equation |
| Arrhenius T in Celsius | Always use Kelvin in Arrhenius equation |
| Nernst equation log vs ln | E = E° - (0.05916/n)log Q uses log₁₀ at 25°C |
| Partition function interpretation | q is NOT a probability — it is a sum of Boltzmann factors |
| Half-life for non-first-order | t₁/₂ depends on [A]₀ for zero and second order |

---

## Key Constants
```
R  = 8.314 J/mol·K
kB = 1.381×10⁻²³ J/K
h  = 6.626×10⁻³⁴ J·s
NA = 6.022×10²³ /mol
F  = 96485 C/mol
c  = 2.998×10⁸ m/s
RT at 25°C = 2.479 kJ/mol
kBT at 25°C = 0.02569 eV
```

---

## Related Skills

- **organic-chemistry-expert**: Reaction mechanisms and kinetics
- **inorganic-chemistry-expert**: Coordination chemistry thermodynamics
- **thermodynamics-expert**: Classical thermodynamics foundations
- **quantum-mechanics-expert**: Quantum basis of chemistry
- **statistical-mechanics**: Microscopic basis of thermodynamics
- **electrochemistry-expert**: Applied electrochemistry
