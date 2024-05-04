from pydantic_settings import BaseSettings
from openai import AsyncClient


class Settings(BaseSettings):
    _llm_client = None

    @property
    def openai_client(self) -> AsyncClient:
        return self._llm_client

    @openai_client.setter
    def openai_client(self, value):
        self._llm_client = value


settings = Settings()

openai_client = AsyncClient(base_url="http://localhost:8101/v1", api_key="password")
settings.openai_client = openai_client
