import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from tracelens.auto_workflow import automatic_repair


def main():
    project_path = Path.cwd()
    result = automatic_repair(project_path)

    print("\n" + "=" * 55)
    print("              TRACELENS AI")
    print("       AI investigates. Tests decide.")
    print("=" * 55)

    print(f"\nProject: {project_path}")
    print(f"Status:  {result['status']}")

    discovery = result["discovery"]

    print("\n[1] PROJECT ANALYSIS")
    print(f"Framework:  {discovery['framework']}")
    print(f"Test files: {discovery['test_files']}")
    print(f"Source:     {discovery['source_file']}")

    workflow = result.get("workflow")

    if workflow is None:
        print("\n[!] Repair workflow could not start.")
        return

    print("\n[2] AI DIAGNOSIS")
    print(workflow.get("ai_diagnosis") or "No diagnosis available.")

    print("\n[3] PROPOSED REPAIR")
    print("-" * 40)
    print(workflow.get("patch") or "No patch proposed.")
    print("-" * 40)

    validation = workflow.get("validation") or {}
    passed = validation.get("passed", False)

    print("\n[4] TEST VALIDATION")

    if passed:
        print("RESULT: PASS")
        print("All tests passed with the proposed repair.")
    else:
        print("RESULT: FAIL")
        print("The proposed repair did not pass validation.")

    print(f"\nTests passed: {passed}")
    print(f"Exit code:    {validation.get('returncode', 'N/A')}")

    print("\n" + "=" * 55)
    print(" AI proposes. Tests decide. Your original code stays safe.")
    print("=" * 55)


if __name__ == "__main__":
    main()