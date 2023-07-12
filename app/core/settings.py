from functools import lru_cache
from pathlib import Path

from fastapi_storages import FileSystemStorage
from pydantic import (
    AnyHttpUrl,
    EmailStr,
    PostgresDsn,
    field_validator,
)
from pydantic_core.core_schema import FieldValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(case_sensitive=True, env_file=".env")

    PROJECT_NAME: str = "My Simple Car"
    API_V1_STR: str = "/api/v1"
    SERVER_HOST: str = "blabla_my_future_domain"  # emails

    # DIRS
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    STORAGE: FileSystemStorage = FileSystemStorage(
        path=str(BASE_DIR / "static")
    )

    # SECURITY
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    PASSWORD_MIN_LENGTH: int = 8
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    USERS_OPEN_REGISTRATION: bool = True
    # BACKEND_CORS_ORIGINS - a JSON-formatted list of origins
    # e.g: '["http://localhost", "http://localhost:4200"]'
    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    # DATABASE
    POSTGRES_SERVER: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SQLALCHEMY_DATABASE_URI: PostgresDsn | None = None

    # REDIS
    REDIS_SERVER: str

    # EMAILS
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None
    EMAILS_FROM_EMAIL: EmailStr | None = None
    EMAILS_FROM_NAME: str | None = None
    EMAIL_RESET_TOKEN_EXPIRE_HOURS: int = 48
    EMAILS_ENABLED: bool = False
    EMAIL_TEMPLATES_DIR: str = str(BASE_DIR / "email-templates" / "build")

    # VALIDATORS
    @field_validator("EMAILS_ENABLED", mode="before")
    def get_emails_enabled(cls, v, info: FieldValidationInfo) -> bool:
        return bool(
            info.data.get("SMTP_HOST")
            and info.data.get("SMTP_PORT")
            and info.data.get("EMAILS_FROM_EMAIL")
        )

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
