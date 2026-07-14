"""
Central application settings.

All secrets and environment-specific values must come from environment
variables (or a local .env file in development) — never hardcoded here.
See .env.example for the full list of supported variables.
"""
from functools import lru_cache

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    # --- App ---
    app_name: str = "My Supplier"
    app_env: str = "development"
    secret_key: str = "change-me-to-a-random-secret"
    debug: bool = True

    # --- Database ---
    database_url: str = "sqlite:///./data/my_supplier.db"

    # --- Business defaults (user-editable via Settings screen; these are fallbacks) ---
    default_budget: float = 0
    min_roi_percent: float = 20
    min_profit_amount: float = 3
    default_shipping_cost: float = 0
    default_packaging_cost: float = 0
    default_returns_allowance_percent: float = 2
    default_marketplace_fee_percent: float = 12.8

    # --- Marketplace API credentials (integration points) ---
    ebay_client_id: str = ""
    ebay_client_secret: str = ""
    ebay_env: str = "sandbox"
    amazon_sp_api_client_id: str = ""
    amazon_sp_api_client_secret: str = ""
    amazon_sp_api_refresh_token: str = ""
    amazon_marketplace_id: str = ""

    # --- Notifications (integration points) ---
    smtp_host: str = ""
    smtp_port: int = 587
    smtp_user: str = ""
    smtp_password: str = ""
    telegram_bot_token: str = ""
    discord_webhook_url: str = ""

    @property
    def is_production(self) -> bool:
        return self.app_env.lower() == "production"


@lru_cache
def get_settings() -> Settings:
    return Settings()
