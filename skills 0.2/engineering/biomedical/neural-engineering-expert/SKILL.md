---
name: neural-engineering-expert
version: 1.0.0
description: Expert-level neural engineering covering neural interfaces, brain-computer interfaces, neural signal processing, deep brain stimulation, and neuroprosthetics.
author: luokai25
tags: [neural engineering, BCI, neural interfaces, deep brain stimulation, neuroprosthetics]
---

# Neural Engineering Expert

## Before Starting
1. Invasive or non-invasive neural interface?
2. Recording, stimulation, or closed-loop system?
3. Clinical device or research tool?

## Core Expertise Areas

### Neural Interfaces
Utah array: 100 electrode silicon array, acute and chronic recording in cortex.
Michigan probe: silicon shank with multiple recording sites along length.
EEG: scalp electrodes, non-invasive, low spatial resolution, clinical standard.
ECoG: electrocorticography, subdural electrodes, better resolution than EEG.
Flexible electronics: conformal arrays reduce mechanical mismatch with brain tissue.

### Neural Signal Processing
Spike sorting: classify action potentials by waveform shape to identify neurons.
LFP: local field potential, population activity, lower frequency than spikes.
Common average reference: subtract mean across channels to reduce common noise.
Coherence: measure of synchrony between two neural signals in frequency domain.
Decoding: machine learning to predict movement or intent from neural signals.

### Brain-Computer Interfaces
Motor BCI: decode motor cortex signals to control prosthetic or cursor.
P300 speller: EEG-based communication for locked-in patients.
SSVEP: steady-state visual evoked potential, gaze-based BCI.
Closed-loop: detect neural state and deliver feedback or stimulation in real time.
Decoder stability: neural tuning drifts over days, adaptive decoders required.

### Stimulation
DBS: deep brain stimulation for Parkinson, depression, OCD, high frequency pulses.
Charge balance: biphasic pulses prevent electrode and tissue damage.
Charge density limit: below 30 microcoulombs per cm squared to avoid damage.
TMS: transcranial magnetic stimulation, non-invasive cortical stimulation.

## Best Practices
- Characterize electrode impedance before and after implantation
- Use charge-balanced biphasic pulses for all neural stimulation
- Validate decoding accuracy on held-out data from separate sessions
- Follow biocompatibility standards for all implantable materials

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Single session decoder assuming stability | Neural tuning drifts, use adaptive or recalibrate regularly |
| Charge imbalance causing tissue damage | Always use charge-balanced stimulation waveforms |
| Ignoring electrode impedance changes | High impedance indicates poor contact or tissue reaction |
| Overinterpreting EEG spatial resolution | EEG integrates over large cortical areas |

## Related Skills
- neuroscience-expert
- biomedical-imaging-expert
- signal-processing-expert
