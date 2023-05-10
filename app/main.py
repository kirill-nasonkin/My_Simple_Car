from fastapi import FastAPI

from app.core.config import settings

app = FastAPI(
    title="My Simple Car", openapi_url=f"{settings.API_V1_STR}/openapi.json"
)
