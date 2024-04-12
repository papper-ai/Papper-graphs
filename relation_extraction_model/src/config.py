import logging

from pydantic_settings import BaseSettings

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)


class Settings(BaseSettings):
    batch_size: int = 8
    use_cuda: bool = True

    class Config:
        extra = "ignore"


settings = Settings()
