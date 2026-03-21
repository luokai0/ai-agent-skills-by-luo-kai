---
name: structural-engineering-expert
version: 1.0.0
description: Expert-level structural engineering covering structural analysis, steel and concrete design, load combinations, deflection, connections, and building codes.
author: luokai25
tags: [structural engineering, steel design, concrete design, loads, connections, codes]
---

# Structural Engineering Expert

## Before Starting
1. Steel, concrete, timber, or composite structure?
2. Building, bridge, or industrial structure?
3. Which design code? (AISC, ACI, Eurocode, AS)

## Core Expertise Areas

### Structural Analysis
Determinate structures: reactions from equilibrium alone, beams, trusses.
Indeterminate structures: additional compatibility equations required.
Stiffness method: global stiffness matrix, solve for nodal displacements.
Influence lines: show effect of moving load at different positions on member force.
Second-order effects: P-delta amplification of moments due to axial loads.

### Steel Design
LRFD: load and resistance factor design, phi times Rn greater than or equal to sum gamma_i Q_i.
Tension members: yielding of gross section and rupture of net section.
Compression: column buckling, effective length factor K.
Beams: flexure, shear, lateral torsional buckling.
Connections: bolted and welded, bearing and slip-critical bolts.

### Concrete Design
Reinforced concrete: steel rebars carry tension, concrete carries compression.
Flexural design: Whitney stress block, tension-controlled failure preferred.
Shear design: stirrups provide shear reinforcement beyond concrete capacity.
Serviceability: crack width and deflection limits under service loads.
Prestressed concrete: precompression offsets tensile stresses from loading.

### Load Combinations
Dead load: permanent weight of structure and non-structural components.
Live load: occupancy loads, reducible for large tributary areas.
Wind load: velocity pressure times exposure and shape factors.
Seismic load: equivalent lateral force or response spectrum analysis.
ASCE 7 combinations: 1.2D + 1.6L dominant combination for gravity design.

## Best Practices
- Always check both strength and serviceability limit states
- Include second-order effects for slender or heavily loaded structures
- Verify load path continuity from point of application to foundation
- Coordinate structural drawings with architectural and MEP drawings

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring lateral torsional buckling in beams | Check unbraced length against limits |
| Wrong effective length for columns | Identify boundary conditions carefully |
| Insufficient concrete cover | Meet code minimums for durability and fire rating |
| Missing load path for lateral loads | Trace lateral loads from roof to foundation |

## Related Skills
- geotechnical-engineering-expert
- hydraulics-expert
- statics-expert
