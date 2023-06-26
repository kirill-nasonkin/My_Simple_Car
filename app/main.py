from fastapi import FastAPI

from app.core.admin_panel import setup_admin
from app.core.config import settings
from app.db.session import engine

app = FastAPI(title="My Simple Car", openapi_url=f"{settings.API_V1_STR}/openapi.json")
setup_admin(app, engine)
