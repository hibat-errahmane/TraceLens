from pathlib import Path

from .test_discovery import discover_tests
from .repair_workflow import investigate_and_validate


def automatic_repair(project_path):
    """Discover project information and run the repair workflow."""

    project_path = Path(project_path).resolve()

    discovery = discover_tests(project_path)

    source_file = discovery["source_file"]
    test_command = discovery["test_command"]

    if source_file is None:
        return {
            "status": "no_source_file",
            "discovery": discovery,
        }

    if test_command is None:
        return {
            "status": "no_test_command",
            "discovery": discovery,
        }

    project_subdir = str(Path(source_file).parent)

    result = investigate_and_validate(
        str(project_path),
        project_subdir,
        source_file,
        test_command,
    )

    return {
        "status": "completed",
        "discovery": discovery,
        "workflow": result,
    }