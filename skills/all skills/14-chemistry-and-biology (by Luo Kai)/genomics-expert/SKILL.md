---
name: genomics-expert
version: 1.0.0
description: Expert-level genomics covering whole genome sequencing, genome assembly, annotation, comparative genomics, functional genomics, single-cell genomics, and multi-omics integration.
author: luo-kai
tags: [genomics, sequencing, NGS, assembly, annotation, omics]
---

# Genomics Expert

## Before Starting
1. What organism and genome size?
2. Short-read or long-read sequencing?
3. Whole genome, exome, or targeted?

## Core Expertise Areas

### Sequencing Technologies
Short-read: Illumina — high accuracy, low cost, 150-300bp reads.
Long-read: PacBio (SMRT), Oxford Nanopore — spans repeats, structural variants.
Hi-C: chromatin conformation, scaffolding assemblies.
Single-cell: 10x Genomics, Drop-seq — individual cell transcriptomes.

### Genome Assembly
De novo assembly: overlap-layout-consensus, de Bruijn graphs.
Tools: SPAdes (short-read), Flye (long-read), Hifiasm (HiFi).
Assembly metrics: N50, L50, contig count, genome completeness (BUSCO).
Scaffolding: Hi-C, optical mapping, genetic maps.

### Genome Annotation
Structural annotation: gene prediction (Augustus, MAKER), repeat masking (RepeatMasker).
Functional annotation: BLAST, InterPro, GO terms, KEGG pathways.
Non-coding elements: promoters, enhancers, regulatory regions.
Comparative annotation: synteny, ortholog identification.

### Variant Calling
SNVs and indels: GATK HaplotypeCaller, DeepVariant.
Structural variants: Manta, LUMPY, PBSV.
Copy number variants: CNVkit, Control-FREEC.
Variant filtering: VQSR, hard filters, population frequency.

### Functional Genomics
RNA-seq: transcript quantification, differential expression (DESeq2, edgeR).
ChIP-seq: protein-DNA binding, peak calling (MACS2).
ATAC-seq: chromatin accessibility, open chromatin regions.
Metagenomics: community profiling, functional annotation of environmental samples.

## Key Patterns



## Best Practices
- Always check sequencing QC before assembly or mapping
- Use BUSCO to assess assembly and annotation completeness
- Filter variants by quality score and depth before analysis
- Validate structural variants with orthogonal evidence
- Document software versions for reproducibility

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Low coverage causing false variants | Aim for 30x minimum for WGS |
| Repeat regions causing assembly gaps | Use long reads to span repeats |
| Contamination in assemblies | Run BLAST against contaminant databases |
| Ignoring batch effects in RNA-seq | Include batch as covariate in model |

## Related Skills
- molecular-biology-expert
- bioinformatics-expert
- genetics-expert
- computational-chemistry-expert
