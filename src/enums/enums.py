from enum import Enum

class ModelProvider(str, Enum):
    OPENAI = "OPENAI"

class ModelTier(str, Enum):
    FAST = "fast"
    REASONING = "reasoning"
