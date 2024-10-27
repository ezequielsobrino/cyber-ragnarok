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
        params = {
            "model": self.model_id,
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ]
        }
        
        # Solo agregamos el parámetro de tokens si NO es uno de los modelos preview
        if self.model_id not in ["o1-mini"]:
            params["max_tokens"] = 10
            params["temperature"] = 0.7
        
        response = self.client.chat.completions.create(**params)
        return response.choices[0].message.content