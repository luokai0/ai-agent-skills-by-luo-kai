---
name: embedded-systems-expert
version: 1.0.0
description: Expert-level embedded systems covering microcontrollers, RTOS, peripheral interfaces, low-power design, bare-metal programming, and embedded Linux.
author: luokai25
tags: [embedded systems, microcontrollers, RTOS, bare-metal, peripherals, low-power]
---

# Embedded Systems Expert

## Before Starting
1. Bare-metal or RTOS-based?
2. Which microcontroller family? (ARM, AVR, ESP32, STM32)
3. Real-time constraints or resource constraints primary concern?

## Core Expertise Areas

### Microcontroller Fundamentals
Architecture: CPU core, flash, RAM, peripherals integrated on one chip.
ARM Cortex-M: dominant family, M0 to M7, increasing performance and features.
Memory map: code, SRAM, peripherals mapped to address space.
Interrupts: NVIC handles priorities, ISR must be short and non-blocking.
Startup code: initialize stack, copy data to RAM, zero BSS, call main.

### Peripheral Interfaces
GPIO: general purpose IO, configure as input or output, pull-up or pull-down.
UART: serial communication, baud rate, start and stop bits, parity.
SPI: synchronous serial, four wires, master-slave, high speed.
I2C: two-wire serial, multi-device on same bus, 7-bit addressing.
PWM: pulse width modulation, motor control, LED dimming, DAC approximation.

### RTOS
Task: independent thread of execution, priority, stack size.
Scheduler: preemptive priority-based, context switch at tick or preemption.
Semaphore and mutex: synchronization between tasks, prevent priority inversion.
Queue: inter-task communication, FIFO data passing.
FreeRTOS: most popular open source RTOS, widely supported.

### Low-Power Design
Sleep modes: stop, standby, hibernate trade wake time for power savings.
Clock gating: disable peripheral clocks when not in use.
Voltage scaling: reduce core voltage at lower frequencies.
Wake sources: RTC, GPIO interrupt, watchdog timer to exit low power mode.

## Best Practices
- Keep ISRs short, set flags and return, process in main loop or task
- Use watchdog timer to recover from firmware hangs
- Test memory usage to avoid stack overflow
- Use hardware debugger not just printf for embedded debugging

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Stack overflow | Size stack carefully, use RTOS stack monitoring |
| Race condition on shared data | Use mutex or disable interrupts around critical section |
| Floating point in ISR | Avoid FPU in ISR or save and restore FPU state |
| Blocking in ISR | Set flag in ISR, process in task or main loop |

## Related Skills
- electronics-expert
- circuit-analysis-expert
- linux-expert
