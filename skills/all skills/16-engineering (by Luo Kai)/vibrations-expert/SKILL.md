---
name: vibrations-expert
version: 1.0.0
description: Expert-level mechanical vibrations covering free and forced vibration, damping, resonance, modal analysis, vibration isolation, and rotating machinery.
author: luo-kai
tags: [vibrations, resonance, modal analysis, damping, rotating machinery, vibration isolation]
---

# Vibrations Expert

## Before Starting
1. Single DOF or multi DOF system?
2. Free, forced, or self-excited vibration?
3. Time domain or frequency domain analysis?

## Core Expertise Areas

### Single DOF Systems
Equation of motion: m x-double-dot + c x-dot + k x = F(t).
Natural frequency: omega_n = sqrt of k over m.
Damping ratio: zeta = c over 2 sqrt of km.
Underdamped: oscillatory decay, frequency omega_d = omega_n sqrt of 1 minus zeta squared.
Critically damped: fastest return to equilibrium without oscillation.

### Forced Vibration
Steady-state amplitude: X = F0 over k times magnification factor.
Resonance: maximum amplitude when excitation frequency equals natural frequency.
Phase angle: response lags excitation, 90 degrees at resonance.
Frequency response function: complex ratio of output to input versus frequency.

### Multi DOF Systems
Mass and stiffness matrices: M x-double-dot + K x = F.
Natural frequencies: eigenvalues of K inverse M.
Mode shapes: eigenvectors, orthogonal with respect to mass matrix.
Modal superposition: response is sum of individual mode responses.

### Rotating Machinery
Unbalance: mass offset from rotation axis causes rotating force excitation.
Critical speed: rotation speed equals natural frequency, resonance in rotor.
Balancing: single plane and two plane balancing to reduce unbalance forces.
Campbell diagram: plot natural frequencies and excitation orders versus speed.

### Vibration Isolation
Transmissibility: ratio of transmitted to applied force.
Isolation: below natural frequency amplifies, above attenuates vibration.
Design rule: isolator natural frequency below one third excitation frequency.
Soft mounts: low stiffness isolators, good isolation but large static deflection.

## Best Practices
- Identify all resonances and ensure operating range avoids them
- Add damping if resonance cannot be avoided through design
- Measure actual natural frequencies to validate analytical models
- Design vibration isolation based on actual equipment operating frequencies

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring damping in resonance analysis | Even small damping limits response at resonance |
| Wrong isolation region | Ensure operating frequency is well above isolator natural frequency |
| Missing higher modes in truncated modal analysis | Include sufficient modes for accurate response |
| Unbalance in rotating equipment | Perform field balancing after assembly |

## Related Skills
- dynamics-expert
- statics-expert
- control-systems-expert
