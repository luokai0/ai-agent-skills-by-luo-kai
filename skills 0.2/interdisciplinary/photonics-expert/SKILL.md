---
name: photonics-expert
version: 1.0.0
description: Expert-level photonics covering guided wave optics, laser physics, nonlinear optics, optical communications, integrated photonics, and quantum photonics.
author: luokai25
tags: [photonics, lasers, fiber optics, integrated photonics, nonlinear optics]
---

# Photonics Expert

## Before Starting
1. Free-space or guided wave optics?
2. Communications, sensing, or quantum application?
3. Classical or quantum photonics?

## Core Expertise Areas

### Guided Wave Optics
Total internal reflection: light confined in high-index waveguide core.
Single mode fiber: one transverse mode, no modal dispersion, long-haul communications.
Multimode fiber: multiple modes, modal dispersion limits bandwidth-distance product.
Dispersion: chromatic dispersion broadens pulses, limits data rate.
Fiber attenuation: lowest at 1550nm, about 0.2 dB per km in silica fiber.

### Laser Physics
Population inversion: more atoms in excited than ground state, required for gain.
Gain medium: semiconductor, gas, solid-state crystal, fiber.
Resonator: mirrors form cavity, select longitudinal modes.
Threshold: gain must exceed cavity losses for lasing.
Mode-locking: ultrashort pulses from coherent superposition of longitudinal modes.

### Nonlinear Optics
Second harmonic generation: two photons combine to produce one at double frequency.
Parametric amplification: signal amplified by pump via chi-2 interaction.
Four-wave mixing: three waves interact via chi-3 to generate fourth.
Kerr effect: intensity-dependent refractive index causes self-phase modulation.
Solitons: pulse shape preserved by balance of dispersion and nonlinearity.

### Integrated Photonics
Silicon photonics: CMOS-compatible, low cost, high volume manufacture.
Ring resonators: compact wavelength filters, modulators, sensors.
Mach-Zehnder: interferometric modulator, electro-optic or thermo-optic tuning.
Photonic integrated circuits: waveguides, splitters, modulators, detectors on chip.

## Best Practices
- Characterize laser wavelength and power before optical measurements
- Minimize reflections that can cause feedback and instability
- Use mode matching for efficient coupling between components
- Consider thermal effects in high-power photonic systems

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring fiber polarization | Use polarization-maintaining fiber for sensitive applications |
| Underestimating coupling losses | Measure insertion loss carefully at each interface |
| Nonlinear effects at high power | Calculate nonlinear length and compare to system length |
| Etalon effects from reflections | Use angled facets and index matching fluid |

## Related Skills
- physics/optics-expert
- physics/electromagnetism-expert
- quantum-computing-expert
