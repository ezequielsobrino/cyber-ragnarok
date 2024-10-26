import os
from dotenv import load_dotenv
from openai import OpenAI
from .base import LLMProvider

class OpenAIProvider(LLMProvider):
    def __init__(self, model_id="gpt-4o-mini"):
        load_dotenv()
        self.client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        self.model_id = model_id

    def get_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            model=self.model_id,
            max_tokens=10,
            temperature=0.7,
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        )
        return response.choices[0].message.content