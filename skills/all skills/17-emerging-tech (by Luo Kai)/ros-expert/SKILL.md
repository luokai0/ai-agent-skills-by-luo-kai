---
name: ros-expert
version: 1.0.0
description: Expert-level ROS and ROS2 covering architecture, nodes, topics, services, actions, launch files, tf2 transforms, Nav2 navigation, and MoveIt motion planning.
author: luo-kai
tags: [ROS, ROS2, robotics, navigation, MoveIt, transforms, nodes]
---

# ROS Expert

## Before Starting
1. ROS1 or ROS2?
2. Which robot platform?
3. Navigation, manipulation, or perception focus?

## Core Expertise Areas

### ROS2 Architecture
Nodes: processes that perform computation, communicate via topics, services, actions.
DDS: data distribution service middleware, replaces ROS1 master.
Topics: publish-subscribe, asynchronous, unidirectional data streams.
Services: request-response, synchronous, short discrete tasks.
Actions: long-running tasks with feedback, goal, result, cancel interface.

### Communication
Messages: typed data structures defined in .msg files.
QoS: quality of service profiles for reliability and history depth.
Parameters: node configuration values, dynamic reconfigure at runtime.
Bag files: record and replay topic data for testing and debugging.

### TF2 Transforms
Transform tree: hierarchy of coordinate frames in robot system.
Static transforms: fixed transforms, published once, for rigid links.
Dynamic transforms: changing transforms, joint states drive robot model.
Lookup: query transform between any two frames at any time in the past.

### Navigation
Nav2: ROS2 navigation stack, global and local planners, costmaps.
Costmap: occupancy grid representing obstacles for planning.
AMCL: adaptive Monte Carlo localization, particle filter for position tracking.
Behavior trees: Nav2 uses BT for task execution and recovery behaviors.

### MoveIt
Motion planning: OMPL planners, collision checking, trajectory execution.
Planning scene: environment model with objects and robot for collision checking.
Kinematics plugins: KDL, TRAC-IK, bio-IK for inverse kinematics.
Execution: trajectory controller interface to robot hardware.

## Best Practices
- Use ROS2 for new projects, prefer lifecycle nodes for robust startup
- Set appropriate QoS for sensor data reliability requirements
- Always check tf tree completeness before running navigation
- Use simulation before deploying to real hardware

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Missing tf frames causing lookup failures | Check tf tree with ros2 run tf2_tools view_frames |
| Wrong QoS causing dropped messages | Match publisher and subscriber QoS profiles |
| Costmap not updating | Check sensor topic names and frame ids |
| MoveIt planning failing | Check SRDF, collision objects, and IK solver config |

## Related Skills
- robot-kinematics-expert
- path-planning-expert
- computer-vision-robotics-expert
