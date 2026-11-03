# Cutaneous Laser Speckle Contrast Imaging (LSCI) Skill

[![License](https://img.shields.io/badge/license-Apache--2.0-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/python-3.8+-brightgreen.svg)](https://www.python.org/)
[![OpenClaw](https://img.shields.io/badge/ecosystem-OpenClaw-orange.svg)](https://openclaw.org/)
[![GenPark](https://img.shields.io/badge/sovereign-GenPark-purple.svg)](https://alphapark.ai/)
[![MCP](https://img.shields.io/badge/protocol-MCP-success.svg)](https://modelcontextprotocol.io/)

Cutaneous Laser Speckle Contrast Imaging (LSCI) and Microvascular Blood Flow Analyzer based on coherent optical scattering physics.

```mermaid
flowchart TD
    A[Local Pixel Intensity Kernel] --> B[Calculate Mean Intensity and Variance]
    B --> C[Compute Speckle Contrast: K = sigma / mean]
    C --> D[Compute Blood Flow Index: BFI = 1 / 2 * T * K^2]
    D --> E[Scale to Laser Speckle Perfusion Units LSPU]
    E --> F[Microvascular Perfusion & Flux Reserve Guidance]
```

## Features
- **Zero PIP Dependencies**: Implemented strictly with Python Standard Library (`math`, `json`, `sys`, `typing`).
- **Coherent Optics Biophysics**: Translates spatial speckle variance into continuous blood velocity metrics.
- **Exposure-Compensated**: Accounts for camera exposure duration $T$ in the BFI equation.
- **Dual Architecture**: Native Python import and Model Context Protocol (MCP) JSON-RPC 2.0 stdio server.

## Quickstart
```bash
python example_usage.py
```

## License
Apache-2.0
