# tests/test_suite.py

from benchai.suite import EvalSuite

def dummy_model(prompt: str) -> str:
    if "capital of France" in prompt:
        return "Paris"
    return "Unknown"

def test_suite_runs():
    suite = EvalSuite(model=dummy_model)
    suite.run(use_case="qa", test_file="tests/fixtures/qa_tests.yaml")
    summary = suite.summarize()

    assert summary.avg_score >= 0.9
    assert summary.pass_rate >= 0.9