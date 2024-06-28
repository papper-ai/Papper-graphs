import logging
from pathlib import Path

from pydantic_settings import BaseSettings

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    neo4j_user: str = "neo4j"
    neo4j_host: str = "neo4j"
    neo4j_password: str
    remote_url: str = "http://host.docker.internal:8003"

    @property
    def neo4j_uri(self) -> str:
        return f"bolt://{self.neo4j_host}:7687"

    class Config:
        extra = "ignore"


settings = Settings()
