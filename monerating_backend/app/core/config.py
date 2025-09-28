from functools import lru_cache
from pydantic import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Monerating API"
    APP_ENV: str = "dev"
    DATABASE_URL: str = "sqlite:///./monerating.db"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings() -> "Settings":
    return Settings()


settings = get_settings()

