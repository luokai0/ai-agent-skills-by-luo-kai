---
author: luo-kai
name: biochemistry-expert
description: Expert-level biochemistry knowledge. Use when working with proteins, enzymes, metabolism, DNA, RNA, carbohydrates, lipids, cell signaling, or bioenergetics. Also use when the user mentions 'enzyme kinetics', 'metabolism', 'glycolysis', 'Krebs cycle', 'DNA replication', 'protein folding', 'amino acids', 'ATP', 'oxidative phosphorylation', 'gene expression', 'lipid bilayer', or 'signal transduction'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Biochemistry Expert

You are a world-class biochemist with deep expertise in protein structure and function, enzyme kinetics, metabolism, molecular biology, cell signaling, bioenergetics, and the chemical basis of life.

## Before Starting

1. **Topic** — Proteins, metabolism, nucleic acids, lipids, or cell signaling?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Goal** — Understand pathway, solve problem, or analyze mechanism?
4. **Context** — Medical, research, pharmaceutical, or academic?
5. **Focus** — Structure, function, regulation, or disease?

---

## Core Expertise Areas

- **Amino Acids & Proteins**: structure, folding, function, techniques
- **Enzyme Kinetics**: Michaelis-Menten, inhibition, regulation
- **Carbohydrate Metabolism**: glycolysis, gluconeogenesis, glycogen
- **Lipid Metabolism**: fatty acid oxidation, synthesis, membranes
- **Krebs Cycle & Oxidative Phosphorylation**: ATP synthesis, electron transport
- **Nucleic Acids**: DNA/RNA structure, replication, transcription, translation
- **Cell Signaling**: receptors, second messengers, kinase cascades
- **Bioenergetics**: thermodynamics, coupled reactions, free energy

---

## Amino Acids & Protein Structure
```
20 standard amino acids:
  Nonpolar/hydrophobic: Gly(G), Ala(A), Val(V), Leu(L), Ile(I),
                        Pro(P), Phe(F), Trp(W), Met(M)
  Polar uncharged:      Ser(S), Thr(T), Cys(C), Tyr(Y), Asn(N), Gln(Q)
  Positively charged:   Lys(K), Arg(R), His(H)  (basic)
  Negatively charged:   Asp(D), Glu(E)  (acidic)

Amino acid chemistry:
  General structure: H₂N-CHR-COOH  (α-carbon with R group)
  Zwitterion at physiological pH
  pKa: α-COOH ~2, α-NH₃⁺ ~9-10, R groups variable
  Henderson-Hasselbalch: pH = pKa + log([A⁻]/[HA])

Protein structure levels:
  Primary:   amino acid sequence (covalent peptide bonds)
  Secondary: local regular structures
    α-helix: 3.6 residues/turn, H-bonds i to i+4
    β-sheet: parallel or antiparallel, H-bonds between strands
    β-turn: reverses chain direction, H-bond i to i+3
    Random coil: no regular structure
  Tertiary:  overall 3D fold (hydrophobic core, disulfide bonds, H-bonds)
  Quaternary: multiple subunits (hemoglobin: 2α+2β)

Forces stabilizing structure:
  Hydrophobic effect: nonpolar residues buried (dominant)
  H-bonds: backbone and side chains
  Electrostatic: salt bridges, charge-charge
  Van der Waals: weak, short-range
  Disulfide bonds: covalent, extracellular proteins

Protein folding:
  Anfinsen's dogma: sequence determines structure
  Chaperones (Hsp70, GroEL): prevent misfolding
  Prions: misfolded proteins that propagate (PrPSc)
  Amyloids: β-sheet aggregates (Alzheimer's Aβ, Parkinson's α-syn)
```

---

## Enzyme Kinetics
```
Michaelis-Menten:
  E + S ⇌ ES → E + P
  v = Vmax[S] / (Km + [S])
  Vmax = kcat[E]total
  Km ≈ affinity (lower Km = higher affinity)
  kcat = turnover number (catalytic efficiency)
  kcat/Km = specificity constant (catalytic efficiency)

Lineweaver-Burk (double reciprocal):
  1/v = (Km/Vmax)(1/[S]) + 1/Vmax
  Y-intercept = 1/Vmax, X-intercept = -1/Km, slope = Km/Vmax

Inhibition types:
  Competitive:
    Inhibitor binds active site, competes with substrate
    Km increases, Vmax unchanged
    1/v = (Km/Vmax)(1+[I]/Ki)(1/[S]) + 1/Vmax
    Overcome by high [S]

  Uncompetitive:
    Inhibitor binds only ES complex
    Both Km and Vmax decrease (ratio stays same)
    Parallel lines on Lineweaver-Burk

  Noncompetitive:
    Inhibitor binds E or ES, not active site
    Vmax decreases, Km unchanged
    Same X-intercept on Lineweaver-Burk

  Mixed:
    Inhibitor binds E and ES with different affinities
    Both Km and Vmax change

Allosteric regulation:
  Effectors bind at sites other than active site
  Sigmoidal kinetics: v = Vmax[S]ⁿ/(K₀.₅ⁿ + [S]ⁿ)
  n = Hill coefficient (>1 = positive cooperativity)
  Feedback inhibition: end product inhibits first enzyme
  Feedforward activation: substrate activates downstream enzyme

Enzyme mechanisms:
  Acid-base catalysis: active site residues as H⁺ donors/acceptors
  Covalent catalysis: Ser, Cys, Lys form covalent intermediates
  Metal ion catalysis: Lewis acid activation, redox
  Proximity/orientation: bring substrates together correctly
  Transition state stabilization: reduce Ea by binding TS tightly
```

---

## Carbohydrate Metabolism
```python
def glycolysis_overview():
    """
    Glycolysis: glucose → 2 pyruvate
    Location: cytoplasm
    Net: 2 ATP, 2 NADH per glucose
    """
    steps = {
        1:  'Glucose + ATP → Glucose-6-phosphate (hexokinase/glucokinase)',
        2:  'G6P → Fructose-6-phosphate (phosphoglucose isomerase)',
        3:  'F6P + ATP → Fructose-1,6-bisphosphate (PFK-1) [KEY REGULATORY STEP]',
        4:  'F1,6BP → DHAP + Glyceraldehyde-3-phosphate (aldolase)',
        5:  'DHAP → G3P (triose phosphate isomerase)',
        6:  'G3P + NAD⁺ + Pi → 1,3-BPG + NADH (G3P dehydrogenase)',
        7:  '1,3-BPG + ADP → 3-phosphoglycerate + ATP (substrate level phosphorylation)',
        8:  '3-PG → 2-phosphoglycerate (phosphoglycerate mutase)',
        9:  '2-PG → PEP + H₂O (enolase)',
        10: 'PEP + ADP → Pyruvate + ATP (pyruvate kinase) [REGULATORY]'
    }
    return {
        'steps': steps,
        'net_ATP': 2,
        'net_NADH': 2,
        'regulation': 'PFK-1 (activated by AMP, F2,6BP; inhibited by ATP, citrate)',
        'pyruvate_fate': {
            'aerobic':      'Pyruvate → Acetyl-CoA (pyruvate dehydrogenase)',
            'anaerobic':    'Pyruvate → Lactate (lactate dehydrogenase)',
            'yeast':        'Pyruvate → Ethanol + CO₂'
        }
    }

def tca_cycle():
    """
    Krebs/TCA cycle: Acetyl-CoA → CO₂
    Location: mitochondrial matrix
    Per turn: 3 NADH, 1 FADH₂, 1 GTP, 2 CO₂
    """
    return {
        'entry':    'Acetyl-CoA (2C) + Oxaloacetate (4C) → Citrate (6C)',
        'steps': {
            1: 'Acetyl-CoA + OAA → Citrate (citrate synthase)',
            2: 'Citrate → Isocitrate (aconitase)',
            3: 'Isocitrate → α-ketoglutarate + CO₂ + NADH (isocitrate dehydrogenase)',
            4: 'α-KG → Succinyl-CoA + CO₂ + NADH (α-KG dehydrogenase)',
            5: 'Succinyl-CoA → Succinate + GTP (succinyl-CoA synthetase)',
            6: 'Succinate → Fumarate + FADH₂ (succinate dehydrogenase)',
            7: 'Fumarate → Malate (fumarase)',
            8: 'Malate → OAA + NADH (malate dehydrogenase)'
        },
        'per_turn': '3 NADH, 1 FADH₂, 1 GTP, 2 CO₂',
        'per_glucose': '6 NADH, 2 FADH₂, 2 GTP (2 turns)',
        'regulation': 'Inhibited by ATP, NADH; activated by ADP, NAD⁺, Ca²⁺'
    }
```

---

## Oxidative Phosphorylation
```
Electron Transport Chain (ETC):
  Location: inner mitochondrial membrane
  NADH → Complex I → CoQ → Complex III → Cyt c → Complex IV → O₂
  FADH₂ → Complex II → CoQ → Complex III → ...

  Complex I (NADH dehydrogenase): NADH → NAD⁺, pumps 4H⁺
  Complex II (succinate dehydrogenase): FADH₂ → FAD (no pumping)
  Complex III (cytochrome bc₁): pumps 4H⁺
  Complex IV (cytochrome c oxidase): pumps 2H⁺, reduces O₂ → H₂O

Chemiosmotic theory (Mitchell):
  H⁺ gradient (proton motive force) drives ATP synthesis
  ΔG = -2.303RT·log([H⁺]in/[H⁺]out) + ZFΔψ
  PMF drives ATP synthase (Complex V)

ATP synthase (Complex V):
  F₀ (membrane): c-ring rotates driven by H⁺ flow
  F₁ (matrix): α₃β₃ catalytic hexamer, 3 ATPs per 360° rotation
  ~2.7 H⁺ per ATP (c-ring has 8-15 subunits depending on species)

ATP yield per glucose (approximate):
  Glycolysis: 2 ATP + 2 NADH (cytoplasmic)
  Pyruvate → Acetyl-CoA: 2 NADH (mitochondrial)
  TCA cycle: 6 NADH + 2 FADH₂ + 2 GTP
  ETC: NADH → 2.5 ATP, FADH₂ → 1.5 ATP
  Total: ~30-32 ATP per glucose (theoretical maximum)

Uncoupling:
  Proton leak bypasses ATP synthase → heat not ATP
  Uncoupling proteins (UCP1): brown adipose tissue thermogenesis
  Dinitrophenol (DNP): artificial uncoupler (historically used for weight loss)
```

---

## Lipid Metabolism
```
Fatty acid oxidation (β-oxidation):
  Location: mitochondrial matrix
  Activated: Fatty acid + CoA + ATP → Acyl-CoA + AMP + PPi
  Each cycle removes 2C as Acetyl-CoA:
    Acyl-CoA → trans-Δ²-Enoyl-CoA (FAD → FADH₂)
    → L-3-Hydroxyacyl-CoA (H₂O addition)
    → 3-Ketoacyl-CoA (NAD⁺ → NADH)
    → Acetyl-CoA + shorter Acyl-CoA (thiolysis)

  Palmitate (16C): 7 cycles → 8 Acetyl-CoA + 7 FADH₂ + 7 NADH
  ATP from palmitate: 7×1.5 + 7×2.5 + 8×10 - 2 (activation) = 106 ATP

Ketone bodies:
  Formed in liver during fasting from excess Acetyl-CoA
  Acetoacetate, β-hydroxybutyrate, acetone
  Exported to brain, heart, muscle as fuel
  Diabetic ketoacidosis: uncontrolled ketone production

Fatty acid synthesis:
  Location: cytoplasm
  Acetyl-CoA (mitochondria) → citrate shuttle → cytoplasm
  Acetyl-CoA + CO₂ + ATP → Malonyl-CoA (ACC, rate-limiting)
  FAS (fatty acid synthase): adds 2C units as Malonyl-CoA
  Net: 8 Acetyl-CoA + 7 ATP + 14 NADPH → Palmitate

Membrane lipids:
  Phospholipids: glycerol backbone, 2 FA, phosphate headgroup
  Sphingolipids: sphingosine backbone (ceramide core)
  Cholesterol: 4 fused rings, membrane fluidity, steroid precursor
  Fluid mosaic model: lateral diffusion in bilayer
```

---

## Nucleic Acids & Molecular Biology
```
DNA structure:
  B-DNA: right-handed double helix, 10 bp/turn, 3.4 Å/bp
  A-T: 2 H-bonds, G-C: 3 H-bonds
  Antiparallel strands: 5′→3′ and 3′→5′
  Major groove: wide, protein binding sites
  Minor groove: narrow

DNA replication:
  Semiconservative: each daughter has one old + one new strand
  Origin of replication: ORC complex binds
  Helicase: unwinds DNA (ATP-dependent)
  SSB proteins: stabilize single strands
  Primase: synthesizes RNA primer (no proofreading needed for start)
  DNA Pol III: main replicase, 5′→3′, proofreads 3′→5′
  DNA Pol I: removes RNA primer, gap fills
  Ligase: seals nicks (NAD⁺ or ATP)
  Leading strand: continuous synthesis
  Lagging strand: Okazaki fragments (5′→3′ synthesis away from fork)
  Telomerase: extends telomeres (TERT reverse transcriptase)

Transcription (prokaryotes):
  Sigma factor: recognizes promoter (-10 and -35 elements)
  RNA polymerase: no primer needed, synthesizes 5′→3′
  Termination: rho-independent (stem-loop) or rho-dependent

Transcription (eukaryotes):
  RNA Pol II: mRNA synthesis, promoter = TATA box (~-25)
  General transcription factors: TFIID, TFIIB, etc.
  5′ cap (7-methylguanosine): added co-transcriptionally
  Poly-A tail: added after cleavage at AAUAAA signal
  Splicing: introns removed by spliceosome (snRNPs)
  Alternative splicing: one gene → multiple proteins

Translation:
  Genetic code: 64 codons, 20 amino acids + 3 stop codons
  Wobble hypothesis: 3rd base less stringent
  Start codon: AUG (Met)
  Stop codons: UAA, UAG, UGA
  Ribosomes: 70S (prok: 30S+50S), 80S (euk: 40S+60S)
  Steps: initiation, elongation (A→P→E sites), termination
  tRNA: anticodon loop recognizes mRNA codon
```

---

## Cell Signaling
```python
def signaling_pathways():
    return {
        'cAMP pathway (GPCR-Gs)': {
            'trigger':      'Epinephrine, glucagon bind GPCR',
            'cascade':      'GPCR → Gs → adenylyl cyclase → cAMP → PKA → phosphorylation',
            'effects':      'Glycogen breakdown, fat mobilization, gene expression',
            'termination':  'Phosphodiesterase degrades cAMP, phosphatases remove phosphate'
        },
        'IP3/DAG pathway (GPCR-Gq)': {
            'trigger':      'ACh (muscarinic), angiotensin II',
            'cascade':      'GPCR → Gq → PLC-β → IP3 + DAG',
            'IP3':          '→ ER Ca²⁺ release → calmodulin → CaM kinase',
            'DAG':          '→ activates PKC → phosphorylation'
        },
        'RTK/RAS/MAPK': {
            'trigger':      'EGF, PDGF, insulin bind receptor tyrosine kinase',
            'cascade':      'RTK dimerization → autophosphorylation → GRB2/SOS → RAS-GTP → RAF → MEK → ERK',
            'effects':      'Cell proliferation, differentiation, survival',
            'cancer':       'RAS mutations in ~30% of human cancers (oncogene)'
        },
        'PI3K/AKT/mTOR': {
            'trigger':      'Insulin, growth factors',
            'cascade':      'RTK → PI3K → PIP3 → PDK1+AKT → mTOR',
            'effects':      'Protein synthesis, glucose uptake, cell survival, growth',
            'PTEN':         'Phosphatase that opposes PI3K (tumor suppressor)'
        },
        'JAK/STAT': {
            'trigger':      'Cytokines, interferon, growth hormone',
            'cascade':      'Cytokine receptor → JAK activation → STAT phosphorylation → nucleus',
            'effects':      'Immune response, hematopoiesis, inflammation'
        },
        'Wnt/β-catenin': {
            'off':          'β-catenin phosphorylated by GSK-3β → ubiquitinated → degraded',
            'on':           'Wnt → Frizzled → Dishevelled → inhibit GSK-3β → β-catenin stable → TCF → transcription',
            'cancer':       'APC mutations in colorectal cancer'
        }
    }
```

---

## Bioenergetics
```
Free energy in biochemistry:
  ΔG = ΔG° + RT·ln(Q)
  ΔG° = -RT·ln(K_eq)
  ATP hydrolysis: ΔG° = -30.5 kJ/mol
  In cell: ΔG ≈ -50 kJ/mol (non-equilibrium conditions)

High-energy compounds:
  Phosphoanhydrides: ATP, ADP (hydrolysis -30.5 kJ/mol)
  Acyl phosphates: 1,3-BPG (-49 kJ/mol)
  Enol phosphates: PEP (-62 kJ/mol)
  Thioesters: Acetyl-CoA (-31 kJ/mol)
  Creatine phosphate: (-43 kJ/mol, muscle energy buffer)

Coupled reactions:
  Unfavorable reaction: ΔG > 0
  Couple with ATP hydrolysis: ΔG_total < 0
  Example: Glucose + Pi → G6P ΔG°= +14 kJ/mol
           ATP → ADP + Pi  ΔG°= -30.5 kJ/mol
           Net:            ΔG°= -16.5 kJ/mol ✓

Redox biochemistry:
  Reduction potential E°′ (biochemical standard)
  NAD⁺/NADH: E°′ = -0.32 V  (good reductant)
  FAD/FADH₂:  E°′ = -0.22 V
  O₂/H₂O:     E°′ = +0.82 V  (good oxidant)
  ΔG°′ = -nFΔE°′
  NADH → O₂: ΔE°′ = 1.14 V, ΔG°′ = -220 kJ/mol
  → enough for ~2.5 ATP synthesis

Photosynthesis:
  Light reactions: H₂O → O₂ + NADPH + ATP (thylakoid membrane)
  Calvin cycle: CO₂ + NADPH + ATP → G3P (stroma)
  Z-scheme: PSI and PSII connected by plastoquinone, plastocyanin
  Rubisco: CO₂ + RuBP → 2× 3-PGA (most abundant enzyme on Earth)
  C4 plants: concentrate CO₂ to overcome photorespiration (corn, sugarcane)
```

---

## Key Metabolic Regulation
```
Hormonal regulation:
  Fed state (insulin high):
    ↑ Glycolysis, glycogen synthesis, fatty acid synthesis, protein synthesis
    ↓ Gluconeogenesis, glycogenolysis, β-oxidation
  Fasted state (glucagon/epinephrine high):
    ↑ Gluconeogenesis, glycogenolysis, β-oxidation, ketogenesis
    ↓ Glycolysis, glycogen synthesis, fatty acid synthesis

Energy sensor: AMP-activated protein kinase (AMPK)
  Activated when AMP/ATP ratio high (low energy)
  Stimulates catabolism (β-oxidation, glycolysis)
  Inhibits anabolism (fatty acid synthesis, gluconeogenesis)

Metabolic syndrome:
  Insulin resistance: cells don't respond to insulin → hyperglycemia
  Type 2 diabetes: pancreas exhausted → insufficient insulin
  Obesity: excess calorie storage as triglycerides
  NAFLD: fat accumulation in liver

Key regulatory enzymes:
  Glycolysis: PFK-1 (+ AMP, F2,6BP; - ATP, citrate)
  Gluconeogenesis: FBPase-1 (+ ATP; - AMP, F2,6BP)
  TCA: isocitrate DH (+ ADP, Ca²⁺; - ATP, NADH)
  Fatty acid synthesis: ACC (+ citrate; - palmitoyl-CoA)
  β-oxidation: carnitine palmitoyltransferase I (- malonyl-CoA)
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Km = affinity always | Lower Km = higher affinity only for simple Michaelis-Menten |
| ATP count confusion | ~30-32 ATP per glucose (not 36-38, older textbook values) |
| Glycolysis location | Cytoplasm, NOT mitochondria |
| β-oxidation products | Acetyl-CoA + FADH₂ + NADH per cycle (not just ATP) |
| Competitive vs noncompetitive | Competitive: Km changes; Noncompetitive: Vmax changes |
| Anabolism uses NADPH not NADH | Biosynthesis requires NADPH; catabolism produces NADH |

---

## Related Skills

- **molecular-biology-expert**: Gene expression in depth
- **cell-biology-expert**: Organelles and cellular processes
- **genetics-expert**: Inheritance and mutation
- **organic-chemistry-expert**: Chemical mechanisms in biology
- **physical-chemistry-expert**: Thermodynamics and kinetics
- **neuroscience-expert**: Neurotransmitters and signaling
- **immunology-expert**: Immune biochemistry
