---
name: materials-informatics-expert
version: 1.0.0
description: Expert-level materials informatics covering materials databases, machine learning for property prediction, high-throughput computation, and data-driven materials discovery.
author: luokai25
tags: [materials informatics, machine learning, materials databases, high-throughput, DFT]
---

# Materials Informatics Expert

## Before Starting
1. Which material class? (metals, ceramics, polymers, 2D materials)
2. Property prediction or structure generation?
3. Computational or experimental data source?

## Core Expertise Areas

### Materials Databases
Materials Project: DFT-calculated properties for over 150,000 inorganic compounds.
AFLOW: high-throughput DFT database with thermodynamic and electronic properties.
OQMD: open quantum materials database, formation energies and stability.
NOMAD: repository for experimental and computational materials data.
Cambridge Structural Database: crystal structures from X-ray diffraction.

### Featurization
Composition features: element fractions, stoichiometry-based descriptors.
Structure features: radial distribution function, coordination environment.
Electronic structure: band gap, DOS features from DFT calculations.
SOAP: smooth overlap of atomic positions, invariant descriptor for local environments.
Graph neural networks: represent crystal structure as graph, learn from topology.

### ML for Property Prediction
CGCNN: crystal graph convolutional neural network, predict formation energy.
MEGNet: graph network for molecules and crystals, multi-property prediction.
Gaussian process: uncertainty quantification, active learning integration.
Transfer learning: pre-train on large DFT dataset, fine-tune on small experimental.

### High-Throughput Workflows
VASP and Quantum ESPRESSO: DFT codes for electronic structure calculations.
pymatgen: Python library for materials analysis and database interface.
Fireworks: workflow management for high-throughput calculations.
Active learning: select most informative experiments to minimize label cost.

## Best Practices
- Validate ML models on held-out data not used in training
- Use uncertainty quantification to guide experimental validation
- Check data quality and consistency before training
- Consider interpretability alongside prediction accuracy

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Training and test set overlap | Ensure proper splitting by structure or composition |
| Ignoring data biases | Databases oversample certain chemistries |
| Overfitting small datasets | Use cross-validation and regularization |
| DFT-experiment gap | Account for systematic errors between DFT and experiment |

## Related Skills
- machine-learning-expert
- computational-chemistry-expert
- physics/condensed-matter-expert
