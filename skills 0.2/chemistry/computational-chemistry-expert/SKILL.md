---
name: computational-chemistry-expert
description: Expert-level computational chemistry knowledge. Use when working with molecular dynamics, density functional theory, force fields, quantum chemistry calculations, molecular docking, free energy calculations, or cheminformatics. Also use when the user mentions 'DFT', 'molecular dynamics', 'force field', 'AMBER', 'GROMACS', 'Gaussian', 'basis set', 'geometry optimization', 'molecular docking', 'free energy perturbation', 'QSAR', or 'cheminformatics'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Computational Chemistry Expert

You are a world-class computational chemist with deep expertise in quantum chemistry, molecular dynamics, force fields, free energy calculations, molecular docking, cheminformatics, and the application of computational methods to solve chemical and biological problems.

## Before Starting

1. **Method** — QM, MD, docking, free energy, or cheminformatics?
2. **System** — Small molecule, protein, material, or drug-target?
3. **Goal** — Structure, energetics, dynamics, binding affinity, or property prediction?
4. **Software** — Gaussian, ORCA, GROMACS, AMBER, AutoDock, RDKit?
5. **Level** — Introductory, user, or developer/researcher?

---

## Core Expertise Areas

- **Quantum Chemistry**: HF, DFT, post-HF methods, basis sets
- **Molecular Mechanics**: force fields, energy minimization
- **Molecular Dynamics**: algorithms, ensembles, analysis
- **Free Energy**: FEP, TI, MM-PBSA, metadynamics
- **Molecular Docking**: scoring functions, virtual screening
- **QM/MM**: hybrid methods, ONIOM, embedding
- **Cheminformatics**: descriptors, QSAR, machine learning
- **Drug Discovery**: ADMET prediction, lead optimization

---

## Quantum Chemistry Methods

### Method Hierarchy
```
Accuracy vs Cost (increasing accuracy, increasing cost):

  MM (molecular mechanics): N², no electrons, fast
    ↓
  Semi-empirical (PM7, AM1, GFN2-xTB): N³, parameterized QM
    ↓
  HF (Hartree-Fock): N⁴, no electron correlation
    ↓
  DFT (B3LYP, PBE0, M06-2X): N³-N⁴, approximate correlation
    ↓
  MP2 (Møller-Plesset 2nd order): N⁵, perturbative correlation
    ↓
  CCSD (coupled cluster singles/doubles): N⁶
    ↓
  CCSD(T) (gold standard): N⁷, best practical accuracy
    ↓
  FCI (full configuration interaction): exact, N! (only tiny systems)

System size capabilities (rough guides):
  MM:          millions of atoms
  Semi-empirical: thousands of atoms
  DFT:         100-1000 atoms (routine), 10,000+ (linear scaling)
  MP2:         ~100 atoms
  CCSD(T):     ~30 atoms
```

### DFT Functionals
```python
def dft_functional_guide():
    return {
        'LDA (Local Density Approximation)': {
            'functionals':  'SVWN',
            'accuracy':     'Poor for chemistry, overbinds',
            'use':          'Solid state physics, rarely for chemistry'
        },
        'GGA (Generalized Gradient Approximation)': {
            'functionals':  'PBE, BLYP, BP86',
            'accuracy':     'Better than LDA, still lacks dispersion',
            'use':          'Large systems, solid state'
        },
        'Hybrid GGA': {
            'functionals':  'B3LYP (most used), PBE0, HSE06',
            'accuracy':     'Good for organic chemistry, thermochemistry',
            'B3LYP':        '20% HF exchange, popular since ~1994',
            'limitation':   'Poor dispersion interactions'
        },
        'Meta-GGA': {
            'functionals':  'TPSS, M06-L',
            'accuracy':     'Better than GGA, no HF exchange'
        },
        'Hybrid Meta-GGA': {
            'functionals':  'M06-2X, M06, TPSSh',
            'M06-2X':       'Excellent for main group thermochemistry + kinetics',
            'use':          'Reaction barriers, noncovalent interactions'
        },
        'Range-separated hybrid': {
            'functionals':  'ωB97X-D, CAM-B3LYP, LC-ωPBE',
            'accuracy':     'Better for charge transfer, excitations',
            'use':          'TD-DFT, long-range CT states'
        },
        'Dispersion corrections': {
            'D3':           'Grimme D3 correction (most common)',
            'D3BJ':         'D3 with Becke-Johnson damping (better)',
            'vdW-DF':       'Non-local correlation functional',
            'use':          'ALWAYS add dispersion for noncovalent interactions!'
        }
    }
```

### Basis Sets
```
Basis set notation guide:
  STO-nG: minimal, rarely used for chemistry
  n-31G:  split valence (6-31G most common split val)
  Polarization functions: * or (d) adds d on heavy atoms
                          ** or (d,p) adds p on H too
  Diffuse functions: + adds diffuse on heavy atoms
                     ++ adds on H too
  Examples:
    6-31G*    = 6-31G(d): good for optimization
    6-31G**   = 6-31G(d,p): better for H-containing
    6-31+G*   = adds diffuse (anions, lone pairs)
    6-311+G** : triple-zeta, good for single points

Correlation-consistent basis sets (Dunning):
  cc-pVDZ: double zeta
  cc-pVTZ: triple zeta (general purpose)
  cc-pVQZ: quadruple zeta
  aug-cc-pVTZ: augmented (diffuse, for anions/weak interactions)
  Extrapolate to CBS limit: E_CBS = E_∞ (complete basis set)

Def2 basis sets (Ahlrichs, ORCA/Turbomole):
  def2-SVP: split valence + polarization (geometry)
  def2-TZVP: triple zeta + polarization (energy)
  def2-QZVP: quadruple zeta (accurate reference)

Effective Core Potentials (ECP):
  Replace core electrons with pseudopotential
  Essential for heavy elements (Pd, Pt, Au, lanthanides)
  SDD, def2-ECP, LANL2DZ
```

---

## Molecular Mechanics & Force Fields
```python
def force_field_energy():
    """
    Classic MM energy function components.
    V_total = V_bond + V_angle + V_torsion + V_vdW + V_elec
    """
    return {
        'Bond stretching': {
            'formula':  'V = ½kb(r - r₀)²  (harmonic)',
            'better':   'Morse: V = De(1-exp(-α(r-r₀)))²',
            'params':   'kb (force constant), r₀ (equilibrium length)'
        },
        'Angle bending': {
            'formula':  'V = ½kθ(θ - θ₀)²',
            'params':   'kθ, θ₀ (equilibrium angle)'
        },
        'Torsional rotation': {
            'formula':  'V = Σ Vn/2 × (1 + cos(nφ - γ))',
            'n':        'Periodicity (1,2,3 or combination)',
            'use':      'Rotation barriers, conformational preferences'
        },
        'Improper torsion': {
            'formula':  'V = kξ(ξ - ξ₀)²',
            'use':      'Planarity of sp² groups (aromatic, carbonyl)'
        },
        'van der Waals (LJ)': {
            'formula':  'V = ε[(r_min/r)¹² - 2(r_min/r)⁶]',
            'r⁻¹²':    'Repulsion (Pauli exclusion)',
            'r⁻⁶':     'Attraction (London dispersion)',
            'cutoff':   'Usually 10-12 Å with switching function'
        },
        'Electrostatics': {
            'formula':  'V = qᵢqⱼ/4πε₀εrᵢⱼ',
            'charges':  'Partial atomic charges (RESP, CM5, AM1-BCC)',
            'long-range': 'Ewald summation or PME (particle mesh Ewald)'
        }
    }

def force_field_families():
    return {
        'AMBER': {
            'for':      'Proteins, nucleic acids, small molecules',
            'variants': 'ff14SB (protein), ff19SB, RNA.OL3, GAFF/GAFF2 (small mol)',
            'software': 'AMBER, GROMACS, OpenMM, NAMD'
        },
        'CHARMM': {
            'for':      'Proteins, lipids, nucleic acids, small molecules',
            'variants': 'CGenFF (small mol), CHARMM36 (protein+lipid)',
            'software': 'NAMD, GROMACS, OpenMM, CHARMM'
        },
        'GROMOS': {
            'for':      'Proteins, biomolecules',
            'variants': '54A7, 53A6',
            'software': 'GROMACS'
        },
        'OPLS': {
            'for':      'Organic liquids, proteins',
            'variants': 'OPLS3e, OPLS-AA/M',
            'software': 'Schrödinger, GROMACS'
        },
        'ReaxFF': {
            'for':      'Reactive systems (bond breaking/forming)',
            'method':   'Bond order potential',
            'use':      'Combustion, catalysis, materials'
        },
        'UFF/DREIDING': {
            'for':      'All elements (universal)',
            'accuracy': 'Lower, but covers full periodic table',
            'use':      'MOFs, inorganic materials, first approximation'
        }
    }
```

---

## Molecular Dynamics
```python
def md_algorithms():
    return {
        'Integrators': {
            'Verlet':       'r(t+dt) = 2r(t) - r(t-dt) + F/m × dt²',
            'Velocity Verlet': 'Stores v and r at same time step',
            'Leapfrog':     'v at half steps, r at full steps (GROMACS default)',
            'Time step':    '1-2 fs for all-atom, 4 fs with H-mass repartition'
        },
        'Thermostats (constant T)': {
            'Velocity rescaling': 'Scale velocities periodically (crude)',
            'Berendsen':    'Exponential approach to T_target (no proper ensemble)',
            'v-rescale':    'Berendsen + stochastic term (correct NVT)',
            'Nose-Hoover':  'Extended system, correct NVT ensemble',
            'Andersen':     'Random velocity reassignment'
        },
        'Barostats (constant P)': {
            'Berendsen':    'Fast pressure coupling (equilibration only)',
            'Parrinello-Rahman': 'Correct NPT ensemble (production runs)',
            'Monte Carlo':  'Volume moves'
        },
        'Constraints': {
            'LINCS':        'Linear constraint solver (GROMACS, bonds to H)',
            'SHAKE':        'Lagrange multipliers, bonds/angles',
            'SETTLE':       'Analytical for water (TIP3P, SPC/E)'
        },
        'Long-range electrostatics': {
            'PME':          'Particle Mesh Ewald (standard for biomolecules)',
            'PPPM':         'Particle-Particle-Particle-Mesh (LAMMPS)',
            'Cutoff':       'Only for truly short-range (rare in biomolecules)'
        }
    }

def md_workflow():
    return {
        'Step 1 — System preparation': [
            'Build/obtain structure (PDB, SMILES → 3D)',
            'Assign force field parameters',
            'Add solvent box (TIP3P, SPC/E, TIP4P-EW)',
            'Add ions to neutralize + physiological salt',
            'Check for missing residues, unnatural amino acids'
        ],
        'Step 2 — Energy minimization': [
            'Steepest descent or conjugate gradient',
            'Remove bad contacts from initial structure',
            'Converge until Fmax < 100-1000 kJ/mol/nm'
        ],
        'Step 3 — Equilibration': [
            'NVT equilibration: heat system to target T (100-500 ps)',
            'NPT equilibration: relax box dimensions (100-500 ps)',
            'Position restraints on heavy atoms during equilibration',
            'Check T, P, density, energy convergence'
        ],
        'Step 4 — Production MD': [
            'Remove restraints (unless specific reason)',
            'Run NPT or NVT for required timescale',
            'Save coordinates every 1-10 ps',
            'Monitor RMSD, energy, box size'
        ],
        'Step 5 — Analysis': [
            'RMSD: structural stability',
            'RMSF: per-residue flexibility',
            'Hydrogen bonds: count and lifetime',
            'Radius of gyration: compactness',
            'Secondary structure: DSSP analysis',
            'Principal component analysis (PCA)'
        ]
    }

def md_timescales():
    return {
        'Bond vibrations':          '1-10 fs',
        'Angle bending':            '10-100 fs',
        'Dihedral rotation':        '1-100 ps',
        'Loop motions':             '10 ps - 1 ns',
        'Helix-coil transitions':   '1-100 ns',
        'Protein folding (small)':  '1 μs - 1 ms',
        'Ion channel gating':       '1-100 ms',
        'Practical MD limit (2024)':'~1-10 μs (standard), >1 ms (Anton supercomputer)'
    }
```

---

## Free Energy Calculations
```python
def free_energy_methods():
    return {
        'Alchemical methods': {
            'FEP (Free Energy Perturbation)': {
                'formula':  'ΔA = -kBT ln⟨exp(-ΔU/kBT)⟩₀',
                'use':      'Relative binding free energies (ΔΔG)',
                'workflow': 'Mutate ligand A → B via λ windows (0→1)',
                'accuracy': '±0.5-1.0 kcal/mol with good sampling'
            },
            'Thermodynamic Integration (TI)': {
                'formula':  'ΔA = ∫₀¹ ⟨∂U/∂λ⟩λ dλ',
                'use':      'Same as FEP, more robust',
                'sampling': 'Multiple λ windows (16-32 typical)'
            },
            'Absolute binding free energy': {
                'formula':  'ΔGbind = Gcomplex - Greceptor - Gligand',
                'method':   'Double decoupling (annihilate in solvent + complex)',
                'accuracy': '±1-2 kcal/mol, computationally expensive'
            }
        },
        'End-point methods (faster, less accurate)': {
            'MM-PBSA': {
                'formula':  'ΔGbind = ΔH_MM + ΔGPB + ΔGSA - TΔS',
                'speed':    'Fast (~hours), useful for ranking',
                'accuracy': '±2-5 kcal/mol (ranking only, not absolute)',
                'use':      'Virtual screening hit prioritization'
            },
            'MM-GBSA': {
                'similar':  'MM-PBSA but GB instead of PB for solvation',
                'faster':   'Generalized Born faster than Poisson-Boltzmann'
            }
        },
        'Enhanced sampling': {
            'Metadynamics': {
                'idea':     'Add Gaussian bias to collective variables → escape local minima',
                'use':      'Free energy surfaces, rare events, binding/unbinding'
            },
            'Umbrella sampling': {
                'idea':     'Harmonic bias along reaction coordinate → PMF',
                'WHAM':     'Weighted histogram analysis method to combine windows'
            },
            'Replica exchange (REMD)': {
                'idea':     'Run multiple replicas at different T, swap periodically',
                'use':      'Improved conformational sampling, folding'
            },
            'Steered MD / SMD': {
                'idea':     'Apply external force to pull along reaction coordinate',
                'use':      'Binding/unbinding pathways, force-extension curves'
            }
        }
    }
```

---

## Molecular Docking
```python
def molecular_docking_guide():
    return {
        'Workflow': [
            '1. Prepare receptor: add H, assign charges, define binding site',
            '2. Prepare ligand: generate 3D, assign charges, set tautomers',
            '3. Define search space: grid box around binding site',
            '4. Run docking: search algorithm + scoring function',
            '5. Analyze results: cluster poses, rank by score',
            '6. Validate: compare with known ligands/crystal structures'
        ],
        'Search algorithms': {
            'Genetic algorithm':    'AutoDock, evolve population of poses',
            'Monte Carlo':          'Random moves + Boltzmann acceptance',
            'Fragment-based':       'Glide, GOLD: grow from anchor fragment',
            'Shape matching':       'ROCS, align to reference shape/pharmacophore'
        },
        'Scoring functions': {
            'Force field based':    'AutoDock (AD4), AMBER terms',
            'Empirical':            'Glide XP, X-Score: fitted to binding data',
            'Knowledge-based':      'PMF Score: statistical potentials',
            'ML-based':             'NNScore, RF-Score, newer deep learning'
        },
        'Software': {
            'AutoDock Vina':        'Free, fast, widely used, ~1 kcal/mol accuracy',
            'Glide (Schrödinger)':  'Commercial, high accuracy, virtual screening',
            'GOLD':                 'Commercial, good for flexible docking',
            'rDock':                'Free, flexible receptor/ligand',
            'DOCK':                 'Academic, pioneering program'
        },
        'Validation': {
            'Re-docking':           'Dock known ligand, check RMSD < 2 Å vs crystal',
            'Cross-docking':        'Dock into structure from different ligand',
            'Enrichment':           'ROC curve on actives vs decoys (AUC > 0.7 good)'
        },
        'Limitations': [
            'Flexible receptor motion often ignored (induced fit)',
            'Entropy poorly captured',
            'Solvation treatment approximate',
            'Scoring not reliable for rank-ordering (enrichment better than affinity)'
        ]
    }
```

---

## QM/MM Methods
```
Hybrid QM/MM:
  QM region: reactive center, metal site, chromophore
  MM region: protein environment, solvent
  Coupling: electrostatic embedding (MM charges polarize QM)
            mechanical embedding (simpler, less accurate)

Boundary treatment:
  Link atom scheme: H atom caps broken C-C bond at QM/MM boundary
  Frozen orbital: LSCF, GHO methods

ONIOM (Gaussian):
  E_ONIOM = E_QM(model) + E_MM(real) - E_MM(model)
  Can have multiple layers: QM1/QM2/MM (three-layer)

Applications:
  Enzyme mechanisms: QM active site + MM protein
  Photochemistry: QM chromophore + MM environment
  Drug binding: QM ligand + MM receptor
  Surface reactions: QM surface cluster + MM bulk

Software:
  Gaussian/ONIOM: standard for small systems
  ChemShell: flexible QM/MM framework
  AMBER + Gaussian/ORCA: biomolecular QM/MM
  CP2K: periodic QM/MM (materials, surfaces)
```

---

## Cheminformatics & Drug Discovery
```python
def cheminformatics_tools():
    return {
        'RDKit (Python)': {
            'use':      'Molecular manipulation, descriptors, fingerprints',
            'features': 'SMILES parsing, 2D/3D generation, substructure search',
            'example':  '''
from rdkit import Chem
from rdkit.Chem import Descriptors, AllChem
mol = Chem.MolFromSmiles("c1ccccc1")
mw = Descriptors.MolWt(mol)
fp = AllChem.GetMorganFingerprintAsBitVect(mol, 2, 2048)
'''
        },
        'Molecular descriptors': {
            '2D':       'MW, logP, TPSA, HBD, HBA, rotatable bonds',
            '3D':       'Shape, volume, surface area, moments of inertia',
            'Fingerprints': 'ECFP (Morgan), MACCS, RDKit, Avalon'
        },
        'Lipinski Ro5 (oral drugs)': {
            'MW':       '≤ 500 Da',
            'logP':     '≤ 5',
            'HBD':      '≤ 5 (H-bond donors)',
            'HBA':      '≤ 10 (H-bond acceptors)',
            'violations':'≤ 1 violation = likely oral bioavailability'
        },
        'ADMET prediction': {
            'Absorption':   'logP, pKa, solubility, Caco-2 permeability',
            'Distribution': 'logD, plasma protein binding, BBB penetration',
            'Metabolism':   'CYP450 substrate/inhibitor prediction',
            'Excretion':    'hERG inhibition (cardiotoxicity)',
            'Tools':        'SwissADME, pkCSM, ADMETlab, ADMET Predictor'
        },
        'QSAR modeling': {
            'workflow':     'Descriptors → feature selection → ML model → validation',
            'validation':   'Train/test split, cross-validation, Y-scrambling',
            'applicability':'Domain of applicability (AD) critical!',
            'ML methods':   'Random forest, SVM, neural networks, graph NNs'
        }
    }

def virtual_screening_workflow():
    return {
        'Library design': [
            'ZINC, Enamine, ChemDiv: purchasable compound libraries',
            'Filter by Ro5/drug-likeness first',
            'Remove PAINS (pan-assay interference compounds)',
            'Remove reactive groups (Michael acceptors, etc.)'
        ],
        'Screening cascade': [
            '1. Pharmacophore/shape screening: millions → thousands',
            '2. Rigid docking: thousands → hundreds',
            '3. Flexible/induced fit docking: hundreds → tens',
            '4. MM-GBSA rescoring: rank top hits',
            '5. MD-based FEP: confirm top 5-10 candidates',
            '6. Experimental validation: synthesis + assay'
        ],
        'De novo design': [
            'Fragment-based: grow from small binding fragments',
            'Generative AI: RNN, VAE, GAN, diffusion models',
            'Graph neural networks: property-guided generation',
            'Reinforce learning: optimize towards target properties'
        ]
    }
```

---

## Popular Software
```python
def computational_chemistry_software():
    return {
        'Quantum Chemistry': {
            'Gaussian':     'Most widely used, all QM methods, commercial',
            'ORCA':         'Free for academia, excellent DFT+correlation',
            'Psi4':         'Open source, high accuracy methods',
            'NWChem':       'Open source, parallel, periodic systems',
            'TURBOMOLE':    'Fast DFT, RI approximation, commercial',
            'CP2K':         'Periodic DFT, QM/MM, free'
        },
        'Molecular Dynamics': {
            'GROMACS':      'Free, fast, biomolecules + materials',
            'AMBER':        'Biomolecules, GPU-accelerated, commercial+free',
            'NAMD':         'Free, very scalable, biomolecules',
            'LAMMPS':       'Free, materials, custom force fields',
            'OpenMM':       'Python API, GPU, highly flexible',
            'DESMOND':      'Schrödinger, very fast on specialized hardware'
        },
        'Visualization': {
            'VMD':          'Free, MD trajectory analysis + visualization',
            'PyMOL':        'Protein visualization, commercial+open source',
            'UCSF Chimera': 'Free, biomolecular visualization',
            'Avogadro':     'Free, molecule building/editing',
            'GaussView':    'Gaussian input/output GUI'
        },
        'Drug Discovery': {
            'Schrödinger':  'Complete commercial suite (Glide, FEP+, Prime)',
            'MOE':          'Commercial, structure-based design',
            'AutoDock':     'Free, academic standard for docking',
            'DOCK':         'Free, UCSF academic',
            'OpenBabel':    'Free, file format conversion, basic operations'
        }
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Wrong basis set for heavy atoms | Use ECP (SDD, def2-ECP) for elements below Kr |
| Ignoring dispersion in DFT | Always add -D3BJ correction for noncovalent interactions |
| Not equilibrating MD properly | Check T, P, density convergence before production run |
| Too short MD timescale | Ensure sampling longer than slowest relevant motion |
| Docking score = binding affinity | Docking scores rank but don't predict ΔG accurately |
| Overfitting QSAR models | Always validate on external test set, check AD |
| Local minimum geometry | Use multiple starting geometries, check for imaginary frequencies |

---

## Related Skills

- **physical-chemistry-expert**: Quantum chemistry foundations
- **biochemistry-expert**: Protein structure and function
- **organic-chemistry-expert**: Reaction mechanisms QM can explain
- **machine-learning-expert**: ML methods in drug discovery
- **high-performance-computing**: HPC for large simulations
