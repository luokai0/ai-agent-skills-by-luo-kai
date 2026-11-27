---
name: manufacturing-processes-expert
version: 1.0.0
description: Expert-level manufacturing processes covering machining, casting, forming, welding, additive manufacturing, tolerances, and process selection.
author: luo-kai
tags: [manufacturing, machining, casting, forming, welding, additive manufacturing, tolerances]
---

# Manufacturing Processes Expert

## Before Starting
1. Which material? (metal, polymer, ceramic, composite)
2. Production volume? (prototype, low, medium, high)
3. Required tolerances and surface finish?

## Core Expertise Areas

### Machining
Turning: remove material from rotating workpiece with single point tool.
Milling: rotating multi-tooth cutter removes material from fixed workpiece.
Drilling: rotating tool creates cylindrical hole.
Cutting speed, feed, depth: three parameters controlling metal removal rate and quality.
Tool materials: HSS, carbide, ceramic, CBN for increasing hardness and temperature.

### Casting
Sand casting: low cost, complex shapes, rough surface finish, high volume.
Die casting: high pressure, good surface finish, close tolerances, metals only.
Investment casting: excellent detail and finish, complex shapes, high cost.
Shrinkage: metals contract on solidification, design patterns with allowance.

### Forming
Forging: compressive force shapes hot or cold metal, improves grain structure.
Rolling: reduce thickness of metal sheet or bar between rolls.
Extrusion: force material through die to create constant cross section.
Sheet metal: bending, deep drawing, stamping for flat stock.

### Additive Manufacturing
FDM: fused deposition modeling, thermoplastic filament, most common desktop printer.
SLA: stereolithography, UV-cured resin, high detail, smooth surface.
SLS: selective laser sintering, powder bed fusion, functional parts, no support needed.
DMLS: direct metal laser sintering, metal powder, aerospace and medical applications.

### Tolerances and Fits
Tolerance: acceptable range of dimension variation.
Clearance fit: shaft always smaller than hole, used for rotation and sliding.
Interference fit: shaft larger than hole, press fit for permanent assembly.
GDandT: geometric dimensioning and tolerancing, controls form, orientation, location.

## Best Practices
- Design for manufacturability from the start
- Choose process based on material, volume, and required tolerances
- Specify tolerances only as tight as functionally necessary
- Consider secondary operations like heat treatment and surface finishing

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Impossible tolerances on castings | Casting tolerances are much looser than machined parts |
| Underestimating additive manufacturing anisotropy | Parts are weaker in build direction |
| Wrong fit specification | Verify clearance or interference fit intention |
| Ignoring tool access in machining | Design features accessible to cutting tool |

## Related Skills
- cad-design-expert
- mechanics-of-materials-expert
- statics-expert
