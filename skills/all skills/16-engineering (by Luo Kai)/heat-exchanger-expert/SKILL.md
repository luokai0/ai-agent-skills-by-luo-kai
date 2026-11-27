---
name: heat-exchanger-expert
version: 1.0.0
description: Expert-level heat exchanger design covering shell and tube, plate, air coolers, heat integration, fouling, and thermal-hydraulic design methods.
author: luo-kai
tags: [heat exchangers, shell and tube, plate heat exchanger, fouling, LMTD, heat integration]
---

# Heat Exchanger Expert

## Before Starting
1. Which exchanger type? (shell and tube, plate, air cooler)
2. New design or rating of existing exchanger?
3. Which fluids and operating conditions?

## Core Expertise Areas

### Heat Exchanger Design
Overall heat transfer coefficient: 1 over U = 1 over hi + rf_i + t over k + rf_o + 1 over ho.
LMTD method: Q = U times A times LMTD times F, F is correction for non-counterflow.
Effectiveness-NTU: use when outlet temperatures unknown, useful for rating.
TEMA standards: Tubular Exchanger Manufacturers Association, designates shell and tube types.

### Shell and Tube Design
Tube side: fluid in tubes, higher pressure service, easier cleaning.
Shell side: fluid outside tubes, baffles direct flow, lower pressure drop.
Baffle design: segmental baffles, 25% cut standard, spacing affects heat transfer and pressure drop.
Tube bundle: fixed, floating head, or U-tube for thermal expansion accommodation.
TEMA types: E, F, G, H, J, X shells with different flow configurations.

### Fouling
Fouling resistance: rf added to thermal resistance, reduces effective U.
Types: particulate, crystallization, corrosion, biological, polymerization fouling.
Mitigation: velocity above 1 m/s, smooth surfaces, chemical treatment, periodic cleaning.
Oversurface: design with extra area to account for fouling over run length.

### Heat Integration
Pinch analysis: identify maximum energy recovery from process hot and cold streams.
Minimum utility: set by pinch temperature, determines minimum heating and cooling.
Heat exchanger network: match hot and cold streams to minimize utility use.
Above and below pinch: never transfer heat across pinch point.

## Best Practices
- Use TEMA fouling factors appropriate for fluid and service
- Verify tube velocity above minimum to prevent fouling and below maximum to prevent erosion
- Check thermal expansion accommodation in fixed tubesheet design
- Perform vibration analysis for shell-side cross flow over tubes

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| LMTD correction factor too low | Consider different configuration or multiple shells in series |
| Excessive pressure drop | Optimize baffle spacing and tube count |
| Ignoring nozzle pressure drop | Include nozzle losses in hydraulic design |
| No provision for cleaning | Design removable bundle or cleaning access for fouling service |

## Related Skills
- heat-transfer-expert
- process-design-expert
- process-simulation-expert
