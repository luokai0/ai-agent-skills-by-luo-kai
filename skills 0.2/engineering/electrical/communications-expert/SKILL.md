---
name: communications-expert
version: 1.0.0
description: Expert-level communications engineering covering modulation, channel capacity, error correction, wireless systems, OFDM, MIMO, and 5G technologies.
author: luokai25
tags: [communications, modulation, Shannon, OFDM, MIMO, 5G, error correction]
---

# Communications Expert

## Before Starting
1. Wired or wireless channel?
2. Physical layer or protocol design?
3. System design or performance analysis?

## Core Expertise Areas

### Information Theory
Shannon capacity: C = B log2 of 1 plus SNR, maximum error-free rate.
Entropy: measure of information content, H = negative sum of p log p.
Channel capacity: depends on bandwidth and SNR, fundamental limit.
Shannon limit: minimum Eb/N0 for reliable communication is negative 1.6 dB.

### Modulation
ASK, FSK, PSK: amplitude, frequency, phase shift keying.
QAM: quadrature amplitude modulation, combines amplitude and phase, high spectral efficiency.
BPSK: binary PSK, most robust, low spectral efficiency.
16-QAM, 64-QAM, 256-QAM: higher order for more bits per symbol, needs higher SNR.
OFDM: orthogonal frequency division multiplexing, divides band into subcarriers.

### Error Correction
Hamming codes: detect and correct single bit errors.
Convolutional codes: memory in encoder, Viterbi decoding.
Turbo codes: near Shannon limit, iterative decoding.
LDPC: low density parity check, near Shannon limit, used in 5G NR.
Polar codes: provably capacity-achieving, used in 5G control channels.

### Wireless Systems
Fading: multipath causes signal amplitude variations, Rayleigh distribution.
Diversity: spatial, frequency, time diversity combat fading.
MIMO: multiple input multiple output, spatial multiplexing increases capacity.
Massive MIMO: hundreds of antennas at base station, beamforming to users.
5G NR: new radio, sub-6 GHz and mmWave, 100 MHz bandwidth, network slicing.

## Best Practices
- Always analyze link budget before designing wireless system
- Account for implementation losses in real system vs theoretical
- Choose modulation order based on actual SNR not peak SNR
- Test error correction performance under expected channel conditions

## Common Pitfalls
| Pitfall | Fix |
|---|---|
| Ignoring implementation losses | Practical systems lose 2-5 dB vs theory |
| Wrong SNR definition | Clarify whether Eb/N0, Es/N0, or SNR per bandwidth |
| Insufficient link margin | Add fade margin for wireless reliability requirement |
| OFDM PAPR issue | Use clipping, predistortion, or tone reservation |

## Related Skills
- signal-processing-expert
- computer-networks-expert
- electronics-expert
