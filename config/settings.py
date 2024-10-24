# config/settings.py
from enum import Enum

class LLMProviderType(Enum):
    GROQ = "groq"
    ANTHROPIC = "anthropic"

class ModelConfig:
    # Default models for each provider
    DEFAULT_GROQ_MODEL = "llama-3.1-70b-versatile"
    DEFAULT_ANTHROPIC_MODEL = "claude-3-haiku-20240307"
    
    # Available models
    AVAILABLE_MODELS = {
        LLMProviderType.GROQ: [
            "llama-3.1-70b-versatile"
        ],
        LLMProviderType.ANTHROPIC: [
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229"
        ]
    }

class MatchConfig:
    def __init__(self):
        # Match participants
        self.MODEL1_NAME = "llama-3.1-70b-versatile"
        self.MODEL2_NAME = "llama-3.1-70b-versatile"
        
        # Match settings
        self.NUM_GAMES = 10
        
        # Provider information
        self._set_provider_info()
    
    def _set_provider_info(self):
        """Determine the provider type for each model"""
        self.MODEL1_PROVIDER = self._get_provider_type(self.MODEL1_NAME)
        self.MODEL2_PROVIDER = self._get_provider_type(self.MODEL2_NAME)
    
    def _get_provider_type(self, model_name: str) -> LLMProviderType:
        """Determine the provider type based on the model name"""
        if any(model_name in models for models in ModelConfig.AVAILABLE_MODELS[LLMProviderType.GROQ]):
            return LLMProviderType.GROQ
        elif any(model_name in models for models in ModelConfig.AVAILABLE_MODELS[LLMProviderType.ANTHROPIC]):
            return LLMProviderType.ANTHROPIC
        else:
            raise ValueError(f"Unknown model: {model_name}")

# Video rendering settings can be moved to a separate config if needed
class VideoConfig:
    WIDTH = 1280
    HEIGHT = 720
    FPS = 30
    INTRO_DURATION = 5
    ROUND_INTRO_DURATION = 3
    WINNER_ANNOUNCEMENT_DURATION = 5
    MOVE_DURATION = 0.5
    END_GAME_DURATION = 2