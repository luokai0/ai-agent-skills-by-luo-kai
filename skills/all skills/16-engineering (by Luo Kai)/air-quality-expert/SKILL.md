---
name: air-quality-expert
version: 1.0.0
description: Expert-level air quality engineering covering pollutant sources, atmospheric dispersion, air quality standards, emission controls, and air quality modeling.
author: luo-kai
tags: [air quality, dispersion modeling, emissions, pollutants, air quality standards]
---

# Air Quality Expert

## Before Starting
1. Source characterization or receptor modeling?
2. Regulatory compliance or research focus?
3. Which pollutants? (criteria, HAPs, GHGs)

## Core Expertise Areas

### Pollutants and Standards
Criteria pollutants: CO, NOx, SOx, PM2.5, PM10, ozone, lead under NAAQS.
HAPs: hazardous air pollutants, 187 listed under Clean Air Act.
GHGs: CO2, CH4, N2O, HFCs regulated under climate policy.
NAAQS: national ambient air quality standards, primary and secondary standards.
AQI: air quality index 0-500, communicates health risk to public.

### Emission Sources
Point sources: stacks, vents, identifiable single emission points.
Area sources: fugitive emissions, agricultural, small sources aggregated.
Mobile sources: vehicles, aircraft, trains, significant urban contribution.
Emission factors: AP-42 database provides emission factors by source category.
Continuous monitoring: CEMS measure emissions in real time for major sources.

### Atmospheric Dispersion
Gaussian plume: C = Q over 2 pi sigma_y sigma_z u times exponential terms.
Stability classes: Pasquill-Gifford A through F, neutral D most common.
Mixing height: limits vertical dispersion, varies diurnally.
AERMOD: EPA preferred model for near-field dispersion from industrial sources.
CALPUFF: Lagrangian puff model for long range and complex terrain.

### Emission Controls
Electrostatic precipitator: charge and collect particles, over 99% efficiency.
Fabric filter: baghouse, PM control, efficiency depends on fabric and cleaning.
Wet scrubber: spray liquid absorbs gas pollutants and large particles.
SCR: selective catalytic reduction, NOx control using ammonia over catalyst.
Thermal oxidizer: combust VOCs and HAPs at high temperature.

## Best Practices
- Use site-specific meteorological data for dispersion modeling
- Validate emission inventory with source testing periodically
- Apply best available control technology for new major sources
- Consider secondary pollutant formation from primary emissions

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Default met data instead of site-specific | Use on-site or nearest representative met station |
| Ignoring building downwash | Include building downwash for stacks near tall structures |
| Wrong emission factor for source type | Match AP-42 table to actual process conditions |
| Missing fugitive emissions | Fugitive sources often exceed stack emissions |

## Related Skills
- environmental-remediation-expert
- water-treatment-expert
- climatology-expert
