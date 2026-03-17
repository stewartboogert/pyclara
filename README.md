# Start-to-End-S2E-simulation-for-CLARA-FEBE

## 📌 Overview

This repository contains a full **Start-to-End (S2E) simulation pipeline** for beam dynamics at the CLARA FEBE beamline, developed at CLARA.

The workflow connects conventional accelerator tracking codes with plasma simulation tools to study **beam-driven plasma wakefield acceleration (PWFA)** using realistic electron beam distributions.

---

## 🧠 Objectives

- Simulate electron beam evolution from injector to plasma stage
- Simulate PWFA and LWFA process
- Compare realistic beam distributions with idealised Gaussian beams

- ## 🧩 Simulation Pipeline

The S2E workflow consists of:
Injector → Linac → Compression → Transport → Plasma (FBPIC)

### Tools used

- ASTRA — injector modelling (optional)
- Elegant — beam tracking through linac and beamline
- FBPIC — plasma wakefield simulation
- Python — data processing and analysis

## 📁 Repository Structure

```text
clara-s2e/
│
├── elegant/          # lattice files and beam generation
├── conversion/       # SDDS → HDF5 conversion scripts
├── fbpic/            # plasma simulation scripts
├── analysis/         # post-processing and diagnostics
├── figures/          # generated plots
├── docs/             # simulation logs and notes
│
├── requirements.txt
└── README.md

---
```

## ⚙️ Installation

Clone the repository:

```bash
git clone https://github.com/your-username/clara-s2e.git
cd clara-s2e
