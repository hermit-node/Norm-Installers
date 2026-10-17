# Norm Installer 1.4.0

**Commit:** `53d0932` — Norm 0.52.6-pre
**Files:** Norm-Installer.py, Make-Norm-Installer.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat
**Lines:** 1338 | **Classes:** 4 | **Functions:** 36
**Schema:** 1

## What this is

Introduces `Make-Norm-Installer.py`, a separate EXE builder that packages the
installer into a distributable binary. The build pipeline is now two-stage:
`Make-Norm-Installer.py` builds the EXE, `Build-Norm-Installer-EXE.bat`
orchestrates it.

## Build & Run

- **Make-Norm-Installer.py** — builds the installer EXE from source (NEW)
- **Build-Norm-Installer-EXE.bat** — simplified to 583 bytes (was 2583 in 1.3.6)
- **Run-Norm-Installer.bat** — source run

## Unique to this version

- **Make-Norm-Installer.py** — dedicated EXE builder (47,961 bytes)
- Build bat simplified — the heavy lifting moved to the Python builder
- Pre-release Norm 0.52.6 package

## Regressions vs later versions

- No `installer_environment.py` (arrives 1.6.6)
- No plugin handling
- No config snapshot / rollback
- No headless mode

## Progressions vs 1.3.6

- +Make-Norm-Installer.py (dedicated EXE builder)
- +2 functions
- Build pipeline split into two stages
