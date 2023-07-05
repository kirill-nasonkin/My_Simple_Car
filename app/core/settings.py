import secrets
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    PostgresDsn,
    validator,
)


class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STORAGE: Path = BASE_DIR / "static"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PASSWORD_MIN_LENGTH: int = 8
    # 3600 seconds * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200"]'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(
        cls, v: str | None, values: dict[str, Any]
    ) -> Any:
        if isinstance(v, str):
            return v
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            user=values.get("POSTGRES_USER"),
            password=values.get("POSTGRES_PASSWORD"),
            host=values.get("POSTGRES_SERVER"),
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )

    REDIS_SERVER: str

    # SMTP_HOST: Optional[str] = None
    # SMTP_PORT: Optional[int] = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None

    class Config:
        case_sensitive = True
        env_file = ".env"


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
