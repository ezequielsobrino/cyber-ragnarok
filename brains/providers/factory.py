class ProviderFactory:
    def create_provider(self, model_id: str):
        if "claude" in model_id.lower():
            from brains.providers.anthropic_provider import AnthropicProvider
            return AnthropicProvider(model_id=model_id)
        elif "llama" in model_id.lower():
            from brains.providers.groq_provider import GroqProvider
            return GroqProvider(model_id=model_id)
        else:
            raise ValueError(f"Unknown model type: {model_id}")