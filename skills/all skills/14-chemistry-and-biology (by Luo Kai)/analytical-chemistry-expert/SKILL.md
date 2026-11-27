---
author: luo-kai
name: analytical-chemistry-expert
description: Expert-level analytical chemistry knowledge. Use when working with chromatography, spectroscopy, electroanalytical methods, sample preparation, quantitative analysis, calibration, statistics, or instrumental analysis. Also use when the user mentions 'HPLC', 'GC', 'mass spectrometry', 'atomic absorption', 'ICP', 'titration', 'calibration curve', 'detection limit', 'NMR', 'chromatography', 'electrochemistry', 'sample preparation', or 'method validation'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Analytical Chemistry Expert

You are a world-class analytical chemist with deep expertise in separation science, spectroscopic methods, electroanalytical techniques, sample preparation, quantitative analysis, statistics, and method validation.

## Before Starting

1. **Goal** — Identify compound, quantify analyte, separate mixture, or validate method?
2. **Sample type** — Liquid, solid, gas, biological, environmental, or pharmaceutical?
3. **Analyte** — Organic, inorganic, metal, or biological molecule?
4. **Technique** — Chromatography, spectroscopy, electrochemistry, or wet chemistry?
5. **Level** — Introductory, undergraduate, or professional/graduate?

---

## Core Expertise Areas

- **Chromatography**: HPLC, GC, TLC, ion chromatography, size exclusion
- **Mass Spectrometry**: ionization methods, analyzers, fragmentation, tandem MS
- **Atomic Spectroscopy**: AAS, ICP-OES, ICP-MS for elemental analysis
- **Molecular Spectroscopy**: UV-Vis, IR, Raman, NMR, fluorescence
- **Electroanalytical**: potentiometry, voltammetry, amperometry, conductometry
- **Sample Preparation**: extraction, digestion, cleanup, preconcentration
- **Quantitative Analysis**: calibration, statistics, QA/QC
- **Method Validation**: accuracy, precision, LOD, LOQ, linearity, ruggedness

---

## Chromatography Fundamentals
```
Separation principle:
  Analytes distribute between stationary phase and mobile phase.
  Retention factor: k = (tR - tM)/tM  (tR = retention time, tM = dead time)
  Selectivity: α = k₂/k₁  (relative retention)
  Resolution: RS = 2(tR2-tR1)/(w1+w2)  RS ≥ 1.5 for baseline separation

Van Deemter equation (band broadening):
  H = A + B/u + Cu
  H = plate height (smaller = better column)
  A = eddy diffusion (packing irregularity)
  B/u = longitudinal diffusion (faster flow reduces this)
  Cu = mass transfer resistance (slower flow reduces this)
  Optimal flow rate: u_opt = √(B/C)
  N = L/H  (theoretical plates, higher = better)

Peak characteristics:
  Gaussian peak: w = 4σ (base width), w₁/₂ = 2.355σ
  N = 16(tR/w)² = 5.545(tR/w₁/₂)²
  Asymmetry factor: As = b/a  (ideal = 1.0)
  Tailing (As > 1): active sites, overloading
  Fronting (As < 1): column overload
```

---

## High Performance Liquid Chromatography (HPLC)
```
Modes:
  Reversed phase (RP-HPLC): nonpolar stationary (C18, C8), polar mobile
    Most common, for organic analytes
    Mobile phase: water + organic modifier (MeOH, ACN)
    Gradient elution: increase organic over time

  Normal phase: polar stationary (silica), nonpolar mobile
    For water-sensitive, nonpolar analytes
    Mobile phase: hexane + polar modifier

  Ion exchange: ionic stationary phase, aqueous mobile
    For ions, amino acids, sugars
    Cation exchange: -SO₃H (strong), -COOH (weak)
    Anion exchange: -NR₃⁺ (strong), -NHR₂⁺ (weak)

  Size exclusion (SEC/GPC): porous particles, no retention
    Separate by size: large molecules elute first
    Used for polymers, proteins (MW determination)

  Hydrophilic interaction (HILIC): polar stationary, organic-rich mobile
    For polar, hydrophilic compounds

Detectors:
  UV-Vis: most common, 190-800 nm, needs chromophore
  Diode array (DAD): full spectrum, peak purity assessment
  Fluorescence: very sensitive, selective, needs fluorophore
  Refractive index (RID): universal, less sensitive, no gradient
  Evaporative light scattering (ELSD): semi-universal, gradient OK
  Mass spectrometry (LC-MS): gold standard for identification + quantitation
  Conductivity: for ions (ion chromatography)

Method development (RP-HPLC):
  1. Choose column: C18 most common, C8 for large molecules
  2. Start: 50/50 water/ACN or MeOH, adjust pH with buffer
  3. Optimize gradient: 5-95% organic over 15 min, then adjust
  4. Adjust pH: affects ionization of ionizable analytes
    Acids: low pH (suppress ionization, better peak shape)
    Bases: high pH or ion-pair reagent
  5. Adjust column temperature: usually 25-40°C
```

---

## Gas Chromatography (GC)
```
Requirements: analyte must be volatile and thermally stable
  Derivatization to improve volatility/stability if needed

Carrier gases: He (best), N₂ (cheap), H₂ (fast, flammable)

Columns:
  Packed: older, low efficiency, preparative
  Capillary (WCOT): fused silica, 0.1-0.53 mm ID, 10-100m
    Most common: 0.25 mm × 30m
  Stationary phases: polydimethylsiloxane (DB-1, nonpolar)
    Phenyl groups (DB-5, 5% phenyl, most versatile)
    Polyethylene glycol (Carbowax, polar)
    "Like dissolves like": polar analytes → polar column

Detectors:
  FID (flame ionization): universal for organics, very sensitive
    Destroys sample, insensitive to H₂O, CO₂, inorganic
  TCD (thermal conductivity): universal, less sensitive, nondestructive
  ECD (electron capture): selective for halogenated, very sensitive
  NPD (nitrogen-phosphorus): selective for N, P compounds
  FPD (flame photometric): selective for S, P
  MS (GC-MS): gold standard, library matching for identification

Kovats retention index:
  I = 100[n + (log tRx - log tRn)/(log tRn+1 - log tRn)]
  Compound retention relative to n-alkanes
  Database searchable, instrument-independent (same phase)

Headspace GC:
  Volatile compounds from solid/liquid matrix
  Static: equilibrium headspace
  Dynamic: purge and trap
  Applications: residual solvents, flavor, blood alcohol
```

---

## Mass Spectrometry
```
Ionization methods:
  EI (electron ionization): hard, 70 eV electrons, for GC-MS
    Produces M⁺• and fragments, reproducible, library searchable
  CI (chemical ionization): soft, [M+H]⁺ or [M-H]⁻, less fragmentation
  ESI (electrospray): very soft, for LC-MS, large biomolecules
    Produces multiply charged ions: [M+nH]ⁿ⁺
    m/z = (M + n×1.008)/n
  APCI (atmospheric pressure CI): LC-MS for smaller molecules
  MALDI (matrix-assisted laser desorption): large biomolecules, polymers
    Mostly singly charged, requires matrix
  FAB (fast atom bombardment): for polar, nonvolatile compounds

Mass analyzers:
  Quadrupole (Q): unit mass resolution, fast scanning, low cost
    Selected ion monitoring (SIM): very sensitive quantitation
  Ion trap: MSⁿ capability, small, traps ions
  Time-of-flight (TOF): high resolution, exact mass, fast
    m/z = (2eV/m)×t²  (flight time → mass)
  Magnetic sector: high resolution, exact mass, expensive
  Orbitrap: ultra-high resolution (>100,000), exact mass
  FT-ICR: highest resolution, research use

Tandem MS (MS/MS):
  Q1: select precursor ion
  Q2: collision induced dissociation (CID)
  Q3: scan or select product ions
  MRM (multiple reaction monitoring): most sensitive for quantitation
  Data-dependent acquisition (DDA): survey scan + MS/MS of top ions
  Data-independent acquisition (DIA): all ions fragmented

High resolution MS:
  Exact mass measurement: identify elemental formula
  Mass accuracy: <5 ppm for formula confirmation
  Isotope pattern: confirms formula (M, M+1, M+2 ratios)
```

---

## Atomic Spectroscopy
```python
def atomic_spectroscopy_methods():
    return {
        'AAS (Atomic Absorption Spectroscopy)': {
            'principle':    'Atoms absorb light at characteristic wavelengths',
            'flame AAS':    'Air-acetylene (2300°C) or N₂O-acetylene (2700°C)',
            'GFAAS':        'Graphite furnace: lower LOD, smaller sample, slow',
            'LOD':          'ppb (μg/L) for flame, ppt (ng/L) for GFAAS',
            'limitation':   'One element at a time',
            'best_for':     'Trace metals: Pb, Cd, Cu, Fe, Zn, Ca, Mg'
        },
        'ICP-OES (Optical Emission Spectroscopy)': {
            'principle':    'Plasma (6000-10000°C) excites atoms → emit light',
            'advantage':    'Multi-element (30-40 simultaneously)',
            'LOD':          'ppb range',
            'plasma':       'Argon ICP at 27 MHz RF',
            'best_for':     'Major and minor elements, quality control'
        },
        'ICP-MS': {
            'principle':    'ICP ionizes atoms → mass spectrometry',
            'advantage':    'Multi-element, isotope ratios, very low LOD',
            'LOD':          'ppt range (ng/L)',
            'isotope':      'Isotope dilution: most accurate quantitation',
            'limitation':   'Isobaric interferences (⁵⁶Fe⁺/⁴⁰Ar¹⁶O⁺)',
            'best_for':     'Ultra-trace metals, environmental, geological'
        },
        'XRF (X-ray fluorescence)': {
            'principle':    'X-rays eject core electrons → characteristic X-rays emitted',
            'advantage':    'Non-destructive, solid samples, multi-element',
            'limitation':   'Surface analysis, matrix effects',
            'best_for':     'Alloys, geological samples, environmental screening'
        }
    }
```

---

## Electroanalytical Methods
```
Potentiometry:
  Measure equilibrium potential (no current)
  E = E°cell + (RT/nF)ln(aOx/aRed)
  Ion-selective electrodes (ISE): glass (pH), fluoride, calcium, nitrate
  Reference electrodes: SCE (Ag/AgCl/KCl), Ag/AgCl

  pH glass electrode:
    E = const - 0.05916·pH  at 25°C
    Junction potential: source of error, use ionic strength adjustment

Voltammetry:
  Apply voltage, measure current
  Cyclic voltammetry (CV): scan E, measure I, reverse
    Reversible couple: |Epa - Epc| = 0.059/n V, Ipa = Ipc
    E°′ = (Epa + Epc)/2
    Ip = 2.69×10⁵ n^(3/2) A D^(1/2) v^(1/2) C  (Randles-Sevcik)
  Differential pulse (DPV): very sensitive, LOD ppb
  Square wave (SWV): fast, sensitive, diagnostic
  Stripping analysis (ASV): preconcentrate onto electrode, strip
    Most sensitive for trace metals (ppt achievable)

Amperometry/Coulometry:
  Amperometry: constant E, measure I vs time
    Biosensors (glucose, etc.)
  Coulometry: measure total charge Q = nFmoles
    Faraday's law: n_analyte = Q/nF
    100% current efficiency: absolute method

Conductometry:
  Measure conductance G = κ(A/l)  (κ = specific conductance)
  Conductometric titration: endpoint by conductance change
  Karl Fischer titration: water determination
```

---

## Sample Preparation
```python
def sample_prep_methods():
    return {
        'Liquid-liquid extraction (LLE)': {
            'principle':    'Distribute analyte between two immiscible solvents',
            'distribution': 'D = [A]org/[A]aq',
            'efficiency':   'E% = 100D/(D+Vaq/Vorg)',
            'optimize':     'pH, salt (salting out), solvent choice',
            'drawback':     'Emulsions, large solvent volumes, manual'
        },
        'Solid phase extraction (SPE)': {
            'principle':    'Load sample, wash matrix, elute analyte',
            'sorbents':     'C18, C8, SAX, SCX, mixed mode, ion exchange',
            'advantages':   'Less solvent, selective, automatable',
            'applications': 'Environmental, pharmaceutical, biological'
        },
        'QuEChERS': {
            'application':  'Pesticides in food (quick, easy, cheap, rugged)',
            'steps':        'Extraction (MeCN) + partitioning (MgSO₄) + dispersive SPE'
        },
        'Microwave digestion': {
            'application':  'Dissolve solid samples for elemental analysis',
            'reagents':     'HNO₃, HCl, HF, H₂O₂ (closed vessel)',
            'advantages':   'Fast, complete digestion, less contamination'
        },
        'Solid phase microextraction (SPME)': {
            'principle':    'Coated fiber equilibrates with headspace or solution',
            'advantage':    'Solvent-free, concentrates analyte, direct GC inject',
            'applications': 'Volatiles, flavor, environmental'
        },
        'Protein precipitation': {
            'agents':       'ACN, MeOH, TCA, ammonium sulfate',
            'use':          'Plasma, serum sample cleanup for drug analysis'
        }
    }
```

---

## Quantitative Analysis & Statistics
```python
import numpy as np

def calibration_statistics(concentrations, signals):
    """
    Linear calibration curve with statistics.
    """
    x = np.array(concentrations)
    y = np.array(signals)
    n = len(x)

    # Linear regression: y = mx + b
    x_mean, y_mean = x.mean(), y.mean()
    Sxx = np.sum((x - x_mean)**2)
    Sxy = np.sum((x - x_mean)*(y - y_mean))
    Syy = np.sum((y - y_mean)**2)

    m = Sxy / Sxx  # slope
    b = y_mean - m * x_mean  # intercept
    r2 = Sxy**2 / (Sxx * Syy)  # R²

    # Residuals
    y_pred = m * x + b
    residuals = y - y_pred
    se = np.sqrt(np.sum(residuals**2) / (n-2))

    # Uncertainties
    sm = se / np.sqrt(Sxx)
    sb = se * np.sqrt(np.sum(x**2) / (n * Sxx))

    # LOD and LOQ from blank
    s_blank = se  # approximation
    lod = 3 * s_blank / m
    loq = 10 * s_blank / m

    return {
        'slope':        round(m, 6),
        'intercept':    round(b, 6),
        'R_squared':    round(r2, 6),
        'SE_slope':     round(sm, 6),
        'SE_intercept': round(sb, 6),
        'LOD':          round(lod, 6),
        'LOQ':          round(loq, 6)
    }

def method_validation_parameters():
    return {
        'Accuracy':     'Recovery % = (found/true) × 100; spike recovery',
        'Precision': {
            'Repeatability':     'Same lab, same analyst, same day (RSD%)',
            'Reproducibility':   'Different labs, analysts, days',
            'Intermediate':      'Same lab, different days/analysts'
        },
        'LOD':          '3σ_blank/m (signal 3× noise above blank)',
        'LOQ':          '10σ_blank/m (quantifiable with ≤10% RSD)',
        'Linearity':    'R² ≥ 0.999, range usually 80-120% of target',
        'Selectivity':  'No interference from matrix components',
        'Ruggedness':   'Robustness to small deliberate variations',
        'Range':        'Concentration interval where method is valid',
        'Uncertainty':  'Combined standard uncertainty: u_c = √Σuᵢ²'
    }

def grubbs_outlier_test(data, alpha=0.05):
    """Grubbs test for outliers in small datasets."""
    data = np.array(data)
    n = len(data)
    mean, std = data.mean(), data.std(ddof=1)
    G = abs(data - mean).max() / std
    # Critical values (approximate for common n and alpha=0.05)
    return {
        'G_calculated': round(G, 4),
        'mean':         round(mean, 4),
        'std':          round(std, 4),
        'suspected_outlier': data[abs(data-mean).argmax()],
        'note': 'Compare G to critical value table for n and alpha'
    }
```

---

## Method Validation
```
ICH Q2(R1) guidelines (pharmaceutical):
  Specificity: no interference
  Linearity: R² ≥ 0.999, test 5+ concentrations
  Range: LOQ to 120% of specification
  Accuracy: spike recovery 98-102% (or 90-110% for complex matrices)
  Precision:
    Repeatability: ≤1% RSD (6 replicates)
    Intermediate: ≤2% RSD
  LOD: 3σ/m, signal-to-noise ≥ 3
  LOQ: 10σ/m, signal-to-noise ≥ 10, ≤10% RSD

FDA Bioanalytical Method Validation:
  Selectivity: no matrix interference
  Calibration: ≥6 non-zero standards, 4/6 back-calculate within 15%
  QC samples: ≥3 concentrations, ≥2/3 at each level within 15%
  Matrix effect: suppress or enhance signal
  Stability: freeze-thaw, bench-top, long-term

Environmental methods (EPA):
  Method detection limit (MDL): 3.14 × s (n=7 replicates at ~1-5× MDL)
  Practical quantitation limit (PQL): ~5-10× MDL
  Matrix spike/matrix spike duplicate: recovery and precision
  Lab control sample (LCS): spike in reagent water
```

---

## Common Analytical Techniques Summary
```python
def technique_selection_guide():
    return {
        'Volatile organics': 'GC-MS (headspace or purge&trap)',
        'Semi-volatile organics': 'GC-MS or HPLC-MS/MS',
        'Pesticides in food': 'GC-MS/MS or LC-MS/MS (QuEChERS)',
        'Trace metals': 'ICP-MS or GFAAS',
        'Major metals': 'ICP-OES or flame AAS',
        'Anions (Cl⁻, NO₃⁻, SO₄²⁻)': 'Ion chromatography',
        'Pharmaceutical impurities': 'HPLC-UV or HPLC-MS',
        'Proteins/peptides': 'LC-MS/MS (bottom-up proteomics)',
        'Drug in plasma': 'LC-MS/MS (protein precipitation)',
        'Polymer MW': 'GPC/SEC with RI detector',
        'Surface composition': 'XPS, SIMS, AES',
        'Crystal structure': 'X-ray diffraction (XRD)',
        'Elemental analysis (bulk)': 'CHNS analyzer, XRF',
        'Water content': 'Karl Fischer titration',
        'pH/ions in solution': 'ISE potentiometry',
        'Redox behavior': 'Cyclic voltammetry',
        'Color/turbidity': 'UV-Vis spectrophotometry'
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Calibration without blank | Always include reagent blank in calibration |
| Matrix mismatch | Match calibration matrix to sample matrix |
| Poor peak integration | Use consistent integration parameters, check manually |
| Carry-over | Inject blanks between samples, optimize wash steps |
| Forgetting units in LOD/LOQ | Report in same units as calibration (μg/L, ng/mL) |
| R² ≈ 1 does not mean accurate | Check residuals, accuracy with QC samples |
| Single point calibration | Use ≥5 point calibration for quantitative work |

---

## Related Skills

- **organic-chemistry-expert**: Structure identification by spectroscopy
- **inorganic-chemistry-expert**: Elemental speciation
- **physical-chemistry-expert**: Spectroscopic theory
- **biochemistry-expert**: Proteomics, metabolomics methods
- **environmental-science-expert**: Environmental monitoring methods
- **pharmaceutical-chemistry**: Drug analysis and validation
