from langchain_core.embeddings import Embeddings
from langchain_core.language_models.chat_models import BaseChatModel
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from loguru import logger

from src.helpers.settings import Settings
from src.enums.enums import ModelProvider

class LLMProviderFactory:

    def __init__(self, config: Settings):
        self.config = config

    def create_llm(
        self,
        provider: str | None = None,
        temperature: float | None = None,
        max_tokens: int | None = None,
    ) -> BaseChatModel:
        provider = provider or self.config.GENERATION_PROVIDER
        temp = (
            temperature
            if temperature is not None
            else self.config.GENERATION_DEFAULT_TEMPERATURE
        )
        tokens = (
            max_tokens
            if max_tokens is not None
            else self.config.GENERATION_DEFAULT_MAX_TOKENS
        )

        if provider == ModelProvider.OPENAI.value:
            return ChatOpenAI(
                model=self.config.GENERATION_MODEL_NAME,
                api_key=self.config.OPENAI_API_KEY,
                base_url=self.config.OPENAI_API_URL or None,
                temperature=temp,
                max_tokens=tokens,
            )

        if provider == ModelProvider.GOOGLE.value:
            return ChatGoogleGenerativeAI(
                model=self.config.GENERATION_MODEL_NAME,
                temperature=temp,
                max_tokens=tokens,
                api_key=self.config.GOOGLE_API_KEY
            )

        logger.error(f"Unsupported LLM provider: {provider}")
        raise ValueError(f"Provider '{provider}' is not supported.")

    def create_embedding_model(
        self, provider: str | None = None
    ) -> Embeddings:
        provider = provider or self.config.EMBEDDING_PROVIDER

        if provider == ModelProvider.OPENAI.value:
            return OpenAIEmbeddings(
                model=self.config.EMBEDDING_MODEL_NAME,
                api_key=self.config.OPENAI_API_KEY,
                base_url=self.config.OPENAI_API_URL or None,
            )

        if provider == ModelProvider.GOOGLE.value:
            return GoogleGenerativeAIEmbeddings(
                model=self.config.EMBEDDING_MODEL_NAME,
                api_key=self.config.GOOGLE_API_KEY
            )

        logger.error(f"Unsupported Embedding provider: {provider}")
        raise ValueError(f"Provider '{provider}' is not supported.")
