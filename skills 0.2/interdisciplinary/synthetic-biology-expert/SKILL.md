---
name: synthetic-biology-expert
version: 1.0.0
description: Expert-level synthetic biology covering genetic parts and devices, genetic circuit design, metabolic engineering, genome engineering, biosafety, and industrial applications.
author: luokai25
tags: [synthetic biology, genetic circuits, metabolic engineering, CRISPR, biofoundry]
---

# Synthetic Biology Expert

## Before Starting
1. Prokaryotic or eukaryotic host organism?
2. Genetic circuits or metabolic engineering focus?
3. Research tool or industrial production application?

## Core Expertise Areas

### Genetic Parts
Promoters: control transcription initiation, constitutive or inducible.
RBS: ribosome binding site controls translation efficiency.
Terminators: stop transcription, prevent read-through.
Registry: iGEM parts registry catalogs standardized biological parts.
Characterization: measure part behavior quantitatively across contexts.

### Genetic Circuits
Toggle switch: bistable circuit with two mutually repressing promoters.
Oscillator: repressilator uses three repressors in ring to generate oscillations.
Logic gates: AND, OR, NOT implemented with transcription factor cascades.
Feedback control: negative feedback reduces variability in gene expression.
Retroactivity: downstream circuit components affect upstream behavior.

### Metabolic Engineering
Pathway design: identify enzymes to convert substrate to target product.
Flux balance analysis: optimize metabolic fluxes using linear programming.
Cofactor engineering: balance NADH and NADPH pools for pathway function.
Dynamic control: regulate pathway expression in response to metabolite levels.
Tolerance engineering: improve host tolerance to toxic products.

### Genome Engineering
CRISPR-Cas9: programmable nuclease for precise genome editing.
Base editing: convert one base to another without double strand break.
Prime editing: search and replace genomic edits, versatile and precise.
Whole genome synthesis: synthesize entire bacterial genomes from DNA oligos.

## Best Practices
- Characterize parts quantitatively before assembling into circuits
- Use orthogonal parts to reduce interference between circuits
- Consider metabolic burden on host when expressing many heterologous genes
- Follow biosafety guidelines and institutional review for all work

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Context dependence of parts | Characterize in intended host not just standard strain |
| Genetic instability | Use stable integration sites, minimize selection pressure |
| Ignoring metabolic burden | Measure growth rate with and without transgene |
| Retroactivity breaking circuit behavior | Add insulators between circuit modules |

## Related Skills
- molecular-biology-expert
- computational-biology-expert
- bioinformatics-expert
