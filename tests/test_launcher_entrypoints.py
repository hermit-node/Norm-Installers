from __future__ import annotations

import importlib.util
import subprocess
import sys
import tempfile
from pathlib import Path
from unittest.mock import patch

repo = Path(__file__).resolve().parents[1]
build = importlib.util.spec_from_file_location("norm_installer_builder", repo / "Build-Installer.py")
assert build and build.loader
mod = importlib.util.module_from_spec(build)
build.loader.exec_module(mod)

assert (repo / "Build-Norm-Installer-EXE.bat").is_file()
assert (repo / "Run-Norm-Installer.bat").is_file()
assert "Build-Installer.bat" in (repo / "Build-Norm-Installer-EXE.bat").read_text()
assert "Run-Installer.bat" in (repo / "Run-Norm-Installer.bat").read_text()
launcher = (repo / "Run-Installer.bat").read_text()
assert "--source" not in launcher  # optional CLI --source is forwarded via %*
assert "%*" in launcher
ignore = (repo / ".gitignore").read_text()
assert "__pycache__/" in ignore and "Norm-Installer.exe" in ignore

with tempfile.TemporaryDirectory(prefix="norm-installer-launcher-") as td:
    root = Path(td)
    (root / "Norm-Installer.spec").write_text("test fixture", encoding="utf-8")
    payload = b"MZ dummy executable bytes"

    seen=[]
    def fake_pyinstaller(args, *, cwd, check):
        assert args[1:4] == ["-m", "PyInstaller", "--noconfirm"]
        assert args[-1] == str(root / "Norm-Installer.spec")
        assert args[args.index("--distpath") + 1] == str(root)
        seen.append(args)
        assert cwd == root and check
        output = root / "Norm-Installer.exe"
        output.write_bytes(payload)
        return subprocess.CompletedProcess(args=args, returncode=0)

    # Simulate the old builder's obsolete second copy.
    (root / "dist").mkdir()
    (root / "dist" / "Norm-Installer.exe").write_bytes(b"old duplicate")
    with patch.object(mod, "ROOT", root), patch.object(mod, "SPEC", root / "Norm-Installer.spec"),          patch.object(mod.subprocess, "run", side_effect=fake_pyinstaller),          patch.object(sys, "argv", ["Build-Installer.py"]):
        mod.main()

    assert len(seen) == 1 and "--clean" not in seen[0]
    assert (root / "Norm-Installer.exe").read_bytes() == payload
    assert not (root / "dist" / "Norm-Installer.exe").exists()
    assert not (root / "dist").exists()
    assert not (root / "Norm-Installer.exe.staging").exists()

    with patch.object(mod, "ROOT", root), patch.object(mod, "SPEC", root / "Norm-Installer.spec"),          patch.object(mod.subprocess, "run", side_effect=fake_pyinstaller),          patch.object(sys, "argv", ["Build-Installer.py", "--clean"]):
        mod.main()
    assert len(seen) == 2 and "--clean" in seen[1]

print("PASS installer BAT compatibility, automatic source selection, ignored artifacts")
print("PASS one installer EXE beside launcher, no dist duplicate, cache reusable")
