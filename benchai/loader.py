import json
import yaml
from pathlib import Path
from typing import List
from benchai.types import TestCase, UseCase

def load_test_cases(file_path: str) -> List[TestCase]:
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"Test file '{file_path}' not found.")

    # Load YAML or JSON
    if path.suffix in ['.yaml', '.yml']:
        with open(path, 'r') as f:
            data = yaml.safe_load(f)
    elif path.suffix == '.json':
        with open(path, 'r') as f:
            data = json.load(f)
    else:
        raise ValueError("Unsupported file format. Use .yaml or .json")

    if not isinstance(data, list):
        raise ValueError("Test file must be a list of test cases.")

    test_cases = []

    for idx, item in enumerate(data):
        try:
            use_case = UseCase(item['use_case'])
            test_case = TestCase(
                prompt=item['prompt'],
                expected=item['expected'],
                use_case=use_case,
                id=item.get('id'),
                metadata=item.get('metadata', {})
            )
            test_cases.append(test_case)
        except Exception as e:
            raise ValueError(f"Invalid test case at index {idx}: {e}")

    return test_cases
