# Norm Installer 1.6.0 (Unified)

**Commit:** `0c668b4` — Norm 0.53.9
**Files:** Norm-Installer.py, Build-Norm-Installer-EXE.bat, Run-Norm-Installer.bat, norm-imprint.example.json
**Lines:** 2291 | **Classes:** 4 | **Functions:** 56
**Schema:** 1

## What this is

A major leap. Gains 675 lines and 12 functions over 1.5.0. Adds Redis,
Ollama, and imprint handling. The repo layout changes significantly —
`src/`, `tests/`, `tools/` directories appear, along with `AUDIT.md`,
`PUBLISH.md`, `RELEASE.md`, `SECURITY.md`, and `SHA256SUMS.txt`.

## Build & Run

- **Build-Norm-Installer-EXE.bat** — 1,156 bytes (was 407)
- **Run-Norm-Installer.bat** — 421 bytes (was 329)
- **norm-imprint.example.json** — NEW (imprint configuration example)

## Unique to this version

- **Redis setup** — full Redis/Memurai configuration
- **Ollama integration** — local model server setup
- **Imprint handling** — non-secret imprint JSON for identity
- **norm-imprint.example.json** — example configuration
- **Repo restructure** — src/, tests/, tools/ directories
- **AUDIT.md, PUBLISH.md, RELEASE.md, SECURITY.md** — documentation suite
- +12 functions, +675 lines over 1.5.0

## Regressions vs later versions

- No `installer_environment.py` (arrives 1.6.6)
- No `build_source_package.py` (arrives 1.6.0 per manifest but not in git tree)
- No plugin handling
- No headless mode

## Progressions vs 1.5.0

- +12 functions, +675 lines
- +Redis, +Ollama, +imprint
- Repo restructured with src/tests/tools
- Documentation suite added
