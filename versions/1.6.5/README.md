# Norm Installer 1.6.5 (Unified)

**Commit:** `97e1413` — Norm 0.53.11 (recovered maintenance baseline)
**Files:** Norm-Installer.py, installer_environment.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat, norm-imprint.example.json
**Lines:** 2401 | **Classes:** 4 | **Functions:** 60
**Schema:** 1

## What this is

Near-identical to 1.6.4 (same line count, function count, and byte count:
105,886). The difference is the `INSTALLER_VERSION` string. This is a
**recovered maintenance baseline** — the commit message says "checkpoint:
recovered 0.53.11 maintenance baseline."

## Build & Run

- Same as 1.6.0–1.6.4

## Unique to this version

- **Recovered maintenance baseline** — checkpoint commit
- Norm 0.53.11 target
- Otherwise identical to 1.6.4

## Regressions vs later versions

- Same as 1.6.4 (no plugin handling, no headless mode)
- `installer_environment.py` is present in this folder but **not yet imported**
  by Norm-Installer.py — the import arrives in 1.6.6

## Progressions vs 1.6.4

- Norm target bumped to 0.53.11
- Version string change only
