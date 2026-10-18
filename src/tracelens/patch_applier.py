
from pathlib import Path

from tracelens.test_runner import run_tests


def apply_patch_and_verify(
    project_path,
    relative_path,
    proposed_content,
    test_command,
    expected_original=None,
):
    """Apply a patch safely and roll back if testing fails."""

    project_root = Path(project_path).resolve()
    target_file = (project_root / relative_path).resolve()

    if not target_file.is_relative_to(project_root):
        raise ValueError("Target file must be inside the project")

    if not target_file.is_file():
        raise FileNotFoundError("Target source file not found")

    original_content = target_file.read_text(encoding="utf-8")

    # Refuse to overwrite changes made since investigation.
    if (
        expected_original is not None
        and original_content != expected_original
    ):
        return {
            "success": False,
            "rolled_back": False,
            "error": "Source file changed since investigation. Investigate again.",
            "result": None,
        }

    try:
        target_file.write_text(proposed_content, encoding="utf-8")
        result = run_tests(project_root, test_command)

        if result["passed"]:
            return {
                "success": True,
                "rolled_back": False,
                "result": result,
            }

        target_file.write_text(original_content, encoding="utf-8")

        return {
            "success": False,
            "rolled_back": True,
            "result": result,
        }

    except Exception:
        target_file.write_text(original_content, encoding="utf-8")
        raise
