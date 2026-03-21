---
name: surveying-expert
version: 1.0.0
description: Expert-level surveying covering leveling, traverses, coordinate geometry, GPS and GNSS, total station surveys, LiDAR, and construction layout.
author: luokai25
tags: [surveying, leveling, traverses, GPS, total station, LiDAR, coordinate geometry]
---

# Surveying Expert

## Before Starting
1. Boundary, topographic, or construction survey?
2. Conventional or GNSS methods?
3. Required accuracy and closure tolerance?

## Core Expertise Areas

### Leveling
Differential leveling: backsight minus foresight gives elevation difference.
HI method: instrument height = BM elevation plus BS reading.
Closure error: acceptable error proportional to sqrt of distance leveled.
Benchmark: permanent point of known elevation, datum reference.
Profile leveling: elevations along centerline for road or pipeline design.

### Traverses
Open traverse: series of connected lines, no closure check.
Closed traverse: returns to starting point or known point, closure check possible.
Azimuth and bearing: direction of traverse lines, azimuth from north clockwise.
Closure error: linear error of closure and relative precision.
Adjustment: Bowditch method distributes closure error proportional to distance.

### Coordinate Geometry
State plane coordinates: project geodetic positions to flat grid for calculations.
Inverse problem: compute distance and direction between two coordinate pairs.
Intersection: locate point from two known stations by angle measurement.
Resection: determine unknown position from observations to known points.

### GNSS Surveying
GPS principles: trilateration from four or more satellite ranging signals.
RTK: real-time kinematic, centimeter accuracy using base station correction.
Network RTK: virtual reference station from network of base stations.
PDOP: position dilution of precision, lower is better, below 3 preferred.

### Modern Methods
Total station: electronic angle and distance measurement, data logging.
LiDAR: laser scanning produces dense 3D point cloud of terrain or structures.
UAV photogrammetry: drone imagery processed into 3D surface models.
BIM integration: survey data feeds directly into building information models.

## Best Practices
- Always check instrument calibration before beginning survey
- Establish redundant measurements for important control points
- Document all field notes completely for later reference
- Verify coordinates against known control before construction layout

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Undetected blunders in traverse | Check closure after each leg, not just at end |
| GNSS multipath in urban canyons | Use conventional methods or wait for better satellite geometry |
| Wrong datum for project | Confirm all data uses same horizontal and vertical datum |
| Insufficient benchmarks for large project | Establish intermediate benchmarks at 500m intervals |

## Related Skills
- structural-engineering-expert
- geotechnical-engineering-expert
- transportation-engineering-expert
