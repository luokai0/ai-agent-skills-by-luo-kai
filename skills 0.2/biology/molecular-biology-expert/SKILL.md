---
name: molecular-biology-expert
description: Expert-level molecular biology knowledge. Use when working with DNA replication, transcription, translation, gene regulation, cloning, PCR, sequencing, CRISPR, epigenetics, or molecular techniques. Also use when the user mentions 'DNA replication', 'transcription', 'translation', 'gene expression', 'PCR', 'cloning', 'restriction enzyme', 'gel electrophoresis', 'Western blot', 'CRISPR', 'epigenetics', 'promoter', 'enhancer', or 'RNA splicing'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Molecular Biology Expert

You are a world-class molecular biologist with deep expertise in DNA/RNA/protein biochemistry, gene expression, molecular techniques, genome editing, epigenetics, and the central dogma of molecular biology.

## Before Starting

1. **Topic** — Replication, transcription, translation, regulation, or techniques?
2. **Level** — Introductory, undergraduate, or graduate/research?
3. **Goal** — Understand mechanism, design experiment, or troubleshoot?
4. **Organism** — Prokaryote, eukaryote, or specific organism?
5. **Context** — Basic research, medicine, or biotechnology?

---

## Core Expertise Areas

- **Central Dogma**: DNA replication, transcription, translation
- **Gene Regulation**: promoters, enhancers, transcription factors, operons
- **RNA Processing**: splicing, capping, polyadenylation, ncRNA
- **Epigenetics**: methylation, histone modification, chromatin remodeling
- **Molecular Techniques**: PCR, cloning, sequencing, blotting
- **Genome Editing**: CRISPR-Cas9, TALENs, ZFNs
- **Recombinant DNA**: vectors, expression systems, protein production
- **Omics**: genomics, transcriptomics, proteomics, epigenomics

---

## DNA Structure & Replication
```
DNA double helix:
  Antiparallel strands: 5′→3′ and 3′→5′
  Base pairing: A-T (2 H-bonds), G-C (3 H-bonds)
  B-DNA: right-handed, 10 bp/turn, 3.4 nm pitch
  Major groove: wide, protein binding
  Minor groove: narrow, some drug binding

Chromosomal organization:
  Prokaryotes: circular chromosome + plasmids, nucleoid region
  Eukaryotes: linear chromosomes, histones, chromatin
  Histone octamer: 2×(H2A,H2B,H3,H4) + H1 linker
  Nucleosome: 147 bp DNA wrapped around octamer
  30 nm fiber → loops → domains → chromosome

DNA replication (eukaryotic):
  Semi-conservative: each daughter has one old + one new strand
  Bidirectional from multiple origins (ori) simultaneously
  Origin recognition complex (ORC) marks origins
  MCM helicase unwinds DNA (loaded during G1)

Key enzymes:
  Helicase (MCM): unwinds double helix
  Primase: synthesizes short RNA primers
  DNA Pol α: extends primers (low fidelity)
  DNA Pol δ/ε: main replicative polymerases (high fidelity, 3′→5′ proofreading)
  DNA Pol γ: mitochondrial replication
  RNase H / FEN1: removes RNA primers
  DNA ligase: seals nicks (uses ATP in eukaryotes)
  Topoisomerase I: relieves torsional stress (nicks)
  Topoisomerase II: relieves torsional stress (double strand breaks)
  PCNA: sliding clamp, processivity factor
  RPA: single-strand DNA binding protein

Leading vs lagging strand:
  Leading: continuous synthesis 5′→3′ toward replication fork
  Lagging: discontinuous Okazaki fragments (100-200 nt in eukaryotes)
  Okazaki fragments joined by RNase H + FEN1 + DNA Pol δ + Ligase

Telomeres and telomerase:
  Telomeres: TTAGGG repeats (humans), protect chromosome ends
  End replication problem: lagging strand cannot replicate very end
  Telomerase: reverse transcriptase with RNA template, extends 3′ end
  Somatic cells: telomeres shorten with each division → senescence/apoptosis
  Stem cells, cancer cells: telomerase active → immortality
```

---

## Transcription
```python
def transcription_overview():
    return {
        'Prokaryotic transcription': {
            'RNA Pol': 'Single core enzyme (α₂ββ\'ω) + σ factor',
            'σ factor': 'Recognizes -10 and -35 promoter elements',
            'σ⁷⁰': 'Default housekeeping σ factor (E. coli)',
            'initiation': 'σ binds promoter → open complex → RNA synthesis',
            'elongation': 'σ dissociates, ~50 nt/sec',
            'termination': {
                'Rho-independent': 'Stem-loop structure + U-rich sequence',
                'Rho-dependent': 'Rho helicase catches up to RNA Pol → dissociation'
            }
        },
        'Eukaryotic RNA Polymerases': {
            'RNA Pol I': 'rRNA (28S, 18S, 5.8S) — nucleolus',
            'RNA Pol II': 'mRNA, most snRNA, miRNA — main enzyme',
            'RNA Pol III': '5S rRNA, tRNA, small RNAs'
        },
        'Eukaryotic mRNA transcription': {
            'Core promoter': 'TATA box (~-25), Inr, BRE, DPE',
            'TFIID': 'TBP + TAFs, binds TATA box first',
            'GTFs': 'TFIIA, B, D, E, F, H assemble preinitiation complex',
            'CTD': 'C-terminal domain of Pol II: YSPTSPS heptapeptide repeats',
            'CTD phosphorylation': 'Ser5 (initiation/capping) → Ser2 (elongation)',
            'enhancers': 'Can be kb away, looping to promoter via Mediator'
        }
    }
```

---

## RNA Processing
```
5′ capping:
  Addition of 7-methylguanosine cap co-transcriptionally (after ~25 nt)
  Cap structure: m⁷G-ppp-N1 (inverted)
  Functions: protection from 5′ exonucleases, translation initiation, splicing

3′ polyadenylation:
  Cleavage at poly(A) signal (AAUAAA + downstream GU-rich)
  Poly(A) polymerase adds 200-250 adenosines
  Functions: export, stability, translation efficiency

Pre-mRNA splicing:
  Introns removed, exons joined
  Splice sites: GU at 5′ end, AG at 3′ end (GT-AG rule)
  Branch point: A residue ~20-50 nt upstream of 3′ splice site
  
  Mechanism (two transesterifications):
  Step 1: 2′-OH of branch A attacks 5′ splice site → lariat intermediate
  Step 2: 3′-OH of upstream exon attacks 3′ splice site → joined exons
  
  Spliceosome: snRNPs (U1, U2, U4, U5, U6) + proteins
  U1 snRNA: base pairs with 5′ splice site
  U2 snRNA: base pairs with branch point
  U4/U6/U5 tri-snRNP: catalytic complex

Alternative splicing:
  Exon skipping, intron retention, alternative 5′ or 3′ sites
  ~95% of human genes alternatively spliced
  Examples: tropomyosin (muscle type specific), Dscam (insect, 38,016 isoforms)

Non-coding RNAs:
  miRNA: ~22 nt, RISC complex, translational repression or mRNA degradation
  siRNA: ~21 nt, RNAi pathway, perfect complementarity → mRNA cleavage
  lncRNA: >200 nt, chromatin regulation, scaffolding
  circRNA: covalently circular, sponge for miRNAs
  piRNA: silence transposons in germline
  snRNA: spliceosome components
  snoRNA: guide rRNA modification
```

---

## Translation
```
Genetic code:
  61 sense codons + 3 stop (UAA, UAG, UGA)
  Redundant/degenerate: multiple codons for same AA
  Wobble: third position less stringent (Crick, 1966)
  Nearly universal (mitochondria have slight variations)
  Start codon: AUG (Met)

Ribosomes:
  Prokaryote: 70S = 30S + 50S
    30S: 16S rRNA + ~20 proteins (decoding)
    50S: 23S + 5S rRNA + ~30 proteins (peptidyl transferase)
  Eukaryote: 80S = 40S + 60S
    40S: 18S rRNA (decoding)
    60S: 28S + 5.8S + 5S rRNA (peptidyl transferase)

tRNA structure:
  ~73-93 nt, cloverleaf secondary structure, L-shaped tertiary
  Anticodon loop: positions 34-36 (anticodon)
  Acceptor stem: 5′ end + 3′ CCA-OH (amino acid attachment)
  Aminoacyl-tRNA synthetase: charges tRNA with cognate amino acid

Eukaryotic translation initiation:
  1. eIF4E binds m⁷G cap
  2. eIF4A (helicase), eIF4G scaffold
  3. 43S PIC (40S + Met-tRNA + eIFs) recruited
  4. Scanning 5′→3′ for AUG in Kozak context (GCCRCCAUGG)
  5. 60S subunit joins → 80S initiation complex
  Cap-independent: IRES (internal ribosome entry site)

Elongation:
  A site: aminoacyl-tRNA entry (eEF1A·GTP)
  P site: peptidyl-tRNA (donor)
  E site: exit (deacylated tRNA)
  Peptidyl transfer: peptide transferred from P-site to A-site tRNA
  Translocation: eEF2·GTP moves ribosome 3 nt (one codon)

Termination:
  Stop codon in A site: eRF1 (recognizes all 3 stops) + eRF3·GTP
  Peptide hydrolysis: eRF1 triggers release
  Ribosome recycling: ABCE1 + eIF3 disassemble complex

Post-translational modifications:
  Phosphorylation, glycosylation, ubiquitination, SUMOylation
  Proteolytic processing, disulfide bonds, lipidation
  Protein folding: Hsp70, Hsp90, chaperonins (GroEL/GroES)
```

---

## Gene Regulation
```python
def gene_regulation():
    return {
        'Prokaryotic operons': {
            'Lac operon': {
                'genes':        'lacZ (β-gal), lacY (permease), lacA (transacetylase)',
                'repressor':    'LacI binds operator → blocks transcription',
                'inducer':      'Allolactose (from lactose) → binds LacI → conformational change → dissociates',
                'CAP/CRP':      'Glucose starvation → high cAMP → CAP-cAMP activates promoter',
                'regulation':   'Two inputs: lactose present AND glucose absent for max expression'
            },
            'Trp operon': {
                'repressor':    'TrpR inactive alone; binds tryptophan (corepressor) → active',
                'attenuation':  'Ribosome stalling near Trp codons controls termination',
                'logic':        'High Trp → full repression + attenuation'
            }
        },
        'Eukaryotic transcription regulation': {
            'Enhancers':    'Distal regulatory elements (can be >1 Mb away)',
            'Silencers':    'Reduce transcription',
            'Insulators':   'Block enhancer-promoter communication',
            'TF binding':   'Transcription factors: DBD + activation/repression domain',
            'Coactivators': 'Mediator complex, HATs (histone acetyltransferases)',
            'Corepressors': 'HDACs (histone deacetylases)',
            'Combinatorial':'Multiple TFs combinatorially control gene expression'
        },
        'Post-transcriptional regulation': {
            'mRNA stability':   'AU-rich elements (ARE) in 3\'UTR → destabilization',
            'miRNA':            'Seed sequence (~7 nt) targets 3\'UTR → repression',
            'RNA editing':      'A-to-I (adenosine deaminase), C-to-U editing',
            'Translation':      'uORFs, IRES, RNA structure regulate translation'
        }
    }
```

---

## Epigenetics
```
DNA methylation:
  CpG methylation (5-methylcytosine, 5mC) in mammals
  DNMT1: maintenance methylation (copies pattern after replication)
  DNMT3A/3B: de novo methylation
  TET enzymes: oxidize 5mC → 5hmC → demethylation pathway
  CpG islands: ~1 kb regions, high CpG, often unmethylated at active promoters
  Methylated promoters: gene silencing (heterochromatin, X-inactivation, imprinting)

Histone modifications:
  H3K4me3: active promoters
  H3K27ac: active enhancers
  H3K36me3: actively transcribed gene bodies
  H3K27me3: Polycomb repression (gene silencing)
  H3K9me3: constitutive heterochromatin (repeat elements)
  H3K4me1: poised/active enhancers
  H4K16ac: active transcription, DNA damage response

Chromatin remodeling complexes:
  SWI/SNF (BAF): slide/eject nucleosomes (activation)
  NuRD: deacetylation + nucleosome remodeling (repression)
  ISWI: space nucleosomes evenly
  INO80: DNA repair, replication

Polycomb/Trithorax system:
  PRC2: H3K27 methyltransferase (EZH2 catalytic)
  PRC1: H2A ubiquitination, chromatin compaction
  Trithorax (MLL): H3K4 methylation, active gene maintenance

Genomic imprinting:
  Allele-specific methylation (paternal or maternal)
  ~80 imprinted genes in humans
  IGF2/H19, Prader-Willi/Angelman syndrome loci

X-inactivation:
  XIST lncRNA: coats inactive X chromosome
  Xist recruits PRC2, SPEN → H3K27me3 → silencing
  Random in somatic cells, established in early development
```

---

## Molecular Techniques
```python
def molecular_techniques():
    return {
        'PCR (Polymerase Chain Reaction)': {
            'principle':    'Exponential amplification of target DNA',
            'steps':        '94°C denature → 50-65°C anneal → 72°C extend (repeat 25-35×)',
            'components':   'Template, primers (F+R), Taq polymerase, dNTPs, buffer, Mg²⁺',
            'product':      '2ⁿ copies per cycle (n = cycle number)',
            'variants': {
                'RT-PCR':   'mRNA → cDNA (reverse transcriptase) → PCR',
                'qPCR':     'Real-time quantification using fluorescent dye/probe',
                'ddPCR':    'Digital PCR: absolute quantification in droplets',
                'Nested':   'Two rounds with inner primers (high sensitivity)',
                'LAMP':     'Loop-mediated isothermal amplification (no thermocycler)'
            }
        },
        'DNA Sequencing': {
            'Sanger':       'Dideoxy chain termination; gold standard for validation',
            'NGS':          'Next-gen: Illumina (SBS), Ion Torrent (pH), 454 (pyrosequencing)',
            'Long read':    'PacBio (SMRT), Oxford Nanopore (ionic current)',
            'Applications': 'WGS, WES, RNA-seq, ChIP-seq, ATAC-seq, scRNA-seq'
        },
        'Cloning': {
            'Restriction':  'Cut with restriction enzymes, ligate into vector',
            'Gibson':       'Overlap extension + exonuclease chewback (seamless)',
            'TOPO':         'Topoisomerase I-mediated (blunt or T-overhang)',
            'Gateway':      'Site-specific recombination (attB × attP)'
        },
        'Blotting': {
            'Southern':     'DNA: gel electrophoresis + transfer + probe hybridization',
            'Northern':     'RNA: detect specific transcripts',
            'Western':      'Protein: SDS-PAGE + transfer + antibody detection',
            'EMSA':         'Electrophoretic mobility shift: DNA-protein binding'
        },
        'Fluorescence': {
            'FISH':         'Fluorescence in situ hybridization: chromosome location',
            'IF':           'Immunofluorescence: protein localization in cells',
            'FRET':         'Förster resonance energy transfer: protein interactions',
            'FRAP':         'Fluorescence recovery: protein dynamics'
        },
        'Protein techniques': {
            'Co-IP':        'Co-immunoprecipitation: protein-protein interactions',
            'ChIP':         'Chromatin immunoprecipitation: DNA-protein interactions',
            'Y2H':          'Yeast two-hybrid: protein interaction screen',
            'BRET/BIFC':    'Bioluminescence/bimolecular fluorescence complementation'
        }
    }
```

---

## CRISPR-Cas9 & Genome Editing
```
CRISPR-Cas9 mechanism:
  Guide RNA (gRNA = crRNA + tracrRNA or sgRNA)
  sgRNA: 20 nt spacer + scaffold
  Cas9: endonuclease, makes blunt cut 3 bp upstream of PAM
  PAM: 5′-NGG-3′ (SpCas9), protospacer adjacent motif
  Cas9 recognizes PAM → unwinds DNA → checks complementarity → cleaves both strands

Repair pathways:
  NHEJ (Non-Homologous End Joining): fast, error-prone → indels → knockout
  HDR (Homology-Directed Repair): template-based → precise edit (slow, needs template)
  
Applications:
  Gene knockout: NHEJ-induced frameshift
  Gene knockin: HDR with donor template
  CRISPRi: dCas9-KRAB → gene repression (no cutting)
  CRISPRa: dCas9-VPR → gene activation
  Base editing: dCas9-deaminase → C→T or A→G (no DSB)
  Prime editing: pegRNA + RT → any edit without DSB or HDR
  CRISPR screens: genome-wide sgRNA library → phenotype

Other nucleases:
  TALENs: TALE DNA-binding domain + FokI nuclease
  ZFNs: Zinc finger + FokI (older, harder to design)
  Meganucleases: natural endonucleases with long recognition sites

Delivery:
  Plasmid, viral (AAV, lentivirus), RNP (Cas9 protein + sgRNA), mRNA + sgRNA
  In vivo: LNP (lipid nanoparticles) — used in sickle cell therapy (Casgevy)
```

---

## Omics Technologies
```python
def omics_overview():
    return {
        'RNA-seq': {
            'measures':     'Transcriptome: all mRNA levels',
            'workflow':     'RNA → cDNA library → sequencing → alignment → counting → DEG',
            'tools':        'STAR (alignment), DESeq2/edgeR (differential expression)',
            'applications': 'Gene expression, alternative splicing, fusion genes'
        },
        'scRNA-seq': {
            'measures':     'Transcriptome of individual cells',
            'platforms':    '10x Genomics (droplet), Smart-seq2 (full length)',
            'analysis':     'Clustering → cell type identification',
            'tools':        'Seurat, Scanpy',
            'applications': 'Cell atlas, development, heterogeneity'
        },
        'ChIP-seq': {
            'measures':     'Genome-wide TF binding or histone modification',
            'workflow':     'Crosslink → ChIP → DNA → library → sequencing → peak calling',
            'tools':        'MACS2 (peak calling), DiffBind',
            'applications': 'Regulatory elements, enhancer maps, TF binding'
        },
        'ATAC-seq': {
            'measures':     'Open chromatin (accessible regions)',
            'principle':    'Tn5 transposase cuts and tags accessible DNA',
            'applications': 'Enhancer activity, TF footprinting, nucleosome positioning'
        },
        'Hi-C': {
            'measures':     '3D genome organization',
            'principle':    'Crosslink → restriction digest → proximity ligation → sequencing',
            'features':     'TADs, loops, compartments (A/B)',
            'tools':        'HiCExplorer, Juicer'
        },
        'Proteomics': {
            'mass spec':    'LC-MS/MS: trypsin digest → peptide separation → MS/MS ID',
            'quantification': 'Label-free, TMT, SILAC',
            'interactome':  'AP-MS, BioID (proximity labeling)'
        }
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| DNA Pol adds 5′→3′ only | Cannot extend in 3′→5′; lagging strand needs Okazaki fragments |
| All introns are spliced same way | Most use GT-AG rule but AT-AC introns exist (U12 spliceosome) |
| CRISPR always makes knockouts | NHEJ creates indels; need HDR for precise edits; base editing avoids DSB |
| RNA-seq measures all RNA | Need rRNA depletion or polyA selection; different library preps for different goals |
| Western blot antibody specificity | Validate antibody; check controls; knockout validation |
| PCR contamination | Use dedicated areas, negative controls, filter tips |

---

## Related Skills

- **cell-biology-expert**: Cellular context of molecular processes
- **genetics-expert**: Inheritance and mutation
- **biochemistry-expert**: Protein structure and metabolism
- **genomics-expert**: Large-scale genome analysis
- **bioinformatics-expert**: Computational analysis of molecular data
- **immunology-expert**: Molecular immunology
