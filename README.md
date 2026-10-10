# Norm Installer 1.5.0 (Unified)

**Commit:** `0a37bb6` — Norm 0.53.8
**Files:** Norm-Installer.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat, test_unified_installer.py
**Lines:** 1616 | **Classes:** 4 | **Functions:** 44
**Schema:** 1

## What this is

The first "unified" installer. `Make-Norm-Installer.py` is **removed** — the
EXE building logic is folded back into the main installer or the build bat.
`test_unified_installer.py` appears for the first time.

## Build & Run

- **Build-Norm-Installer-EXE.bat** — simplified to 407 bytes (was 583)
- **Run-Norm-Installer.bat** — simplified to 329 bytes (was 437)
- **test_unified_installer.py** — NEW test suite

## Unique to this version

- **"unified" suffix** introduced in INSTALLER_VERSION
- **Make-Norm-Installer.py REMOVED** — build logic consolidated
- **test_unified_installer.py** — first dedicated test file
- +4 functions, +206 lines over 1.4.16

## Regressions vs later versions

- No `installer_environment.py` (arrives 1.6.6)
- No `build_source_package.py` (arrives 1.6.0)
- No plugin handling
- No headless mode

## Progressions vs 1.4.16

- +4 functions, +206 lines
- Build system simplified (Make-Norm-Installer.py removed)
- Test suite added
