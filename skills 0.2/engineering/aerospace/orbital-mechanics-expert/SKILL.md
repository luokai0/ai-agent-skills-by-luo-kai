---
name: orbital-mechanics-expert
version: 1.0.0
description: Expert-level orbital mechanics covering Keplerian orbits, orbital maneuvers, Hohmann transfers, rendezvous, interplanetary trajectories, and perturbations.
author: luokai25
tags: [orbital mechanics, Kepler, Hohmann transfer, rendezvous, perturbations, delta-V]
---

# Orbital Mechanics Expert

## Before Starting
1. Earth orbit or interplanetary trajectory?
2. Mission design or operations focus?
3. Impulsive or low-thrust maneuvers?

## Core Expertise Areas

### Keplerian Orbits
Six orbital elements: semi-major axis, eccentricity, inclination, RAAN, argument of perigee, true anomaly.
Vis-viva equation: v squared = GM times 2 over r minus 1 over a.
Orbital period: T = 2 pi sqrt a cubed over GM.
Orbit types: circular, elliptical, parabolic, hyperbolic based on eccentricity.
Specific energy: epsilon = minus GM over 2a, negative for bound orbits.

### Orbital Maneuvers
Hohmann transfer: minimum energy transfer between circular orbits, two burns.
Delta-V: velocity change required for maneuver, determines propellant mass.
Plane change: expensive maneuver, best done at low velocity near apogee.
Bielliptic transfer: three burns, more efficient than Hohmann for large ratio orbits.
Phasing orbit: adjust timing for rendezvous by changing orbital period.

### Rendezvous and Proximity
Clohessy-Wiltshire equations: relative motion near circular reference orbit.
V-bar approach: approach along velocity vector, passive abort safe.
R-bar approach: approach along radial direction, natural drift used.
Hold points: stable relative positions for inspection before docking.

### Perturbations
J2 effect: Earth oblateness causes nodal regression and perigee rotation.
Atmospheric drag: lowers perigee, causes orbit decay for LEO satellites.
Solar radiation pressure: significant for large area-to-mass ratio spacecraft.
Third body: Moon and Sun perturb high Earth orbits.

## Best Practices
- Use high-fidelity propagator for mission planning not just two-body model
- Include delta-V margins for navigation errors and perturbations
- Check launch window constraints for planetary missions
- Verify ground track and coverage for Earth observation missions

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Two-body assumption for long missions | Include perturbations for accurate long-term propagation |
| Ignoring J2 in sun-synchronous design | J2 regression rate must equal Earth orbit rate |
| Wrong reference frame | Clarify ECI vs ECEF vs RTN before calculations |
| Underestimating delta-V margins | Add 10-15% margin for navigation and dispersions |

## Related Skills
- astrodynamics-expert
- spacecraft-design-expert
- propulsion-expert
