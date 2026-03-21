---
name: vlsi-design-expert
version: 1.0.0
description: Expert-level VLSI design covering CMOS logic, custom layout, standard cell design, physical design flow, DRC, LVS, and advanced process nodes.
author: luokai25
tags: [VLSI, CMOS, layout, standard cells, physical design, DRC, LVS]
---

# VLSI Design Expert

## Before Starting
1. Full custom or standard cell design?
2. Which technology node?
3. Analog, digital, or mixed-signal circuit?

## Core Expertise Areas

### CMOS Logic
NMOS: n-channel MOSFET, conducts when gate voltage high.
PMOS: p-channel MOSFET, conducts when gate voltage low.
CMOS inverter: PMOS pull-up, NMOS pull-down, low static power.
CMOS gate: pull-up network PMOS, pull-down network NMOS, dual networks.
Propagation delay: function of load capacitance and drive strength.

### Custom Layout
Design rules: minimum widths, spacings, enclosures for each layer.
Poly, diffusion, metal layers: stack of conducting and insulating layers.
Transistor layout: gate poly crosses active diffusion, contacts on source and drain.
Matching: common centroid layout for differential pairs and current mirrors.
Parasitic extraction: RC parasitics from layout affect circuit performance.

### Physical Design Flow
Floorplanning: partition design into blocks, place macro cells and I/O.
Placement: position standard cells to minimize wire length and meet timing.
Clock tree synthesis: distribute clock with balanced skew and minimal jitter.
Routing: connect cells with metal wires respecting design rules.
Sign-off: DRC, LVS, ERC, timing closure, power analysis.

### Advanced Nodes
FinFET: 3D transistor, multiple gates, better electrostatic control below 20nm.
GAA: gate all around, nanosheets wrap gate completely, used at 3nm and below.
Low-k dielectric: reduce parasitic capacitance between metal layers.
Multi-patterning: achieve sub-wavelength features using multiple lithography passes.

## Best Practices
- Always run DRC and LVS before tapeout
- Extract parasitics and re-simulate critical analog circuits
- Design for manufacturing with OPC and redundant vias
- Meet electromigration rules for all metal layers

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Antenna violations | Add antenna diodes or break metal routes |
| Electromigration violations | Widen critical current-carrying metals |
| Poor matching from mismatch | Use common centroid and dummy structures |
| Clock skew causing timing violations | Rebalance clock tree or adjust placement |

## Related Skills
- digital-electronics-expert
- electronics-expert
- circuit-analysis-expert
