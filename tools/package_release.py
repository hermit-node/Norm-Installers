from __future__ import annotations

import argparse
import hashlib
import re
import subprocess
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(path: Path) -> str:
    result = hashlib.sha256()
    with path.open("rb") as source:
        for block in iter(lambda: source.read(1024 * 1024), b""):
            result.update(block)
    return result.hexdigest().upper()


def main() -> int:
    parser = argparse.ArgumentParser(description="Create the buildable installer source asset")
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=True)

    executable = ROOT / "Norm-Installer.exe"
    if not executable.is_file() or executable.stat().st_size < 1_000_000:
        raise SystemExit("Missing compiled Windows installer executable")

    main_source = (ROOT / "Norm-Installer.py").read_text(encoding="utf-8")
    match = re.search(r'^INSTALLER_VERSION[ ]*=[ ]*"([^"]+)"', main_source, re.M)
    if not match:
        raise SystemExit("Missing installer version")

    version = match.group(1)
    archive = output / f"Norm-Installer-{version}-source.zip"
    tracked = subprocess.check_output(
        ["git", "ls-files", "-z"], cwd=ROOT
    ).split(bytes([0]))

    with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as zf:
        for raw in tracked:
            if not raw:
                continue
            rel = raw.decode("utf-8")
            if rel.endswith(".exe") or "__pycache__" in rel or rel.startswith(".git/"):
                raise SystemExit(f"Unsafe tracked file: {rel}")
            src = ROOT / rel
            if src.is_symlink() or not src.is_file():
                raise SystemExit(f"Missing/unsafe source file: {rel}")
            zf.write(src, arcname=rel.replace(chr(92), "/"))

    required = ("Build-Installer.bat", "Run-Installer.bat", "Build-Installer.py",
                "Norm-Installer.py", "installer_environment.py", "Norm-Installer.spec")
    with zipfile.ZipFile(archive) as zf:
        missing = set(required) - set(zf.namelist())
        if missing:
            raise SystemExit(f"Source kit missing: {sorted(missing)}")

    checksums = output / "SHA256SUMS.txt"
    checksums.write_text(
        f"{sha256(executable)}  Norm-Installer.exe\n"
        f"{sha256(archive)}  {archive.name}\n",
        encoding="ascii", newline="\n",
    )
    print(f"Source asset: {archive} ({archive.stat().st_size} bytes)")
    print(f"Checksums: {checksums}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
