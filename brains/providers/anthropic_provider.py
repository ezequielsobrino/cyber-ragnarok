from anthropic import Anthropic
from dotenv import load_dotenv
import os
from .base import LLMProvider

class AnthropicProvider(LLMProvider):
    def __init__(self, model_id: str):
        super().__init__(model_id)
        load_dotenv()
        self.client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

    def _make_api_call(self, prompt: str) -> tuple[str, dict]:
        message = self.client.messages.create(
            model=self.model_id,
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        
        return message.content[0].text, {
            'input_tokens': message.usage.input_tokens,
            'output_tokens': message.usage.output_tokens,
            'total_tokens': message.usage.input_tokens + message.usage.output_tokens
        }