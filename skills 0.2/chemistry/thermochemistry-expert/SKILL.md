---
name: thermochemistry-expert
description: Expert-level thermochemistry knowledge. Use when working with enthalpy, calorimetry, Hess's law, bond energies, heat of formation, heat of combustion, heat capacity, thermodynamic cycles, or reaction energetics. Also use when the user mentions 'enthalpy', 'Hess law', 'calorimetry', 'heat of formation', 'heat of combustion', 'bond energy', 'specific heat', 'calorimeter', 'endothermic', 'exothermic', 'standard state', or 'thermodynamic cycle'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Thermochemistry Expert

You are a world-class thermochemist with deep expertise in reaction energetics, calorimetry, Hess's law, thermodynamic cycles, bond energies, standard enthalpies, and the relationship between heat, work, and chemical change.

## Before Starting

1. **Topic** — Enthalpy, calorimetry, Hess's law, bond energies, or thermodynamic cycles?
2. **Level** — High school, undergraduate, or graduate?
3. **Goal** — Calculate ΔH, design experiment, or understand concept?
4. **Context** — Chemical reactions, combustion, biological, or materials?
5. **Data available** — Formation enthalpies, bond energies, or calorimetry data?

---

## Core Expertise Areas

- **First Law**: internal energy, enthalpy, heat and work
- **Calorimetry**: bomb calorimeter, coffee cup calorimeter, DSC
- **Hess's Law**: thermodynamic cycles, path independence
- **Standard Enthalpies**: formation, combustion, reaction
- **Bond Energies**: average bond enthalpies, estimation
- **Kirchhoff's Law**: temperature dependence of ΔH
- **Thermodynamic Cycles**: Born-Haber, Kapustinskii
- **Heat Capacity**: Cp, Cv, Dulong-Petit, Debye, Einstein

---

## First Law & Enthalpy
```
First Law of Thermodynamics:
  ΔU = q + w  (internal energy change)
  q = heat transferred to system (+q = heat absorbed)
  w = work done on system (+w = work done on system)

Work types:
  Expansion work: w = -PextΔV  (work done BY system)
  At constant P: w = -PΔV = -ΔnRgasT  (ideal gas)
  Non-expansion work: electrical, surface tension, etc.

Enthalpy:
  H = U + PV
  ΔH = ΔU + Δ(PV) = ΔU + ΔngasRT  (ideal gas, const P)
  At constant P: ΔH = qp  (enthalpy = heat at const pressure)
  At constant V: ΔU = qv  (bomb calorimeter)

Relationship:
  ΔH = ΔU + ΔngasRT
  Δngas = moles gaseous products - moles gaseous reactants
  If Δngas = 0: ΔH ≈ ΔU
  Typical difference: Δngas × 2.5 kJ/mol at 25°C

Sign conventions:
  Exothermic reaction: ΔH < 0  (releases heat to surroundings)
  Endothermic reaction: ΔH > 0  (absorbs heat from surroundings)
  System: the reaction mixture
  Surroundings: everything else (calorimeter, environment)
```

---

## Calorimetry
```python
def coffee_cup_calorimeter(mass_solution, specific_heat,
                            T_initial, T_final,
                            moles_reaction):
    """
    Constant pressure calorimeter (open to atmosphere).
    Assumes solution density ≈ water, Cp(solution) ≈ Cp(water)
    """
    Cp_water = 4.184  # J/g·K
    if specific_heat is None:
        specific_heat = Cp_water

    q_solution = mass_solution * specific_heat * (T_final - T_initial)
    q_reaction  = -q_solution  # heat lost by reaction = heat gained by solution
    delta_H     = q_reaction / moles_reaction  # J/mol

    return {
        'q_solution':   round(q_solution, 2),
        'q_reaction':   round(q_reaction, 2),
        'delta_H_rxn':  round(delta_H, 2),
        'delta_H_kJ':   round(delta_H/1000, 3),
        'sign':         'Exothermic (ΔH < 0)' if delta_H < 0 else 'Endothermic (ΔH > 0)'
    }

def bomb_calorimeter(T_initial, T_final, Ccal,
                      mass_sample, molar_mass):
    """
    Constant volume calorimeter.
    Ccal = heat capacity of calorimeter (J/K or kJ/K)
    Measures qv = ΔU (not ΔH directly)
    """
    delta_T     = T_final - T_initial
    q_cal       = Ccal * delta_T  # heat absorbed by calorimeter
    q_rxn       = -q_cal          # heat released by reaction
    moles       = mass_sample / molar_mass
    delta_U     = q_rxn / moles   # internal energy per mole

    return {
        'delta_T':      round(delta_T, 4),
        'q_reaction':   round(q_rxn, 2),
        'delta_U_mol':  round(delta_U, 2),
        'delta_U_kJ':   round(delta_U/1000, 3),
        'note':         'ΔH = ΔU + ΔngasRT to convert to enthalpy'
    }

def dsc_analysis():
    """
    Differential Scanning Calorimetry.
    Measures heat flow vs temperature.
    """
    return {
        'principle':    'Compare heat flow to sample vs reference',
        'heat_flow':    'dH/dt = Cp × dT/dt  (W)',
        'peak_area':    'ΔH = ∫(heat flow)dt  (enthalpy of transition)',
        'Tg':           'Step change in Cp (glass transition)',
        'Tm':           'Endothermic peak (melting)',
        'Tc':           'Exothermic peak (crystallization, on cooling)',
        'denaturation': 'Protein unfolding: endothermic peak',
        'calibration':  'Use indium (Tm = 156.6°C, ΔHf = 28.45 J/g)'
    }
```

---

## Hess's Law
```
Hess's Law:
  Enthalpy is a state function — path independent.
  ΔH_rxn = Σ ΔH_steps  (regardless of how you get there)

Rules for manipulating reactions:
  1. If reaction reversed: ΔH changes sign
     A → B, ΔH = +50 kJ
     B → A, ΔH = -50 kJ

  2. If reaction multiplied by n: ΔH multiplied by n
     2A → 2B, ΔH = +100 kJ

  3. Add reactions: add ΔH values
     Species appearing on both sides cancel

Example — Formation of CO₂:
  Target: C(s) + O₂(g) → CO₂(g)  ΔH = ?

  Given:
  (1) C(s) + ½O₂(g) → CO(g)      ΔH₁ = -110.5 kJ
  (2) CO(g) + ½O₂(g) → CO₂(g)   ΔH₂ = -283.0 kJ

  Add (1) + (2):
  C(s) + O₂(g) → CO₂(g)   ΔH = -393.5 kJ ✓

Standard enthalpy of reaction:
  ΔrH° = Σ nᵢΔfH°(products) - Σ nⱼΔfH°(reactants)
  Standard state: pure substance at 1 bar, 25°C (298.15 K)
  ΔfH°(element in standard state) = 0 by definition
  Examples: ΔfH°(H₂O,l) = -285.8 kJ/mol
            ΔfH°(CO₂,g)  = -393.5 kJ/mol
            ΔfH°(NH₃,g)  = -46.1 kJ/mol
```

---

## Standard Enthalpies
```python
def standard_enthalpies_database():
    return {
        'Formation ΔfH° (kJ/mol) at 298K': {
            'H₂O(l)':    -285.8,
            'H₂O(g)':    -241.8,
            'CO₂(g)':    -393.5,
            'CO(g)':     -110.5,
            'NH₃(g)':    -46.1,
            'NO(g)':     +90.3,
            'NO₂(g)':    +33.2,
            'SO₂(g)':    -296.8,
            'SO₃(g)':    -395.7,
            'HCl(g)':    -92.3,
            'HF(g)':     -271.1,
            'CH₄(g)':    -74.8,
            'C₂H₄(g)':   +52.5,
            'C₂H₆(g)':   -84.7,
            'C₆H₆(l)':   +49.0,
            'C₆H₁₂O₆(s)':-1274.5,
            'NaCl(s)':   -411.2,
            'CaO(s)':    -635.1,
            'CaCO₃(s)':  -1207.6,
            'Fe₂O₃(s)':  -824.2,
            'Al₂O₃(s)':  -1676.0
        },
        'Combustion ΔcH° (kJ/mol)': {
            'H₂(g)':     -285.8,
            'C(graphite)':-393.5,
            'CH₄(g)':    -890.3,
            'C₂H₆(g)':   -1559.7,
            'C₃H₈(g)':   -2219.2,
            'C₈H₁₈(l)':  -5471.0,
            'C₆H₆(l)':   -3267.6,
            'Glucose':   -2803.0,
            'Sucrose':   -5644.0,
            'Ethanol':   -1366.8
        }
    }

def reaction_enthalpy(reactants, products, hf_data):
    """
    Calculate ΔrH° from standard enthalpies of formation.
    reactants/products: dict of {formula: stoichiometric_coefficient}
    """
    delta_H = 0
    for compound, coeff in products.items():
        delta_H += coeff * hf_data.get(compound, 0)
    for compound, coeff in reactants.items():
        delta_H -= coeff * hf_data.get(compound, 0)
    return round(delta_H, 2)
```

---

## Bond Energies
```
Average bond enthalpy:
  Energy required to break 1 mol of bonds in gaseous molecules
  Always positive (breaking bonds requires energy)
  Approximate: bonds are similar in different molecules but not identical

Estimating ΔH from bond energies:
  ΔH ≈ Σ(bonds broken) - Σ(bonds formed)
  = Σ BE(reactant bonds) - Σ BE(product bonds)

Average bond enthalpies (kJ/mol):
  H-H:   436    C-H:   413    N-H:   391
  O-H:   463    S-H:   338    F-H:   567
  Cl-H:  432    Br-H:  366    I-H:   297
  C-C:   347    C=C:   614    C≡C:   839
  C-N:   305    C=N:   615    C≡N:   891
  C-O:   358    C=O:   745    C≡O:   1072
  N-N:   163    N=N:   418    N≡N:   945
  O-O:   157    O=O:   498
  C-F:   485    C-Cl:  339    C-Br:  285
  Si-O:  368    P-O:   360    S=O:   523

Example: combustion of methane
  CH₄ + 2O₂ → CO₂ + 2H₂O
  Bonds broken: 4(C-H) + 2(O=O) = 4(413) + 2(498) = 2648 kJ
  Bonds formed: 2(C=O) + 4(O-H) = 2(745) + 4(463) = 3342 kJ
  ΔH ≈ 2648 - 3342 = -694 kJ/mol
  (Actual: -890 kJ/mol — bond energies are averages, less accurate)

Limitations:
  Average values — actual bond strength varies with molecular context
  Only works for gas phase reactions (no condensation energies)
  For more accurate results: use standard enthalpies of formation
```

---

## Kirchhoff's Law
```
Temperature dependence of ΔH:
  ΔH(T₂) = ΔH(T₁) + ∫[T₁ to T₂] ΔCp dT

  ΔCp = Σ nᵢCp,i(products) - Σ nⱼCp,j(reactants)

If ΔCp ≈ constant:
  ΔH(T₂) = ΔH(T₁) + ΔCp(T₂ - T₁)

Heat capacity polynomial (Shomate equation):
  Cp = A + BT + CT² + DT³ + E/T²  (J/mol·K)
  Tabulated in NIST WebBook

Integrated form:
  H(T) - H(298) = AT + BT²/2 + CT³/3 + DT⁴/4 - E/T + F - H
  S(T) = A·lnT + BT + CT²/2 + DT³/3 - E/(2T²) + G

Example: ΔcH°(CH₄) at 1000 K vs 298 K
  Need Cp(CH₄,g), Cp(O₂,g), Cp(CO₂,g), Cp(H₂O,g)
  ΔCp = 2Cp(H₂O) + Cp(CO₂) - Cp(CH₄) - 2Cp(O₂)
  Integrate from 298 to 1000 K
  Combustion is more exothermic at higher T if ΔCp > 0
```

---

## Thermodynamic Cycles
```
Born-Haber cycle (lattice energy):
  Calculate lattice energy (ΔHL) from Hess's law
  NaCl formation cycle:
    Na(s) → Na(g)                  ΔHsub = +108 kJ/mol  (sublimation)
    Na(g) → Na⁺(g) + e⁻           IE₁ = +496 kJ/mol    (ionization)
    ½Cl₂(g) → Cl(g)               ½D = +121 kJ/mol      (dissociation)
    Cl(g) + e⁻ → Cl⁻(g)           EA = -349 kJ/mol      (electron affinity)
    Na⁺(g) + Cl⁻(g) → NaCl(s)    ΔHL = ?               (lattice energy)
    Na(s) + ½Cl₂(g) → NaCl(s)    ΔfH° = -411 kJ/mol   (formation)

  Hess: ΔfH° = ΔHsub + IE₁ + ½D + EA + ΔHL
  ΔHL = ΔfH° - ΔHsub - IE₁ - ½D - EA
  ΔHL = -411 - 108 - 496 - 121 - (-349) = -787 kJ/mol

Kapustinskii equation (estimate lattice energy):
  ΔHL = -1214.4·ν·z⁺·z⁻/(r⁺ + r⁻)  [kJ/mol]
  ν = number of ions per formula unit
  z = ionic charges, r = ionic radii (pm)

Hydration cycle:
  ΔHsoln = ΔHL + ΔHhyd(cation) + ΔHhyd(anion)
  If ΔHsoln < 0: dissolution exothermic (NaOH)
  If ΔHsoln > 0: dissolution endothermic (NH₄NO₃, KNO₃)
  Even endothermic dissolution can be spontaneous if ΔSsoln > 0
```

---

## Heat Capacity
```python
def heat_capacity_models():
    return {
        'Classical (Dulong-Petit)': {
            'Cv':   '3R = 24.9 J/mol·K  (per mole atoms in solid)',
            'valid': 'High temperature only',
            'fails': 'At low T, Cv → 0 (quantum effect)'
        },
        'Einstein model': {
            'Cv':   '3R·(θE/T)²·exp(θE/T)/(exp(θE/T)-1)²',
            'θE':   'Einstein temperature = ℏωE/kB',
            'high_T':'→ 3R (Dulong-Petit)',
            'low_T': '→ 0 exponentially (too fast)',
            'use':   'Optical phonon modes'
        },
        'Debye model': {
            'Cv':   '9R(T/θD)³∫₀^(θD/T) x⁴eˣ/(eˣ-1)² dx',
            'θD':   'Debye temperature (ranges 100-2000 K)',
            'T3':   'Cv ∝ T³ at low T (Debye T³ law)',
            'high_T':'→ 3R (Dulong-Petit)',
            'use':   'Acoustic phonon modes, better at low T'
        },
        'Monatomic ideal gas': {
            'Cv':   '3/2 R = 12.47 J/mol·K',
            'Cp':   'Cv + R = 5/2 R = 20.79 J/mol·K',
            'γ':    'Cp/Cv = 5/3 = 1.667'
        },
        'Diatomic ideal gas (high T)': {
            'Cv':   '5/2 R (trans + rot)',
            'Cp':   '7/2 R',
            'γ':    'Cp/Cv = 7/5 = 1.4'
        }
    }

def specific_heats():
    return {
        'Water (l)':   4.184,   # J/g·K
        'Water (s)':   2.09,
        'Water (g)':   2.01,
        'Aluminum':    0.900,
        'Iron':        0.449,
        'Copper':      0.385,
        'Gold':        0.129,
        'Lead':        0.128,
        'Ethanol':     2.44,
        'Glass':       0.84,
        'Air':         1.01,
        'Note':        'Units: J/g·K or kJ/kg·K'
    }
```

---

## Combustion Calorimetry
```python
def combustion_analysis(compound, molecular_formula, delta_c_H):
    """
    Combustion analysis and energy content.
    delta_c_H: standard enthalpy of combustion (kJ/mol)
    """
    # Parse molecular formula (simple implementation)
    import re
    elements = {'C': 12.011, 'H': 1.008, 'O': 15.999,
                'N': 14.007, 'S': 32.06}

    # Energy per gram
    molar_mass = sum(count * elements[elem]
                     for elem, count in
                     [('C', molecular_formula.get('C', 0)),
                      ('H', molecular_formula.get('H', 0)),
                      ('O', molecular_formula.get('O', 0))])

    energy_per_gram = abs(delta_c_H) / molar_mass  # kJ/g
    energy_per_gram_kcal = energy_per_gram / 4.184   # kcal/g

    return {
        'compound':         compound,
        'delta_c_H':        delta_c_H,
        'molar_mass':       round(molar_mass, 2),
        'energy_kJ_g':      round(energy_per_gram, 2),
        'energy_kcal_g':    round(energy_per_gram_kcal, 2),
        'comparison': {
            'gasoline':     '~47 kJ/g',
            'natural_gas':  '~55 kJ/g',
            'coal':         '~30 kJ/g',
            'H₂':           '~142 kJ/g',
            'glucose':      '~15.7 kJ/g',
            'fat':          '~37 kJ/g (9 kcal/g)',
            'protein':      '~17 kJ/g (4 kcal/g)',
            'carbohydrate': '~17 kJ/g (4 kcal/g)'
        }
    }
```

---

## Adiabatic Flame Temperature
```python
def adiabatic_flame_temp(delta_H_rxn, reactant_Cp_total,
                          n_products, product_Cp_total,
                          T_initial=298):
    """
    Estimate adiabatic flame temperature.
    Heat released = heat absorbed by products
    -ΔH_rxn = n_products × Cp_products × ΔT
    """
    if delta_H_rxn >= 0:
        return 'Endothermic reaction — no flame'

    heat_released = abs(delta_H_rxn)  # kJ/mol fuel
    delta_T = heat_released / (n_products * product_Cp_total)
    T_adiabatic = T_initial + delta_T

    return {
        'heat_released_kJ':     round(heat_released, 1),
        'delta_T':              round(delta_T, 1),
        'T_adiabatic_K':        round(T_adiabatic, 1),
        'T_adiabatic_C':        round(T_adiabatic - 273.15, 1),
        'note': 'Actual flame T lower due to heat losses and incomplete combustion'
    }

# Example flame temperatures:
# Methane/air:   ~2230 K
# Methane/O₂:    ~3054 K
# H₂/O₂:        ~3080 K
# Acetylene/O₂:  ~3480 K (hottest common flame)
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Sign confusion for q | q_rxn = -q_calorimeter (equal and opposite) |
| ΔH vs ΔU from bomb calorimeter | Bomb gives ΔU; convert: ΔH = ΔU + ΔngasRT |
| ΔfH°(element) ≠ 0 | Only for element in its STANDARD STATE at 25°C, 1 bar |
| Bond energy equation direction | ΔH = bonds broken - bonds formed (not formed - broken) |
| Hess's law sign errors | Reversed reaction → opposite sign; check all signs carefully |
| Specific heat vs molar heat capacity | Cp(specific) in J/g·K; Cp(molar) in J/mol·K |

---

## Related Skills

- **physical-chemistry-expert**: Full chemical thermodynamics
- **thermodynamics-expert**: Physics thermodynamics foundation
- **analytical-chemistry-expert**: Calorimetric measurement methods
- **biochemistry-expert**: Bioenergetics and metabolic thermochemistry
- **inorganic-chemistry-expert**: Born-Haber cycles, lattice energies
