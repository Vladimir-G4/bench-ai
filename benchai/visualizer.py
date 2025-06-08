# benchai/visualizer.py

import plotly.express as px
import pandas as pd
from benchai.types import EvalResult

class Visualizer:
    def __init__(self, results: list[EvalResult]):
        self.results = results

    def render(self):
        if not self.results:
            print("No results to visualize.")
            return

        data = [
            {
                "Prompt": r.prompt[:100] + "..." if len(r.prompt) > 100 else r.prompt,
                "Score": r.score,
                "Passed": "✅" if r.passed else "❌",
                "Feedback": r.feedback or "",
            }
            for r in self.results
        ]

        df = pd.DataFrame(data)

        fig = px.bar(
            df,
            x="Prompt",
            y="Score",
            color="Passed",
            text="Feedback",
            title="Bench AI Evaluation Results",
            labels={"Score": "Score", "Prompt": "Prompt (truncated)"},
        )

        fig.update_layout(
            xaxis_tickangle=-45,
            height=600,
            margin=dict(t=50, b=150),
        )

        fig.show()
