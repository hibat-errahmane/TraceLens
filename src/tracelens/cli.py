
import argparse
from pathlib import Path

from tracelens.repair_workflow import investigate_and_validate
from tracelens.patch_applier import apply_patch_and_verify


def main():
    parser = argparse.ArgumentParser(
        description="TraceLens AI - local debugging assistant"
    )

    parser.add_argument("--project", default=".")
    parser.add_argument("--subdir", default="demo_app")
    parser.add_argument("--source", default="demo_app/app.py")

    args = parser.parse_args()

    project_root = Path(args.project).resolve()
    source_file = (project_root / args.source).resolve()

    if not source_file.is_relative_to(project_root):
        parser.error("--source must point inside the project directory")

    if not source_file.is_file():
        parser.error(f"Source file not found: {source_file}")

    original_content = source_file.read_text(encoding="utf-8")

    test_command = [
        "python",
        "-m",
        "unittest",
        "discover",
        "-s",
        args.subdir,
        "-p",
        "test_*.py",
        "-v",
    ]

    print("TraceLens AI: investigating...")
    print(f"Project: {project_root}")
    print(f"Source: {args.source}")

    result = investigate_and_validate(
        str(project_root),
        args.subdir,
        args.source,
        test_command,
    )

    print(f"\nWORKFLOW STATUS: {result['status']}")

    if result.get("ai_diagnosis"):
        print("\n--- AI DIAGNOSIS ---")
        print(result["ai_diagnosis"])

    if result.get("patch"):
        print("\n--- PROPOSED PATCH ---")
        print(result["patch"])

    validation = result.get("validation")

    if validation:
        print("\n--- VALIDATION ---")
        print(f"Passed: {validation['passed']}")
        print(f"Exit code: {validation['returncode']}")

    if result.get("status") != "patch_passed_tests":
        print("\nPatch will not be applied because validation did not pass.")
        return

    print("\nThe proposed patch passed the tests.")
    answer = input("Apply this patch to the original file? [y/N]: ").strip().lower()

    if answer != "y":
        print("Patch not applied. Original source remains unchanged.")
        return

    applied = apply_patch_and_verify(
        str(project_root),
        args.source,
        result["patch"],
        test_command,
        expected_original=original_content,
    )

    if applied["success"]:
        print("Patch applied successfully. Tests passed.")
    elif applied.get("rolled_back"):
        print("Patch failed verification. Original source was restored.")
    else:
        print(f"Patch was not applied: {applied.get('error', 'Unknown error')}")


if __name__ == "__main__":
    main()
