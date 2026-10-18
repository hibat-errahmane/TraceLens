
from tracelens.test_runner import run_tests
from tracelens.source_inspector import read_source_file


def collect_evidence(project_path, test_command, source_files):
    """Run tests and collect source code into one report."""

    test_result = run_tests(project_path, test_command)

    source_results = []
    source_errors = []

    for relative_path in source_files:
        try:
            source = read_source_file(project_path, relative_path)
            source_results.append(source)
        except (ValueError, OSError) as error:
            source_errors.append({
                "path": relative_path,
                "error": str(error),
            })

    return {
        "tests": test_result,
        "source_files": source_results,
        "source_errors": source_errors,
    }
