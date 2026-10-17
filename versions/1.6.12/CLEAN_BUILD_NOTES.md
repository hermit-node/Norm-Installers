# Clean build notes

Baseline: recovered `Norm-Installer(1).py` reporting `1.6.11-unified`, plus its matching `installer_environment.py`.

This 1.6.12 keeps the sane in-place installer lineage. It does **not** recreate the abandoned shadow-install architecture.

Targeted changes:

- move `norm.exe` build/version-resource logic into the installer and refuse to install legacy `tools/build_norm.py`;
- support the release-label forms that previously tripped the build (`b`, `b2`, `beta2`, `rc1`, letter revisions, etc.);
- inventory the existing venv once and constrain newest-package resolution by the active requirements of unrelated/older installed packages;
- perform one pip dry-run resolution, one projected full-environment metadata verification, one delta install, then one final `pip check`;
- keep WeasyPrint/Pango reconstruction via the package-pinned verified fetch helper;
- embed the exact uploaded Norm 0.54.3 portable source as the installer's fallback source;
- install `make-listener.bat` / `tools/build_listener.py`, which builds a three-pane `Norm-Listener.exe` plus same-stem JSON wiring file.

No temporary Norm clone, temporary dependency clone, or whole-tree fake-install comparison/promotion pipeline is used.


### Correction pass
- Bundled Norm 0.54.3 SHA-256: `933c8ee7c5a172f22c075012f9778e43c0f6b83efd87f63a53c0cbbdb6d3b179`
- One installed listener BAT only: `C:\Norm\make-listener.bat`.
- Torch exact configured version is protected from generic resolver changes.
- Installer build output is root-level; temporary PyInstaller dist/work are automatically deleted.

### Runway-fix merged source
- Embedded Norm 0.54.3 source: `933c8ee7c5a172f22c075012f9778e43c0f6b83efd87f63a53c0cbbdb6d3b179` SHA-256.
- Preserved prompt-ingress 30-second resource-only grace window and suppressed-prompt tombstones, plus the regression test.
- `make-listener.bat` directly invokes `tools/build_listener.py`; the previous dangling `make_listener.bat` alias has been eliminated.
- Removed the obsolete `make_sse.bat`; no changes to the installer-owned `norm.exe` build or dependency resolution.
