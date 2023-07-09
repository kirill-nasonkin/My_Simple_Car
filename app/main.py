from fastapi import Depends, FastAPI

from app.api.api_v1.api import api_router
from app.auth.config import auth_backend, fastapi_users
from app.core.admin_panel import setup_admin
from app.core.settings import settings
from app.db.session import engine, get_async_session
from app.schemas.users import UserCreate, UserRead, UserUpdate

app = FastAPI(
    title="My Simple Car", openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

setup_admin(app, engine)

app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    prefix="/users",
    tags=["Users"],
)

app.include_router(
    api_router,
    prefix=settings.API_V1_STR,
    dependencies=[Depends(get_async_session)],
)
