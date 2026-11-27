---
name: robot-dynamics-expert
version: 1.0.0
description: Expert-level robot dynamics covering equations of motion, Newton-Euler and Lagrangian formulations, inertia parameters, friction modeling, and dynamic simulation.
author: luo-kai
tags: [robotics, dynamics, Lagrangian, Newton-Euler, inertia, torque control]
---

# Robot Dynamics Expert

## Before Starting
1. Forward or inverse dynamics?
2. Serial or parallel manipulator?
3. Rigid body or flexible link assumption?

## Core Expertise Areas

### Lagrangian Dynamics
Lagrangian: L = T minus V, kinetic energy minus potential energy.
Euler-Lagrange equations: d/dt of partial L over partial q-dot minus partial L over partial q = tau.
Manipulator equation: M times q-double-dot plus C times q-dot plus G = tau.
Inertia matrix M: symmetric positive definite, depends on configuration.
Coriolis matrix C: centripetal and Coriolis terms, depends on config and velocity.

### Newton-Euler Formulation
Recursive algorithm: outward pass computes velocities and accelerations, inward pass computes forces.
Computational efficiency: O(n) for n-joint robot, preferred for real-time control.
Free body diagram: each link has forces and moments from adjacent links.
Inertia tensor: 3x3 matrix, depends on mass distribution and reference frame.

### Inertia Parameters
Ten parameters per link: mass, center of mass position 3 values, inertia tensor 6 values.
Parameter identification: excitation trajectories, least squares estimation.
Minimum inertia parameters: subset that fully determines dynamics, reduces to base parameters.

### Friction and Disturbances
Coulomb friction: constant opposing velocity, discontinuous at zero velocity.
Viscous friction: proportional to velocity, easy to compensate.
Stribeck effect: friction dip near zero velocity, causes stick-slip.
Gravity compensation: subtract G from control torque to cancel gravity effects.

## Best Practices
- Validate dynamics model against experimental measurements
- Use recursive Newton-Euler for real-time control implementations
- Identify inertia parameters in actual hardware for accurate model
- Include friction compensation for precision positioning tasks

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring coupling in multi-joint control | Use full dynamics model not independent joints |
| Wrong inertia reference frame | Always specify frame for inertia tensor |
| Neglecting friction in high-precision tasks | Model and compensate Coulomb and viscous friction |
| Using nominal parameters without identification | Real hardware deviates from CAD model |

## Related Skills
- robot-kinematics-expert
- control-theory-expert
- classical-mechanics-expert
