# Norm Installer 1.3.6

**Commit:** `a7e504c` — Norm 0.52.3
**Files:** Norm-Installer.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat
**Lines:** 1338 | **Classes:** 4 | **Functions:** 34
**Schema:** 1

## What this is

A significant jump from 1.0.0. Adds PostgreSQL and Redis connection setup,
SHA-256 verification of the source package, and connection testing before
install. The installer now validates the environment before touching the
target directory.

## Build & Run

- **Build-Norm-Installer-EXE.bat** — PyInstaller build (larger than 1.0.0's, 2583 bytes)
- **Run-Norm-Installer.bat** — source run

## Unique to this version

- **PostgreSQL setup** — creates database, runs migrations
- **Redis setup** — configures Memurai/Redis connection
- **SHA-256 verification** — validates the portable-source ZIP before install
- **Connection testing** — checks Postgres/Redis reachability pre-install
- **PATCH-NOTES.txt** — first appearance of patch notes in the repo

## Regressions vs later versions

- Still no `Make-Norm-Installer.py` (arrives 1.4.0)
- No `installer_environment.py` (arrives 1.6.6)
- No plugin handling
- No config snapshot / rollback
- No headless mode

## Progressions vs 1.0.0

- +PostgreSQL, +Redis, +SHA-256 verify, +connection test
- ~430 more lines, ~11 more functions
