---
name: bioinformatics-expert
version: 1.0.0
description: Expert-level bioinformatics covering sequence analysis, structural bioinformatics, database searching, phylogenetic analysis, NGS data processing, single-cell analysis, and machine learning in biology.
author: luo-kai
tags: [bioinformatics, sequence analysis, NGS, structural biology, databases, Python]
---

# Bioinformatics Expert

## Before Starting
1. Sequence, structure, or expression data?
2. Genomics, transcriptomics, proteomics, or metagenomics?
3. Tool usage or algorithm development?

## Core Expertise Areas

### Sequence Analysis
Pairwise alignment: Needleman-Wunsch (global), Smith-Waterman (local).
Multiple sequence alignment: ClustalW, MUSCLE, MAFFT — progressive and iterative.
Database search: BLAST — scoring matrix (BLOSUM62), E-value, bit score.
Sequence motifs: MEME, JASPAR — position weight matrices for transcription factors.

### NGS Data Processing
Quality control: FastQC, trimming (Trimmomatic, fastp).
Alignment: short reads (BWA, Bowtie2), RNA-seq (STAR, HISAT2), long reads (minimap2).
Variant calling: GATK, FreeBayes, DeepVariant.
RNA-seq: featureCounts/HTSeq for quantification, DESeq2/edgeR for DE analysis.

### Structural Bioinformatics
Protein structure: PDB format, secondary structure prediction (PSIPRED).
Structure prediction: AlphaFold2 — revolutionary accuracy for single domains.
Molecular docking: AutoDock, Glide — predicting protein-ligand binding.
Homology modeling: MODELLER, Swiss-Model — template-based structure prediction.

### Single-Cell Analysis
scRNA-seq pipeline: Cell Ranger (10x), Seurat/Scanpy for analysis.
Quality control: UMI counts, gene counts, mitochondrial fraction.
Clustering: graph-based (Leiden, Louvain), UMAP/tSNE visualization.
Trajectory analysis: RNA velocity, Monocle, PAGA.

### Python for Bioinformatics
BioPython: sequence parsing, BLAST interface, structure analysis.
Pandas: tabular data — VCF files, expression matrices.
Matplotlib/Seaborn: volcano plots, heatmaps, PCA plots.
Scikit-learn: classification of sequences, feature extraction.

## Key Patterns



## Best Practices
- Always check data quality before analysis
- Use containerized tools (Docker/Singularity) for reproducibility
- Version control analysis scripts and document software versions
- Validate bioinformatic findings with experimental orthogonal methods
- Consider batch effects in multi-sample analyses

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Not checking alignment quality | Always review alignment stats and coverage |
| Ignoring multiple testing | Use FDR correction (Benjamini-Hochberg) |
| Wrong reference genome build | Confirm genome version matches annotation |
| Skipping normalization | Always normalize before comparing samples |

## Related Skills
- genomics-expert
- molecular-biology-expert
- machine-learning-expert
- python-expert
