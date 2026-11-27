---
name: power-grid-expert
version: 1.0.0
description: Expert-level power grid covering AC power systems, transmission and distribution, grid stability, protection systems, renewable integration, and smart grid technologies.
author: luo-kai
tags: [power grid, AC systems, transmission, grid stability, smart grid, renewables]
---

# Power Grid Expert

## Before Starting
1. Generation, transmission, or distribution focus?
2. AC or DC systems?
3. Grid stability or renewable integration challenge?

## Core Expertise Areas

### AC Power Systems
Three-phase power: balanced loads, 120 degree phase separation, P = sqrt3 times VL times IL times pf.
Real vs reactive power: P active power does work, Q reactive power circulates.
Power factor: ratio of real to apparent power, unity is ideal, low causes losses.
Per-unit system: normalizes values to base quantities, simplifies analysis.
Phasors: complex representation of sinusoidal quantities for circuit analysis.

### Transmission System
HVAC: high voltage AC transmission, 110-765 kV, minimizes I squared R losses.
HVDC: high voltage DC, long distance and submarine cables, asynchronous grid connection.
Transformers: step up voltage for transmission, step down for distribution and use.
Line impedance: resistance causes losses, reactance affects stability.
Stability limits: thermal, voltage, and transient stability constrain power flow.

### Grid Stability
Frequency regulation: generation must match load, frequency deviates if unbalanced.
Inertia: rotating generators resist frequency changes, reduces with more inverter-based generation.
Voltage stability: reactive power balance determines voltage profile.
Transient stability: generators must stay synchronized after faults.
Unit commitment and dispatch: scheduling generators to meet forecast demand at minimum cost.

### Renewable Integration
Variability: wind and solar output changes with weather, grid must balance.
Curtailment: renewable generation reduced when demand or transmission limits reached.
Storage: batteries and pumped hydro shift generation in time, provide flexibility.
Grid-forming inverters: synthetic inertia and voltage support from inverter-based resources.

## Best Practices
- Always model worst case contingencies for stability assessment
- Maintain adequate spinning reserve for frequency regulation
- Coordinate protection systems to minimize fault clearing time
- Plan for high renewable penetration in new grid investments

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring reactive power in planning | Voltage stability requires reactive power management |
| Underestimating renewable variability | Use probabilistic methods for grid planning |
| Inadequate protection coordination | Miscoordination causes cascading outages |
| Assuming infinite grid strength | Weak grid impacts inverter control stability |

## Related Skills
- solar-energy-expert
- wind-energy-expert
- energy-storage-expert
