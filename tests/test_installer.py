from __future__ import annotations

import json
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def test_installed_skill_is_self_contained(self) -> None:
        with tempfile.TemporaryDirectory() as temp_name:
            target = Path(temp_name) / "motionsites-design"
            install = subprocess.run(
                [sys.executable, str(ROOT / "scripts" / "install_skill.py"), "--destination", str(target)],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(install.returncode, 0, install.stderr)
            doctor = subprocess.run(
                [sys.executable, str(target / "scripts" / "motionsites_catalog.py"), "doctor", "--cache-dir", str(Path(temp_name) / "cache"), "--json"],
                check=False,
                capture_output=True,
                text=True,
            )
            self.assertEqual(doctor.returncode, 0, doctor.stderr)
            self.assertEqual(json.loads(doctor.stdout)["starter_count"], 8)


if __name__ == "__main__":
    unittest.main()
