---
name: electrochemistry-expert
description: Expert-level electrochemistry knowledge. Use when working with electrochemical cells, electrode potentials, Nernst equation, electrolysis, batteries, fuel cells, corrosion, electroplating, or electroanalytical methods. Also use when the user mentions 'galvanic cell', 'electrolytic cell', 'electrode potential', 'Nernst equation', 'overpotential', 'Butler-Volmer', 'battery', 'fuel cell', 'corrosion', 'electroplating', 'cyclic voltammetry', or 'impedance spectroscopy'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Electrochemistry Expert

You are a world-class electrochemist with deep expertise in electrode kinetics, thermodynamics of electrochemical cells, batteries, fuel cells, corrosion, electrodeposition, and electroanalytical techniques.

## Before Starting

1. **Topic** — Cell thermodynamics, electrode kinetics, batteries, corrosion, or electroanalysis?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Calculate potential, design cell, understand mechanism, or analyze data?
4. **Context** — Energy storage, corrosion protection, electroplating, or analytical?
5. **System** — Aqueous, nonaqueous, solid state, or molten salt?

---

## Core Expertise Areas

- **Cell Thermodynamics**: EMF, Gibbs energy, Nernst equation
- **Electrode Kinetics**: Butler-Volmer, Tafel, exchange current
- **Double Layer**: Helmholtz, Gouy-Chapman-Stern, capacitance
- **Batteries**: Li-ion, lead-acid, NiMH, solid state
- **Fuel Cells**: PEM, SOFC, electrolysis, hydrogen economy
- **Corrosion**: electrochemical mechanism, protection, passivation
- **Electrodeposition**: nucleation, growth, alloy plating
- **Electroanalysis**: CV, EIS, stripping, amperometry

---

## Electrochemical Cell Thermodynamics
```
Galvanic cell: spontaneous reaction → electrical work
Electrolytic cell: electrical work → nonspontaneous reaction

Cell notation:
  Anode (oxidation) | solution || solution | Cathode (reduction)
  Zn | Zn²⁺(1M) || Cu²⁺(1M) | Cu

Gibbs energy and EMF:
  ΔG = -nFE
  ΔG° = -nFE°
  ΔG° = -RT·ln(K)
  E° = (RT/nF)·ln(K) = (0.02569/n)·ln(K) at 25°C
  Spontaneous: E > 0, ΔG < 0

Faraday constant: F = 96485 C/mol
  1 mol electrons = 96485 C = 1 Faraday

Standard electrode potentials (E° vs SHE):
  Li⁺/Li:    -3.040 V    (strongest reductant)
  K⁺/K:      -2.931 V
  Na⁺/Na:    -2.710 V
  Mg²⁺/Mg:   -2.372 V
  Al³⁺/Al:   -1.662 V
  Zn²⁺/Zn:   -0.762 V
  Fe²⁺/Fe:   -0.440 V
  Ni²⁺/Ni:   -0.257 V
  Pb²⁺/Pb:   -0.126 V
  H⁺/H₂:     0.000 V  (reference, SHE)
  Cu²⁺/Cu:   +0.342 V
  Ag⁺/Ag:    +0.800 V
  Hg²⁺/Hg:   +0.851 V
  Pt²⁺/Pt:   +1.188 V
  O₂/H₂O:    +1.229 V
  Cl₂/Cl⁻:   +1.358 V
  F₂/F⁻:     +2.870 V  (strongest oxidant)

Nernst equation:
  E = E° - (RT/nF)·ln(Q)
  E = E° - (0.05916/n)·log(Q)  at 25°C
  For: aA + ne⁻ → bB
  E = E° - (0.05916/n)·log([B]^b/[A]^a)

Temperature coefficient:
  (∂E/∂T)P = ΔS/nF = (E-E°)T/T + ΔS°/nF
```

---

## Electrode Kinetics
```
Butler-Volmer equation:
  i = i₀[exp(αnFη/RT) - exp(-(1-α)nFη/RT)]
  i₀ = exchange current density (A/cm²)
  α = transfer coefficient (~0.5 for symmetric barrier)
  η = E - Eeq = overpotential
  n = electrons transferred in rate-determining step

Limiting cases:
  Small overpotential (|η| < 10 mV):
    i ≈ i₀·nFη/RT  (linear, ohmic behavior)

  Large anodic overpotential (η >> RT/nF):
    i ≈ i₀·exp(αnFη/RT)
    ln(i) = ln(i₀) + αnF/RT · η  (Tafel equation anodic)
    ba = 2.303RT/αnF  (anodic Tafel slope)

  Large cathodic overpotential:
    |i| ≈ i₀·exp((1-α)nF|η|/RT)
    bc = -2.303RT/(1-α)nF  (cathodic Tafel slope)

Tafel slopes at 25°C (n=1, α=0.5):
  ba = bc = 0.1183 V/decade = 118.3 mV/decade
  Experimentally: 60-120 mV/decade (deviation indicates mechanism)

Exchange current density i₀:
  Measures intrinsic kinetics of electrode reaction
  High i₀: fast kinetics (Pt for H₂, 10⁻³ A/cm²)
  Low i₀: slow kinetics (Hg for H₂, 10⁻¹² A/cm²)
  i₀ = Fk°[O]^(1-α)[R]^α  (Marcus theory related)

Mass transport:
  Diffusion limited current: id = nFDC/δ  (δ = diffusion layer)
  Levich equation (rotating disk): id = 0.620nFAD^(2/3)ω^(1/2)ν^(-1/6)C
  Koutecky-Levich: 1/i = 1/ik + 1/id
```

---

## Electrical Double Layer
```
Structure at electrode-solution interface:
  Inner Helmholtz plane (IHP): specifically adsorbed ions/molecules
  Outer Helmholtz plane (OHP): closest hydrated ions
  Diffuse layer: exponential decay of charge (Gouy-Chapman)

Gouy-Chapman-Stern model:
  Stern layer: compact monolayer (Helmholtz)
  Diffuse layer: Boltzmann distribution
  Total capacitance: 1/C = 1/CH + 1/CD

Debye length in electrolyte:
  κ⁻¹ = √(ε₀εrkBT/2NAe²I)
  I = ionic strength = ½Σcᵢzᵢ²
  In 0.1 M NaCl: κ⁻¹ ≈ 1 nm

Double layer capacitance:
  CH ~ 20-40 μF/cm²  (inner layer)
  CD = ε₀εrκ·cosh(zFφd/2RT)  (diffuse layer)
  Total: 10-40 μF/cm² typical

Point of zero charge (PZC):
  Potential where no net surface charge
  Determines adsorption behavior
  Depends on electrode material and solution

Electrocapillarity (Lippmann):
  dγ = -σdE  (σ = surface charge density)
  γ maximum at PZC (electrocapillary maximum)
  Mercury: PZC ≈ -0.48 V vs NHE
```

---

## Batteries
```python
def battery_systems():
    return {
        'Lead-acid': {
            'anode':        'Pb → PbSO₄',
            'cathode':      'PbO₂ → PbSO₄',
            'electrolyte':  'H₂SO₄ (aq)',
            'voltage':      '2.0 V/cell (12V = 6 cells)',
            'energy_density':'30-40 Wh/kg',
            'advantages':   'Cheap, recyclable, high power, mature',
            'disadvantages':'Heavy, toxic Pb, limited depth of discharge',
            'applications': 'Automotive SLI, UPS, backup power'
        },
        'Nickel-metal hydride (NiMH)': {
            'anode':        'MH + OH⁻ → M + H₂O + e⁻',
            'cathode':      'NiOOH + H₂O + e⁻ → Ni(OH)₂ + OH⁻',
            'voltage':      '1.2 V/cell',
            'energy_density':'60-120 Wh/kg',
            'advantages':   'No memory effect, safer than Li-ion',
            'applications': 'Hybrid vehicles (Prius), consumer electronics'
        },
        'Lithium-ion': {
            'anode':        'LiₓC₆ → C₆ + xLi⁺ + xe⁻  (graphite, 0.1V)',
            'cathode':      'Li₁₋ₓCoO₂ + xLi⁺ + xe⁻ → LiCoO₂  (3.9V)',
            'electrolyte':  'LiPF₆ in EC/DMC (organic, nonaqueous)',
            'voltage':      '3.6-3.7 V nominal',
            'energy_density':'150-250 Wh/kg',
            'advantages':   'High energy density, no memory effect, long cycle life',
            'disadvantages':'Safety (thermal runaway), cost, Li supply',
            'cathode_types':'LCO (high energy), NMC, NCA (EV), LFP (safe, long life)',
            'applications': 'EVs, laptops, phones, grid storage'
        },
        'Solid state': {
            'electrolyte':  'Solid Li conductor (LLZO, LGPS, sulfide)',
            'advantages':   'No liquid electrolyte, safer, Li metal anode possible',
            'challenges':   'Interface resistance, manufacturing, cost',
            'status':       'Commercial in small cells, EV scale in development'
        },
        'Lithium-sulfur': {
            'anode':        'Li metal',
            'cathode':      'S₈ → Li₂S (complex polysulfide intermediates)',
            'voltage':      '2.1 V',
            'energy_density':'500+ Wh/kg (theoretical 2600)',
            'challenges':   'Polysulfide shuttle, Li dendrites, low cycle life'
        },
        'Flow batteries': {
            'types':        'Vanadium redox (VRB), Zn-Br, Fe-Cr',
            'concept':      'Electrolytes stored in external tanks, pumped through cell',
            'advantages':   'Decouple power (cell) and energy (tank size)',
            'applications': 'Grid-scale stationary storage'
        }
    }

def battery_metrics():
    return {
        'Specific energy':      'Wh/kg (energy per unit mass)',
        'Energy density':       'Wh/L (energy per unit volume)',
        'Specific power':       'W/kg (power per unit mass)',
        'C-rate':               '1C = full charge/discharge in 1 hour',
        'Cycle life':           'Number of charge-discharge cycles to 80% capacity',
        'Coulombic efficiency': 'Capacity out / Capacity in × 100%',
        'Energy efficiency':    'Energy out / Energy in × 100%',
        'Ragone plot':          'Specific power vs specific energy (compare technologies)',
        'State of charge':      'SOC = remaining capacity / total capacity × 100%',
        'Depth of discharge':   'DOD = 1 - SOC'
    }
```

---

## Fuel Cells
```
Fuel cell: convert chemical energy directly to electricity
  More efficient than heat engine (not Carnot limited)
  No NOx, SOx emissions (with H₂ fuel)

PEM fuel cell (Proton Exchange Membrane):
  Anode: H₂ → 2H⁺ + 2e⁻  (Pt catalyst)
  Cathode: O₂ + 4H⁺ + 4e⁻ → 2H₂O  (Pt catalyst)
  Electrolyte: Nafion membrane (proton conducting)
  Operating T: 60-80°C
  E° = 1.23 V, actual ~0.6-0.7 V (losses)
  Applications: vehicles (Toyota Mirai, Honda Clarity), portable power

Solid oxide fuel cell (SOFC):
  Anode: H₂ + O²⁻ → H₂O + 2e⁻  (Ni/YSZ cermet)
  Cathode: O₂ + 4e⁻ → 2O²⁻  (LSM perovskite)
  Electrolyte: YSZ (Y-stabilized ZrO₂, O²⁻ conductor)
  Operating T: 700-1000°C
  Advantages: fuel flexible (H₂, CH₄, CO), no Pt, highest efficiency
  Applications: stationary power, combined heat and power

Efficiency:
  Thermodynamic max: η_max = ΔG/ΔH = 1 - TΔS/ΔH
  H₂/O₂ at 25°C: η_max = 237/286 = 83%
  Actual: 40-60% (overpotentials, resistance losses)
  vs Carnot engine at 600°C: η_Carnot = 1-300/873 = 66%

Electrolysis (reverse of fuel cell):
  PEM electrolysis: H₂O → H₂ + ½O₂
  Voltage needed: >1.23 V (theoretical) + overpotentials ≈ 1.8-2.0 V
  HER (hydrogen evolution): Pt, MoS₂, Ni catalysts
  OER (oxygen evolution): IrO₂, RuO₂, NiFe catalysts
  Green hydrogen: electrolysis powered by renewables
```

---

## Corrosion
```
Electrochemical mechanism:
  Anodic reaction: M → Mⁿ⁺ + ne⁻  (metal dissolution)
  Cathodic reaction: O₂ + 2H₂O + 4e⁻ → 4OH⁻  (neutral/alkaline)
                     2H⁺ + 2e⁻ → H₂  (acidic)
  Both occur on same surface (local cells)

Types of corrosion:
  Uniform: even attack over whole surface
  Galvanic: dissimilar metals in contact + electrolyte
    Less noble (active) metal corrodes preferentially
    Galvanic series: Mg, Zn, Al, Fe, Ni, Cu, Ag, Pt, Au (noble)
  Pitting: localized attack through passive film
  Crevice: restricted geometry, local acidification
  Intergranular: attack at grain boundaries
  Stress corrosion cracking (SCC): stress + corrosive environment
  Hydrogen embrittlement: H absorption → brittle fracture
  Erosion corrosion: mechanical removal of passive film

Mixed potential theory (Evans diagrams):
  Corrosion potential Ecorr: where ia = ic (anodic = cathodic current)
  Corrosion current icorr: read from Evans diagram at Ecorr
  Corrosion rate: r = icorr·M/(nFρA)  (Faraday's law)

Passivation:
  Stable oxide film forms → large decrease in corrosion current
  Active-passive transition in anodic polarization curve
  Flade potential: transition from passive to active
  Pitting potential Ep: pitting initiates above this potential
  Examples: stainless steel (Cr₂O₃), Al (Al₂O₃), Ti (TiO₂)

Corrosion protection:
  Cathodic protection: make structure the cathode
    Sacrificial anode: Zn, Mg anodes on steel hull
    Impressed current: external power source (pipeline)
  Anodic protection: maintain passive region (tanks with H₂SO₄)
  Coatings: barrier protection (paint, epoxy, zinc phosphate)
  Inhibitors: adsorb on surface, block active sites
  Alloying: stainless steel (>10.5% Cr), Al-Mg alloys
```

---

## Electrodeposition
```
Nucleation and growth:
  3D nucleation: critical nucleus size r* = 2γVm/nFη
  Instantaneous nucleation: all nuclei form simultaneously
  Progressive nucleation: nuclei form throughout deposition
  Determined from chronoamperometry transient shape

Faraday's law for electroplating:
  m = MIt/nF  (mass deposited)
  Thickness = m/(ρA)

Current efficiency:
  η = m_actual/m_theoretical × 100%
  <100% due to H₂ evolution, oxide formation

Bath chemistry effects:
  pH: affects H₂ evolution, hydroxide precipitation
  Complexing agents: control activity, smooth deposits (cyanide for Cu, Ag)
  Brighteners: organic additives → smooth, bright deposits
  Levelers: reduce high-current density preferential plating
  Surfactants: reduce surface tension, improve wetting

Common electroplating systems:
  Cu: CuSO₄/H₂SO₄ (PCB), cyanide bath (decorative)
  Ni: Watts bath (NiSO₄/NiCl₂/H₃BO₃), bright nickel
  Cr: CrO₃/H₂SO₄ (hard chrome, decorative)
  Zn: alkaline or acid bath (corrosion protection on steel)
  Au: cyanide bath (electronics, decorative)
  Ag: cyanide bath (silverware, electronics)

Electroforming:
  Thick deposits forming self-supporting structure
  Remove mandrel → freestanding metal part
  Applications: printing plates, molds, waveguides
```

---

## Electroanalytical Techniques
```python
def electroanalytical_methods():
    return {
        'Cyclic Voltammetry (CV)': {
            'principle':    'Scan E linearly, reverse, measure I vs E',
            'info':         'Reversibility, E°, kinetics, mechanism, concentration',
            'reversible':   '|Epa - Epc| = 59/n mV, Ipa = Ipc at 25°C',
            'Randles-Sevc': 'Ip = 2.69×10⁵ n^(3/2) A D^(1/2) v^(1/2) C',
            'diffusion':    'Ip ∝ √v  (diffusion controlled)',
            'adsorption':   'Ip ∝ v  (adsorption controlled)'
        },
        'Electrochemical Impedance Spectroscopy (EIS)': {
            'principle':    'Small AC perturbation, measure Z vs frequency',
            'Nyquist':      'Im(Z) vs Re(Z), semicircle = charge transfer',
            'Bode':         'log|Z| and phase vs log(f)',
            'Randles circuit': 'Rs (solution) + Cdl || Rct + Zw (Warburg)',
            'Rct':          'Charge transfer resistance = RT/nFi₀',
            'Warburg':      'Zw = σ/√ω - jσ/√ω  (diffusion)',
            'applications': 'Battery characterization, corrosion, coatings'
        },
        'Stripping voltammetry': {
            'ASV':          'Anodic stripping: preconcentrate by reduction, then strip',
            'CSV':          'Cathodic stripping: preconcentrate by oxidation',
            'DPASV':        'Differential pulse ASV: most sensitive (ppt)',
            'applications': 'Trace metals: Pb, Cd, Zn, Cu, Hg, As'
        },
        'Chronoamperometry': {
            'principle':    'Step potential, measure I vs t',
            'Cottrell':     'i = nFACD^(1/2)/π^(1/2)t^(1/2)  (diffusion)',
            'i vs t^(-1/2)':'Linear plot → D measurement',
            'applications': 'Diffusion coefficient, mechanism, nucleation'
        },
        'SECM (Scanning Electrochemical Microscopy)': {
            'principle':    'UME scans near surface, image local reactivity',
            'resolution':   'Submicron with nm-sized tips',
            'applications': 'Corrosion mapping, biological membranes, catalyst screening'
        }
    }
```

---

## Key Equations Summary
```python
def electrochemistry_equations():
    return {
        'Gibbs-EMF':        'ΔG = -nFE',
        'Nernst':           'E = E° - (RT/nF)ln(Q)',
        'Nernst 25°C':      'E = E° - (0.05916/n)log(Q)',
        'Butler-Volmer':    'i = i₀[exp(αFη/RT) - exp(-(1-α)Fη/RT)]',
        'Tafel anodic':     'η = a + b·log(i)  a = -(RT/αnF)ln(i₀)',
        'Cottrell':         'i = nFACD^(1/2)/(π^(1/2)t^(1/2))',
        'Faraday plating':  'm = MIt/nF',
        'Randles-Sevcik':   'Ip = 2.69×10⁵ n^(3/2) A D^(1/2) v^(1/2) C',
        'Debye length':     'κ⁻¹ = √(ε₀εrkBT/2NAe²I)',
        'Levich':           'id = 0.620nFAD^(2/3)ω^(1/2)ν^(-1/6)C'
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Cell voltage = E_cathode + E_anode | E_cell = E_cathode - E_anode (both as reduction potentials) |
| Anode is always negative | Anode negative in galvanic cell, POSITIVE in electrolytic |
| Forgetting sign in Nernst | Products in numerator, reactants in denominator of Q |
| Tafel slope units | ba = 2.303RT/αnF in V/decade, not V/amp |
| Exchange current and corrosion current | i₀: equilibrium kinetics; icorr: at mixed potential |
| High E° = good cathode | High E° = good oxidant = good cathode in galvanic cell |

---

## Related Skills

- **physical-chemistry-expert**: Thermodynamics and kinetics
- **analytical-chemistry-expert**: Electroanalytical methods
- **materials-science-expert**: Battery materials, corrosion
- **energy-storage-expert**: Battery and fuel cell systems
- **inorganic-chemistry-expert**: Electrode materials
