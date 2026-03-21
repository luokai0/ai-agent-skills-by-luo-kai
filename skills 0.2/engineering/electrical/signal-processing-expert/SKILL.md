---
name: signal-processing-expert
version: 1.0.0
description: Expert-level signal processing covering Fourier analysis, sampling theory, digital filters, FFT, spectral estimation, and adaptive filtering.
author: luokai25
tags: [signal processing, Fourier, FFT, digital filters, sampling, spectral analysis]
---

# Signal Processing Expert

## Before Starting
1. Continuous or discrete time signals?
2. FIR or IIR filter design?
3. 1D or multidimensional processing?

## Core Expertise Areas

### Fourier Analysis
Fourier series: periodic signal decomposed into harmonics.
Fourier transform: continuous signal to frequency domain representation.
DTFT: discrete-time Fourier transform for discrete signals.
DFT: discrete Fourier transform, finite length sequence, periodic in frequency.
FFT: fast Fourier transform, O(N log N) algorithm for DFT computation.

### Sampling Theory
Nyquist theorem: sample at twice the highest frequency to avoid aliasing.
Aliasing: frequencies above Nyquist fold back, appear as lower frequencies.
Anti-aliasing filter: lowpass filter before ADC to prevent aliasing.
Interpolation: reconstruct continuous signal from samples using sinc function.
Oversampling: sample faster than Nyquist, use decimation to reduce noise.

### Digital Filters
FIR: finite impulse response, always stable, linear phase possible.
IIR: infinite impulse response, recursive, more efficient but can be unstable.
Filter design: Parks-McClellan for FIR, bilinear transform for IIR from analog.
Z-transform: discrete equivalent of Laplace transform, analyzes filter stability.
Poles and zeros: determine filter frequency response and stability.

### Spectral Estimation
Periodogram: squared magnitude of FFT, basic power spectral density estimate.
Welch method: average periodograms of overlapping segments, reduces variance.
Windowing: reduce spectral leakage, trade resolution for dynamic range.
Parametric methods: AR, ARMA models for spectral estimation.

## Best Practices
- Always apply anti-aliasing filter before sampling
- Choose window function based on spectral leakage requirements
- Verify filter stability by checking poles inside unit circle
- Use zero-padding to increase frequency resolution in DFT

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Aliasing from insufficient sampling rate | Sample at least twice highest frequency of interest |
| Spectral leakage distorting analysis | Apply appropriate window function |
| IIR filter instability | Check all poles inside unit circle |
| Circular convolution confusion | Use zero-padding for linear convolution via DFT |

## Related Skills
- circuit-analysis-expert
- communications-expert
- machine-learning-expert
