---
name: heat-transfer-expert
version: 1.0.0
description: Expert-level heat transfer covering conduction, convection, radiation, heat exchangers, fins, transient heat transfer, and computational heat transfer.
author: luo-kai
tags: [heat transfer, conduction, convection, radiation, heat exchangers, fins]
---

# Heat Transfer Expert

## Before Starting
1. Which mode? (conduction, convection, radiation, or combined)
2. Steady state or transient?
3. Internal or external convection?

## Core Expertise Areas

### Conduction
Fourier law: q = negative k A dT over dx, heat flows down temperature gradient.
Thermal resistance: R = L over kA for flat wall, ln(r2 over r1) over 2 pi k L for cylinder.
Composite walls: resistances in series and parallel, total R determines heat flux.
Fins: extended surfaces increase heat transfer area, fin efficiency eta_f.
Biot number: Bi = hL over k, ratio of convection to conduction resistance.

### Convection
Newton cooling law: q = h A delta T, h is convection coefficient.
Nusselt number: Nu = hL over k, dimensionless convection coefficient.
Forced external: flat plate Nu correlations, cylinder in cross flow.
Forced internal: Dittus-Boelter for turbulent pipe flow, Sieder-Tate with viscosity correction.
Natural convection: buoyancy driven, Rayleigh number Ra = Gr times Pr.

### Radiation
Stefan-Boltzmann: q = epsilon sigma A T4, radiation from surface at T.
View factor: F_12 is fraction of radiation from 1 intercepted by 2.
View factor reciprocity: A1 F12 = A2 F21.
Radiation network: analogous to electrical resistance for enclosures.
Gray body: emissivity constant with wavelength, simplifies radiation calculations.

### Heat Exchangers
LMTD method: Q = UA times LMTD, log mean temperature difference.
Effectiveness-NTU: useful when outlet temperatures unknown.
Parallel flow vs counterflow: counterflow achieves closer temperature approach.
Fouling: additional thermal resistance from deposits, reduces performance over time.

## Best Practices
- Identify dominant heat transfer mode before detailed analysis
- Check Biot number to determine if lumped capacitance is valid
- Use appropriate correlation for flow geometry and regime
- Account for fouling in heat exchanger design with fouling factors

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Lumped capacitance when Bi greater than 0.1 | Use spatial analysis or numerical method |
| Wrong correlation for flow regime | Check Re and geometry match correlation assumptions |
| Ignoring radiation at high temperature | Radiation scales as T4, dominates above 500 C |
| LMTD undefined for equal inlet-outlet temperatures | Use effectiveness-NTU method instead |

## Related Skills
- fluid-mechanics-expert
- thermodynamics-mech-expert
- manufacturing-processes-expert
