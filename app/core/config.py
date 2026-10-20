from functools import lru_cache
from pathlib import Path

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from sqlalchemy.engine import make_url

# project root
PROJECT_ROOT = Path(__file__).resolve().parents[2]


# settings
class Settings(BaseSettings):
    """Application configuration loaded from environment variables or .env"""

    # Pydantic settings configuration
    model_config = SettingsConfigDict(
        env_file=PROJECT_ROOT / ".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # application settings
    app_name: str = Field(default="User Management API", min_length=1)
    debug: bool = False
    database_url: str = Field(min_length=1)

    # validate database_url
    @field_validator("database_url")
    @classmethod
    def validate_database_url(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("DATABASE_URL must not be empty")

        try:
            parsed_url = make_url(value)
        except Exception as exc:
            raise ValueError("DATABASE_URL is not a valid SQLAlchemy URL") from exc

        supported_drivers = {
            "sqlite",
            "postgresql",
            "postgresql+psycopg",
            "postgresql+psycopg2",
        }

        if parsed_url.drivername not in supported_drivers:
            raise ValueError(
                "DATABASE_URL must use SQLite or a supported PostgreSQL driver"
            )

        if parsed_url.drivername == "sqlite" and not parsed_url.database:
            raise ValueError("SQLite DATABASE_URL must specify a database")

        return value


# lru_cache for settings
@lru_cache
def get_settings() -> Settings:
    """Create settings once and reuse them throughout the application."""
    return Settings()
