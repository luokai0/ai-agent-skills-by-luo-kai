---
name: flight-mechanics-expert
version: 1.0.0
description: Expert-level flight mechanics covering aircraft equations of motion, stability and control, performance, handling qualities, and flight simulation.
author: luokai25
tags: [flight mechanics, stability, control, performance, equations of motion, handling qualities]
---

# Flight Mechanics Expert

## Before Starting
1. Fixed wing or rotary wing?
2. Stability analysis or performance calculation?
3. Longitudinal or lateral-directional focus?

## Core Expertise Areas

### Equations of Motion
Six DOF: three translational and three rotational equations in body axes.
Body axes: x forward, y right, z down, aligned with aircraft.
Euler angles: roll phi, pitch theta, yaw psi relate body to inertial frame.
Linearization: small perturbation equations about trim condition.
Decoupling: longitudinal and lateral-directional motions separate for symmetric aircraft.

### Longitudinal Stability
Stick-fixed neutral point: CG location for neutral pitch stability.
Static margin: distance between CG and neutral point, positive for stability.
Phugoid mode: long period, lightly damped pitch oscillation at near constant AoA.
Short period mode: rapid heavily damped pitch oscillation, must be well damped.
Pitch stiffness: Cm_alpha negative for stable aircraft.

### Lateral-Directional Stability
Dihedral effect: roll restoring moment from sideslip, Cl_beta negative.
Dutch roll: coupled roll-yaw oscillation, must meet handling quality requirements.
Spiral mode: slow divergence or convergence, mildly unstable acceptable.
Roll mode: first order roll response to aileron input.

### Aircraft Performance
Thrust required: TR = W times CD over CL.
Maximum range: fly at maximum L over D for jet aircraft.
Maximum endurance: fly at minimum power required.
Rate of climb: RC = excess power over weight.
V-n diagram: flight envelope, structural and aerodynamic limits.

## Best Practices
- Verify trim condition before performing stability analysis
- Check handling qualities against MIL-SPEC or civil requirements
- Include flexible modes for large or high aspect ratio aircraft
- Validate simulation model against flight test data

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong body axis convention | Define axes clearly before writing equations |
| Ignoring propulsion effects on stability | Slipstream and thrust line affect trim and stability |
| Linear analysis outside valid range | Check perturbation amplitudes against nonlinear effects |
| Missing ground effect in takeoff analysis | Ground effect increases L/D near runway |

## Related Skills
- aerodynamics-expert
- control-systems-expert
- astrodynamics-expert
