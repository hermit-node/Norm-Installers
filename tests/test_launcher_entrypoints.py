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
    workpaths=[]
    def fake_pyinstaller(args, *, cwd, check, env):
        assert args[1:4] == ["-m", "PyInstaller", "--noconfirm"]
        assert args[-1] == str(root / "Norm-Installer.spec")
        assert args[args.index("--distpath") + 1] == str(root)
        work = Path(args[args.index("--workpath") + 1])
        assert work.is_dir() and work.name.startswith("norm-installer-build-")
        assert env["PYTHONDONTWRITEBYTECODE"] == "1"
        workpaths.append(work)
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
    assert len(workpaths) == 1 and not workpaths[0].exists()
    assert (root / "Norm-Installer.exe").read_bytes() == payload
    assert not (root / "dist" / "Norm-Installer.exe").exists()
    assert not (root / "dist").exists()
    assert not (root / "Norm-Installer.exe.staging").exists()

    with patch.object(mod, "ROOT", root), patch.object(mod, "SPEC", root / "Norm-Installer.spec"),          patch.object(mod.subprocess, "run", side_effect=fake_pyinstaller),          patch.object(sys, "argv", ["Build-Installer.py", "--clean"]):
        mod.main()
    assert len(seen) == 2 and "--clean" in seen[1]
    assert len(workpaths) == 2 and all(not work.exists() for work in workpaths)

    # A failed build must also remove the work files and preserve an existing EXE.
    def failed_pyinstaller(args, *, cwd, check, env):
        work = Path(args[args.index("--workpath") + 1])
        assert work.is_dir()
        workpaths.append(work)
        raise subprocess.CalledProcessError(3, args)
    with patch.object(mod, "ROOT", root), patch.object(mod, "SPEC", root / "Norm-Installer.spec"), \
         patch.object(mod.subprocess, "run", side_effect=failed_pyinstaller), \
         patch.object(sys, "argv", ["Build-Installer.py"]):
        try:
            mod.main()
        except subprocess.CalledProcessError:
            pass
        else:
            raise AssertionError("Failed build must propagate an error")
    assert len(workpaths) == 3 and not workpaths[-1].exists()
    assert (root / "Norm-Installer.exe").read_bytes() == payload

print("PASS installer BAT compatibility, automatic source selection, ignored artifacts")
print("PASS single EXE, disposable workpath cleaned on success/failure, no dist duplicate")
