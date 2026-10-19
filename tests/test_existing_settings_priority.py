"""Regression tests for 1.6.17 upgrade prefill: installed operator values win.

Run from repository root:
    python -m unittest discover -s tests -p 'test_existing_settings_priority.py'
"""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import installer_environment as env


class ExistingSettingsPriorityTests(unittest.TestCase):
    def test_existing_custom_port_and_tailscale_host_survive_saved_imprint(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            target = Path(folder)
            config = target / "config"
            config.mkdir()
            (config / "settings.ini").write_text(
                "[network]\n"
                "postgres_port = 25434\n"
                "norm_host = current\n"
                "redis_port = 6379\n"
                "current_machine = local-test-host\n"
                "current_domain = example.invalid\n",
                encoding="utf-8",
            )
            # The local imprint was previously saved as a FULL configuration;
            # it is not evidence that the operator changed these values now.
            saved_imprint = {"network": {
                "postgres_port": 5432,
                "norm_host": "loopback",
                "redis_port": 6380,
                "activity_port": 9000,
            }}
            new_defaults = {"network": {
                "postgres_port": 5432,
                "norm_host": "loopback",
                "redis_port": 6379,
                "activity_port": 8766,
            }}
            resolved, _, origins = env.resolve_environment_prefill(
                target, saved_imprint, saved_imprint, new_defaults
            )
            self.assertEqual(resolved["network"]["postgres_port"], 25434)
            self.assertEqual(resolved["network"]["norm_host"], "current")
            # Even a current value equal to the generic default must be
            # preserved, rather than replaced by a stale saved imprint.
            self.assertEqual(resolved["network"]["redis_port"], 6379)
            self.assertEqual(origins["network.postgres_port"], "current")
            # For fields absent from installed configuration, the saved imprint
            # is still allowed to prefill the operator's installation screen.
            self.assertEqual(resolved["network"]["activity_port"], 9000)

    def test_fresh_install_prefills_explicit_imprint(self) -> None:
        with tempfile.TemporaryDirectory() as folder:
            saved = {"network": {"postgres_port": 6001}}
            defaults = {"network": {"postgres_port": 5432}}
            resolved, _, origins = env.resolve_environment_prefill(
                Path(folder), saved, saved, defaults
            )
            self.assertEqual(resolved["network"]["postgres_port"], 6001)
            self.assertEqual(origins["network.postgres_port"], "imprint")


if __name__ == "__main__":
    unittest.main()
