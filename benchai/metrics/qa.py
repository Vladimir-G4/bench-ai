# benchai/metrics/qa.py

import difflib
from typing import Any, Union

class QAValidator:
    def score(self, actual: str, expected: Union[str, list, dict]) -> tuple[float, bool, str]:
        actual = actual.strip().lower()

        if isinstance(expected, str):
            expected_answers = [expected.strip().lower()]
        elif isinstance(expected, list):
            expected_answers = [e.strip().lower() for e in expected]
        else:
            return 0.0, False, "Invalid expected type for QA"

        # Exact match check
        if actual in expected_answers:
            return 1.0, True, "Exact match"

        # Fuzzy match (Diff ratio > threshold)
        best_score = 0.0
        best_match = ""
        for expected_ans in expected_answers:
            ratio = difflib.SequenceMatcher(None, actual, expected_ans).ratio()
            if ratio > best_score:
                best_score = ratio
                best_match = expected_ans

        if best_score >= 0.85:
            return best_score, True, f"Fuzzy match (~{int(best_score * 100)}%)"
        else:
            return best_score, False, f"No strong match (best: '{best_match}', score: {best_score:.2f})"
