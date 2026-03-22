---
name: composites-expert
version: 1.0.0
description: Expert-level composites engineering covering fiber reinforced polymers, matrix materials, laminate theory, manufacturing processes, failure modes, and composite design.
author: luokai25
tags: [composites, carbon fiber, CFRP, laminate theory, fiber reinforced polymers, manufacturing]
---

# Composites Expert

## Before Starting
1. Which fiber? (carbon, glass, aramid)
2. Which matrix? (epoxy, thermoplastic, ceramic)
3. Structural design or manufacturing focus?

## Core Expertise Areas

### Fiber and Matrix Materials
Carbon fiber: high stiffness and strength, low density, expensive, brittle.
Glass fiber: lower stiffness than carbon, cheaper, good impact resistance.
Aramid fiber: Kevlar, high toughness, good impact, poor compression.
Epoxy matrix: most common thermoset, good adhesion, brittle, limited temperature.
Thermoplastic matrix: PEEK, recyclable, tougher than thermoset, higher cost.

### Micromechanics
Rule of mixtures: E1 = Ef times Vf plus Em times Vm for longitudinal modulus.
Transverse modulus: inverse rule of mixtures, matrix dominated.
Longitudinal strength: fiber dominated, approximately Vf times sigma_f_ult.
Fiber volume fraction: typically 55-65% for aerospace structural laminates.

### Classical Laminate Theory
ABD matrix: A membrane stiffness, B coupling, D bending stiffness.
Ply angles: 0 for axial, 90 for transverse, plus minus 45 for shear.
Symmetric laminate: B = 0, no bending-extension coupling.
Balanced laminate: equal plus and minus angle plies, no shear-extension coupling.
Failure criteria: Tsai-Wu or Tsai-Hill for ply-level failure prediction.

### Manufacturing
Hand layup: manual ply placement, low cost, labor intensive, variable quality.
Autoclave cure: high pressure and temperature, aerospace quality, expensive.
RTM: resin transfer molding, inject resin into dry fiber preform.
Filament winding: continuous fiber wound over mandrel for pressure vessels and pipes.
AFP and ATL: automated fiber placement and tape laying for large structures.

## Best Practices
- Design laminate with at least 10% fibers in each principal direction
- Avoid grouping more than 4 plies of same orientation to reduce matrix cracking
- Account for moisture absorption effect on matrix-dominated properties
- Specify non-destructive inspection method for critical composite structures

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Applying isotropic analysis to anisotropic laminates | Use laminate theory for accurate stiffness prediction |
| Ignoring compression strength reduction | CFRP compression strength much lower than tension |
| Wrong cure cycle causing residual stress | Follow manufacturer cure cycle exactly |
| No impact damage assessment | BVID dramatically reduces compression strength |

## Related Skills
- metals-expert
- ceramics-expert
- aircraft-structures-expert
