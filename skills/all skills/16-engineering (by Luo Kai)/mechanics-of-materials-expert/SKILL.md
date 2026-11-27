---
name: mechanics-of-materials-expert
version: 1.0.0
description: Expert-level mechanics of materials covering stress and strain, axial loading, torsion, bending, shear, deflection, buckling, and failure theories.
author: luo-kai
tags: [mechanics of materials, stress, strain, bending, torsion, deflection, buckling]
---

# Mechanics of Materials Expert

## Before Starting
1. Which loading type? (axial, torsional, bending, combined)
2. Which material behavior? (elastic, plastic, viscoelastic)
3. Static or fatigue loading?

## Core Expertise Areas

### Stress and Strain
Normal stress: sigma = F over A, force per unit area perpendicular to surface.
Shear stress: tau = V times Q over I times t, parallel to surface.
Normal strain: epsilon = delta over L, deformation per unit length.
Hooke law: sigma = E times epsilon for linear elastic material.
Poisson ratio: lateral strain is negative nu times axial strain.

### Axial Loading
Deformation: delta = PL over AE.
Statically indeterminate: compatibility equation provides additional equation.
Thermal stress: sigma = E times alpha times delta T for constrained member.
Stress concentration: geometric discontinuities increase local stress by Kt factor.

### Torsion
Shear stress: tau = T times rho over J, varies linearly with radius.
Angle of twist: phi = TL over JG.
Polar moment of inertia: J = pi r4 over 2 for solid circle.
Thin-walled sections: tau = T over 2 times A_enclosed times t.

### Bending
Flexure formula: sigma = M times y over I, linear stress distribution.
Neutral axis: zero normal stress, centroidal axis for symmetric sections.
Shear formula: tau = VQ over It, parabolic distribution in rectangular section.
Deflection: integrate moment-curvature relation, M = EI times d2y over dx2.

### Failure
Von Mises criterion: equivalent stress for ductile materials under combined loading.
Tresca criterion: maximum shear stress theory, conservative for ductile materials.
Buckling: Euler formula Pcr = pi squared EI over L_effective squared.
Fatigue: S-N curve, endurance limit, stress concentration in fatigue.

## Best Practices
- Always identify cross section properties before stress calculation
- Draw shear and moment diagrams for beam problems
- Apply appropriate failure theory for material ductility
- Include stress concentrations in fatigue analysis

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong sign for bending stress | Define positive M direction and y direction consistently |
| Using gross section in buckling | Use minimum moment of inertia for column buckling |
| Ignoring shear in beam deflection | Include shear deflection for short deep beams |
| Applying Euler buckling to short columns | Check slenderness ratio before applying Euler formula |

## Related Skills
- statics-expert
- dynamics-expert
- cad-design-expert
