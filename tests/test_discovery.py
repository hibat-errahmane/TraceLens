import tempfile
import unittest
from pathlib import Path

from tracelens.test_discovery import (
    find_test_files,
    detect_test_framework,
    detect_test_command,
)


class TestDiscovery(unittest.TestCase):

    def test_finds_test_files(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "test_app.py").write_text("", encoding="utf-8")
            (root / "app.py").write_text("", encoding="utf-8")

            self.assertEqual(find_test_files(root), ["test_app.py"])

    def test_ignores_venv(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            venv = root / ".venv"
            venv.mkdir()
            (venv / "test_external.py").write_text("", encoding="utf-8")

            self.assertEqual(find_test_files(root), [])

    def test_defaults_to_unittest(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            self.assertEqual(detect_test_framework(root), "unittest")

    def test_detects_pytest_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "pytest.ini").write_text("[pytest]", encoding="utf-8")

            self.assertEqual(detect_test_framework(root), "pytest")


    def test_detects_pytest_in_requirements(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "requirements.txt").write_text(
                "pytest>=8.0\\n", encoding="utf-8"
            )

            self.assertEqual(detect_test_framework(root), "pytest")

    def test_returns_no_command_without_tests(self):
        with tempfile.TemporaryDirectory() as temp:
            self.assertIsNone(detect_test_command(temp))


if __name__ == "__main__":
    unittest.main()
