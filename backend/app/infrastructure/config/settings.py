"""Application settings loaded from environment variables."""

from functools import lru_cache
from typing import Annotated, Any

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, NoDecode, SettingsConfigDict


class Settings(BaseSettings):
    """Central configuration for the backend application.

    Attributes:
        app_name: Application display name.
        app_env: Runtime environment (development, staging, production).
        debug: Enable debug mode and API docs.
        log_level: Logging verbosity level.
        database_url: Async SQLAlchemy connection URL.
        database_url_sync: Sync connection URL for Alembic.
        cors_origins: Allowed CORS origin URLs.
        smtp_host: SMTP server hostname.
        smtp_port: SMTP server port.
        smtp_from: Default sender email address.
        storage_local_path: Local filesystem storage root path.
    """

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    app_name: str = Field(default="naviera-docs", alias="APP_NAME")
    app_env: str = Field(default="development", alias="APP_ENV")
    debug: bool = Field(default=True, alias="DEBUG")
    log_level: str = Field(default="INFO", alias="LOG_LEVEL")

    database_url: str = Field(
        default="sqlite+aiosqlite:///./data/naviera.db",
        alias="DATABASE_URL",
    )
    database_url_sync: str = Field(
        default="sqlite:///./data/naviera.db",
        alias="DATABASE_URL_SYNC",
    )
    inbox_path: str = Field(default="./data/inbox", alias="INBOX_PATH")
    use_console_notifier: bool = Field(default=True, alias="USE_CONSOLE_NOTIFIER")

    # NoDecode: evita que pydantic-settings interprete el env como JSON (falla con CSV).
    cors_origins: Annotated[list[str], NoDecode] = Field(
        default=["http://localhost:5173"],
        alias="CORS_ORIGINS",
    )

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, value: Any) -> list[str]:
        """Parse comma-separated CORS origins from environment variables."""
        if isinstance(value, str):
            return [origin.strip() for origin in value.split(",") if origin.strip()]
        if isinstance(value, list):
            return value
        return ["http://localhost:5173"]

    smtp_host: str = Field(default="mailhog", alias="SMTP_HOST")
    smtp_port: int = Field(default=1025, alias="SMTP_PORT")
    smtp_user: str = Field(default="", alias="SMTP_USER")
    smtp_password: str = Field(default="", alias="SMTP_PASSWORD")
    smtp_from: str = Field(default="noreply@naviera.local", alias="SMTP_FROM")
    smtp_use_tls: bool = Field(default=False, alias="SMTP_USE_TLS")

    public_api_url: str = Field(
        default="http://localhost:8000",
        alias="PUBLIC_API_URL",
    )
    approval_token_secret: str = Field(
        default="naviera-dev-approval-secret-change-me",
        alias="APPROVAL_TOKEN_SECRET",
    )
    approval_token_max_age_days: int = Field(
        default=7,
        alias="APPROVAL_TOKEN_MAX_AGE_DAYS",
    )

    storage_type: str = Field(default="local", alias="STORAGE_TYPE")
    storage_local_path: str = Field(default="/app/storage", alias="STORAGE_LOCAL_PATH")
    storage_max_upload_mb: int = Field(default=50, alias="STORAGE_MAX_UPLOAD_MB")


@lru_cache
def get_settings() -> Settings:
    """Return cached application settings singleton.

    Returns:
        Loaded Settings instance.
    """
    return Settings()
