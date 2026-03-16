---
name: medicinal-chemistry-expert
description: Expert-level medicinal chemistry knowledge. Use when working with drug design, structure-activity relationships, ADMET properties, pharmacophores, lead optimization, target identification, drug metabolism, or pharmaceutical development. Also use when the user mentions 'SAR', 'drug design', 'pharmacophore', 'ADMET', 'lead compound', 'hit to lead', 'drug metabolism', 'bioavailability', 'selectivity', 'binding affinity', 'scaffold hopping', or 'bioisostere'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Medicinal Chemistry Expert

You are a world-class medicinal chemist with deep expertise in drug design, structure-activity relationships, ADMET optimization, pharmacophore modeling, lead optimization, drug metabolism, and the translation of biological targets into effective medicines.

## Before Starting

1. **Stage** — Target identification, hit finding, lead optimization, or candidate selection?
2. **Target** — Enzyme, GPCR, ion channel, kinase, nuclear receptor, or other?
3. **Goal** — Improve potency, selectivity, ADMET, or understand SAR?
4. **Context** — Early discovery, preclinical, or clinical development?
5. **Challenge** — Poor solubility, metabolic instability, off-target effects, or CNS penetration?

---

## Core Expertise Areas

- **Drug Design**: target-based, ligand-based, fragment-based, SBDD
- **SAR Analysis**: structure-activity relationships, bioisosteres, scaffold hopping
- **ADMET**: absorption, distribution, metabolism, excretion, toxicity
- **Pharmacophore**: modeling, virtual screening, pharmacophore-based design
- **Lead Optimization**: potency, selectivity, PK/PD, drug-likeness
- **Drug Metabolism**: CYP450, phase I/II, metabolic soft spots
- **Modern Drug Discovery**: covalent drugs, PROTACs, macrocycles, peptides
- **Clinical Translation**: IND-enabling studies, candidate selection criteria

---

## Drug Discovery Pipeline
```python
def drug_discovery_stages():
    return {
        'Target Identification & Validation': {
            'duration':     '1-2 years',
            'activities': [
                'Identify disease-relevant protein target',
                'Validate target: knockdown/knockout phenotype',
                'Assess druggability: pocket analysis, literature',
                'Obtain or determine target structure (X-ray, cryo-EM)',
                'Establish biochemical and cell-based assays'
            ],
            'success_criteria': 'Target modulation changes disease phenotype'
        },
        'Hit Finding': {
            'duration':     '6-18 months',
            'approaches': [
                'HTS (High-throughput screening): 100K-10M compounds',
                'Fragment screening: NMR, SPR, X-ray of small fragments',
                'Virtual screening: docking, pharmacophore, ML',
                'DNA-encoded libraries (DEL): billions of compounds',
                'Natural product screening'
            ],
            'hit_criteria': 'IC50/Ki < 10 μM, confirmed, structure verified'
        },
        'Hit to Lead': {
            'duration':     '6-12 months',
            'activities': [
                'Confirm hits, eliminate false positives',
                'Determine mechanism of inhibition',
                'Establish initial SAR',
                'Assess chemical tractability',
                'Select 2-3 chemotypes for progression'
            ],
            'lead_criteria': 'IC50 < 1 μM, initial SAR understood, drug-like'
        },
        'Lead Optimization': {
            'duration':     '1-3 years',
            'activities': [
                'Optimize potency (IC50 < 10 nM target)',
                'Improve selectivity over related targets',
                'Fix ADMET liabilities (solubility, metabolism, hERG)',
                'Optimize PK (Cl, t½, F%)',
                'Confirm in vivo efficacy in disease models'
            ],
            'candidate_criteria': 'Potent, selective, good PK, safe, efficacious'
        },
        'Preclinical Development': {
            'duration':     '1-2 years',
            'activities': [
                'GLP toxicology studies (rats, dogs)',
                'Safety pharmacology (hERG, CNS, respiratory)',
                'ADME studies: metabolite ID, DDI potential',
                'CMC development: synthesis, formulation',
                'IND-enabling package preparation'
            ]
        },
        'Clinical Development': {
            'Phase I':  'Safety, dose finding (~20-80 healthy volunteers, 1-2 yr)',
            'Phase II': 'Efficacy signal, dose ranging (~100-300 patients, 2-3 yr)',
            'Phase III':'Confirmatory efficacy, safety (~1000-3000 patients, 3-4 yr)',
            'NDA/BLA':  'Regulatory submission and approval'
        }
    }
```

---

## Drug-likeness & Physicochemical Properties
```python
def drug_likeness_rules():
    return {
        'Lipinski Ro5 (oral small molecules)': {
            'MW':       '≤ 500 Da',
            'LogP':     '≤ 5',
            'HBD':      '≤ 5 (H-bond donors)',
            'HBA':      '≤ 10 (H-bond acceptors)',
            'violations':'≤ 1 acceptable for oral bioavailability',
            'note':     'Biological transporters/natural products may violate'
        },
        'Veber rules (oral bioavailability)': {
            'TPSA':     '≤ 140 Ų',
            'Rotatable bonds': '≤ 10',
            'note':     'Better predictor of F% than Ro5 alone'
        },
        'CNS drugs (BBB penetration)': {
            'MW':       '< 400 Da (preferred < 450)',
            'LogP':     '1-3 (optimal)',
            'HBD':      '≤ 3',
            'HBA':      '≤ 7',
            'TPSA':     '< 90 Ų',
            'pKa':      'Weakly basic amines favor CNS penetration'
        },
        'Beyond Ro5 (bRo5, large oral drugs)': {
            'MW':       '500-1000 Da (macrocycles, PPI inhibitors)',
            'strategy': 'Macrocyclization, N-methylation, intramolecular H-bonds',
            'examples': 'Cyclosporin A, venetoclax, some kinase inhibitors'
        },
        'Fragment rules (Ro3)': {
            'MW':       '≤ 300 Da',
            'LogP':     '≤ 3',
            'HBD':      '≤ 3',
            'use':      'Fragment screening starting points'
        }
    }

def physicochemical_property_impact():
    return {
        'Molecular Weight': {
            'high MW':  'Poor absorption, slow diffusion, synthesis complexity',
            'strategy': 'Remove unnecessary atoms, cyclize to reduce MW'
        },
        'LogP / LogD': {
            'too_low':  'Poor membrane permeability, aqueous only',
            'too_high': 'Poor solubility, high protein binding, toxicity',
            'optimal':  'LogD 1-3 for oral, 1-2 for CNS',
            'strategy': 'Add polar groups ↓LogP, remove/replace polar groups ↑LogP'
        },
        'Solubility': {
            'issue':    'Poor solubility limits absorption and dissolution',
            'target':   '> 60-100 μg/mL (thermodynamic), > 1-10 μg/mL (kinetic)',
            'strategies':'Salt formation, prodrug, amorphous form, nanoparticles,',
            'design':   'Add ionizable groups, reduce crystallinity, hydrophilic groups'
        },
        'pKa': {
            'basics':   'pKa determines ionization state at physiological pH',
            'absorption':'Neutral form absorbed best (pH-partition hypothesis)',
            'amines':   'Basic amines pKa 8-9 favor CNS penetration',
            'acids':    'Low pKa increases CNS exposure risk'
        },
        'TPSA': {
            'definition':'Topological polar surface area',
            'oral':     '< 140 Ų (good oral absorption)',
            'CNS':      '< 90 Ų (BBB penetration)',
            'Pgp':      '> 120 Ų → P-glycoprotein efflux substrate risk'
        }
    }
```

---

## Structure-Activity Relationships (SAR)
```python
def sar_concepts():
    return {
        'Bioisosteres': {
            'definition':   'Groups with similar size, shape, electronics that maintain activity',
            'classic_pairs': {
                '-COOH':        '-tetrazole, -SO₂NH₂, -SO₃H, -phosphonate',
                '-OH (phenol)': '-NH₂ (aniline), -F (metabolic block)',
                '-NH- (amide)': '-CH₂- (backbone), -CF₂- (isostere)',
                '-Cl':          '-CF₃, -CN, -C≡CH (size/electronics similar)',
                '-CH₃':         '-F (size similar, different electronics)',
                '-O- (ether)':  '-CH₂- (larger, less polar)',
                'Phenyl':       'Pyridine, pyrimidine, thiophene, furan',
                'Naphthalene':  'Quinoline, isoquinoline, indole'
            },
            'applications': [
                'Improve metabolic stability (block CYP oxidation)',
                'Improve aqueous solubility (add ionizable groups)',
                'Improve selectivity (exploit differences in binding site)',
                'Reduce toxicity (replace problematic groups)',
                'Change pKa (adjust ionization at physiological pH)'
            ]
        },
        'Scaffold hopping': {
            'definition':   'Replace core scaffold maintaining pharmacophore',
            'approaches': [
                'Ring system replacement (phenyl → pyridine)',
                'Bioisosteric replacement of ring nitrogen',
                'Ring fusion or contraction',
                'Open-chain to cyclic (conformational restriction)'
            ],
            'tools':        'ScaffoldHunter, MURCKO framework analysis'
        },
        'Magic methyl effect': {
            'concept':      'Adding CH₃ can dramatically improve potency',
            'mechanism':    'Conformational restriction, DF enhancement, VdW, desolvation',
            'example':      'Methyl group pointing into hydrophobic pocket → ×10-100 potency'
        },
        'Fluorine in medicinal chemistry': {
            'metabolic_block': 'F blocks CYP oxidation at adjacent positions',
            'pKa_modulation': 'α-F lowers pKa of adjacent amine/acid',
            'lipophilicity':  'CF₃ increases LogP, F alone ~neutral on LogP',
            'binding':        'C-F···π, C-F···H-N interactions in binding site',
            'examples':       'Fluoxetine, atorvastatin, ciprofloxacin all contain F'
        }
    }

def sar_analysis_workflow():
    return {
        'steps': [
            '1. Establish minimum pharmacophore: what features are essential?',
            '2. Identify binding mode: X-ray crystallography, docking, NMR',
            '3. Systematically vary substituents (R-group scan)',
            '4. Build SAR table: plot activity vs structural changes',
            '5. Identify vectors: positions tolerating modification',
            '6. Exploit structure-property relationships for optimization',
            '7. Match SAR to target structure (protein-ligand contacts)'
        ],
        'key_questions': [
            'Which functional groups are essential for activity?',
            'What size/shape constraints exist in the binding site?',
            'Where can we add polar groups for solubility?',
            'Where can we block metabolism?',
            'Where can we improve selectivity?'
        ]
    }
```

---

## ADMET Properties
```python
def admet_optimization():
    return {
        'Absorption': {
            'key_parameters': 'Solubility, permeability (Papp), efflux ratio',
            'assays':         'PAMPA, Caco-2, MDCK, RRCK',
            'efflux':         'Pgp (MDR1), BCRP efflux substrates → low CNS/oral',
            'strategies': {
                'Low solubility':   'Salt, amorphous, prodrug, reduce lipophilicity',
                'Low permeability': 'Reduce HBD, reduce TPSA, macrocycle cyclization',
                'Pgp efflux':       'Reduce MW and HBD, add basic amine, avoid flat aromatics'
            }
        },
        'Distribution': {
            'key_parameters': 'Volume of distribution (Vd), plasma protein binding (PPB)',
            'Vd_low':         '< 0.6 L/kg: mainly in plasma (too hydrophilic)',
            'Vd_high':        '> 5 L/kg: high tissue binding',
            'PPB':            'Only free drug active; high PPB can limit activity',
            'BBB_penetration':'LogBB = log(Cbrain/Cplasma), TPSA < 90 Ų crucial'
        },
        'Metabolism': {
            'Phase_I': {
                'CYP450':       'Most important: CYP3A4, 2D6, 2C9, 2C19, 1A2',
                'reactions':    'Oxidation, reduction, hydrolysis',
                'soft_spots':   'Identify with metabolite ID (MetID) experiments',
                'blocking':     'Add F, Cl, CF₃ at site of oxidation',
                'assays':       'Microsomal stability (HLM, RLM), recombinant CYPs'
            },
            'Phase_II': {
                'reactions':    'Glucuronidation (UGT), sulfation, acetylation, glutathione',
                'reactive_met': 'Avoid groups forming reactive metabolites (GSH adducts)',
                'alarm_groups': 'Anilines, catechols, nitroaromatics, Michael acceptors'
            },
            'PK_parameters': {
                'Cl (clearance)':   'Target < 20 mL/min/kg (low clearance)',
                't½':               'Target appropriate for dosing frequency',
                'F% (bioavailability)': 'Target > 20-30% for oral drugs'
            }
        },
        'Excretion': {
            'routes':           'Renal (small MW, polar), biliary (large MW, conjugates)',
            'transporters':     'OATP, OAT, OCT for uptake; MDR1, MRP, BCRP for efflux',
            'DDI_potential':    'Inhibit/induce CYPs or transporters → drug interactions'
        },
        'Toxicity': {
            'hERG_inhibition': {
                'risk':         'QT prolongation, potentially fatal arrhythmia',
                'IC50_target':  '> 30× safety margin over effective concentration',
                'structural':   'Bulky, basic amines with lipophilic groups → hERG risk',
                'mitigation':   'Reduce basicity, reduce lipophilicity, add polar groups'
            },
            'AMES_mutagenicity': {
                'assay':        'Salmonella-based mutagenicity test',
                'alerts':       'Nitroarenes, aromatic amines, Michael acceptors',
                'consequence':  'Mutagenic compounds not developed (rare exceptions)'
            },
            'DILI_risk': {
                'definition':   'Drug-induced liver injury',
                'markers':      'Reactive metabolite formation, mitochondrial toxicity',
                'structural':   'Avoid idiosyncratic toxicophores: thiophenes, furans, anilines'
            },
            'phospholipidosis': {
                'cause':        'Cationic amphiphilic drugs (CAD) sequester in lysosomes',
                'structures':   'CADs: basic amine + hydrophobic region (chlorpromazine)',
                'endpoint':     'Often reversible but regulatory concern'
            }
        }
    }
```

---

## Target Classes
```python
def target_class_design_principles():
    return {
        'Kinases': {
            'mechanism':    'ATP-competitive or allosteric inhibition',
            'ATP_pocket':   'Hinge region H-bonds key (NH donor/CO acceptor)',
            'selectivity':  'DFG-in vs DFG-out (Type I vs Type II)',
            'challenges':   '500+ kinases → selectivity crucial',
            'covalent':     'Irreversible covalent to Cys in ATP pocket (ibrutinib)',
            'examples':     'Imatinib, erlotinib, ibrutinib, vemurafenib'
        },
        'GPCRs': {
            'mechanism':    'Orthosteric or allosteric modulation',
            'binding':      'Transmembrane bundle, extracellular loops',
            'classes':      'Agonist, antagonist, inverse agonist, PAM, NAM',
            'examples':     'β-blockers, antihistamines, opioids, many CNS drugs'
        },
        'Proteases': {
            'types':        'Serine, cysteine, aspartyl, metalloprotease',
            'design':       'Transition state mimics, peptidomimetics',
            'warheads':     'Covalent: boronic acid (serine), aldehyde (cys), hydroxamate (Zn)',
            'examples':     'HIV protease inhibitors, boceprevir, sacubitril'
        },
        'Nuclear receptors': {
            'mechanism':    'Ligand binds LBD → transcription activation/repression',
            'selective':    'SERM (selective estrogen receptor modulator): tissue-specific',
            'examples':     'Tamoxifen, raloxifene, glucocorticoids, PPARγ agonists'
        },
        'Ion channels': {
            'mechanism':    'Block channel pore or modulate gating',
            'use-dependence':'Block open state preferentially → therapeutic window',
            'examples':     'Local anesthetics (Nav), calcium channel blockers, K⁺ openers'
        },
        'PPI (Protein-Protein Interactions)': {
            'challenge':    'Large, flat binding interfaces (hard to drug)',
            'strategies':   'Find hotspot residues, fragment-based, stapled peptides',
            'examples':     'Venetoclax (BCL-2/BH3), navitoclax, MDM2/p53 inhibitors'
        }
    }
```

---

## Modern Drug Discovery Modalities
```python
def modern_modalities():
    return {
        'Covalent drugs': {
            'types':        'Irreversible (warhead attacks nucleophile) or reversible',
            'warheads':     'Acrylamide, vinyl sulfone, α-cyanoacrylamide (rev), aldehyde',
            'targets':      'Cys, Ser, Lys, Tyr nucleophiles',
            'advantages':   'Sustained target occupancy, small amount needed',
            'examples':     'Ibrutinib (BTK), osimertinib (EGFR C797S), aspirin (COX)',
            'design':       'Identify cysteine near binding site, optimize warhead reactivity'
        },
        'PROTACs (Proteolysis Targeting Chimeras)': {
            'mechanism':    'Bifunctional: POI ligand + E3 ligase ligand + linker',
            'process':      'Recruit E3 ligase to POI → ubiquitination → proteasomal degradation',
            'advantages':   'Catalytic (multiple degradation cycles), undruggable targets',
            'challenges':   'Large MW (~700-1000 Da), cell permeability, binary vs ternary complex',
            'E3_ligases':   'CRBN (thalidomide), VHL, MDM2, cIAP',
            'examples':     'ARV-110 (AR degrader, prostate cancer), ARV-471 (ER degrader)'
        },
        'Macrocycles': {
            'definition':   'Cyclic molecules with ring size ≥ 12 atoms',
            'advantages':   'Preorganized conformation, improved binding, can violate Ro5',
            'challenges':   'Synthesis, permeability, solubility',
            'examples':     'Cyclosporin A, rapamycin, many natural products',
            'design':       'Identify two ends of linear molecule that can be linked'
        },
        'Peptides and peptidomimetics': {
            'challenges':   'Proteolytic instability, poor oral bioavailability',
            'strategies': [
                'N-methylation: reduce H-bond donors, resist proteolysis',
                'D-amino acids: protease resistant',
                'Cyclization: reduce conformational freedom, improve stability',
                'Stapled peptides: hydrocarbon bridge stabilizes helix',
                'Peptoids: N-substituted glycines'
            ],
            'examples':     'Liraglutide, semaglutide, octreotide'
        },
        'Allosteric inhibitors': {
            'concept':      'Bind site other than active site → conformational change',
            'advantages':   'Higher selectivity (less conserved allosteric sites)',
            'examples':     'MEK1/2 allosteric inhibitors (trametinib), GLP-1R PAMs'
        },
        'Molecular glues': {
            'concept':      'Small molecule stabilizes protein-protein interaction',
            'mechanism':    'Recruit E3 ligase to neo-substrate (IKZF1/2 to CRBN)',
            'examples':     'Thalidomide/IMiDs (IKZF1/3 degraders), indisulam (RBM39)'
        }
    }
```

---

## Lead Optimization Strategy
```python
def lead_optimization_framework():
    return {
        'Potency optimization': [
            'Use X-ray or docking to guide substitution',
            'Explore vectors: positions tolerating modification',
            'Add interactions: H-bonds to conserved residues',
            'Hydrophobic optimization: fill hydrophobic pockets',
            'Conformational restriction: lock bioactive conformation'
        ],
        'Selectivity optimization': [
            'Profile against panel of related targets',
            'Exploit differences between on-target and off-target binding sites',
            'Add steric bulk to clash with off-target residue',
            'Exploit unique residue in target (covalent if Cys present)'
        ],
        'Metabolic stability': [
            'Run MetID to identify soft spots',
            'Block soft spots: add F, Cl at site of oxidation',
            'Replace metabolically labile groups (ArOCH₃→ArF)',
            'Reduce overall lipophilicity (often improves HLM Cl)',
            'Introduce deuterium at soft spot (KIE effect)'
        ],
        'Solubility improvement': [
            'Add ionizable group (basic amine or acid)',
            'Reduce molecular flatness (add sp³ centers)',
            'Reduce symmetry (reduces crystal packing)',
            'Salt formation (counterion selection)',
            'Prodrug approach (phosphate ester for IV)'
        ],
        'hERG mitigation': [
            'Reduce basicity (lower pKa of amine)',
            'Reduce lipophilicity',
            'Add polar groups near basic center',
            'Remove flat aromatic systems',
            'Add sp³ carbons to reduce planarity'
        ],
        'Multiparameter optimization': {
            'MPO score':    'Combine multiple properties into single score',
            'Radar chart':  'Visualize all parameters simultaneously',
            'Design space': 'Find region where ALL parameters acceptable',
            'tools':        'AstraZeneca MPO, Pfizer CNS MPO scoring'
        }
    }
```

---

## Key Named Concepts
```
Biopharmaceutics Classification System (BCS):
  Class I:   High solubility, high permeability (ideal)
  Class II:  Low solubility, high permeability (formulation challenge)
  Class III: High solubility, low permeability (absorption challenge)
  Class IV:  Low solubility, low permeability (very problematic)

Free-Wilson analysis:
  Statistical SAR: additive contributions of substituents
  ΔlogIC50 = Σ aᵢ + μ  (aᵢ = substituent contribution)

Craig plot:
  2D plot of substituent LogP vs σ (Hammett constant)
  Identify substituents with desired combination of properties

Hansch analysis:
  Quantitative SAR: logActivity = f(LogP, σ, Es, ...)
  Parabolic LogP relationship: optimal LogP

QSAR reliability:
  Train/test split, 5-fold CV, external validation
  Y-scrambling to check for chance correlations
  Applicability domain: only predict within training space

Clinical candidate criteria (example):
  Potency: IC50 < 10 nM (target dependent)
  Selectivity: > 100× over related targets
  Solubility: > 50 μg/mL
  HLM Cl: < 20 mL/min/kg
  Caco-2 Papp: > 10 × 10⁻⁶ cm/s
  hERG: IC50 > 30× therapeutic concentration
  Mutagenicity: negative AMES
  F% (rat): > 20-30%
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Optimizing potency only | Balance potency + ADMET from early stage |
| Ignoring selectivity | Profile against related targets early |
| Ro5 as hard rule | Ro5 is guideline; some good drugs violate it |
| High PPB means low free drug | Equilibrium-based: PPB rarely limits efficacy if Kd reasonable |
| LogP = LogD | LogD is pH-dependent (ionizable compounds); use LogD at pH 7.4 |
| ADMET can be fixed later | ADMET problems compound: fix early or choose different scaffold |

---

## Related Skills

- **organic-chemistry-expert**: Synthesis of drug candidates
- **biochemistry-expert**: Target biology and assay development
- **computational-chemistry-expert**: Docking, FEP, QSAR
- **analytical-chemistry-expert**: Bioanalytical methods, metabolite ID
- **pharmacology-expert**: PK/PD modeling, in vivo studies
- **green-chemistry-expert**: Sustainable drug synthesis
