---
name: soft-robotics-expert
version: 1.0.0
description: Expert-level soft robotics covering soft actuators, compliant mechanisms, continuum robots, soft sensors, fabrication methods, and bio-inspired design.
author: luo-kai
tags: [soft robotics, soft actuators, continuum robots, compliant mechanisms, bio-inspired]
---

# Soft Robotics Expert

## Before Starting
1. Actuator, sensor, or full system focus?
2. Medical, manufacturing, or research application?
3. Pneumatic, hydraulic, or material-based actuation?

## Core Expertise Areas

### Soft Actuators
PneuNets: pneumatic networks of chambers, bending motion from inflation.
McKibben muscles: braided pneumatic actuator, contracts under pressure.
DEA: dielectric elastomer actuator, voltage-driven area expansion.
SMA: shape memory alloy, thermally activated contraction and bending.
Hydraulically amplified: HASEL actuators, electrically driven hydraulic pumping.

### Continuum Robots
No rigid links: continuous flexible backbone, bends throughout length.
Tendon-driven: cables routed through structure, tension creates bending.
Concentric tube: nested pre-curved tubes, rotation controls shape.
Applications: endoscopic surgery, inspection in confined spaces.
Modeling: Cosserat rod theory, constant curvature assumption for simplicity.

### Compliant Mechanisms
Distributed compliance: flexibility spread throughout structure.
PRBM: pseudo-rigid body model approximates flexible beam as rigid links with joints.
Topology optimization: design structure to achieve desired compliance distribution.
Living hinges: thin flexible sections allowing rotation in injection molded parts.

### Fabrication
Silicone casting: most common for pneumatic soft robots, multi-part molds.
3D printing: FDM with flexible filaments, PolyJet for multi-material.
4D printing: printed structures change shape when triggered by heat or moisture.
Origami and kirigami: paper-folding inspired structures for deployable designs.

## Best Practices
- Characterize material properties before designing actuators
- Prototype rapidly with 3D printed molds for silicone casting
- Test at full range of motion and pressure before integration
- Consider fatigue life of soft materials under repeated cycling

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Underestimating material nonlinearity | Use hyperelastic models not linear elasticity |
| Air leaks in pneumatic systems | Test each channel before assembly |
| Ignoring gravity effects | Soft robots deform significantly under own weight |
| Poor mold design causing demolding failures | Add draft angles and parting line carefully |

## Related Skills
- robot-kinematics-expert
- control-theory-expert
- biomedical/biomechanics-expert
