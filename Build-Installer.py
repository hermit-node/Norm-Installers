from __future__ import annotations
import argparse, hashlib, os, shutil, subprocess, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parent
SPEC=ROOT/'Norm-Installer.spec'
EXPECTED='AB3BEF2CBCBEB94499FE1D62B410C1A7D609DAC12D2E1014C7EB008423B4E96A'
def sha256(p: Path)->str:
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest().upper()
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--verify-reference',action='store_true')
    ap.add_argument('--clean',action='store_true',help='Explicitly discard the PyInstaller build cache')
    args=ap.parse_args()
    command=[sys.executable,'-m','PyInstaller','--noconfirm']
    if args.clean:
        command.append('--clean')
    command.append(str(SPEC))
    subprocess.run(command,cwd=ROOT,check=True)
    exe=ROOT/'dist'/'Norm-Installer.exe'
    if not exe.is_file(): raise SystemExit('Build completed but dist/Norm-Installer.exe is missing')
    digest=sha256(exe)
    print(f'EXE={exe}')
    print(f'SHA256={digest}')
    print(f'REFERENCE={EXPECTED}')
    print('REFERENCE_MATCH='+str(digest==EXPECTED))
    if args.verify_reference and digest!=EXPECTED: raise SystemExit(2)
    # Publish a launchable EXE beside the source/package discovery roots.
    # The PyInstaller dist/ output is retained; no second build is performed.
    staged=ROOT/'Norm-Installer.exe.staging'
    target=ROOT/'Norm-Installer.exe'
    try:
        shutil.copy2(exe,staged)
        if sha256(staged)!=digest: raise SystemExit('Staged installer checksum mismatch')
        os.replace(staged,target)
    finally:
        staged.unlink(missing_ok=True)
    print(f'LAUNCHABLE_EXE={target}')
if __name__=='__main__': main()
