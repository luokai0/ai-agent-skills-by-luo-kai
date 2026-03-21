---
name: circuit-analysis-expert
version: 1.0.0
description: Expert-level circuit analysis covering KVL, KCL, nodal and mesh analysis, Thevenin and Norton theorems, AC circuits, phasors, and frequency response.
author: luokai25
tags: [circuit analysis, KVL, KCL, Thevenin, AC circuits, phasors]
---

# Circuit Analysis Expert

## Before Starting
1. DC or AC circuit?
2. Linear or nonlinear components?
3. Time domain or frequency domain analysis?

## Core Expertise Areas

### DC Circuit Analysis
KVL: sum of voltages around any closed loop equals zero.
KCL: sum of currents entering any node equals zero.
Nodal analysis: assign node voltages, write KCL at each node.
Mesh analysis: assign mesh currents, write KVL around each mesh.
Superposition: response is sum of responses to each source acting alone.

### Thevenin and Norton
Thevenin: any linear circuit reduces to voltage source in series with resistance.
Norton: any linear circuit reduces to current source in parallel with resistance.
Thevenin voltage: open circuit voltage at output terminals.
Thevenin resistance: resistance seen at terminals with all independent sources zeroed.
Maximum power transfer: load resistance equals Thevenin resistance.

### AC Circuit Analysis
Phasors: complex representation of sinusoids, amplitude and phase in one number.
Impedance: Z = R + jX, complex resistance for AC circuits.
Capacitor impedance: Z = 1 divided by j omega C, decreases with frequency.
Inductor impedance: Z = j omega L, increases with frequency.
Power factor: cos of phase angle between voltage and current.

### Frequency Response
Transfer function: ratio of output to input phasor as function of frequency.
Bode plot: magnitude and phase of transfer function vs log frequency.
Poles and zeros: determine shape of frequency response.
Resonance: LC circuit resonant frequency omega = 1 over sqrt of LC.
Q factor: quality factor, ratio of resonant frequency to bandwidth.

## Best Practices
- Always define reference node before writing nodal equations
- Check dimensional consistency in all circuit equations
- Use complex power for AC power calculations
- Verify results with SPICE simulation for complex circuits

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Sign errors in KVL | Define current directions and voltage polarities consistently |
| Forgetting reactive power | Use apparent power S = P + jQ for AC systems |
| Wrong Thevenin resistance calculation | Zero independent sources before calculating |
| Ignoring initial conditions in transients | Include capacitor voltages and inductor currents |

## Related Skills
- electronics-expert
- control-systems-expert
- signal-processing-expert
