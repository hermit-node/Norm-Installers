Norm Installer 1.6.11-unified source
Target package: Norm 0.54.0-beta2

Key behavior:
- System Python is used to create the target .venv only when it is missing or explicitly recreated.
- Existing target .venv is reused.
- Dependency mode defaults to Newest available, matching 1.6.10: pip resolves/upgrades the package-lock distribution set in the existing target .venv, followed by pip check.
- Existing valid WeasyPrint/Pango runtime is verified and left untouched.
- Managed plugins are SHA-checked first and left untouched when they already match.
- norm.exe is built by installer-owned PyInstaller logic; package-side tools/build_norm.py or tools/exe_build.py is not required.
- Versions such as 0.54.0-beta2 and 0.54.0b are accepted for Windows executable metadata.
- A new norm.exe candidate is validated beside core/norm.exe before replacing the existing executable.

Norm-0.54.0-beta2-portable-source.zip
SHA-256: FD33AF644793FCF7CEA6B28769652DEF92A45F0F98F356143A71ABF25E575F67

Norm-Installer-1.6.11.exe
SHA-256: C6510E8932797D2A9545C3D6709FADA58BA812EF710E2B412AC6EBE0B1947AAB
