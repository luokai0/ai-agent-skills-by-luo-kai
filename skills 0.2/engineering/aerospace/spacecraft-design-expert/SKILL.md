---
name: spacecraft-design-expert
version: 1.0.0
description: Expert-level spacecraft design covering mission analysis, subsystem design, power and thermal management, attitude control, communications, and systems engineering.
author: luokai25
tags: [spacecraft design, mission analysis, ADCS, power systems, thermal control, communications]
---

# Spacecraft Design Expert

## Before Starting
1. Which orbit? (LEO, MEO, GEO, deep space)
2. Mission type? (Earth observation, communications, science, exploration)
3. Which spacecraft class? (CubeSat, smallsat, traditional)

## Core Expertise Areas

### Mission Analysis
Requirements flow-down: mission objectives to system to subsystem requirements.
Orbit selection: driven by coverage, lighting, radiation, and launch cost.
Launch vehicle compatibility: mass, volume, vibration, and acoustic environments.
Mission lifetime: design life drives redundancy, radiation tolerance, consumables.

### Power Subsystem
Solar arrays: BOL and EOL power, degradation from radiation and aging.
Battery sizing: eclipse duration times average power determines capacity.
Power budget: allocate power to each subsystem with margin.
Regulation: unregulated, regulated, and hybrid bus architectures.

### Attitude Determination and Control
Sensors: star trackers, sun sensors, magnetometers, gyroscopes.
Actuators: reaction wheels, magnetorquers, thrusters.
Control modes: detumble, sun pointing, nadir pointing, inertial pointing.
Disturbance torques: gravity gradient, solar pressure, aerodynamic, magnetic.

### Thermal Control
Passive: surface coatings, MLI blankets, radiators control temperature.
Active: heaters, heat pipes, louvers for tighter temperature control.
Thermal math model: lumped capacitance nodes, radiation and conduction links.
Temperature limits: electronics typically -20 to +70 C operational.

### Communications
Link budget: transmit power, antenna gain, path loss, receiver sensitivity.
Frequency bands: UHF for CubeSats, S and X band for smallsats, Ka for high rate.
Data volume: payload data rate times contact time determines link requirements.
Ground station network: multiple stations for coverage, commercial options.

## Best Practices
- Maintain mass and power budgets with margin throughout design
- Design for testability from the start
- Model worst case hot and cold thermal environments
- Verify subsystem interfaces with interface control documents

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Insufficient power margin | Maintain 20% margin on power budget at all phases |
| Wrong eclipse fraction estimate | Calculate eclipse duration accurately for orbit |
| Missing single point failures | Review FMEA and add redundancy for critical functions |
| Underestimating radiation environment | Use environment models for actual orbit and lifetime |

## Related Skills
- orbital-mechanics-expert
- propulsion-expert
- aerodynamics-expert
