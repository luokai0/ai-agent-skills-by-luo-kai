---
name: industrial-automation-expert
version: 1.0.0
description: Expert-level industrial automation covering PLCs, SCADA, industrial networks, safety systems, robot integration, and Industry 4.0 technologies.
author: luo-kai
tags: [industrial automation, PLC, SCADA, industrial networks, safety, Industry 4.0]
---

# Industrial Automation Expert

## Before Starting
1. Discrete or process control?
2. PLC programming or system integration?
3. New installation or existing system upgrade?

## Core Expertise Areas

### PLC Programming
Ladder logic: graphical language resembling relay circuits, most common.
Function block diagram: graphical, shows data flow between function blocks.
Structured text: high-level text language similar to Pascal.
Scan cycle: read inputs, execute program, write outputs, repeat cyclically.
IEC 61131-3: standard defining five PLC programming languages.

### SCADA Systems
SCADA: supervisory control and data acquisition, monitors industrial processes.
HMI: human-machine interface, operator visualization and control.
Historian: time-series database of process data for analysis.
Alarm management: detect abnormal conditions, prioritize operator response.
Remote access: secure remote monitoring and control of distributed facilities.

### Industrial Networks
PROFIBUS: serial fieldbus for sensors and actuators, still widely deployed.
PROFINET: Ethernet-based, real-time communication, dominant in Europe.
EtherNet/IP: Ethernet-based, CIP protocol, dominant in North America.
Modbus: simple serial protocol, legacy but still common.
OPC-UA: platform-independent data exchange standard, key for Industry 4.0.

### Safety Systems
Safety PLC: certified hardware for safety-critical control functions.
SIL: safety integrity level 1 to 4, defines required risk reduction.
Functional safety: IEC 61508 and 61511 standards for safety instrumented systems.
E-stop and safety relay: hardware interlocks for emergency shutdown.

### Industry 4.0
IIoT: industrial internet of things, connect equipment to cloud analytics.
Digital twin: virtual replica of physical system for simulation and optimization.
Edge computing: process data locally before sending to cloud.
Predictive maintenance: sensor data and ML to predict equipment failure.

## Best Practices
- Always follow functional safety standards for safety-critical systems
- Document all ladder logic with clear comments and naming conventions
- Test changes in simulation or off-line before deploying to live plant
- Implement network segmentation to protect control systems from IT threats

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Scan time overrun | Optimize program or increase scan time allocation |
| Missing watchdog timer | Always implement watchdog for critical control loops |
| Inadequate cybersecurity | Segment OT network from IT and internet |
| Ignoring safety lifecycle | Follow IEC 61508 from concept through decommissioning |

## Related Skills
- control-theory-expert
- ros-expert
- embedded-expert
