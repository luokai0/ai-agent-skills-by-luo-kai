---
name: aircraft-structures-expert
version: 1.0.0
description: Expert-level aircraft structures covering structural design philosophy, wing and fuselage analysis, fatigue and damage tolerance, composite structures, and certification.
author: luokai25
tags: [aircraft structures, fatigue, damage tolerance, composites, wing design, certification]
---

# Aircraft Structures Expert

## Before Starting
1. Which structural component? (wing, fuselage, empennage, landing gear)
2. Metallic or composite structure?
3. Static strength or fatigue and damage tolerance?

## Core Expertise Areas

### Structural Design Philosophy
Safe life: retire structure before fatigue failure with safety factor on life.
Fail safe: multiple load paths, single failure does not cause catastrophic failure.
Damage tolerant: assume crack exists, inspect before crack reaches critical size.
Limit load: maximum load expected in service, no permanent deformation.
Ultimate load: limit load times 1.5 factor of safety, no failure.

### Wing Structural Analysis
Box beam: front and rear spars with upper and lower skins carry bending and torsion.
Bending: spars and skin carry span bending moment as axial loads.
Torsion: closed section resists torque, shear flow q = T over 2A.
Shear: spars carry vertical shear force.
Idealized section: lumped flange areas and shear-only webs for analysis.

### Fatigue and Damage Tolerance
S-N curve: stress amplitude vs cycles to failure, endurance limit for steel.
Stress concentration: Kt amplifies nominal stress at holes and fillets.
Miner rule: cumulative damage, sum of ni over Ni equals 1 at failure.
Crack growth: Paris law da over dN = C times delta K to the m power.
Critical crack size: fracture toughness KIc = sigma sqrt pi a times geometry factor.

### Composite Structures
Laminate theory: stiffness from fiber orientation and stacking sequence.
Failure modes: fiber failure, matrix cracking, delamination, buckling.
First ply failure: weakest ply fails first, progressive damage to final failure.
Impact damage: BVID barely visible impact damage, strength reduction allowed.
Lightning strike: conductive mesh or expanded foil protection required.

## Best Practices
- Design for damage tolerance not just static strength
- Establish inspection intervals before entering service
- Test representative coupons and elements before full scale testing
- Use conservative material allowables from statistically valid data

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring stress concentration at fastener holes | Apply Kt in fatigue analysis at every hole |
| Wrong laminate stacking for fatigue | Avoid grouping same-angle plies, interleave |
| Underestimating composite impact sensitivity | Test impact damage tolerance explicitly |
| Missing combined load interaction | Check all load combinations not just individual peaks |

## Related Skills
- aerodynamics-expert
- mechanics-of-materials-expert
- manufacturing-processes-expert
