---
author: luo-kai
name: cell-biology-expert
description: Expert-level cell biology knowledge. Use when working with cell structure, organelles, cell signaling, cell cycle, cell division, cytoskeleton, membrane biology, vesicular trafficking, apoptosis, or cell biology techniques. Also use when the user mentions 'organelle', 'mitochondria', 'endoplasmic reticulum', 'Golgi', 'cytoskeleton', 'cell cycle', 'mitosis', 'meiosis', 'apoptosis', 'signal transduction', 'membrane potential', 'endocytosis', or 'cell migration'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Cell Biology Expert

You are a world-class cell biologist with deep expertise in cell structure, organelle function, membrane biology, cell signaling, cell cycle regulation, vesicular trafficking, cytoskeleton dynamics, and cell death pathways.

## Before Starting

1. **Topic** — Organelles, signaling, cell cycle, cytoskeleton, or trafficking?
2. **Level** — Introductory, undergraduate, or graduate/research?
3. **Goal** — Understand mechanism, design experiment, or troubleshoot?
4. **Cell type** — Prokaryote, animal, plant, or specific cell type?
5. **Context** — Basic biology, disease, or biotechnology?

---

## Core Expertise Areas

- **Cell Structure**: membranes, organelles, compartmentalization
- **Membrane Biology**: lipid bilayer, membrane proteins, transport
- **Organelle Function**: ER, Golgi, mitochondria, lysosomes, nucleus
- **Vesicular Trafficking**: secretory pathway, endocytosis, autophagy
- **Cytoskeleton**: actin, microtubules, intermediate filaments
- **Cell Signaling**: receptors, second messengers, kinase cascades
- **Cell Cycle**: checkpoints, cyclins, CDKs, checkpoints
- **Cell Death**: apoptosis, necrosis, autophagy, pyroptosis

---

## Cell Membranes
```
Fluid mosaic model (Singer & Nicolson 1972):
  Phospholipid bilayer: hydrophilic heads outward, tails inward
  Thickness: ~7-10 nm
  Lateral diffusion: lipids and proteins diffuse freely (mostly)
  Fluidity: affected by temperature, cholesterol, fatty acid saturation

Membrane lipids:
  Phospholipids: PC (phosphatidylcholine), PE, PS, PI, PG
  Sphingolipids: sphingomyelin, glycosphingolipids
  Cholesterol: ~30-40% of animal membranes, modulates fluidity
  Asymmetry: PS and PE on inner leaflet, PC/SM on outer
  Lipid rafts: ordered microdomains rich in cholesterol + sphingolipids

Membrane proteins:
  Integral (transmembrane): span bilayer (α-helices or β-barrel)
  Peripheral: attached to surface (electrostatic or lipid anchor)
  Lipid-anchored: GPI anchor (outer leaflet), palmitoyl/myristoyl (inner)

Membrane transport:
  Passive diffusion: small nonpolar molecules (O₂, CO₂, steroid hormones)
  Facilitated diffusion: carrier proteins or channels (glucose, ions)
  Active transport: ATP-driven against gradient (Na⁺/K⁺ ATPase)
  Secondary active: coupled to ion gradient (Na⁺-glucose cotransporter)

Ion channels:
  Voltage-gated: Na⁺, K⁺, Ca²⁺ channels (action potentials)
  Ligand-gated: nAChR, AMPA, GABA_A (synaptic transmission)
  Mechanosensitive: Piezo1/2 (touch, blood pressure)
  Aquaporins: water channels (kidney, red blood cells)

Nernst equation (equilibrium potential):
  Eₓ = (RT/zF)·ln([X]outside/[X]inside)
  At 37°C: Eₓ = (61.5/z)·log([X]o/[X]i) mV
  Na⁺: ~+60 mV, K⁺: ~-88 mV, Cl⁻: ~-60 mV, Ca²⁺: ~+123 mV
  Resting potential: ~-70 mV (K⁺ dominates permeability)
```

---

## Organelles
```python
def organelle_functions():
    return {
        'Nucleus': {
            'function':     'DNA storage, replication, transcription',
            'structure':    'Double membrane (inner + outer), nuclear pores (NPC)',
            'NPC':          '~120 MDa complex, ~1000 per nucleus, 9 nm central channel',
            'import':       'Nuclear localization signal (NLS) + importins',
            'export':       'Nuclear export signal (NES) + exportins',
            'nucleolus':    'rRNA synthesis and ribosome assembly'
        },
        'Endoplasmic Reticulum': {
            'Rough ER':     'Ribosomes on surface; protein synthesis and N-glycosylation',
            'Smooth ER':    'No ribosomes; lipid synthesis, Ca²⁺ storage, detoxification',
            'functions': [
                'Co-translational translocation of secretory/membrane proteins',
                'Signal peptide → SRP → SRP receptor → translocon (Sec61)',
                'N-linked glycosylation: transfer of 14-sugar oligosaccharide',
                'Protein folding: BiP/GRP78 (HSP70), PDI, calnexin, calreticulin',
                'UPR (Unfolded Protein Response): IRE1, PERK, ATF6'
            ],
            'ER-associated degradation': 'ERAD: misfolded proteins → ubiquitin → proteasome'
        },
        'Golgi Apparatus': {
            'structure':    'Stacked flattened cisternae: cis → medial → trans',
            'cis':          'Receives vesicles from ER',
            'trans':        'Sorts proteins to destinations',
            'TGN':          'Trans-Golgi Network: sorting hub',
            'functions': [
                'O-linked glycosylation',
                'Glycan processing (trimming + addition)',
                'Proteolytic processing (furin)',
                'Sorting to lysosomes, secretory vesicles, plasma membrane'
            ]
        },
        'Mitochondria': {
            'structure':    'Double membrane: outer (VDAC) + inner (cristae, ATP synthase)',
            'matrix':       'TCA cycle, β-oxidation, mtDNA (16.5 kb, 37 genes)',
            'IMS':          'Intermembrane space: cytochrome c (apoptosis)',
            'functions': [
                'ATP synthesis via oxidative phosphorylation',
                'Ca²⁺ buffering',
                'Apoptosis regulation (Bcl-2 family, cytochrome c release)',
                'ROS production and signaling',
                'Thermogenesis (UCP1 in brown fat)'
            ],
            'dynamics':     'Fission (Drp1) and fusion (Mfn1/2, OPA1) balance'
        },
        'Lysosomes': {
            'pH':           '~4.5-5.0 (maintained by V-ATPase)',
            'enzymes':      '~60 acid hydrolases (proteases, lipases, nucleases, glycosidases)',
            'functions': [
                'Degradation of macromolecules',
                'Autophagy (cellular recycling)',
                'Phagocytosis (immune cells)',
                'Signaling hub (mTORC1 activation)'
            ],
            'lysosomal storage': 'Pompe, Gaucher, Niemann-Pick, Tay-Sachs diseases'
        },
        'Peroxisomes': {
            'function':     'H₂O₂-generating oxidations + catalase (H₂O₂ → H₂O)',
            'β-oxidation':  'Very long chain fatty acids (VLCFA) — unlike mitochondria',
            'other':        'Bile acid synthesis, plasmalogen synthesis, ether lipids'
        }
    }
```

---

## Vesicular Trafficking
```
Secretory pathway (anterograde):
  ER → COPII vesicles → ER-Golgi intermediate (ERGIC)
  → cis-Golgi → medial-Golgi → trans-Golgi (cisternal maturation)
  → TGN → secretory vesicles or lysosomes

Retrieval (retrograde):
  Golgi → ER: COPI vesicles (retrieve KDEL-tagged ER residents)
  Endosomes → Golgi: retromer complex

Vesicle budding:
  Coat proteins: COPII (ER→Golgi), COPI (Golgi→ER, intra-Golgi), Clathrin (PM→endosome, TGN)
  Small GTPases: Sar1 (COPII), Arf1 (COPI, clathrin)
  Rab GTPases: ~70 in humans, identity markers for each compartment
    Rab1: ER→Golgi, Rab5: early endosome, Rab7: late endosome, Rab11: recycling

Vesicle fusion:
  SNAREs: v-SNARE (vesicle) + t-SNARE (target) coil → bring membranes together
  NSF + α-SNAP: disassemble SNARE complexes (recycle)
  Synaptotagmin: Ca²⁺ sensor for synaptic vesicle fusion

Endocytosis:
  Clathrin-mediated: receptor-mediated (LDL, transferrin, EGF)
    Clathrin triskelion → coated pit → coated vesicle → early endosome
  Caveolae: flask-shaped, caveolin, lipid rafts, signaling
  Macropinocytosis: large fluid-phase uptake
  Phagocytosis: large particles, Fc or complement receptors

Endosomal trafficking:
  Early endosome (Rab5, EEA1, pH 6-6.5)
  Recycling endosome (Rab11, Rab4): receptors back to PM
  Late endosome / MVB (Rab7, pH 5-5.5): receptors to degradation
    ESCRT machinery: ubiquitinated cargo → intraluminal vesicles
  Lysosome fusion (pH 4.5-5.0): degradation

Autophagy:
  Macroautophagy: double-membrane autophagosome → lysosome
  Initiation: mTORC1 inhibited → ULK1/2 complex activated
  Nucleation: VPS34 (PI3K class III) → PI3P → phagophore
  Elongation: ATG5-ATG12-ATG16L, LC3-II on membrane
  Cargo recognition: p62/SQSTM1 (ubiquitinated cargo), NDP52, optineurin
  Mitophagy: PINK1/Parkin pathway → damaged mitochondria
  ER-phagy, ribophagy: selective organelle degradation
```

---

## Cytoskeleton
```python
def cytoskeleton():
    return {
        'Actin (microfilaments)': {
            'monomer':      'G-actin (globular, 42 kDa)',
            'polymer':      'F-actin (filamentous), 2 strands twisted helix, ~7 nm diameter',
            'polarity':     'Barbed (plus) end: fast growth; Pointed (minus) end: slower',
            'treadmilling': 'ATP-actin adds at barbed, ADP-actin dissociates at pointed',
            'regulators': {
                'Arp2/3':   'Nucleates branched filaments (lamellipodia)',
                'WASP/N-WASP': 'Activates Arp2/3',
                'Formin':   'Nucleates + elongates unbranched filaments (filopodia)',
                'Cofilin':  'Severs and depolymerizes (ADF/cofilin)',
                'Profilin': 'Charges G-actin with ATP, facilitates polymerization',
                'Capping proteins': 'Cap barbed ends to control length'
            },
            'structures':   'Lamellipodia, filopodia, stress fibers, cortex, ring canals'
        },
        'Microtubules': {
            'monomer':      'α/β-tubulin heterodimer (50 kDa each)',
            'polymer':      '13 protofilaments, hollow tube, 25 nm diameter',
            'polarity':     'Plus end: dynamic (GTP-cap); Minus end: stable (anchored at MTOC)',
            'MTOC':         'Microtubule organizing center (centrosome in animal cells)',
            'dynamic instability': 'Stochastic switching between growth and shrinkage',
            'motors': {
                'Kinesin':  'Plus-end directed (anterograde transport toward periphery)',
                'Dynein':   'Minus-end directed (retrograde, toward centrosome)'
            },
            'functions':    'Mitotic spindle, cilia/flagella, axonal transport, organelle positioning',
            'drugs': {
                'Taxol':    'Stabilizes microtubules (cancer treatment)',
                'Colchicine/nocodazole': 'Depolymerizes microtubules'
            }
        },
        'Intermediate filaments': {
            'monomers':     'Keratins (epithelial), vimentin (mesenchymal), neurofilaments (neurons)',
            'structure':    'Coiled-coil dimers → tetramers → filaments, 8-12 nm',
            'polarity':     'Non-polar (unlike actin/MTs)',
            'lamins':       'Nuclear lamins: nuclear lamina, shape, chromatin organization',
            'disease':      'Laminopathies (progeria), epidermolysis bullosa (keratin)'
        },
        'Septins': {
            'function':     'Diffusion barriers, cytokinesis, membrane organization',
            'structure':    'GTPase family, form filaments and rings'
        }
    }
```

---

## Cell Cycle
```
Phases:
  G1: growth, checkpoint (restriction point)
  S: DNA synthesis (replication)
  G2: growth, prep for division
  M: mitosis/meiosis
  G0: quiescent state (reversible or irreversible senescence)

Cyclin-CDK complexes:
  Cyclin D/CDK4,6: G1 progression (mitogen sensing)
  Cyclin E/CDK2: G1/S transition
  Cyclin A/CDK2: S phase (origin firing regulation)
  Cyclin A/CDK1: G2/M transition
  Cyclin B/CDK1 (MPF): M phase entry (Maturation Promoting Factor)

Rb-E2F pathway:
  Rb (retinoblastoma): represses E2F transcription factors
  Cyclin D/CDK4,6 → phosphorylate Rb → releases E2F
  E2F → transcribes S-phase genes (cyclin E, DHFR, PCNA, etc.)
  CDK inhibitors (CKIs): p16 (inhibits CDK4/6), p21, p27 (inhibits CDK2)

Checkpoints:
  G1/S checkpoint: DNA damage → ATM/ATR → Chk1/2 → p53 → p21 → arrest
  Intra-S checkpoint: stalled replication forks → ATR → Chk1 → slow S phase
  G2/M checkpoint: DNA damage → Chk1/2 → Cdc25 degradation → CDK1 inhibited
  Spindle assembly checkpoint (SAC): unattached kinetochores → MCC (Mad1/2, BubR1, Bub3)
    MCC inhibits APC/C → securin + cyclin B stable → metaphase arrest

Mitosis:
  Prophase: chromosomes condense (condensins), centrosome separation
  Prometaphase: NE breaks down, spindle captures kinetochores
  Metaphase: chromosomes align at plate (bi-orientation)
  Anaphase: APC/C-Cdc20 → securin degraded → separase → cohesin cleavage → chromosome separation
  Telophase: nuclear envelope reforms, chromosomes decondense
  Cytokinesis: actomyosin contractile ring (midbody) → cell division

Meiosis:
  Meiosis I: reductional (homologs separate)
    Prophase I: synapsis, crossing over (chiasmata)
    Metaphase I: homologs on metaphase plate (bi-orientation of bivalents)
    Anaphase I: homologs separate (cohesin on arms cleaved, centromeric preserved)
  Meiosis II: equational (sister chromatids separate, like mitosis)
  Result: 4 haploid cells from 1 diploid cell
```

---

## Cell Signaling
```python
def cell_signaling_pathways():
    return {
        'Receptor Tyrosine Kinases (RTK)': {
            'activation':   'Ligand (EGF, PDGF, insulin) → dimerization → autophosphorylation',
            'downstream': {
                'RAS/MAPK':     'Grb2-SOS → RAS-GTP → RAF → MEK → ERK → proliferation',
                'PI3K/AKT':     'PI3K → PIP3 → PDK1 → AKT → mTOR → survival/growth',
                'PLCγ':         'IP3 + DAG → Ca²⁺ release + PKC → various responses',
                'STAT':         'Direct JAK activation → STAT dimerization → transcription'
            }
        },
        'GPCR signaling': {
            'Gs':   'Adenylyl cyclase → cAMP → PKA → CREB, glycogen breakdown',
            'Gi':   'Inhibits adenylyl cyclase, activates K⁺ channels',
            'Gq':   'PLCβ → IP3 + DAG → Ca²⁺ + PKC',
            'G12/13': 'Rho GEFs → RhoA → actin cytoskeleton',
            'desensitization': 'GRK phosphorylation → arrestin → receptor internalization'
        },
        'Wnt/β-catenin': {
            'off':      'Destruction complex (APC/Axin/GSK3β/CK1) phosphorylates β-cat → ubiquitin → degradation',
            'on':       'Wnt → LRP5/6 + Frizzled → Dvl → GSK3β inhibited → β-cat accumulates → TCF target genes',
            'targets':  'Cyclin D1, c-Myc, Axin2'
        },
        'Notch': {
            'activation':   'Delta/Jagged ligand (juxtacrine) → γ-secretase cleaves NICD',
            'NICD':         'Nuclear: displaces co-repressor from CSL → transcription',
            'targets':      'Hes1, Hey1 (differentiation repressors)'
        },
        'Hedgehog': {
            'off':  'Ptch1 inhibits Smo → Gli3 repressor',
            'on':   'Hh ligand → Ptch1 inhibited → Smo active → Gli2/3 activators → target genes',
            'targets': 'Ptch1 (feedback), Gli1, cyclin D'
        },
        'TGF-β/Smad': {
            'activation':   'TGF-β dimer → type II receptor → phosphorylates type I → Smad2/3',
            'complex':      'Smad2/3 + Smad4 → nucleus → gene regulation',
            'effects':      'Growth arrest (p15, p21), EMT, fibrosis, immune suppression'
        },
        'mTOR': {
            'mTORC1':       'Nutrient/growth factor sensor → S6K → protein synthesis',
            'activation':   'PI3K/AKT, RAS/ERK, amino acids (via Rag GTPases), energy',
            'inhibition':   'AMPK, REDD1, rapamycin'
        }
    }
```

---

## Cell Death
```
Apoptosis (programmed cell death):
  Intrinsic (mitochondrial) pathway:
    Stress → BAX/BAK oligomerize in OMM → MOMP (mitochondrial outer membrane permeabilization)
    Cytochrome c release → apoptosome (Apaf-1 + cyt c + procaspase-9)
    Caspase-9 activates caspase-3/7 (executioners)
    Anti-apoptotic Bcl-2, Bcl-xL inhibit BAX/BAK
    BH3-only proteins (BIM, PUMA, NOXA): activate pathway
  
  Extrinsic (death receptor) pathway:
    FasL/TNF → Fas/TNFR → DISC → caspase-8 activation
    Caspase-8 → caspase-3/7 directly, OR cleaves BID → truncated BID → mitochondrial pathway
  
  Morphology: cell shrinkage, chromatin condensation, membrane blebbing, apoptotic bodies
  Phagocytosis: eat-me signals (PS exposure on outer leaflet, calreticulin)
  Caspase substrates: PARP, lamin A, ICAD → DNA fragmentation (laddering), nuclear shrinkage

Necrosis:
  Unregulated: trauma, toxins, extreme stress
  Necroptosis: regulated necrosis (RIPK1/RIPK3/MLKL pathway)
  Membrane rupture → DAMPs released → inflammation

Pyroptosis:
  Inflammasome-mediated: ASC + caspase-1 → IL-1β/IL-18 processing + gasdermin D pores
  Gasdermin D pores → membrane rupture → inflammatory cell death
  Innate immune defense against intracellular pathogens

Ferroptosis:
  Iron-dependent: lipid peroxidation (ROS + iron + PUFAs)
  GPX4: glutathione peroxidase 4 protects against ferroptosis
  RSL3, erastin: induce ferroptosis
  Relevant: cancer, neurodegenerative disease, ischemia

Autophagy-related death:
  Excessive autophagy can lead to cell death in some contexts
  Type II cell death: distinct morphology from apoptosis
```

---

## Cell Migration & Adhesion
```
Cell adhesion molecules:
  Integrins: heterodimers (α+β), bind ECM (collagen, fibronectin, laminin)
    Bidirectional signaling: outside-in (FAK/Src) and inside-out (talin/kindlin)
  Cadherins: Ca²⁺-dependent, cell-cell adhesion (E-cadherin in epithelia)
  Selectins: leukocyte rolling on endothelium
  IgSF-CAMs: NCAM, VCAM, ICAM

Focal adhesions:
  Integrin clusters + actin stress fibers + vinculin/talin/paxillin/FAK
  Signaling: FAK → Src → paxillin → Rac/Rho → cytoskeletal remodeling

Cell migration:
  Lamellipodia: Rac1 → Arp2/3 → branched actin (broad protrusion)
  Filopodia: Cdc42 → formin → bundled actin (spike)
  Rac → lamellipodia; Rho → stress fibers; Cdc42 → filopodia (Ridley/Hall)
  Mesenchymal: lamellipodia-based (slow, contact-dependent)
  Amoeboid: bleb-based, less ECM-dependent (faster)

Epithelial-mesenchymal transition (EMT):
  Loss of E-cadherin, gain of vimentin, N-cadherin
  TFs: Snail, Slug, Twist, ZEB1/2
  Triggered by TGF-β, Notch, Wnt
  Important in cancer invasion and metastasis, embryo development
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Mitosis = cell division | Mitosis = nuclear division; cytokinesis = cytoplasmic division; both needed |
| All cells have centrosomes | Plant cells: no centrosomes (use γ-TuRC at other sites) |
| Apoptosis always via caspases | Caspase-independent apoptosis exists (AIF, EndoG from mitochondria) |
| mTOR = one pathway | mTORC1 and mTORC2 are distinct complexes with different functions |
| Autophagy = bad | Autophagy is usually pro-survival; promotes cancer therapy resistance |
| G0 = permanent arrest | Some G0 cells re-enter cycle (hepatocytes after partial hepatectomy) |

---

## Related Skills

- **molecular-biology-expert**: Gene expression mechanisms
- **biochemistry-expert**: Metabolic pathways in cells
- **genetics-expert**: Cell cycle and cancer genetics
- **neuroscience-expert**: Neuronal cell biology
- **immunology-expert**: Immune cell biology
- **developmental-biology-expert**: Cell fate and differentiation
