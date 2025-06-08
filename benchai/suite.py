# benchai/suite.py

from typing import Optional
from benchai.types import ModelFn, UseCase, EvalSummary
from benchai.loader import load_test_cases
from benchai.runner import Runner
from benchai.visualizer import Visualizer
from benchai.utils import (
    log_success,
    log_failure,
    log_error,
    log_debug,
    short
)
import json

class EvalSuite:
    def __init__(self, model: ModelFn):
        self.model = model
        self._results = []
        self._use_case = None

    def run(self, use_case: str, test_file: str):
        try:
            use_case_enum = UseCase(use_case)
        except ValueError:
            log_error(f"Unsupported use case: {use_case}")
            raise

        self._use_case = use_case_enum
        test_cases = load_test_cases(test_file)

        test_cases = [tc for tc in test_cases if tc.use_case == use_case_enum]
        if not test_cases:
            log_failure(f"No test cases found for use case '{use_case}' in file '{test_file}'")
            raise ValueError(f"No test cases found for use case '{use_case}'")

        log_debug(f"🧪 Running {len(test_cases)} test cases for use case '{use_case}'")

        runner = Runner(self.model)
        self._results = runner.run(test_cases)

        passed = sum(r.passed for r in self._results)
        log_success(f"Completed {len(self._results)} evaluations. {passed} passed.")

    def summarize(self) -> EvalSummary:
        from benchai.types import EvalSummary

        if not self._results:
            log_failure("No results available to summarize.")
            raise RuntimeError("Run `.run()` before summarizing.")

        scores = [r.score for r in self._results]
        passed = [r.passed for r in self._results]
        avg_score = sum(scores) / len(scores) if scores else 0.0
        pass_rate = sum(passed) / len(passed) if passed else 0.0

        log_debug(f"📊 Avg Score: {avg_score:.2f}, Pass Rate: {pass_rate*100:.1f}%")

        return EvalSummary(
            results=self._results,
            avg_score=avg_score,
            pass_rate=pass_rate,
            use_case=self._use_case
        )

    def visualize(self):
        if not self._results:
            log_failure("No results to visualize. Run `.run()` first.")
            raise RuntimeError("No results to visualize.")
        Visualizer(self._results).render()

    def save(self, path: str = "results.json"):
        if not self._results:
            log_failure("No results to save. Run `.run()` first.")
            raise RuntimeError("No results to save.")
        try:
            with open(path, "w") as f:
                from dataclasses import asdict
                json.dump([asdict(r) for r in self._results], f, indent=2)
            log_success(f"Results saved to {path}")
        except Exception as e:
            log_error(f"Failed to save results: {e}")
