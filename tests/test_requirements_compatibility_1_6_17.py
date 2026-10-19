"""Isolated regression tests for 1.6.17 requirements compatibility and Vision Parse.

These tests do not touch an installed Norm runtime or install packages.
Run: python -m unittest discover -s tests -p 'test_requirements_compatibility_1_6_17.py'
"""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("norm_installer_1617_deps", ROOT / "Norm-Installer.py")
assert SPEC and SPEC.loader
installer = importlib.util.module_from_spec(SPEC)
import sys
sys.modules[SPEC.name] = installer
SPEC.loader.exec_module(installer)


class RequirementRepairTests(unittest.TestCase):
    def test_portable_source_and_plugin_dependencies_are_collected(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "core").mkdir()
            (root / "core" / "requirements.txt").write_text(
                "psycopg[binary]==3.3.5\n"
                "opencv-python==5.0.0.93\n"
                "onnxruntime-gpu==1.31.0\n",
                encoding="utf-8",
            )
            plugin = root / "plugins" / "vision_parse"
            plugin.mkdir(parents=True)
            (plugin / "plugin.json").write_text('{"name": "vision_parse"}', encoding="utf-8")
            (plugin / "requirements.txt").write_text(
                "numpy>=2\nimageio-ffmpeg>=0.6\n", encoding="utf-8"
            )
            # Even when legacy lock is present, prefer core requirements.
            (root / "tools").mkdir()
            (root / "tools" / "requirements-lock.txt").write_text(
                "old-unrelated-package==1\n", encoding="utf-8"
            )
            specs = installer._requirements_from_source(
                root, {"source_dir": "core", "requirements_lock": "tools/requirements-lock.txt"}, lambda _: None
            )
            self.assertIn("psycopg[binary]==3.3.5", specs)
            self.assertIn("onnxruntime-gpu==1.31.0", specs)
            self.assertIn("numpy>=2", specs)
            self.assertIn("imageio-ffmpeg>=0.6", specs)
            self.assertIn("PyInstaller>=6", specs)
            self.assertFalse(any(s.startswith("old-unrelated-package") for s in specs))
            self.assertEqual(
                installer._newest_requirement_names(specs).count("psycopg[binary]"), 1
            )

    def test_vision_parse_legacy_package_gets_onnx_cuda_opencv(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            (root / "core").mkdir()
            (root / "core" / "requirements.txt").write_text("numpy>=2\n", encoding="utf-8")
            plugin = root / "plugins" / "vision_parse"
            plugin.mkdir(parents=True)
            (plugin / "plugin.json").write_text("{}", encoding="utf-8")
            specs = installer._requirements_from_source(
                root, {"source_dir": "core"}, lambda _: None
            )
            for name in ("onnxruntime-gpu", "opencv-python", "imageio-ffmpeg", "PyMuPDF"):
                self.assertIn(name, specs)
            self.assertNotIn("opencv-contrib-python", specs)
            self.assertNotIn("opencv-python-headless", specs)

    def test_requirements_package_mode_preserves_existing_when_satisfied(self):
        fake_inventory = {"records": {"redis": {"version": "8.1.0"}}}
        with mock.patch.object(installer, "_inventory_installed_environment", return_value=(fake_inventory, Path("constraints.txt"))), \
             mock.patch.object(installer, "_specs_already_satisfied", return_value=True), \
             mock.patch.object(installer, "_pip_dry_run_report") as resolver:
            delta = installer._resolve_package_dependency_delta(
                Path("python"), ["redis==8.1.0"], Path("."), lambda _: None
            )
            self.assertEqual(delta, {})
            resolver.assert_not_called()

    def test_newest_mode_resolves_as_one_compatible_graph(self):
        fake_inventory = {"records": {}}
        with mock.patch.object(installer, "_inventory_installed_environment", return_value=(fake_inventory, Path("constraints.txt"))), \
             mock.patch.object(installer, "_pip_dry_run_report", return_value={"install": [
                 {"metadata": {"name": "redis", "version": "8.1.1"}}
             ]}) as resolver, \
             mock.patch.object(installer, "_check_projected_environment_compatibility") as validate:
            result = installer._resolve_newest_dependency_delta(
                Path("python"), ["redis==8.1.0", "psycopg[binary]==3.3.5"],
                Path("."), lambda _: None, {"torch": "2.14.0+cu126"}
            )
            self.assertEqual(result, {"redis": "8.1.1"})
            args = resolver.call_args.args
            self.assertIn("psycopg[binary]", args[2])
            self.assertIn("redis", args[2])
            validate.assert_called_once()

    def test_package_mode_dry_run_does_not_upgrade(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            def fake_run(cmd, **kwargs):
                report = Path(cmd[cmd.index("--report") + 1])
                report.write_text(json.dumps({"install": []}))
                return mock.Mock(stdout="")
            with mock.patch.object(installer, "_run", side_effect=fake_run):
                out = installer._pip_dry_run_report(
                    Path("python"), root, ["redis==8.1.0"], root / "none",
                    "package-report.json", lambda _: None, upgrade=False
                )
            self.assertEqual(out["install"], [])


    def test_vision_parse_import_check_warns_when_cuda_not_advertised(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plugin = root / "plugins" / "vision_parse"
            plugin.mkdir(parents=True)
            (plugin / "plugin.json").write_text("{}", encoding="utf-8")
            warnings = []
            output = mock.Mock(returncode=0, stdout=json.dumps({
                "opencv": "5.0.0", "onnxruntime_providers": ["CPUExecutionProvider"]
            }), stderr="")
            with mock.patch.object(installer.subprocess, "run", return_value=output) as run:
                installer._verify_vision_parse_dependencies(
                    Path("python"), root, lambda _: None, warnings
                )
                self.assertTrue(run.called)
            self.assertEqual(len(warnings), 1)
            self.assertIn("CUDA provider", warnings[0])

    def test_vision_parse_import_check_rejects_missing_packages(self):
        with tempfile.TemporaryDirectory() as td:
            root = Path(td)
            plugin = root / "plugins" / "vision_parse"
            plugin.mkdir(parents=True)
            (plugin / "plugin.json").write_text("{}", encoding="utf-8")
            output = mock.Mock(returncode=1, stdout="", stderr="ModuleNotFoundError: No module named 'cv2'")
            with mock.patch.object(installer.subprocess, "run", return_value=output):
                with self.assertRaises(installer.InstallerError):
                    installer._verify_vision_parse_dependencies(
                        Path("python"), root, lambda _: None, []
                    )


if __name__ == "__main__":
    unittest.main()
