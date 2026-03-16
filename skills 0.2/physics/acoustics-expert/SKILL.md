---
name: acoustics-expert
description: Expert-level acoustics knowledge. Use when working with sound waves, acoustic propagation, resonance, standing waves, Doppler effect, room acoustics, ultrasound, noise control, musical acoustics, or architectural acoustics. Also use when the user mentions 'sound wave', 'decibel', 'frequency', 'resonance', 'standing wave', 'Doppler effect', 'acoustic impedance', 'reverberation', 'ultrasound', 'noise control', 'harmonics', or 'sound intensity'.
license: MIT
metadata:
  author: luokai25
  version: "1.0"
  category: science
---

# Acoustics Expert

You are a world-class physicist with deep expertise in acoustics covering sound wave physics, acoustic propagation, resonance, room acoustics, architectural acoustics, musical acoustics, ultrasound, noise control, and psychoacoustics.

## Before Starting

1. **Topic** — Wave physics, room acoustics, musical acoustics, ultrasound, or noise control?
2. **Level** — High school, undergraduate, or graduate?
3. **Goal** — Solve problem, design system, or understand concept?
4. **Context** — Physics, engineering, music, or architecture?
5. **Medium** — Air, water, solid, or biological tissue?

---

## Core Expertise Areas

- **Wave Physics**: speed, frequency, wavelength, intensity, decibels
- **Wave Phenomena**: reflection, refraction, diffraction, interference
- **Resonance**: standing waves, harmonics, normal modes
- **Doppler Effect**: moving sources and observers
- **Room Acoustics**: reverberation, absorption, diffusion
- **Musical Acoustics**: instruments, harmonics, tuning systems
- **Ultrasound**: medical imaging, nondestructive testing
- **Noise Control**: absorption, isolation, active noise control
- **Psychoacoustics**: human hearing, loudness, pitch perception

---

## Sound Wave Fundamentals
```
Sound wave: longitudinal pressure wave in elastic medium.
  Displacement: s(x,t) = s₀cos(kx - ωt)
  Pressure:     p(x,t) = p₀sin(kx - ωt)   (90° out of phase with displacement)
  p₀ = ρ₀vω·s₀  (pressure amplitude)

Wave equation:
  ∂²s/∂t² = v²∂²s/∂x²
  v = speed of sound

Speed of sound:
  General: v = √(B/ρ)  (B = bulk modulus, ρ = density)
  Ideal gas: v = √(γP/ρ) = √(γRT/M)
  Air at 20°C: v = 343 m/s
  Air: v(T) ≈ 331 + 0.6T  (T in Celsius, v in m/s)
  Water: v ≈ 1480 m/s
  Steel: v ≈ 5100 m/s
  Solids faster than liquids faster than gases.

Frequency and wavelength:
  v = fλ
  Audible range: 20 Hz - 20 kHz
  Infrasound: f < 20 Hz
  Ultrasound:  f > 20 kHz
  λ in air at 20°C: λ = 343/f  (17 m at 20 Hz, 17 mm at 20 kHz)
```

---

## Sound Intensity & Decibels
```
Intensity:
  I = P/A = p₀²/2ρv = ½ρvω²s₀²
  Units: W/m²
  Threshold of hearing: I₀ = 10⁻¹² W/m²
  Pain threshold: ~1 W/m²

Decibel scale:
  Sound level: β = 10·log₁₀(I/I₀)  dB
  Inverse square law: I = P_source/(4πr²)  (point source, free field)
  β drops 6 dB per doubling of distance.

Common sound levels:
  0 dB:   threshold of hearing
  20 dB:  whisper
  60 dB:  normal conversation
  85 dB:  hearing damage threshold (prolonged)
  90 dB:  lawn mower
  120 dB: rock concert, jet at 100m (pain threshold)
  140 dB: gunshot, jet engine nearby

Adding intensities:
  Total intensity = ΣI  (add intensities, not dB directly)
  Two equal sources: β_total = β₁ + 3 dB
  10 identical sources: β_total = β₁ + 10 dB

Acoustic power:
  Sound power level: Lw = 10·log₁₀(W/W₀)  W₀ = 10⁻¹² W
  Directivity: Q = I(θ,φ)/I_avg
```

---

## Wave Phenomena
```
Reflection:
  Angle of incidence = angle of reflection
  Hard boundary (wall): pressure antinode, displacement node
  Soft boundary (open end): pressure node, displacement antinode
  Acoustic impedance: Z = ρv  (characteristic impedance)
  Reflection coefficient: R = (Z₂-Z₁)/(Z₂+Z₁)
  Transmission coefficient: T = 2Z₂/(Z₂+Z₁)

Refraction (Snell's law):
  sinθ₁/v₁ = sinθ₂/v₂
  Sound bends toward lower speed regions.
  Temperature gradients → atmospheric refraction.

Diffraction:
  Sound bends around obstacles when λ ≥ obstacle size.
  Low frequencies diffract more than high.
  Explains: can hear around corners (low f), not see.

Interference:
  Constructive: path difference = nλ
  Destructive: path difference = (n+½)λ
  Beats: two close frequencies f₁,f₂
    Beat frequency: fbeat = |f₁ - f₂|
    Perceived as amplitude modulation at fbeat.
```

---

## Resonance & Standing Waves
```
Standing wave: superposition of two traveling waves in opposite directions.
  s(x,t) = 2s₀sin(kx)cos(ωt)
  Nodes: s = 0 always (kx = nπ)
  Antinodes: maximum amplitude (kx = (n+½)π)

Strings (fixed at both ends):
  Boundary condition: nodes at x=0 and x=L
  Harmonics: fn = n·v/2L  n = 1,2,3,...
  Fundamental (n=1): f₁ = v/2L
  Overtones: f₂=2f₁, f₃=3f₁, ... (harmonic series)
  Wave speed on string: v = √(T/μ)  (T=tension, μ=linear density)

Open pipe (open at both ends):
  Pressure nodes at both ends (displacement antinodes)
  fn = n·v/2L  n = 1,2,3,...  (same as string)
  All harmonics present.

Closed pipe (closed at one end):
  Displacement node at closed end, antinode at open end.
  fn = n·v/4L  n = 1,3,5,...  (odd harmonics only)
  Fundamental: f₁ = v/4L

3D resonance (room modes):
  Room modes: f = (v/2)√((nx/Lx)² + (ny/Ly)² + (nz/Lz)²)
  Axial (1D), tangential (2D), oblique (3D) modes.
```

---

## Doppler Effect
```
Moving source, stationary observer:
  f_obs = f_source · v/(v ∓ vs)
  - (minus): source approaching → higher frequency
  + (plus):  source receding → lower frequency

Moving observer, stationary source:
  f_obs = f_source · (v ± vo)/v
  + (plus):  observer approaching → higher frequency

General (both moving):
  f_obs = f_source · (v + vo)/(v + vs)
  Sign convention: positive toward each other.

Mach number:
  M = vs/v  (ratio of source speed to sound speed)
  M < 1: subsonic, M = 1: sonic, M > 1: supersonic

Shock wave (sonic boom):
  Formed when M > 1 (source faster than sound)
  Mach cone half-angle: sinα = 1/M = v/vs
  Bow wave — like boat wake in water.

Applications:
  Police radar: microwave Doppler → vehicle speed
  Medical ultrasound: blood flow velocity measurement
  Astronomy: stellar radial velocities (redshift/blueshift)
  Weather radar: Doppler wind measurement
```

---

## Room Acoustics
```python
def room_acoustics():
    return {
        'Sabine equation': {
            'formula':      'T60 = 0.161 V / (Σ αᵢSᵢ)',
            'T60':          'Reverberation time (seconds for 60 dB decay)',
            'V':            'Room volume (m³)',
            'α':            'Absorption coefficient (0-1)',
            'S':            'Surface area (m²)',
            'Eyring':       'T60 = 0.161 V / (-S·ln(1-ᾱ))  (better for high absorption)'
        },
        'Optimal T60': {
            'speech':       '0.3-0.8 s',
            'chamber music':'1.0-1.5 s',
            'symphony':     '1.8-2.2 s',
            'organ music':  '2.5-4.0 s',
            'lecture hall': '0.6-1.0 s'
        },
        'Room modes': {
            'problem':      'Uneven bass response at low frequencies',
            'solution':     'Diffusers, bass traps, room geometry',
            'Schroeder freq': 'f_S = 2000√(T60/V) — below: modal, above: diffuse'
        },
        'Acoustic defects': {
            'Flutter echo':     'Repeated echoes between parallel walls',
            'Long echo':        'Discrete echo > 50 ms delay (40 m path diff)',
            'Focusing':         'Concave surfaces concentrate sound',
            'Dead spots':       'Interference nulls at certain frequencies/positions'
        }
    }

def absorption_coefficients():
    return {
        'Material':         '125Hz  250Hz  500Hz  1kHz   2kHz   4kHz',
        'Concrete':         '0.01   0.01   0.02   0.02   0.02   0.03',
        'Carpet (thick)':   '0.02   0.06   0.14   0.37   0.60   0.65',
        'Acoustic tile':    '0.20   0.40   0.70   0.80   0.60   0.40',
        'Curtains (heavy)': '0.07   0.31   0.49   0.75   0.70   0.60',
        'Audience/seat':    '0.20   0.40   0.78   0.98   0.96   0.87',
        'Open window':      '1.00   1.00   1.00   1.00   1.00   1.00'
    }
```

---

## Musical Acoustics
```
Harmonic series:
  f, 2f, 3f, 4f, 5f, 6f, ...
  Determines timbre (tone quality) of instruments.
  More high harmonics → brighter, more nasal sound.

Musical intervals (equal temperament, 12-TET):
  Octave:      frequency ratio 2:1  (1200 cents)
  Perfect 5th: 2^(7/12) ≈ 1.498  (700 cents)
  Major 3rd:   2^(4/12) ≈ 1.260  (400 cents)
  Semitone:    2^(1/12) ≈ 1.0595

Just intonation:
  Perfect 5th: 3/2 = 1.500  (pure, no beats)
  Major 3rd:   5/4 = 1.250
  Pythagorean comma: 12 perfect 5ths ≠ 7 octaves

Instrument acoustics:
  Strings: v = √(T/μ), f = nv/2L
  Bowed strings: stick-slip mechanism → sawtooth wave
  Wind instruments: pipe resonances + reed/lip vibrations
  Percussion: 2D membrane modes, bar and plate modes
  Voice: vocal tract resonances (formants) shape spectrum

Psychoacoustics of music:
  Missing fundamental: brain perceives pitch even without f₁
  Consonance/dissonance: related to frequency ratios
  Masking: loud sound hides softer nearby sounds
  Timbre: attack, spectral content, vibrato all contribute
```

---

## Ultrasound
```
Medical ultrasound:
  Frequency: 1-20 MHz (higher f → better resolution, less penetration)
  λ = v/f = 1540/f  (1540 m/s in soft tissue)
  At 5 MHz: λ = 0.3 mm (axial resolution ~λ/2)

Pulse-echo imaging:
  Short pulse sent, echoes timed → depth = v·t/2
  A-mode: amplitude vs depth
  B-mode: brightness 2D image
  M-mode: motion over time

Doppler ultrasound:
  Blood flow: f_shift = 2f₀·v·cosθ/c
  Color Doppler: flow direction coded by color
  Pulsed Doppler: flow at specific depth

Acoustic properties of tissue:
  Impedance: Z = ρv
  Reflection at boundary: R = (Z₂-Z₁)²/(Z₂+Z₁)²
  Attenuation: α ≈ 0.5 dB/cm/MHz (soft tissue)
  Coupling gel: eliminates air interface (Z_air << Z_tissue)

Industrial ultrasound:
  Nondestructive testing (NDT): flaw detection in materials
  Phased array: electronic beam steering
  Thickness gauging: v·t/2
  Sonar: underwater ranging and imaging
  Ultrasonic cleaning: cavitation removes contaminants
```

---

## Noise Control
```python
def noise_control_strategies():
    return {
        'Source control': [
            'Reduce vibration at source (balancing, isolation)',
            'Change process (electric vs combustion)',
            'Mufflers and silencers',
            'Acoustic enclosures around sources'
        ],
        'Path control': [
            'Distance: 6 dB reduction per doubling of distance',
            'Barriers: insertion loss IL = 10·log₁₀(1 + (2N)^(1.5))',
            'N = Fresnel number = 2δ/λ, δ = path length difference',
            'Absorption: line room surfaces',
            'Vibration isolation: springs, damping materials'
        ],
        'Receiver control': [
            'Personal protective equipment (PPE)',
            'Hearing protection: earplugs (10-30 dB)',
            'Enclosures around workers',
            'Time reduction in noisy environment'
        ],
        'Active noise control (ANC)': [
            'Measure noise with microphone',
            'Generate anti-phase sound from speaker',
            'Destructive interference → cancellation',
            'Works best: low frequency, confined paths',
            'Applications: headphones, HVAC ducts, car cabins'
        ]
    }

def sound_transmission_loss(mass_per_area, frequency):
    """
    Mass law for sound insulation.
    TL = 20·log10(m·f) - 42  (dB, approximate)
    """
    TL = 20 * (mass_per_area * frequency) ** 0.5 - 42
    import math
    TL = 20 * math.log10(mass_per_area * frequency) - 42
    return {
        'mass_per_area':    mass_per_area,
        'frequency':        frequency,
        'transmission_loss': round(TL, 1),
        'note': 'Doubling mass or frequency adds ~6 dB'
    }
```

---

## Psychoacoustics
```
Hearing range:
  Frequency: 20 Hz - 20 kHz (decreases with age)
  Intensity: 0 dB - ~120 dB (dynamic range ~120 dB)

Equal loudness contours (Fletcher-Munson):
  Ear most sensitive at 1-4 kHz.
  Need more SPL at low/high frequencies for equal loudness.
  A-weighting: filter mimicking ear sensitivity.
  dBA: A-weighted decibels for human noise assessment.

Loudness:
  Unit: phon (at 1kHz: 1 phon = 1 dB SPL)
  Sone scale: 1 sone = 40 phon, doubles every 10 phon
  10 dB increase ≈ doubling of perceived loudness (approximate)

Pitch perception:
  Place theory: different frequencies excite different cochlear regions
  Temporal theory: firing rate encodes frequency (low f only)
  Missing fundamental: pitch perceived at f₁ even if absent
  Just noticeable difference (JND): ~0.3-0.5% in frequency

Masking:
  Simultaneous masking: loud sound hides softer nearby frequency
  Temporal masking: loud sound affects perception before/after
  Critical bandwidth: ~1/3 octave (Bark scale)
  Basis for MP3/perceptual audio coding
```

---

## Key Equations Summary
```python
def acoustics_formulas():
    return {
        'Wave speed':           'v = fλ = √(γRT/M)',
        'Intensity':            'I = p₀²/2ρv = P/4πr²',
        'Sound level':          'β = 10·log10(I/I₀), I₀ = 10⁻¹² W/m²',
        'Doppler':              'f_obs = f·(v±v_obs)/(v∓v_src)',
        'Standing wave string': 'fn = n·v/2L',
        'Standing wave closed': 'fn = n·v/4L  (n odd)',
        'Sabine reverb':        'T60 = 0.161·V/A',
        'Impedance':            'Z = ρv',
        'Reflection coeff':     'R = (Z2-Z1)/(Z2+Z1)',
        'Beat frequency':       'fbeat = |f1-f2|'
    }
```

---

## Common Pitfalls

| Pitfall | Fix |
|---|---|
| Adding decibels directly | Convert to intensity first, then add, then convert back |
| Confusing frequency and pitch | Pitch is psychoacoustic, frequency is physical |
| Open pipe = closed pipe modes | Open: all harmonics, Closed: odd harmonics only |
| Sound travels faster in hot air | v = √(γRT/M) — higher T → faster v |
| Doubling distance = -3dB | Point source free field: -6 dB per distance doubling |
| Reverberation = echo | Echo: distinct reflection >50ms, Reverb: many overlapping reflections |

---

## Related Skills

- **classical-mechanics-expert**: Wave mechanics foundations
- **electromagnetism-expert**: Analogy between acoustic and EM waves
- **fluid-mechanics-expert**: Acoustic wave propagation in fluids
- **signal-processing-expert**: Fourier analysis of sound
- **biomedical-imaging-expert**: Ultrasound imaging systems
