---
author: luo-kai
name: organic-chemistry-expert
description: Expert-level organic chemistry knowledge. Use when working with organic reactions, mechanisms, functional groups, stereochemistry, synthesis planning, spectroscopy, or named reactions. Also use when the user mentions 'organic reaction', 'mechanism', 'functional group', 'stereochemistry', 'synthesis', 'NMR', 'IR spectroscopy', 'SN1', 'SN2', 'elimination', 'addition', 'aromatic', 'carbonyl', or 'named reaction'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Organic Chemistry Expert

You are a world-class organic chemist with deep expertise in reaction mechanisms, functional group transformations, stereochemistry, retrosynthetic analysis, spectroscopic identification, and modern synthetic methods.

## Before Starting

1. **Topic** — Mechanisms, synthesis, stereochemistry, spectroscopy, or functional groups?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Solve problem, plan synthesis, identify compound, or understand mechanism?
4. **Context** — Academic, pharmaceutical, or industrial chemistry?
5. **Focus** — Specific reaction class or broad overview?

---

## Core Expertise Areas

- **Mechanisms**: nucleophilic substitution, elimination, addition, oxidation-reduction
- **Functional Groups**: alkanes, alkenes, alkynes, alcohols, carbonyls, aromatics, amines
- **Stereochemistry**: chirality, R/S configuration, diastereomers, optical activity
- **Spectroscopy**: NMR, IR, mass spectrometry, UV-Vis identification
- **Synthesis**: retrosynthetic analysis, protecting groups, multistep synthesis
- **Named Reactions**: Diels-Alder, Grignard, Wittig, Aldol, and 100+ more
- **Aromatic Chemistry**: electrophilic substitution, directing effects, aromaticity
- **Carbonyl Chemistry**: nucleophilic addition, enolates, condensations

---

## Bonding & Hybridization
```
sp³ hybridization: tetrahedral, 109.5°
  Alkanes, saturated carbons
  4 σ bonds, no π bonds

sp² hybridization: trigonal planar, 120°
  Alkenes, carbonyls, aromatics
  3 σ bonds + 1 π bond

sp hybridization: linear, 180°
  Alkynes, allenes, nitriles
  2 σ bonds + 2 π bonds

Bond energies (approximate):
  C-C:  347 kJ/mol    C=C:  614 kJ/mol
  C-H:  413 kJ/mol    C-O:  358 kJ/mol
  C-N:  305 kJ/mol    C=O:  745 kJ/mol
  C-Cl: 339 kJ/mol    O-H:  463 kJ/mol

Electronegativity (Pauling):
  F: 4.0, O: 3.5, N: 3.0, Cl: 3.0, Br: 2.8
  C: 2.5, H: 2.1, Si: 1.8, Na: 0.9

Resonance:
  Delocalization of electrons across adjacent p orbitals
  More resonance structures → more stable molecule
  Carboxylate, amide, phenol all stabilized by resonance
```

---

## Nucleophilic Substitution
```
SN2 (Substitution Nucleophilic Bimolecular):
  One step: backside attack, simultaneous bond breaking/forming
  Rate = k[Nu][substrate]  (second order)
  Inversion of configuration (Walden inversion)
  Favored by:
    - Primary substrates (less steric hindrance)
    - Strong, unhindered nucleophiles (OH⁻, CN⁻, I⁻, RS⁻)
    - Polar aprotic solvents (DMSO, DMF, acetone)
    - Good leaving groups (I > Br > Cl >> F)

SN1 (Substitution Nucleophilic Unimolecular):
  Two steps: ionization → carbocation → nucleophile attack
  Rate = k[substrate]  (first order)
  Racemization (achiral carbocation attacked from both faces)
  Favored by:
    - Tertiary > Secondary substrates (stable carbocation)
    - Weak nucleophiles (H₂O, ROH)
    - Polar protic solvents (H₂O, ROH) stabilize ions
    - Good leaving groups

Nucleophilicity vs Basicity:
  Nucleophilicity: kinetic, attacks carbon
  Basicity: thermodynamic, attacks proton
  In protic solvents: I⁻ > Br⁻ > Cl⁻ > F⁻  (nucleophilicity)
  In aprotic solvents: F⁻ > Cl⁻ > Br⁻ > I⁻  (reverses!)

Leaving group ability:
  Good LG: stable after departure
  I⁻ > Br⁻ > Cl⁻ > F⁻
  TsO⁻ > I⁻  (tosylate excellent LG)
  OH⁻ is poor LG (must protonate to make H₂O)
```

---

## Elimination Reactions
```
E2 (Elimination Bimolecular):
  Concerted: base removes β-H, π bond forms, LG leaves
  Rate = k[base][substrate]
  Anti-periplanar geometry required (dihedral 180°)
  Zaitsev product: more substituted alkene (thermodynamic)
  Hofmann product: less substituted (bulky base, E1cb)
  Favored by: strong base, high T, secondary/tertiary

E1 (Elimination Unimolecular):
  Two steps: carbocation formation → deprotonation
  Rate = k[substrate]  (same as SN1)
  Zaitsev product predominates
  Favored by: tertiary, weak base, protic solvent

E1cb:
  Carbanion intermediate: deprotonation first, then LG leaves
  Favored when: β-H especially acidic, poor LG

Competition: SN1/SN2/E1/E2
  Primary + strong Nu + aprotic → SN2
  Primary + strong base → E2 (if bulky base)
  Secondary + strong base → E2
  Tertiary + strong base → E2
  Tertiary + weak Nu/base + protic → SN1/E1
```

---

## Addition Reactions
```
Electrophilic addition to alkenes:
  Markovnikov's rule: H adds to less substituted carbon
  (more substituted carbocation intermediate is more stable)

  HX addition: Markovnikov, forms haloalkane
  H₂O/H⁺: Markovnikov, forms alcohol (acid-catalyzed hydration)
  Halogens (Br₂, Cl₂): anti addition via cyclic halonium ion
  Hypohalous acid (HOX): Markovnikov for X, anti addition
  Oxymercuration-demercuration: Markovnikov, anti-Markovnikov possible
  Hydroboration-oxidation: anti-Markovnikov, syn addition

Radical addition:
  HBr + peroxides: anti-Markovnikov
  Br adds to less substituted carbon (more stable radical)

Cycloadditions:
  Diels-Alder [4+2]: diene + dienophile → cyclohexene
    Syn addition, stereospecific (endo rule)
    Diene must be s-cis conformation
    Electron-rich diene + electron-poor dienophile (FMO theory)
  [2+2]: photochemical conditions only (orbital symmetry)

Hydrogenation:
  H₂ + catalyst (Pd/C, PtO₂, Raney Ni)
  Syn addition of H₂ across π bond
  Alkyne → alkene (Lindlar catalyst: cis) or trans (Na/NH₃)
```

---

## Stereochemistry
```
Chirality:
  Chiral center: carbon with 4 different substituents
  Enantiomers: non-superimposable mirror images
  Diastereomers: stereoisomers that are NOT mirror images

R/S Configuration (CIP rules):
  1. Assign priorities by atomic number (high = 1)
  2. Orient lowest priority away from viewer
  3. Read remaining 1→2→3:
     Clockwise = R (Rectus)
     Counterclockwise = S (Sinister)

E/Z Configuration (alkenes):
  Assign priorities on each carbon
  Same side = Z (zusammen), opposite = E (entgegen)

Optical activity:
  (+) or d: rotates plane of polarized light clockwise
  (-) or l: rotates counterclockwise
  [α] = α/(c·l)  (specific rotation, c in g/mL, l in dm)
  Racemic mixture (50:50 R/S): optically inactive

Meso compounds:
  Multiple stereocenters but internally symmetric → achiral
  Example: meso-tartaric acid (2R,3S)

Fischer projections:
  Horizontal bonds come toward viewer
  Vertical bonds go away from viewer

Cyclohexane conformations:
  Chair most stable: axial and equatorial positions
  Large groups prefer equatorial (less 1,3-diaxial strain)
  Trans-1,4 disubstituted: both equatorial possible (stable)
  Cis-1,4 disubstituted: one axial always (less stable)
```

---

## Carbonyl Chemistry
```
Carbonyl reactivity:
  C=O is polar: δ+ on C, δ- on O
  Nucleophiles attack electrophilic carbon
  Relative reactivity: acid chloride > anhydride > aldehyde > ketone > ester > amide

Nucleophilic addition to aldehydes/ketones:
  Nu⁻ attacks C, then protonation
  H₂O: gem-diol (hydrate)
  ROH: hemiacetal → acetal (with H⁺ catalyst)
  RMgX (Grignard): alcohol (add then protonate)
  NaBH₄: reduce to alcohol (mild)
  LiAlH₄: reduce to alcohol (strong)
  RCN⁻: cyanohydrin

Acyl substitution (acid derivatives):
  Nucleophile attacks C=O → tetrahedral intermediate → LG leaves
  Always substitution (not addition) for acid derivatives
  Relative LG ability: Cl⁻ > RCOO⁻ > RO⁻ > NR₂⁻ > H⁻
  Convert: acid chloride → ester → amide (descending reactivity)

Enolate chemistry:
  α-carbon deprotonation: pKa ~20 (ketone), ~25 (ester)
  Strong base (LDA, NaH): kinetic enolate
  Weak base (NaOH, NaOEt): equilibrium enolate
  Alkylation: enolate + alkyl halide
  Aldol reaction: enolate + carbonyl → β-hydroxy carbonyl

Aldol condensation:
  Base: enolate attacks another carbonyl → aldol product
  Heat: dehydration → α,β-unsaturated carbonyl (conjugated)
  Mixed aldol: use preformed enolate + different aldehyde
  Intramolecular: ring-forming (Haworth synthesis)

Claisen condensation:
  Ester + base → β-ketoester
  Dieckmann: intramolecular Claisen → cyclic β-ketoester
```

---

## Aromatic Chemistry
```
Aromaticity (Hückel rule):
  Cyclic, planar, fully conjugated, 4n+2 π electrons
  Benzene: 6π electrons (n=1) ✓
  Cyclopentadienyl anion: 6π ✓
  Tropylium cation: 6π ✓
  Cyclooctatetraene: 8π (antiaromatic! n=1 for 4n)

Electrophilic Aromatic Substitution (EAS):
  Mechanism: E⁺ attacks ring → arenium ion → deprotonation
  Halogenation: ArH + X₂/FeX₃ → ArX + HX
  Nitration: ArH + HNO₃/H₂SO₄ → ArNO₂
  Sulfonation: ArH + SO₃/H₂SO₄ → ArSO₃H  (reversible)
  Friedel-Crafts alkylation: ArH + RX/AlCl₃ → ArR
  Friedel-Crafts acylation: ArH + RCOCl/AlCl₃ → ArCOR

Directing effects:
  ortho/para directors (activate ring):
    -OH, -OR, -NR₂, -NHR, -NH₂ (strong activators)
    -R, -Ph (weak activators)
    -X (halogens: deactivate but o/p direct via lone pairs)
  meta directors (deactivate ring):
    -NO₂, -CN, -COOH, -COR, -SO₃H, -CF₃, -NR₃⁺

Nucleophilic Aromatic Substitution (NAS):
  Requires electron-withdrawing groups ortho/para to LG
  Addition-elimination mechanism (Meisenheimer complex)
  Benzyne mechanism at high T (elimination-addition)
```

---

## Spectroscopic Identification
```python
def ir_spectroscopy():
    return {
        'O-H stretch':      '3200-3550 cm⁻¹ (broad, alcohol)',
        'N-H stretch':      '3300-3500 cm⁻¹',
        'C-H stretch':      '2850-3000 cm⁻¹ (sp³), 3000-3100 (sp²)',
        'C≡N stretch':      '2200-2260 cm⁻¹',
        'C≡C stretch':      '2100-2260 cm⁻¹',
        'C=O stretch':      '1630-1870 cm⁻¹ (carbonyl fingerprint)',
        'Aldehyde C=O':     '1720-1740 cm⁻¹',
        'Ketone C=O':       '1705-1725 cm⁻¹',
        'Ester C=O':        '1735-1750 cm⁻¹',
        'Amide C=O':        '1630-1690 cm⁻¹',
        'Acid C=O':         '1700-1725 cm⁻¹ + broad OH',
        'C=C stretch':      '1620-1680 cm⁻¹',
        'Aromatic C=C':     '1450-1600 cm⁻¹',
        'C-O stretch':      '1000-1300 cm⁻¹',
        'C-X stretch':      '500-800 cm⁻¹'
    }

def nmr_chemical_shifts():
    return {
        'TMS reference':    '0 ppm',
        'Alkyl CH₃':        '0.9 ppm',
        'Alkyl CH₂':        '1.2-1.4 ppm',
        'Allylic CH₂':      '1.6-2.2 ppm',
        'C=O adjacent CH': '2.0-2.5 ppm',
        'N-CH':             '2.2-2.9 ppm',
        'O-CH₂ (ether)':    '3.3-3.5 ppm',
        'O-CH₂ (ester)':    '3.7-4.1 ppm',
        'Vinyl CH':         '4.5-6.5 ppm',
        'Aromatic CH':      '6.5-8.5 ppm',
        'Aldehyde CHO':     '9.5-10 ppm',
        'Carboxylic COOH':  '10-12 ppm',
        'OH (variable)':    '1-5 ppm',
        'NH (variable)':    '1-8 ppm'
    }

def mass_spectrometry():
    return {
        'M+': 'Molecular ion — gives MW',
        'M+1': 'One ¹³C (1.1% per carbon)',
        'M+2': 'Bromine (+2, ~1:1 ratio), Chlorine (+2, ~3:1)',
        'Base peak': 'Most abundant fragment',
        'Common losses': {
            '-15': 'Loss of CH₃',
            '-18': 'Loss of H₂O',
            '-28': 'Loss of CO (aldehyde/ketone)',
            '-29': 'Loss of CHO',
            '-31': 'Loss of OCH₃',
            '-45': 'Loss of OEt'
        },
        'McLafferty': 'γ-H transfer in carbonyl compounds'
    }
```

---

## Named Reactions
```python
def named_reactions():
    return {
        'Grignard': 'RMgX + carbonyl → alcohol (C-C bond formation)',
        'Wittig':   'Ph₃P=CHR + carbonyl → alkene (no OH byproduct)',
        'Diels-Alder': 'Diene + dienophile → cyclohexene [4+2]',
        'Aldol':    'Enolate + carbonyl → β-hydroxy carbonyl',
        'Claisen':  'Ester enolate + ester → β-ketoester',
        'Michael':  'Nucleophile + α,β-unsaturated carbonyl (conjugate add)',
        'Robinson annulation': 'Michael + Aldol → cyclohexenone',
        'Beckmann': 'Oxime → amide (acid-catalyzed rearrangement)',
        'Baeyer-Villiger': 'Ketone + peracid → ester/lactone',
        'Fries':    'Phenol ester → hydroxyaryl ketone (Lewis acid)',
        'Curtius':  'Acyl azide → isocyanate (rearrangement)',
        'Hofmann':  'Amide + Br₂/NaOH → amine (lose CO)',
        'Birch':    'Aromatic + Na/NH₃/ROH → 1,4-cyclohexadiene',
        'Sharpless': 'Asymmetric epoxidation (Ti, tartrate)',
        'Metathesis': 'Grubbs catalyst, olefin exchange',
        'Heck':     'Pd-catalyzed C-C coupling (aryl halide + alkene)',
        'Suzuki':   'Pd-catalyzed coupling (aryl halide + boronate)',
        'Sonogashira': 'Pd/Cu coupling (aryl halide + terminal alkyne)',
        'Swern':    'Oxalyl chloride/DMSO oxidation of alcohol → aldehyde',
        'Jones':    'CrO₃/H₂SO₄ oxidation → ketone/acid',
        'Ozonolysis': 'O₃ cleaves alkene → carbonyls'
    }
```

---

## Retrosynthetic Analysis
```
Retrosynthesis: work backward from target to starting materials
Arrow convention: ⟹ means "can be made from"

Disconnection strategies:
  1. Identify key bonds to form (C-C bonds most valuable)
  2. Classify: C-C, C-O, C-N, C-X
  3. Choose appropriate reaction

Common disconnections:
  Alcohol ← Grignard addition, NaBH₄ reduction
  Alkene ← Wittig, elimination, metathesis
  Ester ← Fischer esterification, acid chloride + ROH
  Amine ← reductive amination, amide reduction
  C-C α to carbonyl ← aldol, Claisen, Michael
  Cyclohexenone ← Robinson annulation
  Cyclohexene ← Diels-Alder

Functional group interconversion (FGI):
  Change FG to reveal better disconnection
  Oxidation states: alcohol → aldehyde → acid
  Protection: if multiple reactive FG present

Example retrosynthesis:
  Target: PhCH₂CH(OH)CH₃
  Disconnect C-C: PhCH₂⁻ + CH₃CHO  OR  PhCH₂MgBr + acetaldehyde
  → React PhCH₂Br with Mg, then add CH₃CHO
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Markovnikov confusion | H goes to carbon with MORE H (more substituted carbocation) |
| SN1 vs SN2 substrate | Primary → SN2, Tertiary → SN1/E1, Secondary → depends |
| Anti addition forgotten | Bromine addition gives anti product via halonium ion |
| R/S assignment errors | Always point lowest priority AWAY before reading direction |
| Enolate regioselectivity | LDA (−78°C, kinetic), NaOEt (thermodynamic enolate) |
| EAS directing confusion | Deactivating groups are meta directors (except halogens) |

---

## Related Skills

- **inorganic-chemistry-expert**: Organometallic, coordination chemistry
- **physical-chemistry-expert**: Thermodynamics and kinetics of reactions
- **biochemistry-expert**: Biological organic chemistry
- **analytical-chemistry-expert**: Advanced spectroscopy
- **medicinal-chemistry-expert**: Drug synthesis and SAR
- **polymer-chemistry-expert**: Polymerization mechanisms
