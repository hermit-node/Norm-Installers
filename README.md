# Norm Installer 1.6.16

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

## 1.6.15 — Operator plugin ZIP ingestion

**Base:** 1.6.10-unified (commit `cc8753e`, Norm 0.53.20)
**Files:** Norm-Installer.py, installer_environment.py, Build-Installer.bat, Build-Installer.py, Run-Installer.bat, Norm-Installer.spec, norm-imprint.example.json, plugins/
**Version at this historical checkpoint:** `1.6.15`

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

The complete source snapshot tree is in versions/README.md. Original release tags and historical commits are preserved. Source-only 1.6.11 and 1.6.12 revisions were added without compiled executables or bundled Norm source ZIPs.
