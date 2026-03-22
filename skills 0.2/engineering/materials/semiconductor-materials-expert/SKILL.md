---
name: semiconductor-materials-expert
version: 1.0.0
description: Expert-level semiconductor materials covering band theory, silicon processing, compound semiconductors, wide bandgap materials, and semiconductor device fundamentals.
author: luokai25
tags: [semiconductors, silicon, band theory, compound semiconductors, GaN, SiC, doping]
---

# Semiconductor Materials Expert

## Before Starting
1. Silicon or compound semiconductor?
2. Device physics or processing focus?
3. Electronic or photonic application?

## Core Expertise Areas

### Band Theory
Valence band: filled electron states, top defined by valence band maximum.
Conduction band: empty states electrons occupy when excited.
Bandgap: energy gap between valence and conduction band maxima.
Direct bandgap: GaAs, momentum conserved in optical transitions, good for LEDs.
Indirect bandgap: silicon, phonon required for optical transition, poor emitter.

### Silicon
Crystal growth: Czochralski and float zone for single crystal ingots.
Doping: phosphorus or arsenic for n-type, boron for p-type.
Carrier concentration: n times p = ni squared at equilibrium.
Mobility: electron mobility higher than hole mobility in silicon.
Oxidation: thermal oxide SiO2 forms on silicon surface, excellent gate dielectric.

### Compound Semiconductors
GaAs: high electron mobility, direct bandgap, microwave and photonic devices.
InP: higher electron velocity than GaAs, telecom laser wavelengths.
III-V epitaxy: MBE and MOCVD for heterostructure growth.
Heterostructures: quantum wells from bandgap engineering.

### Wide Bandgap Materials
SiC: 3.26 eV bandgap, high breakdown field, power electronics to 200 C.
GaN: 3.4 eV bandgap, 2DEG at AlGaN/GaN interface, high power and frequency.
Ga2O3: 4.8 eV ultrawide bandgap, high breakdown voltage, emerging power device.
Diamond: 5.5 eV, ultimate power semiconductor material, processing challenges.

## Best Practices
- Control defect density carefully as defects degrade device performance
- Match lattice constant when designing heterostructures to minimize strain
- Consider thermal management for wide bandgap power devices
- Verify dopant activation with Hall measurement not just implant dose

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring surface states in compound semiconductors | Surface passivation critical for device performance |
| Lattice mismatch in heterostructures | Calculate critical thickness before growing strained layer |
| Thermal resistance limiting GaN device | Design thermal management from start |
| Assuming silicon processes transfer to compound semiconductors | Each material has unique process requirements |

## Related Skills
- ceramics-expert
- vlsi-design-expert
- physics/condensed-matter-expert
