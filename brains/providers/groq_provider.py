import os
from dotenv import load_dotenv
from groq import Groq
from .base import LLMProvider

class GroqProvider(LLMProvider):
    def __init__(self, model_id="llama-3.1-70b-versatile"):
        load_dotenv()
        self.client = Groq(api_key=os.getenv("GROQ_API_KEY"))
        self.model_id = model_id

    def get_completion(self, prompt: str) -> str:
        response = self.client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=self.model_id,
            temperature=0.2,
            max_tokens=10,
        )
        return response.choices[0].message.content.strip()