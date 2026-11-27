---
name: process-design-expert
version: 1.0.0
description: Expert-level chemical process design covering process flow diagrams, mass and energy balances, equipment sizing, economic evaluation, and sustainable process design.
author: luo-kai
tags: [process design, PFD, mass balance, energy balance, equipment sizing, economics]
---

# Process Design Expert

## Before Starting
1. Greenfield design or retrofit of existing plant?
2. Which process chemistry?
3. Preliminary or detailed design stage?

## Core Expertise Areas

### Process Flow Diagrams
BFD: block flow diagram, overall process blocks and streams.
PFD: process flow diagram, major equipment, streams with conditions and flows.
P and ID: piping and instrumentation diagram, all equipment, valves, instruments.
Stream tables: document temperature, pressure, composition, flow for each stream.

### Mass and Energy Balances
Overall balance: total mass in equals total mass out for steady state.
Component balance: each species balanced separately.
Recycle streams: iterative solution required, tear stream method.
Energy balance: enthalpy difference between inlet and outlet streams.
Reference state: choose consistent reference for enthalpy calculations.

### Equipment Sizing
Heat exchangers: LMTD and U value determine area, tube and shell sizing.
Pumps: head and flow from system curve, pump curve intersection.
Compressors: isentropic work, polytropic efficiency, staging for high ratios.
Vessels: residence time determines volume, L/D ratio for liquid-vapor separation.

### Economic Evaluation
Capital cost: purchased equipment cost, installation factor, total fixed capital.
Operating cost: raw materials, utilities, labor, maintenance, overhead.
NPV: net present value, discounted cash flows over project life.
Payback period: time to recover capital investment from operating profit.

## Best Practices
- Converge mass and energy balances before equipment sizing
- Use simulation software for complex recycle systems
- Include contingency and accuracy range in all cost estimates
- Optimize energy use through heat integration from process start

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong basis for calculations | Define basis clearly, usually per hour or per year |
| Ignoring recycle convergence | Check that recycle streams are converged before proceeding |
| Underestimating installation costs | Use appropriate Lang or Hand factor for total capital |
| Missing utility costs | Include steam, cooling water, electricity in operating cost |

## Related Skills
- reaction-engineering-expert
- separation-processes-expert
- process-control-expert
