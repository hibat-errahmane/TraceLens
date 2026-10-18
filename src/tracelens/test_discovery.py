from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}


def find_test_files(project_path):
    """Find likely Python test files."""

    root = Path(project_path).resolve()

    test_files = []

    for path in root.rglob("*.py"):

        if any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue

        relative_path = path.relative_to(root)

        if "src" in relative_path.parts and "tracelens" in relative_path.parts:
            continue

        if path.name.startswith("test_") or path.name.endswith("_test.py"):
            test_files.append(str(relative_path))

            return test_files
def detect_source_file(project_path, test_files):
    """Find a likely source file next to the first test file."""

    root = Path(project_path).resolve()

    if not test_files:
        return None

    test_path = root / test_files[0]
    test_directory = test_path.parent

    candidates = []

    for path in test_directory.glob("*.py"):
        if path.name.startswith("test_"):
            continue

        if path.name.endswith("_test.py"):
            continue

        if path.name == "__init__.py":
            continue

        candidates.append(path)

    if len(candidates) == 1:
        return str(candidates[0].relative_to(root))

    return None

def detect_test_framework(project_path):
    """Detect the most likely Python testing framework."""

    root = Path(project_path).resolve()

    # pytest configuration at project root
    if (root / "pytest.ini").exists():
        return "pytest"

    # Check pyproject.toml
    pyproject = root / "pyproject.toml"

    if pyproject.exists():
        content = pyproject.read_text(
            encoding="utf-8",
            errors="ignore",
        ).lower()

        if "pytest" in content:
            return "pytest"

    # Check requirements files
    for filename in [
        "requirements.txt",
        "requirements-dev.txt",
    ]:
        requirements = root / filename

        if requirements.exists():
            content = requirements.read_text(
                encoding="utf-8",
                errors="ignore",
            ).lower()

            if "pytest" in content:
                return "pytest"

    # If no pytest evidence exists, use unittest
    return "unittest"


def detect_test_command(project_path):
    """Build a test command from the detected framework."""

    root = Path(project_path).resolve()

    framework = detect_test_framework(root)
    test_files = find_test_files(root)

    if not test_files:
        return None

    if framework == "pytest":
        return [
            "python",
            "-m",
            "pytest",
            "-v",
        ]

    # unittest fallback
    first_test = Path(test_files[0])
    test_directory = str(first_test.parent)

    if test_directory == ".":
        test_directory = "."

    return [
        "python",
        "-m",
        "unittest",
        "discover",
        "-s",
        test_directory,
        "-p",
        "test_*.py",
        "-v",
    ]


def discover_tests(project_path):
    """Discover tests, framework, test command, and source file."""

    test_files = find_test_files(project_path)
    framework = detect_test_framework(project_path)
    command = detect_test_command(project_path)
    source_file = detect_source_file(project_path, test_files)

    return {
        "test_files": test_files,
        "framework": framework,
        "test_command": command,
        "source_file": source_file,
    }