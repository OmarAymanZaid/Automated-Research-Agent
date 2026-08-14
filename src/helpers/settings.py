from __future__ import annotations
from functools import lru_cache
from typing import Literal
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "Automated Research Agent"
    ENVIRONMENT: Literal["local", "staging", "production"] = "local"
    LOG_LEVEL: str = "INFO"

    # Generation Specs
    GENERATION_PROVIDER: str = "OPENAI"
    GENERATION_MODEL_NAME: str = "gpt-4o-mini"
    GENERATION_DEFAULT_MAX_TOKENS: int = 200
    GENERATION_DEFAULT_TEMPERATURE: float = 0.1

    # API Keys
    GOOGLE_API_KEY: str | None = None

    @property
    def is_local(self) -> bool:
        return self.ENVIRONMENT == "local"

@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()
