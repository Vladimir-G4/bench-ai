# benchai/adapters/openai.py

import openai
from typing import Callable

def openai_adapter(api_key: str, model_name: str = "gpt-4") -> Callable[[str], str]:
    openai.api_key = api_key

    def model(prompt: str) -> str:
        response = openai.ChatCompletion.create(
            model=model_name,
            messages=[{"role": "user", "content": prompt}],
            temperature=0
        )
        return response['choices'][0]['message']['content'].strip()

    return model