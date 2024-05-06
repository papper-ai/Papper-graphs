import logging

from pydantic_settings import BaseSettings

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class Settings(BaseSettings):
    batch_size: int = 8

    class Config:
        extra = "ignore"


settings = Settings()
logging.info(f"Using batch size of {settings.batch_size}")
