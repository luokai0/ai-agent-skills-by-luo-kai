---
author: luo-kai
name: quantum-mechanics-expert
description: Expert-level quantum mechanics knowledge. Use when working with wave functions, Schrodinger equation, quantum states, operators, uncertainty principle, quantum tunneling, spin, angular momentum, perturbation theory, or quantum entanglement. Also use when the user mentions 'wave function', 'Schrodinger', 'Heisenberg', 'quantum state', 'eigenvalue', 'superposition', 'tunneling', 'spin', 'Hilbert space', 'Dirac notation', 'commutator', or 'quantum measurement'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Quantum Mechanics Expert

You are a world-class physicist with deep expertise in quantum mechanics covering wave mechanics, matrix mechanics, Dirac notation, quantum operators, exactly solvable systems, angular momentum, spin, perturbation theory, and the foundations of quantum theory.

## Before Starting

1. **Topic** — Wave functions, operators, specific systems, angular momentum, or perturbation theory?
2. **Level** — Introductory, undergraduate, or graduate?
3. **Formulation** — Wave mechanics, matrix mechanics, or Dirac notation?
4. **Goal** — Solve problem, understand concept, or derive result?
5. **System** — Particle in box, harmonic oscillator, hydrogen atom, or spin?

---

## Core Expertise Areas

- **Foundations**: postulates, wave function, Born interpretation
- **Schrodinger Equation**: time-dependent and independent forms
- **Operators & Observables**: Hermitian operators, eigenvalues, commutators
- **Exactly Solvable Systems**: infinite well, harmonic oscillator, hydrogen atom
- **Uncertainty Principle**: Heisenberg, generalized form
- **Angular Momentum**: orbital, spin, addition of angular momenta
- **Approximation Methods**: perturbation theory, variational method, WKB
- **Quantum Entanglement**: EPR, Bell's theorem, density matrix

---

## Postulates of Quantum Mechanics
```
1. STATE:
   A quantum system is completely described by a
   wave function ψ(r,t) or state vector |ψ⟩ in Hilbert space.

2. OBSERVABLES:
   Every observable A corresponds to a Hermitian operator Â.
   Hermitian: Â = Â†  →  real eigenvalues, orthogonal eigenstates.

3. MEASUREMENT:
   Measuring A gives eigenvalue aₙ with probability |⟨aₙ|ψ⟩|².
   After measurement: state collapses to eigenstate |aₙ⟩.

4. EXPECTATION VALUE:
   ⟨A⟩ = ⟨ψ|Â|ψ⟩ = ∫ψ* Â ψ dV

5. TIME EVOLUTION:
   iℏ ∂|ψ⟩/∂t = Ĥ|ψ⟩  (Schrodinger equation)
```

---

## Schrodinger Equation
```
Time-Dependent:
  iℏ ∂ψ/∂t = Ĥψ
  Ĥ = -ℏ²/2m ∇² + V(r,t)

Time-Independent (stationary states):
  Ĥψ = Eψ
  -ℏ²/2m d²ψ/dx² + V(x)ψ = Eψ

General solution:
  Ψ(x,t) = Σcₙψₙ(x)e^(-iEₙt/ℏ)

Probability density:    ρ = |ψ|² = ψ*ψ
Normalization:          ∫|ψ|² dV = 1
Probability current:    J = (ℏ/2mi)(ψ*∇ψ - ψ∇ψ*)
Continuity:             ∂ρ/∂t + ∇·J = 0
```

---

## Dirac Notation
```
State vector:      |ψ⟩  (ket)
Dual vector:       ⟨ψ|  (bra)
Inner product:     ⟨φ|ψ⟩ = ∫φ*ψ dV
Outer product:     |ψ⟩⟨φ|  (operator)
Completeness:      Σₙ|n⟩⟨n| = Î
Orthonormality:    ⟨m|n⟩ = δₘₙ

Operator in basis: Aₘₙ = ⟨m|Â|n⟩  (matrix element)
Expectation:       ⟨A⟩ = ⟨ψ|Â|ψ⟩

Position basis:    ⟨x|ψ⟩ = ψ(x)
Momentum basis:    ⟨p|ψ⟩ = φ(p)

Momentum operator: p̂ = -iℏ∇  (position basis)
Position operator: x̂ = iℏ∂/∂p (momentum basis)
```

---

## Operators & Commutators
```
Commutator:     [Â,B̂] = ÂB̂ - B̂Â

Canonical commutation relations:
  [x̂,p̂] = iℏ
  [xᵢ,pⱼ] = iℏδᵢⱼ
  [xᵢ,xⱼ] = 0
  [pᵢ,pⱼ] = 0

Angular momentum:
  [Lx,Ly] = iℏLz  (cyclic)
  [L²,Lᵢ] = 0

Heisenberg uncertainty:
  ΔAΔb ≥ ½|⟨[Â,B̂]⟩|
  ΔxΔpx ≥ ℏ/2
  ΔEΔt ≥ ℏ/2

Ehrenfest theorem:
  d⟨x⟩/dt = ⟨p⟩/m
  d⟨p⟩/dt = -⟨∂V/∂x⟩
  (quantum expectation values obey classical equations)
```

---

## Exactly Solvable Systems

### Infinite Square Well
```
V(x) = 0 for 0 < x < L, ∞ elsewhere

Solutions:
  ψₙ(x) = √(2/L) sin(nπx/L)   n = 1,2,3,...
  Eₙ = n²π²ℏ²/2mL²  =  n²E₁
  E₁ = π²ℏ²/2mL²  (zero-point energy)

Properties:
  Quantized energy — discrete levels
  Zero-point energy: cannot have E = 0
  Wavefunctions: standing waves
  Orthonormal: ⟨m|n⟩ = δₘₙ
```

### Quantum Harmonic Oscillator
```
V(x) = ½mω²x²

Energy levels: Eₙ = (n + ½)ℏω   n = 0,1,2,...
Ground state:  E₀ = ½ℏω  (zero-point energy)

Ladder operators:
  â  = √(mω/2ℏ)(x̂ + ip̂/mω)  (lowering)
  â† = √(mω/2ℏ)(x̂ - ip̂/mω)  (raising)
  [â,â†] = 1
  Ĥ = ℏω(â†â + ½) = ℏω(N̂ + ½)

Matrix elements:
  â|n⟩  = √n |n-1⟩
  â†|n⟩ = √(n+1)|n+1⟩
  x̂ = √(ℏ/2mω)(â + â†)
  p̂ = i√(mωℏ/2)(â† - â)

Ground state wavefunction:
  ψ₀(x) = (mω/πℏ)^(1/4) exp(-mωx²/2ℏ)
```

### Hydrogen Atom
```
V(r) = -e²/4πε₀r  (Coulomb potential)

Energy levels:
  Eₙ = -13.6 eV/n²   n = 1,2,3,...
  E₁ = -13.6 eV (ground state)

Quantum numbers:
  n = 1,2,3,...         (principal)
  l = 0,1,...,n-1       (orbital angular momentum)
  m = -l,-l+1,...,l     (magnetic)
  s = ±½                (spin)

Wave functions:
  ψₙₗₘ(r,θ,φ) = Rₙₗ(r) · Yₗᵐ(θ,φ)

Bohr radius: a₀ = 4πε₀ℏ²/me² = 0.529 Å
Degeneracy: n² (without spin), 2n² (with spin)

Selection rules:
  Δl = ±1
  Δm = 0,±1
  Δn = any
```

---

## Angular Momentum
```
Orbital angular momentum:
  L = r×p
  L² = Lx² + Ly² + Lz²
  Lz = mℏ    m = -l,...,l
  L² = l(l+1)ℏ²

Spin angular momentum:
  Spin-½ particles (electrons, protons, neutrons)
  Sz = mₛℏ   mₛ = ±½
  S² = s(s+1)ℏ² = 3ℏ²/4

Pauli matrices (spin-½):
  σx = [[0,1],[1,0]]
  σy = [[0,-i],[i,0]]
  σz = [[1,0],[0,-1]]
  S = ℏ/2 · σ

Spin states:
  |↑⟩ = |+½⟩ = [1,0]ᵀ  (spin up)
  |↓⟩ = |-½⟩ = [0,1]ᵀ  (spin down)

Addition of angular momenta:
  J = L + S
  j = |l-s|,...,l+s  (Clebsch-Gordan)
  |j,m⟩ = Σ C(l,m₁;s,m₂|j,m) |l,m₁⟩|s,m₂⟩
```

---

## Quantum Tunneling
```
Tunneling through rectangular barrier (E < V₀):
  Transmission: T ≈ exp(-2κL)
  κ = √(2m(V₀-E))/ℏ
  L = barrier width

WKB approximation:
  T ≈ exp(-2∫√(2m(V(x)-E))/ℏ dx)

Applications:
  Alpha decay: nucleus tunnels through Coulomb barrier
  Scanning tunneling microscope (STM)
  Tunnel diodes
  Nuclear fusion in stars
```

---

## Perturbation Theory
```
H = H₀ + λH'  (λ small perturbation)

First-order energy correction:
  Eₙ¹ = ⟨n⁰|H'|n⁰⟩

First-order state correction:
  |n¹⟩ = Σₖ≠ₙ [⟨k⁰|H'|n⁰⟩/(Eₙ⁰-Eₖ⁰)] |k⁰⟩

Second-order energy correction:
  Eₙ² = Σₖ≠ₙ |⟨k⁰|H'|n⁰⟩|²/(Eₙ⁰-Eₖ⁰)

Degenerate perturbation theory:
  Must diagonalize H' in degenerate subspace first

Time-dependent perturbation theory:
  Fermi's Golden Rule:
  Γᵢ→f = (2π/ℏ)|⟨f|H'|i⟩|² ρ(Ef)
  (transition rate to continuum of final states)
```

---

## Quantum Entanglement & Measurement
```
Entangled state (Bell state):
  |Φ+⟩ = (1/√2)(|↑↑⟩ + |↓↓⟩)
  Cannot be written as |ψ₁⟩⊗|ψ₂⟩

EPR paradox:
  Einstein-Podolsky-Rosen: QM seems non-local
  Measuring one particle instantly affects other

Bell's theorem:
  No local hidden variable theory can reproduce QM predictions
  Bell inequality: |⟨AB⟩+⟨AB'⟩+⟨A'B⟩-⟨A'B'⟩| ≤ 2 (classical)
  QM prediction: can reach 2√2 ≈ 2.83 (violation)
  Experiments confirm QM — nature is non-local

Density matrix:
  Pure state:  ρ = |ψ⟩⟨ψ|,  Tr(ρ²) = 1
  Mixed state: ρ = Σpᵢ|ψᵢ⟩⟨ψᵢ|, Tr(ρ²) < 1
  ⟨A⟩ = Tr(ρÂ)
```

---

## Key Constants
```
ℏ = h/2π = 1.055×10⁻³⁴ J·s  (reduced Planck constant)
h  = 6.626×10⁻³⁴ J·s
me = 9.109×10⁻³¹ kg
e  = 1.602×10⁻¹⁹ C
a₀ = 0.529 Å = 5.29×10⁻¹¹ m  (Bohr radius)
Ry = 13.6 eV  (Rydberg energy)
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Confusing ψ and ψ* | Probability = ψ*ψ = |ψ|² always positive |
| Forgetting normalization | Always check ∫|ψ|²dx = 1 |
| Operator order matters | [Â,B̂] ≠ 0 in general — order is crucial |
| Classical intuition | Quantum particles have no definite position AND momentum |
| Measuring destroys superposition | After measurement state collapses to eigenstate |
| Zero-point energy confusion | Ground state E₀ ≠ 0 for oscillator and well |

---

## Related Skills

- **classical-mechanics-expert**: Classical limit of QM
- **electromagnetism-expert**: QED foundation
- **special-relativity-expert**: Relativistic QM, Dirac equation
- **particle-physics-expert**: QFT builds on QM
- **quantum-computing-expert**: Applied quantum mechanics
- **atomic-physics-expert**: Many-electron atoms
