# Norm Installer 1.6.12

This is the recovered sane 1.6.11 installer lineage with the narrow fixes that were originally intended, plus the desktop listener builder.

## Install source

The installer carries the **merged Norm 0.54.3 runway-fix + listener source** as its built-in fallback source. Its SHA-256 is:

`933c8ee7c5a172f22c075012f9778e43c0f6b83efd87f63a53c0cbbdb6d3b179`

A newer valid Norm source ZIP beside the installer can still win normal auto-selection; an explicitly selected `--source`/GUI package always remains available.

## 1.6.12 behavior

- **Installer-owned `norm.exe` build.** `tools/build_norm.py` is legacy input only: it is not installed, an existing installed copy is removed, and `build_script` is removed from the installed manifest. The installer owns PyInstaller invocation and Windows version-resource generation.
- **Version labels fixed.** Windows metadata accepts normal releases, single-letter revisions (`g`), letter iterations (`b2`, `g2`), and named prereleases (`beta2`, `rc1`, with or without separators).
- **One installed-venv Python compatibility decision.** The selected/system Python is checked against the package once; an existing venv is then checked once for the required Python major/minor and is reused or recreated.
- **Whole-venv dependency safety before changes.** The installer inventories every installed distribution once. Requirements belonging to packages outside Norm's managed set become resolver constraints, so an older package already in the venv can prevent an incompatible upgrade of one of its dependencies.
- **One resolver pass, then projected-environment verification.** Newest mode runs one pip dry-run resolver pass. The proposal is overlaid on the complete installed environment and every applicable `Requires-Dist` relationship is checked in memory before anything is installed. This verification is not another resolver pass.
- **Delta-only install.** Only packages whose resolved versions actually change are installed, using the already-resolved exact versions with `--no-deps`. `pip check` runs afterward as the final confirmation.
- **Exact package-lock mode is protected too.** If the lock already matches, pip resolution/install is skipped. If a repair is needed, the exact pins are dry-run resolved against the same whole-venv constraints and projected compatibility check before changes.
- **WeasyPrint/Pango self-heal.** The installed runtime gets one smoke check. A missing executable, missing DLL/Pango runtime, stale version, or failed PDF render invokes the package-pinned fetch helper with `--force`; the helper reconstructs the verified official runtime atomically and validates it.
- **No shadow Norm installation.** Temporary space is used only for package extraction/build artifacts. There is no second Norm installation or second dependency venv.

## Desktop listener

After installation, run:

`make-listener.bat`

(This is the only listener BAT shipped in the Norm source; it invokes `tools/build_listener.py` directly.)

It builds `Norm-Listener.exe`, a single desktop window containing **Runtime**, **Replies**, and **Prompt** terminal panes. Each pane owns a child role process; output is forwarded into the pane and lines entered in the pane are forwarded to that role's stdin.

The builder also writes `Norm-Listener.json` beside the EXE. That same-stem JSON is the listener's connection wiring: Norm/Activity endpoints, Redis DB/queue details, source host/version, and role routing. It intentionally contains no PostgreSQL password, model API key, or other secret. Move the EXE and JSON together.

## Build

Run `Build-Installer.bat` on Windows with PyInstaller available to the selected build Python. The PyInstaller spec embeds the merged 0.54.3 fallback source into the one-file installer. The listener builder is carried inside that Norm source ZIP.


## 1.6.12 corrections

- `Build-Installer.bat` builds `Norm-Installer.exe` and its `.sha256` beside the build script; PyInstaller dist/work directories are temporary.
- The bundled Norm 0.54.3 source owns exactly one listener command: `make-listener.bat`, backed by `tools/build_listener.py`.
- Legacy listener BAT aliases were removed.
- Torch remains separately managed by `environment.torch_version` + `torch_index_url` and is pinned as a protected exact dependency during generic resolution, so the resolver cannot replace a configured CUDA/local Torch build as a transitive upgrade.
- Legacy `tools/build_norm.py` is absent from the bundled Norm package; Norm EXE compilation remains installer-owned.

## 0.54.3 runway-fix merge

The embedded package also includes the source-level resource-activity 30-second grace-period and ingress-suppression tombstone fix, with `tools/test_resource_runway_suppression.py` regression coverage. The full change is preserved from `Norm-0.54.3-portable-source-runway-fix.zip`; no runtime files were taken from the older listener source. `make-listener.bat` invokes the existing venv Python and `tools/build_listener.py` directly.
