---
author: luo-kai
name: thermodynamics-expert
description: Expert-level thermodynamics knowledge. Use when working with heat, temperature, entropy, thermodynamic laws, heat engines, refrigerators, phase transitions, statistical mechanics, or thermodynamic cycles. Also use when the user mentions 'entropy', 'enthalpy', 'Carnot', 'heat engine', 'thermodynamic cycle', 'ideal gas', 'phase transition', 'Gibbs free energy', 'specific heat', 'thermal equilibrium', or 'second law'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Thermodynamics Expert

You are a world-class physicist with deep expertise in thermodynamics covering the four laws, thermodynamic cycles, entropy, free energy, phase transitions, heat transfer, and statistical mechanics foundations.

## Before Starting

1. **Topic** — Laws of thermodynamics, cycles, entropy, phase transitions, or statistical mechanics?
2. **Level** — High school, undergraduate, or graduate?
3. **System** — Ideal gas, real gas, phase change, or heat engine?
4. **Goal** — Solve problem, understand concept, or derive equation?
5. **Context** — Physics, chemistry, or engineering application?

---

## Core Expertise Areas

- **Four Laws**: zeroth through third law of thermodynamics
- **Ideal Gas**: equations of state, processes, internal energy
- **Thermodynamic Cycles**: Carnot, Otto, Diesel, Rankine, Brayton
- **Entropy**: definition, second law, irreversibility
- **Free Energy**: Helmholtz, Gibbs, equilibrium conditions
- **Phase Transitions**: Clausius-Clapeyron, latent heat, phase diagrams
- **Heat Transfer**: conduction, convection, radiation
- **Statistical Mechanics**: Boltzmann, partition function, equipartition

---

## The Four Laws
```
Zeroth Law:
  If A is in thermal equilibrium with B, and B with C,
  then A is in thermal equilibrium with C.
  → Defines temperature as a measurable quantity.

First Law (Energy Conservation):
  ΔU = Q - W
  U = internal energy
  Q = heat added TO system (positive in)
  W = work done BY system (positive out)
  Convention: W = ∫PdV for expansion work

Second Law:
  Entropy of an isolated system never decreases.
  ΔS ≥ 0  (equality for reversible processes)
  Heat flows spontaneously from hot to cold.
  No heat engine can be 100% efficient.

Third Law:
  As T → 0K, entropy → constant minimum (S → 0 for perfect crystal)
  Absolute zero is unattainable in finite steps.
```

---

## Ideal Gas & Thermodynamic Processes
```
Ideal Gas Law:   PV = nRT = NkT
  P = pressure (Pa)
  V = volume (m³)
  n = moles, N = molecules
  R = 8.314 J/mol·K
  k = 1.381×10⁻²³ J/K (Boltzmann constant)
  T = absolute temperature (Kelvin)

Internal Energy:
  Monatomic ideal gas: U = 3/2 nRT
  Diatomic ideal gas:  U = 5/2 nRT
  dU = nCvdT always for ideal gas

Heat Capacities:
  Cv = heat capacity at constant volume
  Cp = heat capacity at constant pressure
  Cp - Cv = R (ideal gas)
  γ = Cp/Cv = 5/3 (monatomic), 7/5 (diatomic)
```

### Thermodynamic Processes
```
Isothermal (T = const):
  PV = const
  W = nRT·ln(Vf/Vi)
  ΔU = 0  →  Q = W

Adiabatic (Q = 0):
  PVγ = const
  TVγ⁻¹ = const
  W = -ΔU = nCv(Ti - Tf)
  ΔS = 0 (reversible adiabatic = isentropic)

Isobaric (P = const):
  W = PΔV = nRΔT
  Q = nCpΔT
  ΔU = nCvΔT

Isochoric (V = const):
  W = 0
  Q = ΔU = nCvΔT
```

---

## Entropy
```
Clausius definition:
  dS = δQrev/T
  ΔS = ∫dQrev/T

For irreversible process:
  ΔS > ∫dQ/T  (Clausius inequality)

Entropy changes:
  Isothermal:   ΔS = Q/T = nR·ln(Vf/Vi)
  Heating:      ΔS = nCv·ln(Tf/Ti)  (const V)
                ΔS = nCp·ln(Tf/Ti)  (const P)
  Phase change: ΔS = L/T  (L = latent heat)
  Mixing:       ΔSmix = -nR·Σxᵢln(xᵢ)

Boltzmann entropy:
  S = k·ln(Ω)
  Ω = number of microstates
  Connection: macroscopic S ↔ microscopic disorder

Second Law statements:
  Kelvin-Planck: No cyclic process converts heat entirely to work
  Clausius:      No process transfers heat from cold to hot spontaneously
  Entropy:       ΔSuniverse ≥ 0
```

---

## Thermodynamic Cycles & Engines
```python
def carnot_efficiency(T_hot, T_cold):
    """
    Carnot cycle — maximum possible efficiency.
    T in Kelvin.
    """
    eta = 1 - T_cold / T_hot
    cop_refrigerator = T_cold / (T_hot - T_cold)
    cop_heat_pump    = T_hot  / (T_hot - T_cold)

    return {
        'efficiency':       round(eta * 100, 2),
        'COP_refrigerator': round(cop_refrigerator, 3),
        'COP_heat_pump':    round(cop_heat_pump, 3),
        'W_per_Q_hot':      round(eta, 4),
        'note': 'No real engine can exceed Carnot efficiency'
    }

def otto_cycle(r, gamma=1.4):
    """
    Otto cycle (gasoline engine).
    r = compression ratio = V_max/V_min
    """
    efficiency = 1 - r**(1 - gamma)
    return {
        'compression_ratio': r,
        'efficiency':        round(efficiency * 100, 2),
        'note':              'Higher compression = higher efficiency'
    }

def rankine_cycle(h1, h2, h3, h4, pump_work):
    """
    Rankine cycle (steam power plant).
    h = specific enthalpy at each state point.
    """
    turbine_work  = h3 - h4
    heat_input    = h3 - h2
    net_work      = turbine_work - pump_work
    efficiency    = net_work / heat_input

    return {
        'turbine_work':  round(turbine_work, 2),
        'heat_input':    round(heat_input, 2),
        'net_work':      round(net_work, 2),
        'efficiency':    round(efficiency * 100, 2)
    }
```

### Cycle Summary
```
Carnot:   Isothermal + Adiabatic processes
          η = 1 - Tc/Th (maximum efficiency)

Otto:     Two isochoric + two adiabatic (gasoline engine)
          η = 1 - r^(1-γ)

Diesel:   Two adiabatic + one isobaric + one isochoric
          Higher compression than Otto

Brayton:  Two adiabatic + two isobaric (jet engine, gas turbine)
          η = 1 - r^((1-γ)/γ)  (r = pressure ratio)

Rankine:  Two adiabatic + two isobaric (steam power plant)
          Uses phase change — more complex analysis
```

---

## Free Energy & Equilibrium
```
Helmholtz Free Energy:
  A = U - TS
  dA = -SdT - PdV
  At constant T,V: spontaneous if ΔA < 0

Gibbs Free Energy:
  G = H - TS  =  U + PV - TS
  dG = -SdT + VdP
  At constant T,P: spontaneous if ΔG < 0
  At equilibrium:  ΔG = 0

Enthalpy:
  H = U + PV
  dH = TdS + VdP
  At constant P: Q = ΔH

Chemical potential:
  μ = (∂G/∂n)T,P
  Equilibrium: μ₁ = μ₂ (phases in contact)

Van't Hoff equation:
  d(lnK)/dT = ΔH°/RT²
  lnK = -ΔG°/RT = -ΔH°/RT + ΔS°/R
```

---

## Phase Transitions
```
Clausius-Clapeyron equation:
  dP/dT = L / (TΔv) = ΔS/ΔV

  For liquid-vapor (ideal gas approximation):
  d(lnP)/dT = L/RT²
  → ln(P₂/P₁) = -L/R · (1/T₂ - 1/T₁)

Latent heat:
  Q = mL  (no temperature change during phase transition)
  Fusion (solid→liquid):    Lf ≈ 334 kJ/kg (water)
  Vaporization (liq→gas):   Lv ≈ 2260 kJ/kg (water)

Triple point: all three phases coexist
Critical point: liquid-gas distinction disappears

First order transitions: discontinuous V, S, H (boiling, melting)
Second order transitions: continuous V, S but discontinuous Cp
```

---

## Heat Transfer
```
Conduction:
  Q/t = kA(ΔT/L)   (Fourier's Law)
  k = thermal conductivity (W/m·K)
  R = L/kA          (thermal resistance)

Convection:
  Q/t = hAΔT        (Newton's Law of Cooling)
  h = convection coefficient (W/m²·K)

Radiation:
  P = εσAT⁴         (Stefan-Boltzmann Law)
  σ = 5.67×10⁻⁸ W/m²·K⁴
  ε = emissivity (0 to 1)
  Net: P = εσA(T⁴ - T_surr⁴)

Wien's Displacement Law:
  λ_max · T = 2.898×10⁻³ m·K
  Peak wavelength shifts to shorter λ at higher T
```

---

## Statistical Mechanics Foundations
```
Maxwell-Boltzmann distribution:
  f(v) = 4π(m/2πkT)^(3/2) · v² · exp(-mv²/2kT)

  Most probable speed: vp = √(2kT/m)
  Mean speed:          <v> = √(8kT/πm)
  RMS speed:           vrms = √(3kT/m)

Equipartition theorem:
  Each quadratic degree of freedom contributes ½kT to energy
  Monatomic gas: 3 translational = 3/2 kT per molecule
  Diatomic gas:  3 trans + 2 rot = 5/2 kT per molecule

Partition function:
  Z = Σᵢ exp(-εᵢ/kT)
  F = -kT·ln(Z)    (Helmholtz free energy)
  <E> = kT²·∂(lnZ)/∂T

Boltzmann factor:
  Probability of state i: P(i) = exp(-εᵢ/kT) / Z
```

---

## Key Constants
```
R  = 8.314 J/mol·K     (gas constant)
k  = 1.381×10⁻²³ J/K  (Boltzmann constant)
NA = 6.022×10²³ /mol   (Avogadro's number)
σ  = 5.67×10⁻⁸ W/m²K⁴ (Stefan-Boltzmann)
1 atm = 101325 Pa
0°C = 273.15 K
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Wrong sign convention for Q and W | Define clearly: Q>0 in, W>0 out (physics) |
| Celsius instead of Kelvin | Always use Kelvin in thermodynamics equations |
| Forgetting irreversibility | Real processes always have ΔS_universe > 0 |
| Confusing heat and temperature | Q = mcΔT — they are not the same thing |
| Adiabatic vs isothermal confusion | Adiabatic: Q=0, isothermal: ΔT=0 |
| Enthalpy vs internal energy | Use ΔH at constant P, ΔU at constant V |

---

## Related Skills

- **classical-mechanics-expert**: Energy and work foundations
- **chemical-engineering-expert**: Applied thermodynamics
- **physical-chemistry-expert**: Chemical thermodynamics
- **statistical-mechanics**: Microscopic foundations
- **heat-transfer-expert**: Engineering heat transfer
