---
name: biomechanics-expert
version: 1.0.0
description: Expert-level biomechanics covering musculoskeletal mechanics, gait analysis, joint biomechanics, soft tissue mechanics, bone mechanics, and sports biomechanics.
author: luokai25
tags: [biomechanics, musculoskeletal, gait analysis, joint mechanics, soft tissue, bone]
---

# Biomechanics Expert

## Before Starting
1. Which body region or joint?
2. Static analysis or dynamic movement?
3. Hard tissue or soft tissue focus?

## Core Expertise Areas

### Musculoskeletal Mechanics
Free body diagram: isolate body segment, include muscle forces and joint reactions.
Muscle force estimation: redundant problem, optimization methods required.
Moment arm: perpendicular distance from muscle line of action to joint center.
Hill muscle model: contractile element, series elastic, parallel elastic components.
Force-velocity relationship: muscle force decreases with increasing shortening velocity.

### Gait Analysis
Gait cycle: heel strike to next heel strike, stance 60% and swing 40%.
Ground reaction force: measured by force plate, three components.
Joint moments: inverse dynamics from kinematics and GRF data.
EMG: electromyography measures muscle activation timing and relative magnitude.
Kinematics: motion capture tracks marker positions, derives joint angles.

### Joint Biomechanics
Knee: tibiofemoral and patellofemoral joints, cruciate and collateral ligaments.
Hip: ball and socket, high contact forces, cup and stem in total hip replacement.
Spine: intervertebral disc mechanics, facet joint loading, core muscle stabilization.
Shoulder: glenohumeral instability, rotator cuff muscle coordination.

### Tissue Mechanics
Bone: cortical and cancellous, anisotropic, viscoelastic, fracture mechanics.
Cartilage: biphasic theory, fluid pressurization carries load acutely.
Ligament and tendon: nonlinear stress-strain, toe region then linear region.
Muscle: active and passive forces, fiber architecture determines function.

## Best Practices
- Include all relevant muscle forces in joint load calculations
- Validate musculoskeletal models against EMG data
- Account for soft tissue artifacts in motion capture analysis
- Use subject-specific geometry for implant design studies

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring muscle co-contraction | Antagonist muscles increase joint loading |
| Static analysis for dynamic activities | Use inverse dynamics for running and jumping |
| Wrong joint center location | Small errors propagate to large moment errors |
| Assuming rigid bone | Include deformation for fracture risk studies |

## Related Skills
- medical-devices-expert
- statics-expert
- mechanics-of-materials-expert
