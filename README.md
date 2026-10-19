# Norm Installer 1.6.17

## 1.6.17 compatibility repair (2026-10-19)

This revision preserves the distinct KHzz 1.6.17 changes (lean runtime freeze,
opt-in cache cleaning) and integrates the GitHub repair-branch changes.
The previous KHzz state is preserved as tag v1.6.17-khzz-pre-repair.

- Preserve installed host/port/path values when prefilling the installer;
  a saved full imprint is not itself evidence of a newly entered override.
- Prefer core/requirements.txt over legacy requirements-lock.txt.
- Default GUI mode: resolve newest mutually compatible dependencies.
  Alternate GUI mode: follow versions and constraints in requirements.txt.
- Reconcile installed plugin requirements.txt files and older built-in plugin
  runtime requirements, including vision_parse and GUI/browser plugins.
- Restore whole-venv inventory, compatibility dry-run, projected compatibility
  verification and delta-only installation from the 1.6.12 dependency logic.
- Protect the configured PyTorch/CUDA wheel from generic dependency upgrades.
- Verify Vision Parse OpenCV face APIs and ONNX Runtime imports before freezing;
  report missing ONNX CUDA provider while preserving CPU fallback.

Validation: Python compilation, focused tests, source-selection and builder
regression scripts passed in a temporary merge worktree. No full fresh-machine
Norm installation or ONNX CUDA inference smoke was performed.

## Build and launch from this source tree

- Run `Build-Norm-Installer-EXE.bat` to compile the installer using Windows Python 3.14 and PyInstaller. It **reuses PyInstaller's build cache** by default; add `--clean` only if a stale/corrupted cache requires a clean rebuild.
- Run `Run-Norm-Installer.bat` to launch the compiled installer, or the Python source if no built EXE exists.
- `Build-Installer.bat` and `Run-Installer.bat` remain equivalent short-name entry points.
- A successful build writes exactly one `Norm-Installer.exe` beside the launcher; it does not retain a `dist/` copy. PyInstaller build caches are still reused.
- The runner no longer forces the obsolete 0.53.20 source ZIP; supply `--source PATH` to override automatic ZIP/folder selection.
- `.gitignore` excludes Python bytecode, build directories, and generated installer EXEs. `.gitattributes` standardizes BAT line endings.
- Git tags v1.6.11, v1.6.12-initial, and v1.6.12 represent recovered historical source snapshots. They intentionally retain their original incomplete set of helper files.

Installer-owned Norm compilation is restored from the tested 1.6.12-unified
install-kit implementation. This fixes the 1.6.16 regression that incorrectly
required a build_script inside the source ZIP package manifest.

The installer still accepts either a source ZIP or an unpacked source folder,
including beside the installer, within Src, or in a peer Src directory.
Two GUI selectors and --source are available. ZIP checksum validation,
source safety checks, and operator plugin ingestion remain intact.

The actual r25 source package now passes --validate-only unchanged. Its
package manifest provides the version used for executable metadata instead
of inheriting potentially stale project.version in settings.ini.

Installer compilation runs internally with PyInstaller in the selected
runtime venv, writes a separate candidate, executes its --version check,
and only then promotes it to norm.exe. It does NOT run a source-supplied
builder. A full live installation has not been performed by these tests.

## 1.6.16 — ZIP or source folder selection

Change from 1.6.15: Select a Norm source ZIP or unpacked source folder,
without first rebuilding the source archive. Existing ZIP validation,
source synchronization, secret preservation and operator plugin ingestion remain.

## Package selection

The installer searches for valid packages in these locations:

- Source ZIP files beside the running installer.
- Unpacked folder alongside the installer, containing package-manifest.json.
- Src subfolder alongside the installer, or a selected parent containing Src.
- Peer Src directory beside the installer directory.
- Private .norm-local ZIPs retain priority for equivalent versions.

The GUI has Choose ZIP... and Choose source folder... buttons. CLI --source
accepts ZIP or directory. A folder is staged into a temporary copy before
installation, excluding Git metadata and bytecode; symlinks are rejected.
ZIP companion SHA256 checks remain enforced.

Validation without actually installing:
    python Norm-Installer.py --validate-only --source C:\path\to\Src
    python Norm-Installer.py --validate-only --source C:\path\to\Norm-source.zip

Some source archives (including the separately examined r25 sample) omit the
required build_script manifest key. As with 1.6.15, the installer rejects
such packages; source-folder support does not change the package contract.


**Base:** 1.6.10-unified (commit `cc8753e`, Norm 0.53.20)
**Files:** Norm-Installer.py, installer_environment.py, Build-Installer.bat, Build-Installer.py, Run-Installer.bat, Norm-Installer.spec, norm-imprint.example.json, plugins/
**INSTALLER_VERSION:** `1.6.15`

## What this is

1.6.15 is 1.6.10 with one new capability: **operator plugin ZIP ingestion**.
Drop `.zip` files into the `plugins/` subfolder alongside the installer,
and they get extracted into the installed Norm's `plugins/` directory
during install. No more rebuilding the main Norm source portable ZIP just
to change which plugins ship.

## The new feature: `plugins/` folder

- **Location:** `1.6.15/plugins/` (sits next to Norm-Installer.py, or one
  level above the built EXE in `dist/`).
- **What goes in it:** `.zip` files, each containing one plugin (or a
  flat set of files that become one plugin folder).
- **What happens:** `_ingest_operator_plugins()` runs after the main
  source sync and public-plugin reconciliation. It scans `plugins/` for
  `*.zip`, validates members against path traversal, and extracts each
  into `<target>/plugins/`.
- **Layout handling:**
  - Single top-level directory in the ZIP → extracted as that directory
    under `target/plugins/`.
  - Flat / multi-root ZIP → extracted under `target/plugins/<zip_stem>/`.
- **Idempotent:** existing files are overwritten, so re-running with
  updated ZIPs refreshes the installed copy.
- **Safe:** path-traversal members are rejected; empty ZIPs are skipped
  with a warning; non-`.zip` files are ignored.

### Why it matters

Before 1.6.15, every plugin you wanted included had to be baked into the
main Norm source portable ZIP. That meant a full source rebuild every time
the plugin set changed. Now the plugin set is a folder of ZIPs you can
swap without touching the source package.

## Build & Run

- **Build-Installer.bat** — entry point (176 bytes)
- **Build-Installer.py** — PyInstaller spec-based build (1,101 bytes)
- **Norm-Installer.spec** — PyInstaller specification (715 bytes)
- **Run-Installer.bat** — run script (398 bytes)

No build-script changes were needed for the plugins feature: the
`plugins/` folder is a runtime concern (read at install time), not a
build-time concern. The PyInstaller spec bundles the installer code;
the `plugins/` folder is read from disk at install time.

**Where the installer looks for `plugins/`:** the build drops the EXE
into `dist/` (see `Build-Installer.py`), while `plugins/` lives in the
installer source folder one level up. `_ingest_operator_plugins()`
checks the EXE's own directory first, then its parent, so the feature
works whether you run the EXE straight from `dist/` or move it next to
`plugins/`.

## Unique to this version (vs 1.6.10)

- **`_ingest_operator_plugins()`** — new function (~78 lines) that scans
  the installer's `plugins/` folder for ZIPs and extracts them into the
  target's `plugins/` directory.
- **`plugins/` folder** — new subfolder with `.gitkeep` and a usage
  README.
- **`INSTALLER_VERSION`** bumped from `"1.6.10-unified"` to `"1.6.15"`.
- **Call site** in `install_norm()` — `_ingest_operator_plugins()` is
  invoked after `_reconcile_public_plugins()` and before the sync
  summary log.

## Regressions vs 1.6.10

- None. All 1.6.10 functionality is preserved. The new function is
  additive and runs after the existing plugin reconciliation.

## Progressions vs 1.6.10

- +1 function (`_ingest_operator_plugins`)
- +1 folder (`plugins/` with `.gitkeep` and README)
- +1 call site in `install_norm()`
- Operator can now bundle plugins without rebuilding the source ZIP

## Inherited from 1.6.10

Everything else is identical to 1.6.10-unified:

- PyInstaller spec-based build
- Schema-2 plugin support (`_schema2_plugin_src_hash`,
  `_verify_schema2_plugin_folder`)
- Plugin source verification (SHA-256 hash of plugin src/ trees)
- Second-PC configuration (remote model integrations, opt-in)
- plugins.ini reconciliation (manifest-driven plugin settings)
- Config snapshots (retained to max 12)
- External .env (secrets remain in configured external .env)
- 142 plugin-related code references
- Full-backup restore support
- WeasyPrint/Pango runtime validation
- Public plugin reconciliation with pinned source fallback

## Variant note: the old "Installer 1.6.10" folder

A stray folder named `Installer 1.6.10` (with a `README.txt`) used to sit
beside the 1.6.10 folder. It was **not** a different code variant:

- `Norm-Installer.py` and `installer_environment.py` were **byte-identical
  after normalizing line endings** (the stray copy used LF, the canonical
  folder uses CRLF).
- Both copies declared `INSTALLER_VERSION = "1.6.10-unified"`.
- The stray copy had no .bat files, no `.spec`, no `Build-Installer.py`,
  and no `plugins/` folder — it was a partial drop of the same source.

It was merged into the 1.6.10 folder and deleted. See the 1.6.10 README
for the full story.

## Browse all installer versions

Installer versions are preserved by Git tags, not duplicate source directories. Source-only recoveries are tagged v1.6.11, v1.6.12-initial (pre-correction), and v1.6.12 (corrected). These tags do not imply newly compiled binaries. For an archived source file, use: git show v1.6.11:Norm-Installer.py. To export the recovered source, use: git archive --format=zip --output=Norm-Installer-1.6.11-source.zip v1.6.11. Published executable builds belong on GitHub Releases, not inside the source tree.
