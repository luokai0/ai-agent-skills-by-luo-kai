---
author: luo-kai
name: inorganic-chemistry-expert
description: Expert-level inorganic chemistry knowledge. Use when working with coordination chemistry, transition metals, crystal field theory, organometallics, main group chemistry, solid state chemistry, acid-base theory, or inorganic reaction mechanisms. Also use when the user mentions 'coordination complex', 'ligand', 'crystal field', 'transition metal', 'oxidation state', 'organometallic', 'Lewis acid', 'VSEPR', 'symmetry', 'point group', 'solid state', or 'catalysis'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Inorganic Chemistry Expert

You are a world-class inorganic chemist with deep expertise in coordination chemistry, transition metal chemistry, organometallics, main group chemistry, solid state chemistry, symmetry, and inorganic reaction mechanisms.

## Before Starting

1. **Topic** — Coordination chemistry, main group, solid state, organometallics, or symmetry?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Solve problem, predict properties, or understand concept?
4. **Context** — Academic, catalysis, materials, or bioinorganic?
5. **Focus** — Structure, bonding, reactivity, or spectroscopy?

---

## Core Expertise Areas

- **Coordination Chemistry**: ligands, coordination numbers, isomerism
- **Crystal Field Theory**: d-orbital splitting, colors, magnetism
- **Molecular Orbital Theory**: ligand field theory, MO diagrams
- **Organometallics**: 18-electron rule, oxidative addition, reductive elimination
- **Main Group Chemistry**: periodic trends, reactions, structures
- **Solid State**: crystal structures, band theory, ionic solids
- **Symmetry & Group Theory**: point groups, character tables, selection rules
- **Acid-Base Theory**: Lewis, Bronsted, HSAB principle

---

## Periodic Table Trends
```
Atomic radius:
  Increases down group (more shells)
  Decreases across period (more nuclear charge, same shell)
  Lanthanide contraction: 4f electrons poor shielding →
    5d elements smaller than expected → Zr/Hf similar size

Ionization energy:
  Increases across period (more nuclear charge)
  Decreases down group (outer electrons farther away)
  Anomalies: Be > B (2s vs 2p), N > O (half-filled 2p stable)

Electronegativity:
  F highest (4.0), Cs lowest (~0.7)
  Increases across period, decreases down group

Oxidation states:
  Transition metals: multiple states common (Fe: 0,+2,+3,+4,+6)
  Main group: usually fixed (Na: +1, Mg: +2, Al: +3)
  High OS: strong oxidizers (MnO₄⁻: Mn⁷⁺, Cr₂O₇²⁻: Cr⁶⁺)

Periodic trends summary:
  → (left to right): EN↑, IP↑, EA↑, radius↓, metallic character↓
  ↓ (top to bottom): EN↓, IP↓, EA↓, radius↑, metallic character↑
```

---

## Coordination Chemistry
```
Coordination complex: metal center + ligands
  [M(L)n]^charge  notation
  Coordination number (CN): number of donor atoms attached to metal

Common coordination numbers and geometries:
  CN 2: linear (Ag⁺, Au⁺) — [Ag(NH₃)₂]⁺
  CN 4: tetrahedral or square planar
    Tetrahedral: d⁰, d⁵, d¹⁰, weak field
    Square planar: d⁸ (Ni²⁺, Pd²⁺, Pt²⁺, Au³⁺), strong field
  CN 6: octahedral (most common) — majority of TM complexes

Ligand types:
  Monodentate: one donor atom (NH₃, Cl⁻, H₂O, CN⁻, CO)
  Bidentate: two donor atoms (en, ox²⁻, bipy)
  Tridentate: three (dien, terpy)
  Tetradentate: four (trien, salen)
  Hexadentate: six (EDTA⁴⁻)
  Bridging: connects two metals (μ-Cl, μ-OH)

Chelate effect:
  Chelating ligands form more stable complexes than monodentate
  Entropic advantage: fewer molecules → higher entropy of reaction
  EDTA forms very stable complexes (6 donor atoms)

Isomerism:
  Structural isomers:
    Ionization: [Co(NH₃)₅Br]SO₄ vs [Co(NH₃)₅SO₄]Br
    Linkage: [Co(NH₃)₅NO₂]²⁺ (N-bonded) vs [Co(NH₃)₅ONO]²⁺ (O-bonded)
  Stereoisomers:
    Geometric (cis/trans, fac/mer)
    Optical (Δ/Λ for tris-chelate octahedral)
```

---

## Crystal Field Theory (CFT)
```
d-orbital splitting in octahedral field:
  eg (dx²-y², dz²): point directly at ligands → HIGHER energy
  t₂g (dxy, dxz, dyz): point between ligands → LOWER energy

  Crystal field splitting: Δo (10 Dq)
  eg above average by 6 Dq (+0.6Δo)
  t₂g below average by 4 Dq (-0.4Δo)

Strong vs weak field:
  Strong field ligands: large Δo → low spin
  Weak field ligands: small Δo → high spin
  Pairing energy P: cost to pair electrons in same orbital

Spectrochemical series (increasing Δo):
  I⁻ < Br⁻ < Cl⁻ < F⁻ < OH⁻ < H₂O < NH₃ < en < bipy < CN⁻ < CO

  Halides, O-donors: weak field
  N-donors, CO, CN⁻: strong field

Crystal field stabilization energy (CFSE):
  CFSE = n(t₂g)×(-0.4Δo) + n(eg)×(+0.6Δo) - P(if paired)

d-orbital splitting:
  Tetrahedral: Δt = 4/9 Δo (opposite splitting, t₂ above e)
  Square planar: from octahedral, remove two axial ligands

Colors:
  Complex absorbs complementary color to what we see
  Color wheel: red-green, orange-blue, yellow-violet
  d-d transitions: allowed but weak (Laporte forbidden)
  Charge transfer: intense colors (MnO₄⁻ purple, CrO₄²⁻ yellow)

Magnetism:
  Unpaired electrons → paramagnetic
  μ = √(n(n+2)) BM  (n = unpaired electrons)
  All paired → diamagnetic
  High spin d⁵ (Fe³⁺): 5 unpaired, μ = 5.92 BM
  Low spin d⁶ (Fe²⁺, CO): 0 unpaired, diamagnetic
```

---

## Organometallic Chemistry
```
18-Electron Rule:
  Stable organometallics tend to have 18 electrons
  (analogous to noble gas configuration)
  Count: metal d electrons + electrons from all ligands

Ligand electron contributions:
  2e donors: CO, PR₃, NH₃, H₂O, RNC, alkene (η²)
  2e donors (anionic): H⁻, Cl⁻, R⁻, OR⁻, NR₂⁻
  4e donors: butadiene (η⁴), cyclobutadiene (η⁴)
  5e donors: Cp⁻ (η⁵-cyclopentadienyl)
  6e donors: benzene (η⁶), CO₃²⁻

Examples:
  Cr(CO)₆: Cr⁰ (6e) + 6 CO (12e) = 18e ✓
  Fe(CO)₅: Fe⁰ (8e) + 5 CO (10e) = 18e ✓
  Ni(CO)₄: Ni⁰ (10e) + 4 CO (8e) = 18e ✓
  Cp₂Fe (ferrocene): Fe²⁺ (6e) + 2 Cp⁻ (10e) = 16e (18 with ionic)

Key reactions:
  Oxidative addition:
    M(n) + X-Y → M(n+2)(X)(Y)
    Metal oxidation state increases by 2, CN increases by 2
    Requires: coordinatively unsaturated, electron-rich metal

  Reductive elimination:
    M(X)(Y) → M + X-Y  (reverse of OA)
    Forms C-C, C-H, C-X bonds
    Requires: X,Y cis to each other

  Migratory insertion:
    M-CO + M-R → M-COR  (1,2-insertion)
    CO insertion into M-C bond

  β-hydride elimination:
    M-CH₂CH₃ → M-H + CH₂=CH₂
    Requires: β-H, empty coordination site, syn coplanar geometry
    Major decomposition pathway for alkyl complexes

Catalytic cycles:
  Hydrogenation (Wilkinson's catalyst RhCl(PPh₃)₃):
    OA (H₂) → alkene coordination → insertion → RE (alkane)
  Hydroformylation (oxo process):
    CO + H₂ + alkene → aldehyde (Rh or Co catalyst)
  Wacker process:
    CH₂=CH₂ + O₂ → CH₃CHO (Pd catalyst)
  Heck, Suzuki, Negishi: Pd-catalyzed C-C couplings
```

---

## Symmetry & Group Theory
```
Symmetry elements:
  E: identity (all molecules)
  Cn: rotation axis (n-fold: 360°/n)
  σ: mirror plane (σh: horizontal, σv: vertical, σd: dihedral)
  i: inversion center
  Sn: improper rotation axis

Point groups:
  C₁: no symmetry (chiral molecules)
  Cs: only σ
  Ci: only i
  Cn: only Cn axis
  Cnv: Cn + nσv (H₂O: C₂v, NH₃: C₃v)
  Cnh: Cn + σh
  Dn: Cn + nC₂⊥
  Dnh: Dn + σh (BF₃: D₃h, benzene: D₆h)
  Dnd: Dn + nσd (allene: D₂d, ferrocene staggered: D₅d)
  T, Td, Th: tetrahedral (CH₄: Td)
  O, Oh: octahedral (SF₆: Oh)
  Ih: icosahedral (buckminsterfullerene C₆₀: Ih)

Determining point group:
  1. Linear? → C∞v or D∞h
  2. Multiple high-order axes? → T, O, or I
  3. Find principal axis Cn
  4. nC₂⊥ to Cn? → D type
  5. σh? → Cnh or Dnh
  6. nσv or nσd? → Cnv or Dnd

Character tables:
  Irreducible representations label symmetry of orbitals/vibrations
  A, B: non-degenerate; E: doubly degenerate; T: triply degenerate
  Subscripts: 1 (symmetric to C₂), 2 (antisymmetric)
  Superscripts: ′ (symmetric to σh), ″ (antisymmetric)
  g (gerade): symmetric to i; u (ungerade): antisymmetric to i

Applications:
  Selection rules: IR active if change in dipole (same symmetry as x,y,z)
  Raman active: change in polarizability (quadratic functions)
  MO theory: only orbitals of same symmetry can mix
```

---

## Acid-Base Chemistry
```
Arrhenius: acids produce H⁺, bases produce OH⁻ (aqueous only)

Bronsted-Lowry:
  Acid: proton donor, Base: proton acceptor
  Conjugate pairs: HA/A⁻, BH⁺/B

Lewis:
  Acid: electron pair acceptor (BF₃, AlCl₃, H⁺, metal ions)
  Base: electron pair donor (NH₃, F⁻, OH⁻, lone pair donors)

HSAB (Hard and Soft Acids and Bases):
  Hard acids: small, high charge, not polarizable (H⁺, Li⁺, Mg²⁺, Al³⁺, Cr³⁺)
  Soft acids: large, low charge, polarizable (Cu⁺, Ag⁺, Pd²⁺, Pt²⁺, Hg²⁺)
  Hard bases: small, high EN, not polarizable (F⁻, OH⁻, H₂O, NH₃, CO₃²⁻)
  Soft bases: large, low EN, polarizable (I⁻, RS⁻, CN⁻, CO, PR₃)

Principle: Hard prefers Hard, Soft prefers Soft
  AgF (soft/hard): unstable, AgI (soft/soft): very stable
  Fe³⁺ (hard) prefers F⁻, O²⁻; Fe²⁺ (borderline) also S²⁻
  Applications: predicting stability, solubility, reactivity

Acidity in inorganic:
  Binary hydrides: acidity increases across period, down group
    HF < HCl < HBr < HI (bond strength dominates down group)
  Oxoacids: more O on central atom → stronger acid
    H₂SO₄ > H₂SO₃, HNO₃ > HNO₂, HClO₄ > HClO₃ > HClO₂ > HClO
```

---

## Main Group Chemistry
```python
def main_group_reactions():
    return {
        'Group 1 (Alkali metals)': {
            'reactions':    '2M + 2H₂O → 2MOH + H₂↑',
            'trend':        'Reactivity increases down group (Cs most reactive)',
            'flame colors': 'Li: red, Na: yellow, K: violet, Rb: red-violet'
        },
        'Group 2 (Alkaline earths)': {
            'reactions':    'M + 2H₂O → M(OH)₂ + H₂↑ (Ca, Sr, Ba)',
            'CaCO₃':        'CaCO₃ → CaO + CO₂ (calcination at 900°C)',
            'hardness':     'Temporary (HCO₃⁻) and permanent (SO₄²⁻) hardness'
        },
        'Group 13': {
            'Al':           'Amphoteric: reacts with both acids and bases',
            'B':            'Electron deficient, Lewis acid, forms boranes',
            'BF₃':          'Classic Lewis acid, forms adducts BF₃·NH₃'
        },
        'Group 14': {
            'C':            'Allotropes: diamond, graphite, fullerenes, graphene',
            'Si':           'SiO₂ network solid, silicates, silicones',
            'Sn/Pb':        'Amphoteric oxides, +2 and +4 states'
        },
        'Group 15 (Pnictogens)': {
            'N₂':           'Triple bond (945 kJ/mol), very unreactive',
            'NO':           'Radical, bent geometry, important signaling molecule',
            'HNO₃':         'Strong acid, oxidizing agent (Cu, Ag dissolve)',
            'P allotropes': 'White P₄ (reactive), red P (polymeric), black P'
        },
        'Group 16 (Chalcogens)': {
            'O₃':           'Ozone: bent, 117°, oxidizing, UV absorption',
            'H₂O':          'Anomalous properties: H-bonding, high bp/mp',
            'H₂SO₄':        'Dehydrating agent, strong diprotic acid, oleum'
        },
        'Group 17 (Halogens)': {
            'F₂':           'Most electronegative, most oxidizing, attacks glass',
            'Cl₂':          'Cl₂ + H₂O → HCl + HOCl (disproportionation)',
            'interhalides': 'ClF, BrF₃, IF₇ (high coordination possible for heavy)'
        },
        'Group 18 (Noble gases)': {
            'reactivity':   'Kr, Xe: can form compounds with F, O',
            'XeF₂':         'Linear, sp³d, 3 lone pairs',
            'XeF₄':         'Square planar',
            'XeO₃':         'Pyramidal, explosive'
        }
    }
```

---

## Solid State Chemistry
```
Crystal structures:
  Rock salt (NaCl): FCC anions, octahedral holes for cations
    radius ratio: 0.414-0.732
  Cesium chloride (CsCl): simple cubic, cubic holes
    radius ratio: > 0.732
  Zinc blende (ZnS): FCC S²⁻, tetrahedral holes for Zn²⁺
    radius ratio: 0.225-0.414
  Fluorite (CaF₂): FCC Ca²⁺, all tetrahedral holes for F⁻
  Perovskite (CaTiO₃): mixed oxide, superconductor-related structures
  Spinel (AB₂O₄): complex oxide, magnetic materials

Lattice energy:
  U = -Mz⁺z⁻e²NA/4πε₀r₀ × (1 - 1/n)  (Born-Mayer)
  M = Madelung constant (depends on structure)
  NaCl: M = 1.748, CsCl: M = 1.763, ZnS: M = 1.638
  Born-Haber cycle: uses lattice energy thermodynamically

Defects:
  Schottky: equal cation and anion vacancies (ionic radius similar)
  Frenkel: cation displaced to interstitial site (small cation)
  Non-stoichiometry: Fe₁₋ₓO (wustite), variable composition

Band theory (solid state):
  Metals: partially filled band (or overlap)
  Insulators: large band gap (>4 eV)
  Semiconductors: small gap (1-3 eV)
  Doping: n-type (donor) or p-type (acceptor)
```

---

## Bioinorganic Chemistry
```
Essential metal ions in biology:
  Na⁺, K⁺: nerve impulse, osmotic balance
  Ca²⁺: muscle contraction, signaling, bone
  Mg²⁺: ATP cofactor, chlorophyll center
  Fe: hemoglobin (O₂ transport), cytochromes (electron transfer)
  Zn: carbonic anhydrase, carboxypeptidase (structural/catalytic)
  Cu: cytochrome c oxidase, plastocyanin, ceruloplasmin
  Co: vitamin B₁₂ (cobalamin), coenzyme
  Mo: nitrogenase (N₂ fixation), xanthine oxidase
  Mn: photosystem II (O₂ evolution), arginase

Hemoglobin:
  Fe²⁺ in porphyrin ring (heme)
  High spin (deoxy) → low spin (oxy): σ-donor O₂
  Cooperative binding: sigmoidal O₂ saturation curve
  CO binds 240× stronger than O₂ → CO poisoning

Nitrogen fixation:
  N₂ + 8H⁺ + 8e⁻ + 16 ATP → 2NH₃ + H₂ + 16 ADP + 16 Pi
  Nitrogenase enzyme: Fe-Mo cofactor (FeMoco)
  Industrial: Haber-Bosch (Fe catalyst, 450°C, 200 atm)
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Oxidation state in complex | Count electrons carefully: metal charge = complex charge - ligand charges |
| CFSE calculation sign | t₂g electrons negative, eg electrons positive contribution |
| 18-electron rule exceptions | d⁸ square planar complexes stable at 16e (Rh, Ir, Pd, Pt) |
| Point group assignment | Systematic: linear? → high symmetry? → Cn? → C₂⊥? → σ? |
| Hard/soft prediction | HSAB predicts stability, not solubility alone |
| Geometric vs optical isomers | Square planar: cis/trans but NOT optical; octahedral tris-chelate: optical |

---

## Related Skills

- **organic-chemistry-expert**: Organometallic mechanisms
- **physical-chemistry-expert**: Thermodynamics and bonding theory
- **solid-state-physics**: Band theory connection
- **analytical-chemistry-expert**: Spectroscopic methods
- **biochemistry-expert**: Metalloenzymes and bioinorganic
