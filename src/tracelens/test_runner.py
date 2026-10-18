
import subprocess
from pathlib import Path


def run_tests(project_path, command, timeout=60):
    """Run tests and capture their results."""

    project_path = Path(project_path).resolve()

    try:
        result = subprocess.run(
            command,
            cwd=project_path,
            capture_output=True,
            text=True,
            timeout=timeout,
            shell=False,
        )

        return {
            "passed": result.returncode == 0,
            "returncode": result.returncode,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "timed_out": False,
        }

    except subprocess.TimeoutExpired as error:
        return {
            "passed": False,
            "returncode": None,
            "stdout": error.stdout or "",
            "stderr": error.stderr or "",
            "timed_out": True,
        }
