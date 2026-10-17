# Norm Installer 1.0.0

**Commit:** `f16dad2` — Norm 0.52.0
**Files:** Norm-Installer.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat
**Lines:** 905 | **Classes:** 4 | **Functions:** 23
**Schema:** 1

## What this is

The first version of the Norm installer. A single Python file that takes a
portable-source ZIP and unpacks it into a target directory. No venv, no
PostgreSQL, no Redis — just file extraction and a basic Python environment
setup.

## Build & Run

- **Build-Norm-Installer-EXE.bat** — runs PyInstaller to produce a standalone EXE
- **Run-Norm-Installer.bat** — runs the installer from source (no EXE needed)

Both expect the portable-source ZIP to sit in the same directory.

## Unique to this version

- Simplest possible installer: extract ZIP → create venv → done
- No connection testing, no SHA-256 verification of the source package
- No PostgreSQL or Redis setup
- No `Make-Norm-Installer.py` (that arrives in 1.4.0)

## Regressions vs later versions

- No `installer_environment.py` (arrives 1.6.6)
- No PyInstaller `.spec` file (arrives 1.6.10)
- No plugin handling
- No config snapshot / rollback
- No headless mode

## Progressions vs later versions

- Everything after this is a superset. 1.0.0 is the baseline.
