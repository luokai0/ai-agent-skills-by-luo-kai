---
name: hydraulics-expert
version: 1.0.0
description: Expert-level hydraulics covering open channel flow, pipe systems, hydraulic structures, pumps and turbines, flood routing, and stormwater management.
author: luokai25
tags: [hydraulics, open channel, pipe flow, pumps, flood routing, stormwater]
---

# Hydraulics Expert

## Before Starting
1. Open channel or closed conduit?
2. Steady or unsteady flow?
3. Design or analysis mode?

## Core Expertise Areas

### Open Channel Flow
Manning equation: V = 1 over n times R2/3 times S1/2, for uniform flow.
Froude number: Fr = V over sqrt of g times y, subcritical Fr less than 1.
Critical depth: minimum specific energy at given discharge.
Hydraulic jump: rapid transition from supercritical to subcritical, energy loss.
GVF: gradually varied flow profiles, twelve standard types.

### Pipe Systems
Darcy-Weisbach: hf = f times L over D times V squared over 2g.
Moody chart: friction factor from Reynolds number and relative roughness.
Hardy Cross: iterative method for pipe network flow distribution.
Water hammer: pressure surge from rapid valve closure, wave speed analysis.
EPANET: software for water distribution system modeling.

### Hydraulic Structures
Weirs: sharp-crested and broad-crested, discharge measurement and control.
Gates: sluice, tainter, flap gates for flow regulation.
Spillways: ogee, chute, side channel, morning glory types.
Culverts: inlet and outlet control, nomograph design method.

### Pumps and Turbines
Pump curve: head vs discharge relationship for centrifugal pump.
System curve: friction losses plus static head vs discharge.
Operating point: intersection of pump and system curves.
Specific speed: dimensionless parameter characterizing pump type.
Cavitation: occurs when local pressure drops below vapor pressure.

## Best Practices
- Check flow regime before applying appropriate flow equations
- Account for minor losses in pipe system design
- Design for design storm return period appropriate to structure importance
- Verify pump selection against actual system curve not just catalog data

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong Manning n value | Use appropriate value for channel material and condition |
| Ignoring velocity head | Include velocity head in energy calculations |
| Pump operating far from best efficiency | Select pump with BEP near design point |
| Culvert inlet vs outlet control | Check both and use more restrictive condition |

## Related Skills
- structural-engineering-expert
- hydrology-expert
- fluid-mechanics-expert
