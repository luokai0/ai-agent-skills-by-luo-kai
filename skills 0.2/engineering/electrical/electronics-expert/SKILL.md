---
name: electronics-expert
version: 1.0.0
description: Expert-level electronics covering diodes, BJTs, MOSFETs, amplifier design, operational amplifiers, feedback, and analog circuit design.
author: luokai25
tags: [electronics, transistors, amplifiers, op-amps, diodes, analog circuits]
---

# Electronics Expert

## Before Starting
1. Analog or digital electronics?
2. Discrete components or integrated circuits?
3. Small signal or large signal analysis?

## Core Expertise Areas

### Semiconductor Devices
p-n junction diode: exponential IV curve, forward bias conducts, reverse blocks.
Zener diode: operates in reverse breakdown, voltage regulator.
BJT: bipolar junction transistor, current-controlled, NPN and PNP types.
MOSFET: voltage-controlled, N-channel and P-channel, dominant in digital and analog.
Small signal model: linearized model around operating point for AC analysis.

### Amplifier Design
Common emitter: high voltage gain, inverts signal, medium input and output impedance.
Common source: MOSFET equivalent of CE, high voltage gain, very high input impedance.
Common collector: emitter follower, voltage gain near one, high input low output impedance.
Differential amplifier: amplifies difference, rejects common mode, used in op-amps.
Bias design: set operating point stable against temperature and device variation.

### Operational Amplifiers
Ideal op-amp: infinite gain, infinite input impedance, zero output impedance.
Inverting amplifier: gain equals negative Rf over Rin.
Non-inverting amplifier: gain equals 1 plus Rf over Rin.
Integrator: output is integral of input, capacitor in feedback.
Comparator: output saturates based on which input is larger.

### Feedback
Negative feedback: reduces gain, improves bandwidth, reduces distortion.
Gain-bandwidth product: constant for op-amp with feedback.
Stability: phase margin and gain margin determine stability of feedback loop.
Compensation: add capacitor to improve phase margin of op-amp circuits.

## Best Practices
- Always verify operating point before small signal analysis
- Use SPICE to verify hand calculations before building hardware
- Check thermal stability of bias point over temperature range
- Measure actual device parameters rather than relying on typical datasheet values

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong MOSFET region of operation | Check Vgs and Vds to determine saturation vs triode |
| Ignoring base current in BJT circuits | Include beta in bias calculations |
| Op-amp output hitting rails | Check output swing limits against signal requirements |
| Oscillation in high-gain amplifier | Check phase margin and add compensation if needed |

## Related Skills
- circuit-analysis-expert
- signal-processing-expert
- embedded-systems-expert
