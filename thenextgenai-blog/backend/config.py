import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Database
    database_url: str = os.getenv("DATABASE_URL", "postgresql://postgres:password@localhost/thenextgenai")

    # Security
    secret_key: str = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
    jwt_secret: str = os.getenv("JWT_SECRET", "dev-jwt-secret-change-in-production")
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    refresh_token_expiration_days: int = 7

    # Email
    email_provider: str = os.getenv("EMAIL_PROVIDER", "sendgrid")
    sendgrid_api_key: str = os.getenv("SENDGRID_API_KEY", "")
    from_email: str = os.getenv("FROM_EMAIL", "editorial@thenextgenai.com")

    # Frontend
    frontend_url: str = os.getenv("FRONTEND_URL", "http://localhost:3000")
    cors_origins: list = ["http://localhost:3000", "https://thenextgenai.com"]

    # Analytics
    analytics_enabled: bool = os.getenv("ANALYTICS_ENABLED", "true").lower() == "true"

    # Trending
    trending_recalc_hours: int = 6
    trending_min_views: int = 10
    trending_date_range_days: int = 7

    # Pagination
    default_page_size: int = 20
    max_page_size: int = 100

    # Caching (in seconds)
    cache_trending_ttl: int = 6 * 3600
    cache_author_ttl: int = 24 * 3600
    cache_search_ttl: int = 3600

    # Environment
    environment: str = os.getenv("ENVIRONMENT", "development")
    debug: bool = environment == "development"

    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()
