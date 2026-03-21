---
name: digital-electronics-expert
version: 1.0.0
description: Expert-level digital electronics covering Boolean algebra, combinational and sequential logic, FPGA design, HDL programming, timing analysis, and digital system design.
author: luokai25
tags: [digital electronics, Boolean algebra, FPGA, VHDL, Verilog, timing, logic design]
---

# Digital Electronics Expert

## Before Starting
1. ASIC or FPGA implementation?
2. RTL design or verification focus?
3. Which HDL? Verilog or VHDL?

## Core Expertise Areas

### Boolean Logic
Boolean algebra: AND, OR, NOT operations, De Morgan theorems.
Karnaugh map: minimize Boolean expressions graphically, group ones.
Sum of products: canonical form from truth table, AND terms ORed together.
NAND and NOR universality: any logic function implementable with only NAND or only NOR.

### Combinational Logic
Multiplexer: select one of N inputs based on select lines.
Decoder: N inputs to 2 to the N outputs, one-hot output.
Adder: half adder, full adder, ripple carry, carry look-ahead.
Comparator: outputs equal, greater than, less than for two binary numbers.
Propagation delay: time for output to respond to input change.

### Sequential Logic
D flip-flop: samples input on clock edge, most common storage element.
Registers: parallel flip-flops share clock, store multi-bit values.
Counters: binary, Gray code, up-down, synchronous and asynchronous.
State machines: Moore and Mealy, state transition diagram, next state logic.
Setup and hold time: data must be stable around clock edge for correct capture.

### FPGA and HDL
FPGA architecture: LUT-based logic, flip-flops, block RAM, DSP slices, I/O.
Verilog: hardware description language, structural and behavioral modeling.
Synthesis: HDL converted to netlist of standard cells or FPGA primitives.
Timing analysis: static timing analysis verifies setup and hold margins.
Place and route: map netlist to physical FPGA resources, meet timing constraints.

## Best Practices
- Synchronize all inputs to clock domain before using in logic
- Avoid latches by ensuring all paths in combinational always blocks have else clause
- Use synchronous reset for FPGA designs
- Run static timing analysis after every significant change

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Metastability from async inputs | Use two flip-flop synchronizer for all async signals |
| Inferred latches | Assign default values to all outputs in combinational logic |
| Clock domain crossing issues | Use proper CDC techniques with synchronizers |
| Timing violations ignored | Fix all timing violations before tapeout or deployment |

## Related Skills
- circuit-analysis-expert
- embedded-systems-expert
- vlsi-design-expert
