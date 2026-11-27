---
name: robot-kinematics-expert
version: 1.0.0
description: Expert-level robot kinematics covering forward and inverse kinematics, Denavit-Hartenberg parameters, workspace analysis, singularities, and Jacobian-based methods.
author: luo-kai
tags: [robotics, kinematics, DH parameters, inverse kinematics, Jacobian]
---

# Robot Kinematics Expert

## Before Starting
1. Serial or parallel manipulator?
2. Forward or inverse kinematics focus?
3. Analytical or numerical solution needed?

## Core Expertise Areas

### Forward Kinematics
DH parameters: four parameters per joint define frame transformations.
Homogeneous transformation: 4x4 matrix combining rotation and translation.
Frame assignment: DH convention assigns frames to each link systematically.
End-effector pose: product of joint transformation matrices.
Modified DH: Craig convention places frame at proximal joint.

### Inverse Kinematics
Analytical IK: closed-form solution, fast, handles all configurations.
Numerical IK: iterative Jacobian-based methods, general but may not converge.
Multiple solutions: most robots have multiple IK solutions for same end-effector pose.
Singularities: configurations where Jacobian loses rank, infinite IK solutions.
Workspace: reachable and dexterous workspace depend on link lengths and joint limits.

### Jacobian
Geometric Jacobian: maps joint velocities to end-effector velocities.
Analytical Jacobian: partial derivatives of forward kinematics with respect to joint angles.
Jacobian transpose: simple inverse kinematics controller, no matrix inversion.
Pseudoinverse: minimum norm solution for redundant robots.
Damped least squares: avoids singularity issues in numerical IK.

### Spatial Representations
Rotation matrices: 3x3 orthogonal, no singularity but 9 parameters for 3 DOF.
Euler angles: minimal representation, suffer from gimbal lock.
Quaternions: 4 parameters, no singularity, efficient for interpolation.
Axis-angle: intuitive, axis unit vector plus rotation angle.

## Best Practices
- Check DH parameter table against robot manual before implementation
- Always verify forward kinematics against known configurations
- Implement singularity detection and avoidance in controllers
- Use quaternions for orientation interpolation to avoid gimbal lock

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Wrong DH convention | Clarify standard vs modified DH before implementation |
| Ignoring joint limits in IK | Filter solutions violating joint limits |
| Euler angle gimbal lock | Switch to quaternions or rotation matrices |
| Jacobian singularity causing instability | Add damping or singularity avoidance |

## Related Skills
- robot-dynamics-expert
- control-theory-expert
- path-planning-expert
