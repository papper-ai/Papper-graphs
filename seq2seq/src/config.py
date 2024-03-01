from pathlib import Path
import logging

from pydantic_settings import BaseSettings

logging.basicConfig(
        format="%(asctime)s - %(levelname)s - %(message)s",
        level=logging.INFO,
    )

BASE_DIR = Path(__file__).parent


class Settings(BaseSettings):
    lm_mode: str = None

    class Config:
        extra = "ignore"


settings = Settings()
