from pathlib import Path


IGNORED_DIRECTORIES = {
    ".git",
    ".venv",
    "venv",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
}


def scan_project(project_path):
    """Scan a project while ignoring generated and environment files."""

    root = Path(project_path).resolve()

    files = []

    for path in root.rglob("*"):
        if not path.is_file():
            continue

        if any(part in IGNORED_DIRECTORIES for part in path.parts):
            continue

        files.append(str(path.relative_to(root)))

    return {
        "project": str(root),
        "files": files,
    }