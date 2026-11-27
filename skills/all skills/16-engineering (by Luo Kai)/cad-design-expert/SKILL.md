---
name: cad-design-expert
version: 1.0.0
description: Expert-level CAD design covering parametric modeling, assembly design, drawing creation, FEA simulation, design for manufacturing, and PLM workflows.
author: luo-kai
tags: [CAD, parametric modeling, SolidWorks, FEA, assembly, drawing, PLM]
---

# CAD Design Expert

## Before Starting
1. Which CAD software? (SolidWorks, CATIA, NX, Fusion 360, FreeCAD)
2. Part, assembly, or drawing focus?
3. Mechanical design or generative design?

## Core Expertise Areas

### Parametric Part Modeling
Sketch: 2D profile with dimensions and constraints, fully defined best practice.
Features: extrude, revolve, sweep, loft, fillet, chamfer, shell, pattern.
Feature tree: history of operations, order matters for dependencies.
Design intent: model dimensions to reflect design relationships.
Configuration: multiple variants of part within single file.

### Assembly Design
Mates: define relationships between components, coincident, parallel, concentric.
Bottom-up: design parts first, assemble second.
Top-down: design in context of assembly, driven by layout sketch.
Interference detection: check for part collisions in assembly.
Bill of materials: auto-generated list of all components in assembly.

### Engineering Drawings
Views: front, top, side, section, detail, auxiliary views.
Dimensions: fully dimensioned to manufacturing requirements.
Tolerances: GDandT symbols for form, orientation, position, runout.
Title block: part number, revision, material, scale, approval signatures.

### FEA Integration
Mesh: discretize geometry into elements, finer mesh near stress concentrations.
Boundary conditions: fixtures and loads applied to represent real constraints.
Material properties: elastic modulus, Poisson ratio, yield strength.
Results: stress, strain, displacement, factor of safety visualization.

## Best Practices
- Fully define all sketches before creating features
- Use reference geometry to capture design intent in dimensions
- Name features descriptively for maintainability
- Validate FEA mesh quality before trusting results

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Undefined sketch causing unexpected behavior | Always fully define sketches |
| Feature order problems | Understand parent-child relationships in feature tree |
| Over-constrained assembly mates | Use minimum mates to fully define position |
| FEA singularity at sharp corners | Add fillets or interpret local high stress with caution |

## Related Skills
- statics-expert
- mechanics-of-materials-expert
- manufacturing-processes-expert
