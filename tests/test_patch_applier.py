import tempfile
import unittest
import sys
from pathlib import Path
from unittest.mock import patch

from tracelens.patch_applier import apply_patch_and_verify


class TestPatchApplier(unittest.TestCase):

    def test_successful_patch_is_kept(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "app.py"
            source.write_text("value = 1\n", encoding="utf-8")

            with patch(
                "tracelens.patch_applier.run_tests",
                return_value={"passed": True},
            ):
                result = apply_patch_and_verify(
                    temp,
                    "app.py",
                    "value = 2\n",
                    [sys.executable, "-c", "pass"],
                    expected_original="value = 1\n",
                )

            self.assertTrue(result["success"])
            self.assertEqual(source.read_text(encoding="utf-8"), "value = 2\n")

    def test_failed_patch_restores_original(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "app.py"
            source.write_text("value = 1\n", encoding="utf-8")

            with patch(
                "tracelens.patch_applier.run_tests",
                return_value={"passed": False},
            ):
                result = apply_patch_and_verify(
                    temp,
                    "app.py",
                    "value = 2\n",
                    [sys.executable, "-c", "pass"],
                    expected_original="value = 1\n",
                )

            self.assertFalse(result["success"])
            self.assertTrue(result["rolled_back"])
            self.assertEqual(source.read_text(encoding="utf-8"), "value = 1\n")

    def test_refuses_to_overwrite_changed_source(self):
        with tempfile.TemporaryDirectory() as temp:
            source = Path(temp) / "app.py"
            source.write_text("value = 3\n", encoding="utf-8")

            result = apply_patch_and_verify(
                temp,
                "app.py",
                "value = 2\n",
                [sys.executable, "-c", "pass"],
                expected_original="value = 1\n",
            )

            self.assertFalse(result["success"])
            self.assertIn("changed since investigation", result["error"])
            self.assertEqual(source.read_text(encoding="utf-8"), "value = 3\n")
    def test_refuses_to_modify_file_outside_project(self):
        with tempfile.TemporaryDirectory() as temp:
            project = Path(temp) / "project"
            project.mkdir()

            outside_file = Path(temp) / "outside.py"
            outside_file.write_text("value = 1\n", encoding="utf-8")

            with self.assertRaises(ValueError):
                apply_patch_and_verify(
                    project,
                    "../outside.py",
                    "value = 2\n",
                    [sys.executable, "-c", "pass"],
                )

            self.assertEqual(
                outside_file.read_text(encoding="utf-8"),
                "value = 1\n",
            )

if __name__ == "__main__":
    unittest.main()
