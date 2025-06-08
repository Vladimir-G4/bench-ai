# benchai/metrics/codegen.py

import ast

class CodegenValidator:
    def score(self, actual: str, expected: str) -> tuple[float, bool, str]:
        try:
            # Check for syntactic correctness
            ast.parse(actual)
        except SyntaxError as e:
            return 0.0, False, f"Syntax error: {e}"

        # Exact match fallback (naive)
        passed = actual.strip() == expected.strip()
        score = 1.0 if passed else 0.5
        feedback = "Exact match" if passed else "Valid syntax but differs from expected"

        return score, passed, feedback