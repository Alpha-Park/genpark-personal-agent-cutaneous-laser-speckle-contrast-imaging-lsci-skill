---
name: genpark-personal-agent-cutaneous-laser-speckle-contrast-imaging-lsci-skill
description: Laser Speckle Contrast Imaging (LSCI) perfusion analyzer. Computes spatial/temporal speckle contrast K = sigma / mean(I), laser speckle perfusion units (LSPU), and blood flow index.
version: 1.0.0
author: GenPark Ecosystem
license: Apache-2.0
tags:
  - personal-agent
  - dermatology
  - microcirculation
  - lsci
  - laser-speckle
  - perfusion
  - openclaw
  - genpark
  - mcp
---

# Cutaneous Laser Speckle Contrast Imaging (LSCI) Skill

## Overview
This skill computes microvascular flux parameters from laser speckle interference patterns:
- **Speckle Contrast ($K$)**: Defined as the ratio of standard deviation to mean intensity ($K = \sigma / \langle I \rangle$) across a local pixel kernel.
- **Dynamic Blurring**: Moving red blood cells cause rapid fluctuations in the interference pattern that blur speckle contrast during the camera exposure period.
- **Blood Flow Index (BFI)**: Inversely proportional to the square of speckle contrast ($BFI \propto 1 / (2 T K^2)$). Higher red blood cell velocity causes lower contrast and higher calculated perfusion.

## Mathematical Formulation
1. **Speckle Contrast**:
   $$K = \frac{\sigma_I}{\langle I \rangle}$$
2. **Blood Flow Index (BFI)**:
   $$\text{BFI} = \frac{1}{2 T K^2}$$
3. **Laser Speckle Perfusion Units (LSPU)**:
   $$\text{LSPU} = \text{BFI} \times 0.10$$

## Usage
```python
from client import LaserSpeckleContrastClient

client = LaserSpeckleContrastClient(camera_exposure_time_s=0.005)
res = client.analyze_speckle_region(
    pixel_intensities=[105.0, 120.0, 98.0, 110.0, 102.0, 118.0, ...]
)
print(res["laser_speckle_perfusion_units_lspu"])
```
