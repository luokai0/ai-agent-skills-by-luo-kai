---
name: process-simulation-expert
version: 1.0.0
description: Expert-level process simulation covering Aspen Plus, HYSYS, steady state and dynamic simulation, thermodynamic model selection, and simulation troubleshooting.
author: luo-kai
tags: [process simulation, Aspen Plus, HYSYS, thermodynamics, steady state, dynamic simulation]
---

# Process Simulation Expert

## Before Starting
1. Which simulator? (Aspen Plus, HYSYS, ProII, ChemCAD)
2. Steady state or dynamic simulation?
3. New model build or troubleshooting existing?

## Core Expertise Areas

### Thermodynamic Model Selection
Equation of state: Peng-Robinson for hydrocarbons, SRK for gas systems.
Activity coefficient: NRTL or UNIQUAC for polar liquid mixtures, alcohols.
Electrolyte: ELECNRTL for aqueous ionic systems, sour water.
Steam tables: IAPWS-IF97 for steam and water systems.
VLE validation: compare model predictions against experimental data before use.

### Steady State Simulation
Sequential modular: solve each unit operation in sequence, recycle by iteration.
Equation oriented: all equations solved simultaneously, faster convergence.
Convergence: design specs and recycle convergence, sensitivity to tear stream initial values.
Sensitivity analysis: vary one parameter, observe effect on outputs.

### Column Simulation
RadFrac: rigorous distillation, specify stages, reflux ratio, bottoms rate.
Convergence algorithms: Sum-Rates, Newton, strongly non-ideal systems need special handling.
Column internals: specify tray type or packing, sizing and rating modes.
Hydraulics: check flooding, weeping, downcomer backup for tray columns.

### Dynamic Simulation
Pressure-flow model: includes dynamics of pressure and flow changes.
Holdup: vessel and column tray liquid holdup determines dynamic response.
Control loop tuning: test controllers dynamically, tune in simulation before field.
Safety studies: depressurization, relief valve sizing, startup and shutdown.

## Best Practices
- Validate thermodynamic model against experimental data before building full simulation
- Start with simple model and add complexity progressively
- Document all simulation assumptions and basis clearly
- Cross-check simulation results against hand calculations for key streams

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong thermodynamic model | Match model to system chemistry, validate against data |
| Column convergence failure | Provide good initial estimates, try different algorithms |
| Ignoring free water in hydrocarbon simulation | Include three-phase VLE if water present |
| Dynamic model too detailed | Start simple for control studies, add detail only if needed |

## Related Skills
- process-design-expert
- separation-processes-expert
- reaction-engineering-expert
