from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Environment-driven application configuration.

    Defaults target local development (SQLite). Production sets DATABASE_URL to a
    PostgreSQL DSN and all credentials via environment variables — never hardcoded.
    """

    app_name: str = "My Supplier"
    environment: str = "development"
    database_url: str = "sqlite:///./advancestay.db"

    model_config = SettingsConfigDict(env_file=".env", env_prefix="", extra="ignore")


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
