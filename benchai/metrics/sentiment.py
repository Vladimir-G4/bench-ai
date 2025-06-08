# benchai/metrics/sentiment.py

from textblob import TextBlob

class SentimentValidator:
    def score(self, actual: str, expected: str) -> tuple[float, bool, str]:
        actual_sentiment = TextBlob(actual).sentiment.polarity
        expected_sentiment = TextBlob(expected).sentiment.polarity

        diff = abs(actual_sentiment - expected_sentiment)
        passed = diff < 0.3
        score = max(0.0, 1 - diff)
        feedback = f"Polarity diff: {diff:.2f}, Expected: {expected_sentiment:.2f}, Got: {actual_sentiment:.2f}"

        return score, passed, feedback