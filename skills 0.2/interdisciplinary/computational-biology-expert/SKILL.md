---
name: computational-biology-expert
version: 1.0.0
description: Expert-level computational biology covering molecular dynamics simulation, protein structure prediction, systems biology, network analysis, and machine learning in biology.
author: luokai25
tags: [computational biology, molecular dynamics, protein structure, systems biology, ML]
---

# Computational Biology Expert

## Before Starting
1. Molecular, cellular, or systems level?
2. Simulation, prediction, or data analysis?
3. Which software ecosystem? (Python, R, GROMACS, NAMD)

## Core Expertise Areas

### Molecular Dynamics
Force fields: AMBER, CHARMM, GROMOS define atom interactions.
Integration: Verlet or leapfrog algorithm integrates equations of motion.
Periodic boundary conditions: avoid surface effects, simulate bulk behavior.
Thermostat and barostat: maintain temperature and pressure in NPT ensemble.
Free energy: umbrella sampling, metadynamics, alchemical perturbation methods.

### Protein Structure Prediction
AlphaFold2: deep learning, near-experimental accuracy for single domains.
ESMFold: language model based, faster but slightly less accurate than AlphaFold2.
Homology modeling: template-based for sequences with known homologs.
Intrinsically disordered: not well-handled by structure prediction, need ensemble.
Structure validation: DOPE score, MolProbity, Ramachandran plot analysis.

### Systems Biology
ODE models: deterministic kinetic models of reaction networks.
Stochastic simulation: Gillespie algorithm for small molecule numbers.
Boolean networks: coarse-grained on/off gene regulation models.
Metabolic flux analysis: FBA predicts steady-state fluxes in metabolic networks.
Parameter estimation: MCMC and optimization for fitting models to data.

### Network Biology
PPI networks: protein-protein interaction networks, hub proteins.
Gene regulatory networks: transcription factor target relationships.
Network topology: degree distribution, clustering coefficient, shortest paths.
Community detection: modules in biological networks correspond to functional units.

## Best Practices
- Always validate simulation against experimental observables
- Use sufficient simulation time to ensure convergence
- Apply appropriate statistical tests to simulation data
- Document all parameters and software versions for reproducibility

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Insufficient simulation length | Check convergence with multiple metrics |
| Wrong protonation states | Calculate pKa and set protonation at simulation pH |
| Overinterpreting AlphaFold structures | High confidence regions are reliable, low confidence are not |
| Ignoring model identifiability | Many parameters may give same fit to data |

## Related Skills
- molecular-biology-expert
- bioinformatics-expert
- machine-learning-expert
