# ui/app.py

import streamlit as st
from benchai.loader import load_test_cases
from benchai.runner import Runner
from benchai.visualizer import Visualizer
from benchai.types import UseCase
from importlib.util import spec_from_file_location, module_from_spec

st.set_page_config(page_title="Bench AI", layout="wide")

st.title("🧪 Bench AI")
st.markdown("Benchmark any AI model. With one function.")

# Upload test file
test_file = st.file_uploader("Upload your test file (.yaml or .json)", type=["yaml", "yml", "json"])

# Select use case
use_case = st.selectbox("Select use case", [u.value for u in UseCase])

# Upload model file
model_file = st.file_uploader("Upload your Python model file", type=["py"])

if st.button("Run Evaluation") and test_file and model_file:
    with open("uploaded_test_file.yaml", "wb") as f:
        f.write(test_file.read())

    with open("uploaded_model.py", "wb") as f:
        f.write(model_file.read())

    # Load model
    spec = spec_from_file_location("uploaded_model", "uploaded_model.py")
    model_module = module_from_spec(spec)
    spec.loader.exec_module(model_module)

    if not hasattr(model_module, "model"):
        st.error("Your model file must define a function named `model(prompt: str) -> str`.")
    else:
        model_fn = model_module.model
        try:
            st.write("📤 Loading test cases...")
            test_cases = load_test_cases("uploaded_test_file.yaml")
            test_cases = [tc for tc in test_cases if tc.use_case == UseCase(use_case)]

            st.write(f"✅ {len(test_cases)} test cases loaded.")

            runner = Runner(model_fn)
            results = runner.run(test_cases)

            st.write("📊 Evaluation complete.")

            st.write("### Scores:")
            for r in results:
                st.markdown(f"**Prompt:** {r.prompt[:60]}{'...' if len(r.prompt) > 60 else ''}")
                st.markdown(f"**Expected:** {r.expected}")
                st.markdown(f"**Actual:** {r.actual}")
                st.markdown(f"**Score:** {r.score:.2f} | {'✅' if r.passed else '❌'}")
                st.markdown(f"*{r.feedback}*")
                st.markdown("---")

            st.write("### Visual Summary")
            Visualizer(results).render()

        except Exception as e:
            st.error(f"Evaluation failed: {e}")