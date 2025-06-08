from typing import List
from benchai.types import ModelFn, TestCase, EvalResult, UseCase
from benchai.metrics.qa import QAValidator
from benchai.metrics.summarization import SummarizationValidator
from benchai.metrics.codegen import CodegenValidator
from benchai.metrics.sentiment import SentimentValidator

USE_CASE_DISPATCH = {
    UseCase.QA: QAValidator(),
    UseCase.SUMMARIZATION: SummarizationValidator(),
    UseCase.CODEGEN: CodegenValidator(),
    UseCase.SENTIMENT: SentimentValidator(),
    # ... add more as you implement
}

class Runner:
    def __init__(self, model: ModelFn):
        self.model = model

    def run(self, test_cases: List[TestCase]) -> List[EvalResult]:
        results = []

        for case in test_cases:
            # 1. Run model
            try:
                output = self.model(case.prompt)
            except Exception as e:
                results.append(EvalResult(
                    prompt=case.prompt,
                    expected=case.expected,
                    actual=str(e),
                    use_case=case.use_case,
                    score=0.0,
                    passed=False,
                    feedback=f"Model error: {e}",
                    metadata=case.metadata
                ))
                continue

            # 2. Validate output
            validator = USE_CASE_DISPATCH.get(case.use_case)
            if not validator:
                raise ValueError(f"No validator implemented for use case: {case.use_case}")

            score, passed, feedback = validator.score(output, case.expected)

            # 3. Collect result
            results.append(EvalResult(
                prompt=case.prompt,
                expected=case.expected,
                actual=output,
                use_case=case.use_case,
                score=score,
                passed=passed,
                feedback=feedback,
                metadata=case.metadata
            ))

        return results
