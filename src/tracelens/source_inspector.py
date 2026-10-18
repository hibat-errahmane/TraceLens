from pathlib import Path


def read_source_file(project_path, relative_path, max_chars=12000):
    """Read a source file inside a project without modifying it."""

    root = Path(project_path).resolve()
    file_path = (root / relative_path).resolve()

    # Refuse paths that escape the project directory.
    if not file_path.is_relative_to(root):
        raise ValueError("File must be inside the project directory")

    if file_path.suffix != ".py":
        raise ValueError("Only Python source files are supported")

    if not file_path.is_file():
        raise FileNotFoundError(f"Source file not found: {relative_path}")

    content = file_path.read_text(encoding="utf-8-sig")

    return {
        "path": str(file_path.relative_to(root)),
        "content": content[:max_chars],
        "truncated": len(content) > max_chars,
    }
