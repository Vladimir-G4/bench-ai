# benchai/adapters/rest.py

import requests
from typing import Callable

def rest_adapter(url: str, headers: dict = None, payload_key: str = "prompt", response_key: str = "response") -> Callable[[str], str]:
    def model(prompt: str) -> str:
        payload = {payload_key: prompt}
        response = requests.post(url, json=payload, headers=headers or {})
        response.raise_for_status()
        return response.json()[response_key].strip()

    return model