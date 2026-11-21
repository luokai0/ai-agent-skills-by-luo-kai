---
name: generative-media-production
description: Use when producing images, audio, or video with generative models, especially when pulling checkpoints, LoRAs, voice models, or other weights from external registries and must verify licensing, provenance, and output quality before delivery.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Generative Media Production

## Purpose and boundaries

This skill governs end-to-end production of generated media for client, marketing, editorial, or internal use: brief intake, model selection from external registries, generation runs, quality review, and packaging with provenance records.

In scope: image, illustration, short audio, voiceover, and short video generation; selecting and vetting third-party model weights; prompt and parameter documentation; reproducibility records; export and metadata handling.

Out of scope: training new foundation models, generating likenesses of real people without written consent, political or medical imagery intended to be taken as factual, and any output whose purpose is deception.

## Inputs and assumptions

Before generating, confirm:

- **Brief**: deliverable type, dimensions or duration, format, count, intended channel, and usage term (duration, territory, exclusivity).
- **Rights position**: who owns the brief, reference assets, and any voice or face references. Missing rights information is a blocker, not a detail to fill in.
- **Model source**: registry name, model identifier, exact version or commit, and the license file text. Assume nothing about permissive use from a model's popularity.
- **Compute**: available hardware and time budget. Record it, since it affects reproducibility.

If any input is absent, ask. Do not infer rights or licenses.

## Operating workflow

1. **Scope the brief.** Write a one-paragraph spec with acceptance criteria: subject, style constraints, forbidden content, technical specs (resolution, sample rate, frame rate, duration, loudness target).
2. **Shortlist models.** Select 2–3 candidates from registries. For each, record publisher, version, license name, commercial-use clause, restrictions on outputs, and whether the card discloses training-data provenance. Check for included safety or watermarking components and whether they can be disabled, and do not disable them without approval.
3. **Vet weights.** Verify checksums against the registry's published values where provided. Do not load pickled or executable-format artifacts from untrusted sources; prefer safetensors or equivalent formats, and confirm the format against current loader documentation.
4. **Pilot run.** Generate small batches (4–8 outputs) per candidate using a fixed seed set. Log prompt, negative prompt, seed, sampler, steps, guidance scale, model hash, and software versions.
5. **Select and produce.** Choose the candidate that passes the spec with the clearest license. Generate the final set with the same logged parameters.
6. **Post-process.** Upscale, color-correct, normalize loudness, or trim only with logged tools. Keep the raw output alongside the edited version.
7. **Package.** Export to specified formats and attach a manifest (see Deliverable contract).

## Decision gates

- **Gate A (rights):** Proceed only if the model license explicitly permits the intended commercial use and any output restrictions are satisfied. "Research use only" or unclear wording stops the workflow.
- **Gate B (likeness and voice):** Any recognizable real person, or any cloned voice, requires signed consent from that person. Without it, stop.
- **Gate C (safety filters):** If a generated output triggers a content filter, do not route around it. Log the event and escalate.
- **Gate D (external delivery):** Uploading to a public registry, publishing to a channel, or sending to a client requires explicit approval from the project owner.
- **Gate E (destructive actions):** Deleting raw outputs, overwriting prior versions, or purging cache requires approval. Raw outputs are retained until the client accepts delivery.

## Verification and evidence

Measurable checks before delivery:

- Resolution, duration, sample rate, and frame rate match spec exactly (verify with a media probe tool).
- Image: no unintended text artifacts, hand or limb count correct in human subjects, no visible tiling seams; reviewer marks at least 90% of sampled frames as pass.
- Audio: clipping absent; integrated loudness within ±1 LU of target; no sibilance or phase artifacts on a headphone pass and a speaker pass.
- Video: no flicker between keyframes; temporal consistency checked on frame-by-frame sampling at 10% intervals.
- Provenance: manifest hashes match delivered files.

Where a registry or tool advertises a metadata or content-credential standard, confirm current support against official documentation before claiming it. Do not assert compliance with any regulation or standard as a guarantee.

## Failure handling

- **Quality failure:** Adjust one variable at a time (prompt, then seed, then sampler). Record each change. After three failed rounds on one candidate, switch candidates.
- **License ambiguity:** Stop, quote the clause, and request legal review.
- **Corrupted or mismatched weights:** Discard, re-download from the registry, and recheck hashes. Do not patch files manually.
- **Version drift:** If a library or model revision changes results, pin the prior version and note the discrepancy.

## Deliverable contract

Each delivery contains:

1. Final files plus raw outputs in separate folders.
2. `manifest.json` listing each file, SHA-256 hash, model registry, model identifier and version, license name, parameters, seeds, and reviewer sign-off.
3. A rights memo: source of every model, licensing clause relied on, consent records for any real likeness or voice.
4. A short notes file stating known limitations and any unresolved risks.

Do not deliver files lacking a manifest, and do not state that outputs are free of third-party rights. Mark any software or model version detail not verified against current official documentation as "to verify."