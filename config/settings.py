from enum import Enum
from dataclasses import dataclass
from typing import Dict, List

class GameType(Enum):
    TIC_TAC_TOE = "tic_tac_toe"
    CHECKERS = "checkers"

class LLMProviderType(Enum):
    GROQ = "groq"
    ANTHROPIC = "anthropic"
    OPENAI = "openai"

@dataclass
class ModelPricing:
    input_cost: float  # Cost per million tokens
    output_cost: float  # Cost per million tokens

class ModelConfig:
    # Default models for each provider
    DEFAULT_GROQ_MODEL = "llama-3.1-70b-versatile"
    DEFAULT_ANTHROPIC_MODEL = "claude-3-haiku-20240307"
    
    # Model pricing configuration (costs per million tokens)
    MODEL_PRICING: Dict[str, ModelPricing] = {
        # Groq models
        "llama-3.1-70b-versatile": ModelPricing(0.00059, 0.00079),
        "llama-3.1-8b-instant": ModelPricing(0.00005, 0.00008),
        
        # Anthropic models
        "claude-3-haiku-20240307": ModelPricing(0.50, 0.50),
        "claude-3-5-sonnet-20241022": ModelPricing(2.00, 2.00),
        "claude-3-5-sonnet-20240620": ModelPricing(2.00, 2.00),
        "claude-3-opus-20240229": ModelPricing(3.00, 3.00),
        
        # OpenAI models
        "gpt-4o-mini": ModelPricing(0.30, 1.20),
        "gpt-4o": ModelPricing(3.75, 15.00),
        "o1-mini": ModelPricing(0.50, 0.50),
        "o1-preview": ModelPricing(0.50, 0.50)
    }
    
    # Available models
    AVAILABLE_MODELS = {
        LLMProviderType.GROQ: [
            "llama-3.1-70b-versatile",
            "llama-3.1-8b-instant",
        ],
        LLMProviderType.ANTHROPIC: [
            "claude-3-haiku-20240307",
            "claude-3-5-sonnet-20241022",
            "claude-3-5-sonnet-20240620",
            "claude-3-opus-20240229"
        ],
        LLMProviderType.OPENAI: [
            "gpt-4o-mini",
            "gpt-4o",
            "o1-mini",
            "o1-preview"
        ]
    }
    
    @classmethod
    def get_model_pricing(cls, model_name: str) -> ModelPricing:
        """Get the pricing configuration for a specific model"""
        if model_name not in cls.MODEL_PRICING:
            raise ValueError(f"Unknown model: {model_name}")
        return cls.MODEL_PRICING[model_name]

class MatchConfig:
    def __init__(self):
        # Game configuration
        self.GAME_TYPE = GameType.TIC_TAC_TOE
        
        # Match participants
        self.MODEL1_NAME = "llama-3.1-70b-versatile"
        self.MODEL2_NAME = "llama-3.1-8b-instant"
        
        # Match settings
        self.NUM_GAMES = 3
        
        # Provider information
        self._set_provider_info()
    
    def _set_provider_info(self):
        """Determine the provider type for each model"""
        self.MODEL1_PROVIDER = self._get_provider_type(self.MODEL1_NAME)
        self.MODEL2_PROVIDER = self._get_provider_type(self.MODEL2_NAME)
    
    def _get_provider_type(self, model_name: str) -> LLMProviderType:
        """Determine the provider type based on the model name"""
        for provider, models in ModelConfig.AVAILABLE_MODELS.items():
            if model_name in models:
                return provider
        raise ValueError(f"Unknown model: {model_name}")

class VideoConfig:
    WIDTH = 1280
    HEIGHT = 720
    FPS = 30
    INTRO_DURATION = 5
    ROUND_INTRO_DURATION = 3
    WINNER_ANNOUNCEMENT_DURATION = 5
    MOVE_DURATION = 0.5
    END_GAME_DURATION = 2