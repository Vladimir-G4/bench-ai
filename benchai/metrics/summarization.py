# benchai/metrics/summarization.py

from typing import Union
from rouge_score import rouge_scorer

class SummarizationValidator:
    def __init__(self):
        self.scorer = rouge_scorer.RougeScorer(['rougeL'], use_stemmer=True)

    def score(self, actual: str, expected: Union[str, list]) -> tuple[float, bool, str]:
        if isinstance(expected, list):
            expected = expected[0]
        
        scores = self.scorer.score(expected, actual)
        rouge_l = scores['rougeL'].fmeasure

        passed = rouge_l >= 0.4
        feedback = f"ROUGE-L: {rouge_l:.2f}"

        return rouge_l, passed, feedback