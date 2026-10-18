
import re


def diagnose(evidence):
    """Produce a basic diagnosis from collected test and source evidence."""

    test_result = evidence["tests"]
    sources = evidence["source_files"]

    report = {
        "status": "passed" if test_result["passed"] else "failed",
        "summary": "",
        "failure_details": "",
        "source_evidence": [],
        "limitations": [],
    }

    if test_result["passed"]:
        report["summary"] = "All collected tests passed."
        return report

    failure_output = (
        test_result.get("stdout", "")
        + "\n"
        + test_result.get("stderr", "")
    )

    report["summary"] = (
        "Tests failed. The available evidence needs investigation."
    )

    mismatch = re.search(
        r"AssertionError:\s*(.+?)\s*!=\s*(.+)",
        failure_output,
    )

    if mismatch:
        actual, expected = mismatch.groups()
        report["failure_details"] = (
            f"Assertion mismatch: actual result {actual}; "
            f"expected result {expected}."
        )

    for source in sources:
        report["source_evidence"].append({
            "path": source["path"],
            "content": source["content"],
        })

    report["limitations"].append(
        "A value mismatch does not, by itself, prove the root cause."
    )

    if not report["failure_details"]:
        report["limitations"].append(
            "No supported assertion mismatch was extracted."
        )

    return report
