---
name: quantum-computing-expert
version: 1.0.0
description: Expert-level quantum computing covering qubits, quantum gates, quantum algorithms, error correction, quantum hardware platforms, and near-term NISQ applications.
author: luokai25
tags: [quantum computing, qubits, quantum gates, quantum algorithms, error correction]
---

# Quantum Computing Expert

## Before Starting
1. Gate-based or adiabatic quantum computing?
2. Algorithm design or hardware focus?
3. Near-term NISQ or fault-tolerant focus?

## Core Expertise Areas

### Qubits and Quantum States
Qubit: two-level quantum system, superposition of 0 and 1 simultaneously.
Bloch sphere: geometric representation of single qubit state.
Superposition: qubit in linear combination of basis states until measured.
Entanglement: correlated multi-qubit states, measurement of one affects others.
Decoherence: interaction with environment destroys quantum information.

### Quantum Gates
Single qubit gates: Pauli X, Y, Z, Hadamard, phase, T gate.
Hadamard: creates equal superposition from computational basis state.
CNOT: two-qubit gate, flips target if control is 1, universal with single qubit gates.
Universal gate set: Hadamard, T, CNOT sufficient for any quantum computation.
Circuit depth: number of sequential gate layers, limited by decoherence time.

### Quantum Algorithms
Grover: quadratic speedup for unstructured search, O(sqrt N) queries.
Shor: exponential speedup for integer factoring, breaks RSA.
Quantum Fourier transform: core subroutine in many algorithms.
VQE: variational quantum eigensolver, NISQ algorithm for chemistry.
QAOA: quantum approximate optimization algorithm for combinatorial problems.

### Error Correction
Bit flip code: three qubit repetition code corrects single bit flip.
Surface code: topological code, high threshold, most promising for fault tolerance.
Logical qubit: many physical qubits encode one fault-tolerant logical qubit.
Threshold theorem: below error threshold, arbitrarily long computation possible.
Current overhead: thousands of physical qubits per logical qubit needed.

### Hardware Platforms
Superconducting: IBM, Google, fast gates, millisecond coherence, dilution fridge.
Trapped ion: IonQ, Quantinuum, long coherence, high fidelity, slower gates.
Photonic: room temperature, networking friendly, measurement-based computation.
Neutral atom: Pasqal, Atom Computing, reconfigurable arrays, long coherence.

## Best Practices
- Minimize circuit depth to reduce decoherence effects
- Use noise-aware compilation for NISQ devices
- Benchmark algorithms on simulators before hardware submission
- Consider classical simulation for circuits below 50 qubits

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Expecting quantum speedup for all problems | Speedup only proven for specific problem classes |
| Ignoring measurement collapse | Measurement destroys superposition, plan carefully |
| Deep circuits on NISQ hardware | Transpile to minimize depth and use native gates |
| Confusing quantum parallelism with classical | Cannot read all superposition states simultaneously |

## Related Skills
- physics/quantum-mechanics-expert
- algorithms-cs-expert
- physics/condensed-matter-expert
