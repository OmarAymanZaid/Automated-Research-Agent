from enum import Enum

class ModelProvider(str, Enum):
    OPENAI = "OPENAI"
    GOOGLE = "GOOGLE"


class ModelTier(str, Enum):
    FAST = "fast"
    REASONING = "reasoning"

