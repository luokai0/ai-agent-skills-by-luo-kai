---
name: propulsion-expert
version: 1.0.0
description: Expert-level aerospace propulsion covering gas turbine engines, rocket propulsion, thermodynamic cycles, nozzle design, and propellant chemistry.
author: luokai25
tags: [propulsion, gas turbine, rockets, Brayton cycle, nozzles, thrust]
---

# Propulsion Expert

## Before Starting
1. Air-breathing or rocket propulsion?
2. Which engine type? (turbojet, turbofan, turboprop, ramjet, rocket)
3. Design point or off-design analysis?

## Core Expertise Areas

### Gas Turbine Engines
Turbojet: intake, compressor, combustor, turbine, nozzle.
Turbofan: bypass flow around core, better fuel efficiency, lower noise.
Bypass ratio: ratio of bypass to core flow, high BPR for subsonic transport.
Turboprop: turbine drives propeller via gearbox, efficient at low speed.
Compressor pressure ratio: determines thermal efficiency and specific thrust.

### Brayton Cycle Analysis
Ideal cycle: isentropic compression, constant pressure heat addition, isentropic expansion.
Thermal efficiency: eta = 1 minus 1 over r_p to power k-1 over k.
Specific fuel consumption: fuel flow per unit thrust, measure of efficiency.
Component efficiencies: polytropic efficiency for compressor and turbine.
Turbine inlet temperature: key design parameter, limited by material capability.

### Rocket Propulsion
Rocket equation: delta-V = Isp times g0 times ln m0 over mf.
Specific impulse: Isp = thrust over mass flow times g0, measure of propellant efficiency.
Liquid propellants: RP-1/LOX, LH2/LOX, hypergolic NTO/MMH.
Solid propellants: HTPB-based, simple, reliable, not throttleable.
Hybrid: solid fuel with liquid or gaseous oxidizer.

### Nozzle Design
Convergent-divergent nozzle: accelerates flow from subsonic to supersonic.
Area ratio: determines exit Mach number and expansion ratio.
Nozzle efficiency: accounts for friction and non-uniform flow losses.
Thrust coefficient: CF = thrust over P_c times At, measures nozzle performance.

## Best Practices
- Match engine design point to most critical operating condition
- Account for altitude effects on engine performance
- Verify combustion stability before finalizing injector design
- Include installation effects in installed thrust calculation

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring off-design performance | Engine must perform across full flight envelope |
| Overexpanded nozzle at sea level | Check nozzle exit pressure vs ambient |
| Underestimating turbine cooling | TIT limits require significant cooling air fraction |
| Wrong Isp units | Clarify whether Isp is in seconds or N s/kg |

## Related Skills
- aerodynamics-expert
- thermodynamics-mech-expert
- spacecraft-design-expert
