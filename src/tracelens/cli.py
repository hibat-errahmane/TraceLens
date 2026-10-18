
import argparse

from tracelens.repair_workflow import investigate_and_validate


def main():
    parser = argparse.ArgumentParser(
        description="TraceLens AI - local debugging assistant"
    )

    parser.add_argument("--project", default=".")
    parser.add_argument("--subdir", default="demo_app")
    parser.add_argument("--source", default="demo_app/app.py")

    args = parser.parse_args()

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
    print(f"Project: {args.project}")
    print(f"Source: {args.source}")

    result = investigate_and_validate(
        args.project,
        args.subdir,
        args.source,
        test_command,
    )

    print(f"\nWORKFLOW STATUS: {result['status']}")

    if result["ai_diagnosis"]:
        print("\n--- AI DIAGNOSIS ---")
        print(result["ai_diagnosis"])

    if result["patch"]:
        print("\n--- PROPOSED PATCH ---")
        print(result["patch"])

    if result["validation"]:
        print("\n--- VALIDATION ---")
        print(f"Passed: {result['validation']['passed']}")
        print(f"Exit code: {result['validation']['returncode']}")


if __name__ == "__main__":
    main()
