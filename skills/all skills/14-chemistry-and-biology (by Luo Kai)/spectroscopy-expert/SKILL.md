---
author: luo-kai
name: spectroscopy-expert
description: Expert-level spectroscopy knowledge. Use when working with NMR, IR, Raman, UV-Vis, mass spectrometry, fluorescence, X-ray, electron spectroscopy, or any spectroscopic technique for structure determination or chemical analysis. Also use when the user mentions 'NMR spectroscopy', 'chemical shift', 'coupling constant', 'IR absorption', 'Raman scattering', 'UV-Vis absorption', 'fluorescence', 'XPS', 'EPR', 'mass spectrum', 'fragmentation', or 'spectral interpretation'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Spectroscopy Expert

You are a world-class spectroscopist with deep expertise in NMR, IR, Raman, UV-Vis, mass spectrometry, fluorescence, X-ray spectroscopy, electron spectroscopy, and the interpretation of spectra for structural elucidation and chemical analysis.

## Before Starting

1. **Technique** — NMR, IR, UV-Vis, MS, Raman, fluorescence, or X-ray?
2. **Goal** — Structure determination, quantitation, identification, or mechanism?
3. **Sample** — Small molecule, polymer, biological, surface, or solid?
4. **Level** — Introductory, undergraduate, or graduate/research?
5. **Data available** — Spectrum to interpret or concept to understand?

---

## Core Expertise Areas

- **NMR Spectroscopy**: ¹H, ¹³C, 2D NMR, solid state, MRI
- **Infrared & Raman**: vibrational spectroscopy, group frequencies
- **UV-Vis & Fluorescence**: electronic transitions, Beer-Lambert, fluorimetry
- **Mass Spectrometry**: ionization, fragmentation, high resolution
- **X-ray Methods**: XRD, XPS, XAFS, small angle scattering
- **Electron Spectroscopy**: EPR/ESR, Auger, EELS
- **Optical Spectroscopy**: atomic emission, absorption, laser techniques
- **Hyphenated Techniques**: GC-MS, LC-MS, LC-NMR, ICP-MS

---

## Nuclear Magnetic Resonance (NMR)

### Fundamental Principles
```
Basis: nuclei with spin (I ≠ 0) precess in magnetic field
  ¹H: I = ½ (most sensitive, 99.98% natural abundance)
  ¹³C: I = ½ (1.1% natural abundance, less sensitive)
  ¹⁵N: I = ½ (0.4%, important for proteins)
  ³¹P: I = ½ (100%, important for biochemistry)
  ¹⁹F: I = ½ (100%, highly sensitive)
  ²H: I = 1 (deuterium, used as solvent lock)

Larmor frequency:
  ν₀ = γB₀/2π
  γ = gyromagnetic ratio (nucleus-specific)
  ¹H at 11.7 T: ν₀ = 500 MHz (500 MHz NMR)
  ¹³C at 11.7 T: ν₀ = 125.7 MHz

Chemical shift (δ):
  δ = (νsample - νref)/νspectrometer × 10⁶  (ppm)
  Reference: TMS (tetramethylsilane, δ = 0 ppm)
  Shielded (upfield): high electron density, low δ
  Deshielded (downfield): low electron density, high δ
```

### ¹H NMR Chemical Shifts
```
δ (ppm) ranges:
  0-1:    TMS, CH₃ (alkyl), cyclopropane
  0.9:    CH₃ (terminal alkyl)
  1.2:    CH₂ (chain)
  1.5-2:  CH₃/CH₂ adjacent to C=C or C=O
  2-3:    CH adjacent to C=O, ArCH₂, NCCH₂
  3-4:    OCH₃, OCH₂ (ether), NCH (amine adjacent)
  3.5-4:  OCH₂ (ester)
  4.5-6:  vinyl CH, OCH (anomeric)
  5-6:    =CH₂ (terminal alkene)
  6.5-8:  aromatic CH
  7.27:   CDCl₃ solvent residual peak
  8-10:   ArCHO, RCOH (aldehydes)
  9.5-10: RCHO (aliphatic aldehyde)
  10-12:  RCOOH (carboxylic acid)
  NH, OH: variable 1-12 ppm (exchangeable, broadened)
```

### Spin-Spin Coupling
```
J-coupling: through-bond magnetic interaction
  Vicinal (³J): H-C-C-H, most common
    Karplus equation: ³J = A + B·cosφ + C·cos2φ
    φ = dihedral angle
    ³J(gauche, 60°) ≈ 4 Hz, ³J(anti, 180°) ≈ 12 Hz
  Geminal (²J): H-C-H, 0-20 Hz
  Long range (⁴J, ⁵J): through π systems, W arrangement

First-order splitting (n+1 rule):
  n equivalent neighboring H → n+1 lines (Pascal's triangle)
  Doublet: 1 neighbor, d (1:1)
  Triplet: 2 neighbors, t (1:2:1)
  Quartet: 3 neighbors, q (1:3:3:1)
  Pentet: 4 neighbors (1:4:6:4:1)
  Doublet of doublets: dd (2 different neighbors)

Common coupling patterns:
  Ethyl group: -CH₂CH₃: triplet + quartet
  Isopropyl: (CH₃)₂CH-: doublet + septet
  Vinyl: -CH=CH₂: multiplet patterns

Second-order effects:
  Occur when Δν/J < 10
  AB quartet: two coupled protons with similar shifts
  ABX, AMX, AA′BB′: complex patterns
```

### ¹³C NMR
```
Chemical shifts:
  0-50:   alkyl carbons (CH₄: -2.3, cyclohexane: 27)
  15-25:  CH₃ groups
  20-40:  CH₂ groups
  25-50:  CH groups
  50-80:  C adjacent to O or N (ethers, alcohols)
  60-90:  alkynyl carbons (sp)
  100-150: aromatic and vinyl carbons (sp²)
  155-185: carbonyl C (esters, amides)
  190-210: aldehyde and ketone C=O

DEPT experiment:
  Distinguishes CH, CH₂, CH₃ from quaternary C
  DEPT-135: CH and CH₃ up, CH₂ down, C quaternary absent
  DEPT-90:  only CH
  Very useful for structural assignment

APT (Attached Proton Test):
  CH and CH₃: one phase; CH₂ and C: opposite phase
```

### 2D NMR Techniques
```python
def twoD_nmr_experiments():
    return {
        'COSY (¹H-¹H)': {
            'type':         'Homonuclear correlation',
            'shows':        'Through-bond ¹H-¹H coupling',
            'crosspeaks':   'Appear for vicinal (³J) and geminal (²J) coupling',
            'use':          'Trace connectivity of H-C-C-H chains',
            'variants':     'DQF-COSY (better diagonal suppression)'
        },
        'HSQC (¹H-¹³C)': {
            'type':         'Heteronuclear one-bond correlation',
            'shows':        '¹J(CH) correlations',
            'crosspeaks':   'Each H attached directly to C',
            'use':          'Assign ¹³C chemical shifts, count CH groups',
            'variants':     'DEPT-HSQC, multiplicity-edited HSQC'
        },
        'HMBC (¹H-¹³C)': {
            'type':         'Heteronuclear long-range correlation',
            'shows':        '²J and ³J H-C correlations',
            'crosspeaks':   'H to C 2-3 bonds away',
            'use':          'Connect fragments, assign quaternary C',
            'key':          'Essential for complete structure determination'
        },
        'NOESY (¹H-¹H)': {
            'type':         'Through-space correlation',
            'shows':        'Nuclear Overhauser effect (NOE)',
            'distance':     'Crosspeak if H-H < 5 Å',
            'use':          '3D structure, stereochemistry, conformation',
            'variants':     'ROESY (for medium-sized molecules)'
        },
        'TOCSY': {
            'type':         'Total correlation spectroscopy',
            'shows':        'All H in same spin system',
            'use':          'Identify amino acid spin systems in proteins'
        }
    }
```

---

## Infrared (IR) Spectroscopy
```python
def ir_group_frequencies():
    return {
        'X-H Stretches (3000-4000 cm⁻¹)': {
            'O-H free':         '3580-3650 cm⁻¹ (sharp)',
            'O-H H-bonded':     '2500-3300 cm⁻¹ (broad)',
            'N-H primary':      '3300-3500 cm⁻¹ (two bands)',
            'N-H secondary':    '3300-3350 cm⁻¹ (one band)',
            'C-H sp³':          '2850-3000 cm⁻¹',
            'C-H sp²':          '3000-3100 cm⁻¹',
            'C-H sp (alkyne)':  '3300 cm⁻¹ (sharp)',
            'S-H':              '2550-2600 cm⁻¹'
        },
        'Triple Bonds (2000-2500 cm⁻¹)': {
            'C≡C':              '2100-2260 cm⁻¹ (weak/absent if symmetric)',
            'C≡N':              '2200-2260 cm⁻¹ (strong)',
            'C=C=C (allene)':   '1950 cm⁻¹',
            'N=C=O (isocyanate)':'2270 cm⁻¹ (very strong, broad)'
        },
        'C=O Stretches (1630-1870 cm⁻¹)': {
            'Acid chloride':    '1800 cm⁻¹',
            'Anhydride':        '1850 + 1760 cm⁻¹ (two bands)',
            'Ester':            '1735-1750 cm⁻¹',
            'Aldehyde':         '1720-1740 cm⁻¹ + C-H 2720, 2820',
            'Ketone':           '1705-1725 cm⁻¹',
            'Carboxylic acid':  '1700-1725 cm⁻¹ + broad O-H',
            'Amide primary':    '1650-1690 cm⁻¹ + N-H bend 1550-1650',
            'Conjugated C=O':   '~20-30 cm⁻¹ lower than unconjugated',
            'Ring strain':      'Cyclobutanone ~1780, cyclopentanone ~1740'
        },
        'C=C and Aromatics (1400-1680 cm⁻¹)': {
            'C=C alkene':       '1620-1680 cm⁻¹ (variable strength)',
            'Aromatic C=C':     '1450-1600 cm⁻¹ (two bands)',
            'Aromatic C-H bend':'690-900 cm⁻¹ (ring substitution pattern)'
        },
        'Single Bonds (500-1400 cm⁻¹)': {
            'C-O ether/alcohol':'1000-1300 cm⁻¹ (strong)',
            'C-F':              '1000-1400 cm⁻¹',
            'C-Cl':             '600-800 cm⁻¹',
            'C-Br':             '500-600 cm⁻¹',
            'C-I':              '200-500 cm⁻¹',
            'S=O':              '1030-1070 (sulfoxide), 1100-1200 (sulfone)'
        }
    }
```

### Raman Spectroscopy
```
Complementary to IR:
  IR active: change in dipole moment during vibration
  Raman active: change in polarizability during vibration
  Mutual exclusion: centrosymmetric molecules (CO₂, benzene):
    IR and Raman bands are mutually exclusive!

Raman advantages over IR:
  Water is weak Raman scatterer → biological samples OK
  No KBr pellets needed — any form of sample
  Lower frequency range accessible (lattice modes, metals)
  Spatially resolved (Raman microscopy, 1 μm resolution)

Characteristic Raman bands:
  C=C stretch: 1620-1680 cm⁻¹ (strong in Raman, weak in IR)
  C-C stretch: 700-1200 cm⁻¹ (strong in Raman)
  S-S stretch: 500-550 cm⁻¹ (strong in Raman, silent in IR)
  Metal-O:     100-400 cm⁻¹
  Ring breathing: strong symmetric stretches

Surface Enhanced Raman (SERS):
  10⁶-10¹⁴ enhancement on rough metal surfaces (Au, Ag)
  Single molecule detection possible
  Mechanism: electromagnetic (plasmon) + chemical enhancement
```

---

## UV-Vis Spectroscopy
```python
def uv_vis_transitions():
    return {
        'σ → σ*': {
            'energy':   'Very high energy (<150 nm, vacuum UV)',
            'example':  'Alkanes, saturated compounds'
        },
        'n → σ*': {
            'energy':   '150-250 nm',
            'example':  'Water (167 nm), alcohols, ethers, amines',
            'weak':     'Low ε (100-3000 L/mol·cm)'
        },
        'π → π*': {
            'energy':   '150-250 nm (unconjugated), red shifts with conjugation',
            'example':  'Ethylene (165 nm), benzene (254 nm)',
            'strong':   'High ε (10,000-100,000 L/mol·cm)',
            'Woodward': 'Rules predict λmax for conjugated systems'
        },
        'n → π*': {
            'energy':   '250-400 nm (carbonyl, nitro groups)',
            'example':  'Acetone: 270 nm (ε ≈ 15)',
            'weak':     'Symmetry forbidden, low ε',
            'solvent':  'Blue shift in polar solvents (n→π*)'
        },
        'Charge transfer': {
            'energy':   'Visible region (colored compounds)',
            'example':  'MnO₄⁻ (purple), CrO₄²⁻ (yellow), Fe-phen complexes',
            'strong':   'Very high ε (10,000-50,000)'
        }
    }

def woodward_rules_dienes():
    return {
        'Base value (heteroannular diene)': 214,
        'Base value (homoannular diene)':   253,
        'Increments (add for each)': {
            'Extending conjugation (extra C=C)':    +30,
            'Alkyl substituent or ring residue':     +5,
            'Exocyclic double bond':                 +5,
            'OAc substituent':                       0,
            'OR substituent':                        +6,
            'SR substituent':                        +30,
            'Cl, Br substituent':                    +5,
            'NR₂ substituent':                       +60
        },
        'example': 'β-carotene (11 conjugated double bonds): absorbs at ~450 nm → orange'
    }

def beer_lambert():
    return {
        'Law':          'A = εlc = log(I₀/I)',
        'A':            'Absorbance (dimensionless)',
        'ε':            'Molar absorptivity (L/mol·cm)',
        'l':            'Path length (cm)',
        'c':            'Concentration (mol/L)',
        'Transmittance':'T = I/I₀ = 10^(-A)',
        'Linear range': 'A = 0.1 to 1.0 (best accuracy)',
        'Deviations':   'High concentration (ion pairing), stray light, mixed species'
    }
```

---

## Fluorescence Spectroscopy
```
Jablonski diagram:
  Absorption → S₁ (excited singlet)
  Internal conversion → vibrational relaxation (fast, ps)
  Fluorescence: S₁ → S₀ + photon  (ns timescale)
  Intersystem crossing: S₁ → T₁ (spin flip)
  Phosphorescence: T₁ → S₀ + photon (ms-s timescale)

Stokes shift:
  Emission always at longer wavelength than absorption
  Due to vibrational relaxation in excited state
  Large Stokes shift: better for analytical applications (less scatter)

Quantum yield:
  Φ = photons emitted / photons absorbed
  Φ = kr/(kr + knr)  (kr = radiative, knr = nonradiative)
  Fluorescein: Φ ≈ 0.97 (very high)
  Rhodamine 6G: Φ ≈ 0.95
  Tryptophan: Φ ≈ 0.13

Fluorescence lifetime:
  τ = 1/(kr + knr)
  Typically 1-10 ns for organic fluorophores
  Quenching: decreases Φ and τ

Stern-Volmer equation (quenching):
  F₀/F = 1 + kq·τ₀·[Q] = 1 + KSV·[Q]
  KSV = Stern-Volmer constant (dynamic quenching)
  kq: bimolecular quenching rate constant

FRET (Förster Resonance Energy Transfer):
  Energy transfer from donor to acceptor (dipole-dipole)
  E = 1/(1 + (r/R₀)⁶)
  R₀ = Förster radius (1-10 nm)
  Molecular ruler: sensitive to 1-10 nm distances
  Applications: protein conformational changes, biosensors

Fluorescence applications:
  Single molecule detection
  Microscopy (confocal, TIRF, super-resolution STORM/PALM)
  Flow cytometry, ELISA, protein labeling
  Environmental sensors (pH, Ca²⁺, reactive oxygen species)
```

---

## X-ray Spectroscopy
```
X-ray diffraction (XRD):
  Single crystal: full 3D structure (bond lengths ±0.001 Å)
  Powder XRD: phase identification, unit cell parameters
  Bragg's law: 2d·sinθ = nλ
  Structure factor: Fhkl = Σ fⱼ exp(2πi(hxⱼ+kyⱼ+lzⱼ))
  Electron density map: ρ(xyz) = (1/V)Σ Fhkl exp(-2πi(hx+ky+lz))

X-ray photoelectron spectroscopy (XPS):
  Photoelectric effect: hν = KE + BE (binding energy)
  Surface sensitive: ~1-10 nm depth
  Elemental analysis: each element has characteristic BE
  Chemical state: shifts of 1-10 eV indicate oxidation state
  Fe²⁺: 2p₃/₂ at 708 eV, Fe³⁺: 711 eV
  C 1s: alkyl 285, C-O 286, C=O 288, O-C=O 289 eV
  Quantitative: peak areas → composition

X-ray absorption spectroscopy (XAS):
  XANES (near edge): electronic structure, oxidation state, coordination
  EXAFS (extended): local structure, bond lengths, coordination numbers
  Synchrotron required for best data
  Important for: catalysts, biological metal sites, amorphous materials

Small angle X-ray scattering (SAXS):
  Structural features 1-100 nm
  Particle size, shape, polymer conformation
  In situ measurements possible
```

---

## Electron Paramagnetic Resonance (EPR/ESR)
```
Detects unpaired electrons (radicals, transition metals)
Analogous to NMR but for electron spin

Resonance condition:
  hν = gβeB₀  (g = g-factor, βe = Bohr magneton)
  g = 2.0023 for free electron
  Deviation from g = 2.0: spin-orbit coupling, coordination geometry

Hyperfine coupling (A):
  Interaction of electron spin with nuclear spin
  Splits EPR line: 2I+1 lines for nucleus with spin I
  ¹⁴N (I=1): triplet splitting (three lines, 1:1:1)
  ¹H (I=½): doublet splitting
  Coupling constant A (MHz or mT)

Applications:
  Radical detection: reaction intermediates, radiation damage
  Spin labels: TEMPO attached to biomolecules → structure/dynamics
  Transition metal centers: Fe-S clusters, Cu sites, Mn in PSII
  ENDOR: EPR + NMR double resonance → hyperfine details
  Pulsed EPR (DEER): distance measurements 2-8 nm
```

---

## Mass Spectrometry (Advanced)
```python
def ionization_methods_advanced():
    return {
        'EI (70 eV)': {
            'fragments':    'Extensive, reproducible library match',
            'M+•':          'Odd-electron molecular ion',
            'GC-MS':        'Primary technique for volatile organics',
            'limitations':  'Not suitable for labile or large molecules'
        },
        'ESI': {
            'charge_states':'Multiple charges: [M+nH]ⁿ⁺',
            'deconvolution':'MW = (m/z₁ × z₁ - z₁ × 1.008)',
            'soft':         'Intact noncovalent complexes possible',
            'proteins':     'Typical: 10-50 charges for ~50 kDa protein',
            'native MS':    'Preserve protein-protein, protein-ligand complexes'
        },
        'MALDI': {
            'matrix':       'DHB, sinapinic acid, CHCA absorbs laser energy',
            'ions':         'Mostly [M+H]⁺ or [M+Na]⁺ (singly charged)',
            'range':        'kDa to MDa (polymers, proteins)',
            'imaging':      'MALDI-MSI: spatial distribution of molecules in tissue'
        },
        'APCI': {
            'mechanism':    'Corona discharge ionizes solvent → CI of analyte',
            'use':          'LC-MS for less polar compounds (lipids, steroids)'
        },
        'DART': {
            'mechanism':    'Metastable He/N₂ ionizes surface analytes',
            'no_sample_prep':'Direct analysis from surfaces, tablets, food'
        }
    }

def mass_analyzers_performance():
    return {
        'Quadrupole': {
            'resolution':   '~1000 (unit mass)',
            'scan_speed':   'Fast',
            'sensitivity':  'High (SIM mode)',
            'MS/MS':        'Triple quad (QqQ): gold standard quantitation'
        },
        'TOF': {
            'resolution':   '20,000-50,000',
            'mass_accuracy':'5-10 ppm',
            'speed':        'Very fast (μs per spectrum)',
            'use':          'MALDI-TOF, LC-QTOF'
        },
        'Orbitrap': {
            'resolution':   '100,000-500,000+',
            'mass_accuracy':'<2 ppm (with internal calibration)',
            'principle':    'Orbital trapping around spindle electrode',
            'use':          'Proteomics, metabolomics, pharma'
        },
        'FT-ICR': {
            'resolution':   '>1,000,000',
            'mass_accuracy':'<1 ppm',
            'principle':    'Ion cyclotron resonance in magnetic field',
            'limitation':   'Expensive, large magnet, slow scan'
        }
    }
```

---

## Spectral Interpretation Strategy
```python
def structure_elucidation_workflow():
    return {
        'Step 1 — Molecular formula': [
            'High-res MS: exact mass → elemental formula',
            'Degree of unsaturation: DBE = (2C+2+N-H-X)/2',
            'DBE = 0: acyclic, no π bonds',
            'DBE = 1: one ring or one double bond',
            'DBE = 4: benzene ring',
            'DBE > 4: aromatic or multiple rings/double bonds'
        ],
        'Step 2 — Functional groups (IR)': [
            'Check 3200-3600 for O-H, N-H',
            'Check 2100-2300 for triple bonds',
            'Check 1700-1800 for C=O (identify type)',
            'Check 1600-1680 for C=C',
            'Check fingerprint 600-1400'
        ],
        'Step 3 — Carbon framework (¹³C + DEPT)': [
            'Count carbons and types',
            'Identify CH₃, CH₂, CH, quaternary C',
            'Note sp³ (0-50), sp² (100-150), C=O (160-220) regions'
        ],
        'Step 4 — Hydrogen environments (¹H)': [
            'Count H by integration',
            'Identify chemical shifts → functional groups',
            'Analyze splitting patterns → neighboring H',
            'Note exchangeable H (D₂O shake → disappear)'
        ],
        'Step 5 — Connectivity (2D NMR)': [
            'COSY: trace H-C-C-H chains',
            'HSQC: assign each H to its C',
            'HMBC: connect fragments through 2-3 bonds',
            'NOESY: confirm 3D arrangement and stereochemistry'
        ],
        'Step 6 — Assemble structure': [
            'Use DBE to account for all rings/double bonds',
            'Check all data consistent with proposed structure',
            'Compare with literature spectra if available'
        ]
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Integrating exchangeable H | D₂O shake removes OH, NH signals — do before final integration |
| Forgetting solvent peaks | CDCl₃: ¹H at 7.27, ¹³C at 77; DMSO-d₆: ¹H at 2.50 |
| n+1 rule with non-equivalent H | n+1 only for equivalent neighboring H; use dd, ddd for non-equivalent |
| IR of liquid vs solid | Neat film vs KBr pellet vs ATR — band positions shift slightly |
| Beer-Lambert at high concentration | Linear only up to A ≈ 1.0; dilute if needed |
| MS molecular ion assignment | EI: M⁺• is odd-electron; ESI: [M+H]⁺ is even-electron |

---

## Related Skills

- **organic-chemistry-expert**: Structure determination context
- **analytical-chemistry-expert**: Quantitative spectroscopy
- **physical-chemistry-expert**: Quantum mechanical basis
- **inorganic-chemistry-expert**: EPR, XPS of metal complexes
- **biochemistry-expert**: Protein NMR, mass spec proteomics
