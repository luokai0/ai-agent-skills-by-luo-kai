---
name: astrodynamics-expert
version: 1.0.0
description: Expert-level astrodynamics covering orbit determination, trajectory optimization, launch vehicle ascent, re-entry dynamics, and numerical methods for space mission analysis.
author: luokai25
tags: [astrodynamics, orbit determination, trajectory optimization, re-entry, launch]
---

# Astrodynamics Expert

## Before Starting
1. Orbit determination or trajectory design?
2. Launch, on-orbit, or re-entry phase?
3. Impulsive or continuous thrust optimization?

## Core Expertise Areas

### Orbit Determination
Angles-only IOD: Gauss and Laplace methods from three observations.
Range and range-rate: Doppler and ranging measurements for tracking.
Batch least squares: fit orbit to set of observations, minimize residuals.
Kalman filter: sequential estimation updating state with each new observation.
TLE format: two-line element sets from NORAD for catalog objects.

### Trajectory Optimization
Optimal control: Pontryagin minimum principle for minimum fuel trajectories.
Lambert problem: find transfer orbit between two position vectors in given time.
Porkchop plots: contours of delta-V vs departure and arrival date.
Gravity assists: flyby maneuver gains energy from planetary gravity.
Low-thrust: electric propulsion, continuous thrust, requires numerical optimization.

### Launch Vehicle Ascent
Pitch program: gravity turn trajectory minimizes aerodynamic loads.
Staging: discard empty tanks to improve mass ratio.
Payload fairing: protects payload in atmosphere, jettisoned at low dynamic pressure.
Insertion accuracy: target orbit achieved within dispersion limits.

### Re-entry Dynamics
Entry interface: typically 120 km altitude for Earth re-entry.
Heating rate: depends on velocity squared times atmospheric density.
Ballistic coefficient: m over CdA, high BC means less deceleration per unit area.
Skip re-entry: graze atmosphere to reduce heating and extend range.
TPS: thermal protection system, ablative or reusable tiles.

## Best Practices
- Use J2000 inertial frame as reference for orbit calculations
- Validate Lambert solver against known solutions before mission use
- Account for launch site constraints on achievable inclination
- Include Monte Carlo analysis for re-entry landing ellipse

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong gravitational parameter | Use GM = 3.986e14 m3/s2 for Earth |
| Ignoring atmosphere in LEO orbit life | Even tenuous atmosphere causes significant decay |
| Lambert problem time-of-flight sign | Check prograde vs retrograde solution selection |
| Re-entry angle too shallow | Skip-out or range overshoot, too steep causes excessive heating |

## Related Skills
- orbital-mechanics-expert
- spacecraft-design-expert
- propulsion-expert
