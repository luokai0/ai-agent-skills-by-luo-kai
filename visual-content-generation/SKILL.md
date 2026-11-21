---
name: visual-content-generation
description: Use when producing, editing, or validating generated images, diagrams, charts, or other visual assets for data and AI work, including dataset illustrations, model-output figures, slide visuals, and synthetic image batches that must meet stated fidelity, labeling, and provenance requirements.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Visual Content Generation

## Purpose and boundaries

This skill covers turning a stated visual need into a verified image, diagram, chart, or synthetic image set. Typical work: figures for technical reports, architecture diagrams, data charts rendered from tabular inputs, illustrative images for model cards, and synthetic image batches for augmentation or evaluation.

In scope: choosing the generation method (code-rendered vector or chart, text-to-image model, image editing, or manual composition), specifying prompts and parameters, checking outputs against requirements, and packaging assets with provenance records.

Out of scope: generating images of real identifiable people without consent, producing content that impersonates real persons or organizations, creating misleading data visualizations, bypassing provider content policies, and making legal claims about image ownership or licensing. Refer those to the appropriate owner.

## Inputs and assumptions

Before starting, establish:

1. **Purpose and audience**: publication, internal review, training data, demo.
2. **Content specification**: exact labels, numbers, entities, relationships, or scene elements. Numbers and labels must come from a source file, never from memory.
3. **Format**: resolution, aspect ratio, file type, color space, transparency, accessibility requirements (alt text, contrast).
4. **Provenance rules**: whether the output must be labeled as synthetic, and the required metadata.
5. **Tooling available**: which generators, editors, or plotting libraries are approved. Confirm their current capabilities and parameter names against official documentation; do not rely on remembered flags.

If any of items 2 through 4 are missing, ask. Do not assume data values or branding.

## Operating workflow

1. **Classify the request.** Data-bound (charts, plots, quantitative diagrams) versus representational (illustrations, scenes, synthetic photos) versus structural (flowcharts, architecture). This determines the method.
2. **Select the method.**
   - Data-bound: render with a plotting or vector tool from the source data. Never ask a generative image model to produce values.
   - Structural: author as diagram source (for example, a text-defined diagram or SVG) so nodes and edges are editable and checkable.
   - Representational: use a generative model, then edit as needed.
3. **Write the specification.** Produce a one-page spec: content list, layout, palette, typography, excluded elements, and the output file name convention.
4. **Generate a first pass.** For generative models, run a small batch (typically 4 or fewer) to explore variance before committing to a parameter set.
5. **Refine.** Change one variable at a time: prompt wording, seed or variation control if available, reference inputs, or crop. Log each change.
6. **Post-process.** Crop, resize, convert color profile, add text overlays in a vector layer rather than inside raster output where possible.
7. **Verify** (see below), then **package** with provenance.

## Decision gates

- **Gate A (method):** If a chart encodes quantities, it must be code-rendered from data. Generative output for quantitative content is rejected.
- **Gate B (text in image):** Generative models frequently misspell or garble text. Any visible text must be added as a vector overlay or verified character-by-character; otherwise use a text-free generation and add labels separately.
- **Gate C (realism):** If the output depicts a real person, real location, or real event, stop and obtain explicit approval and a disclosure plan.
- **Gate D (external use):** Publishing, uploading to a third-party service, or inserting into a shared dataset requires explicit approval from the owner.
- **Gate E (destructive edits):** Overwriting original assets, deleting source files, or replacing an approved figure requires explicit approval. Save new versions alongside originals.

## Verification and evidence

Check each item and record the result:

- **Data fidelity:** Every plotted value matches the source within the stated tolerance (for example, zero difference for displayed labels; recomputed axis ranges match data min and max). Regenerate the chart from the source and diff the exported data where possible.
- **Text accuracy:** Every label string compared against the spec, exact match, including units and capitalization.
- **Dimensions and format:** Pixel dimensions, aspect ratio, color mode, and file format match the requirement. Confirm by reading file metadata, not by visual judgment.
- **Contrast and accessibility:** Text-to-background contrast meets the target standard in the project guide (state the standard used; WCAG AA is a common reference, verify current criteria). Color is not the only encoding for categories.
- **Artifact scan:** At full zoom, check for garbled glyphs, duplicated limbs or objects, hallucinated logos, and stray marks.
- **Provenance record:** A sidecar file stating generator and version, date, prompt or spec hash, seed where available, source data file and its hash, edits applied, and the synthetic-content label.

Attach the verification table to the deliverable.

## Failure handling

- **Garbled text persists after two regenerations:** Remove text from the generated image and overlay it as vector text.
- **Chart values disagree with source:** Discard the figure, locate the transform step causing the mismatch, fix the pipeline, and re-render. Do not hand-edit numbers.
- **Output resembles a real person or protected mark:** Stop, discard the output from shared locations, and escalate under Gate C.
- **Tool unavailable or behavior changed:** Report the discrepancy, check current official documentation, and do not substitute undocumented parameters.
- **Repeated quality failure after reasonable iteration (about five substantive attempts):** Stop and report the blocker with evidence rather than continuing to vary prompts.

## Deliverable contract

Return:

1. The final asset(s) in the requested format and location.
2. A source file for each asset (plotting script, diagram source, or editable layer file) sufficient to regenerate it.
3. The provenance sidecar and verification table.
4. A short statement of method, known limitations, and any gate decisions requiring sign-off.

Do not deliver assets with unverified numbers, unlabeled synthetic imagery where labeling is required, or unresolved gate items.