import logging
from functools import lru_cache
from pydantic import BaseSettings


logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

logger = logging.getLogger(__name__)


class _Settings(BaseSettings):
    db_dsn: str

    enable_auth: bool = False

    telegram_api_token: str

    class Config:
        env_file = "envs/main.env"


@lru_cache
def _get_settings() -> _Settings:
    return _Settings()


settings = _get_settings()
