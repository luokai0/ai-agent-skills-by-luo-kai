---
name: concrete-design-expert
version: 1.0.0
description: Expert-level concrete design covering reinforced concrete beams, columns, slabs, footings, retaining walls, ACI 318 code provisions, and durability.
author: luokai25
tags: [concrete design, reinforced concrete, ACI 318, beams, columns, slabs, footings]
---

# Concrete Design Expert

## Before Starting
1. Which element? (beam, column, slab, footing, wall)
2. Which loading? (gravity, lateral, combined)
3. Ordinary or seismic design category?

## Core Expertise Areas

### Flexural Design
Equivalent stress block: Whitney block depth a = 0.85 fc times beta1 times c.
Tension-controlled: ensure ductile failure, phi = 0.90 when epsilon_t greater than 0.005.
Minimum reinforcement: rho_min = max of 3 sqrt fc over fy and 200 over fy.
T-beam behavior: flange engages in positive moment regions of floor beams.
Doubly reinforced: compression steel when singly reinforced is insufficient.

### Shear Design
Concrete contribution Vc: 2 sqrt fc times bw times d approximately.
Stirrups: vertical or inclined reinforcement, Vs = Av fy d over s.
Maximum spacing: d over 2 or 24 inches for minimum shear reinforcement.
Deep beams: strut-and-tie model required for a over d less than 2.

### Column Design
Interaction diagram: combined axial and moment capacity envelope.
Slenderness effects: magnify moments for slender columns.
Tied vs spiral: spiral provides better confinement and ductility.
Minimum eccentricity: design for minimum moment even under pure axial load.

### Serviceability
Deflection: immediate plus long-term creep and shrinkage deflection.
Crack control: maximum bar spacing to limit crack width.
Durability: water-cement ratio, cover, and concrete strength for exposure class.
Shrinkage and temperature: minimum reinforcement in slabs for crack control.

## Best Practices
- Check both strength and serviceability for all concrete members
- Ensure proper concrete cover for durability and fire resistance
- Use interaction diagrams for column design under combined loading
- Coordinate rebar placement with formwork and construction sequence

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Compression-controlled failure without ductility check | Ensure tension-controlled or apply reduced phi |
| Ignoring long-term deflection | Multiply immediate deflection by creep factor |
| Insufficient development length | Check all bar terminations for proper development |
| Wrong phi factor for element type | Phi depends on failure mode, not just element type |

## Related Skills
- structural-engineering-expert
- statics-expert
- mechanics-of-materials-expert
