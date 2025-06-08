# ui/app.py

import streamlit as st
import os
import json
from benchai.loader import load_test_cases
from benchai.runner import Runner
from benchai.visualizer import Visualizer
from benchai.types import UseCase
from importlib.util import spec_from_file_location, module_from_spec
from pathlib import Path

# Set page config for a clean, centered layout
st.set_page_config(
    page_title="benchAI - Model Evaluation Platform",
    page_icon="🧪",
    layout="centered",
    initial_sidebar_state="expanded"
)

# Custom CSS for YC-inspired minimalist light theme
st.markdown("""
    <style>
    .main { 
        background-color: #ffffff; 
        color: #1a1a1a; 
        font-family: -apple-system, BlinkMacSystemFont, 'Inter', sans-serif;
    }
    .stButton>button {
        background-color: #f0652f;
        color: #ffffff;
        border: none;
        border-radius: 6px;
        padding: 8px 16px;
        font-weight: 500;
        font-size: 14px;
        transition: background-color 0.2s ease, transform 0.1s ease;
    }
    .stButton>button:hover {
        background-color: #d55528;
        transform: translateY(-1px);
    }
    .stButton>button:disabled {
        background-color: #e5e5e5;
        color: #999999;
    }
    .stFileUploader { 
        border: 1px solid #e5e5e5; 
        border-radius: 6px; 
        padding: 10px; 
        background-color: #fafafa; 
    }
    .stSelectbox { 
        background-color: #fafafa; 
        border: 1px solid #e5e5e5; 
        border-radius: 6px; 
        padding: 6px; 
        color: #1a1a1a; 
    }
    .stSelectbox div[data-baseweb="select"] > div {
        background-color: #fafafa;
        color: #1a1a1a;
        border-radius: 6px;
    }
    .result-card { 
        background-color: #ffffff; 
        border: 1px solid #f0f0f0; 
        border-radius: 6px; 
        padding: 12px; 
        margin-bottom: 12px; 
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
    }
    .success { color: #28a745; }
    .failure { color: #dc3545; }
    .sidebar .stButton>button { 
        width: 100%; 
        background-color: #f0652f;
        border: none;
    }
    .sidebar .stButton>button:hover {
        background-color: #d55528;
    }
    h1 { 
        color: #1a1a1a; 
        font-weight: 600; 
        font-size: 28px; 
        margin-bottom: 8px;
    }
    h3 { 
        color: #333333; 
        font-weight: 500; 
        font-size: 18px; 
        margin-bottom: 10px;
    }
    .stSpinner { 
        display: flex; 
        justify-content: center; 
    }
    .stMarkdown, .stMarkdown p, .stMarkdown div { 
        color: #1a1a1a; 
        font-size: 14px;
    }
    .stSidebar { 
        background-color: #f5f5f5; 
    }
    .table-view th, .table-view td {
        border: 1px solid #e5e5e5;
        padding: 8px;
        font-size: 13px;
    }
    .table-view th {
        background-color: #fafafa;
        font-weight: 500;
    }
    .stProgress .st-bo {
        background-color: #f0652f;
    }
    </style>
""", unsafe_allow_html=True)

# Sidebar for navigation and settings
with st.sidebar:
    st.header("benchAI")
    st.markdown("Evaluate any LLM with precision. Use built-in test suites or upload your own.")
    
    # Select test source
    test_source = st.radio(
        "Test Source", 
        ["Built-in Tests", "Upload Custom Test File"], 
        help="Choose between benchAI's pre-built test suites or your own YAML/JSON file."
    )
    
    # Built-in test files from tests/fixtures/
    test_files = {
        "QA Tests": "tests/fixtures/qa_tests.yaml",
        "Summarization Tests": "tests/fixtures/summarization_tests.yaml"
    }
    
    selected_test = None
    uploaded_test_file = None
    if test_source == "Built-in Tests":
        selected_test = st.selectbox(
            "Select Test Suite", 
            list(test_files.keys()), 
            help="Pick a pre-built test suite for QA or Summarization."
        )
    else:
        uploaded_test_file = st.file_uploader(
            "Upload Test File (.yaml or .json)", 
            type=["yaml", "yml", "json"],
            help="Upload a YAML or JSON file with test cases (e.g., prompts, expected outputs)."
        )
    
    # Select use case
    use_case = st.selectbox(
        "Select Use Case", 
        [u.value for u in UseCase], 
        help="Select the task type (e.g., QA, Summarization) for evaluation."
    )
    
    # Upload model file
    model_file = st.file_uploader(
        "Upload Model File (.py)", 
        type=["py"], 
        help="Upload a Python file with a `model(prompt: str) -> str` function to evaluate."
    )
    
    # Run button
    run_evaluation = st.button("Run Evaluation", disabled=not (model_file and (selected_test or uploaded_test_file)))

# Main content
st.title("benchAI - Model Evaluation Platform")
st.markdown("Test your AI model with a robust, model-agnostic platform built for real-world tasks.")

if run_evaluation:
    # Save uploaded files
    if uploaded_test_file:
        test_file_path = "uploaded_test_file.yaml"
        with open(test_file_path, "wb") as f:
            f.write(uploaded_test_file.read())
    else:
        test_file_path = test_files[selected_test]
    
    with open("uploaded_model.py", "wb") as f:
        f.write(model_file.read())
    
    # Load model
    try:
        spec = spec_from_file_location("uploaded_model", "uploaded_model.py")
        model_module = module_from_spec(spec)
        spec.loader.exec_module(model_module)
        
        if not hasattr(model_module, "model"):
            st.error("❌ Model file must define a function named `model(prompt: str) -> str`.", icon="🚨")
        else:
            model_fn = model_module.model
            with st.spinner("📤 Loading test cases..."):
                try:
                    test_cases = load_test_cases(test_file_path)
                    test_cases = [tc for tc in test_cases if tc.use_case == UseCase(use_case)]
                    
                    if not test_cases:
                        st.error(f"❌ No test cases found for use case '{use_case}' in {test_file_path}.", icon="🚨")
                    else:
                        st.success(f"✅ Loaded {len(test_cases)} test cases for '{use_case}'.", icon="🎉")
                        
                        # Run evaluation with progress bar
                        runner = Runner(model_fn)
                        results = []
                        for i, result in enumerate(runner.run(test_cases)):
                            results.append(result)
                        
                        st.success("📊 Evaluation complete!", icon="🎉")
                        
                        # Export results
                        export_file = f"benchai_results_{use_case}_{Path(test_file_path).stem}.json"
                        with open(export_file, "w") as f:
                            json.dump([r.__dict__ for r in results], f, indent=2)
                        with open(export_file, "rb") as f:
                            st.download_button(
                                label="📥 Download Results (JSON)",
                                data=f,
                                file_name=export_file,
                                mime="application/json",
                                help="Export evaluation results as JSON for CI/CD or further analysis."
                            )
                        
                        # View toggle: Cards or Table
                        view_mode = st.radio("View Results As", ["Cards", "Table"], horizontal=True)
                        
                        # Display results
                        st.header("Evaluation Results")
                        if view_mode == "Cards":
                            for i, r in enumerate(results):
                                with st.expander(f"Test Case {i+1}: {r.prompt[:60]}{'...' if len(r.prompt) > 60 else ''}", expanded=False):
                                    st.markdown(f"""
                                        <div class='result-card'>
                                            <strong>Prompt:</strong> {r.prompt}<br>
                                            <strong>Expected:</strong> {r.expected}<br>
                                            <strong>Actual:</strong> {r.actual}<br>
                                            <strong>Score:</strong> {r.score:.2f} <span class='{'success' if r.passed else 'failure'}'>{'✅' if r.passed else '❌'}</span><br>
                                            <strong>Feedback:</strong> <i>{r.feedback}</i>
                                        </div>
                                    """, unsafe_allow_html=True)
                        else:
                            table_data = [
                                {
                                    "ID": i + 1,
                                    "Prompt": r.prompt[:60] + "..." if len(r.prompt) > 60 else r.prompt,
                                    "Expected": r.expected,
                                    "Actual": r.actual,
                                    "Score": f"{r.score:.2f}",
                                    "Status": "✅" if r.passed else "❌"
                                }
                                for i, r in enumerate(results)
                            ]
                            st.table(table_data)
                        
                        # Visualize results
                        st.header("Visual Summary")
                        visualizer = Visualizer(results)
                        visualizer.render()
                        
                except Exception as e:
                    st.error(f"❌ Evaluation failed: {str(e)}", icon="🚨")
    except Exception as e:
        st.error(f"❌ Failed to load model: {str(e)}", icon="🚨")

# Footer
st.markdown("---")
st.markdown("Built with ❤️ by the benchAI team. Model-agnostic, use-case-aware, CI/CD-ready.")