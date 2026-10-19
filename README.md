# Norm Installer 1.6.16 — corrected standalone installer

This installer consumes a compatible Norm portable-source ZIP or unpacked source folder. It sets up the Python environment, installs requirements, and builds `norm.exe` itself.

## Build and launch

- `Build-Norm-Installer-EXE.bat` or `Build-Installer.bat`: compile the installer.
- `Run-Norm-Installer.bat` or `Run-Installer.bat`: launch the installer.
- `Build-Installer.bat --clean`: clean PyInstaller caches only when specifically requested. Builds reuse caches otherwise.
- `Norm-Installer.py --validate-only --source PATH`: validate without installing.

The build scripts belong to the installer kit. Norm source packages do not need to contain a `build_script` manifest entry.

## Source discovery

Automatic discovery includes source ZIPs beside the installer, unpacked source folders, folders containing a `Src` child, a sibling `Src` folder, and private `.norm-local` packages. GUI selectors and `--source` accept ZIP files or directories. Source checksum checks, path traversal safeguards, and operator plugin ZIP ingestion are preserved.

## Compiled runtime

The installer uses its configured Python venv and PyInstaller to build `norm.exe` into a candidate, verifies its version, and promotes it after successful validation. Normal imported dependencies are collected as required. Unconditional whole-package collection of PDF/media/cryptography libraries is disabled. Shared source modules, plugins, and tools remain separate files accessible to other processes. PyInstaller work/spec caches are reused rather than cleaned by default.

## Validation

Source discovery, checksum handling, launcher modes, `--clean` opt-in, and the installer-owned Norm build command were tested with isolated fixtures. The installer executable was compiled separately; no live Norm files or task state were modified. A full fresh-machine installation has not been performed.

Based on the historical 1.6.16 source, with isolated corrections to the installer-owned compiler and launch kit.
