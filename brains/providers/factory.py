from .groq_provider import GroqProvider
from .anthropic_provider import AnthropicProvider
from config.settings import LLMProviderType

class ProviderFactory:
    def create_provider(self, model_name: str, provider_type: LLMProviderType):
        """
        Create a provider instance based on the provider type and model name.
        
        Args:
            model_name (str): Name of the model to use
            provider_type (LLMProviderType): Type of the provider (GROQ or ANTHROPIC)
            
        Returns:
            Provider instance configured with the specified model
        """
        if provider_type == LLMProviderType.GROQ:
            return GroqProvider(model_name)
        elif provider_type == LLMProviderType.ANTHROPIC:
            return AnthropicProvider(model_name)
        else:
            raise ValueError(f"Unsupported provider type: {provider_type}")