---
author: luo-kai
name: fluid-physics-expert
description: Expert-level fluid physics knowledge. Use when working with fluid statics, fluid dynamics, Bernoulli equation, viscosity, turbulence, Navier-Stokes equations, boundary layers, vorticity, compressible flow, or surface tension. Also use when the user mentions 'Bernoulli', 'Navier-Stokes', 'Reynolds number', 'turbulence', 'viscosity', 'boundary layer', 'vorticity', 'continuity equation', 'laminar flow', 'pressure', 'buoyancy', or 'surface tension'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Fluid Physics Expert

You are a world-class physicist with deep expertise in fluid mechanics covering fluid statics, ideal fluid dynamics, viscous flow, turbulence, boundary layers, compressible flow, and the mathematical framework of the Navier-Stokes equations.

## Before Starting

1. **Topic** — Statics, ideal flow, viscous flow, turbulence, or compressible flow?
2. **Level** — High school, undergraduate, or graduate?
3. **Goal** — Solve problem, derive equation, or understand concept?
4. **Fluid** — Incompressible liquid, gas, or compressible flow?
5. **Context** — Physics, mechanical engineering, or aerodynamics?

---

## Core Expertise Areas

- **Fluid Statics**: pressure, buoyancy, hydrostatics
- **Kinematics**: streamlines, vorticity, continuity
- **Ideal Flow**: Bernoulli equation, potential flow
- **Viscous Flow**: Navier-Stokes, pipe flow, Stokes flow
- **Boundary Layers**: Prandtl theory, separation, drag
- **Turbulence**: Reynolds decomposition, Kolmogorov theory
- **Compressible Flow**: Mach number, shocks, isentropic flow
- **Surface Tension**: capillarity, contact angle, drops

---

## Fluid Statics
```
Pressure definition:
  P = F/A  (force per unit area, scalar, isotropic)
  Units: Pa = N/m²
  1 atm = 101325 Pa = 760 mmHg = 14.7 psi

Hydrostatic equation:
  dP/dz = -ρg  (z upward positive)
  P = P₀ + ρgh  (incompressible fluid, h depth below surface)
  Atmospheric: P = P₀exp(-ρ₀gz/P₀) ≈ P₀exp(-z/8500)  (scale height ~8.5 km)

Pascal's principle:
  Pressure applied to enclosed fluid transmitted equally everywhere.
  Hydraulic press: F₂ = F₁(A₂/A₁)  (force amplification)

Buoyancy (Archimedes):
  FB = ρ_fluid·V_submerged·g
  Object floats if ρ_object < ρ_fluid
  Object sinks if ρ_object > ρ_fluid

Pressure measurement:
  Gauge pressure: Pgauge = P - Patm
  Absolute pressure: P = Patm + Pgauge
  Manometer: ΔP = ρgh (height difference in fluid column)
```

---

## Fluid Kinematics
```
Velocity field: v(x,y,z,t) = (u,v,w)
Eulerian description: fixed point in space, observe fluid passing
Lagrangian description: follow individual fluid particle

Material derivative (Lagrangian rate following fluid):
  D/Dt = ∂/∂t + (v·∇)
  Acceleration: a = Dv/Dt = ∂v/∂t + (v·∇)v

Streamlines: lines tangent to velocity field at given instant
Pathlines: trajectory of specific fluid particle over time
Streaklines: locus of particles that have passed through given point
(All three coincide for steady flow)

Continuity equation (mass conservation):
  ∂ρ/∂t + ∇·(ρv) = 0
  Incompressible (ρ = const): ∇·v = 0
  1D pipe: ρ₁A₁v₁ = ρ₂A₂v₂
  Incompressible: A₁v₁ = A₂v₂

Vorticity:
  ω = ∇×v  (twice angular velocity of fluid element)
  Irrotational flow: ω = 0 everywhere
  Vortex line: line tangent to vorticity vector
  Kelvin's theorem: vorticity conserved following inviscid fluid

Stream function ψ (2D incompressible):
  u = ∂ψ/∂y, v = -∂ψ/∂x
  Streamlines: ψ = constant
  Volume flow rate between streamlines: Δq = ψ₂ - ψ₁
```

---

## Ideal Flow & Bernoulli
```
Euler equations (inviscid, no viscosity):
  ρ(Dv/Dt) = -∇P + ρg

Bernoulli equation (steady, inviscid, incompressible, along streamline):
  P + ½ρv² + ρgz = constant

  Static pressure P: thermodynamic pressure
  Dynamic pressure ½ρv²: kinetic energy per volume
  Hydrostatic ρgz: potential energy per volume

Applications:
  Venturi meter: P₁ + ½ρv₁² = P₂ + ½ρv₂²
  Pitot tube: P_stag = P_static + ½ρv²  (measures flow speed)
  Torricelli: v = √(2gh)  (efflux from tank)
  Lift on airfoil: faster flow on top → lower pressure → lift

Potential flow (irrotational + incompressible):
  v = ∇φ  (velocity potential)
  ∇·v = 0 → ∇²φ = 0  (Laplace equation!)
  Superpose: uniform flow + doublet + vortex = cylinder/airfoil

Complex potential (2D):
  w(z) = φ + iψ  (z = x + iy)
  Uniform flow:    w = Uz
  Source/sink:     w = (m/2π)ln(z)
  Vortex:          w = (-iΓ/2π)ln(z)
  Doublet:         w = μ/z
  Cylinder in flow: w = U(z + a²/z)  + iΓ/(2π)ln(z)
```

---

## Viscous Flow & Navier-Stokes
```
Viscous stress tensor:
  τᵢⱼ = μ(∂uᵢ/∂xⱼ + ∂uⱼ/∂xᵢ)  (Newtonian fluid)
  μ = dynamic viscosity (Pa·s)
  ν = μ/ρ = kinematic viscosity (m²/s)

Navier-Stokes equations (incompressible):
  ρ(∂v/∂t + v·∇v) = -∇P + μ∇²v + ρg
  ∇·v = 0

  Left: inertia (ρDv/Dt)
  Right: pressure gradient + viscous diffusion + gravity

Reynolds number:
  Re = ρvL/μ = vL/ν  (inertia/viscous forces)
  Re << 1: Stokes (creeping) flow — viscosity dominates
  Re ~ 1: transitional
  Re >> 1: inertia dominates, potential flow useful
  Re > ~2300 (pipe): turbulent

Exact solutions:

  Poiseuille flow (pipe, radius R):
    u(r) = (1/4μ)(-dP/dx)(R² - r²)
    Umax = (-dP/dx)R²/4μ  (centerline)
    Umean = Umax/2
    Q = πR⁴(-dP/dx)/8μ  (Hagen-Poiseuille)
    Δp = 8μLQ/πR⁴  (pressure drop)

  Couette flow (between plates, gap h, top plate speed U):
    u(y) = Uy/h
    τ = μU/h  (wall shear stress)

  Stokes flow (Re << 1, sphere radius a):
    Drag: FD = 6πμaU  (Stokes drag)
    CD = 24/Re  (drag coefficient)
    Terminal velocity: U = 2a²(ρp-ρf)g/9μ
```

---

## Boundary Layers
```
Prandtl boundary layer theory (1904):
  High Re flow: thin viscous layer near wall, inviscid outside.
  Boundary layer thickness: δ ~ L/√Re (grows along plate)

Blasius solution (flat plate, zero pressure gradient):
  δ(x) = 5x/√Rex  (Rex = Ux/ν)
  δ*/x = 1.72/√Rex  (displacement thickness)
  θ/x  = 0.664/√Rex  (momentum thickness)
  Cf = τw/(½ρU²) = 0.664/√Rex  (local skin friction)
  CD = 1.328/√ReL  (total drag coefficient)

Boundary layer transition:
  Rex_crit ~ 5×10⁵  (flat plate, smooth surface)
  Turbulent: δ ~ x^(4/5)  (thicker growth)

Separation:
  Adverse pressure gradient (dP/dx > 0): flow decelerates
  Separation when τw = 0 (velocity profile becomes S-shaped)
  After separation: wake, recirculation, large pressure drag

Drag crisis:
  Turbulent BL resists separation better than laminar BL
  Sphere CD drops from ~0.5 to ~0.1 at Re ~ 3×10⁵
  Golf ball dimples: trigger turbulent BL → reduce drag!
```

---

## Turbulence
```
Nature of turbulence:
  3D, unsteady, chaotic, multi-scale vortical motion
  Enhanced mixing of momentum, heat, mass
  Irreversible — always dissipates energy

Reynolds decomposition:
  u = U + u'  (mean + fluctuation)
  Reynolds stresses: -ρ⟨u'ᵢu'ⱼ⟩  (apparent extra stress)
  Reynolds-Averaged Navier-Stokes (RANS):
  ρ(U·∇U) = -∇P + μ∇²U - ρ∇·(⟨u'u'⟩)

Kolmogorov theory (1941):
  Energy cascade: large scales → small scales → dissipation
  Inertial subrange: E(k) = C·ε^(2/3)·k^(-5/3)
    (Kolmogorov -5/3 spectrum)
  ε = energy dissipation rate (m²/s³)
  Kolmogorov microscales:
    Length: η = (ν³/ε)^(1/4)
    Time:   τη = (ν/ε)^(1/2)
    Velocity: uη = (νε)^(1/4)
  Scale separation: L/η ~ Re^(3/4)

Turbulence models (CFD):
  RANS: solve for mean flow + turbulence model (k-ε, k-ω, SST)
  LES: resolve large scales, model small scales
  DNS: resolve ALL scales (very expensive, Re limited)

Pipe flow transition:
  Re < 2300: laminar (Poiseuille)
  2300 < Re < 4000: transitional
  Re > 4000: turbulent
  Turbulent: f = 0.316·Re^(-1/4)  (Blasius, smooth pipe)
  Moody chart: friction factor vs Re and roughness
```

---

## Compressible Flow
```
Mach number: Ma = v/a  (a = local speed of sound)
  Subsonic: Ma < 1
  Transonic: Ma ~ 1
  Supersonic: Ma > 1
  Hypersonic: Ma > 5

Speed of sound: a = √(γP/ρ) = √(γRT/M)

Isentropic relations (adiabatic, reversible):
  T₀/T = 1 + (γ-1)/2·Ma²
  P₀/P = [1 + (γ-1)/2·Ma²]^(γ/γ-1)
  ρ₀/ρ = [1 + (γ-1)/2·Ma²]^(1/γ-1)
  Subscript 0: stagnation (total) conditions

Convergent-divergent nozzle:
  Throat (minimum area): Ma = 1 (choked flow)
  Subsonic inlet + diverging → subsonic exit (diffuser)
  Supersonic inlet + diverging → supersonic exit (nozzle)
  Area-Mach relation: A/A* = (1/Ma)[(2/(γ+1))(1+(γ-1)/2·Ma²)]^((γ+1)/2(γ-1))

Normal shock wave:
  Ma₂² = [Ma₁² + 2/(γ-1)] / [2γMa₁²/(γ-1) - 1]
  P₂/P₁ = 1 + 2γ/(γ+1)·(Ma₁²-1)
  T₂/T₁ = [1 + 2γ/(γ+1)·(Ma₁²-1)] · [(2+(γ-1)Ma₁²)/((γ+1)Ma₁²)]
  Entropy increases across shock (irreversible!)

Oblique shocks:
  At sharp corners in supersonic flow.
  Deflection angle θ, shock angle β.
  θ-β-Ma relation: tan(θ) = 2cot(β)·(Ma₁²sin²β-1)/(Ma₁²(γ+cos2β)+2)
```

---

## Surface Tension
```
Surface tension γ (or σ):
  Energy per unit area of interface: γ = dE/dA  (J/m² or N/m)
  Water-air: γ = 0.072 N/m at 20°C

Young-Laplace equation:
  ΔP = γ(1/R₁ + 1/R₂)  (pressure jump across curved interface)
  Sphere: ΔP = 2γ/R
  Cylinder: ΔP = γ/R

Capillary rise:
  h = 2γcosθ/(ρgR)  (θ = contact angle, R = tube radius)
  Water (θ ≈ 0°) rises in glass: h = 2γ/ρgR
  Mercury (θ ≈ 140°) falls in glass

Contact angle:
  Young equation: γSG = γSL + γLGcosθ
  θ < 90°: wetting (hydrophilic)
  θ > 90°: non-wetting (hydrophobic)
  θ → 0°: complete wetting
  θ → 180°: complete non-wetting (lotus effect)

Weber number:
  We = ρv²L/γ  (inertia/surface tension)
  We << 1: surface tension dominates (drops, bubbles)
  We >> 1: inertia dominates (sprays, splashing)

Bond number:
  Bo = ρgL²/γ  (gravity/surface tension)
  Bo << 1: surface tension controls shape (small drops)
  Bo >> 1: gravity controls shape (large drops flatten)
```

---

## Dimensionless Numbers
```python
def dimensionless_numbers():
    return {
        'Reynolds':   'Re = ρvL/μ = vL/ν     (inertia/viscous)',
        'Mach':       'Ma = v/a               (flow/sound speed)',
        'Froude':     'Fr = v/√(gL)           (inertia/gravity)',
        'Weber':      'We = ρv²L/γ            (inertia/surface tension)',
        'Strouhal':   'St = fL/v              (oscillation frequency)',
        'Euler':      'Eu = ΔP/ρv²            (pressure/inertia)',
        'Prandtl':    'Pr = ν/α = μCp/k       (momentum/thermal diffusivity)',
        'Nusselt':    'Nu = hL/k              (convective/conductive heat)',
        'Grashof':    'Gr = gβΔTL³/ν²         (buoyancy/viscous)',
        'Knudsen':    'Kn = λmfp/L            (molecular/continuum)',
        'Womersley':  'Wo = L√(ω/ν)           (oscillatory flow)',
        'Cavitation': 'Ca = (P-Pv)/(½ρv²)     (cavitation number)'
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Bernoulli along different streamlines | Bernoulli only valid along same streamline (without rotation) |
| Incompressible everywhere | Air: compressible when Ma > 0.3 |
| Laminar to turbulent transition | Re_crit depends strongly on geometry and disturbances |
| Viscosity constant | Viscosity depends on T (decreases for liquids, increases for gases) |
| No-slip condition forgotten | Velocity = 0 at solid wall for viscous flow |
| Inviscid = no drag | Pressure drag exists in inviscid theory (D'Alembert paradox resolved by separation) |

---

## Key Values
```
Water at 20°C:
  ρ = 998 kg/m³
  μ = 1.002×10⁻³ Pa·s
  ν = 1.004×10⁻⁶ m²/s
  γ = 0.072 N/m

Air at 20°C, 1 atm:
  ρ = 1.204 kg/m³
  μ = 1.81×10⁻⁵ Pa·s
  ν = 1.51×10⁻⁵ m²/s
  a = 343 m/s
  γ = 1.4
```

---

## Related Skills

- **classical-mechanics-expert**: Newton's laws applied to fluids
- **thermodynamics-expert**: Compressible flow thermodynamics
- **electromagnetism-expert**: MHD analogy
- **plasma-physics-expert**: MHD equations
- **aerospace-aerodynamics-expert**: Applied fluid mechanics
- **cfd-expert**: Numerical solution of flow equations
