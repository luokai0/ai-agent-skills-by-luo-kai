---
name: statics-expert
version: 1.0.0
description: Expert-level statics covering equilibrium of rigid bodies, free body diagrams, trusses, frames, friction, centroids, and moments of inertia.
author: luo-kai
tags: [statics, equilibrium, free body diagram, trusses, friction, moments of inertia]
---

# Statics Expert

## Before Starting
1. 2D or 3D problem?
2. Rigid body or deformable body?
3. Truss, frame, or machine?

## Core Expertise Areas

### Equilibrium
Conditions: sum of forces equals zero, sum of moments equals zero.
2D equilibrium: three equations, Fx = 0, Fy = 0, moment about any point = 0.
3D equilibrium: six equations, three force and three moment equations.
Free body diagram: isolate body, show all external forces and moments.
Support reactions: pin provides two force reactions, roller one, fixed provides all.

### Trusses
Truss: two-force members connected at joints, loads only at joints.
Method of joints: sum forces at each joint, two equations per joint.
Method of sections: cut through up to three members, sum forces and moments.
Zero force members: can be identified by inspection, simplify analysis.
Determinacy: m + r = 2j for statically determinate truss.

### Friction
Coulomb friction: F = mu times N, friction force proportional to normal force.
Static vs kinetic: static coefficient larger than kinetic.
Impending motion: maximum static friction just before sliding begins.
Wedge friction: self-locking condition when friction angle exceeds wedge angle.

### Centroids and Moments of Inertia
Centroid: geometric center, weighted average position of area or volume.
Composite bodies: sum of component centroids weighted by area or volume.
Second moment of area: I = integral of y squared dA, resists bending.
Parallel axis theorem: I = Icm + A times d squared.

## Best Practices
- Always draw a complete free body diagram before writing equations
- Choose moment point to eliminate unknown forces and simplify solution
- Check solution by summing forces in direction not yet used
- Verify truss determinacy before attempting analysis

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Incomplete free body diagram | Identify and include all contact forces and applied loads |
| Wrong sign convention | Define positive directions clearly at start |
| Ignoring weight of members | Include member weight unless stated massless |
| Moment sign error | Use right-hand rule consistently for 3D problems |

## Related Skills
- dynamics-expert
- mechanics-of-materials-expert
- cad-design-expert
