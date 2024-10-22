import os
from dotenv import load_dotenv
from anthropic import Anthropic
from .base import LLMProvider

class AnthropicProvider(LLMProvider):
    def __init__(self, model_id="claude-3-opus-20240229"):
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
        self.model_id = model_id

    def get_completion(self, prompt: str) -> str:
        response = self.client.messages.create(
            model=self.model_id,
            max_tokens=10,
            temperature=0.2,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.content[0].text