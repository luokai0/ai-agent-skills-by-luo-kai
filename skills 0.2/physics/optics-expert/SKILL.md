---
name: optics-expert
description: Expert-level optics knowledge. Use when working with geometric optics, wave optics, interference, diffraction, polarization, lasers, fiber optics, optical instruments, or photonics. Also use when the user mentions 'reflection', 'refraction', 'Snell law', 'lens', 'mirror', 'interference', 'diffraction', 'polarization', 'laser', 'fiber optic', 'holography', 'aberration', or 'optical instrument'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Optics Expert

You are a world-class physicist with deep expertise in optics covering geometric optics, wave optics, interference, diffraction, polarization, lasers, nonlinear optics, fiber optics, and optical instruments.

## Before Starting

1. **Topic** — Geometric optics, wave optics, interference, diffraction, or lasers?
2. **Level** — High school, undergraduate, or graduate?
3. **Goal** — Solve problem, design system, or understand concept?
4. **Context** — Physics, engineering, or medical optics?
5. **System** — Lenses, mirrors, interferometers, or lasers?

---

## Core Expertise Areas

- **Geometric Optics**: reflection, refraction, lenses, mirrors, ray tracing
- **Wave Optics**: Huygens principle, interference, coherence
- **Diffraction**: single slit, double slit, gratings, resolution limits
- **Polarization**: linear, circular, Brewster's angle, wave plates
- **Lasers**: stimulated emission, cavity, modes, beam properties
- **Fiber Optics**: total internal reflection, modes, dispersion
- **Optical Instruments**: microscope, telescope, camera, spectrometer
- **Nonlinear Optics**: harmonic generation, Kerr effect, parametric processes

---

## Geometric Optics

### Reflection & Refraction
```
Law of Reflection:
  θᵢ = θᵣ  (angle of incidence = angle of reflection)
  Both measured from normal to surface.

Snell's Law (Refraction):
  n₁sinθ₁ = n₂sinθ₂
  n = c/v = refractive index (n ≥ 1)

Common refractive indices:
  Vacuum/air: n = 1.000
  Water:      n = 1.333
  Glass:      n = 1.5
  Diamond:    n = 2.42

Total Internal Reflection:
  Occurs when light goes from dense to less dense medium.
  Critical angle: sinθc = n₂/n₁  (n₁ > n₂)
  θᵢ > θc → total reflection, no transmitted ray.

Dispersion:
  n = n(λ) — different wavelengths refract differently.
  Prism separates white light into spectrum.
  Cauchy equation: n(λ) = A + B/λ²
```

### Mirrors
```
Spherical mirror equation:
  1/f = 1/do + 1/di
  f = R/2  (focal length = half radius of curvature)
  M = -di/do  (magnification, negative = inverted)

Sign conventions:
  do > 0: object in front of mirror
  di > 0: real image (in front), di < 0: virtual image (behind)
  f > 0: concave mirror, f < 0: convex mirror

Flat mirror: f = ∞ → di = -do (virtual, upright, same size)
Concave: converging — real images when do > f
Convex: diverging — always virtual, upright, reduced image
```

### Lenses & Ray Tracing
```
Thin lens equation:
  1/f = 1/do + 1/di
  M = -di/do = hi/ho

Lensmaker's equation:
  1/f = (n-1)[1/R₁ - 1/R₂]
  R > 0: center of curvature on transmission side
  R < 0: center of curvature on incidence side

Lens types:
  Converging (convex): f > 0
  Diverging (concave): f < 0

Three principal rays for ray tracing:
  1. Parallel to axis → passes through focal point F'
  2. Through focal point F → emerges parallel to axis
  3. Through optical center → undeviated

Power: P = 1/f  (diopters, f in meters)
Combined lenses: 1/f_total = 1/f₁ + 1/f₂ - d/(f₁f₂)
```

---

## Wave Optics

### Huygens Principle & Wavefronts
```
Every point on a wavefront acts as a source of secondary wavelets.
New wavefront = envelope of all secondary wavelets.
Explains reflection, refraction, diffraction.

Plane wave: E = E₀cos(kx - ωt)
Spherical wave: E = (E₀/r)cos(kr - ωt)
k = 2π/λ (wave number)
Phase velocity: v = ω/k = c/n
```

### Interference
```
Two-source interference (Young's double slit):
  Path difference: Δ = d·sinθ ≈ d·y/L
  Constructive (bright): Δ = mλ      m = 0,±1,±2,...
  Destructive (dark):    Δ = (m+½)λ
  Fringe spacing: Δy = λL/d

Intensity pattern:
  I = 4I₀cos²(πdsinθ/λ)
  I = 4I₀ at maxima, 0 at minima

Conditions for interference:
  Coherence: stable phase relationship between sources
  Coherence length: Lc = λ²/Δλ
  Coherence time: τc = 1/Δf

Thin film interference:
  Path difference: 2nt (for normal incidence)
  Phase shift: π if reflecting from higher n medium
  Constructive: 2nt = (m+½)λ (one phase shift)
  Destructive:  2nt = mλ     (one phase shift)
  → Anti-reflection coatings: t = λ/4n
  → Soap bubbles, oil films, optical coatings
```

---

## Diffraction
```
Single slit diffraction:
  Minima at: a·sinθ = mλ  m = ±1,±2,...
  Central maximum width: 2λ/a
  Intensity: I = I₀[sin(α)/α]²
  α = πa·sinθ/λ

Double slit (combined):
  I = 4I₀cos²(δ/2)[sin(α)/α]²
  δ = 2πd·sinθ/λ  (interference term)
  α = πa·sinθ/λ   (diffraction envelope)

Diffraction grating:
  Principal maxima: d·sinθ = mλ
  d = grating spacing, m = order
  Resolving power: R = λ/Δλ = mN  (N = number of slits)

Rayleigh criterion (resolution limit):
  θmin = 1.22λ/D  (circular aperture)
  Two sources just resolved when one max falls on other's min.

Fresnel vs Fraunhofer:
  Fraunhofer: far field (L >> a²/λ) — parallel rays
  Fresnel: near field — curved wavefronts
```

---

## Polarization
```
Linear polarization: E oscillates in single plane
Circular polarization: E rotates — equal amplitudes, 90° phase diff
Elliptical polarization: general case

Malus's Law:
  I = I₀cos²θ  (intensity through polarizer at angle θ)

Brewster's Angle (polarization by reflection):
  tanθB = n₂/n₁
  At θB: reflected light is completely s-polarized
  Transmitted light: partially p-polarized

Birefringence:
  Two different refractive indices: no and ne
  Ordinary ray (o-ray): follows Snell's law
  Extraordinary ray (e-ray): does not

Wave plates:
  Quarter-wave plate (QWP): Δφ = π/2
    Linear → circular polarization (and vice versa)
  Half-wave plate (HWP): Δφ = π
    Rotates linear polarization by 2θ

Jones vectors and matrices:
  Horizontal: [1,0], Vertical: [0,1]
  Right circular: [1,-i]/√2
  HWP matrix: [[cos2θ, sin2θ],[sin2θ, -cos2θ]]
```

---

## Lasers
```
Laser = Light Amplification by Stimulated Emission of Radiation

Key concepts:
  Spontaneous emission: random photon emission
  Stimulated emission: incident photon triggers identical photon
  Population inversion: more atoms in excited state than ground state
  → Required for amplification (not thermal equilibrium)

Three/four level systems:
  Three-level: difficult — must depopulate ground state
  Four-level: easier — lasing transition between two excited states
  Ruby laser (3-level), Nd:YAG (4-level)

Laser cavity:
  Two mirrors (one partially transmitting) → standing wave modes
  Mode spacing: Δν = c/2L
  Longitudinal modes: integer wavelengths fit in cavity

Gaussian beam:
  w(z) = w₀√(1 + (z/zR)²)
  zR = πw₀²/λ  (Rayleigh range)
  w₀ = beam waist (minimum radius)
  Beam divergence: θ = λ/πw₀  (diffraction limited)

Laser properties:
  Coherence: long coherence length
  Monochromaticity: narrow linewidth
  Directionality: small divergence
  High intensity: concentrated beam

Common laser types:
  HeNe:   λ = 632.8 nm (red, gas laser)
  CO₂:    λ = 10.6 μm  (infrared, cutting)
  Nd:YAG: λ = 1064 nm  (solid state, pulsed)
  Diode:  various λ    (semiconductor, compact)
  Ti:Sapphire: tunable (ultrafast pulses)
```

---

## Fiber Optics
```
Total internal reflection guides light in fiber core.
Core: higher n, Cladding: lower n
Numerical aperture: NA = √(n_core² - n_clad²) = n·sinθmax

Step-index fiber:
  Sharp boundary between core and cladding.
  Multimode: large core, many propagating modes.
  Single-mode: small core (~8μm), one mode, low dispersion.

Graded-index fiber:
  n decreases gradually from center.
  Reduces intermodal dispersion.

Dispersion types:
  Modal: different modes travel at different speeds
  Chromatic: different wavelengths travel at different speeds
  Material: from dn/dλ
  Waveguide: from fiber geometry

Attenuation:
  Measured in dB/km
  Minimum at λ = 1550 nm (~0.2 dB/km for silica)
  Telecom windows: 1310 nm, 1550 nm

Applications:
  Long-distance communication, endoscopy, sensors
```

---

## Optical Instruments
```python
def microscope_magnification(objective_mag, eyepiece_mag,
                              tube_length=160, f_obj=None):
    total_mag = objective_mag * eyepiece_mag
    return {
        'objective':    objective_mag,
        'eyepiece':     eyepiece_mag,
        'total':        total_mag,
        'resolution':   '0.2 μm (visible light limit)',
        'note':         'Resolution limited by diffraction: d = 0.61λ/NA'
    }

def telescope_magnification(f_objective, f_eyepiece):
    mag = f_objective / f_eyepiece
    return {
        'magnification': mag,
        'f_objective':   f_objective,
        'f_eyepiece':    f_eyepiece,
        'note':          'Larger aperture → better resolution and light gathering'
    }

def camera_depth_of_field(f_number, focal_length, distance, coc=0.03):
    """
    Depth of field calculation.
    coc = circle of confusion (mm)
    """
    import math
    hyp = focal_length**2 / (f_number * coc)
    near = (hyp * distance) / (hyp + distance - focal_length)
    far  = (hyp * distance) / (hyp - distance + focal_length)
    dof  = far - near
    return {
        'near_limit': round(near, 2),
        'far_limit':  round(far, 2),
        'dof':        round(dof, 2),
        'hyperfocal': round(hyp, 2)
    }
```

---

## Aberrations
```
Monochromatic aberrations (Seidel):
  Spherical aberration: marginal rays focus differently than paraxial
  Coma: off-axis point sources form comet shape
  Astigmatism: different focal lengths in two planes
  Field curvature: flat object focuses on curved surface
  Distortion: magnification varies with field height

Chromatic aberration:
  Longitudinal: different colors focus at different distances
  Transverse: different colors have different magnifications
  Correction: achromatic doublet (crown + flint glass)

Zernike polynomials:
  Mathematical basis for describing wavefront aberrations.
  Used in adaptive optics and ophthalmology.
```

---

## Key Equations Summary
```python
def optics_calculator():
    return {
        'thin_lens':        '1/f = 1/do + 1/di',
        'magnification':    'M = -di/do',
        'snell':            'n1*sin(θ1) = n2*sin(θ2)',
        'critical_angle':   'sinθc = n2/n1',
        'brewster':         'tanθB = n2/n1',
        'young_fringes':    'Δy = λL/d',
        'rayleigh':         'θmin = 1.22λ/D',
        'single_slit_min':  'a*sinθ = mλ',
        'grating':          'd*sinθ = mλ',
        'malus':            'I = I0*cos²θ',
        'thin_film_AR':     't = λ/4n'
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Sign convention errors in lens/mirror | Define positive direction consistently |
| Forgetting phase shift on reflection | π phase shift when reflecting from denser medium |
| Rayleigh vs Abbe resolution | Rayleigh for telescopes, Abbe for microscopes |
| Ignoring coherence for interference | Interference only visible with coherent sources |
| Paraxial approximation failure | Valid only for small angles sinθ ≈ θ |
| Confusing focal length and focal point | f is distance, F is the point |

---

## Related Skills

- **electromagnetism-expert**: Light as EM wave
- **quantum-mechanics-expert**: Photons, photoelectric effect
- **special-relativity-expert**: Speed of light
- **photonics-expert**: Advanced optical systems
- **signal-processing-expert**: Fourier optics
