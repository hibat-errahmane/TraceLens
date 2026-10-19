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

    # Extract code from a fenced block, ignoring any explanation after it.
    candidates = re.findall(
        r"```(?:[a-zA-Z0-9_+-]+)?[ \t]*\n(.*?)```",
        diagnosis,
        flags=re.DOTALL,
    )

    
    if candidates:
        patch = candidates[-1].strip() + "\n"
    else:
        # Support a plain-text Python function returned by the AI.
        match = re.search(
            r"(?ms)^def\s+" + re.escape("calculate_total") +
            r"\s*\(.*?(?=\n```|\nPATCH_UNAVAILABLE|\Z)",
            diagnosis,
        )

        if match:
            patch = match.group(0).strip() + "\n"
        else:
            return {
                "status": "patch_not_extracted",
                "ai_diagnosis": diagnosis,
                "patch": None,
                "validation": None,
            }


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