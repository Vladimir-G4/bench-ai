# cli/main.py

import argparse
from benchai.suite import EvalSuite

def main():
    parser = argparse.ArgumentParser(description="benchAI - LLM evaluation CLI")
    parser.add_argument(
        "test_file",
        help="Path to the test YAML or JSON file"
    )
    parser.add_argument(
        "--use-case",
        required=True,
        help="Use case to evaluate (e.g. qa, summarization, codegen)"
    )
    parser.add_argument(
        "--model",
        default="examples/openai_eval.py",
        help="Path to model function file (must define a `model(prompt: str) -> str`)"
    )

    args = parser.parse_args()

    # Dynamically import model
    import importlib.util
    import os

    model_path = os.path.abspath(args.model)
    spec = importlib.util.spec_from_file_location("user_model", model_path)
    user_model = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(user_model)

    if not hasattr(user_model, "model"):
        raise ValueError(f"File {args.model} must define a `model(prompt: str) -> str` function")

    model_fn = user_model.model

    suite = EvalSuite(model=model_fn)
    suite.run(use_case=args.use_case, test_file=args.test_file)

    summary = suite.summarize()

    print(f"\n🔍 Use Case: {args.use_case}")
    print(f"✅ Avg Score: {summary.avg_score:.2f}")
    print(f"✅ Pass Rate: {summary.pass_rate * 100:.1f}%")
    print(f"📊 {len(summary.results)} test cases evaluated.")

    suite.visualize()

if __name__ == "__main__":
    main()
