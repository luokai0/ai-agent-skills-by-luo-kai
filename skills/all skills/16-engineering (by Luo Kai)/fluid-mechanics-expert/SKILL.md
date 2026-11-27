---
name: fluid-mechanics-expert
version: 1.0.0
description: Expert-level fluid mechanics covering fluid statics, continuity, Bernoulli, Navier-Stokes, boundary layers, turbulence, pipe flow, and external aerodynamics.
author: luo-kai
tags: [fluid mechanics, Bernoulli, Navier-Stokes, turbulence, pipe flow, boundary layer]
---

# Fluid Mechanics Expert

## Before Starting
1. Incompressible or compressible flow?
2. Internal or external flow?
3. Laminar or turbulent regime?

## Core Expertise Areas

### Fluid Statics
Pressure variation: dP over dz = negative rho g, increases with depth.
Hydrostatic force: F = rho g h_c times A on submerged surface.
Center of pressure: below centroid for inclined submerged surface.
Buoyancy: upward force equals weight of displaced fluid.

### Conservation Laws
Continuity: rho A V = constant for steady 1D flow.
Bernoulli: P plus half rho V squared plus rho g z = constant along streamline.
Momentum equation: sum of forces equals rate of change of momentum.
Energy equation: adds shaft work and heat transfer to Bernoulli equation.

### Viscous Flow
Reynolds number: Re = rho V L over mu, ratio of inertia to viscous forces.
Laminar pipe flow: Poiseuille flow, parabolic velocity profile, f = 64 over Re.
Turbulent pipe flow: Moody chart relates friction factor to Re and roughness.
Navier-Stokes: governing equations for viscous flow, nonlinear, difficult to solve.

### Boundary Layer
Boundary layer: thin region near wall where viscous effects important.
Displacement thickness: effective thickness of zero velocity region.
Transition: Re_x around 500,000 for flat plate boundary layer transition.
Separation: adverse pressure gradient causes reverse flow and wake.

### Turbulence
Reynolds averaging: separate mean and fluctuating components.
Reynolds stresses: additional apparent stresses from turbulent fluctuations.
k-epsilon model: two transport equations for turbulent kinetic energy and dissipation.
DNS: direct numerical simulation resolves all scales, prohibitively expensive.

## Best Practices
- Check Reynolds number to determine flow regime before analysis
- Verify Bernoulli assumptions before applying to problem
- Use dimensional analysis to guide experimental design
- Validate CFD results against analytical or experimental benchmarks

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Applying Bernoulli across streamlines | Bernoulli valid only along a streamline |
| Ignoring minor losses in pipe systems | Include entrance, exit, fittings in head loss |
| Wrong turbulence model for separated flow | Use more advanced model or LES for separated regions |
| Incorrect Reynolds number scaling | Ensure dynamic similarity in experimental scaling |

## Related Skills
- heat-transfer-expert
- thermodynamics-mech-expert
- physics/fluid-physics-expert
