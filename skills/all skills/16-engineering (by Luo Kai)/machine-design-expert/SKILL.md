---
name: machine-design-expert
version: 1.0.0
description: Expert-level machine design covering shafts, bearings, gears, fasteners, springs, clutches, brakes, and mechanical power transmission systems.
author: luo-kai
tags: [machine design, shafts, bearings, gears, fasteners, springs, power transmission]
---

# Machine Design Expert

## Before Starting
1. Which machine element? (shaft, bearing, gear, fastener, spring)
2. Static or fatigue loading?
3. Design or analysis mode?

## Core Expertise Areas

### Shaft Design
Stress analysis: combined bending, torsion, axial loading.
ASME shaft equation: includes stress concentration, fatigue, and combined loading.
Deflection: check shaft deflection limits for gear and bearing alignment.
Critical speed: rotor dynamics, avoid operating near resonance.
Keys and keyways: transmit torque, stress concentration factor required.

### Bearings
Rolling element: ball, roller, tapered roller, needle, angular contact.
Life rating: L10 life, 90% of bearings survive to rated life.
Dynamic load rating: C value from catalog, P is equivalent dynamic load.
Lubrication: grease for sealed bearings, oil for high speed or high temperature.
Hydrodynamic journal bearings: oil film supports shaft, no contact at operating speed.

### Gears
Spur gears: parallel axes, simple manufacture, noisy at high speed.
Helical gears: angled teeth, smoother and quieter, thrust force generated.
Gear tooth strength: Lewis equation for bending stress at tooth root.
Contact stress: Hertz contact, pitting failure mode.
Gear ratio: input to output speed ratio, inversely proportional to tooth count.

### Fasteners
Bolt preload: clamping force created by tightening, prevents joint separation.
Joint diagram: shows bolt and member stiffness, determines load sharing.
Fatigue of bolts: preload reduces fatigue load range seen by bolt.
Torque-tension relationship: T = K times F times d, K is nut factor.

## Best Practices
- Design for fatigue when cyclic loading is present
- Include stress concentration factors at all geometric discontinuities
- Specify lubrication requirements for all bearings
- Use appropriate safety factor based on load uncertainty and failure consequence

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring fatigue for cyclic loads | Static analysis insufficient for repeated loading |
| Wrong bearing selection for combined loads | Use equivalent dynamic load calculation |
| Insufficient bolt preload | Preload must exceed external separating force |
| Gear interference | Check contact ratio and minimum tooth count |

## Related Skills
- mechanics-of-materials-expert
- dynamics-expert
- cad-design-expert
