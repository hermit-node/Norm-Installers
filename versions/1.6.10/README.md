# Norm Installer 1.6.10 (Unified)

**Commit:** `cc8753e` — Norm 0.53.20 (current HEAD)
**Files:** Norm-Installer.py, installer_environment.py, Build-Installer.bat, Build-Installer.py, Run-Installer.bat, Norm-Installer.spec, norm-imprint.example.json
**Lines:** 3142 | **Classes:** 4 | **Functions:** 69
**Schema:** 1

## What this is

**Completely different build system.** The old Build-Norm-Installer-EXE.bat
and Run-Norm-Installer.bat are replaced by Build-Installer.bat +
Build-Installer.py + Norm-Installer.spec (PyInstaller spec-based build).
Gains 496 lines and 7 functions over 1.6.8.

## Build & Run

- **Build-Installer.bat** — new entry point (176 bytes)
- **Build-Installer.py** — PyInstaller spec-based build (1,101 bytes)
- **Norm-Installer.spec** — PyInstaller specification (715 bytes)
- **Run-Installer.bat** — new run script (398 bytes)

## Unique to this version

- **PyInstaller spec-based build** — Norm-Installer.spec (NEW)
- **Build-Installer.py** — dedicated build script (NEW)
- **Build-Installer.bat / Run-Installer.bat** — renamed from old .bat files
- **Schema-2 plugin support** — `_schema2_plugin_src_hash`, `_verify_schema2_plugin_folder`
- **Plugin source verification** — SHA-256 hash of plugin src/ trees
- **Second-PC configuration** — remote model integrations (opt-in)
- **plugins.ini reconciliation** — manifest-driven plugin settings
- **Config snapshots** — retained to max 12
- **External .env** — secrets remain in configured external .env
- +7 functions, +496 lines over 1.6.8
- **142 plugin-related code references** (vs 4 in 1.6.6–1.6.8)

## Regressions vs later versions

- None — this is the current HEAD

## Progressions vs 1.6.8

- +7 functions, +496 lines
- +PyInstaller spec-based build
- +Schema-2 plugin support
- +Second-PC / remote model configuration
- +plugins.ini reconciliation
- +Config snapshots (max 12)
- +External .env for secrets

## Variant note: the old "Installer 1.6.10" folder

A stray folder named `Installer 1.6.10` (with a `README.txt`) used to sit
beside this one. It was **not** a different code variant:

- `Norm-Installer.py` and `installer_environment.py` are **byte-identical
  after normalizing line endings** (the stray copy used LF, this folder uses
  CRLF). SHA-256 differs only because of the line-ending bytes.
- Both copies declare `INSTALLER_VERSION = "1.6.10-unified"` (line 24).
- The stray copy had no .bat files, no `.spec`, no `Build-Installer.py`, and
  no `plugins/` folder — it was a partial drop of the same 1.6.10-unified
  source.

Its `README.txt` claimed "Target package: Norm 0.53.21" and recorded a
Windows-built EXE:

- `C:\Users\KHzz\Downloads\Norm-Installer-1.6.10.exe`
- SHA-256: `8A23A8A93FD45A3EF72BF3F4E6735A333C3973E76825B2A91597527B7CDA80BE`

That EXE was built from this same 1.6.10-unified source; the "0.53.21"
target label was the package it was pointed at at build time (the installer
code itself carries no hardcoded target version — it installs whatever
source it is given). The stray folder has been merged into this one and
deleted, so this folder is the single canonical home for installer 1.6.10.
