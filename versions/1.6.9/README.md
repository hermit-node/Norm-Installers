# Norm Installer 1.6.9 (Unified)

**Commit:** not in git history — recovered from the build workspace
**Source:** `D:\LOCAL_Share\Code Projects\n_temp\Norm-build-0.53.20\installer-1.6.9-build`
**Files:** Norm-Installer.py, installer_environment.py, Norm-Installer.spec
**Lines:** 3092 | **Schema:** 1
**SHA-256 (Norm-Installer.py):** `e410b1b8a9042096b991d90ab4e4b6453dee1453774bedc6f5e54414742263bf`

## What this is

The one version the archive was missing. The `installer_manifest.md` in
`n_temp\installer_versions` states it plainly: **"1.6.3 and 1.6.9 do not
exist in git history."** This folder fills the 1.6.9 gap. It sits exactly
between 1.6.8 and 1.6.10 in size and line count:

| Version | Norm-Installer.py | Lines |
|---------|-------------------|-------|
| 1.6.8   | 117,989 B         | 2646  |
| **1.6.9** | **148,600 B**   | **3092** |
| 1.6.10  | 151,554 B         | 3142  |

So 1.6.9 is a real, distinct iteration — not a version-string-only
duplicate of its neighbours. It carries most of the growth that 1.6.10
finishes off, but predates 1.6.10's PyInstaller-spec build-system rewrite.

## Build & Run

- **Norm-Installer.spec** — PyInstaller specification (715 bytes, same size
  as 1.6.10's). Present here, so the spec-based build was already in play
  by 1.6.9.
- The build workspace also shipped a compiled `dist/Norm-Installer.exe`
  (12.5 MB) and PyInstaller `build/` intermediates; those are build
  outputs, not source, so they are not copied into this version folder.

## Unique to this version

- **1.6.9-unified** — the missing middle step between 1.6.8 and 1.6.10.
- **~30,600 bytes / ~446 lines larger than 1.6.8** — a substantial code
  addition, not a relabel.
- **installer_environment.py at 16,569 B** — larger than 1.6.8's 12,449 B
  and smaller than 1.6.10's 18,686 B, again a genuine intermediate state.
- **Norm-Installer.spec present** — the spec-based build was already
  established before 1.6.10's full build-system rename.
- **Patch lineage preserved in the build workspace** — three generations of
  diff patches (`apply169` / `final169` / `real169` and their `*_env169`
  counterparts) plus `selftest.txt` / `installer-selftest.txt` /
  `exe-selftest.txt` markers document how this build was assembled and
  verified.

## Regressions vs later versions

- Lacks 1.6.10's renamed build entry points (`Build-Installer.bat` /
  `Build-Installer.py` / `Run-Installer.bat`) — those arrive in 1.6.10.
- No `norm-imprint.example.json` in this folder (present in 1.6.10).

## Provenance note

This folder was created by copying the three source files out of the
`Norm-build-0.53.20` build workspace, which is the only surviving copy of
the 1.6.9-unified installer. The workspace's `.diff` patch files, `.b64`
encodings, `dist/` EXE, and `build/` intermediates were left in place as
build artifacts; only the canonical source files are archived here,
matching the layout of the other version folders.
