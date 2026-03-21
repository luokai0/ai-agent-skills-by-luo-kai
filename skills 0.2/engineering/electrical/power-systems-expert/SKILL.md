---
name: power-systems-expert
version: 1.0.0
description: Expert-level power systems covering power generation, transmission, distribution, power flow analysis, fault analysis, protection, and power electronics.
author: luokai25
tags: [power systems, power flow, fault analysis, protection, transformers, power electronics]
---

# Power Systems Expert

## Before Starting
1. Generation, transmission, or distribution focus?
2. Steady-state or transient analysis?
3. AC or DC system?

## Core Expertise Areas

### Power Flow Analysis
Bus types: slack bus sets reference, PV buses control voltage, PQ buses are loads.
Newton-Raphson: iterative power flow solution, quadratic convergence.
Gauss-Seidel: simpler but slower convergence than Newton-Raphson.
Y-bus admittance matrix: represents network topology and impedances.
DC approximation: linearized power flow for fast contingency screening.

### Fault Analysis
Symmetrical faults: three-phase fault, most severe, simplest to analyze.
Unsymmetrical faults: single line-to-ground most common, use symmetrical components.
Symmetrical components: positive, negative, zero sequence for unbalanced analysis.
Fault current: limited by source impedance, generators, and transformers.
Short circuit MVA: determines equipment rating requirements.

### Protection Systems
Overcurrent relay: trips when current exceeds threshold, time-overcurrent coordination.
Distance relay: impedance-based, protects transmission lines.
Differential relay: compares currents entering and leaving, protects transformers.
Backup protection: redundant relays ensure fault clearing if primary fails.

### Power Electronics
Rectifiers: AC to DC conversion, diode bridge, thyristor controlled.
Inverters: DC to AC, PWM control, used in drives and renewables.
HVDC: high voltage DC transmission, VSC or LCC technology.
FACTS: flexible AC transmission systems, improve stability and power flow control.

## Best Practices
- Always perform contingency analysis for N-1 security standard
- Coordinate protection relays to minimize outage extent
- Validate power flow results against measured data
- Consider harmonic distortion from power electronics in system studies

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Power flow non-convergence | Check initial voltage profile and reduce load step |
| Missing zero sequence path for ground faults | Verify transformer winding configurations |
| Protection coordination gaps | Plot time-current curves for all devices in series |
| Ignoring reactive power limits | Include generator and capacitor reactive limits |

## Related Skills
- circuit-analysis-expert
- control-systems-expert
- power-grid-expert
