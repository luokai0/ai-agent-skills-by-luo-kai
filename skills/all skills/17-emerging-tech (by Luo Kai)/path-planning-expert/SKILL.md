---
name: path-planning-expert
version: 1.0.0
description: Expert-level robot path planning covering configuration space, sampling-based planners, graph search, trajectory optimization, and motion planning under uncertainty.
author: luo-kai
tags: [path planning, motion planning, RRT, PRM, trajectory optimization, SLAM]
---

# Path Planning Expert

## Before Starting
1. Global or local planning?
2. Known or unknown environment?
3. Holonomic or non-holonomic robot?

## Core Expertise Areas

### Configuration Space
C-space: space of all robot configurations, obstacle-free region is C-free.
C-obstacle: set of configurations causing collision with obstacles.
Dimensionality: one dimension per DOF, high-dimensional for complex robots.
Completeness: planner finds path if one exists, or reports none if not.

### Sampling-Based Planners
PRM: probabilistic roadmap, sample configs, connect nearby ones, query multiple times.
RRT: rapidly-exploring random tree, single query, extends tree toward random samples.
RRT-star: asymptotically optimal, rewires tree to minimize cost.
Bidirectional RRT: grow trees from start and goal, connect when they meet.
Informed RRT-star: focus sampling in ellipsoidal subset once solution found.

### Graph Search
Dijkstra: optimal path in weighted graph, explores all nodes within cost bound.
A-star: heuristic-guided search, optimal with admissible heuristic.
D-star: dynamic A-star, replans efficiently as new obstacles discovered.
Lattice planners: regular grid in C-space, supports non-holonomic constraints.

### Trajectory Optimization
CHOMP: covariant Hamiltonian optimization for motion planning, gradient descent.
STOMP: stochastic trajectory optimization, samples noisy trajectories.
TrajOpt: sequential convex optimization, handles collision avoidance as constraint.
Time-optimal trajectory: minimize time subject to velocity and acceleration limits.

## Best Practices
- Choose planner complexity to match problem dimensionality
- Tune sampling distribution to improve planner efficiency
- Post-process planned paths to remove unnecessary detours
- Validate planned trajectories against dynamic feasibility constraints

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Planning in task space for high-DOF robots | Plan in C-space to handle all constraints |
| Ignoring dynamic feasibility | Check velocity and acceleration limits on planned path |
| Inadequate collision checking | Use conservative bounding volumes for safety |
| RRT tree biased to initial region | Ensure uniform random sampling of C-space |

## Related Skills
- robot-kinematics-expert
- control-theory-expert
- computer-vision-robotics-expert
