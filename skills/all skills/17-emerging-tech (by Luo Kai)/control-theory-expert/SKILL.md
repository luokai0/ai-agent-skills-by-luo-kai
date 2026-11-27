---
name: control-theory-expert
version: 1.0.0
description: Expert-level control theory covering PID control, state-space methods, stability analysis, optimal control, robust control, and nonlinear control.
author: luo-kai
tags: [control theory, PID, state-space, stability, optimal control, Lyapunov]
---

# Control Theory Expert

## Before Starting
1. Linear or nonlinear system?
2. Continuous or discrete time?
3. Single input single output or multi-input multi-output?

## Core Expertise Areas

### Classical Control
Transfer function: Laplace domain representation of linear time-invariant systems.
PID controller: proportional, integral, derivative terms, most widely deployed controller.
Root locus: how closed-loop poles move as gain varies.
Bode plot: frequency response magnitude and phase vs frequency.
Gain and phase margin: stability margins from Bode plot.

### State-Space Methods
State equation: x-dot = Ax + Bu, y = Cx + Du.
Controllability: can reach any state from any initial state with appropriate input.
Observability: can infer state from output measurements.
Pole placement: choose control gain K so eigenvalues of A minus BK are desired.
Kalman filter: optimal state estimator for linear systems with Gaussian noise.

### Stability Analysis
Lyapunov stability: find positive definite V such that V-dot is negative semi-definite.
LaSalle invariance: extends Lyapunov for asymptotic stability proof.
Input-output stability: BIBO stability, bounded input gives bounded output.
Robust stability: system remains stable under bounded model uncertainty.

### Optimal Control
LQR: linear quadratic regulator, minimizes quadratic cost on state and input.
Pontryagin minimum principle: necessary conditions for optimal control.
Dynamic programming: Bellman equation, value function approach.
MPC: model predictive control, optimize over receding horizon with constraints.

### Nonlinear Control
Feedback linearization: cancel nonlinearities, apply linear control to linearized system.
Sliding mode: drive state to manifold, robust to disturbances and uncertainty.
Adaptive control: update controller parameters online as system changes.
Backstepping: systematic design for cascaded nonlinear systems.

## Best Practices
- Always verify stability before deploying controller on hardware
- Tune PID with systematic methods not random trial and error
- Validate model before designing model-based controllers
- Test controller robustness to parameter variations and disturbances

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Integral windup | Implement anti-windup in all PID controllers |
| Ignoring actuator saturation | Include saturation in stability analysis |
| Model mismatch in MPC | Robustify MPC or use adaptive approach |
| Derivative kick on setpoint change | Apply derivative on measurement not error |

## Related Skills
- robot-dynamics-expert
- robot-kinematics-expert
- mathematics/optimization-expert
