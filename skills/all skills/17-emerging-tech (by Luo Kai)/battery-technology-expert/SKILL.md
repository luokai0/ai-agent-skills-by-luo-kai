---
name: battery-technology-expert
version: 1.0.0
description: Expert-level battery technology covering electrochemistry, lithium-ion battery physics, battery management systems, degradation mechanisms, and next-generation battery chemistries.
author: luo-kai
tags: [batteries, lithium-ion, BMS, degradation, energy storage, electrochemistry]
---

# Battery Technology Expert

## Before Starting
1. Which battery chemistry? (Li-ion, LFP, solid-state, flow)
2. Stationary storage or mobile application?
3. Cell, module, or pack level?

## Core Expertise Areas

### Lithium-Ion Electrochemistry
Intercalation: lithium ions insert into and extract from electrode lattice.
Cathode: LCO, NMC, NCA, LFP — determines energy density and safety.
Anode: graphite standard, silicon adds capacity but causes volume expansion.
Electrolyte: lithium salt in organic solvent, ionic conductivity, voltage window.
SEI layer: solid electrolyte interphase on anode, protects but consumes lithium.

### Battery Metrics
Energy density: Wh/kg or Wh/L, determines range and weight in applications.
Power density: W/kg, determines acceleration and fast charging capability.
C-rate: charge or discharge rate relative to capacity, 1C fills in one hour.
Round-trip efficiency: energy out over energy in, typically 92-97% for Li-ion.
Cycle life: number of cycles to 80% capacity retention at given conditions.

### Battery Management System
Cell balancing: passive wastes energy, active transfers energy between cells.
State of charge estimation: coulomb counting, OCV lookup, Kalman filter.
State of health: capacity fade and resistance growth tracking over lifetime.
Thermal management: cooling to keep cells in optimal temperature range.
Protection: overvoltage, undervoltage, overcurrent, overtemperature cutoff.

### Degradation Mechanisms
Capacity fade: lithium loss from SEI growth, active material loss.
Resistance growth: electrolyte decomposition, contact resistance increase.
Lithium plating: fast charging at low temperature, risk of dendrite formation.
Calendar aging: degradation even without cycling, temperature dependent.

### Next-Generation Chemistries
Solid-state: solid electrolyte, higher energy density, safer, manufacturing challenges.
Sodium-ion: earth abundant, lower energy density than Li-ion, grid storage application.
Flow batteries: vanadium redox, decouple power and energy, long duration storage.
Lithium-air: theoretical 10x energy density of Li-ion, cycle life challenge.

## Best Practices
- Always characterize cells at multiple temperatures before deployment
- Design thermal management for worst case not average conditions
- Use physics-based models for state estimation in demanding applications
- Test at end-of-life conditions not just beginning of life

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Fast charging without thermal management | Lithium plating and thermal runaway risk |
| Ignoring calendar aging | Batteries degrade in storage, not just cycling |
| Using Ah capacity without SoC correction | Capacity depends on temperature and rate |
| Underestimating pack-level losses | Cell-to-cell variation reduces usable capacity |

## Related Skills
- energy-storage-expert
- solar-energy-expert
- physics/electromagnetism-expert
