---
name: reaction-engineering-expert
version: 1.0.0
description: Expert-level reaction engineering covering reaction kinetics, reactor design, ideal and non-ideal reactors, catalysis, and reactor scale-up.
author: luo-kai
tags: [reaction engineering, kinetics, CSTR, PFR, catalysis, reactor design]
---

# Reaction Engineering Expert

## Before Starting
1. Homogeneous or heterogeneous reaction?
2. Which reactor type? (batch, CSTR, PFR, packed bed)
3. Isothermal or non-isothermal operation?

## Core Expertise Areas

### Reaction Kinetics
Rate law: r = k times CA to power alpha times CB to power beta.
Arrhenius equation: k = A times exp of negative Ea over RT.
Elementary vs non-elementary: rate law derived from mechanism not stoichiometry.
Conversion: X = moles reacted over moles fed.
Selectivity: desired product formed over total product formed.

### Ideal Reactor Design
Batch: dX over dt = negative rA over CA0, closed system, time-dependent.
CSTR: V = FA0 times X over negative rA at exit, well-mixed, steady state.
PFR: dFA over dV = rA, plug flow, axial concentration gradient.
Levenspiel plot: 1 over negative rA vs X, area gives reactor volume.
CSTR in series: approaches PFR performance as number of CSTRs increases.

### Non-Isothermal Reactors
Energy balance: heat generated equals heat removed at steady state.
Adiabatic temperature rise: delta T = negative delta H times CA0 times X over rho Cp.
Multiple steady states: CSTR energy and mole balance can intersect multiple times.
Runaway: temperature sensitivity, Damkohler number determines stability.

### Heterogeneous Catalysis
Langmuir-Hinshelwood: adsorption, surface reaction, desorption steps.
Effectiveness factor: ratio of actual rate to rate without diffusion limitation.
Thiele modulus: phi = L times sqrt k over De, large means diffusion limited.
Packed bed reactor: pressure drop from Ergun equation, catalyst deactivation.

## Best Practices
- Collect kinetic data at multiple temperatures to determine Ea
- Check for mass and heat transfer limitations before fitting intrinsic kinetics
- Design for worst case temperature for safety analysis
- Validate lab kinetics at pilot scale before full scale design

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring heat effects for exothermic reactions | Always include energy balance for non-isothermal design |
| External diffusion limitation in kinetic studies | Use differential reactor or high flow rate |
| Wrong residence time distribution | Characterize RTD with tracer experiment before design |
| Catalyst deactivation not accounted for | Include deactivation kinetics in design equations |

## Related Skills
- process-design-expert
- separation-processes-expert
- safety-engineering-expert
