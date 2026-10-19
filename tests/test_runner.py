import tempfile
import unittest
import sys
from pathlib import Path

from tracelens.test_runner import run_tests


class TestRunner(unittest.TestCase):

    def test_successful_command(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_tests(
                temp,
                [sys.executable, "-c", "print('hello')"],
            )

            self.assertTrue(result["passed"])
            self.assertEqual(result["returncode"], 0)
            self.assertFalse(result["timed_out"])
            self.assertIn("hello", result["stdout"])

    def test_failed_command(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_tests(
                temp,
                [sys.executable, "-c", "raise SystemExit(1)"],
            )

            self.assertFalse(result["passed"])
            self.assertEqual(result["returncode"], 1)
            self.assertFalse(result["timed_out"])

    def test_timeout(self):
        with tempfile.TemporaryDirectory() as temp:
            result = run_tests(
                temp,
                [
                    sys.executable,
                    "-c",
                    "import time; time.sleep(3)",
                ],
                timeout=0.2,
            )

            self.assertFalse(result["passed"])
            self.assertTrue(result["timed_out"])
            self.assertIsNone(result["returncode"])


if __name__ == "__main__":
    unittest.main()
