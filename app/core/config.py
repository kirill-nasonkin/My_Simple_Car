import os

from dotenv import load_dotenv

load_dotenv()

POSTGRES_USER = os.environ.get("POSTGRES_USER")
POSTGRES_PASSWORD = os.environ.get("POSTGRES_PASSWORD")
POSTGRES_DB = os.environ.get("POSTGRES_DB")
POSTGRES_SERVER = os.environ.get("POSTGRES_SERVER")

SQLALCHEMY_DATABASE_URI = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_SERVER}/{POSTGRES_DB}?async_fallback=True"

# import secrets
# from functools import lru_cache
# from typing import Any, Dict, List, Optional, Union
#
# from pydantic import (
#     AnyHttpUrl,
#     BaseSettings,
#     PostgresDsn,
#     validator,
# )
#
#
# class Settings(BaseSettings):
#     API_V1_STR: str = "/api/v1"
#     SECRET_KEY: str = secrets.token_urlsafe(32)
#     # 60 minutes * 24 hours * 8 days = 8 days
#     ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
#
#     # BACKEND_CORS_ORIGINS is a JSON-formatted list of origins
#     # e.g: '["http://localhost", "http://localhost:4200",
#     # "http://localhost:3000", "http://localhost:8080"]'
#     BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
#
#     @validator("BACKEND_CORS_ORIGINS", pre=True)
#     def assemble_cors_origins(
#         cls, v: Union[str, List[str]]
#     ) -> Union[List[str], str]:
#         if isinstance(v, str) and not v.startswith("["):
#             return [i.strip() for i in v.split(",")]
#         elif isinstance(v, (list, str)):
#             return v
#         raise ValueError(v)
#
#     POSTGRES_SERVER: str
#     POSTGRES_USER: str
#     POSTGRES_PASSWORD: str
#     POSTGRES_DB: str
#     SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None
#     #
#     # @validator("SQLALCHEMY_DATABASE_URI", pre=True)
#     # def assemble_db_connection(
#     #     cls, v: Optional[str], values: Dict[str, Any]
#     # ) -> Any:
#     #     if isinstance(v, str):
#     #         return v
#     #     return PostgresDsn.build(
#     #         scheme="postgresql+asyncpg",
#     #         user=values.get("POSTGRES_USER"),
#     #         password=values.get("POSTGRES_PASSWORD"),
#     #         host=values.get("POSTGRES_SERVER"),
#     #         path=f"/{values.get('POSTGRES_DB') or ''}",
#     #     )
#
#     # SMTP_HOST: Optional[str] = None
#     # SMTP_PORT: Optional[int] = None
#     # SMTP_USER: Optional[str] = None
#     # SMTP_PASSWORD: Optional[str] = None
#
#     class Config:
#         case_sensitive = True
#         env_file = ".env"
#
#
# @lru_cache
# def get_settings() -> Settings:
#     return Settings()


# settings = get_settings()
