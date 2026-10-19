# Norm Installer 1.7.0

This release promotes the cumulative fixes from 1.6.17 into a public Windows installer.

- Settings: Operator-customized host, port, path and other machine values survive upgrades. Explicit new installer edits take precedence. Public package defaults do not include KHzz-specific ports.
- Dependencies: Newest mutually compatible packages by default, or versions from core/requirements.txt when selected. Full-venv verification, delta-only installs and legacy plugin requirements support, including Vision Parse OpenCV and ONNX Runtime. CUDA PyTorch is protected.
- Norm runtime: Still compiles core/norm.exe with lean imports, persistent Norm runtime build cache, candidate version check and atomic promotion.
- Installer: Build-Installer.bat creates one portable Norm-Installer.exe beside the build/run scripts. PyInstaller build work is removed on success and failure. No dist duplicate.
- Portability: Use Norm-Installer.exe with a separate Norm portable-source ZIP or unpacked source folder, selected through the GUI or --source. The Norm runtime source is not embedded in the installer.

Assets: Norm-Installer.exe, Norm-Installer-1.7.0-source.zip (complete buildable installer sources and BAT files), SHA256SUMS.txt.

Validated with the Python 3.14 test suite and compiled Windows executable self-test. A full fresh-PC Norm installation and ONNX GPU inference are not certified by these checks.
