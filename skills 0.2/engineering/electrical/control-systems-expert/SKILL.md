---
name: control-systems-expert
version: 1.0.0
description: Expert-level control systems engineering covering feedback control, PID design, root locus, frequency domain methods, state-space design, and digital control.
author: luokai25
tags: [control systems, PID, root locus, Bode, state-space, digital control]
---

# Control Systems Expert

## Before Starting
1. Continuous or discrete time system?
2. SISO or MIMO?
3. Classical or modern control approach?

## Core Expertise Areas

### System Modeling
Transfer function: Laplace domain ratio of output to input for LTI systems.
Block diagram: graphical representation of system interconnections.
State-space: x-dot = Ax + Bu, y = Cx + Du, more general than transfer function.
Linearization: approximate nonlinear system around operating point.
System identification: estimate model parameters from input-output data.

### Classical Control Design
PID: proportional integral derivative, most widely used industrial controller.
Root locus: graphical method to design gain for desired closed-loop poles.
Lead compensator: improves phase margin, speeds up transient response.
Lag compensator: improves steady-state error, reduces high frequency gain.
Ziegler-Nichols: empirical PID tuning from step response or ultimate gain.

### Frequency Domain Design
Gain margin: additional gain before instability, read from Bode at phase -180.
Phase margin: additional phase lag before instability, read from Bode at 0 dB.
Bandwidth: frequency range of effective control, affects disturbance rejection.
Sensitivity function: closed-loop sensitivity to disturbances and model errors.

### Digital Control
Discretization: convert continuous controller to discrete, Tustin or ZOH method.
Sampling rate: choose 10 to 20 times bandwidth for adequate digital control.
Quantization: finite word length effects, limit cycles in digital controllers.
Computational delay: accounts for processing time, degrades phase margin.

## Best Practices
- Always verify stability margins before deploying controller
- Tune conservatively and increase aggressiveness only if needed
- Test controller on simulation model before hardware
- Document tuning rationale for future maintenance

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Insufficient phase margin | Add lead compensation to improve phase margin |
| Integral windup | Implement anti-windup for all integrating controllers |
| Sampling too slow | Sample at minimum 10 times controller bandwidth |
| Ignoring actuator saturation | Include saturation in analysis and add anti-windup |

## Related Skills
- circuit-analysis-expert
- signal-processing-expert
- control-theory-expert
