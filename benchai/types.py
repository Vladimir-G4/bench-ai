from typing import Callable, Any, Dict, List, Optional, Union, Literal
from dataclasses import dataclass, field
from enum import Enum


# 1. User's model: must take a string prompt and return a string output
ModelFn = Callable[[str], str]


# 2. Enum for supported tasks (can grow over time)
class UseCase(str, Enum):
    QA = "qa"
    SUMMARIZATION = "summarization"
    CODEGEN = "codegen"
    FUNCTION_CALL = "function_call"
    RAG = "rag"
    EXTRACTION = "extraction"
    CLASSIFICATION = "classification"
    SENTIMENT = "sentiment"
    TRANSLATION = "translation"
    MATH = "math"
    CONVERSATION = "conversation"
    FACT_CHECK = "fact_check"
    STORY = "story"
    TOPIC_TAGGING = "topic_tagging"


# 3. Each test case from YAML/JSON
@dataclass
class TestCase:
    prompt: str
    expected: Union[str, Dict[str, Any], List[str]]
    use_case: UseCase
    id: Optional[str] = None  # Optional ID for tracking
    metadata: Dict[str, Any] = field(default_factory=dict)  # Optional add-ons (e.g., topic)


# 4. Evaluation result from one prompt
@dataclass
class EvalResult:
    prompt: str
    expected: Any
    actual: str
    use_case: UseCase
    score: float
    passed: bool
    feedback: Optional[str] = None
    metadata: Dict[str, Any] = field(default_factory=dict)


# 5. Summary across all test cases
@dataclass
class EvalSummary:
    results: List[EvalResult]
    avg_score: float
    pass_rate: float
    use_case: UseCase
