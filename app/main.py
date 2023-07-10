from fastapi import Depends, FastAPI

from app.api.api_v1.api import api_router
from app.core.admin_panel import setup_admin
from app.core.settings import settings
from app.db.session import engine, get_async_session

app = FastAPI(
    title="My Simple Car", openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

setup_admin(app, engine)

app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_async_session)],
)
