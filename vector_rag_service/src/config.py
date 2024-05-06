from pathlib import Path

from openai import AsyncClient
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    url_to_llm: str
    url_to_embeddings: str
    _llm_client = None

    @property
    def openai_client(self) -> AsyncClient:
        return self._llm_client

    @openai_client.setter
    def openai_client(self, value):
        self._llm_client = value

    class Config:
        extra = "ignore"


settings = Settings()

openai_client = AsyncClient(base_url=settings.url_to_llm, api_key="password")
settings.openai_client = openai_client
