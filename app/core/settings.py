import secrets
from functools import lru_cache
from pathlib import Path

from fastapi_storages import FileSystemStorage
from pydantic import (
    AnyHttpUrl,
    PostgresDsn,
    field_validator,
)
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")
    API_V1_STR: str = "/api/v1"
    USERS_OPEN_REGISTRATION: bool = True
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STORAGE: FileSystemStorage = FileSystemStorage(
        path=str(BASE_DIR / "static")
    )
    SECRET_KEY: str = secrets.token_urlsafe(32)
    PASSWORD_MIN_LENGTH: int = 8
    # 3600 seconds * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_SECONDS: int = 3600 * 24 * 8

    # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200"]'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
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

    REDIS_SERVER: str

    SMTP_HOST: str | None = None
    SMTP_PORT: int | None = None
    # SMTP_USER: Optional[str] = None
    # SMTP_PASSWORD: Optional[str] = None


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
