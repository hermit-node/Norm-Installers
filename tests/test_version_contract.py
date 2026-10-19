import ast
import os
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def installer_version():
    tree = ast.parse((ROOT / "Norm-Installer.py").read_text(encoding="utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "INSTALLER_VERSION"
            for target in node.targets
        ):
            return ast.literal_eval(node.value)
    raise AssertionError("Missing version declaration")

class VersionContractTests(unittest.TestCase):
    def test_version_matches_docs(self):
        version = installer_version()
        self.assertRegex(version, r"^[0-9]+[.][0-9]+[.][0-9]+$")
        for filename in ("README.md","RELEASE_NOTES.md"):
            text = (ROOT / filename).read_text(encoding="utf-8")
            self.assertTrue(text.startswith("# Norm Installer " + version),filename)
    def test_version_matches_tag(self):
        tag = os.environ.get("NORM_EXPECTED_RELEASE_TAG","")
        if tag:
            self.assertEqual(tag,"v" + installer_version())
