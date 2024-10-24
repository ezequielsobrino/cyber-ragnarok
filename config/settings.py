from enum import Enum

class LLMProviderType(Enum):
    GROQ = "groq"
    ANTHROPIC = "anthropic"

# Default settings
DEFAULT_GROQ_MODEL = "llama-3.1-70b-versatile"
DEFAULT_ANTHROPIC_MODEL = "claude-3-opus-20240229"


# llama-3.1-70b-versatile
# claude-3-haiku-20240307
# claude-3-5-sonnet-20241022

class TournamentConfig:
    def __init__(self):
        self.MODEL1_NAME = "claude-3-5-sonnet-20241022"
        self.MODEL2_NAME = "claude-3-5-sonnet-20240620"
        self.NUM_GAMES = 10