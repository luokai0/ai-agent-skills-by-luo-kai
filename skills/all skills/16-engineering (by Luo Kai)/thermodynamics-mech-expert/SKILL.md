---
name: thermodynamics-mech-expert
version: 1.0.0
description: Expert-level engineering thermodynamics covering laws of thermodynamics, thermodynamic cycles, steam power plants, refrigeration, gas dynamics, and combustion.
author: luo-kai
tags: [thermodynamics, Rankine cycle, Brayton cycle, refrigeration, combustion, entropy]
---

# Thermodynamics Mechanical Expert

## Before Starting
1. Which system type? (closed, open, steady-flow)
2. Which cycle? (Rankine, Brayton, Otto, Diesel, refrigeration)
3. Ideal or real with irreversibilities?

## Core Expertise Areas

### Laws of Thermodynamics
First law: energy is conserved, delta U = Q minus W for closed system.
Second law: entropy of universe increases for irreversible processes.
Entropy: ds = dQ_rev over T, measure of irreversibility.
Exergy: maximum useful work from system brought to equilibrium with environment.

### Power Cycles
Rankine cycle: steam power plant, boiler, turbine, condenser, pump.
Rankine efficiency: improved by superheat, reheat, and regeneration.
Brayton cycle: gas turbine, compressor, combustor, turbine.
Brayton efficiency: eta = 1 minus 1 over r_p to the power k-1 over k.
Combined cycle: gas turbine exhaust heats steam Rankine, 60% efficiency possible.

### Refrigeration
Vapor compression: compressor, condenser, expansion valve, evaporator.
COP: coefficient of performance, QL over W_net for refrigerator.
Heat pump COP: QH over W_net, always greater than refrigerator COP by one.
Carnot COP: maximum possible COP for given temperature limits.

### Gas Dynamics
Mach number: M = V over speed of sound, speed of sound = sqrt of gamma R T.
Isentropic relations: T2 over T1 = P2 over P1 to the k-1 over k power.
Normal shock: supersonic to subsonic, sudden pressure rise, entropy increase.
Nozzle flow: converging accelerates to M=1 at throat, diverging to supersonic.

## Best Practices
- Sketch system and identify boundary before applying first law
- Distinguish heat and work sign conventions carefully
- Use property tables for accurate steam and refrigerant properties
- Check second law consistency of calculated processes

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Sign convention errors | Define positive Q in and positive W out at start |
| Using ideal gas for steam | Use steam tables for accurate properties |
| Ignoring pump work in Rankine | Include pump work even though small compared to turbine |
| Adiabatic assumption for non-insulated system | Only apply adiabatic if process is fast or well-insulated |

## Related Skills
- heat-transfer-expert
- fluid-mechanics-expert
- physics/thermodynamics-expert
