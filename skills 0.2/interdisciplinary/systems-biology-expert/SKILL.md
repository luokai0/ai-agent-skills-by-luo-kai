---
name: systems-biology-expert
version: 1.0.0
description: Expert-level systems biology covering network analysis, multi-omics integration, dynamic modeling, signaling pathway analysis, and emergent properties of biological systems.
author: luokai25
tags: [systems biology, network analysis, multi-omics, signaling, emergent properties]
---

# Systems Biology Expert

## Before Starting
1. Which biological scale? (molecular, cellular, tissue, organism)
2. Data-driven or mechanistic modeling?
3. Steady-state or dynamic analysis?

## Core Expertise Areas

### Biological Networks
Gene regulatory networks: transcription factor to target gene interactions.
Signaling networks: receptor to effector cascades with feedback and crosstalk.
Metabolic networks: enzyme-catalyzed reaction networks, stoichiometric models.
PPI networks: protein interaction maps from yeast two-hybrid, co-IP, mass spec.
Network motifs: recurring subgraphs with functional significance.

### Dynamic Modeling
ODE models: deterministic, kinetic rate laws, mass action and Michaelis-Menten.
Stochastic models: Gillespie algorithm, intrinsic noise from low molecule numbers.
Boolean models: discrete states on and off, fast qualitative analysis.
Agent-based models: individual cell behaviors produce tissue-level patterns.
Bifurcation analysis: how steady states change with parameter variation.

### Multi-Omics Integration
Transcriptomics: mRNA levels by RNA-seq, condition-specific expression.
Proteomics: protein abundance by mass spectrometry, post-translational modifications.
Metabolomics: small molecule profiling by NMR or mass spectrometry.
Integration methods: correlation, regression, network-based, and ML approaches.
Single-cell multi-omics: ATAC-seq and RNA-seq in same cell, regulatory inference.

### Emergent Properties
Robustness: system maintains function under perturbations, feedback-mediated.
Adaptation: return to basal state after step stimulus, integral feedback required.
Bistability: two stable states, hysteresis, switch-like behavior.
Oscillations: sustained periodic behavior from negative feedback with delay.
Noise propagation: how fluctuations in one component affect others.

## Best Practices
- Validate models with independent experimental data not used for fitting
- Perform sensitivity analysis to identify key parameters
- Consider measurement noise when fitting models to experimental data
- Use identifiability analysis before parameter estimation

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Overfitting complex models | Use parsimony, prefer simpler models with good fit |
| Ignoring noise in gene expression | Stochastic models needed for low copy number genes |
| Missing feedback loops | Systematically map all regulatory interactions |
| Confusing correlation with causation | Perturbation experiments needed to establish causation |

## Related Skills
- computational-biology-expert
- molecular-biology-expert
- mathematics/differential-equations-expert
