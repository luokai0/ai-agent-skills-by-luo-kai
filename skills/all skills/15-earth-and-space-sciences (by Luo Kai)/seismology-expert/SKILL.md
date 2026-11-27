---
name: seismology-expert
version: 1.0.0
description: Expert-level seismology covering earthquake seismology, seismic wave propagation, seismometer instrumentation, earthquake source parameters, seismic hazard, and induced seismicity.
author: luo-kai
tags: [seismology, earthquakes, seismic waves, fault mechanics, seismic hazard]
---

# Seismology Expert

## Before Starting
1. Earthquake seismology or exploration seismics?
2. Source, path, or site effects focus?
3. Seismic hazard or Earth structure application?

## Core Expertise Areas

### Seismic Waves
P-waves: compressional, fastest, travel through solids and liquids.
S-waves: shear, slower, only through solids, larger amplitude.
Surface waves: Rayleigh and Love, largest amplitude, most destructive.
Wave speeds: Vp = sqrt of (K + 4/3 G) over rho, Vs = sqrt of G over rho.

### Earthquake Source
Fault types: normal, reverse, strike-slip — defined by focal mechanism.
Focal mechanism: beach ball diagram showing fault plane and slip direction.
Moment magnitude: Mw = 2/3 log10(M0) - 6.05, M0 = seismic moment.
Stress drop: difference between initial and final stress on fault — 1-10 MPa typical.
Gutenberg-Richter: log10(N) = a - bM, b ~ 1 globally.

### Seismic Hazard
PSHA: probabilistic seismic hazard analysis — combines recurrence and attenuation.
Ground motion prediction: attenuation relations, site amplification.
Return period: 475 years for 10% in 50 years (standard engineering design).
Site effects: soft sediments amplify shaking, liquefaction in saturated sands.

### Seismometer Networks
Broadband: IRIS/FDSN global network, flat response 0.001-10 Hz.
Strong motion: accelerometers for near-field recording, not clipped by large events.
Dense arrays: local monitoring, induced seismicity, volcanic tremor.
DAS: distributed acoustic sensing, fiber-optic cables as seismic arrays.

## Best Practices
- Always check instrument response before interpreting waveforms
- Use multiple stations for reliable hypocentral location
- Consider local site conditions in hazard analysis
- Distinguish tectonic from induced seismicity using temporal patterns

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Confusing magnitude scales | Mw is preferred, others saturate for large events |
| Ignoring site amplification | Always apply site correction in hazard analysis |
| Mislabeling focal mechanism planes | Need independent data to identify fault plane |
| Forgetting time zone in phase picking | Always use UTC for seismic data |

## Related Skills
- geophysics-expert
- geology-expert
- physics/fluid-physics-expert
