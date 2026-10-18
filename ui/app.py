import sys
from pathlib import Path

import streamlit as st

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from tracelens.auto_workflow import automatic_repair
from tracelens.patch_applier import apply_patch_and_verify


st.set_page_config(
    page_title="TraceLens AI",
    page_icon="🔍",
)

st.title("🔍 TraceLens AI")
st.write("AI-powered debugging and repair assistant")

st.subheader("Project")

project_path = st.text_input(
    "Project path",
    value=str(PROJECT_ROOT),
)

if st.button("Investigate"):
    with st.spinner("TraceLens is investigating..."):
        result = automatic_repair(project_path)

    st.session_state["result"] = result

result = st.session_state.get("result")

if result:
    discovery = result["discovery"]

    st.subheader("🔎 Discovered Information")
    st.write("**Testing framework:**", discovery["framework"])
    st.write("**Test files:**", discovery["test_files"])
    st.write("**Source file:**", discovery["source_file"])

    workflow = result.get("workflow")

    if workflow:
        st.subheader("📊 Workflow Status")
        st.write(workflow["status"])

        st.subheader("🤖 AI Diagnosis")
        st.write(workflow.get("ai_diagnosis") or "No diagnosis available.")

        patch = workflow.get("patch")

        st.subheader("🛠 Proposed Patch")

        if patch:
            st.code(patch, language="python")

            if workflow.get("validation", {}).get("passed"):
                st.success("✅ Patch passed validation.")

                if st.button("Apply Fix"):
                    with st.spinner("Applying fix and running tests..."):
                        apply_result = apply_patch_and_verify(
                            project_path,
                            discovery["source_file"],
                            patch,
                            discovery["test_command"],
                        )

                    if apply_result["success"]:
                        st.success("🎉 Fix applied successfully! Tests passed.")
                    else:
                        st.error("❌ Fix failed. Original code was restored.")
            else:
                st.error("The proposed patch did not pass validation.")
        else:
            st.info("No patch proposed.")