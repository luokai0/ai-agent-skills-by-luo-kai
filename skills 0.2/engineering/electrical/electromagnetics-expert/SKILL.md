---
name: electromagnetics-expert
version: 1.0.0
description: Expert-level applied electromagnetics covering transmission lines, waveguides, antennas, microwave circuits, EMC, and computational EM methods.
author: luokai25
tags: [electromagnetics, transmission lines, antennas, microwave, waveguides, EMC]
---

# Electromagnetics Expert

## Before Starting
1. Guided wave or antenna application?
2. Which frequency range? RF, microwave, or mm-wave?
3. Analysis or design focus?

## Core Expertise Areas

### Transmission Lines
Characteristic impedance: Z0 = sqrt of L over C per unit length.
Reflection coefficient: Gamma = ZL minus Z0 over ZL plus Z0.
Standing wave ratio: SWR = 1 plus magnitude of Gamma over 1 minus magnitude of Gamma.
Input impedance: varies with line length and load impedance.
Quarter wave transformer: matches impedance by choosing Z1 = sqrt of ZS times ZL.

### Waveguides
TE modes: transverse electric, no E field in propagation direction.
TM modes: transverse magnetic, no H field in propagation direction.
Cutoff frequency: below cutoff, mode is evanescent not propagating.
Rectangular waveguide: dominant TE10 mode, used at microwave frequencies.
Coaxial line: TEM mode, no cutoff, used from DC to microwave.

### Antennas
Radiation resistance: equivalent resistance that dissipates radiated power.
Gain: directional amplification of radiated power versus isotropic.
Half-wave dipole: 2.15 dBi gain, 73 ohm input impedance.
Patch antenna: low profile, used in mobile devices, PCB-integrated.
Phased array: electronically steerable beam, phase shift per element.

### EMC
Emissions: conducted and radiated, limits set by FCC and CE standards.
Immunity: susceptibility to external interference, ESD, EFT, surge.
Shielding: conductive enclosure reduces radiated emissions and susceptibility.
Filtering: ferrite beads and bypass capacitors reduce conducted emissions.

## Best Practices
- Use Smith chart for transmission line and matching network design
- Verify antenna performance with measurement not just simulation
- Design for EMC compliance early not as afterthought
- Use proper grounding and shielding from initial PCB layout

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Impedance mismatch causing reflections | Match impedances at all interfaces |
| Ground plane discontinuities | Route return currents directly under signal traces |
| Antenna detuning near ground plane | Simulate with actual PCB environment |
| Ignoring skin effect at high frequency | Use correct AC resistance in analysis |

## Related Skills
- circuit-analysis-expert
- communications-expert
- physics/electromagnetism-expert
