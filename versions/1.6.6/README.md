# Norm Installer 1.6.6 (Unified)

**Commit:** `e22d7ad` — Norm 0.53.14
**Files:** Norm-Installer.py, installer_environment.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat, norm-imprint.example.json
**Lines:** 2585 | **Classes:** 4 | **Functions:** 61
**Schema:** 1

## What this is

**First appearance of `installer_environment.py`** (12,448 bytes). This
extracts environment-specific logic (connection strings, paths, service
configuration) out of the main installer into a dedicated module. Also adds
migration support.

## Build & Run

- Same as 1.6.0–1.6.5

## Unique to this version

- **installer_environment.py** — NEW dedicated environment module
- **Migration support** — database schema migrations
- +1 function, +184 lines over 1.6.5
- Norm 0.53.14 target
- Full documentation suite (AUDIT.md, PUBLISH.md, RELEASE.md, SECURITY.md)

## Regressions vs later versions

- No plugin handling
- No headless mode
- No PyInstaller spec (arrives 1.6.10)

## Progressions vs 1.6.5

- +installer_environment.py (major architectural change)
- +migration support
- +1 function, +184 lines
