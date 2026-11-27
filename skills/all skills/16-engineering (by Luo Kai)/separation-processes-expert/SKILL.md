---
name: separation-processes-expert
version: 1.0.0
description: Expert-level separation processes covering distillation, absorption, extraction, crystallization, membrane separations, and adsorption for chemical engineering applications.
author: luo-kai
tags: [separation, distillation, absorption, extraction, membranes, crystallization]
---

# Separation Processes Expert

## Before Starting
1. Which separation? (distillation, extraction, membrane, crystallization)
2. Binary or multicomponent system?
3. Design or troubleshooting mode?

## Core Expertise Areas

### Distillation
VLE: vapor-liquid equilibrium, Raoults law for ideal systems.
Relative volatility: alpha = y1 over x1 divided by y2 over x2.
McCabe-Thiele: graphical method for binary distillation design.
Operating lines: rectifying and stripping sections defined by material balance.
Minimum reflux: infinite stages required, Underwood equation for multicomponent.
Efficiency: Murphree tray efficiency accounts for non-ideal stage.

### Absorption and Stripping
Absorption: gas component transferred to liquid solvent.
Operating line: L over G ratio determines separation.
Minimum solvent rate: pinch point at equilibrium line crossing.
NTU and HTU: number and height of transfer units for packed column design.

### Liquid-Liquid Extraction
Distribution coefficient: ratio of solute concentration in extract to raffinate phase.
Selectivity: ratio of distribution coefficients for desired vs undesired solute.
Mixer-settler: contacting stage with phase separation.
Kremser equation: number of theoretical stages for given separation.

### Membrane Separations
Reverse osmosis: pressure drives water through semipermeable membrane.
Ultrafiltration: size exclusion of macromolecules, proteins, colloids.
Gas permeation: solution-diffusion mechanism, selectivity from permeability ratio.
Concentration polarization: solute buildup at membrane reduces flux.

## Best Practices
- Obtain accurate VLE data before distillation column design
- Account for non-ideal thermodynamics using activity coefficient models
- Design for flexible operation across expected feed composition range
- Consider energy integration opportunities between separation units

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Assuming ideal VLE | Use NRTL or UNIQUAC for non-ideal liquid mixtures |
| Ignoring azeotropes | Check for azeotropes before designing distillation sequence |
| Membrane fouling not addressed | Include cleaning protocol and replacement in design |
| Wrong solvent selection for extraction | Screen solvents by selectivity and distribution coefficient |

## Related Skills
- reaction-engineering-expert
- process-design-expert
- process-control-expert
