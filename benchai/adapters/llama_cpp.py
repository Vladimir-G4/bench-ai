# benchai/adapters/llama_cpp.py

from llama_cpp import Llama
from typing import Callable

def llama_cpp_adapter(model_path: str) -> Callable[[str], str]:
    llm = Llama(model_path=model_path)

    def model(prompt: str) -> str:
        output = llm(prompt, max_tokens=200)
        return output["choices"][0]["text"].strip()

    return model