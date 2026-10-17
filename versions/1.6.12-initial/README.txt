Norm Installer 1.6.12-unified source
Target package: Norm 0.54.0c

Delta from 1.6.11:
- config/plugins.ini is protected during in-place package synchronization.
- Existing plugins.ini therefore survives updates and remains available for installer/runtime reconciliation.
- No other installer behavior was intentionally changed.

Existing behavior retained:
- Existing target .venv is reused; system Python creates it only when missing or explicitly recreated.
- Dependency mode defaults to Newest available.
- Existing valid WeasyPrint/Pango is verified and left untouched.
- Managed plugins are SHA-checked first and left untouched when matching.
- norm.exe is built by installer-owned PyInstaller logic.
- Beta/letter versions such as 0.54.0c are accepted.
- Candidate norm.exe is validated before replacing the existing executable.

Norm-0.54.0c-portable-source.zip
SHA-256: AED69ACD5AD54288B684353CA3BD24E1E6E0ED7814A58C4A74396DE5407691DD

Norm-Installer-1.6.12.exe
SHA-256: B6787D5F7D304886B93D99FB6946D3D94C44A867AA0C316BE1EA66DB03BBAD99
