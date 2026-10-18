# TraceLens AI — Project Requirements

## 1. Vision

TraceLens AI is a local-first AI-powered debugging and repair assistant for developers. It helps detect software bugs, investigate their causes using actual source code, propose code changes, and validate proposed fixes with tests.

The goal is to help developers move from discovering a bug to producing a tested, reviewable fix.

## 2. Target Users

Independent developers, students, and small software teams who want help debugging and repairing applications without paid AI APIs.

## 3. Core Workflow

1. Open a supported local software project.
2. Detect a problem through failing tests, runtime errors, incorrect outputs, or monitored logs.
3. Collect relevant evidence, source code, stack traces, and test results.
4. Identify the code potentially responsible for the failure.
5. Ask a locally running AI model to investigate the evidence.
6. Generate a proposed source-code patch.
7. Run appropriate tests in a controlled environment.
8. Report which tests passed or failed and whether the original bug appears resolved.
9. Let the developer review and approve the patch before applying it.

## 4. Functional Requirements

### FR1 — Project Inspection

The system must inspect supported source files and project structure while avoiding unnecessary files such as virtual environments and dependency folders.

### FR2 — Bug Reproduction

The system must support reproducing bugs using existing tests or developer-provided test cases.

### FR3 — Runtime Monitoring

The system must be able to monitor a configured, supported application log file for new errors.

### FR4 — Failure Analysis

The system must collect relevant stack traces, failing assertions, error messages, and source-code context.

### FR5 — Code-Aware Diagnosis

The system must investigate the actual source code rather than relying exclusively on error messages.

### FR6 — Proposed Patches

The system must generate reviewable code changes intended to address the identified bug.

### FR7 — Automated Validation

The system must run relevant tests when a suitable test environment is available and report the actual results.

### FR8 — Regression Awareness

The system should run relevant existing tests to check whether a proposed fix breaks previously working behavior.

### FR9 — Developer Approval

The system must not silently apply proposed patches or execute untrusted commands.

### FR10 — Incident History

The system should save investigation summaries and validation results locally.

## 5. AI Requirements

### AIR1 — Evidence-Based Reasoning

Diagnosis and proposed fixes must be grounded in the source code, observed failures, and available tests.

### AIR2 — Uncertainty

The AI must acknowledge when evidence is insufficient to identify a reliable fix.

### AIR3 — Structured Results

Each investigation should provide:
- Problem summary
- Reproduction evidence
- Relevant files and functions
- Likely cause
- Supporting evidence
- Proposed patch
- Validation results
- Remaining risks and uncertainty

### AIR4 — No Fabricated Results

The system must never claim a test passed unless the test was actually executed and its result verified.

### AIR5 — Untrusted Project Content

Source files, logs, comments, and other project content must be treated as untrusted data, not as instructions that override system safety rules.

### AIR6 — Local AI

The MVP must use the locally running Ollama model rather than a paid external AI API.

## 6. Safety and Privacy

- Process source code and logs locally by default.
- Exclude secrets, virtual environments, and unnecessary dependency files from analysis where possible.
- Limit the amount of code and log data sent to the model.
- Require approval before applying patches.
- Run tests with appropriate timeouts and controlled permissions.
- Preserve the original code until a proposed change is approved.

## 7. MVP Scope

The first working version will support Python projects and focus on this complete workflow:

1. Inspect a small Python project.
2. Reproduce a bug with a test.
3. Identify relevant source code.
4. Generate a proposed patch using the local AI model.
5. Apply the patch only in a controlled test copy or after explicit approval.
6. Run the test again.
7. Report whether the fix passed validation.

Continuous log monitoring will be developed alongside this workflow and integrated into the broader debugging system.

## 8. Limitations

TraceLens cannot guarantee a correct fix for every bug. A passing test only validates the behavior covered by that test. Some failures require additional information, external systems, or manual investigation.

Initial support is limited to Python projects. Additional languages will be introduced only after they have been tested.

## 9. Success Criteria

- Reproduce a known bug using a test.
- Identify the relevant source-code location.
- Produce a reviewable patch.
- Verify test results by executing the tests.
- Demonstrate a successful fix on at least one reproducible bug.
- Detect when evidence is insufficient.
- Avoid unapproved source-code changes.
- Run the MVP without paid AI services.
