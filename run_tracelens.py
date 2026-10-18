import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent / "src"))

from tracelens.auto_workflow import automatic_repair


def main():
    project_path = Path.cwd()
    result = automatic_repair(project_path)

    print("\n=== TRACELENS AI ===")
    print("Project:", project_path)
    print("Status:", result["status"])

    discovery = result["discovery"]
    print("\n=== DISCOVERED INFORMATION ===")
    print("Framework:", discovery["framework"])
    print("Test files:", discovery["test_files"])
    print("Source file:", discovery["source_file"])
    print("Test command:", discovery["test_command"])

    workflow = result.get("workflow")
    if workflow is None:
        print("\nTraceLens could not start the repair workflow.")
        return

    print("\n=== WORKFLOW STATUS ===")
    print(workflow["status"])

    print("\n=== AI DIAGNOSIS ===")
    print(workflow.get("ai_diagnosis") or "No diagnosis available.")

    print("\n=== PROPOSED PATCH ===")
    print(workflow.get("patch") or "No patch proposed.")

    print("\n=== VALIDATION RESULTS ===")
    print(workflow.get("validation"))


if __name__ == "__main__":
    main()
