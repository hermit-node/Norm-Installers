# Norm Installer 1.4.1

**Commit:** `a88c9a0` — Norm 0.52.6
**Files:** Norm-Installer.py, Make-Norm-Installer.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat
**Lines:** 1338 | **Classes:** 4 | **Functions:** 36
**Schema:** 1

## What this is

A hotfix release. Same line count and function count as 1.4.0, but the
Norm-Installer.py SHA-256 differs — the change is a **retry-delete recovery
hotfix** (per the commit message). Also introduces `PATCH-AND-AUDIT-NOTES.txt`.

## Build & Run

- Same as 1.4.0: Make-Norm-Installer.py + Build-Norm-Installer-EXE.bat + Run-Norm-Installer.bat

## Unique to this version

- **Retry-delete recovery hotfix** — fixes a bug where failed deletions weren't retried
- **PATCH-AND-AUDIT-NOTES.txt** — new audit trail file

## Regressions vs later versions

- Same as 1.4.0 (no installer_environment.py, no plugins, no headless)

## Progressions vs 1.4.0

- Bug fix only: retry-delete recovery
- +PATCH-AND-AUDIT-NOTES.txt
- Norm-Installer.py byte count identical (54,189) but SHA differs

## Known quirk

- `Run-Norm-Installer.bat` error message references `Norm-Installer-1.3.8.exe`
  (a stale leftover from the 1.3.x era). The bat itself still works — it runs
  `Norm-Installer.py` via Python; the 1.3.8 reference is only in the fallback
  echo text.
