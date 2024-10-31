from .base import LLMProvider
from .groq_provider import GroqProvider
from .anthropic_provider import AnthropicProvider
from .openai_provider import OpenAIProvider
from config.settings import LLMProviderType

class ProviderFactory:
    def create_provider(self, model_name: str, provider_type: LLMProviderType) -> LLMProvider:
        """
        Create a provider instance based on the provider type and model name.
        
        Args:
            model_name (str): Name of the model to use
            provider_type (LLMProviderType): Type of the provider (GROQ, ANTHROPIC, or OPENAI)
            
        Returns:
            Provider instance configured with the specified model
        """
        if provider_type == LLMProviderType.GROQ:
            return GroqProvider(model_name)
        elif provider_type == LLMProviderType.ANTHROPIC:
            return AnthropicProvider(model_name)
        elif provider_type == LLMProviderType.OPENAI:
            return OpenAIProvider(model_name)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")