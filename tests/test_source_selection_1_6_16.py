from __future__ import annotations
from pathlib import Path
import hashlib, importlib.util, json, subprocess, sys, tempfile, zipfile, os

repo=Path(__file__).resolve().parents[1]
candidate=repo/'Norm-Installer.py'
sys.path.insert(0,str(repo))
import py_compile
py_compile.compile(str(candidate),doraise=True)
spec=importlib.util.spec_from_file_location('norm_installer_candidate',str(candidate))
mod=importlib.util.module_from_spec(spec)
sys.modules[spec.name]=mod
spec.loader.exec_module(mod)
assert mod.INSTALLER_VERSION=='1.6.16'

def package(root,version='0.55.10r25'):
 root.mkdir(parents=True,exist_ok=True)
 m={'package_schema':1,'package_type':'portable-source','name':'Norm','version':version,
    'entrypoint':'core/main.py','settings':'config/settings.ini',
    'requirements_lock':'tools/requirements-lock.txt'}
 for rel,content in {
    'core/main.py':'print("fixture")\n',
    'config/settings.ini':'[environment]\nvenv_path = .venv\n',
    'tools/requirements-lock.txt':'idna==3.10\n',
    'package-manifest.json':json.dumps(m)
 }.items():
  p=root/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(content,encoding='utf8')
 return m
def make_zip(root,archive,prefix=''):
 with zipfile.ZipFile(archive,'w') as z:
  for p in root.rglob('*'):
   if p.is_file():z.write(p, prefix+p.relative_to(root).as_posix())
def test(label,fn):
 fn();print('PASS',label,flush=True)

with tempfile.TemporaryDirectory(prefix='norm-1.6.16-validate-') as tmp:
 b=Path(tmp)
 installer=b/'Installer'
 installer.mkdir()
 direct=installer/'unpacked-source'
 package(direct,'0.55.10r24')
 zi=installer/'Norm-0.55.10r25-portable-source.zip'
 make_zip(direct,zi)
 def test_zip():
  info=mod.inspect_package(zi)
  assert info.version=='0.55.10r24'
  assert info.source_zip==zi.resolve()
  assert info.zip_root==mod.PurePosixPath('.')
  assert mod._source_requirements_text(zi).replace('\r\n','\n')=='idna==3.10\n'
  a=mod._extract_package(info,b/'extracted-zip')
  assert (a/'core/main.py').is_file()
 test('ZIP inspect, extract, requirements',test_zip)
 def test_folder():
  info=mod.inspect_package(direct)
  assert info.source_zip==direct.resolve()
  assert info.version=='0.55.10r24'
  assert mod._source_requirements_text(direct).replace('\r\n','\n')=='idna==3.10\n'
  (direct/'__pycache__').mkdir(exist_ok=True)
  (direct/'__pycache__'/'junk.pyc').write_bytes(b'dummy')
  (direct/'.git').mkdir(exist_ok=True)
  (direct/'.git'/'config').write_text('secret-like git config',encoding='utf8')
  staging=b/'extracted-folder'
  a=mod._extract_package(info,staging)
  assert (a/'core/main.py').read_text()=='print("fixture")\n'
  assert not (a/'.git').exists() and not (a/'__pycache__').exists()
 test('unpacked folder inspect, stage without Git/bytecode',test_folder)
 def test_wrapped():
  pkg=installer/'WithSrc'
  package(pkg/'Src','0.55.10r26')
  assert mod.inspect_package(pkg).version=='0.55.10r26'
  assert mod.inspect_package(pkg).source_zip==pkg/'Src'
 test('parent with Src contents',test_wrapped)
 def test_autodetect():
  sources=mod.list_local_sources(installer)
  assert (installer/'WithSrc').resolve() in sources,sources
  assert direct.resolve() in sources,sources
  assert zi.resolve() in sources,sources
  assert mod.find_latest_source(installer)==(installer/'WithSrc').resolve(),sources
 test('automatic ZIP + folder discovery and version sort',test_autodetect)
 def test_sibling():
  other=b/'SecondInstaller';other.mkdir()
  s=b/'Src';package(s,'0.55.10r27')
  found=mod.list_local_sources(other)
  assert s.resolve() in found,found
  assert mod.find_latest_source(other)==s.resolve()
 test('peer Src sibling of installer directory',test_sibling)
 def test_private():
  private=installer/'.norm-local';private.mkdir()
  pkg=private/'higher.zip'
  make_zip(direct,pkg)
  # same version as ZIP: .norm-local wins
  assert mod.list_local_sources(installer).index(pkg.resolve())<mod.list_local_sources(installer).index(zi.resolve())
 test('.norm-local package priority retained',test_private)
 def test_sha():
  hashp=zi.with_name(zi.name+'.sha256')
  hashp.write_text(hashlib.sha256(zi.read_bytes()).hexdigest()+'  '+zi.name+'\n')
  assert mod.inspect_package(zi).version=='0.55.10r24'
  hashp.write_text('0'*64+'\n')
  try:mod.inspect_package(zi)
  except mod.InstallerError as exc:assert 'mismatch' in str(exc).lower()
  else:raise AssertionError('Checksum mismatch accepted')
 test('ZIP SHA-256 sidecar remains enforced',test_sha)
 def test_malicious():
  bad=installer/'bad';package(bad,'0.55.10r28')
  m=json.loads((bad/'package-manifest.json').read_text())
  m['entrypoint']='../outside.py'
  (bad/'package-manifest.json').write_text(json.dumps(m))
  try:mod.inspect_package(bad)
  except mod.InstallerError:pass
  else:raise AssertionError('directory traversal accepted')
 test('manifest traversal rejected for unpacked folder',test_malicious)
 def test_cli():
  done=subprocess.run([sys.executable,str(candidate),'--validate-only','--source',str(direct)],cwd=str(repo),capture_output=True,text=True)
  assert done.returncode==0,(done.stdout,done.stderr)
  parsed=json.loads(done.stdout)
  assert parsed['source_type']=='directory'
  assert parsed['version']=='0.55.10r24'
 test('headless --validate-only --source folder',test_cli)
print('ALL_INSTALLER_1_6_16_SELECTION_TESTS_PASSED')