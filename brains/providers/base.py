from dataclasses import dataclass
from time import time
from typing import Optional
from abc import ABC, abstractmethod
from contextlib import contextmanager
from config.settings import ModelConfig

@dataclass
class LLMResponse:
    content: str
    input_tokens: int
    output_tokens: int
    total_tokens: int
    cost: float
    response_time: float

class LLMProvider(ABC):
    def __init__(self, model_id: str):
        # Configure pricing based on model
        pricing = ModelConfig.get_model_pricing(model_id)
        self.cost_per_token_input = pricing.input_cost / 1_000_000
        self.cost_per_token_output = pricing.output_cost / 1_000_000
        self.model_id = model_id

    @contextmanager
    def _measure_time(self):
        """Context manager to measure execution time"""
        start_time = time()
        try:
            yield
        finally:
            self.last_response_time = round(time() - start_time, 3)

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        input_cost = input_tokens * self.cost_per_token_input
        output_cost = output_tokens * self.cost_per_token_output
        return input_cost + output_cost
    
    def get_completion(self, prompt: str) -> LLMResponse:
        """
        Template method that handles timing and response creation.
        Subclasses should implement _make_api_call instead of this method.
        """
        with self._measure_time():
            content, usage = self._make_api_call(prompt)
        
        return LLMResponse(
            content=content,
            input_tokens=usage.get('input_tokens', 0),
            output_tokens=usage.get('output_tokens', 0),
            total_tokens=usage.get('total_tokens', 0),
            cost=self._calculate_cost(
                usage.get('input_tokens', 0), 
                usage.get('output_tokens', 0)
            ),
            response_time=self.last_response_time
        )

    @abstractmethod
    def _make_api_call(self, prompt: str) -> tuple[str, dict]:
        """
        Make the actual API call to the LLM provider.
        Returns a tuple of (content, usage_dict)
        usage_dict should contain input_tokens, output_tokens, and total_tokens
        """
        pass