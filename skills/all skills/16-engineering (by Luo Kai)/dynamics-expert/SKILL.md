---
name: dynamics-expert
version: 1.0.0
description: Expert-level dynamics covering kinematics and kinetics of particles and rigid bodies, Newton-Euler equations, energy methods, impulse-momentum, and vibrations.
author: luo-kai
tags: [dynamics, kinematics, kinetics, Newton-Euler, energy methods, vibrations]
---

# Dynamics Expert

## Before Starting
1. Particle or rigid body?
2. Kinematics or kinetics?
3. Translation, rotation, or general plane motion?

## Core Expertise Areas

### Kinematics
Particle kinematics: position, velocity, acceleration as functions of time.
Projectile motion: independent horizontal and vertical motions under gravity.
Relative motion: velocity and acceleration of one point relative to another.
Rigid body rotation: v = omega cross r, a = alpha cross r minus omega squared r.
General plane motion: translation of reference point plus rotation about it.

### Kinetics of Particles
Newton second law: F = ma, vector equation in inertial frame.
Work-energy: work done equals change in kinetic energy.
Impulse-momentum: integral of F dt equals change in linear momentum.
Impact: coefficient of restitution relates velocities before and after collision.

### Kinetics of Rigid Bodies
Translation: F = m times a of center of mass.
Rotation about fixed axis: M = I alpha, moment equation about axis.
General plane motion: F = m times a_cm and M_cm = I_cm times alpha.
Angular momentum: H = I omega, conserved without external moments.

### Vibrations
Free vibration: x double-dot plus omega_n squared x = 0, solution is sinusoidal.
Natural frequency: omega_n = sqrt of k over m for spring-mass system.
Damped vibration: damping ratio zeta determines response type.
Forced vibration: resonance when excitation frequency equals natural frequency.
Transmissibility: ratio of transmitted to applied force in vibration isolation.

## Best Practices
- Clearly identify reference frame before writing kinematic equations
- Use energy methods when forces are conservative for simpler solution
- Check units throughout calculation
- Draw velocity and acceleration diagrams for complex mechanisms

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Non-inertial reference frame in Newton law | Transform to inertial frame first |
| Wrong mass moment of inertia | Use parallel axis theorem when rotating about non-centroidal axis |
| Sign error in impact problems | Define positive directions consistently before and after impact |
| Ignoring constraint forces in energy methods | Constraint forces do no work in ideal joints |

## Related Skills
- statics-expert
- mechanics-of-materials-expert
- vibrations-expert
