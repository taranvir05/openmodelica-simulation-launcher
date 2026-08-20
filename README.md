# openmodelica-simulation-launcher
A desktop application using the PyQt6 library for launching OpenModelica simulation executables with user-specified start and stop times.

## Overview
This project has two parts:
1. An OpenModelica model ("TwoConnectedTanks") compiled into a standalone Windows executable.
2. A PyQt6 GUI application that runs this executable, letting the user choose which application to launch and what start/stop time to simulate with.

## Repository Structure
- `executable/` — the compiled TwoConnectedTanks.exe and its runtime dependencies
- `model/original/` — the unmodified OpenModelica model files as provided
- `model/patched/` — Tank2.mo with a one-line fix (see Known Issue below)
- `src/` — the PyQt6 GUI application
- `docs/screenshots/` — screenshots of the app in use

## Requirements
1. Python 3.6+
2. PyQt6
3. OpenModelica
4. Linux OS or Windows 10/11 OS

## Setup & Installation
1. Clone this repository
2. Install dependencies: `pip install -r requirements.txt`
3. Run the app: `python src/main.py`
4. Click "Browse" and select `executable/TwoConnectedTanks.exe`
5. Enter a start time and stop time (must satisfy 0 <= start < stop < 5)
6. Click "Run"

## How It Works
The GUI collects three inputs — the path to the executable, and integer start/stop times. Before running anything, it validates that:

a. The selected file actually exists
b. Both time values are valid integers
c. They satisfy 0 <= start time < stop time < 5

If any check fails, the app shows a clear error message and does not attempt to run the simulation.

If validation passes, the app launches the executable using Python's subprocess module, passing the times as command-line flags in the form the executable expects:
TwoConnectedTanks.exe -startTime=<value> -stopTime=<value>

This mirrors the exact command OMEdit itself uses internally when simulating the model, confirmed by testing the compiled executable directly from the command line.

## Known Issue & Fix
The provided Tank2.mo model defines a variable T = V/Q1, which is never used anywhere else in the model but causes a division-by-zero error at the very start of the simulation, since Q1 (the flow rate) is zero at t=0.
Since T has no effect on any other variable, state, or output in the model.I patched this single line in `model/patched/Tank2.mo` to `T = V/max(Q1, 1e-6)`,

This prevents the crash without changing the tanks' actual simulated behavior (h and Q1, the values that matter, are unaffected). The original, unmodified model files are kept in model/original/ so the change is easy to verify and compare.

