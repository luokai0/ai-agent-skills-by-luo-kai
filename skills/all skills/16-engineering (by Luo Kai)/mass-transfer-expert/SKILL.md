---
name: mass-transfer-expert
version: 1.0.0
description: Expert-level mass transfer covering molecular diffusion, convective mass transfer, interphase transfer, mass transfer coefficients, and design of mass transfer equipment.
author: luo-kai
tags: [mass transfer, diffusion, convective mass transfer, interphase, absorption, distillation]
---

# Mass Transfer Expert

## Before Starting
1. Single phase or interphase mass transfer?
2. Gas-liquid, liquid-liquid, or gas-solid system?
3. Equipment design or mass transfer analysis?

## Core Expertise Areas

### Molecular Diffusion
Ficks first law: J = negative D times dC over dz, flux proportional to gradient.
Ficks second law: dC over dt = D times d2C over dz2, transient diffusion.
Binary diffusivity: Chapman-Enskog for gases, Wilke-Chang for liquids.
Diffusion in solids: Fickian diffusion, concentration dependent D common.

### Convective Mass Transfer
Mass transfer coefficient: NA = kc times CA_bulk minus CA_surface.
Analogy to heat transfer: Sherwood number analogous to Nusselt number.
Sh = f of Re and Sc, Schmidt number replaces Prandtl number.
Film theory: resistance in thin film near interface.
Penetration theory: surface renewal model, short contact times.

### Interphase Mass Transfer
Two-film theory: resistance in both gas and liquid films at interface.
Overall coefficient: 1 over KG = 1 over kG + H over kL, Henry constant H.
Gas film control: when H is large, liquid phase resistance negligible.
Liquid film control: when H is small, gas phase resistance negligible.

### Column Design
Tray columns: stage efficiency, downcomer sizing, flooding limits.
Packed columns: random or structured packing, HETP, pressure drop.
Flooding: maximum vapor and liquid rates before performance degrades.
Wetting rate: minimum liquid rate to ensure packing surface is wetted.

## Best Practices
- Identify rate-limiting resistance before designing mass transfer equipment
- Verify packing selection against actual system physical properties
- Design for 70-80% of flooding for normal operation with turndown margin
- Account for system foaming tendency in column sizing

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong film resistance assumption | Calculate both resistances and compare |
| Operating too close to flooding | Design for maximum 80% of flood velocity |
| Ignoring liquid maldistribution | Use quality distributor and redistribution every 6m of packing |
| Wrong HETP for conditions | Validate HETP with pilot column data for actual system |

## Related Skills
- separation-processes-expert
- heat-transfer-expert
- reaction-engineering-expert
