# benchai/adapters/huggingface.py

from transformers import pipeline
from typing import Callable

def hf_adapter(model_name: str = "gpt2") -> Callable[[str], str]:
    pipe = pipeline("text-generation", model=model_name)

    def model(prompt: str) -> str:
        outputs = pipe(prompt, max_length=200, do_sample=False)
        return outputs[0]["generated_text"].strip()

    return model