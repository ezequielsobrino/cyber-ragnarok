from enum import Enum

class LLMProviderType(Enum):
    GROQ = "groq"
    ANTHROPIC = "anthropic"

# Default settings
DEFAULT_GROQ_MODEL = "llama-3.1-70b-versatile"
DEFAULT_ANTHROPIC_MODEL = "claude-3-opus-20240229"