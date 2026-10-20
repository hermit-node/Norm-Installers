"""Installer-side CPU model hydration: opt-in network only during install."""
from __future__ import annotations

import importlib.util
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("norm_vision_installer", ROOT / "Norm-Installer.py")
installer = importlib.util.module_from_spec(spec)
import sys
sys.modules[spec.name] = installer
spec.loader.exec_module(installer)

class VisionInstallerHydrationTests(unittest.TestCase):
    def test_legacy_package_without_face_models_skips(self):
        with tempfile.TemporaryDirectory() as name:
            with patch.object(installer.subprocess, "run") as process:
                logs = []
                installer._ensure_vision_parse_models(Path("python"), Path(name), logs.append)
                process.assert_not_called()
                self.assertIn("legacy", logs[0].lower())

    def test_install_executes_pinned_model_hydration_and_cpu_load(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            module=root/"plugins"/"vision_parse"/"src"/"media_faces.py"
            module.parent.mkdir(parents=True)
            module.write_text("# test stub",encoding="utf-8")
            response=SimpleNamespace(returncode=0,stdout=json.dumps({"status":"downloaded","cpu_ready":True}),stderr="")
            with patch.object(installer.subprocess,"run",return_value=response) as process:
                logs=[]
                installer._ensure_vision_parse_models(Path("python"),root,logs.append)
            args=process.call_args.args[0]
            self.assertEqual(args[:3],["python","-B","-c"])
            self.assertIn("setup_models(approved=True)",args[3])
            self.assertIn("FaceDetectorYN.create",args[3])
            self.assertIn("FaceRecognizerSF.create",args[3])
            self.assertEqual(process.call_args.kwargs["cwd"],root)
            self.assertGreaterEqual(process.call_args.kwargs["timeout"],180)
            self.assertIn("downloaded",logs[0])

    def test_existing_models_are_reused_without_calling_setup(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            module=root/"plugins"/"vision_parse"/"src"/"media_faces.py"
            module.parent.mkdir(parents=True)
            module.write_text("# test stub",encoding="utf-8")
            result=SimpleNamespace(returncode=0,stdout='{"status":"reused","cpu_ready":true}',stderr="")
            with patch.object(installer.subprocess,"run",return_value=result):
                log=[]
                installer._ensure_vision_parse_models(Path("python"),root,log.append)
                self.assertIn("reused",log[-1])

    def test_offline_download_failure_is_explicit(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            module=root/"plugins"/"vision_parse"/"src"/"media_faces.py"
            module.parent.mkdir(parents=True)
            module.touch()
            result=SimpleNamespace(returncode=1,stdout="",stderr="URLError: cannot resolve host")
            with patch.object(installer.subprocess,"run",return_value=result):
                with self.assertRaisesRegex(installer.InstallerError,"retry online"):
                    installer._ensure_vision_parse_models(Path("python"),root,lambda msg:None)

    def test_timeout_is_explicit(self):
        with tempfile.TemporaryDirectory() as name:
            root=Path(name)
            module=root/"plugins"/"vision_parse"/"src"/"media_faces.py"
            module.parent.mkdir(parents=True)
            module.touch()
            with patch.object(installer.subprocess,"run",side_effect=subprocess.TimeoutExpired(["python"],240)):
                with self.assertRaisesRegex(installer.InstallerError,"reconnect"):
                    installer._ensure_vision_parse_models(Path("python"),root,lambda msg:None)

if __name__=="__main__":
    unittest.main()
