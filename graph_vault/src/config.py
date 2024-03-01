from pathlib import Path

from pydantic_settings import BaseSettings

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    neo4j_user: str = "neo4j"
    neo4j_password: str

    @property
    def neo4j_uri(self) -> str:
        return "bolt://neo4j:7687"

    class Config:
        extra = "ignore"


settings = Settings()
