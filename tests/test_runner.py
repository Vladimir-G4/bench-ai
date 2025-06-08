# tests/test_runner.py

from benchai.runner import Runner
from benchai.types import TestCase, UseCase

def dummy_model(prompt: str) -> str:
    return "Paris" if "France" in prompt else "Unknown"

def test_runner_executes():
    runner = Runner(model=dummy_model)
    test_cases = [
        TestCase(prompt="What is the capital of France?", expected="Paris", use_case=UseCase.QA)
    ]
    results = runner.run(test_cases)

    assert len(results) == 1
    assert results[0].passed is True
    assert results[0].score == 1.0