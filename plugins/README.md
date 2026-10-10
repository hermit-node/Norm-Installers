# Operator Plugins Folder

Drop `.zip` files in here and the installer will extract them into the
installed Norm's `plugins/` directory during install.

## How it works

1. Place one or more `.zip` files in this folder.
2. Run the installer (built EXE or `python Norm-Installer.py`).
3. During install, after the main source sync and public-plugin
   reconciliation, the installer scans this folder for `*.zip` files
   and extracts each one into `<target>/plugins/`.

## ZIP layout

- **Single top-level directory** (e.g. `myplugin/plugin.json`,
  `myplugin/src/main.py`): extracted directly into `target/plugins/`,
  so the folder becomes `target/plugins/myplugin/`.
- **Flat / multiple top-level entries**: extracted into
  `target/plugins/<zip_stem>/` (the ZIP filename without extension).

## Rules

- Path-traversal members (`..`, absolute paths) are rejected.
- Empty ZIPs are skipped with a warning.
- Existing files are **overwritten**, so re-running the installer with
  updated ZIPs refreshes the installed copy.
- Non-`.zip` files in this folder are ignored.

## Why this exists

Before 1.6.15, any plugin you wanted bundled had to be inside the main
Norm source portable ZIP. That meant rebuilding the source package every
time you wanted to change the plugin set. Now you just drop a ZIP here —
no source rebuild needed.
