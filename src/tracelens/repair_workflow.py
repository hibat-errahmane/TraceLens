import re

from tracelens.evidence import collect_evidence
from tracelens.ai_diagnostician import diagnose_with_ai
from tracelens.patch_validator import validate_patch


def investigate_and_validate(
    project_path,
    project_subdir,
    source_file,
    test_command,
):
    """Collect evidence, request a proposal, and validate it."""

    evidence = collect_evidence(
        project_path,
        test_command,
        [source_file],
    )

    if evidence["tests"]["passed"]:
        return {
            "status": "tests_already_pass",
            "ai_diagnosis": None,
            "patch": None,
            "validation": None,
        }

    ai_result = diagnose_with_ai(evidence)

    if not ai_result["success"]:
        return {
            "status": "ai_error",
            "ai_diagnosis": ai_result["error"],
            "patch": None,
            "validation": None,
        }

    diagnosis = ai_result["diagnosis"]

    
    if "PATCH_UNAVAILABLE" in diagnosis:
        return {
            "status": "patch_not_extracted",
            "ai_diagnosis": diagnosis,
            "patch": None,
            "validation": None,
        }

    # Extract code from a fenced block, regardless of its language label.
    candidates = re.findall(
        r"```[^\n`]*\n(.*?)```",
        diagnosis,
        flags=re.DOTALL,
    )

    if len(candidates) == 1:
        patch = candidates[0].strip() + "\n"
    else:
        # Fallback: extract the known function from an unfenced response.
        match = re.search(
            r"(?m)^def calculate_total\(.*?(?=\n\s*\n|\Z)",
            diagnosis,
            flags=re.DOTALL,
        )

        if not match:
            return {
                "status": "patch_not_extracted",
                "ai_diagnosis": diagnosis,
                "patch": None,
                "validation": None,
            }

        patch = match.group(0).strip() + "\n"


    validation = validate_patch(
        project_path,
        project_subdir,
        source_file,
        patch,
        test_command,
    )

    return {
        "status": (
            "patch_passed_tests"
            if validation["passed"]
            else "patch_failed_tests"
        ),
        "ai_diagnosis": diagnosis,
        "patch": patch,
        "validation": validation,
    }
