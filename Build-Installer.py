from __future__ import annotations

import hashlib
import subprocess
import sys
import tempfile
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SPEC = ROOT / "Norm-Installer.spec"
EXPECTED_SELFTEST = "ok 1.6.12-unified auto-source listener-builder=True version-parser=True bundled-source=0.54.3 projected-compat=True installer-owned-build=True"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest().upper()


def main() -> int:
    final_exe = ROOT / "Norm-Installer.exe"
    with tempfile.TemporaryDirectory(prefix="norm-installer-build-") as temp_name:
        temp = Path(temp_name)
        dist = temp / "dist"
        work = temp / "work"
        subprocess.run(
            [
                sys.executable, "-m", "PyInstaller", "--clean", "--noconfirm",
                "--distpath", str(dist), "--workpath", str(work), str(SPEC),
            ],
            cwd=ROOT,
            check=True,
        )
        built = dist / "Norm-Installer.exe"
        if not built.is_file():
            raise SystemExit("Build completed but temporary Norm-Installer.exe is missing")

        with tempfile.TemporaryDirectory(prefix="norm-installer-selftest-") as test_name:
            result = Path(test_name) / "selftest.txt"
            subprocess.run([str(built), "--self-test-file", str(result)], cwd=ROOT, check=True)
            text = result.read_text(encoding="utf-8-sig").strip()
            if text != EXPECTED_SELFTEST:
                raise SystemExit(f"Installer self-test mismatch: {text!r}")

        shutil.copy2(built, final_exe)

    digest = sha256(final_exe)
    companion = final_exe.with_name(final_exe.name + ".sha256")
    companion.write_text(f"{digest.lower()}  {final_exe.name}\n", encoding="utf-8", newline="\n")
    print(f"EXE={final_exe}")
    print(f"SHA256={digest}")
    print(f"SELFTEST={EXPECTED_SELFTEST}")
    print(f"CHECKSUM={companion}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
