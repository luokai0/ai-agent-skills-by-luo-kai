---
name: process-control-expert
version: 1.0.0
description: Expert-level process control covering feedback and feedforward control, PID tuning, advanced process control, control loop design, and process safety instrumentation.
author: luo-kai
tags: [process control, PID, feedback, feedforward, APC, DCS, safety instrumentation]
---

# Process Control Expert

## Before Starting
1. Single loop or multivariable control?
2. New design or troubleshooting existing loop?
3. Basic regulatory or advanced process control?

## Core Expertise Areas

### Feedback Control
PID controller: most widely used in chemical process control.
Proportional: reduces error but leaves offset for load disturbances.
Integral: eliminates offset, adds phase lag, can cause windup.
Derivative: improves speed of response, amplifies noise.
Direct vs reverse acting: configure based on process gain sign.

### PID Tuning
Open loop test: step test gives process gain, dead time, time constant.
IMC tuning: lambda tuning, set closed loop time constant to lambda.
Ziegler-Nichols: ultimate gain and period from sustained oscillation test.
Cohen-Coon: open loop tuning rules from FOPDT model.
Autotuning: relay feedback test, automated parameter estimation.

### Advanced Process Control
Cascade control: secondary loop controls manipulated variable faster.
Feedforward: measure disturbance and compensate before it affects output.
Ratio control: maintain fixed ratio between two streams.
Override control: select between multiple controllers based on constraint.
Model predictive control: MPC optimizes over prediction horizon with constraints.

### Safety Instrumentation
SIS: safety instrumented system, independent from basic process control.
SIL: safety integrity level determines required probability of failure on demand.
High high and low low: independent alarm and trip levels beyond normal control range.
Proof testing: periodic tests verify SIS functions correctly.

## Best Practices
- Tune controllers conservatively, tighten only if performance insufficient
- Implement anti-windup for all integrating controllers
- Segregate safety systems from regulatory control systems
- Document control philosophy and loop descriptions in control narrative

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Controller windup on output limits | Implement anti-windup in all PID controllers |
| Wrong controller action direction | Verify direct or reverse action before commissioning |
| Cascade with detuned primary | Tune secondary first then primary with secondary in auto |
| SIS on same DCS as regulatory control | Use separate independent SIS hardware |

## Related Skills
- process-design-expert
- reaction-engineering-expert
- safety-engineering-expert
