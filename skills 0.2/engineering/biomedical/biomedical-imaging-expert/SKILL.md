---
name: biomedical-imaging-expert
version: 1.0.0
description: Expert-level biomedical imaging covering X-ray, CT, MRI, ultrasound, nuclear medicine, optical imaging, and image processing for clinical and research applications.
author: luokai25
tags: [biomedical imaging, MRI, CT, ultrasound, X-ray, PET, image processing]
---

# Biomedical Imaging Expert

## Before Starting
1. Which imaging modality?
2. Clinical diagnosis or research application?
3. Image acquisition or image processing focus?

## Core Expertise Areas

### X-ray and CT
X-ray production: electrons accelerated to anode, bremsstrahlung and characteristic radiation.
Attenuation: Beer-Lambert law, tissue contrast from differential attenuation.
CT reconstruction: filtered backprojection or iterative algorithms from projections.
Hounsfield units: CT number scale, air -1000, water 0, bone +1000.
Dose: effective dose in mSv, CT higher than plain X-ray, ALARA principle.

### MRI
Nuclear magnetic resonance: protons align in B0 field, RF pulse tips magnetization.
T1 relaxation: longitudinal recovery, fat bright on T1.
T2 relaxation: transverse decay, water bright on T2.
K-space: raw MRI data in frequency domain, Fourier transform gives image.
Sequences: spin echo, gradient echo, EPI, each with different contrast and speed.

### Ultrasound
Pulse-echo: transducer transmits pulse, receives echoes from tissue interfaces.
Acoustic impedance: Z = rho times c, mismatch causes reflection.
Frequency trade-off: higher frequency gives better resolution but less penetration.
Doppler: frequency shift from moving blood cells, measures flow velocity.
Modes: A-mode, B-mode, M-mode, Doppler, 3D ultrasound.

### Nuclear Medicine
PET: positron emission tomography, FDG tracer, metabolic imaging.
SPECT: single photon emission CT, lower resolution than PET but cheaper.
Radiotracer: injected, accumulates in target tissue, emits detectable radiation.
PET-CT: combined anatomical and functional imaging, standard in oncology.

## Best Practices
- Match imaging modality to clinical question and patient safety
- Use appropriate acquisition protocols to optimize image quality vs dose
- Validate image processing algorithms on representative clinical datasets
- Consider motion artifacts and plan acquisition to minimize them

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring partial volume effect in CT | Account for voxel size when measuring small structures |
| MRI metal artifacts | Screen patients for implants, use metal artifact reduction sequences |
| Ultrasound shadowing from bone or gas | Interpret artifacts in clinical context |
| Registration errors in multi-modal imaging | Use rigid or deformable registration as appropriate |

## Related Skills
- medical-devices-expert
- signal-processing-expert
- machine-learning-expert
