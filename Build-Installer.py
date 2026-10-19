from __future__ import annotations
import argparse, hashlib, os, subprocess, sys, tempfile
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
    # Keep one published EXE and make all PyInstaller work files disposable.
    # The temp workpath prevents reuse and is removed on success or failure.
    with tempfile.TemporaryDirectory(prefix='norm-installer-build-') as work:
        command=[sys.executable,'-m','PyInstaller','--noconfirm',
                 '--distpath',str(ROOT),'--workpath',work]
        if args.clean:  # Optional global PyInstaller cache purge, not required.
            command.append('--clean')
        command.append(str(SPEC))
        subprocess.run(command,cwd=ROOT,check=True,
                       env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    exe=ROOT/'Norm-Installer.exe'
    if not exe.is_file(): raise SystemExit('Build completed but Norm-Installer.exe is missing beside the build scripts')
    digest=sha256(exe)
    print(f'EXE={exe}')
    print(f'SHA256={digest}')
    print(f'REFERENCE={EXPECTED}')
    print('REFERENCE_MATCH='+str(digest==EXPECTED))
    if args.verify_reference and digest!=EXPECTED: raise SystemExit(2)
    # Remove only the obsolete generated duplicate from earlier versions.
    old_copy=ROOT/'dist'/'Norm-Installer.exe'
    if old_copy.is_file():
        old_copy.unlink()
        try: old_copy.parent.rmdir()  # only if dist contains no other files
        except OSError: pass
    print(f'LAUNCHABLE_EXE={exe}')
if __name__=='__main__': main()
