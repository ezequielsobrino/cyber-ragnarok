from abc import ABC, abstractmethod

class LLMProvider(ABC):
    @abstractmethod
    def get_completion(self, prompt: str) -> str:
        """Get completion from LLM provider"""
        pass