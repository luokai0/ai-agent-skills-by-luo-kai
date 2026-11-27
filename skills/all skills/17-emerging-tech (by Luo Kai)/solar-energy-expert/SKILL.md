---
name: solar-energy-expert
version: 1.0.0
description: Expert-level solar energy covering photovoltaic physics, solar cell technologies, system design, grid integration, solar thermal, and the economics of solar deployment.
author: luo-kai
tags: [solar energy, photovoltaics, solar cells, PV systems, grid integration]
---

# Solar Energy Expert

## Before Starting
1. PV or solar thermal?
2. Residential, commercial, or utility scale?
3. Grid-tied or off-grid?

## Core Expertise Areas

### Photovoltaic Physics
p-n junction: built-in electric field separates photogenerated carriers.
Bandgap: photons with energy above bandgap generate electron-hole pairs.
Silicon bandgap: 1.12 eV, ideal for single-junction solar cells.
Shockley-Queisser limit: theoretical max efficiency 33.7% for single junction.
Fill factor: ratio of max power to Voc times Isc, measures cell quality.

### Solar Cell Technologies
Monocrystalline silicon: 20-23% efficiency, highest performance, most expensive.
Polycrystalline silicon: 15-18% efficiency, lower cost, grain boundaries reduce efficiency.
Thin film: CdTe and CIGS, lower efficiency, lower cost, flexible substrates possible.
Perovskite: rapidly improving, over 25% efficiency in lab, stability challenges.
Multi-junction: tandem cells exceed Shockley-Queisser, used in concentrators and space.

### PV System Design
Irradiance: peak sun hours per day for location and tilt angle.
System sizing: load analysis, battery sizing, array sizing, inverter selection.
MPPT: maximum power point tracking, optimizes array operating point.
Inverters: string, micro, central, power optimizers, efficiency curves.
Temperature coefficient: efficiency decreases with temperature, typically -0.3 to -0.5% per C.

### Grid Integration
Net metering: export excess to grid, credit on electricity bill.
Duck curve: midday solar surplus then steep evening ramp, grid management challenge.
Curtailment: solar generation reduced when grid cannot absorb output.
Storage: batteries shift solar generation to evening demand, smooths duck curve.

## Best Practices
- Always use site-specific irradiance data not generic averages
- Account for soiling, shading, and degradation in yield estimates
- Design for worst-case temperature and irradiance conditions
- Size battery storage for target autonomy not just overnight load

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Using STC efficiency for real-world estimates | Use PVGIS or PVWatts with location data |
| Ignoring shading impact | Even partial shading causes disproportionate losses |
| Wrong inverter sizing | Size inverter to expected AC output not DC array peak |
| Forgetting degradation over lifetime | Assume 0.5% per year efficiency loss in projections |

## Related Skills
- energy-storage-expert
- power-grid-expert
- wind-energy-expert
