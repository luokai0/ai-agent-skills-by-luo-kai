---
name: robot-motion-control
description: Use when designing, tuning, reviewing, or verifying motion control for robotic manipulators, mobile robots, or legged platforms, including trajectory generation, controller selection, motion safety limits, and simulation-to-hardware validation.
author: Luo Kai
provenance: original
version: 1.0.0
---

# Robot Motion Control

## Purpose and boundaries

This skill guides engineers through specifying, implementing, tuning, and verifying motion control for physical robots: joint-space and Cartesian trajectory generation, feedback control (PID, state feedback, impedance/admittance, model-based), velocity and torque limiting, and sim-to-real transfer of controllers.

In scope: kinematic and dynamic motion planning outputs consumed by a controller, low-level servo loops, motion profiles, limit checking, gain tuning procedures, and test plans for real hardware.

Out of scope: high-level task planning, perception pipelines, certification claims (CE, ISO 10218, IEC 61508 conformance is not asserted here; consult the relevant standard and a qualified assessor), and firmware changes to vendor drives beyond documented parameters.

## Inputs and assumptions

Collect before acting. If any item is missing, state the assumption explicitly in the deliverable.

- Robot model: DOF, joint limits (position, velocity, acceleration, jerk, torque), link inertias, gear ratios, encoder resolution, sensor placement.
- Actuator interface: command mode (position, velocity, torque, current), control loop rate, communication latency, and vendor-documented saturation behavior. Mark any driver-specific parameter names as requiring verification against the current vendor manual.
- Task requirements: path tolerance, cycle time, payload range, contact or non-contact operation, workspace obstacles.
- Environment: surrounding humans, fixtures, e-stop topology, safe-speed zones.
- Available tools: simulator, logging rate, measurement equipment (tracking laser, accelerometer, force sensor).

Assumptions to record: rigid-body model validity, friction model, sensor noise characteristics, and timing jitter.

## Operating workflow

1. Define the motion requirement as measurable quantities: max tracking error per axis, max Cartesian path deviation, peak joint velocity, acceleration, and jerk, plus cycle time.
2. Derive hard limits from the actuator and mechanical datasheets, then apply a margin (typically 10 to 20 percent below the lowest rated limit, unless the vendor specifies otherwise).
3. Select the trajectory profile: trapezoidal or S-curve for point-to-point joint moves; time-parameterized splines for Cartesian paths. Check that generated velocity, acceleration, and jerk stay within limits at the sampled rate.
4. Select the control law: start with joint-space PID plus feedforward (inverse dynamics or friction compensation) for position-controlled arms; use impedance or admittance control when contact is expected. Justify the choice in one paragraph.
5. Simulate in a model that includes actuator saturation, backlash or compliance if present, and sample delay. Record tracking error and torque profiles.
6. Tune gains in increasing order of risk: lower gains and reduced speed first, then scale speed in steps of no more than 25 percent per run.
7. Commission on hardware under reduced speed, with the e-stop verified before motion.

## Decision gates

- **Gate A (before hardware motion):** Simulation shows all limits respected with margin; e-stop and software limits verified by a second person; workspace clear.
- **Gate B (before increasing speed):** Tracking error within spec for three consecutive runs; no oscillation in torque or velocity; no thermal rise beyond drive guidance.
- **Gate C (before contact tasks):** Force limits configured and tested with a calibrated load or surrogate; collision detection response measured.
- **Gate D (before release):** Logged evidence reviewed; open issues accepted in writing by the robot owner.

If a gate fails, return to the earliest step that could cause the failure. Do not skip gates to meet a schedule.

## Verification and evidence

Each quality check must have a measured value and a pass threshold:

- Tracking error RMS and peak per joint, compared to the specified tolerance.
- Commanded versus achieved velocity and acceleration; peak jerk after filtering.
- Settling time and overshoot for point-to-point moves.
- Control loop jitter (standard deviation of period) below the threshold in the design requirement.
- Path deviation from the programmed Cartesian path, measured with an external reference where available.
- Torque or current peaks as a percentage of the rated limit, with thermal trend.

Log at least the sampling rate required to resolve the highest expected frequency content (generally 5 to 10 times the closed-loop bandwidth). Store raw logs, configuration hash, and gain values with each run.

## Failure handling

- **Oscillation or instability:** Stop, reduce gains by half, and check for unmodeled delay or filter lag before retuning.
- **Limit violation or fault trip:** Do not clear the fault and rerun. Inspect the log for the triggering sample, identify whether the cause is trajectory, load, or sensor, and correct before retrying.
- **Tracking error grows over time:** Suspect thermal drift, belt stretch, or payload change; measure before adjusting gains.
- **Unexpected contact:** Hold the robot in a safe state, preserve logs, and do not resume until the cause is documented.
- **Sim-to-real mismatch exceeding tolerance:** Re-identify friction and inertia parameters; do not compensate by inflating gains alone.

## Deliverable contract

Produce a motion control report containing:

1. Requirement table with measured targets and limits, including margins and their source.
2. Assumptions list with the owner and verification status of each.
3. Trajectory and controller description, including gains, filter settings, and saturation behavior.
4. Simulation results and the hardware test matrix, with pass/fail per gate.
5. Logged metrics against each quality check, with raw log references.
6. Open risks and the approver's name for any accepted deviation.
7. A list of vendor parameters marked "verify against current official documentation."

Do not state that a system is safe, certified, or compliant on the basis of this process alone. Do not report benchmark numbers that were not measured in the stated setup. Do not run hardware motion, change safety limits, or disable protective functions without explicit written approval from the responsible person; treat such actions as irreversible or external-impacting.