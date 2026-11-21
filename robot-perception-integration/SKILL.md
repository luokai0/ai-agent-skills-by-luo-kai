---
name: robot-perception-integration
description: Use when integrating camera, lidar, radar, depth, or other sensor perception outputs into a robot's software stack, including calibration checks, timestamp alignment, detection-to-tracking handoff, and perception validation before planning or control consumes the data.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Robot Perception Integration

## Purpose and boundaries

This skill covers the engineering work of connecting perception modules (object detection, segmentation, depth estimation, localization inputs, occupancy mapping, tracking) to downstream consumers such as planners, controllers, and safety monitors. It applies to mobile robots, manipulators, and autonomous vehicles operating in ROS-based or equivalent middleware.

In scope: sensor-to-frame calibration verification, time synchronization, message contract definition, coordinate transform chains, confidence and uncertainty propagation, latency budgeting, and integration testing against recorded and live data.

Out of scope: training new perception models, selecting hardware procurement, certifying a system for safety standards, and writing planner logic beyond the interface contract.

## Inputs and assumptions

Collect before starting:
- Sensor list with model, mounting pose, intrinsics, and the driver's published frame IDs.
- Current calibration files and their generation date and method.
- Message definitions for each perception output (fields, units, frame, stamp semantics).
- Latency and rate targets for each consumer.
- At least one recorded log (rosbag or equivalent) covering nominal operation and at least one degraded case (occlusion, glare, rain, dropout).
- Ground truth source, if any, and its own error bound.

Assume nothing about timing or frame conventions until measured. Treat any undocumented unit or frame as a defect to resolve, not a default.

## Operating workflow

1. Build a frame graph. List every frame, its parent, and the source of each transform (static URDF, calibration file, dynamic estimator). Flag cycles, duplicate parents, and frames without a publisher.
2. Verify extrinsics. Project a known target (checkerboard or fiducial) through the chain and measure reprojection or point-to-plane error. Record the number and date of samples.
3. Measure timestamp offsets. For each sensor pair, compute the stamp difference distribution on the recorded log. Use the median and 99th percentile, not the mean alone.
4. Define message contracts. For each topic, state frame ID, stamp meaning (capture, processing, or publish time), units, covariance convention, valid ranges, and confidence semantics. Write this as a versioned document in the repository.
5. Implement adapters at the boundary, not inside consumers. Adapters handle frame conversion, interpolation to a common stamp, and rejection of stale or out-of-range messages.
6. Propagate uncertainty. Carry covariance or an explicit confidence score through the handoff. Do not collapse detections to booleans before the consumer needs them.
7. Replay the log through the integrated stack in simulated-time mode and compare outputs to the contract and to ground truth.
8. Run live bench tests at rate, then in the real environment at reduced speed, before any closed-loop authority is granted.

## Decision gates

- Extrinsic gate: proceed only if reprojection error is within the tolerance set by the consumer's accuracy requirement. If no tolerance is stated, stop and request it.
- Timing gate: proceed only if 99th percentile inter-sensor offset is below one third of the consumer's update period. Otherwise add interpolation or fix hardware triggering first.
- Contract gate: no consumer may read a topic that lacks a written contract.
- Degradation gate: the integrated stack must publish a validity flag or drop to a defined safe fallback when inputs go stale beyond the contract timeout.
- Authority gate: closed-loop actuation requires explicit human sign-off from the system owner after passing all prior gates on the target hardware.

## Verification and evidence

Each gate produces a recorded artifact: calibration residual report, timing histogram, contract diff, replay comparison, and bench test log. Store them alongside the code revision and the log identifiers used.

Quantitative checks to report:
- Reprojection RMS error in pixels, per camera, with sample count.
- Stamp offset median and 99th percentile, per sensor pair.
- Detection-to-track association rate on the replay log, compared to a baseline stated in advance.
- Maximum end-to-end latency from capture stamp to consumer receipt.
- Count of messages rejected by adapters, by reason, across the replay.

Do not report a result without the dataset it came from. Do not claim improvement without a same-dataset baseline.

## Failure handling

- Calibration residual exceeds tolerance: recalibrate with more diverse target poses. Do not hand-tune extrinsics to fit the log.
- Timestamps drift over a session: check clock source and driver timestamp mode. Verify against the driver's documentation for the installed version, since timestamp options vary by release.
- Dropped or stale messages: confirm the timeout matches the consumer's update period, then test whether the fallback engages.
- Ghost or duplicated tracks: inspect whether two detectors publish the same object in different frames before changing association thresholds.

Stop and escalate when a failure involves unexplained motion of the robot, a safety monitor disagreement, or a result you cannot reproduce.

## Deliverable contract

The deliverable is a bundle containing:
1. Frame graph diagram or table with transform sources.
2. Versioned message contract documents for every perception topic.
3. Adapter code with unit tests for frame conversion and stale-message rejection.
4. Verification report covering each decision gate, with metrics, dataset identifiers, and pass/fail status.
5. Open risks list, with each item naming its owner and the condition that would change its status.

Mark any library call, message field, or tool option whose behavior depends on version as requiring verification against current official documentation before use.

## What not to do

- Do not tune thresholds on the evaluation log and report results on that same log.
- Do not merge sensor data with unknown or assumed frames.
- Do not enable closed-loop control from perception output without passing the authority gate.
- Do not state accuracy, safety, or compliance outcomes that the evidence does not directly support.
- Do not overwrite recorded logs or calibration files in place; write new versions with provenance.