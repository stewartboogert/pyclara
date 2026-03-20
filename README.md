# Start-to-End-S2E-simulation-for-CLARA-FEBE

## Overview

This repository contains a full **Start-to-End (S2E) simulation pipeline** for beam 
dynamics at the CLARA-FEBE beamline

The workflow connects conventional accelerator tracking codes with plasma simulation 
tools to study **beam-driven plasma wakefield acceleration (PWFA)** using realistic 
electron beam distributions.

---

### Tools used

- ASTRA — injector modelling (optional)
- Elegant — beam tracking through linac and beamline
- FBPIC — plasma wakefield simulation
- Python — data processing and analysis
- Simframe — ASTeC base model description

## Repository Structure

```text
clara-s2e/
│
├── Info/             # project overview and documentation
├── Injector/         # ASTRA injector simulations
├── Output/           # simulation results and data
├── PostInjector/     # Simframe and Elegant input files
├── src/              # python project source code 
└── README.md

---
```

## Installation

Clone the repository:

```bash
git clone https://github.com/Shuyan0224/Start-to-End-S2E-simulation-for-CLARA-FEBE.git clara-s2e
cd clara-s2e
pip install -e .
```

## Running elegant 

```bash 
mkdir Run
cd Run
ln -s ../PostInjector/* .
mpiexec -np #number_cores Pelegant FEBE.ele 
```
The output files can be read using python (you need to have
sdds installed, e.g. `pip install sdds`):

```bash
import sdds

d = sdds.load('FEBE.twi')

# making a standard optics plot 
subplot(2,1,1)
plot(d.getColumnValueList('s'),d.getColumnValueList('betax'))
plot(d.getColumnValueList('s'),d.getColumnValueList('betay'))
subplot(2,1,2)
plot(d.getColumnValueList('s'),d.getColumnValueList('etax'))
plot(d.getColumnValueList('s'),d.getColumnValueList('etay'))

# getting twiss parameters at a named element (e.g betax at CLA-FED-DIA-BPM-01-DRIFT-02
betax = array(d.getColumnValueList("betax"))[array(d.getColumnValueList('ElementName')) == 'CLA-FED-DIA-BPM-01-DRIFT-02']
print(betax)

```
The twi file of the PostInjector optics ```FEBE.twi``` has been placed in the 
PostInjector directory for convvenience

## Apptainer/docker elegant 

If you do not have elegant installed. There is an appaineter image available