from openai import OpenAI
from dotenv import load_dotenv
import os
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, model_id: str):
        super().__init__(model_id)
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

    def _make_api_call(self, prompt: str) -> tuple[str, dict]:
        completion = self.client.chat.completions.create(
            model=self.model_id,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return completion.choices[0].message.content, {
            'input_tokens': completion.usage.prompt_tokens,
            'output_tokens': completion.usage.completion_tokens,
            'total_tokens': completion.usage.total_tokens
        }