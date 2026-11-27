---
name: evolutionary-biology-expert
version: 1.0.0
description: Expert-level evolutionary biology covering natural selection, genetic drift, molecular evolution, phylogenetics, speciation, macroevolution, and the modern synthesis.
author: luo-kai
tags: [evolution, natural selection, phylogenetics, speciation, adaptation, genetics]
---

# Evolutionary Biology Expert

## Before Starting
1. Microevolution or macroevolution focus?
2. Molecular phylogenetics or morphological?
3. Population genetics or comparative biology?

## Core Expertise Areas

### Natural Selection
Requirements: variation, heritability, differential fitness.
Types: directional, stabilizing, disruptive, sexual, kin, group.
Adaptation: trait increasing fitness in current environment.
Fitness: reproductive success relative to population mean.
Selection coefficient s: measure of fitness difference between genotypes.

### Genetic Drift
Random change in allele frequencies due to sampling in finite populations.
Effective population size Ne: determines rate of drift.
Bottleneck: severe reduction reduces genetic diversity.
Founder effect: small founding population carries limited diversity.
Genetic drift vs selection: drift dominates when Nes much less than 1.

### Molecular Evolution
Neutral theory: most molecular variation is selectively neutral (Kimura).
Nearly neutral theory: slightly deleterious mutations important in small populations.
Molecular clock: rate of neutral substitution approximately constant over time.
dN/dS ratio: synonymous vs nonsynonymous substitutions — positive selection if dN/dS greater than 1.
Molecular phylogenetics: sequence alignment, substitution models, tree inference.

### Phylogenetics
Parsimony: minimize evolutionary changes required to explain data.
Maximum likelihood: find tree maximizing probability of observed data.
Bayesian inference: posterior probability of trees given data and prior.
Substitution models: JC69, HKY85, GTR — nucleotide substitution rates.
Bootstrap support: resampling to assess node confidence.

### Speciation
Allopatric: geographic isolation leads to reproductive isolation.
Sympatric: speciation without geographic barrier (rare, requires strong selection).
Reproductive isolation: prezygotic (behavior, morphology) and postzygotic (hybrid sterility).
Biological species concept: groups that interbreed and are reproductively isolated from others.

## Key Patterns



## Best Practices
- Always root phylogenetic trees with an outgroup
- Test multiple substitution models and select by AIC/BIC
- Distinguish adaptation from exaptation
- Consider phylogenetic signal when comparing traits across species
- Account for incomplete lineage sorting in species tree estimation

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Adaptationist storytelling | Test adaptive hypotheses with quantitative predictions |
| Ignoring drift | Selection is not the only evolutionary force |
| Long branch attraction | Use better substitution models, add taxa |
| Confusing gene trees and species trees | Use coalescent-based methods for species trees |

## Related Skills
- genetics-expert
- ecology-expert
- genomics-expert
- molecular-biology-expert
