
import shutil
import tempfile
from pathlib import Path

from tracelens.test_runner import run_tests


def validate_patch(
    project_path,
    project_subdir,
    relative_path,
    proposed_content,
    test_command,
):
    """Test proposed source code in a temporary project copy."""

    project_root = Path(project_path).resolve()
    source_dir = (project_root / project_subdir).resolve()
    original_file = (project_root / relative_path).resolve()

    if not source_dir.is_relative_to(project_root):
        raise ValueError("Project copy must be inside the project root")

    if not original_file.is_relative_to(source_dir):
        raise ValueError("Target file must be inside the copied project")

    if original_file.suffix != ".py":
        raise ValueError("Only Python source files are supported")

    if not source_dir.is_dir() or not original_file.is_file():
        raise FileNotFoundError("Project directory or source file not found")

    with tempfile.TemporaryDirectory(prefix="tracelens_") as temp:
        temp_root = Path(temp)
        temp_project = temp_root / project_subdir

        shutil.copytree(source_dir, temp_project, dirs_exist_ok=True)

        target = temp_root / relative_path
        target.write_text(proposed_content, encoding="utf-8")

        result = run_tests(temp_root, test_command)

        return {
            "passed": result["passed"],
            "returncode": result["returncode"],
            "timed_out": result["timed_out"],
            "stdout": result["stdout"],
            "stderr": result["stderr"],
        }
