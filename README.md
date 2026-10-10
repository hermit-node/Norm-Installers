# Norm Installer 1.6.8 (Unified)

**Commit:** `7e60438` — Norm 0.53.18 (canonical public-safe source)
**Files:** Norm-Installer.py, installer_environment.py, norm-imprint.example.json, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat
**Lines:** 2646 | **Classes:** 4 | **Functions:** 62
**Schema:** 1

## What this is

**Canonical branch** — different file layout from the private branch.
No build_source_package.py, no test_installer.py. The build/run scripts
use the same cached-venv PyInstaller approach as 1.6.0–1.6.7.

## Build & Run

- **Build-Norm-Installer-EXE.bat** — cached-venv PyInstaller build (same as 1.6.0–1.6.7)
- **Run-Norm-Installer.bat** — runs the installer from source or EXE
- Norm-Installer.py and installer_environment.py are the core files

## Unique to this version

- **Canonical branch layout** — different from private branch
- Norm 0.53.18 public-safe source
- +28 lines over 1.6.7

## Regressions vs later versions

- No PyInstaller spec (arrives 1.6.10)
- No Build-Installer.bat/py (arrives 1.6.10)

## Progressions vs 1.6.7

- Canonical branch (public-safe)
- +28 lines
- Different file layout
