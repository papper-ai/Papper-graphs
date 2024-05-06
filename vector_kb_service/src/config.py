from pathlib import Path

import openai
from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    URL_TO_EMBEDDINGS: str

    _openai_client = None

    @property
    def openai_client(self) -> openai.AsyncClient:
        return self._openai_client

    @openai_client.setter
    def openai_client(self, value):
        self._openai_client = value

    class Config:
        extra = "ignore"


settings = Settings()
settings.openai_client = openai.AsyncClient(
    base_url=settings.URL_TO_EMBEDDINGS, api_key="no-password"
)
