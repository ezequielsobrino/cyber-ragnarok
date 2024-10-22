from typing import Dict, Type
from .base import LLMProvider
from .groq_provider import GroqProvider
from .anthropic_provider import AnthropicProvider
from config.settings import LLMProviderType

class LLMProviderFactory:
    _providers: Dict[LLMProviderType, Type[LLMProvider]] = {
        LLMProviderType.GROQ: GroqProvider,
        LLMProviderType.ANTHROPIC: AnthropicProvider
    }

    @classmethod
    def create(cls, provider_type: LLMProviderType, **kwargs) -> LLMProvider:
        """
        Create a new LLM provider instance.
        
        Args:
            provider_type: Type of provider to create
            **kwargs: Additional arguments to pass to the provider constructor
        
        Returns:
            LLMProvider: Instance of the requested provider
            
        Raises:
            ValueError: If provider_type is not supported
        """
        provider_class = cls._providers.get(provider_type)
        if not provider_class:
            raise ValueError(f"Unknown provider type: {provider_type}")
        
        return provider_class(**kwargs)

    @classmethod
    def register_provider(cls, provider_type: LLMProviderType, provider_class: Type[LLMProvider]) -> None:
        """
        Register a new provider type.
        
        Args:
            provider_type: Enum value for the provider type
            provider_class: Class that implements LLMProvider
        """
        cls._providers[provider_type] = provider_class